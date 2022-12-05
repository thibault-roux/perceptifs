


with open("crits.txt", "r", encoding="utf8") as file:
    crits = []
    for ligne in file:
        crits.append(ligne[:-1])
    
with open("syscomp.txt", "r", encoding="utf8") as file:
    syscomp = []
    for ligne in file:
        syscomp.append(ligne[:-1])

# put all transcriptions in RAM
for sys in syscomp:
    for crit in crits:
        with open()

Sample = set() # sample of all transcriptions

# je peux prendre une transcription et voir combien de critère elle satisfait
# sinon, je prends une transcription de façon aléatoire pour nos 1485 types de comparaisons.
# je l'ajoute, ce qui fait augmenter le nombre d'itération de notre critère (on s'en fiche si la transcription satisfait plusieurs critères)
# j'ai peur que certains critères soient sureprésentés. Pour les statistiques, cela pose problème aussi. On ne sait pas quel pourcentage de chaque critère on a dans notre dataset.
# je veux qu'on sache que dans notre dataset de 1000 paires, on a 30 paires qui satisfaient le critère KD_woR-KD-wR ; on a 115 paires qui satisfaient w=

# Il y a énormémement de paires qui sont dans plusieurs critères à la fois.

# Pour la statisticité, je veux que pour chaque paire choisie, on regarde pour chaque critère

