import json
import re

def carregar_usuarios():
    with open('users.json', 'r') as f:
        return json.load(f)

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
