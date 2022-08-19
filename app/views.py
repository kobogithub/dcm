from app import app
from app.mod_cp.models import Document,Rev
from app.mod_cp.forms import DocumentForm
from flask import request,render_template


@app.route("/", methods=["GET", "POST"])
def create_document():
    form = DocumentForm(request.form)
    if request.method == 'POST' or form.validate():
        return 'success'
    return render_template("home.html",form=form)
