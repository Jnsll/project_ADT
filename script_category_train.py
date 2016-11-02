import re, glob
dirname=''
d_entities={}
p=re.compile (r'.+\t(.+)\t\d+-\d+\s(.+)')

files=glob.glob(dirname+'*.ent')
for file in files:
    with open(file, 'r') as fichier:
        for line in fichier:
            m=p.match(line)
            if m:
                cat = m.group(1)
                nom = m.group(2)
            if nom not in d_entities:
                d_entities[nom]=cat
print(d_entities)
