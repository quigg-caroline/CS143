#!/usr/bin/env python

"""Clean comment text for easier parsing."""

from __future__ import print_function

import re
import string
import argparse
import json
import sys

__author__ = ""
__email__ = ""

# Some useful data.
_CONTRACTIONS = {
    "tis": "'tis",
    "aint": "ain't",
    "amnt": "amn't",
    "arent": "aren't",
    "cant": "can't",
    "couldve": "could've",
    "couldnt": "couldn't",
    "didnt": "didn't",
    "doesnt": "doesn't",
    "dont": "don't",
    "hadnt": "hadn't",
    "hasnt": "hasn't",
    "havent": "haven't",
    "hed": "he'd",
    "hell": "he'll",
    "hes": "he's",
    "howd": "how'd",
    "howll": "how'll",
    "hows": "how's",
    "id": "i'd",
    "ill": "i'll",
    "im": "i'm",
    "ive": "i've",
    "isnt": "isn't",
    "itd": "it'd",
    "itll": "it'll",
    "its": "it's",
    "mightnt": "mightn't",
    "mightve": "might've",
    "mustnt": "mustn't",
    "mustve": "must've",
    "neednt": "needn't",
    "oclock": "o'clock",
    "ol": "'ol",
    "oughtnt": "oughtn't",
    "shant": "shan't",
    "shed": "she'd",
    "shell": "she'll",
    "shes": "she's",
    "shouldve": "should've",
    "shouldnt": "shouldn't",
    "somebodys": "somebody's",
    "someones": "someone's",
    "somethings": "something's",
    "thatll": "that'll",
    "thats": "that's",
    "thatd": "that'd",
    "thered": "there'd",
    "therere": "there're",
    "theres": "there's",
    "theyd": "they'd",
    "theyll": "they'll",
    "theyre": "they're",
    "theyve": "they've",
    "wasnt": "wasn't",
    "wed": "we'd",
    "wedve": "wed've",
    "well": "we'll",
    "were": "we're",
    "weve": "we've",
    "werent": "weren't",
    "whatd": "what'd",
    "whatll": "what'll",
    "whatre": "what're",
    "whats": "what's",
    "whatve": "what've",
    "whens": "when's",
    "whered": "where'd",
    "wheres": "where's",
    "whereve": "where've",
    "whod": "who'd",
    "whodve": "whod've",
    "wholl": "who'll",
    "whore": "who're",
    "whos": "who's",
    "whove": "who've",
    "whyd": "why'd",
    "whyre": "why're",
    "whys": "why's",
    "wont": "won't",
    "wouldve": "would've",
    "wouldnt": "wouldn't",
    "yall": "y'all",
    "youd": "you'd",
    "youll": "you'll",
    "youre": "you're",
    "youve": "you've"
}

# Generates all possible n-grams for a set of phrases
# e.g. makeNGrams([['foo', 'bar', 'baz'], ['xyz', 'uvw']], 2) => 'foo_bar bar_baz xyz_uvw'
def makeNGrams(phrases, n):
    nGramList = []
    
    for phrase in phrases:
        index = 0
        while (index < len(phrase) - (n - 1)):
            currNGram = "_".join(phrase[index:index+n])
            nGramList.append(currNGram)
            index += 1
    return " ".join(nGramList)

# Splits a list across any/all of the given splitters
# e.g. splitList([1, 2, 3, 4], [2]) => [[1], [3, 4]]
def splitList(l, splitters):
    finalList = [[]]
    currListIndex = 0
    for item in l:
        if item in splitters:
            finalList.append([])
            currListIndex += 1
            continue
        else:
            finalList[currListIndex].append(item)
    return finalList

def sanitize(text):
    """Do parse the text in variable "text" according to the spec, and return
    a LIST containing FOUR strings 
    1. The parsed text.
    2. The unigrams
    3. The bigrams
    4. The trigrams
    """

    # YOUR CODE GOES BELOW:
    #Step 1: Replace new lines and tab characters with a single space
    text = text.replace('\n', ' ')
    text = text.replace('\t', ' ')

    #Step 2: Remove URLs
    matches = re.findall(r'\[.*\]\(https?:\/\/\S+\)', text)
    for match in matches:
        sub_text= re.findall(r'\[(.*?)\]',match)[0]
        text= re.sub(r'match',sub_text,text)    
    text = re.sub(r'https?:\/\/\S+', "", text)

    #Steps 3 & 4: Split text on single space & separate external punctuations
    text = re.findall(r"[^.,!?;:\s]+|[.,!?;:]", text) #Hardcode external punctuations to be separated

    #Step 5: Remove punctuation/special characters except external punctuation
    punctuation_ok = ['?', ';', ':', ',', '.', '!']
    for n, i in enumerate(text):
        temp = ""
        for char in i:
            char = re.sub(r"[^\w.,!?;:\']", '', char)
            temp = temp + char
        text[n] = temp
    text = list(filter(None, text)) #filter empty strings

    #Step 6: convert to lower case
    text = list(map(lambda x:x.lower(), text))

    # create parsed_text string
    parsed_text = ""
    for word in text:
        if word in _CONTRACTIONS:
            parsed_text += _CONTRACTIONS[word]
        else: parsed_text += word 
        parsed_text += " "
    parsed_text = parsed_text[:-1]

    # Step 8.0: Create list of phrases, where each phrase is a list of strings
    # Separating them into phrases ensures that the n-grams are made only within punctuation boundaries
    phrases = splitList(text, punctuation_ok)

    #Step 8.1 - 8.3: Create unigrams, bigrams, trigrams
    unigrams = makeNGrams(phrases, 1)
    bigrams = makeNGrams(phrases, 2)
    trigrams = makeNGrams(phrases, 3)

    # Step 9: Return results in a list
    return [parsed_text, unigrams, bigrams, trigrams]

if __name__ == "__main__":
    # This is the Python main function.
    # You should be able to run
    # python cleantext.py <filename>
    # and this "main" function will open the file,
    # read it line by line, extract the proper value from the JSON,
    # pass to "sanitize" and print the result as a list.
    with open(sys.argv[1]) as f:
        result = []
        for jsonElement in f:
            jsonData = json.loads(jsonElement)
            answer = sanitize(jsonData["body"])
            result.append(answer)
        print(result)