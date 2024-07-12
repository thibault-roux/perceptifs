
# the file ../../experimentData.json is a json file containing the following format:
"""
[
    {
        "id": "min_0",
        "audioList": [
            {"id": "1", "path": "audio/BFMTV_BFMStory_2012-07-24_175800_229.wav", "reference": "le le début de centres nucléaires militaires", "hypotheses": {"A": "le le le début de centres nuclé militaires", "B": "le le le début deux centres nucléaires militaires"}},
            {"id": "2", "path": "audio/BFMTV_BFMStory_2012-07-26_175800_84.wav", "reference": "en tirer les conclusions mais je je trouve cette", "hypotheses": {"A": "euh en tirer des conclusions mais j je trouve cette euh", "B": "euh en tirer les conclusions mais je je trouve cetteuh"}},
            {"id": "3", "path": "audio/BFMTV_CultureEtVous_2012-02-24_065040_4.wav", "reference": "dimanche soir dufreigne philippe", "hypotheses": {"A": "dimanche soir' une ça", "B": "dimanche soire an t e"}},
            ...
        ]
    },
    {
        "id": "min_1",
        "audioList": [
            {"id": "51", "path": "audio/LCP_EntreLesLignes_2013-03-16_212400_31.wav", "reference": "si l' on regarde dit il les engagements mirobolants de quatre vingt un quatre vingt quinze", "hypotheses": {"A": "si l' on regarde dit-il les engagements mir au bolan de quatre-vingt un quatre-vingt quinze", "B": "si l' on regarde dit-il les engagements miro bolland de quatre-vingt n quatre-vingt quinze"}},
            {"id": "52", "path": "audio/BFMTV_BFMStory_2012-07-24_175800_133.wav", "reference": "nous on parle aux français on parle aux électeurs on parle au coeur du peuple militant et justement", "hypotheses": {"A": "on parle aux français par zola je parle aux électeurs on parle au coeur du peuple militant et justement", "B": "nous on parle aux français euh c' est-à-dire qu' il y a aux électeurs on parle au coeur du peuple militant et justement"}},
    ...
    }
]
"""

import json

def load(): # get the dict of id to reference and hypotheses A and B
    with open("../../experimentData.json") as f:
        data = json.load(f)
    return {d["id"]: {a["id"]: a for a in d["audioList"]} for d in data}


def wer(ref, hyp, model):
    return jiwer.wer(ref, hyp)

def cer(ref, hyp, model):
    return jiwer.cer(ref, hyp)

def semdist(ref, hyp, model):
    return cosine_similarity(model.encode([ref]).reshape(1, -1), model.encode([hyp]).reshape(1, -1))

def phoner(ref, hyp, model):
    return jiwer.cer(model.transliterate(ref), model.transliterate(hyp))



def eval(metric):
    # load metric
    if metric == "wer":
        from jiwer import wer
    elif metric == "cer":
        from jiwer import cer
    elif metric == "semdist":
        from sentence_transformers import SentenceTransformer
        from sklearn.metrics.pairwise import cosine_similarity
    elif metric == "phoner":
        from jiwer import cer
        import epitran
        model = epitran.Epitran("fra-Latn")


    for i in range(20):
        for j in range(1, 9):
            exit()


if __name__ == "__main__":
    data = load()

    print(data["min_0"]["1"])

    
    metrics = ["wer", "cer", "semdist", "phoner"]

    for metric in metrics:
        print(f"metric: {metric}")
        eval(metric)