#!/usr/bin/env python

"""Clean comment text for easier parsing."""

from __future__ import print_function

import re
import string
import argparse


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

# You may need to write regular expressions.

def sanitize(text):
    """Do parse the text in variable "text" according to the spec, and return
    a LIST containing FOUR strings 
    1. The parsed text.
    2. The unigrams
    3. The bigrams
    4. The trigrams
    """

    # YOUR CODE GOES BELOW:
    #print(text)
    #Step 1: Replace new lines and tab characters with a single space
    text = text.replace('\n', ' ')
    text = text.replace('\t', ' ')

    #Step 2: Remove URLs
    #need to replace [text](URL) with text...idk how to do that with regex
    #might need to iterate through text ughh
    matches = re.findall(r'\[.*\]\(https?:\/\/\S+\)', text)
    for match in matches:
        sub_text= re.findall(r'\[(.*?)\]',match)[0]
        text= re.sub(r'match',sub_text,text)    
    text = re.sub(r'https?:\/\/\S+', "", text)

    #Steps 3 & 4: Split text on single space & separate external punctuations
    #This needs to be fixed bc fucks up when special characters are in the middle of words
    text = re.findall(r"[^.,!?;:\s]+|[.,!?;:]", text) #Hardcode external punctuations to be separated

    #Step 5: Remove punctuation/special characters except external punctuation
    #lol need to fix this step/above steps for special characters bc shit is hardcoded
    punctuation_ok = ['?', ';', ':', ',', '.', '!']
    punctuation = ["'"]
    for n, i in enumerate(text):
        temp = ""
        for char in i:
            char = re.sub(r"[^\w.,!?;:\']", '', char)
            temp = temp + char
        text[n] = temp
    text = list(filter(None, text)) #filter empty strings

    #Step 6: convert to lower case
    text = map(lambda x:x.lower(), text)

    # create parsed_text string
    parsed_text = ""
    for word in text:
        parsed_text += word 
        parsed_text += " "
    parsed_text = parsed_text[:-1]
    print(parsed_text)
    #return [parsed_text, unigrams, bigrams, trigrams]


if __name__ == "__main__":
    # This is the Python main function.
    # You should be able to run
    # python cleantext.py <filename>
    # and this "main" function will open the file,
    # read it line by line, extract the proper value from the JSON,
    # pass to "sanitize" and print the result as a list.

    # YOUR CODE GOES BELOW.
    temp = 'That said, is the WSJ (\"our guiding philosophy in five words is \'there shall be open borders\'\") really *that* socially conservative?'
    sanitize(temp)
