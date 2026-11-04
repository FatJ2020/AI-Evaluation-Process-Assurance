# AEPA — AI Evaluation Process Assurance

### Treating the *review process* as something that can fail (not only the model)

**Minimal portfolio prototype** · Synthetic data only · Rule-based · No API key required

> Most AI portfolios ask: “Is the model output good?”  
> AEPA also asks: **“Can we trust the evaluation that produced the score, ranking, or gate result?”**

Companion projects:
- [Industrial AI Evaluation Framework](https://github.com/FatJ2020/Industrial-AI-evaluation-framework) — evaluate industrial LLM *answers*
- [Northstar Operational AI CoPilot](https://github.com/FatJ2020/Northstar-Operational-AI-CoPilot) — govern *who decides*
- [Agent Development Lifecycle (ADL)](https://github.com/FatJ2020/agent-development-lifecycle) — risk-gated *agent release*

Together: **Evaluate → Govern → Lifecycle → Assure the evaluation itself**

---

## Why this exists

Elo rankings, pass rates and gate decisions are only as good as the review process behind them.

Evaluation-side failures (position bias, length bias, vague specs, unstable gates, low inter-rater agreement) can:
- hide real model differences, or
- create false ones

Automotive and semiconductor process control already treat *measurement systems* and *process steps* as failure objects (MSA, Control Plan, gates, severity-first prioritisation). AEPA borrows those **principles** for AI human-evaluation workflows — without pretending AI failures are as measurable as physical defects.

---

## What the minimal demo does

1. Loads synthetic **review-session records** (`data/review_sessions.jsonl`)
2. Flags **evaluation-side risks** with transparent rules
3. Assigns a simple **severity band** (H / M / L) — severity-first, not a fake-precise RPN
4. Recommends: `ACCEPT` · `RE_REVIEW` · `HOLD_BATCH`
5. Writes CSV under `reports/`

No LLM API. Pure Python standard library.

---

## Quick start

```bash
cd AEPA   # or your folder name

python src/aepa_run.py
python src/aepa_run.py --input data/review_sessions.jsonl --output reports/aepa_results.csv
python -m unittest discover -s tests -v
```

Example console output:

```text
AEPA — Evaluation Process Assurance
Evaluated 8 review sessions -> reports/aepa_results.csv

SESS-001  severity=L  flags=none                     -> ACCEPT
SESS-002  severity=H  flags=position_bias_risk       -> RE_REVIEW
SESS-003  severity=H  flags=gate_threshold_unstable  -> HOLD_BATCH
...
```

---

## Risk flags (minimal set)

| Flag | Meaning (portfolio definition) |
|------|--------------------------------|
| `position_bias_risk` | Same preferred side dominates without swap / balance evidence |
| `length_bias_risk` | Longer / more formatted output preferred without content check |
| `hard_fault_not_separated` | Preference recorded while hard-fault tags were ignored |
| `gate_threshold_unstable` | Gate used without stated false-pass / false-reject review |
| `spec_version_drift` | Session mixes unclear or conflicting spec versions |
| `agreement_unknown` | No inter-rater / gold-check signal on subjective dimensions |
| `artifact_not_verified` | Agent/coding-style result accepted on self-report only |

**Severity rule (simple, explicit):**
- Any flag in `{gate_threshold_unstable, artifact_not_verified, hard_fault_not_separated}` → **H**
- Else if any other flag → **M**
- Else → **L**

**Recommendation:**
- **H** + process-integrity flags → `HOLD_BATCH` or `RE_REVIEW`
- **M** → `RE_REVIEW`
- **L** → `ACCEPT` (still subject to normal sampling QA)

---

## Repository layout

```text
README.md
LICENSE
.gitignore
requirements.txt
data/review_sessions.jsonl
src/aepa_run.py
src/aepa_rules.py
tests/test_aepa_rules.py
docs/method_note.md
docs/interview_pitch.md
reports/.gitkeep
```

---

## Limitations (please read)

- Synthetic sessions only; not real Outlier or employer data
- Rules are illustrative, not a validated measurement system
- Not a substitute for project-specific rubrics or statistical MSA
- Does not implement full FMEA worksheets or claim ISO/IATF compliance
- Severity bands are deliberate simplifications (ranges/grades, not false-precise RPN products)


---

## License

MIT License — see [LICENSE](LICENSE).
