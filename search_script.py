import argparse
import os
import sys
import re

def main():
    parser = argparse.ArgumentParser(description="Search for a regex pattern in files within a directory.")
    parser.add_argument("directory", help="The path to the search directory.")
    parser.add_argument("regex", help="The search regex pattern.")
    parser.add_argument("--exclude", help="An optional regex pattern to exclude file names.")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: The specified path '{args.directory}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    print("Searching for files...")
    for file_path in find_files(args.directory, args.exclude):
        result = read_file_content(file_path)
        if result["error"]:
            print(f"Failed to read {file_path}: {result['error']}")
        else:
            print(f"Successfully read {file_path}")

def read_file_content(file_path):
    """
    Reads a file's content, trying different encodings based on the OS.
    Returns a dictionary with content or an error message.
    """
    if sys.platform == "win32":
        encodings = ['windows-1251', 'cp866', 'utf-8']
    else:
        encodings = ['utf-8']

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return {"content": f.read(), "error": None}
        except UnicodeDecodeError:
            continue
        except PermissionError:
            return {"content": None, "error": "Permission denied"}
        except Exception as e:
            return {"content": None, "error": f"An unexpected error occurred: {e}"}
    
    return {"content": None, "error": "Failed to decode with available encodings"}


def find_files(directory, exclude_regex):
    """
    Recursively finds files in a directory that match the extension whitelist
    and do not match the exclusion regex.
    """
    allowed_extensions = ['.java', '.txt', '.sql', '.yaml', '.properties', '.md', '.gradle', '.py']
    
    for root, _, files in os.walk(directory):
        for filename in files:
            # Check extension
            if not any(filename.endswith(ext) for ext in allowed_extensions):
                continue

            # Check exclusion regex
            if exclude_regex and re.search(exclude_regex, filename):
                continue
            
            yield os.path.abspath(os.path.join(root, filename))


if __name__ == "__main__":
    main()
