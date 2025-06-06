# Trabalho - Parte 1 - Analisador Léxico (Parte A)

**Disciplina:** INE5622 - Introdução a Compiladores
**Alunos:** Abmael Batista da Silva,  Jader Theisges e Henrique Silveira Sato.

## Descrição

Este diretório contém a implementação da Parte A do trabalho de Introdução a Compiladores. Trata-se de um analisador léxico implementado manualmente em Python, baseado em diagramas de transição.

O analisador é capaz de:
*   Ler um arquivo de entrada caractere por caractere.
*   Reconhecer os seguintes tipos de tokens:
    *   Identificadores (iniciando com letra, seguido por letras ou números)
    *   Constantes numéricas inteiras
    *   Operadores relacionais (`>`, `<`, `=`, `>=`, `<=`, `≠` - representado como `<>`)
*   Construir e exibir uma tabela de símbolos, diferenciando palavras-chave de identificadores e registrando a linha da primeira ocorrência.
*   Detectar e reportar erros léxicos, indicando a linha e a coluna.

## Como Executar

Para executar o analisador léxico, utilize o Python 3. É necessário fornecer o caminho para o arquivo de entrada como argumento na linha de comando.

```bash
python parteA.py <caminho_para_o_arquivo_de_entrada>
```

**Exemplos:**

1.  **Executando com um arquivo de entrada correto:**
    ```bash
    python parteA.py Testes/teste_correto.txt
    ```

2.  **Executando com um arquivo de entrada contendo erros:**
    ```bash
    python parteA.py Testes/teste_erro.txt
    ```

## Saída Esperada

*   **Em caso de sucesso:** O programa imprimirá a lista de tokens encontrados, cada um com seu tipo, valor (se aplicável), linha e coluna. Em seguida, imprimirá a tabela de símbolos formatada, mostrando o lexema, tipo, número de ocorrências e a linha da primeira ocorrência.
*   **Em caso de erro léxico:** O programa imprimirá uma mensagem de erro indicando o caractere inválido e sua posição (linha e coluna) e encerrará a execução.
