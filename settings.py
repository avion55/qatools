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
        tk.Button(self.root, text="Back", command=self.back_callback, bg="blue", fg="white").pack(pady=20)

        # Add Resource Manager button
        tk.Button(self.root, text="Resource Manager", command=self.open_resource_manager, height=2).pack(pady=10)

    def open_resource_manager(self):
        if not hasattr(self, 'resource_manager'):
            from resource_manager import ResourceManager
            self.resource_manager = ResourceManager(self.root, self.show)
        self.resource_manager.create_ui()