# coding=utf-8
#
# Arquivo responsável por extrair palavras e seus tipos de um diretório com arquivos de texto
# Após feita a extração os dados serão utilizados para criar o POS Tagger
# Utilizado no spaCy
#
# Autor: Renato Aguiar
# 25/04/2017
#
# Em construção

import json


# Carrega o JSON Original
with open('strings.json') as f:
    data1 = json.load(f)
    dados1 = list(data1)

# Carrega o JSON Com novos dados
with open('vocab/strings.json') as f:
    data2 = json.load(f)
    dados2 = list(data2)

## Itera novos dados e verifica se já existem no antigo JSON

novalista = []
for texto in dados2:
    print(texto)
    novalista.append(texto)

for string in novalista:
    dados1.append(string)

# Salva o novo JSON
with open('stringsNovo.json', 'w') as f:
    json.dump(dados1, f)
