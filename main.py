"""
Автор: Юрій Терещенко
Email: yurchikte@gmail.com
Опис: Ця програма призначена для спрощення процесу розробки
      графічних інтерфейсів користувача (GUI) на мові програмування Python
      за допомогою бібліотеки Tkinter. Вона дозволяє візуально конструювати 
      інтерфейси, вибираючи необхідні елементи керування та налаштовуючи їх 
      властивості, а потім автоматично генерує відповідний код на Python.
"""
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext,messagebox
from editor import CustomText, TextEditorWithLineNumbers

import json
import subprocess
import os




class GUIBuilder:
    def __init__(self, root):
        # Ініціалізація вікна, елементів керування та інших атрибутів
        self.root = root
        self.root.title("TYPeGUI Generator")

        self.file_path = "myprogram.py"
        self.project_file_path = ""

        # Атрибути для зберігання попереднього контрола та його фону
        self.previous_control = None
        self.previous_control_bg = None

        self.controls = {}
        self.current_control = None
        self.code_text = None



        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.control_listbox = tk.Listbox(self.root, width=30)
        self.control_listbox.pack(side=tk.LEFT, fill=tk.Y)

        self.control_listbox.bind("<ButtonRelease-1>", self.on_control_select)

        # self.add_button = tk.Button(self.root, text="Add Label", command=self.add_label)
        # self.add_button.pack(side=tk.TOP, fill=tk.X)

        # self.add_button = tk.Button(self.root, text="Add Entry", command=self.add_entry)
        # self.add_button.pack(side=tk.TOP, fill=tk.X)

        # self.add_button = tk.Button(self.root, text="Add Button", command=self.add_button_control)
        # self.add_button.pack(side=tk.TOP, fill=tk.X)

        self.edit_frame = tk.Frame(self.root)
        self.edit_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.label_name = tk.Label(self.edit_frame, text="Name:")
        self.label_name.grid(row=0, column=0, sticky=tk.W)
        self.entry_name = tk.Entry(self.edit_frame)
        self.entry_name.grid(row=0, column=1, sticky=tk.EW)

        self.label_text = tk.Label(self.edit_frame, text="Text:")
        self.label_text.grid(row=1, column=0, sticky=tk.W)
        self.entry_text = tk.Entry(self.edit_frame)
        self.entry_text.grid(row=1, column=1, sticky=tk.EW)

        self.label_row = tk.Label(self.edit_frame, text="Row:")
        self.label_row.grid(row=2, column=0, sticky=tk.W)
        self.entry_row = tk.Entry(self.edit_frame)
        self.entry_row.grid(row=2, column=1, sticky=tk.EW)

        self.label_col = tk.Label(self.edit_frame, text="Column:")
        self.label_col.grid(row=3, column=0, sticky=tk.W)
        self.entry_col = tk.Entry(self.edit_frame)
        self.entry_col.grid(row=3, column=1, sticky=tk.EW)

        self.label_colspan = tk.Label(self.edit_frame, text="Colspan:")
        self.label_colspan.grid(row=4, column=0, sticky=tk.W)
        self.entry_colspan = tk.Entry(self.edit_frame)
        self.entry_colspan.grid(row=4, column=1, sticky=tk.EW)

        self.label_event = tk.Label(self.edit_frame, text="Event:")
        self.label_event.grid(row=5, column=0, sticky=tk.W)

        self.event_combobox = ttk.Combobox(self.edit_frame, values=["Button-1", "Button-2", "Button-3", "KeyPress", "KeyRelease", "FocusOut", "FocusIn"])
        self.event_combobox.grid(row=5, column=1, sticky=tk.EW)
        
                # Add binding to refocus on the listbox after selecting an event
        self.event_combobox.bind("<<ComboboxSelected>>", self.on_event_selected)
        self.event_combobox.configure(exportselection=False)
        
        self.label_function = tk.Label(self.edit_frame, text="Function Name:")
        self.label_function.grid(row=6, column=0, sticky=tk.W)
        self.entry_function = tk.Entry(self.edit_frame)
        self.entry_function.grid(row=6, column=1, sticky=tk.EW)

        self.save_button = tk.Button(self.edit_frame, text="Зберегти", command=self.save_changes, state=tk.DISABLED)
        self.save_button.grid(row=7, column=0, columnspan=2, sticky=tk.EW)

        self.delete_button = tk.Button(self.edit_frame, text="Видалити", command=self.delete_control, state=tk.DISABLED)
        self.delete_button.grid(row=8, column=0, columnspan=2, sticky=tk.EW)

        self.generate_button = tk.Button(self.edit_frame, text="Згенерувати код", command=self.generate_code, state=tk.DISABLED)
        self.generate_button.grid(row=9, column=0, columnspan=2, sticky=tk.EW)
        
        self.event_options = {
            "Label": ["<Button-1>", "<Button-2>", "<Button-3>","<Motion>","<Leave>"],
            "Entry": ["<KeyPress>", "<KeyRelease>", "<FocusIn>", "<FocusOut>"],
            "Button": ["<Button-1>", "<Button-2>", "<Button-3>","<Motion>","<Leave>"]
        }

        # Додаємо меню "Файл"
        menu_bar = tk.Menu(root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Зберегти", command=self.save_project)
        file_menu.add_command(label="Завантажити", command=self.load_project)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

        add_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Додати", menu=add_menu)
        add_menu.add_command(label="Label",command = self.add_label)
        add_menu.add_command(label="Entry", command = self.add_entry)
        add_menu.add_command(label="Button",command = self.add_button_control)

        menu_bar.add_command(label="Виконати", command = self.execute_code)

        
        root.config(menu=menu_bar)
        self.run_file_button = tk.Button(self.edit_frame, text="Відкрити і Виконати", command=self.open_and_execute_code, state=tk.DISABLED)
        self.run_file_button.grid(row=9, column=0, columnspan=2, sticky=tk.EW)
        #self.open_file_button.pack(pady=10)

    def open_and_execute_code(self):
        base_path, _ = os.path.splitext(self.project_file_path)
        # Додавання нового розширення
        new_file_path = base_path + ".py"        
        # Відкрити нове вікно з вмістом згенерованого файлу
        self.code_window = tk.Toplevel(self.root)
        self.code_window.title("TYPeGUI Generator code editor" + new_file_path)

        # Створити редактор з лінійками
        text_editor_frame = TextEditorWithLineNumbers(self.code_window)
        text_editor_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)


        # Доступ до текстового поля з класу TextEditorWithLineNumbers
        self.code_text = text_editor_frame.text_editor

        try:
            with open(new_file_path, "r") as file:
                code_content = file.read()
                self.code_text.insert(tk.END, code_content)
                
                # Виклик highlight_spaces для відображення крапок та оновлення нумерації рядків
                self.code_text.highlight_spaces()
                self.code_text.update_line_numbers()

        except FileNotFoundError:
            self.code_text.insert(tk.END, "# No code found\n")

        # Кнопка для збереження змін
        save_button = tk.Button(self.code_window, text="Зберегти", command=self.save_code)
        save_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Кнопка для відображення відступів
        nonprintable_button = tk.Button(self.code_window, text="Показати/прибрабрати відступи", command=self.show_hide_nonprintable_symbols)
        nonprintable_button.pack(side=tk.LEFT, padx=10, pady=10)        

        # Кнопка для виконання згенерованого коду
        execute_button = tk.Button(self.code_window, text="Виконати", command=self.execute_code)
        execute_button.pack(pady=10)

        #Термінал
                # Текстове поле для виведення
        self.lp_termianl = tk.Text(self)
        self.lp_termianl.pack()


    def show_hide_nonprintable_symbols(self):
        print("shownps")
        if self.code_text.shownps:
            self.code_text.shownps = False
            self.code_text._replace_spaces()
        else:
            self.code_text.shownps = True
            self.code_text._replace_spaces()
            

    def save_code(self):
        print("savecode")
        if hasattr(self, 'code_text'):
            # Зберегти зміни в згенерованому файлі
            base_path, _ = os.path.splitext(self.project_file_path)
            # Додавання нового розширення
            new_file_path = base_path + ".py"
            if new_file_path:
                code_content = self.code_text.get(1.0, tk.END)
                code_content = code_content.replace('·', ' ')
                with open(new_file_path, "w") as file:
                    file.write(code_content)
                    self.run_file_button.config(state=tk.NORMAL)
        else:
            print("Error: Code text widget not initialized")

    def execute_code(self):
        try:
            # Зберегти зміни в згенерованому файлі
            base_path, _ = os.path.splitext(self.project_file_path)
            # Додавання нового розширення
            new_file_path = base_path + ".py"            
            subprocess.run(["python3", new_file_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
    
    def clean_config(self, config):
        # Видаляє несеріалізовані дані з конфігурації
        return {k: v for k, v in config.items() if isinstance(v, (str, int, float, bool))}

    def save_project(self):
        print("SP")
        if self.project_file_path in ["",()] :
            self.project_file_path = filedialog.asksaveasfilename(defaultextension=".json")
        print(self.project_file_path)
        if self.project_file_path != ():
            data = {
                "controls": []
            }
            for control_id, control in self.controls.items():
                if not isinstance(control, tk.Frame):
                    control_data = {
                        "id": control_id,
                        "type": type(control).__name__,
                        "grid": {k: v for k, v in control.grid_info().items() if k != 'in'},
                        "config": self.clean_config(control.config()),
                        "children": []
                    }
                    # Додаємо текстову властивість для Label і Button
                    if isinstance(control, (tk.Label, tk.Button)):
                        control_data["config"]["text"] = control.cget("text")
                    if control.winfo_children():
                        for child in control.winfo_children():
                            control_data["children"].append(self.extract_child_data(child))
                    data["controls"].append(control_data)

            with open(self.project_file_path, "w") as f:
                json.dump(data, f, indent=4)
            self.generate_code()
    def extract_child_data(self, widget):
        child_data = {
            "type": type(widget).__name__,
            "grid": {k: v for k, v in widget.grid_info().items() if k != 'in'},
            "config": self.clean_config(widget.config()),
            "children": []
        }
        # Додаємо текстову властивість для дочірніх Label і Button
        if isinstance(widget, (tk.Label, tk.Button)):
            child_data["config"]["text"] = widget.cget("text")
        child_data["config"]["name"] = widget.cget("name")
        for child in widget.winfo_children():
            child_data["children"].append(self.extract_child_data(child))
        return child_data

    def load_project(self):
        # Очищення інтерфейсу
        for control in self.controls.values():
            control.destroy()
        self.controls.clear()
        self.control_listbox.delete(0, tk.END)

        self.project_file_path = filedialog.askopenfilename(defaultextension=".json")
        if self.project_file_path:
            with open(self.project_file_path, "r") as f:
                data = json.load(f)

            def create_widget_from_data(parent, widget_data):
                widget_class = getattr(tk, widget_data['type'], None)
                if widget_class:
                    widget = widget_class(parent, **widget_data['config'])
                    widget.grid(**{k: v for k, v in widget_data['grid'].items() if k != 'in'})
                    
                    # Додаємо widget до self.controls за control_id
                    control_id = widget_data['id']
                    self.controls[control_id] = widget

                    # Додаємо control_id до listbox
                    self.control_listbox.insert(tk.END, control_id)
                    
                    # Створюємо дочірні елементи рекурсивно
                    for child_data in widget_data.get("children", []):
                        create_widget_from_data(widget, child_data)
                else:
                    messagebox.showerror("Error", f"Unsupported widget type: {widget_data['type']}")
                return widget

            for control_data in data["controls"]:
                create_widget_from_data(self.frame, control_data)
            self.run_file_button.config(state=tk.NORMAL)


    def add_label(self):
        self.add_control(tk.Label, text="New Label")
        self.generate_button.config(state=tk.NORMAL)


    def add_entry(self):
        self.add_control(tk.Entry, text="")
        self.generate_button.config(state=tk.NORMAL)

    def add_button_control(self):
        self.add_control(tk.Button, text="New Button")
        self.generate_button.config(state=tk.NORMAL)

    def add_control(self, control_class, **kwargs):
        row = len(self.controls)
        control_id = f"{control_class.__name__.lower()}_{row}"
        control = control_class(self.frame, **kwargs)
        control.grid(row=row, column=0, padx=5, pady=5, sticky='we')
        self.controls[control_id] = control
        self.control_listbox.insert(tk.END, control_id)
                # Зберігаємо додаткові атрибути у словнику control
        control.config(**kwargs)
    def on_event_selected(self, event):
        pass
    def on_control_select(self, event):
        self.control_listbox.configure(exportselection=False)
        selection = self.control_listbox.curselection()
        if selection:
            self.save_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
            control_id = self.control_listbox.get(selection[0])
            control = self.controls[control_id]
            self.current_control = control

            # Відновлюємо попередній контроль
            if self.previous_control:
                self.previous_control.config(bg=self.previous_control_bg)  # Відновлюємо початковий фон

            # Зберігаємо новий контроль як попередній
            self.previous_control = control
            self.previous_control_bg = control.cget('bg')  # Зберігаємо початковий фон

            # Підсвічуємо новий контроль
            control.config(bg='yellow')  # Встановлюємо новий фон

            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, control_id)

            if isinstance(control, tk.Label) or isinstance(control, tk.Button):
                self.entry_text.delete(0, tk.END)
                self.entry_text.insert(0, control.cget('text'))
            else:
                self.entry_text.delete(0, tk.END)
                self.entry_text.insert(0, control.get())

            row, col, colspan = control.grid_info().get('row', 0), control.grid_info().get('column', 0), control.grid_info().get('columnspan', 0)
            self.entry_row.delete(0, tk.END)
            self.entry_row.insert(0, row)

            self.entry_col.delete(0, tk.END)
            self.entry_col.insert(0, col)

            self.entry_colspan.delete(0, tk.END)
            self.entry_colspan.insert(0, colspan)

            event_bindings = self.get_event_bindings(control)
            self.event_combobox.set('')
            if event_bindings:
                self.event_combobox.set(event_bindings[0])

            control_type = type(control).__name__
            self.event_combobox['values'] = self.event_options.get(control_type, [])

            # Встановлюємо функцію для події, якщо вона є
            function_name = self.get_function_name(control)
            self.entry_function.delete(0, tk.END)
            if function_name:
                self.entry_function.insert(0, function_name)


    def get_event_bindings(self, control):
        bindings = control.bind()
        if isinstance(bindings, dict):
            return [event.replace('<', '').replace('>', '') for event in bindings.keys()]
        elif isinstance(bindings, tuple):
            return [event.replace('<', '').replace('>', '') for event in bindings]
        return []
    def get_function_name(self, control):
        function_name = None
        for event in self.get_event_bindings(control):
            handler = control.bind_class(event)
            if handler:
                function_name = handler.__name__
                break
        return function_name

    def save_changes(self):
        print("Save changes")
        selection = self.control_listbox.curselection()
        if not selection:
            return

        control_id = self.entry_name.get()
        self.entry_name.delete(0, tk.END)
        
        new_text = self.entry_text.get()
        self.entry_text.delete(0, tk.END)
        
        new_row = self.entry_row.get()
        self.entry_row.delete(0, tk.END)
        
        new_col = self.entry_col.get()
        self.entry_col.delete(0, tk.END)

        new_colspan = self.entry_colspan.get()
        self.entry_colspan.delete(0, tk.END)
        
        new_event = self.event_combobox.get()
        self.event_combobox.set('')  # Очищуємо комбо-бокс
        
        function_name = self.entry_function.get()
        
        self.entry_function.delete(0, tk.END)
        print("fname:", function_name)

        if isinstance(self.current_control, tk.Entry):
            self.current_control.delete(0, tk.END)
            self.current_control.insert(0, new_text)
        elif isinstance(self.current_control, tk.Label) or isinstance(self.current_control, tk.Button):
            self.current_control.config(text=new_text)

        self.current_control.grid(row=int(new_row), column=int(new_col), columnspan=int(new_colspan), padx=5, pady=5, sticky='ew')

        if new_event and function_name:
            self.current_control.unbind(f"<{new_event}>")
            self.current_control.bind(f"<{new_event}>", self.create_event_handler(function_name))

        old_control_id = self.control_listbox.get(selection[0])
        if control_id != old_control_id:
            # Видаляємо старий ідентифікатор зі словника
            del self.controls[old_control_id]
            # Додаємо новий ідентифікатор
            self.controls[control_id] = self.current_control
            self.control_listbox.delete(selection[0])
            self.control_listbox.insert(tk.END, control_id)
        else:
            # Оновлюємо контроль у словнику, якщо ідентифікатор не змінився
            self.controls[control_id] = self.current_control
        self.save_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)


    def create_event_handler(self, function_name):
        def event_handler(event):
            func = getattr(self, function_name, None)
            if func:
                func(event)
            else:
                print(f"Function {function_name} not found.")
        return event_handler

    def delete_control(self):
        selection = self.control_listbox.curselection()
        if selection:
            control_id = self.control_listbox.get(selection[0])
            self.controls[control_id].destroy()
            del self.controls[control_id]
            self.control_listbox.delete(selection[0])

    def generate_code(self):
        code = "import tkinter as tk\n\n"
        code += "class MyApp:\n"
        code += "    def __init__(self, root):\n"
        code += "        self.root = root\n"
        code += "        self.root.title(\"Generated GUI\")\n"

        for control_id, control in self.controls.items():
            if isinstance(control, tk.Label):
                codeEl = f"        self.{control_id} = tk.Label(self.root, text='{control.cget('text')}')\n"
            elif isinstance(control, tk.Entry):
                codeEl = f"        self.{control_id} = tk.Entry(self.root)\n"
            elif isinstance(control, tk.Button):
                codeEl = f"        self.{control_id} = tk.Button(self.root, text='{control.cget('text')}', command=self.{control_id}_command)\n"
            print(codeEl)
            code += codeEl
            
            # Генерація коду для прив'язки подій
            events = control.bind()
            for event in events:
                event_type = event.replace('<', '').replace('>', '')
                event_for_name = event_type.replace('-', '_')
                code += f"        self.{control_id}.bind('<{event_type}>', self.{control_id}_{event_for_name}_handler)\n"

            row = control.grid_info().get('row', 0)
            col = control.grid_info().get('column', 0)
            colspan = control.grid_info().get('columnspan', 0)
            code += f"        self.{control_id}.grid(row={row}, column={col},columnspan={colspan}, padx=5, pady=5, sticky='nsew')\n"

        # Генерація методів обробників подій
        for control_id, control in self.controls.items():
            if isinstance(control, tk.Button):
                code += f"\n    def {control_id}_command(self):\n"
                code += f"        # ПІДКАЗКА: додайте код для {control_id}\n"
                code += f"        print('Код функції {control_id}_command виконано')\n"
            
            # Генерація обробників подій
            events = self.get_event_bindings(self.controls[control_id])
            for event in events:
                event_type = event.replace('<', '').replace('>', '')
                event_for_name = event_type.replace('-', '_')
                code += f"\n    def {control_id}_{event_for_name}_handler(self, event):\n"
                code += f"        # ПІДКАЗКА: додайте код для події {control_id}_{event_for_name}_handler\n"
                code += f"        print('{control_id}_{event_for_name}_handler triggered')\n"

        code += "\nif __name__ == '__main__':\n"
        code += "    root = tk.Tk()\n"
        code += "    app = MyApp(root)\n"
        code += "    root.mainloop()\n"
        if self.project_file_path !="":
            base_path, _ = os.path.splitext(self.project_file_path)

            # Додавання нового розширення
            new_file_path = base_path + ".py"

            if new_file_path:
                with open(new_file_path, "w") as file:
                    file.write(code)

                print("Код збережено.")
                self.run_file_button.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Error", "Спочатку збережіть проєкт")




    # ... (інші функції)

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIBuilder(root)
    root.mainloop()
