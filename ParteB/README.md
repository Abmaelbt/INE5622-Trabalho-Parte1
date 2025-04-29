# Trabalho - Parte 1 - Analisador Léxico (Parte B)

**Disciplina:** INE5622 - Introdução a Compiladores
**Alunos:** Abmael Batista da Silva; Jader Theisges 

## Descrição

Este diretório contém a implementação da Parte B do trabalho de Introdução a Compiladores. Trata-se de um analisador léxico implementado utilizando o gerador de analisadores léxicos PLY (Python Lex-Yacc), para a linguagem LSI-2025-1.

O analisador é capaz de:
*   Reconhecer todos os tokens da linguagem LSI-2025-1, incluindo:
    *   Identificadores (variáveis e nomes de funções)
    *   Constantes numéricas inteiras
    *   Palavras-chave (`int`, `if`, `else`, `def`, `print`, `return`)
    *   Operadores relacionais (`>`, `<`, `<=`, `>=`, `!=`, `==`)
    *   Operadores aritméticos (`+`, `-`, `*`, `/`)
    *   Símbolos especiais (`(`, `)`, `{`, `}`, `,`, `;`, `=`)
*   Construir e exibir uma tabela de símbolos, registrando todos os identificadores encontrados.
*   Detectar e reportar erros léxicos, indicando a linha e a coluna onde ocorrem.

## Como Executar

Para executar o analisador léxico, utilize o Python 3. É necessário ter o pacote PLY instalado (`pip install ply`) e fornecer o caminho para o arquivo de entrada como argumento na linha de comando.

```bash
python parteB.py <caminho_para_o_arquivo_de_entrada>
```
**Exemplos:**

1.  **Executando com um arquivo de entrada correto:**
    ```bash
    python parteB.py Testes/parteB_teste_correto.lsi
    ```

2.  **Executando com um arquivo de entrada contendo erros:**
    ```bash
    python parteB.py Testes/parteB_teste_com_erro.lsi
    ```

## Saída Esperada

*   **Em caso de sucesso:** O programa imprimirá a lista de tokens encontrados, cada um com seu tipo, valor (se aplicável), linha e coluna. Em seguida, imprimirá a tabela de símbolos formatada, mostrando todos os identificadores encontrados.
*   **Em caso de erro léxico:** O programa imprimirá uma mensagem de erro indicando o caractere inválido e sua posição (linha e coluna) e encerrará a execução.
