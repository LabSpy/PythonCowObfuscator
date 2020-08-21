import random
import math

__author__ = "Ceoletta Valentina, Zanotti Mattia, Zenari Nicolo"
__version__ = '1.0'
__email__ = "{valentina.ceoletta, mattia.zanotti, nicolo.zenari}@studenti.univr.it"

candidate_lines = ['while', 'for', 'def', 'if ']

def start(source_path):
    # apro il file da offuscare
    source = open(source_path, "r")
    output = open('./result/output.py', 'w') #creo il risultato 

    lines = source.readlines() #leggo tutte le righe del file aperto

    #indica se le variabili del codice morto sono state inizializzate
    #dead_code_variables_is_inizialized = False
    inizialize_dead_code_variables(output)

    # variabile che indica se sono in un blocco di commenti
    comment = False

    value = ('\t', ' ', '', '\n')

    i = 0  #per il numero di lanci della moneta e quindi per sapere quanti possibili inserimenti si possono fare
    key = [] #lista di numeri in binario
    key.append(1) #1 farlocco messo all'inizio del valore

    for line in lines:

        # Verifico se sto entrando in un blocco di commento
        if '"""' in line or "'''" in line:
            # se il blocco non inizia e termina sulla stessa riga, allora comment=True per indicare che sono entrato nel blocco del commento,
            # la variabile comment sarà riportata a False quando verrà trovata la fine del blocco (ovvero la stringa '""""')
            if line.count('"""') or line.count("'''")!= 2:
                comment = not comment #quindi diventa True se sono in un blocco di commento
        else:
            # Se non sono in un blocco di commento
            if comment == False:

                # verifico se ci sono commenti sulla riga, e in tal caso prendo solo la parte di stringa che lo precede
                if '#' in line: #così tolgo i commenti all'attaccante!
                    line = line[:line.find('#')] #prendo la line dall'inizio della riga al commento escluso

                # verifico che line non sia vuota
                if line != '':
                    # verifico che la line non inizi con spazi o tabulazioni (ovvero non sia nello scope di un costrutto)
                    if (not line[0] == ' ') and (not line[0] == '\t') and is_candidate(line):
                        choice = random.randint(0, 1)
                        i+=1
                        #choice
                        #0 = non viene inserito il codice morte
                        #1 = viene inserito il dead code
                        if choice == 0:
                            output.write( line ) #metto la riga candidata
                        
                        else: #choice1 == 1
                            insert_dead_code(output)
                            output.write('\n' + line) #vado a capo e riscrivo la riga nell'output

                        key.append(choice)

                    # se sono nello scope di un costrutto oppure line non è una riga candidata
                    else:

                        # verifico che line non sia fatta solo da spazi e tabulazioni
                        if any(c not in value for c in line):
                            # scrivo la line in output
                            output.write(line)
    output.write('\n')

    '''
    PER IL WATERMARK
    La chiave creata viene resttuita all'utente, con un numero di bit significativi.
    La chiave è un valore numerico da convertire in binario e da considerare di esso solo i bit meno significativi indicati 
    dal secondo valore numerico ritornato dall'offuscatore
    '''
    reversed_key = key[::-1] #inverto la lista per comodità nei calcoli, conversione in decimale da binario
    key_val = 0 #valore numerico di ritorno
    for a in range(0,len(reversed_key)):
        if reversed_key[a] == 1: #considero solo i bit a 1, quelli a 0 non influenzano il conteggio per la conversione
            #in decimale da binario ovviamente
            key_val = pow(2,a) + key_val #converto da binario a decimale


    #Restituisco le chiavi all'utente

    print('-----------------')
    print('                 ')
    print('     Chiave      ')
    print('                 ')
    print('-----------------')
    print('')
    print("Il valore della chiave è: ", key_val)
    print("Il numero dei bit meno significativi da considerare è: ", i) #ritorno del numero di bit da sinistra da considerare 
    print('')
    print('')

    #add di DeadCode alla fine del file! Viene fatto sempre!
    choice = random.randint(1,10)
    for i in range(1,choice):
        insert_dead_code(output) #inserisco un altro dead_code alla fine del file!

    #chiusura dei file
    output.close()
    source.close()

# funzione che aggiunge codice morto
def insert_dead_code(output):
    # seglie a random un file tra trash_code_(number).py
    choice = random.randint(1,10) #quante volte fa l'inseriemnto di DeadCode
    for i in range(1,choice):
        
        ran = random.randint(0, 20) #scelta di uno dei file di DeadCode
        dead_code = open('./dead_code/dead_code_' + str(ran) + '.py', 'r')

        # inserisce il file dead_code_x.py nel file output.py
        for line in dead_code.readlines():
            output.write(line)
        
        output.write('\n')
        dead_code.close()

def inizialize_dead_code_variables(output):
    '''
    Funzione che inizializza le varie funzioni o variabili che sono poi chiamate/usate dai vari DeadCode,
    quindi verrà sempre usata usa volta in tutte le run di offuscamento
    '''
    dead_code_variables = open('./dead_code/dead_code_variables.py', 'r')
    # inizializzo le variabili del codice morto
    for line in dead_code_variables: #quindi aggiungo al mio file di output tutto le variabili contenute nei vari dead code
        #indipendentemente da quale andrò ad usare
        output.write(line)
    output.write('\n')

# funzione che veriifica se la riga è una riga candidata
def is_candidate(source_string):
    for line in candidate_lines: #rispetto alle righe candidate sopra
        if line in source_string: #se nella riga passata c'è una parola tra quelle candidate!
            return True

    return False
