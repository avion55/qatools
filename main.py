import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk
from infi.systray import SysTrayIcon
from pynput import keyboard
from settings import SettingsMenu
from resource_manager import ResourceManager
from syntaxes import SyntaxMenu
from album import AlbumMenu
from custom_strings import CustomStringsMenu
import threading
import sys
import json
import os
import socket  # Add socket to implement a single-instance check


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SuperTools Alpha")

        # Center the window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 360
        window_height = 640
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.root.resizable(False, False)  # Make it un-resizable

        # Set the application icon
        self.root.iconbitmap("superplay_icon.ico")

        self.is_hidden = False
        self.is_closing = False  # Flag to prevent multiple shutdowns

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

    def create_random_menu(self):
        # Destroy all widgets in the main menu
        for widget in self.root.winfo_children():
            if not isinstance(widget, tk.Label):  # Keep the background label
                widget.destroy()

        # Show the Random Menu
        from random_menu import RandomMenu
        random_menu = RandomMenu(self.root, self.create_main_menu)
        random_menu.show()

    def add_back_button(self):
        if os.path.exists("left-arrow.png"):
            original_image = Image.open("left-arrow.png")
            resized_image = original_image.resize((20, 20), Image.Resampling.LANCZOS)
            back_arrow_image = ImageTk.PhotoImage(resized_image)
            back_button = tk.Button(self.root, image=back_arrow_image, command=self.create_main_menu, bg="lightgray")
            back_button.image = back_arrow_image  # Keep a reference to avoid garbage collection
            back_button.place(x=10, y=10)
        else:
            print("Error: left-arrow.png file not found.")

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

        random_menu_button = tk.Button(self.root, text="Random Menu", command=self.create_random_menu)
        self.style_button(random_menu_button)
        random_menu_button.pack(pady=10)

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
        """Handle the close button (X) event to minimize the app."""
        if not self.is_closing:  # Ensure the app is not in the process of shutting down
            self.hide_window()  # Minimize the app to the system tray
        else:
            print("App is already in the process of shutting down.")

    def hide_window(self):
        """Minimize the app to the system tray."""
        if not self.is_hidden:  # Prevent redundant calls to minimize
            self.is_hidden = True
            self.root.withdraw()
            self.show_tray_icon()
        else:
            print("App is already minimized.")

    def show_window(self, systray=None):
        """Restore the app window."""
        if self.is_hidden:  # Only restore if the app is currently hidden
            self.is_hidden = False
            self.root.deiconify()
        else:
            print("App is already visible.")

    def quit_app(self, systray=None):
        """Quit the application gracefully."""
        if self.is_closing:  # Check if the application is already shutting down
            return
        self.is_closing = True  # Set the flag to indicate shutdown is in progress

        try:
            # Signal the tray icon thread to exit gracefully
            if hasattr(self, 'systray') and self.systray is not None:
                # Shutdown the systray in a separate thread to avoid joining the current thread
                threading.Thread(target=self.systray.shutdown, daemon=True).start()
                self.systray = None
        except Exception as e:
            print(f"Error shutting down systray: {e}")

        try:
            # Destroy the main application window
            if self.root is not None:
                self.root.destroy()
        except Exception as e:
            print(f"Error destroying root window: {e}")

        # Exit the application
        os._exit(0)  # Use os._exit to avoid thread join issues

    def show_tray_icon(self):
        """Show the system tray icon."""
        if hasattr(self, 'systray') and self.systray is not None:
            print("Tray icon is already running.")
            return  # Prevent creating multiple tray icons

        # Define the menu options for the tray icon
        menu_options = (
            ("Maximize(Shift+ALT+M)", None, self.show_window),  # Use the same method for the tray icon
        )

        # Define the tray icon
        self.systray = SysTrayIcon(
            "superplay_icon.ico", "SuperTools Alpha", menu_options, default_menu_index=1, on_quit=self.quit_app
        )

        # Override the left-click behavior to block both single and double left-click events
        def on_left_click(systray):
            if not self.is_closing:  # Prevent interaction if shutdown is in progress
                pass  # Ignore both single and double left-click events

        self.systray.on_left_click = on_left_click

        # Start the tray icon in a separate thread
        if not hasattr(self, 'tray_thread') or not self.tray_thread.is_alive():
            self.tray_thread = threading.Thread(target=self.systray.start, daemon=True)
            self.tray_thread.start()
        else:
            print("Tray icon thread is already running.")

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
                            self.show_window()  # Call the same method as the tray icon
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


def is_already_running():
    """Check if another instance of the app is already running."""
    try:
        # Create a socket to bind to a specific port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 65432))  # Use a specific port for the app
        return False  # No other instance is running
    except OSError:
        return True  # Another instance is already running


if __name__ == "__main__":
    if is_already_running():
        print("Another instance of the app is already running.")
        sys.exit(0)  # Exit if another instance is detected

    root = tk.Tk()
    root.configure(bg="#e13974")  # Or the pink hex from your image
    app = App(root)
    root.mainloop()

