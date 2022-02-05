#Author: Ethan Morgan
#Purpose of file:
#   compute all constants (python dicts) and store in data/model/...

import os
import sys
import json


#given an input string, this function will calculate the frequencies for all the single characters and for all the bigram characters in the string
#input:     string (training text in a given language)
#output:    dictionary with character frequencies collected from the string; dictionary with character-bigram frequencies collected from the string
def trainBigramLanguageModel(trainingText):
    """Function to train a bigram language model
    Given an input string, this will calculate the frequencies for all the single characters
    and for all bigram characters in the string.
    Parameters:
        trainingText (str): training text of a given language
    Returns:
        characterFreq (dict of chars): character frequencies collected from the string
        characterBigramFreq (dict of str): character bigram frequencies collected from string
    """
    trainingText = trainingText.lower()
    characterFreq = {}
    characterBigramFreq = {}
    
    for string in trainingText.split('\n'):
        previousChar = "<start>"

        for char in string:
            #Unigram freq
            if not char in characterFreq:
                characterFreq[char] = 1
            else:
                characterFreq[char] += 1

            #bigram freq
            if not (previousChar + char) in characterBigramFreq:
                characterBigramFreq[(previousChar + char)] = 1
            else:
                characterBigramFreq[(previousChar + char)] += 1
            
            previousChar = char
    

    return characterFreq, characterBigramFreq


if __name__ == '__main__':    
    languageTrainingFiles = os.listdir("data/training")
    languages = os.listdir("data/training")
    languageCharacterFreq = list()
    languageBigramCharacterFreq = list()


    for language in languages:

        f = open("data/training/" + language, "r", encoding="utf-8")
        characterFreq, characterBigramFreq = trainBigramLanguageModel(f.read())
        languageCharacterFreq.append(characterFreq.copy())
        languageBigramCharacterFreq.append(characterBigramFreq.copy())
        f.close()

    #dump languageBigramCharacterFreq constants to json file
    file = open("data/model/languageBigramCharacterFreq.json", "w+", encoding="utf-8")
    json.dump(languageBigramCharacterFreq, file)
    file.close()

    #dump languageCharacterFreq constants to json file
    file = open("data/model/languageCharacterFreq.json", "w+", encoding="utf-8")
    json.dump(languageCharacterFreq, file)
    file.close()

