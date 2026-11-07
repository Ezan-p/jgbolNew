"""Request-local monotonic timing; never logs payloads or credentials."""
from contextvars import ContextVar
from contextlib import contextmanager
from functools import wraps
import marshal
from time import perf_counter

current = ContextVar('request_timing', default=None)


@contextmanager
def phase(name):
    metrics = current.get()
    if metrics is None:
        yield
        return
    start = perf_counter()
    try:
        yield
    finally:
        metrics[name + '_ms'] = metrics.get(name + '_ms', 0) + (perf_counter() - start) * 1000


def measured(name):
    def decorate(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            with phase(name):
                return fn(*args, **kwargs)
        return wrapped
    return decorate


def count(name):
    metrics = current.get()
    if metrics is not None:
        metrics[name] = metrics.get(name, 0) + 1


# Kept separate from exported metrics: snapshots must never enter logs.
recalculation_cache = ContextVar('recalculation_cache', default=None)
role_baselines = ContextVar('role_baselines', default=None)
achievement_refresh_cache = ContextVar('achievement_refresh_cache', default=None)


def state_token(value):
    """Detached comparison token for acyclic JSON-shaped roles and rules.

    The C encoder avoids building a second mutable object graph. Unlike JSON,
    it distinguishes numeric/string keys and supports mixed battle-event keys.
    Version 2 serializes values without memoizing object identities, so equal
    replacement dictionaries/strings do not invalidate reuse. Dictionary
    reordering may conservatively cause extra work. Tokens stay in memory;
    never deserialize them or use them as a cross-process/persistent format.
    """
    return marshal.dumps(value, 2)


def request_cache(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        token = recalculation_cache.set({})
        baseline_token = role_baselines.set({})
        achievement_token = achievement_refresh_cache.set({})
        try:
            return fn(*args, **kwargs)
        finally:
            achievement_refresh_cache.reset(achievement_token)
            role_baselines.reset(baseline_token)
            recalculation_cache.reset(token)
    return wrapped
