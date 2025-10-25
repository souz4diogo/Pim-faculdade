import json
import os
import getpass
import hashlib

ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_CONTEUDOS = "conteudos.json"
ARQUIVO_DISCIPLINAS = "disciplinas.json"

class UsuarioBase:
    def __init__(self, id, nome, email, senha, tipo):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        self.tipo = tipo

    def verificar_senha(self, senha):
        return hashlib.sha256(senha.encode()).hexdigest() == self.senha_hash

    @staticmethod
    def gerar_novo_id(usuarios):
        return max([u.id for u in usuarios], default=0) + 1

    def to_dict(self):
        base = {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "senha_hash": self.senha_hash,
            "tipo": self.tipo
        }
        return base

class Aluno(UsuarioBase):
    def __init__(self, id, nome, email, senha, disciplina, turma):
        super().__init__(id, nome, email, senha, tipo="aluno")
        self.disciplina = disciplina
        self.turma = turma

    def to_dict(self):
        base = super().to_dict()
        base["disciplina"] = self.disciplina
        base["turma"] = self.turma
        return base

    @staticmethod
    def from_dict(d):
        a = Aluno(d["id"], d["nome"], d["email"], "placeholder", d["disciplina"], d.get("turma", ""))
        a.senha_hash = d["senha_hash"]
        return a

class Professor(UsuarioBase):
    def __init__(self, id, nome, email, senha, disciplina, senha_provisoria=False):
        super().__init__(id, nome, email, senha, tipo="professor")
        self.disciplina = disciplina
        self.senha_provisoria = senha_provisoria

    def to_dict(self):
        base = super().to_dict()
        base["disciplina"] = self.disciplina
        base["senha_provisoria"] = self.senha_provisoria
        return base

    @staticmethod
    def from_dict(d):
        p = Professor(d["id"], d["nome"], d["email"], "placeholder", d["disciplina"], d.get("senha_provisoria", False))
        p.senha_hash = d["senha_hash"]
        return p

class Coordenador(UsuarioBase):
    def __init__(self, id, nome, email, senha):
        super().__init__(id, nome, email, senha, tipo="coordenador")

    @staticmethod
    def from_dict(d):
        c = Coordenador(d["id"], d["nome"], d["email"], "placeholder")
        c.senha_hash = d["senha_hash"]
        return c

# função de persistencia, le o arquivo JSON que guarda os usuários e transforma os dados em objetos Python
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

# salvar usuarios em json
def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump([u.to_dict() for u in usuarios], f, indent=4, ensure_ascii=False)



# FUNÇÕES DE NEGÓCIO
def autenticar(usuarios):
    email = input("Email: ").strip()
    senha = getpass.getpass("Senha: ").strip()

    for u in usuarios:
        if u.email.lower() == email.lower() and u.verificar_senha(senha):
            print(f"\n✅ Login bem-sucedido! Bem-vindo(a), {u.nome}.")

            # Se professor estiver com senha provisória, obriga alterar
            if isinstance(u, Professor) and u.senha_provisoria:
                print("⚠️ Você está usando a senha provisória. É obrigatório alterá-la.")
                while True:
                    nova_senha = getpass.getpass("Nova senha: ").strip()
                    confirmar = getpass.getpass("Confirme a nova senha: ").strip()
                    if nova_senha == confirmar:
                        u.senha_hash = hashlib.sha256(nova_senha.encode()).hexdigest()
                        u.senha_provisoria = False
                        salvar_usuarios(usuarios)
                        print("✅ Senha alterada com sucesso!")
                        break
                    print("❌ As senhas não coincidem. Tente novamente.")

            return u

    print("❌ Usuário ou senha incorretos.")
    return None

def criar_conta_aluno(usuarios):
    print("\n=== CADASTRO DE ALUNO ===")
    nome = input("Nome: ").strip()
    email = input("Email: ").strip()

    # Loop para confirmação de senha
    while True:
        senha = getpass.getpass("Senha: ").strip()
        senha_conf = getpass.getpass("Confirme a senha: ").strip()
        if senha == senha_conf:
            break
        print("❌ As senhas não coincidem. Tente novamente.")

    # Escolha da disciplina
    disciplina = escolher_disciplina()
    if disciplina is None:
        print("❌ Cadastro cancelado. Nenhuma disciplina disponível.")
        return None

    # Determinar turma automaticamente (30 alunos por turma)
    alunos_disciplina = [a for a in usuarios if a.tipo == "aluno" and a.disciplina == disciplina]
    turma_num = (len(alunos_disciplina) // 30) + 1
    turma = f"{disciplina}{turma_num}"

    # Gerar ID único
    novo_id = UsuarioBase.gerar_novo_id(usuarios)

    # Criar aluno
    novo = Aluno(novo_id, nome, email, senha, disciplina, turma)
    usuarios.append(novo)
    salvar_usuarios(usuarios)
    print(f"✅ Aluno cadastrado com sucesso na turma {turma}!")
    return novo



def criar_primeiro_coordenador(usuarios):
    print("\n=== CRIAÇÃO DO PRIMEIRO COORDENADOR ===")
    nome = input("Nome: ").strip()
    email = input("Email: ").strip()
    while True:
        senha = getpass.getpass("Senha: ").strip()
        senha_conf = getpass.getpass("Confirme a senha: ").strip()
        if senha == senha_conf:
            break
        print("❌ As senhas não coincidem. Tente novamente.")


    novo_id = UsuarioBase.gerar_novo_id(usuarios)

    # cria o coordenador
    novo = Coordenador(novo_id, nome, email, senha)
    usuarios.append(novo)
    salvar_usuarios(usuarios)
    print("✅ Coordenador criado com sucesso!")
    return novo

# metodo para adicionar professor
def adicionar_professor(usuarios, disciplinas):
    print("\n=== ADICIONAR PROFESSOR ===")
    nome = input("Nome do professor: ").strip()
    email = input("Email: ").strip()
    senha = "professor123"

    if not disciplinas:
        print("❌ Nenhuma disciplina disponível. Crie uma disciplina primeiro.")
        return

    print("Disciplinas disponíveis:")
    for i, d in enumerate(disciplinas, 1):
        print(f"{i}. {d}")
    
    while True:
        try:
            escolha = int(input("Escolha a disciplina pelo número: "))
            if 1 <= escolha <= len(disciplinas):
                disciplina = disciplinas[escolha-1]
                break
            print("Número inválido.")
        except ValueError:
            print("Digite um número válido.")

    novo_id = UsuarioBase.gerar_novo_id(usuarios)
    novo = Professor(novo_id, nome, email, "professor123", disciplina, senha_provisoria=True)
    usuarios.append(novo)
    salvar_usuarios(usuarios)
    print(f"✅ Professor adicionado com sucesso na disciplina {disciplina}!")

def salvar_disciplinas():
    """Salva a lista global de disciplinas no arquivo JSON."""
    global disciplinas
    with open(ARQUIVO_DISCIPLINAS, "w", encoding="utf-8") as f:
        json.dump(disciplinas, f, indent=4, ensure_ascii=False)

# carregar todas disciplinas existentes
def carregar_disciplinas():
    """Carrega disciplinas do arquivo JSON para a lista global."""
    global disciplinas
    if os.path.exists(ARQUIVO_DISCIPLINAS):
        with open(ARQUIVO_DISCIPLINAS, "r", encoding="utf-8") as f:
            disciplinas = json.load(f)
    else:
        disciplinas = []

# criar disciplinas
def criar_disciplina():
    print("\n=== CRIAÇÃO DE DISCIPLINA ===")
    nome = input("Nome da disciplina: ").strip()
    if nome in disciplinas:
        print("❌ Essa disciplina já existe.")
        return
    disciplinas.append(nome)
    salvar_disciplinas()
    print(f"✅ Disciplina '{nome}' criada com sucesso!")

# metodo para escolher disciplina
def escolher_disciplina():
    if not disciplinas:
        print("❌ Nenhuma disciplina disponível. Contate o coordenador.")
        return None

    print("\nDisciplinas disponíveis:")
    for i, d in enumerate(disciplinas, 1):
        print(f"{i}. {d}")
    
    while True:
        try:
            escolha = int(input("Escolha a disciplina pelo número: "))
            if 1 <= escolha <= len(disciplinas):
                return disciplinas[escolha - 1]
            print("Número inválido. Tente novamente.")
        except ValueError:
            print("Digite um número válido.")

def listar_usuarios(usuarios):
    print("\n=== LISTA DE USUÁRIOS ===")
    for u in usuarios:
        info = f"Nome: {u.nome}, Email: {u.email}, Tipo: {u.tipo}"
        if hasattr(u, "disciplina"):
            info += f", Disciplina: {u.disciplina}"
        if hasattr(u, "turma"):
            info += f", Turma: {u.turma}"
        print(info)

def salvar_conteudos(conteudos):
    with open(ARQUIVO_CONTEUDOS, "w", encoding="utf-8") as f:
        json.dump(conteudos, f, indent=4, ensure_ascii=False)

def carregar_conteudos():
    if os.path.exists(ARQUIVO_CONTEUDOS):
        with open(ARQUIVO_CONTEUDOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def adicionar_conteudo(professor, turma):
    conteudos = carregar_conteudos()
    titulo = input("Título da aula: ").strip()
    arquivo = input("Arquivo (PDF): ").strip()

    # Procura se já existe entrada
    for entry in conteudos:
        if entry["professor_id"] == professor.id and entry["disciplina"] == professor.disciplina and entry["turma"] == turma:
            entry["conteudos"].append({"titulo": titulo, "arquivo": arquivo})
            salvar_conteudos(conteudos)
            print("✅ Conteúdo adicionado!")
            return

    # Cria nova entrada
    conteudos.append({
        "professor_id": professor.id,
        "disciplina": professor.disciplina,
        "turma": turma,
        "conteudos": [{"titulo": titulo, "arquivo": arquivo}]
    })
    salvar_conteudos(conteudos)
    print("✅ Conteúdo adicionado!")

def mostrar_conteudos_aluno(aluno):
    conteudos = carregar_conteudos()
    encontrados = False
    print(f"\n📚 Conteúdos para {aluno.nome} ({aluno.turma}, {aluno.disciplina}):\n")
    
    for entry in conteudos:
        if entry["disciplina"] == aluno.disciplina and entry["turma"] == aluno.turma:
            encontrados = True
            for c in entry["conteudos"]:
                print(f"- {c['titulo']} → {c['arquivo']}")
    
    if not encontrados:
        print("❌ Nenhum conteúdo disponível para sua turma ainda.")

# TELAS DE USUÁRIOS
def painel_aluno(aluno):
    while True:
        print(f"\n🎓 Painel do Aluno {aluno.nome} — Turma: {aluno.turma}")
        print("1. Ver conteúdos da turma")
        print("2. Sair")
        opc = input("Opção: ").strip()
        if opc == "1":
            mostrar_conteudos_aluno(aluno)
        elif opc == "2":
            break
        else:
            print("Opção inválida.")


def painel_professor(professor):
    while True:
        print(f"\n📘 Painel do Professor {professor.nome} — Disciplina: {professor.disciplina}")
        print("1. Adicionar conteúdo")
        print("2. Ver meus conteúdos")
        print("3. Sair")
        opc = input("Opção: ").strip()

        if opc == "1":
            # Lista turmas existentes para a disciplina
            turmas = sorted(list({a.turma for a in usuarios if isinstance(a, Aluno) and a.disciplina == professor.disciplina}))
            if not turmas:
                print("❌ Nenhuma turma disponível.")
                continue
            print("Turmas disponíveis:")
            for i, t in enumerate(turmas, 1):
                print(f"{i}. {t}")
            while True:
                try:
                    escolha = int(input("Escolha a turma pelo número: "))
                    if 1 <= escolha <= len(turmas):
                        turma_escolhida = turmas[escolha-1]
                        break
                    print("Número inválido.")
                except ValueError:
                    print("Digite um número válido.")
            adicionar_conteudo(professor, turma_escolhida)

        elif opc == "2":
            conteudos = carregar_conteudos()
            encontrados = False
            print(f"\n📚 Conteúdos do Professor {professor.nome} ({professor.disciplina}):")
            for entry in conteudos:
                if entry["professor_id"] == professor.id:
                    encontrados = True
                    print(f"\nTurma: {entry['turma']}")
                    for c in entry["conteudos"]:
                        print(f"- {c['titulo']} → {c['arquivo']}")
            if not encontrados:
                print("❌ Nenhum conteúdo cadastrado.")

        elif opc == "3":
            break
        else:
            print("Opção inválida.")


def painel_coordenador(usuario, usuarios):
    carregar_disciplinas()  # Carrega disciplinas do JSON
    while True:
        print(f"\n🧩 Painel do Coordenador {usuario.nome}")
        print("1. Criar disciplina")
        print("2. Listar usuários")
        print("3. Adicionar professor")
        print("4. Sair do painel")
        
        opcao = input("Opção: ").strip()
        if opcao == "1":
            criar_disciplina()
        elif opcao == "2":
            listar_usuarios(usuarios)
        elif opcao == "3":
            adicionar_professor(usuarios, disciplinas)
        elif opcao == "4":
            break
        else:
            print("Opção inválida.")





# MENU PRINCIPAL
def main():
    global usuarios, disciplinas
    usuarios = carregar_usuarios()
    carregar_disciplinas()

    # Se não existir nenhum coordenador, criar o primeiro
    if not any(u.tipo == "coordenador" for u in usuarios):
        print("\n🚀 Nenhum coordenador encontrado. Crie o primeiro agora.")
        criar_primeiro_coordenador(usuarios)

    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Login")
        print("2. Cadastrar aluno")
        print("3. Sair")
        opc = input("Opção: ").strip()

        if opc == "1":
            usuario = autenticar(usuarios)
            if usuario:
                if usuario.tipo == "aluno":
                    painel_aluno(usuario)
                elif usuario.tipo == "professor":
                    painel_professor(usuario)
                elif usuario.tipo == "coordenador":
                    painel_coordenador(usuario, usuarios)
        elif opc == "2":
            criar_conta_aluno(usuarios)
        elif opc == "3":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()