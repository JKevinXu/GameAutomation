#!/usr/bin/env python3
"""
Shared Configuration for Game Automation
Contains all emulator coordinates and automation settings
"""

# Named coordinates for easy reference
COORDINATES = {
    'play_button': (110, 150),      # Main play button
    'start_game': (836, 159),       # Game start button
    'login_button': (974, 403),     # Login button
    'shi_men_task': (1286, 211),    # shi men task button
    'any_place': (1286, 211),       # any place
    'shi_men_task_go_finish': 'game_elements/go_finish_shimen_icon.png',    # shi men task go finish button (PNG template)
    'dialogue_button': 'game_elements/dialogue_icon.png',  # Dialogue button (PNG template)
}

# Action plans for different automation sequences
ACTION_PLANS = {
    '师门任务': [
        {'action': 'open_app', 'app': 'mumu', 'description': 'Open MuMu emulator'},
        {'action': 'click', 'coordinate': 'play_button', 'description': 'Click emulator play button'},
        {'action': 'wait', 'duration': 10, 'description': 'Wait for emulator to boot'},
        {'action': 'click', 'coordinate': 'start_game', 'description': 'Click game start button'},
        {'action': 'wait', 'duration': 5, 'description': 'Wait for game to load'},
        {'action': 'click', 'coordinate': 'any_place', 'description': 'Click any place'},
        {'action': 'wait', 'duration': 5, 'description': 'Wait for game to load'},
        {'action': 'click', 'coordinate': 'login_button', 'description': 'Click log in button'},
        {'action': 'wait', 'duration': 8, 'description': 'Wait for login to complete'},
        {'action': 'click', 'coordinate': 'shi_men_task', 'description': 'Click shi men task button'},
        {'action': 'wait', 'duration': 3, 'description': 'Wait for game to load'},
        {'action': 'click', 'coordinate': 'shi_men_task_go_finish', 'confidence': 0.8, 'description': 'Click shi men task go finish button'},
    ],
    '320': [
        {'action': 'click', 'coordinate': 'dialogue_button', 'confidence': 0.8, 'description': 'Click dialogue button using template matching'},
        {'action': 'avatar_keyword_click', 'keywords': '320', 'confidence': 0.8, 'description': 'Find and click avatar for 320 recruitment messages'}
    ],
}

# Legacy support - keeping for backward compatibility
PLAY_BUTTONS = {
    1: COORDINATES['play_button'],    # First emulator - "我的安卓"
}

# PyAutoGUI settings
PYAUTOGUI_SETTINGS = {
    'FAILSAFE': True,     # Move mouse to top-left corner to stop
    'PAUSE': 0.5,         # Small pause between actions
}

# Application paths
APPLICATION_PATHS = {
    'mumu': "/Applications/MuMuPlayer.app",
    'chrome': "/Applications/Google Chrome.app",
    'safari': "/Applications/Safari.app",
    'finder': "/System/Library/CoreServices/Finder.app",
    'calculator': "/Applications/Calculator.app",
}

# Legacy support
MUMU_PATHS = [APPLICATION_PATHS['mumu']]

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