import tkinter as tk

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generated GUI")
        self.label_0 = tk.Label(self.root, text='==МІЙ КАЛЬКУЛЯТОР==')
        self.label_0.grid(row=0, column=0,columnspan=2, padx=5, pady=5, sticky='nsew')
        self.label_1 = tk.Label(self.root, text='Перше число')
        self.label_1.grid(row=1, column=0,columnspan=1, padx=5, pady=5, sticky='nsew')
        self.entry_2 = tk.Entry(self.root)
        self.entry_2.grid(row=1, column=1,columnspan=1, padx=5, pady=5, sticky='nsew')
        self.label_3 = tk.Label(self.root, text='Друге число')
        self.label_3.grid(row=3, column=0,columnspan=1, padx=5, pady=5, sticky='nsew')
        self.entry_4 = tk.Entry(self.root)
        self.entry_4.grid(row=3, column=1,columnspan=1, padx=5, pady=5, sticky='nsew')
        self.label_5 = tk.Label(self.root, text='Результат:')
        self.label_5.grid(row=5, column=0,columnspan=2, padx=5, pady=5, sticky='nsew')
        self.button_6 = tk.Button(self.root, text='Сума', command=self.button_6_command)
        self.button_6.grid(row=6, column=0,columnspan=2, padx=5, pady=5, sticky='nsew')
        self.a = 3
        self.b = 2
    def button_6_command(self):
        # ПІДКАЗКА: додайте код для button_6
        a = int(self.entry_2.get())
        b = int(self.entry_4.get())
        print('Код функції button_6_command виконано')
        c = str( a + b )
        self.label_5.config(text = "Результат: "+c)


if __name__ == '__main__':
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()







