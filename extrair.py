# coding=utf-8
#
# Arquivo responsável por extrair palavras e seus tipos do wiktionary
# Após feita a extração os dados serão utilizados para criar o POS Tagger
# Utilizado no spaCy
#
# Referência:
# http://www.clips.ua.ac.be/pages/using-wiktionary-to-build-an-italian-part-of-speech-tagger
# Autor: Renato Aguiar
# 24/04/2017
#


from pattern.web import URL, DOM

from spacy.vocab import Vocab
from spacy.tagger import Tagger
from spacy.tokens import Doc
from spacy.gold import GoldParse

from pathlib import Path
import random
 
# Declaração de variáveis

def extrair():
    url = "http://en.wiktionary.org/wiki/Index:Portuguese/"
    paginas = "abcdefghijklmnopqrstuvwxyz0"
    palavras = []
    taggers = []
    tipos = ['adj','adv','article','pronoun','v','n']
    data = []

    for char in paginas:
        print(char, len(palavras))
        # Efetua o download de todas as páginas que tenham as terminações iguais a string paginas
        html = URL(url + char).download(throttle=10, cached=True)
        # Parse para a árvore HTLM
        dom = DOM(html)
        # Efetua a iteração na lista de palavras e recupera o pos Tagger
        for li in dom("li"):
            try:
                palavra = li("a")[0].content
                tagger = li("i")[0].content.split(" ")[0]
                if palavra not in palavras and tagger in tipos:
                    palavras.append(palavra)
                    tagger = formatarTagger(tagger.upper())
                    taggers.append(tagger)
                    '''with open("Output.txt", "a") as arquivo:
                        arquivo.write(palavra + "-")
                        arquivo.write(tagger)
                        arquivo.write("\n")'''
            except :
                pass

    # Declara um array para receber palavras e taggers
    dados = []
    dados.append(palavras)
    dados.append(taggers)

    # Adicionada o array em uma tupla
    tupla = tuple(dados)

    # Adiciona a tupla a um array(declarado no inicio)
    data.append(tupla)
    # print(data)
    criarPosSpaCy(data)


# Formata a tag para o formato esperado
def formatarTagger(tagger):
    if tagger == 'ADJ':
        tagger = u'A'
    elif tagger == 'ADV':
        tagger = u'AV'
    elif tagger in ('ARTICLE', 'PRONOUN'):
        tagger = u'P'

    return tagger


def criarPosSpaCy(data):

    output_dir = ''

    # Cria os diretorios
    if output_dir is not None:
        output_dir = Path(output_dir)
        ensure_dir(output_dir)
        ensure_dir(output_dir / "pos")
        ensure_dir(output_dir / "vocab")
    
    # Cria o mapa de tags
    vocab = Vocab(tag_map={'N': {'pos': 'NOUN'}, 
                           'V': {'pos': 'VERB'},
                           'A': {'pos': 'ADJ'},
                           'AV': {'pos': 'ADV'},
                           'P': {'pos': 'PRON'},
                           'NUM': {'pos': 'NUM'}})

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