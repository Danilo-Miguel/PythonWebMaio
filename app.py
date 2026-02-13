# Importação de módulos necessários do Flask para gerenciar requisições HTTP
# render_template: renderizar templates HTML
# g: objeto global para armazenar dados da requisição
# flash: exibir mensagens ao usuário
# url_for: gerar URLs das rotas
# request: acessar dados da requisição HTTP
# redirect: redirecionar para outra rota (Status HTTP 302)
# abort: gerar respostas de erro HTTP (Ex: 401, 404)
# session: armazenar dados do usuário logado
from flask import Flask, render_template, g, flash, url_for, request, redirect, abort, session
import sqlite3

# Configuração do nome do banco de dados
DATABASE = "banco.bd"
# Chave secreta para sessões e segurança
SECRET_KEY = "1234"
# Inicializa a aplicação Flask
app = Flask("Olá")
# Carrega as configurações especificas da aplicação
app.config.from_object(__name__)

# Função para realizar a conexão com o banco de dados SQLite
# Retorna: conexão com o banco de dados
def conectar():
    return sqlite3.connect(DATABASE)

# Decorador que executa a função antes de cada requisição HTTP
# Cria a conexão com o banco de dados
@app.before_request
def before_request():
    # Armazena a conexão do banco de dados no contexto global (g)
    g.bd = conectar()  

# Decorador que executa a função após encerrar a requisição HTTP
# Fecha a conexão com o banco de dados
@app.teardown_request   
def teardown_request(f):
    # Encerra a conexão com o banco de dados
    g.bd.close()


# Rota para login com métodos POST e GET
# GET: exibe o formulário de login
# POST: processa o login do usuário
@app.route("/login", methods=["POST", "GET"])    
def login():
    # Variável para armazenar mensagens de erro
    erro = None
    # Validação se a requisição é POST (envio de dados do formulário)
    if(request.method == "POST"):
        # Verifica credenciais: username "Ocean" e password "1234"
        if request.form['username'] == "Ocean" and request.form['password']=="1234":
            # Define a sessão como logada (armazenado no cliente)
            session['logado'] = True 
            # Exibe mensagem de sucesso (Status HTTP 200)
            flash("Usuario logado" + request.form['username'])
            # Redireciona para a página inicial (Status HTTP 302 - Redirect)
            return redirect(url_for('exibir_posts'))
        # Define mensagem de erro se credenciais estiverem incorretas
        erro = "Usuario ou senha incorretos"
    # Renderiza o template de login com possível mensagem de erro (Status HTTP 200 - OK)
    return render_template("login.html", erro=erro)

# Rota para logout do usuário
# Remove a sessão do usuário e redireciona
@app.route('/logout')
def logout():
    # Remove a chave 'logado' da sessão (desconecta o usuário)
    session.pop('logado', None)
    # Exibe mensagem de sucesso (Status HTTP 200)
    flash("Logout Efetuado")
    # Redireciona para a página inicial (Status HTTP 302 - Redirect)
    return redirect(url_for('exibir_posts'))

# Rota para inserir novo post
# Métodos POST e GET
@app.route('/inserir', methods=['POST', 'GET'])
def inserir():
    # Verifica se o usuário está logado
    # Se não estiver logado, retorna Status HTTP 401 - Unauthorized
    if not session.get('logado'):
        abort(401)
    # Obtém o título do formulário (POST)
    titulo = request.form.get('titulo')
    # Obtém o texto do formulário (POST)
    texto = request.form.get('texto')
    # SQL para inserir novo post na tabela 'posts'
    sql = "INSERT INTO posts(titulo, texto) VALUES(?, ?)"
    # Executa a query SQL com os dados do formulário
    g.bd.execute(sql,[titulo,texto])
    # Confirma a transação no banco de dados
    g.bd.commit()
    # Exibe mensagem de sucesso (Status HTTP 200)
    flash('Novo post inserido')
    # Redireciona para a página inicial (Status HTTP 302 - Redirect)
    return redirect(url_for('exibir_posts'))

    
# Rota para exibir todos os posts
# Função para a criação da rota de exibição de posts e busca dos posts na tabela
@app.route('/')
def exibir_posts():
    # SQL para selecionar todos os posts ordenados por ID em ordem decrescente (mais recentes primeiro)
    sql = "SELECT titulo, texto, data_criacao from posts ORDER BY id DESC"
    # Executa a query no banco de dados
    resultado = g.bd.execute(sql)
    # Lista vazia para armazenar os posts processados
    posts = []
    # Itera sobre todos os resultados da query
    for titulo, texto, data_criacao in resultado.fetchall():
        # Adiciona cada post como um dicionário na lista
        posts.append({
          "titulo": titulo,
          "texto": texto,
          "data_criacao": data_criacao  
        })
    # Renderiza o template HTML com os posts (Status HTTP 200 - OK)
    return render_template('exibir_posts.html', post = posts)