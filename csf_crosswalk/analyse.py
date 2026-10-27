"""Score NIST CSF 2.0 coverage from ISO 27001 control status and compare it with target tiers.

The 'indicative tier' is a transparent heuristic based on control coverage. It is NOT an official CSF
Implementation Tier: the CSF Tiers describe the rigour of governance and risk-management practice, which
control status alone cannot show. A declared tier, if you provide one, takes precedence.
"""
from __future__ import annotations

import json
from pathlib import Path

from .annex_a import CONTROLS
from .data import CATEGORIES, FUNCTIONS, TIERS
from .mapping import controls_for, ISO_TO_CSF

STATUSES = ("implemented", "partial", "planned", "not_implemented", "not_applicable")
SEV_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def load_config(path=None):
    p = Path(path) if path else Path(__file__).with_name("config.json")
    return json.loads(p.read_text(encoding="utf-8"))


def indicative_tier(coverage, cfg):
    """Map coverage % to a tier 1-4 using the thresholds in the config. None stays None."""
    if coverage is None:
        return None
    t = cfg["indicative_tier_min_coverage"]
    if coverage >= t["4"]:
        return 4
    if coverage >= t["3"]:
        return 3
    if coverage >= t["2"]:
        return 2
    return 1


def _issue(sev, area, ref, check, title, detail, action):
    return {"severity": sev, "area": area, "ref": ref, "check": check, "title": title, "detail": detail, "action": action}


def _validate(data):
    for cat, t in {**data.get("targets", {}), **data.get("declared_tiers", {})}.items():
        if cat not in CATEGORIES:
            raise ValueError(f"unknown CSF category {cat!r}")
        if t not in TIERS:
            raise ValueError(f"{cat}: tier must be 1..4, got {t!r}")
    for cid, c in data.get("controls", {}).items():
        if cid in CONTROLS and c.get("status") not in STATUSES:
            raise ValueError(f"{cid}: status must be one of {STATUSES}, got {c.get('status')!r}")


def analyse(data, cfg=None):
    cfg = cfg or load_config()
    _validate(data)
    given = data.get("controls", {})
    targets, declared = data.get("targets", {}), data.get("declared_tiers", {})
    default_target = data.get("default_target", cfg["default_target_tier"])
    if default_target not in TIERS:
        raise ValueError(f"default_target must be 1..4, got {default_target!r}")

    issues = []
    for cid in given:
        if cid not in CONTROLS:
            issues.append(_issue("high", "control", cid, "UNKNOWN_CONTROL", "Control ID is not in ISO 27001:2022 Annex A",
                                 f"'{cid}' is not one of the 93 Annex A controls (2013-era numbering?).", "Re-map to the 2022 numbering."))

    cats = []
    for cat, name in CATEGORIES.items():
        mapped = controls_for(cat)
        status = {c: given[c]["status"] if c in given and c in CONTROLS else "unassessed" for c in mapped}
        applicable = [c for c in mapped if status[c] not in ("not_applicable",)]
        unassessed = [c for c in applicable if status[c] == "unassessed"]
        assessed = [c for c in applicable if status[c] != "unassessed"]
        credit = sum(cfg["status_credit"].get(status[c], 0) for c in applicable)
        coverage = round(100 * credit / len(applicable), 1) if applicable else None
        ind = indicative_tier(coverage, cfg) if applicable and assessed else None
        if declared.get(cat) is not None:
            current, basis = declared[cat], "declared"
        else:
            current, basis = ind, "indicative"
        target = targets.get(cat, default_target)
        gap = None if current is None else max(0, target - current)
        cats.append({"id": cat, "function": FUNCTIONS[cat.split(".")[0]], "name": name, "mapped": len(mapped),
                     "applicable": len(applicable), "implemented": sum(status[c] == "implemented" for c in applicable),
                     "unassessed": len(unassessed), "coverage": coverage, "indicative_tier": ind,
                     "declared_tier": declared.get(cat), "current": current, "basis": basis, "target": target, "gap": gap})
        ref = f"{cat} {name}"
        if not mapped:
            issues.append(_issue("medium" if target >= 2 else "low", "category", cat, "NO_ISO_CONTROLS",
                                 f"{ref}: no ISO 27001 control maps here",
                                 "Annex A has no control that clearly addresses this CSF category.",
                                 "Cover it with a supplementary procedure and keep evidence outside the SoA."))
            continue
        if not applicable:
            issues.append(_issue("medium", "category", cat, "CATEGORY_EXCLUDED", f"{ref}: every mapped control is excluded",
                                 f"All {len(mapped)} mapped controls are marked not applicable.", "Confirm the exclusions are intended and justified."))
            continue
        if not assessed:
            issues.append(_issue("high", "category", cat, "CATEGORY_NOT_ASSESSED", f"{ref}: not assessed",
                                 f"None of the {len(applicable)} mapped controls has a status.", "Assess the mapped controls first."))
            continue
        if unassessed:
            issues.append(_issue("low", "category", cat, "UNASSESSED_CONTROLS", f"{ref}: some controls not assessed",
                                 f"{len(unassessed)} of {len(applicable)} mapped controls have no status ({', '.join(unassessed)}).",
                                 "Assess them; they count as zero coverage until then."))
        if gap:
            issues.append(_issue("high" if gap >= 2 else "medium", "category", cat, "BELOW_TARGET",
                                 f"{ref}: below target tier",
                                 f"Current tier {current} ({TIERS[current]}, {basis}), target {target} ({TIERS[target]}), coverage {coverage}%.",
                                 "Close the control gaps listed in the roadmap."))
        if declared.get(cat) is not None and ind is not None and declared[cat] > ind + cfg["declared_tier_margin"]:
            issues.append(_issue("medium", "category", cat, "DECLARED_ABOVE_EVIDENCE", f"{ref}: declared tier looks too high",
                                 f"Declared tier {declared[cat]} but control coverage ({coverage}%) indicates tier {ind}.",
                                 "Provide evidence for the declared tier or lower it."))

    funcs = []
    for code, fname in FUNCTIONS.items():
        rows = [c for c in cats if c["id"].startswith(code + ".")]
        covs = [c["coverage"] for c in rows if c["coverage"] is not None]
        funcs.append({"id": code, "name": fname, "categories": len(rows),
                      "avg_coverage": round(sum(covs) / len(covs), 1) if covs else None,
                      "below_target": sum(1 for c in rows if c["gap"]), "no_iso_controls": sum(1 for c in rows if c["mapped"] == 0)})
    roadmap = sorted((c for c in cats if c["gap"]), key=lambda c: (-c["gap"], c["coverage"] if c["coverage"] is not None else -1, c["id"]))
    issues.sort(key=lambda i: (SEV_ORDER[i["severity"]], i["ref"], i["check"]))
    return {"categories": cats, "functions": funcs, "issues": issues, "roadmap": roadmap}
