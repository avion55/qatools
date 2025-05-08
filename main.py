import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw
import pystray
from pynput import keyboard
import threading
import sys
import json
from syntaxes import SyntaxMenu
from settings import SettingsMenu
from album import AlbumMenu
from resource_manager import ResourceManager

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

    def set_background(self):
        # Set a solid background color using yellow and pink stripes
        canvas = tk.Canvas(self.root, width=360, height=640, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        for i in range(0, 640, 40):
            color = "pink" if i % 80 == 0 else "yellow"
            canvas.create_rectangle(0, i, 360, i + 40, fill=color, outline="")

        return canvas

    def create_syntax_menu(self):
        syntax_menu = SyntaxMenu(self.root, self.create_main_menu)
        syntax_menu.show()
        self.add_back_button()

    def create_settings_menu(self):
        settings_menu = SettingsMenu(self.root, self.create_main_menu)
        settings_menu.show()
        self.add_back_button()

    def create_resource_manager(self):
        resource_manager = ResourceManager(self.root, self.create_settings_menu)
        resource_manager.create_ui()

    def create_album_menu(self):
        album_menu = AlbumMenu(self.root, self.create_main_menu)
        album_menu.show()
        self.add_back_button()

    def add_back_button(self):
        back_button = tk.Button(self.root, text="←", command=self.create_main_menu, font=("Arial", 12), bg="lightgray")
        back_button.place(x=10, y=10)

    def create_main_menu(self):
        # Clear syntax menu buttons
        for widget in self.root.winfo_children():
            widget.destroy()

        # Recreate buttons
        self.create_buttons()

    def style_button(self, button):
        button.config(width=20, height=2, bg="lightblue", activebackground="blue", fg="black")

    def create_buttons(self):
        syntax_button = tk.Button(self.root, text="Syntax Menu", command=self.create_syntax_menu)
        self.style_button(syntax_button)
        syntax_button.pack(pady=10)

        settings_button = tk.Button(self.root, text="Settings", command=self.create_settings_menu)
        self.style_button(settings_button)
        settings_button.pack(pady=10)

        album_button = tk.Button(self.root, text="Album", command=self.create_album_menu)
        self.style_button(album_button)
        album_button.pack(pady=10)

        quit_button = tk.Button(self.root, text="Quit", command=self.quit_app)
        self.style_button(quit_button)
        quit_button.config(bg="red", fg="white")
        quit_button.pack(pady=20)

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
