#!/usr/bin/python3.5
#coding: utf-8

from nltk import *
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

def filter_token():

    stop_words=set(stopwords.words("english"))

    with open('/media/DATA/Documents/MASTER2BIG/Analyse_donnees_text/data_suj1/train/BTID-10003.txt', 'r') as file:
        text=file.read()
        #text_words=[]
        text_words=word_tokenize(text)
        filtered_words = []
        for w in text_words:
            if w not in stop_words:
                filtered_words.append(w)
        
    return filtered_words
