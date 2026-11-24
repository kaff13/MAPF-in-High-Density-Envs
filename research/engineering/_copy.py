"""PHANS-specific copy fast paths with standard alias and fallback semantics.

Use by replacing only the PHANS module's ``copy`` reference inside a scoped
adapter. Never assign to ``copy.deepcopy`` on the shared standard-library module.
"""

from copy import deepcopy as _stdlib_deepcopy


_ATOMIC = frozenset((int, float, bool, str, bytes, complex, type(None)))
_MISSING = object()


def fast_deepcopy(value, memo=None):
    """Copy lists of integer coordinates efficiently, preserving mutable aliases."""
    kind = type(value)
    if kind in _ATOMIC:
        return value
    if kind is tuple and len(value) == 2 and type(value[0]) is int and type(value[1]) is int:
        return value
    if memo is None:
        memo = {}
    previous = memo.get(id(value), _MISSING)
    if previous is not _MISSING:
        return previous
    if kind is list:
        result = []
        memo[id(value)] = result
        # As in stdlib deepcopy, retain source objects for the lifetime of a
        # caller-supplied memo, preventing recycled ids from aliasing old copies.
        memo.setdefault(id(memo), []).append(value)
        result.extend(fast_deepcopy(item, memo) for item in value)
        return result
    return _stdlib_deepcopy(value, memo)
