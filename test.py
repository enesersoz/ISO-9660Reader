import os
import tkinter as tk
from tkinter import filedialog
from main import ISO9660Reader

class ISOExtractorGUI:

    def __init__(self, master):
        self.master = master
        self.master.title("ISO Extractor")

        # ISO file selection button
        self.iso_button = tk.Button(master, text="Choose ISO File", command=self.choose_iso_file)
        self.iso_button.pack(pady=10)

        # Destination folder selection button
        self.destination_button = tk.Button(master, text="Choose Destination Folder",
                                            command=self.choose_destination_folder)
        self.destination_button.pack(pady=10)

        # Extract button
        self.extract_button = tk.Button(master, text="Extract", command=self.extract)
        self.extract_button.pack(pady=10)

        # Label to display selected ISO file
        self.iso_label = tk.Label(master, text="")
        self.iso_label.pack()

        # Label to display selected destination folder
        self.destination_label = tk.Label(master, text="")
        self.destination_label.pack()

        # Create ISO9660Reader instance
        self.iso_reader = None
        self.destination_folder = None

    def choose_iso_file(self):
        iso_path = filedialog.askopenfilename(title="Select ISO File", filetypes=[("ISO files", "*.iso")])
        if iso_path:
            self.iso_label.config(text=f"Selected ISO Path: {iso_path}")
            self.iso_reader = ISO9660Reader(iso_path)

    def choose_destination_folder(self):
        destination_folder = filedialog.askdirectory(title="Select Destination Folder")
        if destination_folder:
            self.destination_label.config(text=f"Selected Destination Folder: {destination_folder}")
            self.destination_folder = destination_folder

    def extract(self):
        try:
            if self.iso_reader and self.destination_folder:
                print("Starting extraction process...")

                # Extract logic here
                root_extent = self.iso_reader.parse_volume_descriptor()
                records = self.iso_reader.parse_directory(root_extent)

                for i, record in enumerate(records, start=1):
                    print(f"\nProcessing record {i}...")
                    # Check if the record has the necessary elements
                    if len(record) >= 11 and record[4] is not None and record[6] is not None and record[
                        8] is not None and record[10] is not None:
                        print("Valid record found.")
                        # Use record[6] (Joliet) or record[8] (standard ISO) for the file path
                        entry_path = os.fsdecode(record[6] if record[6] else record[8]).strip('\0')
                        data_extent = record[10]

                        # Construct the full destination path for the entry
                        destination_path = os.path.join(self.destination_folder, entry_path)

                        # Create directories if they don't exist
                        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

                        # Extract the file data
                        with open(self.iso_reader.iso_path, 'rb') as iso_file:
                            iso_file.seek(data_extent)
                            data = iso_file.read(record[4])

                            # Write the data to the destination file
                            with open(destination_path, 'wb') as output_file:
                                output_file.write(data)

                        print(f"File '{entry_path}' extracted successfully to '{destination_path}'.")
                    else:
                        print(f"Skipping incomplete or invalid record {i}: {record}")

                print("Extraction process completed.")

            else:
                raise ValueError("Error: ISO file or destination folder not selected.")
        except Exception as e:
            print(f"An error occurred during extraction: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ISOExtractorGUI(root)
    root.mainloop()
