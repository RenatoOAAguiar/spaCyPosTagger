# coding=utf-8
#
# Arquivo responsável por extrair palavras e seus tipos de um diretório com arquivos de texto
# Após feita a extração os dados serão utilizados para criar o POS Tagger
# Utilizado no spaCy
#
# Autor: Renato Aguiar
# 25/04/2017
#

import sys
import glob
import errno
import os
import random
import json

from spacy.vocab import Vocab
from spacy.tagger import Tagger
from spacy.tokens import Doc
from spacy.gold import GoldParse

from pathlib import Path

os.chdir("Arquivos") 

palavras = []
tags = []
execoes = ['"_"', '(_(', ')_)', ':_:', ';_;', '?_?', ',_,', '._.']
pontos = ['(', ')', '.', ',', '?', '!', ';', ':', '-', '[', ']', '/', '\\']
simbolos = ['$', '%']
data = []
englishWords = ['made', 'CHANGE', 'in', 'of', 'et', 'and', 'OK', 'Me', 'Too']
excluidos = ['', 'NDAD', 'NHOR']
__noun__ = ['NEST', 'NPRO', 'PROP', 'IN']
__adj__ = ['ADJEST', 'PCP']
__adv__ = ['PDEN', 'ADVEST', 'ADV-KS-REL', 'ADV-KS', 'ADVHOR']
__det__ = ['ART', 'ARTEST', 'DET']
__cconj__ = ['KC', 'KS']
__propn__ = ['NPROP']
__pron__ = ['PROADJ', 'PROPESS', 'PROSUB', 'PRO-KS-REL', 'PRO-KS']
__sym__ = ['CUR']
__num__ = ['NAP', 'NTEL', 'NDAT', 'NUMTEL', 'PRO-KS']

def extrair():
    for file in glob.glob("*.txt"):
        try:
            with open(file) as f: 
                for line in f:
                    for word in line.split("\n"):
                        palavra = word.split("_")[0]
                        if word in execoes or palavra in englishWords:
                            continue
                        elif palavra != '':
                            tag = word.split("_")[1]
                            aux = tratarPontosSimbolos(palavra)
                            if aux is not None:
                                tag = aux
                            tag = formatarTag(tag)
                            tag = formataTags(tag)
                            if tag not in excluidos:
                                palavras.append(palavra)
                                tags.append(tag)

        except IOError as exc:
            if exc.errno != errno.EISDIR: 
                raise 

    # Declara um array para receber palavras e taggers
    dados = []
    dados.append(palavras)
    dados.append(tags)
    with open('../tags.json', 'w') as f:
        json.dump(tags, f)

    # Adicionada o array em uma tupla
    tupla = tuple(dados)

    # Adiciona a tupla a um array(declarado no inicio)
    data.append(tupla)
    # print(data)
    criarPosSpaCy(data)

def formataTags(tag):
    if tag in __noun__:
        return "N"
    elif tag in __adj__:
        return "ADJ"
    elif tag in __adv__:
        return "ADV"
    elif tag in __det__:
        return "A"
    elif tag in __cconj__:
        return "C"
    elif tag in __propn__:
        return "PR"
    elif tag in __pron__:
        return "P"
    elif tag in __sym__:
        return "SYM"
    elif tag in __num__:
        return "NUM"
    else:
        return tag

def formatarTag(tag):
    return tag.replace('|+', '').replace('|', '').replace('!','').replace('[','').replace(']', '').replace('.', '').replace('/', '').replace('=', '').replace(',', '').replace('((','').replace('))','').replace('`','').replace("'", "").rstrip()

def tratarPontosSimbolos(palavra):
    if palavra in pontos:
        return 'PUNCT'
    elif palavra in simbolos:
        return 'SYM'

def criarPosSpaCy(data):
    
    # Setar diretorio onde está localizado o model
    output_dir = ''

    # Cria os diretorios
    if output_dir is not None:
        output_dir = Path(output_dir)
        ensure_dir(output_dir)
        ensure_dir(output_dir / "pos")
        ensure_dir(output_dir / "vocab")
    
    # Cria o mapa de tags
    # Lembrar de não repetir o 'pos', se não o python da crash ao treinar model
    
    vocab = Vocab(tag_map={'N': {'pos': 'NOUN'},
                           'PR': {'pos': 'PROPN'},
                           'V': {'pos': 'VERB'},
                           'ADJ': {'pos': 'ADJ'},
                           'ADV': {'pos': 'ADV'},
                           'PREP': {'pos': 'ADP'},
                           'A': {'pos': 'DET'},
                           'C': {'pos': 'CCONJ'},
                           'P': {'pos': 'PRON'},
                           'PUNCT': {'pos': 'PUNCT'},
                           'NUM': {'pos': 'NUM'},
                           'VAUX': {'pos': 'AUX'},
                           'SYM': {'pos': 'SYM'}})


    # Cria o tagger
    tagger = Tagger(vocab)

    # Itera em todas as palavras que estão na tupla "palavras"
    for palavras, tags in data:
        doc = Doc(vocab, words=palavras)
        gold = GoldParse(doc, tags=tags)
        tagger.update(doc, gold)
    random.shuffle(data)

    # Treina o model
    tagger.model.end_training()

    if output_dir is not None:
        tagger.model.dump(str(output_dir / 'pos' / 'model'))
        with (output_dir / 'vocab' / 'strings.json').open('w') as file_:
            tagger.vocab.strings.dump(file_)

def ensure_dir(path):
    if not path.exists():
        path.mkdir()

def main():
    extrair()


if  __name__ =='__main__':
    main()