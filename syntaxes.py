import tkinter as tk
import json
import random

class SyntaxMenu:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.auto_copy = False

    def style_button(self, button):
        button.config(width=20, height=2, bg="lightblue", activebackground="blue", fg="black")

    def show(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        syntax1_button = tk.Button(self.root, text="Syntax 1", command=self.generate_syntax)
        self.style_button(syntax1_button)
        syntax1_button.pack(pady=10)

        syntax2_button = tk.Button(self.root, text="Syntax 2")
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

    def generate_syntax(self):
        try:
            # Load and filter resources based on checkbox_states
            with open("resources.json") as f:
                res_data = json.load(f)

                checkbox_states = res_data.get("checkbox_states", {})
                resources = {
                    res: res_data[res]
                    for res, enabled in checkbox_states.items()
                    if enabled and res in res_data
                }

            with open("packs.json") as f:
                packs_data = json.load(f)
                global_pack_keys = packs_data.get("global_pack_key", [])

            with open("dynamic_manager.json") as f:
                dr_data = json.load(f)
                dr_keys = dr_data.get("dr_custom_keys", [])
                chest_keys = dr_data.get("chest_custom_keys", [])

            if not resources or not global_pack_keys or not dr_keys or not chest_keys:
                raise ValueError("One or more required input lists are empty")

            # Choose 2 active resources
            selected_resources = random.sample(list(resources.keys()), k=min(2, len(resources)))
            res_parts = [
                f"{res}:{random.randint(1, resources[res])}" for res in selected_resources
            ]

            # Keys
            chest_key = random.choice(chest_keys)
            dr_key = random.choice(dr_keys)
            sticker_pack_key = random.choice(global_pack_keys)
            fallback = random.choice(list(resources.keys()))
            fallback_val = random.randint(1, resources[fallback])
            dr_val = random.randint(1, resources[dr_key]) if dr_key in resources else random.randint(1, 10)

            # Syntax lines
            dr_syntax = f"[dynamic({dr_key}:{dr_val})|{fallback}:{fallback_val}]"
            sticker_syntax = f"[sticker_pack:{sticker_pack_key}]"

            full_syntax = f"chest:{chest_key}(" + "+".join(res_parts + [dr_syntax, sticker_syntax]) + ")"

            self.text_display.config(state="normal")
            self.text_display.delete("1.0", "end")
            self.text_display.insert("end", full_syntax + "\n")
            self.text_display.config(state="disabled")

            if self.auto_copy:
                self.root.clipboard_clear()
                self.root.clipboard_append(full_syntax)
                self.root.update()

        except Exception as e:
            self.text_display.config(state="normal")
            self.text_display.delete("1.0", "end")
            self.text_display.insert("end", f"Error: {e}\n")
            self.text_display.config(state="disabled")
