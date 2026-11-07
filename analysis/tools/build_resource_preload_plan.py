"""Build the bounded prewarm allowlist from audited packaged image dimensions."""
import json
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
MiB = 1024 * 1024


def build():
    inventory = json.loads((ROOT / 'analysis/evidence/resource_inventory.json').read_text())
    byname = {r['logical']: r for r in inventory}
    core = [dict(kind='config', module=mod, getter=getter) for mod, getter in [
        ('d_mainUI', 'getRoleLevelConfig'), ('d_packageUI', 'getPackageCSVConfig'),
        *[('d_data', key) for key in ('getCharacterExperienceCSVConfig', 'getCharacterQualityCSVConfig',
          'getShopItemsPriceCSVConfig', 'getTopScoreExchangeCSVConfig', 'getTopScoreCSVConfig',
          'getRechargeItemsPriceCSVConfig', 'getStoneAttrCSVConfig', 'getMaterialTransformCSVConfig',
          'getCortCollectCSVConfig', 'getAscensionConfig', 'getEquipAscConfig',
          'getPetCSVConfig', 'getSkillCsv_advance', 'getSpecialitemuseCSVConfig')]]]
    warm = [dict(kind='config', module=mod, getter=getter) for mod, getter in [
        ('d_lineupUI', 'getFateCSVConfig'), ('d_packageUI', 'getItemLevelPriceCSVConfig'),
        ('d_packageUI', 'getItembasePriceCSVConfig'), ('d_data', 'getAchievementsCSVConfig'),
        ('d_data', 'getCheerCSVConfig'), ('d_data', 'getAdaptiveCSVConfig'),
        ('d_data', 'getTowerCSVConfig'), ('d_data', 'getGoldRushCSVConfig')]]
    scripts = json.loads((ROOT / 'analysis/evidence/script_inventory.json').read_text())
    modules = {'d_mainUI': 'ui/mainUI', 'd_packageUI': 'ui/packageUI',
               'd_data': 'data', 'd_lineupUI': 'ui/lineupUI'}
    for job in core + warm:
        module = modules[job['module']]
        script = next(row for row in scripts if row['logical'] == f'lua/{module}.lua')
        proto = next(key for key, name in script['functions'].items() if name == job['getter'])
        listing = (ROOT / f'analysis/evidence/lua_named/lua/{module}.lua.txt').read_text()
        body = listing.split('FUNCTION ' + proto + ' ')[1].split('\nFUNCTION ')[0]
        assert 'params=0' in body.splitlines()[0] and 'send_msg' not in body
        job['cache_fields'] = sorted(set(re.findall(r"GSET.*'(g_[^']+)'", body)))
        assert job['cache_fields'], job
    used = set()
    report = []
    def images(target, group, names, budget):
        entries = []
        for name in names:
            if name in used:
                continue
            row = byname[name]
            with Image.open(ROOT / 'jgbol3.87/assets/release_' / row['physical']) as im:
                width, height = im.size
            # Conservative RGBA/POT allocation, including mipmap headroom.
            size = (1 << (width - 1).bit_length()) * (1 << (height - 1).bit_length()) * 4
            size = (size * 4 + 2) // 3
            if size <= 3 * MiB:
                entries.append((size, name))
        total = 0
        for size, name in sorted(entries):
            if total + size > budget:
                continue
            total += size
            used.add(name)
            target.append(dict(kind='texture', path=name, estimated_bytes=size, group=group))
        report.append(dict(group=group, estimated_bytes=total))
    def prefix(path):
        return sorted(n for n in byname if n.startswith(path) and n.endswith('.png'))
    main = ['title.png', 'tollgate1.png', 'tollgate2.png', 'plate.png', 'tip_bkg.png',
            'btn11.png', 'btn12.png', 'btn21.png', 'btn22.png', 'btn31.png', 'btn32.png', 'up.png']
    images(core, 'main', ['v2/mainUI/' + n for n in main], 7 * MiB)
    images(core, 'common', prefix('v2/common/') + prefix('v2/buttons/'), 5 * MiB)
    images(warm, 'inventory', prefix('v2/packageUI/'), 6 * MiB)
    images(warm, 'activities', prefix('v2/funUI/'), 2 * MiB)
    images(warm, 'fish', prefix('v2/fishRushUI/'), 3 * MiB)
    images(warm, 'pray', prefix('v2/qiFuUI/'), 3 * MiB)
    return dict(version=1, retained_texture_bytes=28 * MiB, startup_slice_seconds=0.5,
                startup_max_jobs=64, warm_interval_seconds=0.12, warm_delay_seconds=2,
                slow_job_seconds=0.012, cooldown_seconds=0.5, max_warm_seconds=180,
                core=core, warm=warm), report


if __name__ == '__main__':
    plan, report = build()
    (ROOT / 'server_config/resource_preload.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(dict(core_jobs=len(plan['core']), warm_jobs=len(plan['warm']), groups=report), indent=2))
