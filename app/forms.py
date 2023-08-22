from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect

class Contato(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    message = TextAreaField('message')
    enviar =  SubmitField('Enviar')

class Cadastro(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    telefone = StringField('telefone', validators=[DataRequired()])
    cpf = StringField('cpf', validators=[DataRequired()])
    rua = StringField('rua', validators=[DataRequired()])
    numero = StringField('numero', validators=[DataRequired()])
    bairro = StringField('bairro', validators=[DataRequired()])
    cidade = StringField('cidade', validators=[DataRequired()])
    uf = StringField('uf', validators=[DataRequired()])
    cep = StringField('cep', validators=[DataRequired()])

    

    enviar =  SubmitField('Enviar')