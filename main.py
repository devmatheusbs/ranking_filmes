import requests
import db
from datetime import datetime
db.criardb()
from googletrans import Translator
def nome_filme_formatado(filme):
    filme = traduzir(filme, 'en')
    filme_formatado = filme.replace(" ", "%20")
    return filme_formatado

def get_filme(nome_filme):
    api =  'b097dd2b'
    url = f'http://www.omdbapi.com/?apikey={api}&s={nome_filme}&plot=full&type=movie&page=1-5'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        print('Filme não localizado')

def escolher_filme(data):
    lista_de_filmes = []
    contador = 1 
    filme_escolhido = True
    for filmes_encontrados in data['Search']:
            print(f'{contador}: {filmes_encontrados['Title']}, {filmes_encontrados['Year']}')
            contador += 1
            lista_de_filmes.append(filmes_encontrados)
    while filme_escolhido == True:
        escolha = input("Escolha um número entre 1 e {} ou (n) para nenhuma dessas: ".format(len(lista_de_filmes)))
        if escolha.isdigit() and 1 <= int(escolha) <= len(lista_de_filmes):
            indice_escolhido = int(escolha)     
            filme_escolhido = lista_de_filmes[indice_escolhido-1]
            print(f'\nO Filme selecionado foi {filme_escolhido['Title']}, {filme_escolhido['Year']}')
        elif escolha.lower() == 'n':
            filme_escolhido = None
        else:
            print("Por favor, digite uma opção válida.")      

    return filme_escolhido

def get_dados_filme(titulo, ano):
    api =  'b097dd2b'
    url = f'http://www.omdbapi.com/?apikey={api}&t={titulo}&y={ano}&plot=full'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        print('Filme não localizado')

def traduzir(texto, ling):
    translator = Translator()
    idioma_origem = translator.detect(texto).lang
    traducao = translator.translate(texto, src=idioma_origem, dest=ling).text
    return traducao

def saudar(hora):
    hora = hora.strftime("%H")
    hora = int(hora)
    if 6 <= hora < 12:
        return "Bom dia!"
    elif 12 <= hora < 18:
        return "Boa tarde!"
    else:
        return "Boa noite!"
    
while True:
    hora = datetime.now()
    saudacao = saudar(hora)
    print(f'{saudacao}. Bem-vindo ao seu ranking de filmes! Explore e classifique os melhores filmes de todos os tempos.')
    menu = input('O que deseja hoje? (a)dicionar filmes? (v)er catalogo de filmes, (d)eletar filmes do seu ranking? (a)lterar nota de algum filme? [s]air? ')
    if menu.lower() == 'a': 
        adicionando_filmes = True
        while adicionando_filmes == True:
            filme_input = input('Que filme deseja adicionar: ')
            try: 
                nome_filme = nome_filme_formatado(filme_input)
                data = get_filme(nome_filme)
            except:
                print('Nome Inválido')

            if data['Response'] == 'True':
                filme_escolhido = escolher_filme(data)
                if filme_escolhido is not None:            
                    filme_detalhes = get_dados_filme(filme_escolhido['Title'], filme_escolhido['Year'])            
                    filme_plot = traduzir(filme_detalhes['Plot'], 'pt')
                    genero = traduzir(filme_detalhes['Genre'], 'pt' )
                    print('Enredo: ', filme_plot,'\n')
                    adicionar = input('Deseja adicionar este filme ao seu ranking pessoal? (s/n)')
                    if adicionar.lower() == 's':
                        nota_usuario = input(f"Que nota você daria ao filme {filme_detalhes['Title']}? ")
                        db.inserir_filme(filme_detalhes['Title'], filme_detalhes['Year'], filme_detalhes['Runtime'], filme_detalhes['Director'],filme_detalhes['Writer'], genero, filme_detalhes['Actors'], filme_plot, filme_detalhes['imdbRating'], nota_usuario)
                        print('Filme inserido com sucesso!')
            elif data['Response'] == 'False':
                print('Filme não encontrado, tente mudar os termos de busca ou escrever o nome do filme no idioma original.')            
            resposta = input("Deseja procurar outro filme? (s/n): ")   
            if resposta.lower() == 'n':
                adicionando_filmes = False
    elif menu.lower() == 'v':
        ...
    elif menu.lower() == 'd':
                ...
    elif menu.lower() == 'a':
        ...
    else:
        exit = input('Opção não encontrada, deseja [s]air ou [r]etornar ao meu principal?')
        if exit.lower() == 's':
            break

