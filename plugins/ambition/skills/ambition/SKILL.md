---
name: ambition
description: "Raise the ambition of a task before it runs. Three axes: Altitude (the outcome behind the task), Depth (a top professional's raw material, methods and an outside judge), Range (other fields and their instruments). Produces one rewritten prompt and stops. Keeps the outcome: deeper, not bigger. Triggers: be ambitious, more ambitious, deeper not bigger, raise the bar, what would a top professional do, goal behind the goal, which fields could help, 更有野心, 做深一點, 拉高層次, 跨領域借方法. Not for closed factual questions, scope expansion, tone or length edits, or open-ended judgment calls (those go to best-minds)."
---

<!--
PLATFORM VARIANT: Codex CLI edition.
The canonical source of truth is skills/ambition/SKILL.md at the repo root (Claude Code edition).
Edit the canonical first, then port methodology changes here. This variant differs ONLY in
platform mechanics: frontmatter keeps name and description only, a plain question replaces
AskUserQuestion, "use the best-minds skill" replaces the Skill tool call.

input: a task or prompt the user is about to run
output: the chosen axis with its tell, an axis-specific analysis, one rewritten prompt in a fenced block, then stop
pos: auxiliary skill, a pre-flight step before a task runs
-->

# Ambition

> **Output language: reply in the language of the user's task.** Write the analysis in short sentences. Put one idea in each sentence. Use the active voice. Use one name for each thing. Write the rewritten prompt in the user's voice.

Source: Felix Rieseberg, "How to be more ambitious: A tutorial for humans with models" (2026-10-13, updated 2026-10-16). The four Depth questions quote his prompt. The other techniques are paraphrased from the article. Four guards are paraphrased from Erik MacKinnon's six-model reading of the same article (github.com/erikmackinnon/skills, MIT): the veto on a hard target, the independent outside check, the measured report and the kept artifact.

## Core

Ambition has four types: Speed, Altitude, Depth and Range.

- **Speed** is the same work in less time. It needs no technique. Run the task as asked.
- **Altitude** goes up one level of abstraction. It asks for the outcome behind the task.
- **Depth** does the same task the way a top professional in the field does it.
- **Range** brings in fields the task does not name, with their instruments.

This skill handles Altitude, Depth and Range. Each one makes the task **deeper, not bigger**: the same outcome, a higher standard.

## Input

The task is the text after the skill name. If there is none, use the user's most recent request. If there is none, ask for the task in one line and stop.

When the task names files, data, logs or drafts that you can read, read them before Step 1. Change nothing. Base the analysis on what you found. When you cannot reach the material, work from the task text.

## Step 1: Triage the axis

Pick one axis. Use these tells:

- **Altitude**: the task is a proxy for an outcome. People will hold a meeting about the result, or the user hands over the same kind of task again and again. Example: "make the QBR slides" serves "leadership catches problems early." "Fix this crash" serves "the app stays crash-free."
- **Depth**: the user wants this one task done at the level of the best professional in the field.
- **Range**: the task sits on the surface of one field. Other fields own better instruments for parts of it.
- **Speed**: the task is clear and the user wants it done. Say "this task needs Speed only" and stop. Offer to run it as asked.

Name the axis and its tell in one sentence, then move on.

When the task is an open-ended judgment with no single right answer, the hand-off is the whole reply: say in one or two sentences that this is a judgment call and that best-minds handles it, then use the best-minds skill. When the Skill tool is unavailable, the hand-off sentence names best-minds and ends the reply. Add no command, no code block and no copy of the user's question. A hand-off carries no axis, no analysis, no rewritten prompt and no opinion of your own. The boundary: Range yields fields and instruments for a task that will run. best-minds yields real people's perspectives for a decision.

When two axes fit, pick the axis the user's wording supports. Name the other axis in a few words as a follow-up. When the choice hinges on the user's intent, ask the user one question with the two axes. When interaction is unavailable, state the assumption you chose.

Done when: one axis is named, with its tell, before any analysis, or the hand-off sentence is written and nothing follows it.

## Step 2: Analyze on that axis

Name the field first (for example "SRE incident response", "cohort analysis", "investigative journalism"). Be concrete: name the actual thing, not the category. When you do not know a source, tool or method well enough, say so. Say what you did not find.

### Altitude

1. **Find the goal behind the goal.** Ask: what should happen next after this task is done? Repeat the question until the answer is an outcome someone decides on or acts on. When the same kind of task keeps coming back, climb to an outcome that stays true without the user handing over each case.
2. **Write the ladder.** Three rungs, one sentence each. Rung 1 is the task as asked. Rung 2 asks for the decision the task serves. Rung 3 names the outcome itself, and nothing else. Below the ladder, add one line: what in the user's own history would show that the new way catches problems sooner.
3. **List the prerequisites.** Name what the model needs before the top rung is workable: data access, tools, environments, a way to reproduce and verify. The top rung often changes the workflow, not only the prompt.
4. **Name the outside signal.** What, other than the user or the model, shows that the outcome moved. When the top rung replaces a process, run the new way beside the current one for one cycle. The current process runs as it does today and serves as the comparison. The rewrite asks for the new way only and adds no second deliverable. The new way replaces the current one only after the signal confirms it.

Altitude fits outcome work. It fits creative work badly. When the task is creative, say so and analyze on Depth instead.

Keep the artifact when someone waits for this exact artifact and a different one would let them down: a patch under review, a letter in the user's own voice. Say so and analyze on Depth instead. A required template only fixes the format. A task with a template stays on Altitude.

### Depth

Aim for a result that the best in the field could learn something from. Answer the four questions from the source prompt, for the named field:

> (1) say what a top professional in this field would do here that I'm not asking for; (2) name the rawest material they would start from instead of what has already been digested for me; (3) name the specific methods and tools they would use; (4) say what, other than you or me, would show the result is right.

1. **The professional's moves.** At most three moves that separate expert work from competent work here. Choose the moves with the largest effect on the result. Examples: state the decision the work serves, check base rates, reproduce before fixing, write the counter-argument.
2. **The rawest material.** The dataset, not the chart. The filing, not the article. The logs and the code, not the bug report. Say where it lives when you know.
3. **Methods and tools, named.** Named techniques, instruments, libraries, commands or frameworks, and why each fits. Use the same instruments the best in the field use. When the natural reach is a markdown table, name the database and the statistical model instead. The failure to avoid: a change of vocabulary without a change of instruments. When the material cannot support the method, say so. A few dozen rows do not support a predictive model.
4. **The outside judge.** An external check: a test suite, a benchmark, a reproduction, ground-truth data, a known answer, a measurement, a reviewer, a real user's behavior. Set a measurable threshold or a comparison with a named baseline. State which results pass. State which results fail. Reporting a metric alone does not define these criteria. Prefer a check the model can run itself and get feedback from at once.

Three pressure moves, applied in the rewrite:

- **Set the target at the field's frontier.** Ask for the number the best in the field reach, and state it as reachable. "200 ms", not "faster". When the target seems impossible, tell the model to keep going. Name the constraint that can veto the target, such as correctness, data leakage or a public API. A correctness floor ("no errors") is a veto, not the target. When no known method reaches the target yet, make finding the method the first goal and keep the target.
- **Turn beliefs into hypotheses.** Each belief the user states ("churn is an onboarding problem") becomes a claim to reproduce from the raw material. Ask the model to test it adversarially.
- **Ask for new knowledge.** When the raw material is data or logs, ask for one finding nobody has yet: an earlier signal, a blind spot or a hidden cause. Ask the model to show that the finding holds on data it was not found on.

Done when: the rewritten prompt states a frontier target with its veto, and ends with an outside check whose pass and failure criteria use a measurable threshold or a comparison with a named baseline.

### Range

1. **Replace the nouns with verbs.** Rewrite the task as what it does, for whom, under what constraint. "A QBR deck" becomes "help busy leaders see what caused this quarter's numbers and decide where to move money and people, within 30 minutes."
2. **Assemble the crew by instrument.** From the verbs, list two to four fields, at most four rows, one instrument each. For each field give: the field, the instrument it owns (a method, tool or technique), and the verb that instrument serves. Seat one adversarial field whose instrument tries to break the result (a short seller's position research, a forensic accountant's reconciliation).
3. **Ask for what the field does.** The rewrite asks the model to run that field's instrument on the user's material. A field is a source of methods: ask for the method, never for a persona. The voice stays the user's own.

Done when: every field on the list carries a named instrument and the verb it serves.

## Step 3: Rewrite and stop

Write the rewritten prompt in one fenced block the user can copy. It keeps the user's outcome, scope, voice and language. It asks for exactly what Step 2 found:

- Altitude: the rung the user accepts, with the prerequisites stated as setup steps, and the outside signal.
- Depth: start from the raw material. Use the named methods. State the target and its veto. End with the outside judge and its pass and failure criteria. Include the threshold or named baseline comparison in the rewritten prompt.
- Range: run each field's instrument on the material, end with the adversarial field's check.

When the method needs access, data or software that the model lacks, state it as a setup step at the start of the rewrite. Name what only the user can provide.

Every rewrite ends with an outside check. The outside check is the last section of the rewritten prompt. Put format and style requirements before it. The outside check replaces self-assessment by the model. Another model's agreement is not an outside check. When no outside check exists yet, building one is the first step. When none can exist, name the closest proxy and say what stays unverified.

In the outside check section, ask for the measured result next to the target. Accept an honest miss. Reject a claim of success without a measurement. Ask the model to say so when it shrinks the scope.

Then stop. Offer in one line to run it now. Start the task only when the user says so.

## Deeper, not bigger

A higher standard for the same outcome. Keep the outcome the user is after. Altitude may replace the task with the outcome it serves. No axis adds a parallel deliverable, a feature or a side quest. When a suggestion makes the job larger instead of better, delete it.

The opposite failure is a timid target. A target that a plain attempt already meets is too low. A correctness floor is a requirement, not a target. Raise either one to the field's frontier.

## Relation to best-minds

The two skills form a pipeline. best-minds converges a judgment call into a direction. This skill turns a direction into a prompt that runs at a professional's standard. When a Range analysis turns into "who would disagree about this", stop and use the best-minds skill. When best-minds ends with a direction to execute, it may hand off to this skill. A hand-off to best-minds ends with best-minds. It does not suggest coming back to this skill afterwards.
