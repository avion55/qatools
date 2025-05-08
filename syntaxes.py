import tkinter as tk
import json
import random
import os
from PIL import Image, ImageTk

class SyntaxMenu:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.auto_copy = False

    def style_button(self, button):
        button.config(width=20, height=2, bg="lightblue", activebackground="blue", fg="black")

    def show(self):
        # Set the background for the syntaxes menu
        bg_image = Image.open("bg.png")
        resized_image = bg_image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.Resampling.LANCZOS)
        bg_image_tk = ImageTk.PhotoImage(resized_image)

        # Store the background image as an instance variable to prevent garbage collection
        self.bg_image_tk = bg_image_tk

        bg_label = tk.Label(self.root, image=bg_image_tk)
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

        syntax1_button = tk.Button(self.root, text="Generate Random Chest", command=self.generate_syntax)
        self.style_button(syntax1_button)
        syntax1_button.pack(pady=10)

        syntax2_button = tk.Button(self.root, text="Generate DR Line", command=self.generate_dr_line)
        self.style_button(syntax2_button)
        syntax2_button.pack(pady=10)

        self.text_display = tk.Text(self.root, height=10, width=40, state="disabled", wrap="word")
        self.text_display.pack(pady=10)

        copy_button = tk.Button(self.root, text="Copy", command=self.copy_text)
        self.style_button(copy_button)
        copy_button.pack(pady=5)

        toggle_button = tk.Button(self.root, text="Auto-Copy: OFF", command=self.toggle_auto_copy)
        self.style_button(toggle_button)
        toggle_button.pack(pady=5)

        back_button = tk.Button(self.root, text="←", command=self.back_callback, font=("Arial", 12), bg="lightgray")
        back_button.place(x=10, y=10)

    def copy_text(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.text_display.get("1.0", "end-1c"))
        self.root.update()

    def toggle_auto_copy(self):
        self.auto_copy = not self.auto_copy
        toggle_button_text = "Auto-Copy: ON" if self.auto_copy else "Auto-Copy: OFF"
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button) and "Auto-Copy" in widget.cget("text"):
                widget.config(text=toggle_button_text)

    def load_resources(self):
        with open("resources.json") as f:
            res_data = json.load(f)
            checkbox_states = res_data.get("checkbox_states", {})
            return {
                res: res_data[res]
                for res, enabled in checkbox_states.items()
                if enabled and res in res_data
            }

    def load_dynamic_keys(self):
        dr_keys = []
        if os.path.exists("dynamic_manager.json"):
            with open("dynamic_manager.json") as f:
                dr_data = json.load(f)
                dr_keys = dr_data.get("dr_custom_keys", [])
        return dr_keys

    def generate_syntax(self):
        try:
            # Load all enabled resources from resources.json
            resources = self.load_resources()
            if not resources:
                raise ValueError("No enabled resources found in resources.json.")

            # Load global pack keys from packs.json
            global_pack_keys = []
            if os.path.exists("packs.json"):
                with open("packs.json") as f:
                    packs_data = json.load(f)
                    global_pack_keys = packs_data.get("global_pack_key", [])

            # Load dynamic keys and chest keys from dynamic_manager.json
            dr_keys = []
            chest_keys = []
            if os.path.exists("dynamic_manager.json"):
                with open("dynamic_manager.json") as f:
                    dr_data = json.load(f)
                    dr_keys = dr_data.get("dr_custom_keys", [])
                    chest_keys = dr_data.get("chest_custom_keys", [])

            if not chest_keys:
                raise ValueError("No chest keys available. Please create a custom chest key first.")

            # Include all enabled resources
            res_parts = [f"{res}:{random.randint(1, resources[res])}" for res in resources.keys()]

            # Select a random chest key
            chest_key = random.choice(chest_keys)

            # Generate dynamic syntax if dynamic keys are available
            dr_syntax = ""
            if dr_keys:
                dr_key = random.choice(dr_keys)
                fallback = random.choice(list(resources.keys()))
                fallback_val = random.randint(1, resources[fallback])
                dr_val = random.randint(1, resources.get(dr_key, 10))
                dr_syntax = f"[dynamic({dr_key}:{dr_val})|{fallback}:{fallback_val}]"

            # Generate sticker syntax if global pack keys are available
            sticker_syntax = ""
            if global_pack_keys:
                sticker_pack_key = random.choice(global_pack_keys)
                sticker_syntax = f"[sticker_pack:{sticker_pack_key}]"

            # Combine all parts into the final syntax
            syntax_parts = res_parts
            if dr_syntax:
                syntax_parts.append(dr_syntax)
            if sticker_syntax:
                syntax_parts.append(sticker_syntax)

            full_syntax = f"chest:{chest_key}(" + "+".join(syntax_parts) + ")"

            # Display the generated syntax
            self.text_display.config(state="normal")
            self.text_display.delete("1.0", "end")
            self.text_display.insert("end", full_syntax + "\n")
            self.text_display.config(state="disabled")

            # Auto-copy the syntax if enabled
            if self.auto_copy:
                self.root.clipboard_clear()
                self.root.clipboard_append(full_syntax)
                self.root.update()

        except Exception as e:
            # Handle errors and display them in the text display
            self.text_display.config(state="normal")
            self.text_display.delete("1.0", "end")
            self.text_display.insert("end", f"Error: {e}\n")
            self.text_display.config(state="disabled")

    def generate_dr_line(self):
        try:
            resources = self.load_resources()
            if not resources:
                raise ValueError("No enabled resources found in resources.json.")

            dr_keys = self.load_dynamic_keys()

            output_parts = []

            if dr_keys:
                dr_key = random.choice(dr_keys)
                fallback = random.choice(list(resources.keys()))
                fallback_val = random.randint(1, resources[fallback])
                dr_val = random.randint(1, resources.get(dr_key, 10))
                dr_syntax = f"[dynamic({dr_key}:{dr_val})|{fallback}:{fallback_val}]"
                output_parts.append(dr_syntax)

            # Add all available resources
            for res, max_val in resources.items():
                val = random.randint(1, max_val)
                output_parts.append(f"{res}:{val}")

            full_line = "+".join(output_parts)

            self.text_display.config(state="normal")
            self.text_display.delete("1.0", "end")
            self.text_display.insert("end", full_line + "\n")
            self.text_display.config(state="disabled")

            if self.auto_copy:
                self.root.clipboard_clear()
                self.root.clipboard_append(full_line)
                self.root.update()

        except Exception as e:
            self.text_display.config(state="normal")
            self.text_display.delete("1.0", "end")
            self.text_display.insert("end", f"Error: {e}\n")
            self.text_display.config(state="disabled")

    def resize_background(self, bg_label):
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)