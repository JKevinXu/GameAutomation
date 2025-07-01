# Game Automation Project

Automated gameplay tools for Chinese mobile games using Python, OpenCV, and AI-powered text analysis with macOS LaunchAgent scheduling.

## 🎯 Overview

This project automates the **师门任务 (Shimen Task)** in mobile games running on MuMu emulator. The automation includes:
- **Daily scheduling** using macOS LaunchAgent
- **Template-based UI detection** for reliable clicking
- **Screen capture with permission handling**
- **Multi-step automation workflows**

## 🚀 Features

### Core Automation
- **LaunchAgent scheduling**: Native macOS daily task automation
- **Template matching**: PNG-based UI element detection using OpenCV
- **Emulator integration**: Seamless MuMu emulator control
- **Permission handling**: Proper screen recording and accessibility permissions

### Avatar Detection & Keyword Analysis
- **Avatar template matching**: Detect specific player avatars in chat
- **AI-powered text extraction**: GPT-4o vision model for Chinese text recognition
- **Intelligent keyword detection**: Context-aware keyword analysis
- **Automated avatar clicking**: Click avatars based on message content

### Smart Coordinate Handling
- **Retina display support**: Automatic scaling between logical and physical coordinates
- **Multiple click strategies**: Center, edge, and custom positioning options
- **Visual debugging**: Debug images with bounding boxes and confidence scores

## 📋 How the Process Works

### 1. **LaunchAgent Scheduling (macOS Native)**

The automation uses macOS LaunchAgent instead of cron for better permission handling:

**LaunchAgent File:** `~/Library/LaunchAgents/com.user.shimen.task.plist`
```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>17</integer>
    <key>Minute</key>
    <integer>32</integer>
</dict>
```

**Why LaunchAgent > Cron:**
- ✅ **User context**: Runs with proper GUI permissions
- ✅ **Screen recording**: Inherits user's screen recording permissions
- ✅ **Native macOS**: Better integration with system security
- ✅ **Reliable**: No permission denied errors

### 2. **Automation Workflow (师门任务)**

```mermaid
graph TD
    A[LaunchAgent Triggers] --> B[Open MuMu Emulator]
    B --> C[Wait for Interface]
    C --> D[Template Match: Play Button]
    D --> E[Click Play Button]
    E --> F[Wait for Boot]
    F --> G[Template Match: Start Game]
    G --> H[Click Start Game]
    H --> I[Wait for Game Load]
    I --> J[Template Match: Login]
    J --> K[Click Login]
    K --> L[Template Match: 师门任务]
    L --> M[Click 师门任务]
    M --> N[Template Match: Go Finish]
    N --> O[Click Go Finish]
    O --> P[Complete ✅]
```

### 3. **Template Matching Process**

1. **Screen Capture**: Take screenshot with proper permissions
2. **Scaling Detection**: Handle Retina display (2x scaling)
3. **Template Matching**: Use OpenCV to find UI elements
4. **Confidence Check**: Ensure match confidence > threshold
5. **Coordinate Calculation**: Convert to logical coordinates for clicking

### 4. **Permission Architecture**

**Required macOS Permissions:**
- 🔐 **Screen Recording**: For taking screenshots
- 🔐 **Accessibility**: For controlling other applications
- 🔐 **Full Disk Access**: For comprehensive system access

**Permission Context:**
```
User Login Session
├── LaunchAgent (inherits user permissions)
├── Terminal.app (granted screen recording)
├── Python script (runs in user context)
└── PyAutoGUI (works with proper permissions)
```

## 🔧 Installation & Setup

### 1. **Clone and Install Dependencies**
```bash
git clone <repository-url>
cd game_automation_project
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. **Grant macOS Permissions**

**System Settings → Privacy & Security:**

1. **Screen Recording**:
   - Add `Terminal.app`
   - Check the checkbox ✅

2. **Accessibility**:
   - Add `Terminal.app`
   - Check the checkbox ✅

3. **Full Disk Access**:
   - Add `Terminal.app`
   - Check the checkbox ✅

**⚠️ Important: Restart Terminal after granting permissions!**

### 3. **Set Up LaunchAgent**

The LaunchAgent is automatically created at:
`~/Library/LaunchAgents/com.user.shimen.task.plist`

**Load the LaunchAgent:**
```bash
launchctl load ~/Library/LaunchAgents/com.user.shimen.task.plist
```

**Verify it's running:**
```bash
launchctl list | grep shimen
```

### 4. **Configure Schedule**

Edit the plist file to change timing:
```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>9</integer>    <!-- 9 AM -->
    <key>Minute</key>
    <integer>30</integer>   <!-- 30 minutes -->
</dict>
```

**Reload after changes:**
```bash
launchctl unload ~/Library/LaunchAgents/com.user.shimen.task.plist
launchctl load ~/Library/LaunchAgents/com.user.shimen.task.plist
```

## 📊 Monitoring & Logs

### **Log Files**
- `shimen_task.log`: Main automation execution log
- `launchd_output.log`: LaunchAgent stdout
- `launchd_error.log`: LaunchAgent stderr

### **Real-time Monitoring**
```bash
# Watch automation logs
tail -f shimen_task.log

# Watch LaunchAgent logs
tail -f launchd_output.log
```

### **Debug Template Matching**
Debug images saved to: `debug/avatar_template/`
- Screenshots with detection overlays
- Confidence scores and bounding boxes
- Template matching results

## 🔧 Configuration

### **Action Plans** (config.py)
```python
ACTION_PLANS = {
    '师门任务': [
        {'action': 'open_app', 'app': 'mumu'},
        {'action': 'click', 'coordinate': 'play_button'},
        {'action': 'wait', 'duration': 10},
        # ... more steps
    ]
}
```

### **Template Coordinates**
```python
COORDINATES = {
    'play_button': 'game_elements/play_button.png',
    'start_game': 'game_elements/start_game.png',
    'login_button': 'game_elements/login_button.png',
    # ... more templates
}
```

## 🚨 Troubleshooting

### **Common Issues**

**1. Permission Denied Errors**
```
❌ Error: [Errno 2] No such file or directory: 'screencapture'
```
**Solution:** Grant Screen Recording permission to Terminal.app and restart Terminal

**2. Template Not Found**
```
❌ Icon not found. Best confidence: 0.434 (threshold: 0.800)
```
**Solutions:**
- Lower confidence threshold in config
- Update template image
- Check if UI changed

**3. LaunchAgent Not Running**
```bash
# Check if loaded
launchctl list | grep shimen

# Reload if needed
launchctl unload ~/Library/LaunchAgents/com.user.shimen.task.plist
launchctl load ~/Library/LaunchAgents/com.user.shimen.task.plist
```

### **Permission Verification**
```bash
# Test screenshot capability
screencapture test.png && echo "✅ Permissions working" || echo "❌ Permission denied"

# Test automation manually
./run_shimen_task.sh
```

### **Debug Mode**
```bash
# Run with verbose output
python action_automation.py 师门任务 --verbose

# Check template matching
python avatar_message_block_detection.py --all-templates
```

## 📅 Schedule Management

### **Change Daily Schedule**

#### **Method 1: Standard Update**
```bash
# Edit the plist file to change time
nano ~/Library/LaunchAgents/com.user.shimen.automation.plist

# Change these lines:
# <key>Hour</key>
# <integer>12</integer>    <!-- Change hour -->
# <key>Minute</key>
# <integer>30</integer>    <!-- Change minute -->

# Reload LaunchAgent
launchctl unload ~/Library/LaunchAgents/com.user.shimen.automation.plist
launchctl load ~/Library/LaunchAgents/com.user.shimen.automation.plist
```

#### **Method 2: Quick Command Update**
```bash
# Update to run at 9:30 AM using search/replace
sed -i '' 's/<integer>12<\/integer>/<integer>9<\/integer>/g' ~/Library/LaunchAgents/com.user.shimen.automation.plist
sed -i '' 's/<integer>30<\/integer>/<integer>30<\/integer>/g' ~/Library/LaunchAgents/com.user.shimen.automation.plist

# Reload
launchctl unload ~/Library/LaunchAgents/com.user.shimen.automation.plist
launchctl load ~/Library/LaunchAgents/com.user.shimen.automation.plist
```

### **Verify Schedule Changes**
```bash
# Check if LaunchAgent is loaded
launchctl list | grep shimen

# Verify the actual schedule (should show new time)
launchctl print gui/$(id -u)/com.user.shimen.automation | grep -A 5 "descriptor"

# Should output:
# descriptor = {
#     "Minute" => 30
#     "Hour" => 9
# }
```

### **🚨 Schedule Update Troubleshooting**

#### **Issue: Changes Not Taking Effect**

**Problem**: LaunchAgent shows old schedule even after reload
```bash
# Symptom: This shows wrong time
launchctl print gui/$(id -u)/com.user.shimen.automation | grep -A 5 "descriptor"
```

**Solution 1: Force Complete Reload**
```bash
# Complete unload
launchctl bootout gui/$(id -u)/com.user.shimen.automation
launchctl remove com.user.shimen.automation

# Wait and reload
sleep 3
launchctl load ~/Library/LaunchAgents/com.user.shimen.automation.plist

# Verify
launchctl print gui/$(id -u)/com.user.shimen.automation | grep -A 5 "descriptor"
```

**Solution 2: Create New LaunchAgent (Nuclear Option)**
```bash
# If caching persists, create new LaunchAgent with different name
rm ~/Library/LaunchAgents/com.user.shimen.automation.plist

# Create new one with timestamp in name
cat > ~/Library/LaunchAgents/com.user.shimen.$(date +%H%M).plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.shimen.$(date +%H%M)</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/Users/kx/game_automation_project/run_shimen_task.sh</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>/Users/kx/game_automation_project</string>
    
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>14</integer>
        <key>Minute</key>
        <integer>30</integer>
    </dict>
    
    <key>StandardOutPath</key>
    <string>/Users/kx/game_automation_project/launchd_output.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/kx/game_automation_project/launchd_error.log</string>
    
    <key>RunAtLoad</key>
    <false/>
    
    <key>KeepAlive</key>
    <false/>
    
</dict>
</plist>
EOF

# Load new LaunchAgent
launchctl load ~/Library/LaunchAgents/com.user.shimen.$(date +%H%M).plist
```

### **Common Schedule Examples**

```xml
<!-- Daily at 9:00 AM -->
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>9</integer>
    <key>Minute</key>
    <integer>0</integer>
</dict>

<!-- Daily at 2:30 PM -->
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>14</integer>
    <key>Minute</key>
    <integer>30</integer>
</dict>

<!-- Daily at 11:45 PM -->
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>23</integer>
    <key>Minute</key>
    <integer>45</integer>
</dict>
```

### **Testing Schedule Changes**

```bash
# Set to run in 2 minutes for testing
CURRENT_MINUTE=$(date +%M)
TEST_MINUTE=$((CURRENT_MINUTE + 2))

# Update to test time
sed -i '' "s/<integer>[0-9]*<\/integer>/<integer>$TEST_MINUTE<\/integer>/g" ~/Library/LaunchAgents/com.user.shimen.automation.plist

# Reload and verify
launchctl unload ~/Library/LaunchAgents/com.user.shimen.automation.plist
launchctl load ~/Library/LaunchAgents/com.user.shimen.automation.plist

# Watch logs
tail -f shimen_task.log
```

### **Disable Automation**
```bash
# Unload LaunchAgent
launchctl unload ~/Library/LaunchAgents/com.user.shimen.automation.plist

# Or remove completely
launchctl bootout gui/$(id -u)/com.user.shimen.automation
```

### **Enable Automation**
```bash
# Load LaunchAgent
launchctl load ~/Library/LaunchAgents/com.user.shimen.automation.plist

# Verify it's running
launchctl list | grep shimen
```

### **Schedule Verification Checklist**

✅ **Step 1**: Check plist file content
```bash
cat ~/Library/LaunchAgents/com.user.shimen.automation.plist | grep -A 6 "StartCalendarInterval"
```

✅ **Step 2**: Verify LaunchAgent is loaded
```bash
launchctl list | grep shimen
```

✅ **Step 3**: Check actual loaded schedule
```bash
launchctl print gui/$(id -u)/com.user.shimen.automation | grep -A 5 "descriptor"
```

✅ **Step 4**: Confirm next run time matches expectation
```bash
date && echo "Next run scheduled for: [YOUR_TIME]"
```

**🔧 Pro Tips:**
- Always verify the schedule after changes using `launchctl print`
- Use 24-hour format (14 = 2 PM, 23 = 11 PM)
- Test with a time 2-3 minutes in the future first
- If caching issues persist, create a new LaunchAgent with a different label name
- Keep the old plist file as backup until new schedule is confirmed working

## 🔄 Alternative Approaches

### **Direct Coordinates (Fallback)**
If template matching fails, use `config_no_templates.py`:
- Uses hardcoded coordinates instead of templates
- Bypasses screen recording requirements
- Less reliable but permission-free

### **Manual Execution**
```bash
# Run automation manually
./run_shimen_task.sh

# Run specific action plan
python action_automation.py 师门任务
```

## 📁 Project Structure

```
game_automation_project/
├── action_automation.py              # Main automation engine
├── avatar_message_block_detection.py # Avatar template matching
├── config.py                         # Action plans and coordinates
├── run_shimen_task.sh               # LaunchAgent execution script
├── config_no_templates.py           # Direct coordinate fallback
├── game_elements/                   # UI template images
│   ├── avatar/                      # Avatar templates
│   └── *.png                        # Button templates
├── debug/                           # Debug output
└── ~/Library/LaunchAgents/          # LaunchAgent plist (system location)
    └── com.user.shimen.task.plist
```

## 🎯 Success Criteria

**Automation is working properly when you see:**
```
✅ Step 1/10: Open MuMu emulator
✅ Step 2/10: Click emulator play button  
✅ Step 3/10: Wait for emulator to boot
✅ Step 4/10: Click game start button
... (continues through all 10 steps)
✅ 师门任务 automation completed successfully
```

## 📞 Support

**Log Analysis:**
1. Check `shimen_task.log` for automation steps
2. Check `launchd_error.log` for LaunchAgent issues
3. Check `debug/` folder for template matching images

**Common Success Indicators:**
- LaunchAgent loads without errors
- Screenshots work in Terminal
- Template matching finds UI elements
- All 10 automation steps complete

**Key Files:**
- **LaunchAgent**: `~/Library/LaunchAgents/com.user.shimen.task.plist`
- **Main Script**: `run_shimen_task.sh`
- **Logs**: `shimen_task.log`, `launchd_*.log`
- **Config**: `config.py`

This automation system provides reliable, scheduled execution of mobile game tasks using native macOS scheduling and proper permission handling. 