# _*_ coding:utf-8 _*_

import os
import requests
import string
import runpy
from bs4 import BeautifulSoup


url = 'https://www.letras.mus.br/estilos/'
source_code = requests.get(url)
text = source_code.text
soup = BeautifulSoup(text, "lxml")
array_estilo = []
array_artista = []
array_musica = []
array_letra = []

data = soup.findAll('div', {'class': 'g-2-3'})
for div in data:
    lis = div.findAll('li')
    for x in lis:
        links = x.findAll('a')
        for y in links:
            if y['href'] == '/estilos/bossa-nova/':
                array_estilo.append(y['href'])
            if y['href'] == '/estilos/rock-roll/':
                array_estilo.append(y['href'])
            if y['href'] == '/estilos/samba/':
                array_estilo.append(y['href'])

#coleta todos os artistas
cont = 0
n_artista = 0
while cont < array_estilo.__len__():
    n_artista = 0
    url = 'https://www.letras.mus.br' + array_estilo[cont] + 'artistas.html'
    source_code = requests.get(url)
    text = source_code.text
    soup = BeautifulSoup(text, "lxml")

    data = soup.findAll('div', {'class': 'g-mb'})
    for div in data:
        lis = div.findAll('li')
        if n_artista >= 15:
            break;
        for x in lis:
            links = x.findAll('a')
            if n_artista >= 15:
                break;
            for i in links:
                array_artista.append(i['href'])
                n_artista += 1
                if n_artista >= 15:
                    break;

    cont += 1

print(len(array_artista))
#coleta todas as musicas
cont = 0

#while cont < array_artista.__len__():
while cont < array_artista.__len__():
    url = 'https://www.letras.mus.br' + array_artista[cont]
    source_code = requests.get(url)
    text = source_code.text
    soup = BeautifulSoup(text, "lxml")

    data = soup.findAll('div', {'class': 'g-2-3'})
    for div in data:
        lis = div.findAll('li')
        for x in lis:
            links = x.findAll('a')
            for i in links:
                array_musica.append(i['href'])
                print("Colentando músicas...")
    cont += 1
print(len(array_musica))

# abre arquivo txt
dataset = open('dataset.txt', 'w', encoding='utf-8')
dataset.write('letra,label\n\n')

#acessa todas as musicas
cont = 0

#while cont < array_musica.__len__():
while cont < array_musica.__len__():

    try:
        url = 'https://www.letras.mus.br' + array_musica[cont]
        source_code = requests.get(url)
        text = source_code.text
        soup = BeautifulSoup(text, "lxml")
    except requests.exceptions.TooManyRedirects:
        print("ERRO")

    #seleciona todos os span de todos os links da tag com id=Breadcrumb, e pega o texto da segunda posicao da lista
    label = soup.select("#breadcrumb a span")[1].find_all(text=True)

    #tranforma o texto em tudo maiusculo e subtitui os espacos por underlines
    rotulo = "".join(label).upper().replace(" ", "_")

    #pega o texto da musica
    article_text = ''
    article = soup.find("div", {"class": "cnt-letra"}).findAll('p')
    for element in article:
        article_text += ' ' + ' '.join(element.findAll(text=True))

    #remove pontuação
    for c in string.punctuation:
        article_text = article_text.replace(c, "")

    #array_letra.append(rotulo + article_text)

    print("Coletando letras...")
    #escrever no arquivo
    dataset.write(article_text + ', ' + rotulo + '\n\n\n')

    cont += 1
    print(cont)

dataset.close()
#os.system('gedit dataset.txt')

