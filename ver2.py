import sys
import customtkinter as ctk
from tkinter import messagebox

# Configuration
# 1 minute * 60 seconds * 1000 ms
INTERVAL = 5000


def alerta():
    root.bell()
    # Standard messagebox used because CustomTkinter doesn't have a native popup yet
    raspuns = messagebox.askyesno("Pauza", "Take a rest! \n\nVrei să continui sesiunea?")

    if raspuns:
        root.after(INTERVAL, alerta)
    else:
        root.destroy()
        sys.exit()


def inceput():
    root.withdraw()  # Hides the window
    root.after(INTERVAL, alerta)


# --- UI Setup ---
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Focus Reminder")
root.geometry("400x280")

# Title
label = ctk.CTkLabel(
    root,
    text="Work Session",
    font=ctk.CTkFont(family="Arial", size=24, weight="bold")
)
label.pack(pady=(40, 10))

# Description
desc_label = ctk.CTkLabel(
    root,
    text="Click start to begin the interval.\nThe app will hide and alert you later.",
    text_color="gray70"
)
desc_label.pack(pady=(0, 40))

# Modern Button
button = ctk.CTkButton(
    root,
    text="Start Timer",
    width=160,
    height=40,
    corner_radius=8,
    font=ctk.CTkFont(size=15, weight="bold"),
    command=inceput
)
button.pack()

root.mainloop()