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
                            palavras.append(palavra)
                            tag = word.split("_")[1]
                            aux = tratarPontosSimbolos(palavra)
                            if aux is not None:
                                tag = aux
                            tag = formatarTag(tag)
                            tags.append(tag)
                            if tag == '((':
                                print(palavra)

        except IOError as exc:
            if exc.errno != errno.EISDIR: 
                raise 

    # Declara um array para receber palavras e taggers
    dados = []
    dados.append(palavras)
    dados.append(tags)

    # Adicionada o array em uma tupla
    tupla = tuple(dados)

    # Adiciona a tupla a um array(declarado no inicio)
    data.append(tupla)
    # print(data)
    criarPosSpaCy(data)

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
    vocab = Vocab(tag_map={'N': {'pos': 'NOUN'},
                           'NEST': {'pos': 'NOUN'},
                           'NPRO': {'pos': 'NOUN'},
                           'PROP': {'pos': 'NOUN'},
                           'IN': {'pos': 'NOUN'},
                           'NPROP': {'pos': 'PROPN'},
                           'V': {'pos': 'VERB'},
                           'ADJ': {'pos': 'ADJ'},
                           'PCP': {'pos': 'ADJ'},
                           'ADJEST': {'pos': 'ADJ'},
                           'ADV': {'pos': 'ADV'},
                           'PDEN': {'pos': 'ADV'},
                           'ADVEST': {'pos': 'ADV'},
                           'ADV-KS-REL': {'pos': 'ADV'},
                           'ADV-KS': {'pos': 'ADV'},
                           'ADVHOR': {'pos': 'ADV'},
                           'PREP': {'pos': 'ADP'},
                           'ART': {'pos': 'DET'},
                           'ARTEST': {'pos': 'DET'},
                           'KC': {'pos': 'CCONJ'},
                           'KS': {'pos': 'CCONJ'},
                           'PROADJ': {'pos': 'PRON'},
                           'PRO-KS-REL': {'pos': 'PRON'},
                           'PROPESS': {'pos': 'PRON'},
                           'PROSUB': {'pos': 'PRON'},
                           'PRO-KS': {'pos': 'PRON'},
                           'PUNCT': {'pos': 'PUNCT'},
                           'CUR': {'pos' : 'SYM'},
                           'NUM': {'pos': 'NUM'},
                           'NAP': {'pos': 'NUM'},
                           'NTEL': {'pos': 'NUM'},
                           'NDAT': {'pos': 'NUM'},
                           'NUMTEL': {'pos': 'NUM'},
                           'VAUX': {'pos': 'AUX'},
                           'SYM': {'pos': 'SYM'},
                           '': {'pos': 'X'},
                           'NDAD': {'pos': 'X'},
                           'NHOR': {'pos': 'X'},})


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