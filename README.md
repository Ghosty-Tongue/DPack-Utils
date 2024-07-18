# DPack-Utils

DPack-Utils is a Python utility for unpacking DPack files, a format used for storing compressed data and files. It includes functionality to handle various types of DPack files and extract their contents into readable formats.

## Features

- **DPack Unpacking:** Supports unpacking of DPack files (`*.dpack` and `*.dpak`).
- **Magic Code Verification:** Validates DPack files using predefined magic codes.
- **XML Extraction:** Extracts XML-based DPack files as XML files.
- **Binary Data Handling:** Decompresses and extracts binary data sections from DPack files.
- **Recursive Unpacking:** Option to unpack all DPack files within a specified directory and its subdirectories.

## Requirements

- Python 3.x
- `lxml` library for XML parsing (`pip install lxml`)

## Usage

### Command Line Interface

#### Unpack a Single DPack File

```bash
python DPack.py <path_to_dpack_file>
```

Replace `<path_to_dpack_file>` with the path to your DPack file.

#### Unpack DPack Files in a Directory and Subdirectories

```bash
python DPack.py <path_to_directory>
```

Replace `<path_to_directory>` with the path to the directory containing DPack files.

### Example

```bash
python DPack.py /path/to/dpack_files
```

This command will unpack all DPack files in the specified directory and its subdirectories.

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **ByteArray.py:** The underlying binary data handling is based on the `ByteArray` class provided in `ByteArray.py`.
- **zlib:** Used for decompressing zlib-compressed data within DPack files.
