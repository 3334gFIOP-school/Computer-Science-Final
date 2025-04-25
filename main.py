import tkinter as tk
from tkinter import ttk
from audio import play_song, change_speed, set_volume

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
    # Add some widgets to the "ply_sng" frame
    ttk.Label(ply_sng, text="Music Playing Tab").grid(row=0, column=1, padx=10, pady=10, columnspan=3)
    pse_ply = tk.Button(
        ply_sng,
        text="▶",
        command=lambda: play_song(pse_ply, ""),
        font=attention,
    )
    pse_ply.grid(row=1, column=1, padx=10, pady=10)

    volume_label = ttk.Label(ply_sng, text="Volume: 50%", font=("Helvetica", 14))
    volume_label.grid(row=2, column=1, padx=10, pady=5)  # Centered in column 1

    volume_slider = ttk.Scale(
        ply_sng,
        from_=0,
        to=100,
        orient="horizontal",
        length=200,
        command=lambda value: set_volume(volume_slider, volume_label),
    )
    volume_slider.set(50)
    volume_slider.grid(row=3, column=1, padx=10, pady=5)

    speed_label = ttk.Label(ply_sng, text="Speed: 1x", font=("Helvetica", 14))
    speed_label.grid(row=4, column=1, padx=10, pady=5)  # Centered in column 1

    speed_slider = ttk.Scale(
        ply_sng,
        from_=0.5,
        to=2,
        orient="horizontal",
        length=200,
        command=lambda value: change_speed(speed_slider, speed_label),
    )
    speed_slider.set(1)
    speed_slider.grid(row=5, column=1, padx=10, pady=5)  # Centered in column 1



   # Add widgets to the "test_tab" frame
    ttk.Label(test_tab, text="Test Tab with Slidable Progress Bar").grid(row=0, column=0, padx=10, pady=10)

    # Variables to track progress and song duration
    current_progress = tk.DoubleVar(value=0)  # Current progress (in seconds)
    song_duration = 300  # Example song duration in seconds (5 minutes)

    # Function to update the progress bar dynamically as the song plays
    def update_progress_bar():
        if not is_sliding:  # Only update if the user is not sliding
            current_value = current_progress.get()
            if current_value < song_duration:
                current_progress.set(current_value + 1)  # Increment progress by 1 second
                progress_label.config(text=f"Progress: {int(current_value + 1)}s / {song_duration}s")
                update_canvas_fill()  # Update the left-filled section
                root.after(1000, update_progress_bar)  # Schedule the next update in 1 second

    # Function to handle manual sliding of the progress bar
    def on_slide(value):
        global is_sliding
        is_sliding = True
        progress_label.config(text=f"Progress: {int(float(value))}s / {song_duration}s")
        update_canvas_fill()  # Update the left-filled section dynamically

    # Function to handle when the user releases the slider
    def on_slide_release(event):
        global is_sliding
        is_sliding = False
        current_progress.set(slidable_progress.get())  # Update the progress to the slider's value
        update_progress_bar()  # Resume automatic updates

    # Function to update the left-filled section of the canvas
    def update_canvas_fill():
        progress = current_progress.get()
        fill_width = (progress / song_duration) * canvas_width
        canvas.coords(fill_rect, 0, 0, fill_width, canvas_height)  # Update the filled rectangle

    # Style for the slider
    style = ttk.Style()
    style.theme_use("clam")  # Use the "clam" theme for a modern look
    style.configure(
        "Custom.Horizontal.TScale",
        troughcolor="#e0e0e0",  # Background color of the trough
        sliderthickness=5,     # Thickness of the slider
        background="#4caf50",   # Color of the slider
    )

    # Progress Label
    progress_label = ttk.Label(test_tab, text=f"Progress: 0s / {song_duration}s", font=("Helvetica", 14))
    progress_label.grid(row=1, column=0, padx=10, pady=5)

    # Create a frame to hold both the canvas and the scale
    progress_frame = ttk.Frame(test_tab)
    progress_frame.grid(row=2, column=0, padx=10, pady=5, sticky="n")

    # Canvas for the left-filled section
    canvas_width = 300
    canvas_height = 15
    canvas = tk.Canvas(progress_frame, width=canvas_width, height=canvas_height, bg="#e0e0e0", highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="ew")  # Use grid to position the canvas

    # Create the filled rectangle on the canvas
    fill_rect = canvas.create_rectangle(0, 0, 0, canvas_height, fill="#4caf50", width=0)

    # Slidable Progress Bar (ttk.Scale styled as a progress bar)
    slidable_progress = ttk.Scale(
        progress_frame,
        from_=0,
        to=song_duration,
        orient="horizontal",
        length=canvas_width,
        variable=current_progress,  # Bind the progress variable
        command=on_slide,  # Update the label dynamically when sliding
        style="Custom.Horizontal.TScale",  # Apply the custom style
    )
    slidable_progress.grid(row=0, column=0, sticky="ew")  # Overlay the scale on top of the canvas
    slidable_progress.bind("<ButtonRelease-1>", on_slide_release)


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
        elif selected_tab == "Music Player":
            root.geometry("300x300")

    # Bind the tab change event
    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

    root.geometry("300x200")
    root.mainloop()

repeat = True
while repeat:
    repeat = main(repeat)