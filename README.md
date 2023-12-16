SO9660 Reader

This Python script provides a basic ISO9660 reader that allows you to inspect and extract information from ISO9660 CD/DVD image files. It includes functionality to read volume descriptors, parse directories, list contents, and extract files from the ISO image.

Requirements

The script is written in Python and requires a Python interpreter to run.
Ensure the struct module is available, which is part of the Python standard library.


Usage
Initialization: Provide the path to your ISO9660 file when creating an instance of the ISO9660Reader class.

python
Copy code
iso_path = "/path/to/your/file.iso"
iso_reader = ISO9660Reader(iso_path)
Print Volume Descriptors: Display information about the standard and Joliet volume descriptors.

iso_reader.print_volume_descriptor("Standard", iso_reader.read_volume_descriptor(16 * 2048))
iso_reader.print_volume_descriptor("Joliet", iso_reader.read_volume_descriptor(17 * 2048))
List Contents: List all files and directories in the root directory or specify a path to list its contents.

python
Copy code
# List all entries in the root directory
iso_reader.list_contents("")

# List contents of a specific directory
iso_reader.list_contents("path/to/your/directory")
Extract File: Extract a specific file from the ISO image to a specified destination.

python
Copy code
iso_reader.extract_file(file_path="path/inside/iso/file.txt", destination="path/on/local/machine")
Print ISO Path:

python
Copy code
print(f"ISO Path: {iso_reader.iso_path}")
Note
The script uses the struct module to unpack binary data from the ISO file.
Ensure that the specified ISO file path is correct and the file exists.
The script supports both standard and Joliet extensions.
Example
python
Copy code
iso_path = "/path/to/your/file.iso"
iso_reader = ISO9660Reader(iso_path)

# Print volume descriptors
iso_reader.print_volume_descriptor("Standard", iso_reader.read_volume_descriptor(16 * 2048))
iso_reader.print_volume_descriptor("Joliet", iso_reader.read_volume_descriptor(17 * 2048))

# List all files and directories in the root directory
iso_reader.list_contents("")

# List contents of a specific directory
iso_reader.list_contents("path/to/your/directory")

# Extract a file from the ISO to the current directory
iso_reader.extract_file(file_path="path/inside/iso/file.txt", destination="path/on/local/machine")

print(f"ISO Path: {iso_reader.iso_path}")
Feel free to customize and enhance the script according to your specific needs. If you encounter any issues or have suggestions for improvement, please open an issue or contribute to the development.
