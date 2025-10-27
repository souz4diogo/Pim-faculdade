import json
import os
from models import Aluno, Professor, Coordenador

ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_CONTEUDOS = "conteudos.json"
ARQUIVO_DISCIPLINAS = "disciplinas.json"

def carregar_usuarios():
    if not os.path.exists(ARQUIVO_USUARIOS):
        return []
    with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
        data = json.load(f)
        usuarios = []
        for d in data:
            tipo = d["tipo"]
            if tipo == "aluno":
                usuarios.append(Aluno.from_dict(d))
            elif tipo == "professor":
                usuarios.append(Professor.from_dict(d))
            elif tipo == "coordenador":
                usuarios.append(Coordenador.from_dict(d))
        return usuarios


def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump([u.to_dict() for u in usuarios], f, indent=4, ensure_ascii=False)

def salvar_disciplinas(disciplinas):
    """Salva a lista de disciplinas no arquivo JSON."""
    with open(ARQUIVO_DISCIPLINAS, "w", encoding="utf-8") as f:
        json.dump(disciplinas, f, indent=4, ensure_ascii=False)

    
def carregar_disciplinas():
    """Carrega disciplinas do arquivo JSON."""
    if os.path.exists(ARQUIVO_DISCIPLINAS):
        with open(ARQUIVO_DISCIPLINAS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_conteudos(conteudos):
    with open(ARQUIVO_CONTEUDOS, "w", encoding="utf-8") as f:
        json.dump(conteudos, f, indent=4, ensure_ascii=False)

def carregar_conteudos():
    if os.path.exists(ARQUIVO_CONTEUDOS):
        with open(ARQUIVO_CONTEUDOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []