import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk
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

        # Set the background image
        self.set_background()

        self.create_main_menu()
        self.register_hotkey()

        # Override close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def set_background(self):
        try:
            bg_image = tk.PhotoImage(file="bg.png")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {e}")
            return None

        # Debugging: Check if the image is loaded
        if bg_image.width() == 0 or bg_image.height() == 0:
            print("Debug: Background image failed to load or is empty.")
        else:
            print(f"Debug: Background image loaded with size {bg_image.width()}x{bg_image.height()}.")

        # Resize the window to match the background image dimensions
        self.root.geometry(f"{bg_image.width()}x{bg_image.height()}")

        # Restore the original window size
        self.root.geometry("360x640")

        # Create a label to hold the background image
        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.image = bg_image  # Keep a reference to avoid garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Stretch to fill the window

        # Load and resize the background image using PIL
        original_image = Image.open("bg.png")
        resized_image = original_image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(resized_image)

        # Update the label with the resized image
        bg_label.config(image=bg_image)
        bg_label.image = bg_image  # Keep a reference to avoid garbage collection

        # Lower the background label to ensure it stays at the bottom
        bg_label.lower()

        # Force a redraw of the UI to ensure the background is visible
        self.root.update()

        # Schedule resizing after the window is fully initialized
        self.root.after(100, self.resize_background, bg_label)

        return bg_label

    def resize_background(self, bg_label):
        original_image = Image.open("bg.png")
        resized_image = original_image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(resized_image)
        bg_label.config(image=bg_image)
        bg_label.image = bg_image  # Keep a reference to avoid garbage collection

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

    def create_custom_strings_menu(self):
        from custom_strings import CustomStringsMenu
        custom_strings_menu = CustomStringsMenu(self.root, self.create_main_menu)
        custom_strings_menu.show()

    def add_back_button(self):
        back_button = tk.Button(self.root, text="←", command=self.create_main_menu, font=("Arial", 12), bg="lightgray")
        back_button.place(x=10, y=10)

    def create_main_menu(self):
        # Ensure the background is not destroyed
        for widget in self.root.winfo_children():
            if not isinstance(widget, tk.Label):  # Keep the background label
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

        custom_strings_button = tk.Button(self.root, text="Custom Strings", command=self.create_custom_strings_menu)
        self.style_button(custom_strings_button)
        custom_strings_button.pack(pady=10)

        quit_button = tk.Button(self.root, text="Quit", command=self.quit_app)
        self.style_button(quit_button)
        quit_button.config(bg="red", fg="white")
        quit_button.pack(pady=20)

        # Load links from JSON
        try:
            with open("links.json", "r", encoding="utf-8") as file:  # Use UTF-8 encoding to support emojis
                links = json.load(file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load links.json: {e}")
            return

        # Create small buttons for links
        button_size = 50
        total_width = (button_size * 4) + (20 * 3)  # 4 buttons + 3 spacings
        x_offset = (self.root.winfo_width() - total_width) // 2  # Center horizontally
        y_offset = self.root.winfo_height() - button_size - 20  # 20px margin from bottom
        spacing = 20

        for i in range(1, 5):
            link = links.get(f"button_{i}")
            if link:
                button_name = f"Button {i}"  # Default name
                if isinstance(link, dict):
                    button_name = link.get("name", button_name)
                    link = link.get("url", link)  # Update link if nested

                button = tk.Button(
                    self.root,
                    text=button_name,
                    command=lambda url=link: self.open_link(url),
                    font=("Gothic", 9),
                    bg="#ffcc00",  # Bright yellow background for better visibility
                    fg="black",  # Black text for contrast
                    activebackground="#ff9900",  # Orange for active state
                    activeforeground="white",  # White text for active state
                    relief="raised",
                    bd=2
                )
                button.place(x=x_offset, y=y_offset, width=button_size, height=button_size)
                x_offset += button_size + spacing

    def open_link(self, url):
        import webbrowser
        webbrowser.open(url)

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
    root.configure(bg="#e13974")  # Or the pink hex from your image
    app = App(root)
    root.mainloop()

