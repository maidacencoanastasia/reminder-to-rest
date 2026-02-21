import sys
import threading
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item

# Configuration
INTERVAL = 5000
icon = None  # Initialize global icon variable


def create_icon_image():
    width, height = 64, 64
    image = Image.new('RGB', (width, height), (31, 83, 141))
    dc = ImageDraw.Draw(image)
    dc.ellipse((10, 10, 54, 54), fill=(255, 255, 255))
    return image


def quit_app(icon_param=None, item_param=None):
    global icon
    # If an icon was passed by pystray or exists globally, stop it
    if icon:
        icon.stop()

    # Close the Tkinter window and exit
    root.after(0, root.destroy)
    sys.exit()


def show_window(icon_param, item_param):
    global icon
    if icon:
        icon.stop()
        icon = None  # Reset so we don't try to stop it again
    root.after(0, root.deiconify)


def withdraw_to_tray():
    global icon
    root.withdraw()
    menu = (item('Show App', show_window), item('Quit', quit_app))
    icon = pystray.Icon("BreakReminder", create_icon_image(), "Break Reminder", menu)

    threading.Thread(target=icon.run, daemon=True).start()


def alerta():
    root.bell()
    # Bring hidden window focus for the popup
    raspuns = messagebox.askyesno("Pauza", "Take a rest! \n\nKeep the timer running?")
    if raspuns:
        root.after(INTERVAL, alerta)
    else:
        # Now this will use the global 'icon' safely
        quit_app()


def inceput():
    withdraw_to_tray()
    root.after(INTERVAL, alerta)


# --- UI Setup ---
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("Focus Timer")
root.geometry("400x250")

ctk.CTkLabel(root, text="Break Reminder", font=("Arial", 22, "bold")).pack(pady=(30, 10))
ctk.CTkLabel(root, text="App will minimize to the system tray.", text_color="gray").pack()

start_btn = ctk.CTkButton(
    root, text="Start Session",
    corner_radius=10,
    command=inceput
)
start_btn.pack(pady=40)

# Proper exit if X is clicked
root.protocol('WM_DELETE_WINDOW', quit_app)

root.mainloop()