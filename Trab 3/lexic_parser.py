import ply.lex as lex
import os

class Parser:
    def __init__(self, caminho_arquivo):
        self.caminho = caminho_arquivo
        self.erros_lexicos = []
        self.tabela_simbolos = set()
        self.tokens_encontrados = []
        self.token_infos = []  # Nova lista de infos
        self._definir_tokens()
        self.lexer = lex.lex(module=self)
        self._executar_analise()

    def _definir_tokens(self):
        self.tokens = [
            'ID', 'NUM',
            'LT', 'GT', 'LE', 'GE', 'NE', 'EQ',
            'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
            'ASSIGN',
            'LPAREN', 'RPAREN',
            'LBRACE', 'RBRACE',
            'COMMA', 'SEMICOLON'
        ]

        self.reserved = {
            'int': 'INT',
            'if': 'IF',
            'else': 'ELSE',
            'def': 'DEF',
            'print': 'PRINT',
            'return': 'RETURN'
        }

        self.tokens += list(self.reserved.values())

        # Atributos de regex
        self.t_LT = r'<'
        self.t_GT = r'>'
        self.t_LE = r'<='
        self.t_GE = r'>='
        self.t_NE = r'!='
        self.t_EQ = r'=='
        self.t_PLUS = r'\+'
        self.t_MINUS = r'-'
        self.t_TIMES = r'\*'
        self.t_DIVIDE = r'/'
        self.t_ASSIGN = r'='
        self.t_LPAREN = r'\('
        self.t_RPAREN = r'\)'
        self.t_LBRACE = r'\{'
        self.t_RBRACE = r'\}'
        self.t_COMMA = r','
        self.t_SEMICOLON = r';'
        self.t_ignore = ' \t'

    def _executar_analise(self):
        if not os.path.isfile(self.caminho):
            raise FileNotFoundError(f"Arquivo não encontrado: {self.caminho}")

        with open(self.caminho, 'r') as f:
            codigo = f.read()
        self._source_code = codigo  # Store source code for column calculation

        self.lexer.input(codigo)

        self.tokens_encontrados = []  # Always reset
        self.token_infos = []  # Nova lista de infos
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            # Store (type, value, token_obj) for each token
            self.tokens_encontrados.append((tok.type, tok.value, tok))
            # Calcula linha e coluna
            if hasattr(tok, 'lineno') and hasattr(tok, 'lexpos'):
                line = tok.lineno
                last_cr = self._source_code.rfind('\n', 0, tok.lexpos)
                if last_cr < 0:
                    last_cr = -1
                col = tok.lexpos - last_cr
                col = col if col < 0 else col + 1
            else:
                line, col = None, None
            self.token_infos.append({'type': tok.type, 'value': tok.value, 'line': line, 'col': col})
            if tok.type == 'ID':
                self.tabela_simbolos.add(tok.value)

        if self.erros_lexicos:
            raise Exception("Erros léxicos encontrados:\n" + "\n".join(self.erros_lexicos))

    def get_tabela_simbolos(self):
        return sorted(self.tabela_simbolos)

    def print_token_table(self):
        print(f"{'Idx':<5} {'Type':<12} {'Value':<15} {'Line':<6} {'Col':<5}")
        print('-' * 45)
        for idx, (tipo, val, tok) in enumerate(self.tokens_encontrados):
            if tok and hasattr(tok, 'lineno') and hasattr(tok, 'lexpos') and hasattr(self, '_source_code'):
                line = tok.lineno
                last_cr = self._source_code.rfind('\n', 0, tok.lexpos)
                if last_cr < 0:
                    last_cr = -1
                col = tok.lexpos - last_cr
                col = col if col < 0 else col + 1
                print(f"{idx:<5} {tipo:<12} {str(val):<15} {line:<6} {col:<5}")
            else:
                print(f"{idx:<5} {tipo:<12} {str(val):<15} {'?':<6} {'?':<5}")

    # TOKENS E FUNÇÕES ASSOCIADAS AO LEXER
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    def t_NUM(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        t.lexer.line_start = t.lexpos


    def t_error(self, t):
        linha = t.lexer.lineno
        coluna = self._find_column(t)
        self.erros_lexicos.append(f"Erro léxico na linha {linha}, coluna {coluna}: caractere ilegal '{t.value[0]}'")
        t.lexer.skip(1)

    def _find_column(self, token):
        last_cr = token.lexer.lexdata.rfind('\n', 0, token.lexpos)
        if last_cr < 0:
            last_cr = -1
        return token.lexpos - last_cr
