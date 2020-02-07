import copy

MISSING = object()


def _merge_dicts(a: dict, b: dict, merger, copier=lambda v: v) -> dict:
    out = {}

    # Hack to keep the iteration order the same...
    keys = list(a)
    key_set = set(keys)
    keys += [k for k in b if k not in key_set]

    for key in keys:
        va = a.get(key, MISSING)
        vb = b.get(key, MISSING)
        if vb is MISSING:
            out[key] = copier(va)
        elif va is MISSING:
            out[key] = copier(vb)
        else:
            out[key] = merger(va, vb)
    return out


def _merge_simple(a, b):
    a = copy.deepcopy(a)
    a.__dict__.update(copy.deepcopy(b).__dict__)
    return a
