from app import app, bcrypt, login_manager
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, url_for, request, flash, redirect
from app.forms import Contato, Cadastro_Usuario, Endereco, Cadastro_Empresa, MaterialReciclavel, Vendas
from flask_bcrypt import check_password_hash# Certifique-se de ter esta biblioteca instalada e configurada
import pyodbc
from app.models import CadastroUsuario, CadastroEmpresa
from datetime import date
from config import Config

connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={Config.server};DATABASE={Config.database};UID={Config.username};PWD={Config.password}'
cnxn = pyodbc.connect(connection_string)


@login_manager.user_loader
def load_user(user_id):
    try:
        cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()

        # Verifique se o ID está na tabela de usuários comuns
        cursor.execute("SELECT * FROM USUARIO_funcionario WHERE CPF = ?;", [user_id])
        user_data = cursor.fetchone()

        if user_data:
            user = CadastroUsuario()
            user.id_usuario = user_data.ID_Usuario
            user.cpf = user_data.CPF
            user.nomesocial = user_data.NomeSocial
            user.nome = user_data.Nome
            user.sobrenome = user_data.Sobrenome
            user.genero = user_data.Genero
            user.id_endereco = user_data.ID_Endereco
            user.telefone = user_data.Telefone
            user.email = user_data.Email
            user.senha = user_data.Senha
            user.tipo = user_data.Tipo
            user.data_nascimento = user_data.Data_de_nascimento
            user.rg = user_data.RG
            user.data_cadastro = user_data.Data_Cadastro
            user.id_empresa = user_data.ID_Empresa

            return user

        # Se o ID não estiver na tabela de usuários comuns, verifique na tabela de empresas
        cursor.execute("SELECT * FROM EMPRESA WHERE CNPJ = ?;", [user_id])
        empresa_data = cursor.fetchone()

        if empresa_data:
            empresa = CadastroEmpresa()
            empresa.id_empresa = empresa_data.ID_Empresa
            empresa.cnpj = empresa_data.CNPJ
            empresa.razaosocial = empresa_data.RazaoSocial
            empresa.nome = empresa_data.Nome
            empresa.nomefantasia = empresa_data.NomeFantasia
            empresa.id_endereco = empresa_data.ID_Endereco
            empresa.telefone = empresa_data.Telefone
            empresa.email = empresa_data.Email
            empresa.senha = empresa_data.Senha
            empresa.data_cadastro = empresa_data.Data_Cadastro

            return empresa

        cursor.close()
        cnxn.close()
    except Exception as e:
        print(str(e))

    # Se algo der errado ou o usuário não existir, retorne None
    return None


@app.route('/')
def index():
    return render_template('index.html',titulo = 'Página inicial')

@app.route('/contatos', methods=['POST', 'GET'])
def contatos():
    formulario = Contato()
    print('Acessou a rota contatos!')
    if formulario.validate_on_submit():
        try:
            # Configuração da conexão com o SQL Server
            cnxn = pyodbc.connect(connection_string)
            cursor = cnxn.cursor()

            nome = formulario.nome.data
            email = formulario.email.data
            telefone = formulario.telefone.data
            descricao = formulario.descricao.data

            # Inserir os dados do contato na tabela 'CONTATO' do SQL Server
            cursor.execute("INSERT INTO CONTATO (Nome, Email, telefone, Descricao) VALUES (?, ?, ?, ?);", [nome, email, telefone, descricao])
            cnxn.commit()
            cursor.close()
            cnxn.close()

            flash('Seu cadastro foi enviado com sucesso!')

        except Exception as e:
            flash('Ocorreu um erro ao enviar o cadastro. Entre em contato com o suporte: adm@admin.com')
            print(str(e))

    return render_template('contatos.html', titulo='Contatos', formulario=formulario)


@app.route('/cadastro_produto_reciclavel', methods=['GET', 'POST'])
def cadastro_produto_reciclavel():
    form_reciclavel = MaterialReciclavel()
    if request.method == 'POST':
        # Recupere os dados do formulário
        nome_do_material = form_reciclavel.nome_do_material.data
        tipo_material = form_reciclavel.tipo_material.data
        peso = form_reciclavel.peso.data
        preco_kg = form_reciclavel.preco_kg.data
        valor_venda_moeda_virtual = form_reciclavel.valor_venda_moeda_virtual.data
        valor_moeda_corrente = form_reciclavel.valor_moeda_corrente.data

        try:
            cnxn = pyodbc.connect(connection_string)
            cursor = cnxn.cursor()
            # Insira os dados na tabela de produtos recicláveis
            cursor.execute("INSERT INTO Material_Reciclavel (nome_do_material, tipo_material, peso, preco_kg, valor_venda_moeda_virtual, valor_moeda_corrente) VALUES (?, ?, ?, ?, ?, ?);", (nome_do_material, tipo_material, peso, preco_kg, valor_venda_moeda_virtual,valor_moeda_corrente ))
            cnxn.commit()
            flash('Produto reciclável cadastrado com sucesso', 'success')
            return redirect(url_for('cadastro_produto_reciclavel'))
        except Exception as e:
            flash('Erro ao cadastrar o produto reciclável: ' + str(e), 'danger')

    return render_template('cadastro_produto_reciclavel.html', titulo='Cadastro Produto Reciclavel', form_reciclavel=form_reciclavel)

@app.route('/venda', methods=['GET', 'POST'])
@login_required
def venda():
    form_venda = Vendas()
    form_material = MaterialReciclavel()

    if request.method == 'POST' and form_venda.validate_on_submit() and form_material.validate_on_submit():
        id_material = form_material.id_material.data
        quantidade = form_venda.quantidade.data
        valor_ecoin = form_venda.valor_ecoin.data
        data_da_venda = date.today()

        cnxn = cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()

        try:
            # Consulta SQL para obter o preço de venda com base no id_material
            cursor.execute("SELECT valor_venda FROM MATERIAL_RECICLAVEL WHERE id_material = ?;", id_material)
            row = cursor.fetchone()

            if row:
                valor_venda = row.valor_venda
                valor_total = quantidade * valor_venda

                # Determinar o tipo do usuário logado (Vendedor, Autônomo ou Comprador)
                cursor.execute("SELECT Tipo, ID_usuario FROM Usuario_funcionario WHERE Tipo IN ('Vendedor', 'Comprador', 'Autonomo')")
                results = cursor.fetchall()

                if results:
                    # Extrair os tipos de usuário e IDs do resultado da consulta
                    tipo_usuario, id_usuario = results[0]

                    if tipo_usuario == 'Vendedor' or tipo_usuario == 'Autonomo':
                        id_operador_venda = id_usuario  # Defina o ID do operador de venda como o ID do usuário
                        id_operador_compra = None
                    elif tipo_usuario == 'Comprador':
                        id_operador_venda = None
                        id_operador_compra = id_usuario  # Defina o ID do operador de compra como o ID do usuário

                    # Inserir a venda no banco de dados
                    cursor.execute("INSERT INTO Venda (data_da_venda, id_operador_venda, id_operador_compra, id_material, valor_venda, valor_ecoin) VALUES (?, ?, ?, ?, ?, ?);", (data_da_venda, id_operador_venda, id_operador_compra, id_material, valor_total, valor_ecoin))
                    cnxn.commit()
                    flash('Venda cadastrada com sucesso', 'success')
                    return redirect(url_for('venda'))
                else:
                    flash('Usuário não encontrado ou não tem permissão para realizar vendas.', 'danger')
            else:
                flash('Material não encontrado.', 'danger')
        except Exception as e:
            flash('Erro ao realizar a venda: ' + str(e), 'danger')
        finally:
            cursor.close()
            cnxn.close()

    return render_template('venda.html', form_venda=form_venda, form_material=form_material)



@app.route('/sobre')
def sobre():
    return render_template('sobre.html', titulo = 'Sobre')

@app.route('/cadastro_empresa', methods=['GET','POST'])
def cadastro_empresa():
    cadastro_empresa = Cadastro_Empresa()
    endereco = Endereco()
    if request.method == 'POST':
        try:
            cnxn = pyodbc.connect(connection_string)
            cursor = cnxn.cursor()
           
            hash_senha = cadastro_empresa.senha.data

            cnpj = cadastro_empresa.cnpj.data
            telefone = cadastro_empresa.telefone.data
            nome = cadastro_empresa.nome.data
            nomefantasia = cadastro_empresa.nomefantasia.data
            razaosocial = cadastro_empresa.razaosocial.data
            email = cadastro_empresa.email.data
            telefone = cadastro_empresa.telefone.data
            # Gerar hashes de senha e outros campos sensíveis
            senha = bcrypt.generate_password_hash(hash_senha).decode('utf-8')
            data_cadastro = date.today()
            rua = endereco.rua.data
            bairro = endereco.bairro.data
            cidade = endereco.cidade.data
            uf = endereco.uf.data
            if request.method == 'POST' and 'submit_cep':
                    cep = endereco.cep.data
                    response = request.get(f"https://viacep.com.br/ws/{cep}/json/")
                    data = response.json()

                    if "erro" not in data:
                        rua = data['logradouro']
                        bairro = data['bairro']
                        cidade = data['localidade']
                        uf = data['uf']
                    else:
                        rua, bairro, cidade, uf = None, None, None, None
                        # Você pode adicionar uma mensagem flash aqui para informar que o CEP não foi encontrado
            


            cursor.execute("INSERT INTO ENDERECO (Rua, Bairro, Cidade, UF, cep) VALUES (?, ?, ?, ?,?);", [rua, bairro, cidade, uf, cep])
            cnxn.commit()

            # Obter o ID_Endereco gerado na inserção anterior
            cursor.execute("SELECT @@IDENTITY;")
            id_endereco = cursor.fetchone()[0]
            print(id_endereco)
            # Inserir dados do funcionário na tabela 'USUARIO_funcionario' com o ID_Endereco correto
            cursor.execute("INSERT INTO EMPRESA (CNPJ, NomeFantasia, Nome, ID_Endereco, Telefone, Email, Senha, RazaoSocial, Data_Cadastro) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", [cnpj, nomefantasia, nome, id_endereco, telefone, email, senha, razaosocial, data_cadastro])
            cnxn.commit()
            cursor.close()
            cnxn.close()
            flash('Seu cadastro foi realizado com sucesso!')
        except Exception as e:
            flash('Ocorreu um erro ao cadastrar! Entre em contato com o suporte: adm@admin.com')
            print(str(e))
            print('foi erro de exception')
    return render_template('cadastro_empresa.html', titulo='Cadastro Empresa', cadastro_empresa=cadastro_empresa, endereco=endereco)

@app.route('/cadastro_usuario', methods=['POST', 'GET'])
@login_required
def cadastro_usuario():
    cadastro_usuario = Cadastro_Usuario()
    endereco = Endereco()

    if request.method == 'POST':
        try:
            cnxn = pyodbc.connect(connection_string)
            cursor = cnxn.cursor()
            hash_senha = cadastro_usuario.senha.data          
            cpf = cadastro_usuario.cpf.data
            nomesocial = cadastro_usuario.nomesocial.data
            nome = cadastro_usuario.nome.data
            sobrenome = cadastro_usuario.sobrenome.data
            genero = cadastro_usuario.genero.data
            telefone = cadastro_usuario.telefone.data
            email = cadastro_usuario.email.data
            tipo = cadastro_usuario.tipo.data

            if tipo in ['Vendedor', 'Comprador']:                
                # Se for vendedor ou comprador, solicite o CNPJ
                cnpj = cadastro_usuario.cnpj.data  # Certifique-se de adicionar o campo CNPJ ao seu formulário HTML

                # Consulta SQL para obter o ID da empresa com base no CNPJ
                cursor.execute("SELECT ID_Empresa FROM EMPRESA WHERE CNPJ = ?;", [cnpj])
                row = cursor.fetchone()

                if row:
                    # Se a empresa com o CNPJ existir, obtenha o ID_Empresa
                    id_empresa = row[0]
                else:
                    # Se a empresa com o CNPJ não existir, defina o ID_Empresa como None
                    id_empresa = None
            else:
                # Se não for vendedor ou comprador, defina o ID_Empresa como None
                id_empresa = None

            
            if request.method == 'POST' and 'submit_cep':
                    cep = endereco.cep.data
                    response = request.get(f"https://viacep.com.br/ws/{cep}/json/")
                    data = response.json()

                    if "erro" not in data:
                        rua = data['logradouro']
                        bairro = data['bairro']
                        cidade = data['localidade']
                        uf = data['uf']
                    else:
                        rua, bairro, cidade, uf = None, None, None, None
                        # Você pode adicionar uma mensagem flash aqui para informar que o CEP não foi encontrado

            complemento = endereco.complemento.data
            # Gerar hashes de senha e outros campos sensíveis
            senha =  bcrypt.generate_password_hash(hash_senha).decode('utf-8')
            data_nascimento = cadastro_usuario.data_nascimento.data
            data_cadastro = date.today()
            rg = cadastro_usuario.rg.data
            
            # Inserir dados de endereço na tabela 'ENDERECO' e obter o 'ID_Endereco' gerado
            cursor.execute("INSERT INTO ENDERECO (Rua, Bairro, Cidade, UF, CEP, Complemento) VALUES (?, ?, ?, ?, ?, ?);", [rua, bairro, cidade, uf, cep, complemento])
            cnxn.commit()

            # Obter o ID_Endereco gerado na inserção anterior
            cursor.execute("SELECT @@IDENTITY;")
            id_endereco = cursor.fetchone()[0]
            # Inserir dados do funcionário na tabela 'USUARIO_funcionario' com o ID_Endereco correto
            cursor.execute("INSERT INTO USUARIO_funcionario (CPF, NomeSocial, Nome, Sobrenome, Genero, ID_Endereco, Telefone, Email, Senha, Tipo, Data_de_nascimento, RG, Data_Cadastro, ID_Empresa) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", [cpf, nomesocial, nome, sobrenome, genero, id_endereco, telefone, email, senha, tipo, data_nascimento, rg, data_cadastro, id_empresa])
            cnxn.commit()
            cursor.close()
            cnxn.close()
            
            flash('Seu cadastro foi realizado com sucesso!')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Ocorreu um erro ao cadastrar! Entre em contato com o suporte: adm@admin.com')
            print(str(e))
            print('foi erro de exception2')
    return render_template('cadastro_usuario.html', titulo='Cadastro', cadastro_usuario=cadastro_usuario, endereco=endereco)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        entrada = request.form.get('entrada')
        senha = request.form.get('senha')
        user = None

        cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()

        # Consulta SQL para verificar se o e-mail pertence a um usuário comum
        cursor.execute("SELECT * FROM USUARIO_funcionario WHERE CPF = ?;", [entrada])
        user_data2 = cursor.fetchone()

        # Se não for um usuário comum, verifique se é uma empresa
        if user_data2 is None:
            cursor.execute("SELECT * FROM EMPRESA WHERE CNPJ = ?;", [entrada])
            user_data = cursor.fetchone()
            if user_data:
                user = CadastroEmpresa()
                user.id_empresa = user_data.ID_Empresa
                user.cnpj = user_data.CNPJ
                user.nome = user_data.Nome
                user.nomefantasia = user_data.NomeFantasia
                user.email = user_data.Email
                user.razaosocial = user_data.RazaoSocial
                user.senha = user_data.Senha

        # Se o e-mail pertence a um usuário comum
        elif user_data2:
            user = CadastroUsuario()
            user.id_usuario = user_data2.ID_Usuario
            user.cpf = user_data2.CPF
            user.nome = user_data2.Nome
            user.email = user_data2.Email
            user.sobrenome = user_data2.Sobrenome
            user.senha = user_data2.Senha

        cursor.close()
        cnxn.close()

        if check_password_hash(user.senha, senha):
            login_user(user)
            flash('Seja bem-vindo')
            return redirect(url_for('index'))
        else:
            flash('Senha ou e-mail incorreto!')
    return render_template('login.html', titulo='Login')
@app.route('/sair')
@login_required
def sair():
    #Use a função logout_user() para fazer logout do usuário
    logout_user()
    flash('Você foi desconectado com sucesso.')
    return redirect(url_for('index'))  # Redirecione para a página de login ou outra página desejada após o logout


@app.route('/editar_usuario', methods=['POST', 'GET'])
@login_required
def editar_usuario():
    # Função para obter o usuário da sessão
    # Função para obter o usuário da sessão
    def get_user_from_session():
        if 'user' in session:
            return session['user']
        return None

    # Função para atualizar o usuário na sessão
    def update_user_in_session(usuario):
        session['user'] = usuario
        try:
            cnxn = pyodbc.connect(connection_string)
            cursor = cnxn.cursor()

            senha_atual = request.form.get('senha_atual')
            nova_senha = request.form.get('nova_senha')

            # Recupere o usuário atual da sessão
            # Certifique-se de que você já tem o usuário logado e as informações armazenadas na sessão
            # Isso pode depender de como você gerencia a autenticação no seu aplicativo
            usuario = get_user_from_session()  # Implemente esta função para obter o usuário atual da sessão

            if check_password_hash(usuario.senha, senha_atual):
                usuario.nome = request.form.get('nome')
                usuario.nomesocial = request.form.get('nomesocial')
                usuario.sobrenome = request.form.get('sobrenome')
                usuario.email = request.form.get('email')
                usuario.uf = request.form.get('uf')
                usuario.cpf = request.form.get('cpf')
                usuario.cep = request.form.get('cep')
                usuario.rua = request.form.get('rua')
                usuario.bairro = request.form.get('bairro')
                usuario.cidade = request.form.get('cidade')
                usuario.telefone = request.form.get('telefone')

                if nova_senha:
                    usuario.senha = bcrypt.generate_password_hash(nova_senha).decode('utf-8')

                # Atualize os dados do usuário no SQL Server
                cursor.execute("UPDATE USUARIO_funcionario SET Nome = ?, NomeSocial = ?, Sobrenome = ?, Email = ?, UF = ?, CPF = ?, CEP = ?, Rua = ?, Bairro = ?, Cidade = ?, Telefone = ?, Senha = ? WHERE ID_Usuario = ?;",
                               [usuario.nome, usuario.nomesocial, usuario.sobrenome, usuario.email, usuario.uf, usuario.cpf, usuario.cep, usuario.rua, usuario.bairro, usuario.cidade, usuario.telefone, usuario.senha, usuario.id])

                cnxn.commit()

                # Atualize os dados na sessão
                update_user_in_session(usuario)

                flash('Seus dados foram atualizados com sucesso!')
                return redirect(url_for('index'))
            else:
                flash('Senha atual incorreta!')

        except Exception as e:
            flash('Ocorreu um erro ao atualizar seus dados. Entre em contato com o suporte: adm@admin.com')
            print(str(e))
            print('Foi um erro de exceção')

    return render_template('editar_usuario.html', titulo='Editar')



@app.route('/editar_empresa', methods=['POST', 'GET'])
@login_required
def editar_empresa():
    if request.method == 'POST':
        try:
            cnxn = pyodbc.connect(connection_string)
            cursor = cnxn.cursor()

            senha_atual = request.form.get('senha_atual')
            nova_senha = request.form.get('nova_senha')

            # Recupere o usuário atual da sessão
            # Certifique-se de que você já tem o usuário logado e as informações armazenadas na sessão
            # Isso pode depender de como você gerencia a autenticação no seu aplicativo
            usuario = current_user # Implemente esta função para obter o usuário atual da sessão

            if check_password_hash(usuario.senha, senha_atual):
                usuario.cnpj = request.form.get('nome')
                usuario.nome = request.form.get('sobrenome')
                usuario.email = request.form.get('email')
                usuario.razaosocial = request.form.get('razaosocial')
                usuario.nomefantasia = request.form.get('nomefantasia')
                usuario.uf = request.form.get('uf')
                usuario.cep = request.form.get('cep')
                usuario.rua = request.form.get('rua')
                usuario.bairro = request.form.get('bairro')
                usuario.cidade = request.form.get('cidade')
                usuario.telefone = request.form.get('telefone')


                if nova_senha:
                    usuario.senha = bcrypt.generate_password_hash(nova_senha).decode('utf-8')

                usuario.endereco_rua = request.form.get('endereco_rua')
                usuario.endereco_bairro = request.form.get('endereco_bairro')
                usuario.endereco_cidade = request.form.get('endereco_cidade')
                usuario.endereco_uf = request.form.get('endereco_uf')
                usuario.cadastro_empresa_cnpj = request.form.get('cadastro_empresa_cnpj')

                usuario.cadastro_empresa_nome = request.form.get('cadastro_usuario_nome')
                usuario.cadastro_empresa_noemfantasia = request.form.get('cadastro_empresa_nomefantasia')
                usuario.cadastro_empresa_razaosocial = request.form.get('cadastro_empresa_razaosocial')
                usuario.cadastro_empresa_email = request.form.get('cadastro_usuario_email')
                usuario.cadastro_empresa_telefone = request.form.get('cadastro_usuario_email')

                # Atualize os dados do usuário no SQL Server
                cursor.execute("UPDATE USUARIO_funcionario SET Nome = ?, Sobrenome = ?, Email = ?, Senha = ?, Rua = ?, Bairro = ?, Cidade = ?, UF = ? WHERE ID_Usuario = ?;", 
                               [usuario.nome, usuario.nomefantasia, usuario.razaosocial, usuario.telefone, usuario.email, usuario.senha, usuario.cnpj, usuario.endereco_rua, usuario.endereco_bairro, usuario.endereco_cidade, usuario.endereco_uf, usuario.id])

                cnxn.commit()

                # Atualize os dados na sessão

                flash('Seus dados foram atualizados com sucesso!')
                return redirect(url_for('/'))
            else:
                flash('Senha atual incorreta!')

        except Exception as e:
            flash('Ocorreu um erro ao atualizar seus dados. Entre em contato com o suporte: adm@admin.com')
            print(str(e))
            print('Foi um erro de exceção')

    return render_template('editar_usuario.html', titulo='Editar')




@app.route('/excluir_conta', methods=['GET'])
def excluir_conta():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = CadastroModel.query.filter_by(email = session['email']).first()
    db.session.delete(usuario)
    db.session.commit()
    session.clear()

    flash('Sua conta foi excluida com sucesso!')
    return redirect(url_for('cadastro'))



@app.route('/faq')
def faq():
    return render_template('faq.html', title = 'FAQ')


@app.route('/rec_senha')
def rec_senha():
    return render_template('rec_senha.html', title = 'Recuperação de senha')


@app.route('/ecopainel')
def ecopainel():
    return render_template('ecopainel.html', title = 'Graficos')


@app.route('/esqueceu_senha', methods=['GET', 'POST'])
def esqueceu_senha():    
    return render_template('esqueceu_senha.html', titulo='Esqueceu a Senha')