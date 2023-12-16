import struct
import os

class ISO9660Reader:
    def __init__(self, iso_path):
        self.iso_path = iso_path
        self.volume_descriptor_size = 2048
        self.joliet_supplementary_size = 2048

    def read_volume_descriptor(self, offset):
        with open(self.iso_path, 'rb') as iso_file:
            iso_file.seek(offset)
            raw_data = iso_file.read(struct.calcsize('>BB5s32sIHHHB32xQH'))
            descriptor = struct.unpack('>BB5s32sIHHHB32xQH', raw_data)
            return descriptor

    def parse_volume_descriptor(self):
        standard_extent = self.read_volume_descriptor(16 * 2048)[8]
        joliet_extent = self.read_volume_descriptor(17 * 2048)[8]

        print("Volume Descriptors:")
        print(f"Standard Extent: {standard_extent}")
        print(f"Joliet Extent: {joliet_extent}")

        if joliet_extent != 0:
            return joliet_extent
        else:
            return standard_extent

    def print_volume_descriptor(self, label, descriptor):
        """Print the details of a volume descriptor."""
        print(f"\n{label} Volume Descriptor:")
        print(f"  Type: {descriptor[0]}")
        print(f"  Identifier: {descriptor[1]}")

        # Decode System Identifier as ASCII
        try:
            system_identifier = descriptor[2].decode('ascii').rstrip()
            print(f"  System Identifier: {system_identifier}")
        except UnicodeDecodeError:
            print("  System Identifier: (Unable to decode as ASCII)")

        # Decode Volume Identifier as ASCII
        try:
            volume_identifier = descriptor[3].decode('ascii').rstrip()
            print(f"  Volume Identifier: {volume_identifier}")
        except UnicodeDecodeError:
            print("  Volume Identifier: (Unable to decode as ASCII)")

        # Handle Volume Set Identifier as an integer
        if len(descriptor) > 9:
            print(f"  Volume Set Identifier: {descriptor[9]}")

        # Check for the existence of the rest of the fields
        if len(descriptor) > 12:
            # Continue with the rest of the fields
            print(f"  Total LBA: {descriptor[4]}")
            print(f"  Block Size: {descriptor[5]}")
            print(f"  Path Table Size: {descriptor[6]}")
            print(f"  Path Table LBA: {descriptor[7]}")
            print(f"  Root Directory Record: {descriptor[8]}")
            print(f"  Volume Sequence Number: {descriptor[10]}")
            print(f"  Logical Block Size: {descriptor[11]}")
            print(f"  Path Table Size (Optional): {descriptor[12]}")
        else:
            print("  (Additional fields not available)")

    def read_directory_record(self, offset):
        with open(self.iso_path, 'rb') as iso_file:
            iso_file.seek(offset)
            raw_data = iso_file.read(struct.calcsize('>BBB7sII7sBB32s'))
            record = struct.unpack('>BBB7sII7sBB32s', raw_data)
            return record

    def parse_directory(self, extent):
        records = []
        current_offset = extent

        while True:
            record = self.read_directory_record(current_offset)
            if record[0] == 0:
                break  # Terminator record

            records.append(record)
            current_offset += record[8]

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

            entry_name = os.fsdecode(record[7]).strip('\0')
            if record[1] & 0x02:
                print(f"{indent}{entry_name} (directory)")
            else:
                print(f"{indent}{entry_name} (file)")

    def extract_file(self, file_path, destination=None):
        root_extent = self.parse_volume_descriptor()
        records = self.parse_directory(root_extent)

        for record in records:
            if os.fsdecode(record[7]) == file_path:
                if record[1] & 0x02:
                    print("Error: Specified path is a directory. Use 'list_contents' to view its contents.")
                    return
                else:
                    data_extent = record[10]

                    # Check if destination is specified
                    if destination:
                        destination = os.path.normpath(destination)
                        destination_path = os.path.join(destination, os.path.basename(file_path))
                        with open(destination_path, 'wb') as output_file:
                            with open(self.iso_path, 'rb') as iso_file:
                                iso_file.seek(data_extent)
                                data = iso_file.read(record[4])
                                output_file.write(data)
                        print(f"\nFile '{os.fsdecode(file_path)}' extracted successfully to '{destination_path}'.")
                        return
                    else:
                        # Print file data
                        with open(self.iso_path, 'rb') as iso_file:
                            iso_file.seek(data_extent)
                            data = iso_file.read(record[4])
                            print(f"\nFile '{os.fsdecode(file_path)}' content:")
                            print(data)
        print(f"Error: File '{os.fsdecode(file_path)}' not found.")

if __name__ == "__main__":
    iso_path = "/iso/file.iso"
    print("Current Working Directory:", os.getcwd())
    print("Is file exists:", os.path.exists(iso_path))  # Check if the file exists
    # Provide the full path to the ISO9660Reader constructor
    iso_reader = ISO9660Reader(iso_path)

    # Print volume descriptors
    iso_reader.print_volume_descriptor("Standard", iso_reader.read_volume_descriptor(16 * 2048))
    iso_reader.print_volume_descriptor("Joliet", iso_reader.read_volume_descriptor(17 * 2048))


    # Provide the full path to the ISO9660Reader constructor
    iso_reader = ISO9660Reader(iso_path)

    # List all files and directories in the root directory
    iso_reader.list_contents("")

    # List contents of a specific directory
    iso_reader.list_contents("path/to/your/directory")

    # Extract a file from the ISO to the current directory
    iso_reader.extract_file(file_path="path/inside/iso/file.txt",
                            destination="path/on/local/machine")

    print(f"ISO Path: {iso_reader.iso_path}")