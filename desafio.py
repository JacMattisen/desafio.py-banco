import textwrap

def menu():
    menu = """\n
    ================ MENU ================
    [d]\t Depositar
    [s]\t Sacar
    [e]\t Extrato
    [nc]\t Nova conta
    [lc]\t Listar contas
    [nu]\t Novo usuário
    [q]\t Sair
    => """
    return input(textwrap.dedent(menu))

def depositar (saldo, valor, extrato, /):#Lembrando que o / é argumento posicional
    if  valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print ("\n ||| Depósito conluído |||")
    else:
        print("\n !!! FALHA. O valor informado é inválido !!!")

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques): #Forma nomeada é com o * depois dele 
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print ("\n !!! Saldo insuficiente. !!!")

    elif excedeu_limite:
        print("!!! O valor está acima do permitido a ser sacado. !!!")

    elif excedeu_saques:
        print("!!! Número de saques/dia já execederam. !!!")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: \t\tR$ {valor:.2f} \n"
        numero_saques += 1
        print ("\n ||| Saque realizado com sucesso! |||")
    
    else:
        print("\n!!! O valor informado é inválido. !!!")

    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print ("\n ============= EXTRATO ============= ")
    print ("Nao foram realizadas movimentacoes." if not extrato else extrato)
    print (f"\n Saldo: \t\tR$ {saldo:.2f}")
    print("======================================= ")

def criar_usuario(usuarios):
    cpf = input("Informe o seu CPF (SOMENTE números, sem pontos): ")
    usuario = filtrar_usuario (cpf, usuarios)

    if usuario:
        print("\nJá existe usuário com esse CPF. !!!")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereco (rua, numero - bairro - cidade/sigla Estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print ("==== Parabéns! Usuário criado com sucesso! ====")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o seu CPF do usuário: ")
    usuario = filtrar_usuario (cpf, usuarios)

    if usuario:
        print("\n!!! Conta criada com sucesso!. !!!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print ("\n ### Usuário nao encontrado, fluxo de criacao de conta encerrado! ###")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agencia:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print ("=" * 100)
        print (textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = input(menu)
    
        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar (saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor de saque: "))
        
            saldo, extrato = sacar (
                saldo=saldo, #lembrando que sao Keyword only
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )
            
        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)
    
        elif opcao =="nu": 
            criar_usuario(usuarios)
        
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
main()


