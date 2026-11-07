"""Build a native-only v110 retry candidate without replacing the release."""
import hashlib,json,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from build_channel360 import TOOLS,run
from build_offline import SIGNING_KEY,signer_certificate
from offline_android.native.build_native import build

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 base=ROOT/'build/金箍棒3.87离线正式版v110.apk'
 assert sha(base)=='34720ec6b5dbdaf54ee372f0e725785cfd91f75f42903ba86be194564a9cd03c'
 work=ROOT/'.runtime/v110-guangsu-retry-20261106';work.mkdir(parents=True,exist_ok=True)
 out=ROOT/'build/candidates/金箍棒3.87离线v110-补丁重试待验收.apk';out.parent.mkdir(parents=True,exist_ok=True)
 assert not out.exists(),'Candidate already exists'
 evidence=ROOT/'analysis/evidence/v110/guangsu-retry-20261106'
 validation=json.loads((evidence/'native-retry-validation.json').read_text())
 assert validation['passed'] and validation['native_source_sha256']==sha(ROOT/'offline_android/native/offline.c')
 native=build(work/'liboffline.so')
 with zipfile.ZipFile(base) as old,zipfile.ZipFile(work/'unsigned.apk','w') as new:
  for entry in old.infolist():
   if not entry.filename.startswith('META-INF/'):
    new.writestr(entry,native.read_bytes() if entry.filename=='lib/armeabi-v7a/liboffline.so' else old.read(entry))
 run(TOOLS/'zipalign','-f','4',work/'unsigned.apk',work/'aligned.apk')
 run(TOOLS/'apksigner','sign','--ks',SIGNING_KEY,'--ks-key-alias','channel360','--ks-pass','pass:local-test-only','--out',out,work/'aligned.apk')
 run(TOOLS/'apksigner','verify','--verbose',out);run(TOOLS/'zipalign','-c','4',out)
 assert signer_certificate(base)==signer_certificate(out)
 with zipfile.ZipFile(base) as old,zipfile.ZipFile(out) as new:
  assert new.testzip() is None
  names=lambda z:{n for n in z.namelist() if not n.startswith('META-INF/')}
  assert names(old)==names(new)
  changed=sorted(n for n in names(old) if old.read(n)!=new.read(n))
  assert changed==['lib/armeabi-v7a/liboffline.so'],changed
 digest=sha(out)
 out.with_suffix('.apk.sha256').write_text(digest+'  '+out.name+'\n')
 report=dict(candidate=str(out.relative_to(ROOT)),apk_sha256=digest,base_sha256=sha(base),changed=changed,
  same_certificate=True,manifest_unchanged=True,payload_unchanged=True,native_retry_checks=len(validation['checks']),
  native_adapter_sha256=sha(native),native_source_sha256=validation['native_source_sha256'],
  guangsu_device_tested=False,activity_ui_verified=False,formal_release_replaced=False)
 (evidence/'candidate-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
