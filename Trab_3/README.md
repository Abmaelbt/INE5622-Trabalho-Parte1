### Disciplina: INE5622 - Introdução a Compiladores
### Alunos: Abmael Batista da Silva (222037440), Jader Theisges (22215141) e Henrique Silveira Sato (22201631), Luiz Eduardo da Silva (22202683)


# INE5622 - Trabalho Parte 3

Este repositório contém a implementação do **Trabalho Parte 3** da disciplina **INE5622**. O objetivo deste trabalho é desenvolver soluções para os problemas propostos, utilizando **Python** como linguagem principal.

## Estrutura do Repositório

### Parte 3
O trabalho está localizado no diretório [`Trab_3/`](./Trab_3). Ela contém:


## Pré-requisitos

```
1. python3 --version
2. pip3 --version
```

## Instalação das dependências

1. pip3 install -r requirements.txt

## Como Executar

1. Navegue até o diretório da parte 3 `Trab_3`.
2. Para executar: 

Arquivo correto:
```
python3 main.py Testes/parteB_teste_correto.lsi
```
Arquivo incorreto:
```
python3 main.py Testes/parteB_teste_com_erro_1.lsi
```

## Saídas esperadas

1. Saída esperada (arquivo parteB_teste_correto.lsi): Você verá uma tabela detalhada dos tokens e uma mensagem de sucesso em um painel verde: 
```"Análise sintática concluída com sucesso!"```.


2. Saída esperada (parteB_teste_com_erro_1.lsi): Você verá uma mensagem de erro sintático (ou léxico, se for o caso) em um painel vermelho, indicando a linha e coluna do problema: 
```"Erro:{descrição do erro}"```.


3. Uso incorreto: Se você não fornecer um caminho de arquivo, o programa exibirá: 
```"Uso: python main.py arquivo.lsi"```.


4. Arquivo não encontrado: Se o arquivo especificado não existir, o programa exibirá: 
```"Arquivo não encontrado: {caminho_do_arquivo}"```.
