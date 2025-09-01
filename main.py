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
    input(f"\n{mensagem} ")

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
    """Carrega dados de um arquivo CSV, aplicando conversões de tipo.  """
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
    """Gera um arquivo de texto 'nota.txt' com os detalhes da compra.  """
    print("Funcionalidades ainda ser implementado aqui.")

# --- LÓGICA DO CLIENTE ---

def _cliente_adicionar_item(carrinho, produtos):
    """Função auxiliar para adicionar um item ao carrinho."""
    print("Funcionalidades ainda ser implementado aqui.")
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
    """Gerencia as ações do Supervisor."""
    exibir_cabecalho("PAINEL DO SUPERVISOR")
    print("Funcionalidades do supervisor (CRUD de produtos, etc.) a serem implementadas aqui.")
    pausar_tela()
    return produtos, caixa # Retorna estado (pode ter sido alterado)

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
