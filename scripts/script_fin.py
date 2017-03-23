from script_name_fin import cat_name
from script_train_fin import extract_entities_cat, extract_from_training
from script_others_fin import extract_other_entities, extract_countries
import sys, glob, os, re


def main(dirname):
    print("\tLancement de l'analyse")

    d_entities = extract_entities_cat(dirname + '/train/')

    files = glob.glob(dirname + '/dev/*.txt')
    print("\tOuverture des fichiers ")

    for file in files:
        path = os.path.dirname(file)
        ent_file = re.sub(r'.txt', r'.ent2', os.path.basename(file))
        end_file = path + '/' + ent_file
        #print(end_file)
        annot = extract_from_training(file, d_entities)
        annot_other=extract_other_entities(file)
        annot_countries=extract_countries(file, dirname + '/country_names')
        with open(end_file, 'w') as f_out:
            list_name = cat_name(file)
            for elem in list_name:
                fin_name = 'ID\tBacteria\t' + elem + '\n'
                f_out.write(fin_name)
            for entity in annot:
                fin_ent = 'ID\t' + entity[0] + '\t' + entity[2]+ ' '+ entity[1] + '\n'
                f_out.write(fin_ent)
            for ent in annot_other:
                fin_other= 'ID\t' + annot_other[ent] + '\t' + ent + '\n'
                f_out.write(fin_other)
            for pays in annot_countries:
                fin_pays= 'ID\tGeographical' + '\t' + pays[1]+ ' '+ pays[0] + '\n'
                f_out.write(fin_pays)


    print("\tFin de l'analyse et fermeture des fichiers ")  # print (list_name)



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Precisez le dossier contenant vos fichiers")
    else:
        dirname = sys.argv[1]
        main(dirname)
