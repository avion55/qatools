import tkinter as tk

class SyntaxMenu:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

    def show(self):
        # Clear current widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create Syntax Menu buttons
        tk.Button(self.root, text="Syntax 1", height=2).pack(pady=10)
        tk.Button(self.root, text="Syntax 2", height=2).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.back_callback, bg="blue", fg="white").pack(pady=20)