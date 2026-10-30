"""Route the original new-role JNI movie entry to a lifecycle-aware player."""
from pathlib import Path
from .patch_lifecycle import change_method, after_once, COCOS

PLAYER = 'Lcom/jgbol/offline/NewRoleOpening;'


def patch(decoded):
    path = Path(decoded) / 'smali/com/sygame/jingubang/uc/xiyoujilua.smali'
    text = path.read_text()
    if PLAYER in text:
        return
    text = change_method(text, 'startVideo(Ljava/lang/String;)V', lambda _: f'''
    .locals 0
    invoke-static {{p0}}, {PLAYER}->play(Landroid/app/Activity;)V
    return-void
''')
    text = change_method(text, 'isPlaying()Z', lambda _: f'''
    .locals 1
    invoke-static {{p0}}, {PLAYER}->active(Landroid/app/Activity;)Z
    move-result v0
    return v0
''')
    for callback, method in [('onResume', 'resume'), ('onDestroy', 'destroy')]:
        text = change_method(text, callback + '()V', lambda body, method=method:
            after_once(body, '    .prologue',
                       f'\n    invoke-static {{p0}}, {PLAYER}->{method}(Landroid/app/Activity;)V\n'))
    text = change_method(text, 'onKeyDown(ILandroid/view/KeyEvent;)Z', lambda body:
        after_once(body, '    .prologue', f'''
    invoke-static {{p0, p1}}, {PLAYER}->back(Landroid/app/Activity;I)Z
    move-result v0
    if-eqz v0, :opening_original_key
    return v0
    :opening_original_key
'''))
    if '.method protected onPause()V' in text:
        raise RuntimeError('Unexpected game onPause override')
    text += f'''
.method protected onPause()V
    .locals 0
    invoke-static {{p0}}, {PLAYER}->pause(Landroid/app/Activity;)V
    invoke-super {{p0}}, {COCOS}->onPause()V
    return-void
.end method
'''
    path.write_text(text)
