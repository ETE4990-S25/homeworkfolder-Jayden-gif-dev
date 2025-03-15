import os
import hashlib
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_hash(file_path):
    """
    Calculate the SHA-256 hash of a file.
    """
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):  # Read in chunks
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        logging.error(f"Error hashing {file_path}: {e}")
        return None

def scan_directory(directory):
    """
    Scans a directory and calculates the hash for each file.
    """
    file_hashes = {}
    total_files = 0

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_hash(file_path)

            if file_hash:
                if file_hash in file_hashes:
                    file_hashes[file_hash].append(file_path)
                else:
                    file_hashes[file_hash] = [file_path]

            total_files += 1
            if total_files % 100 == 0:
                print(f"Scanned {total_files} files...")  # Progress update

    # Extract only the duplicate files
    duplicates = {hash_val: paths for hash_val, paths in file_hashes.items() if len(paths) > 1}
    return duplicates

def display_results(duplicates):
    """
    Displays the duplicate files found.
    """
    if duplicates:
        print("\nDuplicate Files Found:")
        for hash_val, paths in duplicates.items():
            print(f"\nSHA-256 Hash: {hash_val}")
            for path in paths:
                print(f"  - {path}")
    else:
        print("No duplicate files found.")

def menu():
    """
    Provides a menu-based UI for the user.
    """
    while True:
        print("\nDuplicate File Finder")
        print("1. Search for duplicate files")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            directory = input("Enter the directory to search: ").strip()
            if os.path.isdir(directory):
                print("\nScanning for duplicate files...\n")
                duplicates = scan_directory(directory)
                display_results(duplicates)
            else:
                print("Invalid directory. Please try again.")
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    menu()
