# AEPA Method Note (minimal)

## Generation-side vs evaluation-side

| Side | Examples |
|------|----------|
| Generation | Hallucination, dropped words, false task-completion, wrong tool args |
| Evaluation | Position bias, length bias, untagged hard faults, unstable gates, unknown agreement |

AEPA only scores **evaluation-side** process risks on synthetic review sessions.

## Severity-first (not RPN product)

Automotive AIAG-VDA practice moved emphasis toward Action Priority rather than raw RPN products, partly because multiplying scales can hide high-severity rare events.  
For AI evaluation, samples are small and subjective dimensions are common — so AEPA uses **H / M / L bands** driven first by integrity flags, not a pseudo-precise numeric RPN.

## What we deliberately did not claim

- Full DFMEA/PFMEA worksheets  
- Statistical MSA study on real annotators  
- Project-specific Outlier rubrics or thresholds  
- Production readiness  

## Borrowed ideas (principle-level)

- MSA → measure agreement before trusting scores  
- Gate / hold point → unstable gate ⇒ HOLD_BATCH  
- Control plan → explicit flags and ruling logic  
- Severity-first prioritisation → integrity flags outrank cosmetic issues  
