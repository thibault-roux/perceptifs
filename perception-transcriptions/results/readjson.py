import json

import argparse
parser = argparse.ArgumentParser(description="Compare opinions for an experience")
parser.add_argument("json1", type=str, help="Name of the first json file.")
parser.add_argument("json2", type=str, help="Name of the second json file.")
args = parser.parse_args()

f1 = open(args.json1)
f2 = open(args.json2)

data1 = json.load(f1)
data2 = json.load(f2)

print(data1["name"])
print(type(data1["answers"]))

dico1 = data1["answers"]
dico2 = data2["answers"]

c = 0
i = 0
for k, v in dico1.items():
    print(k, v, dico2[k])
    if v == dico2[k]:
        c += 1
    else:
        i += 1

print("c:", c)
print("i:", i)

#with open("../audio/datasets/autoselect.txt", "r", encoding="utf8") as file:
    