# syntactic.py
from lexic_parser import Parser
from rich.panel import Panel
from rich.console import Console


class Analyzer:
    LL1_TABLE = {
        'MAIN': {
            'DEF': ['FLIST'],
            'INT': ['STMT'],
            'ID': ['STMT'],
            'PRINT': ['STMT'],
            'RETURN': ['STMT'],
            'IF': ['STMT'],
            'LBRACE': ['STMT'],
            'SEMICOLON': ['STMT'],
            '$': []
        },
        'FLIST': {
            'DEF': ['FDEF', "FLIST'"],
        },
        "FLIST'": {
            'DEF': ['FDEF', "FLIST'"],
            '$': []
        },
        'FDEF': {
            'DEF': ['DEF', 'ID', 'LPAREN', 'PARLIST', 'RPAREN', 'LBRACE', 'STMTLIST', 'RBRACE']
        },
        'PARLIST': {
            'INT': ['INT', 'ID', "PARLIST'"],
            'RPAREN': []
        },
        "PARLIST'": {
            'COMMA': ['COMMA', 'PARLIST'],
            'RPAREN': []
        },
        'VARLIST': {
            'ID': ['ID', "VARLIST'"]
        },
        "VARLIST'": {
            'COMMA': ['COMMA', 'VARLIST'],
            'SEMICOLON': []
        },
        'STMT': {
            'INT': ['INT', 'VARLIST', 'SEMICOLON'],
            'ID': ['ATRIBST', 'SEMICOLON'],
            'PRINT': ['PRINTST', 'SEMICOLON'],
            'RETURN': ['RETURNST', 'SEMICOLON'],
            'IF': ['IFSTMT'],
            'LBRACE': ['LBRACE', 'STMTLIST', 'RBRACE'],
            'SEMICOLON': ['SEMICOLON']
        },
        'ATRIBST': {
            'ID': ['ID', 'ASSIGN', 'ATRIBVAL']
        },
        'ATRIBVAL': {
            'ID': ['FCALL'],
            'NUM': ['EXPR'],
            'LPAREN': ['EXPR']
        },
        'FCALL': {
            'ID': ['ID', 'LPAREN', 'PARLISTCALL', 'RPAREN']
        },
        'PARLISTCALL': {
            'ID': ['ID', "PARLISTCALL'"],
            'RPAREN': []
        },
        "PARLISTCALL'": {
            'COMMA': ['COMMA', 'PARLISTCALL'],
            'RPAREN': []
        },
        'PRINTST': {
            'PRINT': ['PRINT', 'EXPR']
        },
        'RETURNST': {
            'RETURN': ['RETURN', 'RETURNVAL']
        },
        'RETURNVAL': {
            'ID': ['ID'],
            'SEMICOLON': []
        },
        'IFSTMT': {
            'IF': ['IF', 'LPAREN', 'EXPR', 'RPAREN', 'LBRACE', 'STMT', 'RBRACE', 'IFELSTMT']
        },
        'IFELSTMT': {
            'ELSE': ['ELSE', 'LBRACE', 'IFSTMT', 'RBRACE'],
            'INT': [], 'ID': [], 'PRINT': [], 'RETURN': [], 'IF': [], 'LBRACE': [], 'SEMICOLON': [], 'RBRACE': [], '$': []
        },
        'STMTLIST': {
            'INT': ['STMT', "STMTLIST'"],
            'ID': ['STMT', "STMTLIST'"],
            'PRINT': ['STMT', "STMTLIST'"],
            'RETURN': ['STMT', "STMTLIST'"],
            'IF': ['STMT', "STMTLIST'"],
            'LBRACE': ['STMT', "STMTLIST'"],
            'SEMICOLON': ['STMT', "STMTLIST'"],
        },
        "STMTLIST'": {
            'INT': ['STMT', "STMTLIST'"],
            'ID': ['STMT', "STMTLIST'"],
            'PRINT': ['STMT', "STMTLIST'"],
            'RETURN': ['STMT', "STMTLIST'"],
            'IF': ['STMT', "STMTLIST'"],
            'LBRACE': ['STMT', "STMTLIST'"],
            'SEMICOLON': ['STMT', "STMTLIST'"],
            'RBRACE': []
        },
        'EXPR': {
            'ID': ['NUMEXPR', "EXPR'"],
            'NUM': ['NUMEXPR', "EXPR'"],
            'LPAREN': ['NUMEXPR', "EXPR'"]
        },
        "EXPR'": {
            'LT': ['LT', 'NUMEXPR'],
            'LE': ['LE', 'NUMEXPR'],
            'GT': ['GT', 'NUMEXPR'],
            'GE': ['GE', 'NUMEXPR'],
            'EQ': ['EQ', 'NUMEXPR'],
            'NE': ['NE', 'NUMEXPR'],
            'RPAREN': [], 'SEMICOLON': []
        },
        'NUMEXPR': {
            'ID': ['TERM', "NUMEXPR'"],
            'NUM': ['TERM', "NUMEXPR'"],
            'LPAREN': ['TERM', "NUMEXPR'"]
        },
        "NUMEXPR'": {
            'PLUS': ['PLUS', 'TERM', "NUMEXPR'"],
            'MINUS': ['MINUS', 'TERM', "NUMEXPR'"],
            'LT': [], 'LE': [], 'GT': [], 'GE': [], 'EQ': [], 'NE': [], 'RPAREN': [], 'SEMICOLON': []
        },
        'TERM': {
            'ID': ['FACTOR', "TERM'"],
            'NUM': ['FACTOR', "TERM'"],
            'LPAREN': ['FACTOR', "TERM'"]
        },
        "TERM'": {
            'TIMES': ['TIMES', 'FACTOR', "TERM'"],
            'DIVIDE': ['DIVIDE', 'FACTOR', "TERM'"],
            'PLUS': [], 'MINUS': [], 'LT': [], 'LE': [], 'GT': [], 'GE': [], 'EQ': [], 'NE': [], 'RPAREN': [], 'SEMICOLON': []
        },
        'FACTOR': {
            'ID': ['ID'],
            'NUM': ['NUM'],
            'LPAREN': ['LPAREN', 'NUMEXPR', 'RPAREN']
        }
    }

    def __init__(self, path):
        self.path = path
        self.parser = Parser(path)

    def analisar(self):
        tokens = [tipo for tipo, _, _ in self.parser.tokens_encontrados]
        return self.analisar_sintaticamente(tokens)

    def analisar_sintaticamente(self, lista_de_tokens):
        tokens = lista_de_tokens + ['$']
        stack = ['$', 'MAIN']
        i = 0
        while stack:
            topo = stack.pop()
            atual = tokens[i]
            if topo == atual:
                i += 1
            elif topo in self.LL1_TABLE:
                producao = self.LL1_TABLE[topo].get(atual)
                if producao is None:
                    linha, coluna = self._get_token_line_col(i)
                    raise SyntaxError(f"Erro sintático: inesperado '{atual}' em contexto de '{topo}' (linha {linha}, coluna {coluna})")
                for simbolo in reversed(producao):
                    if simbolo != 'ε':
                        stack.append(simbolo)
            else:
                linha, coluna = self._get_token_line_col(i)
                raise SyntaxError(f"Erro sintático: esperado '{topo}', mas veio '{atual}' (linha {linha}, coluna {coluna})")
        if i != len(tokens):
            linha, coluna = self._get_token_line_col(i)
            raise SyntaxError(f"Erro sintático: tokens restantes após fim da análise (linha {linha}, coluna {coluna})")
        return True

    def _get_token_line_col(self, idx):
        # Busca linha e coluna do token idx em self.parser.token_infos
        if hasattr(self.parser, 'token_infos') and idx < len(self.parser.token_infos):
            info = self.parser.token_infos[idx]
            return info.get('line', '?'), info.get('col', '?')
        return '?', '?'

    @staticmethod
    def beautiful_print(path):
        console = Console()
        try:
            analyzer = Analyzer(path)
            analyzer.analisar()
            analyzer.parser.print_token_table()
            console.print(Panel.fit(f"[bold green]Análise sintática concluída com sucesso![/bold green]\nArquivo: [bold]{path}[/bold]", title="[bold cyan]Resultado da Análise[/bold cyan]", border_style="green"))
        except (FileNotFoundError, SyntaxError, Exception) as e:
            console.print(Panel.fit(f"[bold red]Erro:[/bold red] {e}\nArquivo: [bold]{path}[/bold]", title="[bold yellow]Erro na Análise[/bold yellow]", border_style="red"))