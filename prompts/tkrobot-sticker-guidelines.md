# T Krobot Sticker Prompt Guidelines

Use these rules whenever generating or editing T Krobot stickers.

## Non-negotiable Character Invariants

- Black rounded pill-shaped head and black oval torso.
- Large round white glasses with black rims.
- Smooth plain light grey tube arms and legs, around `#ccc`; arms and legs should be about 20% skinnier than the current v8 candidates, and legs may be about 5% longer than the originals.
- Hands use a round black palm blob with light grey `#ccc` fingers and thumbs emerging from the blob's edge. The black part is the palm itself, not a glove wrapped around the fingers. Each hand has one longer thumb and three longer rounded fingers.
- Oversized black oval feet.
- Flat red diamond chest mark, centred on the torso; no gem facets.
- No neck.
- No mouth, smile, open mouth, teeth, tongue, or face hole.
- No joints, segment rings, elbow marks, knee marks, bend lines, or black interior lines on white arms or legs.
- No pupils by default. Use plain white glasses for normal expressions.
- Pupils are allowed only for special looks where they are part of the concept, such as charging or happy, and must stay inside the white glasses.

## Style

Match the original sticker library: clean 2D cartoon, thick black outlines, simple flat shapes, light highlights only, expressive motion marks, transparent background final output.

Use a subtle near-black-to-black gradient on the head and body so the head/torso boundary is easier to read. Keep it recognisably black, not grey. Add a very thin 1px-style light grey shine/border along the bottom edge of the head to separate it from the body. Use only a few emanata/motion marks; do not surround the character with lots of symbols.

Avoid 3D renders, metallic robot details, complex fingers, extra props unless requested, captions, watermarks, and green elements when using chroma key.

## Prompt Skeleton

```text
Use case: stylized-concept
Asset type: T Krobot transparent chat sticker candidate, square PNG
Primary request: Create a T Krobot sticker for "<slug>" on a perfectly flat solid #00ff00 chroma-key background for background removal.
Subject: T Krobot, Tinkertanker company mascot: black rounded robot with a pill-shaped black head and black oval torso using a subtle near-black-to-black gradient, plus a very thin 1px-style light grey shine line along the bottom edge of the head; large round white glasses with black rims; smooth plain light grey tube arms and smooth plain light grey tube legs around #ccc, about 20% skinnier than v8; hands with round black palm blobs plus light grey #ccc thumbs and fingers emerging from the blob edges; oversized black oval feet; flat red diamond chest mark; no neck.
Critical character invariants: NO mouth. NO neck. NO joints. NO segment lines. NO black lines across arms or legs. Light grey limbs must be completely plain continuous skinny shapes with only an outer black outline. Palms must be round black blobs that fingers emerge from, not gloves wrapped around the fingers; fingers and thumbs must be light grey #ccc, longer, not stubby black bits. Centre diamond must be flat red, not faceted. NO pupils by default; only use pupils for special looks such as charging or happy.
Style/medium: clean polished 2D cartoon sticker matching original T Krobot stickers; thick outer black outlines, simple flat shapes with subtle highlight only, not 3D, no metallic detail.
Composition/framing: centred character, generous padding, no cropping. <pose and expression details>
Chroma key: one perfectly uniform #00ff00 background, no shadows, gradients, texture, floor, or reflection. Do not use #00ff00 in the subject.
Avoid: mouth, internal limb lines, segmented limbs, rings on limbs, captions, watermark, extra characters.
```

## Current Notes

- `gasp`: express surprise through hands on cheeks, widened blank glasses, and orange exclamation marks.
- `salute`: both arms must be present; one hand salutes, the other rests clearly at the side or hip.
- `yay`: keep the body upright; use raised arms and a few celebratory marks rather than a mouth. Happy/celebration may use upside-down-U pupils inside the glasses.
- `snooze`: lightning may appear as sleepy lens highlights, not on the black face.
- `shock`: make the reaction readable through recoil, blank widened glasses, and burst marks; avoid drawing pupils or limb bend lines.
