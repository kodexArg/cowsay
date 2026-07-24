```
╭─────────────────────────────────────────╮
│ Based on the original project cowsay —  │
│ https://github.com/cowsay-org/cowsay    │
│                                         │
╰─────────────────────────────────────────╯
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

# cowsay — kodexArg · v1.0.1

Deterministic cowsay for AI agents. Python 3 **stdlib only**. **MIT**.

Credit: original **cowsay** by Tony Monroe; art and spirit from the active community tree **[cowsay-org/cowsay](https://github.com/cowsay-org/cowsay)**. This tree is a kodexArg reimplementation (rounded dialog, agent skill, terminal-aware wrap) — not a fork of the Perl binary.

## Layout

```
bin/cowsay       CLI (compose only)
lib/dialog.py    rounded box, wrap, terminal width
lib/art.py       COWPATH, load cows/*.cow, faces, active cow
cows/*.cow       ASCII resources ($thoughts $eyes $tongue)
SKILL.md         agent skill contract
```

Dialog logic and ASCII art are **separate** so cows can change without rewriting the balloon.

## Install (skills.sh)

```bash
# private
npx skills add git@github.com:kodexArg/cowsay.git
# public later
npx skills add kodexArg/cowsay
# → https://skills.sh/kodexArg/cowsay/cowsay
```

## Local use

```bash
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
./bin/cowsay -l              # loaded stems
./bin/cowsay --set-cow tux   # persist → .active-cow
./bin/cowsay --show-cow
```

Agent slash form (skill contract): `/cowsay tux`, `/cowsay moose`,
`/cowsay default` — any stem from `-l` → `--set-cow` (not a text one-shot).

Priority: `-f` → `COWSAY_COW` → `.active-cow` → `default`.

## Release

**v1.0.1** — display-column box/wrap (EAW / combining); review before git tag.

| Piece | Status |
|-------|--------|
| Rounded dialog + original cow art | stable |
| Layer split (`dialog` / `art` / `cows/`) | stable |
| Terminal-aware wrap, hug-text box | stable |
| Display width (wide/emoji/CJK/combining) | stable |
| Active cow + skill UX | stable |
| Tests | `python3 tests/test_cowsay.py` |
