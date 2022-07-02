
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from typing import List
from sqlalchemy.orm import joinedload

models.Base.metadata.create_all(bind=engine)



app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/author')
async def create_author(form: schemas.Author, db: Session = Depends(get_db)):
    create_author = models.Author(**form.dict())

    db.add(create_author)
    db.commit()
    db.refresh(create_author)

    return create_author


@app.get('/author')
async def get_dept(db: Session = Depends(get_db)):
    return db.query(models.Author).all()


@app.post('/books')
async def create_book(form: schemas.Book, db: Session = Depends(get_db)):
    create_book = models.Book(**form.dict())

    db.add(create_book)
    db.commit()
    db.refresh(create_book)

    return create_book



@app.get("/books/{id}", response_model=schemas.BookSchema)
async def get_book(id: int, db: Session = Depends(get_db)):
    return db.query(models.Book).options(joinedload(models.Book.authors)).\
        where(models.Book.id == id).one()


@app.get("/books", response_model=List[schemas.BookSchema])
async def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).options(joinedload(models.Book.authors)).all()


@app.get("/authors/{id}", response_model=schemas. AuthorSchema)
async def get_author(id: int, db: Session = Depends(get_db)):
    return db.query(models.Author).options(joinedload(models.Author.books)).\
        where(models.Author.id == id).one()


@app.get("/authors", response_model=List[schemas.AuthorSchema])
async def get_authors(db: Session = Depends(get_db)):
    return db.query(models.Author).options(joinedload(models.Author.books)).all()