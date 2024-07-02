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



def get_answers(i, j):
    try:
        with open(f"./data/min_{i}-{j}.json") as f:
            data = json.load(f)
        return data["answers"]
    except FileNotFoundError:
        return None

def agreement_with_majority(num_dataset): # compute the number of times each human agree with most of the other humans
    human2answers = dict() # key: human number, value: answers
    scores = dict() # key: num_human, value: dict(agreement with majority, disagremment with majority)
    for num_human in range(8):
        scores[num_human] = dict()
        scores[num_human]["agreement"] = 0
        scores[num_human]["disagreement"] = 0
        # get answers from json
        answers = get_answers(num_dataset, num_human)
        if answers is not None:
            human2answers[num_human] = answers
        
    # for each human
    for num_human, answers in human2answers.items():
        # for each triplet
        for k, _ in answers.items():
            # count the number of times the human agrees with the majority
            count_A = 0
            count_B = 0
            for num_human2, answers2 in human2answers.items():
                if num_human != num_human2:
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
    print(f"Dataset {num_dataset}")
    for num_human, score in scores.items():
        print(f"Human {num_human}: agreement = {score['agreement']}, disagreement = {score['disagreement']}")

    exit()
                
    return scores

if __name__ == "__main__":
    for num_dataset in range(20):
       scores = agreement_with_majority(num_dataset)