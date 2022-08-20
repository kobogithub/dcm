from sqlalchemy.orm import Session

from app.mod_cp import models, schemas

# Devuelve un documento por numero de documento
def get_document(db: Session, docnum: str) -> schemas.Document:
    return db.query(models.Document).filter(models.Document.docnum == docnum).first()
    
# Crear un documento nuevo  
def create_document(db: Session, document: schemas.Document):
    print(document.dict())
    db_document = models.Document(**document.dict())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

# Devuelve todos los documentos
def get_documents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Document).offset(skip).limit(limit).all()