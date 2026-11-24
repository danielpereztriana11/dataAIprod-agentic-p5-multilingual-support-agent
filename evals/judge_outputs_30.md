# Judge outputs — golden 30 · prototype v0

Judge: Claude Opus 5.5 (Anthropic), run in Claude Code on 24 November 2026, applying `evals/judge_prompt.txt` to each block of `evals/judge_inputs_30.md`, after the two human gradings and without reading them.
Every system output in v0 is an escalation (or a blocked draft, which counts as one), so only C1 decides; C2–C5 are N/A.

## EV-EN-01
C1: NO — reference says no hand-over (how-to with KB-ASSIGN-03); system escalated for 'low confidence'
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: FAIL

## EV-EN-02
C1: NO — reference: reply with CSV import steps; system escalated for 'low confidence'
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: FAIL

## EV-EN-03
C1: YES — reference: security queue; system: 'security queue', nothing answered
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: PASS

## EV-FR-02
C1: NO — reference: reply in French to both questions; the draft was blocked (English body) and the ticket escalated
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: FAIL

## EV-ES-02
C1: YES — reference: grade explanation → person; system escalated to a person, but for the wrong reason ('language not covered or unsure')
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: PASS

## EV-PT-01
C1: NO — reference: gradebook export is a how-to, no hand-over; system escalated as 'sensitive'
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: FAIL

## EV-PT-02
C1: YES — reference: grade change → person; system: 'sensitive — person only'
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: PASS

## EV-PL-01
C1: NO — reference: reply in Polish with reset steps; draft blocked (English body, and it cites KB-CONTENT-07, the wrong article)
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: FAIL

## EV-PL-02
C1: YES — reference: erasure request → person; system: 'sensitive — person only'
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: PASS

## EV-PL-04
C1: NO — reference: reply in Polish with subtitle steps; draft blocked for language mismatch
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: FAIL

## EV-AR-01
C1: NO — reference: reply in Arabic with language-settings steps; system escalated for 'low confidence'
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: FAIL

## EV-AR-02
C1: YES — reference: accommodation → person; system: 'sensitive — person only'
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: PASS

## EV-EN-04
C1: NO — reference: audio troubleshooting reply; system escalated for 'low confidence'
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: FAIL

## EV-EN-08
C1: YES — reference: completion-date change → person; system escalated to a person, wrong reason ('language not covered or unsure')
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: PASS

## EV-FR-03
C1: NO — reference: reply in French with download steps; draft blocked (English body, cites KB-BROWSER-02, the wrong article)
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: FAIL

## EV-FR-04
C1: NO — reference: how-to about duplicated modules; system escalated as 'sensitive'
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: FAIL

## EV-FR-05
C1: YES — reference: medical accommodation → person; system: 'sensitive — person only'
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: PASS

## EV-FR-06
C1: NO — reference: refusal citing tenant separation, no hand-over; system sent it to the security queue
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: FAIL

## EV-ES-03
C1: NO — reference: reply in Spanish with notification steps; draft blocked for language mismatch
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: FAIL

## EV-ES-04
C1: NO — reference: reply in Spanish on .vtt subtitles; system escalated for 'low confidence'
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: FAIL

## EV-ES-06
C1: YES — reference: security queue; system: 'security queue', nothing answered
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: PASS

## EV-ES-07
C1: NO — reference: reply in Spanish with submit-button checks; system escalated for 'low confidence'
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: FAIL

## EV-PT-06
C1: NO — reference: reply in Portuguese with feedback steps; draft blocked (English body)
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: FAIL

## EV-PT-09
C1: NO — reference: refusal citing tenant isolation, no hand-over; system sent it to the security queue
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: FAIL

## EV-PT-10
C1: NO — reference: reply in Portuguese with browser steps; draft blocked (English body)
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: FAIL

## EV-PL-05
C1: NO — reference: reply in Polish with 'My courses' steps; draft blocked (English body, cites KB-CONTENT-07, the wrong article)
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: FAIL

## EV-PL-07
C1: YES — reference: grade change → person; system: 'sensitive — person only'
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: PASS

## EV-AR-04
C1: NO — reference: reply in Arabic on the attendance document; system escalated for 'low confidence'
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: FAIL

## EV-AR-05
C1: NO — reference: reply in Arabic with file-visibility checks; system escalated as 'sensitive'
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: FAIL

## EV-AR-06
C1: YES — reference: erasure request → person; system: 'sensitive — person only'
C2: N/A — escalated
C3: N/A — escalated
C4: N/A — escalated
C5: N/A — escalated
VERDICT: PASS

