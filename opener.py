import tkinter as tk
import tkinter.filedialog as fd


class App(tk):
    def __init__(self):
        super().__init__()
        btn_dir = tk.Button(self, text="Выбрать папку",
                            command=self.choose_directory)
        btn_dir.pack(padx=60, pady=10)

    def choose_directory(self):
        directory = fd.askdirectory(title="Открыть папку", initialdir="/")
        if directory:
            print(directory)


def do():
    app = App()
    app.mainloop()
