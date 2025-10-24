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
        print(f"Found file: {file_path}")

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
