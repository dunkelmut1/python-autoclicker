import time
import threading
import customtkinter as ctk
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode

clicking = False
mouse = Controller()
HOTKEY_1 = KeyCode(char='w')
HOTKEY_2 = KeyCode(char="t")
pressed_keys = set()

def clicker():
    global time_int
    wait_time = time_int.get()
    while clicking:
        mouse.click(Button.left, 1)
        time.sleep(float(wait_time))

def start_clicker():
    global clicking
    if not clicking:
        clicking = True
        click_thread = threading.Thread(target=clicker)
        click_thread.start()
        status_label.configure(text="Auto-Clicker running...")

def stop_clicker():
    global clicking
    clicking = False
    status_label.configure(text="Auto-Clicker paused.")

def toggle_clicker(key):
    if key in [HOTKEY_1, HOTKEY_2]:
        pressed_keys.add(key)
        if HOTKEY_1 in pressed_keys and HOTKEY_2 in pressed_keys:
            if clicking:
                stop_clicker()
            else:
                start_clicker()

def release_key(key):
    if key in pressed_keys:
        pressed_keys.remove(key)

def start_listener():
    listener = Listener(on_press=toggle_clicker, on_release=release_key)
    listener.start()

app = ctk.CTk()
app.title("Auto-Clicker")
app.geometry("400x350")

status_label = ctk.CTkLabel(app, text="Auto-Clicker paused.")
status_label.pack(pady=20)

time_label = ctk.CTkLabel(app, text="Time interval")
time_label.pack(pady=1)

time_int = ctk.CTkEntry(app)
time_int.pack(pady=20)

start_button = ctk.CTkButton(app, text="Start Auto-Clicker", command=start_clicker)
start_button.pack(pady=10)

stop_button = ctk.CTkButton(app, text="Stop Auto-Clicker", command=stop_clicker)
stop_button.pack(pady=10)

exit_button = ctk.CTkButton(app, text="Exit", command=app.quit)
exit_button.pack(pady=10)

start_listener()

app.mainloop()
