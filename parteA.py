# Trabalho - Parte 1 - Analisador Léxico
#
# Disciplina: INE5622 - Introdução a Compiladores
#
# Alunos: Abmael Batista da Silva (22203744); Jader Theisges

class Token:
    def __init__(self, tipo, valor=None, linha=1, coluna=0):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha
        self.coluna = coluna

    def __str__(self):
        if self.valor:
            return f"Token({self.tipo}, {self.valor})"
        return f"Token({self.tipo})"

class TabelaSimbolos:
    def __init__(self):
        self.tabela = {}
        self.inserir_palavras_chave()

    def inserir_palavras_chave(self):
        # Palavras-chave da LSI-2025-1
        palavras_chave = [
            'def', 'int', 'return', 'if', 'else', 'print'
        ]
        for palavra in palavras_chave:
            self.inserir(palavra, 'PALAVRA_CHAVE')

    def inserir(self, lexema, tipo, linha=None):
        if lexema not in self.tabela:
            self.tabela[lexema] = {
                'tipo': tipo,
                'ocorrencias': 1,
                'linha_primeira_ocorrencia': linha
            }
        else:
            self.tabela[lexema]['ocorrencias'] += 1

    def buscar(self, lexema):
        return self.tabela.get(lexema)

    def __str__(self):
        saida = "\nTabela de Símbolos:\n"
        saida += "-" * 70 + "\n"
        saida += "| {:<20} | {:<12} | {:<10} | {:<20} |\n".format("Lexema", "Tipo", "Ocorrências", "Linha Primeira Ocorrência")
        saida += "-" * 70 + "\n"
        for lexema, info in self.tabela.items():
            saida += "| {:<20} | {:<12} | {:<10} | {:<20} |\n".format(
                lexema, 
                info['tipo'], 
                info['ocorrencias'],
                info['linha_primeira_ocorrencia']
            )
        saida += "-" * 70
        return saida

class AnalisadorLexico:
    def __init__(self, input_file):
        with open(input_file, 'r') as f:
            self.conteudo = f.read()
        self.posicao = 0
        self.linha = 1
        self.coluna = 0
        self.tabela_simbolos = TabelaSimbolos()

    def proximo_char(self):
        if self.posicao >= len(self.conteudo):
            return None
        char = self.conteudo[self.posicao]
        self.posicao += 1
        if char == '\n':
            self.linha += 1
            self.coluna = 0
        else:
            self.coluna += 1
        return char

    def voltar_char(self):
        self.posicao -= 1
        self.coluna -= 1
        
    def reconhecer_identificador(self):
        lexema = ''
        char = self.proximo_char()
        
        # funcao isalpha() retorna True se o caractere é uma letra
        if not char.isalpha():
            self.voltar_char()
            return None
            
        lexema += char
        coluna_inicial = self.coluna - 1
        
        while True:
            char = self.proximo_char()
            # funcao isalnum() retorna True se o caractere é alfanumérico
            if char and (char.isalnum()):
                lexema += char
            else:
                if char:
                    self.voltar_char()
                break
        
        # Busca na tabela de símbolos
        info = self.tabela_simbolos.buscar(lexema)
        
        if info and info['tipo'] == 'PALAVRA_CHAVE':
            self.tabela_simbolos.inserir(lexema, 'PALAVRA_CHAVE', self.linha)
            return Token('PALAVRA_CHAVE', lexema, self.linha, coluna_inicial)
        
        # Se não é palavra-chave, é um identificador
        self.tabela_simbolos.inserir(lexema, 'ID', self.linha)
        return Token('ID', lexema, self.linha, coluna_inicial)

    def reconhecer_numero(self):
        numero = ''
        char = self.proximo_char()
        coluna_inicial = self.coluna - 1
        
        if not char.isdigit():
            self.voltar_char()
            return None
            
        while char and char.isdigit():
            numero += char
            char = self.proximo_char()
            
        if char:
            self.voltar_char()
            
        return Token('NUM', int(numero), self.linha, coluna_inicial)

    def reconhecer_operador(self):
        char = self.proximo_char()
        coluna_inicial = self.coluna - 1
        
        if char in ['>', '<', '=']:
            prox_char = self.proximo_char()
            if prox_char == '=':
                return Token('OP', char + prox_char, self.linha, coluna_inicial)
            if char == '<' and prox_char == '>':  # Para ≠
                return Token('OP', '≠', self.linha, coluna_inicial)
            self.voltar_char()
            return Token('OP', char, self.linha, coluna_inicial)
        self.voltar_char()
        return None
    
    def analisar(self):
        tokens = []
        
        while self.posicao < len(self.conteudo):
            char = self.proximo_char()
            
            # Ignora espaços em branco
            if char.isspace():
                continue
                
            self.voltar_char()
            
            # Tenta reconhecer cada tipo de token
            token = (self.reconhecer_identificador() or 
                    self.reconhecer_numero() or 
                    self.reconhecer_operador())
            
            if token:
                tokens.append(token)
            else:
                char = self.proximo_char()
                print(f"Erro léxico: caractere inválido '{char}' na linha {self.linha}, coluna {self.coluna}")
                return None
                
        return tokens

def main():
    import sys
    if len(sys.argv) != 2:
        print("Uso: python parteA.py arquivo_entrada.txt")
        return

    analisador = AnalisadorLexico(sys.argv[1])
    tokens = analisador.analisar()
    
    if tokens:
        print("\nTokens encontrados:")
        for token in tokens:
            print(token)
        print(analisador.tabela_simbolos)

if __name__ == "__main__":
    main()