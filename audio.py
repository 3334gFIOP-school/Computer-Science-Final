def play_song(pse_ply):
    current_text = pse_ply["text"]
    if current_text == "▶":
        # Adjust font size for "Pause" to make it visually similar to "Play"
        pse_ply.config(text="⏸", font=("Helvetica", 20, "bold"))  # Slightly smaller font for pause
    else:
        # Use a consistent font size for "Play"
        pse_ply.config(text="▶", font=("Helvetica", 20, "bold"))  # Slightly larger font for play

def fast_forward():
    pass
