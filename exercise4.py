import sqlite3

# Create a database and connect to it
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create Books table
cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
                    BookID INTEGER PRIMARY KEY,
                    Title TEXT,
                    Author TEXT,
                    ISBN TEXT,
                    Status TEXT)''')

# Create Users table
cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                    UserID INTEGER PRIMARY KEY,
                    Name TEXT,
                    Email TEXT)''')

# Create Reservations table
cursor.execute('''CREATE TABLE IF NOT EXISTS Reservations (
                    ReservationID INTEGER PRIMARY KEY,
                    BookID INTEGER,
                    UserID INTEGER,
                    ReservationDate TEXT,
                    FOREIGN KEY (BookID) REFERENCES Books (BookID),
                    FOREIGN KEY (UserID) REFERENCES Users (UserID))''')
# Function to add a new book to the database
def add_book():
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    isbn = input("Enter the ISBN of the book: ")
    status = input("Enter the status of the book: ")
    
    cursor.execute("INSERT INTO Books (Title, Author, ISBN, Status) VALUES (?, ?, ?, ?)", (title, author, isbn, status))
    conn.commit()
    print("Book added successfully!")

# Function to find a book's details based on BookID
def find_book_details():
    book_id = input("Enter the BookID: ")
    
    cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    book = cursor.fetchone()
    
    if book:
        print("BookID:", book[0])
        print("Title:", book[1])
        print("Author:", book[2])
        print("ISBN:", book[3])
        print("Status:", book[4])
        
        cursor.execute("SELECT * FROM Reservations WHERE BookID = ?", (book_id,))
        reservation = cursor.fetchone()
        
        if reservation:
            user_id = reservation[2]
            cursor.execute("SELECT * FROM Users WHERE UserID = ?", (user_id,))
            user = cursor.fetchone()
            
            print("Reservation Status: Reserved")
            print("Reserved By:")
            print("UserID:", user[0])
            print("Name:", user[1])
            print("Email:", user[2])
        else:
            print("Reservation Status: Not Reserved")
    else:
        print("Book not found!")

# Function to find a book's reservation status based on BookID, Title, UserID, and ReservationID
def find_reservation_status():
    text = input("Enter the BookID, Title, UserID, or ReservationID: ")
    
    if text.startswith("LB"):
        cursor.execute("SELECT * FROM Books WHERE BookID = ?", (text,))
        book = cursor.fetchone()
        
        if book:
            book_id = book[0]
            cursor.execute("SELECT * FROM Reservations WHERE BookID = ?", (book_id,))
            reservation = cursor.fetchone()
            
            if reservation:
                user_id = reservation[2]
                cursor.execute("SELECT * FROM Users WHERE UserID = ?", (user_id,))
                user = cursor.fetchone()
                
                print("Reservation Status: Reserved")
                print("Reserved By:")
                print("UserID:", user[0])
                print("Name:", user[1])
                print("Email:", user[2])
            else:
                print("Reservation Status: Not Reserved")
        else:
            print("Book not found!")
    elif text.startswith("LU"):
        cursor.execute("SELECT * FROM Users WHERE UserID = ?", (text,))
        user = cursor.fetchone()
        
        if user:
            user_id = user[0]
            cursor.execute("SELECT * FROM Reservations WHERE UserID = ?", (user_id,))
            reservation = cursor.fetchone()
            
            if reservation:
                book_id = reservation[1]
                cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
                book = cursor.fetchone()
                
                print("Reservation Status: Reserved")
                print("Reserved Book:")
                print("BookID:", book[0])
                print("Title:", book[1])
                print("Author:", book[2])
                print("ISBN:", book[3])
            else:
                print("Reservation Status: Not Reserved")
        else:
            print("User not found!")
    elif text.startswith("LR"):
        cursor.execute("SELECT * FROM Reservations WHERE ReservationID = ?", (text,))
        reservation = cursor.fetchone()
        
        if reservation:
            book_id = reservation[1]
            cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
            book = cursor.fetchone()
            
            user_id = reservation[2]
            cursor.execute("SELECT * FROM Users WHERE UserID = ?", (user_id,))
            user = cursor.fetchone()
            
            print("Reservation Status: Reserved")
            print("Reserved Book:")
            print("BookID:", book[0])
            print("Title:", book[1])
            print("Author:", book[2])
            print("ISBN:", book[3])
            print("Reserved By:")
            print("UserID:", user[0])
            print("Name:", user[1])
            print("Email:", user[2])
        else:
            print("Reservation not found!")
    else:
        print("Invalid input!")

# Function to find all the books in the database
def find_all_books():
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    
    if books:
        for book in books:
            print("BookID:", book[0])
            print("Title:", book[1])
            print("Author:", book[2])
            print("ISBN:", book[3])
            print("Status:", book[4])
            print()
    else:
        print("No books found!")

# Function to modify/update book details based on its BookID
def modify_book_details():
    book_id = input("Enter the BookID: ")
    
    cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    book = cursor.fetchone()
    
    if book:
        print("Current Book Details:")
        print("Title:", book[1])
        print("Author:", book[2])
        print("ISBN:", book[3])
        print("Status:", book[4])
        
        choice = input("What would you like to modify? (title/author/ISBN/status): ")
        
        if choice == "title":
            new_title = input("Enter the new title: ")
            cursor.execute("UPDATE Books SET Title = ? WHERE BookID = ?", (new_title, book_id))
            conn.commit()
            print("Book title updated successfully!")
        elif choice == "author":
            new_author = input("Enter the new author: ")
            cursor.execute("UPDATE Books SET Author = ? WHERE BookID = ?", (new_author, book_id))
            conn.commit()
            print("Book author updated successfully!")
        elif choice == "ISBN":
            new_isbn = input("Enter the new ISBN: ")
            cursor.execute("UPDATE Books SET ISBN = ? WHERE BookID = ?", (new_isbn, book_id))
            conn.commit()
            print("Book ISBN updated successfully!")
        elif choice == "status":
            new_status = input("Enter the new status: ")
            cursor.execute("UPDATE Books SET Status = ? WHERE BookID = ?", (new_status, book_id))
            cursor.execute("UPDATE Reservations SET ReservationStatus = ? WHERE BookID = ?", (new_status, book_id))
            conn