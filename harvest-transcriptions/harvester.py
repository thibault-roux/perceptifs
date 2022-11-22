from jiwer import wer


import argparse
parser = argparse.ArgumentParser(description="Allows to extract interesting sentence")
parser.add_argument("sys1", type=str, help="Name of the first system.")
parser.add_argument("sys2", type=str, help="Name of the second system.")
# parser.add_argument("metric", type=str, help="Name of the second system.")
# parser.add_argument("difference", type=str, help="Name of the second system.")
args = parser.parse_args()


def removeEPS(sentence):
    new_sentence_list = []
    sentence_list = sentence.split(" ")
    for word in sentence_list:
        if word != '<eps>':
            new_sentence_list.append(word)
    return ' '.join(new_sentence_list)


def get_score(sys): # return a dictionary -> dico[id] = [ref, hyp, wer, cer, ember, semdist]
    dico = dict()
    with open("data/" + sys + "/" + sys + "1.txt", "r", encoding="utf8") as file: # Retrieve id, references, hypothesis
        for ligne in file:
            ligne = ligne[:-1].split("\t")
            id = ligne[0]
            ref = removeEPS(ligne[1])
            hyp = removeEPS(ligne[2])
            dico[id] = dict()
            dico[id]["ref"] = ref # store reference
            dico[id]["hyp"] = hyp # store hypothesis
            
    for metric in ["wer", "cer", "ember", "semdist"]:
        with open("results/correlation/" + metric + "_" + sys + ".txt", "r", encoding="utf8") as file: # Retrieve score for each metric
            for ligne in file:
                ligne = ligne[:-1].split("\t")
                id = ligne[0]
                score = float(ligne[1])
                dico[id][metric] = score

    return dico # dico[id] = [ref, hyp, wer, cer, ember, semdist] # dict of dict
# NB: Scores in correlation correspond to real score computed from data. (One exception catch on 5437 for WER)



def abs(value): # valeur absolue
    if value < 0:
        return -value
    else:
        return value


def retrieve_transcriptions(namesys1, namesys2, diff, limit, min_length=-1, max_length=9999):
    # ====================================
    # conditions optionnelles : 
    # - [one/many] difference relative à une métrique : élevé, faible, nul (identique), peut-être une valeur numérique (exemple: diff(WER) < 10, diff(SemDist) > 20)
    #               -> trois paramètres : métrique, différence < ou >, valeur de différence (pour l'égalité, faire < 0)
    # - longueur de la référence
    # - [one/many] valeur minimum/maximum pour une métrique : Par exemple, le wer doit être au moins à 30% mais inférieur à 70%
    # ====================================
    # conditions systématiques à vérifier:
    # - références identiques
    # - hypothèses différentes

    sys1 = get_score(namesys1)
    sys2 = get_score(namesys2)

    for id, _ in sys1.items():
        if sys1[id]["ref"] == sys2[id]["ref"]: # si les ref sont identiques pour les deux dictionnaires
            if sys1[id]["hyp"] != sys2[id]["hyp"]: # si les hypothèses sont différentes

                length = len(sys1[id]["ref"].split(" "))
                if length >= min_length and length <= max_length: # check the length of the reference
                    # CONTINUER FROM HERE
                    break_value = False
                    for d in diff: # check difference between two metrics
                        d = d.split(",")
                        metric = d[0]
                        bin_op = d[1]
                        dscore = float(d[2]) # difference between the score of sys1 and sys2
                        if bin_op == "<":
                            if abs(sys1[id][metric] - sys2[id][metric]) > dscore: # if the difference is NOT inferior to dscore
                                break_value = True
                                break
                        elif bin_op == ">":
                            if abs(sys1[id][metric] - sys2[id][metric]) < dscore: # if the difference is NOT superior to dscore
                                break_value = True
                                break
                        else:
                            print("Error with bin_op =", bin_op)
                            exit(-1)

                    #for l in limit: # check the minimum and maximum value for each metric

                    if not break_value:
                        #if sys1[id]["wer"] == sys2[id]["wer"]: # le score est le même  # if abs(sys2[k][0] - v[0]) < difference
                        print(sys1[id])
                        print(sys2[id])
                        print("diff:", abs(sys1[id][metric] - sys2[id][metric]))
                        input()
                        


retrieve_transcriptions(args.sys1, args.sys2, diff=["wer,<,10", ], limit=["wer,0,50"], min_length=1, max_length=5) #, diff=["wer,<,30", "semdist,<,0", "cer,>,10"]









# =========== TO DELETE =============

def check_data(sys1, sys2):
    incoherence = 0
    coherence = 0
    wers = []
    for k, v in sys1.items():
        """if v[0] != 100*wer([v[1]], v[2]): # le WER entre la référence et l'hypothèse correspond à celui enregistré
            print(k, 100*wer([v[1]], v[2]), v)"""
        if sys2[k][1] != v[1]: # si les ref sont différentes pour les deux dictionnaires
            print(k)
            print(sys2[k][1])
            print(v[1])
            print()
            incoherence += 1
            wers.append(100*wer([v[1]], [sys2[k][1]]))
        else:
            coherence += 1
    print("Il y a " + str(incoherence) + " incohérence(s) entre les deux fichiers")
    print("Il y a " + str(coherence) + " cohérence(s) entre les deux fichiers")
    print("WER  moyen: ", sum(wers)/len(wers))
    input("Affichage des wers...\n")
    print(wers)

# Step 1 : vérifier que les transcriptions sont alignées (transcription 1 de KD_woR == transcription 1 de KD_wR)
#   -> 821 incohérences pour 4617 cohérences. Supprimons les incohérences ?
# Step 2 : calculer le WER des transcriptions (DONE, c'est ok)

#check_data(sys1, sys2)
