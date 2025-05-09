import tkinter as tk
from PIL import Image, ImageTk
import os

class RandomMenu:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.widgets = []  # Track widgets for cleanup

    def show(self):
        # Set the background
        bg_image = tk.PhotoImage(file="bg.png")
        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.image = bg_image  # Keep a reference to avoid garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()  # Ensure the background label is always at the bottom
        self.widgets.append(bg_label)

        # Add the back button
        if os.path.exists("left-arrow.png"):
            original_image = Image.open("left-arrow.png")
            resized_image = original_image.resize((20, 20), Image.Resampling.LANCZOS)
            back_arrow_image = ImageTk.PhotoImage(resized_image)
            back_button = tk.Button(self.root, image=back_arrow_image, command=self.go_back, bg="lightgray")
            back_button.image = back_arrow_image  # Keep a reference to avoid garbage collection
            back_button.place(x=10, y=10)
            self.widgets.append(back_button)
        else:
            print("Error: left-arrow.png file not found.")

        # Add a non-editable text box at the bottom
        text_display = tk.Text(self.root, height=5, width=40, state="disabled", wrap="word")
        text_display.pack(side="bottom", pady=10)
        self.widgets.append(text_display)
        self.text_display = text_display

    def go_back(self):
        # Destroy all widgets created by this menu
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()
        # Call the back callback
        self.back_callback()

    def update_text(self, text):
        self.text_display.config(state="normal")
        self.text_display.delete("1.0", "end")
        self.text_display.insert("end", text)
        self.text_display.config(state="disabled")
