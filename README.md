# 🍇 Frutaria Banco de Dados LTDA 🍓
### 🍓 "Onde a fruta é fresca e o código é puro. A única frutaria onde o Python colhe as vendas direto do pomar para o terminal!" 🍇

Um sistema de ponto de venda (PDV) para uma pequena frutaria, desenvolvido em Python puro. O projeto simula as interações de Clientes e funcionários (Caixa, Supervisor) através de uma interface de linha de comando (CLI), utilizando arquivos locais (.csv & .txt,) para persistência de informações.

---

## ✨ Principais Funcionalidades

O sistema se dividi em três perfis de acesso, cada um com suas permissões e funcionalidades.

### 👤 Cliente

O cliente pode simular uma experiência de compra completa da frutaria.

-   **Pegar Carrinho:** Inicia uma sessão de compras.
-   **Listar Produtos:** Visualiza todos os produtos com estoque disponível, seus preços e quantidades.
-   **Gerenciar Carrinho:** Pode adicionar e remover produtos do seu carrinho de compras.
-   **Finalizar Compra:** Conclui a sessão, calculando o valor total.
-   **Emitir Nota Fiscal:** Ao finalizar a compra, tem a opção de gerar um arquivo `nota.txt` com o detalhamento da sua compra, incluindo preço unitário de cada item e o valor total.

### 🔐 Administrativo

Área restrita e protegida por senha que dá acesso aos perfis de Caixa e Supervisor.

#### 🧑‍💼 Caixa

Responsável pelas operações diárias do caixa.

-   **Acesso com Senha:** Requer uma senha específica para acessar as funções do caixa.
-   **Panorama Geral:** Ao entrar, visualiza um painel com as informações mais importantes:
    -   Lista de produtos com estoque zerado.
    -   Situação detalhada do dinheiro na caixa registradora (quantidade de cada nota e moeda para troco).
    -   Valor total em caixa, já considerando as compras realizadas pelos clientes.
-   **Verificar Produtos Zerados:** Pode consultar a qualquer momento a lista de todos os produtos até os fora de estoque, que não estão visíveis para os clientes.

#### 🕵️ Supervisor

Possui controle total sobre o inventário e as operações da loja.

-   **Acesso com Senha:** Requer uma senha para o acesso.
-   **Gerenciamento de Produtos (CRUD Completo):**
    -   **Adicionar:** Cadastra novos produtos no sistema.
    -   **Remover:** Exclui produtos do inventário.
    -   **Alterar:** Modifica nome, preço e quantidade em estoque de qualquer produto.
-   **Gerenciamento do Caixa:** Pode alterar o valor em caixa, realizando sangrias (redução) ou adicionando dinheiro para troco.
-   **Log de Alterações:** Todas as ações realizadas pelo supervisor (adição, remoção, alteração de produtos e caixa) são registradas em um arquivo de log (`log_supervisor.txt`) com data e hora, garantindo a rastreabilidade das operações.

---

## 📁 Estrutura de Arquivos

O sistema utiliza arquivos locais para armazenar e gerenciar todos os dados.

-   `produtos.csv`: Armazena o inventário principal da loja.
    -   **Colunas:** `id,nome,preco_venda,quantidade_estoque`
-   `caixa.txt`: Mantém o estado detalhado do dinheiro na caixa registradora.
    -   **Exemplo:** `{"notas": {"50": 2, "20": 3, "10": 5, ...}, "moedas": {"1.00": 10, ...}}`
-   `log_supervisor.txt`: Arquivo de texto que registra todas as ações críticas realizadas pelo Supervisor.
    -   **Formato:** `[AAAA-MM-DD HH:MM:SS] AÇÃO: O produto 'Banana' (ID: 5) teve seu preço alterado para R$ 4.50.`
-   `nota.txt`: Gerado a cada compra finalizada por um cliente que solicita a nota fiscal. O arquivo é sobrescrito a cada nova emissão.

---

## 🧭 Fluxo de Navegação (Idéia Geral)

### Menu Principal (Home)
```text
========================================
   Bem-vindo à Frutaria Banco de Dados LTDA
   Boa tarde! (Horário de Brasília)
========================================

[1] Cliente (Pegar o carrinho de compras)
[2] Administrativo
[0] Sair

Escolha uma opção:

---

========================================
        Área Administrativa
========================================

[1] Acessar como Caixa
[2] Acessar como Supervisor
[0] Voltar ao Menu Principal

Escolha uma opção:
