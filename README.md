# Break Reminder Application

A progressive desktop application designed to help users maintain healthy work habits by providing regular break reminders during focused work sessions.

## Project Overview

This project consists of four versions of a break reminder application, each building upon the previous one with enhanced features and improved user experience:

- **[main.py](main.py)** - Basic version with standard Tkinter GUI
- **[ver2.py](ver2.py)** - Enhanced version using CustomTkinter for modern UI
- **[ver3.py](ver3.py)** - Advanced version with system tray integration
- **[ver4.py](ver4.py)** - Feature-complete version with settings, statistics, and history

## Features by Version

### Version 1 ([main.py](main.py))
- **Basic GUI**: Simple Tkinter interface
- **Customizable Intervals**: Set reminder intervals (currently 5 seconds for testing)
- **Audio Alert**: System bell notification
- **Session Control**: Continue or exit options
- **Clean Interface**: Minimalist design with start button

### Version 2 ([ver2.py](ver2.py))
- **Modern UI**: Dark theme using CustomTkinter
- **Enhanced Styling**: 
  - Modern buttons with rounded corners
  - Professional typography (Arial font)
  - Improved color scheme
- **Better UX**: More descriptive labels and instructions
- **Responsive Design**: 400x280 window with proper spacing

### Version 3 ([ver3.py](ver3.py))
- **System Tray Integration**: App minimizes to system tray
- **Background Operation**: Continues running without visible window
- **Custom Tray Icon**: Generated programmatically with PIL
- **Context Menu**: Right-click menu in system tray
- **Thread Safety**: Proper threading for tray operations
- **Graceful Exit**: Proper cleanup when closing application

### Version 4 ([ver4.py](ver4.py))
- **⭐ ALL FUTURE ENHANCEMENTS IMPLEMENTED ⭐**
- **Customizable Messages**: Edit reminder messages through settings GUI
- **Multiple Interval Presets**: Choose from predefined intervals or set custom ones
- **Break Activity Suggestions**: Random activity suggestions with each break
- **Usage Statistics**: Track sessions, breaks, work time, and averages
- **Sound Customization**: Enable/disable sounds, use custom audio files
- **Notification History**: View last 100 break reminders with timestamps
- **Settings GUI**: Comprehensive configuration interface with tabbed layout
- **Persistent Configuration**: Settings saved automatically to JSON files
- **Enhanced Tray Menu**: Quick access to settings and stats from system tray
- **Professional UI**: Advanced CustomTkinter interface with multiple windows

## Dependencies

### Version 1 (main.py)
```
tkinter (built-in)
sys (built-in)
```

### Version 2 (ver2.py)
```
customtkinter
tkinter (built-in)
sys (built-in)
```

### Version 3 (ver3.py)
```
customtkinter
tkinter (built-in)
sys (built-in)
threading (built-in)
PIL (Pillow)
pystray
```

### Version 4 (ver4.py)
```
customtkinter
tkinter (built-in)
sys (built-in)
threading (built-in)
time (built-in)
json (built-in)
random (built-in)
winsound (built-in - Windows)
pathlib (built-in)
datetime (built-in)
typing (built-in)
PIL (Pillow)
pystray
```

## Installation

1. **Clone or download the project**
2. **Install required dependencies**:
   ```bash
   pip install customtkinter pillow pystray
   ```
   
   *Note: Version 4 uses only built-in libraries beyond these three dependencies.*

## Usage

### Running Version 1 (Basic)
```bash
python main.py
```

### Running Version 2 (Modern UI)
```bash
python ver2.py
```

### Running Version 3 (System Tray)
```bash
python ver3.py
```

### Running Version 4 (Feature Complete)
```bash
python ver4.py
```

## Configuration

### Versions 1-3
The reminder interval can be adjusted by modifying the `INTERVAL` constant:

```python
# For production use (20 minutes):
INTERVAL = 20 * 60 * 1000

# For testing (5 seconds):
INTERVAL = 5000
```

### Version 4 (Advanced Configuration)
Version 4 uses a comprehensive GUI settings system with persistent JSON configuration:

- **Settings GUI**: Access through main window or system tray
- **Configuration Files**: 
  - `reminder_config.json` - App settings
  - `reminder_stats.json` - Usage statistics
  - `reminder_history.json` - Notification history
- **Configurable Options**:
  - Multiple time intervals with presets
  - Custom reminder messages
  - Break activity suggestions
  - Sound settings (system beep or custom audio files)
  - Auto-continue options

## How It Works

1. **Start**: Click the start button to begin a work session
2. **Hide**: The application window hides (or minimizes to tray in v3)
3. **Alert**: After the set interval, a popup reminds you to take a break
4. **Continue**: Choose to continue the session or exit the application

## System Tray Features (Versions 3 & 4)

- **Minimize to Tray**: App runs silently in the background
- **Tray Icon**: Custom blue circular icon with clock symbol (v4)
- **Context Menu**:
  - "Show App": Restore the main window
  - "Settings": Quick access to configuration (v4)
  - "Stop Session": End current work session (v4)
  - "Quit": Exit the application completely

## Advanced Features (Version 4)

### Settings Management
- **Tabbed Interface**: Organized settings in categories
- **Interval Configuration**: Set custom work periods
- **Message Customization**: Edit break reminder texts
- **Activity Suggestions**: Customize break activities
- **Sound Options**: Choose system sounds or custom audio files

### Statistics & Analytics
- **Session Tracking**: Monitor work sessions and breaks
- **Time Analytics**: View total work time and averages
- **Performance Metrics**: Longest sessions and productivity stats
- **Historical Data**: Persistent statistics across app restarts

### Notification History
- **Activity Log**: View last 100 break notifications
- **Timestamp Tracking**: See when breaks were offered
- **Action Recording**: Track continue vs stop decisions
- **History Management**: Clear old entries when needed

## Future Enhancements

### ✅ Implemented in Version 4:
- [x] Customizable reminder messages
- [x] Multiple interval presets
- [x] Break activity suggestions
- [x] Usage statistics tracking
- [x] Sound customization
- [x] Notification history
- [x] Settings configuration GUI

### 🚀 Potential Future Improvements:
- [ ] Cross-platform native notifications
- [ ] Integration with calendar/productivity apps
- [ ] Team collaboration features
- [ ] Advanced analytics and reporting
- [ ] Mobile app companion
- [ ] Plugin system for custom extensions
- [ ] Cloud sync for settings across devices

## Development Notes

- **Language**: Romanian text in popups ("Pauza", "Vrei să continui sesiunea?")
- **Testing Mode**: Current interval set to 5 seconds for development
- **Cross-Platform**: Compatible with Windows, macOS, and Linux
- **Thread Safe**: Version 3 uses proper threading for system tray operations


## License

This project is open source and available for personal and educational use.

## Contributing

Feel free to fork this project and submit improvements via pull requests.