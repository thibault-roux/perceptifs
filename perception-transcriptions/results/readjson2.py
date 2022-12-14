import os
import pickle
from jiwer import wer
import json

metrics = ["bertscore", "cer", "ember", "semdist", "wer"]
systems = ["KD_woR", "KD_wR", "SB_bpe1000", "SB_bpe750", "SB_s2s", "SB_w2v_1k", "SB_w2v_3k", "SB_w2v_7k", "SB_w2v", "SB_xlsr_fr", "SB_xlsr"]




def removeEPS(ligne):
    retour = ""
    ligne = ligne.split(" ")
    for i in range(len(ligne)):
        if ligne[i] != "<eps>":
            retour += ligne[i] + " "
    return retour[:-1]


total = 0

def add(SCORES, ref, hyp, metric, system, score): # add a score value in the giga SCORES
    global total
    if ref not in SCORES:
        SCORES[ref] = dict()
    if hyp not in SCORES[ref]:
        SCORES[ref][hyp] = dict()
    if metric not in SCORES[ref][hyp]:
        SCORES[ref][hyp][metric] = {"system": [system], "score": score}
    else:
        SCORES[ref][hyp][metric]["system"].append(system)
        if abs(SCORES[ref][hyp][metric]["score"] - score) > 0.0002:
            total += 1
            SCORES[ref][hyp][metric]["score"] = wer(ref, hyp)*100
            """print(metric, system)
            print("difference:", abs(SCORES[ref][hyp][metric]["score"] - score))
            print("ref: '" + ref + "'")
            print("hyp: '" + hyp + "'")
            print(SCORES[ref][hyp][metric])
            print("1:", score)
            print("2:", SCORES[ref][hyp][metric]["score"])
            input()
            print("wer:", wer(ref, hyp)*100)
            choice = input("Type the real score. (1/2) : ")
            if choice == "1":
                SCORES[ref][hyp][metric]["score"] = score"""


def init_SCORES(keep):
    SCORES = dict()

    # keep = input("Do you want to keep the previous SCORES? (y/n) : ")
    if keep == "y":
        with open('SCORES.pickle', 'rb') as handle:
            SCORES = pickle.load(handle)
            return SCORES

    for system in systems:
        # dico_system[id] = (ref, hyp)
        with open("../../harvest-transcriptions/data/" + system + "/" + system + "1.txt", "r", encoding="utf8") as file:
            dico_system = dict()
            for ligne in file:
                line = ligne.split("\t")
                id = line[0]
                ref = removeEPS(line[1])
                hyp = removeEPS(line[2])
                dico_system[id] = [ref, hyp]
        for metric in metrics:
            with open("../../harvest-transcriptions/results/correlation/" + metric + "_" + system + ".txt", "r", encoding="utf8") as file:
                for ligne in file:
                    line = ligne[:-1].split("\t")
                    id = line[0]
                    score = float(line[1])
                    ref = dico_system[id][0]
                    hyp = dico_system[id][1]
                    # SCORES[metric][system][id] = [ref, hyp, score]
                    add(SCORES, ref, hyp, metric, system, score)
    overwrite = input("Do you wish to overwrite previous SCORES? (y/n) : ")
    if overwrite == "y":
        with open("SCORES.pickle", "wb") as handle:
            pickle.dump(SCORES, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return SCORES

def score(SCORES, ref, hyp, metric):
    return SCORES[ref][hyp][metric]["score"]


# now, I should check if SCORES make sense by comparing its scores with scores in files
# then, I can observe who's the winner for each choice and look who has the best correlation


if __name__ == "__main__":

    # SCORES[ref][hyp][metric] = {"system": [system1, system2], "score": score}
    SCORES = init_SCORES(keep="y")
    print(len(SCORES))
    print(total)


    human_choices = dict() # humain_choices[20] = [A, A, B, B, A]

    directory = '.'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            if f[-5:] == ".json":
                for id, choice in json.load(open(f))["answers"].items():
                    id = int(id)
                    if id in human_choices:
                        human_choices[id].append(choice)
                    else:
                        human_choices[id] = [choice]
    

    experimentData = dict()
    experimentData_list = json.load(open("../experimentData.json"))
    for i in range(len(experimentData_list)):
        for j in range(len(experimentData_list[i]["audioList"])):
            id = int(experimentData_list[i]["audioList"][j]["id"])
            ref = experimentData_list[i]["audioList"][j]["reference"]
            hypA = experimentData_list[i]["audioList"][j]["hypotheses"]["A"]
            hypB = experimentData_list[i]["audioList"][j]["hypotheses"]["B"]
            experimentData[id] = dict()
            experimentData[id]["reference"] = ref
            experimentData[id]["hypA"] = hypA
            experimentData[id]["hypB"] = hypB

    
    
    # Right now, I have a variable with the SCORES for every metric given reference and hypothesis.
    # SCORES[ref][hyp][metric] = {"system": [system1, system2], "score": score}

    # I also have the human_choices given id
    # human_choices[id] = [A, B, B, B, A]

    # Now, I have the reference and hypothesis given id --> open experimentData.json
    # experimentData[id] = {"reference": je sais, "hypA": je c, "hypB": je sai}

    # I have to browse human_choice and increment score for each metric
    
    grade = dict()
    losses = dict()
    keyerror = dict()
    for metric in metrics:
        grade[metric] = 0
        keyerror[metric] = 0
        losses[metric] = 0

    
    # BROWSING
    for i in range(1, len(human_choices)+1):
        print(i, human_choices[i])
        # look at score for each metric
        nbrA = human_choices[i].count("A")
        nbrB = human_choices[i].count("B")

        ref = experimentData[i]["reference"]
        hypA = experimentData[i]["hypA"]
        hypB = experimentData[i]["hypB"]
        
        if nbrA > nbrB: # A is winner
            # look at SCORES[ref][hypA]
            # browse each metric
            
            for metric in metrics:
                try:
                    if SCORES[ref][hypA][metric]["score"] < SCORES[ref][hypB][metric]["score"]: # minimum because lower is better / A is better
                        grade[metric] += 1
                    else:
                        losses[metric] += 1
                except KeyError:
                    keyerror[metric] += 1
        elif nbrA < nbrB:
            for metric in metrics:
                try:
                    if SCORES[ref][hypA][metric]["score"] > SCORES[ref][hypB][metric]["score"]: # minimum because lower is better / B is better
                        grade[metric] += 1
                    else:
                        losses[metric] += 1
                except KeyError:
                    keyerror[metric] += 1
        else:
            # ex aequo, ignore?
            continue
    
    for metric in metrics:
        print(metric[:5]+":\tgrade = "+str(grade[metric])+"\tlosses = "+str(losses[metric])+"\tscore = "+str(grade[metric]/losses[metric]*100)+"\tkeyerror = "+str(keyerror[metric]))
    print("total:", total)

    # y a t'il beaucoup d'ex aequo selon les métriques?