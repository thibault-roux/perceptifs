

def rater_agreement_average():

    # read the hats.txt file
    hats = dict()
    with open("hats.txt", "r", encoding="utf8") as f:
        id = 1
        next(f)
        for line in f:
            line = line.strip().split("\t")
            hats[id] = {"A": line[2], "B": line[4]}
            id += 1

    N = 50
    Kappas = []
    for i in range(20):
        id = i*50+1

        pA = 0
        pB = 0
        Pis = []
        n = int(hats[id]["A"]) + int(hats[id]["B"]) # 7 most of the times
        for id in range(id, id+50):
            A = int(hats[id]["A"])
            B = int(hats[id]["B"])
            pA += A
            pB += B
            Pi = 1/(n*(n-1)) * (A**2 + B**2 - n)
            Pis.append(Pi)
        pA /= N*n
        pB /= N*n

        P_bar = sum(Pis)/N
        P_bar_e = pA**2 + pB**2

        K = (P_bar - P_bar_e)/(1 - P_bar_e)
        Kappas.append(K)
    print("Average Kappa:", sum(Kappas)/len(Kappas))



def rater_agreement_full():

    # read the hats.txt file
    hats = dict()
    with open("hats.txt", "r", encoding="utf8") as f:
        id = 1
        next(f)
        for line in f:
            line = line.strip().split("\t")
            hats[id] = {"A": line[2], "B": line[4]}
            id += 1

    N = 0 # 850
    Kappas = []
    pA = 0
    pB = 0
    Pis = []
    for id in range(20*50):
        id += 1
        
        n = int(hats[id]["A"]) + int(hats[id]["B"]) # 7 most of the times
        if n != 7:
            continue
        A = int(hats[id]["A"])
        B = int(hats[id]["B"])
        pA += A
        pB += B
        Pi = 1/(n*(n-1)) * (A**2 + B**2 - n)
        Pis.append(Pi)
        N += 1
    pA /= N*7
    pB /= N*7

    P_bar = sum(Pis)/N
    P_bar_e = pA**2 + pB**2

    K = (P_bar - P_bar_e)/(1 - P_bar_e)
    print("Kappa:", K)




def agreement_global():
    # read the hats.txt file
    hats = dict()
    with open("hats.txt", "r", encoding="utf8") as f:
        id = 1
        next(f)
        for line in f:
            line = line.strip().split("\t")
            hats[id] = {"A": line[2], "B": line[4]}
            id += 1

    agreements = []
    for id in range(20*50):
        id += 1
        A = int(hats[id]["A"])
        B = int(hats[id]["B"])

        agreement = max(A, B) / (A + B)        
        agreements.append(agreement)
    print("Average agreement:", sum(agreements)/len(agreements))
    agreeset = set(agreements)
    print(agreeset)

if __name__ == "__main__":
    rater_agreement_average()
    # rater_agreement_full()

    agreement_global()