import random

def load_transcriptions(system):
    id2refhyp = dict()
    with open("data/" + system + "/" + system + "1.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            line = line.split("\t")
            id = line[0]
            ref = line[1]
            hyp = line[2]
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
    print(len(keys))

    hats = load_hats()

    for i in range(20000):
        random_system = random.choice(systems)
        

