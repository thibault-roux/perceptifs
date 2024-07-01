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
        return str(data["name"])
    except FileNotFoundError:
        return None


def annotate():
    annotations = load_annotations()
    for num_dataset in range(20):
        for num_human in range(8):
            # annotate
            name = get_answers(num_dataset, num_human)
            if name in annotations or name is None:
                print(name, "skipped.")
                continue
            print(name)
            inp = input("Male or female? (M/F/X/STOP) ")
            if inp == "STOP" or (inp != "M" and inp != "F" and inp != "X"):
                save_annotations(annotations)
                exit()
            annotations[name] = inp
    save_annotations(annotations)
    

def load_annotations():
    print("Load annotations...")
    annotations = dict()
    try:
        with open("annotation.txt", "r", encoding="utf8") as f:
            for line in f:
                name, annotation = line[:-1].split(" : ")
                annotations[name] = annotation
    except FileNotFoundError:
        print("No annotations.")
        return annotations
    print("Annotations loaded.")
    return annotations

def save_annotations(annotations):
    print("Saving...")
    # save annotations
    with open("annotation.txt", "w", encoding="utf8") as f:
        for name, annotation in annotations.items():
            f.write(str(name) + " : " + str(annotation) + "\n")
    print("Saved.")

def stats():
    annotations = load_annotations()
    count = {"M": 0, "F": 0, "X": 0}
    for annotation in annotations.values():
        count[annotation] += 1
    print(count)

if __name__ == "__main__":
    annotate()
    stats()