---
name: cowsay
description: >
  Deterministic cowsay mode (kodexArg). Final replies are rendered only by
  piping text through this skill's bin/cowsay with a terminal-aware -W width.
  `/cowsay tux`, `/cowsay moose`, `/cowsay default` (any loaded stem from
  `cowsay -l`) works: apply with `cowsay --set-cow <stem>`. When the user
  asks to change the cow without naming one, list every loaded cow, offer
  them as choices, then `--set-cow`. Triggers: /cowsay, /cowsay <stem>,
  cowsay, modo vaca, hablá como vaca, cambiar la vaca, | cowsay, cowthink.
  Confined to this skill tree.
license: MIT
metadata:
  author: kodexArg
  version: "1.0.1"
---

# cowsay (kodexArg)

Renderer is law. The model never draws the cow or the dialog by hand.

## Architecture (do not collapse)

| Layer | Path | Owns |
|-------|------|------|
| CLI | `$SKILL_ROOT/bin/cowsay` | compose only |
| Dialog | `$SKILL_ROOT/lib/dialog.py` | balloon, wrap, terminal width |
| Art | `$SKILL_ROOT/lib/art.py` | COWPATH, load `.cow`, faces, active cow |
| Resources | `$SKILL_ROOT/cows/*.cow` | ASCII figures (`$thoughts` `$eyes` `$tongue`) |
| Active | `$SKILL_ROOT/.active-cow` | one-line stem (persists user choice) |

Changing art resources = add/edit `cows/*.cow`. **Never** freehand ASCII.

## Skill root

`SKILL_ROOT` = directory containing this `SKILL.md`.  
Binary: `$SKILL_ROOT/bin/cowsay`.

## Width (use the terminal)

**Never hardcode `-W 48`.**

```bash
if [ -n "${COWSAY_WIDTH:-}" ]; then
  W="$COWSAY_WIDTH"
elif [ -n "${COLUMNS:-}" ] && [ "$COLUMNS" -gt 0 ] 2>/dev/null; then
  W=$((COLUMNS - 4))
else
  W=$(stty size 2>/dev/null | awk '{print $2}')
  W=${W:-80}
  W=$((W - 4))
fi
[ "$W" -lt 8 ] && W=8
```

Or omit `-W`. Outer box = content + 4.

## Changing the cow (mandatory UX)

Triggers (any language): “cambiar la vaca”, “change the cow”, “otra vaca”,
“usá tux”, “qué vacas hay”, “can you change the cow?”, etc.

### Slash form (works; first-class)

`/cowsay <stem>` where `<stem>` is a **loaded** cow name from `-l` is a full
cow switch — **not** a one-shot of the word. Examples that must work:

| User says | Action |
|-----------|--------|
| `/cowsay tux` | `--set-cow tux` + confirm with tux art |
| `/cowsay moose` | `--set-cow moose` + confirm |
| `/cowsay default` | `--set-cow default` + confirm |
| `/cowsay <any stem from -l>` | same pattern |

Resolve the stem against the live list first (do not invent names):

```bash
"$SKILL_ROOT/bin/cowsay" -l
"$SKILL_ROOT/bin/cowsay" --set-cow <stem>
"$SKILL_ROOT/bin/cowsay" -W "$W" <<'COWEOF'
Listo: vaca activa = <stem>
COWEOF
```

If the token is **not** a loaded stem, treat it as one-shot text (see Session).

### If the user did **not** name a cow

1. Load the menu (authoritative list — do not invent names):

```bash
"$SKILL_ROOT/bin/cowsay" -l
"$SKILL_ROOT/bin/cowsay" --show-cow
```

2. Offer **every** stem returned by `-l` as choices (e.g. `default`, `moose`,
   `tux`, …). Prefer a multiple-choice UI when available; otherwise list them
   clearly in the reply **through cowsay**.
3. Wait for the user pick. Do **not** pick for them.

### If the user named a cow (or just picked one)

Same as slash form — apply immediately (persist + confirm with that art):

```bash
"$SKILL_ROOT/bin/cowsay" --set-cow <stem>
"$SKILL_ROOT/bin/cowsay" -W "$W" <<'COWEOF'
Listo: vaca activa = <stem>
COWEOF
```

(`--set-cow` writes `.active-cow`; later renders without `-f` use it.)

### One-shot without persisting

Only if the user says “solo esta vez” / “just this once”:

```bash
"$SKILL_ROOT/bin/cowsay" -f <stem> -W "$W" <<'COWEOF'
...
COWEOF
```

## Every final reply

1. Write the full answer (user language).
2. Resolve `W` (or omit `-W`).
3. Render with a **quoted** heredoc (uses active cow unless `-f`):

```bash
"$SKILL_ROOT/bin/cowsay" -W "$W" <<'COWEOF'
<the full answer>
COWEOF
```

4. User-visible output = that stdout only, one fenced code block:

````
```
<stdout>
```
````

## Defaults

| | |
|---|---|
| Width | hug text (+1 blank); floor = art width; `-W` only wraps |
| Height | min 3 text rows |
| Cow | `COWSAY_COW` → `.active-cow` → `default` |
| Think | `--think` when asked |

## Session

- `/cowsay` → stay until “basta vaca” / “normal mode” / “salí de cowsay”.
- `/cowsay <stem>` if stem ∈ `cowsay -l` (e.g. `tux`, `moose`, `default`) →
  **cow switch** via `--set-cow` (works; see Changing the cow).
- `/cowsay <text>` if text is **not** a loaded stem → one-shot render of that text.
- Active cow persists across sessions via `.active-cow`.

## Failure

Binary failure → plain text stderr + exit code. No invented art.

## Confinement

Only `$SKILL_ROOT`. After changes: `python3 tests/test_cowsay.py`.
