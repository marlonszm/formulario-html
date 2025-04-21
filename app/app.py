import json
import re
from flask import Flask, request, render_template

app = Flask(__name__)

def carregar_usuarios():
    with open('users.json', 'r') as f:
        return json.load(f)

def salvar_usuario(usuario):
    usuarios = carregar_usuarios()
    usuarios.append(usuario)
    with open('users.json', 'w') as f:
        json.dump(usuarios, f)

def validar_usuario(email, senha):
    usuarios = carregar_usuarios()
    for usuario in usuarios:
        if usuario['email'] == email and usuario['senha'] == senha:
            return usuario
    return None

def checar_permissao(usuario, acao):
    permissoes_rbac = {
        "admin": ["ver_todos_os_dados", "modificar"],
        "usuario": ["ver_ativos"]
    }

    permissoes_abac = {
        "ver_todos_os_dados": lambda u: u["idade"] > 30 and u["departamento"] == "TI",
        "ver_ativos": lambda u: u["localizacao"] == "São Paulo"
    }

    role = usuario.get("role", "")
    if acao in permissoes_rbac.get(role, []) and permissoes_abac.get(acao, lambda u: False)(usuario):
        return True
    return False

def obter_mensagem_permissao(role):
    mensagens = {
        "admin": "Bem-vindo, Admin! Você tem acesso total ao sistema.",
        "usuario": "Cadastro realizado com sucesso! Você tem acesso limitado.",
    }
    return mensagens.get(role, "Cadastro realizado com sucesso!")

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/cadastro', methods=['POST'])
def cadastro():
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')

    if len(nome) < 3:
        return "O nome deve ter pelo menos 3 caracteres.", 400

    regex_email = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    if not re.match(regex_email, email):
        return "E-mail inválido.", 400

    regex_senha = r'^(?=.*[A-Z])(?=.*\d).{8,}$'
    if not re.match(regex_senha, senha):
        return "A senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula e um número.", 400

    role = "usuario" 

    usuario = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "role": role,
    }

    salvar_usuario(usuario)

    mensagem = obter_mensagem_permissao(role)

    return mensagem, 200

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')

    usuario = validar_usuario(email, senha)
    if not usuario:
        return "Credenciais inválidas", 401

    if checar_permissao(usuario, "ver_todos_os_dados"):
        return f"Bem-vindo {usuario['nome']} (admin TI com idade > 30) – Acesso total autorizado!"
    elif checar_permissao(usuario, "ver_ativos"):
        return f"Bem-vindo {usuario['nome']} – Acesso parcial autorizado!"
    else:
        return "Acesso negado. Requisitos de acesso não atendidos.", 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
