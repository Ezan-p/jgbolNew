"""Keep restored legacy Activities responsive while the offline backend starts.

Patch only the decoded build staging tree. The original onCreate/onResume/
onPause/onDestroy bodies still run unchanged for an initialized game instance.
Never block the UI thread, and never return without the framework super call.
"""
from pathlib import Path
import re

GAME = 'Lcom/sygame/jingubang/uc/xiyoujilua;'
COCOS = 'Lorg/cocos2dx/lib/Cocos2dxActivity;'
RUNTIME = 'Lcom/jgbol/offline/OfflineRuntime;'


def change_method(text, signature, transform):
    pattern = re.compile(r'(?ms)(^\.method [^\n]* ' + re.escape(signature) + r'\n)(.*?)(^\.end method)')
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError('Lifecycle baseline mismatch: ' + signature)
    match = matches[0]
    return text[:match.start(2)] + transform(match.group(2)) + text[match.end(2):]


def after_once(body, marker, patch):
    if body.count(marker) != 1:
        raise RuntimeError('Lifecycle super call did not match baseline: ' + marker)
    return body.replace(marker, marker + patch)


def guard_view(body, marker, label):
    return after_once(body, marker, f'''

    iget-object v0, p0, {COCOS}->mGLSurfaceView:Lorg/cocos2dx/lib/Cocos2dxGLSurfaceView;
    if-nez v0, :{label}
    return-void
    :{label}
''')


def patch(decoded):
    decoded = Path(decoded)
    game_path = decoded / 'smali/com/sygame/jingubang/uc/xiyoujilua.smali'
    cocos_path = decoded / 'smali/org/cocos2dx/lib/Cocos2dxActivity.smali'
    game, cocos = game_path.read_text(), cocos_path.read_text()
    old_gate = f'    invoke-static {{}}, {RUNTIME}->awaitReady()V\n'
    game = game.replace(old_gate, '')
    if ':offline_game_created' in game and 'offlineHasGameView()Z' in cocos:
        if '->awaitReady()V' in game:
            raise RuntimeError('Legacy blocking gate remains')
        game_path.write_text(game)
        return

    def remove_eager_libraries(body):
        # Application's worker loads the same libraries after Python startup.
        call = '    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V'
        if body.count(call) != 2 or '"xiyoujilua"' not in body or '"pocketsphinx_jni"' not in body:
            raise RuntimeError('Game native library initializer changed')
        return body.replace(call, '    # Native libraries are loaded by OfflineRuntime before the GL view.')

    game = change_method(game, '<clinit>()V', remove_eager_libraries)
    marker = f'    invoke-super {{p0, p1}}, {COCOS}->onCreate(Landroid/os/Bundle;)V'
    game = change_method(game, 'onCreate(Landroid/os/Bundle;)V', lambda body: after_once(body, marker, f'''

    invoke-virtual {{p0}}, {COCOS}->offlineHasGameView()Z
    move-result v0
    if-nez v0, :offline_game_created
    invoke-static {{p0}}, {RUNTIME}->relaunch(Landroid/app/Activity;)V
    return-void
    :offline_game_created
'''))
    for callback in ('onResume', 'onDestroy'):
        signature = callback + '()V'
        marker = f'    invoke-super {{p0}}, {COCOS}->{signature}'
        def guard_game(body, marker=marker, callback=callback):
            guard = f'''
    invoke-virtual {{p0}}, {COCOS}->offlineHasGameView()Z
    move-result v0
    if-nez v0, :offline_{callback}_created
{marker}
    return-void
    :offline_{callback}_created
'''
            # Guard before any channel/video code. The preserved body retains
            # its original super call on the initialized branch.
            return after_once(body, '    .prologue', guard)
        game = change_method(game, signature, guard_game)

    marker = '    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V'
    cocos = change_method(cocos, 'onCreate(Landroid/os/Bundle;)V', lambda body: after_once(body, marker, f'''

    sget-boolean v0, {RUNTIME}->ready:Z
    if-nez v0, :offline_cocos_ready
    return-void
    :offline_cocos_ready
'''))
    for callback in ('onResume', 'onPause'):
        signature = callback + '()V'
        marker = f'    invoke-super {{p0}}, Landroid/app/Activity;->{signature}'
        cocos = change_method(cocos, signature, lambda body, marker=marker, callback=callback:
                              guard_view(body, marker, 'offline_cocos_' + callback))
    cocos += f'''
.method public final offlineHasGameView()Z
    .locals 1
    iget-object v0, p0, {COCOS}->mGLSurfaceView:Lorg/cocos2dx/lib/Cocos2dxGLSurfaceView;
    if-eqz v0, :offline_no_game_view
    const/4 v0, 0x1
    return v0
    :offline_no_game_view
    const/4 v0, 0x0
    return v0
.end method
'''
    if '->awaitReady()V' in game:
        raise RuntimeError('Legacy blocking gate remains')
    game_path.write_text(game)
    cocos_path.write_text(cocos)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('decoded', type=Path)
    patch(parser.parse_args().decoded)
