# Example: Intermittent Checkout Total Regression

## Example User Request

"Diagnose why the checkout total is sometimes one cent too high after a coupon is removed. Do not guess at the fix."

## Relevant Context

- Fictional app: `MarketBox`, a small commerce service.
- The bug is visible through the public checkout API.
- A recent change moved discount rounding from the cart layer to the pricing layer.
- The user can provide one anonymized request payload that reproduced the issue once.

## How The Skill Should Proceed

1. Build a fast feedback loop by replaying the anonymized checkout payload against the local API or pricing function.
2. Raise the reproduction rate if the failure is intermittent: repeat the same payload, seed time and random values, and compare expected vs actual cents.
3. Confirm the loop matches the user's symptom: coupon removal causes the total to be one cent too high.
4. Generate 3-5 ranked falsifiable hypotheses, such as duplicate rounding, stale coupon state, or tax calculation order.
5. Add targeted instrumentation with a unique debug prefix at boundaries that distinguish the hypotheses.
6. Convert the minimized replay into a regression test at the public checkout/pricing seam before applying the fix.
7. Remove all debug instrumentation and rerun both the regression test and the original replay loop.

## Expected Output Shape

- Reproduction command and observed failure rate.
- Ranked hypotheses with predictions.
- Instrumentation summary and the hypothesis it tested.
- Minimal fix summary.
- Regression test location and validation command.
- Cleanup confirmation, including debug-prefix search.

## Validation Or Review Notes

- The original replay should fail before the fix and pass after the fix.
- The regression test should assert the final observable total, not private rounding helper calls.
- If no correct test seam exists, the output should state that and flag the architecture limitation separately.

## Common Mistakes The Skill Prevents

- Fixing the first plausible rounding line without reproducing the failure.
- Testing a different bug because the replay payload does not include coupon removal.
- Adding broad logs that cannot distinguish hypotheses.
- Leaving temporary debug output in the codebase.
