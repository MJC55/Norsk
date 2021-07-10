##### Code and GUI created by Chamberlin Michele, reliant on excel file created by Maciej Szybiak, Summer 2020
#### Questions or comments to: mjchamberlin26@gmail.com


import random
import pandas as pd
import numpy as np
from difflib import SequenceMatcher
from pandas import ExcelWriter
import os.path
from os import path
import tkinter as tk


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


path_to_folder = "C:/Users/michelechamberlin/Desktop"
if path.exists(str(path_to_folder) + "/Norske_Verber_Test.xlsx"):
    DF = pd.read_excel(str(path_to_folder) + "/Norske_Verber_Test.xlsx", sheet_name='Final')
    print('Previous file loaded')
else:
    DF = pd.read_excel(str(path_to_folder) + "/Norske Verber.xlsx", sheet_name='Final')
    print('No previous file found, will work with original file')
    DF['Hints'] = 0  # Count given hints
    DF['Level Presens'] = 0  # Count correct answers
    DF['Level Preteritum'] = 0  # Count correct answers
    DF['Level Perfekt'] = 0  # Count correct answers
    DF['Done'] = 0  # Count correct answers

wellDoneList = ['Godt jobbet!', 'bra gjort!', 'bravo!', 'gratulerer!', 'super!', 'hva et udyr!', 'Ma che bravo!',
                'Che BEEESTIA!']
tenseList = ['Presens', 'Preteritum','Perfekt']
prevAnswer = 'x'  # initialize variable in order to avoid empty variable

print('\n \n----------------------------------------------------------------')
print(
    'Velkommen til verbstesting \nskriv "h" for et hint, \nskriv "x" for å gå videre til neste verb tid \nskriv "save" for å lagre filen \ntrykk "Ctrl + F2" for å avslutte øvelsen')
print('----------------------------------------------------------------\n \n')
pd.set_option('mode.chained_assignment', None)



def Test(Ans, tense, tries, hints, numb): #
    tense_given = tense
    # tries = 0
    # hints = 0
    global prevAnswer
    empty_Verb_complete = Label(text='', width=50, height=2, font=('Helvetica', 18, '')).grid(row=7,
                                                                                              columnspan=2)  # empty space
    print(DF[str(tenseList[tense])][numb])
    # print(prevAnswer)
    if tries == 0 and hints == 0 and tense == 1:
        print('Verbet er: ' + str(DF['Tysk'][numb]) + ' (' + str(DF['Engelsk'][numb]) + ')')
    #print(str(tenseList[tense]) + '?')
    # Ans = return_entry()#str(input())
    if Ans != 'h':
        prevAnswer = Ans
        # print('prev answer registered')
        # print(prevAnswer)
    if Ans == DF[str(tenseList[tense])][numb]:

        print(random.choice(wellDoneList))
        feedback(2)
        hints=0
        if DF['Hints'][numb] <= 0:
            DF[('Level ' + str(tenseList[tense]))][numb] = 1  # Success at 3, verb will no longer be asked

            if np.sum(DF['Level Presens'][numb] + DF['Level Preteritum'][numb] + DF['Level Perfekt'][numb]) == 3:
                DF['Done'][numb] = 1
                feedback(10)
                verb_complete(numb)
        else:

            DF['Hints'][numb] = DF['Hints'][
                                    numb] - 1  # Hint index is reduced by one, verb will be asked again until all hints have been compensated by correct answers without use of hints
        #print('tense Test')
        #print(tense)
        if tense == 2:  # Move on to next tense, or begin again with new verb
            tense = 0
            numb = new_numb()
        else:
            tense = tense + 1
        current_verb(numb)
        current_tense(tense)
        print(DF[str(tenseList[tense])][numb])
        #print('tense Test 2')
        #print(tense)

        #print(tenseList[tense])
        return tense, hints, numb
    #elif Ans == 'x':
        #print('Ha det!')

    elif Ans == 'h':
        ratio = 1
        counter = 0
        if hints > 5:
            print('Mann...du er virkelig dårlig, kom igjen!')

        while ratio == 1:
            ratio = similar(prevAnswer[0:counter + 1], DF[str(tenseList[tense])][numb][0:counter + 1])
            # print(prevAnswer[0:counter+1])
            # print(DF['Presens'][numb][0:counter+1])
            counter = counter + 1

        empty = Label(text='Hint: '+DF[str(tenseList[tense])][numb][0:counter + hints], width=50, height=2,
                      font=('Helvetica', 18, '')).grid(row=6,
                                                       columnspan=2)  # empty space
        print('Hint: '+DF[str(tenseList[tense])][numb][0:counter + hints])
        print(hints)
        hints = hints + 1  ## Internal index to defeine how much of solution is shown
        DF['Hints'][numb] = DF['Hints'][
                                numb] + 1  # Overall Index to define how many times the verb will be asked until given correctly without hints
        # print(hints)
        return tense, hints, numb
    elif Ans == 'save': ## TODO Add as button
        with ExcelWriter(str(path_to_folder) + '/Norske_Verber_Test.xlsx') as writer:
            DF.to_excel(writer, sheet_name='Final')
            print('Filen er lagret under "Norske_Verber_Test" i depotet ditt')
        empty = Label(text='Filen er lagret under "Norske_Verber_Test" i depotet ditt', width=50, height=2,
                      font=('Helvetica', 18, '')).grid(row=6,
                                                       columnspan=2)  # empty space
        return tense, hints, numb


    elif similar(Ans, DF[str(tenseList[tense])][numb]) > 0.6:
        tries = tries + 1
        ratio = similar(Ans, DF[str(tenseList[tense])][numb])
        print('Nesten (' + str(100 * round(ratio, 3)) + '% match)! Prøv igjen (skriv "h" for et hint)')
        feedback(1)
        return tense, hints, numb
        # Test(tense_given,tries,hints,numb)
    elif Ans == '':
        print('Du må skrive noe....')
        feedback(-1)
        return tense, hints, numb
        # Test(tense_given, tries, hints, numb)

    elif similar(Ans, DF[str(tenseList[tense])][numb]) < 0.6:
        tries = tries + 1
        print('Ikke helt (not quite)! Prøv igjen (skriv "h" for et hint)')
        feedback(0)
        return tense, hints, numb
        # Test(tense_given, tries, hints,numb)

def return_entry(tense_here, tries, hints_here, numb, option):
    """Gets and prints the content of the entry"""
    if option !='nothing':
        content= str(option)
    else:
        content = entry.get()
    print(content)
    #print(tense)
    global tense, hints
    print(content, tense_here, tries, hints_here, numb)
    tense, hints, numb = Test(content, tense_here, tries, hints_here, numb) ## here correct tense
    print(tense, hints, numb )
    #print(tense_here)
    entry.delete(0, 'end')
    #print('tense return entry')
    #print(tense)

    #return tense


def feedback(correctness_level):
    if correctness_level == -1:
        empty = Label(text='Du må skrive noe....', width=50, height=2, font=('Helvetica', 18, '')).grid(row=6,
                                                                                                        columnspan=2)  # empty space
    if correctness_level == 0:
        empty = Label(text='Ikke helt (not quite)! Prøv igjen (skriv "h" for et hint)', width=50, height=2,
                      font=('Helvetica', 18, '')).grid(row=6,
                                                       columnspan=2)  # empty space
    if correctness_level == 1:
        empty = Label(text='Nesten (skriv "h" for et hint)', width=50, height=2,
                      font=('Helvetica', 18, '')).grid(row=6,
                                                       columnspan=2)  # empty space
    if correctness_level == 2:
        empty = Label(text=random.choice(wellDoneList), width=50, height=2,
                      font=('Helvetica', 18, '')).grid(row=6,
                                                       columnspan=2)  # empty space
    if correctness_level == 10:
        empty = Label(text='', width=50, height=2,
                      font=('Helvetica', 18, '')).grid(row=6,
                                                       columnspan=2)  # empty space


def new_numb():
    print('new numb used')
    global numb

    numb = np.random.randint(0, 408)  # 407 is max that can be drawn
    if DF['Done'][numb]==1:
        numb=new_numb()
    print(DF[str(tenseList[tense])][numb])
    print(numb)

    return numb

def verb_complete(numb):
    empty_Verb_complete = Label(text='Greit, du fullførte verbet "' + str(DF['Presens'][numb]) + ', ' + str(
        DF['Preteritum'][numb]) + ', ' + str(DF['Perfekt'][numb]) + '" (' + str(
        np.sum(DF['Done'])) + ' av 408)', width=50, height=2, font=('Helvetica', 18, '')).grid(row=7,
                                                                                                columnspan=2)  # empty space

def current_verb(numb):
    print(numb)
    label =Label(text='Verbet er: ' + str(DF['Tysk'][numb]) + ' (' + str(DF['Engelsk'][numb]) + ')', width=50, height=5, font=('Helvetica', 18, '')).grid(row=3,
                                                                                                 columnspan=2)
def current_tense(tense):
    entry_tense = Label(text=tenseList[tense], width=50, height=2, font=('Helvetica', 18, 'bold')).grid(row=4, columnspan=2)



tense_here = 0
tense = 0
hints = 0
tries = 0


if __name__ == "__main__":

    numb = new_numb()
    #tense = 1
    print('vars initialized')
    from tkinter import *

    master = Tk()
    master.title('Norske Verber')

    tense_here = 0
    tense = 0
    hints = 0
    tries = 0

    # master.geometry("1000x500")

    # Create this method before you create the entry



    #label = Label(text="Hello, Tkinter firend", width=50, height=5, font=('Helvetica', 18, '')).grid(row=3, columnspan=2)  # Width and heiht in text units ##foreground="white", background="black"
    # Label(master, text="Input: ",  height = 10, font=('Helvetica',18,'')).grid(row=4)

    #greeting = Label(text="Norske Verber", font=('Helvetica', 12, '')).grid(row=0, columnspan=2)
    empty = Label(text="", width=70, height=2, font=('Helvetica', 18, '')).grid(row=2, columnspan=2)  # empty space
    label = Label(text='Verbet er: ' + str(DF['Tysk'][numb]) + ' (' + str(DF['Engelsk'][numb]) + ')', width=50,
                  height=5, font=('Helvetica', 18, 'bold')).grid(row=3,
                                                             columnspan=2)
    entry_tense = Label(text=tenseList[tense], width=50, height=2, font=('Helvetica', 18, 'bold')).grid(row=4, columnspan=2)
    entry = Entry(master, width=50, font=('Helvetica', 18, ''))
    entry.grid(row=5, columnspan=2)
    empty_5 = Label(text='', width=50, height=2, font=('Helvetica', 18, '')).grid(row=6, columnspan=2)  # empty space
    empty_Verb_complete = Label(text='', width=50, height=2, font=('Helvetica', 18, '')).grid(row=7, columnspan=2)  # empty space
    B = Button(text ="Hint", font=('Helvetica', 16, ''), command=lambda: return_entry(tense, tries, hints, numb,'h') ).grid(row=8,column=0)#command = helloCallBack
    B = Button(text="Save Progress", font=('Helvetica', 16, ''),  command=lambda: return_entry(tense, tries, hints, numb, 'save')).grid(row=8,
                                                                                  column=1)  # command = helloCallBack
    empty_5 = Label(text='', width=50, height=2, font=('Helvetica', 18, '')).grid(row=9, columnspan=2)  # empty space


    #B = Button(text="Check", command=lambda: return_entry(tense, tries, hints, numb)).grid(row=6, column=2)  # command = helloCallBack

    # Connect the entry with the return button
    #print(tense)
    entry.bind('<Return>', lambda x: return_entry(tense, tries, hints, numb,'nothing'))

    mainloop()
