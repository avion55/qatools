import tkinter as tk
from tkinter import filedialog
import json
import pandas as pd

class AlbumMenu:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.packs = []

    def show(self):
        # Clear current widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Upload button
        tk.Button(self.root, text="Upload", command=self.upload_file, bg="green", fg="white").pack(pady=10)

        # Save button
        tk.Button(self.root, text="Save", command=self.save_packs, bg="blue", fg="white").pack(pady=10)

        # Back button
        tk.Button(self.root, text="Back", command=self.back_callback, bg="red", fg="white").pack(pady=10)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                df = pd.read_excel(file_path)
                if all(col in df.columns for col in ["Pack Key", "Draw Order", "Highest rarity type (Visual)", "Highest rarity amount (Visual)", "Sticker Type UI", "Pack UI"]):
                    self.packs = df["Pack Key"].tolist()
                    with open("packs.json", "w") as file:
                        json.dump(self.packs, file, indent=4)
                    print("Packs loaded successfully.")
                else:
                    print("Invalid file format. Missing required columns.")
            except Exception as e:
                print(f"Error reading file: {e}")

    def save_packs(self):
        # Placeholder for saving filtered packs logic
        print("Save functionality not yet implemented.")