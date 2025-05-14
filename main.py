# Main file, mostly vincent ngl

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from audio import *
from save_load import *
import time

def main(repeat):
    #variable, dictoinary that stores playlists and songs
    playlists = load_to_playlists('songs.csv')
    
    root = tk.Tk()
    root.title("Main Window")
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

            #update playlists, adding and removing songs
            playlists[export[0]] = []
            for i in export[1]:
                playlists[export[0]].append(list(i))

            print(playlists)
            playlists_to_save(playlists, 'songs.csv')

            
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
        from audio import stop_song
        stop_song()
        return repeat
    # Set the window to be resizable

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
            pop_audio(root, ply, "Audio\\normal sound effect.wav", nme) # Make the file path an actual variable that becomes the link from a selection from the playlist in a menu ==================================================================================================================================================================
        options = playlist_names(playlists) #get playlist names ###################################################################################            EEEEEEEEEEEEEEEE

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

    def pop_audio(root, ply, file_path, nme):
        from audio import play_song, stop_song, set_volume, get_song_length
        from utils import update_progress_bar

        playback_position = 0  # Initialize playback position

        ply = False
        root.geometry("")
        clear_frame(ply_sng)  # Clear the previous content of the audio tab
        attention = ("Helvetica", 20, "bold")  # Define the font style for buttons

        # Add a label for the music playing tab
        ttk.Label(ply_sng, text="Music Playing Tab").grid(row=0, column=1, padx=10, pady=10)

        # Volume slider and label
        volume_label = ttk.Label(ply_sng, text="Volume: 50%", font=("Helvetica", 14))
        volume_label.grid(row=2, column=1, padx=10, pady=5)

        volume_slider = ttk.Scale(
            ply_sng,
            from_=0.5,
            to=2,
            orient="horizontal",
            length=1,
            command=lambda value: set_volume(value, volume_label),  # Calls set_volume from audio.py
        )
        volume_slider.set(0.5)
        volume_slider.grid(row=3, column=1, padx=10, pady=5)

        # Speed label and slider
        speed_label = ttk.Label(ply_sng, text="Speed: 1x", font=("Helvetica", 14))
        speed_label.grid(row=4, column=1, padx=10, pady=5)

        from audio import change_speed  # Import change_speed from audio.py
        speed_slider = ttk.Scale(
            ply_sng,
            from_=0.5,
            to=2.0,
            orient="horizontal",
            length=200,
            command=lambda value: change_speed(value, speed_label),  # Calls change_speed function
        )
        speed_slider.set(1.0)
        speed_slider.grid(row=5, column=1, padx=10, pady=5)

        # Playback position progress bar and label
        playback_label = ttk.Label(ply_sng, text="Position: 0s", font=("Helvetica", 14))
        playback_label.grid(row=6, column=1, padx=10, pady=5)

        # Create a blue progress bar for playback position
        style = ttk.Style()
        style.configure("blue.Horizontal.TProgressbar", troughcolor="white", background="blue")

        playback_progress = ttk.Progressbar(
            ply_sng,
            orient="horizontal",
            length=300,
            mode="determinate",
            style="blue.Horizontal.TProgressbar",  # Use the custom blue style
        )
        playback_progress.grid(row=7, column=1, padx=10, pady=10)

        # Start updating the progress bar when playback starts
        total_length = get_song_length(file_path)  # Get the total length of the song
        update_progress_bar(playback_progress, playback_label, total_length, is_playing)
        # Play/Pause button
        pse_ply = tk.Button(
            ply_sng,
            text="▶",
            command=lambda: toggle_play_pause(pse_ply, file_path, lambda: update_progress_bar(playback_progress, playback_label, total_length, is_playing), playback_position, total_length, playlist_song_paths(playlists,list_playlists(playlists)[nme[0]])), # Alec this is where the function that finds the list of the songs in the playlist should go
            font=attention,
        )
        pse_ply.grid(row=1, column=1, padx=10, pady=10)

        # Toggle play/pause functionality
        def toggle_play_pause(button, file_path, progress, playback_position, total_length, list_of_songs):
            global is_playing
            print(f"Button clicked: {button['text']}")  # Debugging: Print the button text
            if button["text"] == "▶":
                is_playing = True
                play_song(button, file_path, list_of_songs, progress, playback_position, total_length)
                update_progress_bar(playback_progress, playback_label, total_length, is_playing)  # Pass the progress bar and label
            else:
                is_playing = False
                play_song(button, file_path, list_of_songs, progress, playback_position, total_length)

    def create_plylst(root): #function to create a playlist
        clear_frame(plylst)
        nme = tk.StringVar()

        def slct_sngs(): #select what songs are in the playlist
            print(f"Playlist name: {nme.get()}")  # Debugging: Print the playlist name
            clear_frame(plylst)
            root.geometry("")
            options = list_songs('songs.csv') #Figure out how to integrate this later ===========================================================

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
    
    def edt_plylst(root): #function to edit playlists
        clear_frame(plylst)

        root.geometry("")

        def edit_sngs(option): #edit songs in a playlist
            nme = lstbox.curselection()
            clear_frame(plylst)
            root.geometry("")
            nme = option[nme[0]]

            options = list_songs('songs.csv') #Figure out how to integrate this later ===========================================================
            preselected_indices = song_index('songs.csv', playlists, nme)  # Integrate this with everything else ###################################################################################

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

        option = playlist_names(playlists) #get playlist names ###################################################################################

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
            # populate box ############################################################################################
            pop_plylst()

            #remove selected playlists
            playlists.pop(playlist_names(playlists)[nme[0]])
            playlists_to_save(playlists, 'songs.csv')

        options = playlist_names(playlists) #Integrate this with everything else ###################################################################################               EEEEEEEEEEEEEEEEEE

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
        def show_songs(option):
            nme = lstbox.curselection()
            print(nme)
            clear_frame(plylst)

            def back():
                clear_frame(plylst)
                pop_plylst()


            options = playlist_songs(playlists, playlist_names(playlists)[nme[0]]) #get songs in the playlist ###################################################################################                 EEEEEEEEEEEEE

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
            
        options = playlist_names(playlists) #get playlist names ###################################################################################                     EEEEEEEEEEEEEEEEEEEEEEE

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

        ttk.Button(plylst, text="Pick playlist", command=lambda: show_songs(options)).pack()



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