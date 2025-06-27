#!/bin/bash

# Shimen Task Daily Automation Script
# This script runs the 师门任务 (Shimen Task) automation

# Set the working directory to the project root
cd /Users/kx/game_automation_project

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "$(date): Activated virtual environment"
fi

# Set up environment variables if needed
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Add any required environment variables (e.g., OpenAI API key if using text extraction)
# export OPENAI_API_KEY="your-api-key-here"

# Log the start time
echo "$(date): Starting 师门任务 automation..." >> shimen_task.log

# Run the automation script with the virtual environment's Python
./venv/bin/python3 action_automation.py 师门任务 >> shimen_task.log 2>&1

# Check if the script ran successfully
if [ $? -eq 0 ]; then
    echo "$(date): 师门任务 automation completed successfully" >> shimen_task.log
else
    echo "$(date): 师门任务 automation failed with exit code $?" >> shimen_task.log
fi

# Log the end time
echo "$(date): Finished 师门任务 automation" >> shimen_task.log
echo "----------------------------------------" >> shimen_task.log 