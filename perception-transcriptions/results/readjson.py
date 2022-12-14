import json

# import argparse
# parser = argparse.ArgumentParser(description="Compare opinions for an experience")
# """parser.add_argument("json1", type=str, help="Name of the first json file.")
# parser.add_argument("json2", type=str, help="Name of the second json file.")"""
# parser.add_argument('files', type=str, nargs='+')
# args = parser.parse_args()

import os

# dicolist = []
# for file in args.files:
#     f = open(file)
#     data = json.load(f)
#     dicolist.append(data["answers"])

dicolist = []
for file in args.files:
    f = open(file)
    data = json.load(f)
    dicolist.append(data["answers"])

total_dico = dict()
for k, _ in dicolist[0].items():
    total_dico[k] = []
    for dico in dicolist:
        total_dico[k].append(dico[k])


minid = int(args.files[0].split("-")[0][4:])
experimentData = json.load(open("../experimentData.json"))
Data = experimentData[minid]["audioList"]
# for i in range(50):
#     j = i+1
#     print(experimentData[minid]["audioList"][j])
#     input()

certain = 0
incertain = 0

for k, v in total_dico.items():
    k = int(k)
    v.sort()
    nbrA = v.count("A")
    nbrB = v.count("B")
    # print(k)
    # print("--", Data[k-1]["reference"])
    # print("A:", Data[k-1]["hypotheses"]["A"])
    # print("B:", Data[k-1]["hypotheses"]["B"])
    # input()
    # print("A:", nbrA)
    # print("B:", nbrB)
    # print("------")

    total = nbrA + nbrB
    percent = nbrA/total * 100
    # print(percent)
    # input()
    if percent < 22 or percent > 78:
        certain += 1
    else:
        incertain += 1

print("certain:", certain)
print("incertain:", incertain)

# Il faut que je code le reader pour qu'il lise tous les fichiers que j'ai
# il faut aussi que je regarde le nombre d'accord avec les métriques

# il faut aussi que je regarde la corrélation entre les ratios de A/B et métrique(A)/métrique(B)

# mon code est tout moisi, je devrais ptet repartir sur des bases plus saines.






#with open("../audio/datasets/autoselect.txt", "r", encoding="utf8") as file:
    

"""
f1 = open(args.json1)
f2 = open(args.json2)

data1 = json.load(f1)
data2 = json.load(f2)

print(data1["name"])
print(type(data1["answers"]))

dico1 = data1["answers"]
dico2 = data2["answers"]
"""
