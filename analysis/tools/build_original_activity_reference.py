"""Export audited original client evidence and static UI illustrations; no game access.
Run: python3 analysis/tools/build_original_activity_reference.py
Requires Pillow; reads v107's previously audited 1263 client assets only.
"""
import csv
import hashlib
import io
import json
import math
import plistlib
import re
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from audit_hotupdate_gap import index, table
from luajit_static import parse, listing

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'analysis/evidence/original_activities_20261102'
IMG = ROOT/'docs/assets/original_activities'
MODULES = ['miniGameUI','goldRushUI','friendsUI','lanternRiddleUI','richmanUI','guessUI','kickUI','snowmanUI','dreamUI','omenUI','alchemyUI','summerUI','answerUI','saveMonkeyUI']
TITLES = ['周末小游戏 · 混元五行阵','淘金 · 浪裹捞金','邀友 · 呼朋唤友','灯谜 · 元宵灯谜会','富翁 · 蓬莱访仙','猜谜 · 灯谜会','万寿山 · 魂缘万寿山','雪人 · 全服堆雪人','梦境 · 仙梦居','天象／年兽 · 年兽请留步','炼丹 · 八卦炼丹炉','夏日 · 雷区寻宝','科举 · 科举考试','救悟空 · 十万猴急']
TABLES = '''guide_index guide_detail RiddleChooseWords gold_rush_config friends_lv_reward friends_recharge_reward hill_top_prize dream_prize_config exam_rank_prize monster_food_prize monster_top_prize get_lingqi_method summer_cards_letter summer_cards_tip answer_rule newbie_content7 newbie_content8 newbie_content9 newbie_content10 newbie_content13 newbie_content14 item_name title_config'''.split()
FONT = '/System/Library/Fonts/Hiragino Sans GB.ttc'

def main():
    OUT.mkdir(parents=True,exist_ok=True); IMG.mkdir(parents=True,exist_ok=True); (OUT/'csv').mkdir(exist_ok=True)
    audit=json.loads((ROOT/'analysis/evidence/hotupdate_gap_20261031/audit.json').read_text())
    expected={r['logical']:r['original_sha256'] for key in ['csv','lua','other_resources'] for r in audit[key]}
    base=ROOT/'jgbol3.87/assets/release_'; _,baseidx=index((base/'index.txt').read_bytes())
    a=zipfile.ZipFile(ROOT/'build/金箍棒3.87离线正式版v107.apk');p=zipfile.ZipFile(io.BytesIO(a.read('assets/offline/program.zip')))
    version,idx=index(p.read('client/release_w/index.txt'));assert version==1263; pn=set(p.namelist()); inputs={}; preview_assets={}; active=None
    def read(n):
        name='client/release_w/'+idx[n];raw=p.read(name) if name in pn else a.read('assets/release_/'+idx[n]);sha=hashlib.sha256(raw).hexdigest()
        if n in expected: assert sha==expected[n],n
        else: assert raw==(base/baseidx[n]).read_bytes(),n
        inputs[n]={'logical':n,'sha256':sha,'origin':'official hotupdate audit' if n in expected else 'original 1205 asset'}
        return raw
    strings={n:plistlib.loads(read(n)) for n in ['v2/String.plist','v2/String2.plist']}
    d={**strings['v2/String2.plist'],**strings['v2/String.plist']}
    prefixes=['mini','gold_rush','friends_','friend_code','lantern','riddle','richman','guess','kick','snow','dream','nian','omen','alchemy','summer','answer','saveMonkey']
    selected={k:v for k,v in d.items() if any(k.startswith(s) for s in prefixes)}
    (OUT/'activity_strings.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n')
    for ui in MODULES+['data']:
        logical='lua/'+('ui/' if ui!='data' else '')+ui+'.lua'; s=listing(parse(read(logical)));(OUT/(ui+'.txt')).write_text(s)
        keys=set(re.findall(r"'([^']+)'",s));(OUT/(ui+'_texts.txt')).write_text('\n'.join(f'{k}: {d[k]}' for k in d if k in keys)+'\n')
    for name in TABLES:
        with (OUT/'csv'/(name+'.csv')).open('w') as f: csv.writer(f).writerows(table(read('csv_config/'+name+'.csv')))
    prot=json.loads((ROOT/'analysis/evidence/hotupdate_gap_20261031/protocol_tables_1263.json').read_text())
    ids={1308,1303,1207,1101,1214,1222,1223,1224,1132,1323,1324,1325,1327,1134,1331,1335,1346}
    (OUT/'requests.json').write_text(json.dumps([v for v in prot['gscl_msg'].values() if v['id'] in ids],ensure_ascii=False,indent=2)+'\n')
    def font(sz):return ImageFont.truetype(FONT,sz)
    def txt(x,y,s,size=22,fill='#f6e2ad'):
        dr.text((x,y),s,font=font(size),fill=fill)
    def art(n,x,y,w,h,stretch=False):
        raw=read(n);preview_assets.setdefault(active,[]).append(n); im=Image.open(io.BytesIO(raw)).convert('RGBA')
        if stretch:im=im.resize((w,h),Image.Resampling.LANCZOS)
        else:im.thumbnail((w,h),Image.Resampling.LANCZOS)
        canvas.paste(im,(int(x+(w-im.width)/2),int(y+(h-im.height)/2)),im)
    def panel(x,y,w,h):dr.rounded_rectangle((x,y,x+w,y+h),12,fill='#34291fe9',outline='#ad824b',width=2)
    def button(path,x,y,w=180,h=65):art(path,x,y,w,h)
    def note(lines):
        panel(956,115,300,590);txt(976,137,'玩法与证据',25)
        yy=190
        for line in lines:
            for start in range(0,len(line),12):txt(978,yy,line[start:start+12],20);yy+=31
            yy+=18
    notes=[
      ['A｜五关，每关100分','A｜400分触发骰子通关奖','A｜猜拳／判断／仙缘猜人','B｜奖励池与掷骰分布缺失'],
      ['A｜末版共九网','A｜首网投入66元宝','A｜首网返还88～200元宝','B｜区间内概率未知'],
      ['A｜邀请好友升级、升VIP','A｜升级四档奖励','A｜奖励经系统消息发放','B｜限额与渠道文案有冲突'],
      ['A｜拖字填入谜底','A｜新春红包','A｜有机会获得元宵锦囊','B｜题库、次数、掉率缺失'],
      ['A｜掷骰前进、累积里程','A｜里程兑换与终极大奖','B｜奖励清单与消耗下发','B｜本图不模拟实际掷骰'],
      ['A｜点击选字组成谜底','A｜道具奖与灯谜锦囊','A｜与1214灯谜协议独立','B｜题面、次数、掉率缺失'],
      ['A｜每摘一次加1积分','A｜三种法力状态','A｜末版榜奖六档至50名','B｜概率、阶段门槛缺失'],
      ['A｜五种材料换雪魄','A｜七档进度奖励','A｜圣诞兔20分钟、日限3次','B｜兑换商店数值缺失'],
      ['A｜六关拼图与好友祝福','A｜六关奖励表已提取','A｜18级开放（原说明）','B｜充值奖励文案存在冲突'],
      ['A｜三种年兽、三种道具','A｜初始粮食1500袋','A｜每100伤害得1辞岁点','B｜血量、刷新、概率缺失'],
      ['A｜材料＋灵气炼制','A｜金丹、银丹、铜丹','A｜四天活动、末日仅兑换','B｜配方、概率、回收比缺失'],
      ['A｜扫雷、开箱、集字','A｜翻格／长按标记','A｜西行取经／师徒西行','B｜雷图与消耗参数缺失'],
      ['A｜乡试→会试→殿试','A｜七天周期、每天一次','A｜晋级15／5／10人','B｜题库、计分公式缺失'],
      ['A｜风火雷宝珠破石救猴','A｜碎石商店、活跃奖励','A｜侦察范围30深度','B｜地图及奖池缺失']]
    for i,ui in enumerate(MODULES):
        active=ui;canvas=Image.new('RGBA',(1280,800),'#171e27');dr=ImageDraw.Draw(canvas)
        txt(26,20,TITLES[i],32);txt(28,69,'原素材静态界面示意｜非原服实机截图｜布局经重排；不表示已接入',18,'#aebfce')
        panel(24,115,912,590)
        folder='miniGame' if ui=='miniGameUI' else 'lanternRiddleUI' if ui=='guessUI' else ui
        bg=f'v2/{folder}/bkg.jpg'
        if bg in idx:art(bg,26,117,908,586,True)
        elif ui=='miniGameUI':art('v2/miniGame/bkg.png',26,117,908,586,True)
        # Individual views use original art; all synthetic state is labelled.
        if ui=='miniGameUI':
            art('v2/miniGame/title0.png',300,130,350,55);art('v2/miniGame/land.png',180,230,590,310)
            for j,(x,y) in enumerate([(430,250),(270,340),(350,440),(530,440),(610,340)]):art(f'v2/miniGame/p_{j+1}.png',x,y,110,70)
            for j in range(3):art(f'v2/miniGame/game{j+1}1.png',85+j*270,565,230,55)
            panel(300,630,370,46);txt(320,640,'队伍、分数与关卡状态待下发',18)
        elif ui=='goldRushUI':
            art('v2/goldRushUI/title.png',300,135,350,60)
            for j in range(4):art(f'v2/goldRushUI/gold_{j+1}.png',100+j*200,300,150,140)
            panel(180,200,600,65);txt(215,215,'首网规则预览：66 → 88～200 元宝',25)
            button('v2/goldRushUI/rush_btn.png',370,500,220,85)
            panel(150,610,660,50);txt(175,622,'九档配置已确认；此图没有执行撒网',21)
        elif ui=='friendsUI':
            art('v2/friendsUI/title.png',310,135,330,55);art('v2/friendsUI/up.png',100,210,740,220)
            panel(115,445,720,80);txt(145,468,'邀请码：未绑定（静态预览）',24)
            button('v2/friendsUI/copy_btn1.png',140,560);button('v2/friendsUI/detail_btn1.png',370,560);button('v2/friendsUI/input1.png',600,560)
        elif ui in ['lanternRiddleUI','guessUI']:
            art('v2/lanternRiddleUI/'+('title3.png' if ui=='lanternRiddleUI' else 'tittle.png'),310,135,340,60)
            art('v2/lanternRiddleUI/char.png',40,230,230,360)
            art('v2/lanternRiddleUI/frame2.png',290,225,590,320,True)
            txt(340,265,'题面由原服下发，未填造题库',23,'#492d20')
            for j in range(4):art('v2/lanternRiddleUI/word2.png',360+j*105,340,70,70)
            for j in range(6):art('v2/lanternRiddleUI/word1.png',325+j*85,445,58,58)
            button('v2/lanternRiddleUI/skip1.png',480,565)
        elif ui=='richmanUI':
            art('v2/richmanUI/title.png',300,135,350,60);art('v2/richmanUI/bkg1.png',70,210,800,330)
            button('v2/richmanUI/roll1.png',240,565,80,80);button('v2/richmanUI/to_shop1.png',380,565);button('v2/richmanUI/mbuy1.png',620,565,240,70)
        elif ui=='kickUI':
            art('v2/kickUI/bkg.png',26,117,908,586,True);art('v2/kickUI/title.png',295,130,370,60)
            for j in range(3):button(f'v2/kickUI/menu{j+1}1.png',735,220+j*140,125,105)
            for j in range(3):art('v2/kickUI/menu41.png',130+j*190,550,70,80)
            panel(90,645,570,40);txt(110,652,'三档阶段礼：具体门槛与奖励待下发',18)
        elif ui=='snowmanUI':
            art('v2/snowmanUI/title.png',300,135,350,70);art('v2/snowmanUI/man7.png',270,280,300,290);art('v2/snowmanUI/rabbit.png',670,330,140,150)
            button('v2/snowmanUI/shop1.png',750,535,130,110);art('v2/snowmanUI/bkg5.png',110,225,720,35)
            panel(100,600,620,65);txt(120,619,'阶段：10 / 20 / 30 / 40 / 60 / 80 / 100%',21)
        elif ui=='dreamUI':
            art('v2/dreamUI/title.png',310,130,340,65)
            for j in range(6):
                x=75+(j%3)*280;y=220+(j//3)*180;art(f'v2/dreamUI/pic{j+1}.png',x,y,250,145)
            button('v2/dreamUI/btn41.png',360,610,230,65)
        elif ui=='omenUI':
            art('v2/omenUI/title.png',300,130,350,65)
            for j in range(3):art(f'v2/omenUI/omen{j+1}.png',150+j*230,310,150,155);art(f'v2/omenUI/btn_{1125+j}_1.png',165+j*230,525,120,110)
            panel(235,210,500,55);txt(260,222,'小年兽 / 大年兽 / 多宝年兽',23)
        elif ui=='alchemyUI':
            art('v2/alchemyUI/title.png',300,130,350,65);art('v2/alchemyUI/stove.png',310,285,320,270)
            for j in range(8):
                ang=j*math.pi/4;x=455+230*math.cos(ang)-37;y=390+165*math.sin(ang)-37;art(f'v2/alchemyUI/pos{j+1}1.png',x,y,75,75)
            button('v2/alchemyUI/refine1.png',355,610,240,65);button('v2/alchemyUI/change1.png',760,530,125,120)
        elif ui=='summerUI':
            art('v2/summerUI/title.png',300,130,350,65)
            for row in range(6):
                for col in range(9):art('v2/summerUI/grid1.png',90+col*65,220+row*65,61,61)
            # No invented mine locations or board dimensions claimed; illustrative viewport only.
            for j,button_name in enumerate(['start1','mark1','change1','shop1']):button('v2/summerUI/'+button_name+'.png',715,210+j*108,170,90)
            txt(115,630,'格子窗口示意；实际地图尺寸、雷数待下发',20)
        elif ui=='answerUI':
            art('v2/answerUI/title.png',300,130,350,65);art('v2/answerUI/abkg.png',80,220,790,340,True)
            txt(350,315,'题目及选项由原服下发',25,'#492d20')
            for j in range(4):art('v2/answerUI/op1.png',340,365+j*40,420,38)
            for j in range(4):button(f'v2/answerUI/btn{j+1}1.png',80+j*205,605,185,60)
        elif ui=='saveMonkeyUI':
            art('v2/saveMonkeyUI/title.png',300,130,350,65)
            for row in range(5):
                for col in range(8):art('v2/saveMonkeyUI/rock11.png',90+col*73,220+row*73,70,70)
            for j,n in enumerate(['feng1','huo1','lei1','eye']):art('v2/saveMonkeyUI/'+n+'.png',740,210+j*105,85,85)
            button('v2/saveMonkeyUI/exchange1.png',120,610,250,65);button('v2/saveMonkeyUI/getToy1.png',420,610,250,65)
        note(notes[i]);txt(26,739,'A = 原客户端规则／表值证据   B = 缺失或冲突待核；图中按钮仅供展示，不可操作',19,'#aebfce')
        canvas.convert('RGB').save(IMG/(ui+'.png'))
    (OUT/'manifest.json').write_text(json.dumps({'version':1263,'verification':'Every extracted resource matches original 1205 bytes or official hotupdate SHA-256 audit.','inputs':list(inputs.values()),'preview_assets':preview_assets,'preview_kind':'Static original-art composition, rearranged layout; not a native runtime capture; no game/saves/network accessed.'},ensure_ascii=False,indent=2)+'\n')
    # Preserve original instructional artwork as additional A evidence.
    for logical, filename in [('v2/saveMonkeyUI/bkg8.png','saveMonkey_original_guide.png'), ('v2/alchemyUI/tip2.png','alchemy_original_unlock1.png'), ('v2/alchemyUI/tip3.png','alchemy_original_unlock2.png'), ('v2/alchemyUI/tip4.png','alchemy_original_unlock3.png')]:
        (IMG/filename).write_bytes(read(logical))
    # Update manifest after supplemental evidence export.
    manifest=json.loads((OUT/'manifest.json').read_text()); manifest['inputs']=list(inputs.values())
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    # A contact overview makes verification of all 14 images easy.
    contact=Image.new('RGB',(1280,7*400),'#171e27')
    for i,ui in enumerate(MODULES):
        im=Image.open(IMG/(ui+'.png'));im.thumbnail((640,400));contact.paste(im,((i%2)*640,(i//2)*400))
    contact.save(IMG/'overview.jpg',quality=88)
    print(json.dumps({'previews':len(MODULES),'verified_resources':len(inputs),'output':str(IMG)},ensure_ascii=False))

if __name__=='__main__':main()
