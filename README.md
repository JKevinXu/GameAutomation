# Game Automation Tool

A command-line tool for automating gameplay in MuMu模拟器Pro on macOS.

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure MuMu模拟器Pro is installed in your Applications folder

## Usage

### Basic Commands

- **Open MuMu模拟器Pro only:**
  ```bash
  python game_automation.py --open-only
  ```

- **Run full automation (opens MuMu + automation steps):**
  ```bash
  python game_automation.py
  ```

- **Verbose output:**
  ```bash
  python game_automation.py --verbose
  ```

## Next Steps

This is a basic foundation. You'll need to specify:
- Which game you want to automate
- What specific actions to perform
- Any image recognition or text detection needs

The tool currently only opens MuMu模拟器Pro. Additional automation features will be added based on your requirements. 