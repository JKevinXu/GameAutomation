#!/usr/bin/env python3
"""
Shared Configuration for Game Automation
Contains all emulator coordinates and automation settings
"""

# Emulator play button coordinates
PLAY_BUTTONS = {
    1: (110, 150),    # First emulator - "我的安卓"
}

# PyAutoGUI settings
PYAUTOGUI_SETTINGS = {
    'FAILSAFE': True,     # Move mouse to top-left corner to stop
    'PAUSE': 0.5,         # Small pause between actions
}

# Application paths
MUMU_PATHS = [
    "/Applications/MuMuPlayer.app"
]

# Timing settings
TIMING = {
    'MUMU_STARTUP_WAIT': 3,     # Seconds to wait after opening MuMu
    'EMULATOR_BOOT_WAIT': 5,    # Seconds to wait for emulator to boot
    'CLICK_PAUSE': 0.5,         # Pause before clicking
}

# Visual marker settings
MARKER_SETTINGS = {
    'MOVEMENT_DURATION': 0.5,   # Duration for mouse movement
    'MARKER_SIZE': 8,           # Size of visual marker squares
    'COUNTDOWN_STEPS': 3,       # Number of countdown steps
} 