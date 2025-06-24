# Trabalho - Parte 1 - Analisador Léxico
#
# Disciplina: INE5622 - Introdução a Compiladores
#
# Alunos: Abmael Batista da Silva (22203744); Jader Theisges (22215141); Henrique Silveira Sato (22201631)

import ply.lex as lex

# Biblicoteca que vamos utilizar no futuro caso precise do parser
# import ply.yacc as yacc

import sys
import os


# DEFINIÇÃO DOS TOKENS
tokens = [
    'ID', 'NUM',
    'LT', 'GT', 'LE', 'GE', 'NE', 'EQ',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'ASSIGN',
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'COMMA', 'SEMICOLON'
]


reserved = {
    'int': 'INT',
    'if': 'IF',
    'else': 'ELSE',
    'def': 'DEF',
    'print': 'PRINT',
    'return': 'RETURN'
}

tokens += list(reserved.values())

# Expr regulares para tokens simples
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_NE = r'!='
t_EQ = r'=='
t_PLUS = r'\+'      # Escape no + porque é um metacaractere em regex
t_MINUS = r'-'      # Escape no * porque é um metacaractere em regex
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'

t_ignore = ' \t'

# variavel global apenas pra salvar todos os possíveis erros
erros_lexicos = []

# controla quebra de linhas e atualizar contadores
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.lexer.line_start = t.lexpos


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # verificamos se o identificador e uma palavra reservada
    # se for, alteramos seu tipo para o correspondente (IF, INT, etc.)
    # se nao for, mantemos como ID
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


# tratamento de erros
def t_error(t):
    line = t.lexer.lineno
    col = find_column(t)
    mensagem = f"Erro léxico na linha {line}, coluna {col}: caractere ilegal '{t.value[0]}'"
    erros_lexicos.append(mensagem)
    t.lexer.skip(1)


# funcao auxiliar para calcular a coluna onde um token aparece
# necessario pois o PLY nao rastreia colunas automaticamente
def find_column(token):
    last_cr = token.lexer.lexdata.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    column = token.lexpos - last_cr
    return column


lexer = lex.lex()


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 analisador.py arquivo.lsi")
        sys.exit(1)

    caminho = sys.argv[1]
    if not os.path.isfile(caminho):
        print(f"Arquivo não encontrado: {caminho}")
        sys.exit(1)

    with open(caminho, 'r') as f:
        codigo = f.read()

    lexer.input(codigo)

    tokens_encontrados = []
    tabela_simbolos = set()

    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_encontrados.append((tok.type, tok.value))
        if tok.type == 'ID':
            tabela_simbolos.add(tok.value)

    # para mostrar todos os erros
    if erros_lexicos:
        print("\nErros Léxicos Encontrados:")
        for erro in erros_lexicos:
            print(f"  {erro}")
        sys.exit(1)

    print("\nLista de Tokens:")
    for tipo, valor in tokens_encontrados:
        print(f"  {tipo}: {valor}")

    print("\nTabela de Símbolos:")
    for simbolo in sorted(tabela_simbolos):
        print(f"  {simbolo}")


if __name__ == "__main__":
    main()
