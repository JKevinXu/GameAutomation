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

class ActionAutomation:
    def __init__(self, verbose=False):
        self.mumu_path = self.find_mumu_path()
        self.verbose = verbose
        
        # Configure PyAutoGUI settings
        if AUTOMATION_AVAILABLE:
            pyautogui.FAILSAFE = PYAUTOGUI_SETTINGS['FAILSAFE']
            pyautogui.PAUSE = PYAUTOGUI_SETTINGS['PAUSE']
        
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
    
    def execute_click_action(self, action):
        """Execute a click action"""
        if not AUTOMATION_AVAILABLE:
            print("❌ Cannot click - automation libraries not available")
            return False
        
        coordinate_name = action.get('coordinate')
        if isinstance(coordinate_name, str):
            # Named coordinate
            if coordinate_name not in COORDINATES:
                print(f"❌ Unknown coordinate name: {coordinate_name}")
                return False
            x, y = COORDINATES[coordinate_name]
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
    
    args = parser.parse_args()
    
    # Check automation availability
    if not AUTOMATION_AVAILABLE and not args.open_only and not args.list_plans and not args.list_coords:
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
    elif args.plan:
        automation.execute_action_plan(args.plan)
    else:
        print("❌ No action plan specified!")
        print("\n📋 Usage examples:")
        print("   python action_automation.py basic_start")
        print("   python action_automation.py --list-plans")
        print("   python action_automation.py --list-coords")
        automation.list_available_plans()

if __name__ == "__main__":
    main() 