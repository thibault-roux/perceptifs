from jiwer import wer

import argparse
parser = argparse.ArgumentParser(description="Check if data are ok")
parser.add_argument("i", type=str, help="start at line number i.")
args = parser.parse_args()

labels = [c for c in "123456789 ()ABCDEFGHIJKLMNOPQRSTUVWXYZæœàâäéèêëïîôöùûüÿç'-".lower()]

weird = []

with open("autoselect.txt", "r", encoding="utf8") as file:
    i = 1
    for j in range(int(args.i)-1):
        next(file)
        i += 1
    for ligne in file:
        ligne = ligne.split("\t")
        print(str(i) + ")")
        print(ligne[0])
        print("ref:", ligne[1])
        print("hyp:", ligne[2]) #, wer(ligne[1], ligne[2]))
        print("hyp:", ligne[3]) #, wer(ligne[1], ligne[3]))
        #if len(ligne[1]) == len(ligne[2]) or len(ligne[1]) == len(ligne[3]):
        for c in ligne[1]:
            if c not in labels:
                print(c, "1")
                weird.append(c)
        for c in ligne[2]:
            if c not in labels:
                print(c, "2")
                weird.append(c)
        for c in ligne[3]:
            if c not in labels:
                print(c, "3")
                weird.append(c)
        
        i += 1

print(weird)
print(set(weird))

# 21, il manque une transcription