from app import app, db
from flask import Flask, render_template, request, url_for, redirect, flash
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
        flash('Você foi cadastrado com sucesso')
        name = cadastro.name.data
        email = cadastro.email.data
        password = cadastro.password.data  
        telefone = cadastro.telefone.data
        novo_contato = CadastroModels(name=name, email=email, password =password, telefone=telefone)
        db.session.add(novo_contato)
        db.session.commit()
        
    return render_template('cadastro.html', title = 'Cadastro', cadastro = cadastro)

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''dados_cadastro = None
    formulario = Cadastro()
    if formulario.validate_on_submit():
        flash('Você foi cadastrado com sucesso')
        name = formulario.name.data
        email = formulario.email.data
        password = formulario.password.data  
        novo_contato = ContatoModels(name=name, email=email, password =password)
        db.session.add(novo_contato)
        db.session.commit()'''
        
    return render_template('login.html', title = 'login')