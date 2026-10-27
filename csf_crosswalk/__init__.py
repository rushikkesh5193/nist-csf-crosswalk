"""ISO 27001 to NIST CSF 2.0 crosswalk and profile gap analysis."""
import json

from .analyse import analyse, load_config

__all__ = ["analyse", "load_config", "load"]


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)
