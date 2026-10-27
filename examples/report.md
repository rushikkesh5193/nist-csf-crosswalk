# NIST CSF 2.0 Profile: ExampleOrg Pvt Ltd (synthetic)

Coverage comes from ISO/IEC 27001:2022 control status through an **indicative** crosswalk. The tiers shown are a heuristic based on coverage unless a tier was declared; they are not an official CSF assessment.

## Summary

- Issues: 0 critical, 5 high, 4 medium, 1 low
- Categories below target: 4 of 22

| Function | Categories | Avg coverage % | Below target | No ISO control |
|---|---|---|---|---|
| Govern | 6 | 96.0 | 0 | 0 |
| Identify | 3 | 61.1 | 0 | 0 |
| Protect | 5 | 76.9 | 0 | 0 |
| Detect | 2 | 75.0 | 1 | 0 |
| Respond | 4 | 56.2 | 2 | 0 |
| Recover | 2 | 50.0 | 1 | 1 |

## Categories

| Category | Name | Mapped | Coverage % | Current | Target | Gap |
|---|---|---|---|---|---|---|
| GV.OC | Organizational Context | 2 | 100.0 | 4 Adaptive (indicative) | 3 Repeatable | 0 |
| GV.RM | Risk Management Strategy | 1 | - | - (indicative) | 3 Repeatable | - |
| GV.RR | Roles, Responsibilities, and Authorities | 6 | 100.0 | 4 Adaptive (indicative) | 3 Repeatable | 0 |
| GV.PO | Policy | 3 | 100.0 | 4 Adaptive (indicative) | 3 Repeatable | 0 |
| GV.OV | Oversight | 2 | 100.0 | 4 Adaptive (indicative) | 3 Repeatable | 0 |
| GV.SC | Cybersecurity Supply Chain Risk Management | 6 | 80.0 | 3 Repeatable (indicative) | 2 Risk Informed | 0 |
| ID.AM | Asset Management | 3 | 100.0 | 4 Adaptive (indicative) | 3 Repeatable | 0 |
| ID.RA | Risk Assessment | 3 | 83.3 | 3 Repeatable (indicative) | 3 Repeatable | 0 |
| ID.IM | Improvement | 1 | 0.0 | 3 Repeatable (declared) | 3 Repeatable | 0 |
| PR.AA | Identity Management, Authentication, and Access Control | 13 | 100.0 | 4 Adaptive (indicative) | 3 Repeatable | 0 |
| PR.AT | Awareness and Training | 1 | 0.0 | - (indicative) | 3 Repeatable | - |
| PR.DS | Data Security | 15 | 100.0 | 4 Adaptive (indicative) | 3 Repeatable | 0 |
| PR.PS | Platform Security | 17 | 97.1 | 4 Adaptive (indicative) | 3 Repeatable | 0 |
| PR.IR | Technology Infrastructure Resilience | 12 | 87.5 | 3 Repeatable (indicative) | 3 Repeatable | 0 |
| DE.CM | Continuous Monitoring | 3 | 50.0 | 2 Risk Informed (indicative) | 4 Adaptive | 2 |
| DE.AE | Adverse Event Analysis | 2 | 100.0 | 4 Adaptive (indicative) | 3 Repeatable | 0 |
| RS.MA | Incident Management | 2 | 75.0 | 3 Repeatable (indicative) | 3 Repeatable | 0 |
| RS.AN | Incident Analysis | 1 | 0.0 | 1 Partial (indicative) | 3 Repeatable | 2 |
| RS.CO | Incident Response Reporting and Communication | 1 | 100.0 | 4 Adaptive (indicative) | 3 Repeatable | 0 |
| RS.MI | Incident Mitigation | 1 | 50.0 | 2 Risk Informed (indicative) | 3 Repeatable | 1 |
| RC.RP | Incident Recovery Plan Execution | 4 | 50.0 | 2 Risk Informed (indicative) | 4 Adaptive | 2 |
| RC.CO | Incident Recovery Communication | 0 | - | - (indicative) | 3 Repeatable | - |

## Issues

### High (5)

| Ref | Check | Detail | Action |
|---|---|---|---|
| A.9.4.1 | UNKNOWN_CONTROL | 'A.9.4.1' is not one of the 93 Annex A controls (2013-era numbering?). | Re-map to the 2022 numbering. |
| DE.CM | BELOW_TARGET | Current tier 2 (Risk Informed, indicative), target 4 (Adaptive), coverage 50.0%. | Close the control gaps listed in the roadmap. |
| PR.AT | CATEGORY_NOT_ASSESSED | None of the 1 mapped controls has a status. | Assess the mapped controls first. |
| RC.RP | BELOW_TARGET | Current tier 2 (Risk Informed, indicative), target 4 (Adaptive), coverage 50.0%. | Close the control gaps listed in the roadmap. |
| RS.AN | BELOW_TARGET | Current tier 1 (Partial, indicative), target 3 (Repeatable), coverage 0.0%. | Close the control gaps listed in the roadmap. |

### Medium (4)

| Ref | Check | Detail | Action |
|---|---|---|---|
| GV.RM | CATEGORY_EXCLUDED | All 1 mapped controls are marked not applicable. | Confirm the exclusions are intended and justified. |
| ID.IM | DECLARED_ABOVE_EVIDENCE | Declared tier 3 but control coverage (0.0%) indicates tier 1. | Provide evidence for the declared tier or lower it. |
| RC.CO | NO_ISO_CONTROLS | Annex A has no control that clearly addresses this CSF category. | Cover it with a supplementary procedure and keep evidence outside the SoA. |
| RS.MI | BELOW_TARGET | Current tier 2 (Risk Informed, indicative), target 3 (Repeatable), coverage 50.0%. | Close the control gaps listed in the roadmap. |

### Low (1)

| Ref | Check | Detail | Action |
|---|---|---|---|
| GV.SC | UNASSESSED_CONTROLS | 1 of 5 mapped controls have no status (A.5.23). | Assess them; they count as zero coverage until then. |

## Remediation roadmap (largest gap first)

1. **RS.AN Incident Analysis**: tier 1 to 3 (coverage 0.0%).
2. **DE.CM Continuous Monitoring**: tier 2 to 4 (coverage 50.0%).
3. **RC.RP Incident Recovery Plan Execution**: tier 2 to 4 (coverage 50.0%).
4. **RS.MI Incident Mitigation**: tier 2 to 3 (coverage 50.0%).
