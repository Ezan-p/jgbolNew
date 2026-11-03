"""Reproducible route/loot budget audit; no account or database writes."""
import copy
import json
import random
import sys
from collections import Counter, deque
from pathlib import Path
from statistics import mean
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity_babel as babel


def route(grid, start, target):
    queue = deque([(start, [])])
    seen = {start}
    while queue:
        pos, path = queue.popleft()
        if pos == target:
            return path
        r, c = pos
        for nxt in ((r-1,c),(r+1,c),(r,c-1),(r,c+1)):
            row, col = nxt
            if (0 <= row < 5 and 0 <= col < 8 and nxt not in seen
                    and (nxt == target or grid[row][col] == 0)):
                seen.add(nxt)
                queue.append((nxt, path + [nxt]))
    return None


def full_clear(source):
    """Greedy nearest interaction with no initial keys/tools, assuming wins.

    This uses full map knowledge to measure a reproducible budget, not a
    promise about fog-of-war discovery or an optimal traveling-salesman tour.
    """
    grid = copy.deepcopy(source)
    pos = (0,0)
    inventory = Counter()
    moves = wins = drops = 0
    stairs = next((r,c) for r,line in enumerate(grid) for c,t in enumerate(line) if t == 3)
    while any(t not in (0,3) for line in grid for t in line):
        choices = []
        for r,line in enumerate(grid):
            for c,typ in enumerate(line):
                if typ in (0,3) or (typ in babel.TOOLS and not inventory[babel.TOOLS[typ]]):
                    continue
                path = route(grid, pos, (r,c))
                if path is not None:
                    choices.append((len(path), r, c, typ))
        assert choices, ('resource deadlock', grid, inventory)
        distance, r, c, typ = min(choices)
        moves += distance
        pos = (r,c)
        grid[r][c] = 0
        if typ in babel.TOOLS:
            inventory[babel.TOOLS[typ]] -= 1
        if typ in (20005,20006,20010,20011,20012):
            inventory[typ] += 1
        wins += int(typ in babel.GUARDS)
        drops += int(typ in babel.GUARDS or typ in (20007,20008,20009))
    path = route(grid,pos,stairs)
    assert path is not None and not any(inventory.values())
    assert (wins,drops) == (7,10)
    return moves + len(path)


def summary(values):
    return dict(min=min(values), max=max(values), mean=round(mean(values),2))


def main():
    samples = {k: dict(direct=[], full=[]) for k in ('11-30','31-50','51-70')}
    runs = []
    for seed in range(100):
        signatures = set()
        direct_total = full_total = 0
        with patch.object(babel.secrets, 'SystemRandom', return_value=random.Random(seed)):
            for floor in range(11,71):
                state = dict(cur_floor=floor, floors={})
                babel.generate(state)
                grid = [[c['elem_type'] for c in line] for line in state['floors'][str(floor)]]
                signature = tuple(t for line in grid for t in line)
                assert signature not in signatures
                signatures.add(signature)
                boss = next((r,c) for r,line in enumerate(grid) for c,t in enumerate(line) if t == 9)
                stairs = next((r,c) for r,line in enumerate(grid) for c,t in enumerate(line) if t == 3)
                path = route(grid,(0,0),boss)
                finish = route(grid,boss,stairs)
                assert path is not None and finish is not None
                direct = len(path) + len(finish)
                minimum = 7 + (floor-11)//20
                assert minimum <= direct <= minimum+2
                full = full_clear(grid)
                tier = ('11-30','31-50','51-70')[(floor-11)//20]
                samples[tier]['direct'].append(direct)
                samples[tier]['full'].append(full)
                direct_total += direct
                full_total += full
        runs.append(dict(direct=direct_total, full=full_total))
    pools = []
    for row in babel.FLOORS:
        if int(row['floor_l']) < 11:
            continue
        entries = row['daoju'].split('/')
        pools.append(dict(floors=[int(row['floor_l']),int(row['floor_r'])],
                          entries=len(entries), probability_per_entry=f'1/{len(entries)}',
                          outcome_weights=dict(Counter(entries))))
    result = dict(date='2026-11-02', seeds=100, maps=6000, passed=True,
                  distinct_layouts_per_run=60, initial_keys_and_tools=0,
                  assumptions='All battles won; full-clear routing uses full map knowledge; no claim of zero-supply completion.',
                  route_energy={tier:{k:summary(v) for k,v in values.items()} for tier,values in samples.items()},
                  energy_11_to_70={k:summary([run[k] for run in runs]) for k in ('direct','full')},
                  rewards_11_to_70=dict(direct_rolls=61,direct_coins=3050,
                                        full_rolls=601,full_coins=30050,
                                        direct_battles=60,full_battles=420),
                  drop_pools=pools)
    out = ROOT/'analysis/evidence/babel_layouts_20261102'
    out.mkdir(parents=True,exist_ok=True)
    (out/'balance.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'drop_pools'},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
