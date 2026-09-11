from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Chave secreta obrigatória para usar sessões no Flask
app.secret_key = 'chave_secreta_restaurar_fc'

# Configuração do Banco de Dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo da Tabela de Usuários
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()

# Rota Inicial / Home
@app.route("/")
def inicio():
    return render_template("inicio.html")

# Rota para a tela de Login
@app.route("/login")
def login():
    return render_template("login.html")

# Rota para processar o Login
@app.route("/autenticar", methods=["POST"])
def autenticar():
    email = request.form["email"]
    senha = request.form["senha"]
    
    usuario = Usuario.query.filter_by(email=email, senha=senha).first()
    
    if usuario:
        # Salva o nome e o email na sessão do Flask
        session['nome'] = usuario.nome
        session['email'] = usuario.email
        return redirect(url_for("painel"))
    else:
        return render_template("login.html", erro="E-mail ou senha incorretos!")

# Rota para a tela de Cadastro
@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

# Rota para processar o Cadastro
@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form["nome"]
    email = request.form["email"]
    senha = request.form["senha"]
    tipo = request.form["tipo"]
    
    # Verifica se o e-mail já existe
    usuario_existente = Usuario.query.filter_by(email=email).first()
    if usuario_existente:
        return render_template("cadastro.html", erro="Este e-mail já está cadastrado!")
    
    novo_usuario = Usuario(nome=nome, email=email, senha=senha, tipo=tipo)
    db.session.add(novo_usuario)
    db.session.commit()
    
    return redirect(url_for("login"))

# Rota do Painel Restrito
@app.route("/painel")
def painel():
    # Verifica se o usuário está logado pela sessão
    if 'nome' not in session:
        return redirect(url_for('login'))
    
    # Puxa o nome salvo na sessão para enviar ao HTML
    return render_template("restaurar.html", nome=session.get('nome'))

# Rota de Logout (Sair)
@app.route("/logout")
def logout():
    session.clear() # Limpa a sessão
    return redirect(url_for('inicio'))

if __name__ == "__main__":
    app.run(debug=True)
