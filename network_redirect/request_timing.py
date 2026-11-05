"""Request-local monotonic timing; never logs payloads or credentials."""
from contextvars import ContextVar
from contextlib import contextmanager
from functools import wraps
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


def request_cache(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        token = recalculation_cache.set({})
        try:
            return fn(*args, **kwargs)
        finally:
            recalculation_cache.reset(token)
    return wrapped
