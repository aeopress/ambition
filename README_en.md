# ambition

A Claude Code and Codex CLI skill. Give it a task. It makes the task deeper, not bigger, then rewrites it as one prompt and stops.

Based on Felix Rieseberg, [How to be more ambitious: A tutorial for humans with models](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/) (2026-10-13). The Depth questions quote his prompt. Structure adapted from [DannyMac180/skills be-ambitious](https://github.com/DannyMac180/skills/tree/main/be-ambitious) (MIT).

## What it does

1. **Triage the axis.** Altitude: the task is a proxy for an outcome. Depth: the task must run at a top professional's level. Range: other fields own better instruments. Speed: run the task as asked, no technique needed.
2. **Analyze on that axis.** Altitude writes the goal behind the goal, a three-rung ladder and the prerequisites. Depth answers four questions: the professional's moves, the rawest material, named methods and tools, an outside judge. Range replaces the nouns with verbs, then lists fields by the instrument each owns.
3. **Rewrite and stop.** One fenced prompt in your voice. It ends with an outside check. The skill offers to run it and waits.

Replies follow the language of your task. The analysis uses short sentences, active voice and one name for each thing.

## Relation to best-minds

[best-minds](https://github.com/yelban/best-minds.TW) convenes real people's perspectives for a judgment call. `ambition` turns a direction into a prompt that runs at a professional's standard. Range gives fields and instruments for a task that will run. best-minds gives perspectives for a decision.

正體中文版：[README.md](README.md)

## Install

Claude Code:

```bash
claude plugin marketplace add yelban/ambition
claude plugin install ambition@ambition
```

Codex CLI:

```bash
codex plugin marketplace add yelban/ambition
codex plugin add ambition@ambition
```

Manual, without a plugin:

```bash
git clone https://github.com/yelban/ambition.git ~/zoo/skills/ambition
ln -s ~/zoo/skills/ambition/skills/ambition ~/.claude/skills/ambition
```

## Update

Claude Code (restart after the update):

```bash
claude plugin marketplace update ambition
claude plugin update ambition@ambition
```

Codex CLI (`upgrade` refreshes the marketplace snapshot only, so install the plugin again):

```bash
codex plugin marketplace upgrade ambition
codex plugin remove ambition@ambition
codex plugin add ambition@ambition
```

Manual install: run `git pull` in the cloned directory.

## Examples

```text
/ambition make the QBR slides from this quarter's data
/ambition we believe churn is an onboarding problem, write the analysis
/ambition which fields could help make this review deck decide a budget in 30 minutes
```

## Evals

`evals/evals.json` holds three cases, one per axis. Run `./evals/run.sh` for all, or `./evals/run.sh --case 2` for one.

## License

MIT
