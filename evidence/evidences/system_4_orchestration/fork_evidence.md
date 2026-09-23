# Fork Isolation and Scratchpad Merge Evidence

Source test:
`tests/test_us04_fork_scratchpad.py`

The fork/scratchpad test verifies that:

- A pre-existing main-session finding is preserved.
- Fork A contributes `fork A finding 1` and `fork A finding 2`.
- Fork B contributes `fork B finding 1`.
- The merged scratchpad contains all of these findings.
- Merge order is deterministic: the pre-existing main entry appears first, followed by fork entries in input order.

Assertions from the test verify:

- `"pre-existing finding"` is present.
- `"fork A finding 1"` is present.
- `"fork A finding 2"` is present.
- `"fork B finding 1"` is present.
- The first merged conclusion is `"pre-existing finding"`.

This demonstrates that fork findings are merged back into the scratchpad without replacing the existing main-session finding.
