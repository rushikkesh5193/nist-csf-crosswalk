from csf_crosswalk import analyse, load_config
from csf_crosswalk.annex_a import CONTROLS

CFG = load_config()


def all_impl(**override):
    c = {cid: {"status": "implemented"} for cid in CONTROLS}
    c.update(override)
    return c


def run(controls=None, **extra):
    data = {"controls": all_impl() if controls is None else controls}
    data.update(extra)
    return analyse(data, CFG)


def cat(res, cid):
    return next(c for c in res["categories"] if c["id"] == cid)


def checks(res, ref=None):
    return {(i["ref"], i["check"]) for i in res["issues"] if ref is None or i["ref"] == ref}
