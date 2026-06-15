# TRACE-HIX v0.2 Engineering Notes

This branch implements the PDF formalization as engineering assets.

Key design choices:

1. DRL actual trace is immutable and must exist before explanation.
2. Explanation output is bounded to summary, why-selected, why-not-alternatives, uncertainty, residual questions, counterfactual-only notes, refs, and claim atoms.
3. Claim atoms provide typed, support-referenced verification units.
4. Hard gates fail closed. Soft scores are reserved for future training/evaluation ranking.
5. Forbidden output scanning applies to explanation outputs. Input bundle governance metadata may declare boundary information.
6. Authority leakage and new decision leakage must remain zero.
