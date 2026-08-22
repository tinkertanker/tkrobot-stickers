# Course-body illustrations (2026-08 keepers)

Accepted 16:9 T Krobot sketches from the illustrations-skill test. These are
**not** the sticker pack and **not** programme heroes.

Future generators: read
`docs/skills/tkrobot-illustrations/references/worked-examples.md` first. Steal
pose, labels, and page density from these files. Do not copy the furniture.

Folder names match `tinkertanker/tinkercademy.com` programme slugs.

| File | Course | Pose |
| --- | --- | --- |
| `knowledge-powered-ai-with-chatgpt/01-grounded-answer.png` | Knowledge-Powered AI | `point-right` |
| `from-prompting-to-pull-request/01-review-the-diff.png` | From Prompting to Pull Request | `point-right` |
| `agentic-workflows-for-businesses/01-weekly-loop.png` | Agentic Workflows | `palm-open` |
| `agentic-engineering-with-claude-code-or-codex/01-direct-and-check.png` | Agentic Engineering | `point-right` |
| `agentic-engineering-with-claude-code-or-codex/02-kind-of-instruction.png` | Agentic Engineering | `hands-on-hips` |
| `agentic-engineering-with-claude-code-or-codex/03-inspectable-loop.png` | Agentic Engineering | `palm-open` |
| `vibe-coding-for-digital-builders/01-the-brief.png` | Vibe Coding for Digital Builders | `point-right` |
| `vibe-coding-for-digital-builders/02-paper-shopfront.png` | Vibe Coding for Digital Builders | `palm-open` |
| `vibe-coding-for-digital-builders/03-live-stall.png` | Vibe Coding for Digital Builders | `point-right` |

All files are 1536×1024 RGB PNG.

## Handoff to tinkercademy.com

Do not put these in `heroImage`. Heroes stay photoreal under
`public/images/generated/hero-review/<slug>/`.

Copy keepers to:

```
public/images/generated/illustrations/<slug>/01-topic.png
```

Then insert an `<img>` after the matching paragraph in
`src/content/programmes/<slug>.md`.

Raw URLs (this branch until PR 5 merges, then the base branch):

```
https://raw.githubusercontent.com/tinkertanker/tkrobot-stickers/<ref>/archive/course-illustrations/<slug>/<file>
```

Use `cursor/test-tkrobot-illustrations-2fb9` as `<ref>` while this PR is open.
After merge, use `tkrobot-illustrations-skill` or `main`, whichever the PR
landed on.

Chat paths under `/opt/cursor/artifacts/` die with the VM. If a shot is a
keeper, copy it here in the same turn.
