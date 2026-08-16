### Shows Nepali Calendar in Tray area, can show overlay of today's date and the whole calendar on a lightweight app.
<img width="216" height="112" alt="image" src="https://github.com/user-attachments/assets/df7990a3-30d2-4569-9c07-2b63da3f960f" />
#### Consumes about 19mb of ram and uses 36.6mb of disk space.

#### Please download the latest zip file from the Release tab or https://github.com/Mingo-coder/Nepali-Calendar-Tray/releases/download/v1.6/NepaliTray.zip
and extract it to use the app on Windows OS. I put a shortcut of the app in Startup folder so it starts with windows everytime.

##### Made using Grok and produces no error as far as I have seen.

## Here's some helpful AI texts.
# NepaliTray
<img width="577" height="603" alt="image" src="https://github.com/user-attachments/assets/b041a239-75f1-4403-9aa6-34fd5083d75f" />

A lightweight Windows system tray app for Nepali (Bikram Sambat) dates.

## Features

### Tray Icon
- Shows today’s Nepali day number in the system tray
- Weekend days use a red background
- Weekdays use a blue background
- Tooltip shows full date with weekday
- Supports Nepali and English display modes

### Calendar Popup
- Full monthly Bikram Sambat calendar
- Sunday-first week layout
- Saturday and Sunday highlighted in red
- Today highlighted clearly
- Previous / next month navigation
- Editable year field (type a year and press Enter)
- Pin button to keep calendar open
- Today button to jump back to current date
- Auto-closes when clicking outside (unless pinned)

### Custom Context Menu
- Large readable Nepali font
- Copy options:
  - Nepali date
  - Nepali time
  - Nepali date + time
  - English date
  - English time
  - English date + time
- Open calendar
- Toggle overlay
- Toggle always-on-top
- Toggle draggable overlay
- Switch language (Nepali ↔ English)
- Quit app

### Floating Overlay
- Optional always-visible date overlay
- Shows month, day, and weekday
- Weekend text in red
- Draggable
- Always-on-top option
- Remembers last position

### Click Behavior
- Single left-click → custom menu
- Double left-click → calendar
- Right-click → small system menu (Open / Quit)

### Calendar Engine
- Pure hybrid Bikram Sambat engine
- Accurate month-length table for **1975–2100 BS**
- Approximation fallback outside that range

### Other
- Single-instance lock (prevents duplicate apps)
- Language toggle updates tray icon, tooltip, calendar, and menus
- Lightweight Python tray app for Windows

## Requirements
- Python 3.x
- Windows
- Packages:
  - `pystray`
  - `pillow`
  - `pyperclip`

## Run
```bash
pip install pystray pillow pyperclip
python NepaliTray.py
