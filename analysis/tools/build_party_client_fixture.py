"""Build isolated native party reward checks; restore UI after completion."""
from pathlib import Path
from verify_party_client import fixture
ROOT=Path(__file__).resolve().parents[2]
source='local function run()\n'+fixture()+'\nend\nlocal result=run();partyPreview.restore();partyPreview=nil;return result\n'
(ROOT/'.runtime/party-fixture.lua').write_text(source)
print('Built 9 native party reward and offline luck checks')
