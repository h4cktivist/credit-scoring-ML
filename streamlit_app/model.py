import urllib.request
from pickle import load
import sklearn


def load_model():
    url = 'https://drive.google.com/uc?export=download&id=13TLGYSEBtBiS179Vlmtq0lyXVdWelLvr'
    with urllib.request.urlopen(url) as f:
        model = load(f)

    return model


def make_prediction(df):
    model = load_model()

    probs = model.predict_proba(df)
    classes = probs[:, 1] > 0.39074379276042953

    result_classes = {
        False: 'Congratulations, you will be granted a loan!',
        True: 'Unfortunately, you will not be given a loan.'
    }

    prediction = result_classes[classes[0]]

    return prediction, probs[:, 1][0]
