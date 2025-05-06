import tkinter as tk
from tkinter import messagebox
import mouse
import keyboard
import time
import threading

def start_auto_clicker():
    try:
        wait_time = float(wait_time_entry.get())
        activation_key = activation_key_entry.get()
        stop_key = stop_key_entry.get()
        quit_key = quit_key_entry.get()

        if not activation_key or not stop_key or not quit_key:
            messagebox.showerror("Error", "All key fields must be filled!")
            return

        def auto_clicker():
            while True:
                # Check if the quit key is pressed
                if keyboard.is_pressed(quit_key):
                    root.destroy()  # Close the Tkinter window
                    raise SystemExit  # Quit the program

                # Check if the activation key is pressed
                if keyboard.is_pressed(activation_key):
                    while True:
                        # Perform the mouse click
                        mouse.click()
                        time.sleep(wait_time)

                        # Check if the stop key is pressed
                        if keyboard.is_pressed(stop_key):
                            break

                        # Check if the quit key is pressed (to exit completely)
                        if keyboard.is_pressed(quit_key):
                            root.destroy()  # Close the Tkinter window
                            raise SystemExit  # Quit the program

                # Add a small delay to prevent high CPU usage
                time.sleep(0.01)

        # Run the auto clicker in a separate thread
        threading.Thread(target=auto_clicker, daemon=True).start()
        messagebox.showinfo("Info", "Auto clicker started! Use the keys to control it.")
    except ValueError:
        messagebox.showerror("Error", "Wait time must be a valid number!")

# Create the main Tkinter window
root = tk.Tk()
root.title("Auto Clicker")

# Wait time input
tk.Label(root, text="Wait Time (seconds):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
wait_time_entry = tk.Entry(root)
wait_time_entry.grid(row=0, column=1, padx=10, pady=5)

# Activation key input
tk.Label(root, text="Activation Key:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
activation_key_entry = tk.Entry(root)
activation_key_entry.grid(row=1, column=1, padx=10, pady=5)

# Stop key input
tk.Label(root, text="Stop Key:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
stop_key_entry = tk.Entry(root)
stop_key_entry.grid(row=2, column=1, padx=10, pady=5)

# Quit key input
tk.Label(root, text="Quit Key:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
quit_key_entry = tk.Entry(root)
quit_key_entry.grid(row=3, column=1, padx=10, pady=5)

# Start button
start_button = tk.Button(root, text="Start Auto Clicker", command=start_auto_clicker)
start_button.grid(row=4, column=0, columnspan=2, pady=10)

# Run the Tkinter event loop
root.mainloop()