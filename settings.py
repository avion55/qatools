import tkinter as tk
import json
import os
from PIL import Image, ImageTk, ImageStat  # Add this import for color analysis

class SettingsMenu:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

    def style_button(self, button):
        button.config(width=20, height=2, bg="lightblue", activebackground="blue", fg="black")

    def show(self):
        # Set the background for the settings menu
        bg_image = Image.open("bg.png")
        resized_image = bg_image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.Resampling.LANCZOS)
        bg_image_tk = ImageTk.PhotoImage(resized_image)

        # Store the background image as an instance variable to prevent garbage collection
        self.bg_image_tk = bg_image_tk

        bg_label = tk.Label(self.root, image=bg_image_tk)
        bg_label.image = bg_image_tk  # Keep a reference to avoid garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()  # Ensure the background label is always at the bottom

        # Ensure the background label is not removed
        for widget in self.root.winfo_children():
            if not isinstance(widget, tk.Label):  # Keep the background label
                widget.destroy()

        # Force a redraw of the UI to ensure the background is visible
        self.root.update()

        # Schedule resizing after the window is fully initialized
        self.root.after(100, self.resize_background, bg_label)

        # Create Settings Menu buttons
        if os.path.exists("left-arrow.png"):
            original_image = Image.open("left-arrow.png")
            resized_image = original_image.resize((20, 20), Image.Resampling.LANCZOS)
            back_arrow_image = ImageTk.PhotoImage(resized_image)
            back_button = tk.Button(self.root, image=back_arrow_image, command=self.back_callback, bg="lightgray")
            back_button.image = back_arrow_image  # Keep a reference to avoid garbage collection
            back_button.place(x=10, y=10)
        else:
            print("Error: left-arrow.png file not found.")

        resource_manager_button = tk.Button(self.root, text="Resource Manager", command=self.open_resource_manager)
        self.style_button(resource_manager_button)
        resource_manager_button.pack(pady=50)

        dynamic_manager_button = tk.Button(self.root, text="Dynamic Manager", command=self.create_dynamic_manager)
        self.style_button(dynamic_manager_button)
        dynamic_manager_button.pack(pady=50)

    def resize_background(self, bg_label):
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def open_resource_manager(self):
        from resource_manager import ResourceManager
        resource_manager = ResourceManager(self.root, self.show)
        resource_manager.create_ui()

    def create_dynamic_manager(self):
        dynamic_manager = DynamicManager(self.root, self.show)
        dynamic_manager.create_ui()

class DynamicManager:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.json_file = "dynamic_manager.json"
        self.bg_color = self.get_dominant_color("bg.png")  # Dynamically set bg_color
        self.data = self.load_json()

    def get_dominant_color(self, image_path):
        """Extract the predominant color from an image."""
        try:
            image = Image.open(image_path)
            image = image.resize((1, 1))  # Resize to 1x1 to get the average color
            dominant_color = image.getpixel((0, 0))
            return f"#{dominant_color[0]:02x}{dominant_color[1]:02x}{dominant_color[2]:02x}"
        except Exception as e:
            print(f"Error extracting dominant color: {e}")
            return "#e13974"  # Default fallback color

    def load_json(self):
        try:
            with open(self.json_file, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"chest_custom_keys": [], "dr_custom_keys": []}

    def save_json(self):
        with open(self.json_file, "w") as file:
            json.dump(self.data, file, indent=4)

    def create_ui(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Canvas):
                continue  # keep canvas
            widget.destroy()

        # Back button at top-left
        if os.path.exists("left-arrow.png"):
            original_image = Image.open("left-arrow.png")
            resized_image = original_image.resize((20, 20), Image.Resampling.LANCZOS)
            back_arrow_image = ImageTk.PhotoImage(resized_image)
            self.back_button = tk.Button(self.root, image=back_arrow_image, command=self.exit_dynamic_manager, bg=self.bg_color, bd=0, highlightthickness=0)
            self.back_button.image = back_arrow_image  # Keep a reference to avoid garbage collection
            self.back_button.place(x=10, y=10)
        else:
            print("Error: left-arrow.png file not found.")

        # Spacer to avoid overlap
        spacer = tk.Frame(self.root, height=60, bg=self.bg_color)
        spacer.pack()

        # Chest label
        chest_label = tk.Label(self.root, text="Custom Chest:", bg=self.bg_color, fg="white", font=("Arial", 12, "bold"))
        chest_label.pack(pady=(10, 2))

        self.chest_entry = tk.Entry(self.root, width=40, bd=1, relief="flat", highlightthickness=1, highlightbackground="white")
        self.chest_entry.pack(pady=5)

        chest_button = tk.Button(self.root, text="Upload to JSON", command=lambda: self.upload_to_json("chest_custom_keys", self.chest_entry),
                                 bg="green", fg="white", width=20, height=1, bd=0, highlightthickness=0)
        chest_button.pack(pady=5)

        # DR label
        dr_label = tk.Label(self.root, text="Custom DR:", bg=self.bg_color, fg="white", font=("Arial", 12, "bold"))
        dr_label.pack(pady=(20, 2))

        self.dr_entry = tk.Entry(self.root, width=40, bd=1, relief="flat", highlightthickness=1, highlightbackground="white")
        self.dr_entry.pack(pady=5)

        dr_button = tk.Button(self.root, text="Upload to JSON", command=lambda: self.upload_to_json("dr_custom_keys", self.dr_entry),
                              bg="green", fg="white", width=20, height=1, bd=0, highlightthickness=0)
        dr_button.pack(pady=5)

    def upload_to_json(self, key, entry):
        value = entry.get().strip()
        if value:
            self.data[key].append(value)
            self.save_json()
            print(f"Uploaded '{value}' to {key} in {self.json_file}")
            entry.delete(0, tk.END)

    def exit_dynamic_manager(self):
        for widget in self.root.winfo_children():
            if not isinstance(widget, tk.Canvas):
                widget.destroy()
        self.back_callback()
