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


import jiwer
import json

import matplotlib.pyplot as plt


def get_feature(i, j, feature_name):
    try:
        with open(f"./data/min_{i}-{j}.json") as f:
            data = json.load(f)
        return int(data[feature_name].lower())
    except FileNotFoundError:
        return None

def view(feature_name):
    features = []
    for num_dataset in range(20):
        for num_human in range(8):
            # get feature from json
            feature = get_feature(num_dataset, num_human, feature_name)
            if feature is not None:
                features.append(feature)
    # print occurence of each unique feature
    for feature in set(features):
        print(f"{feature}: {features.count(feature)}")

    # histogram of feature
    feature2clean = {"age": "Âge"}
    plt.hist(features, bins=20, color='#d5e8d4', edgecolor='#82b366') #, bins=len(set(features)))
    plt.xlabel(feature2clean[feature_name])
    plt.ylabel("Occurence")

    plt.title(f"Histogramme des {feature2clean[feature_name].lower()}s")
    plt.show()
    # save histogram
    plt.savefig(f"./data/histogram_{feature_name}.pdf")

    print("Plot saved.")




if __name__ == "__main__":
    feature_name="age" # language
    view(feature_name)
    