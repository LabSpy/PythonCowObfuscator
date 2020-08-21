import dead_code
import generate_equivalent_instructions_sequence as gen
import obfuscate_variable as ov
import obfuscate_function as of
import replace_constants as rc
import sys
import getopt
import os #per interaggire con il terminale
import time #per calcolare il tempo di esecuzione
#import psutil #per la RAM usata (N.B. non usata nel progetto...per un futuro upgrade)
from staticfg import CFGBuilder
from fpdf import FPDF

__author__ = "Ceoletta Valentina, Zanotti Mattia, Zenari Nicolo"
__version__ = '1.0'
__email__ = "{valentina.ceoletta, mattia.zanotti, nicolo.zenari}@studenti.univr.it"

def main(argv):

    if len(argv) == 0: #se non ho passato nulla è un errore
        #print('Error: invalid use.')
        #print('python3.6 pythonCowObfuscator.py <source.py>')
        #sys.exit(2)
        raise IOError( 'Error: invalid use. Please use : "python3.6 pythonCowObfuscator.py <source.py>" ' )

    try:
        opt, arg = getopt.getopt(argv, " ", ["idir="])
    except getopt.GetoptError:
        #print('Error: invalid use.')
        #print('python3.6 pythonCowObfuscator.py <source.py>')
        #sys.exit(2)
        raise IOError( 'Error: invalid use. Please use : "python3.6 pythonCowObfuscator.py <source.py>" ' )

    source = arg[0] #Nome del file passato

    #check se il file è un file .py 
    extension = os.path.splitext(source)[1]  #take extension of file
    
    if (extension != ".py") :
        raise IOError( 'Invalid input file. Please enter python file' )
    
    #check il file è nella cartella
    if os.path.isfile(source):
        print("-----------")
        print ("File exist")
        print("-----------")
        print('')
        print('')
    else:
        raise IOError( 'File not exist' )

    # create dir result if not exists
    if not os.path.exists('result'):
        os.makedirs('result')

    print('-----------------')
    print('                 ')
    print('    Obfuscate    ')
    print('                 ')
    print('-----------------')
    print('')
    print('')
    print('...In esecuzione...')
    print('')
    print('')
    
    # 0) create cfg
    cfg = CFGBuilder().build_from_file('Before_Obfuscate', source)
    a = cfg.build_visual('CFG/1)Before_Obfuscate', format='pdf', calls=True)

    # 1) dead code
    dead_code.start(source)

    # 1.1) create cfg
    cfg = CFGBuilder().build_from_file('After_Insertion_Dead_Code', './result/output.py')
    a = cfg.build_visual('CFG/2)After_Insertion_Dead_Cod', format='pdf', calls=True)

    # 2) gen sequence
    source = './result/output.py' #Apro l'output che ho creato prima nel dead code
    with open('./result/result1.py', 'w') as res: #creo il primo risultato
        for line in gen.replace_instructions(source): #nel file "generate_equivalent_instructions_sequence.py"
            res.write(line)

    # 2.1) create cfg
    cfg = CFGBuilder().build_from_file('After_Change_Sequence', './result/result1.py')
    a = cfg.build_visual('CFG/3)After_Change_Sequence', format='pdf', calls=True)

    # 3) replace constants
    source = './result/result1.py'
    with open('./result/result2.py', 'w') as res:
        for line in rc.replace_constants(source):
            res.write(line)

    # 3.1) create cfg
    cfg = CFGBuilder().build_from_file('After_Replace_Constants', './result/result2.py')
    a = cfg.build_visual('CFG/4)After_Replace_Constants', format='pdf', calls=True)

    
    # 4) replace variables (nomi di variabili e nomi di funzioni con nomi a caso)
    source = './result/result2.py'
    with open('./result/result3.py', 'w') as res:
        lines,dic = ov.obfuscate(source) #ritorna anche il dizionario delle variabile da cui fare il replace
        for line in lines:
            res.write(line)

    # 4.1) create cfg
    cfg = CFGBuilder().build_from_file('After_Replace_Variables', './result/result3.py')
    a = cfg.build_visual('CFG/5)After_Replace_Variables', format='pdf', calls=True)

    
    # 5) replace function
    source = './result/result3.py'
    with open('./result/obfuscated.py', 'w') as res: #obfuscated.py è il file finale obfuscato
        for line in of.obfuscate(source, dic): #da anche il dizionario delle variabile da cui fare il replace
            #in questo caso interesseranno solo i nomi delle funzioni
            res.write(line)

    # 5.1) create cfg
    cfg = CFGBuilder().build_from_file('After_Replace_Function', './result/obfuscated.py')
    a = cfg.build_visual('CFG/6)After_Replace_Function', format='pdf', calls=True)
    
    print('----------------------')
    print('                      ')
    print('    Text Execution    ')
    print('                      ')
    print('----------------------')
    print('')
    '''Test del tempo di esecuzione'''
    start_time = time.time() #faccio partire il cronometro
    os.system('python ' + arg[0]) #faccio partire il programma
    print("Tempo trascorso del file iniziale: %s" % (time.time() - start_time))

    start_time = time.time() #faccio partire il cronometro
    os.system('chmod 777 ./result/obfuscated.py') #cambio dei permessi del programma
    os.system('python ./result/obfuscated.py' ) #faccio partire il programma
    print("Tempo trascorso del file offuscato: %s" % (time.time() - start_time)) 
    print('')
    print('')   

if __name__ == '__main__':
    main(sys.argv[1:]) #passiamo la riga di comando eseguita
