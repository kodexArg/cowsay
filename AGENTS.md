# AGENTS.md — cowsay (kodexArg)

## Identity

| | |
|---|---|
| Author | kodexArg |
| License | MIT |
| Scope | This tree only (`$SKILL_ROOT` = directory of `SKILL.md`) |

## Product

- Skill: `SKILL.md` — agent must pipe answers through the renderer.
- Renderer: `bin/cowsay` — Python 3 stdlib, deterministic.

## Contract

```bash
printf '%s' "$TEXT" | ./bin/cowsay -W "$COLS"
```

Same text + same flags → same bytes. No random, no locale-dependent layout, no system cowsay.

## Rules

1. Do not write outside this path unless ordered.
2. Do not `apt install cowsay`.
3. Do not freehand cow ASCII in chat; run the binary.
4. After CLI changes: verify with the commands below.

## Verify

```bash
# from repository / skill root
python3 tests/test_cowsay.py
printf '%s' 'moo' | ./bin/cowsay -W 40
printf '%s' 'a b c' | ./bin/cowsay -W 3
printf '%s' 'x' | ./bin/cowsay -W 40 | cmp - <(printf '%s' 'x' | ./bin/cowsay -W 40)
```
