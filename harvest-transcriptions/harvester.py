from jiwer import wer
import os


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
            
    for metric in ["wer", "cer", "ember", "semdist", "bertscore"]:
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
        try:
            txt += metric + " : " + str(float(int(1000*sysid[metric])/1000)) + " ; "
        except KeyError:
            txt += metric + " : _ ; "
            print("KeyError:")
            print(txt)
    txt = txt[:-3] + "\n_"
    return txt


def retrieve_transcriptions(filename, namesys1, namesys2, diff=[], limit=[], inversed=(), min_length=-1, max_length=9999):
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

    
    faccepted = open("transcriptions/mess/" + namesys1 + "-" + namesys2 + "/" + filename, "w")

    sys1 = get_score(namesys1)
    sys2 = get_score(namesys2)

    for id, _ in sys1.items():
        ref = sys1[id]["ref"]
        if "(" in ref or ")" in ref: # remove reference containing disfluences
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
                        # txt =  display(sys1[id], ["wer", "cer", "ember", "semdist"]) + "\n"
                        # txt += display(sys2[id], ["wer", "cer", "ember", "semdist"]) + "\n=================\n"
                        txt = id + "\t" + sys1[id]["ref"] + "\t" + sys1[id]["hyp"] + "\t" + sys2[id]["hyp"] + "\n"
                        faccepted.write(txt)
                        




def harvester_system(sys1, sys2):
    metrics = ["wer", "cer", "ember", "semdist", "bertscore"]
    for m in metrics: # green part
        # very different value for the specific metric between two hypothesis
        retrieve_transcriptions(m[0] + "HD", sys1, sys2, diff=[[m,30,90]], min_length=3, max_length=20)
        # not very different for the specific metric between two hypothesis
        retrieve_transcriptions(m[0] + "LD", sys1, sys2, diff=[[m,0.1,15]], min_length=3, max_length=20)
        # when the metric said that the two hypothesis are equal
        retrieve_transcriptions(m[0] + "=", sys1, sys2, diff=[[m,0,0]], min_length=3, max_length=20)

    for m1 in ["wer", "cer"]:
        for m2 in metrics:
            if m1 != m2:
                # m1 identical but different m2 value
                retrieve_transcriptions(m1[0] + "=;" + m2[0] + "D", sys1, sys2, diff=[[m1,0,0], [m2,1,999]], min_length=3, max_length=20)

    for i in range(len(metrics)):
        for j in range(i+1, len(metrics)):
            m1 = metrics[i]
            m2 = metrics[j]
            # WER indicate that one hypothesis is better but Semdist indicate the other as the best
            retrieve_transcriptions(m1 + "INV" + m2, sys1, sys2, limit=[["wer",5,90]], inversed=("wer", "semdist"), min_length=3, max_length=20)


def harvester(sys1, sys2):
    sorted_sys = [sys1, sys2]
    sorted_sys.sort() # useful to avoir having two files named "sys1-sys2.txt" and "sys2-sys1" as they are the same thing.
    path = "transcriptions/mess/" + sorted_sys[0] + "-" + sorted_sys[1]
    if not os.path.exists(path):
        os.makedirs(path)
    harvester_system(sorted_sys[0], sorted_sys[1])

if __name__ == '__main__':
    harvester(args.sys1, args.sys2)









#retrieve_transcriptions("", args.sys1, args.sys2, diff=[["wer",0,10], ["semdist",30,200]], limit=[["wer",-10,70]], min_length=3, max_length=10)
#retrieve_transcriptions("", args.sys1, args.sys2, diff=[["wer",0,200], ["semdist",10,80]], limit=[["wer",5,90]], inversed=("wer", "semdist"), min_length=3, max_length=20)
# inversed=["wer", "semdist"]   ==   [ wer(hyp1)>wer(hyp2) and semdist(hyp1)<semdist(hyp2) ] or [ wer(hyp1)<wer(hyp2) and semdist(hyp1)>semdist(hyp2)

"""# WER different (one low and the other high)
print("\n\n-----\nWER very different:")
retrieve_transcriptions("wer30-90", args.sys1, args.sys2, diff=[["wer",30,90]], min_length=3, max_length=20)

# WER close
print("\n\n-----\nWER pretty close:")
retrieve_transcriptions("wer1-15", args.sys1, args.sys2, diff=[["wer",1,15]], min_length=3, max_length=20)

# WER identical
print("\n\n-----\nWER identical:")
retrieve_transcriptions("wer0", args.sys1, args.sys2, diff=[["wer",0,0]], min_length=3, max_length=20) # maybe I should limit the maximum wer to be below 100%

# CER identical
print("\n\n-----\nCER identical:")
retrieve_transcriptions("cer0", args.sys1, args.sys2, diff=[["cer",0,0]], min_length=3, max_length=20) # maybe I should limit the maximum cer to be below 100%

# WER identical but different semantical value
print("\n\n-----\nWER identical but different semdist:")
retrieve_transcriptions("wer0semdist2-999", args.sys1, args.sys2, diff=[["wer",0,0], ["semdist",2,999]], min_length=3, max_length=20)

# WER indicate that one hypothesis is better but Semdist indicate the other as the best
print("\n\n-----\nWER and Semdist are contradictory:")
retrieve_transcriptions("opp_wer-semdist", args.sys1, args.sys2, limit=[["wer",5,90]], inversed=("wer", "semdist"), min_length=3, max_length=20)
"""