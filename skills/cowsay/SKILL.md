---
name: cowsay
description: >
  Deterministic cowsay for AI agents (kodexArg). Renders replies through a
  bundled Python stdlib bin/cowsay with terminal-aware wrap and swappable
  ASCII art. Use when the user runs /cowsay, asks for cowsay mode, cowthink,
  modo vaca, change the cow, or switches art with /cowsay tux (or any stem
  from cowsay -l). Apply persistent switches with --set-cow.
license: MIT
compatibility: >
  Requires Python 3. Uses only the Python standard library. Bundled
  bin/cowsay under this skill folder — do not apt-install system cowsay.
metadata:
  author: kodexArg
  version: "1.0.5"
  homepage: https://github.com/kodexArg/cowsay
---

# cowsay

```
╭─────────────────────────────────────────────────────╮
│ Thanks: original cowsay — Tony Monroe / cowsay-org  │
│ https://github.com/cowsay-org/cowsay                │
│                                                     │
│ npx skills add kodexArg/cowsay                      │
│                                                     │
│ /cowsay tux                                         │
│ /cowsay moose                                       │
│ /cowsay default                                     │
│ /cowsay <text>                                      │
╰─────────────────────────────────────────────────────╯
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

Deterministic cowsay for AI agents. Python 3 **stdlib only**. **MIT**.
Page: https://skills.sh/kodexArg/cowsay/cowsay

Skill root after install: wherever the agent placed it (e.g.
`~/.agents/skills/cowsay`). Binary: `$SKILL_ROOT/bin/cowsay`.

## Prerequisites

```bash
python3 --version          # 3.x
test -x "$SKILL_ROOT/bin/cowsay"
"$SKILL_ROOT/bin/cowsay" -l
"$SKILL_ROOT/bin/cowsay" -V
```

No network, no extra packages, no system `cowsay`.

## How to use (chat)

| User says | What happens |
|-----------|----------------|
| `/cowsay` | Enter cowsay mode until “basta vaca” / “normal mode” / “salí de cowsay” |
| `/cowsay tux` | **Switch art** to Tux (persist with `--set-cow tux`) |
| `/cowsay moose` | Switch art to moose |
| `/cowsay default` | Switch art to default cow |
| `/cowsay <stem>` | Switch art if `stem` is listed by `cowsay -l` |
| `/cowsay <text>` | One-shot: render that text if `text` is **not** a loaded stem |
| “change the cow” / “cambiar la vaca” (no name) | List every stem from `-l`, wait for pick, then `--set-cow` |
| “cowthink” / “pensá” | Render with `--think` |
| “solo esta vez” + a stem | One-shot art via `-f <stem>` (do not persist) |

### Example — TUX

```text
/cowsay tux
```

1. Confirm stem is loaded: `"$SKILL_ROOT/bin/cowsay" -l`
2. Persist: `"$SKILL_ROOT/bin/cowsay" --set-cow tux`
3. Confirm by rendering through the binary (Tux art, not freehand ASCII)

**Other cows:** whatever `./bin/cowsay -l` returns (bundled set is typically
`default`, `moose`, `tux`; plus any extra `.cow` under `cows/` or `COWPATH`).

## CLI (local / agent shell)

```bash
printf '%s' 'moo' | "$SKILL_ROOT/bin/cowsay"
printf '%s' 'hi'  | "$SKILL_ROOT/bin/cowsay" -W 40
printf '%s' 'hi'  | "$SKILL_ROOT/bin/cowsay" -W 20 -f tux
printf '%s' 'hmm' | "$SKILL_ROOT/bin/cowsay" -W 40 --think
"$SKILL_ROOT/bin/cowsay" -l
"$SKILL_ROOT/bin/cowsay" --set-cow tux
"$SKILL_ROOT/bin/cowsay" --show-cow
python3 "$SKILL_ROOT/tests/test_cowsay.py"
```

Prefer a **quoted heredoc** for multi-line answers:

```bash
"$SKILL_ROOT/bin/cowsay" -W "$W" <<'COWEOF'
Your full answer here.
COWEOF
```

### Flags (common)

| Flag | Effect |
|------|--------|
| `-W N` | Wrap width (display columns). Prefer terminal width; never hardcode 48 |
| `-f <stem>` | One-shot cow (does not write `.active-cow`) |
| `--set-cow <stem>` | Persist active cow to `.active-cow` |
| `--show-cow` | Print active stem |
| `-l` | List loaded stems |
| `--think` | Thought bubbles instead of speech |
| `-d` / faces | Classic face flags when asked |

### Environment

| Env | Effect |
|-----|--------|
| `COLUMNS` | Terminal width when `-W` omitted |
| `COWSAY_WIDTH` | Pin wrap width (tests/CI; beats `COLUMNS`) |
| `COWSAY_COW` | Force active cow stem (beats `.active-cow`) |
| `COWPATH` | Extra directories of `.cow` files |

### Active cow priority

`-f` → `COWSAY_COW` → `.active-cow` → `default`

## Agent instructions

**Renderer is law.** Never freehand the dialog box or the ASCII animal. Always
run `$SKILL_ROOT/bin/cowsay` and show only its stdout (one fenced code block).

### 1. Resolve width

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

### 2. Switch cow when the user names a stem

```bash
"$SKILL_ROOT/bin/cowsay" -l
"$SKILL_ROOT/bin/cowsay" --set-cow <stem>
"$SKILL_ROOT/bin/cowsay" -W "$W" <<'COWEOF'
Listo: vaca activa = <stem>
COWEOF
```

Do not invent stem names. Source of truth is `-l`.

### 3. Every final reply in cowsay mode

1. Write the full answer in the user’s language.
2. Pipe it through the binary (heredoc above).
3. User-visible output = that stdout only.

### 4. Failure

If the binary exits non-zero, report stderr and exit code in **plain text**.
Do not invent art.

### 5. Confinement

Only operate inside `$SKILL_ROOT`. After code changes:
`python3 "$SKILL_ROOT/tests/test_cowsay.py"`.

## Layout

```text
skills/cowsay/
  SKILL.md          this file (Agent Skills format)
  bin/cowsay        CLI compose only
  lib/dialog.py     balloon, wrap, terminal width
  lib/art.py        COWPATH, load .cow, faces, active cow
  cows/*.cow        ASCII resources ($thoughts $eyes $tongue)
  tests/            goldens
```

Dialog and art are separate layers so figures can change without rewriting the
balloon.

## License

**MIT** — Copyright (c) 2026 kodexArg (Gabriel Cavedal) / kodexarg.com.

Full text: repository root `LICENSE`.
