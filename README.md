# Game Automation Tool

A command-line tool for automating gameplay in MuMu模拟器Pro on macOS.

## Demo Video

🎥 **See the Game Automation Tool in Action**

<iframe src="//player.bilibili.com/player.html?bvid=BV1YTNszpEs3&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" width="600" height="400"> </iframe>

*直接在页面观看演示视频 - Watch the demo video directly on the page*

<!-- Backup link if embed doesn't work -->
🔗 **[Open in Bilibili](https://www.bilibili.com/video/BV1YTNszpEs3)** *(if video doesn't load above)*

<!-- Alternative: If you have a GIF demo -->
<!--
![Demo GIF](path/to/your/demo.gif)
-->

<!-- Alternative: If you have a local video file -->
<!--
https://user-images.githubusercontent.com/USERNAME/VIDEO_ID-hash.mp4
-->

**What the demo shows:**
- Opening MuMu模拟器Pro automatically
- Executing action plans with clicks and waits
- Command-line interface and verbose output
- Available automation features

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