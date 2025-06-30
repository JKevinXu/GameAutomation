#!/bin/bash

# Shimen Task Daily Automation Script (Direct Coordinates Version)
# This script uses direct coordinates instead of template matching to avoid permission issues

# Set the working directory to the project root
cd /Users/kx/game_automation_project

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "$(date): Activated virtual environment"
fi

# Set up environment variables if needed
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Log the start time
echo "$(date): Starting 师门任务 automation (direct coordinates)..." >> shimen_task.log

# Create a temporary config file using direct coordinates
cp config_no_templates.py config.py.backup
cp config_no_templates.py config.py

# Run the automation script with direct coordinates
./venv/bin/python3 action_automation.py 师门任务 >> shimen_task.log 2>&1

# Restore original config
if [ -f "config.py.backup" ]; then
    mv config.py.backup config.py
fi

# Check if the script ran successfully
if [ $? -eq 0 ]; then
    echo "$(date): 师门任务 automation completed successfully" >> shimen_task.log
else
    echo "$(date): 师门任务 automation failed with exit code $?" >> shimen_task.log
fi

# Log the end time
echo "$(date): Finished 师门任务 automation" >> shimen_task.log
echo "----------------------------------------" >> shimen_task.log 