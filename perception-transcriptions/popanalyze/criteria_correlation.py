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


def respect_criteria(i, num_human, filt):
    # return true if the human respect the critera
    # else false
    # i.e. True if filt == gender-male and human is male
    if filt == "nofilter":
        return True # always respecting
    elif filt[:6] == "gender":
        name2genders = dict()
        with open("annotation.txt", "r", encoding="utf8") as file:
            i_t = 0
            num_human_t = 0
            for line in file:
                name, gender = line.split(" : ")
                name2genders[name] = gender[0]
        target = filt[7:]
        name = get_criteria(i, num_human, "name")
        gender = name2genders[name]
        if target == "male":
            if gender == "M":
                return True
            elif gender == "F":
                return False
            elif gender == "X":
                return False
            else:
                raise NotImplementedError("gender unrecognized: " + gender)
        elif target == "female":
            if gender == "F":
                return True
            elif gender == "M":
                return False
            elif gender == "X":
                return False
            else:
                raise NotImplementedError("gender unrecognized: " + gender)
        else:
            raise NotImplementedError("Filter '" + filt + "' not implemented yet.")
    elif filt[:4] == "lang":
        target = filt[5:]
        if target == "others":
            # return true if the language is NOT french
            return "fran" not in get_criteria(i, num_human, "language").lower()
        elif target == "fr":
            # return true if the language is french (should be ignored)
            return "fran" in get_criteria(i, num_human, "language").lower()
        else:
            raise NotImplementedError("Filter '" + filt + "' not implemented yet.")
    elif filt[:7] == "nbrlang":
        target = int(filt[8:])
        if target >= 4:
            return int(get_criteria(i, num_human, "nbOfLanguages")) >= 4
        elif target >= 0:
            return int(get_criteria(i, num_human, "nbOfLanguages")) == target
        else:
            raise NotImplementedError("Filter '" + filt + "' not implemented yet.")
    elif filt[:7] == "studies":
        target = filt[8:]
        first_year, last_year = target.split("-")
        if int(first_year) <= int(get_criteria(i, num_human, "educationLevel")) < int(last_year):
            return True
        else:
            return False
    elif filt[:3] == "age":
        target = filt[4:]
        first_year, last_year = target.split("-")
        if int(first_year) <= int(get_criteria(i, num_human, "age")) < int(last_year):
            return True
        else:
            return False
    else:
        raise NotImplementedError("ERROR. Filter '" + filt + "' does not exist.")
        exit()
    criteria = get_criteria(i, num_human, f)



def compute_correlation(human_data, metric_data, filt):
    # compute correlation between data and metric_data
    # data is a list of 20 minisets, each miniset contains 8 humans, each human has 50 choices
    # metric_data is a list of 20 minisets, each miniset contains 50 choices

    agree = 0
    disagree = 0
    for i in range(len(human_data)):
        for num_human in range(len(human_data[i])):
            # should add a filter here
            if not respect_criteria(i, num_human+1, filt): # if it does respect the criteria
                continue
            for j in range(len(human_data[i][num_human])):
                human_choice = human_data[i][num_human][j]
                metric_choice = metric_data[i][j]
                if human_choice == metric_choice:
                    agree += 1
                else:
                    disagree += 1
    return round(agree / (agree + disagree), 5), (agree+disagree)



if __name__ == "__main__":
    human_data = get_human_choice()
    
    metrics = ["wer", "cer", "semdist", "phoner"]
    filters = ["nofilter",
                "gender-male", "gender-female",
                "lang-fr", "lang-others",
                "nbrlang-1", "nbrlang-2", "nbrlang-3", "nbrlang-4",
                "studies-0-2", "studies-3-4", "studies-5-7", "studies-8-15",
                "age-0-30", "age-31-50", "age-51-99"]

    txt_ratio = ","
    txt_total = ","
    for filt in filters:
        txt_ratio += filt + ","
        txt_total += filt + ","
    txt_ratio = txt_ratio[:-1] + "\n"
    txt_total = txt_total[:-1] + "\n"
    for metric in metrics:
        metric_data = get_metric_choice(metric)
        txt_ratio += metric + ","
        txt_total += metric + ","
        for filt in filters:
            agreement, total = compute_correlation(human_data, metric_data, filt)
            txt_ratio += str(agreement) + ","
            txt_total += str(total) + ","
        txt_ratio = txt_ratio[:-1] + "\n"
        txt_total = txt_total[:-1] + "\n"

    with open("results/ratio.csv", "w") as f:
        f.write(txt_ratio)
    with open("results/total.csv", "w") as f:
        f.write(txt_total)
    print("done")