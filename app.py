from flask import Flask, render_template, request, redirect, url_for
from models import db, Book

app = Flask(__name__)

app.config['SECRET_KEY'] = 'library-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('books'))

@app.route('/books')
def books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        quantity = request.form['quantity']

        book = Book(
            title=title,
            author=author,
            quantity=int(quantity)
        )

        db.session.add(book)
        db.session.commit()

        return redirect('/books')

    return render_template('add_book.html')

@app.route('/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)

    db.session.delete(book)
    db.session.commit()

    return redirect('/books')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
