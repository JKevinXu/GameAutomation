#!/usr/bin/env python3
"""
Coordinate Finder
Help find the exact coordinates of play buttons by hovering mouse over them
"""

import pyautogui
import time
import sys

def find_coordinates():
    """
    Display current mouse coordinates in real-time
    """
    print("🎯 Coordinate Finder")
    print("=" * 50)
    print("Instructions:")
    print("1. Hover your mouse over the FIRST play button")
    print("2. Press ENTER to capture coordinates")
    print("3. Repeat for other play buttons")
    print("4. Press Ctrl+C to exit anytime")
    print()
    
    coordinates = {}
    
    for i in range(1, 4):
        print(f"📍 Finding coordinates for Emulator #{i}")
        print("Move your mouse over the play button and press ENTER...")
        
        try:
            # Show live coordinates
            while True:
                x, y = pyautogui.position()
                print(f"\rCurrent position: ({x}, {y})", end="", flush=True)
                time.sleep(0.1)
                
                # Check if Enter was pressed (we'll use a simple input method)
                # For now, let's just wait for user input
                break
            
            input()  # Wait for Enter
            
            # Capture final coordinates
            x, y = pyautogui.position()
            coordinates[i] = (x, y)
            print(f"\n✅ Emulator #{i} coordinates: ({x}, {y})")
            print()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Coordinate finding cancelled")
            break
    
    # Display all captured coordinates
    if coordinates:
        print("\n" + "=" * 50)
        print("📋 CAPTURED COORDINATES:")
        print("=" * 50)
        for emulator, coords in coordinates.items():
            x, y = coords
            print(f"Emulator #{emulator}: ({x}, {y})")
        
        # Generate updated code
        print("\n🔧 Copy this into simple_click.py:")
        print("-" * 30)
        print("play_buttons = {")
        for emulator, coords in coordinates.items():
            x, y = coords
            print(f"    {emulator}: ({x}, {y}),   # Emulator #{emulator}")
        print("}")

def continuous_display():
    """
    Continuously display mouse coordinates
    """
    print("🎯 Live Coordinate Display")
    print("Press Ctrl+C to stop")
    print("-" * 30)
    
    try:
        while True:
            x, y = pyautogui.position()
            print(f"\rMouse position: ({x}, {y})     ", end="", flush=True)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\n👋 Coordinate display stopped")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--live":
        continuous_display()
    else:
        find_coordinates()

if __name__ == "__main__":
    main() 