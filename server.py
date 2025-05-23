from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse

# In-memory data
books = []

class SimpleAPIHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/books"):
            parsed_path = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed_path.query)
            if "id" in query:
                try:
                    book_id = int(query["id"][0])
                    for book in books:
                        if book["id"] == book_id:
                            self._set_headers()
                            self.wfile.write(json.dumps(book).encode())
                            return
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Book not found"}).encode())
                except:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({"error": "Invalid ID"}).encode())
            else:
                self._set_headers()
                self.wfile.write(json.dumps(books).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def do_POST(self):
        if self.path == "/books":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            book = json.loads(post_data)
            books.append(book)
            self._set_headers(201)
            self.wfile.write(json.dumps({"message": "Book added"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def do_PUT(self):
        if self.path.startswith("/books"):
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            updated_book = json.loads(put_data)

            for i, book in enumerate(books):
                if book["id"] == updated_book["id"]:
                    books[i] = updated_book
                    self._set_headers()
                    self.wfile.write(json.dumps({"message": "Book updated"}).encode())
                    return
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Book not found"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def do_DELETE(self):
        if self.path.startswith("/books"):
            parsed_path = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed_path.query)
            if "id" in query:
                try:
                    book_id = int(query["id"][0])
                    for i, book in enumerate(books):
                        if book["id"] == book_id:
                            books.pop(i)
                            self._set_headers()
                            self.wfile.write(json.dumps({"message": "Book deleted"}).encode())
                            return
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": "Book not found"}).encode())
                except:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({"error": "Invalid ID"}).encode())
            else:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "ID is required"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

def run(server_class=HTTPServer, handler_class=SimpleAPIHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running at http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()



# USE POSTMAN

# GET — Retrieve books
# URL: http://localhost:8000/books

# Method: GET

# Description: Retrieves all books.

# Or to get a specific book by ID:

# URL: http://localhost:8000/books?id=1

# Method: GET

# Description: Retrieves book with ID = 1.

# ______________________________________________________

# POST — Add a new book
# URL: http://localhost:8000/books

# Method: POST

# Headers: Content-Type: application/json

# Body: (raw, JSON example)
# {
#   "id": 1,
#   "title": "Book Title",
#   "author": "Author Name"
# }

# ______________________________________________________

# PUT — Update an existing book
# URL: http://localhost:8000/books

# Method: PUT

# Headers: Content-Type: application/json

# Body: (raw, JSON example — make sure the id matches an existing book)
# {
#   "id": 1,
#   "title": "Updated Book Title",
#   "author": "Updated Author"
# }

# ______________________________________________________

# DELETE — Delete a book
# URL: http://localhost:8000/books?id=1

# Method: DELETE

# Description: Deletes the book with ID = 1.