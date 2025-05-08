import tkinter as tk
import json

class SettingsMenu:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

    def style_button(self, button):
        button.config(width=20, height=2, bg="lightblue", activebackground="blue", fg="black")

    def show(self):
        # Clear current widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create Settings Menu buttons
        back_button = tk.Button(self.root, text="←", command=self.back_callback, font=("Arial", 12), bg="lightgray")
        back_button.place(x=10, y=10)

        resource_manager_button = tk.Button(self.root, text="Resource Manager", command=self.open_resource_manager)
        self.style_button(resource_manager_button)
        resource_manager_button.pack(pady=50)

        dynamic_manager_button = tk.Button(self.root, text="Dynamic Manager", command=self.create_dynamic_manager)
        self.style_button(dynamic_manager_button)
        dynamic_manager_button.pack(pady=50)

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
        self.data = self.load_json()

    def load_json(self):
        try:
            with open(self.json_file, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Create default structure if file doesn't exist or is corrupted
            return {"chest_custom_keys": [], "dr_custom_keys": []}

    def save_json(self):
        with open(self.json_file, "w") as file:
            json.dump(self.data, file, indent=4)

    def create_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Back button
        back_button = tk.Button(self.root, text="←", command=self.back_callback, font=("Arial", 12), bg="lightgray")
        back_button.place(x=10, y=10)

        # Custom Chest input
        chest_label = tk.Label(self.root, text="Custom Chest:")
        chest_label.pack(pady=5)
        chest_entry = tk.Entry(self.root, width=40)
        chest_entry.pack(pady=5)
        chest_button = tk.Button(self.root, text="Upload to JSON", command=lambda: self.upload_to_json("chest_custom_keys", chest_entry))
        chest_button.pack(pady=5)

        # Custom DR input
        dr_label = tk.Label(self.root, text="Custom DR:")
        dr_label.pack(pady=5)
        dr_entry = tk.Entry(self.root, width=40)
        dr_entry.pack(pady=5)
        dr_button = tk.Button(self.root, text="Upload to JSON", command=lambda: self.upload_to_json("dr_custom_keys", dr_entry))
        dr_button.pack(pady=5)

    def upload_to_json(self, key, entry):
        value = entry.get()
        if value:
            self.data[key].append(value)
            self.save_json()
            print(f"Uploaded '{value}' to {key} in {self.json_file}")
            entry.delete(0, tk.END)  # Clear the entry box