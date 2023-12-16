# ISO 9660 Reader

A simple Python script for reading and interacting with ISO 9660 file systems.

## Overview

This Python script, `main.py`, provides a class named `ISO9660Reader` that allows you to work with ISO 9660 file systems. The script utilizes the `tkinter` library to offer a graphical user interface (GUI) for selecting ISO files and performing various operations.

## Features

- Read and parse ISO 9660 volume descriptors.
- List all files and directories in the root directory or a specified directory.
- Extract a specified file from the ISO to a destination folder.

## How to Use

1. **Selecting an ISO File:**
   - Run the script using Python (`python main.py`).
   - A file dialog will prompt you to select an ISO file.

2. **Listing Contents:**
   - The script will display the volume descriptors, list the contents of the root directory, and provide an option to list contents of a specific directory.

3. **Extracting a File:**
   - You can choose to extract a file by providing the path to the file and selecting a destination folder.

## Requirements

- Python 3.x
- `tkinter` library (usually included with Python)

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/ISO-9660-Reader.git
cd ISO-9660-Reader
