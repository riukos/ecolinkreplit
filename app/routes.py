from app import app
from flask import Flask, render_template, request

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
    if request.method == 'POST':
        # Obtem os dados do formulário
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Aqui você pode adicionar a lógica para enviar o e-mail
        # Neste exemplo, apenas imprimiremos os dados no terminal
        print(f'Nome: {name}')
        print(f'email: {email}')
        print(f'Mensagem: {message}')

        return 'Mensagem enviada com sucesso!'

    return render_template('contact.html', title = 'contact')

@app.route('')
if __name__ == '__main__':
    app.run(debug=True)