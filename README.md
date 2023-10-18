# Projeto Flask Iniciante

Este é um projeto Flask simples e direcionado a iniciantes que desejam aprender sobre o desenvolvimento de aplicativos web usando Python e o framework Flask. O objetivo principal deste projeto é fornecer uma base sólida para quem está começando a explorar o mundo do desenvolvimento web e quer construir uma aplicação web funcional e interativa.

## Funcionalidades

O projeto de iniciante do Flask incluirá as seguintes funcionalidades básicas:

    1. Página Inicial: Uma página inicial amigável com informações sobre o projeto e sua finalidade.
    2. Página de Contato: Uma página de contato com um formulário simples para que os usuários possam enviar mensagens.
    3. Armazenamento de Mensagens: A capacidade de armazenar as mensagens enviadas através do formulário de contato e exibi-las em uma página de mensagens recebidas.
    4. Layout Responsivo: O projeto será desenvolvido com um layout responsivo, garantindo uma experiência de usuário agradável tanto em dispositivos móveis quanto em computadores.

## Requisitos

Os requisitos para executar o projeto são:

    • Python==3.11.4
    • blinker==1.6.2
    • click==8.1.6
    • colorama==0.4.6
    • Flask==2.3.2
    • itsdangerous==2.1.2
    • Jinja2==3.1.2
    • MarkupSafe==2.1.3
    • Werkzeug==2.3.6

## Objetivos de Aprendizagem

Tem a inteção de capacitar o aluno a:

    • Configurar e iniciar um projeto Flask básico.
    • Criar rotas (endpoints) para diferentes páginas da aplicação.
    • Criar e renderizar templates HTML usando o Jinja2 (o mecanismo de template do Flask).
    • Entender a estrutura básica de um aplicativo web e a troca de informações entre o cliente e o servidor.
    • Implementar formulários HTML e processá-los no lado do servidor.
    • Armazenar dados de forma simples (por exemplo, em uma lista ou em memória) e exibi-los em diferentes páginas.
    • Desenvolver um layout responsivo com CSS básico para uma experiência amigável em diversos dispositivos.

## Instruções

Para configuração e instalação do ambiente de desenvolvimento basta baixar o arquivo "requirements.txt", colocar numa pasta dedicada ao projeto e executar o comando:
    
    pip install -r requirements.txt

Caso venha a fazer alguma alteração no código execute o comando:
    
    pip freeze > requirements.txt

No terminal, na pasta do seu projeto, execute o seguinte comando para criar uma pasta para as migrações:

    flask db init

Isso criará uma pasta chamada migrations onde as migrações serão armazenadas. Agora você pode usar o seguinte comando para gerar uma migração baseada nos modelos que você definiu:

    flask db migrate -m "Nome da Migração"

Sempre que você fizer alterações em seus modelos e quiser aplicar as migrações pendentes ao banco de dados.

 flask db upgrade

