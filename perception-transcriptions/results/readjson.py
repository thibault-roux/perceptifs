import json

import argparse
parser = argparse.ArgumentParser(description="Compare opinions for an experience")
"""parser.add_argument("json1", type=str, help="Name of the first json file.")
parser.add_argument("json2", type=str, help="Name of the second json file.")"""
parser.add_argument('files', type=str, nargs='+')
args = parser.parse_args()


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

certain = 0
moyen = 0
incertain = 0

for k, v in total_dico.items():
    nbrA = v.count("A")
    nbrB = v.count("B")
    if nbrA == 0 or nbrA == 4:
        certain += 1
    elif nbrA == 1 or nbrA == 3:
        moyen += 1
    elif nbrA == 2:
        incertain += 1
    else:
        print("Error, not implemented")
        exit(-1)

print("certain:", certain)
print("moyen:", moyen)
print("incertain:", incertain)

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
