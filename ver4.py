import sys
import json
import threading
import time
import random
import winsound
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List
import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item

# Configuration files
CONFIG_FILE = "reminder_config.json"
STATS_FILE = "reminder_stats.json"
HISTORY_FILE = "reminder_history.json"

class ReminderConfig:
    """Manages application configuration"""
    
    DEFAULT_CONFIG = {
        "intervals": {
            "Short Break": 5,  # 5 seconds for testing
            "Pomodoro": 25 * 60,
            "Long Break": 30 * 60,
            "Custom": 20 * 60
        },
        "current_interval": "Short Break",
        "messages": [
            "Time for a break! 🎯",
            "Take a moment to rest your eyes 👀",
            "Stretch and hydrate! 💧",
            "Step away from the screen 🚶‍♀️",
            "Deep breath, you've got this! 🧘‍♂️"
        ],
        "break_activities": [
            "Take 5 deep breaths",
            "Do some neck stretches", 
            "Walk around for 2 minutes",
            "Drink a glass of water",
            "Look at something 20 feet away",
            "Do 10 jumping jacks",
            "Practice good posture"
        ],
        "sound_enabled": True,
        "sound_file": "",  # Custom sound file path
        "auto_continue": False,
        "show_activity_suggestion": True
    }
    
    def __init__(self):
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        try:
            if Path(CONFIG_FILE).exists():
                with open(CONFIG_FILE, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults to handle missing keys
                    config = self.DEFAULT_CONFIG.copy()
                    config.update(loaded)
                    return config
            return self.DEFAULT_CONFIG.copy()
        except Exception:
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception:
            pass
    
    def get(self, key: str, default=None):
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        self.config[key] = value
        self.save_config()

class ReminderStats:
    """Manages usage statistics"""
    
    def __init__(self):
        self.stats = self.load_stats()
    
    def load_stats(self) -> Dict:
        try:
            if Path(STATS_FILE).exists():
                with open(STATS_FILE, 'r') as f:
                    return json.load(f)
            return {
                "total_sessions": 0,
                "total_breaks": 0,
                "total_work_time": 0,  # in seconds
                "longest_session": 0,
                "average_session": 0,
                "last_session": None
            }
        except Exception:
            return {}
    
    def save_stats(self):
        try:
            with open(STATS_FILE, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception:
            pass
    
    def log_session_start(self):
        self.session_start = datetime.now()
    
    def log_break_taken(self):
        if hasattr(self, 'session_start'):
            session_duration = (datetime.now() - self.session_start).total_seconds()
            
            self.stats["total_sessions"] += 1
            self.stats["total_breaks"] += 1
            self.stats["total_work_time"] += session_duration
            
            if session_duration > self.stats.get("longest_session", 0):
                self.stats["longest_session"] = session_duration
            
            # Update average
            self.stats["average_session"] = (
                self.stats["total_work_time"] / self.stats["total_sessions"]
            )
            
            self.stats["last_session"] = datetime.now().isoformat()
            self.save_stats()

class ReminderHistory:
    """Manages notification history"""
    
    def __init__(self):
        self.history = self.load_history()
    
    def load_history(self) -> List[Dict]:
        try:
            if Path(HISTORY_FILE).exists():
                with open(HISTORY_FILE, 'r') as f:
                    return json.load(f)
            return []
        except Exception:
            return []
    
    def save_history(self):
        try:
            with open(HISTORY_FILE, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception:
            pass
    
    def add_entry(self, message: str, activity: str = "", action: str = "continue"):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "activity": activity,
            "action": action
        }
        self.history.append(entry)
        
        # Keep only last 100 entries
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        self.save_history()

class SettingsWindow:
    """Settings configuration GUI"""
    
    def __init__(self, parent, config: ReminderConfig):
        self.parent = parent
        self.config = config
        self.window = None
    
    def show(self):
        if self.window and self.window.winfo_exists():
            self.window.focus()
            return
        
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title("Reminder Settings")
        self.window.geometry("600x700")
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Notebook for tabs
        self.notebook = ctk.CTkTabview(self.window)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create tabs
        self.create_intervals_tab()
        self.create_messages_tab()
        self.create_activities_tab()
        self.create_sounds_tab()
        
        # Save/Cancel buttons
        button_frame = ctk.CTkFrame(self.window)
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(
            button_frame, text="Save", 
            command=self.save_settings
        ).pack(side="right", padx=(10, 0))
        
        ctk.CTkButton(
            button_frame, text="Cancel",
            command=self.window.destroy
        ).pack(side="right")
    
    def create_intervals_tab(self):
        tab = self.notebook.add("Intervals")
        
        ctk.CTkLabel(tab, text="Time Intervals", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.interval_vars = {}
        intervals = self.config.get("intervals", {})
        
        for name, seconds in intervals.items():
            frame = ctk.CTkFrame(tab)
            frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(frame, text=f"{name}:").pack(side="left", padx=10)
            
            var = ctk.StringVar(value=str(seconds // 60 if seconds >= 60 else seconds))
            self.interval_vars[name] = var
            
            entry = ctk.CTkEntry(frame, textvariable=var, width=100)
            entry.pack(side="right", padx=10)
            
            unit_text = "minutes" if seconds >= 60 else "seconds"
            ctk.CTkLabel(frame, text=unit_text).pack(side="right")
    
    def create_messages_tab(self):
        tab = self.notebook.add("Messages")
        
        ctk.CTkLabel(tab, text="Reminder Messages", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.messages_text = ctk.CTkTextbox(tab, height=300)
        self.messages_text.pack(fill="both", expand=True, pady=10)
        
        # Load current messages
        messages = self.config.get("messages", [])
        self.messages_text.insert("1.0", "\n".join(messages))
        
        ctk.CTkLabel(
            tab, 
            text="Enter one message per line",
            text_color="gray"
        ).pack()
    
    def create_activities_tab(self):
        tab = self.notebook.add("Activities")
        
        ctk.CTkLabel(tab, text="Break Activities", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.activities_text = ctk.CTkTextbox(tab, height=300)
        self.activities_text.pack(fill="both", expand=True, pady=10)
        
        # Load current activities
        activities = self.config.get("break_activities", [])
        self.activities_text.insert("1.0", "\n".join(activities))
        
        ctk.CTkLabel(
            tab,
            text="Enter one activity per line",
            text_color="gray"
        ).pack()
    
    def create_sounds_tab(self):
        tab = self.notebook.add("Sound")
        
        ctk.CTkLabel(tab, text="Sound Settings", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Sound enabled checkbox
        self.sound_enabled = ctk.BooleanVar(value=self.config.get("sound_enabled", True))
        ctk.CTkCheckBox(
            tab, 
            text="Enable sound notifications",
            variable=self.sound_enabled
        ).pack(pady=10)
        
        # Custom sound file
        sound_frame = ctk.CTkFrame(tab)
        sound_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(sound_frame, text="Custom Sound File:").pack(anchor="w")
        
        file_frame = ctk.CTkFrame(sound_frame)
        file_frame.pack(fill="x", pady=5)
        
        self.sound_file = ctk.StringVar(value=self.config.get("sound_file", ""))
        ctk.CTkEntry(
            file_frame, 
            textvariable=self.sound_file,
            placeholder_text="Leave empty for system beep"
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(
            file_frame,
            text="Browse",
            command=self.browse_sound_file,
            width=80
        ).pack(side="right")
    
    def browse_sound_file(self):
        filename = filedialog.askopenfilename(
            title="Select Sound File",
            filetypes=[("Audio files", "*.wav *.mp3 *.ogg"), ("All files", "*.*")]
        )
        if filename:
            self.sound_file.set(filename)
    
    def save_settings(self):
        # Save intervals
        intervals = {}
        for name, var in self.interval_vars.items():
            try:
                value = int(var.get())
                # Convert to seconds (assume minutes for values > 60)
                intervals[name] = value * 60 if value > 60 or name != "Short Break" else value
            except ValueError:
                messagebox.showerror("Error", f"Invalid interval value for {name}")
                return
        
        self.config.set("intervals", intervals)
        
        # Save messages
        messages_text = self.messages_text.get("1.0", "end-1c")
        messages = [msg.strip() for msg in messages_text.split("\n") if msg.strip()]
        self.config.set("messages", messages)
        
        # Save activities
        activities_text = self.activities_text.get("1.0", "end-1c")
        activities = [act.strip() for act in activities_text.split("\n") if act.strip()]
        self.config.set("break_activities", activities)
        
        # Save sound settings
        self.config.set("sound_enabled", self.sound_enabled.get())
        self.config.set("sound_file", self.sound_file.get())
        
        messagebox.showinfo("Success", "Settings saved successfully!")
        self.window.destroy()

class StatsWindow:
    """Statistics display window"""
    
    def __init__(self, parent, stats: ReminderStats):
        self.parent = parent
        self.stats = stats
        self.window = None
    
    def show(self):
        if self.window and self.window.winfo_exists():
            self.window.focus()
            return
        
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title("Usage Statistics")
        self.window.geometry("400x500")
        self.window.transient(self.parent)
        
        # Title
        ctk.CTkLabel(
            self.window, 
            text="Usage Statistics", 
            font=("Arial", 20, "bold")
        ).pack(pady=20)
        
        # Stats display
        stats_frame = ctk.CTkFrame(self.window)
        stats_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        stats_data = self.stats.stats
        
        # Format statistics
        total_sessions = stats_data.get("total_sessions", 0)
        total_breaks = stats_data.get("total_breaks", 0)
        total_work_hours = stats_data.get("total_work_time", 0) / 3600
        longest_session_min = stats_data.get("longest_session", 0) / 60
        average_session_min = stats_data.get("average_session", 0) / 60
        
        stats_text = [
            f"Total Sessions: {total_sessions}",
            f"Total Breaks Taken: {total_breaks}",
            f"Total Work Time: {total_work_hours:.1f} hours",
            f"Longest Session: {longest_session_min:.1f} minutes",
            f"Average Session: {average_session_min:.1f} minutes"
        ]
        
        for stat in stats_text:
            ctk.CTkLabel(
                stats_frame, 
                text=stat,
                font=("Arial", 14)
            ).pack(pady=10, anchor="w")
        
        # Close button
        ctk.CTkButton(
            self.window,
            text="Close",
            command=self.window.destroy
        ).pack(pady=20)

class HistoryWindow:
    """Notification history window"""
    
    def __init__(self, parent, history: ReminderHistory):
        self.parent = parent
        self.history = history
        self.window = None
    
    def show(self):
        if self.window and self.window.winfo_exists():
            self.window.focus()
            return
        
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title("Notification History")
        self.window.geometry("600x500")
        self.window.transient(self.parent)
        
        # Title
        ctk.CTkLabel(
            self.window,
            text="Recent Notifications", 
            font=("Arial", 20, "bold")
        ).pack(pady=20)
        
        # History display
        self.history_text = ctk.CTkTextbox(self.window)
        self.history_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Load history
        self.refresh_history()
        
        # Buttons
        button_frame = ctk.CTkFrame(self.window)
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(
            button_frame,
            text="Refresh",
            command=self.refresh_history
        ).pack(side="left")
        
        ctk.CTkButton(
            button_frame,
            text="Clear History",
            command=self.clear_history
        ).pack(side="left", padx=(10, 0))
        
        ctk.CTkButton(
            button_frame,
            text="Close",
            command=self.window.destroy
        ).pack(side="right")
    
    def refresh_history(self):
        self.history_text.delete("1.0", "end")
        
        history_entries = self.history.history[-20:]  # Last 20 entries
        history_entries.reverse()  # Most recent first
        
        for entry in history_entries:
            timestamp = datetime.fromisoformat(entry["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            message = entry["message"]
            activity = entry.get("activity", "")
            action = entry.get("action", "continue")
            
            entry_text = f"[{timestamp}] {message}\n"
            if activity:
                entry_text += f"  Activity: {activity}\n"
            entry_text += f"  Action: {action}\n\n"
            
            self.history_text.insert("end", entry_text)
    
    def clear_history(self):
        if messagebox.askyesno("Confirm", "Clear all notification history?"):
            self.history.history = []
            self.history.save_history()
            self.refresh_history()

class BreakReminderApp:
    """Main application class"""
    
    def __init__(self):
        self.config = ReminderConfig()
        self.stats = ReminderStats()
        self.history = ReminderHistory()
        
        self.icon = None
        self.running = False
        
        # Setup UI
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.root.title("Advanced Break Reminder")
        self.root.geometry("500x400")
        self.root.protocol('WM_DELETE_WINDOW', self.quit_app)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        ctk.CTkLabel(
            self.root,
            text="Advanced Break Reminder",
            font=("Arial", 24, "bold")
        ).pack(pady=20)
        
        # Interval selection
        interval_frame = ctk.CTkFrame(self.root)
        interval_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            interval_frame,
            text="Select Interval:",
            font=("Arial", 14)
        ).pack(anchor="w", padx=10, pady=5)
        
        intervals = self.config.get("intervals", {})
        current_interval = self.config.get("current_interval", "Short Break")
        
        self.interval_var = ctk.StringVar(value=current_interval)
        self.interval_menu = ctk.CTkComboBox(
            interval_frame,
            values=list(intervals.keys()),
            variable=self.interval_var,
            command=self.on_interval_change
        )
        self.interval_menu.pack(padx=10, pady=5)
        
        # Control buttons
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=20, fill="x", padx=20)
        
        self.start_btn = ctk.CTkButton(
            button_frame,
            text="Start Session",
            command=self.start_session,
            height=40,
            font=("Arial", 16, "bold")
        )
        self.start_btn.pack(pady=10)
        
        self.stop_btn = ctk.CTkButton(
            button_frame,
            text="Stop Session",
            command=self.stop_session,
            height=40,
            state="disabled"
        )
        self.stop_btn.pack(pady=5)
        
        # Menu buttons
        menu_frame = ctk.CTkFrame(self.root)
        menu_frame.pack(pady=10, fill="x", padx=20)
        
        buttons = [
            ("Settings", self.show_settings),
            ("Statistics", self.show_stats),
            ("History", self.show_history)
        ]
        
        for text, command in buttons:
            ctk.CTkButton(
                menu_frame,
                text=text,
                command=command,
                width=120
            ).pack(side="left", padx=5, pady=5)
    
    def on_interval_change(self, value):
        self.config.set("current_interval", value)
    
    def create_icon_image(self):
        width, height = 64, 64
        image = Image.new('RGB', (width, height), (31, 83, 141))
        dc = ImageDraw.Draw(image)
        dc.ellipse((10, 10, 54, 54), fill=(255, 255, 255))
        # Add a small clock symbol
        dc.arc((20, 20, 44, 44), start=90, end=0, fill=(31, 83, 141), width=2)
        return image
    
    def play_notification_sound(self):
        if not self.config.get("sound_enabled", True):
            return
        
        sound_file = self.config.get("sound_file", "")
        
        try:
            if sound_file and Path(sound_file).exists():
                winsound.PlaySound(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
            else:
                winsound.Beep(800, 500)  # Frequency, duration
        except Exception:
            # Fallback to system bell
            self.root.bell()
    
    def show_break_reminder(self):
        if not self.running:
            return
        
        # Get random message and activity
        messages = self.config.get("messages", ["Time for a break!"])
        activities = self.config.get("break_activities", [])
        
        message = random.choice(messages)
        activity = random.choice(activities) if activities else ""
        
        # Play sound
        self.play_notification_sound()
        
        # Show popup
        popup_text = message
        if activity and self.config.get("show_activity_suggestion", True):
            popup_text += f"\n\nSuggested activity:\n{activity}"
        
        popup_text += "\n\nContinue working?"
        
        response = messagebox.askyesno("Break Time", popup_text)
        
        # Log to history and stats
        action = "continue" if response else "stop"
        self.history.add_entry(message, activity, action)
        
        if response:
            self.stats.log_break_taken()
            # Schedule next reminder
            interval_name = self.interval_var.get()
            interval_seconds = self.config.get("intervals", {}).get(interval_name, 300)
            self.root.after(interval_seconds * 1000, self.show_break_reminder)
        else:
            self.stop_session()
    
    def start_session(self):
        self.running = True
        self.stats.log_session_start()
        
        # Update UI
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        
        # Minimize to tray
        self.withdraw_to_tray()
        
        # Schedule first reminder
        interval_name = self.interval_var.get()
        interval_seconds = self.config.get("intervals", {}).get(interval_name, 300)
        self.root.after(interval_seconds * 1000, self.show_break_reminder)
    
    def stop_session(self):
        self.running = False
        
        # Update UI
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        
        # Stop tray icon
        if self.icon:
            self.icon.stop()
            self.icon = None
        
        # Show main window
        self.root.deiconify()
    
    def withdraw_to_tray(self):
        self.root.withdraw()
        
        menu = (
            item('Show App', self.show_window),
            item('Settings', self.show_settings_from_tray),
            item('Stop Session', self.stop_session),
            item('Quit', self.quit_app)
        )
        
        self.icon = pystray.Icon(
            "AdvancedBreakReminder",
            self.create_icon_image(),
            "Advanced Break Reminder",
            menu
        )
        
        threading.Thread(target=self.icon.run, daemon=True).start()
    
    def show_window(self, icon=None, item=None):
        if self.icon:
            self.icon.stop()
            self.icon = None
        self.root.after(0, self.root.deiconify)
    
    def show_settings_from_tray(self, icon=None, item=None):
        self.root.after(0, lambda: SettingsWindow(self.root, self.config).show())
    
    def show_settings(self):
        SettingsWindow(self.root, self.config).show()
    
    def show_stats(self):
        StatsWindow(self.root, self.stats).show()
    
    def show_history(self):
        HistoryWindow(self.root, self.history).show()
    
    def quit_app(self, icon=None, item=None):
        self.running = False
        if self.icon:
            self.icon.stop()
        self.root.after(0, self.root.destroy)
        sys.exit()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BreakReminderApp()
    app.run()
