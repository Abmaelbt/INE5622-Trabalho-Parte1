from lexic_parser import Parser
from syntatic_analyzer import Analyzer

# parser = Parser("./Testes/parteB_teste_correto.lsi")

# tabela = parser.get_tabela_simbolos()
# tokens = parser.tokens_encontrados


# print("Tabela de Símbolos:", tabela)

# print("\n" + "="*30)
# print("🌟 Tokens Encontrados 🌟")
# print("="*30)
# for idx, token in enumerate(tokens, 1):
#     print(f"{idx:2d}. {token}")
# print("="*30 + "\n")

if __name__ == "__main__":
    # Exemplo de uso: altere o caminho para o arquivo que deseja analisar
    caminho_arquivo = "Testes/parteB_teste_correto.lsi"
    Analyzer.beautiful_print(caminho_arquivo)
