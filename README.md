# Limkokwing Library API

A simple, efficient, and secure API for the Limkokwing University library system. This project allows library staff and users to search for books, borrow and return books, and track overdue books with fines.

## Features

- **Search Books** – Search by title, author, or category
- **Borrow Books** – Borrow available books with automatic due date calculation
- **Return Books** – Return books with automatic fine calculation for overdue items
- **Overdue Tracking** – View all overdue books and accumulated fines
- **Concurrent Access** – Asynchronous design supports multiple simultaneous users

## Tech Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Server:** Uvicorn (ASGI)
- **Validation:** Pydantic

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/GraceD4n/limkokwing-library-api.git
   cd limkokwing-library-api
   ```

2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

Start the API server with:
```bash
python main.py
```

You should see output like:
```
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

The API is now live at `http://localhost:8000`.

Open the interactive Swagger docs at: **http://localhost:8000/docs**

## Stopping the Server

To stop the running server, press **`Ctrl + C`** in the terminal where the server is running. You will see:
```
INFO:     Shutting down
INFO:     Finished server process [xxxx]
```

## Testing the API

You can test the endpoints using any of these methods:

### 1. Swagger UI (Recommended)
Open **http://localhost:8000/docs** in your browser. Click on any endpoint, then click **"Try it out"** to send test requests directly from the browser.

### 2. Using curl (Terminal)
```bash
# Get all books
curl http://localhost:8000/books

# Search books by author
curl "http://localhost:8000/books?author=Ishmael Beah"

# Search books by category
curl "http://localhost:8000/books?category=Fiction"

# Borrow a book (user 1 borrows book 3)
curl -X POST http://localhost:8000/borrow -H "Content-Type: application/json" -d "{\"user_id\": 1, \"book_id\": 3}"

# Return a book
curl -X POST http://localhost:8000/return -H "Content-Type: application/json" -d "{\"user_id\": 1, \"book_id\": 3}"

# Check overdue books
curl http://localhost:8000/overdue

# Get available books
curl http://localhost:8000/books/available
```

### 3. Using a browser
For GET endpoints, simply paste the URL into your browser:
- http://localhost:8000/books
- http://localhost:8000/books?title=Radical
- http://localhost:8000/books/available
- http://localhost:8000/overdue

## API Endpoints

| Method | Endpoint          | Description                          |
|--------|-------------------|--------------------------------------|
| GET    | `/books`          | Search books by title, author, or category |
| POST   | `/borrow`         | Borrow a book                        |
| POST   | `/return`         | Return a borrowed book               |
| GET    | `/overdue`        | Get all overdue books and fines      |
| GET    | `/books/available`| Get all currently available books    |

## Example Usage

### Search for books by author:
```
GET /books?author=Aminatta Forna
```

### Borrow a book:
```json
POST /borrow
{
    "user_id": 1,
    "book_id": 3
}
```

### Return a book:
```json
POST /return
{
    "user_id": 1,
    "book_id": 3
}
```

## Troubleshooting

- **Port already in use:** If port 8000 is occupied, edit the last line of `main.py` to use a different port (e.g., `port=8001`).
- **Module not found:** Make sure you ran `pip install -r requirements.txt` first.
- **Python version:** This project requires Python 3.10 or higher.

## Author

Grace Daniella Sankoh
