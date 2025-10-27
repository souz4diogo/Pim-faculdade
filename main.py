from persistencia import carregar_usuarios, carregar_disciplinas
from autenticacao import autenticar
from gerenciamento import criar_conta_aluno, criar_primeiro_coordenador
from paineis import painel_aluno, painel_professor, painel_coordenador


def main():
    usuarios = carregar_usuarios()
    disciplinas = carregar_disciplinas()

    
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
                    painel_professor(usuario, usuarios)
                elif usuario.tipo == "coordenador":
                    painel_coordenador(usuario, usuarios, disciplinas)
        elif opc == "2":
            criar_conta_aluno(usuarios, disciplinas)
        elif opc == "3":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()