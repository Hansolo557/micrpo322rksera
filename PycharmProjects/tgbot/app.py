from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

books = [
    {'id': 1, 'title': 'Nur', 'San Fra': 'iuwef 1'},
    {'id': 2, 'title': 'Jiue', 'Kisl Ji': 'eqrg 2'},
    {'id': 3, 'title': 'Nur', 'San Fra': 'iuwef 1'},
    {'id': 4, 'title': 'Jiue', 'Kisl Ji': 'eqrg 2'},
    {'id': 5, 'title': 'Nur', 'San Fra': 'iuwef 1'},
    {'id': 6, 'title': 'Jiue', 'Kisl Ji': 'eqrg 2'},
]

class BookList(Resource):
    def get(self):
        return {'books': books}

    def post(self):
        data = request.get_json()
        new_book = {'id': len(books) + 1, 'title': data['title'], 'author': data['author']}
        books.append(new_book)
        return {'book': new_book}, 201

class Book(Resource):
    def get(self, book_id):
        book = next((book for book in books if book['id'] == book_id), None)
        if book:
            return {'book': book}
        else:
            return {'message': 'Book not found'}, 404

    def put(self, book_id):
        book = next((book for book in books if book['id'] == book_id), None)
        if book:
            data = request.get_json()
            book['title'] = data['title']
            book['author'] = data['author']
            return {'book': book}
        else:
            return {'message': 'Book not found'}, 404

    def delete(self, book_id):
        global books
        books = [book for book in books if book['id'] != book_id]
        return {'message': 'Book deleted successfully'}

api.add_resource(BookList, '/books')
api.add_resource(Book, '/books/<int:book_id>')

if __name__ == '__main__':
    app.run(debug=True)
