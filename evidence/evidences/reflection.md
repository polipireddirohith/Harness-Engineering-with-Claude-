# Reflection Brief — Harness Engineering Capstone

**Name:** Ajay Kumar Vavilapalli
**Date:** 2026-09-22

**Environment**

- Model(s): `claude-haiku-4-5-20251001` for System 1; System 2 evaluation artifacts were produced using the configured Anthropic model.
- OS / Python: Linux / Python 3.13
- Approx. API spend: System 1 complete run estimated at `$0.1127`.

---

## Part 1 — Per-system

### System 1 — Agentic loop

1. **Loop control.** Quote the `stop_reason` sequence from one trace. Name the file and function that decides continue-vs-stop, and how.
   → The trace `system_1_claims_loop/trace.jsonl` shows the `stop_reason` sequence `tool_use → end_turn`: the first turn continued with tool calls, and the second turn terminated with `end_turn`. The control logic is implemented in `claims_intake/loop.py` inside `run_loop()`, where the loop continues when `response.stop_reason == "tool_use"` and returns when it is `"end_turn"`; an unexpected stop reason raises `UnexpectedStopReason`. This makes termination depend on the structured API response rather than a fixed number of turns. Artifact: `system_1_claims_loop/trace.jsonl`; implementation: `claims_intake/loop.py`.

2. **Anti-pattern.** Name one anti-pattern `test_antipatterns.py` checks for. What would break in your run if the loop used it?
   → One anti-pattern checked by `tests/test_antipatterns.py` is using string-membership tests against the model's response text to control the loop. The test checks that the loop does not use magic strings from assistant text as its stopping mechanism. If this approach were used, control flow could depend on arbitrary response wording instead of the structured `stop_reason`, making termination brittle. Artifact: `system_1_claims_loop/tests.txt` and `tests/test_antipatterns.py`.

3. **Tool design.** Pick two tools with overlapping inputs. How do the descriptions prevent misrouting? What did a structured tool error let the agent do that a generic string would not?
   → Two tools with overlapping responsibilities are `classify_claim` and `request_clarification`, because both relate to determining the claim type. Their descriptions separate the roles: `classify_claim` commits to a claim type with confidence and rationale after sufficient facts are available, while `request_clarification` is used when the claim remains genuinely ambiguous and a question is needed to distinguish possibilities. The structured tool-error response includes `is_error`, `error_category`, `is_retryable`, and `message`, allowing the agent to distinguish retryable failures from permanent ones instead of treating every failure as an unstructured string. Artifact: `claims_intake/tools.py`.

4. **Your numbers.** Quote the turn count and cost for one claim. How does it differ from the README sample, and why?
   → `claim_03_water_damage` used 7 turns and had an estimated cost of `$0.0313`, with 25,442 input tokens and 1,180 output tokens. The complete run processed 8 fixtures with an estimated total cost of `$0.1127`. The actual numbers differ from a fixed sample because token usage and turn count depend on the individual claim and the tool/clarification interactions required during the run. Artifact: `system_1_claims_loop/run_summary.md`, run `20260922_121649`.

### System 2 — Context strategy

5. **Reduction.** Quote baseline, assembled, reduction. Which section dominates and why keep verbatim?
   → The raw baseline context was 38,708 tokens, while the assembled context was 16,782 tokens, giving a 56.64% reduction. The `active` section dominated the assembled context at 15,789 tokens because it contained the current unresolved issue and needed to remain available for answerability. The resolved sections were compressed, while the active context was kept essentially verbatim because it represented the current work. Artifact: `system_2_context_strategy/budget.json`.

6. **Summarize vs preserve.** State the rule for what gets summarized versus kept byte-exact, citing per-section token numbers.
   → The context strategy compresses resolved conversation sections while preserving the information needed for the current active issue. The budget artifact shows 204 tokens for the case-facts block, 378 tokens for resolved-refund, 429 tokens for resolved-subscription, and 15,789 tokens for the active section. The compression calls reduced the refund section from 12,334 input tokens to 365 output tokens and the subscription section from 11,475 to 416. This preserves the current active context while substantially reducing historical conversation overhead. Artifact: `system_2_context_strategy/budget.json`.

7. **Facts block.** Compare `eval.jsonl` versus control. Which question regressed, and what proves it?
   → The assembled-context evaluation in `eval.jsonl` correctly answered the structured payment-method status question with the exact token `in_progress`, and the evaluation passed. In contrast, the control variant in `eval_control.jsonl`, where the persistent facts block was removed, failed that question because the model stated that no structured status token was available. This shows that the persistent facts block preserved structured information that was necessary to answer the active issue correctly. Artifacts: `system_2_context_strategy/eval.jsonl` and `system_2_context_strategy/eval_control.jsonl`.

### System 3 — Claude Code configuration

8. **Path-scoped rules.** Quote the glob frontmatter. Why is this better than a directory-level CLAUDE.md for cross-cutting conventions?
   → The React rule uses path-scoped YAML frontmatter with `paths: "src/components/**/*"` and `paths: "src/pages/**/*"`. This makes the convention load specifically when relevant React component or page files are edited, rather than applying broadly to an entire directory hierarchy. It is useful for cross-cutting conventions because activation is based on the files being worked on. Artifact: `system_3_claude_config/.claude/rules/react.md`.

9. **Forked skill.** Quote `context: fork` and the allowed-tools set. What does forked plus read-only buy? What breaks without it?
   → The deploy-check skill declares `context: fork` and uses read-only tools including `Read`, `Grep`, `Glob`, and restricted Git/GitHub commands such as `git status`, `git diff`, `git log`, and `gh pr checks`. The fork keeps verbose investigation output isolated from the main session, while the read-only allowlist prevents modification, push, deployment, or migration actions. Without these boundaries, an investigation would have a larger context and action blast radius. Artifact: `system_3_claude_config/.claude/skills/deploy-check/SKILL.md`.

10. **Scope.** What does the validator output say? Give a project-level and user-level scope example.
   → The configuration validator reports `OK`, confirming the submitted project configuration passes its validation. The project-level skill is `.claude/skills/deploy-check/SKILL.md`, which applies within the repository. The configuration also documents a user-level example at `~/.claude/skills/deploy-check-strict/`, which would be personal to one user's environment rather than shared project configuration. Artifact: `system_3_claude_config/validator.txt` and `.claude/skills/deploy-check/SKILL.md`.

### System 4 — Orchestration

11. **Push work down.** Defects SQL query returned versus warm-tier total. Name the indexed query. Why does the model never see full history?
   → The warm tier uses `SELECT * FROM defects WHERE ts > ? ORDER BY ts DESC LIMIT ?` in `WarmStore.defects_since()`, so filtering and limiting happen in SQLite rather than in Python. The schema defines an index on `defects(ts)` as `idx_defects_ts`, supporting the timestamp lookup. My shift run processed 3 new defects, while the warm tier retains broader historical state; the model receives only the SQL-filtered slice needed for the current shift rather than the full history. Artifact: `shift_monitor/warm.py`; run evidence: `system_4_orchestration/shift_run.md`.

12. **Crash recovery.** Explain the resume-vs-fresh decision and staleness threshold. Why can fresh be more reliable?
   → The recovery logic uses a 30-minute staleness threshold, defined as `STALE_RESUME_THRESHOLD_MINUTES = 30` in `shift_monitor/recovery.py`. A partial run inside this window can be resumed because it is still considered part of the same shift's working set; an older partial run is treated as stale and starts fresh, with findings already captured in the manifest injected as a summary. A fresh start can therefore be more reliable than resuming stale state because it avoids continuing from an outdated working set while preserving useful findings already recorded. Artifact: `shift_monitor/recovery.py`.

13. **Small state.** Quote the hot-state byte size. Why does the budget matter for indefinite once-per-shift operation?
   → After my System 4 shift run, `data/hot_state.json` was 672 bytes, which is well below the approximately 5 KB budget. Keeping hot state small matters because this state is carried forward across shifts; a bounded state prevents persistent context from growing indefinitely and keeps each new shift's starting context manageable. The design separates compact hot state from larger warm-tier history stored in SQLite. Artifact: `system_4_orchestration/hot_state_size.txt` and `system_4_orchestration/hot_state.json`.

---

## Part 2 — Synthesis

14. **Three layers.** Locate Model, Harness, and Orchestration in named files.
   → The Model layer is represented by the Claude API interaction in `system-1-agentic-loop/claims_intake/client.py` and the model-driven decisions in the claims loop. The Harness layer is represented by `system-3-claude-config/.claude/`, including path-scoped rules, the `/review` command, and the forked deploy-check skill. The Orchestration layer is represented by System 4's `shift_monitor/pipeline.py`, `warm.py`, and `recovery.py`, which manage shift state, SQL-filtered retrieval, and crash recovery. These files show the separation between model behavior, deterministic control/configuration, and multi-session state management.

15. **Deterministic vs prompt.** Give one deterministic behavior and one prompt-guided behavior. When is each right?
   → A deterministic behavior is the System 1 terminal condition in `claims_intake/loop.py`: the harness continues on `tool_use` and terminates on `end_turn`, so this behavior is enforced by code rather than left to model wording. Another deterministic example is System 3's read-only `allowed-tools` list in `.claude/skills/deploy-check/SKILL.md`. In contrast, tool descriptions in `claims_intake/tools.py` provide prompt-based guidance about when tools such as `classify_claim` or `request_clarification` should be used. Deterministic enforcement is appropriate when violating the rule could break or broaden system behavior; prompt guidance is appropriate when the model needs judgment among valid options.

16. **Context two faces.** Compare System 2 intra-session context versus System 4 cross-session context with numbers.
   → System 2 manages context within a session by compressing resolved conversation history while preserving the active issue and persistent facts. Its budget run reduced the baseline from 38,708 tokens to 16,782, a 56.64% reduction. System 4 manages context across shifts by keeping compact hot state while storing historical defects in the warm SQLite tier; my hot-state artifact was 672 bytes after the shift run. These show two forms of context management: reducing the active conversation window and preventing persistent cross-session state from growing without bound. Artifacts: `system_2_context_strategy/budget.json` and `system_4_orchestration/hot_state_size.txt`.

17. **Reliability you can't see in one run.** Name a test-guaranteed behavior that a single successful run would not reveal.
   → A behavior guaranteed by the automated tests but not necessarily visible from one successful execution is the System 1 anti-pattern protection in `tests/test_antipatterns.py`. The tests verify that the loop does not use assistant-text string matching or a fixed integer iteration limit as its primary stopping mechanism. A single successful run could appear correct even if such brittle control logic were present, whereas the test suite checks the implementation itself. Artifact: `system_1_claims_loop/tests.txt`.

18. **Blast radius.** Pick a system, describe its blast radius and kill switch, grounded in enforcement.
   → System 3 provides a clear blast-radius boundary through the `deploy-check` skill's read-only `allowed-tools` list. The skill can inspect files and run restricted Git/GitHub commands, but it does not have modification, push, deployment, or migration capabilities. Its `context: fork` setting also isolates the investigation context from the main session. This gives the harness a concrete safety boundary: even if the investigation makes an incorrect judgment, its available actions are constrained and its investigation context is isolated. Artifact: `system_3_claude_config/.claude/skills/deploy-check/SKILL.md`.

---

## Part 3 — Honest assessment

19. **What broke.** Name one thing that failed first try and how you fixed it.
   → System 1 initially failed because `anthropic 0.39.0` was incompatible with the installed `httpx 0.28.1`, producing `Client.__init__() got an unexpected keyword argument 'proxies'`. I fixed the environment by installing `httpx<0.28`, which installed `httpx 0.27.2` and allowed the tests and run to complete. This demonstrated that reproducible harness work depends on compatible dependency versions as well as application logic. Artifact: System 1 run environment and `system_1_agentic_loop/run_summary.md`.

20. **What you'd change.** Name one architectural decision you would make differently, grounded in an observation.
   → I would make the evidence-generation workflow part of the project structure from the beginning rather than organizing evidence after completing the four systems. The systems were completed successfully, but preparing the exact evaluator evidence structure afterward required additional organization. I would add a verification step to each system that produces the required test log, run artifact, and supporting measurements immediately after a successful run. This would make the final submission more reproducible and reduce the risk of missing evaluator-required artifacts.


---

## Test-count alignment note

The rubric baseline verification count is 29 + 17 + 35 + 28. The submitted implementation has 29, 30, 35, and 33 pytest cases respectively. System 2 contains the 17 core requirement checks plus 13 supplementary invariant/anti-pattern/token checks. System 4 contains 28 named test functions; its parameterized recovery truth-table test expands to five pytest cases, producing 33 collected cases. These additional checks were retained for reliability and are documented in the corresponding `TEST_MANIFEST.md` files and the root `TEST_COUNT_ALIGNMENT.md`.
