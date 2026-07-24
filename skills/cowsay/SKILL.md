---
name: cowsay
description: >
  Deterministic cowsay mode for AI agents (kodexArg). Render every final
  reply through this skill bin/cowsay with terminal-aware wrap. Use when the
  user runs /cowsay, says cowsay, modo vaca, change the cow, cowthink, or
  asks to switch art with /cowsay tux (or any stem from cowsay -l). Apply
  cow switches via --set-cow. Confined to this skill tree.
license: MIT
metadata:
  author: kodexArg
  version: "1.0.3"
---

# cowsay — kodexArg · v1.0.3

Deterministic cowsay for AI agents. Python 3 **stdlib only**. **MIT**.

Inspired by the original project [cowsay](https://github.com/cowsay-org/cowsay)
(Tony Monroe; community tree cowsay-org/cowsay). This is a kodexArg
reimplementation (rounded dialog, agent skill, terminal-aware wrap) — not a
fork of the Perl binary.

```
╭─────────────────────────────────────────╮
│ Inspired by the original project cowsay │
│ https://github.com/cowsay-org/cowsay    │
│                                         │
╰─────────────────────────────────────────╯
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

## Install (skills.sh)

```bash
npx skills add kodexArg/cowsay
# → https://skills.sh/kodexArg/cowsay/cowsay
```

## Layout

```
skills/cowsay/           installable skill (this folder)
  SKILL.md               this file (agent contract + public docs)
  bin/cowsay             CLI (compose only)
  lib/dialog.py          rounded box, wrap, terminal width
  lib/art.py             COWPATH, load cows/*.cow, faces, active cow
  cows/*.cow             ASCII resources ($thoughts $eyes $tongue)
  tests/                 goldens
```

Dialog logic and ASCII art are **separate** so cows can change without
rewriting the balloon.

## Local use

```bash
# from this skill directory
printf '%s' 'moo' | ./bin/cowsay              # -W = terminal width (wrap only)
printf '%s' 'hi'  | ./bin/cowsay -W 40
printf '%s' 'hi'  | ./bin/cowsay -W 20 -f tux
printf '%s' 'hmm' | ./bin/cowsay -W 40 --think
./bin/cowsay -l
python3 tests/test_cowsay.py
```

| Env | Effect |
|-----|--------|
| `COLUMNS` | terminal width when `-W` omitted |
| `COWSAY_WIDTH` | pin wrap width (tests/CI; beats `COLUMNS`) |
| `COWSAY_COW` | force active cow stem (beats `.active-cow`) |
| `COWPATH` | extra cow directories |

## Dialog vs art

- **Dialog** (`lib/dialog.py`): min 3 text rows; width = **display columns**
  (EAW + combining) + 1 blank, floored by art silhouette; `-W` wraps by
  columns, not codepoints.
- **Art** (`cows/*.cow`): original-style figures; add/replace via `-f name`
  or `--set-cow`.

## Active cow

```bash
./bin/cowsay -l              # loaded stems (cows/ + COWPATH)
./bin/cowsay --set-cow tux   # persist → .active-cow
./bin/cowsay --show-cow
```

Priority: `-f` → `COWSAY_COW` → `.active-cow` → `default`.

### Agent slash form

In chat with the skill loaded, a **loaded cow stem** switches art permanently
(via `--set-cow`). It is **not** a one-shot of that word as bubble text.

**Example — TUX:**

```text
/cowsay tux
```

That runs `--set-cow tux` and confirms with the Tux figure. Later replies use
Tux until you pick another cow.

**Other options:** any stem from `./bin/cowsay -l` (bundled set is typically
`default`, `moose`, `tux`; plus extra `.cow` files under `cows/` or
`COWPATH`):

```text
/cowsay moose
/cowsay default
/cowsay <any-stem-from--l>
```

If the token is **not** a loaded stem, `/cowsay <text>` is a one-shot render
of that text with the current active cow.

## License

**MIT** — Copyright (c) 2026 kodexArg (Gabriel Cavedal) / kodexarg.com.
See the repository root `LICENSE` for the full text.

---

# Agent contract (mandatory)

Renderer is law. The model **never** draws the cow or the dialog by hand.

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

## Changing the cow

### Slash form (works; first-class)

`/cowsay <stem>` where `<stem>` is a loaded cow from `-l`:

```bash
"$SKILL_ROOT/bin/cowsay" -l
"$SKILL_ROOT/bin/cowsay" --set-cow <stem>
"$SKILL_ROOT/bin/cowsay" -W "$W" <<'COWEOF'
Listo: vaca activa = <stem>
COWEOF
```

### Menu (user did not name a cow)

1. `"$SKILL_ROOT/bin/cowsay" -l` and `--show-cow`
2. Offer **every** stem from `-l` (do not invent names)
3. Wait for the pick; then `--set-cow`

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

4. User-visible output = that stdout only, one fenced code block.

## Session

- `/cowsay` → stay until “basta vaca” / “normal mode” / “salí de cowsay”.
- `/cowsay <stem>` if stem ∈ `cowsay -l` → **cow switch** via `--set-cow`.
- `/cowsay <text>` if text is **not** a loaded stem → one-shot.
- Active cow persists via `.active-cow`.

## Failure

Binary failure → plain text stderr + exit code. No invented art.

## Confinement

Only `$SKILL_ROOT`. After changes: `python3 tests/test_cowsay.py`.
