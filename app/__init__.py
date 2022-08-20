from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.mod_cp import crud, models, schemas
from app.db.database import SessionLocal, engine

#models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/documents/", response_model=schemas.Document)
def create_document(document: schemas.CreateDocument, db: Session = Depends(get_db)):
    #db_user = crud.get_user_by_email(db, email=user.email)
    #if db_user:
        #raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_document(db=db, document=document)


@app.get("/documents/", response_model=list[schemas.Document])
def read_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    documents = crud.get_documents(db, skip=skip, limit=limit)
    return documents


@app.get("/documents/{docnum}", response_model=schemas.Document)
def read_document(docnum: str, db: Session = Depends(get_db)):
    db_document = crud.get_document(db, docnum=docnum)
    #if db_user is None:
        #raise HTTPException(status_code=404, detail="User not found")
    return db_document

@app.post("/documents/{document_id}/revs/", response_model=schemas.Rev)
def create_rev(document_id: int, rev: schemas.CreateRev, db: Session = Depends(get_db)):
    db_rev = crud.create_rev(db, rev=rev ,document_id=document_id)
    #if db_user is None:
        #raise HTTPException(status_code=404, detail="
    return db_rev