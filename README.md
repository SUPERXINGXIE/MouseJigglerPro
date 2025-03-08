

# MouseJigglerPro  - Anti-Screensaver Tool 
# 鼠标抖动器 Pro -防止屏幕息屏

**[English]** A professional tool designed to prevent screensaver activation and keep your PC active by simulating human mouse movements, with robust thread management for a clean exit—no lingering processes guaranteed!  
**[中文]** 一款专业工具，通过模拟人类鼠标操作防止屏幕息屏并保持电脑活跃状态，具备强大的线程管理，确保退出时无后台进程残留！


**[English interface display]**


![image](https://github.com/user-attachments/assets/50de690f-8ac8-4889-802f-6dce91dd6eea)



**[中文界面展示]** 


![image](https://github.com/user-attachments/assets/a19fd1dc-0bb1-4b70-832d-40a5b0b47a0e)


## Features / 功能

- **Prevent Screensaver / 防止息屏**: Simulates human mouse and keyboard activity / 模拟人类鼠标和键盘操作。  
- **Light Jiggle / 轻度抖动**: Moves 10px every 5s to avoid screensaver / 每 5 秒移动 10 像素防止息屏。  
- **Crazy Jiggle / 疯狂抖动**: Moves 20px every 1s to maintain activity / 每 1 秒移动 20 像素保持活跃。  
- **System Tray / 系统托盘**: Runs silently in the background / 在后台静默运行。  
- **Clean Exit / 干净退出**: Ensures all threads terminate on exit / 确保退出时所有线程终止。  
- **Bilingual UI / 双语界面**: Supports English and Chinese / 支持英文和中文。  
- **Modern Design / 现代设计**: Clean, centered UI with status indicators / 简洁居中界面，带状态指示灯。

---

## Core Logic / 核心逻辑

### How It Prevents Screensaver & Keeps PC Active / 如何防止息屏并保持电脑活跃

`MouseJigglerPro` combines multiple techniques to ensure your computer remains active and the screen stays on:

1. **Mouse Movement Simulation / 鼠标移动模拟**  
   - Uses `pyautogui` to periodically move the mouse (10px every 5s for Light Jiggle, 20px every 1s for Crazy Jiggle) and return it to the original position, mimicking natural user interaction.  
   - **中文**: 使用 `pyautogui` 定期移动鼠标（轻度每 5 秒 10 像素，疯狂每 1 秒 20 像素）并返回原位，模拟自然用户交互。

2. **Keyboard Activity Simulation / 键盘活动模拟**  
   - Simulates a subtle Shift key press after each mouse movement, reinforcing the "user is active" signal to the OS.  
   - **中文**: 在每次鼠标移动后模拟轻微的 Shift 键按压，进一步向操作系统发送“用户活跃”信号。

3. **Windows API Integration / Windows API 集成**  
   - Calls `SetThreadExecutionState` with `ES_SYSTEM_REQUIRED | ES_CONTINUOUS` flags to explicitly prevent system sleep and screensaver activation, providing a hardware-level guarantee.  
   - **中文**: 调用 `SetThreadExecutionState` 并设置 `ES_SYSTEM_REQUIRED | ES_CONTINUOUS` 标志，明确阻止系统休眠和屏幕保护，直接在硬件层面提供保障。

### Advantages Over Traditional Solutions / 对比传统方案的优势

Compared to traditional mouse jigglers or scripts, `MouseJigglerPro` stands out with its hybrid approach and robust design:

#### Traditional Methods / 传统方法

- **Simple Scripts**: Move the mouse randomly but lack system-level sleep prevention, often failing against modern OS power policies.  
- **Hardware Jiggers**: Physical devices that move the mouse, costly and lack flexibility.  
- **中文**: 简单脚本仅随机移动鼠标，缺乏系统级休眠阻止，常被现代操作系统电源策略拦截；硬件抖动器是物理设备，成本高且不灵活。

#### MouseJigglerPro’s Edge / 本方案优势

1. **Dual-Layer Protection / 双重保护**  
   - Combines software simulation (mouse/keyboard) with Windows API calls for comprehensive activity signaling.  
   - **中文**: 结合软件模拟（鼠标/键盘）和 Windows API 调用，提供全面的活跃信号。  

2. **Thread Safety / 线程安全**  
   - Uses `threading.Event` and daemon threads to ensure all processes terminate cleanly, avoiding zombie processes common in basic scripts.  
   - **中文**: 使用 `threading.Event` 和守护线程，确保所有进程干净退出，避免简单脚本常见的僵尸进程。  

3. **User-Friendly / 用户友好**  
   - Modern UI with bilingual support and system tray integration, unlike command-line-only tools.  
   - **中文**: 现代界面支持双语和系统托盘集成，优于仅限命令行的工具。  

4. **Customizability / 可定制性**  
   - Offers Light and Crazy modes for different use cases, surpassing one-size-fits-all solutions.  
   - **中文**: 提供轻度和疯狂模式，适应不同场景，超越单一模式的方案。

---

## Installation / 安装

### Prerequisites / 前提条件

- **Windows OS** / Windows 操作系统  
- **Python 3.7+**  

### Setup Environment / 环境配置

1. **Clone the Repository** / 克隆仓库  
   ```bash
   git clone [https://github.com/yourusername/MouseJigglerPro.git](https://github.com/SUPERXINGXIE/MouseJigglerPro.git)
   cd MouseJigglerPro
   ```
   > **Note**: If you encounter issues cloning the repository, please ensure the link is correct and your network connection is stable. You may also try accessing the repository directly on GitHub.

2. **Install Dependencies** / 安装依赖  
   ```bash
   pip install -r requirements.txt
   ```

### Dependencies / 依赖项

- `pyautogui`  
- `infi.systray`  
- `Pillow`

---

## Usage / 使用方法

### Running the Script / 运行脚本

```bash
python mouse_jiggler_pro.py
```

### Building the Executable / 打包可执行文件

1. **Install PyInstaller** / 安装 PyInstaller  
   ```bash
   pip install pyinstaller
   ```

2. **Build the EXE** / 打包 EXE  
   ```bash
   python -m PyInstaller mouse_jiggler_pro.spec
   ```

3. **Find the Executable** / 查找可执行文件  
   - The executable will be located in `dist/MouseJigglerPro.exe`.

### How to Use / 操作指南

1. **Launch the Program** / 启动程序  
   - Open `MouseJigglerPro.exe` or run the script.  
2. **Select Language** / 选择语言  
   - Choose English or Chinese.  
3. **Prevent Screensaver** / 防止息屏  
   - Click "Light Jiggle" or "Crazy Jiggle".  
4. **Stop Simulation** / 停止模拟  
   - Click "Stop".  
5. **Exit Cleanly** / 干净退出  
   - Click "Exit" or close the window (no lingering processes).  
6. **Status Indicator** / 状态指示  
   - Green (Light) / Orange (Crazy) / Red (Stopped)  
   - **中文**: 绿色（轻度）/橙色（疯狂）/红色（停止）

---

## Files / 文件清单

- `mouse_jiggler_pro.py`: Main script with core logic / 主脚本，包含核心逻辑。  
- `mouse_jiggler_pro.spec`: PyInstaller config for packaging / PyInstaller 配置文件，用于打包。  
- `icon.ico`: System tray and EXE icon / 系统托盘和 EXE 图标。  
- `window_icon.ico`: GUI window icon / GUI 窗口图标。  
- `requirements.txt`: List of dependencies / 依赖列表。  

**Note / 注意**: Provide `icon.ico` and `window_icon.ico` (32x32 recommended). If size differs, it auto-resizes / 提供 `icon.ico` 和 `window_icon.ico`（建议 32x32），若尺寸不符会自动调整。

---

## Contributing / 贡献

Feel free to fork the repository, submit issues, or send pull requests on GitHub! / 欢迎 Fork、在 GitHub 上提交问题或发送 Pull Request！

## License / 许可证

MIT License - Free to use and modify / MIT 许可证 - 自由使用和修改

---

**[English]** Star this project on GitHub for a reliable, modern way to keep your PC active!  
**[中文]** 在 GitHub 上给这个项目点星，体验可靠、现代的电脑活跃保持方案！

---
