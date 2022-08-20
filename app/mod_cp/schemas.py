from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class NoteBase(BaseModel):
    notenum: int
    docnum: str
    rev: int
    status: str
    verify: str


class Note(NoteBase):
    id: int
    owner_sheet: int

    class Config:
        orm_mode = True

class RicBase(BaseModel):
    date: datetime
    notelist: list[str]

class Ric(RicBase):
    id: int
    owner_sheet: int

    class Config:
        orm_mode = True
class SheetBase(BaseModel):
    id: int
    sheetnum: int
    format: str
    #rics: list[Ric] = []
    #notes: list[Note] = []

class Sheet(SheetBase):
    id: int
    owner_rev: int

    class Config:
        orm_mode = True
class RevBase(BaseModel):
    rev: int
    date: datetime
    os: int
    status: str
    totalsheets: int
    #sheets: list[Sheet] = []

class CreateRev(RevBase):
    pass

class Rev(RevBase):
    id: int
    owner_document_id: int

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