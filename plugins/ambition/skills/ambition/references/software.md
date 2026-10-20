Paraphrased from erikmackinnon/skills (MIT)

# Software

Use this file for software defects, features, speed, code structure, infrastructure, developer tools, or CI. Use only the sections for the chosen axis. Put the selected methods in the rewritten prompt. Do not run the software task here.

## Outcome

- Connect the reported defect to the failure class. A crash repair can serve a broader goal: prevent similar failures from reaching customers. A passing test can serve trust in the module.
- For repeated requests, consider a process that sustains the outcome. Examples include stable builds, fewer crashes, or current dependencies. State the required access and setup in the rewrite. Such a process needs crash records, release-to-commit links, and an environment that can reproduce failures and check repairs. State the setup cost.
- Keep a specific patch, migration, or API when someone depends on that exact result. In that case, choose Depth. Improve the method and proof without replacing the artifact.

## Raw material

Use direct system evidence before a written account of the incident:

- The failed CI job and its output.
- Commit history through `git blame` and `git log`, with issue records.
- Real requests and profiles from production.
- Execution traces, logs, core dumps, and stack traces.

## Methods and tools

| Weak approach | Method to put in the rewrite |
|---|---|
| Change code until it looks plausible | First capture the defect in a small reproduction or failing test. |
| Judge speed from a quick trial | Compare a recorded baseline with repeated measurements after warmup. Select criterion, pytest-benchmark, or hyperfine as appropriate. |
| Treat line coverage as proof | Use mutation testing to check whether tests detect injected defects. |
| Inspect commits one by one | Give `git bisect` a reproduction that identifies the failure. |
| Tune the suspected slow code | Measure first with `EXPLAIN ANALYZE`, browser devtools, `py-spy`, `perf`, or a flame graph. |
| Test only selected examples | Compare with a reference implementation, fuzz inputs, or use property tests through fast-check or Hypothesis. |
| Prove the repair on one machine | Reproduce and verify on the supported platforms. Use VMs or containers where needed. |

If a method needs unavailable software or access, name it as setup in the rewrite. Do not install it during this analysis.

## Other fields worth borrowing from

- **Security:** use threat modeling to identify abuse paths through the change.
- **Manufacturing:** use poka-yoke to prevent an invalid state instead of detecting it afterward.
- **User research:** test a UI through real users who perform representative tasks.
- **Site reliability:** define service-level objectives and error budgets to make reliability measurable.
- **Epidemiology:** group failures by common exposure, such as a release, platform, or feature flag.

## Judges

- Require a regression test to fail on the old version and pass on the repaired version in CI.
- Compare a benchmark with a stored baseline on representative work. Check result correctness as well as speed.
- Replay the reported failure on each relevant platform. Verify that the repaired version removes it.
- Specify a mutation score threshold or a fuzzing duration with zero new crashes.
- For a sustained process, measure its outcome over a stated period. Examples include the build pass rate and the share of sessions without crashes.

## Targets and vetoes

- Choose a demanding target: a tenfold speed gain, a numeric p95 latency limit, zero flaky tests, or a failure class prevented by design. Select one that fits the task.
- Let these constraints veto the target: correct results, compatible public APIs, security, intact data, maintainable code, and acceptable dependency cost.

## Traps

- Do not add a framework or replace the system when a local repair meets the outcome.
- Reject tests that only exercise a mock. Reject benchmarks that only time an already warm cache when the real task requires more.
- Do not omit a difficult platform or quietly replace the requested behavior with a simpler one.
- Match the method to the evidence. A codebase without a specification cannot support a useful formal proof of that specification.
