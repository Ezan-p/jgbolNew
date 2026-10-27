"""One-off recovery of ezan's spell books deleted by zero-count stack cleanup.

Uses the existing 2026-10-27 11:44:11 (UTC+8) backup. Refuses recovery if later
logged requests could consume/convert books, IDs conflict, or slots conflict.
Run with --apply only after reviewing the dry-run report and stopping the server.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import time
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import formation as f

BACKUP=ROOT/'.runtime/offline/backups/ezan-petland-quota-1793072651808646000.json'
SINCE='2026-10-27T03:44:11'
MARKER='zero_count_skill_repair_20261027'
CONSUMING={1025,1071,1076,1212,1053,1054,1056,1074,1079,1225,1332,1343,1088,1086}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    source=json.loads(BACKUP.read_text())
    assert source['register_account']=='ezan'
    books=[i for i in source['attachments'] if i['attach_type']==6 and not i.get('protogenic')]
    assert len(books)==72
    requests=[]
    for path in (ROOT/'.runtime/redirect/sessions').glob('*/events.jsonl'):
        for line in path.open():
            d=json.loads(line)
            if d.get('time','')>=SINCE and d.get('kind')=='game_request' and d.get('message_id') in CONSUMING:
                requests.append(dict(time=d['time'],message_id=d['message_id'],session=path.parent.name))
    report=dict(source=str(BACKUP.relative_to(ROOT)),source_sha256=hashlib.sha256(BACKUP.read_bytes()).hexdigest(),
                source_books=len(books),possible_consuming_requests=requests,applied=False)
    db=sqlite3.connect(ROOT/'.runtime/offline/game.sqlite3',timeout=10)
    try:
        db.execute('BEGIN IMMEDIATE' if args.apply else 'BEGIN')
        raw=db.execute('SELECT data FROM roles WHERE account=?',('ezan',)).fetchone()[0]
        role=json.loads(raw)
        if role.get(MARKER):
            report.update(already_repaired=True,restored_ids=role[MARKER]['ids']);db.rollback()
        else:
            assert not requests,'Consumption requests need manual review; recovery refused'
            existing={i['id']:i for i in role['attachments']}
            added=[]
            for old in books:
                if old['id'] in existing:
                    assert existing[old['id']]['attach_type']==6 and existing[old['id']]['type_id']==old['type_id'],'ID collision'
                    continue
                item=copy.deepcopy(old)
                # Carry the two equipped books with their original companion.
                order=item.get('equip_order',0)
                if 1<=order<=8:
                    owner=next(c['id'] for c in source['corteges'] if c.get('order')==order)
                    current=next((c for c in role['corteges'] if c['id']==owner),{})
                    item['equip_order']=current.get('order',0)
                    if not item['equip_order']:item['equip_pos']=0
                assert not item.get('equip_order') or not any(i['attach_type']==6 and i.get('equip_order')==item['equip_order'] and i.get('equip_pos')==item.get('equip_pos') for i in role['attachments']),'Occupied slot'
                role['attachments'].append(item);added.append(item['id'])
            report.update(restored_ids=added,restored_count=len(added))
            if args.apply:
                stamp=time.time_ns();path=ROOT/f'.runtime/offline/backups/ezan-before-skill-repair-{stamp}.json'
                path.write_text(raw+'\n')
                role[MARKER]=dict(source_sha256=report['source_sha256'],ids=added,time=stamp//10**9)
                f.prepare(role,f.load_rules())
                db.execute('UPDATE roles SET data=? WHERE account=?',(json.dumps(role,ensure_ascii=False),'ezan'));db.commit()
                report.update(applied=True,safety_backup=str(path.relative_to(ROOT)))
            else:db.rollback()
    finally:db.close()
    target=ROOT/'analysis/evidence/skills'/('recovery.json' if args.apply else 'recovery_preview.json')
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
