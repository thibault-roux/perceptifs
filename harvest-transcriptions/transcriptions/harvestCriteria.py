import random

if __name__ == "__main__":
    with open("crits.txt", "r", encoding="utf8") as file:
        crits = set()
        for ligne in file:
            crits.add(ligne[:-1])
        
    with open("syscomp.txt", "r", encoding="utf8") as file:
        syscomp = set()
        for ligne in file:
            syscomp.add(ligne[:-1])

    # put all transcriptions in RAM
    All = dict()
    for sysc in syscomp:
        All[sysc] = dict()
        for crit in crits:
            zeset = set()
            with open("mess/" + sysc + "/" + crit, "r", encoding="utf8") as file:
                for ligne in file:
                    zeset.add(ligne[:-1])
            All[sysc][crit] = zeset


        
    while True:
        Sample = set() # sample of all transcriptions
        satisfy = dict() # to get the number of pair that satisfy each criteria
        for crit in crits:
            satisfy[crit] = 0 # initialize all criteria to zero
        for sysc in syscomp:
            satisfy[sysc] = 0 # initialize all criteria to zero

        while len(Sample) < 1500:
            while True: # select a pair not already in our sample
                rand_sysc = random.sample(syscomp, 1)[0]
                rand_crit = random.sample(crits, 1)[0]
                if len(All[rand_sysc][rand_crit]) >= 1:
                    pair = random.sample(All[rand_sysc][rand_crit], 1)[0]
                if pair not in Sample:
                    break
            Sample.add(pair)


            syscrits = set()
            for sysc in syscomp:
                for crit in crits:
                    if pair in All[sysc][crit]:
                        syscrits.add(sysc)
                        syscrits.add(crit)
            for syscrit in syscrits:
                satisfy[syscrit] += 1

        unsatisfied = []
        for k, v in satisfy.items():
            if v < 50:
                # print(k, v)
                unsatisfied.append(int(v))
        #print("mean:", sum(unsatisfied)/len(unsatisfied)) #maximiser moyenne
        print("len: ", len(unsatisfied)) # minimiser len
        if len(unsatisfied) < 10:
            for k, v in satisfy.items():
                if v < 50:
                    print(k, v)
            ans = input("Is it okay? y/n : ")
            if ans == "y":
                break

    with open("autoselect.txt", "w", encoding="utf8") as file:
        txt = ""
        for line in Sample:
            txt += line + "\n"
        file.write(txt)