import random
import progressbar

def remove_eps(sentence):
    return " ".join([word for word in sentence.split() if word != "<eps>"])

def load_transcriptions(system):
    id2refhyp = dict()
    with open("data/" + system + "/" + system + "1.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            line = line.split("\t")
            id = line[0]
            ref = remove_eps(line[1])
            hyp = remove_eps(line[2])
            id2refhyp[id] = (ref, hyp)
    return id2refhyp

def load_hats():
    path = "/users/troux/these/expe/metrics/Hats.txt"
    hats = set()
    with open(path, "r", encoding="utf8") as file:
        next(file)
        for line in file:
            line = line.split("\t")
            ref = line[0]
            hypA = line[1]
            hypB = line[3]
            hats.add((ref, hypA, hypB))
    return list(hats)




# the objective is to produce a dataset containing triplets not present in HATS
if __name__ == "__main__":
    systems = ["KD_woR", "KD_wR", "SB_bpe1000", "SB_bpe750", "SB_s2s", "SB_w2v_1k", "SB_w2v_3k", "SB_w2v_7k", "SB_xlsr_fr", "SB_xlsr"]

    data = dict()
    for system in systems:
        data[system] = load_transcriptions(system)
    keys = data[systems[0]].keys()

    hats = load_hats()

    MAX_LEN = 20
    dataset_size = 20000 # start to get long

    new_dataset = []
    progress = progressbar.ProgressBar(maxval=dataset_size)
    for i in range(dataset_size):
        progress.update(i)
        random_system1 = random.choice(systems)
        random_system2 = random_system1
        while random_system2 == random_system1:
            random_system2 = random.choice(systems)
        # data[random_system1] # dictionary of id2refhyp
        flag = True
        while flag:
            flag = False
            random_id = random.choice(list(keys))
            ref, hyp1 = data[random_system1][random_id]
            _, hyp2 = data[random_system2][random_id]
        
            if (ref, hyp1, hyp2) in hats or (ref, hyp2, hyp1) in hats:
                flag = True
            elif hyp1 == hyp2:
                flag = True
            elif ref == hyp1 or ref == hyp2:
                flag = True
            elif (ref, hyp1, hyp2) in new_dataset or (ref, hyp2, hyp1) in new_dataset:
                flag = True
            elif len(ref.split(" ")) > MAX_LEN or len(hyp1.split(" ")) > MAX_LEN or len(hyp2.split(" ")) > MAX_LEN:
                flag = True
        new_dataset.append((ref, hyp1, hyp2))
        
    with open("new_dataset.txt", "w") as f:
        for ref, hyp1, hyp2 in new_dataset:
            f.write(ref + "\t" + hyp1 + "\t" + hyp2 + "\n")
    print("done")
    
