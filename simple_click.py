#!/usr/bin/env python3
"""
Simple Play Button Clicker
Directly clicks the play button coordinates found by the automation
"""

import pyautogui
import time
import sys

def click_play_button(emulator_number=1, show_marker=True):
    """
    Click play button for specific emulator using known coordinates
    """
    # Coordinates found from manual coordinate detection
    play_buttons = {
        1: (576, 275),    # First emulator - "我的安卓"
    }
    
    if emulator_number not in play_buttons:
        print(f"❌ Invalid emulator number: {emulator_number}")
        print("Available emulators: 1, 2, 3")
        return False
    
    x, y = play_buttons[emulator_number]
    
    print(f"🎯 Clicking emulator #{emulator_number} play button at ({x}, {y})")
    
    try:
        if show_marker:
            # Show visual marker by moving mouse to position first
            print("🎯 Moving mouse to target position...")
            pyautogui.moveTo(x, y, duration=0.5)  # Smooth movement to show position
            time.sleep(0.5)  # Brief pause to see the position
            
            # Move mouse in a small circle to make it more visible
            print("📍 Marking position with visual indicator...")
            for i in range(3):
                pyautogui.moveRel(8, 0, duration=0.1)
                pyautogui.moveRel(0, 8, duration=0.1)
                pyautogui.moveRel(-8, 0, duration=0.1)
                pyautogui.moveRel(0, -8, duration=0.1)
            
            # Return to center and countdown
            pyautogui.moveTo(x, y, duration=0.2)
            print("⏰ Clicking in:")
            for i in range(3, 0, -1):
                print(f"   {i}...")
                time.sleep(0.5)
        
        # Click the button
        print("🖱️  Clicking now...")
        pyautogui.click(x, y)
        print("✅ Click successful!")
        print("⏳ Waiting for emulator to start...")
        time.sleep(3)
        return True
        
    except Exception as e:
        print(f"❌ Click failed: {e}")
        return False

def main():
    print("🎮 Simple Play Button Clicker")
    print("=" * 40)
    
    # Configure PyAutoGUI
    pyautogui.FAILSAFE = True  # Move mouse to corner to stop
    pyautogui.PAUSE = 0.5
    
    # Get emulator number from command line or default to 1
    emulator_num = 1
    if len(sys.argv) > 1:
        try:
            emulator_num = int(sys.argv[1])
        except ValueError:
            print("❌ Invalid emulator number. Using default (1)")
    
    # Click the button
    click_play_button(emulator_num, show_marker=False)

if __name__ == "__main__":
    main() 