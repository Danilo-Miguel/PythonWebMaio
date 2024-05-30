from flask import Flask, render_template, g, flash, url_for, request, redirect, abort, session
import sqlite3
DATABASE = "banco.bd"
SECRET_KEY = "1234"
app = Flask("Olá")
# Carrega as configurações especificas da aplicação
app.config.from_object(__name__)

# Função para realizar a conexão com o banco de dados
def conectar():
    return sqlite3.connect(DATABASE)
# Função para executar a conexão com o banco de dados
@app.before_request
def before_request():
    g.bd = conectar()  
# Função para encerrar a conexão com o banco de dados
@app.teardown_request   
def teardown_request(f):
    g.bd.close()

@app.route("/login", methods=["POST", "GET"])    
def login():
    erro = None
    if(request.method == "POST"):
        if request.form['username'] == "Ocean" and request.form['password']=="1234":
            session['logado'] = True 
            flash("Usuario logado" + request.form['username'])
            return redirect(url_for('exibir_posts'))
        erro = "Usuario ou senha incorretos"
    return render_template("login.html", erro=erro)


@app.route('/logout')
def logout():
    session.pop('logado', None)
    flash("Logout Efetuado")
    return redirect(url_for('exibir_posts'))


@app.route('/inserir', methods=['POST', 'GET'])
def inserir():
    if not session.get('logado'):
        abort(401)
    titulo = request.form.get('titulo')
    texto = request.form.get('texto')
    sql = "INSERT INTO posts(titulo, texto) VALUES(?, ?)"
    g.bd.execute(sql,[titulo,texto])
    g.bd.commit()
    flash('Novo post inserido')
    return redirect(url_for('exibir_posts'))

    

# Função para a crição da rota de exinição de post e busca dos post na tabela
@app.route('/')
def exibir_posts():
    sql = "SELECT titulo, texto, data_criacao from posts ORDER BY id DESC"
    resultado = g.bd.execute(sql)
    posts = []
    for titulo, texto, data_criacao in resultado.fetchall():
        posts.append({
          "titulo": titulo,
          "texto": texto,
          "data_criacao": data_criacao  
        })
    return render_template('exibir_posts.html', post = posts)