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

def agreement_with_majority(num_dataset): # compute the number of times each human agree with most of the other humans
    human2answers = dict() # key: human number, value: answers
    scores = dict() # key: num_human, value: dict(agreement with majority, disagremment with majority)
    for num_human in range(1, 9):
        # get answers from json
        answers = get_answers(num_dataset, num_human)
        if answers is not None:
            human2answers[num_human] = answers
            scores[num_human] = dict()
            scores[num_human]["agreement"] = 0
            scores[num_human]["disagreement"] = 0
        
    # for each human
    for num_human, answers in human2answers.items():
        # for each triplet
        for k, _ in answers.items():
            # count the number of times the human agrees with the majority
            count_A = 0
            count_B = 0
            for num_human2, answers2 in human2answers.items():
                # if num_human != num_human2:
                if True:
                    if answers2[k] == "A":
                        count_A += 1
                    elif answers2[k] == "B":
                        count_B += 1
                    else:
                        print("Error: answer is not A or B :", answers2[k])
            if count_A > count_B and answers[k] == "A":
                scores[num_human]["agreement"] += 1
            elif count_B > count_A and answers[k] == "B":
                scores[num_human]["agreement"] += 1
            else:
                scores[num_human]["disagreement"] += 1

    # print scores
    # print(f"Dataset {num_dataset}")
    ratios = []
    for num_human, score in scores.items():
        # print(f"Human {num_human}: ratio = {score['agreement']/(score['agreement']+score['disagreement'])} (agree: {score['agreement']}, disagree: {score['disagreement']})")
        ratio = score['agreement']/(score['agreement']+score['disagreement'])
        ratios.append(ratio)

    # local average
    # print("Local", num_dataset, "average ratio:", sum(ratios)/len(ratios))
    return ratios

flag = False

def plot(data):
    # colors = ["#bleu", "#vert", "#orange", "#jaune", "#rouge", "#violet", "#turquoise"]*3 # "#gris_clair", "#gris_bleuté", "#blanc"
    colors = ["#dae8fc", "#d5e8d4", "#ffe6cc", "#fff2cc", "#f8cecc", "#e1d5e7", "#b0e3e6"]*3 # "#f5f5f5", "#bac8d3", "#ffffff"
    edgecolors = ["#6c8ebf", "#82b366", "#d79b00", "#d6b656", "#b85450", "#9673a6", "#0e8088"]*3 # "#666666", "#23445d", "#000000"


    import random
    from collections import Counter
    for i, scores in enumerate(data):
        for score in set(scores):
            # print(score, end=", ")
            x = i+1 # + random.uniform(-0.2, 0.2)
            plt.scatter(x, score, edgecolor=edgecolors[i], c=colors[i], alpha=1, s=100*scores.count(score))

    plt.xlabel('Sous-ensemble de données annotées')
    plt.ylabel('Ratio')
    plt.xticks(range(1, 21,2))
    plt.gca().set_yticklabels([f'{x:.0%}' for x in plt.gca().get_yticks()]) 
    plt.show()


    plt.savefig("data/figure-ratio.png")


if __name__ == "__main__":
    global_ratios = []
    for num_dataset in range(20):
       ratios = agreement_with_majority(num_dataset)
       global_ratios.append(ratios) # list of lists

    print("Average ratio:", sum([sum(ratios) for ratios in global_ratios])/sum([len(ratios) for ratios in global_ratios]))

    plot(global_ratios)