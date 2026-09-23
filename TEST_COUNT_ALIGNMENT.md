# Test Count Alignment Note

The capstone rubric specifies the baseline verification counts as **29 + 17 + 35 + 28**. The submitted implementations contain additional verification coverage, so the raw pytest collection counts are not identical to those baseline numbers. This note makes the evolution explicit rather than presenting the larger suite as if it were the original rubric count.

| System | Rubric baseline | Submitted pytest result | Explanation |
|---|---:|---:|---|
| System 1 — Agentic Loop | 29 | 29 passed | Matches the baseline exactly. |
| System 2 — Context Strategy | 17 | 30 passed | 17 core requirement tests are supplemented by 13 additional tests covering anti-patterns, token methodology, case-fact schema/error handling, and related invariants. |
| System 3 — Claude Code Configuration | 35 | 35 passed | Matches the evaluated implementation suite. The old README line saying 28 was stale and has been corrected. |
| System 4 — Orchestration | 28 | 33 passed | The suite has 28 test functions. One parameterized recovery test expands into 5 pytest cases, so pytest reports 33 collected cases. |

## System 2: 17 core + 13 supplementary

The 17 core tests are the primary behavior checks for transcript handling (5), pruning (4), assembly (3), compression (4), plus one case-facts schema check (1). The 13 supplementary tests are the five anti-pattern checks, four additional case-facts checks, and four token-counting/methodology checks.

The supplementary tests are intentionally retained: they protect implementation invariants that a single successful end-to-end run would not prove. They are not being removed merely to make the count match the rubric.

## System 4: 28 functions vs 33 collected cases

System 4 contains 28 named `test_*` functions. `test_recovery_decide_truth_table` is parameterized and produces five pytest cases, which accounts for the difference between 28 test functions and the 33 cases reported by pytest.

This distinction is now documented in the project and evidence package so the evaluator can reconcile the submitted output with the rubric baseline.
