#!/usr/bin/env python3
"""
Action-Based Game Automation
Executes configurable action plans with clicks, waits, and other actions
"""

import argparse
import subprocess
import sys
import time
import os

# Import shared configuration
from config import ACTION_PLANS, COORDINATES, PYAUTOGUI_SETTINGS, MUMU_PATHS, TIMING, APPLICATION_PATHS

# Import automation libraries
try:
    import pyautogui
    AUTOMATION_AVAILABLE = True
except ImportError:
    AUTOMATION_AVAILABLE = False

# Import coordinate detection functions
try:
    from find_coordinates import find_icon_coordinates_scaled
    ICON_DETECTION_AVAILABLE = True
except ImportError:
    ICON_DETECTION_AVAILABLE = False

# Import avatar detection and text extraction
try:
    from avatar_message_block_detection import find_avatars_with_templates
    from message_text_extractor import MessageTextExtractor
    AVATAR_KEYWORD_DETECTION_AVAILABLE = True
except ImportError:
    AVATAR_KEYWORD_DETECTION_AVAILABLE = False

class ActionAutomation:
    def __init__(self, verbose=False):
        self.mumu_path = self.find_mumu_path()
        self.verbose = verbose
        
        # Configure PyAutoGUI settings
        if AUTOMATION_AVAILABLE:
            pyautogui.FAILSAFE = PYAUTOGUI_SETTINGS['FAILSAFE']
            pyautogui.PAUSE = PYAUTOGUI_SETTINGS['PAUSE']
        
        # Initialize text extractor for keyword detection
        self.text_extractor = None
        if AVATAR_KEYWORD_DETECTION_AVAILABLE:
            self.text_extractor = MessageTextExtractor()
    
    def log(self, message):
        """Print message if verbose mode is enabled"""
        if self.verbose:
            print(f"🔍 DEBUG: {message}")
        
    def find_mumu_path(self):
        """Find MuMu模拟器Pro installation path on Mac"""
        for path in MUMU_PATHS:
            if os.path.exists(path):
                return path
        return None
    
    def open_mumu(self):
        """Open MuMu模拟器Pro"""
        if not self.mumu_path:
            print("❌ MuMu模拟器Pro not found in Applications folder")
            print("Please make sure MuMu模拟器Pro is installed")
            return False
        
        try:
            print(f"🚀 Opening MuMu模拟器Pro from {self.mumu_path}")
            subprocess.run(["open", self.mumu_path], check=True)
            print("✅ MuMu模拟器Pro launched successfully")
            
            # Wait for the emulator to start
            print("⏳ Waiting for emulator interface to load...")
            time.sleep(TIMING['MUMU_STARTUP_WAIT'])
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to open MuMu模拟器Pro: {e}")
            return False
    
    def execute_action(self, action):
        """Execute a single action from the action plan"""
        action_type = action.get('action')
        description = action.get('description', 'No description')
        
        print(f"📋 {description}")
        
        if action_type == 'click':
            return self.execute_click_action(action)
        elif action_type == 'avatar_keyword_click':
            return self.execute_avatar_keyword_click_action(action)
        elif action_type == 'wait':
            return self.execute_wait_action(action)
        elif action_type == 'open_app':
            return self.execute_open_app_action(action)
        elif action_type == 'open_mumu':
            # Legacy support
            return self.open_mumu()
        else:
            print(f"❌ Unknown action type: {action_type}")
            return False
    
    def execute_avatar_keyword_click_action(self, action):
        """
        Execute avatar keyword click action - finds avatars and returns coordinates if keyword is found
        
        Args:
            action: Dictionary containing:
                - 'keywords': Single keyword string or list of keywords to check for
                - 'avatar_templates': List of avatar template paths (optional, defaults to all available)
                - 'confidence': Avatar detection confidence threshold (optional, default 0.8)
                - 'return_coordinates': If True, returns coordinates instead of clicking (optional, default False)
        
        Returns:
            bool or dict: True/False for success/failure, or coordinates dict if return_coordinates=True
        """
        if not AVATAR_KEYWORD_DETECTION_AVAILABLE:
            print("❌ Avatar keyword detection not available - missing avatar_message_block_detection or message_text_extractor")
            return False
        
        if not self.text_extractor:
            print("❌ Text extractor not initialized")
            return False
        
        # Get action parameters
        keywords = action.get('keywords')
        if not keywords:
            print("❌ No keywords specified for avatar_keyword_click action")
            return False
        
        # Convert single keyword to list
        if isinstance(keywords, str):
            keywords = [keywords]
        
        avatar_templates = action.get('avatar_templates')
        if not avatar_templates:
            # Use all available templates
            from avatar_message_block_detection import list_available_templates
            avatar_templates = list_available_templates()
            if not avatar_templates:
                print("❌ No avatar templates available")
                return False
        
        confidence = action.get('confidence', 0.8)
        return_coordinates = action.get('return_coordinates', False)
        
        try:
            print(f"🔍 Searching for avatars with keywords: {keywords}")
            print(f"🎯 Using {len(avatar_templates)} avatar templates")
            
            # Find avatars using template matching
            avatar_detections = find_avatars_with_templates(avatar_templates, confidence)
            
            if not avatar_detections:
                print("❌ No avatars detected")
                return False
            
            print(f"✅ Found {len(avatar_detections)} avatar(s)")
            
            # Check each detected avatar's message block for keywords
            for i, detection in enumerate(avatar_detections, 1):
                avatar = detection['avatar']
                text_analysis = detection['text_analysis']
                click_coords = detection['click_coordinates']['recommended']
                
                print(f"\n🔍 Checking avatar {i} for keywords...")
                
                # Extract text area image for keyword analysis
                from avatar_message_block_detection import capture_chat_region
                chat_image = capture_chat_region()
                
                # Get text area bounds
                text_bounds = text_analysis['text_area_bounds']
                text_area_image = chat_image[
                    text_bounds['y']:text_bounds['y'] + text_bounds['height'],
                    text_bounds['x']:text_bounds['x'] + text_bounds['width']
                ]
                
                # Check for keywords using LLM
                if len(keywords) == 1:
                    keyword_result = self.text_extractor.contains_keyword(text_area_image, keywords[0])
                else:
                    keyword_result = self.text_extractor.contains_any_keyword(text_area_image, keywords)
                
                # Check if keywords were found
                is_related = keyword_result.get('is_related', False) or keyword_result.get('is_related_to_any', False)
                confidence_score = keyword_result.get('confidence', 0)
                
                if is_related and confidence_score >= 70:  # Require at least 70% confidence
                    print(f"✅ Keywords found in avatar {i} message block!")
                    print(f"   Confidence: {confidence_score}%")
                    if keyword_result.get('explanation'):
                        print(f"   Explanation: {keyword_result['explanation']}")
                    
                    # Convert physical coordinates back to logical coordinates
                    logical_x = click_coords['x'] // 2  # Divide by scale factor
                    logical_y = click_coords['y'] // 2
                    
                    coordinates_result = {
                        'x': logical_x,
                        'y': logical_y,
                        'physical_x': click_coords['x'],
                        'physical_y': click_coords['y'],
                        'avatar_info': {
                            'template': avatar['template_name'],
                            'confidence': avatar['confidence'],
                            'position': (avatar['x'], avatar['y'])
                        },
                        'keyword_info': keyword_result
                    }
                    
                    if return_coordinates:
                        print(f"📍 Returning coordinates: logical ({logical_x}, {logical_y}), physical ({click_coords['x']}, {click_coords['y']})")
                        return coordinates_result
                    else:
                        # Click the avatar
                        print(f"🖱️  Clicking avatar at logical coordinates ({logical_x}, {logical_y})")
                        pyautogui.click(logical_x, logical_y)
                        print("✅ Avatar clicked successfully!")
                        return True
                else:
                    if is_related:
                        print(f"⚠️  Keywords found but confidence too low: {confidence_score}%")
                    else:
                        print(f"❌ Keywords not found in avatar {i}")
            
            print("❌ No avatars with matching keywords found")
            return False
            
        except Exception as e:
            print(f"❌ Avatar keyword click action failed: {e}")
            return False
    
    def execute_click_action(self, action):
        """Execute a click action"""
        if not AUTOMATION_AVAILABLE:
            print("❌ Cannot click - automation libraries not available")
            return False
        
        coordinate_name = action.get('coordinate')
        if isinstance(coordinate_name, str):
            # Check if it's a named coordinate
            if coordinate_name in COORDINATES:
                coord_value = COORDINATES[coordinate_name]
                
                # Check if coordinate value is a PNG template path
                if isinstance(coord_value, str) and coord_value.endswith('.png'):
                    # Use PNG template matching to get coordinates
                    if not ICON_DETECTION_AVAILABLE:
                        print("❌ Cannot use icon detection - find_coordinates module not available")
                        return False
                    
                    confidence = action.get('confidence', 0.8)
                    
                    try:
                        print(f"🔍 Detecting coordinates for icon: {coord_value}")
                        print(f"🎯 Confidence threshold: {confidence}")
                        
                        coords = find_icon_coordinates_scaled(
                            template_path=coord_value,
                            confidence=confidence
                        )
                        
                        if coords:
                            x, y = coords
                            print(f"✅ Icon detected at coordinates: ({x}, {y})")
                        else:
                            print("❌ Failed to detect icon coordinates")
                            return False
                            
                    except Exception as e:
                        print(f"❌ Icon detection failed: {e}")
                        return False
                else:
                    # Regular coordinate tuple
                    x, y = coord_value
            else:
                print(f"❌ Unknown coordinate name: {coordinate_name}")
                return False
        elif isinstance(coordinate_name, (list, tuple)) and len(coordinate_name) == 2:
            # Direct coordinate tuple
            x, y = coordinate_name
        else:
            print(f"❌ Invalid coordinate format: {coordinate_name}")
            return False
        
        try:
            self.log(f"Clicking at ({x}, {y})")
            print(f"🖱️  Clicking at ({x}, {y})")
            pyautogui.click(x, y)
            print("✅ Click successful!")
            return True
            
        except Exception as e:
            print(f"❌ Click failed: {e}")
            return False
    

    def execute_wait_action(self, action):
        """Execute a wait action"""
        duration = action.get('duration', 1)
        
        try:
            print(f"⏳ Waiting {duration} seconds...")
            time.sleep(duration)
            print("✅ Wait completed!")
            return True
            
        except Exception as e:
            print(f"❌ Wait failed: {e}")
            return False
    
    def execute_open_app_action(self, action):
        """Execute an open application action"""
        app_name = action.get('app')
        
        if not app_name:
            print("❌ No app specified in open_app action")
            return False
        
        if app_name not in APPLICATION_PATHS:
            print(f"❌ Unknown application: {app_name}")
            print(f"Available apps: {', '.join(APPLICATION_PATHS.keys())}")
            return False
        
        app_path = APPLICATION_PATHS[app_name]
        
        if not os.path.exists(app_path):
            print(f"❌ Application not found: {app_path}")
            return False
        
        try:
            print(f"🚀 Opening {app_name} from {app_path}")
            subprocess.run(["open", app_path], check=True)
            print(f"✅ {app_name} launched successfully")
            
            # Wait for the application to start
            if app_name == 'mumu':
                print("⏳ Waiting for emulator interface to load...")
                time.sleep(TIMING['MUMU_STARTUP_WAIT'])
            else:
                print("⏳ Waiting for application to load...")
                time.sleep(1)  # Default 1 second wait for other apps
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to open {app_name}: {e}")
            return False
    
    def find_avatar_coordinates_for_keyword(self, keywords, avatar_templates=None, confidence=0.8):
        """
        Helper method to find avatar coordinates for a specific keyword without clicking
        
        Args:
            keywords: Single keyword string or list of keywords to check for
            avatar_templates: List of avatar template paths (optional)
            confidence: Avatar detection confidence threshold (optional)
            
        Returns:
            dict or None: Coordinates and metadata if found, None otherwise
        """
        action = {
            'action': 'avatar_keyword_click',
            'keywords': keywords,
            'avatar_templates': avatar_templates,
            'confidence': confidence,
            'return_coordinates': True,
            'description': f'Find coordinates for keyword: {keywords}'
        }
        
        return self.execute_avatar_keyword_click_action(action)
    
    def execute_action_plan(self, plan_name):
        """Execute a complete action plan"""
        if plan_name not in ACTION_PLANS:
            print(f"❌ Unknown action plan: {plan_name}")
            print(f"Available plans: {', '.join(ACTION_PLANS.keys())}")
            return False
        
        action_plan = ACTION_PLANS[plan_name]
        
        print("🎮 Starting Action-Based Game Automation")
        print("=" * 50)
        print(f"📋 Executing plan: '{plan_name}'")
        print(f"📊 Total actions: {len(action_plan)}")
        print("-" * 50)
        
        for i, action in enumerate(action_plan, 1):
            print(f"\n🔄 Step {i}/{len(action_plan)}:")
            
            if not self.execute_action(action):
                print(f"❌ Failed at step {i}. Stopping execution.")
                return False
        
        print("\n" + "=" * 50)
        print("🎉 Action plan completed successfully!")
        return True
    
    def list_available_plans(self):
        """List all available action plans"""
        print("📋 Available Action Plans:")
        print("=" * 40)
        
        for plan_name, actions in ACTION_PLANS.items():
            print(f"\n🎯 {plan_name}:")
            for i, action in enumerate(actions, 1):
                action_type = action.get('action', 'unknown')
                description = action.get('description', 'No description')
                
                if action_type == 'click':
                    coord = action.get('coordinate', 'unknown')
                    print(f"   {i}. Click {coord} - {description}")
                elif action_type == 'avatar_keyword_click':
                    keywords = action.get('keywords', 'unknown')
                    print(f"   {i}. Avatar keyword click [{keywords}] - {description}")
                elif action_type == 'wait':
                    duration = action.get('duration', 'unknown')
                    print(f"   {i}. Wait {duration}s - {description}")
                elif action_type == 'open_app':
                    app = action.get('app', 'unknown')
                    print(f"   {i}. Open {app} - {description}")
                else:
                    print(f"   {i}. {action_type} - {description}")
    
    def list_coordinates(self):
        """List all available named coordinates"""
        print("📍 Available Coordinates:")
        print("=" * 30)
        
        for name, (x, y) in COORDINATES.items():
            print(f"   {name}: ({x}, {y})")

def main():
    parser = argparse.ArgumentParser(description="Action-Based Game Automation Tool")
    parser.add_argument("plan", nargs='?', help="Action plan to execute")
    parser.add_argument("--list-plans", action="store_true", 
                       help="List all available action plans")
    parser.add_argument("--list-coords", action="store_true",
                       help="List all available coordinates")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")
    parser.add_argument("--open-only", action="store_true", 
                       help="Only open MuMu模拟器Pro without running automation")
    parser.add_argument("--find-keyword", type=str,
                       help="Find avatar coordinates for specified keyword without clicking")
    
    args = parser.parse_args()
    
    # Check automation availability
    if not AUTOMATION_AVAILABLE and not args.open_only and not args.list_plans and not args.list_coords and not args.find_keyword:
        print("⚠️  Automation libraries not found!")
        print("📦 Install with: pip install pyautogui")
        sys.exit(1)
    
    automation = ActionAutomation(verbose=args.verbose)
    
    if args.list_plans:
        automation.list_available_plans()
    elif args.list_coords:
        automation.list_coordinates()
    elif args.open_only:
        automation.open_mumu()
    elif args.find_keyword:
        print(f"🔍 Finding avatar coordinates for keyword: {args.find_keyword}")
        result = automation.find_avatar_coordinates_for_keyword(args.find_keyword)
        if result:
            print("✅ Coordinates found:")
            print(f"   Logical: ({result['x']}, {result['y']})")
            print(f"   Physical: ({result['physical_x']}, {result['physical_y']})")
            print(f"   Avatar: {result['avatar_info']['template']} (confidence: {result['avatar_info']['confidence']:.3f})")
            print(f"   Keyword confidence: {result['keyword_info']['confidence']}%")
        else:
            print("❌ No avatar found with the specified keyword")
    elif args.plan:
        automation.execute_action_plan(args.plan)
    else:
        print("❌ No action plan specified!")
        print("\n📋 Usage examples:")
        print("   python action_automation.py basic_start")
        print("   python action_automation.py --list-plans")
        print("   python action_automation.py --list-coords")
        print("   python action_automation.py --find-keyword 320")

if __name__ == "__main__":
    main() 