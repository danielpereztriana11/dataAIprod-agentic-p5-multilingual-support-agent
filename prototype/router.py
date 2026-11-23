"""Step 1 — the router (rung 2: classical ML).
Two small models trained on data/tickets_synthetic.csv (synthetic, never the eval-set):
- language: character n-grams + logistic regression -> en | fr | es | pt | pl | ar | other
- category: character n-grams + logistic regression -> how_do_i | sensitive | security | technical
Returns the label and its confidence (max predict_proba)."""
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

HERE = os.path.dirname(os.path.abspath(__file__))
_LANG, _CAT = None, None


def train(csv_path=os.path.join(HERE, "data", "tickets_synthetic.csv")):
    global _LANG, _CAT
    df = pd.read_csv(csv_path)
    _LANG = make_pipeline(TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 3)), LogisticRegression(max_iter=2000, C=10))
    _LANG.fit(df["text"], df["language"])
    _CAT = make_pipeline(TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5)), LogisticRegression(max_iter=2000, C=10))
    _CAT.fit(df["text"], df["category"])


def _top(model, text):
    proba = model.predict_proba([text])[0]
    i = proba.argmax()
    return model.classes_[i], float(proba[i])


def detect_language(text):
    if _LANG is None:
        train()
    return _top(_LANG, text)


def predict(text):
    """Return dict(language, lang_conf, category, cat_conf)."""
    if _CAT is None:
        train()
    lang, lc = _top(_LANG, text)
    cat, cc = _top(_CAT, text)
    return {"language": lang, "lang_conf": lc, "category": cat, "cat_conf": cc}
