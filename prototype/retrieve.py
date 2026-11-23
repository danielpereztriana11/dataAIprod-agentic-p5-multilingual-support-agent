"""Step 3a — retrieval over the English KB (kb/*.md), chunked by '## ' heading.
v0 = TF-IDF on character n-grams (catches cognates: export/exportar, notification/notificaciones).
It does NOT understand Polish or Arabic against English text: that is a known limit, measured by the eval."""

import glob
import os
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

HERE = os.path.dirname(os.path.abspath(__file__))
_CHUNKS, _VEC, _MAT = [], None, None
MIN_SCORE = 0.10


def _load(kb_dir=os.path.join(HERE, "kb")):
    global _CHUNKS, _VEC, _MAT
    _CHUNKS = []
    for path in sorted(glob.glob(os.path.join(kb_dir, "*.md"))):
        art = os.path.basename(path)[:-3]
        text = open(path, encoding="utf-8").read()
        for sec in re.split(r"\n## ", text)[1:]:
            title, _, body = sec.partition("\n")
            _CHUNKS.append({"article": art, "section": title.strip(), "text": body.strip()})
    docs = [c["section"] + " " + c["text"] for c in _CHUNKS]
    _VEC = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True).fit(docs)
    _MAT = _VEC.transform(docs)


def top_k(query, k=3, min_score=MIN_SCORE):
    if _VEC is None:
        _load()
    sims = cosine_similarity(_VEC.transform([query]), _MAT)[0]
    order = sims.argsort()[::-1][:k]
    return [dict(_CHUNKS[i], score=float(sims[i])) for i in order if sims[i] >= min_score]
