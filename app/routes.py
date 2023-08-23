from app import app, db, bcrypt
from flask import Flask, render_template, request, url_for, redirect, flash, session
from app.forms import Contato, Cadastro
from app.models import ContatoModels, CadastroModels

import time

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = 'home')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html', title = 'sobre')


@app.route('/projetos')
def projetos():
    return render_template('projetos.html', title = 'projetos')

# Rota para a página de contato com o formulário
@app.route('/contact',  methods=['GET', 'POST'])
def contact():
    formulario = Contato()
    if formulario.validate_on_submit():
        flash('Sua messagem foi enviada com sucesso')
        name = formulario.name.data
        email = formulario.email.data  
        message = formulario.message.data
        novo_contato = ContatoModels(name=name, email=email, message=message)
        db.session.add(novo_contato)
        db.session.commit()
        
    return render_template('contact.html', title = 'Contato', formulario = formulario)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    cadastro = Cadastro()
    
    if cadastro.validate_on_submit():
        try:
            name = cadastro.name.data
            email = cadastro.email.data
            password = cadastro.password.data
            hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

            telefone = cadastro.telefone.data
            
            # Novos campos para CPF e Endereço
            cpf = cadastro.cpf.data
            rua = cadastro.rua.data
            numero = cadastro.numero.data
            bairro = cadastro.bairro.data
            cidade = cadastro.cidade.data
            uf = cadastro.uf.data
            cep = cadastro.cep.data
            
            # Criar instância do modelo de usuário
            novo_usuario = CadastroModels(
                name=name,
                email=email,
                password=hash_password,
                telefone=telefone,
                cpf=cpf,
                rua=rua,
                numero=numero,
                bairro=bairro,
                cidade=cidade,
                uf=uf,
                cep=cep
                )
            
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Você foi cadastrado com sucesso')
        except Exception as e:
            flash('Ocorreu um erro ao cadastrar!, Entre em contato com o suporte: admin@admin.com')
            print(str(e))
            
    return render_template('cadastro.html', title='Cadastro', cadastro=cadastro)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = CadastroModels.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            session['email'] = user.email
            session['name'] = user.name
            session['telefone'] = user.telefone
            session['password'] = user.password
            session['cpf'] = user.cpf
            session['rua'] = user.rua
            session['numero'] = user.numero
            session['bairro'] = user.bairro
            session['cidade'] = user.bairro
            session['uf'] = user.uf
            session['cep'] = user.cep


            flash('Seja bem vindo')
            return redirect(url_for("index"))
        else:
            flash("Email ou senha incorreto")
    return render_template('login.html', title='Login')

@app.route('/editarusuario', methods=['GET', 'POST'])
def editarusuario():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = CadastroModels.query.filter_by(email=session['email']).first()
    
    if request.method == 'POST':
        usuario.nome = request.form.get('name')
        usuario.email = request.form.get('email')
        usuario.telefone = request.form.get('telefone')
        
        # Atualizar senha, se fornecida no formulário
        password = request.form.get('password')
        if password:
            usuario.password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Atualizar CPF
        usuario.cpf = request.form.get('cpf')
        
        # Atualizar Endereço
        usuario.rua = request.form.get('rua')
        usuario.numero = request.form.get('numero')
        usuario.bairro = request.form.get('bairro')
        usuario.cidade = request.form.get('cidade')
        usuario.uf = request.form.get('uf')
        usuario.cep = request.form.get('cep')
        
        db.session.commit()
        
        # Atualizar os dados na sessão (se necessário)
        session['name'] = usuario.nome
        session['email'] = usuario.email
        session['telefone'] = usuario.telefone
        session['cpf'] = usuario.cpf
        session['rua'] = usuario.rua
        session['numero'] = usuario.numero
        session['bairro'] = usuario.bairro
        session['cidade'] = usuario.cidade
        session['uf'] = usuario.uf
        session['cep'] = usuario.cep

        flash('Seus dados foram atualizados com sucesso!')
        
    return render_template('editarusuario.html', titulo='Editar', usuario=usuario)



@app.route('/delete_conta', methods=['GET', 'POST'])
def delete_conta():
    if 'email' not in session:
        return redirect(url_for('login'))
    usuario = CadastroModels.query.filter_by(email = session['email']).first()
    db.session.delete(usuario)
    db.session.commit()
    session.clear()
    flash('Sua conta foi deletada!')

    return redirect(url_for('cadastro'))
    

def new_func(usuario):
    return usuario



@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('name', None)
    session.pop('password', None)
    session.pop('telefone', None)
    session.pop('cpf', None)
    session.pop('rua', None)
    session.pop('numero', None)
    session.pop('bairro', None)
    session.pop('cidade', None)
    session.pop('uf', None)
    session.pop('cep', None)


    return redirect(url_for('login'))