#!/usr/bin/env python3
"""
Live Mouse Coordinate Display
Shows real-time mouse coordinates as you move your mouse
"""

import pyautogui
import time
import sys
import os

def clear_line():
    """Clear the current line in terminal"""
    print('\r' + ' ' * 80, end='')
    print('\r', end='')

def live_coordinates():
    """
    Display live mouse coordinates with enhanced visibility
    """
    print("🖱️  Live Mouse Coordinate Tracker")
    print("=" * 50)
    print("Move your mouse around to see coordinates")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    print()
    
    try:
        last_x, last_y = -1, -1
        
        while True:
            x, y = pyautogui.position()
            
            # Only update if position changed (reduces flicker)
            if x != last_x or y != last_y:
                clear_line()
                print(f"🎯 Mouse Position: ({x:4d}, {y:4d})", end='', flush=True)
                last_x, last_y = x, y
            
            time.sleep(0.05)  # Update every 50ms for smooth tracking
            
    except KeyboardInterrupt:
        clear_line()
        print("\n\n✅ Coordinate tracking stopped")
        print("\n💡 Usage tip:")
        print("1. Hover over the play button you want to click")
        print("2. Note the coordinates displayed")
        print("3. Update simple_click.py with those coordinates")

def capture_on_click():
    """
    Capture coordinates when user clicks
    """
    print("🖱️  Click Coordinate Capture")
    print("=" * 50)
    print("Click anywhere to capture coordinates")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    print()
    
    captured = []
    
    try:
        while True:
            x, y = pyautogui.position()
            print(f"\r🎯 Current: ({x:4d}, {y:4d}) - Click to capture!", end='', flush=True)
            
            # Check for mouse click (this is a simplified approach)
            time.sleep(0.1)
            
            # Note: This is a basic implementation
            # For click detection, we'd need more advanced techniques
            
    except KeyboardInterrupt:
        clear_line()
        print("\n\n✅ Capture mode stopped")
        if captured:
            print("\n📋 Captured coordinates:")
            for i, (x, y) in enumerate(captured, 1):
                print(f"Position {i}: ({x}, {y})")

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--click":
            capture_on_click()
        elif sys.argv[1] == "--help":
            print("🖱️  Live Coordinate Tools")
            print("=" * 30)
            print("python live_coordinates.py          # Live position tracking")
            print("python live_coordinates.py --click  # Click capture mode")
            print("python live_coordinates.py --help   # Show this help")
        else:
            print("❌ Unknown option. Use --help for usage info")
    else:
        live_coordinates()

if __name__ == "__main__":
    main() 