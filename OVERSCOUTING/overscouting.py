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

        self.ascii_art = """

                                                    _   _             
                                                   | | (_)            
             _____   _____ _ __ ___  ___ ___  _   _| |_ _ _ __   __ _ 
            / _ \ \ / / _ \ '__/ __|/ __/ _ \| | | | __| | '_ \ / _` |
           | (_) \ V /  __/ |  \__ \ (_| (_) | |_| | |_| | | | | (_| |
            \___/ \_/ \___|_|  |___/\___\___/ \__,_|\__|_|_| |_|\__, |
                                                                 __/ |
                                                                |___/ 
            by FIRST FRC Team Overture - 7421        
            
            Bienvenido a OverScouting, la herramienta de compilación de datos por QR.
            Agradecemos la aplicación de QRScout de Red Hawk Robotics 2713.                            
        """
        
        self.ascii_display = tk.Text(self.root, height=20, width=100)
        self.ascii_display.pack()
        self.ascii_display.insert(tk.END, self.ascii_art)
        self.ascii_display.config(state='disabled')
        
        self.data_history = []  # Stack for undo feature
        self.current_data = ""  # Keep track of the current data

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        self.text_area = scrolledtext.ScrolledText(self.main_frame, height=15, width=75)
        self.text_area.pack(pady=(0, 10))

        self.add_entry_button = tk.Button(self.main_frame, text="Add Entry", command=self.save_current_state)
        self.add_entry_button.pack(side=tk.LEFT, padx=(0, 10))

        self.undo_button = tk.Button(self.main_frame, text="Undo", command=self.undo_change)
        self.undo_button.pack(side=tk.LEFT, padx=(0, 10))

        self.save_button = tk.Button(self.main_frame, text="Save CSV", command=self.save_csv)
        self.save_button.pack(side=tk.LEFT)

        self.autosave_interval = 30  # Autosave every 30 seconds
        self.autosave_thread = threading.Thread(target=self.autosave_data, daemon=True)
        self.autosave_thread.start()

        self.load_existing_data()

    def save_current_state(self):
        """Save the current state before adding new entry for undo functionality."""
        self.data_history.append(self.text_area.get('1.0', tk.END))  # Save the current state
        # Add your logic here for handling the new entry if needed

    def undo_change(self):
        """Undo the last entry based on significant action."""
        if self.data_history:
            last_state = self.data_history.pop()
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert('1.0', last_state)

    def autosave_data(self):
        """Periodically autosave the data to a backup file, ensuring data is CSV-formatted."""
        while True:
            content = self.text_area.get('1.0', tk.END).strip()
            # Assuming TAB-separated data; replace '\t' with ',' if necessary
            lines = content.split('\n')
            csv_formatted_lines = [line.replace('\t', ',') for line in lines]

            with open(backup_filename, 'w', newline='') as file:
                for line in csv_formatted_lines:
                    file.write(line + '\n')
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
            with open(backup_filename, 'w', newline='') as backup_file:
                backup_file.write(content)

if __name__ == "__main__":
    root = tk.Tk()
    app = OverScoutingApp(root)
    root.mainloop()
