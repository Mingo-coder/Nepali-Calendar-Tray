# Shows Nepali Calendar in Tray area, can show overlay of today's date and the whole calendar on a lightweight app.
<img width="216" height="112" alt="image" src="https://github.com/user-attachments/assets/df7990a3-30d2-4569-9c07-2b63da3f960f" />

#### Please download the latest zip file from the Release tab or https://github.com/Mingo-coder/Nepali-Calendar-Tray/releases/download/v1.6/NepaliTray.zip
and extract it to use the app on Windows OS. I put a shortcut of the app in Startup folder so it starts with windows everytime.

#### Made using Grok and produces no error as far as I have seen. Main goal was to create a lightweight app that shows nepali calendar. Language can also be selected in right-click menu.
<img width="577" height="603" alt="image" src="https://github.com/user-attachments/assets/b041a239-75f1-4403-9aa6-34fd5083d75f" />

## Here's some helpful AI texts.
# Nepali Date Tray

A lightweight Windows system tray app that shows the current **Bikram Sambat (Nepali)** date.

## Features

- Displays today’s Nepali date in the system tray
- Large clear day number (with optional full short date mode)
- Small drag-able Overlay of Today's date
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
