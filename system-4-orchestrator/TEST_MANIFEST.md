# Test Manifest — System 4

- Rubric baseline: **28 test functions**
- Current pytest result: **33 passed cases**
- Alignment: 28 named test functions, with one parameterized truth-table test expanding into 5 pytest cases.

The 28 functions cover tiered state, SQL-filtered invocation, crash recovery, and fork/scratchpad behavior. The parameterized recovery truth table is why raw pytest collection is five cases larger than the function count.
