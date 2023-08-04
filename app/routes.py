from app import app
from flask import Flask, render_template, request, url_for, redirect, flash
from app.forms import Contato
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
        flash("Seu formulario foi eviado com sucesso")
        time.sleep(2)
        return redirect('/contact')
    return render_template('contact.html', title = 'contato', formulario = formulario)

