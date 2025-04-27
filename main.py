import tkinter as tk
from tkinter import ttk
from audio import play_song, change_speed, set_volume

class MultiSelectListbox(tk.Frame):
    def __init__(self, master, options, nme, preselected_indices=None, **kwargs):
        super().__init__(master, **kwargs)
        self.options = options
        self.nme = nme

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

        # Pre-select items if indices are provided
        if preselected_indices:
            for index in preselected_indices:
                self.listbox.selection_set(index)

    def print_selected_items(self):
        # Print selected items in the terminal
        selected_indices = self.listbox.curselection()
        selected = [self.listbox.get(i) for i in selected_indices]
        export = [str(self.nme), selected] #['Playlist name', ['song1','song2'...]]
        print(f"Selected items: {selected}")

    def clear_selection(self):
        # Clear all selections in the Listbox
        self.listbox.selection_clear(0, tk.END)

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
    notebook.add(plylst, text="Playlist edit")
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



    def create_plylst():
        clear_frame(plylst)
        nme = tk.StringVar()

        def slct_sngs():
            nme.get() #?????????????????
            clear_frame(plylst)

            options = [] #Figure out how to integrate this later ===========================================================

            # Create and pack the MultiSelectListbox
            listbox = MultiSelectListbox(plylst, options, nme)
            listbox.pack(padx=10, pady=10, fill='both', expand=True)

            # Add a button to clear selected items
            clear_button = tk.Button(plylst, text="Clear selection", command=listbox.clear_selection)
            clear_button.pack(pady=10)

            # Add a button to print selected items
            show_button = tk.Button(plylst, text="Add items to playlist", command=listbox.print_selected_items)
            show_button.pack(pady=10)




        ttk.Label(plylst, text="Enter name of playlist:").grid(column=0, row=0, padx=10, pady=10)
        ttk.Entry(plylst, textvariable=nme).grid(column=0, row=1, padx=5, pady=5)
        ttk.Button(plylst, text="Enter information", command=slct_sngs).grid(column=0, row=2, padx=10, pady=10)
    
    def edt_plylst(root):
        clear_frame(plylst)

        root.geometry("400x400")

        def edit_sngs():
            nme = lstbox.curselection()
            clear_frame(plylst)
            #root.geometry("400x150")

            options = ["song1", "song2", "song3"] #Figure out how to integrate this later ===========================================================
            preselected_indices = [0, 2]  # Integrate this with everything else ###################################################################################

            # Create and pack the MultiSelectListbox
            listbox = MultiSelectListbox(plylst, options, nme, preselected_indices)
            listbox.pack(padx=10, pady=10, fill='both', expand=True)

            # Add a button to clear selected items
            clear_button = tk.Button(plylst, text="Clear selection", command=listbox.clear_selection)
            clear_button.pack(pady=10)

            # Add a button to print selected items
            show_button = tk.Button(plylst, text="Finalize playlist", command=listbox.print_selected_items)
            show_button.pack(pady=10)


            # The rest of this is someone else's ############################################################################################

        options = ["option 1", "option 2", "option 3"] #Integrate this with everything else ###################################################################################

        # Scrollbar
        scrollbar = tk.Scrollbar(plylst, orient='vertical')
        scrollbar.pack(side='right', fill='y')

        # Listbox
        lstbox = tk.Listbox(
            plylst,
            selectmode='single',
            yscrollcommand=scrollbar.set
        )
        lstbox.pack(side='left', fill='both', expand=True)

        # Configure the scrollbar to work with the Listbox
        scrollbar.config(command=lstbox.yview)

        # Populate the Listbox with options
        for option in options:
            lstbox.insert(tk.END, option)

        ttk.Button(plylst, text="Pick playlist", command=edit_sngs).pack()

    def delt():
        clear_frame(plylst)


    def pop_plylst():
        ttk.Label(plylst, text="Please select an option:").grid(column = 1, row = 0, padx = 10, pady = 10)
        ttk.Button(plylst, text="Create a playlist", command=create_plylst).grid(column = 0, row=1, padx=5, pady=5)
        ttk.Button(plylst, text="Edit songs in playlist", command=lambda: edt_plylst(root)).grid(column=1, row=1, padx=5, pady=5)
        ttk.Button(plylst, text="Delete playlist", command=delt).grid(column=2, row=1, padx=5, pady=5)

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
        elif selected_tab == "Playlist edit":
            clear_frame(plylst)
            root.geometry("400x150")
            pop_plylst()
            

    # Bind the tab change event
    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

    root.geometry("300x200")
    root.mainloop()

repeat = True
while repeat:
    repeat = main(repeat)