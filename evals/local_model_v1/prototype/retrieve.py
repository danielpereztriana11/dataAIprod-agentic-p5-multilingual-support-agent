"""Step 3a — retrieval over the English KB (kb/*.md), chunked by '## ' heading.
v0 = TF-IDF on character n-grams (catches cognates: export/exportar, notification/notificaciones).
It does NOT understand Polish or Arabic against English text: that is a known limit, measured by the eval."""

import glob
import json
from urllib.request import Request, urlopen
import os
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

HERE = os.path.dirname(os.path.abspath(__file__))
_CHUNKS, _VEC, _MAT = [], None, None
_EMBED_CACHE = None
MIN_SCORE = 0.10


def _load(kb_dir=os.path.join(HERE, "kb")):
    global _CHUNKS, _VEC, _MAT, _EMBED_CACHE
    _EMBED_CACHE = None
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


def _embed(inputs):
    payload = json.dumps({"model": "paraphrase-multilingual", "input": inputs}).encode("utf-8")
    request = Request("http://127.0.0.1:11434/api/embed", data=payload,
                      headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=120) as response:
        embeddings = json.load(response)["embeddings"]
    if len(embeddings) != len(inputs) or any(not v for v in embeddings):
        raise ValueError("Invalid embedding response")
    return embeddings


def semantic_top_k(query, k=3, min_score=0.50, min_margin=0.04):
    """Local prototype. Low or ambiguous matches return no source, not a guess."""
    global _EMBED_CACHE
    if _VEC is None:
        _load()
    try:
        if _EMBED_CACHE is None:
            _EMBED_CACHE = _embed([c["section"] + " " + c["text"] for c in _CHUNKS])
        query_vector = _embed([query])
        sims = cosine_similarity(query_vector, _EMBED_CACHE)[0]
        order = sims.argsort()[::-1]
        first = int(order[0])
        different = next((int(i) for i in order if _CHUNKS[i]["article"] != _CHUNKS[first]["article"]), None)
        if sims[first] < min_score or (different is not None and sims[first] - sims[different] < min_margin):
            return []
        return [dict(_CHUNKS[int(i)], score=float(sims[i])) for i in order[:k] if sims[i] >= min_score]
    except (OSError, ValueError, KeyError, TypeError):
        return []  # unavailable model, malformed response or invalid vectors -> handoff

def top_k(query, k=3, min_score=MIN_SCORE):
    if os.getenv("RETRIEVAL_MODE") == "semantic":
        return semantic_top_k(query, k=k)
    if _VEC is None:
        _load()
    sims = cosine_similarity(_VEC.transform([query]), _MAT)[0]
    order = sims.argsort()[::-1][:k]
    return [dict(_CHUNKS[i], score=float(sims[i])) for i in order if sims[i] >= min_score]
