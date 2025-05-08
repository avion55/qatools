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
                data = json.load(file)
                # Load checkbox states from the JSON file
                self.checkbox_states = data.get("checkbox_states", {key: True for key in data.keys() if key != "checkbox_states"})
                return {key: value for key, value in data.items() if key != "checkbox_states"}
        except (FileNotFoundError, json.JSONDecodeError):
            # Default values if the file is missing or corrupted
            self.checkbox_states = {"free_wild": True, "free_undo": True, "free_stock": True, "free_entry": True, "coins": True}
            return {
                "free_wild": 1,
                "free_undo": 1,
                "free_stock": 1,
                "free_entry": 1,
                "coins": 1
            }

    def save_resources(self):
        for resource, slider in self.sliders.items():
            self.resources[resource] = slider.get()

        # Save checkbox states to the JSON file
        data_to_save = self.resources.copy()
        data_to_save["checkbox_states"] = self.checkbox_states

        with open("resources.json", "w") as file:
            json.dump(data_to_save, file, indent=4)

        tk.messagebox.showinfo("Saved", "Resources have been saved successfully!")

    def create_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        self.sliders = {}
        self.checkboxes = {}
        self.checkbox_vars = {}

        # Back button
        back_button = tk.Button(self.root, text="←", command=self.back_callback, font=("Arial", 12), bg="lightgray")
        back_button.place(x=10, y=10)

        # Adjust the starting position of resources to avoid overlap
        resources_frame = tk.Frame(self.root)
        resources_frame.pack(pady=(50, 0))  # Add top padding to push resources below the back button

        for resource, value in self.resources.items():
            # Create a frame for each resource inside the resources_frame
            frame = tk.Frame(resources_frame)
            frame.pack(fill="x", padx=10, pady=5)

            # Create a checkbox
            var = tk.BooleanVar(value=self.checkbox_states.get(resource, True))
            checkbox = tk.Checkbutton(frame, text=resource, variable=var, state="normal", command=lambda r=resource, v=var: self.toggle_resource(r, v))
            checkbox.pack(side="left", padx=5)
            self.checkboxes[resource] = checkbox
            self.checkbox_vars[resource] = var

            # Create a slider with a fixed length
            max_value = 100 if resource != "coins" else 1000000
            slider = tk.Scale(frame, from_=1, to=max_value, orient="horizontal", length=200)  # Set fixed length
            slider.set(value)
            slider.pack(side="right", fill="x", expand=False)
            self.sliders[resource] = slider

        # Save button
        save_button = tk.Button(self.root, text="Save", command=self.save_resources, bg="green", fg="white")
        save_button.pack(pady=10)

        # Test button
        test_button = tk.Button(self.root, text="TEST", command=self.test_resources, bg="blue", fg="white")
        test_button.pack(pady=10)

        # Add padding to avoid overlap
        padding_frame = tk.Frame(self.root, height=30)
        padding_frame.pack()

        self.ui_created = True

    def toggle_resource(self, resource, var):
        is_enabled = var.get()
        self.checkbox_states[resource] = is_enabled
        if is_enabled:
            self.sliders[resource].config(state="normal")
        else:
            self.sliders[resource].config(state="disabled")

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