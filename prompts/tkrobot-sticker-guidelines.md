# T Krobot Sticker Prompt Guidelines

Use these rules whenever generating or editing T Krobot stickers.

## Non-negotiable Character Invariants

- Black rounded pill-shaped head and black oval torso.
- Large round white glasses with black rims.
- Smooth plain white tube arms and legs.
- Black mitten hands and oversized black oval feet.
- Red diamond chest mark, centred on the torso.
- No mouth, smile, open mouth, teeth, tongue, or face hole.
- No joints, segment rings, elbow marks, knee marks, bend lines, or black interior lines on white arms or legs.
- Pupils are allowed when useful, but keep them inside the white glasses.

## Style

Match the original sticker library: clean 2D cartoon, thick black outlines, simple flat shapes, light highlights only, expressive motion marks, transparent background final output.

Avoid 3D renders, metallic robot details, complex fingers, extra props unless requested, captions, watermarks, and green elements when using chroma key.

## Prompt Skeleton

```text
Use case: stylized-concept
Asset type: T Krobot transparent chat sticker candidate, square PNG
Primary request: Create a T Krobot sticker for "<slug>" on a perfectly flat solid #00ff00 chroma-key background for background removal.
Subject: T Krobot, Tinkertanker company mascot: black rounded robot with a pill-shaped black head, black oval torso, large round white glasses with black rims, smooth plain white tube arms and smooth plain white tube legs, black mitten hands, oversized black oval feet, red diamond chest mark.
Critical character invariants: NO mouth. NO joints. NO segment lines. NO black lines across arms or legs. White limbs must be completely plain continuous white shapes with only an outer black outline. Pupils are allowed inside the glasses if useful.
Style/medium: clean polished 2D cartoon sticker matching original T Krobot stickers; thick outer black outlines, simple flat shapes with subtle highlight only, not 3D, no metallic detail.
Composition/framing: centred character, generous padding, no cropping. <pose and expression details>
Chroma key: one perfectly uniform #00ff00 background, no shadows, gradients, texture, floor, or reflection. Do not use #00ff00 in the subject.
Avoid: mouth, internal limb lines, segmented limbs, rings on limbs, captions, watermark, extra characters.
```

## Current Notes

- `gasp`: express surprise through hands on cheeks, widened glasses/pupils, and orange exclamation marks.
- `salute`: both arms must be present; one hand salutes, the other rests clearly at the side or hip.
- `yay`: keep the body upright; use raised arms and celebratory marks rather than a mouth.
- `snooze`: lightning may appear as sleepy lens highlights, not on the black face.
- `shock`: make the reaction readable through recoil, pupils, and burst marks; avoid drawing limb bend lines.
