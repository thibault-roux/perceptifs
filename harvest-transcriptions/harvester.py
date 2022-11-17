from jiwer import wer

def removeEPS(sentence):
    new_sentence_list = []
    sentence_list = sentence.split(" ")
    for word in sentence_list:
        if word != '<eps>':
            new_sentence_list.append(word)
    return ' '.join(new_sentence_list)



pair = ["KD_woR", "KD_R"]

def get_score(metric, id):
    dico = dict()
    with open("results/correlation/" + metric + "_" + id + ".txt", "r", encoding="utf8") as file:
        for ligne in file:
            ligne = ligne[:-1].split("\t")
            dico[int(ligne[0])] = [float(ligne[1]), "<EMPTY>", "<EMPTY>"]
    with open("data/" + id + "/" + id + "1.txt", "r", encoding="utf8") as file:
        for ligne in file:
            ligne = ligne[:-1].split("\t")
            dico[int(ligne[0])] = [dico[int(ligne[0])][0], removeEPS(ligne[1]), removeEPS(ligne[2])]
    new_dico = dict()
    for k, v in dico.items():
        new_dico = 
    return dico

wer_kd_woR = get_score("wer", "KD_woR")
wer_kd_wR  = get_score("wer", "KD_wR")

# def check_data():


incoherence = 0
wers = []
for k, v in wer_kd_woR.items():
    """if v[0] != 100*wer([v[1]], v[2]): # le WER entre la référence et l'hypothèse correspond à celui enregistré
        print(k, 100*wer([v[1]], v[2]), v)"""
    if wer_kd_wR[k][1] != v[1]: # si les ref sont identiques pour les deux dictionnaires
        print(k)
        print(wer_kd_wR[k][1])
        print(v[1])
        print()
        incoherence += 1
        wers.append(100*wer([v[1]], [wer_kd_wR[k][1]]))
print("Il y a " + str(incoherence) + " incohérence(s) entre les deux fichiers")
print("WER  moyen: ", sum(wers)/len(wers))

# Step 1 : vérifier que les transcriptions sont alignées (transcription 1 de KD_woR == transcription 1 de KD_wR)
# Step 2 : calculer le WER des transcriptions