from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class NoteBase(BaseModel):
    notenum: int
    docnum: str
    rev: int
    status: str
    verify: str
    sheets: str

class CreateNote(NoteBase):
    pass

class Note(NoteBase):
    id: int
    owner_ric_id: int

    class Config:
        orm_mode = True

#class RicBase(BaseModel):
    #date: datetime
    #notelist: list[str]

#class Ric(RicBase):
    #id: int
    #owner_sheet: int

    #class Config:
        #orm_mode = True
class RicBase(BaseModel):
    id: int
    rev: str
    date: datetime
    status: str
class CreateRic(RicBase):
    pass
class Ric(RicBase):
    id: int
    owner_rev_id : int
    notes: list[Note] = []
    class Config:
        orm_mode = True

class RevBase(BaseModel):
    rev: int
    date: datetime
    os: int
    status: str
    totalsheets: int

class CreateRev(RevBase):
    pass

class Rev(RevBase):
    id: int
    owner_document_id: int
    rics: list[Ric] = []

    class Config:
        orm_mode = True

class DocumentBase(BaseModel):
    docnum: str
    doccnea: Optional[str]
    docqbnet: Optional[str]
    title: str
    section: str

class CreateDocument(DocumentBase):
    pass
class Document(DocumentBase):
    id: int
    revs: list[Rev] = []

    class Config:
        orm_mode = True