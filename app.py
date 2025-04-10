from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash
from markupsafe import escape
import re

app = Flask(__name__)

@app.after_request
def aplicar_csp(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self';"
    return response

@app.route('/')
def formulario():
    return render_template('form.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    nome = escape(request.form.get('nome', '').strip())
    email = escape(request.form.get('email', '').strip())
    senha = request.form.get('senha', '').strip()

    erros = []

    if len(nome) < 3:
        erros.append("Nome deve ter pelo menos 3 caracteres.")
    
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        erros.append("E-mail inválido.")
    
    if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', senha):
        erros.append("Senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula e um número.")

    if erros:
        return "<br>".join(erros), 400

    senha_hash = generate_password_hash(senha)

    return "<span style='color: green;'>Cadastro realizado com sucesso!</span>"

if __name__ == '__main__':
    app.run(debug=True)
