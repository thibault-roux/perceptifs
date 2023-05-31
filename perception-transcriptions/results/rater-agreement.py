import json
import os


def get_data(): # return human_choices[miniset][subject_id][id] = "A" or "B"
    human_choices = dict() # human_choices["18"]["1d3fe665"][763] = "A"

    directory = '.'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            if f[-5:] == ".json":
                try:
                    miniset = int(f.split("min_")[1].split("-")[0])
                    subject_id = f.split("min_")[1].split("-")[1].split(".")[0]
                except IndexError:
                    # print(f)
                    continue
                try:
                    human_choices[miniset][subject_id] = dict() 
                except KeyError:
                    human_choices[miniset] = dict()
                    human_choices[miniset][subject_id] = dict()
                for id, choice in json.load(open(f))["answers"].items():
                    id = int(id)
                    human_choices[miniset][subject_id][id] = choice
    return human_choices



def Kendall(miniset, v):
    # v[subject_id][id] = "A" or "B"
    subjects = list(v.keys())
    print(subjects)

    for i in range(len(subjects)):
        for j in range(i+1, len(subjects)):
            subject1 = subjects[i]
            subject2 = subjects[j]
            # check how many times they agree
            N = 0 # agree
            for id in v[subject1].keys():
                if v[subject1][id] == v[subject2][id]:
                    N += 1
            n = 50 # number of stimuli
            partial_concordance = 2*N/(n*(n-1))
            partial_concordances.append(partial_concordance)

    input()

    exit(-1)



if __name__ == "__main__":
    human_choices = get_data() # human_choices[miniset][subject_id][id] = "A" or "B"

    kendalls = []
    # for miniset, v in human_choices.items():
    for miniset in range(len(human_choices)):
        v = human_choices[miniset]
        kendalls.append(Kendall(miniset, v))

    print("len:", len(human_choices))


