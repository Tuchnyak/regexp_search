# Regex Search Script

A cross-platform Python script for recursive text search using regular expressions in a specified directory.

## Features

- **Recursive directory traversal** - searches through all subdirectories
- **File type filtering** - processes only specific file extensions (configurable whitelist)
- **Regex pattern matching** - supports PCRE-compatible regular expressions including multi-line patterns
- **File exclusion** - optional regex pattern to exclude files by name
- **Smart encoding detection** - automatically detects file encoding based on OS:
  - Windows: tries `windows-1251`, `cp866`, `utf-8`
  - Linux/macOS: tries `utf-8`
- **Comprehensive error handling** - continues operation on non-fatal errors
- **JSON report generation** - saves results and errors in structured JSON format
- **Real-time progress output** - displays current file being processed and match counts

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Installation

Clone the repository or download the script:

```bash
git clone https://github.com/yourusername/regexp_search.git
cd regexp_search
```

## Usage

### Basic usage:

```bash
python search_script.py <directory_path> <search_regex> [--exclude <exclude_regex>]
```

### Arguments:

- `directory_path` (required) - Path to the directory to search in
- `search_regex` (required) - PCRE-compatible regular expression for text search
- `--exclude <exclude_regex>` (optional) - Regular expression to exclude files by name

### Examples:

Search for import statements in Java files:
```bash
python search_script.py /path/to/project "import\s+java\.util\.\w+"
```

Search for a pattern excluding log files:
```bash
python search_script.py /path/to/project "ERROR.*Exception" --exclude ".*\.log"
```

Search for multi-line patterns:
```bash
python search_script.py /path/to/project "class\s+\w+\s*{\s*public"
```

## Supported File Extensions

The script processes only files with the following extensions:
- `.java`
- `.txt`
- `.sql`
- `.yaml`
- `.properties`
- `.md`
- `.gradle`
- `.py`

## Output

### Console Output

During execution, the script displays:
- Current file being processed
- Number of matches found in each file
- Error messages for inaccessible files or encoding issues
- Final status message

### JSON Report

If matches are found or errors occur, a JSON report is generated in the search directory:

**Filename format:** `YYYYMMDD_HHmm_result_<first_15_chars_of_regex>.json`

**Structure:**
```json
{
  "results": {
    "/full/path/to/file1.txt": [
      "First match (can be multiline)",
      "Second match"
    ],
    "/full/path/to/file2.java": [
      "Single match in this file"
    ]
  },
  "errors": [
    {
      "path": "/full/path/to/inaccessible/folder",
      "reason": "Permission denied"
    },
    {
      "path": "/full/path/to/file_with_encoding_issue.txt",
      "reason": "Failed to decode with available encodings"
    }
  ]
}
```

## Error Handling

- **Fatal errors:** Invalid start directory causes immediate termination
- **Non-fatal errors:** File access or encoding errors are logged and the script continues
  - Permission denied errors
  - Encoding detection failures
  - Other file reading errors

## Development

### Project Structure

```
regexp_search/
├── search_script.py          # Main script
├── README.md                 # This file
├── .gitignore               # Git ignore configuration
├── 00_additional_context.md # Project context documentation
├── 01_spec.md               # Technical specification (Russian)
└── 02_prompt_plan.md        # Development plan
```

### Testing

The script can be tested with various scenarios:
1. Files with different encodings
2. Directories with restricted permissions
3. Multi-line pattern matching
4. File exclusion patterns
5. Empty directories and files

## License

This project is open source. Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.