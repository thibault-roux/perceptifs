
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
import progressbar

def load(): # get the dict of id to reference and hypotheses A and B
    with open("../../experimentData.json") as f:
        data = json.load(f)
    return {d["id"]: {a["id"]: a for a in d["audioList"]} for d in data}


def wer(ref, hyp, model):
    return jiwer.wer(ref, hyp)

def cer(ref, hyp, model):
    return jiwer.cer(ref, hyp)

def semdist(ref, hyp, model): # lower is better
    return 1 - cosine_similarity(model.encode([ref]).reshape(1, -1), model.encode([hyp]).reshape(1, -1))

def phoner(ref, hyp, model):
    return jiwer.cer(model.transliterate(ref), model.transliterate(hyp))



def eval(metric):
    metric_choices = dict()
    for i in range(20):
        metric_choices[i] = dict()
        # progressbar for j
        bar = progressbar.ProgressBar(max_value=50)
        jbar = 0
        for j in range(i*50+1, i*50+51):
            jbar += 1
            bar.update(jbar)

            ref = data[f"min_{i}"][str(j)]["reference"]
            hyp_A = data[f"min_{i}"][str(j)]["hypotheses"]["A"]
            hyp_B = data[f"min_{i}"][str(j)]["hypotheses"]["B"]

            scoreA = metric_function(ref, hyp_A, model)
            scoreB = metric_function(ref, hyp_B, model)
            if scoreA < scoreB:
                metric_choices[i][j] = "A"
            elif scoreA > scoreB:
                metric_choices[i][j] = "B"
            else:
                metric_choices[i][j] = "C"

    return metric_choices


def save(metric, metric_choices):
    with open(metric + ".txt", "w", encoding="utf8") as f:
        # metric_choices is a dict of dict
        for i in metric_choices:
            for j in metric_choices[i]:
                f.write(f"{i} {j} {metric_choices[i][j]}\n")


if __name__ == "__main__":
    data = load()

    
    metrics = ["wer", "cer", "semdist", "phoner"]

    for metric in metrics:        
        # load metric
        if metric == "wer":
            import jiwer
            model = None
            metric_function = wer
        elif metric == "cer":
            import jiwer
            model = None
            metric_function = cer
        elif metric == "semdist":
            from sentence_transformers import SentenceTransformer
            from sklearn.metrics.pairwise import cosine_similarity
            # load sentence camembert
            model = SentenceTransformer('dangvantuan/sentence-camembert-large')
            metric_function = semdist
        elif metric == "phoner":
            from jiwer import cer
            import epitran
            model = epitran.Epitran("fra-Latn")
            metric_function = phoner
        else:
            raise ValueError("Metric not implemented:", metric)


        print(f"metric: {metric}")
        metric_choices = eval(metric)
        save(metric, metric_choices)