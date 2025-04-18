import tkinter as tk

class MultiSelectCombobox(tk.Frame):
    def __init__(self, master, options, **kwargs):
        super().__init__(master, **kwargs)
        self.options = options
        self.vars = {}

        # Display field
        self.display = tk.Entry(self, state='readonly')
        self.display.pack(fill='x')
        self.display.bind('<Button-1>', self.toggle_menu)

        # Toplevel dropdown menu
        self.menu = tk.Toplevel(self)
        self.menu.withdraw()  # Hide initially
        self.menu.overrideredirect(True)
        self.menu.attributes("-topmost", True)

        # Populate checkboxes
        for option in options:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(self.menu, text=option, variable=var, command=self.update_display)
            cb.pack(anchor='w')
            self.vars[option] = var

        # Handle clicks outside to close menu
        self.menu.bind("<FocusOut>", lambda e: self.menu.withdraw())

    def toggle_menu(self, event=None):
        if self.menu.winfo_ismapped():
            self.menu.withdraw()
        else:
            x = self.winfo_rootx()
            y = self.winfo_rooty() + self.winfo_height()
            self.menu.geometry(f"+{x}+{y}")
            self.menu.deiconify()
            self.menu.focus_set()

    def update_display(self):
        selected = [opt for opt, var in self.vars.items() if var.get()]
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.insert(0, ', '.join(selected))
        self.display.config(state='readonly')

    def get_selected(self):
        return [opt for opt, var in self.vars.items() if var.get()]

# Example usage
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Multi-Select ComboBox Example")

    multi_combo = MultiSelectCombobox(root, ['Option A', 'Option B', 'Option C'])
    multi_combo.pack(pady=20, padx=20)

    def show_selection():
        print("Selected:", multi_combo.get_selected())

    tk.Button(root, text="Get Selected", command=show_selection).pack(pady=10)

    root.mainloop()
