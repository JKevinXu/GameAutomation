#!/usr/bin/env python3
"""
Coordinate Finder
Help find the exact coordinates of play buttons by hovering mouse over them
"""

import pyautogui
import time
import sys
import cv2
import numpy as np
import os
from typing import Tuple, Optional, List

def detect_display_scaling() -> float:
    """
    Detect display scaling factor by comparing logical vs physical screen dimensions
    
    Returns:
        float: Scaling factor (e.g., 2.0 for 2x scaling)
    """
    # Get logical screen size (what mouse coordinates use)
    logical_size = pyautogui.size()
    
    # Get physical screenshot size  
    screenshot = pyautogui.screenshot()
    physical_size = screenshot.size
    
    scaling_x = physical_size[0] / logical_size[0]
    scaling_y = physical_size[1] / logical_size[1]
    
    print(f"📏 Logical screen size: {logical_size[0]} x {logical_size[1]}")
    print(f"📷 Physical screenshot size: {physical_size[0]} x {physical_size[1]}")
    print(f"🔍 Scaling factors: X={scaling_x:.2f}, Y={scaling_y:.2f}")
    
    # Use average scaling factor
    scaling_factor = (scaling_x + scaling_y) / 2
    return scaling_factor

def logical_to_physical_coords(logical_x: int, logical_y: int, scaling_factor: float = None) -> Tuple[int, int]:
    """
    Convert logical coordinates (mouse position) to physical coordinates (screenshot)
    
    Args:
        logical_x, logical_y: Mouse/logical coordinates
        scaling_factor: Display scaling factor (auto-detected if None)
        
    Returns:
        Tuple[int, int]: Physical coordinates for screenshot
    """
    if scaling_factor is None:
        scaling_factor = detect_display_scaling()
    
    physical_x = int(logical_x * scaling_factor)
    physical_y = int(logical_y * scaling_factor)
    
    return physical_x, physical_y

def physical_to_logical_coords(physical_x: int, physical_y: int, scaling_factor: float = None) -> Tuple[int, int]:
    """
    Convert physical coordinates (screenshot) to logical coordinates (mouse position)
    
    Args:
        physical_x, physical_y: Screenshot coordinates
        scaling_factor: Display scaling factor (auto-detected if None)
        
    Returns:
        Tuple[int, int]: Logical coordinates for mouse positioning
    """
    if scaling_factor is None:
        scaling_factor = detect_display_scaling()
    
    logical_x = int(physical_x / scaling_factor)
    logical_y = int(physical_y / scaling_factor)
    
    return logical_x, logical_y

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

def find_icon_coordinates(template_path: str, confidence: float = 0.8, screenshot_path: str = None) -> Optional[Tuple[int, int]]:
    """
    Find the coordinates of an icon on the screen using template matching
    
    Args:
        template_path (str): Path to the template image (icon to find)
        confidence (float): Minimum confidence threshold (0.0-1.0). Default is 0.8
        screenshot_path (str): Optional path to save the screenshot for debugging
        
    Returns:
        Tuple[int, int]: (x, y) coordinates of the center of the found icon
        None: If icon is not found
    """
    try:
        # Check if template file exists
        if not os.path.exists(template_path):
            print(f"❌ Template image not found: {template_path}")
            return None
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Save screenshot if path provided (for debugging)
        if screenshot_path:
            # Ensure debug directory exists if saving to debug folder
            if "debug/" in screenshot_path:
                os.makedirs("debug", exist_ok=True)
            cv2.imwrite(screenshot_path, screenshot_cv)
            print(f"📸 Screenshot saved to: {screenshot_path}")
        
        # Load template image
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            print(f"❌ Failed to load template image: {template_path}")
            return None
        
        # Get template dimensions
        template_height, template_width = template.shape[:2]
        
        # Perform template matching
        result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
        
        # Find the best match
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # Check if confidence threshold is met
        if max_val < confidence:
            print(f"❌ Icon not found. Best match confidence: {max_val:.3f} (threshold: {confidence:.3f})")
            print(f"💡 Try lowering the confidence threshold or check if the template image matches the current screen")
            return None
        
        # Calculate center coordinates
        center_x = max_loc[0] + template_width // 2
        center_y = max_loc[1] + template_height // 2
        
        print(f"✅ Icon found at ({center_x}, {center_y}) with confidence: {max_val:.3f}")
        return (center_x, center_y)
        
    except Exception as e:
        print(f"❌ Error during icon detection: {e}")
        return None


def find_all_icon_coordinates(template_path: str, confidence: float = 0.8) -> List[Tuple[int, int]]:
    """
    Find all instances of an icon on the screen
    
    Args:
        template_path (str): Path to the template image
        confidence (float): Minimum confidence threshold
        
    Returns:
        List[Tuple[int, int]]: List of (x, y) coordinates for all found instances
    """
    try:
        if not os.path.exists(template_path):
            print(f"❌ Template image not found: {template_path}")
            return []
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Load template
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            print(f"❌ Failed to load template image: {template_path}")
            return []
        
        template_height, template_width = template.shape[:2]
        
        # Perform template matching
        result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
        
        # Find all locations above threshold
        locations = np.where(result >= confidence)
        found_coords = []
        
        # Convert to center coordinates
        for pt in zip(*locations[::-1]):  # Switch x and y
            center_x = pt[0] + template_width // 2
            center_y = pt[1] + template_height // 2
            found_coords.append((center_x, center_y))
        
        print(f"✅ Found {len(found_coords)} instances of the icon")
        for i, (x, y) in enumerate(found_coords, 1):
            print(f"   Instance {i}: ({x}, {y})")
        
        return found_coords
        
    except Exception as e:
        print(f"❌ Error during icon detection: {e}")
        return []


def click_icon_by_template(template_path: str, confidence: float = 0.8, click_delay: float = 0.5) -> bool:
    """
    Find and click an icon using template matching
    
    Args:
        template_path (str): Path to the template image
        confidence (float): Minimum confidence threshold
        click_delay (float): Delay after clicking
        
    Returns:
        bool: True if icon was found and clicked, False otherwise
    """
    coords = find_icon_coordinates(template_path, confidence)
    
    if coords:
        x, y = coords
        print(f"🖱️ Clicking icon at ({x}, {y})")
        pyautogui.click(x, y)
        time.sleep(click_delay)
        return True
    
    return False


def interactive_icon_finder():
    """
    Interactive tool to find icons using template matching
    """
    print("🎯 Interactive Icon Finder")
    print("=" * 50)
    print("This tool helps you find icons on screen using template matching")
    print()
    
    while True:
        print("\nOptions:")
        print("1. Find single icon")
        print("2. Find all instances of an icon")
        print("3. Find and click icon")
        print("4. Exit")
        
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "4":
                print("👋 Goodbye!")
                break
            
            if choice not in ["1", "2", "3"]:
                print("❌ Invalid choice. Please enter 1-4.")
                continue
            
            # Get template path
            template_path = input("Enter path to template image: ").strip()
            if not template_path:
                print("❌ Template path cannot be empty")
                continue
            
            # Get confidence threshold
            try:
                confidence_input = input("Enter confidence threshold (0.0-1.0, default 0.8): ").strip()
                confidence = float(confidence_input) if confidence_input else 0.8
                if not 0.0 <= confidence <= 1.0:
                    print("❌ Confidence must be between 0.0 and 1.0")
                    continue
            except ValueError:
                print("❌ Invalid confidence value")
                continue
            
            # Execute chosen action
            if choice == "1":
                coords = find_icon_coordinates(template_path, confidence)
                if coords:
                    print(f"📍 Icon coordinates: {coords}")
                
            elif choice == "2":
                coords_list = find_all_icon_coordinates(template_path, confidence)
                if coords_list:
                    print(f"📍 Found {len(coords_list)} instances")
                
            elif choice == "3":
                success = click_icon_by_template(template_path, confidence)
                if success:
                    print("✅ Icon clicked successfully")
                else:
                    print("❌ Failed to find and click icon")
        
        except KeyboardInterrupt:
            print("\n\n⚠️ Operation cancelled")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def find_icon_coordinates_scaled(template_path: str, logical_x: int = None, logical_y: int = None, 
                               confidence: float = 0.8, screenshot_path: str = None) -> Optional[Tuple[int, int]]:
    """
    Find icon coordinates with automatic display scaling handling
    
    Args:
        template_path: Path to template image
        logical_x, logical_y: Expected logical coordinates (optional, for validation)
        confidence: Matching confidence threshold
        screenshot_path: Debug screenshot path
        
    Returns:
        Tuple[int, int]: Logical coordinates (for mouse clicking)
    """
    try:
        # Detect scaling
        scaling_factor = detect_display_scaling()
        
        # Check if template file exists
        if not os.path.exists(template_path):
            print(f"❌ Template image not found: {template_path}")
            return None
        
        # Take screenshot and convert to OpenCV format
        screenshot = pyautogui.screenshot()
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Save debug screenshot if requested
        if screenshot_path:
            if "debug/" in screenshot_path:
                os.makedirs("debug", exist_ok=True)
            cv2.imwrite(screenshot_path, screenshot_cv)
            print(f"📸 Screenshot saved to: {screenshot_path}")
        
        # Load template
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            print(f"❌ Failed to load template: {template_path}")
            return None
        
        # Get template dimensions
        template_height, template_width = template.shape[:2]
        
        # Perform template matching
        result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # Check confidence threshold
        if max_val < confidence:
            print(f"❌ Icon not found. Best confidence: {max_val:.3f} (threshold: {confidence:.3f})")
            return None
        
        # Calculate physical center coordinates
        physical_center_x = max_loc[0] + template_width // 2
        physical_center_y = max_loc[1] + template_height // 2
        
        # Convert to logical coordinates for mouse clicking
        logical_center_x, logical_center_y = physical_to_logical_coords(
            physical_center_x, physical_center_y, scaling_factor
        )
        
        print(f"✅ Icon found!")
        print(f"   Physical coords (screenshot): ({physical_center_x}, {physical_center_y})")
        print(f"   Logical coords (mouse): ({logical_center_x}, {logical_center_y})")
        print(f"   Confidence: {max_val:.3f}")
        
        # If expected logical coordinates provided, show comparison
        if logical_x is not None and logical_y is not None:
            distance = np.sqrt((logical_center_x - logical_x)**2 + (logical_center_y - logical_y)**2)
            print(f"   Distance from expected ({logical_x}, {logical_y}): {distance:.1f} pixels")
        
        return logical_center_x, logical_center_y
        
    except Exception as e:
        print(f"❌ Error during detection: {e}")
        return None

def click_icon_by_template_scaled(template_path: str, logical_x: int = None, logical_y: int = None,
                                confidence: float = 0.8, click_delay: float = 0.5) -> bool:
    """
    Find and click icon with automatic scaling handling
    
    Args:
        template_path: Path to template image
        logical_x, logical_y: Expected logical coordinates (optional)
        confidence: Matching confidence threshold  
        click_delay: Delay after clicking
        
    Returns:
        bool: True if icon found and clicked
    """
    coords = find_icon_coordinates_scaled(template_path, logical_x, logical_y, confidence)
    
    if coords:
        x, y = coords
        print(f"🖱️ Clicking at logical coordinates ({x}, {y})")
        pyautogui.click(x, y)
        time.sleep(click_delay)
        return True
    
    return False

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--live":
            continuous_display()
        elif sys.argv[1] == "--icon":
            interactive_icon_finder()
        elif sys.argv[1] == "--help":
            print("🎯 Coordinate Finder Tools")
            print("=" * 30)
            print("python find_coordinates.py              # Manual coordinate finding")
            print("python find_coordinates.py --live       # Live coordinate display")
            print("python find_coordinates.py --icon       # Interactive icon finder")
            print("python find_coordinates.py --help       # Show this help")
        else:
            print("❌ Unknown option. Use --help for usage info")
    else:
        find_coordinates()

if __name__ == "__main__":
    main() 