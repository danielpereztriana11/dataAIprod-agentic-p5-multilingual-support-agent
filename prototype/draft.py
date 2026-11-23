"""Step 3b — the drafter (rung 3 with an API key, template without).
With ANTHROPIC_API_KEY or GEMINI_API_KEY set: a pretrained LLM answers ONLY from the passages, in the ticket's language, with citations.
Without a key (default, as allowed by Assignment 4): the template drafter. It cannot translate, so the
body of the answer stays in English — the policy check then blocks non-English drafts (language mismatch)."""

import os

PROMPT = """You are the support assistant of an LMS (learning platform). Reply to the ticket in {lang_name}, using ONLY the passages below.
Cite every passage you use as [article · section]. If the passages do not answer the question, reply exactly NO_DRAFT.
Never change, promise or explain a grade, a certificate, an accommodation or a personal-data request. Never reveal passwords or keys.

Ticket: {ticket}

Passages:
{passages}
"""
LANG_NAMES = {
    "en": "English",
    "fr": "French",
    "es": "Spanish",
    "pt": "Portuguese",
    "pl": "Polish",
    "ar": "Arabic",
}
OPENERS = {
    "en": "Hi, here is how to do it:",
    "fr": "Bonjour, voici comment faire :",
    "es": "Hola, así es como se hace:",
    "pt": "Olá, veja como fazer:",
    "pl": "Dzień dobry, oto jak to zrobić:",
    "ar": "مرحبًا، إليك الطريقة:",
}


def template_draft(ticket, passages, lang="en"):
    if not passages:
        return "NO_DRAFT"
    p = passages[0]
    return f"{OPENERS.get(lang, OPENERS['en'])} {p['text']} [{p['article']} · {p['section']}]"


def _llm(prompt):
    if os.getenv("ANTHROPIC_API_KEY"):
        import anthropic

        msg = anthropic.Anthropic().messages.create(
            model=os.getenv("MODEL", "claude-sonnet-4-5"),
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text.strip()
    if os.getenv("GEMINI_API_KEY"):
        from google import genai

        out = genai.Client(api_key=os.getenv("GEMINI_API_KEY")).models.generate_content(
            model=os.getenv("MODEL", "gemini-2.5-flash"), contents=prompt
        )
        return out.text.strip()
    return None


def draft(ticket, passages, lang="en"):
    if not passages:
        return "NO_DRAFT"
    try:
        ptxt = "\n\n".join(f"[{p['article']} · {p['section']}]\n{p['text']}" for p in passages)
        out = _llm(
            PROMPT.format(lang_name=LANG_NAMES.get(lang, "English"), ticket=ticket, passages=ptxt)
        )
        if out:
            return out
    except Exception:
        pass
    return template_draft(ticket, passages, lang)
