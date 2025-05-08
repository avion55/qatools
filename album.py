import tkinter as tk
from tkinter import filedialog, messagebox
import json
import pandas as pd
import os
from PIL import Image, ImageTk

class AlbumMenu:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.packs = []

    def style_button(self, button):
        button.config(width=20, height=2, bg="lightblue", activebackground="blue", fg="black")

    def show(self):
        # Set the background for the album menu
        bg_image = Image.open("bg.png")
        resized_image = bg_image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.Resampling.LANCZOS)
        bg_image_tk = ImageTk.PhotoImage(resized_image)

        # Store the background image as an instance variable to prevent garbage collection
        self.bg_image_tk = bg_image_tk

        bg_label = tk.Label(self.root, image=bg_image_tk)
        bg_label.image = bg_image_tk  # Keep a reference to avoid garbage collection
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

        # Upload button
        upload_button = tk.Button(self.root, text="Upload", command=self.upload_file)
        self.style_button(upload_button)
        upload_button.pack(pady=10)

        # Save button
        save_button = tk.Button(self.root, text="Save", command=self.save_packs)
        self.style_button(save_button)
        save_button.pack(pady=10)

        # Filter button
        filter_button = tk.Button(self.root, text="Filter", command=self.filter_packs)
        self.style_button(filter_button)
        filter_button.pack(pady=10)

        # Clear Global Pack Keys button
        clear_button = tk.Button(self.root, text="Clear Global Pack Keys", command=self.clear_global_pack_keys)
        self.style_button(clear_button)
        clear_button.pack(pady=10)

        # Back button
        back_button = tk.Button(self.root, text="←", command=self.back_callback, font=("Arial", 12), bg="lightgray")
        back_button.place(x=10, y=10)

    def resize_background(self, bg_label):
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                df = pd.read_excel(file_path)
                if all(col in df.columns for col in ["Pack Key", "Draw Order", "Highest rarity type (Visual)", "Highest rarity amount (Visual)", "Sticker Type UI", "Pack UI"]):
                    # Convert the entire DataFrame to a dictionary grouped by column names
                    data_dict = {col: df[col].dropna().tolist() for col in df.columns}
                    self.packs = data_dict["Pack Key"]  # Update self.packs with "Pack Key" values
                    
                    # Save the entire data dictionary to JSON
                    with open("packs.json", "w") as file:
                        json.dump(data_dict, file, indent=4)
                    
                    print("Packs and data loaded successfully.")
                else:
                    print("Invalid file format. Missing required columns.")
            except Exception as e:
                print(f"Error reading file: {e}")

    def filter_packs(self):
        # Open a dialog to get filter criteria
        filter_window = tk.Toplevel(self.root)
        filter_window.title("Filter Packs")

        tk.Label(filter_window, text="Select Column:").grid(row=0, column=0, padx=10, pady=5)
        column_var = tk.StringVar(filter_window)
        column_var.set("")  # Default value
        columns = []  # Placeholder for dynamic column names

        # Load column names dynamically from packs.json
        try:
            with open("packs.json", "r") as file:
                packs_data = json.load(file)
                columns = [col for col in packs_data.keys() if col != "Pack Key" and col != "global_pack_key"]  # Exclude "Pack Key" and "global_pack_key"
        except Exception as e:
            print(f"Error loading columns: {e}")

        column_menu = tk.OptionMenu(filter_window, column_var, *columns)
        column_menu.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(filter_window, text="Select Value:").grid(row=1, column=0, padx=10, pady=5)
        value_var = tk.StringVar(filter_window)
        value_menu = tk.OptionMenu(value_var, "")  # Placeholder, will be updated dynamically
        value_menu.grid(row=1, column=1, padx=10, pady=5)

        def update_values(*args):
            selected_column = column_var.get()
            try:
                # Load the packs.json file
                with open("packs.json", "r") as file:
                    packs_data = json.load(file)

                # Extract unique values for the selected column, converting all values to strings
                unique_values = list(set(str(value) for value in packs_data.get(selected_column, [])))
                unique_values.sort()  # Sort for better usability

                # Update the value menu
                value_var.set("")  # Reset the selected value
                menu = value_menu["menu"]
                menu.delete(0, "end")
                for value in unique_values:
                    menu.add_command(label=value, command=lambda v=value: value_var.set(v))
            except Exception as e:
                print(f"Error updating values: {e}")

        column_var.trace("w", update_values)  # Update values when column selection changes

        def apply_filter():
            selected_column = column_var.get()
            selected_value = value_var.get()
            try:
                # Load the packs.json file
                with open("packs.json", "r") as file:
                    packs_data = json.load(file)

                # Ensure the selected column exists in the data
                if selected_column not in packs_data:
                    print(f"Column '{selected_column}' not found in data.")
                    return

                # Filter the Pack Key values based on the selected column and value
                filtered_packs = [
                    packs_data["Pack Key"][i]
                    for i in range(len(packs_data["Pack Key"]))
                    if i < len(packs_data[selected_column]) and str(packs_data[selected_column][i]) == selected_value
                ]

                # Save the filtered Pack Key values under global_pack_key in the JSON file
                packs_data["global_pack_key"] = filtered_packs
                with open("packs.json", "w") as file:
                    json.dump(packs_data, file, indent=4)

                print(f"Filtered packs saved under 'global_pack_key': {filtered_packs}")
                filter_window.destroy()
            except Exception as e:
                print(f"Error applying filter: {e}")

        tk.Button(filter_window, text="Apply", command=apply_filter, bg="green", fg="white").grid(row=2, column=0, columnspan=2, pady=10)

    def save_packs(self):
        if self.packs:
            try:
                # Filter out NaN values before saving
                valid_packs = [pack for pack in self.packs if pd.notna(pack)]
                with open("filtered_packs.json", "w") as file:
                    json.dump(valid_packs, file, indent=4)
                print("Filtered packs saved successfully.")
            except Exception as e:
                print(f"Error saving packs: {e}")
        else:
            print("No packs to save. Please upload and filter packs first.")

    def clear_global_pack_keys(self):
        try:
            if os.path.exists("packs.json"):
                with open("packs.json", "r+") as f:
                    data = json.load(f)
                    if "global_pack_key" in data:
                        data["global_pack_key"] = []
                        f.seek(0)
                        json.dump(data, f, indent=4)
                        f.truncate()
                messagebox.showinfo("Success", "Global pack keys cleared successfully.")
            else:
                messagebox.showwarning("Warning", "packs.json file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")