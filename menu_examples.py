
import tkinter as tk
from tkinter import ttk

# Main application window
root = tk.Tk()
root.title("Main Window")

# Function to open the Treeview window
def open_treeview_window():
    tree_window = tk.Toplevel(root)
    tree_window.title("Treeview Example")

    tree = ttk.Treeview(tree_window, columns=("Size", "Modified"), show="headings")
    tree.heading("Size", text="Size")
    tree.heading("Modified", text="Modified")
    tree.insert("", "end", values=("File1.txt", "15 KB", "2025-04-11"))
    tree.insert("", "end", values=("File2.txt", "20 KB", "2025-04-10"))
    tree.pack(fill=tk.BOTH, expand=True)

# Function to open the Notebook window
def open_notebook_window():
    notebook_window = tk.Toplevel(root)
    notebook_window.title("Notebook Example")

    notebook = ttk.Notebook(notebook_window)
    frame1 = ttk.Frame(notebook)
    frame2 = ttk.Frame(notebook)

    notebook.add(frame1, text="Tab 1")
    notebook.add(frame2, text="Tab 2")

    ttk.Label(frame1, text="This is Tab 1").pack(pady=10, padx=10)
    ttk.Label(frame2, text="This is Tab 2").pack(pady=10, padx=10)

    notebook.pack(fill=tk.BOTH, expand=True)

# Function to open the Progressbar window
def open_progressbar_window():
    progress_window = tk.Toplevel(root)
    progress_window.title("Progressbar Example")

    progress = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=20, padx=20)

    progress["value"] = 50  # Set progress to 50%

# Buttons to open each window
btn_treeview = ttk.Button(root, text="Open Treeview Window", command=open_treeview_window)
btn_treeview.pack(pady=10)

btn_notebook = ttk.Button(root, text="Open Notebook Window", command=open_notebook_window)
btn_notebook.pack(pady=10)

btn_progressbar = ttk.Button(root, text="Open Progressbar Window", command=open_progressbar_window)
btn_progressbar.pack(pady=10)

# Run the application
root.mainloop()