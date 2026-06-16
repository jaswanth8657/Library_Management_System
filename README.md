# Library Management System

A terminal-based **Library Management System** built with Python that helps librarians and users manage book inventories and issue/return operations seamlessly.

## Features

1. **Welcome Message**: Displays a professional welcome banner when the program starts.
2. **Add Book**: Allows adding new books to the library (checks for empty names and duplicates, and saves them permanently).
3. **View Books**: Displays a numbered list of all available books in the library.
4. **Search Book**: Searches for books case-insensitively by title.
5. **Issue Book**: Issues a book by removing it from the available pool (`books.txt`) and logging it in the issued pool (`issued_books.txt`).
6. **Return Book**: Returns an issued book by removing it from the issued records and placing it back into the available pool.
7. **File Storage**: Fully persistent storage utilizing text files (`books.txt` and `issued_books.txt`) which are automatically generated if they don't exist.
8. **Robust Error Handling**: Gracefully handles `ValueError`, `FileNotFoundError`, empty entries, and invalid menu inputs without crashing.

---

## Color Scheme (via `colorama`)
To provide a premium and visually pleasing CLI experience, the application uses a cohesive color scheme:
- **Banner**: Cyan (`Fore.CYAN`)
- **Menu Options**: Yellow (`Fore.YELLOW`)
- **User Inputs / Prompts**: White (`Fore.WHITE`)
- **Success Messages**: Green (`Fore.GREEN`)
- **Error Messages**: Red (`Fore.RED`)
- **Information Messages**: Blue (`Fore.BLUE`)

---

## File Structure

```text
Library_Management_System/
│
├── library.py          # Complete application source code
├── books.txt           # Text file database of available books
└── issued_books.txt    # Text file database of issued books
```

---

## Installation & Setup

### 1. Prerequisites
Make sure you have **Python 3.x** installed. You will also need the `colorama` library for colored output.

### 2. Install Dependencies
Install the required dependency using pip:
```bash
pip install colorama
```

---

## How to Run

Execute the program from your terminal:
```bash
python library.py
```

### Usage Instructions
1. Run the script and navigate using the numbered menu options (`1` to `6`).
2. Input choice values when prompted.
3. To safely exit and save all records, select option `6`.
