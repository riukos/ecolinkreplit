from app import app
from flask import render_template

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

