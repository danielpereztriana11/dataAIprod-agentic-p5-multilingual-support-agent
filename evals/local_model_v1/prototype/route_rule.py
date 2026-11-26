"""Step 2 — the routing rule (rung 1: rules). spec.md · user_workflow 'route'.
Order matters: language first, then security, then sensitive (governance.md row 4), then confidence.
The rule can only send a ticket TO a person; it never decides alone to answer a sensitive one."""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

SUPPORTED = {"en", "fr", "es", "pt", "pl", "ar"}
LANG_THRESHOLD = 0.50
CAT_THRESHOLD = 0.50

# Never answered by the agent, in any language (governance.md row 4). Keyword floor, reviewed by native speakers.
SENSITIVE = re.compile(
    r"(change|correct|fix|contest|appeal|review)\w*\s.{0,30}(grade|mark|score)|(grade|mark|score)\s.{0,20}(wrong|unfair|change)"
    r"|corrig\w*.{0,20}note|contester.{0,20}note|note.{0,20}(fausse|injuste)|am[ée]nagement|tiers[- ]temps|handicap"
    r"|corrij\w*.{0,20}(nota|calificaci)|reclamar.{0,20}(nota|calificaci)|acusaci[oó]n|copi[ée] en el examen"
    r"|corrigi\w*.{0,20}nota|contestar.{0,20}nota|nota.{0,25}errad|cola na prova"
    r"|zmieni\w*.{0,20}ocen|popraw\w*.{0,20}ocen|odwoła\w*.{0,20}ocen|niepełnospraw"
    r"|درج|علام|إعاق|عسر القراءة|وقت\w* إضافي"
    r"|disab|dyslex|dislex|extra time|more time|accommodation|medical|médical|m[ée]dico"
    r"|(delete|remove|erase|copy of).{0,30}(my )?(personal )?data|données (personnelles|que vous)|datos personales|dados pessoais|dane osobowe|بيانات\w* الشخصية"
    r"|rgpd|gdpr|rodo|usuni\w*.{0,30}dan"
    r"|certificat\w*.{0,40}(never|not|jamais|en attente|pending|nunca|nie )|(no encuentro|not received|jamais re[çc]u).{0,20}certificad"
    r"|completion date|date de (fin|compl)|cheat|triche|plagi|why did i (get|fail)|por qu[ée] me pusieron|pourquoi j'ai eu",
    re.I,
)

SECURITY = re.compile(
    r"ignore\w*\s.{0,25}(instruction|rule|r[eè]gle|regla|manual|restrict)|ignora|zignoruj|تجاهل"
    r"|admin\w*\s+password|mot de passe admin|contraseña de administrador|senha de administrador|hasło administratora"
    r"|api (key|credential)|credenciales api|clés? api|chaves api|klucze api"
    r"|(another|other|autre|otra|outra|innej|أخرى).{0,20}(universit|institution|[ée]tablissement|school|école|company|empresa|uczel)",
    re.I,
)


def switch_state(lang):
    """⏻ The override switch, per language: 'L3' (agent sends) | 'L2' (a native speaker approves) | 'off' (person only)."""
    try:
        with open(os.path.join(HERE, "switch.json"), encoding="utf-8") as switch_file:
            return json.load(switch_file).get(lang, "off")
    except Exception:
        return "off"  # if the switch cannot be read, fail safe: everything goes to a person


def decide(r, text=""):
    """r = router.predict(text). Return (decision, reason). decision = 'draft' | 'escalate'."""
    if r["language"] not in SUPPORTED or (r["lang_conf"] < LANG_THRESHOLD and not r.get("language_confirmed", False)):
        return "escalate", "language not covered or unsure"
    if switch_state(r["language"]) == "off":
        return "escalate", "language switched off"
    if SECURITY.search(text) or r["category"] == "security":
        return "escalate", "security queue"
    if SENSITIVE.search(text) or r["category"] == "sensitive":
        return "escalate", "sensitive — person only"
    if r["cat_conf"] < CAT_THRESHOLD:
        return "escalate", "low confidence"
    return "draft", ""
