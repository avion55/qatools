import tkinter as tk
import json
from PIL import Image, ImageTk

class ResourceManager:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.bg_color = "#e13974"
        self.root.configure(bg=self.bg_color)
        self.resources = self.load_resources()
        self.create_ui()

    def load_resources(self):
        try:
            with open("resources.json", "r") as file:
                data = json.load(file)
                self.checkbox_states = data.get("checkbox_states", {key: True for key in data.keys() if key != "checkbox_states"})
                return {key: value for key, value in data.items() if key != "checkbox_states"}
        except (FileNotFoundError, json.JSONDecodeError):
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

        data_to_save = self.resources.copy()
        data_to_save["checkbox_states"] = self.checkbox_states

        with open("resources.json", "w") as file:
            json.dump(data_to_save, file, indent=4)

        tk.messagebox.showinfo("Saved", "Resources have been saved successfully!")

    def create_ui(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Canvas):  # keep canvas
                continue
            widget.destroy()

        self.sliders = {}
        self.checkboxes = {}
        self.checkbox_vars = {}

        # Back button
        self.back_button = tk.Button(self.root, text="←", command=self.back_callback, font=("Arial", 12), bg="lightgray", bd=0, highlightthickness=0)
        self.back_button.place(x=10, y=10)

        # Spacer
        spacer = tk.Frame(self.root, height=60, bg=self.bg_color, bd=0, highlightthickness=0)
        spacer.pack()

        # Resources
        for resource, value in self.resources.items():
            frame = tk.Frame(self.root, bg=self.bg_color, bd=0, highlightthickness=0)
            frame.pack(fill="x", padx=10, pady=5)

            var = tk.BooleanVar(value=self.checkbox_states.get(resource, True))
            checkbox = tk.Checkbutton(frame, text=resource, variable=var, command=lambda r=resource, v=var: self.toggle_resource(r, v),
                                      bg=self.bg_color, activebackground=self.bg_color, selectcolor=self.bg_color)
            checkbox.pack(side="left", padx=5)
            self.checkboxes[resource] = checkbox
            self.checkbox_vars[resource] = var

            max_value = 100 if resource != "coins" else 1000000
            slider = tk.Scale(frame, from_=1, to=max_value, orient="horizontal", length=200,
                              bg=self.bg_color, troughcolor="#f175a2", highlightthickness=0, bd=0)
            slider.set(value)
            slider.pack(side="right")
            self.sliders[resource] = slider

        # Save button
        save_button = tk.Button(self.root, text="Save", command=self.save_resources, bg="green", fg="white", width=20, height=2, bd=0, highlightthickness=0)
        save_button.pack(pady=10)

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

    def show(self):
        def apply_background():
            width = self.root.winfo_width()
            height = self.root.winfo_height()

            self.canvas = tk.Canvas(self.root, width=width, height=height, highlightthickness=0, bd=0)
            bg_image = Image.open("bg.png").resize((width, height), Image.Resampling.LANCZOS)
            self.bg_image_tk = ImageTk.PhotoImage(bg_image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image_tk)
            self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
            self.canvas.lower()

            for widget in self.root.winfo_children():
                if not isinstance(widget, tk.Canvas):
                    widget.destroy()

            self.create_ui()
            self.back_button.lift()

        self.root.after(50, apply_background)

    def resize_background(self, bg_label):
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
