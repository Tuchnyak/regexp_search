# Development Plan: Regex Search Script

This document outlines a step-by-step plan for creating the regex search script. It is broken down into phases and individual steps, each with a corresponding prompt for a code-generation LLM.

## Phase 1: Project Skeleton and Argument Parsing

- [x] **Step 1.1: Initial Setup and CLI Arguments**
  - Create the main script file.
  - Implement command-line argument parsing for the three required inputs.
  - Add basic validation for the existence of the main directory path.

```text
Create a Python script named `search_script.py`.
Inside this script, use the `argparse` module to set up command-line argument parsing.
The script must accept three arguments:
1. `directory`: The path to the search directory (required).
2. `regex`: The search regex pattern (required).
3. `--exclude` (optional): An optional regex pattern to exclude file names.

Add a basic check to ensure the `directory` path exists and is a directory. If not, print an error message to stderr and exit the script with a non-zero status code.
For now, in the main execution block, simply print the parsed arguments to confirm they are being received correctly.
```

## Phase 2: File Discovery and Filtering

- [x] **Step 2.1: Recursive File Traversal**
  - Build upon the previous step to walk the directory tree.
  - Implement the file extension whitelist.
  - Implement the file name exclusion logic.

```text
Modify the `search_script.py` from the previous step.
Define a constant list of allowed file extensions: `['.java', '.txt', '.sql', '.yaml', '.properties', '.md', '.gradle', '.py']`.
Create a function `find_files(directory, exclude_regex)` that takes the starting directory and the optional exclusion regex.
This function should:
1. Use `os.walk()` to recursively traverse the directory.
2. For each file found, check if its extension is in the allowed list.
3. If an `exclude_regex` is provided, also check if the file's name matches it. If it does, skip the file.
4. The function should yield the full, absolute path of each file that passes these filters.

In the main execution block, call this new function with the parsed arguments and loop through the results, printing each yielded file path. This will verify the traversal and filtering logic.
```

## Phase 3: File Content Reading and OS-Specific Encodings

- [ ] **Step 3.1: Implement Encoding-Aware File Reading**
  - Detect the host operating system.
  - Create a function that attempts to read a file's content using a sequence of encodings based on the OS.
  - Handle potential `PermissionError` and `UnicodeDecodeError` gracefully.

```text
Further modify `search_script.py`.
Create a new function `read_file_content(file_path)`. This function will encapsulate the logic for reading a file.
Inside this function:
1. Import the `sys` module to detect the operating system (`sys.platform`).
2. Define the encoding lists: `['windows-1251', 'cp866', 'utf-8']` for Windows (`'win32'`) and `['utf-8']` for others (Linux/macOS).
3. Loop through the appropriate list of encodings. For each encoding, attempt to open and read the entire content of the file at `file_path`.
4. Use a `try...except` block. If the file is read successfully, return a dictionary `{"content": file_content, "error": None}`.
5. If a `UnicodeDecodeError` occurs, continue to the next encoding.
6. If a `PermissionError` occurs, or if all encodings fail, return a dictionary indicating the failure, e.g., `{"content": None, "error": "Permission denied"}` or `{"content": None, "error": "Failed to decode"}`.

Update the main loop to call `read_file_content()` for each file path found. For now, just print a success or failure message based on the returned dictionary.
```

## Phase 4: Regex Searching and Result Aggregation

- [ ] **Step 4.1: Perform Regex Search and Store Results**
  - Integrate the `re` module to search file content.
  - Store successful matches in a dictionary.
  - Store any errors encountered during file processing in a list.

```text
Now, let's integrate the actual search logic into `search_script.py`.
In the main execution block, initialize two empty data structures before the loop: `results = {}` and `errors = []`.
Modify the main loop that iterates through the files:
1. For each file, call `read_file_content()`.
2. If the content was read successfully (no error):
   a. Use the `re` module to find all matches of the input `regex` pattern in the content. Use `re.findall()` with the `re.MULTILINE` flag to support multi-line patterns.
   b. If any matches are found, add an entry to the `results` dictionary where the key is the absolute file path and the value is the list of matches.
3. If there was an error reading the file:
   a. Append a dictionary `{"path": file_path, "reason": error_message}` to the `errors` list.

After the loop finishes, print the `results` dictionary and the `errors` list to the console to verify that data is being collected correctly.
```

## Phase 5: JSON Output Generation

- [ ] **Step 5.1: Generate Filename and Write JSON Report**
  - Create the logic for generating the timestamped and regex-based filename.
  - Write the aggregated results and errors to a JSON file in the specified format.
  - Handle the case where no matches are found and no errors occurred.

```text
This is the final implementation step for `search_script.py`. Let's wire up the JSON output.
1. Import the `datetime`, `json`, and `os` modules.
2. Create a helper function `sanitize_filename(text)` that takes a string and removes or replaces characters that are invalid for filenames. It should also truncate the string to 15 characters.
3. In the main block, after the file processing loop is complete, add the final logic:
   a. Check if both the `results` dictionary and the `errors` list are empty. If so, print "Поиск завершен. Совпадений не найдено." and exit.
   b. If there is data to report, construct the output filename using the pattern `YYYYMMDD_HHmm_result_<sanitized_regex>.json`. The file should be saved in the original search directory.
   c. Create a final dictionary for the JSON output: `{"results": results, "errors": errors}`.
   d. Write this dictionary to the generated JSON file path using `json.dump()` with an indent for readability.
   e. Print the final confirmation message to the console: `Работа завершена. Результаты сохранены в файл: [generated_filename]`.

Finally, add the specified console logging inside the main loop:
- Before reading a file: `print(f"Просмотр файла: {file_path}...")`
- After finding matches in a file: `print(f"Найдено совпадений: {len(matches)}")`
```
