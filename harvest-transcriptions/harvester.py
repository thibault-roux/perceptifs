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






# =========== TO DELETE =============
def check_data(sys1, sys2):
    incoherence = 0
    coherence = 0
    wers = []
    for k, v in sys1.items():
        # if v[0] != 100*wer([v[1]], v[2]): # le WER entre la référence et l'hypothèse correspond à celui enregistré
        #     print(k, 100*wer([v[1]], v[2]), v)
        if sys2[k]["ref"] != v["ref"]: # si les ref sont différentes pour les deux dictionnaires
            print(k)
            print(sys2[k]["ref"])
            print(v["ref"])
            print()
            incoherence += 1
            wers.append(100*wer([v["ref"]], [sys2[k]["ref"]]))
        else:
            coherence += 1
    print("Il y a " + str(incoherence) + " incohérence(s) entre les deux fichiers")
    print("Il y a " + str(coherence) + " cohérence(s) entre les deux fichiers")
    print("WER  moyen: ", sum(wers)/len(wers))
    input("Affichage des wers...\n")
    print(wers)

# sys1 = get_score(args.sys1)
# sys2 = get_score(args.sys2)
# check_data(sys1, sys2)







def abs(value): # valeur absolue
    if value < 0:
        return -value
    else:
        return value

def display(sysid, metrics):
    txt = "ref : " + sysid["ref"] + "\n"
    txt += "hyp : " + sysid["hyp"] + "\n"

    for metric in metrics:
        txt += metric + " : " + str(float(int(1000*sysid[metric])/1000)) + " ; "
    txt = txt[:-3] + "\n_"
    return txt


def retrieve_transcriptions(namesys1, namesys2, diff=[], limit=[], inversed=(), min_length=-1, max_length=9999):
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

    faccepted = open("transcriptions/temp.txt", "a")

    for id, _ in sys1.items():
        if "(h)" in sys1[id]["ref"].split(" "): # remove reference containing disfluences
            continue
        if sys1[id]["ref"] == sys2[id]["ref"]: # if references are identical
            if sys1[id]["hyp"] != sys2[id]["hyp"]: # if hypothesis are different

                length = len(sys1[id]["ref"].split(" "))
                if length >= min_length and length <= max_length: # check the length of the reference
                    break_value = False
                    for d in diff: # check difference between two metrics
                        metric = d[0]
                        minsco = d[1] # minimum difference between the score of sys1 and sys2 
                        maxsco = d[2] # maximum difference between the score of sys1 and sys2
                        if metric not in sys1[id] or metric not in sys2[id]:
                            break_value = True
                            break
                        difference = abs(sys1[id][metric] - sys2[id][metric])
                        if difference < minsco or difference > maxsco:
                            break_value = True
                            break

                    for l in limit: # check the minimum and maximum value for each metric
                        metric = l[0]
                        minsco = l[1]
                        maxsco = l[2]
                        if metric not in sys1[id] or metric not in sys2[id]:
                            break_value = True
                            break
                        for sys in [sys1, sys2]:
                            score = sys[id][metric]
                            if score < minsco or score > maxsco:
                                break_value = True
                                break

                    if len(inversed) == 2:
                        good_value = False
                        if (( sys1[id][inversed[0]] > sys2[id][inversed[0]]
                            and sys1[id][inversed[1]] < sys2[id][inversed[1]] )
                            or ( sys1[id][inversed[0]] < sys2[id][inversed[0]]
                            and sys1[id][inversed[1]] > sys2[id][inversed[1]] )):
                            good_value = True
                    else:
                        good_value = True

                    if not break_value and good_value:
                        #if sys1[id]["wer"] == sys2[id]["wer"]: # le score est le même  # if abs(sys2[k][0] - v[0]) < difference
                        print(display(sys1[id], ["wer", "semdist"])) # ["wer", "cer", "ember", "semdist"]))
                        print(display(sys2[id], ["wer", "semdist"])) # ["wer", "cer", "ember", "semdist"]))
                        answer = input("\nSave? (y/n/quit) : ")
                        if answer == "y":
                            txt =  display(sys1[id], ["wer", "cer", "ember", "semdist"]) + "\n"
                            txt += display(sys2[id], ["wer", "cer", "ember", "semdist"]) + "\n=================\n"
                            faccepted.write(txt)
                        elif answer == "quit":
                            return 0
                        print("=================")
                        

# WER different (one low and the other high)
print("\n\n-----\nWER very different:")
retrieve_transcriptions(args.sys1, args.sys2, diff=[["wer",30,200]], min_length=3, max_length=20)

# WER close
print("\n\n-----\nWER pretty close:")
retrieve_transcriptions(args.sys1, args.sys2, diff=[["wer",1,15]], min_length=3, max_length=20)

# WER identical
print("\n\n-----\nWER identical:")
retrieve_transcriptions(args.sys1, args.sys2, diff=[["wer",0,0]], min_length=3, max_length=20) # maybe I should limit the maximum wer to be below 100%

# CER identical
print("\n\n-----\nCER identical:")
retrieve_transcriptions(args.sys1, args.sys2, diff=[["cer",0,0]], min_length=3, max_length=20) # maybe I should limit the maximum cer to be below 100%

# WER identical but different semantical value
print("\n\n-----\nWER identical but different semdist:")
retrieve_transcriptions(args.sys1, args.sys2, diff=[["wer",0,0], ["semdist",2,999]], min_length=3, max_length=20)

# WER indicate that one hypothesis is better but Semdist indicate the other as the best
print("\n\n-----\nWER and Semdist are contradictory:")
retrieve_transcriptions(args.sys1, args.sys2, limit=[["wer",5,90]], inversed=("wer", "semdist"), min_length=3, max_length=20)


#retrieve_transcriptions(args.sys1, args.sys2, diff=[["wer",0,10], ["semdist",30,200]], limit=[["wer",-10,70]], min_length=3, max_length=10)
#retrieve_transcriptions(args.sys1, args.sys2, diff=[["wer",0,200], ["semdist",10,80]], limit=[["wer",5,90]], inversed=("wer", "semdist"), min_length=3, max_length=20)
# inversed=["wer", "semdist"]   ==   [ wer(hyp1)>wer(hyp2) and semdist(hyp1)<semdist(hyp2) ] or [ wer(hyp1)<wer(hyp2) and semdist(hyp1)>semdist(hyp2)