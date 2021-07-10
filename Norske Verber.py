##### Code created by Chamberlin Michele, reliant on excel file created by Maciej Szybiak, Summer 2020
#### Questions to: mjchamberlin26@gmail.com


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
    DF = pd.read_excel(str(path_to_folder)+"/Norske Verber.xlsx",sheet_name='Final')
    print('No previous file found, will work with original file')
    DF['Hints'] = 0 # Count given hints
    DF['Level'] = 0 # Count correct answers

wellDoneList = ['Godt jobbet!', 'bra gjort!', 'bravo!', 'gratulerer!', 'super!', 'hva et udyr!', 'Ma che bravo!', 'Che BEEESTIA!']
prevAnswer='x' # initialize variable in order to avoid empty variable






def Test (tense,tries,hints,numb):
    tense_given = tense
    #tries = 0
    #hints = 0
    global prevAnswer
    #print(prevAnswer)
    if tries == 0 and hints==0 and tense == 'Presens':
        print('Verbet er: ' + str(DF['Tysk'][numb]) + ' (' + str(DF['Engelsk'][numb]) + ')')
    print(str(tense)+'?')
    Ans = str(input())
    if Ans != 'h':
        prevAnswer = Ans
        #print('prev answer registered')
        #print(prevAnswer)
    if Ans == DF[str(tense)][numb]:
        print(random.choice(wellDoneList))
        if DF['Hints'][numb] ==0:
            DF['Level'][numb] = DF['Level'][numb]+ 1 # Success at 3, verb will no longer be asked

        else: DF['Hints'][numb] = DF['Hints'][numb]-1 # Hint index is reduced by one, verb will be asked again until all hints have been compensated by correct answers without use of hints
    elif Ans == 'x':
        print('Ha det!')
    elif Ans == 'h':
        ratio = 1
        counter = 0
        if hints > 5:
            print('Mann...du er virkelig dårlig, kom igjen!')

        while ratio == 1:
            ratio = similar(prevAnswer[0:counter + 1], DF[str(tense)][numb][0:counter + 1])
            # print(prevAnswer[0:counter+1])
            # print(DF['Presens'][numb][0:counter+1])
            counter = counter + 1

        print(DF[str(tense)][numb][0:counter+hints])
        print(hints)
        hints = hints + 1 ## Internal index to defeine how much of solution is shown
        DF['Hints'][numb] = DF['Hints'][numb]+ 1 # Overall Index to define how many times the verb will be asked until given correctly without hints
        #print(hints)
        Test(tense_given, tries, hints,numb)
    elif Ans == 'save':
        with ExcelWriter(str(path_to_folder)+'/Norske_Verber_Test.xlsx') as writer:
            DF.to_excel(writer,sheet_name='Final')
            print('Filen er lagret under "Norske_Verber_Test" i depotet ditt')

    elif similar(Ans,DF[str(tense)][numb]) >0.6:
        tries = tries +1
        ratio = similar(Ans,DF[str(tense)][numb])
        print ('Nesten ('+str(100*round(ratio,3))+'% match)! Prøv igjen (skriv "h" for et hint)')
        Test(tense_given,tries,hints,numb)
    elif Ans == '':
        print('Du må skrive noe....')
        Test(tense_given, tries, hints, numb)

    elif similar(Ans,DF[str(tense)][numb]) <0.6:
        tries = tries +1
        print ('Ikke helt (not quite)! Prøv igjen (skriv "h" for et hint)')
        Test(tense_given, tries, hints,numb)







print('\n \n----------------------------------------------------------------')
print('Velkommen til verbstesting \nskriv "h" for et hint, \nskriv "x" for å gå videre til neste verb tid \nskriv "save" for å lagre filen \ntrykk "Ctrl + F2" for å avslutte øvelsen' )
print('----------------------------------------------------------------\n \n')
pd.set_option('mode.chained_assignment', None)


while np.sum(DF['Level']) != 3*len(DF['Level']):
    numb = np.random.randint(0, 408)  # 407 is max that can be drawn
    if DF['Level'][numb]<3:

        tries =0 # Currently not implemented, can be used to limit number of tries before solution is shown
        hints = 0
        Test('Presens',0,0,numb)
        Test('Preteritum',0,0,numb)
        Test('Perfekt',0,0,numb)
        if DF['Level'][numb] == 3:
            print('Greit, du fullførte verbet ' + str(DF['Presens'][numb]) + ', ' + str(DF['Preteritum'][numb]) + ', ' + str( DF['Perfekt'][numb]) + ' (' + str(np.sum(DF['Level'])) + ' av 408)')





top = tk.Tk()
# Code to add widgets will go here...
greeting = tk.Label(text="Hello, Tkinter")
label = tk.Label(text="Hello, Tkinter firend", foreground="white", background="black", width=100, height = 10) # Width and heiht in text units
#estring = tk.StringVar()
entry = tk.Entry()
greeting.pack()
label.pack()

entry.pack()


# Create this method before you create the entry
def return_entry(en):
    """Gets and prints the content of the entry"""
    content = entry.get()
    print(content)

top.mainloop()

name = entry.get()
print(name)
print(textvariable)

print(name)


top = tkinter.Tk()
L1 = tkinter.Label(top, text="User Name")
L1.pack( side=TOP)
E1 = tkinter.Entry(top, bd =5)
E1.pack(side=RIGHT)
top.mainloop()




from tkinter import *
master = Tk()
#master.geometry("1000x500")

# Create this method before you create the entry
def return_entry(en):
    """Gets and prints the content of the entry"""
    content = entry.get()
    print(content)
    entry.delete(0, 'end')
    return(content)






greeting = Label(text="Norske Verber", font=('Helvetica',25,'bold')).grid(row=0, columnspan=2)
empty = Label(text="", width=50, height = 2, font=('Helvetica',18,'')).grid(row=2, columnspan=2) # empty space
label = Label(text="Hello, Tkinter firend", width=50, height = 5, font=('Helvetica',18,'')).grid(row=3, columnspan=2) # Width and heiht in text units ##foreground="white", background="black"
#Label(master, text="Input: ",  height = 10, font=('Helvetica',18,'')).grid(row=4)

entry = Entry(master, width = 50 ,font=('Helvetica',18,''))
entry.grid(row=4, columnspan=2)
empty = Label(text="", width=50, height = 2, font=('Helvetica',18,'')).grid(row=5, columnspan=2) # empty space
B = Button(text ="Hint", command=Test('Presens',0,0,45) ).grid(row=6,column=1)#command = helloCallBack
B = Button(text ="Check" ).grid(row=6, column=2)#command = helloCallBack

# Connect the entry with the return button
entry.bind('<Return>', return_entry)

mainloop()