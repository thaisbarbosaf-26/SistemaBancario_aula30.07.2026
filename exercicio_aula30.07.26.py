import csv
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

saldo = 100
extrato = []
historico_saldo = [saldo]  # guarda o saldo após cada movimentação, para plotar depois
ARQUIVO_CSV = "extrato_movimentacao.csv"


def salvar_no_csv(tipo, valor):
    with open(ARQUIVO_CSV, mode="a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(
            [datetime.now().strftime("%d/%m/%Y %H:%M:%S"), tipo, f"{valor:.2f}", f"{saldo:.2f}"]
        )


def exibir_banco():
    print("\n===== CAIXA ELETRONICO =====")
    print("1- Consultar Saldo")
    print("2- Depositar Dinheiro")
    print("3- Sacar Dinheiro")
    print("4- Ver Extrato")
    print("5- Movimentações")
    print("6- Relatório Avançado (Pandas & NumPy)")
    print("7- Sair")


def consultar_saldo():
    print(f"\nSeu saldo atual é: R$ {saldo:.2f}")


def depositar_dinheiro():
    global saldo
    valor = float(input("\nDigite o valor a ser depositado R$ "))
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        historico_saldo.append(saldo)  # adiciona o novo saldo na lista do gráfico
        salvar_no_csv("Depósito", valor)
        print(f"\nDepósito de R$ {valor:.2f} realizado com sucesso.")
    else:
        print("\nValor inválido.")


def sacar_dinheiro():
    global saldo
    valor = float(input("\nDigite o valor a ser sacado R$ "))
    if valor > 0 and valor <= saldo:
        saldo -= valor
        extrato.append(f"Saque: R$ {valor:.2f}")
        historico_saldo.append(saldo)  # adiciona o novo saldo na lista do gráfico
        salvar_no_csv("Saque", valor)
        print(f"\nSaque de R$ {valor:.2f} realizado com sucesso.")
    else:
        print("\nSaldo insuficiente ou valor inválido.")


def ver_extrato():
    print("\n===== EXTRATO =====")
    if not extrato:
        print("Nenhuma movimentação realizada.")
    else:
        for movimentacao in extrato:
            print(movimentacao)
    print(f"\nSaldo atual: R$ {saldo:.2f}")


def ver_movimentacoes():
    plt.plot(historico_saldo, marker="o")  # desenha a lista de saldos, um ponto por movimentação
    plt.title("Evolução do Saldo")
    plt.ylabel("Saldo (R$)")
    plt.show()


def relatorio_avancado():
    print("\n===== RELATÓRIO AVANÇADO =====")

    # --- Parte 1: Pandas -> ler o CSV e organizar como tabela (DataFrame) ---
    # Repare a diferença: em vez de um "for" lendo linha por linha, o pandas
    # carrega o arquivo inteiro em uma tabela e já sabemos manipular colunas.
    colunas = ["Data", "Tipo", "Valor", "Saldo"]
    try:
        df = pd.read_csv(ARQUIVO_CSV, names=colunas)
    except FileNotFoundError:
        print("Nenhuma movimentação registrada ainda.")
        return

    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y %H:%M:%S")

    print("\n-- Tabela de movimentações (pandas.DataFrame) --")
    print(df.to_string(index=False))

    # groupby: soma os valores agrupando por tipo de movimentação
    print("\n-- Total por tipo (df.groupby) --")
    print(df.groupby("Tipo")["Valor"].sum())

    # describe: estatística descritiva pronta (contagem, média, min, max...)
    print("\n-- Estatística dos valores (df['Valor'].describe()) --")
    print(df["Valor"].describe())

    # filtro: só as movimentações de hoje
    hoje = df[df["Data"].dt.date == datetime.now().date()]
    print(f"\n-- Movimentações de hoje: {len(hoje)} --")

    # --- Parte 2: NumPy -> cálculos sobre o histórico de saldo ---
    # Toda coluna do pandas já é, por baixo dos panos, um array NumPy.
    # Aqui pegamos essa coluna "pura" para fazer contas em todos os números
    # de uma vez, sem precisar escrever um "for".
    saldos = df["Saldo"].to_numpy()

    print("\n-- Estatísticas do saldo (numpy) --")
    print(f"Saldo médio: R$ {np.mean(saldos):.2f}")
    print(f"Maior saldo: R$ {np.max(saldos):.2f}")
    print(f"Menor saldo: R$ {np.min(saldos):.2f}")
    print(f"Desvio padrão: R$ {np.std(saldos):.2f}")

    # diff: a diferença entre cada saldo e o saldo anterior, tudo de uma vez
    variacoes = np.diff(saldos)
    print("\n-- Variação entre movimentações (numpy.diff) --")
    print(variacoes)


def main():
    while True:
        exibir_banco()
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            consultar_saldo()
        elif opcao == "2":
            depositar_dinheiro()
        elif opcao == "3":
            sacar_dinheiro()
        elif opcao == "4":
            ver_extrato()
        elif opcao == "5":
            ver_movimentacoes()
        elif opcao == "6":
            relatorio_avancado()
        elif opcao == "7":
            print("\nSaindo do sistema. Obrigado por utilizar o Caixa Eletrônico.")
            break
        else:
            print("\nOpção inválida. Por favor, escolha uma opção válida.")


if __name__ == "__main__":
    main()