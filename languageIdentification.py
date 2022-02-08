#Author: Ethan Morgan
#uniqname: etcmo

import sys
import os
import math
import json


#purpose: 
#   1. use trainBigramLanguageModel to build a unigram and bigram dictionaries for each of the three language files provided as training
#   2. open the test file, provided as the first argument on the command line, and for each line in the test file, apply identifyLanguage function
#input:     string (text for which the language is to be identified),
#           list of strings (each correspondin to a language name),
#           list of dictionaries with single character frequencies (each corresponding to the single character frequencies in a language),
#           list of dictionaries with bigram character frequencies (each dictionary corresponding to the bigram character frequencies in a language)
#               (in the input lists, elements at a given positon K in the lists correspond to the same language L)
#output:    string (the name of the most likely language)
def identifyLanguage(languageText, languages, languageCharacterFreq, languageBigramCharacterFreq):
    """ Function will determine the language of a string
    Parameters:
        languageText (str): string for language to be identified
        languages (list of str): the possible languages the text could represent
        languageCharacterFreq (list of dicts[char] to freq): list of language dicts of single character freqs for a specific language
        languageBigramCharacterFreq (list of dicts[str] to freq): each dictionary cooresponding to a language bigram character freq
    Returns:
        languageGuess (str): language that the model thinks it is
    """
    languageProbabilities = list()
    currentFrequency = 0
    #for each language
    for langNumber, language in enumerate(languages):
        
        currLanguageFrequency = 0
        singleCharFreq = 0
        bigramFreq = 0
        vocabulary = len(list(languageCharacterFreq[langNumber].keys()))
        #iterate through text
        currChar = "<start>"
        nextChar = languageText[0]
        #check to make sure it is not empty
        if len(languageText) == 0:
            continue
        
        # this chunck of code will do the bigram calculating
        #   for a design choice I decided to include the <start> tag at the beginning of lines

        #compute <start> and languageText[0]
        if not (currChar + nextChar) in languageBigramCharacterFreq[langNumber]:
            bigramFreq = 0
        else:
            bigramFreq = languageBigramCharacterFreq[langNumber][(currChar + nextChar)]
        if not currChar in languageCharacterFreq[langNumber]:
            singleCharFreq = 0
        else:
            singleCharFreq = languageCharacterFreq[langNumber][(currChar)]
        currLanguageFrequency += math.log( ( bigramFreq + 1) / (singleCharFreq + vocabulary))


        #compute for the rest of languagetext[1:] -> as in the previous code we only tested for <start> and languageText[0]
        for index in range(0, len(languageText) - 1):
            currChar = languageText[index]
            nextChar = languageText[index + 1]
            #getting bigram Frequncy
            if not (currChar + nextChar) in languageBigramCharacterFreq[langNumber]:
                bigramFreq = 0
            else:
                bigramFreq = languageBigramCharacterFreq[langNumber][(currChar + nextChar)]
            
            #getting single Char Frequency
            if not (currChar) in languageCharacterFreq[langNumber]:
                singleCharFreq = 0
            else:
                singleCharFreq = languageCharacterFreq[langNumber][(currChar)]

            #solve using log based forumla
            currLanguageFrequency += math.log( ( bigramFreq + 1) / (singleCharFreq + vocabulary))
        
        #found language frequency
        languageProbabilities.append(currLanguageFrequency)
    
    #find language with max probability
    maxIndex = 0
    for index in range(1, len(languageProbabilities)):
        if (languageProbabilities[maxIndex] < languageProbabilities[index]):
            maxIndex = index
    return languages[maxIndex]



#sample run: python languageIdentification.py languageIdentification.data/test
# it should produce a file called  languageIdentification.output

def printHelpMessage():
    print("""Help Statement:
        2 Modes of Execution:
            1. Computer: input string on command line and then output response
                $ python languageIdentification.py comp inputFile
            2. Personal: wait for user input and then computer responds.
                $ python languageIdentification.py person
        """)
    return

def computerMode(languages, languageCharacterFreq, languageBigramCharacterFreq):
    return 1

def personMode(languages, languageCharacterFreq, languageBigramCharacterFreq):
    print("Press q to quit")
    while(True):
        print("Write your language:")
        text = input()
        if text == "q" or text == "quit":
            return
        if len(text) == 0:
            continue
        print(identifyLanguage(text, languages, languageCharacterFreq, languageBigramCharacterFreq))

if __name__ == '__main__':    

    #checking for input validity
    if len(sys.argv) < 1:
        printHelpMessage()
        exit(1)
    if sys.argv[1] != "comp" and sys.argv[1] != "person":
        printHelpMessage()
        exit(1)

    #load in constants
    languages = os.listdir("data/training")
    languageCharacterFreq = list()
    languageBigramCharacterFreq = list()

    file = open("data/model/languageBigramCharacterFreq.json", "r", encoding="utf-8")
    languageBigramCharacterFreq = json.load(file)
    file = open("data/model/languageCharacterFreq.json", "r", encoding="utf-8")
    languageCharacterFreq = json.load(file)


    if sys.argv[1] == "comp":
        computerMode(languages, languageCharacterFreq, languageBigramCharacterFreq)
    elif sys.argv[1] == "person":
        personMode(languages, languageCharacterFreq, languageBigramCharacterFreq)

    exit(0)
    
    #ii:    run identifyLanguage on each line
    testLines = open(sys.argv[1], "r", encoding="ISO-8859-1")
    languageIdentificationOutput = open("languageIdentification.output", "w",  encoding="ISO-8859-1")
    #for each line in the test run identifyLanguage
    for index, testLine in enumerate(testLines):
        languageGuess = identifyLanguage(testLine, languages, languageCharacterFreq, languageBigramCharacterFreq)
        languageIdentificationOutput.write(str(index + 1) + " " + languageGuess + "\n")

    languageIdentificationOutput.close()
