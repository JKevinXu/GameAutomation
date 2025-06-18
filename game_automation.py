#!/usr/bin/env python3
"""
Gameplay Automation Tool
A command-line tool for automating gameplay in MuMu模拟器Pro
"""

import argparse
import subprocess
import sys
import time
import os
from pathlib import Path

# Import automation libraries
try:
    import pyautogui
    AUTOMATION_AVAILABLE = True
except ImportError:
    AUTOMATION_AVAILABLE = False

class GameAutomation:
    def __init__(self, verbose=False):
        self.mumu_path = self.find_mumu_path()
        self.verbose = verbose
        
        # Configure PyAutoGUI settings
        if AUTOMATION_AVAILABLE:
            pyautogui.FAILSAFE = True  # Move mouse to top-left corner to stop
            pyautogui.PAUSE = 0.5      # Small pause between actions
        
    def log(self, message):
        """Print message if verbose mode is enabled"""
        if self.verbose:
            print(f"🔍 DEBUG: {message}")
        
    def find_mumu_path(self):
        """Find MuMu模拟器Pro installation path on Mac"""
        common_paths = [
            "/Applications/MuMuPlayer.app"
        ]
        
        for path in common_paths:
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
            time.sleep(3)  # Increased wait time for interface to fully load
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to open MuMu模拟器Pro: {e}")
            return False
    
    def get_play_button_coordinates(self, emulator_index=1):
        """
        Get play button coordinates for specific emulator using known positions
        """
        play_buttons = {
            1: (576, 275),    # First emulator - "我的安卓"
        }
        
        if emulator_index in play_buttons:
            return play_buttons[emulator_index]
        else:
            return None
    
    def click_play_button(self, emulator_index=1):
        """
        Click the play button for the specified emulator using direct coordinates
        """
        if not AUTOMATION_AVAILABLE:
            print("❌ Cannot click - automation libraries not available")
            return False
        
        print(f"🎯 Clicking emulator #{emulator_index} play button...")
        
        # Get coordinates for the specified emulator
        coordinates = self.get_play_button_coordinates(emulator_index)
        
        if not coordinates:
            print(f"❌ Invalid emulator number: {emulator_index}")
            print("Available emulator: 1")
            return False
        
        target_x, target_y = coordinates
        
        try:
            print(f"🖱️  Clicking play button #{emulator_index} at ({target_x}, {target_y})")
            pyautogui.click(target_x, target_y)
            
            print("✅ Play button clicked successfully!")
            print("⏳ Waiting for emulator to start...")
            time.sleep(5)  # Wait for emulator to boot
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to click play button: {e}")
            return False
    
    def run_automation(self, emulator_index=1):
        """Main automation workflow"""
        print("🎮 Starting Game Automation Tool")
        print("=" * 50)
        
        # Step 1: Open MuMu模拟器Pro
        if not self.open_mumu():
            return
        
        # Step 2: Click play button to start emulator
        if self.click_play_button(emulator_index):
            print(f"🎉 Emulator #{emulator_index} started successfully!")
            print("📱 Android emulator is now running and ready for game automation")
        else:
            print("⚠️  Could not start emulator automatically")
            print("💡 You can manually click the play button and then add more automation features")

def main():
    parser = argparse.ArgumentParser(description="Gameplay Automation Tool for MuMu模拟器Pro")
    parser.add_argument("--open-only", action="store_true", 
                       help="Only open MuMu模拟器Pro without running automation")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")
    parser.add_argument("--emulator", "-e", type=int, default=1,
                       help="Which emulator to start (1=first, 2=second, 3=third)")
    parser.add_argument("--click-only", action="store_true",
                       help="Only click play button (assumes MuMu is already open)")
    
    args = parser.parse_args()
    
    # Check automation availability
    if not AUTOMATION_AVAILABLE and not args.open_only:
        print("⚠️  Automation libraries not found!")
        print("📦 Install with: pip install pyautogui")
        print("🔄 Running in open-only mode...")
        args.open_only = True
    
    automation = GameAutomation(verbose=args.verbose)
    
    if args.open_only:
        automation.open_mumu()
    elif args.click_only:
        automation.click_play_button(args.emulator)
    else:
        automation.run_automation(args.emulator)

if __name__ == "__main__":
    main() 