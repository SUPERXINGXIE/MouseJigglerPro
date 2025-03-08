

# MouseJigglerPro 背景描述 / Background Description of MouseJigglerPro

## 背景挑战 / Background Challenges

在现代企业办公环境中，员工常面临以下技术限制与场景痛点：  
In modern enterprise office environments, employees often face the following technical limitations and scenario pain points:

### 1. IT 管控限制 / IT Management Restrictions
- 公司统一强制开启屏幕保护/定时息屏策略（如 15 分钟无操作自动黑屏）。  
  The company enforces a unified screen saver/timed lock screen policy (e.g., automatic screen blackout after 15 minutes of inactivity).  
- 电源管理设置被锁定，禁止用户手动调整休眠时长。  
  Power management settings are locked, preventing users from manually adjusting sleep durations.  
- 安全策略监控异常进程，传统脚本类工具易被拦截。  
  Security policies monitor abnormal processes, making traditional script-based tools prone to interception.

### 2. 自动化测试场景 / Automated Testing Scenarios
- 长时间无人值守的 UI 测试（如 Web/APP 回归测试）。  
  Long-term unattended UI testing (e.g., regression testing for web or app interfaces).  
- Android 设备通过 USB 连接进行 ADB 调试时，因电脑息屏中断测试流程。  
  During ADB debugging of Android devices via USB, the test process is interrupted due to the computer screen locking.  
- 自动化脚本执行期间需持续模拟人工交互信号。  
  Continuous simulation of human interaction signals is required during the execution of automated scripts.

### 3. 办公协作风险 / Office Collaboration Risks
- 协同工具（钉钉/企业微信）检测到电脑不活跃时强制下线。  
  Collaboration tools (e.g., DingTalk/WeChat Work) force users offline when the computer is detected as inactive.  
- 视频会议软件（Zoom/Teams）因息屏导致画面黑屏。  
  Video conferencing software (e.g., Zoom/Teams) blacks out the screen due to inactivity.  
- 需保持“在线”状态应对考勤/任务监控行为。  
  Maintaining an “online” status is necessary to comply with attendance/task monitoring requirements.



## 解决方案特性 / Solution Features

MouseJigglerPro 通过以下技术组合精准应对上述场景：  
MouseJigglerPro addresses the above scenarios with the following technical combinations:

### 1. 双重防护机制 / Dual Protection Mechanism
- **OS 层级干预 / OS-Level Intervention**：调用 Windows API `SetThreadExecutionState`，直接向系统发送“保持唤醒”指令，绕过电源管理策略。  
  Calls the Windows API `SetThreadExecutionState` to directly send a “stay awake” instruction to the system, bypassing power management policies.  
- **行为模拟层 / Behavior Simulation Layer**：通过 `pyautogui` 实现：  
  Implemented via `pyautogui`:  
  - **轻度模式 / Gentle Mode**：每 5 秒 10px 随机方向移动（模拟正常操作频率）。  
    Moves the mouse 10px in a random direction every 5 seconds (simulating normal operation frequency).  
  - **疯狂模式 / Frenzy Mode**：每秒 20px 高频抖动（应对极端休眠策略）。  
    High-frequency jitter of 20px per second (to handle extreme sleep policies).

### 2. 智能化适配策略 / Intelligent Adaptation Strategy
- **动态频率调节 / Dynamic Frequency Adjustment**：根据目标应用敏感度自动切换工作模式。  
  Automatically switches operating modes based on the sensitivity of the target application.  
- **进程隐匿技术 / Process Concealment Technology**：采用守护线程 + 事件监听机制，退出时自动清理进程残留。  
  Uses daemon threads and event listeners, automatically cleaning up residual processes upon exit.  
- **硬件兼容优化 / Hardware Compatibility Optimization**：完美支持 USB 外接显示器/虚拟机环境。  
  Perfectly supports USB external monitors and virtual machine environments.

### 3. 场景化功能矩阵 / Scenario-Based Feature Matrix
以下是 MouseJigglerPro 在不同场景中的功能支持：  
The following outlines MouseJigglerPro’s feature support across different scenarios:

![mermaid-diagram-2025-03-09-015122](https://github.com/user-attachments/assets/651f5d85-1244-47d5-85ef-276bcfaaa369)

## 技术优势对比 / Technical Advantage Comparison

以下是对比 MouseJigglerPro 与传统解决方案的技术优势：  
The following compares the technical advantages of MouseJigglerPro against traditional solutions:

| 维度 / Dimension            | MouseJigglerPro                              | 传统解决方案 / Traditional Solutions               |
|----------------------------|----------------------------------------------|-----------------------------------------------|
| 系统兼容性 / System Compatibility | Win10+/macOS                                | 仅支持特定 Windows 版本 / Limited to specific Windows versions |
| 隐蔽性 / Concealment         | 系统托盘静默运行 / Silent system tray operation | 需保持脚本窗口前置 / Requires keeping script window in foreground |
| 抗检测能力 / Anti-Detection Capability | 模拟自然操作轨迹 / Simulates natural operation patterns | 固定频率易被识别为脚本 / Fixed frequency easily identified as script |
| 多任务支持 / Multitasking Support | 支持同时运行测试/办公 / Supports simultaneous testing and office tasks | 单一用途脚本 / Single-purpose scripts |
| 资源占用 / Resource Usage   | <1% CPU & 内存 / <1% CPU & memory            | 高频脚本导致性能损耗 / High-frequency scripts cause performance degradation |



## 总结 / Summary

该方案通过精准模拟人类行为特征，在满足企业合规要求的前提下，有效解决了现代化办公场景中的屏幕息屏痛点，实现了安全性与效率的双重提升。MouseJigglerPro 不仅提供用户友好的双语界面，还通过线程安全设计、干净退出机制和系统托盘集成，确保了产品的专业性、可靠性和隐蔽性，成为应对企业 IT 管控、自动化测试及办公协作场景的理想工具。  

This solution effectively addresses the screen lock pain points in modern office scenarios while meeting enterprise compliance requirements, achieving a dual enhancement in security and efficiency. MouseJigglerPro not only offers a user-friendly bilingual interface but also ensures professionalism, reliability, and concealment through thread-safe design, clean exit mechanisms, and system tray integration, making it an ideal tool for handling enterprise IT restrictions, automated testing, and office collaboration scenarios.




# MouseJigglerPro  - Anti-Screensaver Tool 
# 鼠标抖动器 Pro - 防止屏幕息屏

**[English]** A professional tool designed to prevent screensaver activation and keep your PC active by simulating human mouse movements, with robust thread management for a clean exit—no lingering processes guaranteed!  
**[中文]** 一款专业工具，通过模拟人类鼠标操作防止屏幕息屏并保持电脑活跃状态，具备强大的线程管理，确保退出时无后台进程残留！


**[English interface display]**

Tool address ： [MouseJigglerPro V1.0.0 Release](https://github.com/SUPERXINGXIE/MouseJigglerPro/releases/tag/MouseJigglerPro_V1.0.0)

![image](https://github.com/user-attachments/assets/50de690f-8ac8-4889-802f-6dce91dd6eea)



**[中文界面展示]** 

工具地址 ： [MouseJigglerPro V1.0.0 Release](https://github.com/SUPERXINGXIE/MouseJigglerPro/releases/tag/MouseJigglerPro_V1.0.0)

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
