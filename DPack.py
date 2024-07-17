# DPack.py

from ByteArray import ByteArray
from pathlib import Path
from lxml import etree
import os, zlib, sys
import time

class DPackItem:
    def __init__(self, itemName: str, itemData: bytes):
        self.itemName = itemName
        self.itemData = itemData

class DPack:
    def __init__(self):
        self.magicCodes = [
            1146110283,  # DPack
            1836597052,  # XML
            1885433148  # XMC (XML)
        ]

        self.unpackDir = 'unpacked/'

        if not os.path.exists(self.unpackDir):
            os.mkdir(self.unpackDir)

    def unpack(self, file_path: str):
        data = zlib.decompress(open(file_path, 'rb').read())

        reader = ByteArray(data)

        magicCode = reader.readUnsignedInt()

        if magicCode not in self.magicCodes:
            raise Exception(f'Magic code invalid: {magicCode}!')

        # Extract the file name without the extension
        file_name = Path(file_path).stem

        # Create a subdirectory within 'unpacked/' using the file name
        unpack_subdir = os.path.join(self.unpackDir, file_name)
        os.makedirs(unpack_subdir, exist_ok=True)

        if magicCode in [self.magicCodes[1], self.magicCodes[2]]:
            # XML file
            root = etree.fromstring(reader.toByteArray())
            open(f"{unpack_subdir}/{file_name}.xml", "wb").write(etree.tostring(root, pretty_print=True))
            return

        numFiles = reader.readUnsignedShort()

        lengths = []

        for _ in range(numFiles):
            length = reader.readUnsignedInt()

            lengths.append(length)

        names = []

        for _ in range(numFiles):
            lengthBytes = reader.readUnsignedShort()

            name = reader.readMultiByte(lengthBytes)

            names.append(name)

        for i in range(numFiles):
            data = reader.readBytes(lengths[i])

            # Get the original directory path for the file
            original_dir_path, file_name_with_ext = os.path.split(names[i])

            # Create directories within 'unpack_subdir' if they exist in 'original_dir_path'
            file_dir = os.path.join(unpack_subdir, original_dir_path)
            os.makedirs(file_dir, exist_ok=True)

            with open(os.path.join(file_dir, file_name_with_ext), 'wb') as outDisk:
                print(f'Writing {names[i]} to disk!')
                outDisk.write(data)

if __name__ == "__main__":
    dPack = DPack()

    while True:
        user_input = input("Please provide the path to a DPack file or a folder containing DPack files (or 'exit' to quit, 'help' for instructions): ")

        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'help':
            print("To specify a DPack file location, provide the full path including the file extension (.dpack or .dpak).")
            print("To specify a folder location, provide the full path to the folder.")
            continue

        path = user_input.strip()

        def unpack_all_dpacks_in_folder(folder_path):
            dpack_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.dpack') or f.lower().endswith('.dpak')]
            for dpack_file in dpack_files:
                dpack_file_path = os.path.join(folder_path, dpack_file)
                try:
                    dPack.unpack(dpack_file_path)
                except Exception as e:
                    print(f"Error occurred while unpacking '{dpack_file}': {str(e)}")

            subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
            for subfolder in subfolders:
                subfolder_path = os.path.join(folder_path, subfolder)
                unpack_all_dpacks_in_folder(subfolder_path)

        if os.path.isfile(path):
            # Unpack a single DPack file
            if not (path.lower().endswith('.dpack') or path.lower().endswith('.dpak')):
                print("Invalid file extension. Please make sure the file has the .dpack or .dpak extension.")
                continue

            try:
                # Measure the start time
                start_time = time.time()

                dPack.unpack(path)

                # Measure the end time
                end_time = time.time()

                # Calculate the time taken for unpacking
                time_taken_seconds = end_time - start_time

                # Convert time taken to a human-readable format
                m, s = divmod(time_taken_seconds, 60)
                h, m = divmod(m, 60)
                time_taken_human_readable = f"{int(h)} hours, {int(m)} minutes, {int(s)} seconds"

                # Display a summary of what was unpacked and how long it took
                unpacked_files = os.listdir(dPack.unpackDir)
                print(f"\nUnpacked the following files:")
                for file in unpacked_files:
                    print(file)

                print(f"\nUnpacking took {time_taken_human_readable}.")

            except Exception as e:
                print(f"Error occurred: {str(e)}")
        elif os.path.isdir(path):
            # Unpack all DPack files in the folder and its subfolders
            dPack.unpackDir = 'unpacked/'
            unpack_all_dpacks_in_folder(path)
        else:
            print("Invalid input. Please provide the path to a DPack file or a folder containing DPack files.")