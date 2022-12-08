from random import randrange as rand

with open("autoselect.txt", "r", encoding="utf8") as file:
    pairs = []
    for ligne in file:
        pairs.append(ligne[:-1])

"""iterator = 0
global_i = 0
while len(pairs) > 0:
    miniset = []
    for i in range(50):
        randnum = rand(len(pairs))
        miniset.append(pairs.pop(randnum))
    with open("min_" + str(iterator) + ".txt", "w", encoding="utf8") as file:
        txt = ""
        for p in miniset:
            txt += str(global_i) + "\t" + p + "\n"
            global_i += 1
        file.write(txt)
    iterator += 1"""



# begin
txt = "[\n"

iterator = 0
global_i = 0

while len(pairs) > 0:
    miniset = []
    # for each minidataset 0 to 19 (20)
    txt += "\t{\n\t\t\"id\": \"min_" + str(iterator) + "\",\n"
    txt += "\t\t\"audioList\": [\n"

    for i in range(50):
        randnum = rand(len(pairs))
        miniset.append(pairs.pop(randnum))

    # for each pair of minidataset (0 to 49 - 50 to 99 - ...)
    for p in miniset:
        pair = p.split("\t")
        path = "audio/" + pair[0] + ".wav"
        ref = pair[1]
        hyp1 = pair[2]
        hyp2 = pair[3]
        
        global_i += 1
        txt += "\t\t\t{\"id\": \"" + str(global_i) + "\", \"path\": \"" + path + "\", \"reference\": \"" + ref + "\","
        txt += " \"hypotheses\": {\"A\": \"" + hyp1 + "\", \"B\": \"" + hyp2 + "\"}},\n"

    # après parcours de chaque minidataset
    txt = txt[:-2] + "\n\t\t]\n\t},\n"
    iterator += 1

# après parcours de tous les minidataset
txt = txt[:-2] + "\n]"

with open("experimentData.json", "w", encoding="utf8") as file:
    file.write(txt)