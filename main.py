import sys
import tkinter as tk
from tkinter import messagebox

# minute * secunde * milisecunde
# INTERVAL = 1 * 60 * 1000
INTERVAL = 5000


def alerta():
    root.bell()
    raspuns = messagebox.askyesno("Pauza", "Take a rest! \n Pentru a inchide app press NO")
    if raspuns:
        root.after(INTERVAL, alerta)
    else:
        root.destroy()
        sys.exit()


def inceput():
    root.withdraw()
    root.after(INTERVAL, alerta)


root = tk.Tk()
root.geometry("500x300")
label = tk.Label(root, text="Reminder", font=("Arial", 20))
label.pack()
button = tk.Button(text="Start", width=20, command=inceput)
button.pack(pady=50)
root.mainloop()
