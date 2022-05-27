import xml.etree.ElementTree as ET
import os

# функция возвращает список .xml файлов из папки, включая подпапки, кроме proto_.xml
def get_file_list(path):
    filelist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".xml") and file != "proto_.xml":
                filelist.append(os.path.join(root, file))
    print(filelist)  #  Проверка пути!!!!!!!!!!!!!!!!
    return filelist


#  MIF Функция парсит кпт и вытаскивает количество контуров, количество точек и их координаты
def make_list_for_mif_actual_land(file_name):
    list_land = []
    tree = ET.parse(file_name)
    # ------------------------------возвращает список участков----------------------------------------------
    land_records = tree.findall('cadastral_blocks/cadastral_block/record_data/base_data/land_records/land_record')
    for land_record in land_records:
        #  ---------------------------возвращает список контуров в каждом участке----------------------------
        spatal_elements = land_record.findall("./contours_location/contours/contour/entity_spatial/"
                                              "spatials_elements/spatial_element")
        if len(spatal_elements) > 0:
            list_land.append("Region ")
            list_land.append(len(spatal_elements))
            for spatal_element in spatal_elements:
                # ---------------возвращает список координат точек в каждом контуре в каждом участке---------
                ordinates = spatal_element.findall("./ordinates/ordinate")
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
    file_mif_head = open('C:/KPT/_Example/actual_land.mif', 'a')
    head_data = [
        'Version   450',
        'Charset "WindowsCyrillic"',
        'Delimiter ","',
        'CoordSys Earth Projection 8, 1001, "m", 88.466666, 0, 1, 2300000, -5512900.5630000001 '
        'Bounds (-5949281.53901, -15515038.0608) (10549281.539, 4489236.93476)',
        'Columns 8',
        'type Char(30)',
        'cad_number Char(30)',
        'readable_address Char(254)',
        'permitted_use Char(100)',
        'area Char(50)',
        'cost Char(50)',
        'category Char(50)',
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
    data = tree.findall('cadastral_blocks/cadastral_block/record_data/base_data/land_records/land_record')
    for data1 in data:
        #  ------------------- проверка на наличие координат границ------------------------------------------
        coordinates = data1.findall("./contours_location/contours/contour/entity_spatial/"
                                              "spatials_elements/spatial_element")
        if len(coordinates) > 0:
            #  -------------------Тип объекта------------------------------------------
            data2 = data1.findall('./object/common_data/type/value')
            if len(data2) >= 1:
                for tipe in data2:
                    _type = tipe.text
            else:
                _type = "None"
            #  -------------------Кадастровый номер------------------------------------------
            data3 = data1.findall('./object/common_data/cad_number')
            if len(data3) >= 1:
                for cad_number in data3:
                    _cad_number = cad_number.text
            else:
                _cad_number = "None"
            #  -------------------Адрес-------------------------------------------
            data4 = data1.findall('./address_location/address/readable_address')
            if len(data4) >= 1:
                for adress in data4:
                    _adress = adress.text
                    rez_adress = _adress.replace('"', '\'')
            else:
                _adress = "None"
            #  -------------------Вид разрешенного использования--------------
            data5 = data1.findall('params/permitted_use/permitted_use_established/by_document')
            if len(data5) >= 1:
                for permitted_use in data5:
                    _permitted_use = permitted_use.text
            else:
                _permitted_use = "None"
            #  --------------------Площадь------------------------------------------
            data6 = data1.findall('params/area/value')
            if len(data6) >= 1:
                for area in data6:
                    _area = area.text
            else:
                    _area = "None"
            #  --------------------Цена------------------------------------------
            date7 = data1.findall('./cost/value')
            if len(date7) >= 1:
                for cost in date7:
                    _cost = cost.text
            else:
                _cost = "None"
            #  -------------------Категоря---------------------------------------
            date8 = data1.findall('params/category/type/value')
            if len(date8) >= 1:
                for category in date8:
                    _category = category.text
            else:
                _category = "None"
            # Формирует строку mid файла
            a = ("\"" + _type[:30] +
                 "\"," + "\"" + _cad_number[:30] +
                 "\"," + "\"" + rez_adress[:250] +
                 "\"," + "\"" + _permitted_use[:100] +
                 "\"," + "\"" + _area[:50] +
                 "\"," + "\"" + _cost[:50] +
                 "\"," + "\"" + _category[:50] +
                 "\"," + "\"" + request +
                 "\"," + "\n")
            # Формирует данные по всем строкам для записи в mid файл
            list_semantic_land = (list_semantic_land + a)
    return list_semantic_land

if __name__ == '__main__':
    print_head_mif()
# -------------------------Открываем поочередно кпт.xml файлы----------------------------------
    filelist = get_file_list("C:/KPT/_Example")
    for file_name in filelist:
        file_mif = open('C:/KPT/_Example/actual_land.mif', 'a')
# ------------------------записываем полученный список в mif файл-------------------------------
        list_coordinate_land_record = make_list_for_mif_actual_land(file_name)
        for data8 in list_coordinate_land_record:
           file_mif.write(str(data8) + '\n')
        file_mif.close()
# ---------------------------записываем данные mid в файл---------------------------------------
        land = make_list_for_mid_actual_land(file_name)
        file_mid = open('C:/KPT/_Example/actual_land.mid', 'a')
        file_mid.write(land)
        file_mid.close()
