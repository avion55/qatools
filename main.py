import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw
import pystray
from pynput import keyboard
import threading
import sys
from syntaxes import SyntaxMenu

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartApp")
        self.root.geometry("360x640")  # Smartphone size
        self.root.resizable(False, False)  # Make it un-resizable

        self.is_hidden = False

        self.create_main_menu()
        self.register_hotkey()

        # Override close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_syntax_menu(self):
        # Clear main menu buttons
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create Syntax Menu buttons
        tk.Button(self.root, text="Syntax 1", height=2).pack(pady=10)
        tk.Button(self.root, text="Syntax 2", height=2).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu, bg="blue", fg="white").pack(pady=20)

    def create_main_menu(self):
        # Clear syntax menu buttons
        for widget in self.root.winfo_children():
            widget.destroy()

        # Recreate main menu buttons
        self.create_buttons()

    def create_buttons(self):
        tk.Button(self.root, text="Syntax Menu", command=self.create_syntax_menu, height=2).pack(pady=10)
        tk.Button(self.root, text="Quit", command=self.quit_app, bg="red", fg="white").pack(pady=20)

    def on_closing(self):
        self.hide_window()

    def hide_window(self):
        self.is_hidden = True
        self.root.withdraw()
        self.show_tray_icon()

    def show_window(self):
        self.is_hidden = False
        self.root.deiconify()
        self.icon.stop()

    def quit_app(self):
        try:
            if hasattr(self, 'icon'):
                self.icon.stop()
        except Exception:
            pass
        self.root.destroy()
        sys.exit()

    def show_tray_icon(self):
        # Create an icon image
        image = Image.new('RGB', (64, 64), color='black')
        dc = ImageDraw.Draw(image)
        dc.rectangle((0, 0, 64, 64), fill='blue')
        dc.text((10, 20), 'App', fill='white')

        self.icon = pystray.Icon("name", image, "SmartApp", menu=None)
        threading.Thread(target=self.icon.run, daemon=True).start()

    def register_hotkey(self):
        def on_press(key):
            try:
                if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                    self.alt_pressed = True
                elif key == keyboard.Key.shift:
                    self.shift_pressed = True
                elif hasattr(key, 'char') and key.char.lower() == 'm':
                    if getattr(self, 'alt_pressed', False) and getattr(self, 'shift_pressed', False):
                        if self.is_hidden:
                            self.show_window()
            except Exception:
                pass

        def on_release(key):
            if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                self.alt_pressed = False
            elif key == keyboard.Key.shift:
                self.shift_pressed = False

        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.daemon = True
        listener.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
