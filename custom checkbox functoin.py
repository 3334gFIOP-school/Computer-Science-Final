import tkinter as tk

class MultiSelectListbox(tk.Frame):
    def __init__(self, master, options, **kwargs):
        super().__init__(master, **kwargs)
        self.options = options

        # Frame for the Listbox and Scrollbar
        self.listbox_frame = tk.Frame(self)
        self.listbox_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.listbox_frame, orient='vertical')
        self.scrollbar.pack(side='right', fill='y')

        # Listbox
        self.listbox = tk.Listbox(
            self.listbox_frame,
            selectmode='multiple',
            yscrollcommand=self.scrollbar.set
        )
        self.listbox.pack(side='left', fill='both', expand=True)

        # Configure the scrollbar to work with the Listbox
        self.scrollbar.config(command=self.listbox.yview)

        # Populate the Listbox with options
        for option in options:
            self.listbox.insert(tk.END, option)

    def print_selected_items(self):
        # Print selected items in the terminal
        selected_indices = self.listbox.curselection()
        selected = [self.listbox.get(i) for i in selected_indices]
        print(selected)

    def clear_selection(self):
        # Clear all selections in the Listbox
        self.listbox.selection_clear(0, tk.END)


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("MultiSelect Listbox Example")

    # Example options
    options = ["Option 1", "Option 2", "Option 3", "Option 4"]

    # Create and pack the MultiSelectListbox
    listbox = MultiSelectListbox(root, options)
    listbox.pack(padx=10, pady=10, fill='both', expand=True)

    # Add a button to clear selected items
    clear_button = tk.Button(root, text="Clear selection", command=listbox.clear_selection)
    clear_button.pack(pady=10)

    # Add a button to print selected items
    show_button = tk.Button(root, text="Show selected items", command=listbox.print_selected_items)
    show_button.pack(pady=10)

    # Run the application
    root.mainloop()