from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []  # Lista para armazenar as contas do usuário
    
    def realizar_transaçao(self, conta, transaçao):
        transaçao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class ContaCorrente:
    def __init__(self, usuario, numero):
        self.usuario = usuario
        self.agencia = "0001"
        self.numero = numero
        self.saldo = 0
        self.limite = 500
        self.extrato_movimentacoes = ""
        self.numero_saques = 0
        self.LIMITE_SAQUES = 3

    @classmethod
    def nova_conta(cls, usuario,numero):
        return cls(numero, usuario)
    
    @property
    def saldo(self):
        return self.saldo
    
    @property
    def numero(self):
        return self.numero
    
    @property
    def usuario(self):
        return self.usuario
    
    @property
    def numero_saques(self):
        return self.numero_saques
    
    @property
    def limite(self):
        return self.limite
    
    @property
    def agencia(self):
        return self.agencia
    
    @property
    def LIMITE_SAQUES(self):
        return self.LIMITE_SAQUES
    
    @property
    def extrato_movimentacoes(self):
        return self.extrato_movimentacoes

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato_movimentacoes += f"Depósito: R$ {valor:.2f}\n"
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        else:
            print("Operação falhou! O valor informado é inválido.")
            return False
        
        return True

    def sacar(self, valor):
        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > self.limite
        excedeu_saques = self.numero_saques >= self.LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")
        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")
        elif valor > 0:
            self.saldo -= valor
            self.extrato_movimentacoes += f"Saque: R$ {valor:.2f}\n"
            self.numero_saques += 1
            print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
            return True
        
        else:
            print("Operação falhou! O valor informado é inválido.")

        return False    

    def transferir(self, valor, conta_destino):
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            conta_destino.depositar(valor)
            self.extrato_movimentacoes += f"Transferência: R$ {valor:.2f} para {conta_destino.usuario.nome}\n"
            print(f"Transferência de R$ {valor:.2f} realizada com sucesso para {conta_destino.usuario.nome}.")
        else:
            print("Operação falhou! Verifique se o valor é válido e se você possui saldo suficiente.")

    def definir_limite(self, novo_limite):
        if novo_limite > 0:
            self.limite = novo_limite
            print(f"Limite de saque alterado para R$ {novo_limite:.2f}.")
        else:
            print("Operação falhou! O novo limite deve ser um valor positivo.")

    def zerar_conta(self):
        self.saldo = 0
        self.limite = 500
        self.extrato_movimentacoes = ""
        self.numero_saques = 0
        print("Conta zerada com sucesso!")

    def mostrar_extrato(self):
        print("\n====== EXTRATO ======")
        print("Não foram realizadas movimentações." if not self.extrato_movimentacoes else self.extrato_movimentacoes)
        print(f"Saldo: R$ {self.saldo:.2f}")
        print("========================")

    def mostrar_dados_usuario(self):
        print("\n====== DADOS DO USUÁRIO ======")
        print(f"Nome: {self.usuario.nome}")
        print(f"Data de Nascimento: {self.usuario.data_nascimento}")
        print(f"CPF: {self.usuario.cpf}")
        print(f"Endereço: {self.usuario.endereco}")
        print("========================")


def main():
    usuarios = []
    menu_principal = """
    [1] Criar Usuário
    [2] Criar Conta Corrente
    [3] Selecionar Conta Corrente
    [0] Sair
    => """
    
    while True:
        opcao = input(menu_principal)

        if opcao == "1":
            nome = input("Informe o nome do cliente: ")
            data_nascimento = input("Informe a data de nascimento (DD/MM/AAAA): ")
            cpf = input("Informe o CPF: ")
            endereco = input("Informe o endereço: ")
            
            usuario = Usuario(nome, data_nascimento, cpf, endereco)
            usuarios.append(usuario)
            print(f"Usuário criado com sucesso para {nome}!")

        elif opcao == "2":
            if not usuarios:
                print("Nenhum usuário disponível. Crie um usuário primeiro.")
                continue
            
            print("\n=== Usuários Disponíveis ===")
            for i, usuario in enumerate(usuarios):
                print(f"[{i}] {usuario.nome}")
            indice_usuario = int(input("Escolha o usuário: "))
            
            if 0 <= indice_usuario < len(usuarios):
                conta = ContaCorrente(usuarios[indice_usuario])
                usuarios[indice_usuario].adicionar_conta(conta)  # Adiciona a conta à lista de contas do usuário
                print(f"Conta corrente criada com sucesso para {usuarios[indice_usuario].nome}!")
            else:
                print("Usuário inválido.")

        elif opcao == "3":
            if not any(usuario.contas for usuario in usuarios):
                print("Nenhuma conta disponível. Crie uma conta corrente primeiro.")
                continue
            
            print("\n=== Contas Correntes Disponíveis ===")
            for i, usuario in enumerate(usuarios):
                for j, conta in enumerate(usuario.contas):
                    print(f"[{i}-{j}] {conta.usuario.nome} (Conta {j + 1})")
            escolha = input("Escolha a conta (formato 'i-j', por exemplo '0-1'): ")
            try:
                indice_usuario, indice_conta = map(int, escolha.split('-'))
                conta_selecionada = usuarios[indice_usuario].contas[indice_conta]
                
                menu_conta = """
                [1] Depositar
                [2] Sacar
                [3] Extrato
                [4] Transferir
                [5] Definir Limite
                [6] Zerar Conta
                [7] Mostrar Dados do Usuário
                [0] Voltar
                => """
                
                while True:
                    opcao_conta = input(menu_conta)

                    if opcao_conta == "1":
                        valor = float(input("Informe o valor do depósito: "))
                        conta_selecionada.depositar(valor)

                    elif opcao_conta == "2":
                        valor = float(input("Informe o valor do saque: "))
                        conta_selecionada.sacar(valor)

                    elif opcao_conta == "3":
                        conta_selecionada.mostrar_extrato()

                    elif opcao_conta == "4":
                        valor = float(input("Informe o valor da transferência: "))
                        print("=== Contas Disponíveis para Transferência ===")
                        for u in usuarios:
                            for c in u.contas:
                                if c != conta_selecionada:
                                    print(f"{u.nome} (Conta de {c.usuario.nome})")
                        indice_destino = input("Escolha a conta destino (formato 'i-j'): ")
                        try:
                            idx_usuario_destino, idx_conta_destino = map(int, indice_destino.split('-'))
                            conta_destino = usuarios[idx_usuario_destino].contas[idx_conta_destino]
                            conta_selecionada.transferir(valor, conta_destino)
                        except (ValueError, IndexError):
                            print("Conta de destino inválida.")

                    elif opcao_conta == "5":
                        novo_limite = float(input("Informe o novo limite de saque: "))
                        conta_selecionada.definir_limite(novo_limite)

                    elif opcao_conta == "6":
                        conta_selecionada.zerar_conta()

                    elif opcao_conta == "7":
                        conta_selecionada.mostrar_dados_usuario()

                    elif opcao_conta == "0":
                        break

                    else:
                        print("Operação inválida! Por favor, selecione novamente a operação desejada.")
            except (ValueError, IndexError):
                print("Escolha inválida.")

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Operação inválida! Por favor, selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
