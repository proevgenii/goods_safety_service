import re
import pickle
import nltk

nltk.download("stopwords")
from nltk.corpus import stopwords
import pymorphy2

russian_stopwords = stopwords.words("russian")
morph = pymorphy2.MorphAnalyzer()


def clear_text(string: str) -> str:
    """Remove all non-alphabetic characters and save only Russian characters and also remove words with lenght <3"""
    string = re.sub("[^А-я\s]+", " ", string.lower())
    return re.sub(r"\b\w{1,3}\b", "", string)


def lemmatize_dubl(string: str) -> str:
    """Lemmatize input string and delete stop words"""
    return " ".join(
        [
            morph.parse(word)[0].normal_form
            for word in string.split()
            if word not in russian_stopwords
        ]
    )


def predict_baseline(name: str) -> dict:
    """Predict class of Группа продукции using Общее наименование продукции return dict like {`prod_group`: `name of production group`}"""

    # TODO: fix this, not optimal in terms of speed
    # load model
    with open("models/baseline_model.pkl", "rb") as f:
        clf = pickle.load(f)
    #TODO: fix this, not optimal in terms of speed
    with open("data/group_dict.pkl", "rb") as f:
        group_dct = pickle.load(f)

    # preprocess text
    clear_name = clear_text(name)
    clear_name = lemmatize_dubl(clear_name)
    # run clf
    cls = clf.predict([clear_name])

    return {"prod_group": group_dct[cls[0]]}
