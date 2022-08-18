from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField, SubmitField)
from wtforms.validators import DataRequired, Length

class DocumentForm(FlaskForm):
    docnum = StringField('Codigo de Documento', validators=[DataRequired(), Length(max=50)])
    doccnea = StringField('Codigo CNEA')
    docqbnet = StringField('Codigo QBNet')
    title = TextAreaField('Titulo', validators=[DataRequired()])
    section = StringField('Seccion', validators=[DataRequired()])

    submit = SubmitField('Registrar')