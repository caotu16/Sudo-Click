"""
SUDO Click Global - Công cụ click với Global Hotkey
Author: Sudo
Version: 5.0.0 - Perfect Edition
"""

import tkinter as tk
import time
import threading
import webbrowser
import sys
import ctypes
from ctypes import wintypes
import keyboard  # Thư viện keyboard cho global hotkey

# Windows API constants
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202

class SUDOClickGlobal:
    def __init__(self):
        """Khởi tạo ứng dụng SUDO Click Global"""
        self.root = tk.Tk()
        self.is_running = False
        self.current_position = None
        self.click_count = 0
        self.total_clicks = 50
        self.click_delay = 0.2
        self.hotkey = 'f9'  # Phím tắt global
        
        # Load Windows API functions
        try:
            self.user32 = ctypes.windll.user32
            self.kernel32 = ctypes.windll.kernel32
        except:
            print("⚠ Không thể load Windows API, sử dụng fallback")
            self.user32 = None
        
        self.setup_window()
        self.setup_widgets()
        self.setup_global_hotkey()
        
        # In thông tin khởi động
        print("=== SUDO Click Global v5.0.0 by Sudo ===")
        print("🌍 Global Hotkey - Hoạt động ở mọi ứng dụng!")
        print("🔥 Tính năng:")
        print(f"  - Phím tắt GLOBAL: {self.hotkey.upper()}")
        print("  - Hoạt động khi đang trong game/app khác")
        print("  - Không cần focus vào SUDO Click")
        print("  - Click được vào mọi phần mềm")
        print("  - 50 lần click đôi với delay 0.2s")
        print("📖 Hướng dẫn:")
        print("  1. Để SUDO Click chạy nền")
        print("  2. Vào game/app khác")
        print(f"  3. Hover chuột + nhấn {self.hotkey.upper()} để click")
        print(f"  4. Nhấn {self.hotkey.upper()} lại để dừng")
        print("⚠ Lưu ý: Chạy với quyền Administrator!")
        print("=====================================")
    
    def setup_window(self):
        """Cấu hình cửa sổ chính"""
        self.root.title("SUDO Click")
        self.root.geometry("300x250")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
        
        # Căn giữa cửa sổ
        self.center_window()
        
        # Đặt cửa sổ luôn ở trên cùng
        self.root.attributes('-topmost', True)
        
        # Minimize to system tray style
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
    
    def center_window(self):
        """Căn giữa cửa sổ"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def minimize_to_tray(self):
        """Ẩn cửa sổ thay vì đóng"""
        self.root.withdraw()  # Ẩn cửa sổ
        print("💡 SUDO Click đang chạy nền. Nhấn F9 ở bất kỳ đâu!")
    
    def show_window(self):
        """Hiện lại cửa sổ"""
        self.root.deiconify()
        self.root.lift()
        self.root.attributes('-topmost', True)
    
    def setup_widgets(self):
        """Tạo giao diện đơn giản"""
        # Main frame
        self.main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=10, pady=10)
        self.main_frame.pack(fill='both', expand=True)
        
        # Status text variable
        self.status_text = tk.StringVar()
        self.status_text.set(f"Nhấn {self.hotkey.upper()} để chạy")
        
        # Main status button - TO GẤPE ĐÔI
        self.main_button = tk.Button(
            self.main_frame,
            textvariable=self.status_text,
            font=('Arial', 10),
            relief='raised',
            bd=1,
            padx=5,
            pady=12,  # Tăng gấp đôi từ 5 lên 12
            width=22,
            state='disabled',
            bg='white',
            fg='black'
        )
        self.main_button.pack(pady=(0, 8))
        
        # Global status label - TEXT MỚI DÀI HƠN
        self.global_label = tk.Label(
            self.main_frame,
            text="Chạy phần mềm này với quyền Administrator,\nđưa chuột vào vị trí cần click và nhấn F9\nđể Chạy hoặc Dừng.",
            font=('Arial', 8),
            bg='#f0f0f0',
            fg='green',
            justify='center'
        )
        self.global_label.pack(pady=(0, 8))
        
        # Version label - THÊM PHIÊN BẢN
        self.version_label = tk.Label(
            self.main_frame,
            text="Phiên bản 5.0.0",
            font=('Arial', 7),
            bg='#f0f0f0',
            fg='gray'
        )
        self.version_label.pack(pady=(0, 8))
        
        # Help button
        self.help_button = tk.Button(
            self.main_frame,
            text="Hỗ trợ",
            font=('Arial', 9),
            relief='raised',
            bd=1,
            padx=5,
            pady=3,
            width=22,
            command=self.open_help,
            bg='white',
            fg='black'
        )
        self.help_button.pack(pady=(0, 5))
        
        # Exit instruction
        self.exit_instruction = tk.Label(
            self.main_frame,
            text="Nhấn nút Thoát để tắt hẳn phần mềm",
            font=('Arial', 7),
            bg='#f0f0f0',
            fg='red'
        )
        self.exit_instruction.pack(pady=(0, 5))
        
        # Exit button
        self.exit_button = tk.Button(
            self.main_frame,
            text="Thoát",
            font=('Arial', 9),
            relief='raised',
            bd=1,
            padx=5,
            pady=3,
            width=22,
            command=self.exit_app,
            bg='#ffcccc',
            fg='red'
        )
        self.exit_button.pack()
    
    def setup_global_hotkey(self):
        """Đăng ký global hotkey"""
        try:
            # Đăng ký phím tắt global
            keyboard.add_hotkey(self.hotkey, self.on_global_hotkey)
            print(f"✅ Đã đăng ký global hotkey: {self.hotkey.upper()}")
            
            # Đăng ký thêm Ctrl+Shift+S để hiện cửa sổ
            keyboard.add_hotkey('ctrl+shift+s', self.show_window)
            print("✅ Đăng ký Ctrl+Shift+S để hiện cửa sổ")
            
        except Exception as e:
            print(f"❌ Lỗi đăng ký global hotkey: {e}")
            print("⚠ Có thể cần chạy với quyền Administrator")
            
            # Fallback: local hotkey
            self.root.bind(f'<KeyPress-{self.hotkey.upper()}>', self.on_global_hotkey)
            self.root.focus_set()
    
    def get_cursor_position(self):
        """Lấy vị trí chuột bằng Windows API"""
        try:
            if self.user32:
                point = wintypes.POINT()
                self.user32.GetCursorPos(ctypes.byref(point))
                return (point.x, point.y)
            else:
                # Fallback method
                import pyautogui
                pos = pyautogui.position()
                return (int(pos.x), int(pos.y))
        except Exception as e:
            print(f"❌ Lỗi lấy vị trí chuột: {e}")
            return (500, 300)
    
    def windows_click(self, x, y):
        """Click bằng Windows API"""
        try:
            if not self.user32:
                return self.fallback_click(x, y)
            
            # Lấy handle của cửa sổ tại vị trí click
            hwnd = self.user32.WindowFromPoint(wintypes.POINT(x, y))
            
            if hwnd:
                # Chuyển đổi tọa độ screen sang client
                client_point = wintypes.POINT(x, y)
                self.user32.ScreenToClient(hwnd, ctypes.byref(client_point))
                
                # Tạo lParam từ tọa độ
                lParam = (client_point.y << 16) | (client_point.x & 0xFFFF)
                
                # Click đôi bằng PostMessage
                self.user32.PostMessageW(hwnd, WM_LBUTTONDOWN, 0, lParam)
                time.sleep(0.01)
                self.user32.PostMessageW(hwnd, WM_LBUTTONUP, 0, lParam)
                time.sleep(0.01)
                self.user32.PostMessageW(hwnd, WM_LBUTTONDOWN, 0, lParam)
                time.sleep(0.01)
                self.user32.PostMessageW(hwnd, WM_LBUTTONUP, 0, lParam)
                
                return True
            else:
                return self.fallback_click(x, y)
                
        except Exception as e:
            print(f"❌ Lỗi Windows API: {e}")
            return self.fallback_click(x, y)
    
    def fallback_click(self, x, y):
        """Phương pháp click fallback"""
        try:
            if self.user32:
                # Method 1: SetCursorPos + mouse_event
                self.user32.SetCursorPos(x, y)
                time.sleep(0.01)
                self.user32.mouse_event(0x0002, 0, 0, 0, 0)  # LEFTDOWN
                time.sleep(0.01)
                self.user32.mouse_event(0x0004, 0, 0, 0, 0)  # LEFTUP
                time.sleep(0.01)
                self.user32.mouse_event(0x0002, 0, 0, 0, 0)  # LEFTDOWN
                time.sleep(0.01)
                self.user32.mouse_event(0x0004, 0, 0, 0, 0)  # LEFTUP
                return True
            else:
                # Method 2: pyautogui fallback
                import pyautogui
                pyautogui.doubleClick(x, y)
                return True
        except Exception as e:
            print(f"❌ Lỗi fallback click: {e}")
            return False
    
    def on_global_hotkey(self):
        """Xử lý khi nhấn global hotkey"""
        print(f"🔥 Global hotkey {self.hotkey.upper()} được nhấn!")
        print(f"   Trạng thái: {'đang chạy' if self.is_running else 'đã dừng'}")
        
        if not self.is_running:
            self.start_clicking()
        else:
            self.stop_clicking()
    
    def start_clicking(self):
        """Bắt đầu auto-clicking"""
        try:
            # Lấy vị trí chuột hiện tại
            self.current_position = self.get_cursor_position()
            print(f"📍 Vị trí click: {self.current_position}")
            
            self.is_running = True
            self.click_count = 0
            self.status_text.set(f"Nhấn {self.hotkey.upper()} để dừng")
            
            print("🚀 Bắt đầu global auto-click...")
            
            # Bắt đầu clicking trong thread riêng
            click_thread = threading.Thread(target=self.click_loop, daemon=True)
            click_thread.start()
            
        except Exception as e:
            print(f"❌ Lỗi khi bắt đầu: {e}")
    
    def stop_clicking(self):
        """Dừng auto-clicking"""
        self.is_running = False
        self.status_text.set(f"Nhấn {self.hotkey.upper()} để chạy")
        print(f"⏹ Đã dừng! Hoàn thành {self.click_count} lần click")
    
    def click_loop(self):
        """Vòng lặp thực hiện click"""
        try:
            print(f"🎯 Bắt đầu global click {self.total_clicks} lần tại {self.current_position}")
            
            while self.is_running and self.click_count < self.total_clicks:
                if self.current_position:
                    x, y = self.current_position
                    success = self.windows_click(x, y)
                    
                    if success:
                        self.click_count += 1
                        remaining = self.total_clicks - self.click_count
                        print(f"🖱 Global Click {self.click_count}/{self.total_clicks} (còn {remaining})")
                        
                        # Cập nhật UI thread-safe
                        self.root.after(0, lambda: self.status_text.set(f"Đang chạy... ({remaining} lần)"))
                    
                    time.sleep(self.click_delay)
                else:
                    break
            
            # Hoàn thành
            self.is_running = False
            if self.click_count >= self.total_clicks:
                print("✅ Hoàn thành tất cả global clicks!")
                self.root.after(0, lambda: self.status_text.set("Hoàn thành! F9 để chạy lại"))
                self.root.after(3000, lambda: self.status_text.set(f"Nhấn {self.hotkey.upper()} để chạy"))
            else:
                self.root.after(0, lambda: self.status_text.set(f"Nhấn {self.hotkey.upper()} để chạy"))
                
        except Exception as e:
            print(f"❌ Lỗi trong vòng lặp: {e}")
            self.is_running = False
    
    def open_help(self):
        """Mở trang web hỗ trợ"""
        try:
            print("🌐 Mở trang hỗ trợ...")
            webbrowser.open("https://nguyencaotu.com")
        except Exception as e:
            print(f"❌ Không thể mở trình duyệt: {e}")
    
    def exit_app(self):
        """Thoát hoàn toàn khỏi ứng dụng"""
        try:
            print("👋 Đang thoát SUDO Click...")
            # Dọn dẹp global hotkey
            keyboard.unhook_all()
            # Dừng auto-clicking nếu đang chạy
            self.is_running = False
            # Đóng ứng dụng
            self.root.quit()
            self.root.destroy()
        except Exception as e:
            print(f"❌ Lỗi khi thoát: {e}")
        finally:
            sys.exit(0)
    
    def run(self):
        """Chạy ứng dụng"""
        try:
            print("💡 Tip: Đóng cửa sổ để chạy nền, Ctrl+Shift+S để hiện lại")
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n👋 Ứng dụng đã đóng!")
        except Exception as e:
            print(f"❌ Lỗi ứng dụng: {e}")
        finally:
            try:
                keyboard.unhook_all()
            except:
                pass
            print("🔚 SUDO Click Global đã kết thúc")

def main():
    """Hàm chính"""
    try:
        app = SUDOClickGlobal()
        app.run()
    except Exception as e:
        print(f"❌ Lỗi khởi động SUDO Click Global: {e}")
        input("Nhấn Enter để thoát...")

if __name__ == "__main__":
    main()
