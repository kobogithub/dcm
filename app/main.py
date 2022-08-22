from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from app.mod_cp import crud, models, schemas
from app.db.database import SessionLocal, engine
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

tag_metadata = [
   {
    "name":"documents",
    "description":"Manejo de los documentos del dcm."
   },
   {
    "name":"revs",
    "description":"Manejo de las revisiones de los documentos."
   } 
  ]
app = FastAPI(
    title="Swagger Document Control Manager - OpenAPI 3.0",
    description="## Documentacion de API DCM",
    contact={
        "name":"Kevin Barroso",
        "url":"https://github.com/kobogithub",
        "email":"kobo.devops@gmail.com"
    },
    version="0.0.1",
    tag_metadata=tag_metadata
)

templates = Jinja2Templates(directory="app/templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request,skip: int = 0, limit: int = 100,db: Session = Depends(get_db)):
    documents = crud.get_documents(db, skip=skip, limit=limit)
    return templates.TemplateResponse('home.html',{'request': request, 'documents': documents})

@app.post("/documents/", response_model=schemas.Document, tags=['documents'])
def create_document(document: schemas.CreateDocument, db: Session = Depends(get_db)):
    #db_user = crud.get_user_by_email(db, email=user.email)
    #if db_user:
        #raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_document(db=db, document=document)


@app.get("/documents/", response_model=list[schemas.Document], tags=['documents'])
def read_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    documents = crud.get_documents(db, skip=skip, limit=limit)
    return documents


@app.get("/documents/{docnum}", response_model=schemas.Document, tags=['documents'])
def read_document(docnum: str, db: Session = Depends(get_db)):
    db_document = crud.get_document(db, docnum=docnum)
    #if db_user is None:
        #raise HTTPException(status_code=404, detail="User not found")
    return db_document

@app.post("/documents/{document_id}/revs/", response_model=schemas.Rev, tags=['revs'])
def create_rev(document_id: int, rev: schemas.CreateRev, db: Session = Depends(get_db)):
    db_rev = crud.create_rev(db, rev=rev ,document_id=document_id)
    #if db_user is None:
        #raise HTTPException(status_code=404, detail="
    return db_rev

@app.post("/revs/{rev_id}/sheets/", responde_model=schemas.Sheet, tags=['revs'])
def create_sheet()