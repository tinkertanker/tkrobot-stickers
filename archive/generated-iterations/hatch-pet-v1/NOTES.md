# T Krobot Hatch Pet sticker candidates

These concepts were recovered from the validated T Krobot Codex Hatch Pet v2 atlas created in Codex task `019f7d68-62de-7780-a3e1-a2e2c7de82e1` on 20 July 2026, then redrawn at full sticker resolution with Imagegen.

## Contents

- `pet-sources/` contains the exact transparent `192 x 208` cells cropped from the final `1536 x 2288` Hatch Pet atlas. They are composition references only and retain the pet pipeline's edge artefacts.
- Built-in Imagegen source renders were used locally to produce the redraws, but are intentionally excluded from the repository because flattened chroma exports are not pack artefacts.
- `stickers/` contains the clean square `1254 x 1254` transparent PNG redraws.
- `contact-sheet.png` previews the eight regenerated candidates.

Several of these concepts were promoted into the definitive pack in `stickers/` (`sus`, `running-left`, `running-right`, `palm-open`, `rubbing-tummy`, `failed-sitting`, `jumping-for-joy`, `happy`). Treat this folder as provenance and composition reference for those pack entries, not as a second working set.

## Historical shortlist (now mostly promoted)

| Priority | Proposed slug | Candidate | Outcome |
| --- | --- | --- | --- |
| 1 | `sus` | `sus.png` | Promoted into `stickers/sus.png`. |
| 2 | `on-my-way` | `running-right.png` | Promoted as `running-right` (with `running-left` pair). |
| 3 | `palm-open` | `palm-open.png` | Promoted into `stickers/palm-open.png`. |
| 4 | `rubbing-tummy` | `rubbing-tummy.png` | Promoted into `stickers/rubbing-tummy.png`. |
| 5 | `wiped-out` | `failed-sitting.png` | Promoted as `failed-sitting`. |

`jumping-for-joy.png` and `happy.png` were also promoted despite some overlap with `yay.png`. Both deliberately reuse the same upside-down-U happy eyes. The waving frame was reviewed but not retained because it overlaps `greetings.png`.

## Selected atlas pose references

| Candidate | Atlas row | Cell | Hatch Pet state |
| --- | ---: | ---: | --- |
| `happy.png` | 0 | 2 | idle |
| `running-right.png` | 1 | 3 | running-right |
| `running-left.png` | 2 | 3 | running-left |
| `jumping-for-joy.png` | 4 | 1 | jumping |
| `failed-sitting.png` | 5 | 4 | failed |
| `palm-open.png` | 6 | 0 | waiting |
| `rubbing-tummy.png` | 7 | 0 | running/processing |
| `sus.png` | 8 | 1 | review |

## Regeneration and edge-quality note

The installed atlas is lossless WebP, but the pet pipeline starts from chroma-keyed `192 x 208` cells. The pre-despill frames have a green fringe; despill converts it into the grey/dotted edge that became conspicuous when enlarged roughly 5.5 times. This is a Hatch Pet source-resolution and chroma-cleanup artefact, not JPEG/WebP compression.

The retained concepts were therefore redrawn from scratch at `1254 x 1254` by built-in Imagegen. Each pet cell supplied pose only; approved definitive stickers supplied style, proportions, glasses and hand construction. `jumping-for-joy.png` and `rubbing-tummy.png` received targeted Imagegen edits to match the happy-eye treatment from `happy.png`. `running-right.png` is a deterministic horizontal mirror of the approved `running-left.png` redraw because the character has no asymmetric prop, text, pupil or lighting cue in this pose.

The new transparent PNGs pass these checks:

- square `1254 x 1254` RGBA files with transparent corners
- no green-dominant non-transparent pixels after background removal
- clean silhouettes on a contrasting pink-background visual review
- no mouths, default pupils, necks, limb joints, internal limb lines, captions, props or shadows
- exactly three large rectangular fingers plus one thumb on each visible hand
