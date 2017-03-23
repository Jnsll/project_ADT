#!/usr/bin/python3.5
# coding: utf-8

import glob, nltk
from nltk.tokenize import word_tokenize




def extract_other_entities(file):
    """
        Extracts the entities and corresponding categories from the dev data files (.txt) thanks to the training data.
    :param file: path to the file to process
    :type file: str
    :param d_entities: all entities and categories extracted from the training data
    :type d_entities: dict
    :return: entities and categories of the file which are found in the training data
    :rtype: list
    """
    # Lists of targeted entities
    environb = ['environment', 'environments', 'medium', 'location', 'sample', 'nature', 'extract']
    environa = ['tropical', 'subtropical', 'permafrost']
    noenv = ['different', 'harsh', 'mild', 'normal', 'ordinary', 'safe', 'target', 'unique', 'various']
    water = ['lake', 'lakes', 'waters', 'water', 'spring', 'marine', 'aquatic', 'sea', 'ocean', 'rain', 'meromictic',
             'river', 'aquarium', 'wastewater']
    host = ['murine', 'bovine', 'tick', 'microbe', 'microorganism', 'non-human', 'pest']
    hostpart = ['cell', 'cell-wall', 'filaments', 'flagellum', 'macrophage', 'organelle', 'peptoglycan layer',
                'rhizosphere', 'spore', 'tissue', 'abcesses', 'excretions', 'fluids', 'lesions', 'phyllome', 'rhizome',
                'secretions', 'tumors', 'wounds', 'intestinal', 'blood', 'intracellular', 'root', 'heart', 'endophyte',
                'endosymbiont', 'epiphytic']
    geo = ['hospital', 'Institute']
    food = ['food', 'meat', 'vegetables']
    soil = ['soil', 'soils']
    medical = ['catheter', 'nosocomial', 'therapeutic', 'pharmaceutic', 'vaccine', 'gloves', 'scissors', 'scalpel']

    with open(file, 'r') as fichier:
        text = fichier.read()
        words = word_tokenize(text, 'english')
    tagged = nltk.pos_tag(words)
    compteur = 0
    annot = {}
    for mot in tagged:
        if mot[0] == 'in':  # Entities detected by introduction with 'in'
            if tagged[compteur + 1][1] == 'NN' and tagged[compteur + 2][1] == 'NN':
                annot[tagged[compteur + 1][0] + ' ' + tagged[compteur + 2][0]] = 'Environment'
            if tagged[compteur + 1][1] == 'DT' and tagged[compteur + 2][1] == 'NN' and tagged[compteur + 3][1] == 'NN':
                annot[tagged[compteur + 2][0] + ' ' + tagged[compteur + 3][0]] = 'Environment'
            if tagged[compteur + 1][1] == 'DT' and tagged[compteur + 2][1] == 'JJ' and tagged[compteur + 3][1] == 'NN':
                annot[tagged[compteur + 2][0] + ' ' + tagged[compteur + 3][0]] = 'Environment'
            if tagged[compteur + 1][1] == 'NNP' and tagged[compteur + 2][1] != 'NN':  # Geographical
                annot[tagged[compteur + 1][0]] = 'Geographical'
        if mot[0] == 'within':  # Entities detected by introduction with 'within'
            if tagged[compteur + 1][1] == 'DT' and tagged[compteur + 2][1] == 'NN' and tagged[compteur + 3][
                1] == 'NN' and tagged[compteur + 4][1] == 'NN':
                annot[tagged[compteur + 2][0] + ' ' + tagged[compteur + 3][0] + ' ' + tagged[compteur + 4][
                    0]] = 'HostPart'
        # Entities detected with using a 'database' of target words
        if mot[0] in environb:
            if tagged[compteur - 1][1] == 'JJ' and tagged[compteur - 1][0] not in noenv:
                annot[tagged[compteur - 1][0] + ' ' + mot[0]] = 'Environment'
        if mot[0] in environa:
            if tagged[compteur + 1][1] == 'NN':
                annot[mot[0] + ' ' + tagged[compteur + 1][0]] = 'Environment'
        if mot[0] in water:
            annot[tagged[compteur][0]] = 'Water'
        if mot[0] in medical:
            annot[tagged[compteur][0]] = 'Medical'
        if mot[0] in soil:
            annot[tagged[compteur][0]] = 'Soil'
        if mot[0] in food:
            annot[tagged[compteur][0]] = 'Food'
        if mot[0] in host:
            annot[tagged[compteur][0]] = 'Host'
        if mot[0] in hostpart:
            annot[tagged[compteur][0]] = 'HostPart'
        if mot[0] in geo:
            annot[tagged[compteur][0]] = 'Geographical'

        compteur += 1  # Following word in text

    return annot


def extract_countries(file, countries_file):
    countries = {}
    with open(countries_file, 'r') as c_file:
        for line in c_file:
            country = line.rstrip('\n')
            taille = len(country.split())
            if taille in countries:
                countries[taille].append(tuple(country.split()))
            else:
                countries[taille] = [tuple(country.split())]

    localisations = []
    with open(file, 'r') as fichier:
        text = fichier.read()
        words = word_tokenize(text, 'english')
    position = 0
    for z in range(len(words)):
        position += len(words[z]) + 1
        for taille in countries:
            if len(words) - z - 1 < taille - 1: break
            for pays in countries[taille]:
                if words[z] != pays[0]: continue
                detect = True
                for i in range(1, len(pays)):
                    if words[z + i] != pays[i]:
                        detect = False
                        break
                if detect:
                    deb = position - len(words[z])
                    if len(pays) != 1:
                        for w in range(1, taille):
                            position += len(pays[w])
                    localisations.append([' '.join(pays), str(deb) + '-' + str(position)])
                    z = z + taille
    return localisations
