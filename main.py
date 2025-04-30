# Main file, mostly vincent ngl

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from audio import *
import time

def main(repeat):
    root = tk.Tk()
    root.title("Main Window")
    is_sliding = False
    ply = False
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

    notebook.add(menu, text="Menu")
    notebook.add(ply_sng, text="Music Player")
    notebook.add(plylst, text="Playlist edit")
    notebook.pack(expand=True, fill="both")

    # Function to populate the "menu" frame
    def populate_menu():
        ttk.Label(menu, text="Welcome to Music Player!\nSelect a tab to continue").pack(pady=5)

    # Populate the "menu" frame initially
    populate_menu()

    def pick_plylst(root):

        def clear_frame(frame):
            print(f"Clearing frame: {frame}")  # Debugging: Print which frame is being cleared
            for widget in frame.winfo_children():
                print(f"Destroying widget: {widget}")  # Debugging: Print each widget being destroyed
                widget.destroy()

        clear_frame(ply_sng)
        root.geometry("")

        def pck():
            nme = lstbox.curselection()
            clear_frame(ply_sng)
            # This is someone else's ############################################################################################
            pop_audio(root, ply)
        options = ["option 1", "option 2", "option 3"] #Integrate this with everything else ###################################################################################

        # Scrollbar
        scrollbar = tk.Scrollbar(ply_sng, orient='vertical')
        scrollbar.pack(side='right', fill='y')

        # Listbox
        lstbox = tk.Listbox(
            ply_sng,
            selectmode='single',
            yscrollcommand=scrollbar.set
        )
        lstbox.pack(side='left', fill='both', expand=True)

        # Configure the scrollbar to work with the Listbox
        scrollbar.config(command=lstbox.yview)

        # Populate the Listbox with options
        for option in options:
            lstbox.insert(tk.END, option)

        ttk.Button(ply_sng, text="Pick playlist", command=pck).pack()
    pick_plylst(root)

    def pop_audio(root, ply):
        ply = True
        root.geometry("")
        clear_frame(ply_sng)  # Clear the previous content of the audio tab
        attention = ("Helvetica", 20, "bold")

        # Add a label for the music playing tab
        ttk.Label(ply_sng, text="Music Playing Tab").grid(row=0, column=1, padx=10, pady=10, columnspan=3)

        # State variable to track whether the song is sliding
        is_sliding = {"value": False}

        # Function to handle play/pause button
        def ply(pse_ply, file_path, is_sliding):
            if pse_ply["text"] == "▶":  # If the button shows "play"
                pse_ply["text"] = "⏸"  # Change to "pause"
                is_sliding["value"] = True  # Set is_sliding to True
                play_song(pse_ply, file_path)  # Play the song
            else:  # If the button shows "pause"
                pse_ply["text"] = "▶"  # Change to "play"
                is_sliding["value"] = False  # Set is_sliding to False
                play_song(pse_ply, file_path)  # Pause the song (you need to implement this function)

        # Play/Pause button
        pse_ply = tk.Button(
            ply_sng,
            text="▶",
            command=lambda: ply(pse_ply, "Audio/normal sound effect.wav", is_sliding),
            font=attention,
        )
        pse_ply.grid(row=1, column=1, padx=10, pady=10)

        # Volume label and slider
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

        # Speed label and slider
        speed_label = ttk.Label(ply_sng, text="Speed: 1x", font=("Helvetica", 14))
        speed_label.grid(row=4, column=1, padx=10, pady=5)  # Centered in column 1

        speed_slider = ttk.Scale(
            ply_sng,
            from_=0.5,
            to=2.0,
            orient="horizontal",
            length=200,
            command=lambda value: change_speed(speed_slider, speed_label),
        )
        speed_slider.set(1.0)
        speed_slider.grid(row=5, column=1, padx=10, pady=5)

                # Add a dynamic slider to the "Music Player" tab
        def add_dynamic_slider_to_music_player(is_sliding):
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
                -handle_radius,
                0,
                handle_radius,
                canvas_height,
                fill="blue",
                outline="",
            )

            # State to track the slider's position and whether it's sliding
            slider_state = {"current_width": 0, "is_sliding": False, "timer": None}

            # Function to update the slider position
            def update_slider():
                if is_sliding["value"]:  # Check if the slider should move
                    slider_state["is_sliding"] = True  # Mark as sliding
                    slider_state["current_width"] += 1  # Increment the slider position

                    # Stop sliding if the slider reaches the end
                    if slider_state["current_width"] >= canvas_width:
                        slider_state["current_width"] = canvas_width
                        is_sliding["value"] = False  # Stop sliding

                    # Update the slider's position
                    canvas.coords(blue_bar, 0, 0, slider_state["current_width"], canvas_height)
                    canvas.coords(
                        handle,
                        slider_state["current_width"] - handle_radius,
                        0,
                        slider_state["current_width"] + handle_radius,
                        canvas_height,
                    )

                    # Schedule the next update
                    slider_state["timer"] = ply_sng.after(1000, update_slider)  # Update every 1 second
                else:
                    slider_state["is_sliding"] = False  # Mark as not sliding

            # Function to start the slider
            def start_slider():
                if not slider_state["is_sliding"]:  # Prevent multiple timers
                    update_slider()

            # Function to stop the slider
            def stop_slider():
                if slider_state["timer"]:
                    ply_sng.after_cancel(slider_state["timer"])  # Cancel the timer
                    slider_state["timer"] = None
                slider_state["is_sliding"] = False

            # Bind the slider to start and stop events
            canvas.bind("<Button-1>", lambda event: start_slider())  # Start sliding on click
            canvas.bind("<ButtonRelease-1>", lambda event: stop_slider())  # Stop sliding on release

            # Start updating the slider
            start_slider()

        # Initialize the sliding state
        is_sliding = {"value": False}

        # Add the dynamic slider to the "Music Player" tab
        add_dynamic_slider_to_music_player(is_sliding)


    def create_plylst(root):
        clear_frame(plylst)
        nme = tk.StringVar()

        def slct_sngs():
            print(f"Playlist name: {nme.get()}")  # Debugging: Print the playlist name
            clear_frame(plylst)
            root.geometry("")
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

        root.geometry("")

        def edit_sngs(option):
            nme = lstbox.curselection()
            clear_frame(plylst)
            root.geometry("")
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
        root.geometry("")

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
        root.geometry("")
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
    # Function to handle tab changes
    def on_tab_changed(event, root, ply):
        selected_tab = notebook.tab(notebook.select(), "text")
        print(f"Tab changed to: {selected_tab}")  # Debugging: Print the selected tab

        if selected_tab == "Menu":
            if not menu.winfo_children():  # Only repopulate if the frame is empty
                populate_menu()
        elif selected_tab == "Music Player":
            if ply == True:
                root.update_idletasks()  # Update the geometry based on the widgets
                root.geometry("")  # Let Tkinter automatically resize the window
        elif selected_tab == "Playlist edit":
            clear_frame(plylst)
            pop_plylst()
            root.update_idletasks()  # Update the geometry based on the widgets
            root.geometry("")  # Let Tkinter automatically resize the window
            

    # Bind the tab change event
    notebook.bind("<<NotebookTabChanged>>", lambda event: on_tab_changed(event, root, ply))

    root.geometry("")
    root.mainloop()

repeat = True
while repeat:
    repeat = main(repeat)