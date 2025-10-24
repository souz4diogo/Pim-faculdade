alunos = []
atividades = []
respostas = []  



#----funcoes do professor----#
def cadastrarAluno():
    while True:
        print("""
        [1] Cadastrar aluno/Turma
        [2] Voltar
        """)
        opcao = input("Digite o número para escolher a opção: ")

        if opcao == "1":
            aluno = input("Digite um login para o aluno: ")
            turma = input("Digite a turma na qual o aluno estará: ")

            alunos.append({"login": aluno, "turma": turma})
            print(f"Aluno {aluno} cadastrado na turma {turma}!\n")

        elif opcao == "2":
            print("Voltando para o menu do Professor...\n")
            break  
        else:
            print("Digite um valor válido\n")


def enviarAtividades():
    while True:
        print("""
        [1] Criar nova atividade
        [2] Voltar
        """)
        opcao = input("Digite a opção: ")

        if opcao == "1":
            descricao = input("Digite o enunciado da atividade: ")
            turma = input("Para qual turma essa atividade é destinada? ")

            atividades.append({"descricao": descricao, "turma": turma})
            print("Atividade cadastrada com sucesso!\n")
        elif opcao == "2":
            print("Voltando para o painel do Professor...\n")
            break
        else:
            print("Opção inválida!\n")


def painelProfessor():
    while True:
        print("""
        [1] Cadastrar Aluno
        [2] Enviar atividade
        [3] Listar alunos
        [4] Listar atividades
        [5] Ver respostas dos alunos
        [6] Sair 
        """)
        opcao = input("Digite o número para escolher a opção: ")

        if opcao == "1":
            cadastrarAluno()
        elif opcao == "2":
            enviarAtividades()
        elif opcao == "3":
            if alunos:
                print("\n=== Alunos cadastrados ===")
                for idx, aluno in enumerate(alunos, start=1):
                    print(f"{idx}. {aluno['login']} - Turma: {aluno['turma']}")
                print()
            else:
                print("Nenhum aluno cadastrado ainda.\n")
        elif opcao == "4":
            if atividades:
                print("\n=== Atividades cadastradas ===")
                for idx, atv in enumerate(atividades, start=1):
                    print(f"{idx}. {atv['descricao']} (Turma: {atv['turma']})")
                print()
            else:
                print("Nenhuma atividade cadastrada ainda.\n")
        elif opcao == "5":
            if respostas:
                print("\n=== Respostas enviadas ===")
                for idx, resp in enumerate(respostas, start=1):
                    print(f"{idx}. {resp['aluno']} (Turma: {resp['turma']}) respondeu: {resp['resposta']}")
                print()
            else:
                print("Nenhuma resposta enviada ainda.\n")
        elif opcao == "6":
            print("Saindo do painel do Professor...")
            break
        else:
            print("Opção inválida, tente novamente!\n")


#------funcoes do aluno----#
def painelAluno(login, turma):
    while True:
        print(f"""
        Bem-vindo {login} da turma {turma}!
        [1] Ver atividades 
        [2] Enviar resposta
        [3] Sair
        """)
        opcao = input("Escolha sua opção: ")

        if opcao == "1":
            print("\n=== Suas atividades ===")
            encontrou = False
            for atv in atividades:
                if atv["turma"] == turma:
                    print(f"- {atv['descricao']}")
                    encontrou = True
            if not encontrou:
                print("Nenhuma atividade para sua turma.\n")

        elif opcao == "2":
            resposta = input("Digite sua resposta: ")
            respostas.append({"aluno": login, "turma": turma, "resposta": resposta})
            print("Resposta enviada com sucesso!\n")

        elif opcao == "3":
            print("Saindo do painel do aluno...\n")
            break
        else:
            print("Opção inválida, tente novamente!\n")


#---------funcoes autenticacao---------#
def painelProfessorAuth():
    while True:
        print("""
        [1] Digitar usuário como professor
        [2] Voltar
        """)
        opcao = input("Escolha sua opção: ")

        if opcao == "1":
            usuario = input("Usuário: ")
            senha = input("Senha: ")
            if usuario == "adm@escolar.com" and senha == "123":
                print("Login realizado com sucesso!\n")
                painelProfessor()  
            else:
                print("Usuário ou senha incorretos!\n")
        elif opcao == "2":
            print("Voltando para o menu principal...\n")
            break  
        else:
            print("Opção inválida, tente novamente!\n")


def painelAlunoAuth():
    while True:
        print("""
        [1] Login
        [2] Sair
        """)
        opcao = input("Escolha sua opção: ")

        if opcao == "1":
            loginAluno = input("Digite seu login como aluno: ")
            turmaAluno = input("Digite sua turma: ")

            encontrado = False
            for aluno in alunos:
                if aluno["login"] == loginAluno and aluno["turma"] == turmaAluno:
                    encontrado = True
                    break

            if encontrado:
                print(f"Login bem-sucedido! Bem-vindo, {loginAluno} da turma {turmaAluno}\n")
                painelAluno(loginAluno, turmaAluno)
            else:
                print("Aluno não encontrado ou turma incorreta!\n")

        elif opcao == "2":
            print("Saindo do painel do aluno...\n")
            break
        else:
            print("Opção inválida, tente novamente!\n")


#-----painel de exibicao-----#
def painelSelecionar():
    while True:  
        print("""
    [1] Professor
    [2] Aluno
    [3] Sair      
        """)
        
        opcao = input("Digite o número para escolher a opção: ")

        if opcao == "1":
            print("Você selecionou Professor\n")
            painelProfessorAuth() 
        elif opcao == "2":
            print("Você selecionou Aluno\n")
            painelAlunoAuth()
        elif opcao == "3":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida, tente novamente!\n")


painelSelecionar()
