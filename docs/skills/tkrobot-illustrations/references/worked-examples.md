# Worked examples (course body, 2026-08)

Nine keepers from the first live run of this skill, against real
tinkercademy.com programme pages. Look at them after the lock sheets.
They show T Krobot *in a scene*, with object-only labels and a stolen
sticker pose.

Do **not** attach these as `reference_image_paths` on `image_gen` unless you
are editing that same file. Attaching them as style refs recycles the
furniture (the no-recycling rule). Attach the lock sheets and the matching
sticker PNG instead.

Files live at `archive/course-illustrations/<programme-slug>/`.

## What to steal

- One idea per frame. If you need a fourth point, it is a second image.
- T Krobot does the job with its body: pointing, open palm on a surface,
  hands on hips. Never a caption standing next to a diagram.
- Labels name objects or flow (`our files`, `still yours to check`). They
  do not cheer the pose.
- The interesting object is low-tech and slightly wrong: a card-catalogue,
  a weigh-station, a coat rack, a postbag. Not a laptop screenshot.
- GPT caller. Grok invented grips.

## What not to steal

Each metaphor below is spent. Same theme next time = new furniture.

Do not reuse: card-catalogue + citation string, farm gate + doorbell,
barrel-organ, trolley + weigh-station, coat-rack instructions, circular
garden path + off-path crate, overflowing postbag + pinboard, taped paper
shopfront, speaking-tube + market stall.

`assets/examples/` is still Xiaohei-era density calibration. Do not use
those files as the character.

## What failed in this run

- Labelling the robot as the result (`grounded answer` pointing at T
  Krobot). The answer has to be a thing in the scene.
- Leaving keepers only at `/opt/cursor/artifacts/…`. Chat cannot fetch
  that path later. Commit keepers here the same turn.
- Thumbs-up plus a slogan (`job done`). The sticker already says it.
- Grips: cranks, stamps, pencils, magnifying glasses. Change the pose.

## Shot list (as run)

Placement is the paragraph *after* which the image should sit on the
programme page.

### Knowledge-Powered AI

`knowledge-powered-ai-with-chatgpt/01-grounded-answer.png` — after the RAG
/ “your knowledge assets” paragraph. Concept metaphor. Pose: `point-right`.
A catalogue drawer, a string, a slip on a lectern. Labels: our files /
citation / grounded answer. The slip is the answer, not the robot.

### From Prompting to Pull Request

`from-prompting-to-pull-request/01-review-the-diff.png` — after the
overview. Workflow. Pose: `point-right`. Scraps → gate clipboard →
doorbell URL. Labels: prompt scraps / review the diff / live URL.

### Agentic Workflows

`agentic-workflows-for-businesses/01-weekly-loop.png` — after the weekly
loop claim. Workflow. Pose: `palm-open`, flat on the box, not on a crank.
Paper rings → self-turning barrel-organ → checklist. Labels: weekly loop /
the agent runs it / you still check.

### Agentic Engineering

Three anchors. Skip a fourth unless the page grows.

1. `…/01-direct-and-check.png` — after “direct that work and check the
   result”. Workflow. Pose: `point-right`. Brief → trolley of crates →
   weigh-station. Labels: the brief / agent drafts / still yours to check.
2. `…/02-kind-of-instruction.png` — after “Choose the right kind of
   instruction”. System close-up. Pose: `hands-on-hips`. Uneven coat-rack
   objects, not a 2×2 slide. Labels: standing instructions / a skill /
   a tool / one-off.
3. `…/03-inspectable-loop.png` — after “Build an agent loop you can
   inspect”. Concept metaphor. Pose: `palm-open` on the stop-gate. Circular
   path, crate *outside* the path, kitchen timer. Labels: the loop /
   memory stays outside / hard stop.

### Vibe Coding for Digital Builders

The three stations on the page.

1. `…/01-the-brief.png` — after ChatGPT / problem discovery. Before/after.
   Pose: `point-right`. Postbag → one pinned brief + silhouette. Labels:
   the mess / one brief / whose problem.
2. `…/02-paper-shopfront.png` — after Figma. Concept metaphor. Pose:
   `palm-open`. Taped paper facade. Labels: paper shopfront / try it first.
   Weaker than the others (a drawing of a shop, not a standing cardboard
   set) but it still reads.
3. `…/03-live-stall.png` — after Lovable + Supabase. Workflow. Pose:
   `point-right`. Speaking-tube → stall → cupboard. Labels: said in
   English / live stall / data cupboard.

AE2 and VC1 were the cleanest. Knowledge v1 (answer labelled on the robot)
was rejected; v2 is the file above.

## Deliver

1. Commit keepers under `archive/course-illustrations/<slug>/` in this repo
   so they have a raw GitHub URL.
2. On `tinkertanker/tinkercademy.com`, copy to
   `public/images/generated/illustrations/<slug>/` and insert an `<img>` in
   `src/content/programmes/<slug>.md`. Leave `heroImage` alone.
3. Report placement, which shots are solid, which are optional. Skip the
   style lecture.
