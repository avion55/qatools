import tkinter as tk

class SyntaxMenu:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

    def style_button(self, button):
        button.config(width=20, height=2, bg="lightblue", activebackground="blue", fg="black")

    def show(self):
        # Clear current widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create Syntax Menu buttons
        syntax1_button = tk.Button(self.root, text="Syntax 1")
        self.style_button(syntax1_button)
        syntax1_button.pack(pady=10)

        syntax2_button = tk.Button(self.root, text="Syntax 2")
        self.style_button(syntax2_button)
        syntax2_button.pack(pady=10)

        # Add a text printing element
        self.text_display = tk.Text(self.root, height=10, width=40, state="disabled", wrap="word")
        self.text_display.pack(pady=10)

        # Add a Copy button
        copy_button = tk.Button(self.root, text="Copy", command=self.copy_text)
        self.style_button(copy_button)
        copy_button.pack(pady=5)

        # Add an Auto-Copy toggle button
        self.auto_copy = False
        toggle_button = tk.Button(self.root, text="Auto-Copy: OFF", command=self.toggle_auto_copy)
        self.style_button(toggle_button)
        toggle_button.pack(pady=5)

        # Back button
        back_button = tk.Button(self.root, text="←", command=self.back_callback, font=("Arial", 12), bg="lightgray")
        back_button.place(x=10, y=10)

    def copy_text(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.text_display.get("1.0", "end-1c"))
        self.root.update()  # Keeps the clipboard content

    def toggle_auto_copy(self):
        self.auto_copy = not self.auto_copy
        toggle_button_text = "Auto-Copy: ON" if self.auto_copy else "Auto-Copy: OFF"
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button) and "Auto-Copy" in widget.cget("text"):
                widget.config(text=toggle_button_text)