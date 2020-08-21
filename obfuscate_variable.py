import tokenizer
from generate_replacement import generate
import token
import re #per le ReGeX

__author__ = "Ceoletta Valentina, Zanotti Mattia, Zenari Nicolo"
__version__ = '1.0'
__email__ = "{valentina.ceoletta, mattia.zanotti, nicolo.zenari}@studenti.univr.it"

""" Dictionary of regex pattern """
pattern_search = { 'if_pat': '\s*if\s*\w+',
                'for_pat': '\s*for\s*\w+\s*in\s*',
                'imp_pat': '\s*import\s*\w*',
                'met_pat': '\s*\w*\(\w*\)\s*',
                'ass_pat': '\s*\w*\s*\=\s*\w*',
                'wh_pat': '\s*while\s*\w*\:',
                'with_pat': '\s*with\s*[^\s.]*\s*',
                'def_pat': '\s*def\s*\w+\s*\(\w*',
                }

""" List of variable name to ignore """
ignore_variable = ['__name__', '__main__', '__doc__', '__getattr__',
                '__setattr__', '__class__', '__bases__', '__subclasses__',
                '__init__', '__dict__', 'and', 'not', '__author__',
                '__copyright__', '__credits__', '__license__', '__version__',
                '__maintainer__', '__email__', '__status__']

""" Dictionary of variable to replace """
replacement_dic = {}

""" List of imported module """
import_list = []


def obfuscate(source): #prima funzione chiamata da pythonCowObfuscator()
    """
    Given the source code,it searchs for variables name and replaces them.

    :param source: Source file.
    :return: A list of lines.
    """
    lines = tokenizer.tokenize_file(source) #spezzo le varie line del codice sorgente, che sarà ovviamente il codice
    #che deriva dal passaggio precedente
    for ind, line in enumerate(lines):
        for pattern in pattern_search.values(): #scorro i pattern che desidero trovare con le ReGeX
            match = re.search(pattern, line) #faccio il match tra line e pattern (ovvero la ReGeX)
            if match: #se ho il match
                search_variable_to_replace(line) 
    lines = replace(lines) #sostituisco le vecchie variabili con quelle nuove, lo fa per tutto il file, quindi per tutte le righe del file
    return (lines, replacement_dic)


def search_variable_to_replace(line):
    """
    For each line, it searchs for variables name, creates new variables and saves them in a dictionary.

    :param line: A single line from tokenizer.tokenize_file(...).
    """
    token_line = tokenizer.tokenize_line(line) #spezzo la line
    #prendo tutti i nomi delle variabili per sostituirli con variabili a caso
    for ind, tok in enumerate(token_line):
        old = ''
        # case 1: (var) or (var,
        if token_line[ind][1] == '(' and token_line[ind+1][0] == token.NAME and (token_line[ind+2][1] == ')' or token_line[ind+2][1] == ','):
            old = token_line[ind+1][1]

        # case 2: (var ) or (var ,
        elif token_line[ind][1] == '(' and token_line[ind+1][0] == token.NAME and token_line[ind+2][1] == ' ' and (token_line[ind+3][1] == ')' or token_line[ind+3][1] == ','):
            old = token_line[ind+1][1]

        # case 3: ( var) or ( var,
        elif token_line[ind][1] == '(' and token_line[ind+1][1] == ' ' and token_line[ind+2][0] == token.NAME and (token_line[ind+3][1] == ')' or token_line[ind+3][1] == ','):
            old = token_line[ind+2][1]

        # case 4: ( var ) or ( var ,
        elif token_line[ind][1] == '(' and token_line[ind+1][1] == ' ' and token_line[ind+2][0] == token.NAME and token_line[ind+3][1] == ' ' and (token_line[ind+4][1] == ')' or token_line[ind+4][1] == ','):
            old = token_line[ind+2][1]

        # case 5 ,var) or ,var,
        elif token_line[ind][1] == ',' and token_line[ind+1][0] == token.NAME and (token_line[ind+2][1] == ')' or token_line[ind+2][1] == ','):
            old = token_line[ind+1][1]

        # case 6: , var) or , var,
        elif token_line[ind][1] == ',' and token_line[ind+1][1] == ' ' and token_line[ind+2][0] == token.NAME and (token_line[ind+3][1] == ')' or token_line[ind+3][1] == ','):
            old = token_line[ind+2][1]

        # case 7: ,var ) or ,var ,
        elif token_line[ind][1] == ',' and token_line[ind+1][0] == token.NAME and token_line[ind+2][1] == ' ' and (token_line[ind+3][1] == ')' or token_line[ind+3][1] == ','):
            old = token_line[ind+1][1]

        # case 8: , var ) or , var ,
        elif token_line[ind][1] == ',' and token_line[ind+1][1] == ' ' and token_line[ind+2][0] == token.NAME and token_line[ind+3][1] == ' ' and (token_line[ind+4][1] == ')' or token_line[ind+4][1] == ','):
            old = token_line[ind+2][1]

        # case 9: assignment
        elif token_line[ind][0] == token.NAME and (token_line[ind+1][1] == '=' or token_line[ind+2][1] == '='):
            old = token_line[ind][1]

        # case 10: as var :
        elif token_line[ind][1] == 'as' and ((token_line[ind+1][0] == token.NAME and token_line[ind+2][1] == ':') or token_line[ind+1][0] == token.NAME):
            old = token_line[ind+1][1]

        # case 11: for var
        elif token_line[ind][1] == 'for' and token_line[ind+1][0] == token.NAME:
            old = token_line[ind+1][1]

        # case 12: if var
        elif token_line[ind][1] == 'if' and token_line[ind+1][0] == token.NAME and not token_line[ind+2][1] == '(':
            old = token_line[ind+1][1]

        # case 13: save import module
        elif token_line[ind][1] == 'import' and token_line[ind+1][0] == token.NAME:
            import_list.append(token_line[ind+1][1])

        if old not in replacement_dic.keys() and not old == '': #se old non è già presente nel dizionario di quello che si deve sostituire
            replace = generate() #genero un nome di una funziomne a caso 
            
            # Non seve il controllo se un nuovo nome di variabile esiste o meno, siamo sicuri che sia univoco
            # per il discorso di probabilità
            #while replace in replacement_dic.values(): #nel caso in cui creo un nome di una variabile già presente
            #    replace = generate() #genero un nome di una funziomne a caso
            
            replacement_dic[old] = replace #cambio il vecchio nome della funzione con quello nuovo!


def replace(lines):
    """
    For each line, it replaces the old variables name with the new ones.

    :param lines: A list of lines.
    :return: A list of modified lines.
    """
    for index, line in enumerate(lines): #guardo tutte le righe
        if not line == '\n': #se non è una riga da andare a capo e basta
            token_line = tokenizer.tokenize_line(line) #spezzo la linea
            for ind, tok in enumerate(token_line): #emumero le porzioni della riga
                #identifico se le porzioni sono nei dizionari per essere sostituitex 
                if token_line[ind][1] in replacement_dic.keys() and token_line[ind][1] not in ignore_variable:
                    if ind > 1 and token_line[ind-2][1] in import_list:
                        continue
                    if token_line[ind][0] == token.NAME and token_line[ind+1][1] == '(':
                        continue
                    token_line[ind][1] = replacement_dic.get(token_line[ind][1]) 

            lines[index] = tokenizer.untokenize_line(token_line)
    return lines #lista di linee modificate
