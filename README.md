# cowsay — kodexArg

Deterministic cowsay for AI agents: `SKILL.md` + `bin/cowsay` (Python 3, **stdlib only**).

MIT License. Same stdin + same flags ⇒ same stdout. No system `cowsay`.

## Install (skills CLI / skills.sh)

While the GitHub repo is **private**, only accounts with access can install:

```bash
# SSH (recommended when private)
npx skills add git@github.com:kodexArg/cowsay.git

# HTTPS (needs a GitHub token with repo scope)
npx skills add https://github.com/kodexArg/cowsay.git
```

After you make the repo **public**, the public install line is:

```bash
npx skills add kodexArg/cowsay
```

That first public install also starts **skills.sh** listing (there is no submit form — telemetry from `npx skills add` indexes the skill). Page shape once listed:

`https://skills.sh/kodexArg/cowsay/cowsay`

## Local use

```bash
printf '%s' 'moo' | ./bin/cowsay -W 48
printf '%s' 'hello' | ./bin/cowsay -W 20 -f tux
printf '%s' 'hmm' | ./bin/cowsay -W 40 --think
python3 tests/test_cowsay.py
```

| Path | Role |
|------|------|
| `bin/cowsay` | renderer (v0.2.2) |
| `cows/*.cow` | templates (`$thoughts` `$eyes` `$tongue`) |
| `tests/test_cowsay.py` | goldens / regressions |
| `SKILL.md` | agent contract (root skill for skills CLI) |
| `AGENTS.md` | repo confine |
| `LICENSE` | MIT |

## Publish checklist (skills.sh)

1. Repo has root `SKILL.md` with `name` + `description` frontmatter (done).
2. MIT `LICENSE` + this README (done).
3. Start **private** → develop/test installs over SSH.
4. When ready for the directory: `gh repo edit kodexArg/cowsay --visibility public` (or Settings → Danger zone).
5. Run once (or have others run): `npx skills add kodexArg/cowsay -y`
6. Optional discoverability: `gh repo edit kodexArg/cowsay --add-topic agent-skills --add-topic skills-sh`
