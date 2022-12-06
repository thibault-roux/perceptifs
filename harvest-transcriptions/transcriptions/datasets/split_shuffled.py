from random import randrange as rand

with open("autoselect.txt", "r", encoding="utf8") as file:
    pairs = []
    for ligne in file:
        pairs.append(ligne[:-1])

iterator = 0
while len(pairs) > 0:
    miniset = []
    for i in range(100):
        randnum = rand(len(pairs))
        miniset.append(pairs.pop(randnum))
    with open("min_" + str(iterator) + ".txt", "w", encoding="utf8") as file:
        txt = ""
        for p in miniset:
            txt += p + "\n"
        file.write(txt)
    iterator += 1
