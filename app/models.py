from app import app,db
from flask_login import UserMixin

class CadastroUsuario(UserMixin):
    id_usuario = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    nomesocial = db.Column(db.String(40))
    nome = db.Column(db.String(40), nullable=False)
    sobrenome = db.Column(db.String(40), nullable=False)
    genero = db.Column(db.String(40), nullable=False)
    id_endereco = db.Column(db.String(40), nullable=True)
    telefone = db.Column(db.String(15), nullable=False)    
    email = db.Column(db.String(60), nullable=False, unique=True) 
    senha = db.Column(db.String(10), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    data_nascimento = db.Column(db.String(50), nullable=False)
    rg = db.Column(db.String(50), nullable=False)
    data_cadastro = db.Column(db.String(50), nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    id_empresa = db.Column(db.String(50), nullable=True)
    

    def get_id(self):
        return str(self.cpf)
    
class CadastroEmpresa(UserMixin):
    id_empresa = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String(14), nullable=False, unique=True)
    razaosocial = db.Column(db.String(40))
    nome = db.Column(db.String(40), nullable=False)
    nomefantasia = db.Column(db.String(40), nullable=False)
    id_endereco = db.Column(db.String(40), nullable=True)
    telefone = db.Column(db.String(15), nullable=False)    
    email = db.Column(db.String(60), nullable=False, unique=True) 
    senha = db.Column(db.String(10), nullable=False)
    data_cadastro = db.Column(db.String(50), nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    id_empresa = db.Column(db.String(50), nullable=True)

    def get_id(self):
        return str(self.cnpj)