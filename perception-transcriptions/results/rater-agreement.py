import json
import os


def get_data(): # return human_choices[miniset][subject_id][id] = "A" or "B"
    human_choices = dict() # human_choices["18"]["1d3fe665"][763] = "A"

    directory = '.'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            if f[-5:] == ".json":
                try:
                    miniset = int(f.split("min_")[1].split("-")[0])
                    subject_id = f.split("min_")[1].split("-")[1].split(".")[0]
                except IndexError:
                    # print(f)
                    continue
                try:
                    human_choices[miniset][subject_id] = dict() 
                except KeyError:
                    human_choices[miniset] = dict()
                    human_choices[miniset][subject_id] = dict()
                for id, choice in json.load(open(f))["answers"].items():
                    id = int(id)
                    human_choices[miniset][subject_id][id] = choice
    return human_choices



# def Kendall(miniset, v):
#     # v[subject_id][id] = "A" or "B"
#     subjects = list(v.keys())
#     print(subjects)

#     partial_concordances = []
#     for i in range(len(subjects)):
#         for j in range(i+1, len(subjects)):
#             subject1 = subjects[i]
#             subject2 = subjects[j]
#             # check how many times they agree
#             N = 0 # agree
#             for id in v[subject1].keys():
#                 if v[subject1][id] == v[subject2][id]:
#                     N += 1
#             n = 50 # number of stimuli
#             partial_concordance = 2*N/(n*(n-1))
#             partial_concordances.append(partial_concordance)

#     input()

#     exit(-1)




def Kendall(miniset, v):

    N = 50
    n = len(v.keys()) # 7 most of times
    k = 2 # A and B
    Sum_full = N*n

    # p is computed with the full column
    pA = 0
    pB = 0
    
    # P bar is computed with a sum of A and B for each triplet

    humans = list(v.keys())
    for id in v[humans[0]]: # wrong, we want a pA and pB for each triplet
        for human in humans:
            if v[human][id] == "A":
                pA += 1
            elif v[human][id] == "B":
                pB += 1
    print("pA:", pA)
    print("pB:", pB)
    pA /= Sum_full
    pB /= Sum_full
    print("pA:", pA)
    print("pB:", pB)
    input()
    
    # faut qu'on calcule p_barre

if __name__ == "__main__":
    # human_choices = get_data() # human_choices[miniset][subject_id][id] = "A" or "B"

    # kendalls = []
    # # for miniset, v in human_choices.items():
    # for miniset in range(len(human_choices)):
    #     v = human_choices[miniset]
    #     kendalls.append(Kendall(miniset, v))

    # print("len:", len(human_choices))


    # read the hats.txt file
    hats = dict()
    with open("hats.txt", "r", encoding="utf8") as f:
        id = 1
        next(f)
        for line in f:
            line = line.strip().split("\t")
            hats[id] = {"A": line[2], "B": line[4]}
            id += 1

    N = 50
    Kappas = []
    for i in range(20):
        id = i*50+1

        pA = 0
        pB = 0
        Pis = []
        n = int(hats[id]["A"]) + int(hats[id]["B"]) # 7 most of the times
        for id in range(id, id+50):
            A = int(hats[id]["A"])
            B = int(hats[id]["B"])
            pA += A
            pB += B
            Pi = 1/(n*(n-1)) * (A**2 + B**2 - n)
            Pis.append(Pi)
        pA /= N*n
        pB /= N*n

        P_bar = sum(Pis)/N
        P_bar_e = pA**2 + pB**2

        K = (P_bar - P_bar_e)/(1 - P_bar_e)
        print(K)
        Kappas.append(K)
    print("Average Kappa:", sum(Kappas)/len(Kappas))






