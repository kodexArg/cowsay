---
name: cowsay
description: >
  Deterministic cowsay mode (kodexArg). Final replies are rendered only by
  piping text through this skill's bin/cowsay with an explicit -W width.
  Triggers: /cowsay, cowsay, modo vaca, hablá como vaca, lo que dice una vaca,
  | cowsay, cowthink. Confined to this skill tree (directory of this SKILL.md).
license: MIT
metadata:
  author: kodexArg
  version: "0.2.2"
---

# cowsay (kodexArg)

Renderer is law. The model never draws the cow.

## Skill root

`SKILL_ROOT` = absolute path of the directory that contains **this** `SKILL.md`
(after install that is wherever the agent placed the skill; in this repo it is
the repository root).

Binary:

```text
$SKILL_ROOT/bin/cowsay
```

Cowfiles: `$SKILL_ROOT/cows/`. Python 3 stdlib. Same stdin + same `-W` ⇒ same
stdout. No system `cowsay`.

## Every final reply

1. Write the full answer (user language, real content).
2. Render:

```bash
printf '%s' "$ANSWER" | "$SKILL_ROOT/bin/cowsay" -W 48
```

3. User-visible output = that stdout only, inside one fenced code block:

````
```
<stdout>
```
````

No freehand ASCII. No “approximate” balloon. No offline cow drawing.

## Defaults

| | |
|---|---|
| Width | `-W 48` unless the user asks another |
| Cow | default (`-f` only if asked: `tux`, `moose`, …) |
| Think | `--think` when user asks cowthink / pensá |
| Faces | classic `-b -d -g -p -s -t -w -y`, `-e`, `-T` only if asked |

## Session

- `/cowsay` or “modo vaca” → stay in this mode until “basta vaca” / “normal mode” / “salí de cowsay”.
- `/cowsay <text>` → one-shot render of that text.

## Failure / meta

If the binary fails, report stderr and exit code in **plain text** (not through the cow). Do not invent art.

Cowfiles load only from bundled `cows/` and `COWPATH` dirs (resolved real path must stay under those roots; `.cow` → outside symlink is refused).

## Confinement

Only this skill tree (`$SKILL_ROOT`). No apt, no global skill links, no other trees unless ordered.
After CLI changes: `python3 tests/test_cowsay.py` from `$SKILL_ROOT`.
