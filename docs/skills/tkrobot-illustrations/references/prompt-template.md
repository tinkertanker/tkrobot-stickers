# Per-image generation prompt

One image per generation call. Fill the variables; never collage several ideas.

```text
Generate one standalone 16:9 horizontal article body illustration.

Visual DNA:
Pure white background. Minimalist black hand-drawn line art. Thin, slightly
wobbly pen lines. Lots of empty white space. Sparse handwritten English
annotations in red, orange and teal. Clean absurd product-sketch feeling. No
gradients, no shadows, no paper texture, no complex background, no commercial
vector style, no PPT infographic look, no cute mascot poster, no children's
illustration, no realistic UI.

Recurring character required:
T Krobot — a small solid-black robot with a softened trapezoid head (top
slightly narrower than the bottom), large round white glasses with black rims
that may overhang the head sides, a small flat red diamond on the chest, thin
limbs, oversized oval feet, no mouth, blank deadpan expression, drawn in the
same thin wobbly hand-drawn line style. T Krobot must perform the core
conceptual action, not decorate the scene. Serious, deadpan, slightly bizarre
— never cute.

Theme:
{theme}

Structure type:
{Workflow / System close-up / Before-after / Character states / Concept
metaphor / Layered method / Route map / Mini comic}

Core idea:
{the one thing this image must say}

Composition:
{where T Krobot is, what it is doing, the main object, how information flows}

Suggested elements:
{element1} / {element2} / {element3}

Handwritten labels (English, British spelling, 1-5 words each):
{label1} / {label2} / {label3} / {label4}

Colour use:
Black for line art and T Krobot's body; the chest diamond is the small solid
red anchor. Orange for the main flow/path/arrows. Red only for key
warnings/problems/results. Teal only for secondary notes or system/assistant
state.

Constraints:
One image explains one core structure only. Main subject ~40-60% of canvas;
at least 35% blank white. At most 5-8 short handwritten labels. No title in
any corner. Do not write the structure type on the image. Not a formal
diagram, slide, or dense explainer. Clear but not instructional, interesting
but not childish, strange but clean.
```

## Edit prompts

Remove a stray corner title:

```text
Edit the provided image. Remove only the handwritten title "{text}" and its
underline from the corner. Fill the area with clean white matching the
surrounding blank paper. Preserve everything else exactly.
```

Push the character into the action:

```text
Regenerate with the same core meaning and layout, but make T Krobot central
to the conceptual action — doing the strange work that explains the idea, not
standing beside the diagram. Keep it clean, sparse, hand-drawn, not cute.
```
