"""
Basic API Structure with open-software
Limkokwing Library API
A FastAPI-based library management system that allows users to search for books,
borrow and return books, and track overdue books with fines.
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import asyncio

app = FastAPI(
    title="Limkokwing Library API",
    description="A simple, efficient, and secure API for the Limkokwing library system.",
    version="1.0.0"
)

# --- Data Models (Type Annotations) ---

class Book(BaseModel):
    id: int
    title: str
    author: str
    category: str
    available: bool = True

class BorrowRequest(BaseModel):
    user_id: int
    book_id: int

class ReturnRequest(BaseModel):
    user_id: int
    book_id: int

class BorrowRecord(BaseModel):
    user_id: int
    book_id: int
    borrow_date: datetime
    due_date: datetime
    returned: bool = False

# --- In-Memory Database ---

books_db: list[Book] = [
    Book(id=1, title="Radical Inclusion", author="David Moinina Sengeh", category="Leadership"),
    Book(id=2, title="The Memory of Love", author="Aminatta Forna", category="Fiction"),
    Book(id=3, title="The Last Harmattan of Alusine Dunbar", author="Syl Cheney-Coker", category="Fiction"),
    Book(id=4, title="The Gilded One", author="Namina Forna", category="Fantasy"),
    Book(id=5, title="Road to Freedom", author="Yema Lucilda Hunter", category="Historical Fiction"),
    Book(id=6, title="The Palm Oil Stain", author="Nadia Maddy", category="Fiction"),
    Book(id=7, title="Ancestor Stones", author="Aminatta Forna", category="Fiction"),
    Book(id=8, title="Radiance of Tomorrow", author="Ishmael Beah", category="Fiction"),
    Book(id=9, title="The Bite of the Mango", author="Mariatu Kamara", category="Non-Fiction"),
    Book(id=10, title="So the Path Does Not Die", author="Pede Holist", category="Fiction"),
    Book(id=11, title="A Long Way Gone", author="Ishmael Beah", category="Non-Fiction"),
    Book(id=12, title="The Devil That Danced on the Water", author="Aminatta Forna", category="Memoir"),
]

borrow_records: list[BorrowRecord] = []

LOAN_PERIOD_DAYS: int = 14
FINE_PER_DAY: float = 2.50


# --- Endpoint 1: Search Books ---

@app.get("/books", response_model=list[Book])
async def search_books(
    title: Optional[str] = Query(None, description="Search by book title"),
    author: Optional[str] = Query(None, description="Search by author name"),
    category: Optional[str] = Query(None, description="Search by category")
) -> list[Book]:
    """
    Search for books by title, author, or category.
    Returns all books if no search parameters are provided.
    """
    await asyncio.sleep(0.1)  # Simulate async database query

    results: list[Book] = books_db

    if title:
        results = [b for b in results if title.lower() in b.title.lower()]
    if author:
        results = [b for b in results if author.lower() in b.author.lower()]
    if category:
        results = [b for b in results if category.lower() in b.category.lower()]

    return results


# --- Endpoint 2: Borrow a Book ---

@app.post("/borrow")
async def borrow_book(request: BorrowRequest) -> dict:
    """
    Borrow a book from the library.
    Creates a borrow record with a 14-day loan period.
    """
    await asyncio.sleep(0.1)  # Simulate async processing

    book: Optional[Book] = None
    for b in books_db:
        if b.id == request.book_id:
            book = b
            break

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    if not book.available:
        raise HTTPException(status_code=400, detail="Book is currently not available")

    # Mark book as unavailable
    book.available = False

    # Create borrow record
    record = BorrowRecord(
        user_id=request.user_id,
        book_id=request.book_id,
        borrow_date=datetime.now(),
        due_date=datetime.now() + timedelta(days=LOAN_PERIOD_DAYS)
    )
    borrow_records.append(record)

    return {
        "message": f"Book '{book.title}' borrowed successfully",
        "due_date": record.due_date.strftime("%Y-%m-%d"),
        "user_id": request.user_id
    }


# --- Endpoint 3: Return a Book ---

@app.post("/return")
async def return_book(request: ReturnRequest) -> dict:
    """
    Return a borrowed book to the library.
    Calculates fines if the book is overdue.
    """
    await asyncio.sleep(0.1)  # Simulate async processing

    # Find the active borrow record
    record: Optional[BorrowRecord] = None
    for r in borrow_records:
        if r.user_id == request.user_id and r.book_id == request.book_id and not r.returned:
            record = r
            break

    if record is None:
        raise HTTPException(status_code=404, detail="No active borrow record found")

    # Mark as returned
    record.returned = True

    # Mark book as available again
    for book in books_db:
        if book.id == request.book_id:
            book.available = True
            break

    # Calculate fine if overdue
    fine: float = 0.0
    if datetime.now() > record.due_date:
        overdue_days: int = (datetime.now() - record.due_date).days
        fine = overdue_days * FINE_PER_DAY

    return {
        "message": "Book returned successfully",
        "fine": fine,
        "overdue": fine > 0
    }


# --- Endpoint 4: Get Overdue Books ---

@app.get("/overdue")
async def get_overdue_books() -> list[dict]:
    """
    Get a list of all overdue books along with calculated fines.
    """
    await asyncio.sleep(0.1)  # Simulate async database query

    overdue_list: list[dict] = []
    current_time: datetime = datetime.now()

    for record in borrow_records:
        if not record.returned and current_time > record.due_date:
            overdue_days: int = (current_time - record.due_date).days
            fine: float = overdue_days * FINE_PER_DAY

            # Find book title
            book_title: str = "Unknown"
            for book in books_db:
                if book.id == record.book_id:
                    book_title = book.title
                    break

            overdue_list.append({
                "user_id": record.user_id,
                "book_id": record.book_id,
                "book_title": book_title,
                "due_date": record.due_date.strftime("%Y-%m-%d"),
                "overdue_days": overdue_days,
                "fine": fine
            })

    return overdue_list


# --- Endpoint 5: Get All Available Books ---

@app.get("/books/available", response_model=list[Book])
async def get_available_books() -> list[Book]:
    """
    Get all books that are currently available for borrowing.
    """
    await asyncio.sleep(0.1)  # Simulate async database query
    return [book for book in books_db if book.available]


# --- Endpoint 6: Simulate Concurrent Multi-User Operations ---

@app.post("/simulate")
async def simulate_concurrent_users() -> dict:
    """
    Demonstrates asynchronous programming by simulating multiple users
    borrowing and returning books at the same time using asyncio.gather.

    asyncio.gather schedules all tasks concurrently so they overlap in
    execution — none waits for the previous one to finish.
    """

    async def borrow_for_user(user_id: int, book_id: int) -> dict:
        """Simulate a single user borrowing a book asynchronously."""
        await asyncio.sleep(0.1)  # Non-blocking I/O simulation
        try:
            result: dict = await borrow_book(BorrowRequest(user_id=user_id, book_id=book_id))
            return {"user_id": user_id, "action": "borrow", "status": "success", "detail": result["message"]}
        except HTTPException as e:
            return {"user_id": user_id, "action": "borrow", "status": "failed", "detail": e.detail}

    async def return_for_user(user_id: int, book_id: int) -> dict:
        """Simulate a single user returning a book asynchronously."""
        await asyncio.sleep(0.1)  # Non-blocking I/O simulation
        try:
            result: dict = await return_book(ReturnRequest(user_id=user_id, book_id=book_id))
            return {"user_id": user_id, "action": "return", "status": "success", "detail": result["message"]}
        except HTTPException as e:
            return {"user_id": user_id, "action": "return", "status": "failed", "detail": e.detail}

    # Phase 1: Four users borrow different books at the same time
    borrow_tasks: list = [
        borrow_for_user(user_id=201, book_id=5),
        borrow_for_user(user_id=202, book_id=6),
        borrow_for_user(user_id=203, book_id=7),
        borrow_for_user(user_id=204, book_id=8),
    ]
    borrow_results: tuple = await asyncio.gather(*borrow_tasks)

    # Phase 2: The same four users return their books at the same time
    return_tasks: list = [
        return_for_user(user_id=201, book_id=5),
        return_for_user(user_id=202, book_id=6),
        return_for_user(user_id=203, book_id=7),
        return_for_user(user_id=204, book_id=8),
    ]
    return_results: tuple = await asyncio.gather(*return_tasks)

    return {
        "message": "Concurrent simulation complete — all tasks ran simultaneously via asyncio.gather",
        "borrow_phase": list(borrow_results),
        "return_phase": list(return_results),
    }


# --- Run the application ---

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
