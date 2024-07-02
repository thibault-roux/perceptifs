# in this analyze, we will check how much humans agree with the majority instead of with each other

# we analyze the choice of humans given 1000 triplets (i.e. a reference, and two hypothesis). Each human evaluate 50 triplets. 
# The dataset is splitted in 20 sets.

# in folder ./data, there are files in this format:
#   min_0-1.json
#   min_0-2.json
#   min_0-3.json
#   min_0-4.json
#   min_1-1.json
#   min_1-2.json
#   min_1-3.json
#   min_1-4.json
#   min_2-1.json
#   min_2-2.json
#   ...
#   min_19-763686.json

# each file is a json file, containing choices of one human. The format is the following:
# {
#		 "name": "Paul Dupond",
#		 "age": "25",
#		 "language": "Français",
#		 "nbOfLanguages": "2",
#		 "educationLevel": "5",
#		 "timestamp": "2022-12-09 14:30:24",
#		 "ip": "193.47.210.73",
#		 "answers": {"1":"B","2":"B","3":"B","4":"B","5":"B","6":"A","7":"B","8":"A","9":"B","10":"B","11":"B","12":"B","13":"A","14":"A","15":"B","16":"A","17":"B","18":"B","19":"B","20":"B","21":"B","22":"B","23":"A","24":"B","25":"A","26":"A","27":"B","28":"A","29":"A","30":"A","31":"A","32":"A","33":"B","34":"A","35":"A","36":"B","37":"B","38":"A","39":"A","40":"A","41":"A","42":"A","43":"A","44":"B","45":"B","46":"A","47":"A","48":"B","49":"B","50":"A"}}



import json

import matplotlib.pyplot as plt



def get_answers(i, j):
    try:
        with open(f"./data/min_{i}-{j}.json") as f:
            data = json.load(f)
        return data["answers"]
    except FileNotFoundError:
        return None

def get_name(i, j):
    try:
        with open(f"./data/min_{i}-{j}.json") as f:
            data = json.load(f)
        return data["name"]
    except FileNotFoundError:
        return None

def get_choice():
    # put it to data format
    data = []
    for num_dataset in range(20):
        miniset = []
        for num_human in range(1, 9):
            answers = get_answers(num_dataset, num_human)
            if answers is not None:
                try:
                    miniset.append([1 if answers[key] == "A" else 0 for key, value in answers.items()])
                except KeyError:
                    print("answers:", answers)
                    print("num_dataset:", num_dataset)
                    print("num_human:", num_human)
                    exit()
            data.append(miniset)
    return data




import numpy as np
from statsmodels.stats.inter_rater import fleiss_kappa

"""
# Exemple de génération de données (à remplacer par vos données réelles)
# data = [
#     [
#         [1, 0, 1, 1, 0, 1, 0, ..., 0],  # Annotations for 50 triplets by annotator 1 in set 1
#         [0, 1, 1, 1, 0, 0, 1, ..., 1],  # Annotations for 50 triplets by annotator 2 in set 1
#         ...
#         [1, 1, 0, 1, 0, 1, 1, ..., 0],  # Annotations for 50 triplets by annotator 7 in set 1
#     ],
#     ...
#     [
#         [1, 0, 1, 1, 1, 0, 1, ..., 1],  # Annotations for 50 triplets by annotator 1 in set 20
#         [0, 1, 0, 1, 0, 1, 0, ..., 0],  # Annotations for 50 triplets by annotator 2 in set 20
#         ...
#         [1, 1, 1, 0, 0, 1, 0, ..., 1],  # Annotations for 50 triplets by annotator 7 in set 20
#     ],
# ]

# data = [
#     [
#         [0, 1, 1], # local choices of human 1 of set 1
#         [1, 1, 1], # local choices of human 2 of set 1
#         [0, 1, 1],
#         [0, 1, 1]
#     ],
#     [
#         [1, 1, 1], # local choices of human 1 (or 5) of set 2
#         [1, 1, 1],
#         [1, 1, 1],
#         [1, 1, 1]
#     ],
#     [
#         [0, 0, 0],
#         [0, 0, 0],
#         [0, 0, 0],
#         [1, 0, 0]
#     ]
# ]
"""

def prepare_data_for_kappa(data):
    # Flatten the data: merge all sets into one
    flattened_data = [triplet for set_ in data for triplet in zip(*set_)]
    
    # Count the number of 0's and 1's for each triplet
    count_data = np.zeros((len(flattened_data), 2), dtype=int)
    
    for i, triplet in enumerate(flattened_data):
        count_data[i, 0] = triplet.count(0)
        count_data[i, 1] = triplet.count(1)
    
    return count_data


if __name__ == "__main__":
    data = get_choice()

    
    # compute a fleiss's kappa per set
    kappas = []
    for i in range(20):
        count_data = prepare_data_for_kappa([data[i]])
        kappas.append(fleiss_kappa(count_data, method='fleiss'))
    print("Kappas:", kappas)
    print("Average kappa:", sum(kappas)/len(kappas))

    # count_data = prepare_data_for_kappa(data)
    # print(count_data)
    # kappa = fleiss_kappa(count_data, method='fleiss')

    # print("Kappa de Fleiss:", kappa)
