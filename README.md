# Game Automation Project

Automated gameplay tools for Chinese mobile games using Python, OpenCV, and AI-powered text analysis.

## Features

### Core Automation
- **Action-based automation**: Configurable action plans with clicks, waits, and app launching
- **Template-based clicking**: PNG template matching for reliable UI element detection
- **Emulator integration**: Seamless MuMu emulator control and interaction

### Avatar Detection & Keyword Analysis
- **Avatar template matching**: Detect specific player avatars in chat using OpenCV
- **AI-powered text extraction**: GPT-4o vision model for accurate Chinese text recognition
- **Intelligent keyword detection**: Context-aware keyword analysis with confidence scoring
- **Automated avatar clicking**: Click avatars based on message content

### Smart Coordinate Handling
- **Retina display support**: Automatic scaling between logical and physical coordinates
- **Multiple click strategies**: Center, edge, and custom positioning options
- **Visual debugging**: Debug images with bounding boxes and confidence scores

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd game_automation_project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API key** (for text extraction)
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. **Add avatar templates**
   - Place avatar images in `game_elements/avatar/`
   - Supported formats: PNG, JPG, JPEG

## Usage

### Basic Avatar Keyword Detection

Find avatar coordinates for specific keywords:
```bash
# Find avatar for "320" recruitment messages
python action_automation.py --find-keyword 320

# Find avatar for game activities
python action_automation.py --find-keyword 章鱼王
```

### Action Plans with Keyword Detection

Run predefined action plans:
```bash
# Search for multiple keywords and click matching avatar
python action_automation.py auto_keyword_click

# Specifically find 320 recruitment messages
python action_automation.py find_320_player

# Original action plans still work
python action_automation.py 师门任务
```

### Programmatic Usage

```python
from action_automation import ActionAutomation

automation = ActionAutomation()

# Find coordinates without clicking
result = automation.find_avatar_coordinates_for_keyword("320")
if result:
    print(f"Click at: ({result['x']}, {result['y']})")
    print(f"Confidence: {result['keyword_info']['confidence']}%")

# Use in action plans
action = {
    'action': 'avatar_keyword_click',
    'keywords': ['320', '章鱼王'],
    'confidence': 0.8,
    'description': 'Find and click avatar for keywords'
}
automation.execute_action(action)
```

### Configuration

Add custom action plans in `config.py`:
```python
ACTION_PLANS = {
    'my_custom_plan': [
        {
            'action': 'avatar_keyword_click',
            'keywords': ['师门', '任务'],
            'confidence': 0.8,
            'description': 'Click avatar for task-related messages'
        },
    ],
}
```

## Action Types

### Standard Actions
- **click**: Click at named coordinates or PNG templates
- **wait**: Pause execution for specified duration
- **open_app**: Launch applications (MuMu emulator, etc.)

### Avatar Keyword Actions
- **avatar_keyword_click**: Find and click avatars based on message keywords

#### Avatar Keyword Click Parameters
- `keywords`: String or list of keywords to search for
- `avatar_templates`: List of template paths (optional, uses all if not specified)
- `confidence`: Avatar detection confidence (0.0-1.0, default 0.8)
- `return_coordinates`: Return coordinates instead of clicking (optional)

## File Structure

```
game_automation_project/
├── action_automation.py          # Main automation system
├── avatar_message_block_detection.py  # Avatar template matching
├── message_text_extractor.py     # AI-powered text extraction
├── config.py                     # Action plans and coordinates
├── demo_avatar_keyword_click.py  # Usage examples
├── game_elements/
│   ├── avatar/                   # Avatar template images
│   └── *.png                     # UI element templates
└── debug/                        # Debug output and visualizations
```

## How It Works

### Avatar Detection Pipeline
1. **Screenshot Capture**: Captures chat region with retina scaling
2. **Template Matching**: Uses OpenCV to find avatars with high confidence
3. **Text Area Analysis**: Analyzes message blocks to the right of avatars
4. **Keyword Detection**: Uses GPT-4o vision to check for relevant keywords
5. **Coordinate Calculation**: Returns precise click coordinates

### Intelligent Keyword Analysis
The system uses AI to understand context, not just exact matches:
- **Direct keywords**: "320", "章鱼王", "师门"
- **Related concepts**: "挑战章鱼王" → detected for "任务" keyword
- **Game terminology**: Understands abbreviations and slang
- **Confidence scoring**: 70%+ required for action execution

### Coordinate System
- **Logical coordinates**: Standard screen coordinates (e.g., 640×1136)
- **Physical coordinates**: Retina display coordinates (2× scaling)
- **Automatic conversion**: Seamless handling between systems

## Debugging

### Visual Debug Output
- Screenshot with detection overlays saved to `debug/avatar_template/`
- Bounding boxes for avatars (red), text areas (green), message blocks (blue)
- Confidence scores and click points marked

### Verbose Mode
```bash
python action_automation.py --verbose auto_keyword_click
```

### Demo Script
```bash
python demo_avatar_keyword_click.py
```

## Examples

### Find 320 Level Players
```python
automation = ActionAutomation()
result = automation.find_avatar_coordinates_for_keyword("320")
# Finds: "320来人", "65-69级进组", recruitment messages
```

### Multi-Keyword Search
```python
keywords = ["章鱼王", "师门", "任务"]
result = automation.find_avatar_coordinates_for_keyword(keywords)
# Finds any avatar discussing these activities
```

### Game Activity Detection
```python
action = {
    'action': 'avatar_keyword_click',
    'keywords': ['章鱼王', '副本', '组队'],
    'description': 'Join group activities'
}
```

## Requirements

- Python 3.7+
- OpenCV (cv2)
- PyAutoGUI
- OpenAI API access
- macOS (for MuMu emulator integration)

## API Configuration

Set your OpenAI API key:
```bash
# In terminal
export OPENAI_API_KEY="sk-your-key-here"

# Or in Python
import os
os.environ['OPENAI_API_KEY'] = 'sk-your-key-here'
```

## Tips

1. **Avatar Templates**: Use clear, cropped avatar images for best detection
2. **Keyword Selection**: Choose distinctive keywords that appear in target messages
3. **Confidence Tuning**: Lower confidence (0.6-0.7) for broader matching
4. **Debug Mode**: Use `--verbose` flag to see detailed detection process
5. **Multiple Keywords**: Use lists for flexible matching: `['320', '组队', '副本']` 