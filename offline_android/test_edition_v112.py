"""Once-only additive v112 supplies for the isolated fixed test account."""
from .test_edition_seed import ACCOUNT
from . import test_edition_v110 as previous

MAP_ITEMS = tuple((tid, 500) for tid in range(1431, 1441))
RICE_ITEMS = tuple((tid, 300) for tid in range(1213, 1217))
ITEMS = MAP_ITEMS + RICE_ITEMS
MARKER = 'test_v112_maps500_rice300_v1'


def grant_supplies(backend):
    if backend.account != ACCOUNT:
        return False
    from network_redirect import summon
    role = backend.profile()
    if MARKER in role:
        return False
    for tid, count in ITEMS:
        summon.add_item(role, tid, count)
    role[MARKER] = dict(items={str(tid): count for tid, count in ITEMS},
                        maps_total=5000, rice_total=1200)
    # Persist inventory and receipt atomically, including failures before commit.
    with backend.db:
        backend.save(role, gameplay=False)
    return True


def fixed_accounts_class():
    from network_redirect import game_clock
    base = previous.fixed_accounts_class()

    class FixedAccounts(base):
        def __init__(self, directory, port, emit, *, network_time=None):
            super().__init__(directory, port, emit, network_time=network_time)
            fixed = self.backends[ACCOUNT]
            try:
                with game_clock.scope(fixed.clock):
                    grant_supplies(fixed)
            except BaseException:
                self.close()
                raise

    return FixedAccounts
