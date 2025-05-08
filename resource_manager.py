import tkinter as tk
import json

class ResourceManager:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.resources = self.load_resources()
        self.create_ui()

    def load_resources(self):
        try:
            with open("resources.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "free_wild": 1,
                "free_undo": 1,
                "free_stock": 1,
                "free_entry": 1,
                "coins": 1
            }

    def create_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        self.sliders = {}
        self.checkboxes = {}
        self.checkbox_vars = {}

        for resource, value in self.resources.items():
            # Create a frame for each resource
            frame = tk.Frame(self.root)
            frame.pack(fill="x", padx=10, pady=5)

            # Create a checkbox
            var = tk.BooleanVar(value=True)
            checkbox = tk.Checkbutton(frame, text=resource, variable=var, state="normal", command=lambda r=resource: self.toggle_resource(r))
            checkbox.pack(side="left", padx=5)
            self.checkboxes[resource] = checkbox
            self.checkbox_vars[resource] = var

            # Create a slider
            max_value = 100 if resource != "coins" else 1000000
            slider = tk.Scale(frame, from_=1, to=max_value, orient="horizontal")
            slider.set(value)
            slider.pack(side="right", fill="x", expand=True)
            self.sliders[resource] = slider

        # Save button
        save_button = tk.Button(self.root, text="Save", command=self.save_resources, bg="green", fg="white")
        save_button.pack(pady=10)

        # Test button
        test_button = tk.Button(self.root, text="TEST", command=self.test_resources, bg="blue", fg="white")
        test_button.pack(pady=10)

        # Back button
        back_button = tk.Button(self.root, text="Back", command=self.back_callback, bg="blue", fg="white")
        back_button.pack(pady=10)

        self.ui_created = True

    def toggle_resource(self, resource):
        is_enabled = self.checkbox_vars[resource].get()
        if is_enabled:
            self.sliders[resource].config(state="normal")
        else:
            self.sliders[resource].config(state="disabled")

    def save_resources(self):
        for resource, slider in self.sliders.items():
            self.resources[resource] = slider.get()

        with open("resources.json", "w") as file:
            json.dump(self.resources, file, indent=4)

        tk.messagebox.showinfo("Saved", "Resources have been saved successfully!")

    def test_resources(self):
        import random
        enabled_resources = [
            f"{resource}:{random.randint(1, self.sliders[resource].get())}"
            for resource, var in self.checkbox_vars.items() if var.get()
        ]
        if enabled_resources:
            print("\n".join(enabled_resources))
        else:
            print("No resources are enabled.")