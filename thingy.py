import mouse
import keyboard
import time

print("starting...")

while True:
    if keyboard.is_pressed('\\'):
        while True:
            mouse.click()
            time.sleep(0)

            if keyboard.is_pressed('q'):
                break
    if keyboard.is_pressed('esc'):
        break