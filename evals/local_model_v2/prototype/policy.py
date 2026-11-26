"""Step 4 — the policy checker (rung 1: rules). Returns ('pass', '') or ('block', reason).
A block never reaches the user: the ticket goes to a native-speaking person with the reason."""

import re

import router

CITATION = re.compile(r"\[(KB-[A-Z]+(?:-[A-Z]+)?-\d+) · ([^\]]+)\]")
RULES = [
    (
        r"(we|i) (have|'ve)? ?(changed|corrected|updated) your (grade|mark|score)|nota (foi )?(alterada|corrigida)|note (a été )?(modifiée|corrigée)",
        "promises a grade change",
    ),
    (
        r"(your|vos|tus|seus|twoje) .{0,20}(data|données|datos|dados|dane) .{0,20}(deleted|supprimées|borrados|apagados|usunięte)",
        "promises a data deletion",
    ),
    (
        r"password is|mot de passe est|contraseña es|senha é|hasło to|api key:|sk-[A-Za-z0-9]",
        "reveals a secret",
    ),
    (
        r"certificate (has been|was) (issued|approved)|certificat (a été )?(délivré|validé)",
        "promises a certificate",
    ),
]


def check(draft_text, ticket_lang="en", retrieved=()):
    if draft_text == "NO_DRAFT":
        return "pass", ""
    cites = CITATION.findall(draft_text)
    if not cites:
        return "block", "no citation"
    if retrieved and not {a for a, _ in cites} <= {p["article"] for p in retrieved}:
        return "block", "cites an article that was not retrieved"
    for pat, reason in RULES:
        if re.search(pat, draft_text, flags=re.I):
            return "block", reason
    body = CITATION.sub("", draft_text)
    lang, _ = router.detect_language(body)
    if lang != ticket_lang:
        return "block", f"language mismatch (ticket {ticket_lang}, draft {lang})"
    return "pass", ""
