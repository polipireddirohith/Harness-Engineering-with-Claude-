# Evidence Directory — Harness Engineering Capstone

This directory maps each required submission artifact to its location in the repository.

| System | Required Artifact | Path |
|--------|------------------|------|
| System 1 — Agentic Loop | Run summary (all 8 claims, terminal outcomes) | `evidences/system_1_claims_loop/run_summary.md` |
| System 1 — Agentic Loop | Full tool-call trace (claim_04_neighbor_injury) | `evidences/system_1_claims_loop/trace.jsonl` |
| System 1 — Agentic Loop | Test output (29 passed) | `evidences/system_1_claims_loop/tests.txt` |
| System 1 — Agentic Loop | Test manifest | `evidences/system_1_TEST_MANIFEST.md` |
| System 2 — Context Strategy | Budget + token counts | `evidences/system_2_context_strategy/budget.json` |
| System 2 — Context Strategy | Eval results (full vs compressed context) | `evidences/system_2_context_strategy/eval.jsonl` |
| System 2 — Context Strategy | Control eval (baseline) | `evidences/system_2_context_strategy/eval_control.jsonl` |
| System 2 — Context Strategy | Test output (30 passed) | `evidences/system_2_context_strategy/tests.txt` |
| System 2 — Context Strategy | Test manifest | `evidences/system_2_TEST_MANIFEST.md` |
| System 3 — Claude Config | CLAUDE.md | `evidences/system_3_claude_config/CLAUDE.md` |
| System 3 — Claude Config | Validator output | `evidences/system_3_claude_config/validator.txt` |
| System 3 — Claude Config | Rules directory | `evidences/system_3_claude_config/.claude/` |
| System 3 — Claude Config | Test output (35 passed) | `evidences/system_3_claude_config/tests.txt` |
| System 3 — Claude Config | Test manifest | `evidences/system_3_TEST_MANIFEST.md` |
| System 4 — Orchestration | Shift run log | `evidences/system_4_orchestration/shift_run.md` |
| System 4 — Orchestration | Hot state size proof | `evidences/system_4_orchestration/hot_state_size.txt` |
| System 4 — Orchestration | Fork/fanout evidence | `evidences/system_4_orchestration/fork_evidence.md` |
| System 4 — Orchestration | Test output (33 passed) | `evidences/system_4_orchestration/tests.txt` |
| System 4 — Orchestration | Test manifest | `evidences/system_4_TEST_MANIFEST.md` |
| All Systems | Student reflection (20 Q&A) | `evidences/reflection.md` |

## Evidence Highlights

### System 1 — Agentic Loop (System Prompt + Guardrail)

All 8 fixture claims terminate in a routing decision (`routed`) or a human escalation (`escalated`). The
system prompt's **Mandatory Terminal Tool Contract** (added in `system_prompt.py`) explicitly requires the
model to call either `route_to_adjuster` or `escalate_to_human` before `end_turn`. A guardrail in
`run.py` detects any claim where `session.terminal_called` is False and re-prompts the model to complete
the terminal step.

- `claim_06_low_confidence_escalation` → **escalated** (confidence below 0.6 after clarification)
- All other 7 claims → **routed** to the appropriate adjuster queue

### System 2 — Context Strategy

The `retail_context` compression pipeline reduces the conversation context by **56.64%** (from ~7,200 to
~3,120 tokens on average across the product catalog use case) while preserving answer quality — answerability
score remains at 1.0 across all compressed eval queries.

### System 3 — Claude Config

All `@import`-based rule files resolve correctly. The `validator.txt` shows **OK** for all paths. Path-scoped
`.claude/rules/` are structured per-project under `ecommerce_team_config`.

### System 4 — Orchestration

`WarmStore.defects_since()` pushes date-range filtering into SQLite, keeping the hot state under 10 KB.
Fork/fanout is evidenced for parallel alert routing in `fork_evidence.md`.
