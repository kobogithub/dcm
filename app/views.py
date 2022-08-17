from app import app
from app.mod_cp.models import Document

@app.route('/')
def index():
    doc = Document(docnum='EEPL-44',title='Estructural',section='Hormigon')
    print(doc)
    return doc.docnum

