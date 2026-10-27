"""NIST Cybersecurity Framework (CSF) 2.0 structure: 6 Functions and 22 Categories.

Identifiers and names were checked against two published summaries of the CSF 2.0 core
(final version released February 2024). Subcategories are not included. For formal work, use
NIST's own publication (NIST CSWP 29) and its Informative References.
"""
FUNCTIONS = {"GV": "Govern", "ID": "Identify", "PR": "Protect", "DE": "Detect", "RS": "Respond", "RC": "Recover"}

CATEGORIES = {
    "GV.OC": "Organizational Context",
    "GV.RM": "Risk Management Strategy",
    "GV.RR": "Roles, Responsibilities, and Authorities",
    "GV.PO": "Policy",
    "GV.OV": "Oversight",
    "GV.SC": "Cybersecurity Supply Chain Risk Management",
    "ID.AM": "Asset Management",
    "ID.RA": "Risk Assessment",
    "ID.IM": "Improvement",
    "PR.AA": "Identity Management, Authentication, and Access Control",
    "PR.AT": "Awareness and Training",
    "PR.DS": "Data Security",
    "PR.PS": "Platform Security",
    "PR.IR": "Technology Infrastructure Resilience",
    "DE.CM": "Continuous Monitoring",
    "DE.AE": "Adverse Event Analysis",
    "RS.MA": "Incident Management",
    "RS.AN": "Incident Analysis",
    "RS.CO": "Incident Response Reporting and Communication",
    "RS.MI": "Incident Mitigation",
    "RC.RP": "Incident Recovery Plan Execution",
    "RC.CO": "Incident Recovery Communication",
}

TIERS = {1: "Partial", 2: "Risk Informed", 3: "Repeatable", 4: "Adaptive"}

assert len(FUNCTIONS) == 6 and len(CATEGORIES) == 22
assert all(c.split(".")[0] in FUNCTIONS for c in CATEGORIES)
