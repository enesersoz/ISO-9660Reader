# ISO9660 Reader in Python

This Python script provides a straightforward ISO9660 reader, enabling you to examine and extract information from ISO9660 CD/DVD image files. It includes functionalities for reading volume descriptors, parsing directories, listing contents, and extracting files from the ISO image.

## Requirements

- **Python Interpreter:**
  - Ensure you have Python installed to run this script.

- **Struct Module:**
  - The script relies on the struct module, which is part of the Python standard library.

## Usage

### Initialization:

Provide the path to your ISO9660 file when creating an instance of the `ISO9660Reader` class.

### Print Volume Descriptors:

Display information about the standard and Joliet volume descriptors.

### List Contents:

List all files and directories in the root directory or specify a path to list its contents.

### Extract File:

Extract a specific file from the ISO image to a specified destination.

### Print ISO Path:

Display the path of the loaded ISO file.

## Note

- The script utilizes the struct module to unpack binary data from the ISO file.
- Ensure that the specified ISO file path is accurate, and the file exists.
- The script supports both standard and Joliet extensions.

## Example

Feel free to customize and enhance the script according to your specific needs. If you encounter any issues or have suggestions for improvement, please open an issue or contribute to the development. Your feedback is highly appreciated!
