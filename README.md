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

# cowsay — kodexArg · v1.0.2

Deterministic cowsay for AI agents. Python 3 **stdlib only**. **MIT**.

Credit: original **cowsay** by Tony Monroe; art and spirit from the active community tree **[cowsay-org/cowsay](https://github.com/cowsay-org/cowsay)**. This tree is a kodexArg reimplementation (rounded dialog, agent skill, terminal-aware wrap) — not a fork of the Perl binary.

## Layout

```
skills/cowsay/           ← installable skill (skills.sh convention)
  SKILL.md               agent skill contract
  bin/cowsay             CLI (compose only)
  lib/dialog.py          rounded box, wrap, terminal width
  lib/art.py             COWPATH, load cows/*.cow, faces, active cow
  cows/*.cow             ASCII resources ($thoughts $eyes $tongue)
  tests/                 goldens
README.md LICENSE        package docs (repo root)
```

Dialog logic and ASCII art are **separate** so cows can change without rewriting the balloon.

> **skills.sh note:** the directory indexes skills under `skills/<name>/SKILL.md`.
> A root-level `SKILL.md` installs via the CLI but does **not** get a skill page.

## Install (skills.sh)

```bash
npx skills add kodexArg/cowsay
# → https://skills.sh/kodexArg/cowsay/cowsay
```

## Local use

```bash
cd skills/cowsay
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

- **Dialog** (`lib/dialog.py`): min 3 rows; width = **display columns** (EAW + combining) + 1 blank, floored by art silhouette; `-W` wraps by columns not codepoints.
- **Art** (`cows/*.cow`): original-style figures; add/replace via `-f name` or `--set-cow`.

## Active cow

```bash
cd skills/cowsay
./bin/cowsay -l              # loaded stems (whatever is in cows/ + COWPATH)
./bin/cowsay --set-cow tux   # persist → .active-cow
./bin/cowsay --show-cow
```

Priority: `-f` → `COWSAY_COW` → `.active-cow` → `default`.

### Agent slash form (skill contract)

In chat with the skill loaded, a **loaded cow stem** switches art permanently
(via `--set-cow`). It is **not** a one-shot of that word as bubble text.

**Example — TUX:**

```text
/cowsay tux
```

That runs `--set-cow tux` and confirms with the Tux figure. Later replies use
Tux until you pick another cow.

**Other options:** any stem returned by `./bin/cowsay -l` (bundled set today
is typically `default`, `moose`, `tux`; plus any extra `.cow` files you add
under `cows/` or via `COWPATH`). Examples:

```text
/cowsay moose
/cowsay default
/cowsay <any-stem-from--l>
```

If the token is **not** a loaded stem, `/cowsay <text>` is a one-shot render
of that text with the current active cow.

## Release

**v1.0.2** — skills.sh layout (`skills/cowsay/`); display-column box/wrap.

| Piece | Status |
|-------|--------|
| Rounded dialog + original cow art | stable |
| Layer split (`dialog` / `art` / `cows/`) | stable |
| Terminal-aware wrap, hug-text box | stable |
| Display width (wide/emoji/CJK/combining) | stable |
| Active cow + skill UX (`/cowsay tux`, …) | stable |
| Tests | `python3 tests/test_cowsay.py` |
