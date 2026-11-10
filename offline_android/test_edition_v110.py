"""Once-only treasure maps for the isolated test account; not an official payload."""
from .test_edition_seed import ACCOUNT
from . import test_edition_v108 as previous

MAP_ITEMS = ((1431, 500),)  # One-tier 九幽宝图, 500 additional maps in total.
MARKER = 'test_v110_abyss_maps_500_v1'


def grant_maps(backend):
    if backend.account != ACCOUNT:
        return False
    from network_redirect import summon
    role = backend.profile()
    if MARKER in role:
        return False
    for item_id, count in MAP_ITEMS:
        summon.add_item(role, item_id, count)
    role[MARKER] = dict(items={str(tid): count for tid, count in MAP_ITEMS}, total=500)
    # Reward and receipt are one role row; rollback any uncommitted save failure.
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
                    grant_maps(fixed)
            except Exception:
                self.close()
                raise

    return FixedAccounts
