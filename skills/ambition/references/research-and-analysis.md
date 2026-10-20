Paraphrased from erikmackinnon/skills (MIT)

# Research and analysis

Use this file for investigations, data analysis, market research, user research, literature reviews, or technical due diligence. Use only the sections for the chosen axis. Put the selected methods in one rewritten prompt, then stop.

## Outcome

- Name the decision, belief, or action that depends on the answer. If no answer would change it, reconsider the size of the research task.
- When evidence cannot support one verdict, map the options. Show what distinguishes them, the best opposing case, and the evidence that would resolve each uncertainty. Keep this map as the task's single result.
- Seek a finding beyond a summary. Examples include a signal that appears sooner, a cause that was missed, or evidence that rejects an accepted assumption.

## Raw material

Start with direct evidence: source code, transcripts, company filings, original study data, research papers, raw logs, and the underlying dataset. A dashboard, abstract, or secondary account can hide the evidence. When only a summary is accessible, state the access limit and mark its claims as not yet verified.

## Methods and tools

| Weak approach | Method to put in the rewrite |
|---|---|
| Select a claim using the complete dataset | Reserve unseen observations. Use them for one final test after selecting the claim. |
| Accept an internal explanation | Reproduce it from direct evidence with a test that can reject it. |
| Trust one account | Cross-check claims across sources. Link each central claim to evidence that supports it. |
| Keep reading without a stopping rule | State hypotheses and their predicted observations before inspecting the evidence. |
| Treat correlation as a cause | Check base rates. Where evidence permits, use a natural experiment or difference-in-differences comparison. |
| Report only what happened | Model the previous year from logs. Find a signal that was available before the event, then test its predictions on unseen observations. |

Choose tools that can check the calculation: R, SQL, Python, statistical libraries, or executable notebooks. Do not replace calculation with prose. Put missing tools, data, or access in the rewrite's setup steps. Do not install software now.

## Other fields worth borrowing from

- **Forecasting:** record probabilities and deadlines so later events can score predictions.
- **Journalism:** trace each assertion to its speaker, the speaker's access to facts, and the original record.
- **Short selling:** examine incentives and search for evidence that an interested party would conceal.
- **Intelligence analysis:** compare competing explanations against the evidence. Seek observations that would reject each explanation.
- **Epidemiology:** identify exposure groups, measure base rates, and test alternative causes.

## Judges

- Use reserved data once. A dataset loses independence when it guides revisions to the claim.
- Record predictions before opening the results. Include an observation date and a rule that scores each prediction.
- Audit the cited records against each central claim. Verify quotations and provenance without relying on agreement with the draft's conclusion.
- Replicate the result with another dataset or another method. Define how close the results must be to count as agreement.

## Targets and vetoes

- Select a target that fits the question. One option detects a warning a stated number of days before the current process. Another predicts unseen outcomes above a named baseline. Require primary evidence for central claims as a correctness veto.
- Reject results that depend on leaked test data, inadequate samples, violated privacy or consent, or claims beyond what the sources can establish.

## Traps

- Do not fit a complex model to sparse evidence. State what evidence is missing. Put access to it in the rewrite's setup. State which claims remain unverified until that evidence exists.
- More papers and more pages do not by themselves improve a literature review.
- Separate verified facts, deductions, and opinions. Smooth prose does not turn a synthesis into a finding.
- Use a chart to test or explain a stated claim. Do not add charts without one.
