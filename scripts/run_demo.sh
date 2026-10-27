#!/usr/bin/env bash
# Regenerate the synthetic assessment, run the crosswalk and the tests.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m tools.gen_sample examples/sample_assessment.json
python3 -m csf_crosswalk examples/sample_assessment.json --out-dir examples
python3 -m unittest discover -s tests
