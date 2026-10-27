"""python3 -m csf_crosswalk assessment.json [--out-dir DIR] [--fail-on SEVERITY]"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import analyse, load
from .analyse import SEV_ORDER
from .report import to_markdown, to_json, profile_csv, crosswalk_csv


def main(argv=None):
    ap = argparse.ArgumentParser(prog="csf_crosswalk")
    ap.add_argument("assessment")
    ap.add_argument("--out-dir")
    ap.add_argument("--fail-on", choices=list(SEV_ORDER))
    a = ap.parse_args(argv)
    if not Path(a.assessment).is_file():
        print(f"error: {a.assessment} not found", file=sys.stderr)
        return 2
    try:
        data = load(a.assessment)
        res = analyse(data)
    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    org = data.get("organisation", "Organisation")
    if a.out_dir:
        o = Path(a.out_dir)
        o.mkdir(parents=True, exist_ok=True)
        (o / "report.md").write_text(to_markdown(res, org), encoding="utf-8")
        (o / "report.json").write_text(to_json(res, org), encoding="utf-8")
        (o / "csf_profile.csv").write_text(profile_csv(res), encoding="utf-8")
        (o / "iso_to_csf_crosswalk.csv").write_text(crosswalk_csv(), encoding="utf-8")
        print(f"{len(res['issues'])} issues; {len(res['roadmap'])} categories below target -> {o}/")
    else:
        print(to_markdown(res, org))
    if a.fail_on and any(SEV_ORDER[i["severity"]] <= SEV_ORDER[a.fail_on] for i in res["issues"]):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
