# in this analyze, we will check how much humans agree with each other

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

def average_agreement(num_dataset):
    human2answers = dict() # key: human number, value: answers
    scores = dict() # key: num_human, value: dict(agreement with other humans, disagremment with other humans)
    for num_human in range(8):
        scores[num_human] = dict()
        scores[num_human]["agreement"] = 0
        scores[num_human]["disagreement"] = 0
        # get answers from json
        answers = get_answers(num_dataset, num_human)
        if answers is not None:
            human2answers[num_human] = answers

    for num_human1, answers1 in human2answers.items():
        for num_human2, answers2 in human2answers.items():
            if num_human1 != num_human2:
                # compare answers
                for k in range(1, 50):
                    k = str(k)
                    # print("answers1[k]:", answers1[k], " & answers2[k]:", answers2[k])
                    if answers1[k] == answers2[k]:
                        scores[num_human1]["agreement"] += 1
                    else:
                        scores[num_human1]["disagreement"] += 1

    for num_human, _ in human2answers.items():
        a = scores[num_human]["agreement"]
        d = scores[num_human]["disagreement"]
        print(f"human {num_human} has {a} agreements and {d} disagreements, which is {a/(a+d)*100}% agreement")
    print()

if __name__ == "__main__":
    for num_dataset in range(20):
       data = average_agreement(num_dataset)