import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class CustomStringsMenu:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.buttons = []
        self.text_widget = None

    def show(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Set background
        try:
            original_image = Image.open("bg.png")
            resized_image = original_image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.Resampling.LANCZOS)
            bg_image = ImageTk.PhotoImage(resized_image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {e}")
            return

        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.image = bg_image  # Keep reference
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Back button
        back_button = tk.Button(self.root, text="←", command=self.back_callback, font=("Arial", 12), bg="lightgray")
        back_button.place(x=10, y=10)

        # Upload button
        upload_button = tk.Button(self.root, text="Upload TXT", command=self.upload_file, font=("Arial", 12), bg="lightblue")
        upload_button.place(x=150, y=10)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file_path:
            return

        try:
            with open(file_path, "r") as file:
                content = file.read()
            self.parse_file(content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")

    def parse_file(self, content):
        # Clear existing buttons and text widget
        for button in self.buttons:
            button.destroy()
        self.buttons.clear()
        if self.text_widget:
            self.text_widget.destroy()

        # Parse content
        categories = {}
        lines = content.splitlines()
        current_category = None

        for line in lines:
            line = line.strip()
            if line.startswith("//"):
                current_category = line[2:].strip()  # Remove // and trim
                categories[current_category] = []
            elif current_category:
                categories[current_category].append(line)

        # Create buttons for categories
        y_offset = 50
        for category, values in categories.items():
            button = tk.Button(self.root, text=category, command=lambda v=values: self.show_values(v), font=("Arial", 12), bg="lightgreen")
            button.place(x=10, y=y_offset, width=340, height=30)
            self.buttons.append(button)
            y_offset += 40

        # Create text widget at the bottom
        self.text_widget = tk.Text(self.root, wrap="word", font=("Arial", 12), state="disabled")
        self.text_widget.place(x=10, y=400, width=340, height=200)

    def show_values(self, values):
        if self.text_widget:
            self.text_widget.config(state="normal")  # Enable editing temporarily to update content
            self.text_widget.delete("1.0", tk.END)
            import random
            random_value = random.choice(values)
            self.text_widget.insert(tk.END, random_value)
            self.text_widget.config(state="disabled")  # Disable editing again
