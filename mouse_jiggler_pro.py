# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import time
import threading
import sys
import ctypes
import os
import logging
from infi.systray import SysTrayIcon  # pip install infi.systray
from PIL import Image  # pip install Pillow

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 语言配置
LANGUAGES = {
    "zh": {
        "title": "鼠标抖动器 Pro - 防息屏工具",
        "light": "轻度抖动",
        "light_desc": "每 5 秒移动 10 像素，模拟操作防息屏",
        "crazy": "疯狂抖动",
        "crazy_desc": "每 1 秒移动 20 像素，保持活跃状态",
        "stop": "停止",
        "stop_desc": "停止模拟操作",
        "exit": "退出",
        "exit_desc": "退出程序",
        "status_idle": "状态：未运行",
        "status_light": "状态：轻度抖动运行中",
        "status_crazy": "状态：疯狂抖动运行中",
        "runtime": "运行时间：{hours:02d}:{minutes:02d}:{seconds:02d}",
        "start_light_msg": "轻度抖动已启动，防止息屏！",
        "start_crazy_msg": "疯狂抖动已启动，保持活跃！",
        "stop_msg": "抖动已停止！",
        "minimize_msg": "程序已最小化到托盘，继续防息屏",
    },
    "en": {
        "title": "Mouse Jiggler Pro - Anti-Screensaver Tool",
        "light": "Light Jiggle",
        "light_desc": "Move 10px every 5s to prevent screensaver",
        "crazy": "Crazy Jiggle",
        "crazy_desc": "Move 20px every 1s to keep PC active",
        "stop": "Stop",
        "stop_desc": "Stop simulation",
        "exit": "Exit",
        "exit_desc": "Exit the application",
        "status_idle": "Status: Not Running",
        "status_light": "Status: Light Jiggle Running",
        "status_crazy": "Status: Crazy Jiggle Running",
        "runtime": "Runtime: {hours:02d}:{minutes:02d}:{seconds:02d}",
        "start_light_msg": "Light Jiggle started to prevent screensaver!",
        "start_crazy_msg": "Crazy Jiggle started to keep PC active!",
        "stop_msg": "Jiggle stopped!",
        "minimize_msg": "Minimized to tray, still preventing screensaver",
    }
}

def resource_path(relative_path):
    """获取资源文件的绝对路径，支持开发和打包环境"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def resize_icon_if_needed(icon_path, target_size=(32, 32)):
    """检查图标大小并调整为目标尺寸，保持程序图标清晰"""
    try:
        with Image.open(icon_path) as img:
            if img.size != target_size:
                logging.info(f"Resizing {icon_path} from {img.size} to {target_size}")
                img = img.resize(target_size, Image.Resampling.LANCZOS)
                temp_path = os.path.join(os.path.dirname(icon_path), "temp_window_icon.ico")
                img.save(temp_path, format="ICO")
                return temp_path
            return icon_path
    except Exception as e:
        logging.error(f"Failed to process icon {icon_path}: {str(e)}")
        return icon_path

class MouseJigglerPro:
    def __init__(self, root):
        self.root = root
        self.lang = "zh"  # 默认中文
        self.root.title(LANGUAGES[self.lang]["title"])
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f6f5")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 处理窗口图标并设置
        icon_path = resource_path("window_icon.ico")
        adjusted_icon_path = resize_icon_if_needed(icon_path)
        try:
            self.root.iconbitmap(adjusted_icon_path)
        except tk.TclError:
            logging.warning("Failed to load window_icon.ico. Ensure the file exists and is a valid ICO.")

        # 运行状态控制
        self.running = threading.Event()  # 使用 Event 替代布尔值
        self.jiggle_thread = None
        self.runtime_thread = None
        self.start_time = None
        self.systray = None

        # Windows API 初始化，用于防止系统休眠和息屏
        self.kernel32 = ctypes.windll.kernel32
        self.SetThreadExecutionState = self.kernel32.SetThreadExecutionState
        self.SetThreadExecutionState.argtypes = [ctypes.c_uint]
        self.SetThreadExecutionState.restype = ctypes.c_uint
        self.ES_SYSTEM_REQUIRED = 0x00000001
        self.ES_CONTINUOUS = 0x80000000

        # UI 初始化
        self.setup_language_selector()
        self.setup_ui()
        self.setup_systray()

    def setup_language_selector(self):
        self.lang_frame = ttk.Frame(self.root, padding="10")
        self.lang_frame.pack(fill="x")
        ttk.Label(self.lang_frame, text="Language / 语言:").pack(side="left")
        self.lang_combo = ttk.Combobox(self.lang_frame, values=["中文 (zh)", "English (en)"], state="readonly")
        self.lang_combo.pack(side="left", padx=5)
        self.lang_combo.set("中文 (zh)")
        self.lang_combo.bind("<<ComboboxSelected>>", self.change_language)

    def change_language(self, event):
        selected = self.lang_combo.get()
        self.lang = "zh" if "zh" in selected else "en"
        self.root.title(LANGUAGES[self.lang]["title"])
        self.update_ui_text()

    def setup_ui(self):
        # 主框架居中
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(expand=True)

        # 标题
        self.label = ttk.Label(self.main_frame, text=LANGUAGES[self.lang]["title"], font=("Arial", 16, "bold"), foreground="#2c3e50")
        self.label.pack(pady=(0, 20))

        # 按钮样式
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10, borderwidth=0)
        style.configure("Desc.TLabel", font=("Arial", 10), foreground="#7f8c8d")
        style.map("TButton", background=[("active", "#3498db"), ("disabled", "#bdc3c7")],
                  foreground=[("active", "#ffffff"), ("disabled", "#95a5a6")])

        # 操作按钮框架，偏左布局
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(anchor="w", pady=10)

        self.light_frame = ttk.Frame(self.button_frame)
        self.light_frame.pack(side="top", pady=5, anchor="w")
        self.light_button = ttk.Button(self.light_frame, text=LANGUAGES[self.lang]["light"], command=self.start_light, width=15)
        self.light_button.pack(side="left")
        self.light_desc = ttk.Label(self.light_frame, text=LANGUAGES[self.lang]["light_desc"], style="Desc.TLabel")
        self.light_desc.pack(side="left", padx=10)

        self.crazy_frame = ttk.Frame(self.button_frame)
        self.crazy_frame.pack(side="top", pady=5, anchor="w")
        self.crazy_button = ttk.Button(self.crazy_frame, text=LANGUAGES[self.lang]["crazy"], command=self.start_crazy, width=15)
        self.crazy_button.pack(side="left")
        self.crazy_desc = ttk.Label(self.crazy_frame, text=LANGUAGES[self.lang]["crazy_desc"], style="Desc.TLabel")
        self.crazy_desc.pack(side="left", padx=10)

        # 控制按钮框架，偏左布局
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(anchor="w", pady=20)

        self.stop_frame = ttk.Frame(self.control_frame)
        self.stop_frame.pack(side="top", pady=5, anchor="w")
        self.stop_button = ttk.Button(self.stop_frame, text=LANGUAGES[self.lang]["stop"], command=self.stop, width=15, state="disabled")
        self.stop_button.pack(side="left")
        self.stop_desc = ttk.Label(self.stop_frame, text=LANGUAGES[self.lang]["stop_desc"], style="Desc.TLabel")
        self.stop_desc.pack(side="left", padx=10)

        self.exit_frame = ttk.Frame(self.control_frame)
        self.exit_frame.pack(side="top", pady=5, anchor="w")
        self.exit_button = ttk.Button(self.exit_frame, text=LANGUAGES[self.lang]["exit"], command=self.exit_app, width=15)
        self.exit_button.pack(side="left")
        self.exit_desc = ttk.Label(self.exit_frame, text=LANGUAGES[self.lang]["exit_desc"], style="Desc.TLabel")
        self.exit_desc.pack(side="left", padx=10)

        # 状态显示
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(pady=10)
        self.status_indicator = tk.Canvas(self.status_frame, width=10, height=10, bg="#f5f6f5", highlightthickness=0)
        self.status_indicator.pack(side="left", padx=5)
        self.status_indicator.create_oval(2, 2, 8, 8, fill="#e74c3c")  # 默认红色（未运行）
        self.status_label = ttk.Label(self.status_frame, text=LANGUAGES[self.lang]["status_idle"], font=("Arial", 10), foreground="#7f8c8d")
        self.status_label.pack(side="left")

        self.time_label = ttk.Label(self.main_frame, text="运行时间：00:00:00", font=("Arial", 10), foreground="#7f8c8d")
        self.time_label.pack(pady=10)

    def update_ui_text(self):
        self.label.config(text=LANGUAGES[self.lang]["title"])
        self.light_button.config(text=LANGUAGES[self.lang]["light"])
        self.light_desc.config(text=LANGUAGES[self.lang]["light_desc"])
        self.crazy_button.config(text=LANGUAGES[self.lang]["crazy"])
        self.crazy_desc.config(text=LANGUAGES[self.lang]["crazy_desc"])
        self.stop_button.config(text=LANGUAGES[self.lang]["stop"])
        self.stop_desc.config(text=LANGUAGES[self.lang]["stop_desc"])
        self.exit_button.config(text=LANGUAGES[self.lang]["exit"])
        self.exit_desc.config(text=LANGUAGES[self.lang]["exit_desc"])
        self.status_label.config(text=LANGUAGES[self.lang]["status_idle"] if not self.running.is_set() else
                                LANGUAGES[self.lang]["status_light"] if self.jiggle_thread and self.jiggle_thread.args[0] == 5 else
                                LANGUAGES[self.lang]["status_crazy"])

    def setup_systray(self):
        menu_options = (("Show Window / 显示窗口", None, self.show_window),)
        self.systray = SysTrayIcon(resource_path("icon.ico"), LANGUAGES[self.lang]["title"], menu_options, on_quit=self.on_systray_quit)
        self.systray.start()

    def set_prevent_sleep(self):
        """设置系统状态，防止息屏和休眠"""
        flags = self.ES_SYSTEM_REQUIRED | self.ES_CONTINUOUS
        result = self.SetThreadExecutionState(flags)
        if result == 0:
            logging.error("Failed to set prevent sleep/screensaver")
        else:
            logging.info("Prevent sleep/screensaver set successfully")

    def reset_prevent_sleep(self):
        """重置系统状态，允许息屏和休眠"""
        result = self.SetThreadExecutionState(self.ES_CONTINUOUS)
        if result == 0:
            logging.error("Failed to reset prevent sleep/screensaver")
        else:
            logging.info("Prevent sleep/screensaver reset successfully")

    def update_runtime(self):
        while self.running.is_set():
            if self.start_time:
                elapsed = int(time.time() - self.start_time)
                hours, remainder = divmod(elapsed, 3600)
                minutes, seconds = divmod(remainder, 60)
                self.time_label.config(text=LANGUAGES[self.lang]["runtime"].format(hours=hours, minutes=minutes, seconds=seconds))
            time.sleep(1)

    def start_light(self):
        if not self.running.is_set():
            try:
                self.set_prevent_sleep()
                self.running.set()  # 标记运行状态
                self.start_time = time.time()
                self.light_button.config(state="disabled")
                self.crazy_button.config(state="disabled")
                self.stop_button.config(state="normal")
                self.status_label.config(text=LANGUAGES[self.lang]["status_light"], foreground="#2ecc71")
                self.status_indicator.create_oval(2, 2, 8, 8, fill="#2ecc71")
                self.jiggle_thread = threading.Thread(target=self.jiggle, args=(5, 10))
                self.jiggle_thread.daemon = True  # 设置为守护线程
                self.jiggle_thread.start()
                self.runtime_thread = threading.Thread(target=self.update_runtime)
                self.runtime_thread.daemon = True
                self.runtime_thread.start()
                messagebox.showinfo("Info", LANGUAGES[self.lang]["start_light_msg"])
            except Exception as e:
                logging.error(f"Light jiggle failed: {str(e)}")
                messagebox.showerror("Error", f"Failed: {str(e)}")

    def start_crazy(self):
        if not self.running.is_set():
            try:
                self.set_prevent_sleep()
                self.running.set()
                self.start_time = time.time()
                self.light_button.config(state="disabled")
                self.crazy_button.config(state="disabled")
                self.stop_button.config(state="normal")
                self.status_label.config(text=LANGUAGES[self.lang]["status_crazy"], foreground="#e67e22")
                self.status_indicator.create_oval(2, 2, 8, 8, fill="#e67e22")
                self.jiggle_thread = threading.Thread(target=self.jiggle, args=(1, 20))
                self.jiggle_thread.daemon = True
                self.jiggle_thread.start()
                self.runtime_thread = threading.Thread(target=self.update_runtime)
                self.runtime_thread.daemon = True
                self.runtime_thread.start()
                messagebox.showinfo("Info", LANGUAGES[self.lang]["start_crazy_msg"])
            except Exception as e:
                logging.error(f"Crazy jiggle failed: {str(e)}")
                messagebox.showerror("Error", f"Failed: {str(e)}")

    def jiggle(self, interval, distance):
        """模拟人类操作，移动鼠标并按键以防止息屏"""
        try:
            while self.running.is_set():
                x, y = pyautogui.position()
                pyautogui.moveTo(x + distance, y + distance, duration=0.1)
                pyautogui.moveTo(x, y, duration=0.1)
                pyautogui.press('shift', presses=1, interval=0.01)
                time.sleep(interval)
        except Exception as e:
            logging.error(f"Jiggle thread error: {str(e)}")

    def stop(self):
        if self.running.is_set():
            try:
                self.running.clear()  # 停止运行状态
                self.cleanup_threads()
                self.reset_prevent_sleep()
                self.start_time = None
                self.light_button.config(state="normal")
                self.crazy_button.config(state="normal")
                self.stop_button.config(state="disabled")
                self.status_label.config(text=LANGUAGES[self.lang]["status_idle"], foreground="#7f8c8d")
                self.status_indicator.create_oval(2, 2, 8, 8, fill="#e74c3c")
                self.time_label.config(text="运行时间：00:00:00")
                messagebox.showinfo("Info", LANGUAGES[self.lang]["stop_msg"])
            except Exception as e:
                logging.error(f"Stop failed: {str(e)}")
                messagebox.showerror("Error", f"Failed: {str(e)}")

    def cleanup_threads(self):
        """清理所有线程，确保退出时无残留"""
        if self.jiggle_thread and self.jiggle_thread.is_alive():
            self.jiggle_thread.join(timeout=1.0)
            if self.jiggle_thread.is_alive():
                logging.warning("Jiggle thread did not terminate gracefully")
        if self.runtime_thread and self.runtime_thread.is_alive():
            self.runtime_thread.join(timeout=1.0)
            if self.runtime_thread.is_alive():
                logging.warning("Runtime thread did not terminate gracefully")
        self.jiggle_thread = None
        self.runtime_thread = None

    def exit_app(self):
        """统一退出逻辑，确保所有资源清理"""
        try:
            self.running.clear()  # 停止所有线程
            self.cleanup_threads()
            self.reset_prevent_sleep()
            if self.systray:
                self.systray.shutdown()
            self.root.quit()  # 退出 Tkinter 主循环
            self.root.destroy()
            sys.exit(0)
        except Exception as e:
            logging.error(f"Exit failed: {str(e)}")
            messagebox.showerror("Error", f"Failed: {str(e)}")
            sys.exit(1)

    def on_closing(self):
        """窗口关闭时执行完整退出"""
        if self.running.is_set():
            messagebox.showinfo("Info", LANGUAGES[self.lang]["minimize_msg"])
            self.root.withdraw()  # 如果运行中，仅最小化
        else:
            self.exit_app()  # 未运行时直接退出

    def show_window(self, systray):
        self.root.deiconify()

    def on_systray_quit(self, systray):
        self.exit_app()

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseJigglerPro(root)
    root.mainloop()