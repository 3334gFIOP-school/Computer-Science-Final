import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Custom Slider with Green Progress Bar")
    root.geometry("400x200")

    # Create a notebook
    notebook = tk.Frame(root)
    notebook.pack(expand=True, fill="both")

    # Add a new tab for the slider
    slider_tab = tk.Frame(notebook)
    slider_tab.pack(expand=True, fill="both")

    # Add a label to display the slider value
    slider_value_label = tk.Label(slider_tab, text="Value: 50", font=("Helvetica", 14))
    slider_value_label.pack(pady=20)

    # Create a frame to hold the custom slider
    slider_frame = tk.Frame(slider_tab)
    slider_frame.pack(pady=20)

    # Canvas for the custom slider
    canvas_width = 300
    canvas_height = 20
    canvas = tk.Canvas(slider_frame, width=canvas_width, height=canvas_height, bg="blue", highlightthickness=0)
    canvas.pack()

    # Create the green progress bar rectangle
    green_bar = canvas.create_rectangle(0, 0, 0, canvas_height, fill="green", width=0)

    # Create the slider handle (circle)
    handle_radius = 10
    handle = canvas.create_oval(
        0 - handle_radius, 0, handle_radius, canvas_height, fill="white", outline="black"
    )

    # Function to update the green progress bar and handle position
    def update_slider(event):
        # Get the x-coordinate of the mouse click, constrained to the canvas width
        x = max(0, min(event.x, canvas_width))
        # Update the green progress bar width
        canvas.coords(green_bar, 0, 0, x, canvas_height)
        # Update the handle position
        canvas.coords(handle, x - handle_radius, 0, x + handle_radius, canvas_height)
        # Calculate the slider value (0-100) based on the x-coordinate
        value = int((x / canvas_width) * 100)
        slider_value_label.config(text=f"Value: {value}")

    # Bind mouse events to the canvas
    canvas.bind("<B1-Motion>", update_slider)  # Dragging the slider
    canvas.bind("<Button-1>", update_slider)   # Clicking on the slider

    root.mainloop()

if __name__ == "__main__":
    main()