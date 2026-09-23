# Shift Run Evidence

Command executed:

`python -m shift_monitor run-shift --shift C --warm-db data/warm.sqlite --hot-state data/hot_state.json --scratchpad data/scratchpad.md --recorded-response fixtures/recorded_responses/shift_C_2026-04-30.json`

Observed run output:

```text
run_shift start: shift=C since=2026-09-22T04:56:07Z
run_shift done: shift=C new=3
shift C: 3 new defects
SELECT * FROM defects
WHERE ts > ?
ORDER BY ts DESC
LIMIT ?
The warm-tier query applies the timestamp filter and row limit in SQL rather than loading the full defect history and filtering it in Python.

The warm database used for this run contained 3 seeded defects, and the Shift C run reported 3 new defects from the SQL-filtered slice.

Recorded response:

Shift C 2026-04-30: 3 high + 2 medium defects on capacitor-bank-C-7, all from lot 2026-0430-B (DAR 0.39, ESR ~19 mOhm); 1 low VP-4 vent squeal (repeat). Lot quarantine recommended.
