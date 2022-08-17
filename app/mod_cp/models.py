from email.policy import default
from app import db
from datetime import datetime as dt

"""
##############################################################
######## Modelos de Datos para el Panel de Carga (CP) ########
##############################################################
"""
class Document(db.Model):
    '''
    Representa un Documento del Proyecto Carem25 en la Base de Datos \n
    Existen dos tipos de documentos, los emitidos por CNEA y por la UG NA-SA. \n
    Dependiendo del campo se detalla la siguiente tabla de datos\n
    \n
    |   Name    |   CNEA    |   UG  |   Type    |   Description                              |
    | --------- | --------- | ----- | --------- | ------------------------------------------ |
    | docnum    |     X     |   X   |  String   | Codigo del plano                           |
    | doccnea   |           |   X   |  String   | Codigo de documento de CNEA (Documento UG) |
    | docqbnet  |           |   X   |  String   | Codigo del Sistema QBNet                   |
    | title     |     X     |   X   |  String   | Titulo del documento                       |
    | section   |     X     |   X   |  String   | Seccion de la carpeta                      |
    | revs      |     X     |   X   |  Table    | Tabla de revisiones del documento          |
    '''
    __tablename__ = 'document'
    id = db.Column(db.Integer, primary_key=True)
    docnum = db.Column(db.String(255), nullable=False, unique=True)
    doccnea = db.Column(db.String(255),nullable=True)
    docqbnet = db.Column(db.String(255),nullable=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    section = db.Column(db.String(255), nullable=False, unique=True)
    revs = db.relationship('Rev',backref='document', lazy=True)
    
    def __repr__(self) -> str:
        return f'Document {self.docnum}'
    
    def __save__(self):
        '''
        Guardda el documento en la Base de Datos
        '''
        db.session.add(self)
        db.session.commit()
    


class Rev(db.Model):
    '''
    Se almacena las revisiones del documento, la APROBADA LIBERADA como las SUPERADAS \n
    Tambien poseen una tabla de diferencias con los documentos emitidos por CNEA y UG.\n
    \n
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
    __tablename__ = 'rev'
    id = db.Column(db.Integer, primary_key=True)
    rev = db.Column(db.Integer,nullable=False, unique=True)
    date = db.Column(db.DateTime, nullable=False, unique=True,default=dt.utcnow())
    os = db.Column(db.Integer, nullable=False, unique=True)
    status = db.Column(db.String(255), nullable=False, unique=True)
    totalsheets = db.Column(db.Integer, nullable=False, unique=True)
    sheets = db.relationship('Sheet',backref='rev', lazy=True)
    owner = db.Column(db.Integer,db.ForeignKey('document.id'))

class Sheet(db.Model):
    '''
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
    __tablename__ = 'sheet'
    id = db.Column(db.Integer, primary_key=True)
    sheetnum = db.Column(db.Integer, nullable=False, unique=True)
    format = db.Column(db.String(255), nullable=False)
    ric = db.relationship('Ric',backref='owned_sheet', lazy=True)
    notes = db.relationship('Note',backref='sheet', lazy=True)
    owner = db.Column(db.Integer,db.ForeignKey('rev.id'))


class Ric(db.Model):
    '''
    Las Revisiones Internas de Cambios o Master son generadas por documentos de cambio.\n
    \n
    |   Name      |   Type    |   Description                              |
    | ----------- | --------- | ------------------------------------------ |
    | rev         |  Integer  | Revision del Master                        |
    | date        |  String   | Fecha de Liberacion del Master             |
    | notelist    |  Array    | Lista de Notas Vinculadas                  |
    | owner       |  Key      | Clave vinculada a la tabla de sheets       |
 
    '''
    __tablename__ = 'ric'
    id = db.Column(db.Integer, primary_key=True)
    rev = db.Column(db.String(255), nullable=False, unique=True)
    date = db.Column(db.DateTime, nullable=False, unique=True,default=dt.utcnow)
    notelist = db.Column(db.String(255), nullable=False, unique=True)
    owner = db.Column(db.Integer,db.ForeignKey('sheet.id'))

class Note(db.Model):
    '''
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
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True)
    notenum = db.Column(db.Integer, nullable=False, unique=True)
    docnum = db.Column(db.String(255), nullable=False, unique=True)
    rev = db.Column(db.Integer, nullable=False, unique=True)
    verify = db.Column(db.String(255), nullable=False, unique=True)
    status = db.Column(db.String(255), nullable=False, unique=True)
    owner = db.Column(db.Integer,db.ForeignKey('sheet.id'))