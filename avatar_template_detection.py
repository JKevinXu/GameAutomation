#!/usr/bin/env python3
"""
Avatar Template Detection
Find specific avatars using template matching, then analyze text areas to their right
"""

import pyautogui
import cv2
import numpy as np
import os
import argparse
from datetime import datetime
from typing import Tuple, List, Dict, Optional

# Configuration
CHAT_AREA = (660, 145, 935, 496)  # Logical coordinates
SCALE_FACTOR = 2
OUTPUT_DIR = "debug/avatar_template"
AVATAR_TEMPLATES_DIR = "game_elements/avatar"

# Text area analysis settings - Message area size based on (720,347) to (930,458)
# Enlarged with scaling factor of 2 for physical coordinates
TEXT_AREA_OFFSET_X = 10  # Pixels to the right of avatar to start looking for text
TEXT_AREA_WIDTH = 420   # Width of text area to analyze (930-720) * 2
TEXT_AREA_HEIGHT = 222  # Height of text area (458-347) * 2
TEXT_AREA_HEIGHT_PADDING = 0  # No padding since we have exact height

def setup_directories():
    """Create necessary directories"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(AVATAR_TEMPLATES_DIR, exist_ok=True)
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print(f"📁 Avatar directory: {AVATAR_TEMPLATES_DIR}")

def capture_chat_region() -> np.ndarray:
    """Capture chat region with scaling"""
    x1, y1, x2, y2 = CHAT_AREA
    
    # Scale to physical coordinates
    physical_x1 = int(x1 * SCALE_FACTOR)
    physical_y1 = int(y1 * SCALE_FACTOR)
    physical_x2 = int(x2 * SCALE_FACTOR)
    physical_y2 = int(y2 * SCALE_FACTOR)
    
    print(f"📸 Capturing chat region: logical ({x1}, {y1}) to ({x2}, {y2})")
    print(f"📸 Physical coordinates: ({physical_x1}, {physical_y1}) to ({physical_x2}, {physical_y2})")
    
    full_screenshot = pyautogui.screenshot()
    chat_region = full_screenshot.crop((physical_x1, physical_y1, physical_x2, physical_y2))
    
    chat_array = np.array(chat_region)
    chat_cv = cv2.cvtColor(chat_array, cv2.COLOR_RGB2BGR)
    
    return chat_cv

def find_avatar_by_template(chat_image: np.ndarray, template_path: str, 
                           confidence: float = 0.8) -> List[Dict]:
    """
    Find avatar using template matching
    
    Args:
        chat_image: Screenshot of chat area
        template_path: Path to avatar template image
        confidence: Matching confidence threshold
        
    Returns:
        List of detected avatar locations with metadata
    """
    if not os.path.exists(template_path):
        print(f"❌ Template not found: {template_path}")
        return []
    
    # Load template
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        print(f"❌ Failed to load template: {template_path}")
        return []
    
    template_height, template_width = template.shape[:2]
    
    # Perform template matching
    result = cv2.matchTemplate(chat_image, template, cv2.TM_CCOEFF_NORMED)
    
    # Find all locations above threshold
    locations = np.where(result >= confidence)
    
    avatar_detections = []
    
    for pt in zip(*locations[::-1]):  # Switch x and y
        match_confidence = result[pt[1], pt[0]]
        
        avatar_detection = {
            'template_name': os.path.basename(template_path),
            'x': pt[0],
            'y': pt[1],
            'width': template_width,
            'height': template_height,
            'confidence': float(match_confidence),
            'center_x': pt[0] + template_width // 2,
            'center_y': pt[1] + template_height // 2
        }
        
        avatar_detections.append(avatar_detection)
    
    print(f"✅ Found {len(avatar_detections)} instances of {os.path.basename(template_path)}")
    
    return avatar_detections

def analyze_text_area_right_of_avatar(chat_image: np.ndarray, avatar: Dict) -> Dict:
    """
    Analyze the text area to the right of a detected avatar using specified dimensions
    
    Args:
        chat_image: Screenshot of chat area
        avatar: Avatar detection dictionary
        
    Returns:
        Analysis results including text area bounds and characteristics
    """
    chat_height, chat_width = chat_image.shape[:2]
    
    # Define text area bounds relative to avatar with specified dimensions
    text_x = avatar['x'] + avatar['width'] + TEXT_AREA_OFFSET_X
    text_y = avatar['y']  # Align with avatar top
    text_width = min(TEXT_AREA_WIDTH, chat_width - text_x)
    text_height = TEXT_AREA_HEIGHT
    
    # Ensure bounds are within image
    if text_x >= chat_width or text_y >= chat_height:
        return None
    
    # Adjust if the area would exceed image bounds
    if text_x + text_width > chat_width:
        text_width = chat_width - text_x
    if text_y + text_height > chat_height:
        text_height = chat_height - text_y
    
    # Extract text area
    text_area = chat_image[text_y:text_y + text_height, text_x:text_x + text_width]
    
    # Analyze text area characteristics
    gray_text = cv2.cvtColor(text_area, cv2.COLOR_BGR2GRAY)
    
    # Calculate text density (rough estimate)
    edges = cv2.Canny(gray_text, 50, 150)
    text_density = np.sum(edges > 0) / (text_width * text_height)
    
    # Calculate color variance (text areas usually have more variation)
    color_variance = np.var(gray_text)
    
    text_analysis = {
        'text_area_bounds': {
            'x': text_x,
            'y': text_y,
            'width': text_width,
            'height': text_height
        },
        'text_density': text_density,
        'color_variance': float(color_variance),
        'has_text_likely': text_density > 0.02 and color_variance > 100,  # Heuristic thresholds
        'message_block_bounds': {
            'x': 0,  # Full width from left edge
            'y': text_y,
            'width': text_x + text_width,
            'height': text_height
        }
    }
    
    return text_analysis

def calculate_click_coordinates(avatar: Dict, text_analysis: Dict) -> Dict:
    """
    Calculate optimal click coordinates for the avatar
    """
    # Multiple click options
    click_options = {
        'avatar_center': {
            'x': avatar['center_x'],
            'y': avatar['center_y'],
            'description': 'Center of avatar'
        },
        'avatar_right_edge': {
            'x': avatar['x'] + avatar['width'] - 5,
            'y': avatar['center_y'],
            'description': 'Right edge of avatar'
        },
        'message_left_area': {
            'x': max(5, avatar['x'] - 10),
            'y': avatar['center_y'],
            'description': 'Left area of message block'
        }
    }
    
    # Recommend best click point (avatar center is usually safest)
    recommended_click = click_options['avatar_center']
    
    return {
        'recommended': recommended_click,
        'options': click_options
    }

def find_avatars_with_templates(template_paths: List[str], confidence: float = 0.8) -> List[Dict]:
    """
    Main function to find avatars using multiple templates
    
    Args:
        template_paths: List of paths to avatar template images
        confidence: Matching confidence threshold
        
    Returns:
        List of detected avatars with analysis
    """
    print("🎯 Starting Avatar Template Detection")
    print("=" * 50)
    
    setup_directories()
    
    # Capture chat region
    chat_image = capture_chat_region()
    chat_height, chat_width = chat_image.shape[:2]
    
    # Save full chat screenshot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_chat_path = os.path.join(OUTPUT_DIR, f"full_chat_{timestamp}.png")
    cv2.imwrite(full_chat_path, chat_image)
    print(f"📸 Saved full chat screenshot: {full_chat_path}")
    
    all_detections = []
    
    # Process each template
    for template_path in template_paths:
        print(f"\n🔍 Processing template: {template_path}")
        
        avatar_detections = find_avatar_by_template(chat_image, template_path, confidence)
        
        for avatar in avatar_detections:
            # Analyze text area to the right
            text_analysis = analyze_text_area_right_of_avatar(chat_image, avatar)
            
            if text_analysis:
                # Calculate click coordinates
                click_coords = calculate_click_coordinates(avatar, text_analysis)
                
                # Combine all information
                detection_result = {
                    'avatar': avatar,
                    'text_analysis': text_analysis,
                    'click_coordinates': click_coords,
                    'template_file': template_path
                }
                
                all_detections.append(detection_result)
    
    # Remove duplicate detections (same avatar detected by multiple templates)
    unique_detections = remove_duplicate_detections(all_detections)
    
    # Create visualization
    if unique_detections:
        visualize_avatar_detections(chat_image, unique_detections, timestamp)
        print_detection_results(unique_detections)
    else:
        print("❌ No avatars detected")
    
    return unique_detections

def remove_duplicate_detections(detections: List[Dict], min_distance: int = 50) -> List[Dict]:
    """
    Remove duplicate detections that are too close to each other
    """
    if len(detections) <= 1:
        return detections
    
    unique_detections = []
    
    for detection in detections:
        is_duplicate = False
        avatar = detection['avatar']
        
        for existing in unique_detections:
            existing_avatar = existing['avatar']
            
            # Calculate distance between centers
            distance = np.sqrt((avatar['center_x'] - existing_avatar['center_x'])**2 + 
                             (avatar['center_y'] - existing_avatar['center_y'])**2)
            
            if distance < min_distance:
                # Keep the one with higher confidence
                if avatar['confidence'] > existing_avatar['confidence']:
                    # Replace existing with current
                    unique_detections.remove(existing)
                    unique_detections.append(detection)
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique_detections.append(detection)
    
    print(f"📊 Removed duplicates: {len(detections)} → {len(unique_detections)} unique detections")
    return unique_detections

def visualize_avatar_detections(chat_image: np.ndarray, detections: List[Dict], timestamp: str):
    """
    Create visualization of avatar detections and text areas
    """
    debug_image = chat_image.copy()
    
    for i, detection in enumerate(detections):
        avatar = detection['avatar']
        text_analysis = detection['text_analysis']
        click_coords = detection['click_coordinates']['recommended']
        
        # Draw avatar bounding box in red
        cv2.rectangle(debug_image,
                     (avatar['x'], avatar['y']),
                     (avatar['x'] + avatar['width'], avatar['y'] + avatar['height']),
                     (0, 0, 255), 2)  # Red
        
        # Draw text area in green
        text_bounds = text_analysis['text_area_bounds']
        cv2.rectangle(debug_image,
                     (text_bounds['x'], text_bounds['y']),
                     (text_bounds['x'] + text_bounds['width'], text_bounds['y'] + text_bounds['height']),
                     (0, 255, 0), 1)  # Green
        
        # Draw message block in blue
        msg_bounds = text_analysis['message_block_bounds']
        cv2.rectangle(debug_image,
                     (msg_bounds['x'], msg_bounds['y']),
                     (msg_bounds['x'] + msg_bounds['width'], msg_bounds['y'] + msg_bounds['height']),
                     (255, 0, 0), 1)  # Blue
        
        # Draw click point
        cv2.circle(debug_image, (click_coords['x'], click_coords['y']), 5, (0, 0, 255), -1)
        
        # Label
        cv2.putText(debug_image, f"Avatar {i+1}", 
                   (avatar['x'], avatar['y'] - 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        # Show confidence
        cv2.putText(debug_image, f"{avatar['confidence']:.2f}", 
                   (avatar['x'], avatar['y'] + avatar['height'] + 15), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
    
    # Save visualization
    filename = f"avatar_detections_{timestamp}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    cv2.imwrite(filepath, debug_image)
    
    print(f"💾 Saved detection visualization: {filepath}")

def print_detection_results(detections: List[Dict]):
    """
    Print detailed results of avatar detections
    """
    print("\n📋 Avatar Detection Results:")
    print("=" * 50)
    
    for i, detection in enumerate(detections, 1):
        avatar = detection['avatar']
        text_analysis = detection['text_analysis']
        click_coords = detection['click_coordinates']['recommended']
        
        print(f"\n🎯 Avatar {i} ({avatar['template_name']}):")
        print(f"   Position: ({avatar['x']}, {avatar['y']})")
        print(f"   Size: {avatar['width']}x{avatar['height']}")
        print(f"   Confidence: {avatar['confidence']:.3f}")
        print(f"   Click at: ({click_coords['x']}, {click_coords['y']})")
        print(f"   Text likely: {text_analysis['has_text_likely']}")
        print(f"   Text density: {text_analysis['text_density']:.4f}")

def list_available_templates() -> List[str]:
    """List all available avatar template files"""
    if not os.path.exists(AVATAR_TEMPLATES_DIR):
        return []
    
    template_files = []
    for file in os.listdir(AVATAR_TEMPLATES_DIR):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            template_files.append(os.path.join(AVATAR_TEMPLATES_DIR, file))
    
    return template_files

def main():
    parser = argparse.ArgumentParser(description="Find avatars using template matching")
    parser.add_argument("templates", nargs='*', help="Avatar template image paths")
    parser.add_argument("--confidence", "-c", type=float, default=0.8,
                       help="Matching confidence threshold (0.0-1.0)")
    parser.add_argument("--list-templates", action="store_true",
                       help="List available template files")
    parser.add_argument("--all-templates", action="store_true",
                       help="Use all templates in the templates directory")
    
    args = parser.parse_args()
    
    setup_directories()
    
    if args.list_templates:
        templates = list_available_templates()
        print("📋 Available avatar templates:")
        for template in templates:
            print(f"   {template}")
        return
    
    # Determine which templates to use
    template_paths = []
    
    if args.all_templates:
        template_paths = list_available_templates()
        if not template_paths:
            print(f"❌ No template files found in {AVATAR_TEMPLATES_DIR}")
            print("💡 Add .png/.jpg files to the game_elements/avatar/ directory")
            return
    elif args.templates:
        template_paths = args.templates
    else:
        print("❌ No templates specified!")
        print("\n📋 Usage examples:")
        print("   python avatar_template_detection.py game_elements/avatar/user1.png")
        print("   python avatar_template_detection.py --all-templates")
        print("   python avatar_template_detection.py --list-templates")
        return
    
    # Run detection
    detections = find_avatars_with_templates(template_paths, args.confidence)
    
    if detections:
        print(f"\n✅ Successfully detected {len(detections)} avatars!")
    else:
        print("\n❌ No avatars found. Try:")
        print("   - Lowering confidence with --confidence 0.6")
        print("   - Checking template images are clear")
        print("   - Ensuring game chat is visible")

if __name__ == "__main__":
    main() 