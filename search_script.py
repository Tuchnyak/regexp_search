import argparse
import os
import sys
import re
import json
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(
        description="Search for a regex pattern in files within a directory."
    )
    parser.add_argument("directory", help="The path to the search directory.")
    parser.add_argument("regex", help="The search regex pattern.")
    parser.add_argument(
        "--exclude", help="An optional regex pattern to exclude file names."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(
            f"Error: The specified path '{args.directory}' is not a valid directory.",
            file=sys.stderr,
        )
        sys.exit(1)

    results = {}
    errors = []

    for file_path in find_files(args.directory, args.exclude):
        print(f"Просмотр файла: {file_path}...")
        result = read_file_content(file_path)
        if result["error"]:
            errors.append({"path": file_path, "reason": result["error"]})
            print(f"Ошибка при чтении файла: {result['error']}")
        else:
            try:
                matches = re.findall(args.regex, result["content"], re.MULTILINE)
                if matches:
                    results[file_path] = matches
                    print(f"Найдено совпадений: {len(matches)}")
            except re.error as e:
                print(f"Error: Invalid regex pattern: {e}", file=sys.stderr)
                sys.exit(1)

    # Check if there are any results or errors
    if not results and not errors:
        print("Поиск завершен. Совпадений не найдено.")
        sys.exit(0)

    # Generate output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    sanitized_regex = sanitize_filename(args.regex)
    output_filename = f"{timestamp}_result_{sanitized_regex}.json"
    output_path = os.path.join(args.directory, output_filename)

    # Create output data
    output_data = {"results": results, "errors": errors}

    # Write to JSON file
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"Работа завершена. Результаты сохранены в файл: {output_filename}")
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)


def read_file_content(file_path):
    """
    Reads a file's content, trying different encodings based on the OS.
    Returns a dictionary with content or an error message.
    """
    if sys.platform == "win32":
        encodings = ["windows-1251", "cp866", "utf-8"]
    else:
        encodings = ["utf-8"]

    for encoding in encodings:
        try:
            with open(file_path, "r", encoding=encoding) as f:
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
    allowed_extensions = [
        ".java",
        ".txt",
        ".sql",
        ".yaml",
        ".properties",
        ".md",
        ".gradle",
        ".py",
    ]

    for root, _, files in os.walk(directory):
        for filename in files:
            # Check extension
            if not any(filename.endswith(ext) for ext in allowed_extensions):
                continue

            # Check exclusion regex
            if exclude_regex and re.search(exclude_regex, filename):
                continue

            yield os.path.abspath(os.path.join(root, filename))


def sanitize_filename(text):
    """
    Sanitizes a string to be safe for use in a filename.
    Removes or replaces invalid characters and truncates to 15 characters.
    """
    # Replace common regex special characters and filesystem-unsafe characters
    safe_chars = []
    for char in text:
        if char.isalnum() or char in ("_", "-"):
            safe_chars.append(char)
        elif char in (
            " ",
            ".",
            "\\",
            "/",
            "|",
            "*",
            "?",
            "<",
            ">",
            ":",
            '"',
            "\n",
            "\r",
            "\t",
        ):
            safe_chars.append("_")
        else:
            safe_chars.append("_")

    result = "".join(safe_chars)

    # Remove leading/trailing underscores and collapse multiple underscores
    result = re.sub(r"_+", "_", result).strip("_")

    # Truncate to 15 characters
    if len(result) > 15:
        result = result[:15]

    # If result is empty or just underscores, use a default
    if not result or result == "_":
        result = "search"

    return result


if __name__ == "__main__":
    main()
