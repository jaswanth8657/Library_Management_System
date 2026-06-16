import os
import datetime
from colorama import Fore, Style, init

# Initialize colorama to automatically reset console colors after print statements
init(autoreset=True)

# File names for persisting library books and issued books records
BOOKS_FILE = "books.txt"
ISSUED_FILE = "issued_books.txt"
# Predefined categories for books
CATEGORIES = ["Programming", "Fiction", "Science", "History", "Other"]


class Book:
    """
    Represents a book in the library system.
    """
    def __init__(self, title, category="General", due_date=None):
        self.title = title
        self.category = category
        self.due_date = due_date  # Format: YYYY-MM-DD string, only populated when issued

    def __str__(self):
        # Format string depending on whether it has a due date (issued or not)
        if self.due_date:
            return f"{self.title}|{self.category}|{self.due_date}"
        return f"{self.title}|{self.category}"

    def matches(self, query):
        """
        Checks if the book title or category contains the query substring (case-insensitive).
        """
        return query.lower() in self.title.lower() or query.lower() in self.category.lower()

    def is_equal(self, title):
        """
        Checks if the book title is exactly equal to the given title (case-insensitive).
        """
        return self.title.lower() == title.lower()


class Library:
    """
    Manages the library collection, coordinating the load, save, view, 
    search, issue, and return functions.
    """
    def __init__(self, books_file, issued_file):
        self.books_file = books_file
        self.issued_file = issued_file

    def _create_file_if_not_exists(self, filename):
        """Helper to create files automatically if they do not exist."""
        if not os.path.exists(filename):
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    pass
            except Exception as e:
                print(Fore.RED + f"[ERROR] Could not create file {filename}: {e}")

    def load_books_from_file(self, filename, is_issued=False):
        """
        Loads book titles and metadata from a given text file and returns a list of Book objects.
        """
        self._create_file_if_not_exists(filename)
        books = []
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split('|')
                        title = parts[0]
                        category = parts[1] if len(parts) > 1 else "General"
                        due_date = parts[2] if len(parts) > 2 else None
                        
                        # Populate a default due date for issued books if missing in legacy records
                        if is_issued and not due_date:
                            due_date = (datetime.date.today() + datetime.timedelta(days=14)).isoformat()
                            
                        books.append(Book(title, category, due_date))
        except FileNotFoundError:
            print(Fore.RED + f"[ERROR] File '{filename}' not found!")
        except Exception as e:
            print(Fore.RED + f"[ERROR] Unexpected error reading '{filename}': {e}")
        return books

    def save_books_to_file(self, filename, books):
        """
        Saves a list of Book objects to the specified text file.
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for book in books:
                    f.write(str(book) + '\n')
        except Exception as e:
            print(Fore.RED + f"[ERROR] Unexpected error saving to '{filename}': {e}")

    def add_book(self):
        """
        Prompts for a book title, displays category choices, and prompts the user to select one.
        Validates input, checks for duplicates, and saves the new book.
        """
        books = self.load_books_from_file(self.books_file)
        issued_books = self.load_books_from_file(self.issued_file, is_issued=True)
        
        book_name = input(Fore.WHITE + "Enter Book Name: ").strip()
        
        if not book_name:
            print(Fore.RED + "[ERROR] Book name cannot be empty!")
            return
            
        if any(b.is_equal(book_name) for b in books) or any(b.is_equal(book_name) for b in issued_books):
            print(Fore.RED + "[ERROR] Book is already issued!")
            return
            
        print(Fore.BLUE + "\nAvailable Categories:")
        for idx, category_name in enumerate(CATEGORIES, 1):
            print(Fore.YELLOW + f"{idx}. {category_name}")
            
        while True:
            choice = input(Fore.WHITE + f"Select Category (1-{len(CATEGORIES)}): ").strip()
            if not choice:
                category = "General"
                break
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(CATEGORIES):
                    category = CATEGORIES[choice_idx]
                    break
                else:
                    print(Fore.RED + f"[ERROR] Please enter a number between 1 and {len(CATEGORIES)}.")
            except ValueError:
                print(Fore.RED + f"[ERROR] Invalid choice. Please enter a valid number.")
                
        books.append(Book(book_name, category))
        self.save_books_to_file(self.books_file, books)
        print(Fore.GREEN + "[SUCCESS] Book Added Successfully!")

    def view_books(self):
        """
        Displays all available books from the library collection in a numbered list.
        """
        books = self.load_books_from_file(self.books_file)
        if not books:
            print(Fore.BLUE + "No available books in the library.")
            return
            
        print(Fore.BLUE + "Available Books:")
        for index, book in enumerate(books, 1):
            print(Fore.BLUE + f"{index}. {book.title} [Category: {book.category}] (Status: Available)")

    def search_book(self):
        """
        Searches for a book by title or category (case-insensitive substring) and displays status.
        """
        books = self.load_books_from_file(self.books_file)
        issued_books = self.load_books_from_file(self.issued_file, is_issued=True)
        
        query = input(Fore.WHITE + "Enter Book Name: ").strip()
        if not query:
            print(Fore.RED + "[ERROR] Search query cannot be empty!")
            return
            
        available_matches = [b for b in books if b.matches(query)]
        issued_matches = [b for b in issued_books if b.matches(query)]
        
        if not available_matches and not issued_matches:
            print(Fore.RED + "[ERROR] Book Not Found!")
            return
            
        print(Fore.BLUE + "\nBook Found:")
        for book in available_matches:
            print(Fore.GREEN + f"{book.title} [Category: {book.category}] (Status: Available)")
        for book in issued_matches:
            print(Fore.YELLOW + f"{book.title} [Category: {book.category}] (Status: Issued, Due Date: {book.due_date})")

    def issue_book(self):
        """
        Allows a user to borrow/issue a book.
        Calculates a due date (14 days from today), removes it from available, and saves to issued.
        """
        books = self.load_books_from_file(self.books_file)
        issued_books = self.load_books_from_file(self.issued_file, is_issued=True)
        
        book_name = input(Fore.WHITE + "Enter Book Name: ").strip()
        if not book_name:
            print(Fore.RED + "[ERROR] Book name cannot be empty!")
            return
            
        matching_available = [b for b in books if b.is_equal(book_name)]
        matching_issued = [b for b in issued_books if b.is_equal(book_name)]
        
        if matching_available:
            exact_book = matching_available[0]
            books.remove(exact_book)
            self.save_books_to_file(self.books_file, books)
            
            # Calculate due date: 14 days in the future
            due_date = (datetime.date.today() + datetime.timedelta(days=14)).isoformat()
            exact_book.due_date = due_date
            
            issued_books.append(exact_book)
            self.save_books_to_file(self.issued_file, issued_books)
            print(Fore.GREEN + f"[SUCCESS] Book Issued Successfully! Due Date: {due_date}")
        elif matching_issued:
            print(Fore.RED + "[ERROR] Book is already issued!")
        else:
            print(Fore.RED + "[ERROR] Book Not Found in available library records!")

    def return_book(self):
        """
        Allows a user to return an issued book.
        Removes it from the issued file, checks for overdue fines, and adds it back to available.
        """
        books = self.load_books_from_file(self.books_file)
        issued_books = self.load_books_from_file(self.issued_file, is_issued=True)
        
        book_name = input(Fore.WHITE + "Enter Book Name: ").strip()
        if not book_name:
            print(Fore.RED + "[ERROR] Book name cannot be empty!")
            return
            
        matching_issued = [b for b in issued_books if b.is_equal(book_name)]
        
        if matching_issued:
            exact_book = matching_issued[0]
            issued_books.remove(exact_book)
            self.save_books_to_file(self.issued_file, issued_books)
            
            # Fine Calculation (Default: $1.00 or 1 unit per day overdue)
            due_date_str = exact_book.due_date
            fine = 0
            days_overdue = 0
            if due_date_str:
                try:
                    due_date = datetime.date.fromisoformat(due_date_str)
                    today = datetime.date.today()
                    if today > due_date:
                        days_overdue = (today - due_date).days
                        fine = days_overdue * 1  # Fine calculation logic
                except ValueError:
                    pass  # Gracefully fall back if invalid date string format
            
            # Reset due date and move back to books list
            exact_book.due_date = None
            books.append(exact_book)
            self.save_books_to_file(self.books_file, books)
            
            print(Fore.GREEN + "[SUCCESS] Book Returned Successfully!")
            if fine > 0:
                print(Fore.RED + f"[LATE] Book was overdue by {days_overdue} day(s). Fine incurred: ${fine:.2f}")
            else:
                print(Fore.BLUE + "[INFO] Book returned on time. No fine incurred.")
        else:
            print(Fore.RED + "[ERROR] This book is not in the issued records!")


# Global Library System Instance
library_system = Library(BOOKS_FILE, ISSUED_FILE)

# Top-level global wrappers to satisfy standard function signature requirements
def load_books(filename):
    """Loads books from filename and returns a list of titles."""
    books_objs = library_system.load_books_from_file(filename)
    return [book.title for book in books_objs]

def save_books(filename, books):
    """Saves a list of book titles (strings) to filename, preserving category if existing."""
    existing_books = library_system.load_books_from_file(filename)
    existing_by_title = {b.title.lower(): b for b in existing_books}
    
    book_objs = []
    for title in books:
        title_lower = title.lower()
        if title_lower in existing_by_title:
            book_objs.append(existing_by_title[title_lower])
        else:
            book_objs.append(Book(title))
    library_system.save_books_to_file(filename, book_objs)

def add_book():
    """Wrapper function to add a book."""
    library_system.add_book()

def view_books():
    """Wrapper function to view books."""
    library_system.view_books()

def search_book():
    """Wrapper function to search a book."""
    library_system.search_book()

def issue_book():
    """Wrapper function to issue a book."""
    library_system.issue_book()

def return_book():
    """Wrapper function to return a book."""
    library_system.return_book()

def display_menu():
    """
    Displays the professional welcome message and menu options.
    """
    print()
    # Banner in CYAN
    print(Fore.CYAN + "=========================================")
    print(Fore.CYAN + "       LIBRARY MANAGEMENT SYSTEM         ")
    print(Fore.CYAN + "=========================================")
    # Menu Options in YELLOW
    print(Fore.YELLOW + "1. Add Book")
    print(Fore.YELLOW + "2. View Books")
    print(Fore.YELLOW + "3. Search Book")
    print(Fore.YELLOW + "4. Issue Book")
    print(Fore.YELLOW + "5. Return Book")
    print(Fore.YELLOW + "6. Exit")
    print(Fore.CYAN + "=========================================")

def main():
    """
    Main controller function that loops continuously, handles user selection,
    and catches standard/unexpected exceptions to prevent app crashes.
    """
    while True:
        try:
            display_menu()
            
            # Prompt choice in white
            choice = input(Fore.WHITE + "Enter Choice: ").strip()
            
            if choice == "1":
                add_book()
            elif choice == "2":
                view_books()
            elif choice == "3":
                search_book()
            elif choice == "4":
                issue_book()
            elif choice == "5":
                return_book()
            elif choice == "6":
                print(Fore.GREEN + "\nThank you for using the Library Management System. Goodbye!")
                break
            elif not choice:
                print(Fore.RED + "[ERROR] Choice cannot be empty. Please enter an option from 1 to 6.")
            else:
                print(Fore.RED + "[ERROR] Invalid choice. Please select an option between 1 and 6.")
                
        except ValueError as ve:
            print(Fore.RED + f"[ERROR] Value error: {ve}")
        except FileNotFoundError as fnfe:
            print(Fore.RED + f"[ERROR] File system error: {fnfe}")
        except KeyboardInterrupt:
            print(Fore.GREEN + "\n\nProgram interrupted. Exiting. Goodbye!")
            break
        except Exception as e:
            print(Fore.RED + f"[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
