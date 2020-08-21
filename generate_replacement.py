from random import randint #per fare la scelta random, tipo lancio di moneta
import random
import string

__author__ = "Ceoletta Valentina, Zanotti Mattia, Zenari Nicolo"
__version__ = '1.0'
__email__ = "{valentina.ceoletta, mattia.zanotti, nicolo.zenari}@studenti.univr.it"

def length(): #per la lunghezza della nuova variabile o funzione (per il nome inteso)
    #lunghezza di massimo 20    
    """
    Returns a random integer used as length for the key name.
    """
    return randint(5,20)


def cap_letter(): #per le lettere in uppercase
    #così ho 26 possibili casi 
    """
    Random generator for uppercase letter.
    """
    letters = string.ascii_uppercase
    random_letter = random.choice(letters)

    return random_letter


def low_letter(): #per le lettere il lowercase
    #così ho 26 possibili casi
    """
    Random generator for lowercase letter.
    """
    letters = string.ascii_lowercase
    random_letter = random.choice(letters)

    return random_letter


def choice_letter(): #sceglie se la letterà saà maiuscola o minuscola
    #Così ho 26 possibili casi per ogni scelta
    """
    Random generator for choosing the next letter.
    """
    if randint(0,1) == 0:
        return cap_letter()
    else:
        return low_letter()


def generate(): #genera un nuovo nome di variabile/funzione in modo random
    #Genero un nuovo nome e la probabilità di generare lo stesso nome due volte è di:
    # 1/(52^n) * 1/(52  ^n) ....con n compreso tra 5 e 20
    #Quindi la probabilità è estremamente bassa
    """
    Generates a new variable/function name.
    """
    key = ''
    for i in range(0, length()):
        key+=choice_letter()
    return key
