---
name: tkrobot-illustrations
description: Generate T Krobot whimsical body-text illustrations — 16:9 white-background hand-drawn explainer images where T Krobot performs the core conceptual action. Use when asked to illustrate an article, tutorial, blog post, proposal, course page section, methodology, workflow, process, state, or metaphor; or when asked for "illustrations", "body images", "shot list", "explainer sketch", or "xiaohei-style" images for Tinkercademy/Tinkertanker content.
---

# T Krobot whimsical illustrations

## What this is

Turn a piece of writing's key judgement, process, structure, state, or metaphor
into a single 16:9 hand-drawn explanatory image. Not commercial illustration,
not PPT infographics, not cute mascot posters — a clean, whimsical,
product-sketch-feeling drawing where **T Krobot does the strange work that
explains the idea**.

T Krobot must participate in the core action — standing in the machine,
leaning on the gate, pointing at the break, pushing with an open palm.
Never standing beside the diagram as decoration. Hands stay **open or
pointing**; do not grip or hold objects (those poses collapse).

This is distinct from the sticker pack (transparent chat stickers) and from
banner composition (deterministic hero scenes). This skill produces editorial
body images for articles, tutorials, proposals, and course-page prose.

## Read before generating

Always read `references/tkrobot-sketch-mode.md` and look at the lock sheets
before the first `image_gen` call. T Krobot is the sticker mascot with **light
grey tube limbs** and **black palm + grey tab hands** that only **open or
point**. Not an all-black Xiaohei stick figure, not cartoon gloves, not a
grip.

- `assets/character-lock-canonical.png` — anatomy and colours.
- `assets/character-lock-sketch.png` — the same character in thin-line form.
- `assets/hand-lock-canonical.png` and `assets/hand-lock-sketch.png` — hands.
  Also `docs/references/hand-size-anchor.png`.
- `references/style-dna.md` — page DNA, colours, lettering, hard bans.
- `references/composition-patterns.md` — structure types, metaphor invention,
  no-recycling rule.
- `references/prompt-template.md` — the per-image generation prompt.
- `references/qa-checklist.md` — post-generation checks and edit prompts.

## Workflow

### 1. Digest the text

Read the article/tutorial/proposal. Extract: the core claim, the paragraphs
carrying a cognitive turn, which ideas deserve a picture, and which are fine as
prose. Do not illustrate evenly — pick the **cognitive anchors**: a key
judgement, a break in a pipeline, an input→output loop, a fork, a
before/after, a common trap, a state change.

### 2. Shot list first

If the user asks "how should we illustrate this", reply with a shot list, each
entry: placement (after which paragraph), theme, core idea, structure type,
what T Krobot is doing, suggested elements, suggested annotation words.
Default 3–6 images; short pieces 1–2. Enough is enough.

### 3. Generate one image at a time

If the user asks to generate, generate — one `image_gen` call per image, using
`references/prompt-template.md`. Attach the character lock sheets **and** the
hand lock sheets as `reference_image_paths` on that call. Never collage
multiple ideas into one image. Invent a fresh metaphor from *this* text each
time; never reuse a previous composition (see the no-recycling rule).

### 4. Check and iterate

Run `references/qa-checklist.md`. Check the character — then every visible
hand — against the lock sheets before anything else. Regenerate or edit if:
the robot drifted into Xiaohei (black stick limbs, pill head, dotted eyes);
hands drifted into gloves, five digits, sausages, grips, or black fists;
T Krobot is
mere decoration; the canvas is crowded; it reads as a flowchart or slide; the
annotations are long or numerous; a type-title appears in a corner; the style
went cute or went vector; the background isn't clean white.

### 5. Deliver

Save into the consuming project, e.g. `assets/<slug>-illustrations/01-topic.png`,
numbered in article order. Report: how many, where each goes, which are solid
and which optional. Let the images speak; skip style theory.

## Attribution

Adapted for T Krobot from [ian-xiaohei-illustrations](https://github.com/helloianneo/ian-xiaohei-illustrations)
by Ian Neo (MIT). See `NOTICE.md`.
