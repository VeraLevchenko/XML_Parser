import xml.etree.ElementTree as ET
import os

# функция возвращает список .xml файлов из папки, включая подпапки, кроме proto_.xml
def get_file_list(path):
    filelist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".xml") and file != "proto_.xml":
                filelist.append(os.path.join(root, file))
    # print(filelist)  #  Проверка пути!!!!!!!!!!!!!!!!
    return filelist


#  MIF Функция парсит кпт и вытаскивает количество контуров, количество точек и их координаты
def make_list_for_mif(file_name):
    list_land = []
    tree = ET.parse(file_name)
    # возвращает список участков
    land_records = tree.findall('cadastral_blocks/cadastral_block/record_data/base_data/build_records/build_record')
    print(len(land_records))
    for land_record in land_records:
        # возвращает список контуров в каждом участке
        contours = land_record.findall("./contours/contour")
        print(len(contours))
        list_land.append("Region ")
        list_land.append(len(contours))
        for contour in contours:
            # возвращает список координат точек в каждом контуре в каждом участке
            ordinates = contour.findall("./entity_spatial/spatials_elements/spatial_element/ordinates/ordinate")
            list_land.append(len(ordinates))
            # возращаем значение координат из списка
            for ordinate in ordinates:
                y = ordinate.find('y').text
                x = ordinate.find('x').text
                list_land.append(y)
                list_land.append(x)
    return list_land


#  MIF Функция печатает в файл mif заголовочные данные
def print_head_mif():
    file_mif_head = open('C:/KPT/_Example/actual_build.mif', 'a')
    head_data = [
        'Version   450',
        'Charset "WindowsCyrillic"',
        'Delimiter ","',
        'CoordSys Earth Projection 8, 1001, "m", 88.466666, 0, 1, 2300000, -5512900.5630000001 '
        'Bounds (-5949281.53901, -15515038.0608) (10549281.539, 4489236.93476)',
        'Columns 7',
        'type Char(30)',
        'cad_number Char(30)',
        'readable_address Char(254)',
        'permitted_use Char(254)',
        'area Char(50)',
        'cost Char(50)',
        'date_download Char(10)',
        'Data'
        ]
    for index in head_data:
        file_mif_head.write(index + '\n')
    file_mif_head.close()


def make_list_for_mid_actual_land(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()
    request = root[1][0].text
    list_semantic_land = ''
    data = tree.findall('cadastral_blocks/cadastral_block/record_data/base_data/build_records/build_record')
    for data1 in data:
        data2 = data1.findall('./object/common_data/type/value')
        for tipe in data2:
            _type = tipe.text
        data3 = data1.findall('./object/common_data/cad_number')
        for cad_number in data3:
            _cad_number = cad_number.text
        data4 = data1.findall('./address_location/address/readable_address')
        for adress in data4:
            _adress = adress.text
        data5 = data1.findall('./params/purpose/value')
        if len(data5) >= 1:
            for permitted_use in data5:
                _permitted_use = permitted_use.text
                #  Обрезаем, если длина строки более 250
                if len(_permitted_use) > 250:
                    _permitted_use = _permitted_use[:250] + "..."

        else:
            _permitted_use = "None"
        data6 = data1.findall('params/area')
        for area in data6:
            _area = area.text
        date6 = data1.findall('./cost/value')
        if len(date6) >= 1:
            for cost in date6:
                _cost = cost.text
        else:
            _cost = "None"
         # Формирует строку mid файла
        a = ("\"" + _type +
             "\"," + "\"" + _cad_number +
             "\"," + "\"" + _adress +
             "\"," + "\"" + _permitted_use +
             "\"," + "\"" + _area +
             "\"," + "\"" + _cost +
             "\"," + "\"" + request +
             "\"," + "\n")
        # Формирует данные по всем строкам для записи в mid файл
        list_semantic_land = (list_semantic_land + a)
    return list_semantic_land


if __name__ == '__main__':
     # Запись заголовков в mif
    print_head_mif()
    # filelist = get_file_list("C:/Users/Necvetaeva_v/PycharmProjects/ParserXML/materials/23.05.2022_12_32_выгрузка/Новая папка")
    filelist = get_file_list("C:/KPT/_Example")
    # Открываем поочередно кпт.xml файлы
    for file_name in filelist:
        file_mif = open('C:/KPT/_Example/actual_build.mif', 'a')
        list_coordinate_land_record = make_list_for_mif(file_name)
        # записываем полученный список в mif файл
        for data8 in list_coordinate_land_record:
           file_mif.write(str(data8) + '\n')
        file_mif.close()
        # записываем данные mid в файл
        land = make_list_for_mid_actual_land(file_name)
        file_mid = open('C:/KPT/_Example/actual_build.mid', 'a')
        file_mid.write(land)
        file_mid.close()
