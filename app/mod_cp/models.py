from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base
"""
##############################################################
######## Modelos de Datos para el Panel de Carga (CP) ########
##############################################################
"""
class Document(Base):
    '''
    ## Tabla de Documentos
    Representa un Documento del Proyecto Carem25 en la Base de Datos
    Existen dos tipos de documentos, los emitidos por CNEA y por la UG NA-SA.
    Dependiendo del campo se detalla la siguiente tabla de datos
    |   Name    |   CNEA    |   UG  |   Type    |   Description                              |
    | --------- | --------- | ----- | --------- | ------------------------------------------ |
    | docnum    |     X     |   X   |  String   | Codigo del plano                           |
    | doccnea   |           |   X   |  String   | Codigo de documento de CNEA (Documento UG) |
    | docqbnet  |           |   X   |  String   | Codigo del Sistema QBNet                   |
    | title     |     X     |   X   |  String   | Titulo del documento                       |
    | section   |     X     |   X   |  String   | Seccion de la carpeta                      |
    | revs      |     X     |   X   |  Table    | Tabla de revisiones del documento          |
    '''
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True,index=True)
    docnum = Column(String(255), nullable=False, unique=True, index=True)
    doccnea = Column(String(255), nullable=False)
    docqbnet = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False, unique=True)
    section = Column(String(255), nullable=False, unique=True)

    revs = relationship('Rev',back_populates='owner_document')
    
class Rev(Base):
    '''
    ## Tabla de Revisiones
    Se almacena las revisiones del documento, la APROBADA LIBERADA como las SUPERADAS \n
    Tambien poseen una tabla de diferencias con los documentos emitidos por CNEA y UG.
    |   Name      |   CNEA    |   UG  |   Type    |   Description                              |
    | ----------- | --------- | ----- | --------- | ------------------------------------------ |
    | rev         |     X     |   X   |  Integer  | Numero de Revision                         |
    | date        |     X     |   X   |  String   | Fecha de Revision                          |
    | os          |     X     |       |  Integer  | Orden de Servicio                          |
    | status      |     X     |   X   |  String   | Estado del Documento                       |
    | totalsheets |     X     |   X   |  Integer  | Cantidad Total de hojas del documento      |
    | sheets      |     X     |   X   |  Table    | Tabla de hojas del documento               |
    | owner       |     X     |   X   |  Key      | Clave vinculada a la tabla de documento    |
    '''
    __tablename__ = "revs"
    id = Column(Integer, primary_key=True, index=True)
    rev = Column(Integer,nullable=False, unique=True, index=True)
    date = Column(String(255), nullable=False, unique=True,index=True)
    os = Column(Integer, nullable=False, unique=True,index=True)
    status = Column(String(255), nullable=False, unique=True)
    totalsheets = Column(Integer, nullable=False, unique=True)

    sheets = relationship('Sheet',back_populates='owner_rev')

    owner_document = Column(Integer,ForeignKey('documents.id'))

class Sheet(Base):
    '''
    ## Tabla de Hojas
    Cuando se genera un master, puede afectarse la/s hoja/s de un documento *CNEA*.\n
    \n
    |   Name      |   Type    |   Description                              |
    | ----------- | --------- | ------------------------------------------ |
    | sheetnum    |  Integer  | Numero de Hoja                             |
    | format      |  String   | Formato de la Hoja A0,A1,A1.0,etc..        |
    | ric         |  Table    | Tabla de Revision Interna de Cambios       |
    | notes       |  Table    | Tabla de Notas Afectadas al documento      |
    | owner       |  Key      | Clave vinculada a la tabla de revisiones   |
 
    '''
    __tablename__ = "sheets"
    id = Column(Integer, primary_key=True)
    sheetnum = Column(Integer, nullable=False, unique=True)
    format = Column(String(255), nullable=False)

    ric = relationship('Ric',back_populates='owned_sheet', lazy=True)

    notes = relationship('Note',back_populates='owner_sheet', lazy=True)

    owner_rev = Column(Integer(),ForeignKey('revs.id'))


class Ric(Base):
    '''
    ## Tabla de revisiones Interna de Cambios
    Las Revisiones Internas de Cambios o Master son generadas por documentos de cambio.\n
    \n
    |   Name      |   Type    |   Description                              |
    | ----------- | --------- | ------------------------------------------ |
    | rev         |  Integer  | Revision del Master                        |
    | date        |  String   | Fecha de Liberacion del Master             |
    | notelist    |  Array    | Lista de Notas Vinculadas                  |
    | owner       |  Key      | Clave vinculada a la tabla de sheets       |
 
    '''
    __tablename__ = "rics"
    id = Column(Integer, primary_key=True)
    rev = Column(String(255), nullable=False, unique=True)
    date = Column(String(255), nullable=False, unique=True)
    notelist = Column(String(255), nullable=False, unique=True)

    owner_sheet = Column(Integer,ForeignKey('sheets.id'))

class Note(Base):
    '''
    ## Tabla de Notas
    Detalle de la nota que afecta el documento, se categorizan en tres tipos \n
    de documentos Notificacion de Cambio en Obra (NCO), Aclaracion Tecnica(AT) y\n
    Solicitud de Cambio en Obra (SCO).\n
    \n
    |   Name      |  NCO  |   AT  |  SCO  |   Type    |   Description                              |
    | ----------- | ----- | ----- | ----- | --------- | ------------------------------------------ |
    | notenum     |   X   |   X   |   X   |  Integer  | Numero de Nota                             |
    | docnum      |   X   |   X   |   X   |  String   | Codigo del documento                       |
    | rev         |   X   |   X   |   X   |  Integer  | Revision del documento                     |
    | status      |   X   |   X   |   X   |  String   | Estado del Documento                       |
    | verify      |   X   |       |       |  String   | Estado de Verificacion en la Obra          |
    | owner       |   X   |   X   |   X   |  Key      | Clave vinculada a la tabla de sheets       |

    '''
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    notenum = Column(Integer, nullable=False, unique=True)
    docnum = Column(String(255), nullable=False, unique=True)
    rev = Column(Integer, nullable=False, unique=True)
    verify = Column(String(255), nullable=False, unique=True)
    status = Column(String(255), nullable=False, unique=True)

    owner_sheet = Column(Integer,ForeignKey('sheets.id'))



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
