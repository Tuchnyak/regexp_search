import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Search for a regex pattern in files within a directory.")
    parser.add_argument("directory", help="The path to the search directory.")
    parser.add_argument("regex", help="The search regex pattern.")
    parser.add_argument("--exclude", help="An optional regex pattern to exclude file names.")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: The specified path '{args.directory}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    print("Parsed arguments:")
    print(f"  Directory: {args.directory}")
    print(f"  Regex: {args.regex}")
    print(f"  Exclude pattern: {args.exclude}")

if __name__ == "__main__":
    main()
