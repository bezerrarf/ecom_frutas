import csv
import os
from datetime import datetime

# --- CONSTANTES E CONFIGURAÇÕES GLOBAIS ---
ARQUIVO_PRODUTOS = 'produtos.csv'
ARQUIVO_CAIXA = 'caixa.csv'
ARQUIVO_LOG = 'log_supervisor.txt'
ARQUIVO_NOTA = 'nota.txt'
SENHAS = {"caixa": "123", "supervisor": "admin"}

# --- FUNÇÕES AUXILIARES DE INTERFACE E UTILIDADE ---

def limpar_tela():
    """Limpa o console do terminal para melhorar a legibilidade."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar_tela(mensagem="Pressione Enter para continuar..."):
    """Pausa a execução e aguarda o usuário pressionar Enter."""
    input(f"\n{mensagem}")

def exibir_cabecalho(titulo):
    """Exibe um cabeçalho formatado e centralizado."""
    limpar_tela()
    print("=" * 45)
    print(f"   {titulo.center(35)}")
    print("=" * 45)

def obter_saudacao():
    """Retorna uma saudação simples (Bom dia, Boa tarde, Boa noite) baseada na hora local."""
    hora = datetime.now().hour
    if 5 <= hora < 12: return "Bom dia!"
    if 12 <= hora < 18: return "Boa tarde!"
    return "Boa noite!"

# --- FUNÇÕES DE GERENCIAMENTO DE DADOS (I/O) ---

def carregar_dados_csv(caminho_arquivo, conversoes):
    #Carrega dados de um arquivo CSV, aplicando conversões de tipo.   
    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as f:
            leitor = csv.DictReader(f)
            dados = []
            for linha in leitor:
                for chave, tipo in conversoes.items():
                    linha[chave] = tipo(linha[chave])
                dados.append(linha)
            return dados
    except FileNotFoundError:
        print(f"AVISO: Arquivo '{caminho_arquivo}' não encontrado. Iniciando com dados vazios.")
        return []

def salvar_dados_csv(caminho_arquivo, dados, cabecalho):
    """Salva uma lista de dicionários em um arquivo CSV."""
    with open(caminho_arquivo, mode='w', encoding='utf-8', newline='') as f:
        escritor = csv.DictWriter(f, fieldnames=cabecalho)
        escritor.writeheader()
        escritor.writerows(dados)

def logar_acao(mensagem):
    """Registra uma mensagem no arquivo de log do supervisor com data e hora."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(ARQUIVO_LOG, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {mensagem}\n")

def gerar_nota_fiscal(carrinho, total_compra):
    """Gera um arquivo de texto 'nota.txt' com os detalhes da compra.

    Args:
        carrinho (list): A lista de itens no carrinho do cliente.
        total_compra (float): O valor total da compra.
    """
    with open(ARQUIVO_NOTA, 'w', encoding='utf-8') as nota:
        nota.write("=" * 45 + "\n")
        nota.write("      NOTA FISCAL - FRUTARIA BDLTDA\n")
        nota.write("=" * 45 + "\n")
        for item in carrinho:
            preco_unitario = float(item['preco_venda'])
            subtotal = item['quantidade'] * preco_unitario
            linha = f"{item['nome']} ({item['quantidade']}x R${preco_unitario:.2f})".ljust(33)
            subtotal_str = f"R${subtotal:.2f}".rjust(11)
            nota.write(linha + subtotal_str + "\n")
        nota.write("-" * 45 + "\n")
        nota.write(f"TOTAL DA COMPRA:".ljust(33) + f"R${total_compra:.2f}".rjust(11) + "\n")
        nota.write("=" * 45 + "\n")
    print(f"\nNota fiscal gerada com sucesso no arquivo '{ARQUIVO_NOTA}'!")

# --- LÓGICA DO CLIENTE ---

def _cliente_adicionar_item(carrinho, produtos):
    """Função auxiliar para adicionar um item ao carrinho."""
    try:
        id_prod = int(input("Digite o ID do produto: "))
        produto_em_estoque = next((p for p in produtos if p['id'] == id_prod and p['quantidade_estoque'] > 0), None)
        
        if not produto_em_estoque:
            print("Erro: Produto não encontrado ou sem estoque.")
            return carrinho

        qtd = int(input(f"Quantidade de '{produto_em_estoque['nome']}': "))
        if 0 < qtd <= produto_em_estoque['quantidade_estoque']:
            item_no_carrinho = next((item for item in carrinho if item['id'] == id_prod), None)
            if item_no_carrinho:
                item_no_carrinho['quantidade'] += qtd
            else:
                carrinho.append({'id': id_prod, 'nome': produto_em_estoque['nome'], 'preco_venda': produto_em_estoque['preco_venda'], 'quantidade': qtd})
            print("Produto adicionado com sucesso!")
        else:
            print(f"Erro: Quantidade inválida ou estoque insuficiente ({produto_em_estoque['quantidade_estoque']} disponíveis).")
    except ValueError:
        print("Erro: ID e quantidade devem ser números.")
    return carrinho

def menu_cliente(produtos):
    """Gerencia o fluxo de compra do cliente."""
    carrinho = []
    while True:
        exibir_cabecalho("CARRINHO DE COMPRAS")
        print("[1] Ver produtos\n[2] Adicionar item\n[3] Remover item\n[4] Ver carrinho\n[5] Finalizar compra\n[0] Voltar")
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            exibir_cabecalho("PRODUTOS DISPONÍVEIS")
            for p in produtos:
                if p['quantidade_estoque'] > 0:
                    print(f"ID: {p['id']:<3} | {p['nome']:<25} | R$ {p['preco_venda']:.2f}")
            pausar_tela()
        elif opcao == '2':
            carrinho = _cliente_adicionar_item(carrinho, produtos)
            pausar_tela()
        elif opcao == '3':
            try:
                id_prod = int(input("Digite o ID do produto a remover: "))
                # A linha abaixo é a correção: reatribui a lista filtrada à variável carrinho.
                carrinho = [item for item in carrinho if item['id'] != id_prod]
                print(f"Produto com ID {id_prod} removido do carrinho.")
            except ValueError:
                print("Erro: ID deve ser um número.")
            pausar_tela()
        elif opcao == '4':
            exibir_cabecalho("MEU CARRINHO")
            if not carrinho:
                print("Carrinho vazio.")
            else:
                total = sum(item['quantidade'] * item['preco_venda'] for item in carrinho)
                for item in carrinho:
                    print(f"- {item['nome']} | Qtd: {item['quantidade']} | Subtotal: R$ {item['quantidade'] * item['preco_venda']:.2f}")
                print(f"\nTotal: R$ {total:.2f}")
            pausar_tela()
        elif opcao == '5':
            if not carrinho:
                print("\nCarrinho vazio. Adicione itens para finalizar.")
                pausar_tela()
                continue
            
            total_compra = sum(item['quantidade'] * item['preco_venda'] for item in carrinho)
            print(f"\nTotal da compra: R$ {total_compra:.2f}")
            if input("Confirmar compra? (s/n): ").lower() == 's':
                for item_carrinho in carrinho:
                    for produto_estoque in produtos:
                        if produto_estoque['id'] == item_carrinho['id']:
                            produto_estoque['quantidade_estoque'] -= item_carrinho['quantidade']
                            break
                
                if input("Deseja nota fiscal? (s/n): ").lower() == 's':
                    gerar_nota_fiscal(carrinho, total_compra)
                
                logar_acao(f"COMPRA REALIZADA: Valor R$ {total_compra:.2f}.")
                print("\nCompra finalizada com sucesso!")
                pausar_tela()
                return produtos, total_compra
        elif opcao == '0':
            return produtos, 0.0
        else:
            print("Opção inválida!")
            pausar_tela()

# --- LÓGICA ADMINISTRATIVA ---

def menu_caixa(produtos, caixa, total_vendas):
    """Exibe o painel de informações para o Caixa."""
    exibir_cabecalho("PAINEL DO CAIXA")
    print("[Produtos com Estoque Zerado]")
    produtos_zerados = [p for p in produtos if p['quantidade_estoque'] == 0]
    if produtos_zerados:
        for p in produtos_zerados: print(f"- {p['nome']}")
    else:
        print("Nenhum.")

    print("\n[Situação do Caixa]")
    total_caixa_inicial = sum(item['valor'] * item['quantidade'] for item in caixa)
    print(f"Valor inicial em caixa: R$ {total_caixa_inicial:.2f}")
    print(f"Vendas da sessão:       R$ {total_vendas:.2f}")
    print(f"Valor total atual:      R$ {total_caixa_inicial + total_vendas:.2f}")
    pausar_tela()

def menu_supervisor(produtos, caixa):
    """Gerencia o menu de ações do Supervisor para CRUD de produtos e gestão do caixa."""
    while True:
        exibir_cabecalho("PAINEL DO SUPERVISOR")
        print("[1] Listar produtos\n[2] Adicionar produto\n[3] Alterar produto\n[4] Remover produto\n[5] Gerenciar caixa\n[0] Voltar")
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            exibir_cabecalho("LISTA COMPLETA DE PRODUTOS")
            for p in produtos:
                print(f"ID: {p['id']:<3} | {p['nome']:<25} | R$ {p['preco_venda']:.2f} | Estoque: {p['quantidade_estoque']}")
            pausar_tela()
        elif opcao == '2':
            exibir_cabecalho("ADICIONAR NOVO PRODUTO")
            try:
                nome = input("Nome do novo produto: ")
                preco = float(input("Preço de venda (ex: 4.50): "))
                estoque = int(input("Quantidade em estoque inicial: "))
                if preco <= 0 or estoque < 0:
                    print("Erro: Preço e estoque devem ser valores positivos.")
                else:
                    novo_id = max(p['id'] for p in produtos) + 1 if produtos else 1
                    produtos.append({'id': novo_id, 'nome': nome, 'preco_venda': preco, 'quantidade_estoque': estoque})
                    logar_acao(f"PRODUTO ADICIONADO: '{nome}' (ID: {novo_id}).")
                    print(f"\nProduto '{nome}' adicionado com sucesso!")
            except ValueError:
                print("\nErro: Preço e estoque devem ser números válidos.")
            pausar_tela()
        elif opcao == '3':
            exibir_cabecalho("ALTERAR PRODUTO EXISTENTE")
            try:
                id_prod = int(input("Digite o ID do produto a alterar: "))
                produto = next((p for p in produtos if p['id'] == id_prod), None)
                if not produto:
                    print("Erro: Nenhum produto encontrado com este ID.")
                else:
                    print(f"Alterando: '{produto['nome']}'")
                    novo_preco_str = input(f"Novo preço (Enter para manter R${produto['preco_venda']:.2f}): ")
                    if novo_preco_str:
                        produto['preco_venda'] = float(novo_preco_str)
                        logar_acao(f"PREÇO ALTERADO: ID {id_prod} para R${produto['preco_venda']:.2f}.")
                    
                    novo_estoque_str = input(f"Novo estoque (Enter para manter {produto['quantidade_estoque']}): ")
                    if novo_estoque_str:
                        produto['quantidade_estoque'] = int(novo_estoque_str)
                        logar_acao(f"ESTOQUE ALTERADO: ID {id_prod} para {produto['quantidade_estoque']} unidades.")
                    
                    print("\nProduto atualizado!")
            except ValueError:
                print("\nErro: ID, preço e estoque devem ser números.")
            pausar_tela()
        elif opcao == '4':
            exibir_cabecalho("REMOVER PRODUTO")
            try:
                id_prod = int(input("Digite o ID do produto a remover: "))
                produto = next((p for p in produtos if p['id'] == id_prod), None)
                if not produto:
                    print("Erro: Nenhum produto encontrado com este ID.")
                else:
                    if input(f"Remover '{produto['nome']}'? (s/n): ").lower() == 's':
                        produtos = [p for p in produtos if p['id'] != id_prod]
                        logar_acao(f"PRODUTO REMOVIDO: '{produto['nome']}' (ID: {id_prod}).")
                        print("Produto removido.")
                    else:
                        print("Operação cancelada.")
            except ValueError:
                print("\nErro: ID deve ser um número.")
            pausar_tela()
        elif opcao == '5':            
            print("Funcionalidade de gerenciamento de caixa a ser implementada.")
            pausar_tela()
        elif opcao == '0':
            return produtos, caixa
        else:
            print("Opção inválida!")
            pausar_tela()

def menu_administrativo(produtos, caixa, total_vendas):
    """Gerencia o menu de acesso à área administrativa."""
    while True:
        exibir_cabecalho("ÁREA ADMINISTRATIVA")
        print("[1] Acessar como Caixa\n[2] Acessar como Supervisor\n[0] Voltar")
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            if input("Senha de Caixa: ") == SENHAS["caixa"]:
                menu_caixa(produtos, caixa, total_vendas)
            else:
                print("Senha incorreta!")
                pausar_tela()
        elif opcao == '2':
            if input("Senha de Supervisor: ") == SENHAS["supervisor"]:
                produtos, caixa = menu_supervisor(produtos, caixa)
            else:
                print("Senha incorreta!")
                pausar_tela()
        elif opcao == '0':
            break
    return produtos, caixa

# --- FUNÇÃO PRINCIPAL ---

def main():
    """Função principal que executa o loop do programa."""
    conversoes_produtos = {'id': int, 'preco_venda': float, 'quantidade_estoque': int}
    conversoes_caixa = {'valor': float, 'quantidade': int}
    
    produtos = carregar_dados_csv(ARQUIVO_PRODUTOS, conversoes_produtos)
    caixa = carregar_dados_csv(ARQUIVO_CAIXA, conversoes_caixa)
    total_vendas_sessao = 0.0

    while True:
        exibir_cabecalho(f"Frutaria Banco de Dados - {obter_saudacao()}")
        print("[1] Cliente\n[2] Administrativo\n[0] Sair")
        escolha = input("\nEscolha uma opção: ")

        if escolha == '1':
            produtos, valor_compra = menu_cliente(produtos)
            total_vendas_sessao += valor_compra
        elif escolha == '2':
            produtos, caixa = menu_administrativo(produtos, caixa, total_vendas_sessao)
        else:
            salvar_dados_csv(ARQUIVO_PRODUTOS, produtos, ['id', 'nome', 'preco_venda', 'quantidade_estoque'])
            salvar_dados_csv(ARQUIVO_CAIXA, caixa, ['tipo', 'valor', 'quantidade'])
            print("\nDados salvos. Obrigado e volte sempre!")
            break

if __name__ == "__main__":
    main()
