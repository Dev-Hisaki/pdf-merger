import os
import re
import shutil
import sys
import time
from PIL import Image

def clear_console():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def sanitize_filename(filename):
    """Remove or replace invalid characters in a filename."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def ensure_export_folder():
    """Ensure the export folder exists or create it."""
    export_folder = os.path.join(os.getcwd(), "export")
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    return export_folder

def check_existing_pdf(folder_name, export_folder):
    """Check if PDF version already exists."""
    sanitized_name = sanitize_filename(folder_name)
    pdf_path = os.path.join(export_folder, f"{sanitized_name}.pdf")
    return pdf_path if os.path.exists(pdf_path) else None

def confirm_action(prompt):
    """Generic confirmation prompt."""
    while True:
        choice = input(f"\n{prompt} (y/n): ").strip().lower()
        if choice in ('y', 'yes'):
            return True
        elif choice in ('n', 'no'):
            return False
        else:
            print("Please enter 'y' or 'n'")

def delete_source_folder(folder_path):
    """Safely delete the source folder after successful conversion."""
    if not confirm_action(f"Delete original folder '{os.path.basename(folder_path)}'?"):
        return False

    try:
        if os.path.isdir(folder_path):
            print(f"Deleting {folder_path}...")
            shutil.rmtree(folder_path)
            print("Folder deleted successfully")
            return True
    except Exception as e:
        print(f"\033[91mError deleting folder: {str(e)}\033[0m")
    return False

def notify_completion(success=True, filename=None, existing_pdf=None):
    """Display operation completion status."""
    clear_console()
    if existing_pdf:
        print("\n\033[93m⚠ PDF already exists! Operation canceled.\033[0m")
        print(f"Existing file: {os.path.abspath(existing_pdf)}")
    elif success and filename:
        print("\n\033[92m✓ Conversion completed successfully!\033[0m")
        print(f"PDF created: {os.path.basename(filename)}")
        print(f"Location: {os.path.abspath(filename)}")
    else:
        print("\n\033[91m✗ Conversion failed or no files were processed\033[0m")
    time.sleep(1.5)

def process_images(folder_path, export_folder):
    """Process images and create PDF."""
    folder_name = os.path.basename(folder_path.rstrip(os.sep))
    sanitized_name = sanitize_filename(folder_name)
    output_path = os.path.join(export_folder, f"{sanitized_name}.pdf")
    
    existing_pdf = check_existing_pdf(folder_name, export_folder)
    if existing_pdf:
        return None, existing_pdf
    
    image_files = [
        os.path.join(folder_path, f) for f in sorted(os.listdir(folder_path))
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ]
    
    if not image_files:
        return None, None
    
    try:
        images = [Image.open(img).convert('RGB') for img in image_files]
        images[0].save(output_path, save_all=True, append_images=images[1:], quality=100)
        return output_path, None
    except Exception as e:
        print(f"\n\033[91mError: {str(e)}\033[0m")
        return None, None

def show_menu():
    """Display main menu options."""
    print("\n" + "═"*50)
    print(" "*20 + "\033[1mMAIN MENU\033[0m")
    print("═"*50)
    print("1. Convert images to PDF")
    print("2. Delete processed folders")
    print("3. Exit program")
    print("═"*50)

def main():
    clear_console()
    export_folder = ensure_export_folder()
    processed_folders = set()
    
    while True:
        show_menu()
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            clear_console()
            print("\n=== IMAGE TO PDF CONVERSION ===")
            target_folder = input("\nEnter folder path containing images: ").strip()
            
            if not os.path.isdir(target_folder):
                print("\033[91mError: Invalid directory path\033[0m")
                time.sleep(1)
                continue
                
            print("\nProcessing...", end='', flush=True)
            spinner = ['|', '/', '-', '\\']
            for i in range(15):
                time.sleep(0.1)
                print(f"\rProcessing... {spinner[i % 4]}", end='', flush=True)
                
            result, existing = process_images(target_folder, export_folder)
            notify_completion(bool(result), result, existing)
            
            if result and confirm_action("Keep original image folder?"):
                processed_folders.add(target_folder)
            elif result:
                if delete_source_folder(target_folder):
                    processed_folders.discard(target_folder)
            
        elif choice == '2':
            clear_console()
            if not processed_folders:
                print("\n\033[93mNo folders marked for deletion\033[0m")
                time.sleep(1)
                continue
                
            print("\n=== FOLDER CLEANUP ===")
            print("Folders pending deletion:")
            for idx, folder in enumerate(processed_folders, 1):
                print(f"{idx}. {folder}")
            
            if confirm_action("Proceed with deletion of all listed folders?"):
                for folder in list(processed_folders):
                    if delete_source_folder(folder):
                        processed_folders.remove(folder)
        
        elif choice == '3':
            if confirm_exit():
                break
        
        else:
            print("\033[91mInvalid choice. Please try again.\033[0m")
            time.sleep(0.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\033[91mFatal error: {str(e)}\033[0m")
        sys.exit(1)
