# in this analyze, we will compute correlation between some human profils and some metrics

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

def get_criteria(i, j, criteria):
    try:
        with open(f"./data/min_{i}-{j}.json") as f:
            data = json.load(f)
        return data[criteria]
    except FileNotFoundError:
        return None

def get_human_choice():
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


def get_metric_choice(metric):
    metric_data = []
    miniset = []
    with open("./metrics/" + metric + ".txt", "r", encoding="utf8") as f:
        for line in f: # each line is in the format 0 1 B
            choice = line.split(" ")[2].strip()
            if choice == "A":
                miniset.append(1)
            elif choice == "B":
                miniset.append(0)
            elif choice == "C":
                miniset.append(2)
            else:
                print("ERROR. choice =", choice)
                exit()
            if len(miniset) == 50:
                metric_data.append(miniset)
                miniset = []
    return metric_data


def compute_correlation(human_data, metric_data, f): # f = filter
    # compute correlation between data and metric_data
    # data is a list of 20 minisets, each miniset contains 8 humans, each human has 50 choices
    # metric_data is a list of 20 minisets, each miniset contains 50 choices

    agree = 0
    disagree = 0
    for i in range(len(human_data)):
        for num_human in range(len(human_data[i])):
            for j in range(len(human_data[i][num_human])):
                # should add a filter here
                human_choice = human_data[i][num_human][j]
                metric_choice = metric_data[i][j]
                if human_choice == metric_choice:
                    agree += 1
                else:
                    disagree += 1
    return agree / (agree + disagree), (agree+disagree)



if __name__ == "__main__":
    human_data = get_human_choice()
    
    metrics = ["wer", "cer", "semdist", "phoner"]
    filters = ["gender", "lang", "nbrlang", "studies", "age"]
    for metric in metrics:
        metric_data = get_metric_choice("semdist")
        for f in filters:
            agreement, total = compute_correlation(human_data, metric_data, f)
    print("agreement:", agreement)