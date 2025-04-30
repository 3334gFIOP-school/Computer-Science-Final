# Main file, mostly vincent ngl

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from audio import *
import time

def main(repeat):
    root = tk.Tk()
    root.title("Main Window")

    class MultiSelectListbox(tk.Frame):
        def __init__(self, master, options, nme, preselected_indices=None, **kwargs):
            super().__init__(master, **kwargs)
            self.options = options
            self.nme = nme
            print(f"Playlist name: {self.nme}")  # Debugging: Print the playlist name

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
            # Print items in the terminal
            selected_indices = self.listbox.curselection()
            selected = [self.listbox.get(i) for i in selected_indices]
            export = [str(self.nme), selected] #['Playlist name', ['song1','song2'...]]
            print(f"Selected items: {selected}")
            try:
                # Export ans save here
                pass
                messagebox.showerror(title="Export", message=f"Saved {self.nme} playlist")
                clear_frame(plylst)
                pop_plylst()
                
            except Exception as e:
                messagebox.showerror(title="Export", message=f"Failed to save {self.nme} playlist")

        def clear_selection(self):
            # Clear all selections in the Listbox
            self.listbox.selection_clear(0, tk.END)

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
        command=lambda: play_song(pse_ply, "Audio/normal sound effect.wav"),
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
        from_=0.10,
        to=5.00,
        orient="horizontal",
        length=200,
        command=lambda value: change_speed(speed_slider, speed_label),
    )
    speed_slider.set(1)
    speed_slider.grid(row=5, column=1, padx=10, pady=5)  # Centered in column 1

    # Add a dynamic slider to the "Music Player" tab
    def add_dynamic_slider_to_music_player():
        # Create a frame to hold the custom slider
        slider_frame = tk.Frame(ply_sng, bg="white")  # White background
        slider_frame.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Canvas for the custom slider
        canvas_width = 300
        canvas_height = 20
        canvas = tk.Canvas(slider_frame, width=canvas_width, height=canvas_height, bg="white", highlightthickness=0)
        canvas.pack()

        # Create the lighter blue progress bar rectangle
        blue_bar = canvas.create_rectangle(0, 0, 0, canvas_height, fill="lightblue", width=0)

        # Create the slider handle (circle)
        handle_radius = 10
        handle = canvas.create_oval(
            0 - handle_radius, 0, handle_radius, canvas_height, fill="white", outline="black"
        )

        # Add a label to display the slider value
        slider_value_label = tk.Label(slider_frame, text="Value: 0", font=("Helvetica", 14), bg="white")
        slider_value_label.pack(pady=10)

        # Variables to track progress
        current_progress = 0
        song_duration = 100  # Example song duration in seconds (adjust as needed)
        is_sliding = False  # Flag to track if the user is manually sliding the handle

        # Function to update the slider dynamically
        def update_slider():
            nonlocal current_progress
            if not is_sliding:  # Only update if the user is not sliding
                if current_progress <= song_duration:
                    # Calculate the x-coordinate for the progress
                    x = (current_progress / song_duration) * canvas_width
                    # Update the lighter blue progress bar width
                    canvas.coords(blue_bar, 0, 0, x, canvas_height)
                    # Update the handle position
                    canvas.coords(handle, x - handle_radius, 0, x + handle_radius, canvas_height)
                    # Update the slider value label
                    slider_value_label.config(text=f"Value: {current_progress}")
                    # Increment the progress
                    current_progress += 1
                    # Schedule the next update in 1 second
                    ply_sng.after(1000, update_slider)

        # Function to handle manual sliding
        def on_slide(event):
            nonlocal is_sliding, current_progress
            is_sliding = True  # User is sliding
            # Get the x-coordinate of the mouse click, constrained to the canvas width
            x = max(0, min(event.x, canvas_width))
            # Update the lighter blue progress bar width
            canvas.coords(blue_bar, 0, 0, x, canvas_height)
            # Update the handle position
            canvas.coords(handle, x - handle_radius, 0, x + handle_radius, canvas_height)
            # Calculate the slider value (0-100) based on the x-coordinate
            current_progress = int((x / canvas_width) * song_duration)
            slider_value_label.config(text=f"Value: {current_progress}")

        # Function to handle when the user releases the slider
        def on_release(event):
            nonlocal is_sliding
            is_sliding = False  # User has stopped sliding
            update_slider()  # Resume automatic updates

        # Bind mouse events to the canvas
        canvas.bind("<B1-Motion>", on_slide)  # Dragging the slider
        canvas.bind("<Button-1>", on_slide)   # Clicking on the slider
        canvas.bind("<ButtonRelease-1>", on_release)  # Releasing the slider

        # Start the slider update loop
        update_slider()

    # Call the function to add the dynamic slider to the "Music Player" tab
    add_dynamic_slider_to_music_player()

    # Add widgets to the "test_tab" frame
    ttk.Label(test_tab, text="Test Tab with Custom Slider").grid(row=0, column=0, padx=10, pady=10)

    # Create a frame to hold the custom slider
    slider_frame = tk.Frame(test_tab, bg="white")  # White background
    slider_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    # Canvas for the custom slider
    canvas_width = 300
    canvas_height = 20
    canvas = tk.Canvas(slider_frame, width=canvas_width, height=canvas_height, bg="white", highlightthickness=0)
    canvas.pack()

    # Create the lighter blue progress bar rectangle
    blue_bar = canvas.create_rectangle(0, 0, 0, canvas_height, fill="lightblue", width=0)

    # Create the slider handle (circle)
    handle_radius = 10
    handle = canvas.create_oval(
        0 - handle_radius, 0, handle_radius, canvas_height, fill="white", outline="black"
    )

    # Add a label to display the slider value
    slider_value_label = tk.Label(slider_frame, text="Value: 50", font=("Helvetica", 14), bg="white")
    slider_value_label.pack(pady=10)

    # Function to update the lighter blue progress bar and handle position
    def update_slider(event):
        # Get the x-coordinate of the mouse click, constrained to the canvas width
        x = max(0, min(event.x, canvas_width))
        # Update the lighter blue progress bar width
        canvas.coords(blue_bar, 0, 0, x, canvas_height)
        # Update the handle position
        canvas.coords(handle, x - handle_radius, 0, x + handle_radius, canvas_height)
        # Calculate the slider value (0-100) based on the x-coordinate
        value = int((x / canvas_width) * 100)
        slider_value_label.config(text=f"Value: {value}")

    # Bind mouse events to the canvas
    canvas.bind("<B1-Motion>", update_slider)  # Dragging the slider
    canvas.bind("<Button-1>", update_slider)   # Clicking on the slider

    # Restore the theme
    style = ttk.Style()
    style.theme_use("clam")  # Restore the "clam" theme
    style.configure(
        "Custom.Horizontal.TScale",
        troughcolor="#e0e0e0",  # Background color of the trough
        sliderthickness=5,     # Thickness of the slider
        background="#4caf50",   # Color of the slider
    )

    def create_plylst(root):
        clear_frame(plylst)
        nme = tk.StringVar()

        def slct_sngs():
            print(f"Playlist name: {nme.get()}")  # Debugging: Print the playlist name
            clear_frame(plylst)
            root.geometry("400x400")
            options = [] #Figure out how to integrate this later ===========================================================

            # Create and pack the MultiSelectListbox
            listbox = MultiSelectListbox(plylst, options, nme.get())
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

        def edit_sngs(option):
            nme = lstbox.curselection()
            clear_frame(plylst)
            #root.geometry("400x150")
            nme = option[nme[0]]

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

        option = ["option 1", "option 2", "option 3"] #Integrate this with everything else ###################################################################################

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
        for optio in option:
            lstbox.insert(tk.END, optio)

        ttk.Button(plylst, text="Pick playlist", command=lambda: edit_sngs(option)).pack()

    def delt(root):
        clear_frame(plylst)
        root.geometry("400x400")

        def del_plylst():
            nme = lstbox.curselection()
            clear_frame(plylst)
            # This is someone else's ############################################################################################
            pop_plylst()
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

        ttk.Button(plylst, text="Pick playlist", command=del_plylst).pack()

    def show_plylst(root):
        clear_frame(plylst)
        root.geometry("400x400")
        def show_songs():
            nme = lstbox.curselection()
            clear_frame(plylst)

            def back():
                clear_frame(plylst)
                pop_plylst()


            options = ["option 1", "option 2", "option 3"] #Integrate this with everything else ###################################################################################

            # Scrollbar
            scrollbar = tk.Scrollbar(plylst, orient='vertical')
            scrollbar.pack(side='right', fill='y')

            # Listbox
            ltbox = tk.Listbox(
                plylst,
                selectmode='readonly',
                yscrollcommand=scrollbar.set
            )
            ltbox.pack(side='left', fill='both', expand=True)

            # Configure the scrollbar to work with the Listbox
            scrollbar.config(command=ltbox.yview)

            # Populate the Listbox with options
            for option in options:
                ltbox.insert(tk.END, option)

            ttk.Button(plylst, text="Go back", command=back).pack()
            
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

        ttk.Button(plylst, text="Pick playlist", command=show_songs).pack()



    def pop_plylst():
        ttk.Label(plylst, text="Please select an option:").grid(column = 1, row = 0, padx = 10, pady = 10)
        ttk.Button(plylst, text="Create a playlist", command=lambda: create_plylst(root)).grid(column = 0, row=1, padx=5, pady=5)
        ttk.Button(plylst, text="Edit songs in playlist", command=lambda: edt_plylst(root)).grid(column=1, row=1, padx=5, pady=5)
        ttk.Button(plylst, text="Delete playlist", command=lambda: delt(root)).grid(column=2, row=1, padx=5, pady=5)
        ttk.Button(plylst, text="Show songs in playlist", command=lambda: show_plylst(root)).grid(column=1, row=2, padx=5, pady=5)

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
            root.geometry("350x350")
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