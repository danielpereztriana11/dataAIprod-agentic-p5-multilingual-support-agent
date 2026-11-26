import os
import retrieve

cases = [
    ("en", "How do I change my profile photo?", "KB-PROFILE-01"),
    ("fr", "Comment changer la langue de la plateforme ?", "KB-SETTINGS-02"),
    ("es", "¿Cómo descargo los recursos del curso?", "KB-CONTENT-02"),
    ("pt", "Como adiciono legendas a um vídeo?", "KB-CONTENT-04"),
    ("pl", "Jak pobrać materiały z kursu?", "KB-CONTENT-02"),
    ("ar", "كيف أغير كلمة المرور؟", "KB-ACCOUNT-01"),
]
for lang, question, expected in cases:
    os.environ.pop("RETRIEVAL_MODE", None)
    baseline = retrieve.top_k(question)
    os.environ["RETRIEVAL_MODE"] = "semantic"
    semantic = retrieve.top_k(question)
    def show(result):
        return ", ".join(f"{x['article']}:{x['score']:.3f}" for x in result) or "handoff"
    print(f"{lang} expected={expected} | tfidf={show(baseline)} | semantic={show(semantic)}")
