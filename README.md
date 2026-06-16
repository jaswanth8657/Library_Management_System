# Library Management System

A terminal-based **Library Management System** built with Python using Object-Oriented Programming (OOP). The system manages library inventory, tracks book categories, handles due dates, calculates late return fines, and persists all transaction states using local files.

---

## Architecture (OOP Design)
The project is built on solid Object-Oriented Programming principles:
- **`Book` Class**: Encapsulates a book's properties (title, category, and due date) and provides case-insensitive search matching and exact duplicate verification.
- **`Library` Class**: Coordinates library operations (adding, listing, searching, issuing, and returning books) and manages file operations (`books.txt` and `issued_books.txt`).
- **Global Wrapper API**: Maintains top-level functions (`add_book`, `view_books`, etc.) that act as wrappers for the active `Library` instance, guaranteeing zero integration breakage with existing automated scripts or test runners.

---

## Features

1. **Welcome Message**: Displays a professional welcome banner in Cyan on startup.
2. **Add Book with Category Selection**:
   - Prompts for a book title and lets the user select from a predefined list of categories (`Programming`, `Fiction`, `Science`, `History`, `Other`).
   - If the book name is already present in either available or issued lists, it blocks addition and prints `[ERROR] Book is already issued!`.
3. **View Books & Category Status**: Displays a numbered list of all available books in the library showing their category and `Available` status.
4. **Search Book**: Searches books (by title or category) case-insensitively, displaying matches and their current state (e.g. `Available` or `Issued` with its corresponding due date).
5. **Issue Book (Due Date Management)**:
   - Issues a book by removing it from the available list and transferring it to the issued list.
   - Automatically calculates and assigns a return deadline (14 days from today).
6. **Return Book & Fine Calculation**:
   - Moves the returned book back to the available list.
   - Calculates late returns based on the return deadline, charging a late fine of `$1.00` per day overdue.
7. **File Storage**: Persistent storage in pipe-delimited text format (`Title|Category` or `Title|Category|DueDate`) that automatically creates files if they are missing.
8. **Robust Error Handling**: Gracefully handles value parsing, missing files, and invalid choices without crashing.

---

## Color Scheme (via `colorama`)
To provide a premium console experience, the application uses a cohesive color scheme:
- **Banner / Separators**: Cyan (`Fore.CYAN`)
- **Menu & Selection Lists**: Yellow (`Fore.YELLOW`)
- **User Inputs / Prompts**: White (`Fore.WHITE`)
- **Success Messages**: Green (`Fore.GREEN`)
- **Error Messages / Late Fees**: Red (`Fore.RED`)
- **Information Messages**: Blue (`Fore.BLUE`)

---

## File Structure

```text
Library_Management_System/
│
├── library.py          # Refactored OOP application source code
├── books.txt           # File database storing available books (Title|Category)
├── issued_books.txt    # File database storing issued books (Title|Category|DueDate)
└── .gitignore          # Ignores byte-compiled python files and test output
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
2. Input choices and text when prompted.
3. Select option `6` to exit the program safely.
