import tkinter as tk
from tkinter import messagebox
import pygetwindow as gw
import pyautogui
import time

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("窗口控制器")
        
        self.drag_label = tk.Label(root, text="拖拽到目标窗口")
        self.drag_label.pack(pady=10)

        self.start_button = tk.Button(root, text="开始点击", command=self.start_clicking)
        self.start_button.pack(side=tk.LEFT, padx=20)

        self.exit_button = tk.Button(root, text="退出", command=root.quit)
        self.exit_button.pack(side=tk.RIGHT, padx=20)
        
        self.target_windows = []
        
        self.root.bind("<ButtonRelease-1>", self.get_window)
        
    def get_window(self, event):
        try:
            window = gw.getActiveWindow()
            if window and window not in self.target_windows:
                self.target_windows.append(window)
                messagebox.showinfo("窗口添加", f"窗口 {window.title} 已添加")
        except Exception as e:
            messagebox.showerror("错误", str(e))
        
    def start_clicking(self):
        if len(self.target_windows) != 4:
            messagebox.showerror("错误", "请添加四个窗口")
            return
        
        screen_width, screen_height = pyautogui.size()
        window_width = screen_width // 2
        window_height = screen_height // 2
        
        positions = [
            (0, 0),
            (window_width, 0),
            (0, window_height),
            (window_width, window_height)
        ]
        
        for i, window in enumerate(self.target_windows):
            window.moveTo(*positions[i])
            window.resizeTo(window_width, window_height)
            window.activate()
            window.minimize()
            window.restore()
        
        self.root.after(100, self.click_loop)
    
    def click_loop(self):
        for window in self.target_windows:
            window.activate()
            center_x, center_y = window.left + window.width // 2, window.top + window.height // 2
            for _ in range(10):
                pyautogui.click(center_x, center_y)
                time.sleep(0.1)
        
        self.root.after(1000, self.click_loop)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
