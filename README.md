# Image to PDF Converter

A Python utility that converts folders of images into PDF files with an interactive menu-driven interface.
Support for my other program bundledwebptojpg at https://github.com/Dev-Hisaki/bundledwebptojpg.git

## Features

- 📄 Convert multiple images (JPG, JPEG, PNG) to a single PDF file
- 🗂️ Automatic PDF naming based on folder name
- ✅ Duplicate detection to prevent overwriting existing PDFs
- 🗑️ Optional source folder deletion after conversion
- 🎨 Clean console interface with colored status messages
- 📁 Organized output in dedicated export folder

## Requirements

- Python 3.6 or higher
- Pillow (PIL) library

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/image-to-pdf-converter.git
cd image-to-pdf-converter
```

### 2. Install Dependencies

Install the required Python package using pip:

```bash
pip install Pillow
```

Or if you're using Python 3 specifically:

```bash
pip3 install Pillow
```

### Alternative: Using Requirements File

Create a `requirements.txt` file with:
```
Pillow>=10.0.0
```

Then install:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Program

```bash
python image_to_pdf.py
```

Or on some systems:
```bash
python3 image_to_pdf.py
```

### Main Menu Options

1. **Convert images to PDF**
   - Enter the path to a folder containing image files
   - Images will be sorted alphabetically and combined into a single PDF
   - Choose whether to keep or delete the original folder

2. **Delete processed folders**
   - View and delete folders that were previously marked for cleanup
   - Batch deletion of multiple processed folders

3. **Exit program**
   - Safely exit the application

### Supported Image Formats

- `.jpg`
- `.jpeg`
- `.png`

### Example Workflow

```
1. Run the program
2. Select option 1 (Convert images to PDF)
3. Enter folder path: /path/to/your/images
4. Wait for processing to complete
5. Choose whether to keep or delete the original folder
6. PDF will be created in the 'export' folder
```

## Output

- All PDFs are saved in an `export` folder created in the same directory as the script
- PDF files are named after the source folder (with invalid characters sanitized)
- If a PDF with the same name already exists, the conversion is canceled to prevent overwriting

## Error Handling

The program includes robust error handling for:
- Invalid directory paths
- Missing or corrupted image files
- File system permissions
- Duplicate PDF detection

## Notes

- Images are automatically converted to RGB format for PDF compatibility
- PDFs are created with maximum quality (quality=100)
- The program will not overwrite existing PDFs - you must manually delete or rename existing files first
- Original folder deletion requires explicit confirmation for safety

## Troubleshooting

**"ModuleNotFoundError: No module named 'PIL'"**
- Install Pillow: `pip install Pillow`

**"Error: Invalid directory path"**
- Ensure the folder path exists and is accessible
- Use absolute paths or correct relative paths

**"PDF already exists! Operation canceled"**
- Delete or rename the existing PDF in the export folder
- Or rename your source folder to generate a different output name

## License

This project is open source and available under the MIT License.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
