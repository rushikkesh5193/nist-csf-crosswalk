from __future__ import annotations

import csv
import io
import json

from .annex_a import CONTROLS
from .data import TIERS
from .mapping import ISO_TO_CSF


def _t(n):
    return "-" if n is None else f"{n} {TIERS[n]}"


def profile_csv(res):
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["Category", "Function", "Name", "Mapped controls", "Applicable", "Coverage %", "Current tier", "Basis", "Target tier", "Gap"])
    for c in res["categories"]:
        w.writerow([c["id"], c["function"], c["name"], c["mapped"], c["applicable"], "" if c["coverage"] is None else c["coverage"],
                    "" if c["current"] is None else c["current"], c["basis"], c["target"], "" if c["gap"] is None else c["gap"]])
    return buf.getvalue()


def crosswalk_csv():
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["ISO 27001:2022 control", "Title", "NIST CSF 2.0 categories (indicative)"])
    for cid, cats in ISO_TO_CSF.items():
        w.writerow([cid, CONTROLS[cid]["title"], " ".join(cats)])
    return buf.getvalue()


def to_json(res, org):
    return json.dumps({"organisation": org, **res}, indent=2)


def to_markdown(res, org):
    sev = {s: sum(i["severity"] == s for i in res["issues"]) for s in ("critical", "high", "medium", "low")}
    L = [f"# NIST CSF 2.0 Profile: {org}", "",
         "Coverage comes from ISO/IEC 27001:2022 control status through an **indicative** crosswalk. The tiers shown are a heuristic "
         "based on coverage unless a tier was declared; they are not an official CSF assessment.", "",
         "## Summary", ""]
    L.append(f"- Issues: {sev['critical']} critical, {sev['high']} high, {sev['medium']} medium, {sev['low']} low")
    L.append(f"- Categories below target: {len(res['roadmap'])} of {len(res['categories'])}", )
    L += ["", "| Function | Categories | Avg coverage % | Below target | No ISO control |", "|---|---|---|---|---|"]
    for f in res["functions"]:
        L.append(f"| {f['name']} | {f['categories']} | {'-' if f['avg_coverage'] is None else f['avg_coverage']} | {f['below_target']} | {f['no_iso_controls']} |")
    L += ["", "## Categories", "", "| Category | Name | Mapped | Coverage % | Current | Target | Gap |", "|---|---|---|---|---|---|---|"]
    for c in res["categories"]:
        L.append(f"| {c['id']} | {c['name']} | {c['mapped']} | {'-' if c['coverage'] is None else c['coverage']} | {_t(c['current'])} ({c['basis']}) | {_t(c['target'])} | {'-' if c['gap'] is None else c['gap']} |")
    L += ["", "## Issues", ""]
    if not res["issues"]:
        L += ["No issues.", ""]
    for s in ("critical", "high", "medium", "low"):
        g = [i for i in res["issues"] if i["severity"] == s]
        if g:
            L += [f"### {s.capitalize()} ({len(g)})", "", "| Ref | Check | Detail | Action |", "|---|---|---|---|"]
            L += [f"| {i['ref']} | {i['check']} | {i['detail']} | {i['action']} |" for i in g]
            L.append("")
    L += ["## Remediation roadmap (largest gap first)", ""]
    if not res["roadmap"]:
        L.append("All categories meet their target.")
    for n, c in enumerate(res["roadmap"], 1):
        L.append(f"{n}. **{c['id']} {c['name']}**: tier {c['current']} to {c['target']} (coverage {c['coverage']}%).")
    L.append("")
    return "\n".join(L)
