from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField)
from wtforms.validators import InputRequired, Length

class DocumentForm(FlaskForm):
    docnum = StringField('Codigo de Documento', validators=[InputRequired()])
    doccnea = StringField('Codigo CNEA')
    docqbnet = StringField('Codigo QBNet')
    title = StringField('Titulo', validators=[InputRequired()])
    section = StringField('Seccion', validators=[InputRequired()])