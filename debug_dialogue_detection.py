#!/usr/bin/env python3
"""
Debug script to investigate dialogue icon detection discrepancy
Expected: (605, 420) vs Detected: (1212, 843)
"""

import cv2
import numpy as np
import pyautogui
import os
from find_coordinates import find_icon_coordinates, find_all_icon_coordinates, detect_display_scaling, logical_to_physical_coords, physical_to_logical_coords

def debug_detection_area():
    """Debug what's being detected at different locations"""
    print("🔍 Debugging Dialogue Icon Detection")
    print("=" * 50)
    
    # Ensure debug directory exists
    os.makedirs("debug", exist_ok=True)
    
    # Detect display scaling
    scaling_factor = detect_display_scaling()
    
    template_path = "game_elements/dialogue_icon.png"
    expected_logical = (605, 420)
    expected_physical = logical_to_physical_coords(605, 420, scaling_factor)
    
    print(f"🎯 Expected logical coords (mouse): {expected_logical}")
    print(f"🎯 Expected physical coords (screenshot): {expected_physical}")
    
    # Take current screenshot
    screenshot = pyautogui.screenshot()
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # Load template
    template = cv2.imread(template_path)
    if template is None:
        print("❌ Could not load template")
        return
    
    template_h, template_w = template.shape[:2]
    print(f"📏 Template size: {template_w} x {template_h}")
    
    # Get screen dimensions
    screen_w, screen_h = screenshot.size
    print(f"📺 Screen size: {screen_w} x {screen_h}")
    
    # Check what's at the expected position (using physical coordinates)
    exp_x, exp_y = expected_physical
    
    # Extract region around expected position
    margin = 50
    exp_region = screenshot_cv[
        max(0, exp_y-margin):min(screen_h, exp_y+margin),
        max(0, exp_x-margin):min(screen_w, exp_x+margin)
    ]
    cv2.imwrite("debug/expected_region.png", exp_region)
    print(f"💾 Saved expected region to: debug/expected_region.png")
    print(f"📏 Region extracted from physical coords: ({exp_x-margin}, {exp_y-margin}) to ({exp_x+margin}, {exp_y+margin})")
    
    # Perform template matching with debug info
    result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    detected_x = max_loc[0] + template_w // 2
    detected_y = max_loc[1] + template_h // 2
    
    print(f"\n🎯 Detected position: ({detected_x}, {detected_y})")
    print(f"📊 Best match confidence: {max_val:.3f}")
    
    # Extract region around detected position
    det_region = screenshot_cv[
        max(0, detected_y-margin):min(screen_h, detected_y+margin),
        max(0, detected_x-margin):min(screen_w, detected_x+margin)
    ]
    cv2.imwrite("debug/detected_region.png", det_region)
    print(f"💾 Saved detected region to: debug/detected_region.png")
    
    # Check confidence at expected position
    if (0 <= exp_x < result.shape[1] and 0 <= exp_y < result.shape[0]):
        exp_confidence = result[exp_y, exp_x]
        print(f"📊 Confidence at expected position: {exp_confidence:.3f}")
    
    # Save full screenshot with markers
    marked_screenshot = screenshot_cv.copy()
    
    # Mark expected position (green circle) - use physical coordinates
    cv2.circle(marked_screenshot, expected_physical, 20, (0, 255, 0), 3)
    cv2.putText(marked_screenshot, "Expected", (expected_physical[0]-50, expected_physical[1]-30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Mark detected position (red circle)
    cv2.circle(marked_screenshot, (detected_x, detected_y), 20, (0, 0, 255), 3)
    cv2.putText(marked_screenshot, "Detected", (detected_x-50, detected_y-30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    cv2.imwrite("debug/comparison_screenshot.png", marked_screenshot)
    print(f"💾 Saved comparison screenshot to: debug/comparison_screenshot.png")
    
    # Distance between positions (both in physical coordinates)
    distance = np.sqrt((detected_x - expected_physical[0])**2 + (detected_y - expected_physical[1])**2)
    print(f"📏 Distance between expected and detected: {distance:.1f} pixels (physical coords)")
    
    # Also show logical coordinate distance
    from find_coordinates import physical_to_logical_coords
    detected_logical = physical_to_logical_coords(detected_x, detected_y, scaling_factor)
    logical_distance = np.sqrt((detected_logical[0] - expected_logical[0])**2 + (detected_logical[1] - expected_logical[1])**2)
    print(f"📏 Distance in logical coordinates: {logical_distance:.1f} pixels")

def test_at_expected_position():
    """Test detection with a lower confidence at the expected position"""
    print("\n🧪 Testing at Expected Position")
    print("=" * 40)
    
    template_path = "game_elements/dialogue_icon.png"
    
    # Try different confidence levels
    confidence_levels = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
    
    for confidence in confidence_levels:
        print(f"\nTrying confidence: {confidence}")
        coords = find_icon_coordinates(template_path, confidence=confidence)
        
        if coords:
            distance_to_expected = np.sqrt((coords[0] - 605)**2 + (coords[1] - 420)**2)
            print(f"✅ Found at: {coords}, distance to expected: {distance_to_expected:.1f}px")
            
            if distance_to_expected < 100:  # Within 100 pixels of expected
                print("🎯 This match is close to your expected position!")
                break
        else:
            print(f"❌ Not found at confidence {confidence}")

def check_multiple_matches_near_expected():
    """Check for matches near the expected position"""
    print("\n🔍 Checking for Multiple Matches Near Expected Position")
    print("=" * 60)
    
    # Detect scaling for consistent coordinate handling
    scaling_factor = detect_display_scaling()
    
    template_path = "game_elements/dialogue_icon.png"
    expected_logical = (605, 420)
    expected_physical = logical_to_physical_coords(605, 420, scaling_factor)
    
    # Get all matches with lower confidence
    all_coords = find_all_icon_coordinates(template_path, confidence=0.5)
    
    print(f"\nAnalyzing {len(all_coords)} total matches...")
    
    close_matches = []
    for coords in all_coords:
        # Convert physical match coordinates to logical for comparison
        logical_coords = physical_to_logical_coords(coords[0], coords[1], scaling_factor)
        distance = np.sqrt((logical_coords[0] - expected_logical[0])**2 + (logical_coords[1] - expected_logical[1])**2)
        if distance < 200:  # Within 200 logical pixels
            close_matches.append((logical_coords, distance))
    
    if close_matches:
        print(f"\n🎯 Found {len(close_matches)} matches within 200px of expected position:")
        close_matches.sort(key=lambda x: x[1])  # Sort by distance
        
        for i, (coords, distance) in enumerate(close_matches[:10]):  # Show top 10
            print(f"   {i+1}. {coords} (distance: {distance:.1f}px)")
    else:
        print("❌ No matches found near expected position")

def main():
    """Main debugging function"""
    print("🐛 Dialogue Icon Detection Debugger")
    print("=" * 60)
    print("Expected position: (605, 420)")
    print("Detected position: (1212, 843)")
    print("Let's investigate the discrepancy...")
    print()
    
    try:
        debug_detection_area()
        test_at_expected_position()
        check_multiple_matches_near_expected()
        
        print("\n" + "=" * 60)
        print("🔍 Debug Summary:")
        print("1. Check 'debug/comparison_screenshot.png' to see both positions marked")
        print("2. Check 'debug/expected_region.png' and 'debug/detected_region.png' to compare areas")
        print("3. Look for the closest match to your expected position above")
        print("\n💡 Possible reasons for discrepancy:")
        print("- Multiple monitors or different screen scaling")
        print("- Template might be matching a different UI element")
        print("- Game UI might have changed or moved")
        print("- Screenshot might be from a different resolution")
        
    except Exception as e:
        print(f"❌ Error during debugging: {e}")

if __name__ == "__main__":
    main() 