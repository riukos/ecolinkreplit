from app import app, db
from flask import Flask, render_template, request, url_for, redirect, flash
from app.forms import Contato
from app.models import ContatoModels
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
    dados_formulario = None
    formulario = Contato()
    if formulario.validate_on_submit():
        flash('Sua messagem foi enviada com sucesso')
        name = formulario.name.data
        email = formulario.email.data  
        message = formulario.message.data
        novo_contato = ContatoModels(name=name, email=email, message=message)
        db.session.add(novo_contato)
        db.session.commit()
        
    return render_template('contact.html', title = 'Contato', formulario = formulario, dados_formulario = dados_formulario)

