import streamlit as st
import json
import os

# Apply custom styles
st.markdown("""
    <style>
        .stButton>button {
            background-color: #007BFF !important;
            color: white !important;
            border-radius: 5px;
            padding: 10px;
            width: 100% !important;
        }
        .stButton>button:hover {
            background-color: #0056b3 !important;
        }
    </style>
""", unsafe_allow_html=True)

class LibraryManager:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.library = self.load_library()

    def load_library(self):
        """Load library data from JSON file or create a new one if it doesn't exist."""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_library(self):
        """Save the updated library data to JSON file."""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.library, file, indent=4, ensure_ascii=False)

    def add_book(self, title, author, year, genre, read_status):
        """Add a new book to the library."""
        if not title or not author:
            st.error("Title and Author cannot be empty!")
            return
        
        self.library.append({
            "title": title.strip(),
            "author": author.strip(),
            "year": int(year),
            "genre": genre.strip(),
            "read": read_status
        })
        self.save_library()
        st.success(f"✅ Book **{title}** added successfully!")

    def remove_book(self, title):
        """Remove a book by title."""
        initial_count = len(self.library)
        self.library = [book for book in self.library if book["title"].lower() != title.lower()]
        self.save_library()
        
        if len(self.library) < initial_count:
            st.success(f"❌ Book **{title}** removed successfully!")
        else:
            st.warning(f"⚠️ Book **{title}** not found in the library.")

    def search_books(self, query):
        """Search for books by title or author."""
        return [book for book in self.library if query.lower() in book["title"].lower() or query.lower() in book["author"].lower()]

    def display_statistics(self):
        """Show total books and percentage of read books."""
        total_books = len(self.library)
        read_books = sum(1 for book in self.library if book["read"])
        percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
        return total_books, percentage_read

manager = LibraryManager()

# App Title
st.title("📚 Personal Library Manager")

# Sidebar Menu
menu = st.sidebar.radio("Menu", ["Add Book", "Remove Book", "Search Books", "Display All Books", "Statistics"])

# --- Add a New Book ---
if menu == "Add Book":
    st.header("📖 Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, step=1, value=2024)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Have you read this book?")
    
    if st.button("➕ Add Book"):
        manager.add_book(title, author, year, genre, read_status)

# --- Remove a Book ---
elif menu == "Remove Book":
    st.header("❌ Remove a Book")
    title = st.text_input("Enter the title of the book to remove")
    
    if st.button("🗑 Remove Book"):
        manager.remove_book(title)

# --- Search Books ---
elif menu == "Search Books":
    st.header("🔍 Search for a Book")
    query = st.text_input("Enter title or author")
    
    if st.button("🔎 Search"):
        results = manager.search_books(query)
        
        if results:
            for book in results:
                st.subheader(f"📖 {book['title']}")
                st.write(f"**Author:** {book['author']}")
                st.write(f"**Year:** {book['year']}")
                st.write(f"**Genre:** {book['genre']}")
                st.write(f"**Status:** {'✅ Read' if book['read'] else '❌ Unread'}")
                st.markdown("---")
        else:
            st.warning("⚠️ No matching books found.")

# --- Display All Books ---
elif menu == "Display All Books":
    st.header("📚 Your Library")
    
    if not manager.library:
        st.warning("Your library is empty.")
    else:
        for book in manager.library:
            st.subheader(f"📖 {book['title']}")
            st.write(f"**Author:** {book['author']}")
            st.write(f"**Year:** {book['year']}")
            st.write(f"**Genre:** {book['genre']}")
            st.write(f"**Status:** {'✅ Read' if book['read'] else '❌ Unread'}")
            st.markdown("---")

# --- Library Statistics ---
elif menu == "Statistics":
    st.header("📊 Library Statistics")
    
    total_books, percentage_read = manager.display_statistics()
    
    st.write(f"**📚 Total Books:** {total_books}")
    st.write(f"**📖 Percentage Read:** {percentage_read:.2f}%")

st.markdown("---")
st.caption("🚀 Built with Streamlit - A Simple Personal Library Manager")
