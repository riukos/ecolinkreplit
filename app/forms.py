from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,TelField,TextAreaField,SubmitField, PasswordField, SelectField, DecimalField, DateField
from wtforms.validators import DataRequired, Email, Length, Regexp
from flask_wtf.csrf import CSRFProtect

class Contato(FlaskForm):
    nome = StringField('nome')
    email = EmailField('email',validators=[DataRequired(), Email()])
    telefone = TelField('telefone',validators=[DataRequired()])
    descricao = TextAreaField('mensagem')
    enviar = SubmitField('Enviar')

class Cadastro_Usuario(FlaskForm):
    cpf = StringField('CPF', validators=[
        DataRequired(message='Campo obrigatório.'),
        Regexp(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', message='Formato de CPF inválido.')
    ])
    rg = StringField('RG', validators=[
        DataRequired(message="O campo RG é obrigatório."),
        Regexp(r'^\d{1,10}$', message="O RG deve conter apenas números, no máximo 10 dígitos.")
    ])
    data_nascimento = DateField('Data de Nascimento', format='%Y-%m-%d', validators=[DataRequired()])
    data_cadastro = StringField('Data Cadastro')
    nomesocial = StringField('Nome Social')
    nome = StringField('Nome')
    sobrenome = StringField('Sobrenome')
    genero = SelectField('genero', choices=[
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino'),
        ('Outro', 'Outro')        
        ], validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[
        DataRequired(),
        Regexp(r"^(?:\+?55)?\s?(?:\(?[1-9][0-9]\)?\s?)?(?:[2-9][0-9]{3,4}\-?[0-9]{4})$", message="formato do numero de telefone invalido")
    ])
    email = EmailField('Email', validators=[
        DataRequired(),
        Regexp(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", message="Email inválido!")
    ])
    tipo = SelectField('Função', choices=[
        ('Autonomo', 'Autonomo'),
        ('Comprador', 'Comprador'),
        ('Vendedor', 'Vendedor')        
        ], validators=[DataRequired()])
    cnpj = StringField('CNPJ', validators=[
        DataRequired(message='Campo obrigatório.'),
        Regexp(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', message='Formato de CNPJ inválido.')
    ])
    senha = PasswordField('Senha', validators=[
    DataRequired(),
    Length(min=8, message="A senha deve ter pelo menos 8 caracteres."),
    Regexp(r"\d", message="A senha deve conter pelo menos 1 número."),
    Regexp(r"[!@#$%^&*()_+\-=\[\]{};:'\"\\|,.<>\/?]", message="A senha deve conter pelo menos um carácter especial."),
    Regexp(r"^[^\s].*[^\s]$", message="A senha não pode ter espaços em branco à esquerda ou à direita.")
])
    enviar = SubmitField('Cadastrar')

class Cadastro_Empresa(FlaskForm):
    cnpj = StringField('CNPJ', validators=[
        DataRequired(message='Campo obrigatório.'),
        Regexp(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', message='Formato de CNPJ inválido.')
    ])
    razaosocial = StringField('Razão Social')
    nome = StringField('Nome')
    nomefantasia = StringField('Nome fantasia')
    telefone = StringField('Telefone', validators=[
        DataRequired(),
        Regexp(r"^(?:\+?55)?\s?(?:\(?[1-9][0-9]\)?\s?)?(?:[2-9][0-9]{3,4}\-?[0-9]{4})$", message="formato do numero de telefone invalido")
    ])
    email = EmailField('Email', validators=[
        DataRequired(),
        Regexp(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", message="Email invalido!"), Email()
    ])
    senha = PasswordField('Senha', validators=[
    DataRequired(),
    Length(min=8, message="Password must be at least 8 characters long."),
    Regexp(r"\d", message="Password must contain at least 1 number."),
    Regexp(r"[!@#$%^&*()_+\-=\[\]{};:'\"\\|,.<>\/?]", message="A senha deve conter pelo menos um carácter especial."),
    Regexp(r"^[^\s].*[^\s]$", message="A senha não pode ter espaços em branco à esquerda ou à direita.")
])
    enviar = SubmitField('Enviar')

class Endereco(FlaskForm):
    cep = StringField('CEP', validators=[
        DataRequired(message="Campo obrigatório."),
        Length(min=8, max=8, message="O CEP deve conter 8 dígitos."),
        Regexp(r"^\d{8}$", message="Formato de CEP inválido.")
    ])
    complemento = StringField('COmplemento')
    rua = StringField('Rua')
    numero = StringField('Número')
    bairro = StringField('Bairro')
    cidade = StringField('Cidade')
    uf = StringField('UF')

class MaterialReciclavel(FlaskForm):
    nome_do_material = StringField('Nome do Material', validators=[DataRequired(), Length(max=255)])
    tipo_material = SelectField('Tipo de Material', choices=[
        ('Plástico', 'Plástico'),
        ('Papel', 'Papel'),
        ('Vidro', 'Vidro'),
        ('Ferro', 'Ferro'),
        ('Aluminio', 'Aluminio'),
        ('Cobre', 'Cobre'),
        ('Outro', 'Outro')
    ], validators=[DataRequired()])
    peso = StringField('Peso do Material', validators=[DataRequired(), Length(max=255)])
    preco_kg = DecimalField('Preço por Quilograma', places=3, validators=[DataRequired()])
    valor_venda_moeda_virtual = DecimalField('Valor de Venda em Moeda Virtual', places=3, validators=[DataRequired()])
    valor_moeda_corrente = DecimalField('Valor de Venda em Moeda Corrente', places=3, validators=[DataRequired()])
class Vendas(FlaskForm):
    data_da_venda = StringField('Data Cadastro')
    id_operador_venda = StringField('ID do Operador de Venda')
    id_operador_compra = StringField('ID do Operador de Compra')
    valor_venda = DecimalField('Valor de Venda', places=2, validators=[DataRequired()])
    valor_ecoin = DecimalField('Valor em Ecoin', places=2, validators=[DataRequired()])
    id_material = StringField('ID do Operador de Venda')
    enviar = SubmitField('Enviar')