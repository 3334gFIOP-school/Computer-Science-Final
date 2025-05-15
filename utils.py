def update_progress_bar(playback_progress, playback_label, total_length, is_playing, playback_position=0):
    if is_playing:
        playback_position += 1  # Increment playback position by 1 second
        playback_progress["value"] = (playback_position / total_length) * 100  # Update progress bar
        playback_label.config(text=f"Position: {playback_position}s")  # Update the playback label with the current position

        # Schedule the function to run again after 1 second
        if playback_position < total_length:
            playback_label.after(
                1000,
                update_progress_bar,
                playback_progress,
                playback_label,
                total_length,
                is_playing,
                playback_position,
            )
    else:
        playback_label.config(text=f"Paused at: {playback_position}s")  # Update label when pauseddef update_progress_bar(playback_progress, playback_label, total_length, is_playing):