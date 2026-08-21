# Per-image generation prompt

One image per generation call. Fill the variables; never collage several ideas.

Attach these lock sheets as reference images on the same call
(`reference_image_paths` or the equivalent), in this order:

1. `docs/skills/tkrobot-illustrations/assets/character-lock-canonical.png`
2. `docs/skills/tkrobot-illustrations/assets/character-lock-sketch.png`
3. `docs/skills/tkrobot-illustrations/assets/hand-lock-canonical.png`
4. `docs/skills/tkrobot-illustrations/assets/hand-lock-sketch.png`

Copy T Krobot — and especially the hands — from those sheets. Do not invent
a black stick-figure or cartoon gloves. If the tool only accepts a few
references, keep the two hand sheets.

```text
Generate one standalone 16:9 horizontal article body illustration.

Visual DNA:
Pure white background. Minimalist black hand-drawn line art. Thin, slightly
wobbly pen lines. Lots of empty white space. Sparse handwritten English
annotations in red, orange and teal. Clean absurd product-sketch feeling. No
gradients, no shadows, no paper texture, no complex background, no commercial
vector style, no PPT infographic look, no cute mascot poster, no children's
illustration, no realistic UI.

Recurring character — copy the attached lock sheets:
T Krobot, the Tinkertanker mascot. Same character in every pose.

MUST match the lock sheets:
- Head: solid black softened trapezoid, top ~90% as wide as the bottom, rounded
  corners, no neck.
- Body: solid black softened trapezoid / rounded pear, wider at the base.
- Glasses: two large perfectly round empty-white lenses, thin black rims, short
  bridge. Frames may overhang the head sides. No pupils, no dots inside.
- Chest: one small flat red diamond in the centre of the torso — a diamond, not
  bars, not on the shoulder.
- Arms and legs: light grey (#e1e1e1) smooth tubes with a thin black outline.
  Moderately slim. NEVER solid black. NEVER hair-thin stick lines. No joints.
- Hands (copy the hand-lock sheets): each visible hand is a ROUND SOLID BLACK
  PALM BLOB with exactly FOUR light-grey rectangular tabs growing from its
  edge — three fingers in a row plus one thumb set apart. Tabs are LARGE flat
  rectangles with hard sides.
  Allowed poses only:
  OPEN — four tabs fanned, palm toward us, waving, or flat on a surface.
  POINT — one grey finger tab out, grey thumb, two tabs along the palm.
  THUMBS-UP — palm CLOSED: black blob as a closed palm, three grey finger
  tabs tucked as short stubs on the blob, one grey thumb tab straight up.
  CLOSED — palm closed at rest: black blob at the side or on a hip, all
  grey tabs tucked as stubs, not fanned.
  Never grip, hold, wrap, crank, stamp, carry, pinch, or OK. If a hand is
  curled around an object, redraw — push, lean, stand in, point, or
  thumbs-up instead.
- Feet: oversized solid black ovals.
- No mouth, no eyebrows, no blush. Deadpan.

T Krobot must perform the core conceptual action, not decorate the scene.
Serious, slightly bizarre — never cute.

NOT this character:
Xiaohei / 小黑 / an all-black stick figure with two white circles for eyes.
If the limbs are black, it is the wrong robot. Redraw.

Theme:
{theme}

Structure type:
{Workflow / System close-up / Before-after / Character states / Concept
metaphor / Layered method / Route map / Mini comic}

Core idea:
{the one thing this image must say}

Composition:
{where T Krobot is, the body action — not a grip — the main object, how
information flows. Hands: open, point, thumbs-up (palm-closed), or closed.}

Suggested elements:
{element1} / {element2} / {element3}

Handwritten labels (English, British spelling, 1-5 words each):
{label1} / {label2} / {label3} / {label4}

Colour use:
Black for line art and T Krobot's head/body; limbs stay light grey. The chest
diamond is the small solid red anchor. Orange for the main flow/path/arrows.
Red only for key warnings/problems/results. Teal only for secondary notes or
system/assistant state.

Constraints:
One image explains one core structure only. Main subject ~40-60% of canvas;
at least 35% blank white. At most 5-8 short handwritten labels. No title in
any corner. Do not write the structure type on the image. Not a formal
diagram, slide, or dense explainer. Clear but not instructional, interesting
but not childish, strange but clean. No extra type on props (no "STAMPED",
no "WEEKLY BRIEFING" headings). Hands: open, point, thumbs-up (palm-closed),
or closed at rest — no grips.
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
Keep T Krobot on-model: grey tube limbs, trapezoid black head and body, empty
round white glasses, red chest diamond, black palm blobs with four large
grey rectangular tabs. Hands: open, point, thumbs-up (palm-closed), or
closed at rest — no gripping. Not an all-black stick figure. Not cartoon
gloves.
```

Fix an off-model T Krobot (keep the scene):

```text
Edit the provided image. Replace every robot with T Krobot from the attached
character lock sheets: black softened-trapezoid head and body, large empty
round white glasses, flat red diamond centred on the chest, light grey tube
limbs with thin black outlines, black oval feet, no mouth, no pupils. Do not
turn the limbs black. Do not turn the head into a pill. Preserve the scene,
labels, and layout.
```

Fix the hands only (keep the rest):

```text
Edit the provided image. Fix only T Krobot's hands to match the attached
hand-lock sheets. Each visible hand: a round solid-black palm blob, with
exactly three light-grey rectangular finger tabs plus one grey thumb tab
growing from the blob's edge. Large flat tabs, hard sides. Each hand is
OPEN, POINTING, THUMBS-UP (palm-closed), or CLOSED at rest. If it is
wrapped around a handle, uncurl it and move the object so it is not
being held. Thumbs-up must keep the palm closed (tucked stubs + thumb
up), not an open fan. Not
white gloves, not five digits, not sausages, not all-black fists, not
striped mittens. Leave the head, body, scene, and labels untouched.
```
