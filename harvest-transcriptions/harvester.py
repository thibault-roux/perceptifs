from jiwer import wer


import argparse
parser = argparse.ArgumentParser(description="Allows to extract interesting sentence")
parser.add_argument("sys1", type=str, help="Name of the first system.")
parser.add_argument("sys2", type=str, help="Name of the second system.")
parser.add_argument("metric", type=str, help="Name of the second system.")
parser.add_argument("difference", type=str, help="Name of the second system.")
args = parser.parse_args()


def removeEPS(sentence):
    new_sentence_list = []
    sentence_list = sentence.split(" ")
    for word in sentence_list:
        if word != '<eps>':
            new_sentence_list.append(word)
    return ' '.join(new_sentence_list)




def get_score(metric, id): # return a dictionary -> dico[id] = [score, ref, hyp]
    dico = dict()
    with open("results/correlation/" + metric + "_" + id + ".txt", "r", encoding="utf8") as file: # ID to score
        for ligne in file:
            ligne = ligne[:-1].split("\t")
            dico[int(ligne[0])] = [float(ligne[1]), "<EMPTY>", "<EMPTY>"]
    with open("data/" + id + "/" + id + "1.txt", "r", encoding="utf8") as file: # ID to ref and hyp in the same dico
        for ligne in file:
            ligne = ligne[:-1].split("\t")
            dico[int(ligne[0])] = [dico[int(ligne[0])][0], removeEPS(ligne[1]), removeEPS(ligne[2])]
    return dico # dico[id] = [score, ref, hyp]
# NB: Scores in correlation correspond to real score computed from data. (One exception catch on 5437 for WER)


sys1 = get_score(args.metric, args.sys1)
sys2 = get_score(args.metric, args.sys2)

def check_data(sys1, sys2):
    incoherence = 0
    coherence = 0
    wers = []
    for k, v in sys1.items():
        """if v[0] != 100*wer([v[1]], v[2]): # le WER entre la référence et l'hypothèse correspond à celui enregistré
            print(k, 100*wer([v[1]], v[2]), v)"""
        if sys2[k][1] != v[1]: # si les ref sont identiques pour les deux dictionnaires
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

check_data(sys1, sys2)