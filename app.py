from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            publication_date TEXT NOT NULL,
            genre TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Route for displaying the page
@app.route('/')
def index():
    return render_template('index.html')

# API route for reading books (GET request)
@app.route('/books', methods=['GET'])
def get_books():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM books')
    books = c.fetchall()
    conn.close()

    # Convert query result to a list of dictionaries for easy JSONification
    books_list = [{"id": book[0], "title": book[1], "author": book[2], "publication_date": book[3], "genre": book[4]} for book in books]
    return jsonify(books_list)

# API route for creating a new book (POST request)
@app.route('/books', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    publication_date = request.form['publication_date']
    genre = request.form['genre']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO books (title, author, publication_date, genre) VALUES (?, ?, ?, ?)',
              (title, author, publication_date, genre))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

# API route for deleting a book (DELETE request)
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

# Run the app
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
