import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import csv
import os
import threading
import time

filename = "data_backup.csv"
backup_filename = "data_backup_autosave.csv"
backup_filename2 = "data_backup_autosave2.csv"

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
        
        self.data_history = []  
        self.current_data = ""  

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        self.text_area = scrolledtext.ScrolledText(self.main_frame, height=15, width=75)
        self.text_area.pack(pady=(0, 10))

        self.add_entry_button = tk.Button(self.main_frame, text="Add Entry", command=self.save_current_state)
        self.add_entry_button.pack(side=tk.LEFT, padx=(0, 10))

        self.undo_button = tk.Button(self.main_frame, text="Undo", command=self.undo_change)
        self.undo_button.pack(side=tk.LEFT, padx=(0, 10))

        self.save_button = tk.Button(self.main_frame, text="Save CSV", command=self.save_csv_and_txt)
        self.save_button.pack(side=tk.LEFT)

        self.autosave_interval = 30
        self.autosave_thread = threading.Thread(target=self.autosave_data, daemon=True)
        self.autosave_thread.start()

        self.status_message_area = scrolledtext.ScrolledText(self.main_frame, height=2, width=75)
        self.status_message_area.pack(pady=(10, 0))
        self.status_message_area.insert(tk.END, "Status messages will appear here.")
        self.status_message_area.config(state='disabled')

        self.load_existing_data()

    def update_status(self, message, display_in_main_text_area=False):
        """Update the status message area with the given message.
        
        Args:
            message (str): The message to display.
            display_in_main_text_area (bool): If True, display the message in the main text area.
        """
        if display_in_main_text_area:
            self.text_area.config(state='normal')
            self.text_area.insert(tk.END, f"\n{message}")  
            self.text_area.config(state='disabled')
        else:
            self.status_message_area.config(state='normal')
            self.status_message_area.delete('1.0', tk.END)
            self.status_message_area.insert('1.0', message)
            self.status_message_area.config(state='disabled')
            self.root.after(5000, lambda: self.status_message_area.delete('1.0', tk.END))


    def save_current_state(self):
        """Save the current state before adding new entry for undo functionality."""
        self.data_history.append(self.text_area.get('1.0', tk.END))
        self.update_status("Entry ready to be added.")

    def undo_change(self):
        """Undo the last entry based on significant action."""
        if self.data_history:
            last_state = self.data_history.pop()
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert('1.0', last_state)
            self.update_status("Last action undone successfully.")

    def autosave_data(self):
        """Periodically autosave the data to backup files for redundancy."""
        while True:
            content = self.text_area.get('1.0', tk.END).strip()
            lines = content.split('\n')
            csv_formatted_lines = [line.replace('\t', ',') for line in lines]

            for backup_file in [backup_filename, backup_filename2]:
                try:
                    with open(backup_file, 'w', newline='') as file:
                        file.writelines([line + '\n' for line in csv_formatted_lines])
                except Exception as e:
                    self.update_status(f"Error autosaving data: {e}", True)
            time.sleep(self.autosave_interval)

    def load_existing_data(self):
        """Load existing data from the backup file, if it exists."""
        load_filename = backup_filename if os.path.exists(backup_filename) else filename
        if os.path.exists(load_filename):
            with open(load_filename, 'r', newline='') as file:
                data = file.read()
                self.text_area.insert(tk.END, data)
                self.current_data = data

    def save_csv_and_txt(self):
        """Prompt the user for a file save location, then save the content to both CSV and TXT files."""
        content = self.text_area.get('1.0', tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "There is no content to save.")
            return

        export_filename_csv = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save CSV"
        )

        if not export_filename_csv:
            self.update_status("Save operation cancelled.", display_in_main_text_area=True)
            return

        export_filename_txt = export_filename_csv.rsplit('.', 1)[0] + ".txt"

        try:
            lines = content.split('\n')
            data_list = [line.split('\t') for line in lines if line]
            with open(export_filename_csv, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(data_list)

            with open(export_filename_txt, 'w', newline='') as txt_file:
                txt_file.write(content.replace('\t', ','))

            messagebox.showinfo("Success", "Data saved to CSV and TXT successfully.")
            self.update_status("Data saved to CSV and TXT successfully.", display_in_main_text_area=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save files: {e}")
            self.update_status(f"Failed to save files: {e}", display_in_main_text_area=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = OverScoutingApp(root)
    root.mainloop()
