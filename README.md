# Harness Engineering with Claude — Capstone Project

Capstone submission for the **Claude AI Engineer: Harness Engineering** program. This repository implements the core engineering harness around Claude agents: agentic control loops, context and state management strategies, team configuration, and multi-shift orchestration.

---

## Systems Overview

### [System 1 — Agentic Loop](system-1-agentic-loop/)
**Claims Intake Agent with a `stop_reason`-Driven Loop**
- Dispatches model actions deterministically based on structured API `stop_reason` (`tool_use` to continue, `end_turn` to terminate).
- Structured tool execution with per-turn audit logging and structured error taxonomy (`is_error`, `error_category`, `is_retryable`).
- Dynamic task decomposition with guardrails.

### [System 2 — Context Strategy](system-2-context-strategy/)
**Long-Conversation Context Strategy for Retail Support Copilot**
- Deterministic tool output pruning to strip redundant payload fields without LLM calls.
- Persistent, structured case-facts block to preserve critical state tokens across turns.
- Budget-constrained conversation history compression preserving active issue context.
- Final working prompt assembly and citation tracking.

### [System 3 — Claude Code Configuration](system-3-claude-code-config/)
**Claude Code Configuration for Multi-Surface Monorepo Teams**
- Modular `CLAUDE.md` architecture with path-scoped rules (`paths: "src/..."`).
- Project-scoped `/review` command with verification hooks.
- Forked read-only `deploy-check` skill (`context: fork`) with restricted tool allowlists.
- Decision framework for Plan Mode vs. Explore Mode.

### [System 4 — Orchestration](system-4-orchestrator/)
**Multi-Shift Quality Monitoring System with Claude Orchestration**
- Three-tier storage architecture (hot in-memory, warm SQLite, cold archive) keeping per-session footprint minimal.
- Per-shift invocation pipeline with deterministic stage transitions.
- Robust crash recovery with state reconciliation and truth-table verification.
- Forked scratchpads for isolated sub-agent investigations.

---

## Test Count Alignment

Verification counts and test suite reconciliation are documented in [`TEST_COUNT_ALIGNMENT.md`](TEST_COUNT_ALIGNMENT.md):

| System | Rubric Baseline | Submitted Pytest Result | Status |
|---|---:|---:|---|
| **System 1 — Agentic Loop** | 29 | 29 passed | Exact match |
| **System 2 — Context Strategy** | 17 | 30 passed | 17 core + 13 supplementary invariant tests |
| **System 3 — Claude Code Configuration** | 35 | 35 passed | Exact match |
| **System 4 — Orchestration** | 28 | 33 passed | 28 test functions (1 parameterized into 5 cases) |

---

## Evidence & Verification

- Pre-generated run traces, evaluation logs, budget metrics, and reflection briefs are available in the [`evidence/`](evidence/) directory.
- Complete packaged evidence archive: [`harness-engineering-capstone-evidence.zip`](harness-engineering-capstone-evidence.zip).