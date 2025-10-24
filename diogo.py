import json, hashlib, getpass, os

ARQUIVO_CONTAS = "usuarios.json"
ARQUIVO_AULAS = "aulas.json"
ARQUIVO_PROVAS = "provas.json"


# ========== CLASSES ==========
class Usuario:
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    def to_dict(self):
        return {
            "nome": self.nome,
            "email": self.email,
            "senha_hash": self.senha_hash,
            "tipo": self.__class__.__name__
        }


class Aluno(Usuario):
    def __init__(self, nome, email, senha, disciplina, turma):
        super().__init__(nome, email, senha)
        self.disciplina = disciplina
        self.turma = turma
        self.notas = {}

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "disciplina": self.disciplina,
            "turma": self.turma,
            "notas": self.notas
        })
        return base


class Professor(Usuario):
    def __init__(self, nome, email, senha, disciplina):
        super().__init__(nome, email, senha)
        self.disciplina = disciplina

    def to_dict(self):
        base = super().to_dict()
        base.update({"disciplina": self.disciplina})
        return base


class Coordenador(Usuario):
    def __init__(self, nome, email, senha):
        super().__init__(nome, email, senha)

def carregar_json(caminho, padrao):
    if not os.path.exists(caminho):
        return padrao
    with open(caminho, "r", encoding="utf-8") as arq:
        return json.load(arq)

def salvar_json(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as arq:
        json.dump(dados, arq, indent=4, ensure_ascii=False)

def autenticar():
    contas = carregar_json(ARQUIVO_CONTAS, [])
    email = input("Email: ").strip()
    senha = getpass.getpass("Senha: ").strip()
    hash_senha = hashlib.sha256(senha.encode()).hexdigest()

    for c in contas:
        if c["email"].lower() == email.lower() and c["senha_hash"] == hash_senha:
            print(f"✅ Login bem-sucedido ({c['tipo']}).")
            return c
    print("❌ Email ou senha incorretos.")
    return None


def criar_conta():
    contas = carregar_json(ARQUIVO_CONTAS, [])

    # Primeiro usuário sempre coordenador
    if not contas:
        print("🛠️ Criando coordenador inicial:")
        nome = input("Nome: ").strip()
        email = input("Email: ").strip()
        senha = getpass.getpass("Senha: ").strip()
        novo = Coordenador(nome, email, senha)
        contas.append(novo.to_dict())
        salvar_json(ARQUIVO_CONTAS, contas)
        print("✅ Coordenador criado.")
        return novo.to_dict()

    print("🧑 Cadastro de Aluno:")
    nome = input("Nome: ").strip()
    email = input("Email: ").strip()
    senha = getpass.getpass("Senha: ").strip()
    disciplina = input("Disciplina: ").strip()
    turma = gerar_turma(disciplina, contas)

    novo = Aluno(nome, email, senha, disciplina, turma)
    contas.append(novo.to_dict())
    salvar_json(ARQUIVO_CONTAS, contas)
    print(f"✅ Aluno cadastrado na turma {turma}.")
    return novo.to_dict()

def gerar_turma(disciplina, contas):
    alunos = [c for c in contas if c["tipo"] == "Aluno" and c.get("disciplina") == disciplina]
    num_turmas = len(alunos) // 30 + 1
    return f"{disciplina}{num_turmas}"

def main():
    print("=== Sistema Educacional ===")
    conta = None
    while not conta:
        print("\n1. Login\n2. Criar Conta\n3. Sair")
        esc = input("Opção: ").strip()
        if esc == "1":
            conta = autenticar()
        elif esc == "2":
            conta = criar_conta()
        elif esc == "3":
            print("Até logo!")
            return
        else:
            print("Opção inválida.")
    abrir_painel(conta)

def abrir_painel(conta):
    tipo = conta["tipo"]
    if tipo == "Coordenador":
        painel_coordenador(conta)
    elif tipo == "Professor":
        painel_professor(conta)
    elif tipo == "Aluno":
        painel_aluno(conta)

def painel_coordenador(conta):
    while True:
        print(f"\n🔹 Painel do Coordenador ({conta['nome']})")
        print("1. Adicionar Professor")
        print("2. Listar Usuários")
        print("3. Sair")
        esc = input("Opção: ").strip()

        if esc == "1":
            adicionar_professor()
        elif esc == "2":
            listar_usuarios()
        elif esc == "3":
            break
        else:
            print("Opção inválida.")

def painel_professor(conta):
    while True:
        print(f"\n👨‍🏫 Painel do Professor ({conta['nome']})")
        print("1. Adicionar Aula")
        print("2. Criar Prova")
        print("3. Sair")
        esc = input("Opção: ").strip()

        if esc == "1":
            adicionar_aula(conta)
        elif esc == "2":
            criar_prova(conta)
        elif esc == "3":
            break
        else:
            print("Opção inválida.")

def painel_aluno(conta):
    while True:
        print(f"\n🎓 Painel do Aluno ({conta['nome']}) - Turma {conta['turma']}")
        print("1. Ver Aulas")
        print("2. Fazer Prova")
        print("3. Ver Notas")
        print("4. Sair")
        esc = input("Opção: ").strip()

        if esc == "1":
            ver_aulas(conta)
        elif esc == "2":
            fazer_prova(conta)
        elif esc == "3":
            ver_notas(conta)
        elif esc == "4":
            break
        else:
            print("Opção inválida.")

def adicionar_professor():
    contas = carregar_json(ARQUIVO_CONTAS, [])
    nome = input("Nome do professor: ").strip()
    email = input("Email: ").strip()
    senha = getpass.getpass("Senha inicial: ").strip()
    disciplina = input("Disciplina: ").strip()

    novo = Professor(nome, email, senha, disciplina)
    contas.append(novo.to_dict())
    salvar_json(ARQUIVO_CONTAS, contas)
    print("✅ Professor adicionado com sucesso.")


def listar_usuarios():
    contas = carregar_json(ARQUIVO_CONTAS, [])
    for c in contas:
        print(f"- {c['tipo']}: {c['nome']} ({c['email']})")

def adicionar_aula(conta):
    aulas = carregar_json(ARQUIVO_AULAS, [])
    titulo = input("Título da aula: ").strip()
    conteudo = input("Conteúdo da aula: ").strip()

    nova_aula = {
        "disciplina": conta["disciplina"],
        "professor": conta["nome"],
        "titulo": titulo,
        "conteudo": conteudo
    }
    aulas.append(nova_aula)
    salvar_json(ARQUIVO_AULAS, aulas)
    print("✅ Aula adicionada.")


def criar_prova(conta):
    provas = carregar_json(ARQUIVO_PROVAS, [])
    titulo = input("Título da prova: ").strip()
    questoes = []

    for i in range(1, 11):
        print(f"\nQuestão {i}:")
        enunciado = input("Pergunta: ").strip()
        alternativas = [input(f"Alternativa {x}: ").strip() for x in ["A", "B", "C", "D"]]
        correta = input("Alternativa correta (A/B/C/D): ").upper()
        questoes.append({
            "pergunta": enunciado,
            "alternativas": alternativas,
            "correta": correta
        })

    nova_prova = {
        "titulo": titulo,
        "disciplina": conta["disciplina"],
        "professor": conta["nome"],
        "questoes": questoes,
        "notas": {}
    }
    provas.append(nova_prova)
    salvar_json(ARQUIVO_PROVAS, provas)
    print("✅ Prova criada com sucesso.")

def ver_aulas(conta):
    aulas = carregar_json(ARQUIVO_AULAS, [])
    aulas_filtradas = [a for a in aulas if a["disciplina"] == conta["disciplina"]]
    if not aulas_filtradas:
        print("📭 Nenhuma aula disponível.")
        return
    for aula in aulas_filtradas:
        print(f"\n📘 {aula['titulo']} — Prof: {aula['professor']}\n{aula['conteudo']}\n")


def fazer_prova(conta):
    provas = carregar_json(ARQUIVO_PROVAS, [])
    provas_disp = [p for p in provas if p["disciplina"] == conta["disciplina"]]

    if not provas_disp:
        print("❌ Nenhuma prova disponível.")
        return

    print("\nProvas disponíveis:")
    for i, p in enumerate(provas_disp, 1):
        print(f"{i}. {p['titulo']}")
    esc = int(input("Escolha uma: ")) - 1
    prova = provas_disp[esc]

    acertos = 0
    for q in prova["questoes"]:
        print(f"\n{q['pergunta']}")
        for idx, alt in enumerate(q["alternativas"], start=65):
            print(f"{chr(idx)}) {alt}")
        resp = input("Sua resposta: ").upper().strip()
        if resp == q["correta"]:
            acertos += 1

    nota = acertos
    prova["notas"][conta["email"]] = nota

    # Atualiza no arquivo
    todas = carregar_json(ARQUIVO_PROVAS, [])
    for p in todas:
        if p["titulo"] == prova["titulo"]:
            p["notas"] = prova["notas"]
    salvar_json(ARQUIVO_PROVAS, todas)

    # Atualiza nota do aluno
    contas = carregar_json(ARQUIVO_CONTAS, [])
    for c in contas:
        if c["email"] == conta["email"]:
            c.setdefault("notas", {})[prova["titulo"]] = nota
    salvar_json(ARQUIVO_CONTAS, contas)

    print(f"✅ Prova concluída! Nota: {nota}/10")


def ver_notas(conta):
    if not conta.get("notas"):
        print("📭 Nenhuma nota disponível.")
        return
    for prova, nota in conta["notas"].items():
        print(f"{prova}: {nota}/10")

if __name__ == "__main__":
    main()
