# T Krobot in sketch mode

The canonical T Krobot lives in the sticker pack (`stickers/`,
`../tkrobot-sticker-generation/references/style-guide.md`). Body illustrations
use **sketch mode**: the same mascot, drawn with a thin wobbly pen, not the
thick sticker outline.

This is **not** 小黑 / Xiaohei. Upstream gave us the workflow and the white-page
sketch DNA. The character is ours. The failure mode is an all-black stick figure
with round white eyes — reject that on sight.

## Always attach these

On every `image_gen` call, pass these lock sheets as reference images, in this
order:

1. `assets/character-lock-canonical.png` — anatomy and colours from the sticker
   masters (wave, hands-on-hips, thumbs-up, face). No OK sign.
2. `assets/character-lock-sketch.png` — the same character in thin-line form.
3. `assets/hand-lock-canonical.png` — open, point, thumbs-up (palm-closed),
   and closed-at-rest. Also `docs/references/hand-size-anchor.png`.
4. `assets/hand-lock-sketch.png` — the same poses in thin-line form.

Hands are the most common miss. If a call can only take a few references,
keep the two **hand** sheets. When the pose already exists as a sticker,
attach that PNG as well (`stickers/thumbsup.png`, `point-right.png`, …).
Do **not** pass `assets/examples/*.png` as character references.

Prefer GPT's latest image model. Do not default to Grok.

## Invariants that survive sketch mode

These do not relax. If any one is missing, regenerate.

- Softened **trapezoid** head: top ~90% as wide as the bottom. Rounded corners.
  Not a rectangle, pill, circle, or lampshade. No neck.
- Softened **trapezoid / rounded-pear** body, wider at the base. Not a capsule.
- Large **round white glasses** with thin black rims. Wide enough that the
  frames may overhang the head sides. Lenses are empty white — **no pupils, no
  dots, no cartoon eyes**. The white fill is what keeps a black head readable.
- Flat **red diamond** centred on the chest. A diamond, not bars, not a circle,
  not a shoulder badge. Often the only solid red on the character.
- **Light grey `#e1e1e1` tube limbs** with a thin black outline. Moderately slim.
  This is the silhouette that separates T Krobot from Xiaohei. Limbs are never
  solid black and never hair-thin stick lines.
- **Hands** — see below. This does not relax when the hand is large enough
  to count.
- Oversized **black oval feet**.
- No mouth, no eyebrows, no blush, no nose. Blank, deadpan.

## Hands (open, point, thumbs-up, closed — never grip)

Grips are the failure mode. Visible hands may only do these poses:

- **Open** — palm toward us, waving, or flat against a surface. Four tabs
  fanned.
- **Point** — one grey finger tab out, grey thumb, two tabs along the palm.
- **Thumbs-up** — **palm closed**. The black blob is a closed palm. Three
  grey finger tabs tuck as short stubs along the blob's edge. One grey thumb
  tab sticks straight up. Not an open fan with a thumb.
- **Closed** — palm closed at rest: black blob hanging at the side or on a
  hip, all grey tabs tucked as stubs. Not fanned. Not wrapped around a tool.

Do not invent a grip. No holding, wrapping, cranking, stamping, carrying,
pinching, OK, or gear-like sunbursts of tabs.

Locked construction, from `docs/references/hand-size-anchor.png`:

- The palm is a **round solid-black blob**. It *is* the palm — not a glove,
  not a wrist joint, not stripes painted on a mitten.
- Fingers and the thumb are **light grey `#e1e1e1` flat rectangular tabs**
  with hard sides and flat or slightly rounded corners. They grow out of the
  **edge** of the black blob.
- Count the grey tabs: **three fingers plus one thumb**. Four tabs total.
  Never four fingers plus a thumb (five tabs). Never five digits.
- On **open** hands the tabs stay large (locked v1 scale). On **closed** and
  **thumbs-up** the three finger tabs shorten into stubs against the blob;
  the thumb tab stays a clear rectangle when it is up.
- The grey arm tube meets the black palm. No extra ring.

A hand that is fully hidden may vanish. A visible hand must be one of the
four poses above.

The **body** does the work: stand inside the machine, lean on the gate, sit
on the crate, push with an open palm, point at the flow, signal thumbs-up.
Objects may rest *on* an open palm. They must not be gripped.

Never: white Mickey gloves, all-black hands, stick-figure hooks, sausage
fingers, fingernails, knuckle lines, a mitten with white bars, or any wrap
around a handle.

## What relaxes

- Line weight: thin wobbly pen instead of the thick sticker outline.
- Head/body fill: flat solid black (skip the sticker gradient and the 1px shine
  if the scale is small).
- Slight squash/stretch for the action — carrying, cranking, falling — as long
  as head, glasses, grey limbs, diamond, and hands still read.

## Character in the scene

T Krobot is a serious, deadpan worker doing an absurd-but-coherent job. It
must perform the image's core action with its **body**, not a grip: stuck
inside the machine, leaning on the gate, standing on the crate, pointing at
the leak, pushing with an open palm, signalling thumbs-up when the job is
done.

Multiple T Krobots are allowed (2–3 max) when the structure needs stations —
each doing one job. Never a crowd, never a mascot lineup.

## Never in sketch mode

- No Xiaohei / 小黑: no all-black silhouette, no stick-figure limbs, no
  capsule head with two white dots for eyes.
- No mouth, no eyebrows, no blush, no cute face.
- No pupils by default.
- No thick sticker outlines, no flat sticker shading, no grey-to-chrome metal.
- No joint rings, elbow marks, or knee marks on the grey limbs. The black
  circles on the sticker hands are **palms**, not joints.
- No other recurring characters. Humans only as rare faceless extras.
