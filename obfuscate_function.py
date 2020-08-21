import tokenizer
from generate_replacement import generate
import token
import re


""" Dictionary of function to replace """
replacement_dic = {}


def obfuscate(source,dictionary): #il file sorgente (del passaggio precedente) e il dizionario delle variabili da sostituire
    """
    Given the source code and the variable dictionary,it searchs for function name and replaces them.

    :param source: Source file.
    :param dictionary: Variable dictionary.
    :return: A list of lines.
    """
    lines = tokenizer.tokenize_file(source) #spezzo il file in lines
    for ind, line in enumerate(lines): #idicizzo le lines e le controllo tutte
        pattern_search = '\s*def\s*\w+\s*\(\w*' #ReGeX da cercare, per le def = funzioni
        match = re.search(pattern_search, line) #applico la ReGeX e cerco le def
        if match: #se ci sono dei match nella line di questa iterazione
            search_function_to_replace(line, dictionary) #chiamta di funzione per cambiare il nome della funzione in tale line
    lines = replace(lines) #faccio il cambio della line con quelle presenti nel dizionario

    return lines


def search_function_to_replace(line,dictionary):
    """
    For each line, it searchs for function name, creates new variables and saves them in a dictionary.

    :param line: A single line from tokenizer.tokenize_file(...).
    :param dictionary: Variable dictionary.
    """
    token_line = tokenizer.tokenize_line(line) #spezzo la line
    for ind, tok in enumerate(token_line):
        old = ''

        if token_line[ind][1] == 'def' and token_line[ind+1][0] == token.NAME: #se la line è una dichiarazione di funzione
            #quindi ha una def
            old = token_line[ind+1][1] #salvo l'od line

        replace = generate() #genero un nuovo nuìome per la funzione (generate() in generate_replacement.py)
        if replace not in dictionary.values() and old not in replacement_dic.keys() and not old == '': #se questo nome non è 
            #già nel dizionario e non è quello che si vuole cambiare 

            # Non seve il controllo se un nuovo nome di variabile esiste o meno, siamo sicuri che sia univoco
            # per il discorso di probabilità
            #while replace in replacement_dic.values(): #se il nuovo nome è già presente nel dizionario dei nomi delle funzioni
            #    replace = generate() #nel caso, genero un altro nome random

            replacement_dic[old] = replace #sostituisco all'indice dell'old il nuovo nome della funzione


def replace(lines):
    """
    For each line, it replaces the old functions name with the new ones.

    :param lines: A list of lines.
    :return: A list of modified lines.
    """
    for index, line in enumerate(lines): #guardo ogni line del file
        if not line == '\n': #evito le line con lo \n, quelle che vanno a capo
            token_line = tokenizer.tokenize_line(line) #spezzo la line
            for ind, token in enumerate(token_line): #guardo i token della line
                if token_line[ind][1] in replacement_dic.keys(): #se il nome della def è nel dizionario delle funzioni da cambiare
                    token_line[ind][1] = replacement_dic.get(token_line[ind][1]) #cambio il nome della funzione

            lines[index] = tokenizer.untokenize_line(token_line) #ricostruisco la line
    return lines #ritorno le righe del file
