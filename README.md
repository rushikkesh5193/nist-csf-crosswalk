# nist-csf-crosswalk

A small Python tool that takes an **ISO/IEC 27001:2022 Annex A control assessment** and shows where you stand against **NIST Cybersecurity Framework 2.0**. It maps the 93 Annex A controls to the 22 CSF categories, computes coverage per category, gives an indicative tier, and lists the gaps against a target.

Python standard library only (tested on Python 3.13).

> **Data note.** `examples/sample_assessment.json` is **synthetic** (an invented "ExampleOrg"). Ten problems are injected on purpose so the tests can check the tool finds exactly those. Nothing here comes from a real organisation.

## Why

Many organisations already have an ISO 27001 Statement of Applicability but are asked to show a NIST CSF profile for a customer, regulator or board. This tool reuses the assessment you already have instead of starting again, and shows where the two frameworks do not line up.

## Quick start

```bash
python3 -m csf_crosswalk examples/sample_assessment.json --out-dir out    # report.md, report.json, two CSVs
python3 -m csf_crosswalk examples/sample_assessment.json --fail-on high   # exit 1 if any high issue (CI)
python3 -m unittest discover -s tests                                     # 28 tests
bash scripts/run_demo.sh                                                  # regenerate data, report, tests
```

## How it works

1. **Mapping.** Each of the 93 Annex A controls maps to 1-3 CSF 2.0 categories (`csf_crosswalk/mapping.py`). Every control is mapped; a test enforces this.
2. **Coverage.** For each category: implemented = 1.0, partial = 0.5, planned or not implemented = 0. Not-applicable controls leave the denominator. Controls with no status count as zero and are flagged. Credits are in `config.json`.
3. **Indicative tier.** Coverage of 30% or more gives Tier 2, 65% Tier 3, 95% Tier 4, otherwise Tier 1.
4. **Targets and declared tiers.** Set a `default_target`, per-category `targets`, and optionally the tier you `declared_tiers` for a category. A declared tier is used as the current tier but challenged if it is more than one above the evidence.

| Check | Raised when |
|---|---|
| `BELOW_TARGET` | Current tier is under target (high if 2 or more tiers short, else medium) |
| `CATEGORY_NOT_ASSESSED` | No mapped control has a status (high) |
| `CATEGORY_EXCLUDED` | All mapped controls are marked not applicable (medium) |
| `UNASSESSED_CONTROLS` | Some mapped controls have no status (low) |
| `DECLARED_ABOVE_EVIDENCE` | Declared tier exceeds the indicative tier by more than the margin (medium) |
| `NO_ISO_CONTROLS` | No Annex A control maps to the category (medium) |
| `UNKNOWN_CONTROL` | Control ID is not in Annex A (high) |

**A real finding from the mapping:** no Annex A control maps to `RC.CO` (recovery communication), so ISO 27001 coverage alone says nothing about it. The tool reports this instead of hiding it.

## Input format

```json
{"organisation": "ExampleOrg",
 "default_target": 3,
 "targets": {"DE.CM": 4},
 "declared_tiers": {"ID.IM": 3},
 "controls": {"A.5.1": {"status": "implemented"}, "A.5.8": {"status": "not_applicable", "justification": "..."}}}
```

Invalid categories, tiers outside 1-4 and unknown statuses are rejected with a clear message (exit code 2).

## Limitations

- **The crosswalk is my own indicative mapping at category level.** It is not an official NIST or ISO mapping. Reasonable people would map some controls differently; edit `mapping.py` to suit your view.
- **The tier is a coverage heuristic, not an official CSF Implementation Tier assessment.** Real tiers also consider process, risk management and integration, which a control checklist cannot show.
- **It trusts the statuses you give it.** It does not verify that a control is actually implemented or effective.
- **Coverage is control-count based.** Every control in a category weighs the same.
- **ISO 27001 certification needs more than Annex A** (clauses 4-10); this tool covers Annex A only.
- No persistence, UI or authentication. It reads JSON and writes reports.

## Layout

```
csf_crosswalk/  data.py  annex_a.py  mapping.py  analyse.py  report.py  config.json  __main__.py
tools/          gen_sample.py     synthetic data generator
tests/          28 tests
examples/       sample_assessment.json  report.md  report.json  csf_profile.csv  iso_to_csf_crosswalk.csv
scripts/        run_demo.sh
```
