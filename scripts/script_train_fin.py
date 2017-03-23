#!/usr/bin/python3.5
# coding: utf-8

import re, glob, nltk
from nltk.tokenize import word_tokenize


def extract_entities_cat(dirname):
    """
		Extracts the entities and according categories from the .ent files in a training directory
		and returns a dictionnary of all the entities as keys and their categories as values.

		:param dirname: name of the directory where the files are located
		:type dirname: str
		:return: entities and categories of the .ent files in the training directory
		:rtype: dict of str

	"""
    d_entities = {}
    # Regex to extract the different groups (entities + categories)
    p = re.compile(r'\d+\t([A-Za-z]+)\s\d+-\d+\s([A-Za-z ]+)(\s\d+-\d+\s([A-Za-z ]+))?')

    files = glob.glob(dirname + '*.ent') # Process of all the .ent files in the directory dirname
    for file in files:
        with open(file, 'r') as fichier:
            for line in fichier:
                m = p.match(line)
                if not m: break
                cat = m.group(1)
                nom = m.group(2)
                if cat == 'Bacteria': continue #Not interrested in the names of bacteria
                mots=word_tokenize(nom, 'english') #If the entity is composed of several tokens/words
                d_entities[tuple(mots)] = cat
                if m.group(4) is not None:
                    d_entities[tuple(word_tokenize(m.group(4), 'english'))] = cat

    return d_entities


def extract_from_training(file, d_entities):
    """
        Extracts the entities and corresponding categories from the dev data files (.txt) thanks to the training data.
    :param file: path to the file to process
    :type file: str
    :param d_entities: all entities and categories extracted from the training data
    :type d_entities: dict
    :return: entities and categories of the file which are found in the training data
    :rtype: list
    """
    annotation=[]
    with open(file, 'r') as fichier:
        text=fichier.read()
        words=word_tokenize(text, 'english')
    position=0
    for z in range(len(words)):
        position += len(words[z]) + 1
        for entity in d_entities:
            if len(words)-z-1<len(entity)-1: continue
            if words[z] != entity[0]: continue
            detect=True
            for i in range(1,len(entity)):
                if words[z+i] != entity[i]:
                    detect=False
                    break
            if detect:
                deb = position - len(words[z])
                if len(entity) != 1:
                    for w in range(1, len(entity)):
                        position += len(entity[w])
                annotation.append([d_entities[entity], ' '.join(entity), str(deb) +'-'+str(position)])
                z=z+len(entity)
    return annotation

   
#dirname='/media/DATA/Master/Analyse_donnees_text/data_suj1/train/'
#dico_entities_cat=extract_entities_cat(dirname)
# print(dico_entities_cat)
#file='/media/DATA/Master/Analyse_donnees_text/data_suj1/dev/BTID-10095.txt'
#annot= extract_from_training(file, dico_entities_cat)
#print(annot)