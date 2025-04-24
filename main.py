import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from audio import play_song

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
    notebook.add(ply_sng, text="Music Player")
    notebook.pack(expand=True, fill="both")

    # Function to populate the "menu" frame
    def populate_menu():
        ttk.Label(menu, text="Welcome to Music Player!\nSelect a tab to continue").pack(pady=5)

    # Populate the "menu" frame initially
    populate_menu()


    attention = ("Helvetica", 20, "bold")
    # Add some widgets to the "test_tab" frame
    tk.Label(ply_sng, text="Music Playing Tab").grid(row=0, column=1, padx=10, pady=10, columnspan=3)
    pse_ply = tk.Button(ply_sng, text="⏸", command=lambda: play_song(pse_ply), font=attention)
    pse_ply.config(text="▶", font=("Helvetica", 20, "bold"))
    pse_ply.grid(row=1, column=1, padx=10, pady=10)

    ff = tk.Button(ply_sng, text="⏭", command=lambda: play_song(pse_ply), font=attention)

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
    root.geometry("300x200")
    root.mainloop()

repeat = True
while repeat:
    repeat = main(repeat)