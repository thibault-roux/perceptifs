

if __name__ == "__main__":
    total = 0
    criteria = dict()
    with open("autoselect.txt", "r", encoding="utf8") as file:
        for line in file:
            line = line[:-1].split("\t")
            crits = line[4].split(",")
            for crit in crits:
                """if crit not in criteria:
                    criteria[crit] = 0
                criteria[crit] += 1
                """

                crits_local = []
                if len(crit.split("-")) == 2:
                    crits_local = crit.split("-")
                    crits_local.sort()
                    crits_local = [f"{crits_local[0]}-{crits_local[1]}"]
                else:
                    crits_local.append(crit)
                for crit_local in crits_local:
                    if crit_local not in criteria:
                        criteria[crit_local] = 0
                    criteria[crit_local] += 1
            total += 1


    #for crit in criteria:
    #    print(f"{crit}: {criteria[crit]}")


    crit_metrics = ["'b='", "bHD", "bLD", "'c='", "'c=;bD'", "'c=;eD'", "cerINVbertscore", "cerINVember", "cerINVsemdist", "cHD", "cLD", "'c=;sD'", "'c=;wD'", "'e='", "eHD", "eLD", "emberINVbertscore", "emberINVsemdist", "'s='", "semdistINVbertscore", "sHD", "sLD", "'w='", "'w=;bD'", "'w=;cD'", "'w=;eD'", "werINVbertscore", "werINVcer", "werINVember", "werINVsemdist", "wHD", "wLD", "'w=;sD'"]
    systems = ["KD_woR","KD_wR","SB_bpe1000","SB_bpe750","SB_s2s","SB_w2v_1k","SB_w2v_3k","SB_w2v_7k","SB_xlsr"]
    compare_systems = set()
    for system1 in systems:
        for system2 in systems:
            if system1 != system2:
                compare = [system1, system2]
                compare.sort()
                compare_systems.add(f"{compare[0]}-{compare[1]}")

    for compare_system in compare_systems:
        if compare_system not in criteria:
            print(compare_system,": 0")
        else:
            print(compare_system,":", criteria[compare_system])


    """for crit1 in systems:
        for crit2 in systems:
            if crit1 != crit2:
                crit = f"{crit1}-{crit2}"
                if crit not in criteria:
                    print(f"{crit}: 0")
                else:
                    print(f"{crit}: {criteria[crit]}")"""
