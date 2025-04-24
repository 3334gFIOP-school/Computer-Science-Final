import tkinter as tk

root = tk.Tk()
frame = tk.Frame(root)
frame.pack(expand=True, fill="both")

volume_label = tk.Label(frame, text="Volume: 50%", font=("Helvetica", 14))
volume_label.grid(row=0, column=0, padx=10, pady=5)

def set_volume(value):
    volume_label.config(text=f"Volume: {int(float(value))}%")

volume_slider = tk.Scale(
    frame, from_=0, to=100, orient="horizontal", length=200, command=set_volume
)
volume_slider.set(50)
volume_slider.grid(row=1, column=0, padx=10, pady=5)

root.mainloop()