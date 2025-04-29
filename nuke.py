import keyboard
import time
import mouse
import threading
from pynput.mouse import Listener, Button, Controller
import pygetwindow as gw

# Mouse controller instance
mouse_controller = Controller()

# Function to block left mouse clicks
def block_mouse_clicks():
    def on_click(x, y, button, pressed):
        if button == Button.left and pressed:
            # Move the mouse back to its current position to suppress the click
            mouse_controller.position = (x, y)
            return False  # Suppress the left-click event
        return True  # Allow other mouse events

    with Listener(on_click=on_click) as listener:
        listener.join()

def get_chrome_window_position():
    windows = gw.getWindowsWithTitle("Google Chrome")
    if windows:
        chrome_window = windows[0]  # Assume the first match is the desired window
        return chrome_window.left + chrome_window.width // 2, chrome_window.top + chrome_window.height // 2
    return None

# Function to lock the mouse in place
def lock_mouse():
    fixed_position = (500, 500)  # Adjust as needed
    while True:
        mouse_controller.position = fixed_position
        time.sleep(0.01)  # Small delay to reduce CPU usage

# Main function
def main():
    # Start the mouse-locking thread
    mouse_thread = threading.Thread(target=lock_mouse, daemon=True)
    mouse_thread.start()

    # Start the mouse-click-blocking thread
    click_block_thread = threading.Thread(target=block_mouse_clicks, daemon=True)
    click_block_thread.start()

    # Keep the program running
    while True:
        time.sleep(1)

main()