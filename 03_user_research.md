# 03 — User research · P5 Multilingual LMS support agent

> Before Session 4. Three conversations (20 min each) + one usability test of your prototype with two of them.
> Mom Test rules (Rob Fitzpatrick): ask about past behaviour, not opinions; never pitch; never ask “would you use…?”.
> If you cannot reach real users, classmates can play the role — say so in the table.

## Who we talked to
| # | Who (role, company type — no personal data) | Real user or classmate in role? | Date | Interviewer · note-taker |
|---|---|---|---|---|
| 1 | Student at a French school, Arabic speaker (Moroccan Darija), using the school's course platform in French | Real user | 23 Nov 2026 | [Oussama] · [daniel] |
| 2 | Former international student at a French public university (non-native French speaker, fluent in English); university systems and course platform in French only | Real user | 23 Nov 2026 | [Daniel] · [come] |
| 3 | French student on exchange at a South Korean university, using the university's online course platform (interface and help in Korean only) | Real user | 23 Nov 2026 | [come] · [oussama] |

## Interview guide (adapt it — keep it about the past)
1. Tell me about the last time you got stuck on your school's course platform. What happened, step by step?
2. How did you find help? In which language? How long did it take?
3. What annoyed you the most? If you could change one thing in that moment, what would it be?
*Avoid:* “Would you use an AI that…?” · “Do you like this idea?” · “How much would you pay?”

## What we heard (facts, in their words)
| # | Quote or observed behaviour | Which part of our brief it confirms or contradicts |
|---|---|---|
| 1 | Last time he was blocked on the school platform while submitting an assignment: the page would not load and he could not log in. | Confirms a frequent ticket type (login / page not loading near a deadline), close to eval cases EV-PL-01 and EV-PT-05; the agent cannot fix an outage, it must give the cited steps and hand off fast |
| 1 | He asked a Moroccan classmate on WhatsApp, in French and a bit of Darija, and got help in about 15 minutes. | Confirms users go around official support to someone who speaks their language — the job our agent competes with. Contradicts an assumption: users may write in a dialect (Darija) or mix languages, not standard Arabic — gap to add to governance.md "known gaps by segment" |
| 1 | What annoyed him most: "the lack of responsiveness of the support" and the stress of not submitting on time. | Confirms the wait is the pain (PT/PL/AR wait 2–3× longer); a deadline makes a slow answer costly — the hand-off for a blocked submission must be prioritised |
| 2 | All university systems were in French only; he needed to know if he could be exempted from a mandatory English course, but "the options were not clear and the information was very incomplete". | Confirms §1: information exists in one language only, and is incomplete — a KB coverage gap, not only a translation gap (data audit, question 3 "coverage") |
| 2 | To get an answer he had to go in person to a university office; the language-centre staff did not speak English well. | Confirms the way back must lead to a person who speaks the user's language (native-speaker hand-off), not just "a human" |
| 2 | He took the course anyway and found out later he was not obliged to — "I lost my time for nothing". | Confirms the cost of no answer or a wrong answer is high for the user, not only for support (§2, cost of an error) |
| 2 | His question (exemption from a mandatory course) is an academic decision, not a "how do I" question. | Confirms the governance line: the agent can explain the procedure from a cited article, but the decision stays with a person — hand-off (EU AI Act Annex III, governance.md row 4) |
| 3 | The whole course platform was in Korean: he could not search it with Ctrl+F because he could not read or type the words he was looking for. | Confirms §1: the help exists, but in a language the user cannot read — the core problem of P5 |
| 3 | He copy-pasted the site into a translation website section by section — "complicated", and still not enough to find the setting. | Confirms pain step 4 (translate / adapt): machine translation of whole pages is not an answer (§5, "why the rung below fails") |
| 3 | He could not solve it alone and waited several days to ask a native speaker how to change the language. | Confirms the wait for native speakers and the value of a native-speaker hand-off; "how do I change the interface language" is a routine case (EV-AR-01) |
| 3 | The language he needed (Korean) is outside our 6 supported languages. | Confirms the WON'T "languages beyond the 6" and the edge case "language not covered → hand-off": the way back must not mean waiting days |

## Usability test — one task, think aloud, don't help
**Prototype link:** see `03_prototype_link.md` · **Task given:** "You want to export your class's grades to Excel. Ask the help chat in your own language, and find where the answer comes from."
| Tester | Finished without help? (yes / no) | Where they hesitated | What they expected instead |
|---|---|---|---|
| A (prototype v0.1) | No | Did not understand why there were two pages ("Learner help chat" and "Agent console"); found the site too complex. Asking in Portuguese gave "Being checked", not the answer. | One simple help chat with the answer; would never have thought of switching Portuguese from L2 to L3 in the console to get it. |
| B (prototype v0.1) | No | Same: two pages not understood, site "a bit too complex"; stuck on the Portuguese "Being checked" message. | Same: expected the answer in the chat; the L2/L3 switch meant nothing to them. |

## Desirability gate — do they want it?
- [ ] 4 of 5 (or 2 of 2 in this homework) finished the task without help — **0 of 2** on v0.1
- [x] They told us what they did last time — not what they would do
- [ ] At least one said “I want this before…”
- [x] Our out-of-scope list grew; our success criterion did not move — Korean and dialects confirmed out of scope; the 57 % criterion unchanged

**Decision:** back to the brief, then Session 4 build — because 0 of 2 testers finished the task on v0.1: the learner must see one simple chat, the agent console is a staff tool and must be separate, and an L2 answer must say clearly when it will arrive.
