import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def main(repeat):
    root = tk.Tk()
    root.title("Main Window")

    def on_close():
        nonlocal repeat
        repeat = False
        root.destroy()
        return repeat

    root.protocol("WM_DELETE_WINDOW", on_close)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    notebook = ttk.Notebook(root)
    ply_sng = ttk.Frame(notebook)
    menu = ttk.Frame(notebook)
    plylst = ttk.Frame(notebook)
    frame4 = ttk.Frame(notebook)
    test_tab = ttk.Frame(notebook)  # Create a new test tab

    notebook.add(menu, text="Menu")
    notebook.add(test_tab, text="Test Tab")  # Add the test tab to the notebook
    notebook.pack(expand=True, fill="both")

    # Function to populate the "menu" frame
    def populate_menu():
        ttk.Label(menu, text="Label 1").pack(pady=5)

    # Populate the "menu" frame initially
    populate_menu()

    # Add some widgets to the "test_tab" frame
    ttk.Label(test_tab, text="This is the Test Tab").pack(pady=10)
    ttk.Button(test_tab, text="Test Button", command=lambda: print("Test Button Clicked")).pack(pady=10)

    # Function to clear all widgets from a frame
    def clear_frame(frame):
        print(f"Clearing frame: {frame}")  # Debugging: Print which frame is being cleared
        for widget in frame.winfo_children():
            print(f"Destroying widget: {widget}")  # Debugging: Print each widget being destroyed
            widget.destroy()

    # Function to handle tab changes
    def on_tab_changed(event):
        selected_tab = notebook.tab(notebook.select(), "text")
        print(f"Tab changed to: {selected_tab}")  # Debugging: Print the selected tab
        if selected_tab == "Menu":
            if not menu.winfo_children():  # Only repopulate if the frame is empty
                populate_menu()

    # Bind the tab change event
    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

    # Add a button to clear the "menu" frame
    ttk.Button(root, text="Clear Menu", command=lambda: clear_frame(menu)).pack(pady=10)

    root.mainloop()

repeat = True
while repeat:
    repeat = main(repeat)