"""Generate a SYNTHETIC assessment for demos and tests (the organisation is invented).

    python3 -m tools.gen_sample examples/sample_assessment.json
"""
from __future__ import annotations

import json
import sys

from csf_crosswalk.annex_a import CONTROLS

OVERRIDES = {
    "A.8.16": "partial", "A.7.4": "partial", "A.8.15": "partial",      # Detect: weak monitoring
    "A.5.26": "partial", "A.5.28": "planned",                           # Respond gaps
    "A.5.29": "planned", "A.5.30": "partial",                           # Recover gaps
    "A.5.27": "not_implemented", "A.8.8": "partial",
}
OMIT = {"A.6.3", "A.5.23"}                                              # never assessed
NA = {"A.5.8": "No in-house project delivery.", "A.8.30": "No outsourced development."}


def build():
    controls = {}
    for cid in CONTROLS:
        if cid in OMIT:
            continue
        if cid in NA:
            controls[cid] = {"status": "not_applicable", "justification": NA[cid]}
        else:
            controls[cid] = {"status": OVERRIDES.get(cid, "implemented")}
    controls["A.9.4.1"] = {"status": "implemented"}                     # injected: 2013-era control number
    return {"_note": "SYNTHETIC DATA. The organisation is invented.", "organisation": "ExampleOrg Pvt Ltd (synthetic)",
            "default_target": 3, "targets": {"DE.CM": 4, "RC.RP": 4, "GV.SC": 2},
            "declared_tiers": {"ID.IM": 3}, "controls": controls}


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "examples/sample_assessment.json"
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(build(), fh, indent=1)
    print(f"wrote {out}")
