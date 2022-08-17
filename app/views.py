from app import app
from app.mod_cp.models import Document,Rev

@app.route('/')
def index():
    doc = Document(docnum='EEPL-44',title='Estructural',section='Hormigon')
    print(doc.id)
    rev = Rev(rev=1,date='2022-02-01',os=150,status='APROBADO LIBERADO',totalsheets=5,owner=doc.id)
    print(rev.owner)
    return doc.revs

