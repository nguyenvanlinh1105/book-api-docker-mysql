from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import pandas as pd

app = FastAPI()

# ----------- Database connection ----------
def get_connection():
    return mysql.connector.connect(
        host="testing_mysql",  
        user="root",           
        password="0387092630Linh",
        database="local_db",
    )

# ----------- Pydantic model ----------
class Book(BaseModel):
    id : int
    title: str
    

class BookUpdate(BaseModel):
    id : int
    title: str

# ----------- READ all books ----------
@app.get("/books")
def read_books():
    try:
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM books", conn)
        conn.close()
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------- CREATE new book ----------
@app.post("/books")
def create_book(book: Book):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO books (id, title) VALUES (%s, %s)"
    cursor.execute(query, (book.id, book.title))
    conn.commit()
    book_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {"id": book_id, "message": "Book created successfully"}

# ----------- UPDATE a book ----------
@app.put("/books/{book_id}")
def update_book(book_id: int, book: BookUpdate):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "UPDATE books SET title = %s WHERE id = %s"
    cursor.execute(query, (book.title, book_id))
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Book not found")

    cursor.close()
    conn.close()
    return {"message": "Book updated successfully"}


# ----------- DELETE a book ----------
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Book deleted successfully"}
