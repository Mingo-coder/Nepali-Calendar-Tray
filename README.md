# Shows Nepali Calendar in Tray area
<img width="138" height="93" alt="image" src="https://github.com/user-attachments/assets/a146ba01-7bd7-4f21-a39e-b19b926adb3d" />

### Made using Grok and produces no error as far as I have seen. I'm unable to make it show the whole date in tray so that is the only thing broken here.

#### Please download the zip file for the Release tab or https://github.com/Mingo-coder/Nepali-Calendar-Tray/releases/download/v1.0/NepaliTray.zip
and extract it to use the app on Windows OS. I put a shortcut in Startup folder so it starts with windows everytime.

### Main goal was to create a lightweight app that shows nepali calendar. Language can also be selected in right-click menu.
<img width="577" height="603" alt="image" src="https://github.com/user-attachments/assets/b041a239-75f1-4403-9aa6-34fd5083d75f" />

## Here's some AI text if you want to bother reading them.

# Nepali Date Tray

A lightweight Windows system tray app that shows the current **Bikram Sambat (Nepali)** date.

## Features

- Displays today’s Nepali date in the system tray
- Large clear day number (with optional full short date mode)
- Green highlight on Saturdays and Sundays
- Red highlight on Weekdays
- Left-click opens a clean Nepali calendar
- Navigate between months with ← → buttons
- Week starts from Sunday
- Weekends highlighted in red
- Language toggle (Nepali ↔ English)
- Single instance protection
- Lightweight and offline

## Requirements

- Windows 10 / 11
- No extra installation needed when using the pre-built version

## How to Run

1. Download the latest release
2. Extract the folder
3. Run `NepaliDate.exe`

## Building from Source

```bash
pip install pystray pillow nepali-datetime

# Build (recommended)
pyinstaller --onedir --noconsole --name "NepaliDate" --collect-all nepali_datetime nepali_tray.py
