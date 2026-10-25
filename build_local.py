"""Patch the preserved 3.87 compatibility APK with a permanent local login."""
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from build_channel360 import ROOT, WORK, JAVA, TOOLS, apktool, run


def build(output=None):
    source = ROOT / 'build/jgbol3.87-360-list.apk'
    if not source.exists():
        raise RuntimeError('缺少本地构建输入 build/jgbol3.87-360-list.apk')
    output = Path(output or ROOT / 'build/jgbol3.87-local.apk')
    directory = ROOT / '.runtime/local-build'
    framework = ROOT / '.runtime/tools/apktool-framework'
    apktool('d', '-f', '-p', framework, '-o', directory, source)
    bridge = directory / 'smali/com/syyx/sdkproxy/ThirdPartyAPI.smali'
    text = bridge.read_text()
    def replace(name, body):
        nonlocal text
        pattern = r'(\.method [^\n]* ' + re.escape(name) + r'\([^\n]*\n).*?\.end method'
        text, count = re.subn(pattern, lambda m: m[1] + body + '\n.end method', text, flags=re.S)
        if count != 1:
            raise RuntimeError('Unexpected bridge method: ' + name)
    for name in ('login', 'switchAccount'):
        replace(name, '''    .locals 1
    const/4 v0, SWITCH_FLAG
    sput-boolean v0, Lcom/syyx/sdkproxy/LocalLogin;->switching:Z
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_ui_instance:Landroid/app/Activity;
    invoke-static {v0}, Lcom/syyx/sdkproxy/LocalLogin;->show(Landroid/app/Activity;)V
    return-void'''.replace('SWITCH_FLAG', '0x1' if name == 'switchAccount' else '0x0'))
    # No channel initialization, purchase, forums or shutdown hooks can open SDK UI.
    text = re.sub(r'    invoke-static \{v0\}, Lcom/qihoo/gamecenter/sdk/matrix/Matrix;->init\(Landroid/app/Activity;\)V', '', text)
    for name in ('onDestroy', 'pay', 'purchase', 'purchase_By_infos', 'forum', 'showMMap', 'getLoginInfo', 'refreshBalance'):
        replace(name, '    .locals 0\n    return-void')
    text += '''
.method public static localComplete(Ljava/lang/String;)V
    .locals 3
    sput-object p0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->mAccessToken:Ljava/lang/String;
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_map:Ljava/util/Map;
    const-string v1, "access_token"
    invoke-interface {v0, v1, p0}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    sget-object v0, Lcom/syyx/sdkproxy/ThirdPartyAPI;->m_sEventCallback:Lcom/syyx/sdkproxy/ThirdPartyCallback;
    const/4 v1, 0x1
    const/4 v2, 0x0
    invoke-interface {v0, v1, v2}, Lcom/syyx/sdkproxy/ThirdPartyCallback;->onEvent(II)V
    return-void
.end method
'''
    bridge.write_text(text)
    shutil.copyfile(ROOT / 'local_login/LocalLogin.smali', bridge.with_name('LocalLogin.smali'))
    manifest = directory / 'AndroidManifest.xml'
    ET.register_namespace('android', 'http://schemas.android.com/apk/res/android')
    tree = ET.parse(manifest)
    ns = '{http://schemas.android.com/apk/res/android}'
    app = tree.getroot().find('application')
    # ChargeActivity is also the original weekly browser; keep its declaration.
    for child in list(app):
        name = child.get(ns + 'name', '')
        if name.startswith(('com.qihoo', 'QHOPENSDK')):
            app.remove(child)
    for child in list(tree.getroot()):
        if child.tag == 'uses-permission' and child.get(ns + 'name', '').split('.')[-1] in (
            'SEND_SMS', 'READ_SMS', 'WRITE_SMS', 'RECEIVE_SMS', 'READ_CONTACTS',
            'ACCESS_COARSE_LOCATION', 'ACCESS_FINE_LOCATION', 'SYSTEM_ALERT_WINDOW'):
            tree.getroot().remove(child)
    tree.write(manifest, encoding='utf-8', xml_declaration=True)
    metadata = directory / 'apktool.yml'
    metadata.write_text(metadata.read_text().replace('versionCode: 87', 'versionCode: 90'))
    unsigned = ROOT / '.runtime/local-unsigned.apk'
    aligned = ROOT / '.runtime/local-aligned.apk'
    apktool('b', '-p', framework, '-o', unsigned, directory)
    run(TOOLS / 'zipalign', '-f', '4', unsigned, aligned)
    run(TOOLS / 'apksigner', 'sign', '--ks', WORK / 'local-test.p12', '--ks-key-alias', 'channel360',
        '--ks-pass', 'pass:local-test-only', '--out', output, aligned)
    run(TOOLS / 'apksigner', 'verify', '--verbose', output)
    run(TOOLS / 'zipalign', '-c', '4', output)
    print('本地账号版已构建：', output)


if __name__ == '__main__':
    build()
