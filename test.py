from main import ISO9660Reader
from tkinter import filedialog, simpledialog

class test:
    if __name__ == "__main__":
        iso_path = "iso/file.iso" # We can use this line of code if dont want to select iso file with the help of Gui
        print("Current Working Directory:", os.getcwd())
        print("Is file exists:", os.path.exists(iso_path))  # Check if the file exists
        
        # Create an instance of ISO9660Reader by selecting an ISO file with a GUI
        iso_reader = ISO9660Reader.select_iso_file()

        # Print volume descriptors
        iso_reader.print_volume_descriptor("Standard", iso_reader.read_volume_descriptor(16 * 2048))
        iso_reader.print_volume_descriptor("Joliet", iso_reader.read_volume_descriptor(17 * 2048))

        # List all files and directories in the root directory
        iso_reader.list_contents("")

        # List contents of a specific directory
        iso_reader.list_contents("path/to/your/directory")

        # Ask the user to select a file for extraction
        file_to_extract = ISO9660Reader.select_file()
        destination_folder = filedialog.askdirectory(title="Select Destination Folder")

        # Extract a file from the ISO to the specified destination
        iso_reader.extract_file(file_path=file_to_extract, destination=destination_folder)

        print(f"ISO Path: {iso_reader.iso_path}")
