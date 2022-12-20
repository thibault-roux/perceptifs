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

    return dico # dico[id] = [ref, hyp, wer, cer, ember, semdist, bertscore] # dict of dict


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


if __name__ == '__main__':

    sys1 = get_score(args.sys1)
    sys2 = get_score(args.sys2)

    # dico[id] = [ref, hyp, wer, cer, ember, semdist]

    better1 = 0
    better2 = 0
    egal = 0
    for id, score1 in sys1.items():
        score2 = sys2[id]

        if score1["ref"] == score2["ref"]: # refs are the same
            # print(args.sys1, score1["hyp"])
            # print(args.sys2, score1["hyp"])
            # input()

            if score1["bertscore"] > score2["bertscore"]:
                better2 += 1
                # print(args.sys2, "a gagné")
            elif score1["bertscore"] < score2["bertscore"]:
                better1 += 1
                # print(args.sys1, "a gagné")
            else:
                egal += 1

    print("better1:", better1)
    print("better2:", better2)
    print("egal:", egal)

    print("sys1:", args.sys1)
    print("sys2:", args.sys2)

    if better1 > better2:
        print(args.sys1, "est le meilleur système.")

    # versus between each system for each metric at the pair level


