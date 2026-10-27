"""Indicative crosswalk from ISO/IEC 27001:2022 Annex A controls to NIST CSF 2.0 categories.

This mapping is the author's own category-level judgement, not an official NIST or ISO mapping. A control can
map to more than one category. Use NIST's published Informative References for any formal mapping.
"""
from .annex_a import CONTROLS
from .data import CATEGORIES

ISO_TO_CSF = {
    # A.5 Organizational
    "A.5.1": ["GV.PO"], "A.5.2": ["GV.RR"], "A.5.3": ["PR.AA"], "A.5.4": ["GV.RR"], "A.5.5": ["RS.CO"],
    "A.5.6": ["ID.RA"], "A.5.7": ["ID.RA"], "A.5.8": ["GV.RM"], "A.5.9": ["ID.AM"], "A.5.10": ["GV.PO"],
    "A.5.11": ["ID.AM"], "A.5.12": ["ID.AM"], "A.5.13": ["PR.DS"], "A.5.14": ["PR.DS"],
    "A.5.15": ["PR.AA"], "A.5.16": ["PR.AA"], "A.5.17": ["PR.AA"], "A.5.18": ["PR.AA"],
    "A.5.19": ["GV.SC"], "A.5.20": ["GV.SC"], "A.5.21": ["GV.SC"], "A.5.22": ["GV.SC"], "A.5.23": ["GV.SC"],
    "A.5.24": ["RS.MA"], "A.5.25": ["DE.AE"], "A.5.26": ["RS.MA", "RS.MI", "RC.RP"], "A.5.27": ["ID.IM"],
    "A.5.28": ["RS.AN"], "A.5.29": ["RC.RP", "PR.IR"], "A.5.30": ["PR.IR", "RC.RP"],
    "A.5.31": ["GV.OC"], "A.5.32": ["GV.OC"], "A.5.33": ["PR.DS"], "A.5.34": ["PR.DS"],
    "A.5.35": ["GV.OV"], "A.5.36": ["GV.OV"], "A.5.37": ["GV.PO"],
    # A.6 People
    "A.6.1": ["GV.RR"], "A.6.2": ["GV.RR"], "A.6.3": ["PR.AT"], "A.6.4": ["GV.RR"], "A.6.5": ["GV.RR"],
    "A.6.6": ["PR.DS"], "A.6.7": ["PR.PS"], "A.6.8": ["DE.AE"],
    # A.7 Physical
    "A.7.1": ["PR.AA"], "A.7.2": ["PR.AA"], "A.7.3": ["PR.AA"], "A.7.4": ["DE.CM"], "A.7.5": ["PR.IR"],
    "A.7.6": ["PR.AA"], "A.7.7": ["PR.DS"], "A.7.8": ["PR.IR"], "A.7.9": ["PR.PS"], "A.7.10": ["PR.DS"],
    "A.7.11": ["PR.IR"], "A.7.12": ["PR.IR"], "A.7.13": ["PR.PS"], "A.7.14": ["PR.DS"],
    # A.8 Technological
    "A.8.1": ["PR.PS"], "A.8.2": ["PR.AA"], "A.8.3": ["PR.AA"], "A.8.4": ["PR.AA"], "A.8.5": ["PR.AA"],
    "A.8.6": ["PR.IR"], "A.8.7": ["PR.PS"], "A.8.8": ["ID.RA"], "A.8.9": ["PR.PS"], "A.8.10": ["PR.DS"],
    "A.8.11": ["PR.DS"], "A.8.12": ["PR.DS"], "A.8.13": ["PR.DS", "RC.RP"], "A.8.14": ["PR.IR"],
    "A.8.15": ["PR.PS", "DE.CM"], "A.8.16": ["DE.CM"], "A.8.17": ["PR.PS"], "A.8.18": ["PR.PS"],
    "A.8.19": ["PR.PS"], "A.8.20": ["PR.IR"], "A.8.21": ["PR.IR"], "A.8.22": ["PR.IR"], "A.8.23": ["PR.IR"],
    "A.8.24": ["PR.DS"], "A.8.25": ["PR.PS"], "A.8.26": ["PR.PS"], "A.8.27": ["PR.PS"], "A.8.28": ["PR.PS"],
    "A.8.29": ["PR.PS"], "A.8.30": ["GV.SC"], "A.8.31": ["PR.PS"], "A.8.32": ["PR.PS"],
    "A.8.33": ["PR.DS"], "A.8.34": ["PR.DS"],
}

assert set(ISO_TO_CSF) == set(CONTROLS), "mapping must cover exactly the 93 Annex A controls"
assert all(c in CATEGORIES for cats in ISO_TO_CSF.values() for c in cats), "unknown CSF category in mapping"


def controls_for(category):
    return [cid for cid, cats in ISO_TO_CSF.items() if category in cats]
