#!/usr/bin/python
#coding: utf-8


import re, nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#nltk.download()



stop_words = stopwords.words("english")

list_stop_words = ["et","also","far","thus","sea","whereas","any","other"]

list_tag7 = [['NNP', 'NN', 'NN', '.', 'NN', 'NNP', 'CD']]
list_tag6 = [['NNP', 'NNP', 'NN', 'NN', '.', 'NNP']]
list_tag5 = [['NNP', 'NN', 'NNP', 'NN', 'NNP']]
list_tag4 = [['NN', 'NN', 'NNP', 'PRP'], ['NNP', 'NN', 'NNP', 'CD'], ['NNP', 'NN', '.', 'NNP'], ['NNP', 'NN', '.', 'CC'], ['NNP', 'NNS', 'VBP', 'CD'], ['NNP', 'NNP', 'VBZ', 'CD'],['NNP', 'VBZ', 'NNP', 'CD']]
list_tag3 = [['NNP', 'VBZ', 'NNP'], ['NNP', 'NN', 'CD'], ['NNP', 'NN', 'NNP'], ['NNP', 'VBD', 'CD'], ['NNP', 'NNS', 'NNP']]
list_tag2 = [['NNP', 'NN'],['NNP', 'NNP'], ['NNP', 'NNS'], ['NNS', 'NNS'], ['NN', 'NN'], ['NNS', 'VBP']]
list_tag1 = [['NNP'], ['NNS'], ['NN']]

list_tagg_v2 = ['NNP', 'NNS', 'NN']


def cat_name(file):
			with open(file, 'r') as f_in :
				list_name=[]
				list_name_inText=[]
				position=0
				for n,line in enumerate(f_in) :
					list_taggs= []
					list_tag= []
					

					"""---- Generation des tagg ---- """

					tokens = word_tokenize(line)
					tokens = [i for i in tokens if i not in stop_words]
					taggs = nltk.pos_tag(tokens)
					

					"""---- Traitement de la première ligne de chaque texte ----"""
					
					if n==0 : 
						name=''
						for tagg1 in taggs :
							list_taggs.append(tagg1[1])
						if check_tagg(list_taggs) : 			#Verifie que la première ligne est une liste de taggs correspondant à un nom de bactérie
							for tag in taggs :
								list_tag.append(tag[0])
							name=' '.join(list_tag)
						if name!='':											#Trouve la position du nom dans le texte
							start=position+line.find(name)
							if start==-1 : start=0							#Problème avec les espaces entre les mots (pas de reconnaissance)
							end=start+len(name)
							list00=str(start)+'-'+str(end)+' '+name 			#Resultat sous la forme debut-fin nom
							
							list_name.append(list00)
							


					"""---- Recherche les noms de bactérie dans le reste du texte qui est plus complexe ----"""

					if n!=0:
					
						"""---- On récupère l'ensemble des termes qui ressemble aux noms des bactérie de la première ligne ----"""

						if name : 
							namePart=name.split(" ")
							partName=namePart[0]+' '+namePart[1]
							regexPattern=re.compile(r'((%s)( %s)?( strain)?( [A-Z0-9\-]+)?)' %(namePart[0], namePart[1]))
							partNameInText=re.findall(regexPattern, line)
							for elem in partNameInText : 
								if elem[0] in list_name_inText :										#Partie du programme pour récupérer la posistion quand le même mot est présent plusieurs fois donc nécessite de vérifier que le nom a déjà été trouvé une première fois
									new_start0=end0-position											#la recherche de la position prend un nouveau départ : start=position+line.find() donne la position sur l'ensemble du texte. on ne veut récupérer la position que sur la ligne courante.
									start0=position+line.find(elem[0], new_start0)						#Recherche la position du mot avec le nouveau départ et donne la position du mot dans le texte
									end0=start0+len(elem[0])
									list0=str(start0)+'-'+str(end0)+' '+elem[0]
									oldstart=start0
								else :
									start0=position+line.find(elem[0])
									end0=start0+len(elem[0])
									list0=str(start0)+'-'+str(end0)+' '+elem[0] 						#Resultat sous la forme debut-fin nom
									list_name_inText.append(elem[0])
								list_name.append(list0)

						else: partName=''

						"""---- On récupère l'ensemble des termes qui ressemble à des noms de bactérie (fini par um/us/i/ii/a/as) ----"""
				
						if re.match(r'(.+)?([A-Z][a-z]+(um|us|i|ii|a|as) (sp . )?([a-z]+)?) (.+)', line) :
							nom=re.findall(r'([A-Z][a-z]+(um|us|i|ii|a|as) (sp . )?([a-z]+)?)', line)
							liste1=[]
							for j in range(len(nom)) :
								if nom[j][0] not in list_name :
									next_word=nom[j][0].split(" ")[1]
									if next_word not in stop_words and next_word not in list_stop_words :
											if nom[j][0]!=partName :
												if nom[j][0] in liste1:											#Partie du programme pour récupérer la posistion quand le même mot est présent plusieurs fois donc nécessite de vérifier que le nom a déjà été trouvé une première fois
													new_start1=end1-position									#la recherche de la position prend un nouveau départ : start=position+line.find() donne la position sur l'ensemble du texte. on ne veut récupérer la position que sur la ligne courante.
													start1=position+line.find(nom[j][0], new_start1)			#Recherche la position du mot avec le nouveau départ et donne la position du mot dans le texte
													end1=start1+len(nom[j][0])
													list2=str(start1)+'-'+str(end1)+' '+nom[j][0]

												else:
													start1=position+line.find(nom[j][0])
													end1=start1+len(nom[j][0])
													list2=str(start1)+'-'+str(end1)+' '+nom[j][0]
													liste1.append(nom[j][0])
												list_name.append(list2)



						"""---- On récupère les noms ou phrases avec bacteria ou bacterial----"""
						debut=re.match(r'(.+)bacteria', line )
						if debut :
							bacteria=re.findall(r'((([A-Za-z]+ ){2})([A-Za-z]+)?bacteria?)', line)	#Recherche les différentes formes ou le nom fini par bactérie (cyanobacterie ou green sulfur bacterie)
							liste2=[]
							liste3=[]
							liste4=[]
							for m in range(len(bacteria)):
								
								"""--- Si le nom est de la forme cyanobactérie ---"""
								if bacteria[m][3]!='':													
									name1 = bacteria[m][3]+'bacteria'
									if name1 in liste2:
										new_start2=end2-position
										start2=position+line.find(name1, new_start2)
										end2=start2+len(name1)
										list3=str(start2)+'-'+str(end2)+' '+name1

									else:
										start2=position+line.find(name1)
										end2=start2+len(name1)
										list3=str(start2)+'-'+str(end2)+' '+name1
										liste2.append(name1)
									
									list_name.append(list3)

									"""--- Si le nom est de la forme green sulfur bactérie ---"""
								elif bacteria[m][2][:-1] not in stop_words and bacteria[m][2][:-1] not in list_stop_words: #On élimine les formes complexes qui ne correspondent pas à un nom de bactérie car contient des stop_word
									tagg_bacteria = nltk.pos_tag(word_tokenize(bacteria[m][0]))							   #On vérifie que les mots précédant bactéria correspondent à des patterns particuliers
									
									if tagg_bacteria[1][1] in ['JJ', 'NN', 'NNP']:					
										if tagg_bacteria[0][1] in ['JJ', 'NN']:												#Si les deux mots précédants bacteria ont des patterns corrects (ex : green sulfur bacteria)

											if bacteria[m][0] in liste3:													#Partie du programme pour récupérer la posistion quand le même mot est présent plusieurs fois
												new_start3=end3-position
												start3=position+line.find(bacteria[m][0], new_start3)
												end3=start3+len(bacteria[m][0])
												list4=str(start3)+'-'+str(end3)+' '+bacteria[m][0]

											else:
												start3=position+line.find(bacteria[m][0])
												end3=start3+len(bacteria[m][0])
												list4=str(start3)+'-'+str(end3)+' '+bacteria[m][0]
												liste3.append(bacteria[m][0])
											
											list_name.append(list4)

										else : 
											name2=tagg_bacteria[1][0]+' bacteria'											#Si seulement le mot précédant bactéria a un pattern correct (ex : phytotrophic bacteria)

											if name2 in liste4:																#Partie du programme pour récupérer la posistion quand le même mot est présent plusieurs fois
												new_start4=end4-position
												start4=position+line.find(name2, new_start4)
												end4=start4+len(name2)
												list5=str(start4)+'-'+str(end4)+' '+name2

											else:
												start4=position+line.find(name2)
												end4=start4+len(name2)
												list5=str(start4)+'-'+str(end4)+' '+name2
												liste4.append(name2)
											
											list_name.append(list5)
								

							
						

						"""---- On récupère l'ensemble des abréviations qui correspondent à des bactéries----"""
						if re.match(r'(.+)([A-Z]\. [a-z]+)(.+)', line) :
							abb=re.findall(r'[A-Z]\. [a-z]+', line )
							liste5=[]
							for k in range(len(abb)):
								if abb[k] not in list_name :
									next_abb=abb[k].split(" ")[1]
									if next_abb not in stop_words and next_abb not in list_stop_words :
										if abb[k] in liste5:																#Partie du programme pour récupérer la posistion quand le même mot est présent plusieurs fois
											new_start5=end5-position	
											start5=position+line.find(abb[k], new_start5)
											end5=start5+len(abb[k])
											list6=str(start5)+'-'+str(end5)+' '+abb[k]
											list_name.append(list6)

										else :
											start5=position+line.find(abb[k])
											end5=start5+len(abb[k])
											list6=str(start5)+'-'+str(end5)+' '+abb[k]
											liste5.append(abb[k])

										list_name.append(list6)

									
					position+=len(line)
				return list_name	
	


def check_tagg(list):
	if len(list)==1 : 
		if list in list_tag1 : return True
	if len(list)==2 :
		if list in list_tag2 : return True
	if len(list)==3 : 
		if list in list_tag3 : return True
	if len(list)==4 : 
		if list in list_tag4 : return True
	if len(list)==5 : 
		if list in list_tag5 : return True
	if len(list)==6 : 
		if list in list_tag6 : return True
	if len(list)==7 : 
		if list in list_tag7 : return True