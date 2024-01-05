import os
import tkinter as tk
from tkinter import filedialog
import struct

class ISO9660Reader:
    def __init__(self, iso_path):
        self.iso_path = iso_path
        self.SECTOR_SIZE = 2048

    def read_volume_descriptor(self, offset):
        try:
            with open(self.iso_path, 'rb') as iso_file:
                iso_file.seek(offset)
                raw_data = iso_file.read(struct.calcsize('>BB5s32sIHHHB32xQH'))
                print(f"Raw Data at Offset {offset}: {raw_data}")
                if len(raw_data) != struct.calcsize('>BB5s32sIHHHB32xQH'):
                    return None  # or raise specific exception

                descriptor = struct.unpack('>BB5s32sIHHHB32xQH', raw_data)
                print(f"Unpacked Descriptor: {descriptor}")
                return descriptor
        except struct.error as e:
            raise ValueError(f"Error reading volume descriptor at offset {offset}: {e}")
        except Exception as e:
            raise ValueError(f"An unexpected error occurred while reading volume descriptor: {e}")
    def parse_volume_descriptor(self):
        try:
            standard_extent = self.read_volume_descriptor(16 * self.SECTOR_SIZE)
            if standard_extent is None or len(standard_extent) < 9 or standard_extent[8] == 0:
                raise ValueError("Error: Unable to read a valid standard volume descriptor.")

            joliet_extent = self.read_volume_descriptor(17 * self.SECTOR_SIZE)
            print("Volume Descriptors:")
            print(f"Standard Extent: {standard_extent[8]}")
            print(f"Joliet Extent: {joliet_extent[8] if joliet_extent else 'N/A'}")

            if joliet_extent is None or len(joliet_extent) < 9:
                return standard_extent[8]
            else:
                return joliet_extent[8]
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise ValueError(f"An unexpected error occurred while parsing volume descriptor: {e}")

    def read_directory_record(self, offset):
        try:
            if offset is None:
                raise ValueError("Invalid offset. Volume descriptor might be missing or corrupted.")

            with open(self.iso_path, 'rb') as iso_file:
                iso_file.seek(offset)
                raw_data = iso_file.read(struct.calcsize('>BBB7sII7sBB32s'))
                print(f"Raw Data at Offset {offset}: {raw_data}")

                if len(raw_data) != struct.calcsize('>BBB7sII7sBB32s'):
                    return None  # or raise specific exception

                record = struct.unpack('>BBB7sII7sBB32s', raw_data)
                return record
        except struct.error as e:
            raise ValueError(f"Error reading directory record at offset {offset}: {e}")
        except Exception as e:
            raise ValueError(f"An unexpected error occurred while reading directory record: {e}")

    def parse_directory(self, extent):
        records = []
        for offset in range(extent, extent + self.SECTOR_SIZE, self.SECTOR_SIZE):
            try:
                record = self.read_directory_record(offset)
                if record and None not in record:  # Skip records with None values
                    records.append(record)
            except Exception as e:
                # Log the exception and continue to the next record
                print(f"Error processing record at offset {offset}: {e}")
                pass  # Add this line to suppress the error message for skipped records

        return records

    def list_contents(self, path=None):
        root_extent = self.parse_volume_descriptor()
        records = self.parse_directory(root_extent)

        if path:
            # Handle both relative and absolute paths
            path = os.path.normpath(path)
            path = path.encode('utf-8')

            target_record = None
            for record in records:
                if record[7].decode('utf-8') == path:
                    target_record = record
                    break

            if not target_record:
                print(f"Error: Path '{os.fsdecode(path)}' not found.")
                return

            if target_record[1] & 0x02:
                # Directory
                directory_extent = target_record[10]
                directory_records = self.parse_directory(directory_extent)
                print(f"\nContents of directory '{os.fsdecode(path)}':")
                self.list_entries(directory_records, indent='  ')
            else:
                # File
                print(f"\nFile information for '{os.fsdecode(path)}':")
                print(f"    Size: {target_record[4]} bytes")
                print(f"    Data Extent: {target_record[10]}")
        else:
            # List all entries
            print("\nAll Files and Directories:")
            self.list_entries(records)

    def list_entries(self, records, indent=''):
        for record in records:
            if record[0] == 0x02:
                continue  # Skip hidden directories

            entry_name = os.fsdecode(record[7]).rstrip('\0')  # Remove trailing null characters
            entry_name_str = entry_name if isinstance(entry_name, str) else entry_name.decode('utf-8', 'ignore')

            if record[1] & 0x02:
                print(f"{indent}{entry_name_str} (directory)")
            else:
                print(f"{indent}{entry_name_str} (file)")

