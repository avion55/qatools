import tkinter as tk

class SettingsMenu:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

    def show(self):
        # Clear current widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create Settings Menu buttons
        tk.Button(self.root, text="←", command=self.back_callback, font=("Arial", 12), bg="lightgray").place(x=10, y=10)

    def open_resource_manager(self):
        from resource_manager import ResourceManager
        resource_manager = ResourceManager(self.root, self.show)
        resource_manager.create_ui()