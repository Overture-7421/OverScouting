import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import csv
import os
import threading
import time

filename = "data_backup.csv"
backup_filename = "data_backup_autosave.csv"

class OverScoutingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OverScouting")

        self.data_history = []  # Stack for undo feature
        self.current_data = ""  # Keep track of the current data

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        self.text_area = scrolledtext.ScrolledText(self.main_frame, height=15, width=75)
        self.text_area.pack(pady=(0, 10))
        self.text_area.bind("<KeyRelease>", self.on_text_change)  # Bind text change event

        self.undo_button = tk.Button(self.main_frame, text="Undo", command=self.undo_change)
        self.undo_button.pack(side=tk.LEFT, padx=(0, 10))

        self.save_button = tk.Button(self.main_frame, text="Save CSV", command=self.save_csv)
        self.save_button.pack(side=tk.LEFT)

        self.autosave_interval = 30  # Autosave every 30 seconds
        self.autosave_thread = threading.Thread(target=self.autosave_data, daemon=True)
        self.autosave_thread.start()

        self.load_existing_data()

    def on_text_change(self, event=None):
        new_data = self.text_area.get('1.0', tk.END)
        if self.current_data != new_data:
            self.data_history.append(self.current_data)  # Save the previous state
            self.current_data = new_data  # Update current state

    def undo_change(self):
        if self.data_history:
            last_state = self.data_history.pop()
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert('1.0', last_state)
            self.current_data = last_state  # Update current state

    def autosave_data(self):
        """Periodically autosave the data to a backup file."""
        while True:
            with open(backup_filename, 'w', newline='') as file:
                file.write(self.text_area.get('1.0', tk.END))
            time.sleep(self.autosave_interval)

    def load_existing_data(self):
        """Load existing data from the backup file, if it exists."""
        load_filename = backup_filename if os.path.exists(backup_filename) else filename
        if os.path.exists(load_filename):
            with open(load_filename, 'r', newline='') as file:
                data = file.read()
                self.text_area.insert(tk.END, data)
                self.current_data = data

    def save_csv(self):
        """Parse the text area content and save it to a CSV file."""
        content = self.text_area.get('1.0', tk.END).strip()
        lines = content.split('\n')
        data_list = [line.split('\t') for line in lines if line]

        export_filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if export_filename:
            with open(export_filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data_list)
            messagebox.showinfo("Success", "Data saved to CSV successfully.")
            # After a successful save, backup file can be updated to reflect this state
            with open(backup_filename, 'w', newline='') as backup_file:
                backup_file.write(content)

if __name__ == "__main__":
    root = tk.Tk()
    app = OverScoutingApp(root)
    root.mainloop()
