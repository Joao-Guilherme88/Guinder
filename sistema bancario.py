class ContaBancaria:
    def __init__(self, nome):
        self.nome = nome
        self.saldo = 0
        self.limite = 500
        self.extrato = ""
        self.numero_saques = 0
        self.LIMITE_SAQUES = 3

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito: R$ {valor:.2f}\n"
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        else:
            print("Operação falhou! O valor informado é inválido.")

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
            self.extrato += f"Saque: R$ {valor:.2f}\n"
            self.numero_saques += 1
            print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
        else:
            print("Operação falhou! O valor informado é inválido.")

    def extrato(self):
        print("\n====== EXTRATO ======")
        print("Não foram realizadas movimentações." if not self.extrato else self.extrato)
        print(f"Saldo: R$ {self.saldo:.2f}")
        print("========================")


def main():
    menu = """
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [0] Sair
    => """
    
    conta = ContaBancaria("Cliente")

    while True:
        opcao = input(menu)

        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))
            conta.depositar(valor)

        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))
            conta.sacar(valor)

        elif opcao == "3":
            conta.extrato()

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Operação inválida! Por favor, selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
