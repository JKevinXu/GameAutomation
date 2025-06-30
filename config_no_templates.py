#!/usr/bin/env python3
"""
Direct Coordinate Configuration for Cron Jobs
Uses hardcoded coordinates instead of template matching to bypass permission issues
"""

# Named coordinates using direct coordinates (no screencapture needed)
COORDINATES = {
    # Replace these with actual coordinates from your setup
    # You can find these by manually hovering over buttons and noting coordinates
    'play_button': (960, 540),      # REPLACE: MuMu emulator play button coordinates
    'start_game': (960, 600),       # REPLACE: Game start button coordinates  
    'login_button': (960, 500),     # REPLACE: Login button coordinates
    'shi_men_task': (800, 400),     # REPLACE: Shi men task button coordinates
    'any_place': (1286, 211),       # Keep existing coordinate
    'shi_men_task_go_finish': (900, 450),  # REPLACE: Go finish button coordinates
    'dialogue_button': (750, 350),   # REPLACE: Dialogue button coordinates
    'join_team': (850, 500),        # REPLACE: Join team button coordinates
}

# Action plans for different automation sequences
ACTION_PLANS = {
    '师门任务': [
        {'action': 'open_app', 'app': 'mumu', 'description': 'Open MuMu emulator'},
        {'action': 'click', 'coordinate': 'play_button', 'description': 'Click emulator play button'},
        {'action': 'wait', 'duration': 10, 'description': 'Wait for emulator to boot'},
        {'action': 'click', 'coordinate': 'start_game', 'description': 'Click game start button'},
        {'action': 'wait', 'duration': 36, 'description': 'Wait for game to load'},
        {'action': 'click', 'coordinate': 'login_button', 'description': 'Click log in button'},
        {'action': 'wait', 'duration': 5, 'description': 'Wait for login to complete'},
        {'action': 'click', 'coordinate': 'shi_men_task', 'description': 'Click shi men task button'},
        {'action': 'wait', 'duration': 3, 'description': 'Wait for game to load'},
        {'action': 'click', 'coordinate': 'shi_men_task_go_finish', 'description': 'Click shi men task go finish button'},
    ],
}

# Legacy support
PLAY_BUTTONS = {
    1: COORDINATES['play_button'],
}

# PyAutoGUI settings
PYAUTOGUI_SETTINGS = {
    'FAILSAFE': True,
    'PAUSE': 0.5,
}

# Application paths
APPLICATION_PATHS = {
    'mumu': "/Applications/MuMuPlayer.app"
}

# Legacy support
MUMU_PATHS = [APPLICATION_PATHS['mumu']]

# Timing settings
TIMING = {
    'MUMU_STARTUP_WAIT': 3,
    'EMULATOR_BOOT_WAIT': 5,
    'CLICK_PAUSE': 0.5,
}

# Visual marker settings
MARKER_SETTINGS = {
    'MOVEMENT_DURATION': 0.5,
    'MARKER_SIZE': 8,
    'COUNTDOWN_STEPS': 3,
} 