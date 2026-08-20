# T Krobot in sketch mode

The canonical T Krobot lives in the sticker pack (`stickers/`,
`../tkrobot-sticker-generation/references/style-guide.md`). Body illustrations
use **sketch mode**: the same mascot, drawn with a thin wobbly pen, not the
thick sticker outline.

This is **not** 小黑 / Xiaohei. Upstream gave us the workflow and the white-page
sketch DNA. The character is ours. The failure mode is an all-black stick figure
with round white eyes — reject that on sight.

## Always attach these

On every `image_gen` call, pass both lock sheets as reference images, in this
order:

1. `assets/character-lock-canonical.png` — anatomy and colours from the sticker
   masters (wave, hands-on-hips, OK, face).
2. `assets/character-lock-sketch.png` — the same character in thin-line sketch
   form.

Do **not** pass `assets/examples/*.png` as character references. Those files
calibrate page density only; older ones may still look like Xiaohei.

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
- Hands: round **black palm blobs**; fingers read as short light-grey tabs or a
  mitten at small sizes. Exact three-fingers-plus-thumb relaxes when the
  character is tiny.
- Oversized **black oval feet**.
- No mouth, no eyebrows, no blush, no nose. Blank, deadpan.

## What relaxes

- Line weight: thin wobbly pen instead of the thick sticker outline.
- Head/body fill: flat solid black (skip the sticker gradient and the 1px shine
  if the scale is small).
- Slight squash/stretch for the action — carrying, cranking, falling — as long
  as head, glasses, grey limbs, and diamond still read.

## Character in the scene

T Krobot is a serious, deadpan worker doing an absurd-but-coherent job. It
must perform the image's core action: stuck inside the machine, pulling the
wrong cable, guarding the gate, hauling the crate, weighing the ideas,
patching the pipe, feeding pages into a strange device.

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
