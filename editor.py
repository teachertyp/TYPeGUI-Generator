class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<KeyRelease>", self.highlight_spaces)
        self.bind("<Control-c>", self.copy_without_dots)
        self.bind("<Control-Insert>", self.copy_without_dots)  # Additional key binding for copying
        self.bind("<Control-v>", self.paste_text)
        self.bind("<Shift-Insert>", self.paste_text)  # Additional key binding for pasting
        self.bind("<Control-a>", self.select_all)
        self.bind("<Button-1>", self.hide_context_menu)  # Hide context menu on left-click
        self.bind("<Button-3>", self.show_context_menu)
        self.bind("<KeyRelease>", self.highlight_spaces)
        
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy_without_dots)
        self.context_menu.add_command(label="Paste", command=self.paste_text)
        self.context_menu.add_command(label="Select All", command=self.select_all)

    def highlight_spaces(self, event=None):
        self.tag_remove('space', '1.0', tk.END)
        text = self.get('1.0', tk.END)
        for index, char in enumerate(text):
            if char == ' ':
                pos = f"1.0 + {index} chars"
                self.tag_add('space', pos, f"{pos} +1c")
                self.tag_configure('space', foreground='red')
        self._replace_spaces()
        self.update_line_numbers()

    def _replace_spaces(self):
        self.tag_remove('replace', '1.0', tk.END)
        text = self.get('1.0', tk.END)
        for index, char in enumerate(text):
            if char == ' ':
                pos = f"1.0 + {index} chars"
                self.tag_add('replace', pos, f"{pos} +1c")
                self.replace(pos, f"{pos} +1c", '·')
        self.tag_configure('replace', foreground='red')

    def copy_without_dots(self, event=None):
        try:
            self.clipboard_clear()
            selection = self.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.clipboard_append(selection.replace('·', ' '))
            return "break"  # Prevent default Ctrl+C handling
        except tk.TclError:
            pass  # No selection

    def paste_text(self, event=None):
        try:
            clipboard_content = self.clipboard_get()
            self.insert(tk.INSERT, clipboard_content.replace('·', ' '))
            return "break"  # Prevent default pasting
        except tk.TclError:
            pass  # Clipboard is empty or unavailable

    def select_all(self, event=None):
        self.tag_add(tk.SEL, "1.0", tk.END)
        self.mark_set(tk.INSERT, "1.0")
        self.see(tk.INSERT)
        return "break"  # Prevent default Ctrl+A handling

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def hide_context_menu(self, event=None):
        self.context_menu.unpost()  # Hide context menu when clicking on the text
    
    def update_line_numbers(self, event=None):
        line_numbers = "\n".join(str(i + 1) for i in range(int(self.index(tk.END).split(".")[0]) - 1))
        self.line_numbers_widget.config(state=tk.NORMAL)
        self.line_numbers_widget.delete("1.0", tk.END)
        self.line_numbers_widget.insert(tk.INSERT, line_numbers)
        self.line_numbers_widget.config(state=tk.DISABLED)

    def on_scroll(self, event=None):
        self.line_numbers_widget.yview_moveto(self.yview()[0])        


class TextEditorWithLineNumbers(tk.Frame):
    def on_scrollbar_scroll(self, *args):
        """Синхронізація прокрутки при використанні смуги прокрутки"""
        self.text_editor.yview(*args)
        self.line_numbers.yview(*args)

    def on_text_scroll(self, *args):
        """Синхронізація прокрутки при використанні колеса миші або клавіш"""
        self.scrollbar.set(*args)
        self.line_numbers.yview_moveto(args[0])  
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(expand=True, fill=tk.BOTH)
        # Додаємо смугу прокрутки
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.line_numbers = tk.Text(self, width=4, padx=5, takefocus=0, border=0,
                                    background='lightgray', state='disabled')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        self.text_editor = CustomText(self, wrap=tk.WORD)
        self.text_editor.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.text_editor.line_numbers_widget = self.line_numbers
        self.text_editor.update_line_numbers()
        
        # Зв'язуємо смугу прокрутки з текстовим полем
        self.scrollbar.config(command=self.on_scrollbar_scroll)
        self.text_editor.config(yscrollcommand=self.scrollbar.set)