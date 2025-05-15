def update_progress_bar(playback_progress, playback_label, total_length, is_playing, playback_position=0):
    """
    Updates the playback progress bar and label dynamically.
    """
    from audio import is_playing

    # Store the ID of the scheduled `after` call
    if not hasattr(update_progress_bar, "after_id"):
        update_progress_bar.after_id = None

    if is_playing:
        # Cancel any previously scheduled `after` call
        if update_progress_bar.after_id is not None:
            playback_label.after_cancel(update_progress_bar.after_id)

        playback_progress["value"] = (playback_position / total_length) * 100  # Update progress bar
        playback_label.config(text=f"Position: {int(playback_position)}s")  # Update the playback label with the current position

        # Schedule the function to run again after 1 second
        if playback_position < total_length:
            update_progress_bar.after_id = playback_label.after(
                1000,
                update_progress_bar,
                playback_progress,
                playback_label,
                total_length,
                is_playing,
                playback_position + 1,  # Increment playback position
            )
        else:
            print("Playback complete")
            playback_label.config(text="Playback complete")
            playback_progress["value"] = 100  # Set progress bar to 100%
            update_progress_bar.after_id = None  # Reset the `after_id` when complete
    else:
        # Cancel any previously scheduled `after` call
        if update_progress_bar.after_id is not None:
            playback_label.after_cancel(update_progress_bar.after_id)
            update_progress_bar.after_id = None

        playback_label.config(text=f"Paused at: {int(playback_position)}s")  # Update label when paused

    # Return the updated playback position
    return playback_position