# Plan Mode vs Direct Execution

## 1. Plan Mode

Use plan mode when a change crosses multiple files, has unclear dependencies, or requires investigation before implementation. For example, a change involving the files `docs/plan-mode-vs-direct-execution.md`, `tests/test_us05_plan_mode_doc.py`, and `tests/test_us05_plan_mode_doc.py` should be planned first. The goal is to understand the affected surfaces, dependencies, and validation steps and to prevent costly rework.

## 2. Direct Execution

Use direct execution for a small, well-scoped change whose behavior and location are already clear. For example, updating one function in `ecommerce_team_config/plan_mode_doc.py` is appropriate when the required behavior is known. This is a one-function change rather than a broad architectural investigation.

## 3. Explore

Use an Explore-style investigation when the main task is discovery. Isolate verbose discovery output out of the main working context so the primary task stays focused. Record useful findings in a scratchpad (Playbook) so the investigation can be reviewed without repeatedly carrying all discovery output forward.

## 4. Combined Workflow

A combined workflow uses plan-mode investigation → direct execution: first investigate the affected files and dependencies, then switch to direct execution for the well-scoped implementation once the plan is clear.

## 5. Curriculum Reference

The curriculum includes Knight-Webb's “SWE Is Becoming Plan and Review” as an anchor-talk/module 8 reference. The planning approach here follows that plan-and-review framing: investigate and establish the intended change before executing a focused implementation.
