LuaJIT dump version=1; source='@D:\\mg_update_\\lua_cache\\lua1\\96d7bfc80446c4ad76e979a14eb48185.data'; root=proto67

FUNCTION proto0 offset=0x4a source_lines=85-88 params=0
UPVALUES ['CCLuaLog', 'string']
00001 [L87] UGET     A=0 B=0 C=0 D=0 CCLuaLog
00002 [L87] UGET     A=1 B=0 C=1 D=1 string
00003 [L87] TGETS    A=1 B=1 C=0 D=256 'format'
00004 [L87] VARG     A=2 B=0 C=0 D=0 
00005 [L87] CALLM    A=1 B=0 C=0 D=0 
00006 [L87] CALLM    A=0 B=1 C=0 D=256 
00007 [L88] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto1 offset=0x95 source_lines=165-185 params=0
UPVALUES ['cclog']
00001 [L166] UGET     A=0 B=0 C=0 D=0 cclog
00002 [L166] KSTR     A=1 B=0 C=0 D=0 'show Package'
00003 [L166] CALL     A=0 B=1 C=2 D=258 
00004 [L168] GGET     A=0 B=0 C=1 D=1 'd_ms'
00005 [L168] TGETS    A=0 B=0 C=2 D=2 'd_tianShuUI'
00006 [L168] TGETS    A=0 B=0 C=3 D=3 'showHint'
00007 [L168] CALL     A=0 B=1 C=1 D=257 
00008 [L170] GGET     A=0 B=0 C=4 D=4 'create'
00009 [L170] GGET     A=1 B=0 C=1 D=1 'd_ms'
00010 [L170] TGETS    A=1 B=1 C=5 D=261 'd_mainUI'
00011 [L170] TGETS    A=1 B=1 C=6 D=262 'g_mainUI'
00012 [L170] TGETS    A=1 B=1 C=7 D=263 'main_layer'
00013 [L170] CALL     A=0 B=1 C=2 D=258 
00014 [L178] GGET     A=0 B=0 C=1 D=1 'd_ms'
00015 [L178] TGETS    A=0 B=0 C=5 D=5 'd_mainUI'
00016 [L178] TGETS    A=0 B=0 C=6 D=6 'g_mainUI'
00017 [L178] TGETS    A=0 B=0 C=8 D=8 'player_layer'
00018 [L178] MOV      A=1 B=0 C=0 D=0 
00019 [L178] TGETS    A=0 B=0 C=9 D=9 'setVisible'
00020 [L178] KPRI     A=2 B=0 C=1 D=1 
00021 [L178] CALL     A=0 B=1 C=3 D=259 
00022 [L181] GGET     A=0 B=0 C=1 D=1 'd_ms'
00023 [L181] TGETS    A=0 B=0 C=5 D=5 'd_mainUI'
00024 [L181] TGETS    A=0 B=0 C=6 D=6 'g_mainUI'
00025 [L181] TGETS    A=0 B=0 C=10 D=10 'menu_other_layer'
00026 [L181] ISEQP    A=0 B=0 C=0 D=0 
00027 [L181] JMP      A=0 B=128 C=16 D=32784 target=44
00028 [L182] GGET     A=0 B=0 C=1 D=1 'd_ms'
00029 [L182] TGETS    A=0 B=0 C=5 D=5 'd_mainUI'
00030 [L182] TGETS    A=0 B=0 C=6 D=6 'g_mainUI'
00031 [L182] TGETS    A=0 B=0 C=7 D=7 'main_layer'
00032 [L182] MOV      A=1 B=0 C=0 D=0 
00033 [L182] TGETS    A=0 B=0 C=11 D=11 'removeChild'
00034 [L182] GGET     A=2 B=0 C=12 D=12 'dMainUI'
00035 [L182] TGETS    A=2 B=2 C=6 D=518 'g_mainUI'
00036 [L182] TGETS    A=2 B=2 C=10 D=522 'menu_other_layer'
00037 [L182] KPRI     A=3 B=0 C=2 D=2 
00038 [L182] CALL     A=0 B=1 C=4 D=260 
00039 [L183] GGET     A=0 B=0 C=1 D=1 'd_ms'
00040 [L183] TGETS    A=0 B=0 C=5 D=5 'd_mainUI'
00041 [L183] TGETS    A=0 B=0 C=6 D=6 'g_mainUI'
00042 [L183] KPRI     A=1 B=0 C=0 D=0 
00043 [L183] TSETS    A=1 B=0 C=10 D=10 'menu_other_layer'
00044 [L185] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto2 offset=0x20f source_lines=206-214 params=1
UPVALUES []
00001 [L207] TGETS    A=1 B=0 C=0 D=0 'name'
00002 [L207] ISNES    A=1 B=0 C=1 D=1 'exit'
00003 [L207] JMP      A=1 B=128 C=11 D=32779 target=15
00004 [L208] TNEW     A=1 B=0 C=0 D=0 
00005 [L208] GSET     A=1 B=0 C=2 D=2 'g_updatePackageFunc'
00006 [L209] KPRI     A=1 B=0 C=1 D=1 
00007 [L209] GSET     A=1 B=0 C=3 D=3 'g_isInPackage'
00008 [L210] KSHORT   A=1 B=0 C=0 D=0 0
00009 [L210] GSET     A=1 B=0 C=4 D=4 'g_lastSelectedItemButton'
00010 [L211] TNEW     A=1 B=0 C=0 D=0 
00011 [L211] GSET     A=1 B=0 C=5 D=5 'g_lastRequestUsedItem'
00012 [L212] GGET     A=1 B=0 C=6 D=6 'packageTagDef'
00013 [L212] TGETS    A=1 B=1 C=7 D=263 'none'
00014 [L212] GSET     A=1 B=0 C=8 D=8 'g_packageTag'
00015 [L214] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto3 offset=0x2ef source_lines=188-259 params=1
UPVALUES ['CCDirector', 'CCLayer']
00001 [L190] MOV      A=2 B=0 C=0 D=0 
00002 [L190] TGETS    A=1 B=0 C=0 D=0 'getChildByTag'
00003 [L190] GGET     A=3 B=0 C=1 D=1 'd_ms'
00004 [L190] TGETS    A=3 B=3 C=2 D=770 'd_mainUI'
00005 [L190] TGETS    A=3 B=3 C=3 D=771 'boardID'
00006 [L190] TGETS    A=3 B=3 C=4 D=772 'package'
00007 [L190] CALL     A=1 B=2 C=3 D=515 
00008 [L191] ISF      A=0 B=0 C=1 D=1 
00009 [L191] JMP      A=2 B=128 C=1 D=32769 target=11
00010 [L192] UCLO     A=0 B=128 C=173 D=32941 target=184
00011 [L195] UGET     A=2 B=0 C=0 D=0 CCDirector
00012 [L195] MOV      A=3 B=0 C=2 D=2 
00013 [L195] TGETS    A=2 B=2 C=5 D=517 'sharedDirector'
00014 [L195] CALL     A=2 B=2 C=2 D=514 
00015 [L195] MOV      A=3 B=0 C=2 D=2 
00016 [L195] TGETS    A=2 B=2 C=6 D=518 'getVisibleSize'
00017 [L195] CALL     A=2 B=2 C=2 D=514 
00018 [L196] TNEW     A=3 B=0 C=0 D=0 
00019 [L196] GSET     A=3 B=0 C=7 D=7 'g_packageUI'
00020 [L197] MOV      A=3 B=0 C=0 D=0 
00021 [L200] UGET     A=4 B=0 C=1 D=1 CCLayer
00022 [L200] MOV      A=5 B=0 C=4 D=4 
00023 [L200] TGETS    A=4 B=4 C=8 D=1032 'create'
00024 [L200] CALL     A=4 B=2 C=2 D=514 
00025 [L201] MOV      A=6 B=0 C=0 D=0 
00026 [L201] TGETS    A=5 B=0 C=9 D=9 'addChild'
00027 [L201] MOV      A=7 B=0 C=4 D=4 
00028 [L201] KSHORT   A=8 B=0 C=5 D=5 5
00029 [L201] CALL     A=5 B=1 C=4 D=260 
00030 [L202] GGET     A=5 B=0 C=1 D=1 'd_ms'
00031 [L202] TGETS    A=5 B=5 C=2 D=1282 'd_mainUI'
00032 [L202] TGETS    A=5 B=5 C=10 D=1290 'g_boardlayer'
00033 [L202] GGET     A=6 B=0 C=1 D=1 'd_ms'
00034 [L202] TGETS    A=6 B=6 C=2 D=1538 'd_mainUI'
00035 [L202] TGETS    A=6 B=6 C=3 D=1539 'boardID'
00036 [L202] TGETS    A=6 B=6 C=4 D=1540 'package'
00037 [L202] TSETV    A=4 B=5 C=6 D=1286 
00038 [L203] MOV      A=6 B=0 C=4 D=4 
00039 [L203] TGETS    A=5 B=4 C=11 D=1035 'setTag'
00040 [L203] GGET     A=7 B=0 C=1 D=1 'd_ms'
00041 [L203] TGETS    A=7 B=7 C=2 D=1794 'd_mainUI'
00042 [L203] TGETS    A=7 B=7 C=3 D=1795 'boardID'
00043 [L203] TGETS    A=7 B=7 C=4 D=1796 'package'
00044 [L203] CALL     A=5 B=1 C=3 D=259 
00045 [L205] KPRI     A=5 B=0 C=2 D=2 
00046 [L205] GSET     A=5 B=0 C=12 D=12 'g_isInPackage'
00047 [L214] FNEW     A=5 B=0 C=13 D=13 {'kind': 'proto', 'id': 2}
00048 [L216] MOV      A=7 B=0 C=4 D=4 
00049 [L216] TGETS    A=6 B=4 C=14 D=1038 'registerScriptHandler'
00050 [L216] MOV      A=8 B=0 C=5 D=5 
00051 [L216] CALL     A=6 B=1 C=3 D=259 
00052 [L218] GGET     A=6 B=0 C=1 D=1 'd_ms'
00053 [L218] TGETS    A=6 B=6 C=2 D=1538 'd_mainUI'
00054 [L218] TGETS    A=6 B=6 C=15 D=1551 'showBoard'
00055 [L218] MOV      A=7 B=0 C=4 D=4 
00056 [L218] CALL     A=6 B=1 C=2 D=258 
00057 [L219] GGET     A=6 B=0 C=1 D=1 'd_ms'
00058 [L219] TGETS    A=6 B=6 C=2 D=1538 'd_mainUI'
00059 [L219] GGET     A=7 B=0 C=1 D=1 'd_ms'
00060 [L219] TGETS    A=7 B=7 C=2 D=1794 'd_mainUI'
00061 [L219] TGETS    A=7 B=7 C=3 D=1795 'boardID'
00062 [L219] TGETS    A=7 B=7 C=4 D=1796 'package'
00063 [L219] TSETS    A=7 B=6 C=16 D=1552 'g_currentBoard'
00064 [L221] GGET     A=6 B=0 C=7 D=7 'g_packageUI'
00065 [L221] TSETS    A=4 B=6 C=17 D=1553 'board_layer'
00066 [L222] GGET     A=6 B=0 C=7 D=7 'g_packageUI'
00067 [L222] TSETS    A=0 B=6 C=18 D=1554 'parent'
00068 [L224] TDUP     A=6 B=0 C=19 D=19 {'kind': 'table', 'value': {'x': 0.5, 'y': 0.56}}
00069 [L225] TDUP     A=7 B=0 C=20 D=20 {'kind': 'table', 'value': {'scaleY': 0.8, 'scaleX': 0.95}}
00070 [L226] GGET     A=8 B=0 C=7 D=7 'g_packageUI'
00071 [L226] GGET     A=9 B=0 C=1 D=1 'd_ms'
00072 [L226] TGETS    A=9 B=9 C=2 D=2306 'd_mainUI'
00073 [L226] TGETS    A=9 B=9 C=22 D=2326 'createBoardBkg'
00074 [L226] MOV      A=10 B=0 C=4 D=4 
00075 [L226] MOV      A=11 B=0 C=6 D=6 
00076 [L226] MOV      A=12 B=0 C=7 D=7 
00077 [L226] KPRI     A=13 B=0 C=1 D=1 
00078 [L226] CALL     A=9 B=2 C=5 D=517 
00079 [L226] TSETS    A=9 B=8 C=21 D=2069 'board_size'
00080 [L229] TDUP     A=8 B=0 C=23 D=23 {'kind': 'table', 'value': {'x': 0.12, 'y': 0.88}}
00081 [L232] TDUP     A=9 B=0 C=24 D=24 {'kind': 'table', 'value': {'npic': 'v2/packageUI/Label_weapon1.png', 'scale': 0.18, 'disPic': 'v2/packageUI/Label_weapon2.png', 'x': 0}}
00082 [L234] KNUM     A=10 B=0 C=1 D=1 -0.11
00083 [L234] MULVN    A=10 B=10 C=0 D=2560 
00084 [L234] TSETS    A=10 B=9 C=25 D=2329 'y'
00085 [L234] GGET     A=10 B=0 C=26 D=26 'packageTagDef'
00086 [L234] TGETS    A=10 B=10 C=27 D=2587 'weapon'
00087 [L234] TSETS    A=10 B=9 C=28 D=2332 'tag'
00088 [L234] GGET     A=10 B=0 C=29 D=29 'showPackage'
00089 [L234] TSETS    A=10 B=9 C=30 D=2334 'call_back'
00090 [L234] TSETB    A=9 B=8 C=1 D=2049 
00091 [L234] TDUP     A=9 B=0 C=31 D=31 {'kind': 'table', 'value': {'npic': 'v2/packageUI/Label_armor1.png', 'scale': 0.18, 'disPic': 'v2/packageUI/Label_armor2.png', 'y': -0.11, 'x': 0}}
00092 [L235] GGET     A=10 B=0 C=26 D=26 'packageTagDef'
00093 [L235] TGETS    A=10 B=10 C=32 D=2592 'armor'
00094 [L235] TSETS    A=10 B=9 C=28 D=2332 'tag'
00095 [L235] GGET     A=10 B=0 C=29 D=29 'showPackage'
00096 [L235] TSETS    A=10 B=9 C=30 D=2334 'call_back'
00097 [L235] TSETB    A=9 B=8 C=2 D=2050 
00098 [L235] TDUP     A=9 B=0 C=33 D=33 {'kind': 'table', 'value': {'npic': 'v2/packageUI/Label_magic-item1.png', 'scale': 0.18, 'disPic': 'v2/packageUI/Label_magic-item2.png', 'y': -0.22, 'x': 0}}
00099 [L236] GGET     A=10 B=0 C=26 D=26 'packageTagDef'
00100 [L236] TGETS    A=10 B=10 C=34 D=2594 'fabao'
00101 [L236] TSETS    A=10 B=9 C=28 D=2332 'tag'
00102 [L236] GGET     A=10 B=0 C=29 D=29 'showPackage'
00103 [L236] TSETS    A=10 B=9 C=30 D=2334 'call_back'
00104 [L236] TSETB    A=9 B=8 C=3 D=2051 
00105 [L236] TDUP     A=9 B=0 C=35 D=35 {'kind': 'table', 'value': {'npic': 'v2/packageUI/Label_spell1.png', 'scale': 0.18, 'disPic': 'v2/packageUI/Label_spell2.png', 'y': -0.33, 'x': 0}}
00106 [L237] GGET     A=10 B=0 C=26 D=26 'packageTagDef'
00107 [L237] TGETS    A=10 B=10 C=36 D=2596 'skill'
00108 [L237] TSETS    A=10 B=9 C=28 D=2332 'tag'
00109 [L237] GGET     A=10 B=0 C=29 D=29 'showPackage'
00110 [L237] TSETS    A=10 B=9 C=30 D=2334 'call_back'
00111 [L237] TSETB    A=9 B=8 C=4 D=2052 
00112 [L237] TDUP     A=9 B=0 C=37 D=37 {'kind': 'table', 'value': {'npic': 'v2/packageUI/stone1.png', 'scale': 0.18, 'disPic': 'v2/packageUI/stone2.png', 'y': -0.44, 'x': 0}}
00113 [L238] GGET     A=10 B=0 C=26 D=26 'packageTagDef'
00114 [L238] TGETS    A=10 B=10 C=38 D=2598 'stone'
00115 [L238] TSETS    A=10 B=9 C=28 D=2332 'tag'
00116 [L238] GGET     A=10 B=0 C=29 D=29 'showPackage'
00117 [L238] TSETS    A=10 B=9 C=30 D=2334 'call_back'
00118 [L238] TSETB    A=9 B=8 C=5 D=2053 
00119 [L238] TDUP     A=9 B=0 C=39 D=39 {'kind': 'table', 'value': {'npic': 'v2/packageUI/Label_props1.png', 'scale': 0.18, 'disPic': 'v2/packageUI/Label_props2.png', 'y': -0.55, 'x': 0}}
00120 [L239] GGET     A=10 B=0 C=26 D=26 'packageTagDef'
00121 [L239] TGETS    A=10 B=10 C=40 D=2600 'props'
00122 [L239] TSETS    A=10 B=9 C=28 D=2332 'tag'
00123 [L239] GGET     A=10 B=0 C=29 D=29 'showPackage'
00124 [L239] TSETS    A=10 B=9 C=30 D=2334 'call_back'
00125 [L239] TSETB    A=9 B=8 C=6 D=2054 
00126 [L239] TDUP     A=9 B=0 C=41 D=41 {'kind': 'table', 'value': {'npic': 'v2/smithUI/smith1.png', 'scale': 0.12, 'disPic': 'v2/smithUI/smith2.png', 'y': -0.66, 'x': 0}}
00127 [L240] GGET     A=10 B=0 C=42 D=42 'pressSmith'
00128 [L240] TSETS    A=10 B=9 C=30 D=2334 'call_back'
00129 [L240] TSETB    A=9 B=8 C=7 D=2055 
00130 [L243] GGET     A=9 B=0 C=1 D=1 'd_ms'
00131 [L243] TGETS    A=9 B=9 C=43 D=2347 'd_stoneUI'
00132 [L243] TGETS    A=9 B=9 C=44 D=2348 'g_self'
00133 [L243] TGETS    A=9 B=9 C=45 D=2349 'isOpen'
00134 [L243] IST      A=0 B=0 C=9 D=9 
00135 [L243] JMP      A=9 B=128 C=10 D=32778 target=146
00136 [L244] KSHORT   A=9 B=0 C=6 D=6 6
00137 [L244] KSHORT   A=10 B=0 C=7 D=7 7
00138 [L244] KSHORT   A=11 B=0 C=1 D=1 1
00139 [L244] FORI     A=9 B=128 C=6 D=32774 target=146
00140 [L245] TGETV    A=13 B=8 C=12 D=2060 
00141 [L245] TGETV    A=14 B=8 C=12 D=2060 
00142 [L245] TGETS    A=14 B=14 C=25 D=3609 'y'
00143 [L245] ADDVN    A=14 B=14 C=2 D=3586 
00144 [L245] TSETS    A=14 B=13 C=25 D=3353 'y'
00145 [L244] FORL     A=9 B=127 C=250 D=32762 target=140
00146 [L248] TNEW     A=9 B=0 C=0 D=0 
00147 [L248] GSET     A=9 B=0 C=46 D=46 'g_itemButton'
00148 [L249] MOV      A=10 B=0 C=4 D=4 
00149 [L249] TGETS    A=9 B=4 C=9 D=1033 'addChild'
00150 [L249] GGET     A=11 B=0 C=1 D=1 'd_ms'
00151 [L249] TGETS    A=11 B=11 C=47 D=2863 'd_u'
00152 [L249] TGETS    A=11 B=11 C=48 D=2864 'createMenu'
00153 [L249] MOV      A=12 B=0 C=8 D=8 
00154 [L249] GGET     A=13 B=0 C=46 D=46 'g_itemButton'
00155 [L249] KPRI     A=14 B=0 C=2 D=2 
00156 [L249] CALL     A=11 B=2 C=4 D=516 
00157 [L249] KSHORT   A=12 B=0 C=5 D=5 5
00158 [L249] CALL     A=9 B=1 C=4 D=260 
00159 [L251] GGET     A=9 B=0 C=1 D=1 'd_ms'
00160 [L251] TGETS    A=9 B=9 C=43 D=2347 'd_stoneUI'
00161 [L251] TGETS    A=9 B=9 C=44 D=2348 'g_self'
00162 [L251] TGETS    A=9 B=9 C=45 D=2349 'isOpen'
00163 [L251] IST      A=0 B=0 C=9 D=9 
00164 [L251] JMP      A=9 B=128 C=12 D=32780 target=177
00165 [L252] GGET     A=9 B=0 C=46 D=46 'g_itemButton'
00166 [L252] TGETB    A=9 B=9 C=5 D=2309 
00167 [L252] MOV      A=10 B=0 C=9 D=9 
00168 [L252] TGETS    A=9 B=9 C=49 D=2353 'setVisible'
00169 [L252] KPRI     A=11 B=0 C=1 D=1 
00170 [L252] CALL     A=9 B=1 C=3 D=259 
00171 [L253] GGET     A=9 B=0 C=46 D=46 'g_itemButton'
00172 [L253] TGETB    A=9 B=9 C=5 D=2309 
00173 [L253] MOV      A=10 B=0 C=9 D=9 
00174 [L253] TGETS    A=9 B=9 C=50 D=2354 'setEnabled'
00175 [L253] KPRI     A=11 B=0 C=1 D=1 
00176 [L253] CALL     A=9 B=1 C=3 D=259 
00177 [L256] KSHORT   A=9 B=0 C=0 D=0 0
00178 [L256] GSET     A=9 B=0 C=51 D=51 'g_lastSelectedItemButton'
00179 [L258] GGET     A=9 B=0 C=29 D=29 'showPackage'
00180 [L258] GGET     A=10 B=0 C=26 D=26 'packageTagDef'
00181 [L258] TGETS    A=10 B=10 C=27 D=2587 'weapon'
00182 [L258] CALL     A=9 B=1 C=2 D=258 
00183 [L259] RET0     A=0 B=0 C=1 D=1 
00184 [L259] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto4 offset=0xc27 source_lines=261-264 params=0
UPVALUES []
00001 [L263] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L263] TGETS    A=0 B=0 C=1 D=1 'd_smithUI'
00003 [L263] TGETS    A=0 B=0 C=2 D=2 'show'
00004 [L263] CALL     A=0 B=1 C=1 D=257 
00005 [L264] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto5 offset=0xc62 source_lines=267-270 params=1
UPVALUES []
00001 [L268] GGET     A=1 B=0 C=0 D=0 'd_ms'
00002 [L268] TGETS    A=1 B=1 C=1 D=257 'd_handbookUI'
00003 [L268] TGETS    A=1 B=1 C=2 D=258 'g_self'
00004 [L268] TSETS    A=0 B=1 C=3 D=259 'ready_open_tag'
00005 [L269] GGET     A=1 B=0 C=0 D=0 'd_ms'
00006 [L269] TGETS    A=1 B=1 C=4 D=260 'd_other_functionUI'
00007 [L269] TGETS    A=1 B=1 C=5 D=261 'menuHandbookCallback'
00008 [L269] MOV      A=2 B=0 C=0 D=0 
00009 [L269] CALL     A=1 B=1 C=2 D=258 
00010 [L270] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto6 offset=0xd00 source_lines=293-304 params=1
UPVALUES ['pairs', 'noUseBtnProps', 'type']
00001 [L294] UGET     A=1 B=0 C=0 D=0 pairs
00002 [L294] UGET     A=2 B=0 C=1 D=1 noUseBtnProps
00003 [L294] CALL     A=1 B=4 C=2 D=1026 
00004 [L294] ISNEXT   A=4 B=128 C=18 D=32786 target=23
00005 [L295] UGET     A=6 B=0 C=2 D=2 type
00006 [L295] MOV      A=7 B=0 C=5 D=5 
00007 [L295] CALL     A=6 B=2 C=2 D=514 
00008 [L295] ISNES    A=6 B=0 C=0 D=0 'table'
00009 [L295] JMP      A=6 B=128 C=9 D=32777 target=19
00010 [L296] TGETB    A=6 B=5 C=1 D=1281 
00011 [L296] ISGT     A=6 B=0 C=0 D=0 
00012 [L296] JMP      A=6 B=128 C=10 D=32778 target=23
00013 [L296] TGETB    A=6 B=5 C=2 D=1282 
00014 [L296] ISGT     A=0 B=0 C=6 D=6 
00015 [L296] JMP      A=6 B=128 C=7 D=32775 target=23
00016 [L297] KPRI     A=6 B=0 C=1 D=1 
00017 [L297] RET1     A=6 B=0 C=2 D=2 
00018 [L298] JMP      A=6 B=128 C=4 D=32772 target=23
00019 [L299] ISNEV    A=5 B=0 C=0 D=0 
00020 [L299] JMP      A=6 B=128 C=2 D=32770 target=23
00021 [L300] KPRI     A=6 B=0 C=1 D=1 
00022 [L300] RET1     A=6 B=0 C=2 D=2 
00023 [L294] ITERN    A=4 B=3 C=3 D=771 
00024 [L294] ITERL    A=4 B=127 C=236 D=32748 target=5
00025 [L303] KPRI     A=1 B=0 C=2 D=2 
00026 [L303] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto7 offset=0xdcf source_lines=305-321 params=1
UPVALUES ['m_t']
00001 [L306] KPRI     A=1 B=0 C=0 D=0 
00002 [L307] TGETS    A=2 B=0 C=0 D=0 'equip_order'
00003 [L307] ISF      A=0 B=0 C=2 D=2 
00004 [L307] JMP      A=3 B=128 C=35 D=32803 target=40
00005 [L307] TGETS    A=2 B=0 C=0 D=0 'equip_order'
00006 [L307] KSHORT   A=3 B=0 C=0 D=0 0
00007 [L307] ISGE     A=3 B=0 C=2 D=2 
00008 [L307] JMP      A=2 B=128 C=31 D=32799 target=40
00009 [L308] TGETS    A=2 B=0 C=0 D=0 'equip_order'
00010 [L308] KSHORT   A=3 B=0 C=8 D=8 8
00011 [L308] ISGT     A=2 B=0 C=3 D=3 
00012 [L308] JMP      A=2 B=128 C=13 D=32781 target=26
00013 [L309] GGET     A=2 B=0 C=1 D=1 'd_ms'
00014 [L309] TGETS    A=2 B=2 C=2 D=514 'd_data'
00015 [L309] TGETS    A=2 B=2 C=3 D=515 'getMyCortName'
00016 [L309] GGET     A=3 B=0 C=1 D=1 'd_ms'
00017 [L309] TGETS    A=3 B=3 C=4 D=772 'd_lineupUI'
00018 [L309] TGETS    A=3 B=3 C=5 D=773 'g_usedCharacters'
00019 [L309] TGETS    A=4 B=0 C=0 D=0 'equip_order'
00020 [L309] TGETV    A=3 B=3 C=4 D=772 
00021 [L309] TGETS    A=3 B=3 C=6 D=774 'character'
00022 [L309] TGETS    A=3 B=3 C=7 D=775 'type'
00023 [L309] CALL     A=2 B=2 C=2 D=514 
00024 [L309] MOV      A=1 B=0 C=2 D=2 
00025 [L309] JMP      A=2 B=128 C=35 D=32803 target=61
00026 [L311] GGET     A=2 B=0 C=1 D=1 'd_ms'
00027 [L311] TGETS    A=2 B=2 C=2 D=514 'd_data'
00028 [L311] TGETS    A=2 B=2 C=3 D=515 'getMyCortName'
00029 [L311] GGET     A=3 B=0 C=1 D=1 'd_ms'
00030 [L311] TGETS    A=3 B=3 C=4 D=772 'd_lineupUI'
00031 [L311] TGETS    A=3 B=3 C=8 D=776 'g_cheerCharacters'
00032 [L311] TGETS    A=4 B=0 C=0 D=0 'equip_order'
00033 [L311] SUBVN    A=4 B=4 C=0 D=1024 
00034 [L311] TGETV    A=3 B=3 C=4 D=772 
00035 [L311] TGETS    A=3 B=3 C=6 D=774 'character'
00036 [L311] TGETS    A=3 B=3 C=7 D=775 'type'
00037 [L311] CALL     A=2 B=2 C=2 D=514 
00038 [L311] MOV      A=1 B=0 C=2 D=2 
00039 [L312] JMP      A=2 B=128 C=21 D=32789 target=61
00040 [L313] TGETS    A=2 B=0 C=9 D=9 'csvInfo'
00041 [L313] TGETS    A=2 B=2 C=10 D=522 'mainType'
00042 [L313] UGET     A=3 B=0 C=0 D=0 m_t
00043 [L313] TGETS    A=3 B=3 C=11 D=779 'stone'
00044 [L313] ISNEV    A=2 B=0 C=3 D=3 
00045 [L313] JMP      A=2 B=128 C=15 D=32783 target=61
00046 [L313] TGETS    A=2 B=0 C=12 D=12 'owner_id'
00047 [L313] ISF      A=0 B=0 C=2 D=2 
00048 [L313] JMP      A=3 B=128 C=12 D=32780 target=61
00049 [L313] TGETS    A=2 B=0 C=12 D=12 'owner_id'
00050 [L313] KSHORT   A=3 B=0 C=0 D=0 0
00051 [L313] ISGE     A=3 B=0 C=2 D=2 
00052 [L313] JMP      A=2 B=128 C=8 D=32776 target=61
00053 [L314] GGET     A=2 B=0 C=1 D=1 'd_ms'
00054 [L314] TGETS    A=2 B=2 C=13 D=525 'd_stoneUI'
00055 [L314] TGETS    A=2 B=2 C=14 D=526 'getOwnerNameByID'
00056 [L314] TGETS    A=3 B=0 C=12 D=12 'owner_id'
00057 [L314] TGETS    A=4 B=0 C=9 D=9 'csvInfo'
00058 [L314] TGETS    A=4 B=4 C=15 D=1039 'sub_type'
00059 [L314] CALL     A=2 B=2 C=3 D=515 
00060 [L314] MOV      A=1 B=0 C=2 D=2 
00061 [L316] IST      A=0 B=0 C=1 D=1 
00062 [L316] JMP      A=2 B=128 C=24 D=32792 target=87
00063 [L316] TGETS    A=2 B=0 C=16 D=16 'level'
00064 [L316] ISF      A=0 B=0 C=2 D=2 
00065 [L316] JMP      A=3 B=128 C=21 D=32789 target=87
00066 [L316] TGETS    A=2 B=0 C=16 D=16 'level'
00067 [L316] KSHORT   A=3 B=0 C=2 D=2 2
00068 [L316] ISGT     A=3 B=0 C=2 D=2 
00069 [L316] JMP      A=2 B=128 C=17 D=32785 target=87
00070 [L316] TGETS    A=2 B=0 C=9 D=9 'csvInfo'
00071 [L316] ISF      A=0 B=0 C=2 D=2 
00072 [L316] JMP      A=3 B=128 C=14 D=32782 target=87
00073 [L316] TGETS    A=2 B=0 C=9 D=9 'csvInfo'
00074 [L316] TGETS    A=2 B=2 C=17 D=529 'quality'
00075 [L316] KSHORT   A=3 B=0 C=5 D=5 5
00076 [L316] ISGT     A=3 B=0 C=2 D=2 
00077 [L316] JMP      A=2 B=128 C=9 D=32777 target=87
00078 [L316] TGETS    A=2 B=0 C=9 D=9 'csvInfo'
00079 [L316] TGETS    A=2 B=2 C=18 D=530 'skillType'
00080 [L316] ISEQN    A=2 B=0 C=1 D=1 1
00081 [L316] JMP      A=2 B=128 C=5 D=32773 target=87
00082 [L316] TGETS    A=2 B=0 C=19 D=19 'protogenic'
00083 [L316] ISEQN    A=2 B=0 C=1 D=1 1
00084 [L316] JMP      A=2 B=128 C=2 D=32770 target=87
00085 [L317] KPRI     A=2 B=0 C=2 D=2 
00086 [L317] RET1     A=2 B=0 C=2 D=2 
00087 [L319] KPRI     A=2 B=0 C=1 D=1 
00088 [L319] RET1     A=2 B=0 C=2 D=2 

FUNCTION proto8 offset=0x1075 source_lines=334-336 params=0
UPVALUES ['itemInfo']
00001 [L335] GGET     A=0 B=0 C=0 D=0 'requestUseItem'
00002 [L335] UGET     A=1 B=0 C=0 D=0 itemInfo
00003 [L335] CALL     A=0 B=1 C=2 D=258 
00004 [L336] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto9 offset=0x10b1 source_lines=339-346 params=1
UPVALUES ['transInfo', 'string']
00001 [L340] GGET     A=1 B=0 C=0 D=0 'd_ms'
00002 [L340] TGETS    A=1 B=1 C=1 D=257 'd_mainUI'
00003 [L340] TGETS    A=1 B=1 C=2 D=258 'g_playerInfo'
00004 [L340] TGETS    A=1 B=1 C=3 D=259 'level'
00005 [L340] UGET     A=2 B=0 C=0 D=0 transInfo
00006 [L340] TGETV    A=2 B=2 C=0 D=512 
00007 [L340] TGETS    A=2 B=2 C=4 D=516 'min_role_level'
00008 [L340] ISGE     A=1 B=0 C=2 D=2 
00009 [L340] JMP      A=1 B=128 C=17 D=32785 target=27
00010 [L341] GGET     A=1 B=0 C=0 D=0 'd_ms'
00011 [L341] TGETS    A=1 B=1 C=5 D=261 'd_info'
00012 [L341] TGETS    A=1 B=1 C=6 D=262 'show'
00013 [L341] UGET     A=2 B=0 C=1 D=1 string
00014 [L341] TGETS    A=2 B=2 C=7 D=519 'format'
00015 [L341] GGET     A=3 B=0 C=0 D=0 'd_ms'
00016 [L341] TGETS    A=3 B=3 C=8 D=776 'd_hz'
00017 [L341] TGETS    A=3 B=3 C=9 D=777 'gethz'
00018 [L341] KSTR     A=4 B=0 C=10 D=10 'stone_lv_limit'
00019 [L341] CALL     A=3 B=2 C=2 D=514 
00020 [L341] UGET     A=4 B=0 C=0 D=0 transInfo
00021 [L341] TGETV    A=4 B=4 C=0 D=1024 
00022 [L341] TGETS    A=4 B=4 C=4 D=1028 'min_role_level'
00023 [L341] CALL     A=2 B=2 C=3 D=515 
00024 [L341] KSHORT   A=3 B=0 C=2 D=2 2
00025 [L341] CALL     A=1 B=1 C=3 D=259 
00026 [L341] JMP      A=1 B=128 C=6 D=32774 target=33
00027 [L344] GGET     A=1 B=0 C=0 D=0 'd_ms'
00028 [L344] TGETS    A=1 B=1 C=11 D=267 'd_smithUI'
00029 [L344] TGETS    A=1 B=1 C=6 D=262 'show'
00030 [L344] UGET     A=2 B=0 C=0 D=0 transInfo
00031 [L344] TGETV    A=2 B=2 C=0 D=512 
00032 [L344] CALL     A=1 B=1 C=2 D=258 
00033 [L346] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto10 offset=0x11e6 source_lines=369-376 params=0
UPVALUES ['itemInfo', 'math']
00001 [L370] UGET     A=0 B=0 C=0 D=0 itemInfo
00002 [L370] TGETS    A=0 B=0 C=0 D=0 'count'
00003 [L370] KSHORT   A=1 B=0 C=10 D=10 10
00004 [L370] ISGT     A=1 B=0 C=0 D=0 
00005 [L370] JMP      A=0 B=128 C=22 D=32790 target=28
00006 [L371] TDUP     A=0 B=0 C=2 D=2 {'kind': 'table', 'value': {'min': 1}}
00007 [L371] UGET     A=1 B=0 C=1 D=1 math
00008 [L371] TGETS    A=1 B=1 C=1 D=257 'min'
00009 [L371] KSHORT   A=2 B=0 C=15 D=15 15
00010 [L371] UGET     A=3 B=0 C=0 D=0 itemInfo
00011 [L371] TGETS    A=3 B=3 C=0 D=768 'count'
00012 [L371] CALL     A=1 B=2 C=3 D=515 
00013 [L371] TSETS    A=1 B=0 C=3 D=3 'max'
00014 [L371] UGET     A=1 B=0 C=0 D=0 itemInfo
00015 [L371] TGETS    A=1 B=1 C=4 D=260 'type_id'
00016 [L371] TSETS    A=1 B=0 C=5 D=5 'itemType'
00017 [L372] GGET     A=1 B=0 C=6 D=6 'd_ms'
00018 [L372] TGETS    A=1 B=1 C=7 D=263 'd_treasureMapUI'
00019 [L372] TGETS    A=1 B=1 C=8 D=264 'createBatchUse'
00020 [L372] GGET     A=2 B=0 C=6 D=6 'd_ms'
00021 [L372] TGETS    A=2 B=2 C=9 D=521 'd_mainUI'
00022 [L372] TGETS    A=2 B=2 C=10 D=522 'g_mainUI'
00023 [L372] TGETS    A=2 B=2 C=11 D=523 'main_layer'
00024 [L372] MOV      A=3 B=0 C=0 D=0 
00025 [L372] GGET     A=4 B=0 C=12 D=12 'sendUseItemRequest'
00026 [L372] CALL     A=1 B=1 C=4 D=260 
00027 [L372] JMP      A=0 B=128 C=9 D=32777 target=37
00028 [L374] GGET     A=0 B=0 C=6 D=6 'd_ms'
00029 [L374] TGETS    A=0 B=0 C=13 D=13 'd_info'
00030 [L374] TGETS    A=0 B=0 C=14 D=14 'show'
00031 [L374] GGET     A=1 B=0 C=6 D=6 'd_ms'
00032 [L374] TGETS    A=1 B=1 C=15 D=271 'd_hz'
00033 [L374] TGETS    A=1 B=1 C=16 D=272 'gethz'
00034 [L374] KSTR     A=2 B=0 C=17 D=17 'treasureMap_info5'
00035 [L374] CALL     A=1 B=0 C=2 D=2 
00036 [L374] CALLM    A=0 B=1 C=0 D=256 
00037 [L376] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto11 offset=0x136b source_lines=383-385 params=0
UPVALUES ['itemInfo']
00001 [L384] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L384] TGETS    A=0 B=0 C=1 D=1 'd_data'
00003 [L384] TGETS    A=0 B=0 C=2 D=2 'createBatchSale'
00004 [L384] GGET     A=1 B=0 C=0 D=0 'd_ms'
00005 [L384] TGETS    A=1 B=1 C=3 D=259 'd_mainUI'
00006 [L384] TGETS    A=1 B=1 C=4 D=260 'g_mainUI'
00007 [L384] TGETS    A=1 B=1 C=5 D=261 'main_layer'
00008 [L384] UGET     A=2 B=0 C=0 D=0 itemInfo
00009 [L384] TGETS    A=2 B=2 C=6 D=518 'type_id'
00010 [L384] UGET     A=3 B=0 C=0 D=0 itemInfo
00011 [L384] TGETS    A=3 B=3 C=7 D=775 'count'
00012 [L384] CALL     A=0 B=1 C=4 D=260 
00013 [L385] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto12 offset=0x140c source_lines=398-404 params=0
UPVALUES ['itemInfo']
00001 [L400] TNEW     A=0 B=0 C=0 D=0 
00002 [L401] UGET     A=1 B=0 C=0 D=0 itemInfo
00003 [L401] TSETS    A=1 B=0 C=0 D=0 'skill_info'
00004 [L402] KSHORT   A=1 B=0 C=1 D=1 1
00005 [L402] TSETS    A=1 B=0 C=1 D=1 'from_btn'
00006 [L403] GGET     A=1 B=0 C=2 D=2 'd_ms'
00007 [L403] TGETS    A=1 B=1 C=3 D=259 'd_skillUpgradeUI'
00008 [L403] TGETS    A=1 B=1 C=4 D=260 'show'
00009 [L403] MOV      A=2 B=0 C=0 D=0 
00010 [L403] KSHORT   A=3 B=0 C=1 D=1 1
00011 [L403] CALL     A=1 B=1 C=3 D=259 
00012 [L404] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto13 offset=0x1498 source_lines=405-408 params=0
UPVALUES ['itemInfo']
00001 [L406] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L406] TGETS    A=0 B=0 C=1 D=1 'd_smithUI'
00003 [L406] TGETS    A=0 B=0 C=2 D=2 'showFenjie'
00004 [L406] UGET     A=1 B=0 C=0 D=0 itemInfo
00005 [L406] CALL     A=0 B=1 C=2 D=258 
00006 [L408] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto14 offset=0x14e9 source_lines=425-430 params=0
UPVALUES ['itemInfo']
00001 [L427] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L427] TGETS    A=0 B=0 C=1 D=1 'd_stoneUpgradeUI'
00003 [L427] TGETS    A=0 B=0 C=2 D=2 'canUpgrade'
00004 [L427] UGET     A=1 B=0 C=0 D=0 itemInfo
00005 [L427] KPRI     A=2 B=0 C=2 D=2 
00006 [L427] CALL     A=0 B=2 C=3 D=515 
00007 [L427] ISF      A=0 B=0 C=0 D=0 
00008 [L427] JMP      A=1 B=128 C=10 D=32778 target=19
00009 [L428] GGET     A=0 B=0 C=0 D=0 'd_ms'
00010 [L428] TGETS    A=0 B=0 C=1 D=1 'd_stoneUpgradeUI'
00011 [L428] TGETS    A=0 B=0 C=3 D=3 'show'
00012 [L428] GGET     A=1 B=0 C=0 D=0 'd_ms'
00013 [L428] TGETS    A=1 B=1 C=4 D=260 'd_mainUI'
00014 [L428] TGETS    A=1 B=1 C=5 D=261 'g_mainUI'
00015 [L428] TGETS    A=1 B=1 C=6 D=262 'main_layer'
00016 [L428] KSHORT   A=2 B=0 C=40 D=40 40
00017 [L428] UGET     A=3 B=0 C=0 D=0 itemInfo
00018 [L428] CALL     A=0 B=1 C=4 D=260 
00019 [L430] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto15 offset=0x15a4 source_lines=432-434 params=0
UPVALUES ['itemInfo']
00001 [L433] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L433] TGETS    A=0 B=0 C=1 D=1 'd_stoneCastUI'
00003 [L433] TGETS    A=0 B=0 C=2 D=2 'pressCast'
00004 [L433] GGET     A=1 B=0 C=0 D=0 'd_ms'
00005 [L433] TGETS    A=1 B=1 C=3 D=259 'd_mainUI'
00006 [L433] TGETS    A=1 B=1 C=4 D=260 'g_mainUI'
00007 [L433] TGETS    A=1 B=1 C=5 D=261 'main_layer'
00008 [L433] UGET     A=2 B=0 C=0 D=0 itemInfo
00009 [L433] CALL     A=0 B=1 C=3 D=259 
00010 [L434] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto16 offset=0x1629 source_lines=473-482 params=0
UPVALUES ['itemInfo']
00001 [L474] UGET     A=0 B=0 C=0 D=0 itemInfo
00002 [L477] GGET     A=1 B=0 C=0 D=0 'd_ms'
00003 [L477] TGETS    A=1 B=1 C=1 D=257 'd_equipmentUpgradeUI'
00004 [L477] TGETS    A=1 B=1 C=2 D=258 'checkEquipmentCanUpgrade'
00005 [L477] KPRI     A=2 B=0 C=2 D=2 
00006 [L477] UGET     A=3 B=0 C=0 D=0 itemInfo
00007 [L477] TGETS    A=3 B=3 C=3 D=771 'level'
00008 [L477] UGET     A=4 B=0 C=0 D=0 itemInfo
00009 [L477] TGETS    A=4 B=4 C=4 D=1028 'csvInfo'
00010 [L477] TGETS    A=4 B=4 C=5 D=1029 'quality'
00011 [L477] UGET     A=5 B=0 C=0 D=0 itemInfo
00012 [L477] TGETS    A=5 B=5 C=6 D=1286 'reborn_bit'
00013 [L477] CALL     A=1 B=2 C=5 D=517 
00014 [L477] ISNEN    A=1 B=0 C=0 D=0 2
00015 [L477] JMP      A=1 B=128 C=1 D=32769 target=17
00016 [L478] RET0     A=0 B=0 C=1 D=1 
00017 [L481] GGET     A=1 B=0 C=0 D=0 'd_ms'
00018 [L481] TGETS    A=1 B=1 C=1 D=257 'd_equipmentUpgradeUI'
00019 [L481] TGETS    A=1 B=1 C=7 D=263 'showEnhanceLayer'
00020 [L481] GGET     A=2 B=0 C=0 D=0 'd_ms'
00021 [L481] TGETS    A=2 B=2 C=8 D=520 'd_mainUI'
00022 [L481] TGETS    A=2 B=2 C=9 D=521 'g_mainUI'
00023 [L481] TGETS    A=2 B=2 C=10 D=522 'main_layer'
00024 [L481] MOV      A=3 B=0 C=0 D=0 
00025 [L481] KSHORT   A=4 B=0 C=40 D=40 40
00026 [L481] CALL     A=1 B=1 C=4 D=260 
00027 [L482] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto17 offset=0x1756 source_lines=484-488 params=0
UPVALUES ['itemInfo']
00001 [L485] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L485] TGETS    A=0 B=0 C=1 D=1 'd_stoneUI'
00003 [L485] TGETS    A=0 B=0 C=2 D=2 'canJoin'
00004 [L485] KPRI     A=1 B=0 C=2 D=2 
00005 [L485] CALL     A=0 B=2 C=2 D=514 
00006 [L485] ISF      A=0 B=0 C=0 D=0 
00007 [L485] JMP      A=1 B=128 C=8 D=32776 target=16
00008 [L486] GGET     A=0 B=0 C=0 D=0 'd_ms'
00009 [L486] TGETS    A=0 B=0 C=1 D=1 'd_stoneUI'
00010 [L486] TGETS    A=0 B=0 C=3 D=3 'showStoneLayer'
00011 [L486] GGET     A=1 B=0 C=4 D=4 'g_packageUI'
00012 [L486] TGETS    A=1 B=1 C=5 D=261 'parent'
00013 [L486] KSHORT   A=2 B=0 C=40 D=40 40
00014 [L486] UGET     A=3 B=0 C=0 D=0 itemInfo
00015 [L486] CALL     A=0 B=1 C=4 D=260 
00016 [L488] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto18 offset=0x17f7 source_lines=523-525 params=0
UPVALUES ['menu']
00001 [L524] UGET     A=0 B=0 C=0 D=0 menu
00002 [L524] MOV      A=1 B=0 C=0 D=0 
00003 [L524] TGETS    A=0 B=0 C=0 D=0 'setHandlerPriority'
00004 [L524] KSHORT   A=2 B=255 C=130 D=65410 -126
00005 [L524] CALL     A=0 B=1 C=3 D=259 
00006 [L525] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto19 offset=0x183d source_lines=322-528 params=5
UPVALUES ['CCArray', 'string', 'table', 'ccp', 'hasBtn', 'CCSprite', 'math', 'tolua', 'CCMenu']
00001 [L323] GGET     A=5 B=0 C=0 D=0 'd_ms'
00002 [L323] TGETS    A=5 B=5 C=1 D=1281 'd_createCell'
00003 [L323] TGETS    A=5 B=5 C=2 D=1282 'createCellWithOwner'
00004 [L323] MOV      A=6 B=0 C=0 D=0 
00005 [L323] MOV      A=7 B=0 C=2 D=2 
00006 [L323] MOV      A=8 B=0 C=3 D=3 
00007 [L323] MOV      A=9 B=0 C=4 D=4 
00008 [L323] CALL     A=5 B=1 C=5 D=261 
00009 [L326] UGET     A=5 B=0 C=0 D=0 CCArray
00010 [L326] MOV      A=6 B=0 C=5 D=5 
00011 [L326] TGETS    A=5 B=5 C=3 D=1283 'create'
00012 [L326] CALL     A=5 B=2 C=2 D=514 
00013 [L327] TNEW     A=6 B=0 C=0 D=0 
00014 [L330] KSHORT   A=7 B=255 C=130 D=65410 -126
00015 [L330] TSETS    A=7 B=6 C=4 D=1540 'priority'
00016 [L331] KPRI     A=7 B=0 C=2 D=2 
00017 [L331] TSETS    A=7 B=6 C=5 D=1541 'usedDefaultRect'
00018 [L333] GGET     A=7 B=0 C=6 D=6 'packageTagDef'
00019 [L333] TGETS    A=7 B=7 C=7 D=1799 'props'
00020 [L333] ISNEV    A=1 B=0 C=7 D=7 
00021 [L333] JMP      A=7 B=128 C=169 D=32937 target=191
00022 [L336] FNEW     A=7 B=0 C=8 D=8 {'kind': 'proto', 'id': 8}
00023 [L337] GGET     A=8 B=0 C=0 D=0 'd_ms'
00024 [L337] TGETS    A=8 B=8 C=9 D=2057 'd_data'
00025 [L337] TGETS    A=8 B=8 C=10 D=2058 'getTransInfoByTypeid'
00026 [L337] TGETS    A=9 B=2 C=11 D=523 'type_id'
00027 [L337] KPRI     A=10 B=0 C=2 D=2 
00028 [L337] CALL     A=8 B=2 C=3 D=515 
00029 [L338] ISF      A=0 B=0 C=8 D=8 
00030 [L338] JMP      A=9 B=128 C=63 D=32831 target=94
00031 [L346] FNEW     A=9 B=0 C=12 D=12 {'kind': 'proto', 'id': 9}
00032 [L347] TNEW     A=10 B=0 C=0 D=0 
00033 [L347] TSETS    A=10 B=6 C=13 D=1549 'menuItems'
00034 [L348] TGETS    A=10 B=4 C=14 D=1038 'width'
00035 [L348] MULVN    A=10 B=10 C=0 D=2560 
00036 [L349] TGETB    A=11 B=8 C=2 D=2050 
00037 [L349] ISF      A=0 B=0 C=11 D=11 
00038 [L349] JMP      A=12 B=128 C=27 D=32795 target=66
00039 [L350] UGET     A=11 B=0 C=2 D=2 table
00040 [L350] TGETS    A=11 B=11 C=15 D=2831 'insert'
00041 [L350] TGETS    A=12 B=6 C=13 D=1549 'menuItems'
00042 [L350] TDUP     A=13 B=0 C=16 D=16 {'kind': 'table', 'value': {'spic': 'v2/transformUI/btn12.png', 'tag': 2, 'npic': 'v2/transformUI/btn11.png'}}
00043 [L350] GGET     A=14 B=0 C=0 D=0 'd_ms'
00044 [L350] TGETS    A=14 B=14 C=17 D=3601 'd_mainUI'
00045 [L350] TGETS    A=14 B=14 C=18 D=3602 'g_playerInfo'
00046 [L350] TGETS    A=14 B=14 C=19 D=3603 'level'
00047 [L350] TGETB    A=15 B=8 C=2 D=2050 
00048 [L350] TGETS    A=15 B=15 C=20 D=3860 'min_role_level'
00049 [L350] ISLT     A=14 B=0 C=15 D=15 
00050 [L350] JMP      A=14 B=128 C=2 D=32770 target=53
00051 [L350] KPRI     A=14 B=0 C=1 D=1 
00052 [L350] JMP      A=15 B=128 C=1 D=32769 target=54
00053 [L350] KPRI     A=14 B=0 C=2 D=2 
00054 [L350] TSETS    A=14 B=13 C=21 D=3349 'isGray'
00055 [L351] TSETS    A=9 B=13 C=22 D=3350 'tapHandler'
00056 [L351] UGET     A=14 B=0 C=3 D=3 ccp
00057 [L351] MOV      A=15 B=0 C=10 D=10 
00058 [L351] TGETS    A=16 B=4 C=23 D=1047 'height'
00059 [L351] MULVN    A=16 B=16 C=1 D=4097 
00060 [L351] CALL     A=14 B=2 C=3 D=515 
00061 [L351] TSETS    A=14 B=13 C=24 D=3352 'pos'
00062 [L350] CALL     A=11 B=1 C=3 D=259 
00063 [L352] TGETS    A=11 B=4 C=14 D=1038 'width'
00064 [L352] MULVN    A=11 B=11 C=2 D=2818 
00065 [L352] SUBVV    A=10 B=10 C=11 D=2571 
00066 [L354] TGETB    A=11 B=8 C=1 D=2049 
00067 [L354] ISF      A=0 B=0 C=11 D=11 
00068 [L354] JMP      A=12 B=128 C=85 D=32853 target=154
00069 [L355] UGET     A=11 B=0 C=2 D=2 table
00070 [L355] TGETS    A=11 B=11 C=15 D=2831 'insert'
00071 [L355] TGETS    A=12 B=6 C=13 D=1549 'menuItems'
00072 [L355] TDUP     A=13 B=0 C=25 D=25 {'kind': 'table', 'value': {'spic': 'v2/transformUI/btn02.png', 'tag': 1, 'npic': 'v2/transformUI/btn01.png'}}
00073 [L355] GGET     A=14 B=0 C=0 D=0 'd_ms'
00074 [L355] TGETS    A=14 B=14 C=17 D=3601 'd_mainUI'
00075 [L355] TGETS    A=14 B=14 C=18 D=3602 'g_playerInfo'
00076 [L355] TGETS    A=14 B=14 C=19 D=3603 'level'
00077 [L355] TGETB    A=15 B=8 C=1 D=2049 
00078 [L355] TGETS    A=15 B=15 C=20 D=3860 'min_role_level'
00079 [L355] ISLT     A=14 B=0 C=15 D=15 
00080 [L355] JMP      A=14 B=128 C=2 D=32770 target=83
00081 [L355] KPRI     A=14 B=0 C=1 D=1 
00082 [L355] JMP      A=15 B=128 C=1 D=32769 target=84
00083 [L355] KPRI     A=14 B=0 C=2 D=2 
00084 [L355] TSETS    A=14 B=13 C=21 D=3349 'isGray'
00085 [L356] TSETS    A=9 B=13 C=22 D=3350 'tapHandler'
00086 [L356] UGET     A=14 B=0 C=3 D=3 ccp
00087 [L356] MOV      A=15 B=0 C=10 D=10 
00088 [L356] TGETS    A=16 B=4 C=23 D=1047 'height'
00089 [L356] MULVN    A=16 B=16 C=1 D=4097 
00090 [L356] CALL     A=14 B=2 C=3 D=515 
00091 [L356] TSETS    A=14 B=13 C=24 D=3352 'pos'
00092 [L355] CALL     A=11 B=1 C=3 D=259 
00093 [L357] JMP      A=9 B=128 C=60 D=32828 target=154
00094 [L358] UGET     A=9 B=0 C=4 D=4 hasBtn
00095 [L358] TGETS    A=10 B=2 C=11 D=523 'type_id'
00096 [L358] CALL     A=9 B=2 C=2 D=514 
00097 [L358] ISF      A=0 B=0 C=9 D=9 
00098 [L358] JMP      A=10 B=128 C=55 D=32823 target=154
00099 [L359] TNEW     A=9 B=8 C=0 D=2048 
00100 [L359] TDUP     A=10 B=0 C=26 D=26 {'kind': 'table', 'value': {'npic': 'v2/packageUI/use1.png', 'spic': 'v2/packageUI/use2.png'}}
00101 [L359] TSETS    A=7 B=10 C=22 D=2582 'tapHandler'
00102 [L360] UGET     A=11 B=0 C=3 D=3 ccp
00103 [L360] TGETS    A=12 B=4 C=14 D=1038 'width'
00104 [L360] MULVN    A=12 B=12 C=0 D=3072 
00105 [L360] TGETS    A=13 B=4 C=23 D=1047 'height'
00106 [L360] MULVN    A=13 B=13 C=1 D=3329 
00107 [L360] CALL     A=11 B=2 C=3 D=515 
00108 [L360] TSETS    A=11 B=10 C=24 D=2584 'pos'
00109 [L360] TSETB    A=10 B=9 C=1 D=2305 
00110 [L360] TSETS    A=9 B=6 C=13 D=1549 'menuItems'
00111 [L361] GGET     A=9 B=0 C=0 D=0 'd_ms'
00112 [L361] TGETS    A=9 B=9 C=27 D=2331 'd_treasureMapUI'
00113 [L361] TGETS    A=9 B=9 C=28 D=2332 'isJiuYouBaoTu'
00114 [L361] TGETS    A=10 B=2 C=11 D=523 'type_id'
00115 [L361] CALL     A=9 B=2 C=2 D=514 
00116 [L361] ISF      A=0 B=0 C=9 D=9 
00117 [L361] JMP      A=10 B=128 C=36 D=32804 target=154
00118 [L362] UGET     A=9 B=0 C=5 D=5 CCSprite
00119 [L362] MOV      A=10 B=0 C=9 D=9 
00120 [L362] TGETS    A=9 B=9 C=3 D=2307 'create'
00121 [L362] KSTR     A=11 B=0 C=29 D=29 'v2/packageUI/piliangshiyong1.png'
00122 [L362] CALL     A=9 B=2 C=3 D=515 
00123 [L363] UGET     A=10 B=0 C=5 D=5 CCSprite
00124 [L363] MOV      A=11 B=0 C=10 D=10 
00125 [L363] TGETS    A=10 B=10 C=3 D=2563 'create'
00126 [L363] KSTR     A=12 B=0 C=30 D=30 'v2/packageUI/piliangshiyong2.png'
00127 [L363] CALL     A=10 B=2 C=3 D=515 
00128 [L364] TGETS    A=11 B=2 C=31 D=543 'count'
00129 [L364] KSHORT   A=12 B=0 C=10 D=10 10
00130 [L364] ISGE     A=11 B=0 C=12 D=12 
00131 [L364] JMP      A=11 B=128 C=8 D=32776 target=140
00132 [L365] MOV      A=12 B=0 C=9 D=9 
00133 [L365] TGETS    A=11 B=9 C=32 D=2336 'setMaskEff'
00134 [L365] KSTR     A=13 B=0 C=33 D=33 'v2/gray.shader'
00135 [L365] CALL     A=11 B=1 C=3 D=259 
00136 [L366] MOV      A=12 B=0 C=10 D=10 
00137 [L366] TGETS    A=11 B=10 C=32 D=2592 'setMaskEff'
00138 [L366] KSTR     A=13 B=0 C=33 D=33 'v2/gray.shader'
00139 [L366] CALL     A=11 B=1 C=3 D=259 
00140 [L376] FNEW     A=11 B=0 C=34 D=34 {'kind': 'proto', 'id': 10}
00141 [L377] TGETS    A=12 B=6 C=13 D=1549 'menuItems'
00142 [L377] TDUP     A=13 B=0 C=35 D=35 {'kind': 'table', 'value': {}}
00143 [L377] TSETS    A=9 B=13 C=36 D=3364 'nSprite'
00144 [L377] TSETS    A=10 B=13 C=37 D=3365 'sSprite'
00145 [L377] TSETS    A=11 B=13 C=22 D=3350 'tapHandler'
00146 [L377] UGET     A=14 B=0 C=3 D=3 ccp
00147 [L377] TGETS    A=15 B=4 C=14 D=1038 'width'
00148 [L377] MULVN    A=15 B=15 C=3 D=3843 
00149 [L377] TGETS    A=16 B=4 C=23 D=1047 'height'
00150 [L377] MULVN    A=16 B=16 C=1 D=4097 
00151 [L377] CALL     A=14 B=2 C=3 D=515 
00152 [L377] TSETS    A=14 B=13 C=24 D=3352 'pos'
00153 [L377] TSETB    A=13 B=12 C=2 D=3074 
00154 [L382] GGET     A=9 B=0 C=0 D=0 'd_ms'
00155 [L382] TGETS    A=9 B=9 C=9 D=2313 'd_data'
00156 [L382] TGETS    A=9 B=9 C=38 D=2342 'g_ep_price'
00157 [L382] TGETS    A=10 B=2 C=11 D=523 'type_id'
00158 [L382] TGETV    A=9 B=9 C=10 D=2314 
00159 [L382] ISF      A=0 B=0 C=9 D=9 
00160 [L382] JMP      A=10 B=128 C=29 D=32797 target=190
00161 [L385] FNEW     A=9 B=0 C=39 D=39 {'kind': 'proto', 'id': 11}
00162 [L386] TDUP     A=10 B=0 C=40 D=40 {'kind': 'table', 'value': {'npic': 'v2/batchBuyUI/sale1.png', 'spic': 'v2/batchBuyUI/sale2.png'}}
00163 [L386] TSETS    A=9 B=10 C=22 D=2582 'tapHandler'
00164 [L387] TGETS    A=11 B=6 C=13 D=1549 'menuItems'
00165 [L387] ISF      A=0 B=0 C=11 D=11 
00166 [L387] JMP      A=12 B=128 C=13 D=32781 target=180
00167 [L388] UGET     A=11 B=0 C=3 D=3 ccp
00168 [L388] TGETS    A=12 B=4 C=14 D=1038 'width'
00169 [L388] MULVN    A=12 B=12 C=4 D=3076 
00170 [L388] TGETS    A=13 B=4 C=23 D=1047 'height'
00171 [L388] MULVN    A=13 B=13 C=1 D=3329 
00172 [L388] CALL     A=11 B=2 C=3 D=515 
00173 [L388] TSETS    A=11 B=10 C=24 D=2584 'pos'
00174 [L389] UGET     A=11 B=0 C=2 D=2 table
00175 [L389] TGETS    A=11 B=11 C=15 D=2831 'insert'
00176 [L389] TGETS    A=12 B=6 C=13 D=1549 'menuItems'
00177 [L389] MOV      A=13 B=0 C=10 D=10 
00178 [L389] CALL     A=11 B=1 C=3 D=259 
00179 [L389] JMP      A=11 B=128 C=10 D=32778 target=190
00180 [L391] UGET     A=11 B=0 C=3 D=3 ccp
00181 [L391] TGETS    A=12 B=4 C=14 D=1038 'width'
00182 [L391] MULVN    A=12 B=12 C=0 D=3072 
00183 [L391] TGETS    A=13 B=4 C=23 D=1047 'height'
00184 [L391] MULVN    A=13 B=13 C=1 D=3329 
00185 [L391] CALL     A=11 B=2 C=3 D=515 
00186 [L391] TSETS    A=11 B=10 C=24 D=2584 'pos'
00187 [L392] TNEW     A=11 B=8 C=0 D=2048 
00188 [L392] TSETB    A=10 B=11 C=1 D=2817 
00189 [L392] TSETS    A=11 B=6 C=13 D=1549 'menuItems'
00190 [L394] UCLO     A=7 B=128 C=229 D=32997 target=420
00191 [L395] GGET     A=7 B=0 C=6 D=6 'packageTagDef'
00192 [L395] TGETS    A=7 B=7 C=41 D=1833 'skill'
00193 [L395] ISNEV    A=1 B=0 C=7 D=7 
00194 [L395] JMP      A=7 B=128 C=48 D=32816 target=243
00195 [L404] FNEW     A=7 B=0 C=42 D=42 {'kind': 'proto', 'id': 12}
00196 [L398] GSET     A=7 B=0 C=43 D=43 'pressSkillUpgrade'
00197 [L408] FNEW     A=7 B=0 C=44 D=44 {'kind': 'proto', 'id': 13}
00198 [L405] GSET     A=7 B=0 C=45 D=45 'pressFenjie'
00199 [L411] GGET     A=7 B=0 C=46 D=46 'checkEquipmentCanFenjie'
00200 [L411] MOV      A=8 B=0 C=2 D=2 
00201 [L411] CALL     A=7 B=2 C=2 D=514 
00202 [L412] ISF      A=0 B=0 C=7 D=7 
00203 [L412] JMP      A=8 B=128 C=25 D=32793 target=229
00204 [L413] TNEW     A=8 B=8 C=0 D=2048 
00205 [L413] TDUP     A=9 B=0 C=47 D=47 {'kind': 'table', 'value': {'npic': 'v2/enhanceUI/up1.png', 'spic': 'v2/enhanceUI/up2.png'}}
00206 [L413] GGET     A=10 B=0 C=43 D=43 'pressSkillUpgrade'
00207 [L413] TSETS    A=10 B=9 C=22 D=2326 'tapHandler'
00208 [L414] UGET     A=10 B=0 C=3 D=3 ccp
00209 [L414] TGETS    A=11 B=4 C=14 D=1038 'width'
00210 [L414] MULVN    A=11 B=11 C=0 D=2816 
00211 [L414] TGETS    A=12 B=4 C=23 D=1047 'height'
00212 [L414] MULVN    A=12 B=12 C=5 D=3077 
00213 [L414] CALL     A=10 B=2 C=3 D=515 
00214 [L414] TSETS    A=10 B=9 C=24 D=2328 'pos'
00215 [L414] TSETB    A=9 B=8 C=1 D=2049 
00216 [L415] TDUP     A=9 B=0 C=48 D=48 {'kind': 'table', 'value': {'npic': 'v2/smithUI/btn_rollback1.png', 'spic': 'v2/smithUI/btn_rollback2.png'}}
00217 [L415] GGET     A=10 B=0 C=45 D=45 'pressFenjie'
00218 [L415] TSETS    A=10 B=9 C=22 D=2326 'tapHandler'
00219 [L416] UGET     A=10 B=0 C=3 D=3 ccp
00220 [L416] TGETS    A=11 B=4 C=14 D=1038 'width'
00221 [L416] MULVN    A=11 B=11 C=0 D=2816 
00222 [L416] TGETS    A=12 B=4 C=23 D=1047 'height'
00223 [L416] MULVN    A=12 B=12 C=6 D=3078 
00224 [L416] CALL     A=10 B=2 C=3 D=515 
00225 [L416] TSETS    A=10 B=9 C=24 D=2328 'pos'
00226 [L416] TSETB    A=9 B=8 C=2 D=2050 
00227 [L416] TSETS    A=8 B=6 C=13 D=1549 'menuItems'
00228 [L416] JMP      A=8 B=128 C=191 D=32959 target=420
00229 [L418] TNEW     A=8 B=8 C=0 D=2048 
00230 [L418] TDUP     A=9 B=0 C=49 D=49 {'kind': 'table', 'value': {'npic': 'v2/enhanceUI/up1.png', 'spic': 'v2/enhanceUI/up2.png'}}
00231 [L418] GGET     A=10 B=0 C=43 D=43 'pressSkillUpgrade'
00232 [L418] TSETS    A=10 B=9 C=22 D=2326 'tapHandler'
00233 [L419] UGET     A=10 B=0 C=3 D=3 ccp
00234 [L419] TGETS    A=11 B=4 C=14 D=1038 'width'
00235 [L419] MULVN    A=11 B=11 C=0 D=2816 
00236 [L419] TGETS    A=12 B=4 C=23 D=1047 'height'
00237 [L419] MULVN    A=12 B=12 C=5 D=3077 
00238 [L419] CALL     A=10 B=2 C=3 D=515 
00239 [L419] TSETS    A=10 B=9 C=24 D=2328 'pos'
00240 [L419] TSETB    A=9 B=8 C=1 D=2049 
00241 [L420] TSETS    A=8 B=6 C=13 D=1549 'menuItems'
00242 [L421] JMP      A=7 B=128 C=177 D=32945 target=420
00243 [L422] GGET     A=7 B=0 C=6 D=6 'packageTagDef'
00244 [L422] TGETS    A=7 B=7 C=50 D=1842 'stone'
00245 [L422] ISNEV    A=1 B=0 C=7 D=7 
00246 [L422] JMP      A=7 B=128 C=102 D=32870 target=349
00247 [L430] FNEW     A=7 B=0 C=51 D=51 {'kind': 'proto', 'id': 14}
00248 [L425] GSET     A=7 B=0 C=52 D=52 'pressStoneUpgrade'
00249 [L434] FNEW     A=7 B=0 C=53 D=53 {'kind': 'proto', 'id': 15}
00250 [L442] UGET     A=8 B=0 C=5 D=5 CCSprite
00251 [L442] MOV      A=9 B=0 C=8 D=8 
00252 [L442] TGETS    A=8 B=8 C=3 D=2051 'create'
00253 [L442] KSTR     A=10 B=0 C=54 D=54 'v2/enhanceUI/up1.png'
00254 [L442] CALL     A=8 B=2 C=3 D=515 
00255 [L443] UGET     A=9 B=0 C=5 D=5 CCSprite
00256 [L443] MOV      A=10 B=0 C=9 D=9 
00257 [L443] TGETS    A=9 B=9 C=3 D=2307 'create'
00258 [L443] KSTR     A=11 B=0 C=55 D=55 'v2/enhanceUI/up2.png'
00259 [L443] CALL     A=9 B=2 C=3 D=515 
00260 [L444] GGET     A=10 B=0 C=52 D=52 'pressStoneUpgrade'
00261 [L445] GGET     A=11 B=0 C=0 D=0 'd_ms'
00262 [L445] TGETS    A=11 B=11 C=56 D=2872 'd_stoneUpgradeUI'
00263 [L445] TGETS    A=11 B=11 C=57 D=2873 'canUpgrade'
00264 [L445] MOV      A=12 B=0 C=2 D=2 
00265 [L445] KPRI     A=13 B=0 C=1 D=1 
00266 [L445] CALL     A=11 B=2 C=3 D=515 
00267 [L445] IST      A=0 B=0 C=11 D=11 
00268 [L445] JMP      A=11 B=128 C=8 D=32776 target=277
00269 [L446] MOV      A=12 B=0 C=8 D=8 
00270 [L446] TGETS    A=11 B=8 C=32 D=2080 'setMaskEff'
00271 [L446] KSTR     A=13 B=0 C=33 D=33 'v2/gray.shader'
00272 [L446] CALL     A=11 B=1 C=3 D=259 
00273 [L447] MOV      A=12 B=0 C=9 D=9 
00274 [L447] TGETS    A=11 B=9 C=32 D=2336 'setMaskEff'
00275 [L447] KSTR     A=13 B=0 C=33 D=33 'v2/gray.shader'
00276 [L447] CALL     A=11 B=1 C=3 D=259 
00277 [L450] TGETS    A=11 B=2 C=19 D=531 'level'
00278 [L450] ISF      A=0 B=0 C=11 D=11 
00279 [L450] JMP      A=12 B=128 C=22 D=32790 target=302
00280 [L450] TGETS    A=11 B=2 C=19 D=531 'level'
00281 [L450] KSHORT   A=12 B=0 C=10 D=10 10
00282 [L450] ISGT     A=12 B=0 C=11 D=11 
00283 [L450] JMP      A=11 B=128 C=18 D=32786 target=302
00284 [L450] TGETS    A=11 B=2 C=19 D=531 'level'
00285 [L450] KSHORT   A=12 B=0 C=11 D=11 11
00286 [L450] ISGE     A=11 B=0 C=12 D=12 
00287 [L450] JMP      A=11 B=128 C=14 D=32782 target=302
00288 [L451] UGET     A=11 B=0 C=5 D=5 CCSprite
00289 [L451] MOV      A=12 B=0 C=11 D=11 
00290 [L451] TGETS    A=11 B=11 C=3 D=2819 'create'
00291 [L451] KSTR     A=13 B=0 C=58 D=58 'v2/stoneCastUI/s_asc1.png'
00292 [L451] CALL     A=11 B=2 C=3 D=515 
00293 [L451] MOV      A=8 B=0 C=11 D=11 
00294 [L452] UGET     A=11 B=0 C=5 D=5 CCSprite
00295 [L452] MOV      A=12 B=0 C=11 D=11 
00296 [L452] TGETS    A=11 B=11 C=3 D=2819 'create'
00297 [L452] KSTR     A=13 B=0 C=59 D=59 'v2/stoneCastUI/s_asc2.png'
00298 [L452] CALL     A=11 B=2 C=3 D=515 
00299 [L452] MOV      A=9 B=0 C=11 D=11 
00300 [L453] MOV      A=10 B=0 C=7 D=7 
00301 [L453] JMP      A=11 B=128 C=32 D=32800 target=334
00302 [L458] TGETS    A=11 B=2 C=19 D=531 'level'
00303 [L458] ISF      A=0 B=0 C=11 D=11 
00304 [L458] JMP      A=12 B=128 C=29 D=32797 target=334
00305 [L458] TGETS    A=11 B=2 C=19 D=531 'level'
00306 [L458] KSHORT   A=12 B=0 C=11 D=11 11
00307 [L458] ISGT     A=12 B=0 C=11 D=11 
00308 [L458] JMP      A=11 B=128 C=25 D=32793 target=334
00309 [L459] UGET     A=11 B=0 C=5 D=5 CCSprite
00310 [L459] MOV      A=12 B=0 C=11 D=11 
00311 [L459] TGETS    A=11 B=11 C=3 D=2819 'create'
00312 [L459] KSTR     A=13 B=0 C=60 D=60 'v2/stoneCastUI/lingshitilian1.png'
00313 [L459] CALL     A=11 B=2 C=3 D=515 
00314 [L459] MOV      A=8 B=0 C=11 D=11 
00315 [L460] UGET     A=11 B=0 C=5 D=5 CCSprite
00316 [L460] MOV      A=12 B=0 C=11 D=11 
00317 [L460] TGETS    A=11 B=11 C=3 D=2819 'create'
00318 [L460] KSTR     A=13 B=0 C=61 D=61 'v2/stoneCastUI/lingshitilian2.png'
00319 [L460] CALL     A=11 B=2 C=3 D=515 
00320 [L460] MOV      A=9 B=0 C=11 D=11 
00321 [L461] MOV      A=10 B=0 C=7 D=7 
00322 [L462] TGETS    A=11 B=2 C=19 D=531 'level'
00323 [L462] KSHORT   A=12 B=0 C=11 D=11 11
00324 [L462] ISGE     A=12 B=0 C=11 D=11 
00325 [L462] JMP      A=11 B=128 C=8 D=32776 target=334
00326 [L463] MOV      A=12 B=0 C=8 D=8 
00327 [L463] TGETS    A=11 B=8 C=32 D=2080 'setMaskEff'
00328 [L463] KSTR     A=13 B=0 C=33 D=33 'v2/gray.shader'
00329 [L463] CALL     A=11 B=1 C=3 D=259 
00330 [L464] MOV      A=12 B=0 C=9 D=9 
00331 [L464] TGETS    A=11 B=9 C=32 D=2336 'setMaskEff'
00332 [L464] KSTR     A=13 B=0 C=33 D=33 'v2/gray.shader'
00333 [L464] CALL     A=11 B=1 C=3 D=259 
00334 [L468] TNEW     A=11 B=8 C=0 D=2048 
00335 [L468] TDUP     A=12 B=0 C=62 D=62 {'kind': 'table', 'value': {}}
00336 [L468] TSETS    A=8 B=12 C=36 D=3108 'nSprite'
00337 [L468] TSETS    A=9 B=12 C=37 D=3109 'sSprite'
00338 [L468] TSETS    A=10 B=12 C=22 D=3094 'tapHandler'
00339 [L469] UGET     A=13 B=0 C=3 D=3 ccp
00340 [L469] TGETS    A=14 B=4 C=14 D=1038 'width'
00341 [L469] MULVN    A=14 B=14 C=0 D=3584 
00342 [L469] TGETS    A=15 B=4 C=23 D=1047 'height'
00343 [L469] MULVN    A=15 B=15 C=1 D=3841 
00344 [L469] CALL     A=13 B=2 C=3 D=515 
00345 [L469] TSETS    A=13 B=12 C=24 D=3096 'pos'
00346 [L469] TSETB    A=12 B=11 C=1 D=2817 
00347 [L469] TSETS    A=11 B=6 C=13 D=1549 'menuItems'
00348 [L469] JMP      A=7 B=128 C=71 D=32839 target=420
00349 [L482] FNEW     A=7 B=0 C=63 D=63 {'kind': 'proto', 'id': 16}
00350 [L473] GSET     A=7 B=0 C=64 D=64 'equipmentUpgrade'
00351 [L488] FNEW     A=7 B=0 C=65 D=65 {'kind': 'proto', 'id': 17}
00352 [L484] GSET     A=7 B=0 C=66 D=66 'equipSlot'
00353 [L490] UGET     A=7 B=0 C=5 D=5 CCSprite
00354 [L490] MOV      A=8 B=0 C=7 D=7 
00355 [L490] TGETS    A=7 B=7 C=3 D=1795 'create'
00356 [L490] KSTR     A=9 B=0 C=67 D=67 'v2/packageUI/enhance1.png'
00357 [L490] CALL     A=7 B=2 C=3 D=515 
00358 [L491] UGET     A=8 B=0 C=5 D=5 CCSprite
00359 [L491] MOV      A=9 B=0 C=8 D=8 
00360 [L491] TGETS    A=8 B=8 C=3 D=2051 'create'
00361 [L491] KSTR     A=10 B=0 C=68 D=68 'v2/packageUI/enhance2.png'
00362 [L491] CALL     A=8 B=2 C=3 D=515 
00363 [L492] GGET     A=9 B=0 C=0 D=0 'd_ms'
00364 [L492] TGETS    A=9 B=9 C=69 D=2373 'd_equipmentUpgradeUI'
00365 [L492] TGETS    A=9 B=9 C=70 D=2374 'checkEquipmentCanUpgrade'
00366 [L492] KPRI     A=10 B=0 C=1 D=1 
00367 [L492] TGETS    A=11 B=2 C=19 D=531 'level'
00368 [L492] TGETS    A=12 B=2 C=71 D=583 'csvInfo'
00369 [L492] TGETS    A=12 B=12 C=72 D=3144 'quality'
00370 [L492] TGETS    A=13 B=2 C=73 D=585 'reborn_bit'
00371 [L492] CALL     A=9 B=2 C=5 D=517 
00372 [L492] ISNEN    A=9 B=0 C=7 D=7 2
00373 [L492] JMP      A=9 B=128 C=8 D=32776 target=382
00374 [L493] MOV      A=10 B=0 C=7 D=7 
00375 [L493] TGETS    A=9 B=7 C=32 D=1824 'setMaskEff'
00376 [L493] KSTR     A=11 B=0 C=33 D=33 'v2/gray.shader'
00377 [L493] CALL     A=9 B=1 C=3 D=259 
00378 [L494] MOV      A=10 B=0 C=8 D=8 
00379 [L494] TGETS    A=9 B=8 C=32 D=2080 'setMaskEff'
00380 [L494] KSTR     A=11 B=0 C=33 D=33 'v2/gray.shader'
00381 [L494] CALL     A=9 B=1 C=3 D=259 
00382 [L497] UGET     A=9 B=0 C=5 D=5 CCSprite
00383 [L497] MOV      A=10 B=0 C=9 D=9 
00384 [L497] TGETS    A=9 B=9 C=3 D=2307 'create'
00385 [L497] KSTR     A=11 B=0 C=74 D=74 'v2/stoneUI/putin_btn1.png'
00386 [L497] CALL     A=9 B=2 C=3 D=515 
00387 [L498] UGET     A=10 B=0 C=5 D=5 CCSprite
00388 [L498] MOV      A=11 B=0 C=10 D=10 
00389 [L498] TGETS    A=10 B=10 C=3 D=2563 'create'
00390 [L498] KSTR     A=12 B=0 C=75 D=75 'v2/stoneUI/putin_btn2.png'
00391 [L498] CALL     A=10 B=2 C=3 D=515 
00392 [L500] TNEW     A=11 B=8 C=0 D=2048 
00393 [L500] TDUP     A=12 B=0 C=76 D=76 {'kind': 'table', 'value': {}}
00394 [L500] TSETS    A=7 B=12 C=36 D=3108 'nSprite'
00395 [L500] TSETS    A=8 B=12 C=37 D=3109 'sSprite'
00396 [L500] GGET     A=13 B=0 C=64 D=64 'equipmentUpgrade'
00397 [L500] TSETS    A=13 B=12 C=22 D=3094 'tapHandler'
00398 [L500] UGET     A=13 B=0 C=3 D=3 ccp
00399 [L500] TGETS    A=14 B=4 C=14 D=1038 'width'
00400 [L500] MULVN    A=14 B=14 C=0 D=3584 
00401 [L500] TGETS    A=15 B=4 C=23 D=1047 'height'
00402 [L500] MULVN    A=15 B=15 C=1 D=3841 
00403 [L500] CALL     A=13 B=2 C=3 D=515 
00404 [L500] TSETS    A=13 B=12 C=24 D=3096 'pos'
00405 [L500] TSETB    A=12 B=11 C=1 D=2817 
00406 [L501] TDUP     A=12 B=0 C=77 D=77 {'kind': 'table', 'value': {}}
00407 [L501] TSETS    A=9 B=12 C=36 D=3108 'nSprite'
00408 [L501] TSETS    A=10 B=12 C=37 D=3109 'sSprite'
00409 [L501] GGET     A=13 B=0 C=66 D=66 'equipSlot'
00410 [L501] TSETS    A=13 B=12 C=22 D=3094 'tapHandler'
00411 [L501] UGET     A=13 B=0 C=3 D=3 ccp
00412 [L501] TGETS    A=14 B=4 C=14 D=1038 'width'
00413 [L501] MULVN    A=14 B=14 C=8 D=3592 
00414 [L501] TGETS    A=15 B=4 C=23 D=1047 'height'
00415 [L501] MULVN    A=15 B=15 C=1 D=3841 
00416 [L501] CALL     A=13 B=2 C=3 D=515 
00417 [L501] TSETS    A=13 B=12 C=24 D=3096 'pos'
00418 [L501] TSETB    A=12 B=11 C=2 D=2818 
00419 [L501] TSETS    A=11 B=6 C=13 D=1549 'menuItems'
00420 [L504] TGETS    A=7 B=6 C=13 D=1549 'menuItems'
00421 [L504] ISF      A=0 B=0 C=7 D=7 
00422 [L504] JMP      A=8 B=128 C=9 D=32777 target=432
00423 [L505] GGET     A=7 B=0 C=0 D=0 'd_ms'
00424 [L505] TGETS    A=7 B=7 C=78 D=1870 'd_tableView'
00425 [L505] TGETS    A=7 B=7 C=79 D=1871 'createTableViewMenu'
00426 [L505] MOV      A=8 B=0 C=6 D=6 
00427 [L505] CALL     A=7 B=2 C=2 D=514 
00428 [L506] MOV      A=9 B=0 C=0 D=0 
00429 [L506] TGETS    A=8 B=0 C=80 D=80 'addChild'
00430 [L506] MOV      A=10 B=0 C=7 D=7 
00431 [L506] CALL     A=8 B=1 C=3 D=259 
00432 [L509] UCLO     A=0 B=128 C=0 D=32768 target=433
00433 [L509] RET0     A=0 B=0 C=1 D=1 
00434 [L511] MOV      A=8 B=0 C=5 D=5 
00435 [L511] TGETS    A=7 B=5 C=31 D=1311 'count'
00436 [L511] CALL     A=7 B=2 C=2 D=514 
00437 [L512] KSHORT   A=8 B=0 C=0 D=0 0
00438 [L512] ISGE     A=8 B=0 C=7 D=7 
00439 [L512] JMP      A=8 B=128 C=48 D=32816 target=488
00440 [L513] TGETS    A=8 B=4 C=14 D=1038 'width'
00441 [L513] MULNV    A=8 B=8 C=9 D=2057 
00442 [L514] KSHORT   A=9 B=0 C=1 D=1 1
00443 [L514] MOV      A=10 B=0 C=7 D=7 
00444 [L514] KSHORT   A=11 B=0 C=1 D=1 1
00445 [L514] FORI     A=9 B=128 C=19 D=32787 target=465
00446 [L515] UGET     A=13 B=0 C=7 D=7 tolua
00447 [L515] TGETS    A=13 B=13 C=81 D=3409 'cast'
00448 [L515] MOV      A=15 B=0 C=5 D=5 
00449 [L515] TGETS    A=14 B=5 C=82 D=1362 'objectAtIndex'
00450 [L515] SUBVN    A=16 B=12 C=10 D=3082 
00451 [L515] CALL     A=14 B=2 C=3 D=515 
00452 [L515] KSTR     A=15 B=0 C=83 D=83 'CCMenuItemImage'
00453 [L515] CALL     A=13 B=2 C=3 D=515 
00454 [L516] MOV      A=15 B=0 C=13 D=13 
00455 [L516] TGETS    A=14 B=13 C=84 D=3412 'setPosition'
00456 [L516] TGETS    A=16 B=4 C=14 D=1038 'width'
00457 [L516] MULVN    A=16 B=16 C=0 D=4096 
00458 [L516] SUBVN    A=17 B=12 C=10 D=3082 
00459 [L516] MULVV    A=17 B=8 C=17 D=2065 
00460 [L516] SUBVV    A=16 B=16 C=17 D=4113 
00461 [L516] TGETS    A=17 B=4 C=23 D=1047 'height'
00462 [L516] MULVN    A=17 B=17 C=1 D=4353 
00463 [L516] CALL     A=14 B=1 C=4 D=260 
00464 [L514] FORL     A=9 B=127 C=237 D=32749 target=446
00465 [L519] UGET     A=9 B=0 C=8 D=8 CCMenu
00466 [L519] MOV      A=10 B=0 C=9 D=9 
00467 [L519] TGETS    A=9 B=9 C=85 D=2389 'createWithArray'
00468 [L519] MOV      A=11 B=0 C=5 D=5 
00469 [L519] CALL     A=9 B=2 C=3 D=515 
00470 [L520] MOV      A=11 B=0 C=9 D=9 
00471 [L520] TGETS    A=10 B=9 C=84 D=2388 'setPosition'
00472 [L520] KSHORT   A=12 B=0 C=0 D=0 0
00473 [L520] KSHORT   A=13 B=0 C=0 D=0 0
00474 [L520] CALL     A=10 B=1 C=4 D=260 
00475 [L521] MOV      A=11 B=0 C=0 D=0 
00476 [L521] TGETS    A=10 B=0 C=80 D=80 'addChild'
00477 [L521] MOV      A=12 B=0 C=9 D=9 
00478 [L521] CALL     A=10 B=1 C=3 D=259 
00479 [L525] FNEW     A=10 B=0 C=86 D=86 {'kind': 'proto', 'id': 18}
00480 [L526] GGET     A=11 B=0 C=0 D=0 'd_ms'
00481 [L526] TGETS    A=11 B=11 C=87 D=2903 'd_u'
00482 [L526] TGETS    A=11 B=11 C=88 D=2904 'delay'
00483 [L526] MOV      A=12 B=0 C=9 D=9 
00484 [L526] KNUM     A=13 B=0 C=11 D=11 0.1
00485 [L526] MOV      A=14 B=0 C=10 D=10 
00486 [L526] CALL     A=11 B=1 C=4 D=260 
00487 [L526] UCLO     A=8 B=128 C=0 D=32768 target=488
00488 [L528] UCLO     A=0 B=128 C=0 D=32768 target=489
00489 [L528] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto20 offset=0x29a1 source_lines=532-539 params=0
UPVALUES ['currentPackageDataTable']
00001 [L533] UGET     A=0 B=0 C=0 D=0 currentPackageDataTable
00002 [L533] TGETS    A=0 B=0 C=0 D=0 'currentPackageItems'
00003 [L534] IST      A=0 B=0 C=0 D=0 
00004 [L534] JMP      A=1 B=128 C=1 D=32769 target=6
00005 [L535] RET0     A=0 B=0 C=1 D=1 
00006 [L538] GGET     A=1 B=0 C=1 D=1 'd_ms'
00007 [L538] TGETS    A=1 B=1 C=2 D=258 'd_batchSaleUI'
00008 [L538] TGETS    A=1 B=1 C=3 D=259 'show'
00009 [L538] MOV      A=2 B=0 C=0 D=0 
00010 [L538] CALL     A=1 B=1 C=2 D=258 
00011 [L539] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto21 offset=0x2a42 source_lines=541-546 params=0
UPVALUES []
00001 [L542] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L542] TGETS    A=0 B=0 C=1 D=1 'd_equipAdvanceUI'
00003 [L542] TGETS    A=0 B=0 C=2 D=2 'canJoin'
00004 [L542] KPRI     A=1 B=0 C=2 D=2 
00005 [L542] CALL     A=0 B=2 C=2 D=514 
00006 [L542] IST      A=0 B=0 C=0 D=0 
00007 [L542] JMP      A=0 B=128 C=1 D=32769 target=9
00008 [L543] RET0     A=0 B=0 C=1 D=1 
00009 [L545] GGET     A=0 B=0 C=0 D=0 'd_ms'
00010 [L545] TGETS    A=0 B=0 C=1 D=1 'd_equipAdvanceUI'
00011 [L545] TGETS    A=0 B=0 C=3 D=3 'showAdvanceLayer'
00012 [L545] GGET     A=1 B=0 C=4 D=4 'g_packageUI'
00013 [L545] TGETS    A=1 B=1 C=5 D=261 'parent'
00014 [L545] KSHORT   A=2 B=0 C=20 D=20 20
00015 [L545] CALL     A=0 B=1 C=3 D=259 
00016 [L546] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto22 offset=0x2ae2 source_lines=565-568 params=0
UPVALUES ['CCDirector', 'currentPackageDataTable']
00001 [L566] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L566] TGETS    A=0 B=0 C=1 D=1 'd_filterLayer'
00003 [L566] TGETS    A=0 B=0 C=2 D=2 'show'
00004 [L566] UGET     A=1 B=0 C=0 D=0 CCDirector
00005 [L566] MOV      A=2 B=0 C=1 D=1 
00006 [L566] TGETS    A=1 B=1 C=3 D=259 'sharedDirector'
00007 [L566] CALL     A=1 B=2 C=2 D=514 
00008 [L566] MOV      A=2 B=0 C=1 D=1 
00009 [L566] TGETS    A=1 B=1 C=4 D=260 'getRunningScene'
00010 [L566] CALL     A=1 B=2 C=2 D=514 
00011 [L566] KSHORT   A=2 B=0 C=100 D=100 100
00012 [L567] GGET     A=3 B=0 C=0 D=0 'd_ms'
00013 [L567] TGETS    A=3 B=3 C=1 D=769 'd_filterLayer'
00014 [L567] TGETS    A=3 B=3 C=5 D=773 'TAG'
00015 [L567] TGETS    A=3 B=3 C=6 D=774 'Equip_All'
00016 [L567] GGET     A=4 B=0 C=7 D=7 'ensureFilter'
00017 [L567] UGET     A=5 B=0 C=1 D=1 currentPackageDataTable
00018 [L567] TGETS    A=5 B=5 C=8 D=1288 'currentFilter'
00019 [L566] CALL     A=0 B=1 C=6 D=262 
00020 [L568] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto23 offset=0x2bda source_lines=580-582 params=0
UPVALUES ['menu']
00001 [L581] UGET     A=0 B=0 C=0 D=0 menu
00002 [L581] MOV      A=1 B=0 C=0 D=0 
00003 [L581] TGETS    A=0 B=0 C=0 D=0 'setHandlerPriority'
00004 [L581] KSHORT   A=2 B=255 C=130 D=65410 -126
00005 [L581] CALL     A=0 B=1 C=3 D=259 
00006 [L582] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto24 offset=0x2c20 source_lines=548-584 params=3
UPVALUES ['CCArray', 'CCMenuItemImage', 'createBatchSaleLayer', 'showAdvance', 'CCDirector', 'currentPackageDataTable', 'CCMenu', 'CCPointMake']
00001 [L549] UGET     A=3 B=0 C=0 D=0 CCArray
00002 [L549] MOV      A=4 B=0 C=3 D=3 
00003 [L549] TGETS    A=3 B=3 C=0 D=768 'create'
00004 [L549] CALL     A=3 B=2 C=2 D=514 
00005 [L550] GGET     A=4 B=0 C=1 D=1 'packageTagDef'
00006 [L550] TGETS    A=4 B=4 C=2 D=1026 'fabao'
00007 [L550] ISGT     A=1 B=0 C=4 D=4 
00008 [L550] JMP      A=4 B=128 C=48 D=32816 target=57
00009 [L551] UGET     A=4 B=0 C=1 D=1 CCMenuItemImage
00010 [L551] MOV      A=5 B=0 C=4 D=4 
00011 [L551] TGETS    A=4 B=4 C=0 D=1024 'create'
00012 [L551] KSTR     A=6 B=0 C=3 D=3 'v2/packageUI/piliangchushou1.png'
00013 [L551] KSTR     A=7 B=0 C=4 D=4 'v2/packageUI/piliangchushou2.png'
00014 [L551] CALL     A=4 B=2 C=4 D=516 
00015 [L552] MOV      A=6 B=0 C=4 D=4 
00016 [L552] TGETS    A=5 B=4 C=5 D=1029 'registerScriptTapHandler'
00017 [L552] UGET     A=7 B=0 C=2 D=2 createBatchSaleLayer
00018 [L552] CALL     A=5 B=1 C=3 D=259 
00019 [L554] MOV      A=6 B=0 C=4 D=4 
00020 [L554] TGETS    A=5 B=4 C=6 D=1030 'setPosition'
00021 [L554] TGETS    A=7 B=2 C=7 D=519 'width'
00022 [L554] MULVN    A=7 B=7 C=0 D=1792 
00023 [L554] TGETS    A=8 B=2 C=8 D=520 'height'
00024 [L554] MULVN    A=8 B=8 C=1 D=2049 
00025 [L554] CALL     A=5 B=1 C=4 D=260 
00026 [L555] MOV      A=6 B=0 C=3 D=3 
00027 [L555] TGETS    A=5 B=3 C=9 D=777 'addObject'
00028 [L555] MOV      A=7 B=0 C=4 D=4 
00029 [L555] CALL     A=5 B=1 C=3 D=259 
00030 [L557] GGET     A=5 B=0 C=10 D=10 'd_ms'
00031 [L557] TGETS    A=5 B=5 C=11 D=1291 'd_equipAdvanceUI'
00032 [L557] TGETS    A=5 B=5 C=12 D=1292 'canJoin'
00033 [L557] CALL     A=5 B=2 C=1 D=513 
00034 [L557] ISF      A=0 B=0 C=5 D=5 
00035 [L557] JMP      A=6 B=128 C=21 D=32789 target=57
00036 [L558] UGET     A=5 B=0 C=1 D=1 CCMenuItemImage
00037 [L558] MOV      A=6 B=0 C=5 D=5 
00038 [L558] TGETS    A=5 B=5 C=0 D=1280 'create'
00039 [L558] KSTR     A=7 B=0 C=13 D=13 'v2/equipAdvanceUI/menu_ad1.png'
00040 [L558] KSTR     A=8 B=0 C=14 D=14 'v2/equipAdvanceUI/menu_ad2.png'
00041 [L558] CALL     A=5 B=2 C=4 D=516 
00042 [L559] MOV      A=7 B=0 C=5 D=5 
00043 [L559] TGETS    A=6 B=5 C=5 D=1285 'registerScriptTapHandler'
00044 [L559] UGET     A=8 B=0 C=3 D=3 showAdvance
00045 [L559] CALL     A=6 B=1 C=3 D=259 
00046 [L561] MOV      A=7 B=0 C=5 D=5 
00047 [L561] TGETS    A=6 B=5 C=6 D=1286 'setPosition'
00048 [L561] TGETS    A=8 B=2 C=7 D=519 'width'
00049 [L561] MULVN    A=8 B=8 C=2 D=2050 
00050 [L561] TGETS    A=9 B=2 C=8 D=520 'height'
00051 [L561] MULVN    A=9 B=9 C=1 D=2305 
00052 [L561] CALL     A=6 B=1 C=4 D=260 
00053 [L562] MOV      A=7 B=0 C=3 D=3 
00054 [L562] TGETS    A=6 B=3 C=9 D=777 'addObject'
00055 [L562] MOV      A=8 B=0 C=5 D=5 
00056 [L562] CALL     A=6 B=1 C=3 D=259 
00057 [L568] FNEW     A=4 B=0 C=15 D=15 {'kind': 'proto', 'id': 22}
00058 [L570] UGET     A=5 B=0 C=1 D=1 CCMenuItemImage
00059 [L570] MOV      A=6 B=0 C=5 D=5 
00060 [L570] TGETS    A=5 B=5 C=0 D=1280 'create'
00061 [L570] KSTR     A=7 B=0 C=16 D=16 'v2/buttons/filter21.png'
00062 [L570] KSTR     A=8 B=0 C=17 D=17 'v2/buttons/filter22.png'
00063 [L570] CALL     A=5 B=2 C=4 D=516 
00064 [L571] MOV      A=7 B=0 C=5 D=5 
00065 [L571] TGETS    A=6 B=5 C=5 D=1285 'registerScriptTapHandler'
00066 [L571] MOV      A=8 B=0 C=4 D=4 
00067 [L571] CALL     A=6 B=1 C=3 D=259 
00068 [L573] MOV      A=7 B=0 C=5 D=5 
00069 [L573] TGETS    A=6 B=5 C=6 D=1286 'setPosition'
00070 [L573] TGETS    A=8 B=2 C=7 D=519 'width'
00071 [L573] MULVN    A=8 B=8 C=3 D=2051 
00072 [L573] TGETS    A=9 B=2 C=8 D=520 'height'
00073 [L573] MULVN    A=9 B=9 C=1 D=2305 
00074 [L573] CALL     A=6 B=1 C=4 D=260 
00075 [L574] MOV      A=7 B=0 C=3 D=3 
00076 [L574] TGETS    A=6 B=3 C=9 D=777 'addObject'
00077 [L574] MOV      A=8 B=0 C=5 D=5 
00078 [L574] CALL     A=6 B=1 C=3 D=259 
00079 [L576] UGET     A=6 B=0 C=6 D=6 CCMenu
00080 [L576] MOV      A=7 B=0 C=6 D=6 
00081 [L576] TGETS    A=6 B=6 C=18 D=1554 'createWithArray'
00082 [L576] MOV      A=8 B=0 C=3 D=3 
00083 [L576] CALL     A=6 B=2 C=3 D=515 
00084 [L577] MOV      A=8 B=0 C=6 D=6 
00085 [L577] TGETS    A=7 B=6 C=6 D=1542 'setPosition'
00086 [L577] UGET     A=9 B=0 C=7 D=7 CCPointMake
00087 [L577] KSHORT   A=10 B=0 C=0 D=0 0
00088 [L577] KSHORT   A=11 B=0 C=0 D=0 0
00089 [L577] CALL     A=9 B=0 C=3 D=3 
00090 [L577] CALLM    A=7 B=1 C=1 D=257 
00091 [L578] MOV      A=8 B=0 C=0 D=0 
00092 [L578] TGETS    A=7 B=0 C=19 D=19 'addChild'
00093 [L578] MOV      A=9 B=0 C=6 D=6 
00094 [L578] CALL     A=7 B=1 C=3 D=259 
00095 [L582] FNEW     A=7 B=0 C=20 D=20 {'kind': 'proto', 'id': 23}
00096 [L584] UCLO     A=0 B=128 C=0 D=32768 target=97
00097 [L584] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto25 offset=0x307b source_lines=596-602 params=0
UPVALUES ['packageTag', 'num']
00001 [L597] UGET     A=0 B=0 C=0 D=0 packageTag
00002 [L597] GGET     A=1 B=0 C=0 D=0 'packageTagDef'
00003 [L597] TGETS    A=1 B=1 C=1 D=257 'props'
00004 [L597] ISEQV    A=0 B=0 C=1 D=1 
00005 [L597] JMP      A=0 B=128 C=9 D=32777 target=15
00006 [L597] UGET     A=0 B=0 C=0 D=0 packageTag
00007 [L597] GGET     A=1 B=0 C=0 D=0 'packageTagDef'
00008 [L597] TGETS    A=1 B=1 C=2 D=258 'stone'
00009 [L597] ISEQV    A=0 B=0 C=1 D=1 
00010 [L597] JMP      A=0 B=128 C=4 D=32772 target=15
00011 [L598] UGET     A=0 B=0 C=1 D=1 num
00012 [L598] ADDVN    A=0 B=0 C=0 D=0 
00013 [L598] RET1     A=0 B=0 C=2 D=2 
00014 [L598] JMP      A=0 B=128 C=2 D=32770 target=17
00015 [L600] UGET     A=0 B=0 C=1 D=1 num
00016 [L600] RET1     A=0 B=0 C=2 D=2 
00017 [L602] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto26 offset=0x310c source_lines=606-622 params=1
UPVALUES ['CCNode', 'packageTag', 'createHeaderMenu', 'headerMenuSize', 'packageItemsInfo', 'createCellOnPackage', 'bkgPic', 'cellSize']
00001 [L607] UGET     A=1 B=0 C=0 D=0 CCNode
00002 [L607] MOV      A=2 B=0 C=1 D=1 
00003 [L607] TGETS    A=1 B=1 C=0 D=256 'create'
00004 [L607] CALL     A=1 B=2 C=2 D=514 
00005 [L608] UGET     A=2 B=0 C=1 D=1 packageTag
00006 [L608] GGET     A=3 B=0 C=1 D=1 'packageTagDef'
00007 [L608] TGETS    A=3 B=3 C=2 D=770 'props'
00008 [L608] ISEQV    A=2 B=0 C=3 D=3 
00009 [L608] JMP      A=2 B=128 C=28 D=32796 target=38
00010 [L608] UGET     A=2 B=0 C=1 D=1 packageTag
00011 [L608] GGET     A=3 B=0 C=1 D=1 'packageTagDef'
00012 [L608] TGETS    A=3 B=3 C=3 D=771 'stone'
00013 [L608] ISEQV    A=2 B=0 C=3 D=3 
00014 [L608] JMP      A=2 B=128 C=23 D=32791 target=38
00015 [L609] ISNEN    A=0 B=0 C=0 D=0 1
00016 [L609] JMP      A=2 B=128 C=6 D=32774 target=23
00017 [L610] UGET     A=2 B=0 C=2 D=2 createHeaderMenu
00018 [L610] MOV      A=3 B=0 C=1 D=1 
00019 [L610] UGET     A=4 B=0 C=1 D=1 packageTag
00020 [L610] UGET     A=5 B=0 C=3 D=3 headerMenuSize
00021 [L610] CALL     A=2 B=1 C=4 D=260 
00022 [L610] JMP      A=2 B=128 C=27 D=32795 target=50
00023 [L612] UGET     A=2 B=0 C=4 D=4 packageItemsInfo
00024 [L612] SUBVN    A=3 B=0 C=0 D=0 
00025 [L612] TGETV    A=2 B=2 C=3 D=515 
00026 [L612] ISF      A=0 B=0 C=2 D=2 
00027 [L612] JMP      A=3 B=128 C=22 D=32790 target=50
00028 [L613] UGET     A=2 B=0 C=5 D=5 createCellOnPackage
00029 [L613] MOV      A=3 B=0 C=1 D=1 
00030 [L613] UGET     A=4 B=0 C=1 D=1 packageTag
00031 [L613] UGET     A=5 B=0 C=4 D=4 packageItemsInfo
00032 [L613] SUBVN    A=6 B=0 C=0 D=0 
00033 [L613] TGETV    A=5 B=5 C=6 D=1286 
00034 [L613] UGET     A=6 B=0 C=6 D=6 bkgPic
00035 [L613] UGET     A=7 B=0 C=7 D=7 cellSize
00036 [L613] CALL     A=2 B=1 C=6 D=262 
00037 [L615] JMP      A=2 B=128 C=12 D=32780 target=50
00038 [L617] UGET     A=2 B=0 C=4 D=4 packageItemsInfo
00039 [L617] TGETV    A=2 B=2 C=0 D=512 
00040 [L617] ISF      A=0 B=0 C=2 D=2 
00041 [L617] JMP      A=3 B=128 C=8 D=32776 target=50
00042 [L618] UGET     A=2 B=0 C=5 D=5 createCellOnPackage
00043 [L618] MOV      A=3 B=0 C=1 D=1 
00044 [L618] UGET     A=4 B=0 C=1 D=1 packageTag
00045 [L618] UGET     A=5 B=0 C=4 D=4 packageItemsInfo
00046 [L618] TGETV    A=5 B=5 C=0 D=1280 
00047 [L618] UGET     A=6 B=0 C=6 D=6 bkgPic
00048 [L618] UGET     A=7 B=0 C=7 D=7 cellSize
00049 [L618] CALL     A=2 B=1 C=6 D=262 
00050 [L621] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto27 offset=0x32bd source_lines=624-630 params=1
UPVALUES ['packageTag', 'headerMenuSize', 'cellSize']
00001 [L625] ISNEN    A=0 B=0 C=0 D=0 1
00002 [L625] JMP      A=1 B=128 C=14 D=32782 target=17
00003 [L625] UGET     A=1 B=0 C=0 D=0 packageTag
00004 [L625] GGET     A=2 B=0 C=0 D=0 'packageTagDef'
00005 [L625] TGETS    A=2 B=2 C=1 D=513 'props'
00006 [L625] ISEQV    A=1 B=0 C=2 D=2 
00007 [L625] JMP      A=1 B=128 C=9 D=32777 target=17
00008 [L625] UGET     A=1 B=0 C=0 D=0 packageTag
00009 [L625] GGET     A=2 B=0 C=0 D=0 'packageTagDef'
00010 [L625] TGETS    A=2 B=2 C=2 D=514 'stone'
00011 [L625] ISEQV    A=1 B=0 C=2 D=2 
00012 [L625] JMP      A=1 B=128 C=4 D=32772 target=17
00013 [L626] UGET     A=1 B=0 C=1 D=1 headerMenuSize
00014 [L626] TGETS    A=1 B=1 C=3 D=259 'height'
00015 [L626] RET1     A=1 B=0 C=2 D=2 
00016 [L626] JMP      A=1 B=128 C=3 D=32771 target=20
00017 [L628] UGET     A=1 B=0 C=2 D=2 cellSize
00018 [L628] TGETS    A=1 B=1 C=3 D=259 'height'
00019 [L628] RET1     A=1 B=0 C=2 D=2 
00020 [L630] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto28 offset=0x3382 source_lines=588-633 params=1
UPVALUES ['currentPackageDataTable', 'CCSizeMake', 'scrSize', 'CCNode', 'createHeaderMenu', 'headerMenuSize', 'createCellOnPackage']
00001 [L590] UGET     A=1 B=0 C=0 D=0 currentPackageDataTable
00002 [L590] TGETS    A=1 B=1 C=0 D=256 'packageTag'
00003 [L591] UGET     A=2 B=0 C=1 D=1 CCSizeMake
00004 [L591] UGET     A=3 B=0 C=2 D=2 scrSize
00005 [L591] TGETS    A=3 B=3 C=1 D=769 'width'
00006 [L591] MULNV    A=3 B=3 C=0 D=768 
00007 [L591] UGET     A=4 B=0 C=2 D=2 scrSize
00008 [L591] TGETS    A=4 B=4 C=2 D=1026 'height'
00009 [L591] MULNV    A=4 B=4 C=1 D=1025 
00010 [L591] CALL     A=2 B=2 C=3 D=515 
00011 [L592] KSTR     A=3 B=0 C=3 D=3 'v2/packageUI/xinxilan.png'
00012 [L594] TNEW     A=4 B=0 C=0 D=0 
00013 [L595] LEN      A=5 B=0 C=0 D=0 
00014 [L602] FNEW     A=6 B=0 C=5 D=5 {'kind': 'proto', 'id': 25}
00015 [L602] TSETS    A=6 B=4 C=4 D=1028 'tableViewNumberOfRows'
00016 [L604] UGET     A=6 B=0 C=0 D=0 currentPackageDataTable
00017 [L604] TSETS    A=0 B=6 C=6 D=1542 'currentShowItems'
00018 [L622] FNEW     A=6 B=0 C=8 D=8 {'kind': 'proto', 'id': 26}
00019 [L622] TSETS    A=6 B=4 C=7 D=1031 'drawCellAtIndex'
00020 [L630] FNEW     A=6 B=0 C=10 D=10 {'kind': 'proto', 'id': 27}
00021 [L630] TSETS    A=6 B=4 C=9 D=1033 'heightForRowAtIndex'
00022 [L632] UCLO     A=0 B=128 C=0 D=32768 target=23
00023 [L632] RET1     A=4 B=0 C=2 D=2 

FUNCTION proto29 offset=0x3553 source_lines=635-654 params=1
UPVALUES ['currentPackageDataTable', 'getPackageCellsDataSource']
00001 [L636] UGET     A=1 B=0 C=0 D=0 currentPackageDataTable
00002 [L636] TGETS    A=1 B=1 C=0 D=256 'packageTableView'
00003 [L637] IST      A=0 B=0 C=1 D=1 
00004 [L637] JMP      A=2 B=128 C=1 D=32769 target=6
00005 [L638] RET0     A=0 B=0 C=1 D=1 
00006 [L641] GGET     A=2 B=0 C=1 D=1 'd_ms'
00007 [L641] TGETS    A=2 B=2 C=2 D=514 'd_filterLayer'
00008 [L641] TGETS    A=2 B=2 C=3 D=515 'check'
00009 [L643] UGET     A=3 B=0 C=0 D=0 currentPackageDataTable
00010 [L643] TSETS    A=0 B=3 C=4 D=772 'currentFilter'
00011 [L644] UGET     A=3 B=0 C=0 D=0 currentPackageDataTable
00012 [L644] TGETS    A=3 B=3 C=5 D=773 'currentPackageItems'
00013 [L645] TNEW     A=4 B=0 C=0 D=0 
00014 [L646] KSHORT   A=5 B=0 C=1 D=1 1
00015 [L646] LEN      A=6 B=0 C=3 D=3 
00016 [L646] KSHORT   A=7 B=0 C=1 D=1 1
00017 [L646] FORI     A=5 B=128 C=13 D=32781 target=31
00018 [L647] ISF      A=0 B=0 C=2 D=2 
00019 [L647] JMP      A=9 B=128 C=10 D=32778 target=30
00020 [L647] MOV      A=9 B=0 C=2 D=2 
00021 [L647] TGETV    A=10 B=3 C=8 D=776 
00022 [L647] MOV      A=11 B=0 C=0 D=0 
00023 [L647] CALL     A=9 B=2 C=3 D=515 
00024 [L647] ISF      A=0 B=0 C=9 D=9 
00025 [L647] JMP      A=10 B=128 C=4 D=32772 target=30
00026 [L648] LEN      A=9 B=0 C=4 D=4 
00027 [L648] ADDVN    A=9 B=9 C=0 D=2304 
00028 [L648] TGETV    A=10 B=3 C=8 D=776 
00029 [L648] TSETV    A=10 B=4 C=9 D=1033 
00030 [L646] FORL     A=5 B=127 C=243 D=32755 target=18
00031 [L652] UGET     A=5 B=0 C=1 D=1 getPackageCellsDataSource
00032 [L652] MOV      A=6 B=0 C=4 D=4 
00033 [L652] CALL     A=5 B=2 C=2 D=514 
00034 [L653] MOV      A=7 B=0 C=1 D=1 
00035 [L653] TGETS    A=6 B=1 C=6 D=262 'reloadData'
00036 [L653] MOV      A=8 B=0 C=5 D=5 
00037 [L653] CALL     A=6 B=1 C=3 D=259 
00038 [L654] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto30 offset=0x3715 source_lines=656-695 params=1
UPVALUES ['o_t', 'm_t', 'table']
00001 [L658] GGET     A=1 B=0 C=0 D=0 'g_isPackageSorted'
00002 [L658] IST      A=0 B=0 C=1 D=1 
00003 [L658] JMP      A=1 B=128 C=2 D=32770 target=6
00004 [L659] GGET     A=1 B=0 C=1 D=1 'sortItems'
00005 [L659] CALL     A=1 B=1 C=1 D=257 
00006 [L662] GGET     A=1 B=0 C=2 D=2 'g_packageItemsInfo'
00007 [L664] GGET     A=2 B=0 C=3 D=3 'packageTagDef'
00008 [L664] TGETS    A=2 B=2 C=4 D=516 'weapon'
00009 [L664] ISNEV    A=0 B=0 C=2 D=2 
00010 [L664] JMP      A=2 B=128 C=8 D=32776 target=19
00011 [L665] GGET     A=2 B=0 C=5 D=5 'g_reorgItemsInfo'
00012 [L665] UGET     A=3 B=0 C=0 D=0 o_t
00013 [L665] TGETS    A=3 B=3 C=6 D=774 'item'
00014 [L665] TGETV    A=2 B=2 C=3 D=515 
00015 [L665] UGET     A=3 B=0 C=1 D=1 m_t
00016 [L665] TGETS    A=3 B=3 C=4 D=772 'weapon'
00017 [L665] TGETV    A=1 B=2 C=3 D=515 
00018 [L665] JMP      A=2 B=128 C=70 D=32838 target=89
00019 [L667] GGET     A=2 B=0 C=3 D=3 'packageTagDef'
00020 [L667] TGETS    A=2 B=2 C=7 D=519 'armor'
00021 [L667] ISNEV    A=0 B=0 C=2 D=2 
00022 [L667] JMP      A=2 B=128 C=8 D=32776 target=31
00023 [L668] GGET     A=2 B=0 C=5 D=5 'g_reorgItemsInfo'
00024 [L668] UGET     A=3 B=0 C=0 D=0 o_t
00025 [L668] TGETS    A=3 B=3 C=6 D=774 'item'
00026 [L668] TGETV    A=2 B=2 C=3 D=515 
00027 [L668] UGET     A=3 B=0 C=1 D=1 m_t
00028 [L668] TGETS    A=3 B=3 C=8 D=776 'guard'
00029 [L668] TGETV    A=1 B=2 C=3 D=515 
00030 [L668] JMP      A=2 B=128 C=58 D=32826 target=89
00031 [L670] GGET     A=2 B=0 C=3 D=3 'packageTagDef'
00032 [L670] TGETS    A=2 B=2 C=9 D=521 'fabao'
00033 [L670] ISNEV    A=0 B=0 C=2 D=2 
00034 [L670] JMP      A=2 B=128 C=8 D=32776 target=43
00035 [L671] GGET     A=2 B=0 C=5 D=5 'g_reorgItemsInfo'
00036 [L671] UGET     A=3 B=0 C=0 D=0 o_t
00037 [L671] TGETS    A=3 B=3 C=6 D=774 'item'
00038 [L671] TGETV    A=2 B=2 C=3 D=515 
00039 [L671] UGET     A=3 B=0 C=1 D=1 m_t
00040 [L671] TGETS    A=3 B=3 C=10 D=778 'talismans'
00041 [L671] TGETV    A=1 B=2 C=3 D=515 
00042 [L671] JMP      A=2 B=128 C=46 D=32814 target=89
00043 [L673] GGET     A=2 B=0 C=3 D=3 'packageTagDef'
00044 [L673] TGETS    A=2 B=2 C=11 D=523 'skill'
00045 [L673] ISNEV    A=0 B=0 C=2 D=2 
00046 [L673] JMP      A=2 B=128 C=23 D=32791 target=70
00047 [L674] GGET     A=2 B=0 C=5 D=5 'g_reorgItemsInfo'
00048 [L674] UGET     A=3 B=0 C=0 D=0 o_t
00049 [L674] TGETS    A=3 B=3 C=11 D=779 'skill'
00050 [L674] TGETV    A=2 B=2 C=3 D=515 
00051 [L674] ISTC     A=1 B=0 C=2 D=2 
00052 [L674] JMP      A=3 B=128 C=1 D=32769 target=54
00053 [L674] TNEW     A=1 B=0 C=0 D=0 
00054 [L675] LEN      A=2 B=0 C=1 D=1 
00055 [L676] MOV      A=3 B=0 C=2 D=2 
00056 [L676] KSHORT   A=4 B=0 C=1 D=1 1
00057 [L676] KSHORT   A=5 B=255 C=255 D=65535 -1
00058 [L676] FORI     A=3 B=128 C=10 D=32778 target=69
00059 [L677] TGETV    A=7 B=1 C=6 D=262 
00060 [L677] TGETS    A=7 B=7 C=12 D=1804 'protogenic'
00061 [L677] ISEQN    A=7 B=0 C=0 D=0 0
00062 [L677] JMP      A=7 B=128 C=5 D=32773 target=68
00063 [L678] UGET     A=7 B=0 C=2 D=2 table
00064 [L678] TGETS    A=7 B=7 C=13 D=1805 'remove'
00065 [L678] MOV      A=8 B=0 C=1 D=1 
00066 [L678] MOV      A=9 B=0 C=6 D=6 
00067 [L678] CALL     A=7 B=1 C=3 D=259 
00068 [L676] FORL     A=3 B=127 C=246 D=32758 target=59
00069 [L680] JMP      A=2 B=128 C=19 D=32787 target=89
00070 [L683] GGET     A=2 B=0 C=3 D=3 'packageTagDef'
00071 [L683] TGETS    A=2 B=2 C=14 D=526 'props'
00072 [L683] ISNEV    A=0 B=0 C=2 D=2 
00073 [L683] JMP      A=2 B=128 C=4 D=32772 target=78
00074 [L684] GGET     A=2 B=0 C=15 D=15 'getAllProps'
00075 [L684] CALL     A=2 B=1 C=1 D=257 
00076 [L685] GGET     A=1 B=0 C=16 D=16 'g_propsTable'
00077 [L685] JMP      A=2 B=128 C=11 D=32779 target=89
00078 [L686] GGET     A=2 B=0 C=3 D=3 'packageTagDef'
00079 [L686] TGETS    A=2 B=2 C=17 D=529 'stone'
00080 [L686] ISNEV    A=0 B=0 C=2 D=2 
00081 [L686] JMP      A=2 B=128 C=7 D=32775 target=89
00082 [L687] GGET     A=2 B=0 C=5 D=5 'g_reorgItemsInfo'
00083 [L687] UGET     A=3 B=0 C=0 D=0 o_t
00084 [L687] TGETS    A=3 B=3 C=6 D=774 'item'
00085 [L687] TGETV    A=2 B=2 C=3 D=515 
00086 [L687] UGET     A=3 B=0 C=1 D=1 m_t
00087 [L687] TGETS    A=3 B=3 C=17 D=785 'stone'
00088 [L687] TGETV    A=1 B=2 C=3 D=515 
00089 [L690] IST      A=0 B=0 C=1 D=1 
00090 [L690] JMP      A=2 B=128 C=1 D=32769 target=92
00091 [L691] TNEW     A=1 B=0 C=0 D=0 
00092 [L694] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto31 offset=0x39ec source_lines=718-722 params=1
UPVALUES ['currentPackageDataTable']
00001 [L719] TGETS    A=1 B=0 C=0 D=0 'name'
00002 [L719] ISNES    A=1 B=0 C=1 D=1 'exit'
00003 [L719] JMP      A=1 B=128 C=2 D=32770 target=6
00004 [L720] TNEW     A=1 B=0 C=0 D=0 
00005 [L720] USETV    A=0 B=0 C=1 D=1 currentPackageDataTable
00006 [L722] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto32 offset=0x3a48 source_lines=698-747 params=1
UPVALUES ['cclog', 'CCLayer', 'currentPackageDataTable', 'getItemsByPackageTag', 'CCDirector', 'getPackageCellsDataSource']
00001 [L699] UGET     A=1 B=0 C=0 D=0 cclog
00002 [L699] KSTR     A=2 B=0 C=0 D=0 'show package, packageTag: %d'
00003 [L699] MOV      A=3 B=0 C=0 D=0 
00004 [L699] CALL     A=1 B=1 C=3 D=259 
00005 [L701] GGET     A=1 B=0 C=1 D=1 'g_lastSelectedItemButton'
00006 [L701] ISEQN    A=1 B=0 C=0 D=0 0
00007 [L701] JMP      A=1 B=128 C=7 D=32775 target=15
00008 [L702] GGET     A=1 B=0 C=2 D=2 'g_itemButton'
00009 [L702] GGET     A=2 B=0 C=1 D=1 'g_lastSelectedItemButton'
00010 [L702] TGETV    A=1 B=1 C=2 D=258 
00011 [L702] MOV      A=2 B=0 C=1 D=1 
00012 [L702] TGETS    A=1 B=1 C=3 D=259 'setEnabled'
00013 [L702] KPRI     A=3 B=0 C=2 D=2 
00014 [L702] CALL     A=1 B=1 C=3 D=259 
00015 [L704] GGET     A=1 B=0 C=2 D=2 'g_itemButton'
00016 [L704] TGETV    A=1 B=1 C=0 D=256 
00017 [L704] MOV      A=2 B=0 C=1 D=1 
00018 [L704] TGETS    A=1 B=1 C=3 D=259 'setEnabled'
00019 [L704] KPRI     A=3 B=0 C=1 D=1 
00020 [L704] CALL     A=1 B=1 C=3 D=259 
00021 [L706] GSET     A=0 B=0 C=1 D=1 'g_lastSelectedItemButton'
00022 [L708] GGET     A=1 B=0 C=4 D=4 'tagDef'
00023 [L708] TGETS    A=1 B=1 C=5 D=261 'packageLayerTag'
00024 [L710] GGET     A=2 B=0 C=6 D=6 'g_packageUI'
00025 [L710] TGETS    A=2 B=2 C=7 D=519 'board_layer'
00026 [L710] MOV      A=3 B=0 C=2 D=2 
00027 [L710] TGETS    A=2 B=2 C=8 D=520 'getChildByTag'
00028 [L710] MOV      A=4 B=0 C=1 D=1 
00029 [L710] CALL     A=2 B=2 C=3 D=515 
00030 [L711] IST      A=0 B=0 C=2 D=2 
00031 [L711] JMP      A=3 B=128 C=15 D=32783 target=47
00032 [L712] UGET     A=3 B=0 C=1 D=1 CCLayer
00033 [L712] MOV      A=4 B=0 C=3 D=3 
00034 [L712] TGETS    A=3 B=3 C=9 D=777 'create'
00035 [L712] CALL     A=3 B=2 C=2 D=514 
00036 [L712] MOV      A=2 B=0 C=3 D=3 
00037 [L713] GGET     A=3 B=0 C=6 D=6 'g_packageUI'
00038 [L713] TGETS    A=3 B=3 C=7 D=775 'board_layer'
00039 [L713] MOV      A=4 B=0 C=3 D=3 
00040 [L713] TGETS    A=3 B=3 C=10 D=778 'addChild'
00041 [L713] MOV      A=5 B=0 C=2 D=2 
00042 [L713] CALL     A=3 B=1 C=3 D=259 
00043 [L714] MOV      A=4 B=0 C=2 D=2 
00044 [L714] TGETS    A=3 B=2 C=11 D=523 'setTag'
00045 [L714] MOV      A=5 B=0 C=1 D=1 
00046 [L714] CALL     A=3 B=1 C=3 D=259 
00047 [L716] MOV      A=4 B=0 C=2 D=2 
00048 [L716] TGETS    A=3 B=2 C=12 D=524 'removeAllChildrenWithCleanup'
00049 [L716] KPRI     A=5 B=0 C=2 D=2 
00050 [L716] CALL     A=3 B=1 C=3 D=259 
00051 [L722] FNEW     A=3 B=0 C=13 D=13 {'kind': 'proto', 'id': 31}
00052 [L724] MOV      A=5 B=0 C=2 D=2 
00053 [L724] TGETS    A=4 B=2 C=14 D=526 'registerScriptHandler'
00054 [L724] MOV      A=6 B=0 C=3 D=3 
00055 [L724] CALL     A=4 B=1 C=3 D=259 
00056 [L726] UGET     A=4 B=0 C=2 D=2 currentPackageDataTable
00057 [L726] TSETS    A=0 B=4 C=15 D=1039 'packageTag'
00058 [L728] UGET     A=4 B=0 C=3 D=3 getItemsByPackageTag
00059 [L728] MOV      A=5 B=0 C=0 D=0 
00060 [L728] CALL     A=4 B=2 C=2 D=514 
00061 [L728] GSET     A=4 B=0 C=16 D=16 'packageItemsInfo'
00062 [L730] UGET     A=4 B=0 C=2 D=2 currentPackageDataTable
00063 [L730] GGET     A=5 B=0 C=16 D=16 'packageItemsInfo'
00064 [L730] TSETS    A=5 B=4 C=17 D=1041 'currentPackageItems'
00065 [L732] GGET     A=4 B=0 C=16 D=16 'packageItemsInfo'
00066 [L732] LEN      A=4 B=0 C=4 D=4 
00067 [L732] KSHORT   A=5 B=0 C=0 D=0 0
00068 [L732] ISGT     A=4 B=0 C=5 D=5 
00069 [L732] JMP      A=4 B=128 C=2 D=32770 target=72
00070 [L733] UCLO     A=0 B=128 C=0 D=32768 target=71
00071 [L733] RET0     A=0 B=0 C=1 D=1 
00072 [L736] UGET     A=4 B=0 C=4 D=4 CCDirector
00073 [L736] MOV      A=5 B=0 C=4 D=4 
00074 [L736] TGETS    A=4 B=4 C=18 D=1042 'sharedDirector'
00075 [L736] CALL     A=4 B=2 C=2 D=514 
00076 [L736] MOV      A=5 B=0 C=4 D=4 
00077 [L736] TGETS    A=4 B=4 C=19 D=1043 'getVisibleSize'
00078 [L736] CALL     A=4 B=2 C=2 D=514 
00079 [L737] GGET     A=5 B=0 C=6 D=6 'g_packageUI'
00080 [L737] TGETS    A=5 B=5 C=20 D=1300 'board_size'
00081 [L738] TDUP     A=6 B=0 C=22 D=22 {'kind': 'table', 'value': {}}
00082 [L738] TGETS    A=7 B=4 C=21 D=1045 'width'
00083 [L738] MULVN    A=7 B=7 C=1 D=1793 
00084 [L738] TSETS    A=7 B=6 C=23 D=1559 'x'
00085 [L738] TGETS    A=7 B=5 C=24 D=1304 'y'
00086 [L738] TSETS    A=7 B=6 C=24 D=1560 'y'
00087 [L738] TGETS    A=7 B=4 C=21 D=1045 'width'
00088 [L738] MULVN    A=7 B=7 C=2 D=1794 
00089 [L738] TSETS    A=7 B=6 C=21 D=1557 'width'
00090 [L738] TGETS    A=7 B=5 C=25 D=1305 'height'
00091 [L738] MULVN    A=7 B=7 C=3 D=1795 
00092 [L738] TSETS    A=7 B=6 C=25 D=1561 'height'
00093 [L739] GGET     A=7 B=0 C=26 D=26 'd_ms'
00094 [L739] TGETS    A=7 B=7 C=27 D=1819 'd_tableView'
00095 [L739] TGETS    A=7 B=7 C=28 D=1820 'tableView'
00096 [L739] MOV      A=8 B=0 C=2 D=2 
00097 [L739] MOV      A=9 B=0 C=6 D=6 
00098 [L739] CALL     A=7 B=2 C=3 D=515 
00099 [L741] UGET     A=8 B=0 C=2 D=2 currentPackageDataTable
00100 [L741] TSETS    A=7 B=8 C=29 D=2077 'packageTableView'
00101 [L743] UGET     A=8 B=0 C=5 D=5 getPackageCellsDataSource
00102 [L743] GGET     A=9 B=0 C=16 D=16 'packageItemsInfo'
00103 [L743] CALL     A=8 B=2 C=2 D=514 
00104 [L745] MOV      A=10 B=0 C=7 D=7 
00105 [L745] TGETS    A=9 B=7 C=30 D=1822 'startScroll'
00106 [L745] CALL     A=9 B=1 C=2 D=258 
00107 [L746] MOV      A=10 B=0 C=7 D=7 
00108 [L746] TGETS    A=9 B=7 C=31 D=1823 'setDataSource'
00109 [L746] MOV      A=11 B=0 C=8 D=8 
00110 [L746] CALL     A=9 B=1 C=3 D=259 
00111 [L747] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto33 offset=0x3f1b source_lines=750-791 params=1
UPVALUES ['currentPackageDataTable', 'pairs']
00001 [L751] UGET     A=1 B=0 C=0 D=0 currentPackageDataTable
00002 [L751] TGETS    A=1 B=1 C=0 D=256 'packageTableView'
00003 [L752] IST      A=0 B=0 C=1 D=1 
00004 [L752] JMP      A=2 B=128 C=1 D=32769 target=6
00005 [L753] RET0     A=0 B=0 C=1 D=1 
00006 [L756] UGET     A=2 B=0 C=0 D=0 currentPackageDataTable
00007 [L756] TGETS    A=2 B=2 C=1 D=513 'packageTag'
00008 [L757] ISF      A=0 B=0 C=2 D=2 
00009 [L757] JMP      A=3 B=128 C=4 D=32772 target=14
00010 [L757] GGET     A=3 B=0 C=2 D=2 'packageTagDef'
00011 [L757] TGETS    A=3 B=3 C=3 D=771 'props'
00012 [L757] ISEQV    A=2 B=0 C=3 D=3 
00013 [L757] JMP      A=3 B=128 C=1 D=32769 target=15
00014 [L758] RET0     A=0 B=0 C=1 D=1 
00015 [L761] KPRI     A=3 B=0 C=0 D=0 
00016 [L762] GGET     A=4 B=0 C=4 D=4 'getAllProps'
00017 [L762] CALL     A=4 B=1 C=1 D=257 
00018 [L763] UGET     A=4 B=0 C=1 D=1 pairs
00019 [L763] GGET     A=5 B=0 C=5 D=5 'g_propsTable'
00020 [L763] CALL     A=4 B=4 C=2 D=1026 
00021 [L763] ISNEXT   A=7 B=128 C=5 D=32773 target=27
00022 [L764] TGETS    A=9 B=8 C=6 D=2054 'type_id'
00023 [L764] ISNEV    A=9 B=0 C=0 D=0 
00024 [L764] JMP      A=9 B=128 C=2 D=32770 target=27
00025 [L765] MOV      A=3 B=0 C=8 D=8 
00026 [L766] JMP      A=4 B=128 C=2 D=32770 target=29
00027 [L763] ITERN    A=7 B=3 C=3 D=771 
00028 [L763] ITERL    A=7 B=127 C=249 D=32761 target=22
00029 [L770] IST      A=0 B=0 C=3 D=3 
00030 [L770] JMP      A=4 B=128 C=3 D=32771 target=34
00031 [L771] GGET     A=4 B=0 C=7 D=7 'refreshPackage'
00032 [L771] CALL     A=4 B=1 C=1 D=257 
00033 [L772] RET0     A=0 B=0 C=1 D=1 
00034 [L775] UGET     A=4 B=0 C=0 D=0 currentPackageDataTable
00035 [L775] TGETS    A=4 B=4 C=8 D=1032 'currentShowItems'
00036 [L776] IST      A=0 B=0 C=4 D=4 
00037 [L776] JMP      A=5 B=128 C=1 D=32769 target=39
00038 [L777] RET0     A=0 B=0 C=1 D=1 
00039 [L780] KPRI     A=5 B=0 C=0 D=0 
00040 [L781] KSHORT   A=6 B=0 C=1 D=1 1
00041 [L781] LEN      A=7 B=0 C=4 D=4 
00042 [L781] KSHORT   A=8 B=0 C=1 D=1 1
00043 [L781] FORI     A=6 B=128 C=13 D=32781 target=57
00044 [L782] TGETV    A=10 B=4 C=9 D=1033 
00045 [L782] TGETS    A=10 B=10 C=9 D=2569 'id'
00046 [L782] TGETS    A=11 B=3 C=9 D=777 'id'
00047 [L782] ISNEV    A=10 B=0 C=11 D=11 
00048 [L782] JMP      A=10 B=128 C=7 D=32775 target=56
00049 [L782] TGETV    A=10 B=4 C=9 D=1033 
00050 [L782] TGETS    A=10 B=10 C=6 D=2566 'type_id'
00051 [L782] TGETS    A=11 B=3 C=6 D=774 'type_id'
00052 [L782] ISNEV    A=10 B=0 C=11 D=11 
00053 [L782] JMP      A=10 B=128 C=2 D=32770 target=56
00054 [L783] MOV      A=5 B=0 C=9 D=9 
00055 [L784] JMP      A=6 B=128 C=1 D=32769 target=57
00056 [L781] FORL     A=6 B=127 C=243 D=32755 target=44
00057 [L788] ISF      A=0 B=0 C=5 D=5 
00058 [L788] JMP      A=6 B=128 C=4 D=32772 target=63
00059 [L789] MOV      A=7 B=0 C=1 D=1 
00060 [L789] TGETS    A=6 B=1 C=10 D=266 'updateCellAtIndex'
00061 [L789] MOV      A=8 B=0 C=5 D=5 
00062 [L789] CALL     A=6 B=1 C=3 D=259 
00063 [L791] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto34 offset=0x417d source_lines=811-859 params=1
UPVALUES ['o_t', 'm_t', 'CCDirector']
00001 [L812] GGET     A=1 B=0 C=0 D=0 'g_isInPackage'
00002 [L812] ISF      A=0 B=0 C=1 D=1 
00003 [L812] JMP      A=2 B=128 C=63 D=32831 target=67
00004 [L812] GGET     A=1 B=0 C=1 D=1 'g_packageTag'
00005 [L812] GGET     A=2 B=0 C=2 D=2 'packageTagDef'
00006 [L812] TGETS    A=2 B=2 C=3 D=515 'props'
00007 [L812] ISNEV    A=1 B=0 C=2 D=2 
00008 [L812] JMP      A=1 B=128 C=58 D=32826 target=67
00009 [L813] TGETS    A=1 B=0 C=4 D=4 'type_id'
00010 [L814] TGETS    A=2 B=0 C=5 D=5 'attach_type'
00011 [L815] UGET     A=3 B=0 C=0 D=0 o_t
00012 [L815] TGETS    A=3 B=3 C=6 D=774 'item'
00013 [L815] ISEQV    A=2 B=0 C=3 D=3 
00014 [L815] JMP      A=3 B=128 C=1 D=32769 target=16
00015 [L816] RET0     A=0 B=0 C=1 D=1 
00016 [L819] GGET     A=3 B=0 C=7 D=7 'g_itemAttrTable'
00017 [L819] TGETV    A=3 B=3 C=1 D=769 
00018 [L820] ISF      A=0 B=0 C=3 D=3 
00019 [L820] JMP      A=4 B=128 C=3 D=32771 target=23
00020 [L820] TGETS    A=4 B=3 C=8 D=776 'mainType'
00021 [L820] IST      A=0 B=0 C=4 D=4 
00022 [L820] JMP      A=4 B=128 C=1 D=32769 target=24
00023 [L821] RET0     A=0 B=0 C=1 D=1 
00024 [L824] TGETS    A=4 B=3 C=8 D=776 'mainType'
00025 [L824] UGET     A=5 B=0 C=1 D=1 m_t
00026 [L824] TGETS    A=5 B=5 C=9 D=1289 'talismans'
00027 [L824] ISGT     A=4 B=0 C=5 D=5 
00028 [L824] JMP      A=4 B=128 C=1 D=32769 target=30
00029 [L825] RET0     A=0 B=0 C=1 D=1 
00030 [L838] UGET     A=4 B=0 C=2 D=2 CCDirector
00031 [L838] MOV      A=5 B=0 C=4 D=4 
00032 [L838] TGETS    A=4 B=4 C=10 D=1034 'sharedDirector'
00033 [L838] CALL     A=4 B=2 C=2 D=514 
00034 [L838] MOV      A=5 B=0 C=4 D=4 
00035 [L838] TGETS    A=4 B=4 C=11 D=1035 'getVisibleSize'
00036 [L838] CALL     A=4 B=2 C=2 D=514 
00037 [L840] GGET     A=5 B=0 C=12 D=12 'g_packageUI'
00038 [L840] TGETS    A=5 B=5 C=13 D=1293 'cells_layer'
00039 [L840] TGETS    A=5 B=5 C=14 D=1294 'cells_height'
00040 [L842] KNUM     A=6 B=0 C=0 D=0 0.23
00041 [L843] TGETS    A=7 B=4 C=15 D=1039 'height'
00042 [L843] DIVVV    A=7 B=5 C=7 D=1287 
00043 [L843] SUBNV    A=7 B=7 C=1 D=1793 
00044 [L845] TSETS    A=3 B=0 C=16 D=16 'csvInfo'
00045 [L855] TGETS    A=8 B=4 C=15 D=1039 'height'
00046 [L855] MULNV    A=8 B=8 C=2 D=2050 
00047 [L856] GGET     A=9 B=0 C=17 D=17 'createCell'
00048 [L856] MOV      A=10 B=0 C=0 D=0 
00049 [L856] MOV      A=11 B=0 C=6 D=6 
00050 [L856] MOV      A=12 B=0 C=7 D=7 
00051 [L856] GGET     A=13 B=0 C=2 D=2 'packageTagDef'
00052 [L856] TGETS    A=13 B=13 C=3 D=3331 'props'
00053 [L856] KSHORT   A=14 B=0 C=1 D=1 1
00054 [L856] CALL     A=9 B=3 C=6 D=774 
00055 [L857] GGET     A=11 B=0 C=12 D=12 'g_packageUI'
00056 [L857] TGETS    A=11 B=11 C=13 D=2829 'cells_layer'
00057 [L857] MOV      A=12 B=0 C=11 D=11 
00058 [L857] TGETS    A=11 B=11 C=18 D=2834 'addCell'
00059 [L857] MOV      A=13 B=0 C=9 D=9 
00060 [L857] TDUP     A=14 B=0 C=20 D=20 {'kind': 'table', 'value': {}}
00061 [L857] TGETS    A=15 B=10 C=19 D=2579 'width'
00062 [L857] TSETS    A=15 B=14 C=19 D=3603 'width'
00063 [L857] TGETS    A=15 B=10 C=15 D=2575 'height'
00064 [L857] ADDVV    A=15 B=15 C=8 D=3848 
00065 [L857] TSETS    A=15 B=14 C=15 D=3599 'height'
00066 [L857] CALL     A=11 B=1 C=4 D=260 
00067 [L859] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto35 offset=0x4468 source_lines=861-879 params=0
UPVALUES ['currentPackageDataTable', 'getItemsByPackageTag', 'getPackageCellsDataSource', 'cclog']
00001 [L862] UGET     A=0 B=0 C=0 D=0 currentPackageDataTable
00002 [L862] TGETS    A=0 B=0 C=0 D=0 'packageTableView'
00003 [L863] IST      A=0 B=0 C=0 D=0 
00004 [L863] JMP      A=1 B=128 C=1 D=32769 target=6
00005 [L864] RET0     A=0 B=0 C=1 D=1 
00006 [L867] UGET     A=1 B=0 C=0 D=0 currentPackageDataTable
00007 [L867] TGETS    A=1 B=1 C=1 D=257 'packageTag'
00008 [L868] IST      A=0 B=0 C=1 D=1 
00009 [L868] JMP      A=2 B=128 C=1 D=32769 target=11
00010 [L869] RET0     A=0 B=0 C=1 D=1 
00011 [L872] UGET     A=2 B=0 C=1 D=1 getItemsByPackageTag
00012 [L872] MOV      A=3 B=0 C=1 D=1 
00013 [L872] CALL     A=2 B=2 C=2 D=514 
00014 [L872] GSET     A=2 B=0 C=2 D=2 'packageItemsInfo'
00015 [L874] GGET     A=2 B=0 C=2 D=2 'packageItemsInfo'
00016 [L874] LEN      A=2 B=0 C=2 D=2 
00017 [L874] KSHORT   A=3 B=0 C=0 D=0 0
00018 [L874] ISGT     A=3 B=0 C=2 D=2 
00019 [L874] JMP      A=2 B=128 C=10 D=32778 target=30
00020 [L875] UGET     A=2 B=0 C=2 D=2 getPackageCellsDataSource
00021 [L875] GGET     A=3 B=0 C=2 D=2 'packageItemsInfo'
00022 [L875] CALL     A=2 B=2 C=2 D=514 
00023 [L876] UGET     A=3 B=0 C=3 D=3 cclog
00024 [L876] KSTR     A=4 B=0 C=3 D=3 'refreshPackage success, reloadData!!!!'
00025 [L876] CALL     A=3 B=1 C=2 D=258 
00026 [L877] MOV      A=4 B=0 C=0 D=0 
00027 [L877] TGETS    A=3 B=0 C=4 D=4 'reloadData'
00028 [L877] MOV      A=5 B=0 C=2 D=2 
00029 [L877] CALL     A=3 B=1 C=3 D=259 
00030 [L879] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto36 offset=0x45ee source_lines=882-947 params=7
UPVALUES ['CCDirector', 'CCSprite', 'tonumber', 'string', 'math', 'ccp', 'ccc3']
00001 [L883] GGET     A=7 B=0 C=0 D=0 'd_ms'
00002 [L883] TGETS    A=7 B=7 C=1 D=1793 'd_skillUpgradeUI'
00003 [L883] TGETS    A=7 B=7 C=2 D=1794 'initSkillCsv'
00004 [L883] CALL     A=7 B=1 C=1 D=257 
00005 [L884] UGET     A=7 B=0 C=0 D=0 CCDirector
00006 [L884] MOV      A=8 B=0 C=7 D=7 
00007 [L884] TGETS    A=7 B=7 C=3 D=1795 'sharedDirector'
00008 [L884] CALL     A=7 B=2 C=2 D=514 
00009 [L884] MOV      A=8 B=0 C=7 D=7 
00010 [L884] TGETS    A=7 B=7 C=4 D=1796 'getVisibleSize'
00011 [L884] CALL     A=7 B=2 C=2 D=514 
00012 [L885] GGET     A=8 B=0 C=0 D=0 'd_ms'
00013 [L885] TGETS    A=8 B=8 C=1 D=2049 'd_skillUpgradeUI'
00014 [L885] TGETS    A=8 B=8 C=5 D=2053 'g_self'
00015 [L885] TGETS    A=8 B=8 C=6 D=2054 'csv_map_skill'
00016 [L885] TGETV    A=8 B=8 C=1 D=2049 
00017 [L886] KSHORT   A=9 B=0 C=0 D=0 0
00018 [L887] KSHORT   A=10 B=0 C=0 D=0 0
00019 [L888] KPRI     A=11 B=0 C=0 D=0 
00020 [L889] MOV      A=12 B=0 C=3 D=3 
00021 [L891] KPRI     A=13 B=0 C=1 D=1 
00022 [L892] GGET     A=14 B=0 C=0 D=0 'd_ms'
00023 [L892] TGETS    A=14 B=14 C=7 D=3591 'd_wakeUI'
00024 [L892] TGETS    A=14 B=14 C=8 D=3592 'initCsv'
00025 [L892] CALL     A=14 B=1 C=1 D=257 
00026 [L893] ISNEN    A=1 B=0 C=0 D=0 21
00027 [L893] JMP      A=14 B=128 C=31 D=32799 target=59
00028 [L894] UGET     A=14 B=0 C=1 D=1 CCSprite
00029 [L894] MOV      A=15 B=0 C=14 D=14 
00030 [L894] TGETS    A=14 B=14 C=9 D=3593 'create'
00031 [L894] KSTR     A=16 B=0 C=10 D=10 'v2/introUI/xi.png'
00032 [L894] CALL     A=14 B=2 C=3 D=515 
00033 [L894] MOV      A=11 B=0 C=14 D=14 
00034 [L895] GGET     A=14 B=0 C=0 D=0 'd_ms'
00035 [L895] TGETS    A=14 B=14 C=1 D=3585 'd_skillUpgradeUI'
00036 [L895] TGETS    A=14 B=14 C=5 D=3589 'g_self'
00037 [L895] TGETS    A=14 B=14 C=11 D=3595 'csv_map_rulai_skill'
00038 [L895] TGETV    A=14 B=14 C=3 D=3587 
00039 [L895] TGETB    A=10 B=14 C=2 D=3586 
00040 [L896] ISF      A=0 B=0 C=5 D=5 
00041 [L896] JMP      A=14 B=128 C=9 D=32777 target=51
00042 [L897] MULVN    A=14 B=10 C=1 D=2561 
00043 [L897] GGET     A=15 B=0 C=0 D=0 'd_ms'
00044 [L897] TGETS    A=15 B=15 C=12 D=3852 'd_charPositionUI'
00045 [L897] TGETS    A=15 B=15 C=13 D=3853 'g_charPosUI'
00046 [L897] TGETS    A=15 B=15 C=14 D=3854 'current_characterInfo'
00047 [L897] TGETS    A=15 B=15 C=15 D=3855 'magic'
00048 [L897] DIVVN    A=15 B=15 C=2 D=3842 
00049 [L897] ADDVV    A=10 B=14 C=15 D=3599 
00050 [L897] JMP      A=14 B=128 C=104 D=32872 target=155
00051 [L899] GGET     A=14 B=0 C=0 D=0 'd_ms'
00052 [L899] TGETS    A=14 B=14 C=12 D=3596 'd_charPositionUI'
00053 [L899] TGETS    A=14 B=14 C=13 D=3597 'g_charPosUI'
00054 [L899] TGETS    A=14 B=14 C=14 D=3598 'current_characterInfo'
00055 [L899] TGETS    A=14 B=14 C=15 D=3599 'magic'
00056 [L899] DIVVN    A=14 B=14 C=2 D=3586 
00057 [L899] ADDVV    A=10 B=10 C=14 D=2574 
00058 [L900] JMP      A=14 B=128 C=96 D=32864 target=155
00059 [L901] TGETB    A=14 B=8 C=8 D=2056 
00060 [L901] ISNES    A=14 B=0 C=16 D=16 '1'
00061 [L901] JMP      A=14 B=128 C=16 D=32784 target=78
00062 [L902] UGET     A=14 B=0 C=1 D=1 CCSprite
00063 [L902] MOV      A=15 B=0 C=14 D=14 
00064 [L902] TGETS    A=14 B=14 C=9 D=3593 'create'
00065 [L902] KSTR     A=16 B=0 C=17 D=17 'v2/introUI/damage.png'
00066 [L902] CALL     A=14 B=2 C=3 D=515 
00067 [L902] MOV      A=11 B=0 C=14 D=14 
00068 [L903] UGET     A=14 B=0 C=2 D=2 tonumber
00069 [L903] TGETB    A=15 B=8 C=9 D=2057 
00070 [L903] CALL     A=14 B=2 C=2 D=514 
00071 [L903] UGET     A=15 B=0 C=2 D=2 tonumber
00072 [L903] TGETB    A=16 B=8 C=14 D=2062 
00073 [L903] CALL     A=15 B=2 C=2 D=514 
00074 [L903] SUBVN    A=16 B=12 C=3 D=3075 
00075 [L903] MULVV    A=15 B=15 C=16 D=3856 
00076 [L903] ADDVV    A=10 B=14 C=15 D=3599 
00077 [L903] JMP      A=14 B=128 C=77 D=32845 target=155
00078 [L904] TGETB    A=14 B=8 C=8 D=2056 
00079 [L904] ISNES    A=14 B=0 C=18 D=18 '2'
00080 [L904] JMP      A=14 B=128 C=16 D=32784 target=97
00081 [L905] UGET     A=14 B=0 C=1 D=1 CCSprite
00082 [L905] MOV      A=15 B=0 C=14 D=14 
00083 [L905] TGETS    A=14 B=14 C=9 D=3593 'create'
00084 [L905] KSTR     A=16 B=0 C=19 D=19 'v2/introUI/defence.png'
00085 [L905] CALL     A=14 B=2 C=3 D=515 
00086 [L905] MOV      A=11 B=0 C=14 D=14 
00087 [L906] UGET     A=14 B=0 C=2 D=2 tonumber
00088 [L906] TGETB    A=15 B=8 C=10 D=2058 
00089 [L906] CALL     A=14 B=2 C=2 D=514 
00090 [L906] UGET     A=15 B=0 C=2 D=2 tonumber
00091 [L906] TGETB    A=16 B=8 C=14 D=2062 
00092 [L906] CALL     A=15 B=2 C=2 D=514 
00093 [L906] SUBVN    A=16 B=12 C=3 D=3075 
00094 [L906] MULVV    A=15 B=15 C=16 D=3856 
00095 [L906] ADDVV    A=10 B=14 C=15 D=3599 
00096 [L906] JMP      A=14 B=128 C=58 D=32826 target=155
00097 [L907] TGETB    A=14 B=8 C=8 D=2056 
00098 [L907] ISNES    A=14 B=0 C=20 D=20 '3'
00099 [L907] JMP      A=14 B=128 C=16 D=32784 target=116
00100 [L908] UGET     A=14 B=0 C=1 D=1 CCSprite
00101 [L908] MOV      A=15 B=0 C=14 D=14 
00102 [L908] TGETS    A=14 B=14 C=9 D=3593 'create'
00103 [L908] KSTR     A=16 B=0 C=21 D=21 'v2/introUI/mana.png'
00104 [L908] CALL     A=14 B=2 C=3 D=515 
00105 [L908] MOV      A=11 B=0 C=14 D=14 
00106 [L909] UGET     A=14 B=0 C=2 D=2 tonumber
00107 [L909] TGETB    A=15 B=8 C=11 D=2059 
00108 [L909] CALL     A=14 B=2 C=2 D=514 
00109 [L909] UGET     A=15 B=0 C=2 D=2 tonumber
00110 [L909] TGETB    A=16 B=8 C=14 D=2062 
00111 [L909] CALL     A=15 B=2 C=2 D=514 
00112 [L909] SUBVN    A=16 B=12 C=3 D=3075 
00113 [L909] MULVV    A=15 B=15 C=16 D=3856 
00114 [L909] ADDVV    A=10 B=14 C=15 D=3599 
00115 [L909] JMP      A=14 B=128 C=39 D=32807 target=155
00116 [L910] TGETB    A=14 B=8 C=8 D=2056 
00117 [L910] ISNES    A=14 B=0 C=22 D=22 '5'
00118 [L910] JMP      A=14 B=128 C=16 D=32784 target=135
00119 [L911] UGET     A=14 B=0 C=1 D=1 CCSprite
00120 [L911] MOV      A=15 B=0 C=14 D=14 
00121 [L911] TGETS    A=14 B=14 C=9 D=3593 'create'
00122 [L911] KSTR     A=16 B=0 C=23 D=23 'v2/introUI/health.png'
00123 [L911] CALL     A=14 B=2 C=3 D=515 
00124 [L911] MOV      A=11 B=0 C=14 D=14 
00125 [L912] UGET     A=14 B=0 C=2 D=2 tonumber
00126 [L912] TGETB    A=15 B=8 C=13 D=2061 
00127 [L912] CALL     A=14 B=2 C=2 D=514 
00128 [L912] UGET     A=15 B=0 C=2 D=2 tonumber
00129 [L912] TGETB    A=16 B=8 C=14 D=2062 
00130 [L912] CALL     A=15 B=2 C=2 D=514 
00131 [L912] SUBVN    A=16 B=12 C=3 D=3075 
00132 [L912] MULVV    A=15 B=15 C=16 D=3856 
00133 [L912] ADDVV    A=10 B=14 C=15 D=3599 
00134 [L912] JMP      A=14 B=128 C=20 D=32788 target=155
00135 [L914] KPRI     A=13 B=0 C=2 D=2 
00136 [L915] UGET     A=14 B=0 C=1 D=1 CCSprite
00137 [L915] MOV      A=15 B=0 C=14 D=14 
00138 [L915] TGETS    A=14 B=14 C=9 D=3593 'create'
00139 [L915] KSTR     A=16 B=0 C=24 D=24 'v2/introUI/skill_strong.png'
00140 [L915] CALL     A=14 B=2 C=3 D=515 
00141 [L915] MOV      A=11 B=0 C=14 D=14 
00142 [L916] ISF      A=0 B=0 C=6 D=6 
00143 [L916] JMP      A=14 B=128 C=2 D=32770 target=146
00144 [L917] MOV      A=10 B=0 C=6 D=6 
00145 [L917] JMP      A=14 B=128 C=9 D=32777 target=155
00146 [L919] UGET     A=14 B=0 C=2 D=2 tonumber
00147 [L919] TGETB    A=15 B=8 C=12 D=2060 
00148 [L919] CALL     A=14 B=2 C=2 D=514 
00149 [L919] UGET     A=15 B=0 C=2 D=2 tonumber
00150 [L919] TGETB    A=16 B=8 C=14 D=2062 
00151 [L919] CALL     A=15 B=2 C=2 D=514 
00152 [L919] SUBVN    A=16 B=12 C=3 D=3075 
00153 [L919] MULVV    A=15 B=15 C=16 D=3856 
00154 [L919] ADDVV    A=10 B=14 C=15 D=3599 
00155 [L922] ISF      A=0 B=0 C=5 D=5 
00156 [L922] JMP      A=14 B=128 C=12 D=32780 target=169
00157 [L922] IST      A=0 B=0 C=13 D=13 
00158 [L922] JMP      A=14 B=128 C=10 D=32778 target=169
00159 [L922] ISEQN    A=1 B=0 C=0 D=0 21
00160 [L922] JMP      A=14 B=128 C=8 D=32776 target=169
00161 [L923] GGET     A=14 B=0 C=0 D=0 'd_ms'
00162 [L923] TGETS    A=14 B=14 C=7 D=3591 'd_wakeUI'
00163 [L923] TGETS    A=14 B=14 C=25 D=3609 'g_csv'
00164 [L923] TGETS    A=14 B=14 C=26 D=3610 'rate'
00165 [L923] TGETV    A=14 B=14 C=1 D=3585 
00166 [L923] DIVVN    A=14 B=14 C=4 D=3588 
00167 [L923] ADDNV    A=14 B=14 C=3 D=3587 
00168 [L923] MULVV    A=10 B=10 C=14 D=2574 
00169 [L925] ISNEN    A=1 B=0 C=0 D=0 21
00170 [L925] JMP      A=14 B=128 C=10 D=32778 target=181
00171 [L926] UGET     A=14 B=0 C=3 D=3 string
00172 [L926] TGETS    A=14 B=14 C=27 D=3611 'format'
00173 [L926] KSTR     A=15 B=0 C=28 D=28 '%.1f'
00174 [L926] MOV      A=16 B=0 C=10 D=10 
00175 [L926] CALL     A=14 B=2 C=3 D=515 
00176 [L926] MOV      A=10 B=0 C=14 D=14 
00177 [L927] MOV      A=14 B=0 C=10 D=10 
00178 [L927] KSTR     A=15 B=0 C=29 D=29 '%'
00179 [L927] CAT      A=9 B=14 C=15 D=3599 
00180 [L927] JMP      A=14 B=128 C=18 D=32786 target=199
00181 [L928] TGETB    A=14 B=8 C=8 D=2056 
00182 [L928] ISNES    A=14 B=0 C=30 D=30 '4'
00183 [L928] JMP      A=14 B=128 C=6 D=32774 target=190
00184 [L929] UGET     A=14 B=0 C=4 D=4 math
00185 [L929] TGETS    A=14 B=14 C=31 D=3615 'floor'
00186 [L929] MOV      A=15 B=0 C=10 D=10 
00187 [L929] CALL     A=14 B=2 C=2 D=514 
00188 [L929] MOV      A=9 B=0 C=14 D=14 
00189 [L929] JMP      A=14 B=128 C=9 D=32777 target=199
00190 [L931] UGET     A=14 B=0 C=3 D=3 string
00191 [L931] TGETS    A=14 B=14 C=27 D=3611 'format'
00192 [L931] KSTR     A=15 B=0 C=28 D=28 '%.1f'
00193 [L931] MOV      A=16 B=0 C=10 D=10 
00194 [L931] CALL     A=14 B=2 C=3 D=515 
00195 [L931] MOV      A=10 B=0 C=14 D=14 
00196 [L932] MOV      A=14 B=0 C=10 D=10 
00197 [L932] KSTR     A=15 B=0 C=29 D=29 '%'
00198 [L932] CAT      A=9 B=14 C=15 D=3599 
00199 [L935] GGET     A=14 B=0 C=0 D=0 'd_ms'
00200 [L935] TGETS    A=14 B=14 C=32 D=3616 'd_u'
00201 [L935] TGETS    A=14 B=14 C=33 D=3617 'createByStyle'
00202 [L935] TDUP     A=15 B=0 C=34 D=34 {'kind': 'table', 'value': {'font': 'arial', 'fontsize': 26, 'type': 'label'}}
00203 [L935] TSETS    A=9 B=15 C=35 D=3875 'string'
00204 [L935] CALL     A=14 B=2 C=2 D=514 
00205 [L936] MOV      A=16 B=0 C=11 D=11 
00206 [L936] TGETS    A=15 B=11 C=36 D=2852 'setPosition'
00207 [L936] MOV      A=17 B=0 C=2 D=2 
00208 [L936] CALL     A=15 B=1 C=3 D=259 
00209 [L937] MOV      A=16 B=0 C=14 D=14 
00210 [L937] TGETS    A=15 B=14 C=36 D=3620 'setPosition'
00211 [L937] TGETS    A=17 B=2 C=37 D=549 'x'
00212 [L937] TGETS    A=18 B=7 C=38 D=1830 'width'
00213 [L937] MULNV    A=18 B=18 C=5 D=4613 
00214 [L937] ADDVV    A=17 B=17 C=18 D=4370 
00215 [L937] TGETS    A=18 B=2 C=39 D=551 'y'
00216 [L937] CALL     A=15 B=1 C=4 D=260 
00217 [L938] MOV      A=16 B=0 C=14 D=14 
00218 [L938] TGETS    A=15 B=14 C=40 D=3624 'setAnchorPoint'
00219 [L938] UGET     A=17 B=0 C=5 D=5 ccp
00220 [L938] KSHORT   A=18 B=0 C=0 D=0 0
00221 [L938] KNUM     A=19 B=0 C=6 D=6 0.5
00222 [L938] CALL     A=17 B=0 C=3 D=3 
00223 [L938] CALLM    A=15 B=1 C=1 D=257 
00224 [L939] ISF      A=0 B=0 C=4 D=4 
00225 [L939] JMP      A=15 B=128 C=8 D=32776 target=234
00226 [L940] MOV      A=16 B=0 C=14 D=14 
00227 [L940] TGETS    A=15 B=14 C=41 D=3625 'setColor'
00228 [L940] UGET     A=17 B=0 C=6 D=6 ccc3
00229 [L940] TGETB    A=18 B=4 C=1 D=1025 
00230 [L940] TGETB    A=19 B=4 C=2 D=1026 
00231 [L940] TGETB    A=20 B=4 C=3 D=1027 
00232 [L940] CALL     A=17 B=0 C=4 D=4 
00233 [L940] CALLM    A=15 B=1 C=1 D=257 
00234 [L943] MOV      A=16 B=0 C=0 D=0 
00235 [L943] TGETS    A=15 B=0 C=42 D=42 'addChild'
00236 [L943] MOV      A=17 B=0 C=11 D=11 
00237 [L943] KSHORT   A=18 B=0 C=5 D=5 5
00238 [L943] CALL     A=15 B=1 C=4 D=260 
00239 [L944] MOV      A=16 B=0 C=0 D=0 
00240 [L944] TGETS    A=15 B=0 C=42 D=42 'addChild'
00241 [L944] MOV      A=17 B=0 C=14 D=14 
00242 [L944] KSHORT   A=18 B=0 C=5 D=5 5
00243 [L944] CALL     A=15 B=1 C=4 D=260 
00244 [L946] RET1     A=14 B=0 C=2 D=2 

FUNCTION proto37 offset=0x4db2 source_lines=949-993 params=1
UPVALUES ['table', 'o_t']
00001 [L956] TNEW     A=1 B=0 C=0 D=0 
00002 [L957] KSHORT   A=2 B=0 C=1 D=1 1
00003 [L957] TGETS    A=3 B=0 C=0 D=0 'object_list'
00004 [L957] LEN      A=3 B=0 C=3 D=3 
00005 [L957] KSHORT   A=4 B=0 C=1 D=1 1
00006 [L957] FORI     A=2 B=128 C=31 D=32799 target=38
00007 [L958] KSHORT   A=6 B=0 C=1 D=1 1
00008 [L958] GGET     A=7 B=0 C=1 D=1 'g_packageItemsInfo'
00009 [L958] LEN      A=7 B=0 C=7 D=7 
00010 [L958] KSHORT   A=8 B=0 C=1 D=1 1
00011 [L958] FORI     A=6 B=128 C=25 D=32793 target=37
00012 [L959] TGETS    A=10 B=0 C=0 D=0 'object_list'
00013 [L959] TGETV    A=10 B=10 C=5 D=2565 
00014 [L959] GGET     A=11 B=0 C=1 D=1 'g_packageItemsInfo'
00015 [L959] TGETV    A=11 B=11 C=9 D=2825 
00016 [L959] TGETS    A=11 B=11 C=2 D=2818 'id'
00017 [L959] ISNEV    A=10 B=0 C=11 D=11 
00018 [L959] JMP      A=10 B=128 C=17 D=32785 target=36
00019 [L960] GGET     A=10 B=0 C=1 D=1 'g_packageItemsInfo'
00020 [L960] TGETV    A=10 B=10 C=9 D=2569 
00021 [L960] TGETS    A=10 B=10 C=3 D=2563 'attach_type'
00022 [L960] TGETS    A=11 B=0 C=4 D=4 'obj_type'
00023 [L960] ISNEV    A=10 B=0 C=11 D=11 
00024 [L960] JMP      A=10 B=128 C=11 D=32779 target=36
00025 [L961] LEN      A=10 B=0 C=1 D=1 
00026 [L961] ADDVN    A=10 B=10 C=0 D=2560 
00027 [L961] GGET     A=11 B=0 C=1 D=1 'g_packageItemsInfo'
00028 [L961] TGETV    A=11 B=11 C=9 D=2825 
00029 [L961] TSETV    A=11 B=1 C=10 D=266 
00030 [L962] UGET     A=10 B=0 C=0 D=0 table
00031 [L962] TGETS    A=10 B=10 C=5 D=2565 'remove'
00032 [L962] GGET     A=11 B=0 C=1 D=1 'g_packageItemsInfo'
00033 [L962] MOV      A=12 B=0 C=9 D=9 
00034 [L962] CALL     A=10 B=1 C=3 D=259 
00035 [L963] JMP      A=6 B=128 C=1 D=32769 target=37
00036 [L958] FORL     A=6 B=127 C=231 D=32743 target=12
00037 [L957] FORL     A=2 B=127 C=225 D=32737 target=7
00038 [L968] ISF      A=0 B=0 C=1 D=1 
00039 [L968] JMP      A=2 B=128 C=49 D=32817 target=89
00040 [L968] LEN      A=2 B=0 C=1 D=1 
00041 [L968] KSHORT   A=3 B=0 C=0 D=0 0
00042 [L968] ISGE     A=3 B=0 C=2 D=2 
00043 [L968] JMP      A=2 B=128 C=45 D=32813 target=89
00044 [L969] KSHORT   A=2 B=0 C=1 D=1 1
00045 [L969] LEN      A=3 B=0 C=1 D=1 
00046 [L969] KSHORT   A=4 B=0 C=1 D=1 1
00047 [L969] FORI     A=2 B=128 C=41 D=32809 target=89
00048 [L970] TGETV    A=6 B=1 C=5 D=261 
00049 [L971] TGETS    A=7 B=6 C=3 D=1539 'attach_type'
00050 [L972] TGETS    A=8 B=6 C=6 D=1542 'type_id'
00051 [L973] KPRI     A=9 B=0 C=0 D=0 
00052 [L974] UGET     A=10 B=0 C=1 D=1 o_t
00053 [L974] TGETS    A=10 B=10 C=7 D=2567 'item'
00054 [L974] ISNEV    A=7 B=0 C=10 D=10 
00055 [L974] JMP      A=10 B=128 C=8 D=32776 target=64
00056 [L975] TGETS    A=10 B=6 C=8 D=1544 'csvInfo'
00057 [L975] TGETS    A=10 B=10 C=9 D=2569 'mainType'
00058 [L976] ISF      A=0 B=0 C=10 D=10 
00059 [L976] JMP      A=11 B=128 C=10 D=32778 target=70
00060 [L977] GGET     A=11 B=0 C=10 D=10 'g_reorgItemsInfo'
00061 [L977] TGETV    A=11 B=11 C=7 D=2823 
00062 [L977] TGETV    A=9 B=11 C=10 D=2826 
00063 [L978] JMP      A=10 B=128 C=6 D=32774 target=70
00064 [L979] UGET     A=10 B=0 C=1 D=1 o_t
00065 [L979] TGETS    A=10 B=10 C=11 D=2571 'skill'
00066 [L979] ISNEV    A=7 B=0 C=10 D=10 
00067 [L979] JMP      A=10 B=128 C=2 D=32770 target=70
00068 [L980] GGET     A=10 B=0 C=10 D=10 'g_reorgItemsInfo'
00069 [L980] TGETV    A=9 B=10 C=7 D=2567 
00070 [L983] ISF      A=0 B=0 C=9 D=9 
00071 [L983] JMP      A=10 B=128 C=16 D=32784 target=88
00072 [L984] KSHORT   A=10 B=0 C=1 D=1 1
00073 [L984] LEN      A=11 B=0 C=9 D=9 
00074 [L984] KSHORT   A=12 B=0 C=1 D=1 1
00075 [L984] FORI     A=10 B=128 C=12 D=32780 target=88
00076 [L985] TGETS    A=14 B=6 C=2 D=1538 'id'
00077 [L985] TGETV    A=15 B=9 C=13 D=2317 
00078 [L985] TGETS    A=15 B=15 C=2 D=3842 'id'
00079 [L985] ISNEV    A=14 B=0 C=15 D=15 
00080 [L985] JMP      A=14 B=128 C=6 D=32774 target=87
00081 [L986] UGET     A=14 B=0 C=0 D=0 table
00082 [L986] TGETS    A=14 B=14 C=5 D=3589 'remove'
00083 [L986] MOV      A=15 B=0 C=9 D=9 
00084 [L986] MOV      A=16 B=0 C=13 D=13 
00085 [L986] CALL     A=14 B=1 C=3 D=259 
00086 [L987] JMP      A=10 B=128 C=1 D=32769 target=88
00087 [L984] FORL     A=10 B=127 C=244 D=32756 target=76
00088 [L969] FORL     A=2 B=127 C=215 D=32727 target=48
00089 [L993] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto38 offset=0x508e source_lines=1005-1011 params=0
UPVALUES ['item']
00001 [L1006] TDUP     A=0 B=0 C=1 D=1 {'kind': 'table', 'value': {}}
00002 [L1007] UGET     A=1 B=0 C=0 D=0 item
00003 [L1007] TGETS    A=1 B=1 C=0 D=256 'id'
00004 [L1007] TSETS    A=1 B=0 C=2 D=2 'des_id'
00005 [L1008] UGET     A=1 B=0 C=0 D=0 item
00006 [L1008] TGETS    A=1 B=1 C=3 D=259 'is_lock'
00007 [L1008] ISNEN    A=1 B=0 C=0 D=0 1
00008 [L1008] JMP      A=1 B=128 C=2 D=32770 target=11
00009 [L1008] KSHORT   A=1 B=0 C=2 D=2 2
00010 [L1008] JMP      A=2 B=128 C=1 D=32769 target=12
00011 [L1008] KSHORT   A=1 B=0 C=1 D=1 1
00012 [L1008] TSETS    A=1 B=0 C=4 D=4 'flag'
00013 [L1010] GGET     A=1 B=0 C=5 D=5 'd_ms'
00014 [L1010] TGETS    A=1 B=1 C=6 D=262 'd_u'
00015 [L1010] TGETS    A=1 B=1 C=7 D=263 'main_server_send_msg'
00016 [L1010] GGET     A=2 B=0 C=5 D=5 'd_ms'
00017 [L1010] TGETS    A=2 B=2 C=8 D=520 'd_msg_def'
00018 [L1010] TGETS    A=2 B=2 C=9 D=521 'gscl_msg_id'
00019 [L1010] TGETS    A=2 B=2 C=10 D=522 'msg_lock_item'
00020 [L1010] MOV      A=3 B=0 C=0 D=0 
00021 [L1010] CALL     A=1 B=1 C=3 D=259 
00022 [L1011] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto39 offset=0x5180 source_lines=995-1020 params=3
UPVALUES []
00001 [L996] ISTC     A=3 B=0 C=0 D=0 
00002 [L996] JMP      A=3 B=128 C=2 D=32770 target=5
00003 [L996] GGET     A=3 B=0 C=0 D=0 'g_packageUI'
00004 [L996] TGETS    A=3 B=3 C=1 D=769 'itemIntroLayer'
00005 [L997] ISTC     A=4 B=0 C=1 D=1 
00006 [L997] JMP      A=4 B=128 C=2 D=32770 target=9
00007 [L997] GGET     A=4 B=0 C=0 D=0 'g_packageUI'
00008 [L997] TGETS    A=4 B=4 C=2 D=1026 'last_show_item'
00009 [L998] ISF      A=0 B=0 C=3 D=3 
00010 [L998] JMP      A=5 B=128 C=2 D=32770 target=13
00011 [L998] IST      A=0 B=0 C=4 D=4 
00012 [L998] JMP      A=5 B=128 C=1 D=32769 target=14
00013 [L999] UCLO     A=0 B=128 C=67 D=32835 target=81
00014 [L1001] GGET     A=5 B=0 C=3 D=3 'd_ms'
00015 [L1001] TGETS    A=5 B=5 C=4 D=1284 'd_u'
00016 [L1001] TGETS    A=5 B=5 C=5 D=1285 'clearLayer'
00017 [L1001] GGET     A=6 B=0 C=0 D=0 'g_packageUI'
00018 [L1001] TGETS    A=6 B=6 C=1 D=1537 'itemIntroLayer'
00019 [L1001] KSHORT   A=7 B=0 C=10 D=10 10
00020 [L1001] KSHORT   A=8 B=4 C=210 D=1234 1234
00021 [L1001] CALL     A=5 B=2 C=4 D=516 
00022 [L1002] GGET     A=6 B=0 C=3 D=3 'd_ms'
00023 [L1002] TGETS    A=6 B=6 C=6 D=1542 'd_wakeUI'
00024 [L1002] TGETS    A=6 B=6 C=7 D=1543 'getStarSprite'
00025 [L1002] TGETS    A=7 B=4 C=8 D=1032 'type_id'
00026 [L1002] TGETS    A=8 B=4 C=9 D=1033 'level'
00027 [L1002] IST      A=0 B=0 C=8 D=8 
00028 [L1002] JMP      A=9 B=128 C=1 D=32769 target=30
00029 [L1002] KSHORT   A=8 B=0 C=1 D=1 1
00030 [L1002] KPRI     A=9 B=0 C=0 D=0 
00031 [L1002] TGETS    A=10 B=4 C=10 D=1034 'is_lock'
00032 [L1002] ISEQN    A=10 B=0 C=0 D=0 1
00033 [L1002] JMP      A=10 B=128 C=2 D=32770 target=36
00034 [L1002] KPRI     A=10 B=0 C=1 D=1 
00035 [L1002] JMP      A=11 B=128 C=1 D=32769 target=37
00036 [L1002] KPRI     A=10 B=0 C=2 D=2 
00037 [L1002] CALL     A=6 B=2 C=5 D=517 
00038 [L1003] MOV      A=8 B=0 C=5 D=5 
00039 [L1003] TGETS    A=7 B=5 C=11 D=1291 'addChild'
00040 [L1003] GGET     A=9 B=0 C=3 D=3 'd_ms'
00041 [L1003] TGETS    A=9 B=9 C=4 D=2308 'd_u'
00042 [L1003] TGETS    A=9 B=9 C=12 D=2316 'setStyles'
00043 [L1003] MOV      A=10 B=0 C=6 D=6 
00044 [L1003] TDUP     A=11 B=0 C=13 D=13 {'kind': 'table', 'value': {'scale': 0.18, 'x': 0.36, 'y': 0.68}}
00045 [L1003] CALL     A=9 B=0 C=3 D=3 
00046 [L1003] CALLM    A=7 B=1 C=1 D=257 
00047 [L1004] ISF      A=0 B=0 C=2 D=2 
00048 [L1004] JMP      A=7 B=128 C=30 D=32798 target=79
00049 [L1011] FNEW     A=7 B=0 C=14 D=14 {'kind': 'proto', 'id': 38}
00050 [L1012] TGETS    A=8 B=4 C=10 D=1034 'is_lock'
00051 [L1012] ISNEN    A=8 B=0 C=0 D=0 1
00052 [L1012] JMP      A=8 B=128 C=2 D=32770 target=55
00053 [L1012] KSTR     A=8 B=0 C=15 D=15 'ulock'
00054 [L1012] JMP      A=9 B=128 C=1 D=32769 target=56
00055 [L1012] KSTR     A=8 B=0 C=16 D=16 'alock'
00056 [L1013] TDUP     A=9 B=0 C=17 D=17 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00057 [L1015] TDUP     A=10 B=0 C=18 D=18 {'kind': 'table', 'value': {'y': 0.22, 'x': 0.5}}
00058 [L1016] KSTR     A=11 B=0 C=19 D=19 'v2/wakeUI/'
00059 [L1016] MOV      A=12 B=0 C=8 D=8 
00060 [L1016] KSTR     A=13 B=0 C=20 D=20 '1.png'
00061 [L1016] CAT      A=11 B=11 C=13 D=2829 
00062 [L1016] TSETS    A=11 B=10 C=21 D=2581 'npic'
00063 [L1016] KSTR     A=11 B=0 C=19 D=19 'v2/wakeUI/'
00064 [L1016] MOV      A=12 B=0 C=8 D=8 
00065 [L1016] KSTR     A=13 B=0 C=22 D=22 '2.png'
00066 [L1016] CAT      A=11 B=11 C=13 D=2829 
00067 [L1016] TSETS    A=11 B=10 C=23 D=2583 'spic'
00068 [L1016] TSETS    A=7 B=10 C=24 D=2584 'call_back'
00069 [L1016] TSETB    A=10 B=9 C=1 D=2305 
00070 [L1018] MOV      A=11 B=0 C=5 D=5 
00071 [L1018] TGETS    A=10 B=5 C=11 D=1291 'addChild'
00072 [L1018] GGET     A=12 B=0 C=3 D=3 'd_ms'
00073 [L1018] TGETS    A=12 B=12 C=4 D=3076 'd_u'
00074 [L1018] TGETS    A=12 B=12 C=25 D=3097 'createMenu'
00075 [L1018] MOV      A=13 B=0 C=9 D=9 
00076 [L1018] CALL     A=12 B=2 C=2 D=514 
00077 [L1018] KSHORT   A=13 B=0 C=1 D=1 1
00078 [L1018] CALL     A=10 B=1 C=4 D=260 
00079 [L1020] UCLO     A=0 B=128 C=0 D=32768 target=80
00080 [L1020] RET0     A=0 B=0 C=1 D=1 
00081 [L1020] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto40 offset=0x5498 source_lines=1034-1041 params=0
UPVALUES ['introLayer', 'closeCallBack']
00001 [L1035] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L1035] TGETS    A=0 B=0 C=1 D=1 'd_u'
00003 [L1035] TGETS    A=0 B=0 C=2 D=2 'remove'
00004 [L1035] UGET     A=1 B=0 C=0 D=0 introLayer
00005 [L1035] CALL     A=0 B=1 C=2 D=258 
00006 [L1036] USETP    A=0 B=0 C=0 D=0 introLayer
00007 [L1037] UGET     A=0 B=0 C=1 D=1 closeCallBack
00008 [L1037] ISF      A=0 B=0 C=0 D=0 
00009 [L1037] JMP      A=1 B=128 C=2 D=32770 target=12
00010 [L1038] UGET     A=0 B=0 C=1 D=1 closeCallBack
00011 [L1038] CALL     A=0 B=1 C=1 D=257 
00012 [L1040] KPRI     A=0 B=0 C=2 D=2 
00013 [L1040] RET1     A=0 B=0 C=2 D=2 

FUNCTION proto41 offset=0x5514 source_lines=1095-1129 params=0
UPVALUES ['itemInfo', 'isAsc', 'packageTag', 'CCSprite', 'CCPointMake', 'CCRectMake']
00001 [L1097] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L1097] TGETS    A=0 B=0 C=1 D=1 'd_data'
00003 [L1097] TGETS    A=0 B=0 C=2 D=2 'getCertainSmallSprite'
00004 [L1097] UGET     A=1 B=0 C=0 D=0 itemInfo
00005 [L1097] TGETS    A=1 B=1 C=3 D=259 'attach_type'
00006 [L1097] UGET     A=2 B=0 C=0 D=0 itemInfo
00007 [L1097] TGETS    A=2 B=2 C=4 D=516 'type_id'
00008 [L1097] IST      A=0 B=0 C=2 D=2 
00009 [L1097] JMP      A=3 B=128 C=3 D=32771 target=13
00010 [L1097] UGET     A=2 B=0 C=0 D=0 itemInfo
00011 [L1097] TGETS    A=2 B=2 C=5 D=517 'buyInfo'
00012 [L1097] TGETS    A=2 B=2 C=4 D=516 'type_id'
00013 [L1097] UGET     A=3 B=0 C=0 D=0 itemInfo
00014 [L1097] TGETS    A=3 B=3 C=6 D=774 'level'
00015 [L1097] IST      A=0 B=0 C=3 D=3 
00016 [L1097] JMP      A=4 B=128 C=1 D=32769 target=18
00017 [L1097] KSHORT   A=3 B=0 C=1 D=1 1
00018 [L1097] UGET     A=4 B=0 C=1 D=1 isAsc
00019 [L1097] UGET     A=5 B=0 C=0 D=0 itemInfo
00020 [L1097] TGETS    A=5 B=5 C=7 D=1287 'star_level'
00021 [L1097] CALL     A=0 B=2 C=6 D=518 
00022 [L1099] UGET     A=1 B=0 C=2 D=2 packageTag
00023 [L1099] GGET     A=2 B=0 C=8 D=8 'packageTagDef'
00024 [L1099] TGETS    A=2 B=2 C=9 D=521 'props'
00025 [L1099] ISEQV    A=1 B=0 C=2 D=2 
00026 [L1099] JMP      A=1 B=128 C=130 D=32898 target=157
00027 [L1099] UGET     A=1 B=0 C=2 D=2 packageTag
00028 [L1099] GGET     A=2 B=0 C=8 D=8 'packageTagDef'
00029 [L1099] TGETS    A=2 B=2 C=10 D=522 'stone'
00030 [L1099] ISEQV    A=1 B=0 C=2 D=2 
00031 [L1099] JMP      A=1 B=128 C=125 D=32893 target=157
00032 [L1100] MOV      A=2 B=0 C=0 D=0 
00033 [L1100] TGETS    A=1 B=0 C=11 D=11 'getContentSize'
00034 [L1100] CALL     A=1 B=2 C=2 D=514 
00035 [L1101] UGET     A=2 B=0 C=0 D=0 itemInfo
00036 [L1101] TGETS    A=2 B=2 C=12 D=524 'csvInfo'
00037 [L1101] TGETS    A=2 B=2 C=13 D=525 'quality'
00038 [L1102] UGET     A=3 B=0 C=0 D=0 itemInfo
00039 [L1102] TGETS    A=3 B=3 C=7 D=775 'star_level'
00040 [L1102] ISNEN    A=3 B=0 C=0 D=0 1
00041 [L1102] JMP      A=3 B=128 C=30 D=32798 target=72
00042 [L1103] UGET     A=3 B=0 C=3 D=3 CCSprite
00043 [L1103] MOV      A=4 B=0 C=3 D=3 
00044 [L1103] TGETS    A=3 B=3 C=14 D=782 'create'
00045 [L1103] KSTR     A=5 B=0 C=15 D=15 'v2/shengxing/sixstar.png'
00046 [L1103] CALL     A=3 B=2 C=3 D=515 
00047 [L1104] GGET     A=4 B=0 C=0 D=0 'd_ms'
00048 [L1104] TGETS    A=4 B=4 C=16 D=1040 'd_u'
00049 [L1104] TGETS    A=4 B=4 C=17 D=1041 'setStyles'
00050 [L1104] MOV      A=5 B=0 C=3 D=3 
00051 [L1104] TDUP     A=6 B=0 C=18 D=18 {'kind': 'table', 'value': {'scale': 0.06}}
00052 [L1104] CALL     A=4 B=1 C=3 D=259 
00053 [L1105] MOV      A=5 B=0 C=3 D=3 
00054 [L1105] TGETS    A=4 B=3 C=19 D=787 'setPosition'
00055 [L1105] TGETS    A=6 B=1 C=20 D=276 'width'
00056 [L1105] MULNV    A=6 B=6 C=1 D=1537 
00057 [L1105] TGETS    A=7 B=1 C=21 D=277 'height'
00058 [L1105] MULNV    A=7 B=7 C=1 D=1793 
00059 [L1105] CALL     A=4 B=1 C=4 D=260 
00060 [L1106] MOV      A=5 B=0 C=3 D=3 
00061 [L1106] TGETS    A=4 B=3 C=22 D=790 'setAnchorPoint'
00062 [L1106] UGET     A=6 B=0 C=4 D=4 CCPointMake
00063 [L1106] KSHORT   A=7 B=0 C=0 D=0 0
00064 [L1106] KSHORT   A=8 B=0 C=0 D=0 0
00065 [L1106] CALL     A=6 B=0 C=3 D=3 
00066 [L1106] CALLM    A=4 B=1 C=1 D=257 
00067 [L1107] MOV      A=5 B=0 C=0 D=0 
00068 [L1107] TGETS    A=4 B=0 C=23 D=23 'addChild'
00069 [L1107] MOV      A=6 B=0 C=3 D=3 
00070 [L1107] CALL     A=4 B=1 C=3 D=259 
00071 [L1107] JMP      A=3 B=128 C=85 D=32853 target=157
00072 [L1109] UGET     A=3 B=0 C=3 D=3 CCSprite
00073 [L1109] MOV      A=4 B=0 C=3 D=3 
00074 [L1109] TGETS    A=3 B=3 C=14 D=782 'create'
00075 [L1109] KSTR     A=5 B=0 C=24 D=24 'v2/newIntroUI/star_bkg.png'
00076 [L1109] CALL     A=3 B=2 C=3 D=515 
00077 [L1110] MOV      A=5 B=0 C=3 D=3 
00078 [L1110] TGETS    A=4 B=3 C=11 D=779 'getContentSize'
00079 [L1110] CALL     A=4 B=2 C=2 D=514 
00080 [L1111] MOV      A=6 B=0 C=3 D=3 
00081 [L1111] TGETS    A=5 B=3 C=19 D=787 'setPosition'
00082 [L1111] TGETS    A=7 B=1 C=20 D=276 'width'
00083 [L1111] MULNV    A=7 B=7 C=1 D=1793 
00084 [L1111] TGETS    A=8 B=1 C=21 D=277 'height'
00085 [L1111] MULNV    A=8 B=8 C=1 D=2049 
00086 [L1111] CALL     A=5 B=1 C=4 D=260 
00087 [L1112] MOV      A=6 B=0 C=3 D=3 
00088 [L1112] TGETS    A=5 B=3 C=22 D=790 'setAnchorPoint'
00089 [L1112] UGET     A=7 B=0 C=4 D=4 CCPointMake
00090 [L1112] KSHORT   A=8 B=0 C=0 D=0 0
00091 [L1112] KSHORT   A=9 B=0 C=0 D=0 0
00092 [L1112] CALL     A=7 B=0 C=3 D=3 
00093 [L1112] CALLM    A=5 B=1 C=1 D=257 
00094 [L1113] MOV      A=6 B=0 C=3 D=3 
00095 [L1113] TGETS    A=5 B=3 C=25 D=793 'setScale'
00096 [L1113] TGETS    A=7 B=1 C=20 D=276 'width'
00097 [L1113] MULNV    A=7 B=7 C=2 D=1794 
00098 [L1113] TGETS    A=8 B=4 C=20 D=1044 'width'
00099 [L1113] DIVVV    A=7 B=7 C=8 D=1800 
00100 [L1113] CALL     A=5 B=1 C=3 D=259 
00101 [L1114] MOV      A=6 B=0 C=0 D=0 
00102 [L1114] TGETS    A=5 B=0 C=23 D=23 'addChild'
00103 [L1114] MOV      A=7 B=0 C=3 D=3 
00104 [L1114] CALL     A=5 B=1 C=3 D=259 
00105 [L1115] ISF      A=0 B=0 C=2 D=2 
00106 [L1115] JMP      A=5 B=128 C=50 D=32818 target=157
00107 [L1115] KSHORT   A=5 B=0 C=0 D=0 0
00108 [L1115] ISGE     A=5 B=0 C=2 D=2 
00109 [L1115] JMP      A=5 B=128 C=47 D=32815 target=157
00110 [L1116] UGET     A=5 B=0 C=0 D=0 itemInfo
00111 [L1116] TGETS    A=5 B=5 C=12 D=1292 'csvInfo'
00112 [L1116] TGETS    A=5 B=5 C=13 D=1293 'quality'
00113 [L1116] DIVVN    A=5 B=5 C=3 D=1283 
00114 [L1117] UGET     A=6 B=0 C=3 D=3 CCSprite
00115 [L1117] MOV      A=7 B=0 C=6 D=6 
00116 [L1117] TGETS    A=6 B=6 C=14 D=1550 'create'
00117 [L1117] KSTR     A=8 B=0 C=26 D=26 'v2/introUI/stars.png'
00118 [L1117] CALL     A=6 B=2 C=3 D=515 
00119 [L1118] MOV      A=8 B=0 C=6 D=6 
00120 [L1118] TGETS    A=7 B=6 C=11 D=1547 'getContentSize'
00121 [L1118] CALL     A=7 B=2 C=2 D=514 
00122 [L1119] MOV      A=9 B=0 C=6 D=6 
00123 [L1119] TGETS    A=8 B=6 C=27 D=1563 'setTextureRect'
00124 [L1119] UGET     A=10 B=0 C=5 D=5 CCRectMake
00125 [L1119] KSHORT   A=11 B=0 C=0 D=0 0
00126 [L1119] KSHORT   A=12 B=0 C=0 D=0 0
00127 [L1119] TGETS    A=13 B=7 C=20 D=1812 'width'
00128 [L1119] MULVV    A=13 B=13 C=5 D=3333 
00129 [L1119] TGETS    A=14 B=7 C=21 D=1813 'height'
00130 [L1119] CALL     A=10 B=0 C=5 D=5 
00131 [L1119] CALLM    A=8 B=1 C=1 D=257 
00132 [L1121] MOV      A=9 B=0 C=6 D=6 
00133 [L1121] TGETS    A=8 B=6 C=19 D=1555 'setPosition'
00134 [L1121] TGETS    A=10 B=1 C=20 D=276 'width'
00135 [L1121] MULNV    A=10 B=10 C=1 D=2561 
00136 [L1121] TGETS    A=11 B=1 C=21 D=277 'height'
00137 [L1121] MULNV    A=11 B=11 C=1 D=2817 
00138 [L1121] CALL     A=8 B=1 C=4 D=260 
00139 [L1122] MOV      A=9 B=0 C=6 D=6 
00140 [L1122] TGETS    A=8 B=6 C=22 D=1558 'setAnchorPoint'
00141 [L1122] UGET     A=10 B=0 C=4 D=4 CCPointMake
00142 [L1122] KSHORT   A=11 B=0 C=0 D=0 0
00143 [L1122] KSHORT   A=12 B=0 C=0 D=0 0
00144 [L1122] CALL     A=10 B=0 C=3 D=3 
00145 [L1122] CALLM    A=8 B=1 C=1 D=257 
00146 [L1123] MOV      A=9 B=0 C=6 D=6 
00147 [L1123] TGETS    A=8 B=6 C=25 D=1561 'setScale'
00148 [L1123] TGETS    A=10 B=1 C=20 D=276 'width'
00149 [L1123] MULNV    A=10 B=10 C=2 D=2562 
00150 [L1123] TGETS    A=11 B=7 C=20 D=1812 'width'
00151 [L1123] DIVVV    A=10 B=10 C=11 D=2571 
00152 [L1123] CALL     A=8 B=1 C=3 D=259 
00153 [L1124] MOV      A=9 B=0 C=0 D=0 
00154 [L1124] TGETS    A=8 B=0 C=23 D=23 'addChild'
00155 [L1124] MOV      A=10 B=0 C=6 D=6 
00156 [L1124] CALL     A=8 B=1 C=3 D=259 
00157 [L1128] RET1     A=0 B=0 C=2 D=2 

FUNCTION proto42 offset=0x5a46 source_lines=1442-1460 params=0
UPVALUES ['itemInfo', 'gethz', 'introLayer']
00001 [L1443] UGET     A=0 B=0 C=0 D=0 itemInfo
00002 [L1443] TGETS    A=0 B=0 C=0 D=0 'star_level'
00003 [L1444] GGET     A=1 B=0 C=1 D=1 'd_ms'
00004 [L1444] TGETS    A=1 B=1 C=2 D=258 'd_mainUI'
00005 [L1444] TGETS    A=1 B=1 C=3 D=259 'g_playerInfo'
00006 [L1444] TGETS    A=1 B=1 C=4 D=260 'reborn_layer'
00007 [L1444] IST      A=0 B=0 C=1 D=1 
00008 [L1444] JMP      A=2 B=128 C=1 D=32769 target=10
00009 [L1444] KSHORT   A=1 B=0 C=0 D=0 0
00010 [L1445] KSHORT   A=2 B=0 C=4 D=4 4
00011 [L1445] ISGE     A=1 B=0 C=2 D=2 
00012 [L1445] JMP      A=2 B=128 C=8 D=32776 target=21
00013 [L1446] GGET     A=2 B=0 C=1 D=1 'd_ms'
00014 [L1446] TGETS    A=2 B=2 C=5 D=517 'd_info'
00015 [L1446] TGETS    A=2 B=2 C=6 D=518 'show'
00016 [L1446] UGET     A=3 B=0 C=1 D=1 gethz
00017 [L1446] KSTR     A=4 B=0 C=7 D=7 'asc30'
00018 [L1446] CALL     A=3 B=0 C=2 D=2 
00019 [L1446] CALLM    A=2 B=1 C=0 D=256 
00020 [L1447] RET0     A=0 B=0 C=1 D=1 
00021 [L1449] ISNEN    A=0 B=0 C=0 D=0 1
00022 [L1449] JMP      A=2 B=128 C=10 D=32778 target=33
00023 [L1450] GGET     A=2 B=0 C=1 D=1 'd_ms'
00024 [L1450] TGETS    A=2 B=2 C=5 D=517 'd_info'
00025 [L1450] TGETS    A=2 B=2 C=6 D=518 'show'
00026 [L1450] GGET     A=3 B=0 C=1 D=1 'd_ms'
00027 [L1450] TGETS    A=3 B=3 C=8 D=776 'd_hz'
00028 [L1450] TGETS    A=3 B=3 C=9 D=777 'gethz'
00029 [L1450] KSTR     A=4 B=0 C=10 D=10 'shengxing5'
00030 [L1450] CALL     A=3 B=0 C=2 D=2 
00031 [L1450] CALLM    A=2 B=1 C=0 D=256 
00032 [L1451] RET0     A=0 B=0 C=1 D=1 
00033 [L1453] TNEW     A=2 B=0 C=0 D=0 
00034 [L1454] UGET     A=3 B=0 C=0 D=0 itemInfo
00035 [L1454] TSETS    A=3 B=2 C=11 D=523 'skill_info'
00036 [L1455] KSHORT   A=3 B=0 C=120 D=120 120
00037 [L1455] TSETS    A=3 B=2 C=12 D=524 'from_btn'
00038 [L1456] UGET     A=3 B=0 C=2 D=2 introLayer
00039 [L1456] TGETS    A=3 B=3 C=14 D=782 'parent'
00040 [L1456] TSETS    A=3 B=2 C=13 D=525 'parent_layer'
00041 [L1457] KPRI     A=3 B=0 C=2 D=2 
00042 [L1457] TSETS    A=3 B=2 C=15 D=527 'isNeedUpdate'
00043 [L1458] GGET     A=3 B=0 C=1 D=1 'd_ms'
00044 [L1458] TGETS    A=3 B=3 C=16 D=784 'd_skillUpgradeUI'
00045 [L1458] TGETS    A=3 B=3 C=17 D=785 'create_wshengxing'
00046 [L1458] MOV      A=4 B=0 C=2 D=2 
00047 [L1458] CALL     A=3 B=1 C=2 D=258 
00048 [L1459] GGET     A=3 B=0 C=18 D=18 'closeAndRemoveIntroLayer'
00049 [L1459] CALL     A=3 B=1 C=1 D=257 
00050 [L1460] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto43 offset=0x5c5e source_lines=1640-1663 params=2
UPVALUES ['CCSprite', 'contentNode', 'CCPointMake']
00001 [L1641] UGET     A=2 B=0 C=0 D=0 CCSprite
00002 [L1641] MOV      A=3 B=0 C=2 D=2 
00003 [L1641] TGETS    A=2 B=2 C=0 D=512 'create'
00004 [L1641] KSTR     A=4 B=0 C=1 D=1 'v2/newIntroUI/big_bkg1.png'
00005 [L1641] CALL     A=2 B=2 C=3 D=515 
00006 [L1642] MOV      A=4 B=0 C=2 D=2 
00007 [L1642] TGETS    A=3 B=2 C=2 D=514 'getContentSize'
00008 [L1642] CALL     A=3 B=2 C=2 D=514 
00009 [L1643] UGET     A=4 B=0 C=1 D=1 contentNode
00010 [L1643] MOV      A=5 B=0 C=4 D=4 
00011 [L1643] TGETS    A=4 B=4 C=3 D=1027 'addChild'
00012 [L1643] MOV      A=6 B=0 C=2 D=2 
00013 [L1643] KSHORT   A=7 B=255 C=251 D=65531 -5
00014 [L1643] CALL     A=4 B=1 C=4 D=260 
00015 [L1645] UGET     A=4 B=0 C=0 D=0 CCSprite
00016 [L1645] MOV      A=5 B=0 C=4 D=4 
00017 [L1645] TGETS    A=4 B=4 C=0 D=1024 'create'
00018 [L1645] KSTR     A=6 B=0 C=4 D=4 'v2/newIntroUI/big_bkg2.png'
00019 [L1645] CALL     A=4 B=2 C=3 D=515 
00020 [L1646] MOV      A=6 B=0 C=4 D=4 
00021 [L1646] TGETS    A=5 B=4 C=2 D=1026 'getContentSize'
00022 [L1646] CALL     A=5 B=2 C=2 D=514 
00023 [L1647] TGETS    A=6 B=3 C=5 D=773 'height'
00024 [L1647] MULVN    A=6 B=6 C=0 D=1536 
00025 [L1647] SUBVV    A=6 B=0 C=6 D=6 
00026 [L1647] TGETS    A=7 B=5 C=5 D=1285 'height'
00027 [L1647] DIVVV    A=6 B=6 C=7 D=1543 
00028 [L1648] MOV      A=8 B=0 C=4 D=4 
00029 [L1648] TGETS    A=7 B=4 C=6 D=1030 'setScaleY'
00030 [L1648] MOV      A=9 B=0 C=6 D=6 
00031 [L1648] CALL     A=7 B=1 C=3 D=259 
00032 [L1649] UGET     A=7 B=0 C=1 D=1 contentNode
00033 [L1649] MOV      A=8 B=0 C=7 D=7 
00034 [L1649] TGETS    A=7 B=7 C=3 D=1795 'addChild'
00035 [L1649] MOV      A=9 B=0 C=4 D=4 
00036 [L1649] KSHORT   A=10 B=255 C=251 D=65531 -5
00037 [L1649] CALL     A=7 B=1 C=4 D=260 
00038 [L1651] UGET     A=7 B=0 C=0 D=0 CCSprite
00039 [L1651] MOV      A=8 B=0 C=7 D=7 
00040 [L1651] TGETS    A=7 B=7 C=0 D=1792 'create'
00041 [L1651] KSTR     A=9 B=0 C=1 D=1 'v2/newIntroUI/big_bkg1.png'
00042 [L1651] CALL     A=7 B=2 C=3 D=515 
00043 [L1652] MOV      A=9 B=0 C=7 D=7 
00044 [L1652] TGETS    A=8 B=7 C=7 D=1799 'setFlipY'
00045 [L1652] KPRI     A=10 B=0 C=2 D=2 
00046 [L1652] CALL     A=8 B=1 C=3 D=259 
00047 [L1653] UGET     A=8 B=0 C=1 D=1 contentNode
00048 [L1653] MOV      A=9 B=0 C=8 D=8 
00049 [L1653] TGETS    A=8 B=8 C=3 D=2051 'addChild'
00050 [L1653] MOV      A=10 B=0 C=7 D=7 
00051 [L1653] KSHORT   A=11 B=255 C=251 D=65531 -5
00052 [L1653] CALL     A=8 B=1 C=4 D=260 
00053 [L1655] MOV      A=9 B=0 C=2 D=2 
00054 [L1655] TGETS    A=8 B=2 C=8 D=520 'setAnchorPoint'
00055 [L1655] UGET     A=10 B=0 C=2 D=2 CCPointMake
00056 [L1655] KNUM     A=11 B=0 C=1 D=1 0.5
00057 [L1655] KSHORT   A=12 B=0 C=1 D=1 1
00058 [L1655] CALL     A=10 B=0 C=3 D=3 
00059 [L1655] CALLM    A=8 B=1 C=1 D=257 
00060 [L1656] MOV      A=9 B=0 C=2 D=2 
00061 [L1656] TGETS    A=8 B=2 C=9 D=521 'setPosition'
00062 [L1656] TGETS    A=10 B=1 C=10 D=266 'x'
00063 [L1656] TGETS    A=11 B=1 C=11 D=267 'y'
00064 [L1656] CALL     A=8 B=1 C=4 D=260 
00065 [L1658] MOV      A=9 B=0 C=4 D=4 
00066 [L1658] TGETS    A=8 B=4 C=8 D=1032 'setAnchorPoint'
00067 [L1658] UGET     A=10 B=0 C=2 D=2 CCPointMake
00068 [L1658] KNUM     A=11 B=0 C=1 D=1 0.5
00069 [L1658] KSHORT   A=12 B=0 C=1 D=1 1
00070 [L1658] CALL     A=10 B=0 C=3 D=3 
00071 [L1658] CALLM    A=8 B=1 C=1 D=257 
00072 [L1659] MOV      A=9 B=0 C=4 D=4 
00073 [L1659] TGETS    A=8 B=4 C=9 D=1033 'setPosition'
00074 [L1659] TGETS    A=10 B=1 C=10 D=266 'x'
00075 [L1659] TGETS    A=11 B=1 C=11 D=267 'y'
00076 [L1659] TGETS    A=12 B=3 C=5 D=773 'height'
00077 [L1659] SUBVV    A=11 B=11 C=12 D=2828 
00078 [L1659] CALL     A=8 B=1 C=4 D=260 
00079 [L1661] MOV      A=9 B=0 C=7 D=7 
00080 [L1661] TGETS    A=8 B=7 C=8 D=1800 'setAnchorPoint'
00081 [L1661] UGET     A=10 B=0 C=2 D=2 CCPointMake
00082 [L1661] KNUM     A=11 B=0 C=1 D=1 0.5
00083 [L1661] KSHORT   A=12 B=0 C=1 D=1 1
00084 [L1661] CALL     A=10 B=0 C=3 D=3 
00085 [L1661] CALLM    A=8 B=1 C=1 D=257 
00086 [L1662] MOV      A=9 B=0 C=7 D=7 
00087 [L1662] TGETS    A=8 B=7 C=9 D=1801 'setPosition'
00088 [L1662] TGETS    A=10 B=1 C=10 D=266 'x'
00089 [L1662] TGETS    A=11 B=1 C=11 D=267 'y'
00090 [L1662] TGETS    A=12 B=3 C=5 D=773 'height'
00091 [L1662] ADDVV    A=11 B=11 C=12 D=2828 
00092 [L1662] SUBVV    A=11 B=11 C=0 D=2816 
00093 [L1662] CALL     A=8 B=1 C=4 D=260 
00094 [L1663] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto44 offset=0x5f40 source_lines=1023-1806 params=4
UPVALUES ['CCDirector', 'CCLayer', 'CCArray', 'CCLayerColor', 'ccc4', 'CCSprite', 'CCMenuItemImage', 'CCMenu', 'CCPointMake', 'CCNode', 'CCRectMake', 'm_t', 'ccp', 'tostring', 'ccc3', 'gethz', 'string', 'o_t', 'math', 'table', 'CCLabelTTF', 'CCSizeMake', 'kCCTextAlignmentLeft']
00001 [L1024] TDUP     A=4 B=0 C=0 D=0 {'kind': 'table', 'value': {1: 254, 2: 235, 3: 192}}
00002 [L1025] UGET     A=5 B=0 C=0 D=0 CCDirector
00003 [L1025] MOV      A=6 B=0 C=5 D=5 
00004 [L1025] TGETS    A=5 B=5 C=1 D=1281 'sharedDirector'
00005 [L1025] CALL     A=5 B=2 C=2 D=514 
00006 [L1025] MOV      A=6 B=0 C=5 D=5 
00007 [L1025] TGETS    A=5 B=5 C=2 D=1282 'getVisibleSize'
00008 [L1025] CALL     A=5 B=2 C=2 D=514 
00009 [L1026] UGET     A=6 B=0 C=1 D=1 CCLayer
00010 [L1026] MOV      A=7 B=0 C=6 D=6 
00011 [L1026] TGETS    A=6 B=6 C=3 D=1539 'create'
00012 [L1026] CALL     A=6 B=2 C=2 D=514 
00013 [L1027] GGET     A=7 B=0 C=4 D=4 'g_packageUI'
00014 [L1027] TSETS    A=6 B=7 C=5 D=1797 'itemIntroLayer'
00015 [L1028] GGET     A=7 B=0 C=4 D=4 'g_packageUI'
00016 [L1028] TSETS    A=0 B=7 C=6 D=1798 'last_show_item'
00017 [L1029] UGET     A=7 B=0 C=2 D=2 CCArray
00018 [L1029] MOV      A=8 B=0 C=7 D=7 
00019 [L1029] TGETS    A=7 B=7 C=3 D=1795 'create'
00020 [L1029] CALL     A=7 B=2 C=2 D=514 
00021 [L1031] UGET     A=8 B=0 C=3 D=3 CCLayerColor
00022 [L1031] MOV      A=9 B=0 C=8 D=8 
00023 [L1031] TGETS    A=8 B=8 C=3 D=2051 'create'
00024 [L1031] UGET     A=10 B=0 C=4 D=4 ccc4
00025 [L1031] KSHORT   A=11 B=0 C=0 D=0 0
00026 [L1031] KSHORT   A=12 B=0 C=0 D=0 0
00027 [L1031] KSHORT   A=13 B=0 C=0 D=0 0
00028 [L1031] KSHORT   A=14 B=0 C=100 D=100 100
00029 [L1031] CALL     A=10 B=0 C=5 D=5 
00030 [L1031] CALLM    A=8 B=2 C=1 D=513 
00031 [L1032] MOV      A=10 B=0 C=6 D=6 
00032 [L1032] TGETS    A=9 B=6 C=7 D=1543 'addChild'
00033 [L1032] MOV      A=11 B=0 C=8 D=8 
00034 [L1032] KSHORT   A=12 B=255 C=246 D=65526 -10
00035 [L1032] CALL     A=9 B=1 C=4 D=260 
00036 [L1041] FNEW     A=9 B=0 C=8 D=8 {'kind': 'proto', 'id': 40}
00037 [L1034] GSET     A=9 B=0 C=9 D=9 'closeAndRemoveIntroLayer'
00038 [L1043] UGET     A=9 B=0 C=5 D=5 CCSprite
00039 [L1043] MOV      A=10 B=0 C=9 D=9 
00040 [L1043] TGETS    A=9 B=9 C=3 D=2307 'create'
00041 [L1043] KSTR     A=11 B=0 C=10 D=10 'v2/messageUI/frame1.png'
00042 [L1043] CALL     A=9 B=2 C=3 D=515 
00043 [L1044] GGET     A=10 B=0 C=11 D=11 'd_ms'
00044 [L1044] TGETS    A=10 B=10 C=12 D=2572 'd_u'
00045 [L1044] TGETS    A=10 B=10 C=13 D=2573 'setStyles'
00046 [L1044] MOV      A=11 B=0 C=9 D=9 
00047 [L1044] TDUP     A=12 B=0 C=14 D=14 {'kind': 'table', 'value': {'scaleY': 0.83, 'x': 0.5, 'y': 0.55}}
00048 [L1044] CALL     A=10 B=1 C=3 D=259 
00049 [L1045] MOV      A=11 B=0 C=6 D=6 
00050 [L1045] TGETS    A=10 B=6 C=7 D=1543 'addChild'
00051 [L1045] MOV      A=12 B=0 C=9 D=9 
00052 [L1045] CALL     A=10 B=1 C=3 D=259 
00053 [L1048] TNEW     A=10 B=0 C=0 D=0 
00054 [L1049] GGET     A=11 B=0 C=9 D=9 'closeAndRemoveIntroLayer'
00055 [L1049] TSETS    A=11 B=10 C=15 D=2575 'outFunc'
00056 [L1050] GGET     A=11 B=0 C=11 D=11 'd_ms'
00057 [L1050] TGETS    A=11 B=11 C=12 D=2828 'd_u'
00058 [L1050] TGETS    A=11 B=11 C=17 D=2833 'getRealRect'
00059 [L1050] MOV      A=12 B=0 C=9 D=9 
00060 [L1050] CALL     A=11 B=2 C=2 D=514 
00061 [L1050] TSETS    A=11 B=10 C=16 D=2576 'rect'
00062 [L1051] GGET     A=11 B=0 C=11 D=11 'd_ms'
00063 [L1051] TGETS    A=11 B=11 C=12 D=2828 'd_u'
00064 [L1051] TGETS    A=11 B=11 C=18 D=2834 'createSwallowTouchLayerFunc'
00065 [L1051] MOV      A=12 B=0 C=6 D=6 
00066 [L1051] MOV      A=13 B=0 C=10 D=10 
00067 [L1051] CALL     A=11 B=1 C=3 D=259 
00068 [L1053] UGET     A=11 B=0 C=6 D=6 CCMenuItemImage
00069 [L1053] MOV      A=12 B=0 C=11 D=11 
00070 [L1053] TGETS    A=11 B=11 C=3 D=2819 'create'
00071 [L1053] KSTR     A=13 B=0 C=19 D=19 'v2/introUI/close1.png'
00072 [L1053] KSTR     A=14 B=0 C=20 D=20 'v2/introUI/close2.png'
00073 [L1053] CALL     A=11 B=2 C=4 D=516 
00074 [L1054] MOV      A=13 B=0 C=11 D=11 
00075 [L1054] TGETS    A=12 B=11 C=21 D=2837 'setTag'
00076 [L1054] GGET     A=14 B=0 C=22 D=22 'g_introButtonType'
00077 [L1054] TGETS    A=14 B=14 C=23 D=3607 'close'
00078 [L1054] CALL     A=12 B=1 C=3 D=259 
00079 [L1055] GGET     A=12 B=0 C=11 D=11 'd_ms'
00080 [L1055] TGETS    A=12 B=12 C=12 D=3084 'd_u'
00081 [L1055] TGETS    A=12 B=12 C=13 D=3085 'setStyles'
00082 [L1055] MOV      A=13 B=0 C=11 D=11 
00083 [L1055] TDUP     A=14 B=0 C=24 D=24 {'kind': 'table', 'value': {'x': 0.73, 'y': 0.93}}
00084 [L1055] CALL     A=12 B=1 C=3 D=259 
00085 [L1056] MOV      A=13 B=0 C=11 D=11 
00086 [L1056] TGETS    A=12 B=11 C=25 D=2841 'registerScriptTapHandler'
00087 [L1056] MOV      A=14 B=0 C=1 D=1 
00088 [L1056] CALL     A=12 B=1 C=3 D=259 
00089 [L1057] UGET     A=12 B=0 C=7 D=7 CCMenu
00090 [L1057] MOV      A=13 B=0 C=12 D=12 
00091 [L1057] TGETS    A=12 B=12 C=26 D=3098 'createWithItem'
00092 [L1057] MOV      A=14 B=0 C=11 D=11 
00093 [L1057] CALL     A=12 B=2 C=3 D=515 
00094 [L1058] MOV      A=14 B=0 C=12 D=12 
00095 [L1058] TGETS    A=13 B=12 C=27 D=3099 'setPosition'
00096 [L1058] UGET     A=15 B=0 C=8 D=8 CCPointMake
00097 [L1058] KSHORT   A=16 B=0 C=0 D=0 0
00098 [L1058] KSHORT   A=17 B=0 C=0 D=0 0
00099 [L1058] CALL     A=15 B=0 C=3 D=3 
00100 [L1058] CALLM    A=13 B=1 C=1 D=257 
00101 [L1059] MOV      A=14 B=0 C=6 D=6 
00102 [L1059] TGETS    A=13 B=6 C=7 D=1543 'addChild'
00103 [L1059] MOV      A=15 B=0 C=12 D=12 
00104 [L1059] KSHORT   A=16 B=0 C=10 D=10 10
00105 [L1059] CALL     A=13 B=1 C=4 D=260 
00106 [L1061] TDUP     A=13 B=0 C=29 D=29 {'kind': 'table', 'value': {}}
00107 [L1061] TGETS    A=14 B=5 C=28 D=1308 'width'
00108 [L1061] MULNV    A=14 B=14 C=0 D=3584 
00109 [L1061] TSETS    A=14 B=13 C=30 D=3358 'x'
00110 [L1061] TGETS    A=14 B=5 C=31 D=1311 'height'
00111 [L1061] MULNV    A=14 B=14 C=1 D=3585 
00112 [L1061] TSETS    A=14 B=13 C=32 D=3360 'y'
00113 [L1061] TGETS    A=14 B=5 C=28 D=1308 'width'
00114 [L1061] MULNV    A=14 B=14 C=2 D=3586 
00115 [L1061] TSETS    A=14 B=13 C=28 D=3356 'width'
00116 [L1061] TGETS    A=14 B=5 C=31 D=1311 'height'
00117 [L1061] MULNV    A=14 B=14 C=3 D=3587 
00118 [L1061] TSETS    A=14 B=13 C=31 D=3359 'height'
00119 [L1062] TDUP     A=14 B=0 C=33 D=33 {'kind': 'table', 'value': {}}
00120 [L1062] TGETS    A=15 B=13 C=30 D=3358 'x'
00121 [L1062] TSETS    A=15 B=14 C=30 D=3614 'x'
00122 [L1062] TGETS    A=15 B=13 C=32 D=3360 'y'
00123 [L1062] TSETS    A=15 B=14 C=32 D=3616 'y'
00124 [L1063] TDUP     A=15 B=0 C=34 D=34 {'kind': 'table', 'value': {}}
00125 [L1063] TGETS    A=16 B=13 C=28 D=3356 'width'
00126 [L1063] TSETS    A=16 B=15 C=28 D=3868 'width'
00127 [L1063] TGETS    A=16 B=13 C=31 D=3359 'height'
00128 [L1063] TSETS    A=16 B=15 C=31 D=3871 'height'
00129 [L1065] KSHORT   A=16 B=0 C=0 D=0 0
00130 [L1067] GGET     A=17 B=0 C=11 D=11 'd_ms'
00131 [L1067] TGETS    A=17 B=17 C=35 D=4387 'd_inertiaLayer'
00132 [L1067] TGETS    A=17 B=17 C=36 D=4388 'inertiaLayer'
00133 [L1067] TGETS    A=17 B=17 C=37 D=4389 'new'
00134 [L1067] MOV      A=18 B=0 C=15 D=15 
00135 [L1067] MOV      A=19 B=0 C=14 D=14 
00136 [L1067] MOV      A=20 B=0 C=13 D=13 
00137 [L1067] CALL     A=17 B=2 C=4 D=516 
00138 [L1068] MOV      A=19 B=0 C=6 D=6 
00139 [L1068] TGETS    A=18 B=6 C=7 D=1543 'addChild'
00140 [L1068] TGETS    A=20 B=17 C=38 D=4390 'scrollView'
00141 [L1068] KSHORT   A=21 B=0 C=100 D=100 100
00142 [L1068] CALL     A=18 B=1 C=4 D=260 
00143 [L1070] UGET     A=18 B=0 C=9 D=9 CCNode
00144 [L1070] MOV      A=19 B=0 C=18 D=18 
00145 [L1070] TGETS    A=18 B=18 C=3 D=4611 'create'
00146 [L1070] CALL     A=18 B=2 C=2 D=514 
00147 [L1071] MOV      A=20 B=0 C=18 D=18 
00148 [L1071] TGETS    A=19 B=18 C=27 D=4635 'setPosition'
00149 [L1071] TGETS    A=21 B=14 C=30 D=3614 'x'
00150 [L1071] UNM      A=21 B=0 C=21 D=21 
00151 [L1071] TGETS    A=22 B=14 C=32 D=3616 'y'
00152 [L1071] UNM      A=22 B=0 C=22 D=22 
00153 [L1071] CALL     A=19 B=1 C=4 D=260 
00154 [L1074] UGET     A=19 B=0 C=5 D=5 CCSprite
00155 [L1074] MOV      A=20 B=0 C=19 D=19 
00156 [L1074] TGETS    A=19 B=19 C=3 D=4867 'create'
00157 [L1074] KSTR     A=21 B=0 C=39 D=39 'v2/newIntroUI/head_bkg.png'
00158 [L1074] CALL     A=19 B=2 C=3 D=515 
00159 [L1075] GGET     A=20 B=0 C=11 D=11 'd_ms'
00160 [L1075] TGETS    A=20 B=20 C=12 D=5132 'd_u'
00161 [L1075] TGETS    A=20 B=20 C=13 D=5133 'setStyles'
00162 [L1075] MOV      A=21 B=0 C=19 D=19 
00163 [L1075] TDUP     A=22 B=0 C=40 D=40 {'kind': 'table', 'value': {'x': 0.5, 'y': 0.89}}
00164 [L1075] CALL     A=20 B=1 C=3 D=259 
00165 [L1076] MOV      A=21 B=0 C=18 D=18 
00166 [L1076] TGETS    A=20 B=18 C=7 D=4615 'addChild'
00167 [L1076] MOV      A=22 B=0 C=19 D=19 
00168 [L1076] CALL     A=20 B=1 C=3 D=259 
00169 [L1078] UGET     A=20 B=0 C=5 D=5 CCSprite
00170 [L1078] MOV      A=21 B=0 C=20 D=20 
00171 [L1078] TGETS    A=20 B=20 C=3 D=5123 'create'
00172 [L1078] KSTR     A=22 B=0 C=41 D=41 'v2/introUI/intro_label.png'
00173 [L1078] CALL     A=20 B=2 C=3 D=515 
00174 [L1079] GGET     A=21 B=0 C=11 D=11 'd_ms'
00175 [L1079] TGETS    A=21 B=21 C=12 D=5388 'd_u'
00176 [L1079] TGETS    A=21 B=21 C=13 D=5389 'setStyles'
00177 [L1079] MOV      A=22 B=0 C=20 D=20 
00178 [L1079] TDUP     A=23 B=0 C=42 D=42 {'kind': 'table', 'value': {'x': 0.5, 'y': 0.9}}
00179 [L1079] CALL     A=21 B=1 C=3 D=259 
00180 [L1080] MOV      A=22 B=0 C=18 D=18 
00181 [L1080] TGETS    A=21 B=18 C=7 D=4615 'addChild'
00182 [L1080] MOV      A=23 B=0 C=20 D=20 
00183 [L1080] CALL     A=21 B=1 C=3 D=259 
00184 [L1083] MOV      A=22 B=0 C=19 D=19 
00185 [L1083] TGETS    A=21 B=19 C=43 D=4907 'getContentSize'
00186 [L1083] CALL     A=21 B=2 C=2 D=514 
00187 [L1084] TGETS    A=22 B=21 C=31 D=5407 'height'
00188 [L1084] ADDVV    A=16 B=16 C=22 D=4118 
00189 [L1086] TGETS    A=22 B=0 C=44 D=44 'attach_type'
00190 [L1086] IST      A=0 B=0 C=22 D=22 
00191 [L1086] JMP      A=22 B=128 C=12 D=32780 target=204
00192 [L1087] TGETS    A=22 B=0 C=45 D=45 'csvInfo'
00193 [L1087] ISF      A=0 B=0 C=22 D=22 
00194 [L1087] JMP      A=23 B=128 C=9 D=32777 target=204
00195 [L1087] TGETS    A=22 B=0 C=45 D=45 'csvInfo'
00196 [L1087] TGETS    A=22 B=22 C=46 D=5678 'quality'
00197 [L1087] ISNEN    A=22 B=0 C=4 D=4 0
00198 [L1087] JMP      A=22 B=128 C=5 D=32773 target=204
00199 [L1088] GGET     A=22 B=0 C=11 D=11 'd_ms'
00200 [L1088] TGETS    A=22 B=22 C=47 D=5679 'd_common_def'
00201 [L1088] TGETS    A=22 B=22 C=48 D=5680 'object_type'
00202 [L1088] TGETS    A=22 B=22 C=49 D=5681 'item'
00203 [L1088] TSETS    A=22 B=0 C=44 D=44 'attach_type'
00204 [L1091] TGETS    A=22 B=0 C=50 D=50 'reborn_bit'
00205 [L1091] ISF      A=0 B=0 C=22 D=22 
00206 [L1091] JMP      A=23 B=128 C=7 D=32775 target=214
00207 [L1091] TGETS    A=22 B=0 C=50 D=50 'reborn_bit'
00208 [L1091] KSHORT   A=23 B=0 C=0 D=0 0
00209 [L1091] ISLT     A=23 B=0 C=22 D=22 
00210 [L1091] JMP      A=22 B=128 C=2 D=32770 target=213
00211 [L1091] KPRI     A=22 B=0 C=1 D=1 
00212 [L1091] JMP      A=23 B=128 C=1 D=32769 target=214
00213 [L1091] KPRI     A=22 B=0 C=2 D=2 
00214 [L1092] TGETS    A=23 B=0 C=45 D=45 'csvInfo'
00215 [L1092] TGETS    A=23 B=23 C=51 D=5939 'packageTag'
00216 [L1093] TDUP     A=24 B=0 C=52 D=52 {'kind': 'table', 'value': {1: 'v2/introUI/damage.png', 2: 'v2/introUI/defence.png', 3: 'v2/introUI/health.png'}}
00217 [L1129] FNEW     A=25 B=0 C=53 D=53 {'kind': 'proto', 'id': 41}
00218 [L1130] KPRI     A=26 B=0 C=0 D=0 
00219 [L1131] GGET     A=27 B=0 C=54 D=54 'packageTagDef'
00220 [L1131] TGETS    A=27 B=27 C=55 D=6967 'props'
00221 [L1131] ISEQV    A=23 B=0 C=27 D=27 
00222 [L1131] JMP      A=27 B=128 C=8 D=32776 target=231
00223 [L1131] GGET     A=27 B=0 C=54 D=54 'packageTagDef'
00224 [L1131] TGETS    A=27 B=27 C=56 D=6968 'skill'
00225 [L1131] ISEQV    A=23 B=0 C=27 D=27 
00226 [L1131] JMP      A=27 B=128 C=4 D=32772 target=231
00227 [L1131] GGET     A=27 B=0 C=54 D=54 'packageTagDef'
00228 [L1131] TGETS    A=27 B=27 C=57 D=6969 'stone'
00229 [L1131] ISNEV    A=23 B=0 C=27 D=27 
00230 [L1131] JMP      A=27 B=128 C=224 D=32992 target=455
00231 [L1132] MOV      A=27 B=0 C=25 D=25 
00232 [L1132] CALL     A=27 B=2 C=1 D=513 
00233 [L1133] GGET     A=28 B=0 C=11 D=11 'd_ms'
00234 [L1133] TGETS    A=28 B=28 C=12 D=7180 'd_u'
00235 [L1133] TGETS    A=28 B=28 C=13 D=7181 'setStyles'
00236 [L1133] MOV      A=29 B=0 C=27 D=27 
00237 [L1133] TDUP     A=30 B=0 C=58 D=58 {'kind': 'table', 'value': {'scale': 0.18, 'x': 0.36, 'y': 0.68}}
00238 [L1133] CALL     A=28 B=1 C=3 D=259 
00239 [L1134] TGETS    A=28 B=0 C=45 D=45 'csvInfo'
00240 [L1134] TGETS    A=28 B=28 C=59 D=7227 'mainType'
00241 [L1134] UGET     A=29 B=0 C=11 D=11 m_t
00242 [L1134] TGETS    A=29 B=29 C=60 D=7484 'awaken_star'
00243 [L1134] ISEQV    A=28 B=0 C=29 D=29 
00244 [L1134] JMP      A=28 B=128 C=4 D=32772 target=249
00245 [L1135] MOV      A=29 B=0 C=18 D=18 
00246 [L1135] TGETS    A=28 B=18 C=7 D=4615 'addChild'
00247 [L1135] MOV      A=30 B=0 C=27 D=27 
00248 [L1135] CALL     A=28 B=1 C=3 D=259 
00249 [L1137] TGETS    A=28 B=0 C=61 D=61 'upgrade_level'
00250 [L1137] ISF      A=0 B=0 C=28 D=28 
00251 [L1137] JMP      A=29 B=128 C=29 D=32797 target=281
00252 [L1137] TGETS    A=28 B=0 C=61 D=61 'upgrade_level'
00253 [L1137] ISEQN    A=28 B=0 C=4 D=4 0
00254 [L1137] JMP      A=28 B=128 C=26 D=32794 target=281
00255 [L1138] MOV      A=29 B=0 C=27 D=27 
00256 [L1138] TGETS    A=28 B=27 C=43 D=6955 'getContentSize'
00257 [L1138] CALL     A=28 B=2 C=2 D=514 
00258 [L1139] UGET     A=29 B=0 C=5 D=5 CCSprite
00259 [L1139] MOV      A=30 B=0 C=29 D=29 
00260 [L1139] TGETS    A=29 B=29 C=3 D=7427 'create'
00261 [L1139] KSTR     A=31 B=0 C=62 D=62 'v2/enhanceUI/wu.png'
00262 [L1139] CALL     A=29 B=2 C=3 D=515 
00263 [L1140] MOV      A=31 B=0 C=27 D=27 
00264 [L1140] TGETS    A=30 B=27 C=7 D=6919 'addChild'
00265 [L1140] MOV      A=32 B=0 C=29 D=29 
00266 [L1140] CALL     A=30 B=1 C=3 D=259 
00267 [L1141] MOV      A=31 B=0 C=29 D=29 
00268 [L1141] TGETS    A=30 B=29 C=63 D=7487 'setAnchorPoint'
00269 [L1141] UGET     A=32 B=0 C=12 D=12 ccp
00270 [L1141] KSHORT   A=33 B=0 C=1 D=1 1
00271 [L1141] KSHORT   A=34 B=0 C=0 D=0 0
00272 [L1141] CALL     A=32 B=0 C=3 D=3 
00273 [L1141] CALLM    A=30 B=1 C=1 D=257 
00274 [L1142] MOV      A=31 B=0 C=29 D=29 
00275 [L1142] TGETS    A=30 B=29 C=27 D=7451 'setPosition'
00276 [L1142] TGETS    A=32 B=28 C=28 D=7196 'width'
00277 [L1142] MULNV    A=32 B=32 C=5 D=8197 
00278 [L1142] TGETS    A=33 B=28 C=31 D=7199 'height'
00279 [L1142] MULNV    A=33 B=33 C=6 D=8454 
00280 [L1142] CALL     A=30 B=1 C=4 D=260 
00281 [L1145] UGET     A=28 B=0 C=5 D=5 CCSprite
00282 [L1145] MOV      A=29 B=0 C=28 D=28 
00283 [L1145] TGETS    A=28 B=28 C=3 D=7171 'create'
00284 [L1145] KSTR     A=30 B=0 C=64 D=64 'v2/newIntroUI/bkg1.png'
00285 [L1145] CALL     A=28 B=2 C=3 D=515 
00286 [L1146] GGET     A=29 B=0 C=11 D=11 'd_ms'
00287 [L1146] TGETS    A=29 B=29 C=12 D=7436 'd_u'
00288 [L1146] TGETS    A=29 B=29 C=13 D=7437 'setStyles'
00289 [L1146] MOV      A=30 B=0 C=28 D=28 
00290 [L1146] TDUP     A=31 B=0 C=65 D=65 {'kind': 'table', 'value': {'x': 0.58, 'y': 0.68}}
00291 [L1146] CALL     A=29 B=1 C=3 D=259 
00292 [L1147] MOV      A=30 B=0 C=18 D=18 
00293 [L1147] TGETS    A=29 B=18 C=7 D=4615 'addChild'
00294 [L1147] MOV      A=31 B=0 C=28 D=28 
00295 [L1147] KSHORT   A=32 B=255 C=254 D=65534 -2
00296 [L1147] CALL     A=29 B=1 C=4 D=260 
00297 [L1149] MOV      A=30 B=0 C=28 D=28 
00298 [L1149] TGETS    A=29 B=28 C=43 D=7211 'getContentSize'
00299 [L1149] CALL     A=29 B=2 C=2 D=514 
00300 [L1149] MOV      A=26 B=0 C=29 D=29 
00301 [L1150] KPRI     A=29 B=0 C=0 D=0 
00302 [L1151] TGETS    A=30 B=0 C=61 D=61 'upgrade_level'
00303 [L1151] ISF      A=0 B=0 C=30 D=30 
00304 [L1151] JMP      A=31 B=128 C=82 D=32850 target=387
00305 [L1151] TGETS    A=30 B=0 C=61 D=61 'upgrade_level'
00306 [L1151] KSHORT   A=31 B=0 C=0 D=0 0
00307 [L1151] ISGE     A=31 B=0 C=30 D=30 
00308 [L1151] JMP      A=30 B=128 C=78 D=32846 target=387
00309 [L1153] UGET     A=30 B=0 C=5 D=5 CCSprite
00310 [L1153] MOV      A=31 B=0 C=30 D=30 
00311 [L1153] TGETS    A=30 B=30 C=3 D=7683 'create'
00312 [L1153] KSTR     A=32 B=0 C=66 D=66 'v2/introUI/health.png'
00313 [L1153] CALL     A=30 B=2 C=3 D=515 
00314 [L1154] MOV      A=32 B=0 C=30 D=30 
00315 [L1154] TGETS    A=31 B=30 C=27 D=7707 'setPosition'
00316 [L1154] TGETS    A=33 B=26 C=28 D=6684 'width'
00317 [L1154] MULVN    A=33 B=33 C=7 D=8455 
00318 [L1154] TGETS    A=34 B=26 C=31 D=6687 'height'
00319 [L1154] MULVN    A=34 B=34 C=8 D=8712 
00320 [L1154] CALL     A=31 B=1 C=4 D=260 
00321 [L1156] MOV      A=32 B=0 C=30 D=30 
00322 [L1156] TGETS    A=31 B=30 C=63 D=7743 'setAnchorPoint'
00323 [L1156] UGET     A=33 B=0 C=8 D=8 CCPointMake
00324 [L1156] KSHORT   A=34 B=0 C=0 D=0 0
00325 [L1156] KNUM     A=35 B=0 C=8 D=8 0.5
00326 [L1156] CALL     A=33 B=0 C=3 D=3 
00327 [L1156] CALLM    A=31 B=1 C=1 D=257 
00328 [L1157] MOV      A=32 B=0 C=28 D=28 
00329 [L1157] TGETS    A=31 B=28 C=7 D=7175 'addChild'
00330 [L1157] MOV      A=33 B=0 C=30 D=30 
00331 [L1157] KSHORT   A=34 B=0 C=5 D=5 5
00332 [L1157] CALL     A=31 B=1 C=4 D=260 
00333 [L1159] KSHORT   A=31 B=0 C=12 D=12 12
00334 [L1160] GGET     A=32 B=0 C=11 D=11 'd_ms'
00335 [L1160] TGETS    A=32 B=32 C=12 D=8204 'd_u'
00336 [L1160] TGETS    A=32 B=32 C=67 D=8259 'createByStyle'
00337 [L1160] TDUP     A=33 B=0 C=68 D=68 {'kind': 'table', 'value': {'font': 'arial', 'fontsize': 26, 'type': 'label'}}
00338 [L1160] UGET     A=34 B=0 C=13 D=13 tostring
00339 [L1160] MOV      A=35 B=0 C=31 D=31 
00340 [L1160] CALL     A=34 B=2 C=2 D=514 
00341 [L1160] KSTR     A=35 B=0 C=69 D=69 '%'
00342 [L1160] CAT      A=34 B=34 C=35 D=8739 
00343 [L1160] TSETS    A=34 B=33 C=70 D=8518 'string'
00344 [L1160] CALL     A=32 B=2 C=2 D=514 
00345 [L1161] MOV      A=34 B=0 C=32 D=32 
00346 [L1161] TGETS    A=33 B=32 C=27 D=8219 'setPosition'
00347 [L1161] TGETS    A=35 B=26 C=28 D=6684 'width'
00348 [L1161] MULVN    A=35 B=35 C=9 D=8969 
00349 [L1161] TGETS    A=36 B=26 C=31 D=6687 'height'
00350 [L1161] MULVN    A=36 B=36 C=8 D=9224 
00351 [L1161] CALL     A=33 B=1 C=4 D=260 
00352 [L1162] MOV      A=34 B=0 C=32 D=32 
00353 [L1162] TGETS    A=33 B=32 C=63 D=8255 'setAnchorPoint'
00354 [L1162] UGET     A=35 B=0 C=8 D=8 CCPointMake
00355 [L1162] KSHORT   A=36 B=0 C=0 D=0 0
00356 [L1162] KNUM     A=37 B=0 C=8 D=8 0.5
00357 [L1162] CALL     A=35 B=0 C=3 D=3 
00358 [L1162] CALLM    A=33 B=1 C=1 D=257 
00359 [L1163] MOV      A=34 B=0 C=32 D=32 
00360 [L1163] TGETS    A=33 B=32 C=71 D=8263 'setColor'
00361 [L1163] UGET     A=35 B=0 C=14 D=14 ccc3
00362 [L1163] TGETB    A=36 B=4 C=1 D=1025 
00363 [L1163] TGETB    A=37 B=4 C=2 D=1026 
00364 [L1163] TGETB    A=38 B=4 C=3 D=1027 
00365 [L1163] CALL     A=35 B=0 C=4 D=4 
00366 [L1163] CALLM    A=33 B=1 C=1 D=257 
00367 [L1164] MOV      A=34 B=0 C=28 D=28 
00368 [L1164] TGETS    A=33 B=28 C=7 D=7175 'addChild'
00369 [L1164] MOV      A=35 B=0 C=32 D=32 
00370 [L1164] KSHORT   A=36 B=0 C=5 D=5 5
00371 [L1164] CALL     A=33 B=1 C=4 D=260 
00372 [L1166] MOV      A=34 B=0 C=30 D=30 
00373 [L1166] TGETS    A=33 B=30 C=72 D=7752 'getPositionLua'
00374 [L1166] CALL     A=33 B=2 C=2 D=514 
00375 [L1166] GSET     A=33 B=0 C=73 D=73 'advanceposition'
00376 [L1167] GGET     A=33 B=0 C=11 D=11 'd_ms'
00377 [L1167] TGETS    A=33 B=33 C=12 D=8460 'd_u'
00378 [L1167] TGETS    A=33 B=33 C=67 D=8515 'createByStyle'
00379 [L1167] TDUP     A=34 B=0 C=74 D=74 {'kind': 'table', 'value': {'y': 0.78, 'font': 'arial', 'type': 'label', 'x': 0.58, 'fontsize': 30}}
00380 [L1167] TGETS    A=35 B=0 C=45 D=45 'csvInfo'
00381 [L1167] TGETS    A=35 B=35 C=75 D=9035 'name'
00382 [L1167] TSETS    A=35 B=34 C=70 D=8774 'string'
00383 [L1167] TSETS    A=4 B=34 C=76 D=8780 'color'
00384 [L1167] CALL     A=33 B=2 C=2 D=514 
00385 [L1167] MOV      A=29 B=0 C=33 D=33 
00386 [L1167] JMP      A=30 B=128 C=64 D=32832 target=451
00387 [L1169] GGET     A=30 B=0 C=54 D=54 'packageTagDef'
00388 [L1169] TGETS    A=30 B=30 C=57 D=7737 'stone'
00389 [L1169] ISNEV    A=23 B=0 C=30 D=30 
00390 [L1169] JMP      A=30 B=128 C=25 D=32793 target=416
00391 [L1169] TGETS    A=30 B=0 C=77 D=77 'level'
00392 [L1169] KSHORT   A=31 B=0 C=10 D=10 10
00393 [L1169] ISGE     A=31 B=0 C=30 D=30 
00394 [L1169] JMP      A=30 B=128 C=21 D=32789 target=416
00395 [L1169] TGETS    A=30 B=0 C=77 D=77 'level'
00396 [L1169] KSHORT   A=31 B=0 C=12 D=12 12
00397 [L1169] ISGE     A=30 B=0 C=31 D=31 
00398 [L1169] JMP      A=30 B=128 C=17 D=32785 target=416
00399 [L1170] GGET     A=30 B=0 C=11 D=11 'd_ms'
00400 [L1170] TGETS    A=30 B=30 C=12 D=7692 'd_u'
00401 [L1170] TGETS    A=30 B=30 C=67 D=7747 'createByStyle'
00402 [L1170] TDUP     A=31 B=0 C=78 D=78 {'kind': 'table', 'value': {'y': 0.77, 'type': 'label', 'x': 0.58, 'fontsize': 30}}
00403 [L1170] GGET     A=32 B=0 C=11 D=11 'd_ms'
00404 [L1170] TGETS    A=32 B=32 C=79 D=8271 'd_hz'
00405 [L1170] TGETS    A=32 B=32 C=80 D=8272 'gethz'
00406 [L1170] KSTR     A=33 B=0 C=81 D=81 'stone_ascName'
00407 [L1170] TGETS    A=34 B=0 C=45 D=45 'csvInfo'
00408 [L1170] TGETS    A=34 B=34 C=82 D=8786 'sub_type'
00409 [L1170] CAT      A=33 B=33 C=34 D=8482 
00410 [L1170] CALL     A=32 B=2 C=2 D=514 
00411 [L1170] TSETS    A=32 B=31 C=70 D=8006 'string'
00412 [L1170] TSETS    A=4 B=31 C=76 D=8012 'color'
00413 [L1170] CALL     A=30 B=2 C=2 D=514 
00414 [L1170] MOV      A=29 B=0 C=30 D=30 
00415 [L1170] JMP      A=30 B=128 C=35 D=32803 target=451
00416 [L1171] GGET     A=30 B=0 C=54 D=54 'packageTagDef'
00417 [L1171] TGETS    A=30 B=30 C=57 D=7737 'stone'
00418 [L1171] ISNEV    A=23 B=0 C=30 D=30 
00419 [L1171] JMP      A=30 B=128 C=21 D=32789 target=441
00420 [L1171] TGETS    A=30 B=0 C=77 D=77 'level'
00421 [L1171] KSHORT   A=31 B=0 C=11 D=11 11
00422 [L1171] ISGE     A=31 B=0 C=30 D=30 
00423 [L1171] JMP      A=30 B=128 C=17 D=32785 target=441
00424 [L1172] GGET     A=30 B=0 C=11 D=11 'd_ms'
00425 [L1172] TGETS    A=30 B=30 C=12 D=7692 'd_u'
00426 [L1172] TGETS    A=30 B=30 C=67 D=7747 'createByStyle'
00427 [L1172] TDUP     A=31 B=0 C=83 D=83 {'kind': 'table', 'value': {'y': 0.77, 'type': 'label', 'x': 0.58, 'fontsize': 30}}
00428 [L1172] GGET     A=32 B=0 C=11 D=11 'd_ms'
00429 [L1172] TGETS    A=32 B=32 C=79 D=8271 'd_hz'
00430 [L1172] TGETS    A=32 B=32 C=80 D=8272 'gethz'
00431 [L1172] KSTR     A=33 B=0 C=84 D=84 'stone_tilianName'
00432 [L1172] TGETS    A=34 B=0 C=45 D=45 'csvInfo'
00433 [L1172] TGETS    A=34 B=34 C=82 D=8786 'sub_type'
00434 [L1172] CAT      A=33 B=33 C=34 D=8482 
00435 [L1172] CALL     A=32 B=2 C=2 D=514 
00436 [L1172] TSETS    A=32 B=31 C=70 D=8006 'string'
00437 [L1172] TSETS    A=4 B=31 C=76 D=8012 'color'
00438 [L1172] CALL     A=30 B=2 C=2 D=514 
00439 [L1172] MOV      A=29 B=0 C=30 D=30 
00440 [L1172] JMP      A=30 B=128 C=10 D=32778 target=451
00441 [L1174] GGET     A=30 B=0 C=11 D=11 'd_ms'
00442 [L1174] TGETS    A=30 B=30 C=12 D=7692 'd_u'
00443 [L1174] TGETS    A=30 B=30 C=67 D=7747 'createByStyle'
00444 [L1174] TDUP     A=31 B=0 C=85 D=85 {'kind': 'table', 'value': {'y': 0.77, 'font': 'arial', 'type': 'label', 'x': 0.58, 'fontsize': 30}}
00445 [L1174] TGETS    A=32 B=0 C=45 D=45 'csvInfo'
00446 [L1174] TGETS    A=32 B=32 C=75 D=8267 'name'
00447 [L1174] TSETS    A=32 B=31 C=70 D=8006 'string'
00448 [L1174] TSETS    A=4 B=31 C=76 D=8012 'color'
00449 [L1174] CALL     A=30 B=2 C=2 D=514 
00450 [L1174] MOV      A=29 B=0 C=30 D=30 
00451 [L1179] MOV      A=31 B=0 C=18 D=18 
00452 [L1179] TGETS    A=30 B=18 C=7 D=4615 'addChild'
00453 [L1179] MOV      A=32 B=0 C=29 D=29 
00454 [L1179] CALL     A=30 B=1 C=3 D=259 
00455 [L1182] KNUM     A=27 B=0 C=10 D=10 0.36
00456 [L1184] GGET     A=28 B=0 C=54 D=54 'packageTagDef'
00457 [L1184] TGETS    A=28 B=28 C=55 D=7223 'props'
00458 [L1184] ISNEV    A=23 B=0 C=28 D=28 
00459 [L1184] JMP      A=28 B=128 C=199 D=32967 target=659
00460 [L1185] TDUP     A=28 B=0 C=86 D=86 {'kind': 'table', 'value': {1: 253, 2: 190, 3: 37}}
00461 [L1186] GGET     A=29 B=0 C=11 D=11 'd_ms'
00462 [L1186] TGETS    A=29 B=29 C=12 D=7436 'd_u'
00463 [L1186] TGETS    A=29 B=29 C=87 D=7511 'getSingleHzWidthBySize'
00464 [L1186] KSHORT   A=30 B=0 C=30 D=30 30
00465 [L1186] CALL     A=29 B=2 C=2 D=514 
00466 [L1187] KSHORT   A=30 B=0 C=0 D=0 0
00467 [L1189] TGETS    A=31 B=0 C=88 D=88 'count'
00468 [L1189] ISF      A=0 B=0 C=31 D=31 
00469 [L1189] JMP      A=32 B=128 C=29 D=32797 target=499
00470 [L1190] GGET     A=31 B=0 C=11 D=11 'd_ms'
00471 [L1190] TGETS    A=31 B=31 C=79 D=8015 'd_hz'
00472 [L1190] TGETS    A=31 B=31 C=80 D=8016 'gethz'
00473 [L1190] KSTR     A=32 B=0 C=89 D=89 'number'
00474 [L1190] CALL     A=31 B=2 C=2 D=514 
00475 [L1190] KSTR     A=32 B=0 C=90 D=90 ': '
00476 [L1190] TGETS    A=33 B=0 C=88 D=88 'count'
00477 [L1190] CAT      A=31 B=31 C=33 D=7969 
00478 [L1191] GGET     A=32 B=0 C=11 D=11 'd_ms'
00479 [L1191] TGETS    A=32 B=32 C=12 D=8204 'd_u'
00480 [L1191] TGETS    A=32 B=32 C=67 D=8259 'createByStyle'
00481 [L1191] TDUP     A=33 B=0 C=91 D=91 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 30}}
00482 [L1191] TSETS    A=31 B=33 C=70 D=8518 'string'
00483 [L1191] MULNV    A=34 B=29 C=11 D=7435 
00484 [L1191] SUBNV    A=34 B=34 C=12 D=8716 
00485 [L1191] TSETS    A=34 B=33 C=30 D=8478 'x'
00486 [L1191] MULVN    A=34 B=30 C=6 D=7686 
00487 [L1191] SUBNV    A=34 B=34 C=13 D=8717 
00488 [L1191] TSETS    A=34 B=33 C=32 D=8480 'y'
00489 [L1192] TSETS    A=28 B=33 C=76 D=8524 'color'
00490 [L1192] TDUP     A=34 B=0 C=92 D=92 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00491 [L1192] TSETS    A=34 B=33 C=93 D=8541 'anchor'
00492 [L1191] CALL     A=32 B=2 C=2 D=514 
00493 [L1193] MOV      A=34 B=0 C=18 D=18 
00494 [L1193] TGETS    A=33 B=18 C=7 D=4615 'addChild'
00495 [L1193] MOV      A=35 B=0 C=32 D=32 
00496 [L1193] KSHORT   A=36 B=0 C=10 D=10 10
00497 [L1193] CALL     A=33 B=1 C=4 D=260 
00498 [L1194] ADDVN    A=30 B=30 C=14 D=7694 
00499 [L1196] TGETS    A=31 B=0 C=45 D=45 'csvInfo'
00500 [L1196] ISF      A=0 B=0 C=31 D=31 
00501 [L1196] JMP      A=32 B=128 C=49 D=32817 target=551
00502 [L1196] TGETS    A=31 B=0 C=45 D=45 'csvInfo'
00503 [L1196] TGETS    A=31 B=31 C=94 D=8030 'show_level'
00504 [L1196] ISF      A=0 B=0 C=31 D=31 
00505 [L1196] JMP      A=32 B=128 C=45 D=32813 target=551
00506 [L1196] TGETS    A=31 B=0 C=45 D=45 'csvInfo'
00507 [L1196] TGETS    A=31 B=31 C=94 D=8030 'show_level'
00508 [L1196] KSHORT   A=32 B=0 C=0 D=0 0
00509 [L1196] ISGE     A=32 B=0 C=31 D=31 
00510 [L1196] JMP      A=31 B=128 C=40 D=32808 target=551
00511 [L1196] TGETS    A=31 B=0 C=45 D=45 'csvInfo'
00512 [L1196] TGETS    A=31 B=31 C=94 D=8030 'show_level'
00513 [L1196] KSHORT   A=32 B=31 C=48 D=7984 7984
00514 [L1196] ISLT     A=32 B=0 C=31 D=31 
00515 [L1196] JMP      A=31 B=128 C=5 D=32773 target=521
00516 [L1196] TGETS    A=31 B=0 C=45 D=45 'csvInfo'
00517 [L1196] TGETS    A=31 B=31 C=94 D=8030 'show_level'
00518 [L1196] KSHORT   A=32 B=31 C=45 D=7981 7981
00519 [L1196] ISGE     A=31 B=0 C=32 D=32 
00520 [L1196] JMP      A=31 B=128 C=30 D=32798 target=551
00521 [L1197] GGET     A=31 B=0 C=11 D=11 'd_ms'
00522 [L1197] TGETS    A=31 B=31 C=79 D=8015 'd_hz'
00523 [L1197] TGETS    A=31 B=31 C=80 D=8016 'gethz'
00524 [L1197] KSTR     A=32 B=0 C=95 D=95 'skill_up_level'
00525 [L1197] CALL     A=31 B=2 C=2 D=514 
00526 [L1197] KSTR     A=32 B=0 C=90 D=90 ': '
00527 [L1197] TGETS    A=33 B=0 C=45 D=45 'csvInfo'
00528 [L1197] TGETS    A=33 B=33 C=94 D=8542 'show_level'
00529 [L1197] CAT      A=31 B=31 C=33 D=7969 
00530 [L1198] GGET     A=32 B=0 C=11 D=11 'd_ms'
00531 [L1198] TGETS    A=32 B=32 C=12 D=8204 'd_u'
00532 [L1198] TGETS    A=32 B=32 C=67 D=8259 'createByStyle'
00533 [L1198] TDUP     A=33 B=0 C=96 D=96 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 30}}
00534 [L1198] TSETS    A=31 B=33 C=70 D=8518 'string'
00535 [L1198] MULNV    A=34 B=29 C=11 D=7435 
00536 [L1198] SUBNV    A=34 B=34 C=12 D=8716 
00537 [L1198] TSETS    A=34 B=33 C=30 D=8478 'x'
00538 [L1198] MULVN    A=34 B=30 C=6 D=7686 
00539 [L1198] SUBNV    A=34 B=34 C=13 D=8717 
00540 [L1198] TSETS    A=34 B=33 C=32 D=8480 'y'
00541 [L1199] TSETS    A=28 B=33 C=76 D=8524 'color'
00542 [L1199] TDUP     A=34 B=0 C=97 D=97 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00543 [L1199] TSETS    A=34 B=33 C=93 D=8541 'anchor'
00544 [L1198] CALL     A=32 B=2 C=2 D=514 
00545 [L1200] MOV      A=34 B=0 C=18 D=18 
00546 [L1200] TGETS    A=33 B=18 C=7 D=4615 'addChild'
00547 [L1200] MOV      A=35 B=0 C=32 D=32 
00548 [L1200] KSHORT   A=36 B=0 C=10 D=10 10
00549 [L1200] CALL     A=33 B=1 C=4 D=260 
00550 [L1201] ADDVN    A=30 B=30 C=14 D=7694 
00551 [L1203] TGETS    A=31 B=0 C=45 D=45 'csvInfo'
00552 [L1203] ISF      A=0 B=0 C=31 D=31 
00553 [L1203] JMP      A=32 B=128 C=39 D=32807 target=593
00554 [L1203] TGETS    A=31 B=0 C=45 D=45 'csvInfo'
00555 [L1203] TGETS    A=31 B=31 C=98 D=8034 'base_experience_plus'
00556 [L1203] ISF      A=0 B=0 C=31 D=31 
00557 [L1203] JMP      A=32 B=128 C=35 D=32803 target=593
00558 [L1203] TGETS    A=31 B=0 C=45 D=45 'csvInfo'
00559 [L1203] TGETS    A=31 B=31 C=98 D=8034 'base_experience_plus'
00560 [L1203] KSHORT   A=32 B=0 C=0 D=0 0
00561 [L1203] ISGE     A=32 B=0 C=31 D=31 
00562 [L1203] JMP      A=31 B=128 C=30 D=32798 target=593
00563 [L1204] GGET     A=31 B=0 C=11 D=11 'd_ms'
00564 [L1204] TGETS    A=31 B=31 C=79 D=8015 'd_hz'
00565 [L1204] TGETS    A=31 B=31 C=80 D=8016 'gethz'
00566 [L1204] KSTR     A=32 B=0 C=99 D=99 'exp'
00567 [L1204] CALL     A=31 B=2 C=2 D=514 
00568 [L1204] KSTR     A=32 B=0 C=90 D=90 ': '
00569 [L1204] TGETS    A=33 B=0 C=45 D=45 'csvInfo'
00570 [L1204] TGETS    A=33 B=33 C=98 D=8546 'base_experience_plus'
00571 [L1204] CAT      A=31 B=31 C=33 D=7969 
00572 [L1205] GGET     A=32 B=0 C=11 D=11 'd_ms'
00573 [L1205] TGETS    A=32 B=32 C=12 D=8204 'd_u'
00574 [L1205] TGETS    A=32 B=32 C=67 D=8259 'createByStyle'
00575 [L1205] TDUP     A=33 B=0 C=100 D=100 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 30}}
00576 [L1205] TSETS    A=31 B=33 C=70 D=8518 'string'
00577 [L1205] MULNV    A=34 B=29 C=11 D=7435 
00578 [L1205] SUBNV    A=34 B=34 C=12 D=8716 
00579 [L1205] TSETS    A=34 B=33 C=30 D=8478 'x'
00580 [L1205] MULVN    A=34 B=30 C=6 D=7686 
00581 [L1205] SUBNV    A=34 B=34 C=13 D=8717 
00582 [L1205] TSETS    A=34 B=33 C=32 D=8480 'y'
00583 [L1206] TSETS    A=28 B=33 C=76 D=8524 'color'
00584 [L1206] TDUP     A=34 B=0 C=101 D=101 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00585 [L1206] TSETS    A=34 B=33 C=93 D=8541 'anchor'
00586 [L1205] CALL     A=32 B=2 C=2 D=514 
00587 [L1207] MOV      A=34 B=0 C=18 D=18 
00588 [L1207] TGETS    A=33 B=18 C=7 D=4615 'addChild'
00589 [L1207] MOV      A=35 B=0 C=32 D=32 
00590 [L1207] KSHORT   A=36 B=0 C=10 D=10 10
00591 [L1207] CALL     A=33 B=1 C=4 D=260 
00592 [L1208] ADDVN    A=30 B=30 C=14 D=7694 
00593 [L1211] TGETS    A=31 B=0 C=45 D=45 'csvInfo'
00594 [L1211] ISF      A=0 B=0 C=31 D=31 
00595 [L1211] JMP      A=32 B=128 C=36 D=32804 target=632
00596 [L1211] TGETS    A=31 B=0 C=45 D=45 'csvInfo'
00597 [L1211] TGETS    A=31 B=31 C=59 D=7995 'mainType'
00598 [L1211] UGET     A=32 B=0 C=11 D=11 m_t
00599 [L1211] TGETS    A=32 B=32 C=102 D=8294 'ext_skill'
00600 [L1211] ISNEV    A=31 B=0 C=32 D=32 
00601 [L1211] JMP      A=31 B=128 C=30 D=32798 target=632
00602 [L1212] TGETS    A=31 B=0 C=77 D=77 'level'
00603 [L1212] IST      A=0 B=0 C=31 D=31 
00604 [L1212] JMP      A=32 B=128 C=1 D=32769 target=606
00605 [L1212] KSHORT   A=31 B=0 C=1 D=1 1
00606 [L1214] MOV      A=33 B=0 C=18 D=18 
00607 [L1214] TGETS    A=32 B=18 C=7 D=4615 'addChild'
00608 [L1214] GGET     A=34 B=0 C=11 D=11 'd_ms'
00609 [L1214] TGETS    A=34 B=34 C=12 D=8716 'd_u'
00610 [L1214] TGETS    A=34 B=34 C=67 D=8771 'createByStyle'
00611 [L1214] TDUP     A=35 B=0 C=103 D=103 {'kind': 'table', 'value': {'pic': 'v2/introUI/level.png', 'x': 0.56, 'y': 0.63}}
00612 [L1214] CALL     A=34 B=0 C=2 D=2 
00613 [L1214] CALLM    A=32 B=1 C=1 D=257 
00614 [L1215] MOV      A=33 B=0 C=18 D=18 
00615 [L1215] TGETS    A=32 B=18 C=7 D=4615 'addChild'
00616 [L1215] GGET     A=34 B=0 C=11 D=11 'd_ms'
00617 [L1215] TGETS    A=34 B=34 C=12 D=8716 'd_u'
00618 [L1215] TGETS    A=34 B=34 C=67 D=8771 'createByStyle'
00619 [L1215] TDUP     A=35 B=0 C=104 D=104 {'kind': 'table', 'value': {'font': 'arial', 'y': 0.63, 'type': 'label', 'x': 0.59, 'fontsize': 26}}
00620 [L1215] UGET     A=36 B=0 C=13 D=13 tostring
00621 [L1215] TGETS    A=37 B=0 C=77 D=77 'level'
00622 [L1215] IST      A=0 B=0 C=37 D=37 
00623 [L1215] JMP      A=38 B=128 C=1 D=32769 target=625
00624 [L1215] KSHORT   A=37 B=0 C=1 D=1 1
00625 [L1215] CALL     A=36 B=2 C=2 D=514 
00626 [L1215] TSETS    A=36 B=35 C=70 D=9030 'string'
00627 [L1215] TDUP     A=36 B=0 C=105 D=105 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00628 [L1215] TSETS    A=36 B=35 C=93 D=9053 'anchor'
00629 [L1215] TSETS    A=4 B=35 C=76 D=9036 'color'
00630 [L1215] CALL     A=34 B=0 C=2 D=2 
00631 [L1215] CALLM    A=32 B=1 C=1 D=257 
00632 [L1218] TGETS    A=31 B=0 C=45 D=45 'csvInfo'
00633 [L1218] TGETS    A=31 B=31 C=59 D=7995 'mainType'
00634 [L1218] UGET     A=32 B=0 C=11 D=11 m_t
00635 [L1218] TGETS    A=32 B=32 C=60 D=8252 'awaken_star'
00636 [L1218] ISNEV    A=31 B=0 C=32 D=32 
00637 [L1218] JMP      A=31 B=134 C=110 D=34414 target=2284
00638 [L1219] ISF      A=0 B=0 C=2 D=2 
00639 [L1219] JMP      A=31 B=128 C=13 D=32781 target=653
00640 [L1220] MOV      A=32 B=0 C=18 D=18 
00641 [L1220] TGETS    A=31 B=18 C=7 D=4615 'addChild'
00642 [L1220] GGET     A=33 B=0 C=11 D=11 'd_ms'
00643 [L1220] TGETS    A=33 B=33 C=12 D=8460 'd_u'
00644 [L1220] TGETS    A=33 B=33 C=67 D=8515 'createByStyle'
00645 [L1220] TDUP     A=34 B=0 C=106 D=106 {'kind': 'table', 'value': {'y': 0.3, 'type': 'label', 'x': 0.5, 'fontsize': 26}}
00646 [L1220] UGET     A=35 B=0 C=15 D=15 gethz
00647 [L1220] KSTR     A=36 B=0 C=107 D=107 'wake35'
00648 [L1220] CALL     A=35 B=2 C=2 D=514 
00649 [L1220] TSETS    A=35 B=34 C=70 D=8774 'string'
00650 [L1220] TSETS    A=4 B=34 C=76 D=8780 'color'
00651 [L1220] CALL     A=33 B=0 C=2 D=2 
00652 [L1220] CALLM    A=31 B=1 C=1 D=257 
00653 [L1222] GGET     A=31 B=0 C=108 D=108 'addStarLockInfo'
00654 [L1222] MOV      A=32 B=0 C=6 D=6 
00655 [L1222] MOV      A=33 B=0 C=0 D=0 
00656 [L1222] MOV      A=34 B=0 C=2 D=2 
00657 [L1222] CALL     A=31 B=1 C=4 D=260 
00658 [L1223] JMP      A=28 B=134 C=89 D=34393 target=2284
00659 [L1225] GGET     A=28 B=0 C=54 D=54 'packageTagDef'
00660 [L1225] TGETS    A=28 B=28 C=56 D=7224 'skill'
00661 [L1225] ISEQV    A=23 B=0 C=28 D=28 
00662 [L1225] JMP      A=28 B=128 C=4 D=32772 target=667
00663 [L1225] GGET     A=28 B=0 C=54 D=54 'packageTagDef'
00664 [L1225] TGETS    A=28 B=28 C=57 D=7225 'stone'
00665 [L1225] ISNEV    A=23 B=0 C=28 D=28 
00666 [L1225] JMP      A=28 B=129 C=141 D=33165 target=1064
00667 [L1227] TGETS    A=28 B=0 C=61 D=61 'upgrade_level'
00668 [L1227] ISF      A=0 B=0 C=28 D=28 
00669 [L1227] JMP      A=29 B=128 C=31 D=32799 target=701
00670 [L1227] TGETS    A=28 B=0 C=61 D=61 'upgrade_level'
00671 [L1227] KSHORT   A=29 B=0 C=0 D=0 0
00672 [L1227] ISGE     A=29 B=0 C=28 D=28 
00673 [L1227] JMP      A=28 B=128 C=27 D=32795 target=701
00674 [L1228] MOV      A=29 B=0 C=18 D=18 
00675 [L1228] TGETS    A=28 B=18 C=7 D=4615 'addChild'
00676 [L1228] GGET     A=30 B=0 C=11 D=11 'd_ms'
00677 [L1228] TGETS    A=30 B=30 C=12 D=7692 'd_u'
00678 [L1228] TGETS    A=30 B=30 C=67 D=7747 'createByStyle'
00679 [L1228] TDUP     A=31 B=0 C=109 D=109 {'kind': 'table', 'value': {'pic': 'v2/introUI/level.png', 'x': 0.5, 'y': 0.74}}
00680 [L1228] CALL     A=30 B=0 C=2 D=2 
00681 [L1228] CALLM    A=28 B=1 C=1 D=257 
00682 [L1229] MOV      A=29 B=0 C=18 D=18 
00683 [L1229] TGETS    A=28 B=18 C=7 D=4615 'addChild'
00684 [L1229] GGET     A=30 B=0 C=11 D=11 'd_ms'
00685 [L1229] TGETS    A=30 B=30 C=12 D=7692 'd_u'
00686 [L1229] TGETS    A=30 B=30 C=67 D=7747 'createByStyle'
00687 [L1229] TDUP     A=31 B=0 C=110 D=110 {'kind': 'table', 'value': {'font': 'arial', 'y': 0.74, 'type': 'label', 'x': 0.53, 'fontsize': 26}}
00688 [L1229] UGET     A=32 B=0 C=13 D=13 tostring
00689 [L1229] TGETS    A=33 B=0 C=77 D=77 'level'
00690 [L1229] IST      A=0 B=0 C=33 D=33 
00691 [L1229] JMP      A=34 B=128 C=1 D=32769 target=693
00692 [L1229] KSHORT   A=33 B=0 C=1 D=1 1
00693 [L1229] CALL     A=32 B=2 C=2 D=514 
00694 [L1229] TSETS    A=32 B=31 C=70 D=8006 'string'
00695 [L1229] TDUP     A=32 B=0 C=111 D=111 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00696 [L1229] TSETS    A=32 B=31 C=93 D=8029 'anchor'
00697 [L1229] TSETS    A=4 B=31 C=76 D=8012 'color'
00698 [L1229] CALL     A=30 B=0 C=2 D=2 
00699 [L1229] CALLM    A=28 B=1 C=1 D=257 
00700 [L1229] JMP      A=28 B=128 C=34 D=32802 target=735
00701 [L1231] GGET     A=28 B=0 C=54 D=54 'packageTagDef'
00702 [L1231] TGETS    A=28 B=28 C=57 D=7225 'stone'
00703 [L1231] ISNEV    A=23 B=0 C=28 D=28 
00704 [L1231] JMP      A=28 B=128 C=4 D=32772 target=709
00705 [L1231] TGETS    A=28 B=0 C=77 D=77 'level'
00706 [L1231] KSHORT   A=29 B=0 C=10 D=10 10
00707 [L1231] ISLT     A=29 B=0 C=28 D=28 
00708 [L1231] JMP      A=28 B=128 C=26 D=32794 target=735
00709 [L1232] MOV      A=29 B=0 C=18 D=18 
00710 [L1232] TGETS    A=28 B=18 C=7 D=4615 'addChild'
00711 [L1232] GGET     A=30 B=0 C=11 D=11 'd_ms'
00712 [L1232] TGETS    A=30 B=30 C=12 D=7692 'd_u'
00713 [L1232] TGETS    A=30 B=30 C=67 D=7747 'createByStyle'
00714 [L1232] TDUP     A=31 B=0 C=112 D=112 {'kind': 'table', 'value': {'pic': 'v2/introUI/level.png', 'x': 0.52, 'y': 0.7}}
00715 [L1232] CALL     A=30 B=0 C=2 D=2 
00716 [L1232] CALLM    A=28 B=1 C=1 D=257 
00717 [L1233] MOV      A=29 B=0 C=18 D=18 
00718 [L1233] TGETS    A=28 B=18 C=7 D=4615 'addChild'
00719 [L1233] GGET     A=30 B=0 C=11 D=11 'd_ms'
00720 [L1233] TGETS    A=30 B=30 C=12 D=7692 'd_u'
00721 [L1233] TGETS    A=30 B=30 C=67 D=7747 'createByStyle'
00722 [L1233] TDUP     A=31 B=0 C=113 D=113 {'kind': 'table', 'value': {'font': 'arial', 'y': 0.7, 'type': 'label', 'x': 0.54, 'fontsize': 26}}
00723 [L1233] UGET     A=32 B=0 C=13 D=13 tostring
00724 [L1233] TGETS    A=33 B=0 C=77 D=77 'level'
00725 [L1233] IST      A=0 B=0 C=33 D=33 
00726 [L1233] JMP      A=34 B=128 C=1 D=32769 target=728
00727 [L1233] KSHORT   A=33 B=0 C=1 D=1 1
00728 [L1233] CALL     A=32 B=2 C=2 D=514 
00729 [L1233] TSETS    A=32 B=31 C=70 D=8006 'string'
00730 [L1233] TDUP     A=32 B=0 C=114 D=114 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00731 [L1233] TSETS    A=32 B=31 C=93 D=8029 'anchor'
00732 [L1233] TSETS    A=4 B=31 C=76 D=8012 'color'
00733 [L1233] CALL     A=30 B=0 C=2 D=2 
00734 [L1233] CALLM    A=28 B=1 C=1 D=257 
00735 [L1236] GGET     A=28 B=0 C=54 D=54 'packageTagDef'
00736 [L1236] TGETS    A=28 B=28 C=56 D=7224 'skill'
00737 [L1236] ISNEV    A=23 B=0 C=28 D=28 
00738 [L1236] JMP      A=28 B=128 C=125 D=32893 target=864
00739 [L1237] MOV      A=28 B=0 C=4 D=4 
00740 [L1239] GGET     A=29 B=0 C=11 D=11 'd_ms'
00741 [L1239] TGETS    A=29 B=29 C=115 D=7539 'd_wakeUI'
00742 [L1239] TGETS    A=29 B=29 C=116 D=7540 'isAwaken'
00743 [L1239] TGETS    A=30 B=0 C=117 D=117 'awaken'
00744 [L1239] CALL     A=29 B=2 C=2 D=514 
00745 [L1239] ISF      A=0 B=0 C=29 D=29 
00746 [L1239] JMP      A=30 B=128 C=1 D=32769 target=748
00747 [L1240] TDUP     A=28 B=0 C=118 D=118 {'kind': 'table', 'value': {1: 0, 2: 255, 3: 0}}
00748 [L1243] TGETS    A=29 B=0 C=61 D=61 'upgrade_level'
00749 [L1243] ISF      A=0 B=0 C=29 D=29 
00750 [L1243] JMP      A=30 B=128 C=27 D=32795 target=778
00751 [L1243] TGETS    A=29 B=0 C=61 D=61 'upgrade_level'
00752 [L1243] KSHORT   A=30 B=0 C=0 D=0 0
00753 [L1243] ISGE     A=30 B=0 C=29 D=29 
00754 [L1243] JMP      A=29 B=128 C=23 D=32791 target=778
00755 [L1244] GGET     A=29 B=0 C=119 D=119 'createSkillLabel'
00756 [L1244] MOV      A=30 B=0 C=18 D=18 
00757 [L1244] TGETS    A=31 B=0 C=120 D=120 'type_id'
00758 [L1244] IST      A=0 B=0 C=31 D=31 
00759 [L1244] JMP      A=32 B=128 C=2 D=32770 target=762
00760 [L1244] TGETS    A=31 B=0 C=121 D=121 'buyInfo'
00761 [L1244] TGETS    A=31 B=31 C=120 D=8056 'type_id'
00762 [L1244] GGET     A=32 B=0 C=11 D=11 'd_ms'
00763 [L1244] TGETS    A=32 B=32 C=12 D=8204 'd_u'
00764 [L1244] TGETS    A=32 B=32 C=122 D=8314 'makePoint'
00765 [L1244] KNUM     A=33 B=0 C=8 D=8 0.5
00766 [L1244] KNUM     A=34 B=0 C=9 D=9 0.68
00767 [L1244] CALL     A=32 B=2 C=3 D=515 
00768 [L1244] TGETS    A=33 B=0 C=77 D=77 'level'
00769 [L1244] MOV      A=34 B=0 C=28 D=28 
00770 [L1244] GGET     A=35 B=0 C=11 D=11 'd_ms'
00771 [L1244] TGETS    A=35 B=35 C=115 D=9075 'd_wakeUI'
00772 [L1244] TGETS    A=35 B=35 C=116 D=9076 'isAwaken'
00773 [L1244] TGETS    A=36 B=0 C=117 D=117 'awaken'
00774 [L1244] CALL     A=35 B=2 C=2 D=514 
00775 [L1244] TGETS    A=36 B=0 C=123 D=123 'effect_value'
00776 [L1244] CALL     A=29 B=1 C=8 D=264 
00777 [L1244] JMP      A=29 B=128 C=22 D=32790 target=800
00778 [L1246] GGET     A=29 B=0 C=119 D=119 'createSkillLabel'
00779 [L1246] MOV      A=30 B=0 C=18 D=18 
00780 [L1246] TGETS    A=31 B=0 C=120 D=120 'type_id'
00781 [L1246] IST      A=0 B=0 C=31 D=31 
00782 [L1246] JMP      A=32 B=128 C=2 D=32770 target=785
00783 [L1246] TGETS    A=31 B=0 C=121 D=121 'buyInfo'
00784 [L1246] TGETS    A=31 B=31 C=120 D=8056 'type_id'
00785 [L1246] GGET     A=32 B=0 C=11 D=11 'd_ms'
00786 [L1246] TGETS    A=32 B=32 C=12 D=8204 'd_u'
00787 [L1246] TGETS    A=32 B=32 C=122 D=8314 'makePoint'
00788 [L1246] KNUM     A=33 B=0 C=15 D=15 0.62
00789 [L1246] KNUM     A=34 B=0 C=13 D=13 0.7
00790 [L1246] CALL     A=32 B=2 C=3 D=515 
00791 [L1246] TGETS    A=33 B=0 C=77 D=77 'level'
00792 [L1246] MOV      A=34 B=0 C=28 D=28 
00793 [L1246] GGET     A=35 B=0 C=11 D=11 'd_ms'
00794 [L1246] TGETS    A=35 B=35 C=115 D=9075 'd_wakeUI'
00795 [L1246] TGETS    A=35 B=35 C=116 D=9076 'isAwaken'
00796 [L1246] TGETS    A=36 B=0 C=117 D=117 'awaken'
00797 [L1246] CALL     A=35 B=2 C=2 D=514 
00798 [L1246] TGETS    A=36 B=0 C=123 D=123 'effect_value'
00799 [L1246] CALL     A=29 B=1 C=8 D=264 
00800 [L1249] TGETS    A=29 B=0 C=120 D=120 'type_id'
00801 [L1249] ISNEN    A=29 B=0 C=16 D=16 21
00802 [L1249] JMP      A=29 B=128 C=136 D=32904 target=939
00803 [L1250] GGET     A=29 B=0 C=11 D=11 'd_ms'
00804 [L1250] TGETS    A=29 B=29 C=124 D=7548 'd_skillUpgradeUI'
00805 [L1250] TGETS    A=29 B=29 C=125 D=7549 'initSkillCsv'
00806 [L1250] CALL     A=29 B=1 C=1 D=257 
00807 [L1251] GGET     A=29 B=0 C=11 D=11 'd_ms'
00808 [L1251] TGETS    A=29 B=29 C=124 D=7548 'd_skillUpgradeUI'
00809 [L1251] TGETS    A=29 B=29 C=126 D=7550 'g_self'
00810 [L1251] TGETS    A=29 B=29 C=127 D=7551 'csv_map_rulai_skill'
00811 [L1251] TGETS    A=30 B=0 C=77 D=77 'level'
00812 [L1251] TGETV    A=29 B=29 C=30 D=7454 
00813 [L1251] TGETB    A=29 B=29 C=3 D=7427 
00814 [L1252] TDUP     A=30 B=0 C=128 D=128 {'kind': 'table', 'value': {1: 255, 2: 255, 3: 255}}
00815 [L1253] GGET     A=31 B=0 C=11 D=11 'd_ms'
00816 [L1253] TGETS    A=31 B=31 C=115 D=8051 'd_wakeUI'
00817 [L1253] TGETS    A=31 B=31 C=116 D=8052 'isAwaken'
00818 [L1253] TGETS    A=32 B=0 C=117 D=117 'awaken'
00819 [L1253] CALL     A=31 B=2 C=2 D=514 
00820 [L1253] ISF      A=0 B=0 C=31 D=31 
00821 [L1253] JMP      A=32 B=128 C=14 D=32782 target=836
00822 [L1254] GGET     A=31 B=0 C=11 D=11 'd_ms'
00823 [L1254] TGETS    A=31 B=31 C=115 D=8051 'd_wakeUI'
00824 [L1254] TGETS    A=31 B=31 C=129 D=8065 'initCsv'
00825 [L1254] CALL     A=31 B=1 C=1 D=257 
00826 [L1255] GGET     A=31 B=0 C=11 D=11 'd_ms'
00827 [L1255] TGETS    A=31 B=31 C=115 D=8051 'd_wakeUI'
00828 [L1255] TGETS    A=31 B=31 C=130 D=8066 'g_csv'
00829 [L1255] TGETS    A=31 B=31 C=131 D=8067 'rate'
00830 [L1255] TGETS    A=32 B=0 C=120 D=120 'type_id'
00831 [L1255] TGETV    A=31 B=31 C=32 D=7968 
00832 [L1255] DIVVN    A=31 B=31 C=17 D=7953 
00833 [L1255] ADDNV    A=31 B=31 C=14 D=7950 
00834 [L1255] MULVV    A=29 B=29 C=31 D=7455 
00835 [L1256] TDUP     A=30 B=0 C=132 D=132 {'kind': 'table', 'value': {1: 0, 2: 255, 3: 0}}
00836 [L1258] UGET     A=31 B=0 C=16 D=16 string
00837 [L1258] TGETS    A=31 B=31 C=133 D=8069 'format'
00838 [L1258] KSTR     A=32 B=0 C=134 D=134 '%0.1f'
00839 [L1258] MOV      A=33 B=0 C=29 D=29 
00840 [L1258] CALL     A=31 B=2 C=3 D=515 
00841 [L1258] KSTR     A=32 B=0 C=69 D=69 '%'
00842 [L1258] CAT      A=31 B=31 C=32 D=7968 
00843 [L1259] MOV      A=33 B=0 C=18 D=18 
00844 [L1259] TGETS    A=32 B=18 C=7 D=4615 'addChild'
00845 [L1259] GGET     A=34 B=0 C=11 D=11 'd_ms'
00846 [L1259] TGETS    A=34 B=34 C=12 D=8716 'd_u'
00847 [L1259] TGETS    A=34 B=34 C=67 D=8771 'createByStyle'
00848 [L1259] TDUP     A=35 B=0 C=135 D=135 {'kind': 'table', 'value': {'pic': 'v2/introUI/dun.png', 'x': 0.62, 'y': 0.63}}
00849 [L1259] CALL     A=34 B=0 C=2 D=2 
00850 [L1259] CALLM    A=32 B=1 C=1 D=257 
00851 [L1260] MOV      A=33 B=0 C=18 D=18 
00852 [L1260] TGETS    A=32 B=18 C=7 D=4615 'addChild'
00853 [L1260] GGET     A=34 B=0 C=11 D=11 'd_ms'
00854 [L1260] TGETS    A=34 B=34 C=12 D=8716 'd_u'
00855 [L1260] TGETS    A=34 B=34 C=67 D=8771 'createByStyle'
00856 [L1260] TDUP     A=35 B=0 C=136 D=136 {'kind': 'table', 'value': {'font': 'arial', 'y': 0.63, 'type': 'label', 'x': 0.64, 'fontsize': 26}}
00857 [L1260] TSETS    A=31 B=35 C=70 D=9030 'string'
00858 [L1260] TDUP     A=36 B=0 C=137 D=137 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00859 [L1260] TSETS    A=36 B=35 C=93 D=9053 'anchor'
00860 [L1260] TSETS    A=30 B=35 C=76 D=9036 'color'
00861 [L1260] CALL     A=34 B=0 C=2 D=2 
00862 [L1260] CALLM    A=32 B=1 C=1 D=257 
00863 [L1261] JMP      A=28 B=128 C=75 D=32843 target=939
00864 [L1264] TGETS    A=28 B=0 C=45 D=45 'csvInfo'
00865 [L1264] TGETS    A=28 B=28 C=82 D=7250 'sub_type'
00866 [L1265] KNUM     A=29 B=0 C=15 D=15 0.62
00867 [L1266] GGET     A=30 B=0 C=54 D=54 'packageTagDef'
00868 [L1266] TGETS    A=30 B=30 C=57 D=7737 'stone'
00869 [L1266] ISNEV    A=23 B=0 C=30 D=30 
00870 [L1266] JMP      A=30 B=128 C=5 D=32773 target=876
00871 [L1266] TGETS    A=30 B=0 C=77 D=77 'level'
00872 [L1266] KSHORT   A=31 B=0 C=10 D=10 10
00873 [L1266] ISGE     A=31 B=0 C=30 D=30 
00874 [L1266] JMP      A=30 B=128 C=1 D=32769 target=876
00875 [L1267] KNUM     A=29 B=0 C=18 D=18 0.55
00876 [L1269] MOV      A=31 B=0 C=18 D=18 
00877 [L1269] TGETS    A=30 B=18 C=7 D=4615 'addChild'
00878 [L1269] GGET     A=32 B=0 C=11 D=11 'd_ms'
00879 [L1269] TGETS    A=32 B=32 C=12 D=8204 'd_u'
00880 [L1269] TGETS    A=32 B=32 C=67 D=8259 'createByStyle'
00881 [L1269] TDUP     A=33 B=0 C=138 D=138 {'kind': 'table', 'value': {'y': 0.7}}
00882 [L1269] TGETV    A=34 B=24 C=28 D=6172 
00883 [L1269] TSETS    A=34 B=33 C=139 D=8587 'pic'
00884 [L1269] TSETS    A=29 B=33 C=30 D=8478 'x'
00885 [L1269] CALL     A=32 B=0 C=2 D=2 
00886 [L1269] CALLM    A=30 B=1 C=1 D=257 
00887 [L1270] KPRI     A=30 B=0 C=0 D=0 
00888 [L1271] TGETS    A=31 B=0 C=77 D=77 'level'
00889 [L1271] ISF      A=0 B=0 C=31 D=31 
00890 [L1271] JMP      A=32 B=128 C=17 D=32785 target=908
00891 [L1271] TGETS    A=31 B=0 C=77 D=77 'level'
00892 [L1271] KSHORT   A=32 B=0 C=10 D=10 10
00893 [L1271] ISGE     A=32 B=0 C=31 D=31 
00894 [L1271] JMP      A=31 B=128 C=13 D=32781 target=908
00895 [L1272] GGET     A=31 B=0 C=11 D=11 'd_ms'
00896 [L1272] TGETS    A=31 B=31 C=140 D=8076 'd_stoneCastUI'
00897 [L1272] TGETS    A=31 B=31 C=141 D=8077 'initConfig'
00898 [L1272] CALL     A=31 B=1 C=1 D=257 
00899 [L1273] GGET     A=31 B=0 C=11 D=11 'd_ms'
00900 [L1273] TGETS    A=31 B=31 C=140 D=8076 'd_stoneCastUI'
00901 [L1273] TGETS    A=31 B=31 C=126 D=8062 'g_self'
00902 [L1273] TGETS    A=31 B=31 C=142 D=8078 'csv'
00903 [L1273] TGETV    A=31 B=31 C=28 D=7964 
00904 [L1273] TGETS    A=32 B=0 C=77 D=77 'level'
00905 [L1273] TGETV    A=31 B=31 C=32 D=7968 
00906 [L1273] TGETS    A=30 B=31 C=143 D=8079 'plus'
00907 [L1273] JMP      A=31 B=128 C=10 D=32778 target=918
00908 [L1275] GGET     A=31 B=0 C=11 D=11 'd_ms'
00909 [L1275] TGETS    A=31 B=31 C=144 D=8080 'd_data'
00910 [L1275] TGETS    A=31 B=31 C=145 D=8081 'g_stoneAttrTable'
00911 [L1275] TGETV    A=31 B=31 C=28 D=7964 
00912 [L1275] TGETS    A=32 B=0 C=77 D=77 'level'
00913 [L1275] IST      A=0 B=0 C=32 D=32 
00914 [L1275] JMP      A=33 B=128 C=1 D=32769 target=916
00915 [L1275] KSHORT   A=32 B=0 C=1 D=1 1
00916 [L1275] TGETV    A=31 B=31 C=32 D=7968 
00917 [L1275] TGETS    A=30 B=31 C=146 D=8082 'base'
00918 [L1277] MOV      A=32 B=0 C=18 D=18 
00919 [L1277] TGETS    A=31 B=18 C=7 D=4615 'addChild'
00920 [L1277] GGET     A=33 B=0 C=11 D=11 'd_ms'
00921 [L1277] TGETS    A=33 B=33 C=12 D=8460 'd_u'
00922 [L1277] TGETS    A=33 B=33 C=67 D=8515 'createByStyle'
00923 [L1277] TDUP     A=34 B=0 C=147 D=147 {'kind': 'table', 'value': {'font': 'arial', 'y': 0.7, 'type': 'label', 'fontsize': 26}}
00924 [L1277] UGET     A=35 B=0 C=16 D=16 string
00925 [L1277] TGETS    A=35 B=35 C=133 D=9093 'format'
00926 [L1277] KSTR     A=36 B=0 C=148 D=148 '%.1f'
00927 [L1277] MULVN    A=37 B=30 C=17 D=7697 
00928 [L1277] CALL     A=35 B=2 C=3 D=515 
00929 [L1277] KSTR     A=36 B=0 C=69 D=69 '%'
00930 [L1277] CAT      A=35 B=35 C=36 D=8996 
00931 [L1277] TSETS    A=35 B=34 C=70 D=8774 'string'
00932 [L1277] TDUP     A=35 B=0 C=149 D=149 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00933 [L1277] TSETS    A=35 B=34 C=93 D=8797 'anchor'
00934 [L1277] TSETS    A=4 B=34 C=76 D=8780 'color'
00935 [L1277] ADDVN    A=35 B=29 C=19 D=7443 
00936 [L1277] TSETS    A=35 B=34 C=30 D=8734 'x'
00937 [L1277] CALL     A=33 B=0 C=2 D=2 
00938 [L1277] CALLM    A=31 B=1 C=1 D=257 
00939 [L1279] TGETS    A=28 B=0 C=61 D=61 'upgrade_level'
00940 [L1279] ISF      A=0 B=0 C=28 D=28 
00941 [L1279] JMP      A=29 B=128 C=4 D=32772 target=946
00942 [L1279] TGETS    A=28 B=0 C=61 D=61 'upgrade_level'
00943 [L1279] KSHORT   A=29 B=0 C=0 D=0 0
00944 [L1279] ISGE     A=29 B=0 C=28 D=28 
00945 [L1279] JMP      A=28 B=128 C=0 D=32768 target=946
00946 [L1283] ISF      A=0 B=0 C=2 D=2 
00947 [L1283] JMP      A=28 B=133 C=56 D=34104 target=2284
00948 [L1284] KPRI     A=28 B=0 C=0 D=0 
00949 [L1285] GGET     A=29 B=0 C=54 D=54 'packageTagDef'
00950 [L1285] TGETS    A=29 B=29 C=56 D=7480 'skill'
00951 [L1285] ISNEV    A=23 B=0 C=29 D=29 
00952 [L1285] JMP      A=29 B=128 C=53 D=32821 target=1006
00953 [L1286] TGETS    A=29 B=0 C=45 D=45 'csvInfo'
00954 [L1286] TGETS    A=29 B=29 C=46 D=7470 'quality'
00955 [L1286] ISNEN    A=29 B=0 C=20 D=20 5
00956 [L1286] JMP      A=29 B=133 C=47 D=34095 target=2284
00957 [L1286] GGET     A=29 B=0 C=11 D=11 'd_ms'
00958 [L1286] TGETS    A=29 B=29 C=124 D=7548 'd_skillUpgradeUI'
00959 [L1286] TGETS    A=29 B=29 C=150 D=7574 'isCanAdvance'
00960 [L1286] TGETS    A=30 B=0 C=120 D=120 'type_id'
00961 [L1286] CALL     A=29 B=2 C=2 D=514 
00962 [L1286] ISF      A=0 B=0 C=29 D=29 
00963 [L1286] JMP      A=30 B=133 C=40 D=34088 target=2284
00964 [L1287] UGET     A=29 B=0 C=6 D=6 CCMenuItemImage
00965 [L1287] MOV      A=30 B=0 C=29 D=29 
00966 [L1287] TGETS    A=29 B=29 C=3 D=7427 'create'
00967 [L1287] KSTR     A=31 B=0 C=151 D=151 'v2/enhanceUI/up_2.png'
00968 [L1287] KSTR     A=32 B=0 C=151 D=151 'v2/enhanceUI/up_2.png'
00969 [L1287] CALL     A=29 B=2 C=4 D=516 
00970 [L1287] MOV      A=28 B=0 C=29 D=29 
00971 [L1288] MOV      A=30 B=0 C=28 D=28 
00972 [L1288] TGETS    A=29 B=28 C=21 D=7189 'setTag'
00973 [L1288] GGET     A=31 B=0 C=22 D=22 'g_introButtonType'
00974 [L1288] TGETS    A=31 B=31 C=152 D=8088 'enhanceSkill'
00975 [L1288] CALL     A=29 B=1 C=3 D=259 
00976 [L1289] GGET     A=29 B=0 C=11 D=11 'd_ms'
00977 [L1289] TGETS    A=29 B=29 C=12 D=7436 'd_u'
00978 [L1289] TGETS    A=29 B=29 C=13 D=7437 'setStyles'
00979 [L1289] MOV      A=30 B=0 C=28 D=28 
00980 [L1289] TDUP     A=31 B=0 C=153 D=153 {'kind': 'table', 'value': {'x': 0.58, 'y': 0.6}}
00981 [L1289] CALL     A=29 B=1 C=3 D=259 
00982 [L1290] MOV      A=30 B=0 C=28 D=28 
00983 [L1290] TGETS    A=29 B=28 C=25 D=7193 'registerScriptTapHandler'
00984 [L1290] MOV      A=31 B=0 C=1 D=1 
00985 [L1290] CALL     A=29 B=1 C=3 D=259 
00986 [L1291] MOV      A=30 B=0 C=7 D=7 
00987 [L1291] TGETS    A=29 B=7 C=154 D=1946 'addObject'
00988 [L1291] MOV      A=31 B=0 C=28 D=28 
00989 [L1291] CALL     A=29 B=1 C=3 D=259 
00990 [L1292] TGETS    A=29 B=0 C=77 D=77 'level'
00991 [L1292] KSHORT   A=30 B=0 C=10 D=10 10
00992 [L1292] ISLT     A=29 B=0 C=30 D=30 
00993 [L1292] JMP      A=29 B=128 C=6 D=32774 target=1000
00994 [L1292] TGETS    A=29 B=0 C=61 D=61 'upgrade_level'
00995 [L1292] ISF      A=0 B=0 C=29 D=29 
00996 [L1292] JMP      A=29 B=128 C=3 D=32771 target=1000
00997 [L1292] TGETS    A=29 B=0 C=61 D=61 'upgrade_level'
00998 [L1292] ISEQN    A=29 B=0 C=4 D=4 0
00999 [L1292] JMP      A=29 B=133 C=4 D=34052 target=2284
01000 [L1293] GGET     A=29 B=0 C=11 D=11 'd_ms'
01001 [L1293] TGETS    A=29 B=29 C=12 D=7436 'd_u'
01002 [L1293] TGETS    A=29 B=29 C=155 D=7579 'grayMenuItem'
01003 [L1293] MOV      A=30 B=0 C=28 D=28 
01004 [L1293] CALL     A=29 B=1 C=2 D=258 
01005 [L1295] JMP      A=29 B=132 C=254 D=34046 target=2284
01006 [L1297] GGET     A=29 B=0 C=54 D=54 'packageTagDef'
01007 [L1297] TGETS    A=29 B=29 C=57 D=7481 'stone'
01008 [L1297] ISNEV    A=23 B=0 C=29 D=29 
01009 [L1297] JMP      A=29 B=128 C=11 D=32779 target=1021
01010 [L1297] TGETS    A=29 B=0 C=77 D=77 'level'
01011 [L1297] ISNEN    A=29 B=0 C=21 D=21 10
01012 [L1297] JMP      A=29 B=128 C=8 D=32776 target=1021
01013 [L1298] UGET     A=29 B=0 C=6 D=6 CCMenuItemImage
01014 [L1298] MOV      A=30 B=0 C=29 D=29 
01015 [L1298] TGETS    A=29 B=29 C=3 D=7427 'create'
01016 [L1298] KSTR     A=31 B=0 C=156 D=156 'v2/stoneCastUI/asc1.png'
01017 [L1298] KSTR     A=32 B=0 C=157 D=157 'v2/stoneCastUI/asc2.png'
01018 [L1298] CALL     A=29 B=2 C=4 D=516 
01019 [L1298] MOV      A=28 B=0 C=29 D=29 
01020 [L1298] JMP      A=29 B=128 C=23 D=32791 target=1044
01021 [L1299] GGET     A=29 B=0 C=54 D=54 'packageTagDef'
01022 [L1299] TGETS    A=29 B=29 C=57 D=7481 'stone'
01023 [L1299] ISNEV    A=23 B=0 C=29 D=29 
01024 [L1299] JMP      A=29 B=128 C=12 D=32780 target=1037
01025 [L1299] TGETS    A=29 B=0 C=77 D=77 'level'
01026 [L1299] KSHORT   A=30 B=0 C=11 D=11 11
01027 [L1299] ISGT     A=30 B=0 C=29 D=29 
01028 [L1299] JMP      A=29 B=128 C=8 D=32776 target=1037
01029 [L1300] UGET     A=29 B=0 C=6 D=6 CCMenuItemImage
01030 [L1300] MOV      A=30 B=0 C=29 D=29 
01031 [L1300] TGETS    A=29 B=29 C=3 D=7427 'create'
01032 [L1300] KSTR     A=31 B=0 C=158 D=158 'v2/stoneCastUI/tilian.png'
01033 [L1300] KSTR     A=32 B=0 C=159 D=159 'v2/stoneCastUI/tilian2.png'
01034 [L1300] CALL     A=29 B=2 C=4 D=516 
01035 [L1300] MOV      A=28 B=0 C=29 D=29 
01036 [L1300] JMP      A=29 B=128 C=7 D=32775 target=1044
01037 [L1302] UGET     A=29 B=0 C=6 D=6 CCMenuItemImage
01038 [L1302] MOV      A=30 B=0 C=29 D=29 
01039 [L1302] TGETS    A=29 B=29 C=3 D=7427 'create'
01040 [L1302] KSTR     A=31 B=0 C=160 D=160 'v2/newIntroUI/upgrade1.png'
01041 [L1302] KSTR     A=32 B=0 C=161 D=161 'v2/newIntroUI/upgrade2.png'
01042 [L1302] CALL     A=29 B=2 C=4 D=516 
01043 [L1302] MOV      A=28 B=0 C=29 D=29 
01044 [L1304] MOV      A=30 B=0 C=28 D=28 
01045 [L1304] TGETS    A=29 B=28 C=21 D=7189 'setTag'
01046 [L1304] GGET     A=31 B=0 C=22 D=22 'g_introButtonType'
01047 [L1304] TGETS    A=31 B=31 C=162 D=8098 'stoneUpgrade'
01048 [L1304] CALL     A=29 B=1 C=3 D=259 
01049 [L1305] GGET     A=29 B=0 C=11 D=11 'd_ms'
01050 [L1305] TGETS    A=29 B=29 C=12 D=7436 'd_u'
01051 [L1305] TGETS    A=29 B=29 C=13 D=7437 'setStyles'
01052 [L1305] MOV      A=30 B=0 C=28 D=28 
01053 [L1305] TDUP     A=31 B=0 C=163 D=163 {'kind': 'table', 'value': {'x': 0.58, 'y': 0.6}}
01054 [L1305] CALL     A=29 B=1 C=3 D=259 
01055 [L1306] MOV      A=30 B=0 C=28 D=28 
01056 [L1306] TGETS    A=29 B=28 C=25 D=7193 'registerScriptTapHandler'
01057 [L1306] MOV      A=31 B=0 C=1 D=1 
01058 [L1306] CALL     A=29 B=1 C=3 D=259 
01059 [L1307] MOV      A=30 B=0 C=7 D=7 
01060 [L1307] TGETS    A=29 B=7 C=154 D=1946 'addObject'
01061 [L1307] MOV      A=31 B=0 C=28 D=28 
01062 [L1307] CALL     A=29 B=1 C=3 D=259 
01063 [L1309] JMP      A=28 B=132 C=196 D=33988 target=2284
01064 [L1311] TGETS    A=28 B=0 C=77 D=77 'level'
01065 [L1311] IST      A=0 B=0 C=28 D=28 
01066 [L1311] JMP      A=29 B=128 C=1 D=32769 target=1068
01067 [L1311] KSHORT   A=28 B=0 C=1 D=1 1
01068 [L1312] TGETS    A=29 B=0 C=164 D=164 'advance_level'
01069 [L1312] IST      A=0 B=0 C=29 D=29 
01070 [L1312] JMP      A=30 B=128 C=1 D=32769 target=1072
01071 [L1312] KSHORT   A=29 B=0 C=0 D=0 0
01072 [L1313] TGETS    A=30 B=0 C=165 D=165 'star_count'
01073 [L1313] IST      A=0 B=0 C=30 D=30 
01074 [L1313] JMP      A=31 B=128 C=1 D=32769 target=1076
01075 [L1313] KSHORT   A=30 B=0 C=0 D=0 0
01076 [L1314] TGETS    A=31 B=0 C=166 D=166 'cur_spirit_count'
01077 [L1314] IST      A=0 B=0 C=31 D=31 
01078 [L1314] JMP      A=32 B=128 C=1 D=32769 target=1080
01079 [L1314] KSHORT   A=31 B=0 C=0 D=0 0
01080 [L1315] TGETS    A=32 B=0 C=167 D=167 'cast_level'
01081 [L1315] IST      A=0 B=0 C=32 D=32 
01082 [L1315] JMP      A=33 B=128 C=1 D=32769 target=1084
01083 [L1315] KSHORT   A=32 B=0 C=0 D=0 0
01084 [L1316] TGETS    A=33 B=0 C=50 D=50 'reborn_bit'
01085 [L1316] IST      A=0 B=0 C=33 D=33 
01086 [L1316] JMP      A=34 B=128 C=1 D=32769 target=1088
01087 [L1316] KSHORT   A=33 B=0 C=0 D=0 0
01088 [L1318] UGET     A=34 B=0 C=5 D=5 CCSprite
01089 [L1318] MOV      A=35 B=0 C=34 D=34 
01090 [L1318] TGETS    A=34 B=34 C=3 D=8707 'create'
01091 [L1318] KSTR     A=36 B=0 C=168 D=168 'v2/newIntroUI/big_bkg.png'
01092 [L1318] CALL     A=34 B=2 C=3 D=515 
01093 [L1319] GGET     A=35 B=0 C=11 D=11 'd_ms'
01094 [L1319] TGETS    A=35 B=35 C=12 D=8972 'd_u'
01095 [L1319] TGETS    A=35 B=35 C=13 D=8973 'setStyles'
01096 [L1319] MOV      A=36 B=0 C=34 D=34 
01097 [L1319] TDUP     A=37 B=0 C=170 D=170 {'kind': 'table', 'value': {'scale': 0.44296875, 'x': 0.5, 'y': 0.85}}
01098 [L1319] TDUP     A=38 B=0 C=169 D=169 {'kind': 'table', 'value': {1: 0.5, 2: 1}}
01099 [L1319] TSETS    A=38 B=37 C=93 D=9565 'anchor'
01100 [L1319] CALL     A=35 B=1 C=3 D=259 
01101 [L1320] MOV      A=36 B=0 C=18 D=18 
01102 [L1320] TGETS    A=35 B=18 C=7 D=4615 'addChild'
01103 [L1320] MOV      A=37 B=0 C=34 D=34 
01104 [L1320] CALL     A=35 B=1 C=3 D=259 
01105 [L1321] GGET     A=35 B=0 C=11 D=11 'd_ms'
01106 [L1321] TGETS    A=35 B=35 C=12 D=8972 'd_u'
01107 [L1321] TGETS    A=35 B=35 C=171 D=9131 'getRealScale'
01108 [L1321] MOV      A=36 B=0 C=34 D=34 
01109 [L1321] CALL     A=35 B=3 C=2 D=770 
01110 [L1322] ADDVN    A=27 B=36 C=19 D=9235 
01111 [L1324] MULNV    A=37 B=35 C=8 D=8968 
01112 [L1324] SUBNV    A=37 B=37 C=8 D=9480 
01113 [L1324] SUBNV    A=38 B=36 C=22 D=9238 
01114 [L1326] MOV      A=39 B=0 C=25 D=25 
01115 [L1326] CALL     A=39 B=2 C=1 D=513 
01116 [L1327] GGET     A=40 B=0 C=11 D=11 'd_ms'
01117 [L1327] TGETS    A=40 B=40 C=12 D=10252 'd_u'
01118 [L1327] TGETS    A=40 B=40 C=13 D=10253 'setStyles'
01119 [L1327] MOV      A=41 B=0 C=39 D=39 
01120 [L1327] TDUP     A=42 B=0 C=172 D=172 {'kind': 'table', 'value': {}}
01121 [L1327] MULNV    A=43 B=35 C=23 D=8983 
01122 [L1327] ADDVV    A=43 B=37 C=43 D=9515 
01123 [L1327] TSETS    A=43 B=42 C=30 D=10782 'x'
01124 [L1327] MULNV    A=43 B=36 C=24 D=9240 
01125 [L1327] ADDVV    A=43 B=38 C=43 D=9771 
01126 [L1327] TSETS    A=43 B=42 C=32 D=10784 'y'
01127 [L1327] MULNV    A=43 B=36 C=25 D=9241 
01128 [L1327] TSETS    A=43 B=42 C=173 D=10925 'scaleH'
01129 [L1327] CALL     A=40 B=1 C=3 D=259 
01130 [L1328] MOV      A=41 B=0 C=18 D=18 
01131 [L1328] TGETS    A=40 B=18 C=7 D=4615 'addChild'
01132 [L1328] MOV      A=42 B=0 C=39 D=39 
01133 [L1328] CALL     A=40 B=1 C=3 D=259 
01134 [L1330] GGET     A=40 B=0 C=11 D=11 'd_ms'
01135 [L1330] TGETS    A=40 B=40 C=144 D=10384 'd_data'
01136 [L1330] TGETS    A=40 B=40 C=174 D=10414 'getNameByTypeId'
01137 [L1330] UGET     A=41 B=0 C=17 D=17 o_t
01138 [L1330] TGETS    A=41 B=41 C=49 D=10545 'item'
01139 [L1330] TGETS    A=42 B=0 C=120 D=120 'type_id'
01140 [L1330] MOV      A=43 B=0 C=22 D=22 
01141 [L1330] CALL     A=40 B=2 C=4 D=516 
01142 [L1331] GGET     A=41 B=0 C=11 D=11 'd_ms'
01143 [L1331] TGETS    A=41 B=41 C=12 D=10508 'd_u'
01144 [L1331] TGETS    A=41 B=41 C=67 D=10563 'createByStyle'
01145 [L1331] TDUP     A=42 B=0 C=175 D=175 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 30}}
01146 [L1331] TSETS    A=40 B=42 C=70 D=10822 'string'
01147 [L1331] MULNV    A=43 B=35 C=25 D=8985 
01148 [L1331] ADDVV    A=43 B=37 C=43 D=9515 
01149 [L1331] TSETS    A=43 B=42 C=30 D=10782 'x'
01150 [L1331] MULNV    A=43 B=36 C=26 D=9242 
01151 [L1331] ADDVV    A=43 B=38 C=43 D=9771 
01152 [L1331] TSETS    A=43 B=42 C=32 D=10784 'y'
01153 [L1331] TDUP     A=43 B=0 C=176 D=176 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
01154 [L1331] TSETS    A=43 B=42 C=93 D=10845 'anchor'
01155 [L1331] TSETS    A=4 B=42 C=76 D=10828 'color'
01156 [L1331] CALL     A=41 B=2 C=2 D=514 
01157 [L1332] MOV      A=43 B=0 C=18 D=18 
01158 [L1332] TGETS    A=42 B=18 C=7 D=4615 'addChild'
01159 [L1332] MOV      A=44 B=0 C=41 D=41 
01160 [L1332] CALL     A=42 B=1 C=3 D=259 
01161 [L1333] KSHORT   A=42 B=0 C=0 D=0 0
01162 [L1333] ISGE     A=42 B=0 C=32 D=32 
01163 [L1333] JMP      A=42 B=128 C=31 D=32799 target=1195
01164 [L1333] KSHORT   A=42 B=0 C=5 D=5 5
01165 [L1333] ISGE     A=32 B=0 C=42 D=42 
01166 [L1333] JMP      A=42 B=128 C=28 D=32796 target=1195
01167 [L1334] GGET     A=42 B=0 C=11 D=11 'd_ms'
01168 [L1334] TGETS    A=42 B=42 C=12 D=10764 'd_u'
01169 [L1334] TGETS    A=42 B=42 C=171 D=10923 'getRealScale'
01170 [L1334] MOV      A=43 B=0 C=41 D=41 
01171 [L1334] CALL     A=42 B=2 C=2 D=514 
01172 [L1335] MOV      A=44 B=0 C=18 D=18 
01173 [L1335] TGETS    A=43 B=18 C=7 D=4615 'addChild'
01174 [L1335] GGET     A=45 B=0 C=11 D=11 'd_ms'
01175 [L1335] TGETS    A=45 B=45 C=12 D=11532 'd_u'
01176 [L1335] TGETS    A=45 B=45 C=67 D=11587 'createByStyle'
01177 [L1335] TDUP     A=46 B=0 C=179 D=179 {'kind': 'table', 'value': {}}
01178 [L1335] KSTR     A=47 B=0 C=177 D=177 'v2/ascCast/cast_lv'
01179 [L1335] MOV      A=48 B=0 C=32 D=32 
01180 [L1335] KSTR     A=49 B=0 C=178 D=178 '.png'
01181 [L1335] CAT      A=47 B=47 C=49 D=12081 
01182 [L1335] TSETS    A=47 B=46 C=139 D=11915 'pic'
01183 [L1335] MULNV    A=47 B=35 C=25 D=8985 
01184 [L1335] ADDVV    A=47 B=37 C=47 D=9519 
01185 [L1335] ADDVV    A=47 B=47 C=42 D=12074 
01186 [L1335] TSETS    A=47 B=46 C=30 D=11806 'x'
01187 [L1335] MULNV    A=47 B=36 C=26 D=9242 
01188 [L1335] ADDVV    A=47 B=38 C=47 D=9775 
01189 [L1335] TSETS    A=47 B=46 C=32 D=11808 'y'
01190 [L1335] TDUP     A=47 B=0 C=180 D=180 {'kind': 'table', 'value': {1: -0.1, 2: 0.5}}
01191 [L1335] TSETS    A=47 B=46 C=93 D=11869 'anchor'
01192 [L1335] CALL     A=45 B=0 C=2 D=2 
01193 [L1335] CALLM    A=43 B=1 C=1 D=257 
01194 [L1335] JMP      A=42 B=128 C=30 D=32798 target=1225
01195 [L1336] KSHORT   A=42 B=0 C=0 D=0 0
01196 [L1336] ISGE     A=42 B=0 C=29 D=29 
01197 [L1336] JMP      A=42 B=128 C=27 D=32795 target=1225
01198 [L1337] GGET     A=42 B=0 C=11 D=11 'd_ms'
01199 [L1337] TGETS    A=42 B=42 C=12 D=10764 'd_u'
01200 [L1337] TGETS    A=42 B=42 C=171 D=10923 'getRealScale'
01201 [L1337] MOV      A=43 B=0 C=41 D=41 
01202 [L1337] CALL     A=42 B=2 C=2 D=514 
01203 [L1338] MOV      A=44 B=0 C=18 D=18 
01204 [L1338] TGETS    A=43 B=18 C=7 D=4615 'addChild'
01205 [L1338] GGET     A=45 B=0 C=11 D=11 'd_ms'
01206 [L1338] TGETS    A=45 B=45 C=12 D=11532 'd_u'
01207 [L1338] TGETS    A=45 B=45 C=67 D=11587 'createByStyle'
01208 [L1338] TDUP     A=46 B=0 C=182 D=182 {'kind': 'table', 'value': {}}
01209 [L1338] KSTR     A=47 B=0 C=181 D=181 'v2/equipAdvanceUI/ad'
01210 [L1338] MOV      A=48 B=0 C=29 D=29 
01211 [L1338] KSTR     A=49 B=0 C=178 D=178 '.png'
01212 [L1338] CAT      A=47 B=47 C=49 D=12081 
01213 [L1338] TSETS    A=47 B=46 C=139 D=11915 'pic'
01214 [L1338] MULNV    A=47 B=35 C=25 D=8985 
01215 [L1338] ADDVV    A=47 B=37 C=47 D=9519 
01216 [L1338] ADDVV    A=47 B=47 C=42 D=12074 
01217 [L1338] TSETS    A=47 B=46 C=30 D=11806 'x'
01218 [L1338] MULNV    A=47 B=36 C=26 D=9242 
01219 [L1338] ADDVV    A=47 B=38 C=47 D=9775 
01220 [L1338] TSETS    A=47 B=46 C=32 D=11808 'y'
01221 [L1338] TDUP     A=47 B=0 C=183 D=183 {'kind': 'table', 'value': {1: -0.1, 2: 0.5}}
01222 [L1338] TSETS    A=47 B=46 C=93 D=11869 'anchor'
01223 [L1338] CALL     A=45 B=0 C=2 D=2 
01224 [L1338] CALLM    A=43 B=1 C=1 D=257 
01225 [L1341] MOV      A=43 B=0 C=18 D=18 
01226 [L1341] TGETS    A=42 B=18 C=7 D=4615 'addChild'
01227 [L1341] GGET     A=44 B=0 C=11 D=11 'd_ms'
01228 [L1341] TGETS    A=44 B=44 C=12 D=11276 'd_u'
01229 [L1341] TGETS    A=44 B=44 C=67 D=11331 'createByStyle'
01230 [L1341] TDUP     A=45 B=0 C=184 D=184 {'kind': 'table', 'value': {'pic': 'v2/introUI/level.png'}}
01231 [L1341] MULNV    A=46 B=35 C=25 D=8985 
01232 [L1341] ADDVV    A=46 B=37 C=46 D=9518 
01233 [L1341] TSETS    A=46 B=45 C=30 D=11550 'x'
01234 [L1341] MULNV    A=46 B=36 C=27 D=9243 
01235 [L1341] ADDVV    A=46 B=38 C=46 D=9774 
01236 [L1341] TSETS    A=46 B=45 C=32 D=11552 'y'
01237 [L1341] TDUP     A=46 B=0 C=185 D=185 {'kind': 'table', 'value': {1: 1.1, 2: 0.5}}
01238 [L1341] TSETS    A=46 B=45 C=93 D=11613 'anchor'
01239 [L1341] CALL     A=44 B=0 C=2 D=2 
01240 [L1341] CALLM    A=42 B=1 C=1 D=257 
01241 [L1342] MOV      A=43 B=0 C=18 D=18 
01242 [L1342] TGETS    A=42 B=18 C=7 D=4615 'addChild'
01243 [L1342] GGET     A=44 B=0 C=11 D=11 'd_ms'
01244 [L1342] TGETS    A=44 B=44 C=12 D=11276 'd_u'
01245 [L1342] TGETS    A=44 B=44 C=67 D=11331 'createByStyle'
01246 [L1342] TDUP     A=45 B=0 C=186 D=186 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 26}}
01247 [L1342] UGET     A=46 B=0 C=13 D=13 tostring
01248 [L1342] MOV      A=47 B=0 C=28 D=28 
01249 [L1342] CALL     A=46 B=2 C=2 D=514 
01250 [L1342] TSETS    A=46 B=45 C=70 D=11590 'string'
01251 [L1342] TDUP     A=46 B=0 C=187 D=187 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
01252 [L1342] TSETS    A=46 B=45 C=93 D=11613 'anchor'
01253 [L1342] TSETS    A=4 B=45 C=76 D=11596 'color'
01254 [L1342] MULNV    A=46 B=35 C=25 D=8985 
01255 [L1342] ADDVV    A=46 B=37 C=46 D=9518 
01256 [L1342] TSETS    A=46 B=45 C=30 D=11550 'x'
01257 [L1342] MULNV    A=46 B=36 C=27 D=9243 
01258 [L1342] ADDVV    A=46 B=38 C=46 D=9774 
01259 [L1342] TSETS    A=46 B=45 C=32 D=11552 'y'
01260 [L1342] CALL     A=44 B=0 C=2 D=2 
01261 [L1342] CALLM    A=42 B=1 C=1 D=257 
01262 [L1345] MULNV    A=42 B=36 C=28 D=9244 
01263 [L1345] ADDVV    A=42 B=38 C=42 D=9770 
01264 [L1345] MULNV    A=43 B=36 C=29 D=9245 
01265 [L1345] ADDVV    A=43 B=38 C=43 D=9771 
01266 [L1346] MULNV    A=44 B=35 C=30 D=8990 
01267 [L1346] ADDVV    A=44 B=37 C=44 D=9516 
01268 [L1346] MULNV    A=45 B=35 C=31 D=8991 
01269 [L1346] MULNV    A=46 B=35 C=32 D=8992 
01270 [L1347] KSHORT   A=47 B=0 C=0 D=0 0
01271 [L1348] GGET     A=48 B=0 C=11 D=11 'd_ms'
01272 [L1348] TGETS    A=48 B=48 C=144 D=12432 'd_data'
01273 [L1348] TGETS    A=48 B=48 C=145 D=12433 'g_stoneAttrTable'
01274 [L1348] TGETV    A=48 B=48 C=23 D=12311 
01275 [L1349] TGETS    A=49 B=0 C=188 D=188 'star_level'
01276 [L1350] TGETS    A=50 B=0 C=188 D=188 'star_level'
01277 [L1350] IST      A=0 B=0 C=50 D=50 
01278 [L1350] JMP      A=50 B=128 C=1 D=32769 target=1280
01279 [L1351] KSHORT   A=49 B=0 C=0 D=0 0
01280 [L1353] GGET     A=50 B=0 C=11 D=11 'd_ms'
01281 [L1353] TGETS    A=50 B=50 C=189 D=12989 'd_stoneUI'
01282 [L1353] TGETS    A=50 B=50 C=126 D=12926 'g_self'
01283 [L1353] TGETS    A=50 B=50 C=190 D=12990 'Slots'
01284 [L1353] TGETS    A=51 B=0 C=45 D=45 'csvInfo'
01285 [L1353] TGETS    A=51 B=51 C=46 D=13102 'quality'
01286 [L1353] TGETV    A=50 B=50 C=51 D=12851 
01287 [L1353] ADDVV    A=50 B=50 C=49 D=12849 
01288 [L1354] TGETS    A=51 B=0 C=191 D=191 'drill_count'
01289 [L1354] IST      A=0 B=0 C=51 D=51 
01290 [L1354] JMP      A=52 B=128 C=1 D=32769 target=1292
01291 [L1354] KSHORT   A=51 B=0 C=0 D=0 0
01292 [L1355] KSHORT   A=52 B=0 C=1 D=1 1
01293 [L1355] KSHORT   A=53 B=0 C=4 D=4 4
01294 [L1355] KSHORT   A=54 B=0 C=1 D=1 1
01295 [L1355] FORI     A=52 B=128 C=136 D=32904 target=1432
01296 [L1356] SUBVN    A=56 B=55 C=14 D=14094 
01297 [L1356] MULVV    A=56 B=56 C=45 D=14381 
01298 [L1356] ADDVV    A=56 B=44 C=56 D=11320 
01299 [L1357] KSTR     A=57 B=0 C=57 D=57 'stone'
01300 [L1357] MOV      A=58 B=0 C=55 D=55 
01301 [L1357] KSTR     A=59 B=0 C=192 D=192 '_level'
01302 [L1357] CAT      A=57 B=57 C=59 D=14651 
01303 [L1357] TGETV    A=57 B=0 C=57 D=57 
01304 [L1357] IST      A=0 B=0 C=57 D=57 
01305 [L1357] JMP      A=58 B=128 C=1 D=32769 target=1307
01306 [L1357] KSHORT   A=57 B=0 C=0 D=0 0
01307 [L1358] KSHORT   A=58 B=0 C=0 D=0 0
01308 [L1358] ISGE     A=58 B=0 C=57 D=57 
01309 [L1358] JMP      A=58 B=128 C=93 D=32861 target=1403
01310 [L1359] KPRI     A=58 B=0 C=0 D=0 
01311 [L1360] KSHORT   A=59 B=0 C=10 D=10 10
01312 [L1360] ISGE     A=59 B=0 C=57 D=57 
01313 [L1360] JMP      A=59 B=128 C=12 D=32780 target=1326
01314 [L1361] GGET     A=59 B=0 C=11 D=11 'd_ms'
01315 [L1361] TGETS    A=59 B=59 C=140 D=15244 'd_stoneCastUI'
01316 [L1361] TGETS    A=59 B=59 C=141 D=15245 'initConfig'
01317 [L1361] CALL     A=59 B=1 C=1 D=257 
01318 [L1362] GGET     A=59 B=0 C=11 D=11 'd_ms'
01319 [L1362] TGETS    A=59 B=59 C=140 D=15244 'd_stoneCastUI'
01320 [L1362] TGETS    A=59 B=59 C=126 D=15230 'g_self'
01321 [L1362] TGETS    A=59 B=59 C=142 D=15246 'csv'
01322 [L1362] TGETV    A=59 B=59 C=23 D=15127 
01323 [L1362] TGETV    A=59 B=59 C=57 D=15161 
01324 [L1362] TGETS    A=58 B=59 C=143 D=15247 'plus'
01325 [L1362] JMP      A=59 B=128 C=2 D=32770 target=1328
01326 [L1364] TGETV    A=59 B=48 C=57 D=12345 
01327 [L1364] TGETS    A=58 B=59 C=146 D=15250 'base'
01328 [L1366] ADDVV    A=47 B=47 C=58 D=12090 
01329 [L1367] GGET     A=59 B=0 C=11 D=11 'd_ms'
01330 [L1367] TGETS    A=59 B=59 C=144 D=15248 'd_data'
01331 [L1367] TGETS    A=59 B=59 C=193 D=15297 'getCertainSmallSprite'
01332 [L1367] TGETS    A=60 B=0 C=44 D=44 'attach_type'
01333 [L1367] GGET     A=61 B=0 C=11 D=11 'd_ms'
01334 [L1367] TGETS    A=61 B=61 C=189 D=15805 'd_stoneUI'
01335 [L1367] TGETS    A=61 B=61 C=194 D=15810 'getStoneTypeID'
01336 [L1367] MOV      A=62 B=0 C=23 D=23 
01337 [L1367] CALL     A=61 B=2 C=2 D=514 
01338 [L1367] MOV      A=62 B=0 C=57 D=57 
01339 [L1367] TGETS    A=63 B=0 C=188 D=188 'star_level'
01340 [L1367] CALL     A=59 B=2 C=5 D=517 
01341 [L1368] GGET     A=60 B=0 C=11 D=11 'd_ms'
01342 [L1368] TGETS    A=60 B=60 C=12 D=15372 'd_u'
01343 [L1368] TGETS    A=60 B=60 C=13 D=15373 'setStyles'
01344 [L1368] MOV      A=61 B=0 C=59 D=59 
01345 [L1368] TDUP     A=62 B=0 C=195 D=195 {'kind': 'table', 'value': {}}
01346 [L1368] TSETS    A=56 B=62 C=30 D=15902 'x'
01347 [L1368] TSETS    A=42 B=62 C=32 D=15904 'y'
01348 [L1368] MULNV    A=63 B=36 C=31 D=9247 
01349 [L1368] TSETS    A=63 B=62 C=173 D=16045 'scaleH'
01350 [L1368] CALL     A=60 B=1 C=3 D=259 
01351 [L1369] MOV      A=61 B=0 C=18 D=18 
01352 [L1369] TGETS    A=60 B=18 C=7 D=4615 'addChild'
01353 [L1369] MOV      A=62 B=0 C=59 D=59 
01354 [L1369] CALL     A=60 B=1 C=3 D=259 
01355 [L1372] MOV      A=61 B=0 C=18 D=18 
01356 [L1372] TGETS    A=60 B=18 C=7 D=4615 'addChild'
01357 [L1372] GGET     A=62 B=0 C=11 D=11 'd_ms'
01358 [L1372] TGETS    A=62 B=62 C=12 D=15884 'd_u'
01359 [L1372] TGETS    A=62 B=62 C=67 D=15939 'createByStyle'
01360 [L1372] TDUP     A=63 B=0 C=196 D=196 {'kind': 'table', 'value': {'pic': 'v2/newIntroUI/stone_value_bkg.png'}}
01361 [L1372] TSETS    A=56 B=63 C=30 D=16158 'x'
01362 [L1372] TSETS    A=43 B=63 C=32 D=16160 'y'
01363 [L1372] CALL     A=62 B=0 C=2 D=2 
01364 [L1372] CALLM    A=60 B=1 C=1 D=257 
01365 [L1373] MOV      A=61 B=0 C=18 D=18 
01366 [L1373] TGETS    A=60 B=18 C=7 D=4615 'addChild'
01367 [L1373] GGET     A=62 B=0 C=11 D=11 'd_ms'
01368 [L1373] TGETS    A=62 B=62 C=12 D=15884 'd_u'
01369 [L1373] TGETS    A=62 B=62 C=67 D=15939 'createByStyle'
01370 [L1373] TDUP     A=63 B=0 C=197 D=197 {'kind': 'table', 'value': {}}
01371 [L1373] TGETV    A=64 B=24 C=23 D=6167 
01372 [L1373] TSETS    A=64 B=63 C=139 D=16267 'pic'
01373 [L1373] SUBVV    A=64 B=56 C=46 D=14382 
01374 [L1373] TSETS    A=64 B=63 C=30 D=16158 'x'
01375 [L1373] TSETS    A=43 B=63 C=32 D=16160 'y'
01376 [L1373] MULNV    A=64 B=36 C=33 D=9249 
01377 [L1373] TSETS    A=64 B=63 C=173 D=16301 'scaleH'
01378 [L1373] TDUP     A=64 B=0 C=198 D=198 {'kind': 'table', 'value': {1: 1, 2: 0.5}}
01379 [L1373] TSETS    A=64 B=63 C=93 D=16221 'anchor'
01380 [L1373] CALL     A=62 B=0 C=2 D=2 
01381 [L1373] CALLM    A=60 B=1 C=1 D=257 
01382 [L1374] MOV      A=61 B=0 C=18 D=18 
01383 [L1374] TGETS    A=60 B=18 C=7 D=4615 'addChild'
01384 [L1374] GGET     A=62 B=0 C=11 D=11 'd_ms'
01385 [L1374] TGETS    A=62 B=62 C=12 D=15884 'd_u'
01386 [L1374] TGETS    A=62 B=62 C=67 D=15939 'createByStyle'
01387 [L1374] TDUP     A=63 B=0 C=199 D=199 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 26}}
01388 [L1374] UGET     A=64 B=0 C=16 D=16 string
01389 [L1374] TGETS    A=64 B=64 C=133 D=16517 'format'
01390 [L1374] KSTR     A=65 B=0 C=200 D=200 ' %.1f%%'
01391 [L1374] MULVN    A=66 B=58 C=17 D=14865 
01392 [L1374] CALL     A=64 B=2 C=3 D=515 
01393 [L1374] TSETS    A=64 B=63 C=70 D=16198 'string'
01394 [L1374] SUBVV    A=64 B=56 C=46 D=14382 
01395 [L1374] TSETS    A=64 B=63 C=30 D=16158 'x'
01396 [L1374] TSETS    A=43 B=63 C=32 D=16160 'y'
01397 [L1374] TDUP     A=64 B=0 C=201 D=201 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
01398 [L1374] TSETS    A=64 B=63 C=93 D=16221 'anchor'
01399 [L1374] TSETS    A=4 B=63 C=76 D=16204 'color'
01400 [L1374] CALL     A=62 B=0 C=2 D=2 
01401 [L1374] CALLM    A=60 B=1 C=1 D=257 
01402 [L1374] JMP      A=58 B=128 C=28 D=32796 target=1431
01403 [L1375] ISGT     A=55 B=0 C=50 D=50 
01404 [L1375] JMP      A=58 B=128 C=26 D=32794 target=1431
01405 [L1377] MOV      A=59 B=0 C=18 D=18 
01406 [L1377] TGETS    A=58 B=18 C=7 D=4615 'addChild'
01407 [L1377] GGET     A=60 B=0 C=11 D=11 'd_ms'
01408 [L1377] TGETS    A=60 B=60 C=12 D=15372 'd_u'
01409 [L1377] TGETS    A=60 B=60 C=67 D=15427 'createByStyle'
01410 [L1377] TDUP     A=61 B=0 C=202 D=202 {'kind': 'table', 'value': {'pic': 'v2/stoneUI/unsee.png'}}
01411 [L1377] MULNV    A=62 B=36 C=31 D=9247 
01412 [L1377] TSETS    A=62 B=61 C=173 D=15789 'scaleH'
01413 [L1377] TSETS    A=56 B=61 C=30 D=15646 'x'
01414 [L1377] TSETS    A=42 B=61 C=32 D=15648 'y'
01415 [L1377] CALL     A=60 B=0 C=2 D=2 
01416 [L1377] CALLM    A=58 B=1 C=1 D=257 
01417 [L1378] ISGE     A=51 B=0 C=55 D=55 
01418 [L1378] JMP      A=58 B=128 C=12 D=32780 target=1431
01419 [L1379] MOV      A=59 B=0 C=18 D=18 
01420 [L1379] TGETS    A=58 B=18 C=7 D=4615 'addChild'
01421 [L1379] GGET     A=60 B=0 C=11 D=11 'd_ms'
01422 [L1379] TGETS    A=60 B=60 C=12 D=15372 'd_u'
01423 [L1379] TGETS    A=60 B=60 C=67 D=15427 'createByStyle'
01424 [L1379] TDUP     A=61 B=0 C=203 D=203 {'kind': 'table', 'value': {'pic': 'v2/stoneUI/lock.png'}}
01425 [L1379] TSETS    A=56 B=61 C=30 D=15646 'x'
01426 [L1379] TSETS    A=42 B=61 C=32 D=15648 'y'
01427 [L1379] MULNV    A=62 B=36 C=31 D=9247 
01428 [L1379] TSETS    A=62 B=61 C=173 D=15789 'scaleH'
01429 [L1379] CALL     A=60 B=0 C=2 D=2 
01430 [L1379] CALLM    A=58 B=1 C=1 D=257 
01431 [L1355] FORL     A=52 B=127 C=120 D=32632 target=1296
01432 [L1383] UGET     A=52 B=0 C=6 D=6 CCMenuItemImage
01433 [L1383] MOV      A=53 B=0 C=52 D=52 
01434 [L1383] TGETS    A=52 B=52 C=3 D=13315 'create'
01435 [L1383] KSTR     A=54 B=0 C=204 D=204 'v2/shengxing/dianji.png'
01436 [L1383] KSTR     A=55 B=0 C=204 D=204 'v2/shengxing/dianji.png'
01437 [L1383] CALL     A=52 B=2 C=4 D=516 
01438 [L1384] GGET     A=53 B=0 C=11 D=11 'd_ms'
01439 [L1384] TGETS    A=53 B=53 C=12 D=13580 'd_u'
01440 [L1384] TGETS    A=53 B=53 C=13 D=13581 'setStyles'
01441 [L1384] MOV      A=54 B=0 C=52 D=52 
01442 [L1384] TDUP     A=55 B=0 C=205 D=205 {'kind': 'table', 'value': {'scaleX': 0.45}}
01443 [L1384] MULNV    A=56 B=35 C=8 D=8968 
01444 [L1384] ADDVV    A=56 B=37 C=56 D=9528 
01445 [L1384] TSETS    A=56 B=55 C=30 D=14110 'x'
01446 [L1384] MULNV    A=56 B=36 C=31 D=9247 
01447 [L1384] ADDVV    A=56 B=38 C=56 D=9784 
01448 [L1384] TSETS    A=56 B=55 C=32 D=14112 'y'
01449 [L1384] CALL     A=53 B=1 C=3 D=259 
01450 [L1385] MOV      A=54 B=0 C=52 D=52 
01451 [L1385] TGETS    A=53 B=52 C=21 D=13333 'setTag'
01452 [L1385] GGET     A=55 B=0 C=22 D=22 'g_introButtonType'
01453 [L1385] TGETS    A=55 B=55 C=206 D=14286 'slot'
01454 [L1385] CALL     A=53 B=1 C=3 D=259 
01455 [L1386] MOV      A=54 B=0 C=52 D=52 
01456 [L1386] TGETS    A=53 B=52 C=25 D=13337 'registerScriptTapHandler'
01457 [L1386] MOV      A=55 B=0 C=1 D=1 
01458 [L1386] CALL     A=53 B=1 C=3 D=259 
01459 [L1387] MOV      A=54 B=0 C=7 D=7 
01460 [L1387] TGETS    A=53 B=7 C=154 D=1946 'addObject'
01461 [L1387] MOV      A=55 B=0 C=52 D=52 
01462 [L1387] CALL     A=53 B=1 C=3 D=259 
01463 [L1405] ISF      A=0 B=0 C=2 D=2 
01464 [L1405] JMP      A=53 B=128 C=51 D=32819 target=1516
01465 [L1406] UGET     A=53 B=0 C=6 D=6 CCMenuItemImage
01466 [L1406] MOV      A=54 B=0 C=53 D=53 
01467 [L1406] TGETS    A=53 B=53 C=3 D=13571 'create'
01468 [L1406] KSTR     A=55 B=0 C=207 D=207 'v2/newIntroUI/enhance1.png'
01469 [L1406] KSTR     A=56 B=0 C=208 D=208 'v2/newIntroUI/enhance2.png'
01470 [L1406] CALL     A=53 B=2 C=4 D=516 
01471 [L1408] GGET     A=54 B=0 C=11 D=11 'd_ms'
01472 [L1408] TGETS    A=54 B=54 C=209 D=14033 'd_equipmentUpgradeUI'
01473 [L1408] TGETS    A=54 B=54 C=210 D=14034 'checkEquipmentCanUpgrade'
01474 [L1408] KPRI     A=55 B=0 C=1 D=1 
01475 [L1408] TGETS    A=56 B=0 C=77 D=77 'level'
01476 [L1408] TGETS    A=57 B=0 C=45 D=45 'csvInfo'
01477 [L1408] TGETS    A=57 B=57 C=46 D=14638 'quality'
01478 [L1408] TGETS    A=58 B=0 C=50 D=50 'reborn_bit'
01479 [L1408] CALL     A=54 B=2 C=5 D=517 
01480 [L1408] ISNEN    A=54 B=0 C=11 D=11 2
01481 [L1408] JMP      A=54 B=128 C=5 D=32773 target=1487
01482 [L1409] GGET     A=54 B=0 C=11 D=11 'd_ms'
01483 [L1409] TGETS    A=54 B=54 C=12 D=13836 'd_u'
01484 [L1409] TGETS    A=54 B=54 C=155 D=13979 'grayMenuItem'
01485 [L1409] MOV      A=55 B=0 C=53 D=53 
01486 [L1409] CALL     A=54 B=1 C=2 D=258 
01487 [L1411] GGET     A=54 B=0 C=11 D=11 'd_ms'
01488 [L1411] TGETS    A=54 B=54 C=12 D=13836 'd_u'
01489 [L1411] TGETS    A=54 B=54 C=13 D=13837 'setStyles'
01490 [L1411] MOV      A=55 B=0 C=53 D=53 
01491 [L1411] TDUP     A=56 B=0 C=211 D=211 {'kind': 'table', 'value': {}}
01492 [L1411] MULNV    A=57 B=35 C=34 D=8994 
01493 [L1411] ADDVV    A=57 B=37 C=57 D=9529 
01494 [L1411] TSETS    A=57 B=56 C=30 D=14366 'x'
01495 [L1411] MULNV    A=57 B=36 C=27 D=9243 
01496 [L1411] ADDVV    A=57 B=38 C=57 D=9785 
01497 [L1411] TSETS    A=57 B=56 C=32 D=14368 'y'
01498 [L1411] CALL     A=54 B=1 C=3 D=259 
01499 [L1412] MOV      A=55 B=0 C=53 D=53 
01500 [L1412] TGETS    A=54 B=53 C=21 D=13589 'setTag'
01501 [L1412] GGET     A=56 B=0 C=22 D=22 'g_introButtonType'
01502 [L1412] TGETS    A=56 B=56 C=212 D=14548 'enhance'
01503 [L1412] CALL     A=54 B=1 C=3 D=259 
01504 [L1413] MOV      A=55 B=0 C=53 D=53 
01505 [L1413] TGETS    A=54 B=53 C=213 D=13781 'setScale'
01506 [L1413] KNUM     A=56 B=0 C=26 D=26 0.9
01507 [L1413] CALL     A=54 B=1 C=3 D=259 
01508 [L1414] MOV      A=55 B=0 C=53 D=53 
01509 [L1414] TGETS    A=54 B=53 C=25 D=13593 'registerScriptTapHandler'
01510 [L1414] MOV      A=56 B=0 C=1 D=1 
01511 [L1414] CALL     A=54 B=1 C=3 D=259 
01512 [L1415] MOV      A=55 B=0 C=7 D=7 
01513 [L1415] TGETS    A=54 B=7 C=154 D=1946 'addObject'
01514 [L1415] MOV      A=56 B=0 C=53 D=53 
01515 [L1415] CALL     A=54 B=1 C=3 D=259 
01516 [L1418] KNIL     A=53 B=0 C=54 D=54 
01517 [L1421] GGET     A=55 B=0 C=11 D=11 'd_ms'
01518 [L1421] TGETS    A=55 B=55 C=214 D=14294 'd_equipAdvanceUI'
01519 [L1421] TGETS    A=55 B=55 C=126 D=14206 'g_self'
01520 [L1421] TGETS    A=55 B=55 C=215 D=14295 'is_open'
01521 [L1421] ISF      A=0 B=0 C=55 D=55 
01522 [L1421] JMP      A=56 B=130 C=131 D=33411 target=2166
01523 [L1421] TGETS    A=55 B=0 C=45 D=45 'csvInfo'
01524 [L1421] TGETS    A=55 B=55 C=46 D=14126 'quality'
01525 [L1421] KSHORT   A=56 B=0 C=4 D=4 4
01526 [L1421] ISGT     A=56 B=0 C=55 D=55 
01527 [L1421] JMP      A=55 B=130 C=126 D=33406 target=2166
01528 [L1422] GGET     A=55 B=0 C=11 D=11 'd_ms'
01529 [L1422] TGETS    A=55 B=55 C=214 D=14294 'd_equipAdvanceUI'
01530 [L1423] TGETS    A=56 B=55 C=216 D=14296 'getConsts'
01531 [L1423] CALL     A=56 B=1 C=1 D=257 
01532 [L1424] TGETS    A=56 B=55 C=126 D=14206 'g_self'
01533 [L1424] TGETS    A=56 B=56 C=217 D=14553 'Value'
01534 [L1424] TGETS    A=57 B=0 C=45 D=45 'csvInfo'
01535 [L1424] TGETS    A=57 B=57 C=46 D=14638 'quality'
01536 [L1424] TGETV    A=56 B=56 C=57 D=14393 
01537 [L1424] TGETS    A=57 B=0 C=45 D=45 'csvInfo'
01538 [L1424] TGETS    A=57 B=57 C=59 D=14651 'mainType'
01539 [L1424] TGETV    A=56 B=56 C=57 D=14393 
01540 [L1424] TGETV    A=56 B=56 C=29 D=14365 
01541 [L1424] TGETV    A=53 B=56 C=30 D=14366 
01542 [L1426] KSHORT   A=56 B=0 C=0 D=0 0
01543 [L1426] ISLT     A=56 B=0 C=33 D=33 
01544 [L1426] JMP      A=56 B=128 C=16 D=32784 target=1561
01545 [L1426] ISF      A=0 B=0 C=2 D=2 
01546 [L1426] JMP      A=56 B=128 C=138 D=32906 target=1685
01547 [L1426] GGET     A=56 B=0 C=11 D=11 'd_ms'
01548 [L1426] TGETS    A=56 B=56 C=218 D=14554 'd_equipAscUI'
01549 [L1426] TGETS    A=56 B=56 C=219 D=14555 'canAsc'
01550 [L1426] MOV      A=57 B=0 C=0 D=0 
01551 [L1426] CALL     A=56 B=2 C=2 D=514 
01552 [L1426] ISF      A=0 B=0 C=56 D=56 
01553 [L1426] JMP      A=57 B=128 C=131 D=32899 target=1685
01554 [L1426] GGET     A=56 B=0 C=11 D=11 'd_ms'
01555 [L1426] TGETS    A=56 B=56 C=220 D=14556 'd_mainUI'
01556 [L1426] TGETS    A=56 B=56 C=221 D=14557 'g_playerInfo'
01557 [L1426] TGETS    A=56 B=56 C=77 D=14413 'level'
01558 [L1426] KSHORT   A=57 B=0 C=70 D=70 70
01559 [L1426] ISGT     A=57 B=0 C=56 D=56 
01560 [L1426] JMP      A=56 B=128 C=124 D=32892 target=1685
01561 [L1428] ISNEN    A=33 B=0 C=4 D=4 0
01562 [L1428] JMP      A=56 B=128 C=50 D=32818 target=1613
01563 [L1428] ISF      A=0 B=0 C=2 D=2 
01564 [L1428] JMP      A=56 B=128 C=48 D=32816 target=1613
01565 [L1429] MOV      A=57 B=0 C=6 D=6 
01566 [L1429] TGETS    A=56 B=6 C=7 D=1543 'addChild'
01567 [L1429] GGET     A=58 B=0 C=11 D=11 'd_ms'
01568 [L1429] TGETS    A=58 B=58 C=12 D=14860 'd_u'
01569 [L1429] TGETS    A=58 B=58 C=67 D=14915 'createByStyle'
01570 [L1429] TDUP     A=59 B=0 C=222 D=222 {'kind': 'table', 'value': {'pic': 'v2/ascCast/asc_bkg.png', 'x': 0.765, 'y': 0.55}}
01571 [L1429] CALL     A=58 B=2 C=2 D=514 
01572 [L1429] KSHORT   A=59 B=3 C=241 D=1009 1009
01573 [L1429] CALL     A=56 B=1 C=4 D=260 
01574 [L1430] UGET     A=56 B=0 C=6 D=6 CCMenuItemImage
01575 [L1430] MOV      A=57 B=0 C=56 D=56 
01576 [L1430] TGETS    A=56 B=56 C=3 D=14339 'create'
01577 [L1430] KSTR     A=58 B=0 C=223 D=223 'v2/ascCast/asc1.png'
01578 [L1430] KSTR     A=59 B=0 C=224 D=224 'v2/ascCast/asc2.png'
01579 [L1430] CALL     A=56 B=2 C=4 D=516 
01580 [L1431] MOV      A=58 B=0 C=56 D=56 
01581 [L1431] TGETS    A=57 B=56 C=21 D=14357 'setTag'
01582 [L1431] GGET     A=59 B=0 C=22 D=22 'g_introButtonType'
01583 [L1431] TGETS    A=59 B=59 C=225 D=15329 'asc'
01584 [L1431] CALL     A=57 B=1 C=3 D=259 
01585 [L1432] GGET     A=57 B=0 C=11 D=11 'd_ms'
01586 [L1432] TGETS    A=57 B=57 C=12 D=14604 'd_u'
01587 [L1432] TGETS    A=57 B=57 C=13 D=14605 'setStyles'
01588 [L1432] MOV      A=58 B=0 C=56 D=56 
01589 [L1432] TDUP     A=59 B=0 C=226 D=226 {'kind': 'table', 'value': {'x': 0.765, 'y': 0.55}}
01590 [L1432] CALL     A=57 B=1 C=3 D=259 
01591 [L1433] MOV      A=58 B=0 C=56 D=56 
01592 [L1433] TGETS    A=57 B=56 C=25 D=14361 'registerScriptTapHandler'
01593 [L1433] MOV      A=59 B=0 C=1 D=1 
01594 [L1433] CALL     A=57 B=1 C=3 D=259 
01595 [L1434] UGET     A=57 B=0 C=7 D=7 CCMenu
01596 [L1434] MOV      A=58 B=0 C=57 D=57 
01597 [L1434] TGETS    A=57 B=57 C=26 D=14618 'createWithItem'
01598 [L1434] MOV      A=59 B=0 C=56 D=56 
01599 [L1434] CALL     A=57 B=2 C=3 D=515 
01600 [L1435] MOV      A=59 B=0 C=57 D=57 
01601 [L1435] TGETS    A=58 B=57 C=27 D=14619 'setPosition'
01602 [L1435] UGET     A=60 B=0 C=8 D=8 CCPointMake
01603 [L1435] KSHORT   A=61 B=0 C=0 D=0 0
01604 [L1435] KSHORT   A=62 B=0 C=0 D=0 0
01605 [L1435] CALL     A=60 B=0 C=3 D=3 
01606 [L1435] CALLM    A=58 B=1 C=1 D=257 
01607 [L1436] MOV      A=59 B=0 C=6 D=6 
01608 [L1436] TGETS    A=58 B=6 C=7 D=1543 'addChild'
01609 [L1436] MOV      A=60 B=0 C=57 D=57 
01610 [L1436] KNUM     A=61 B=0 C=35 D=35 100001
01611 [L1436] CALL     A=58 B=1 C=4 D=260 
01612 [L1436] JMP      A=56 B=128 C=72 D=32840 target=1685
01613 [L1437] KSHORT   A=56 B=0 C=4 D=4 4
01614 [L1437] ISGT     A=56 B=0 C=32 D=32 
01615 [L1437] JMP      A=56 B=128 C=60 D=32828 target=1676
01616 [L1438] GGET     A=56 B=0 C=11 D=11 'd_ms'
01617 [L1438] TGETS    A=56 B=56 C=12 D=14348 'd_u'
01618 [L1438] TGETS    A=56 B=56 C=67 D=14403 'createByStyle'
01619 [L1438] TDUP     A=57 B=0 C=227 D=227 {'kind': 'table', 'value': {'pic': 'v2/ascCast/asc_bkg.png', 'x': 0.765, 'y': 0.55}}
01620 [L1438] CALL     A=56 B=2 C=2 D=514 
01621 [L1439] GGET     A=57 B=0 C=11 D=11 'd_ms'
01622 [L1439] TGETS    A=57 B=57 C=12 D=14604 'd_u'
01623 [L1439] TGETS    A=57 B=57 C=13 D=14605 'setStyles'
01624 [L1439] MOV      A=58 B=0 C=56 D=56 
01625 [L1439] TDUP     A=59 B=0 C=228 D=228 {'kind': 'table', 'value': {'scale': 0.15}}
01626 [L1439] CALL     A=57 B=1 C=3 D=259 
01627 [L1440] MOV      A=58 B=0 C=6 D=6 
01628 [L1440] TGETS    A=57 B=6 C=7 D=1543 'addChild'
01629 [L1440] MOV      A=59 B=0 C=56 D=56 
01630 [L1440] KSHORT   A=60 B=3 C=241 D=1009 1009
01631 [L1440] CALL     A=57 B=1 C=4 D=260 
01632 [L1441] TGETS    A=57 B=0 C=188 D=188 'star_level'
01633 [L1441] ISEQN    A=57 B=0 C=14 D=14 1
01634 [L1441] JMP      A=57 B=128 C=50 D=32818 target=1685
01635 [L1460] FNEW     A=57 B=0 C=229 D=229 {'kind': 'proto', 'id': 42}
01636 [L1442] GSET     A=57 B=0 C=230 D=230 'callbackShengxing'
01637 [L1461] UGET     A=57 B=0 C=6 D=6 CCMenuItemImage
01638 [L1461] MOV      A=58 B=0 C=57 D=57 
01639 [L1461] TGETS    A=57 B=57 C=3 D=14595 'create'
01640 [L1461] KSTR     A=59 B=0 C=231 D=231 'v2/shengxing/comfirm_sx.png'
01641 [L1461] KSTR     A=60 B=0 C=231 D=231 'v2/shengxing/comfirm_sx.png'
01642 [L1461] CALL     A=57 B=2 C=4 D=516 
01643 [L1462] MOV      A=59 B=0 C=57 D=57 
01644 [L1462] TGETS    A=58 B=57 C=21 D=14613 'setTag'
01645 [L1462] GGET     A=60 B=0 C=22 D=22 'g_introButtonType'
01646 [L1462] TGETS    A=60 B=60 C=23 D=15383 'close'
01647 [L1462] CALL     A=58 B=1 C=3 D=259 
01648 [L1463] GGET     A=58 B=0 C=11 D=11 'd_ms'
01649 [L1463] TGETS    A=58 B=58 C=12 D=14860 'd_u'
01650 [L1463] TGETS    A=58 B=58 C=13 D=14861 'setStyles'
01651 [L1463] MOV      A=59 B=0 C=57 D=57 
01652 [L1463] TDUP     A=60 B=0 C=232 D=232 {'kind': 'table', 'value': {'x': 0.765, 'y': 0.55}}
01653 [L1463] CALL     A=58 B=1 C=3 D=259 
01654 [L1464] MOV      A=59 B=0 C=57 D=57 
01655 [L1464] TGETS    A=58 B=57 C=25 D=14617 'registerScriptTapHandler'
01656 [L1464] GGET     A=60 B=0 C=230 D=230 'callbackShengxing'
01657 [L1464] CALL     A=58 B=1 C=3 D=259 
01658 [L1465] UGET     A=58 B=0 C=7 D=7 CCMenu
01659 [L1465] MOV      A=59 B=0 C=58 D=58 
01660 [L1465] TGETS    A=58 B=58 C=26 D=14874 'createWithItem'
01661 [L1465] MOV      A=60 B=0 C=57 D=57 
01662 [L1465] CALL     A=58 B=2 C=3 D=515 
01663 [L1466] MOV      A=60 B=0 C=58 D=58 
01664 [L1466] TGETS    A=59 B=58 C=27 D=14875 'setPosition'
01665 [L1466] UGET     A=61 B=0 C=8 D=8 CCPointMake
01666 [L1466] KSHORT   A=62 B=0 C=0 D=0 0
01667 [L1466] KSHORT   A=63 B=0 C=0 D=0 0
01668 [L1466] CALL     A=61 B=0 C=3 D=3 
01669 [L1466] CALLM    A=59 B=1 C=1 D=257 
01670 [L1467] MOV      A=60 B=0 C=6 D=6 
01671 [L1467] TGETS    A=59 B=6 C=7 D=1543 'addChild'
01672 [L1467] MOV      A=61 B=0 C=58 D=58 
01673 [L1467] KSHORT   A=62 B=39 C=18 D=10002 10002
01674 [L1467] CALL     A=59 B=1 C=4 D=260 
01675 [L1468] JMP      A=56 B=128 C=9 D=32777 target=1685
01676 [L1470] MOV      A=57 B=0 C=6 D=6 
01677 [L1470] TGETS    A=56 B=6 C=7 D=1543 'addChild'
01678 [L1470] GGET     A=58 B=0 C=11 D=11 'd_ms'
01679 [L1470] TGETS    A=58 B=58 C=12 D=14860 'd_u'
01680 [L1470] TGETS    A=58 B=58 C=67 D=14915 'createByStyle'
01681 [L1470] TDUP     A=59 B=0 C=233 D=233 {'kind': 'table', 'value': {'pic': 'v2/ascCast/asc_bkg.png', 'x': 0.765, 'y': 0.55}}
01682 [L1470] CALL     A=58 B=2 C=2 D=514 
01683 [L1470] KSHORT   A=59 B=3 C=241 D=1009 1009
01684 [L1470] CALL     A=56 B=1 C=4 D=260 
01685 [L1473] KSHORT   A=56 B=0 C=0 D=0 0
01686 [L1473] ISGE     A=56 B=0 C=33 D=33 
01687 [L1473] JMP      A=56 B=128 C=117 D=32885 target=1805
01688 [L1474] GGET     A=56 B=0 C=11 D=11 'd_ms'
01689 [L1474] TGETS    A=56 B=56 C=234 D=14570 'd_equipCastUI'
01690 [L1474] TGETS    A=56 B=56 C=235 D=14571 'getCastEffect'
01691 [L1474] TGETS    A=57 B=0 C=45 D=45 'csvInfo'
01692 [L1474] TGETS    A=57 B=57 C=59 D=14651 'mainType'
01693 [L1474] MOV      A=58 B=0 C=32 D=32 
01694 [L1474] CALL     A=56 B=2 C=3 D=515 
01695 [L1474] MOV      A=54 B=0 C=56 D=56 
01696 [L1476] UGET     A=56 B=0 C=5 D=5 CCSprite
01697 [L1476] MOV      A=57 B=0 C=56 D=56 
01698 [L1476] TGETS    A=56 B=56 C=3 D=14339 'create'
01699 [L1476] KSTR     A=58 B=0 C=236 D=236 'v2/newIntroUI/cast_bkg.png'
01700 [L1476] CALL     A=56 B=2 C=3 D=515 
01701 [L1476] MOV      A=34 B=0 C=56 D=56 
01702 [L1477] GGET     A=56 B=0 C=11 D=11 'd_ms'
01703 [L1477] TGETS    A=56 B=56 C=12 D=14348 'd_u'
01704 [L1477] TGETS    A=56 B=56 C=13 D=14349 'setStyles'
01705 [L1477] MOV      A=57 B=0 C=34 D=34 
01706 [L1477] TDUP     A=58 B=0 C=238 D=238 {'kind': 'table', 'value': {'scale': 0.453125, 'x': 0.5}}
01707 [L1477] TDUP     A=59 B=0 C=237 D=237 {'kind': 'table', 'value': {1: 0.5, 2: 1}}
01708 [L1477] TSETS    A=59 B=58 C=93 D=14941 'anchor'
01709 [L1477] TSETS    A=38 B=58 C=32 D=14880 'y'
01710 [L1477] CALL     A=56 B=1 C=3 D=259 
01711 [L1478] MOV      A=57 B=0 C=18 D=18 
01712 [L1478] TGETS    A=56 B=18 C=7 D=4615 'addChild'
01713 [L1478] MOV      A=58 B=0 C=34 D=34 
01714 [L1478] CALL     A=56 B=1 C=3 D=259 
01715 [L1479] GGET     A=56 B=0 C=11 D=11 'd_ms'
01716 [L1479] TGETS    A=56 B=56 C=12 D=14348 'd_u'
01717 [L1479] TGETS    A=56 B=56 C=171 D=14507 'getRealScale'
01718 [L1479] MOV      A=57 B=0 C=34 D=34 
01719 [L1479] CALL     A=56 B=3 C=2 D=770 
01720 [L1480] ADDVV    A=27 B=27 C=57 D=6969 
01721 [L1483] MOV      A=59 B=0 C=18 D=18 
01722 [L1483] TGETS    A=58 B=18 C=7 D=4615 'addChild'
01723 [L1483] GGET     A=60 B=0 C=11 D=11 'd_ms'
01724 [L1483] TGETS    A=60 B=60 C=12 D=15372 'd_u'
01725 [L1483] TGETS    A=60 B=60 C=67 D=15427 'createByStyle'
01726 [L1483] TDUP     A=61 B=0 C=239 D=239 {'kind': 'table', 'value': {}}
01727 [L1483] TGETV    A=62 B=24 C=23 D=6167 
01728 [L1483] TSETS    A=62 B=61 C=139 D=15755 'pic'
01729 [L1483] MULNV    A=62 B=56 C=36 D=14372 
01730 [L1483] SUBNV    A=62 B=62 C=8 D=15880 
01731 [L1483] TSETS    A=62 B=61 C=30 D=15646 'x'
01732 [L1483] MULNV    A=62 B=57 C=24 D=14616 
01733 [L1483] SUBVV    A=62 B=38 C=62 D=9790 
01734 [L1483] TSETS    A=62 B=61 C=32 D=15648 'y'
01735 [L1483] TDUP     A=62 B=0 C=240 D=240 {'kind': 'table', 'value': {1: 1.1, 2: 0.5}}
01736 [L1483] TSETS    A=62 B=61 C=93 D=15709 'anchor'
01737 [L1483] CALL     A=60 B=0 C=2 D=2 
01738 [L1483] CALLM    A=58 B=1 C=1 D=257 
01739 [L1484] KSTR     A=58 B=0 C=241 D=241 '+'
01740 [L1484] UGET     A=59 B=0 C=18 D=18 math
01741 [L1484] TGETS    A=59 B=59 C=242 D=15346 'floor'
01742 [L1484] TGETS    A=60 B=54 C=243 D=14067 'percent'
01743 [L1484] MULVN    A=60 B=60 C=17 D=15377 
01744 [L1484] CALL     A=59 B=2 C=2 D=514 
01745 [L1484] KSTR     A=60 B=0 C=244 D=244 '% +'
01746 [L1484] TGETS    A=61 B=54 C=143 D=13967 'plus'
01747 [L1484] CAT      A=58 B=58 C=61 D=14909 
01748 [L1485] MOV      A=60 B=0 C=18 D=18 
01749 [L1485] TGETS    A=59 B=18 C=7 D=4615 'addChild'
01750 [L1485] GGET     A=61 B=0 C=11 D=11 'd_ms'
01751 [L1485] TGETS    A=61 B=61 C=12 D=15628 'd_u'
01752 [L1485] TGETS    A=61 B=61 C=67 D=15683 'createByStyle'
01753 [L1485] TDUP     A=62 B=0 C=245 D=245 {'kind': 'table', 'value': {'type': 'label', 'font': 'arial', 'fontsize': 26}}
01754 [L1485] MULNV    A=63 B=56 C=36 D=14372 
01755 [L1485] SUBNV    A=63 B=63 C=8 D=16136 
01756 [L1485] TSETS    A=63 B=62 C=30 D=15902 'x'
01757 [L1485] MULNV    A=63 B=57 C=24 D=14616 
01758 [L1485] SUBVV    A=63 B=38 C=63 D=9791 
01759 [L1485] TSETS    A=63 B=62 C=32 D=15904 'y'
01760 [L1485] TDUP     A=63 B=0 C=246 D=246 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
01761 [L1485] TSETS    A=63 B=62 C=93 D=15965 'anchor'
01762 [L1485] TSETS    A=58 B=62 C=70 D=15942 'string'
01763 [L1485] TDUP     A=63 B=0 C=247 D=247 {'kind': 'table', 'value': {1: 155, 2: 155, 3: 23}}
01764 [L1485] TSETS    A=63 B=62 C=76 D=15948 'color'
01765 [L1485] CALL     A=61 B=0 C=2 D=2 
01766 [L1485] CALLM    A=59 B=1 C=1 D=257 
01767 [L1488] ISF      A=0 B=0 C=2 D=2 
01768 [L1488] JMP      A=59 B=129 C=141 D=33165 target=2166
01769 [L1489] UGET     A=59 B=0 C=6 D=6 CCMenuItemImage
01770 [L1489] MOV      A=60 B=0 C=59 D=59 
01771 [L1489] TGETS    A=59 B=59 C=3 D=15107 'create'
01772 [L1489] KSTR     A=61 B=0 C=248 D=248 'v2/ascCast/btn21.png'
01773 [L1489] KSTR     A=62 B=0 C=249 D=249 'v2/ascCast/btn22.png'
01774 [L1489] CALL     A=59 B=2 C=4 D=516 
01775 [L1494] GGET     A=60 B=0 C=11 D=11 'd_ms'
01776 [L1494] TGETS    A=60 B=60 C=12 D=15372 'd_u'
01777 [L1494] TGETS    A=60 B=60 C=13 D=15373 'setStyles'
01778 [L1494] MOV      A=61 B=0 C=59 D=59 
01779 [L1494] TDUP     A=62 B=0 C=250 D=250 {'kind': 'table', 'value': {}}
01780 [L1494] MULNV    A=63 B=56 C=37 D=14373 
01781 [L1494] ADDNV    A=63 B=63 C=8 D=16136 
01782 [L1494] TSETS    A=63 B=62 C=30 D=15902 'x'
01783 [L1494] MULNV    A=63 B=57 C=24 D=14616 
01784 [L1494] SUBVV    A=63 B=38 C=63 D=9791 
01785 [L1494] TSETS    A=63 B=62 C=32 D=15904 'y'
01786 [L1494] CALL     A=60 B=1 C=3 D=259 
01787 [L1495] MOV      A=61 B=0 C=59 D=59 
01788 [L1495] TGETS    A=60 B=59 C=21 D=15125 'setTag'
01789 [L1495] GGET     A=62 B=0 C=22 D=22 'g_introButtonType'
01790 [L1495] TGETS    A=62 B=62 C=251 D=16123 'cast'
01791 [L1495] CALL     A=60 B=1 C=3 D=259 
01792 [L1496] MOV      A=61 B=0 C=59 D=59 
01793 [L1496] TGETS    A=60 B=59 C=213 D=15317 'setScale'
01794 [L1496] KNUM     A=62 B=0 C=26 D=26 0.9
01795 [L1496] CALL     A=60 B=1 C=3 D=259 
01796 [L1497] MOV      A=61 B=0 C=59 D=59 
01797 [L1497] TGETS    A=60 B=59 C=25 D=15129 'registerScriptTapHandler'
01798 [L1497] MOV      A=62 B=0 C=1 D=1 
01799 [L1497] CALL     A=60 B=1 C=3 D=259 
01800 [L1498] MOV      A=61 B=0 C=7 D=7 
01801 [L1498] TGETS    A=60 B=7 C=154 D=1946 'addObject'
01802 [L1498] MOV      A=62 B=0 C=59 D=59 
01803 [L1498] CALL     A=60 B=1 C=3 D=259 
01804 [L1499] JMP      A=56 B=129 C=105 D=33129 target=2166
01805 [L1502] TGETS    A=56 B=55 C=252 D=14332 'getExtraInfo'
01806 [L1502] TGETS    A=57 B=0 C=45 D=45 'csvInfo'
01807 [L1502] TGETS    A=57 B=57 C=46 D=14638 'quality'
01808 [L1502] TGETS    A=58 B=0 C=45 D=45 'csvInfo'
01809 [L1502] TGETS    A=58 B=58 C=59 D=14907 'mainType'
01810 [L1502] CALL     A=56 B=2 C=3 D=515 
01811 [L1503] LEN      A=57 B=0 C=56 D=56 
01812 [L1504] UGET     A=58 B=0 C=5 D=5 CCSprite
01813 [L1504] MOV      A=59 B=0 C=58 D=58 
01814 [L1504] TGETS    A=58 B=58 C=3 D=14851 'create'
01815 [L1504] KSTR     A=60 B=0 C=253 D=253 'v2/newIntroUI/ad_bkg.png'
01816 [L1504] CALL     A=58 B=2 C=3 D=515 
01817 [L1504] MOV      A=34 B=0 C=58 D=58 
01818 [L1505] GGET     A=58 B=0 C=11 D=11 'd_ms'
01819 [L1505] TGETS    A=58 B=58 C=12 D=14860 'd_u'
01820 [L1505] TGETS    A=58 B=58 C=13 D=14861 'setStyles'
01821 [L1505] MOV      A=59 B=0 C=34 D=34 
01822 [L1505] TDUP     A=60 B=0 C=255 D=255 {'kind': 'table', 'value': {'x': 0.5}}
01823 [L1505] TDUP     A=61 B=0 C=254 D=254 {'kind': 'table', 'value': {1: 0.5, 2: 1}}
01824 [L1505] TSETS    A=61 B=60 C=93 D=15453 'anchor'
01825 [L1505] TSETS    A=38 B=60 C=32 D=15392 'y'
01826 [L1505] CALL     A=58 B=1 C=3 D=259 
01827 [L1506] KSHORT   A=58 B=0 C=4 D=4 4
01828 [L1506] ISGE     A=58 B=0 C=57 D=57 
01829 [L1506] JMP      A=58 B=128 C=1 D=32769 target=1831
01830 [L1507] KSHORT   A=57 B=0 C=4 D=4 4
01831 [L1509] MOV      A=59 B=0 C=18 D=18 
01832 [L1509] TGETS    A=58 B=18 C=7 D=4615 'addChild'
01833 [L1509] MOV      A=60 B=0 C=34 D=34 
01834 [L1509] CALL     A=58 B=1 C=3 D=259 
01835 [L1510] GGET     A=58 B=0 C=11 D=11 'd_ms'
01836 [L1510] TGETS    A=58 B=58 C=12 D=14860 'd_u'
01837 [L1510] TGETS    A=58 B=58 C=171 D=15019 'getRealScale'
01838 [L1510] MOV      A=59 B=0 C=34 D=34 
01839 [L1510] CALL     A=58 B=3 C=2 D=770 
01840 [L1511] ADDVV    A=27 B=27 C=59 D=6971 
01841 [L1513] TNEW     A=60 B=0 C=6 D=6 
01842 [L1513] MULNV    A=61 B=59 C=38 D=15142 
01843 [L1513] SUBVV    A=61 B=38 C=61 D=9789 
01844 [L1513] TSETB    A=61 B=60 C=1 D=15361 
01845 [L1513] MULNV    A=61 B=59 C=36 D=15140 
01846 [L1513] SUBVV    A=61 B=38 C=61 D=9789 
01847 [L1513] TSETB    A=61 B=60 C=2 D=15362 
01848 [L1513] MULNV    A=61 B=59 C=39 D=15143 
01849 [L1513] SUBVV    A=61 B=38 C=61 D=9789 
01850 [L1513] TSETB    A=61 B=60 C=3 D=15363 
01851 [L1513] MULNV    A=61 B=59 C=8 D=15112 
01852 [L1513] SUBVV    A=61 B=38 C=61 D=9789 
01853 [L1513] TSETB    A=61 B=60 C=4 D=15364 
01854 [L1513] MULNV    A=61 B=59 C=22 D=15126 
01855 [L1513] SUBVV    A=61 B=38 C=61 D=9789 
01856 [L1513] TSETB    A=61 B=60 C=5 D=15365 
01857 [L1514] TDUP     A=61 B=1 C=1 D=257 {'kind': 'table', 'value': {}}
01858 [L1514] TDUP     A=62 B=1 C=0 D=256 {'kind': 'table', 'value': {1: 155, 2: 155, 3: 23}}
01859 [L1514] KSTR     A=63 B=1 C=2 D=258 'greenow'
01860 [L1514] TSETV    A=62 B=61 C=63 D=15679 
01861 [L1515] TDUP     A=62 B=1 C=3 D=259 {'kind': 'table', 'value': {1: 125, 2: 125, 3: 125}}
01862 [L1515] KSTR     A=63 B=1 C=4 D=260 'gray'
01863 [L1515] TSETV    A=62 B=61 C=63 D=15679 
01864 [L1516] TDUP     A=62 B=1 C=5 D=261 {'kind': 'table', 'value': {1: 254, 2: 235, 3: 192}}
01865 [L1516] KSTR     A=63 B=1 C=6 D=262 'paper'
01866 [L1516] TSETV    A=62 B=61 C=63 D=15679 
01867 [L1517] KNIL     A=62 B=0 C=65 D=65 
01868 [L1519] MULNV    A=66 B=58 C=25 D=14873 
01869 [L1519] SUBNV    A=65 B=66 C=8 D=16904 
01870 [L1520] KSTR     A=66 B=1 C=7 D=263 'getNumHZ'
01871 [L1520] TGETV    A=66 B=55 C=66 D=14146 
01872 [L1520] MOV      A=67 B=0 C=29 D=29 
01873 [L1520] CALL     A=66 B=2 C=2 D=514 
01874 [L1520] GGET     A=67 B=0 C=11 D=11 'd_ms'
01875 [L1520] TGETS    A=67 B=67 C=79 D=17231 'd_hz'
01876 [L1520] TGETS    A=67 B=67 C=80 D=17232 'gethz'
01877 [L1520] KSTR     A=68 B=1 C=8 D=264 'jie_hz'
01878 [L1520] CALL     A=67 B=2 C=2 D=514 
01879 [L1520] KSTR     A=68 B=1 C=9 D=265 '  '
01880 [L1520] CAT      A=62 B=66 C=68 D=16964 
01881 [L1521] GGET     A=66 B=0 C=11 D=11 'd_ms'
01882 [L1521] TGETS    A=66 B=66 C=12 D=16908 'd_u'
01883 [L1521] TGETS    A=66 B=66 C=67 D=16963 'createByStyle'
01884 [L1521] TDUP     A=67 B=1 C=10 D=266 {'kind': 'table', 'value': {'type': 'label', 'font': 'arial', 'fontsize': 26}}
01885 [L1521] TSETS    A=65 B=67 C=30 D=17182 'x'
01886 [L1521] TGETB    A=68 B=60 C=1 D=15361 
01887 [L1521] TSETS    A=68 B=67 C=32 D=17184 'y'
01888 [L1521] TDUP     A=68 B=1 C=11 D=267 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
01889 [L1521] TSETS    A=68 B=67 C=93 D=17245 'anchor'
01890 [L1521] TSETS    A=62 B=67 C=70 D=17222 'string'
01891 [L1521] KSTR     A=68 B=1 C=2 D=258 'greenow'
01892 [L1521] TGETV    A=68 B=61 C=68 D=15684 
01893 [L1521] TSETS    A=68 B=67 C=76 D=17228 'color'
01894 [L1521] CALL     A=66 B=2 C=2 D=514 
01895 [L1521] MOV      A=63 B=0 C=66 D=66 
01896 [L1522] GGET     A=66 B=0 C=11 D=11 'd_ms'
01897 [L1522] TGETS    A=66 B=66 C=12 D=16908 'd_u'
01898 [L1522] TGETS    A=66 B=66 C=171 D=17067 'getRealScale'
01899 [L1522] MOV      A=67 B=0 C=63 D=63 
01900 [L1522] CALL     A=66 B=2 C=2 D=514 
01901 [L1522] MOV      A=64 B=0 C=66 D=66 
01902 [L1523] MOV      A=67 B=0 C=18 D=18 
01903 [L1523] TGETS    A=66 B=18 C=7 D=4615 'addChild'
01904 [L1523] MOV      A=68 B=0 C=63 D=63 
01905 [L1523] CALL     A=66 B=1 C=3 D=259 
01906 [L1526] ADDVV    A=65 B=65 C=64 D=16704 
01907 [L1527] KSHORT   A=66 B=0 C=1 D=1 1
01908 [L1527] TGETS    A=67 B=55 C=126 D=14206 'g_self'
01909 [L1527] KSTR     A=68 B=1 C=12 D=268 'MAX_STAR_COUNT'
01910 [L1527] TGETV    A=67 B=67 C=68 D=17220 
01911 [L1527] KSHORT   A=68 B=0 C=1 D=1 1
01912 [L1527] FORI     A=66 B=128 C=101 D=32869 target=2014
01913 [L1528] SUBVN    A=70 B=69 C=14 D=17678 
01914 [L1528] MULVN    A=70 B=70 C=40 D=17960 
01915 [L1528] MULVV    A=70 B=70 C=35 D=17955 
01916 [L1528] ADDVV    A=70 B=65 C=70 D=16710 
01917 [L1529] GGET     A=71 B=0 C=11 D=11 'd_ms'
01918 [L1529] TGETS    A=71 B=71 C=12 D=18188 'd_u'
01919 [L1529] TGETS    A=71 B=71 C=67 D=18243 'createByStyle'
01920 [L1529] TDUP     A=72 B=1 C=13 D=269 {'kind': 'table', 'value': {'pic': 'v2/equipAdvanceUI/star_emp.png'}}
01921 [L1529] TSETS    A=70 B=72 C=30 D=18462 'x'
01922 [L1529] TGETB    A=73 B=60 C=1 D=15361 
01923 [L1529] TSETS    A=73 B=72 C=32 D=18464 'y'
01924 [L1529] TDUP     A=73 B=1 C=14 D=270 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
01925 [L1529] TSETS    A=73 B=72 C=93 D=18525 'anchor'
01926 [L1529] CALL     A=71 B=2 C=2 D=514 
01927 [L1529] MOV      A=63 B=0 C=71 D=71 
01928 [L1530] MOV      A=72 B=0 C=63 D=63 
01929 [L1530] TGETS    A=71 B=63 C=213 D=16341 'setScale'
01930 [L1530] KNUM     A=73 B=0 C=41 D=41 0.8
01931 [L1530] CALL     A=71 B=1 C=3 D=259 
01932 [L1531] MOV      A=72 B=0 C=18 D=18 
01933 [L1531] TGETS    A=71 B=18 C=7 D=4615 'addChild'
01934 [L1531] MOV      A=73 B=0 C=63 D=63 
01935 [L1531] CALL     A=71 B=1 C=3 D=259 
01936 [L1532] ISLE     A=69 B=0 C=30 D=30 
01937 [L1532] JMP      A=71 B=128 C=5 D=32773 target=1943
01938 [L1532] TGETS    A=71 B=55 C=126 D=14206 'g_self'
01939 [L1532] KSTR     A=72 B=1 C=15 D=271 'MAX_ADVANCE_LEVEL'
01940 [L1532] TGETV    A=71 B=71 C=72 D=18248 
01941 [L1532] ISNEV    A=29 B=0 C=71 D=71 
01942 [L1532] JMP      A=71 B=128 C=20 D=32788 target=1963
01943 [L1533] GGET     A=71 B=0 C=11 D=11 'd_ms'
01944 [L1533] TGETS    A=71 B=71 C=12 D=18188 'd_u'
01945 [L1533] TGETS    A=71 B=71 C=67 D=18243 'createByStyle'
01946 [L1533] TDUP     A=72 B=1 C=16 D=272 {'kind': 'table', 'value': {'pic': 'v2/equipAdvanceUI/star_fill.png'}}
01947 [L1533] TSETS    A=70 B=72 C=30 D=18462 'x'
01948 [L1533] TGETB    A=73 B=60 C=1 D=15361 
01949 [L1533] TSETS    A=73 B=72 C=32 D=18464 'y'
01950 [L1533] TDUP     A=73 B=1 C=17 D=273 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
01951 [L1533] TSETS    A=73 B=72 C=93 D=18525 'anchor'
01952 [L1533] CALL     A=71 B=2 C=2 D=514 
01953 [L1533] MOV      A=63 B=0 C=71 D=71 
01954 [L1534] MOV      A=72 B=0 C=63 D=63 
01955 [L1534] TGETS    A=71 B=63 C=213 D=16341 'setScale'
01956 [L1534] KNUM     A=73 B=0 C=41 D=41 0.8
01957 [L1534] CALL     A=71 B=1 C=3 D=259 
01958 [L1535] MOV      A=72 B=0 C=18 D=18 
01959 [L1535] TGETS    A=71 B=18 C=7 D=4615 'addChild'
01960 [L1535] MOV      A=73 B=0 C=63 D=63 
01961 [L1535] CALL     A=71 B=1 C=3 D=259 
01962 [L1535] JMP      A=71 B=128 C=50 D=32818 target=2013
01963 [L1536] ADDVN    A=71 B=30 C=14 D=7694 
01964 [L1536] ISNEV    A=69 B=0 C=71 D=71 
01965 [L1536] JMP      A=71 B=128 C=47 D=32815 target=2013
01966 [L1537] TGETS    A=71 B=55 C=126 D=14206 'g_self'
01967 [L1537] KSTR     A=72 B=1 C=18 D=274 'StarCost'
01968 [L1537] TGETV    A=71 B=71 C=72 D=18248 
01969 [L1537] TGETS    A=72 B=0 C=45 D=45 'csvInfo'
01970 [L1537] TGETS    A=72 B=72 C=46 D=18478 'quality'
01971 [L1537] TGETV    A=71 B=71 C=72 D=18248 
01972 [L1537] TGETS    A=72 B=0 C=45 D=45 'csvInfo'
01973 [L1537] TGETS    A=72 B=72 C=59 D=18491 'mainType'
01974 [L1537] TGETV    A=71 B=71 C=72 D=18248 
01975 [L1537] ADDVN    A=72 B=29 C=14 D=7438 
01976 [L1537] TGETV    A=71 B=71 C=72 D=18248 
01977 [L1537] ADDVN    A=72 B=30 C=14 D=7694 
01978 [L1537] TGETV    A=71 B=71 C=72 D=18248 
01979 [L1537] DIVVV    A=62 B=31 C=71 D=8007 
01980 [L1538] GGET     A=71 B=0 C=11 D=11 'd_ms'
01981 [L1538] TGETS    A=71 B=71 C=12 D=18188 'd_u'
01982 [L1538] TGETS    A=71 B=71 C=67 D=18243 'createByStyle'
01983 [L1538] TDUP     A=72 B=1 C=19 D=275 {'kind': 'table', 'value': {'pic': 'v2/equipAdvanceUI/star_fill.png'}}
01984 [L1538] TSETS    A=70 B=72 C=30 D=18462 'x'
01985 [L1538] TGETB    A=73 B=60 C=1 D=15361 
01986 [L1538] TSETS    A=73 B=72 C=32 D=18464 'y'
01987 [L1538] TDUP     A=73 B=1 C=20 D=276 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
01988 [L1538] TSETS    A=73 B=72 C=93 D=18525 'anchor'
01989 [L1538] CALL     A=71 B=2 C=2 D=514 
01990 [L1538] MOV      A=63 B=0 C=71 D=71 
01991 [L1539] MOV      A=72 B=0 C=63 D=63 
01992 [L1539] TGETS    A=71 B=63 C=43 D=16171 'getContentSize'
01993 [L1539] CALL     A=71 B=2 C=2 D=514 
01994 [L1540] MOV      A=73 B=0 C=63 D=63 
01995 [L1540] KSTR     A=74 B=1 C=21 D=277 'setTextureRect'
01996 [L1540] TGETV    A=72 B=63 C=74 D=16202 
01997 [L1540] UGET     A=74 B=0 C=10 D=10 CCRectMake
01998 [L1540] KSHORT   A=75 B=0 C=0 D=0 0
01999 [L1540] KSHORT   A=76 B=0 C=0 D=0 0
02000 [L1540] TGETS    A=77 B=71 C=28 D=18204 'width'
02001 [L1540] MULVV    A=77 B=77 C=62 D=19774 
02002 [L1540] TGETS    A=78 B=71 C=31 D=18207 'height'
02003 [L1540] CALL     A=74 B=0 C=5 D=5 
02004 [L1540] CALLM    A=72 B=1 C=1 D=257 
02005 [L1541] MOV      A=73 B=0 C=63 D=63 
02006 [L1541] TGETS    A=72 B=63 C=213 D=16341 'setScale'
02007 [L1541] KNUM     A=74 B=0 C=41 D=41 0.8
02008 [L1541] CALL     A=72 B=1 C=3 D=259 
02009 [L1542] MOV      A=73 B=0 C=18 D=18 
02010 [L1542] TGETS    A=72 B=18 C=7 D=4615 'addChild'
02011 [L1542] MOV      A=74 B=0 C=63 D=63 
02012 [L1542] CALL     A=72 B=1 C=3 D=259 
02013 [L1527] FORL     A=66 B=127 C=155 D=32667 target=1913
02014 [L1546] KSTR     A=66 B=0 C=241 D=241 '+'
02015 [L1546] UGET     A=67 B=0 C=18 D=18 math
02016 [L1546] TGETS    A=67 B=67 C=242 D=17394 'floor'
02017 [L1546] TGETS    A=68 B=53 C=243 D=13811 'percent'
02018 [L1546] MULNV    A=68 B=68 C=17 D=17425 
02019 [L1546] CALL     A=67 B=2 C=2 D=514 
02020 [L1546] KSTR     A=68 B=0 C=244 D=244 '% +'
02021 [L1546] TGETS    A=69 B=53 C=143 D=13711 'plus'
02022 [L1546] CAT      A=62 B=66 C=69 D=16965 
02023 [L1547] GGET     A=66 B=0 C=11 D=11 'd_ms'
02024 [L1547] TGETS    A=66 B=66 C=12 D=16908 'd_u'
02025 [L1547] TGETS    A=66 B=66 C=67 D=16963 'createByStyle'
02026 [L1547] TDUP     A=67 B=1 C=22 D=278 {'kind': 'table', 'value': {'type': 'label', 'font': 'arial', 'fontsize': 26}}
02027 [L1547] MULNV    A=68 B=35 C=31 D=8991 
02028 [L1547] ADDNV    A=68 B=68 C=8 D=17416 
02029 [L1547] TSETS    A=68 B=67 C=30 D=17182 'x'
02030 [L1547] TGETB    A=68 B=60 C=1 D=15361 
02031 [L1547] TSETS    A=68 B=67 C=32 D=17184 'y'
02032 [L1547] TDUP     A=68 B=1 C=23 D=279 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
02033 [L1547] TSETS    A=68 B=67 C=93 D=17245 'anchor'
02034 [L1547] TSETS    A=62 B=67 C=70 D=17222 'string'
02035 [L1547] KSTR     A=68 B=1 C=2 D=258 'greenow'
02036 [L1547] TGETV    A=68 B=61 C=68 D=15684 
02037 [L1547] TSETS    A=68 B=67 C=76 D=17228 'color'
02038 [L1547] CALL     A=66 B=2 C=2 D=514 
02039 [L1547] MOV      A=63 B=0 C=66 D=66 
02040 [L1548] MOV      A=67 B=0 C=18 D=18 
02041 [L1548] TGETS    A=66 B=18 C=7 D=4615 'addChild'
02042 [L1548] MOV      A=68 B=0 C=63 D=63 
02043 [L1548] CALL     A=66 B=1 C=3 D=259 
02044 [L1551] TGETB    A=66 B=60 C=5 D=15365 
02045 [L1551] TGETB    A=67 B=60 C=4 D=15364 
02046 [L1551] SUBVV    A=66 B=66 C=67 D=16963 
02047 [L1551] DIVVN    A=66 B=66 C=42 D=16938 
02048 [L1552] MULNV    A=67 B=58 C=39 D=14887 
02049 [L1552] SUBNV    A=65 B=67 C=8 D=17160 
02050 [L1553] KSHORT   A=67 B=0 C=1 D=1 1
02051 [L1553] MOV      A=68 B=0 C=57 D=57 
02052 [L1553] KSHORT   A=69 B=0 C=1 D=1 1
02053 [L1553] FORI     A=67 B=128 C=63 D=32831 target=2117
02054 [L1554] TGETV    A=71 B=56 C=70 D=14406 
02055 [L1554] TGETS    A=71 B=71 C=77 D=18253 'level'
02056 [L1554] ISGE     A=29 B=0 C=71 D=71 
02057 [L1554] JMP      A=71 B=128 C=4 D=32772 target=2062
02058 [L1554] KSTR     A=71 B=1 C=4 D=260 'gray'
02059 [L1554] TGETV    A=71 B=61 C=71 D=15687 
02060 [L1554] IST      A=0 B=0 C=71 D=71 
02061 [L1554] JMP      A=72 B=128 C=2 D=32770 target=2064
02062 [L1554] KSTR     A=71 B=1 C=6 D=262 'paper'
02063 [L1554] TGETV    A=71 B=61 C=71 D=15687 
02064 [L1555] GGET     A=72 B=0 C=11 D=11 'd_ms'
02065 [L1555] TGETS    A=72 B=72 C=12 D=18444 'd_u'
02066 [L1555] TGETS    A=72 B=72 C=67 D=18499 'createByStyle'
02067 [L1555] TDUP     A=73 B=1 C=24 D=280 {'kind': 'table', 'value': {'type': 'label', 'font': 'arial', 'fontsize': 22}}
02068 [L1555] TSETS    A=65 B=73 C=30 D=18718 'x'
02069 [L1555] TGETB    A=74 B=60 C=4 D=15364 
02070 [L1555] SUBVN    A=75 B=70 C=14 D=17934 
02071 [L1555] MULVV    A=75 B=75 C=66 D=19266 
02072 [L1555] ADDVV    A=74 B=74 C=75 D=19019 
02073 [L1555] TSETS    A=74 B=73 C=32 D=18720 'y'
02074 [L1555] TDUP     A=74 B=1 C=25 D=281 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
02075 [L1555] TSETS    A=74 B=73 C=93 D=18781 'anchor'
02076 [L1555] TGETV    A=74 B=56 C=70 D=14406 
02077 [L1555] TGETB    A=74 B=74 C=1 D=18945 
02078 [L1555] TSETS    A=74 B=73 C=70 D=18758 'string'
02079 [L1555] TSETS    A=71 B=73 C=76 D=18764 'color'
02080 [L1555] CALL     A=72 B=2 C=2 D=514 
02081 [L1555] MOV      A=63 B=0 C=72 D=72 
02082 [L1556] GGET     A=72 B=0 C=11 D=11 'd_ms'
02083 [L1556] TGETS    A=72 B=72 C=12 D=18444 'd_u'
02084 [L1556] TGETS    A=72 B=72 C=171 D=18603 'getRealScale'
02085 [L1556] MOV      A=73 B=0 C=63 D=63 
02086 [L1556] CALL     A=72 B=2 C=2 D=514 
02087 [L1556] MOV      A=64 B=0 C=72 D=72 
02088 [L1557] MOV      A=73 B=0 C=18 D=18 
02089 [L1557] TGETS    A=72 B=18 C=7 D=4615 'addChild'
02090 [L1557] MOV      A=74 B=0 C=63 D=63 
02091 [L1557] CALL     A=72 B=1 C=3 D=259 
02092 [L1559] GGET     A=72 B=0 C=11 D=11 'd_ms'
02093 [L1559] TGETS    A=72 B=72 C=12 D=18444 'd_u'
02094 [L1559] TGETS    A=72 B=72 C=67 D=18499 'createByStyle'
02095 [L1559] TDUP     A=73 B=1 C=26 D=282 {'kind': 'table', 'value': {'type': 'label', 'font': 'arial', 'fontsize': 22}}
02096 [L1559] MULNV    A=74 B=64 C=43 D=16427 
02097 [L1559] ADDVV    A=74 B=65 C=74 D=16714 
02098 [L1559] TSETS    A=74 B=73 C=30 D=18718 'x'
02099 [L1559] TGETB    A=74 B=60 C=4 D=15364 
02100 [L1559] SUBVN    A=75 B=70 C=14 D=17934 
02101 [L1559] MULVV    A=75 B=75 C=66 D=19266 
02102 [L1559] ADDVV    A=74 B=74 C=75 D=19019 
02103 [L1559] TSETS    A=74 B=73 C=32 D=18720 'y'
02104 [L1559] TDUP     A=74 B=1 C=27 D=283 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
02105 [L1559] TSETS    A=74 B=73 C=93 D=18781 'anchor'
02106 [L1559] TGETV    A=74 B=56 C=70 D=14406 
02107 [L1559] TGETB    A=74 B=74 C=2 D=18946 
02108 [L1559] TSETS    A=74 B=73 C=70 D=18758 'string'
02109 [L1559] TSETS    A=71 B=73 C=76 D=18764 'color'
02110 [L1559] CALL     A=72 B=2 C=2 D=514 
02111 [L1559] MOV      A=63 B=0 C=72 D=72 
02112 [L1560] MOV      A=73 B=0 C=18 D=18 
02113 [L1560] TGETS    A=72 B=18 C=7 D=4615 'addChild'
02114 [L1560] MOV      A=74 B=0 C=63 D=63 
02115 [L1560] CALL     A=72 B=1 C=3 D=259 
02116 [L1553] FORL     A=67 B=127 C=193 D=32705 target=2054
02117 [L1564] ISF      A=0 B=0 C=2 D=2 
02118 [L1564] JMP      A=67 B=128 C=47 D=32815 target=2166
02119 [L1565] UGET     A=67 B=0 C=6 D=6 CCMenuItemImage
02120 [L1565] MOV      A=68 B=0 C=67 D=67 
02121 [L1565] TGETS    A=67 B=67 C=3 D=17155 'create'
02122 [L1565] KSTR     A=69 B=1 C=28 D=284 'v2/equipAdvanceUI/advance1.png'
02123 [L1565] KSTR     A=70 B=1 C=29 D=285 'v2/equipAdvanceUI/advance2.png'
02124 [L1565] CALL     A=67 B=2 C=4 D=516 
02125 [L1567] GGET     A=68 B=0 C=11 D=11 'd_ms'
02126 [L1567] TGETS    A=68 B=68 C=214 D=17622 'd_equipAdvanceUI'
02127 [L1567] KSTR     A=69 B=1 C=30 D=286 'canJoin'
02128 [L1567] TGETV    A=68 B=68 C=69 D=17477 
02129 [L1567] CALL     A=68 B=2 C=1 D=513 
02130 [L1567] IST      A=0 B=0 C=68 D=68 
02131 [L1567] JMP      A=68 B=128 C=5 D=32773 target=2137
02132 [L1568] GGET     A=68 B=0 C=11 D=11 'd_ms'
02133 [L1568] TGETS    A=68 B=68 C=12 D=17420 'd_u'
02134 [L1568] TGETS    A=68 B=68 C=155 D=17563 'grayMenuItem'
02135 [L1568] MOV      A=69 B=0 C=67 D=67 
02136 [L1568] CALL     A=68 B=1 C=2 D=258 
02137 [L1570] GGET     A=68 B=0 C=11 D=11 'd_ms'
02138 [L1570] TGETS    A=68 B=68 C=12 D=17420 'd_u'
02139 [L1570] TGETS    A=68 B=68 C=13 D=17421 'setStyles'
02140 [L1570] MOV      A=69 B=0 C=67 D=67 
02141 [L1570] TDUP     A=70 B=1 C=31 D=287 {'kind': 'table', 'value': {}}
02142 [L1570] MULNV    A=71 B=58 C=37 D=14885 
02143 [L1570] ADDNV    A=71 B=71 C=8 D=18184 
02144 [L1570] TSETS    A=71 B=70 C=30 D=17950 'x'
02145 [L1570] TGETB    A=71 B=60 C=4 D=15364 
02146 [L1570] TSETS    A=71 B=70 C=32 D=17952 'y'
02147 [L1570] CALL     A=68 B=1 C=3 D=259 
02148 [L1571] MOV      A=69 B=0 C=67 D=67 
02149 [L1571] TGETS    A=68 B=67 C=21 D=17173 'setTag'
02150 [L1571] GGET     A=70 B=0 C=22 D=22 'g_introButtonType'
02151 [L1571] KSTR     A=71 B=1 C=32 D=288 'advance'
02152 [L1571] TGETV    A=70 B=70 C=71 D=17991 
02153 [L1571] CALL     A=68 B=1 C=3 D=259 
02154 [L1572] MOV      A=69 B=0 C=67 D=67 
02155 [L1572] TGETS    A=68 B=67 C=213 D=17365 'setScale'
02156 [L1572] KNUM     A=70 B=0 C=26 D=26 0.9
02157 [L1572] CALL     A=68 B=1 C=3 D=259 
02158 [L1573] MOV      A=69 B=0 C=67 D=67 
02159 [L1573] TGETS    A=68 B=67 C=25 D=17177 'registerScriptTapHandler'
02160 [L1573] MOV      A=70 B=0 C=1 D=1 
02161 [L1573] CALL     A=68 B=1 C=3 D=259 
02162 [L1574] MOV      A=69 B=0 C=7 D=7 
02163 [L1574] TGETS    A=68 B=7 C=154 D=1946 'addObject'
02164 [L1574] MOV      A=70 B=0 C=67 D=67 
02165 [L1574] CALL     A=68 B=1 C=3 D=259 
02166 [L1579] MOV      A=56 B=0 C=18 D=18 
02167 [L1579] TGETS    A=55 B=18 C=7 D=4615 'addChild'
02168 [L1579] GGET     A=57 B=0 C=11 D=11 'd_ms'
02169 [L1579] TGETS    A=57 B=57 C=12 D=14604 'd_u'
02170 [L1579] TGETS    A=57 B=57 C=67 D=14659 'createByStyle'
02171 [L1579] TDUP     A=58 B=1 C=33 D=289 {'kind': 'table', 'value': {}}
02172 [L1579] TGETV    A=59 B=24 C=23 D=6167 
02173 [L1579] TSETS    A=59 B=58 C=139 D=14987 'pic'
02174 [L1579] MULNV    A=59 B=35 C=25 D=8985 
02175 [L1579] ADDVV    A=59 B=37 C=59 D=9531 
02176 [L1579] TSETS    A=59 B=58 C=30 D=14878 'x'
02177 [L1579] MULNV    A=59 B=36 C=44 D=9260 
02178 [L1579] ADDVV    A=59 B=38 C=59 D=9787 
02179 [L1579] TSETS    A=59 B=58 C=32 D=14880 'y'
02180 [L1579] TDUP     A=59 B=1 C=34 D=290 {'kind': 'table', 'value': {1: 1.1, 2: 0.5}}
02181 [L1579] TSETS    A=59 B=58 C=93 D=14941 'anchor'
02182 [L1579] CALL     A=57 B=0 C=2 D=2 
02183 [L1579] CALLM    A=55 B=1 C=1 D=257 
02184 [L1581] TNEW     A=55 B=0 C=0 D=0 
02185 [L1582] GGET     A=56 B=0 C=11 D=11 'd_ms'
02186 [L1582] TGETS    A=56 B=56 C=189 D=14525 'd_stoneUI'
02187 [L1582] KSTR     A=57 B=1 C=35 D=291 'getEquipBaseEffect'
02188 [L1582] TGETV    A=56 B=56 C=57 D=14393 
02189 [L1582] MOV      A=57 B=0 C=0 D=0 
02190 [L1582] KPRI     A=58 B=0 C=0 D=0 
02191 [L1582] TGETS    A=59 B=0 C=188 D=188 'star_level'
02192 [L1582] CALL     A=56 B=2 C=4 D=516 
02193 [L1583] UGET     A=57 B=0 C=19 D=19 table
02194 [L1583] KSTR     A=58 B=1 C=36 D=292 'insert'
02195 [L1583] TGETV    A=57 B=57 C=58 D=14650 
02196 [L1583] MOV      A=58 B=0 C=55 D=55 
02197 [L1583] UGET     A=59 B=0 C=18 D=18 math
02198 [L1583] TGETS    A=59 B=59 C=242 D=15346 'floor'
02199 [L1583] MOV      A=60 B=0 C=56 D=56 
02200 [L1583] CALL     A=59 B=0 C=2 D=2 
02201 [L1583] CALLM    A=57 B=1 C=1 D=257 
02202 [L1585] UGET     A=57 B=0 C=19 D=19 table
02203 [L1585] KSTR     A=58 B=1 C=36 D=292 'insert'
02204 [L1585] TGETV    A=57 B=57 C=58 D=14650 
02205 [L1585] MOV      A=58 B=0 C=55 D=55 
02206 [L1585] UGET     A=59 B=0 C=18 D=18 math
02207 [L1585] TGETS    A=59 B=59 C=242 D=15346 'floor'
02208 [L1585] MULVV    A=60 B=56 C=47 D=14383 
02209 [L1585] CALL     A=59 B=0 C=2 D=2 
02210 [L1585] CALLM    A=57 B=1 C=1 D=257 
02211 [L1587] ISF      A=0 B=0 C=53 D=53 
02212 [L1587] JMP      A=57 B=128 C=13 D=32781 target=2226
02213 [L1588] TGETS    A=57 B=53 C=143 D=13711 'plus'
02214 [L1588] TGETS    A=58 B=53 C=243 D=13811 'percent'
02215 [L1588] MULVV    A=58 B=56 C=58 D=14394 
02216 [L1588] ADDVV    A=57 B=57 C=58 D=14650 
02217 [L1589] UGET     A=58 B=0 C=19 D=19 table
02218 [L1589] KSTR     A=59 B=1 C=36 D=292 'insert'
02219 [L1589] TGETV    A=58 B=58 C=59 D=14907 
02220 [L1589] MOV      A=59 B=0 C=55 D=55 
02221 [L1589] UGET     A=60 B=0 C=18 D=18 math
02222 [L1589] TGETS    A=60 B=60 C=242 D=15602 'floor'
02223 [L1589] MOV      A=61 B=0 C=57 D=57 
02224 [L1589] CALL     A=60 B=0 C=2 D=2 
02225 [L1589] CALLM    A=58 B=1 C=1 D=257 
02226 [L1592] ISF      A=0 B=0 C=54 D=54 
02227 [L1592] JMP      A=57 B=128 C=13 D=32781 target=2241
02228 [L1593] TGETS    A=57 B=54 C=143 D=13967 'plus'
02229 [L1593] TGETS    A=58 B=54 C=243 D=14067 'percent'
02230 [L1593] MULVV    A=58 B=56 C=58 D=14394 
02231 [L1593] ADDVV    A=57 B=57 C=58 D=14650 
02232 [L1594] UGET     A=58 B=0 C=19 D=19 table
02233 [L1594] KSTR     A=59 B=1 C=36 D=292 'insert'
02234 [L1594] TGETV    A=58 B=58 C=59 D=14907 
02235 [L1594] MOV      A=59 B=0 C=55 D=55 
02236 [L1594] UGET     A=60 B=0 C=18 D=18 math
02237 [L1594] TGETS    A=60 B=60 C=242 D=15602 'floor'
02238 [L1594] MOV      A=61 B=0 C=57 D=57 
02239 [L1594] CALL     A=60 B=0 C=2 D=2 
02240 [L1594] CALLM    A=58 B=1 C=1 D=257 
02241 [L1596] KPRI     A=57 B=0 C=0 D=0 
02242 [L1597] LEN      A=58 B=0 C=55 D=55 
02243 [L1597] KSHORT   A=59 B=0 C=2 D=2 2
02244 [L1597] KSHORT   A=60 B=255 C=255 D=65535 -1
02245 [L1597] FORI     A=58 B=128 C=13 D=32781 target=2259
02246 [L1598] IST      A=0 B=0 C=57 D=57 
02247 [L1598] JMP      A=62 B=128 C=4 D=32772 target=2252
02248 [L1598] TGETV    A=62 B=55 C=61 D=14141 
02249 [L1598] KSHORT   A=63 B=0 C=0 D=0 0
02250 [L1598] ISGE     A=63 B=0 C=62 D=62 
02251 [L1598] JMP      A=62 B=128 C=6 D=32774 target=2258
02252 [L1599] KSTR     A=62 B=0 C=241 D=241 '+'
02253 [L1599] TGETV    A=63 B=55 C=61 D=14141 
02254 [L1599] ISTC     A=64 B=0 C=57 D=57 
02255 [L1599] JMP      A=64 B=128 C=1 D=32769 target=2257
02256 [L1599] KSTR     A=64 B=1 C=37 D=293 ''
02257 [L1599] CAT      A=57 B=62 C=64 D=15936 
02258 [L1597] FORL     A=58 B=127 C=243 D=32755 target=2246
02259 [L1602] UGET     A=58 B=0 C=13 D=13 tostring
02260 [L1602] TGETB    A=59 B=55 C=1 D=14081 
02261 [L1602] CALL     A=58 B=2 C=2 D=514 
02262 [L1602] ISTC     A=59 B=0 C=57 D=57 
02263 [L1602] JMP      A=59 B=128 C=1 D=32769 target=2265
02264 [L1602] KSTR     A=59 B=1 C=37 D=293 ''
02265 [L1602] CAT      A=57 B=58 C=59 D=14907 
02266 [L1603] MOV      A=59 B=0 C=18 D=18 
02267 [L1603] TGETS    A=58 B=18 C=7 D=4615 'addChild'
02268 [L1603] GGET     A=60 B=0 C=11 D=11 'd_ms'
02269 [L1603] TGETS    A=60 B=60 C=12 D=15372 'd_u'
02270 [L1603] TGETS    A=60 B=60 C=67 D=15427 'createByStyle'
02271 [L1603] TDUP     A=61 B=1 C=38 D=294 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 26}}
02272 [L1603] TSETS    A=57 B=61 C=70 D=15686 'string'
02273 [L1603] MULNV    A=62 B=35 C=25 D=8985 
02274 [L1603] ADDVV    A=62 B=37 C=62 D=9534 
02275 [L1603] TSETS    A=62 B=61 C=30 D=15646 'x'
02276 [L1603] MULNV    A=62 B=36 C=44 D=9260 
02277 [L1603] ADDVV    A=62 B=38 C=62 D=9790 
02278 [L1603] TSETS    A=62 B=61 C=32 D=15648 'y'
02279 [L1603] TDUP     A=62 B=1 C=39 D=295 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
02280 [L1603] TSETS    A=62 B=61 C=93 D=15709 'anchor'
02281 [L1603] TSETS    A=4 B=61 C=76 D=15692 'color'
02282 [L1603] CALL     A=60 B=0 C=2 D=2 
02283 [L1603] CALLM    A=58 B=1 C=1 D=257 
02284 [L1607] KNUM     A=28 B=0 C=45 D=45 0.87
02285 [L1608] TGETS    A=29 B=0 C=45 D=45 'csvInfo'
02286 [L1608] KSTR     A=30 B=1 C=40 D=296 'description'
02287 [L1608] TGETV    A=29 B=29 C=30 D=7454 
02288 [L1608] IST      A=0 B=0 C=29 D=29 
02289 [L1608] JMP      A=30 B=128 C=1 D=32769 target=2291
02290 [L1608] KSTR     A=29 B=1 C=37 D=293 ''
02291 [L1610] TGETS    A=30 B=0 C=45 D=45 'csvInfo'
02292 [L1610] ISF      A=0 B=0 C=30 D=30 
02293 [L1610] JMP      A=31 B=128 C=25 D=32793 target=2319
02294 [L1610] TGETS    A=30 B=0 C=45 D=45 'csvInfo'
02295 [L1610] TGETS    A=30 B=30 C=59 D=7739 'mainType'
02296 [L1610] UGET     A=31 B=0 C=11 D=11 m_t
02297 [L1610] TGETS    A=31 B=31 C=102 D=8038 'ext_skill'
02298 [L1610] ISNEV    A=30 B=0 C=31 D=31 
02299 [L1610] JMP      A=30 B=128 C=19 D=32787 target=2319
02300 [L1611] TGETS    A=30 B=0 C=77 D=77 'level'
02301 [L1611] IST      A=0 B=0 C=30 D=30 
02302 [L1611] JMP      A=31 B=128 C=1 D=32769 target=2304
02303 [L1611] KSHORT   A=30 B=0 C=1 D=1 1
02304 [L1612] TGETS    A=31 B=0 C=45 D=45 'csvInfo'
02305 [L1612] KSTR     A=32 B=1 C=41 D=297 'ext_skill_desc'
02306 [L1612] TGETV    A=31 B=31 C=32 D=7968 
02307 [L1612] ISF      A=0 B=0 C=31 D=31 
02308 [L1612] JMP      A=32 B=128 C=10 D=32778 target=2319
02309 [L1612] TGETS    A=31 B=0 C=45 D=45 'csvInfo'
02310 [L1612] KSTR     A=32 B=1 C=41 D=297 'ext_skill_desc'
02311 [L1612] TGETV    A=31 B=31 C=32 D=7968 
02312 [L1612] TGETV    A=31 B=31 C=30 D=7966 
02313 [L1612] ISF      A=0 B=0 C=31 D=31 
02314 [L1612] JMP      A=32 B=128 C=4 D=32772 target=2319
02315 [L1613] TGETS    A=31 B=0 C=45 D=45 'csvInfo'
02316 [L1613] KSTR     A=32 B=1 C=41 D=297 'ext_skill_desc'
02317 [L1613] TGETV    A=31 B=31 C=32 D=7968 
02318 [L1613] TGETV    A=29 B=31 C=30 D=7966 
02319 [L1618] TGETS    A=30 B=0 C=45 D=45 'csvInfo'
02320 [L1618] ISF      A=0 B=0 C=30 D=30 
02321 [L1618] JMP      A=31 B=128 C=14 D=32782 target=2336
02322 [L1618] TGETS    A=30 B=0 C=45 D=45 'csvInfo'
02323 [L1618] TGETS    A=30 B=30 C=59 D=7739 'mainType'
02324 [L1618] UGET     A=31 B=0 C=11 D=11 m_t
02325 [L1618] TGETS    A=31 B=31 C=60 D=7996 'awaken_star'
02326 [L1618] ISNEV    A=30 B=0 C=31 D=31 
02327 [L1618] JMP      A=30 B=128 C=8 D=32776 target=2336
02328 [L1619] GGET     A=30 B=0 C=11 D=11 'd_ms'
02329 [L1619] TGETS    A=30 B=30 C=115 D=7795 'd_wakeUI'
02330 [L1619] KSTR     A=31 B=1 C=42 D=298 'getStarDesc'
02331 [L1619] TGETV    A=30 B=30 C=31 D=7711 
02332 [L1619] TGETS    A=31 B=0 C=120 D=120 'type_id'
02333 [L1619] TGETS    A=32 B=0 C=77 D=77 'level'
02334 [L1619] CALL     A=30 B=2 C=3 D=515 
02335 [L1619] MOV      A=29 B=0 C=30 D=30 
02336 [L1622] UGET     A=30 B=0 C=20 D=20 CCLabelTTF
02337 [L1622] MOV      A=31 B=0 C=30 D=30 
02338 [L1622] TGETS    A=30 B=30 C=3 D=7683 'create'
02339 [L1622] MOV      A=32 B=0 C=29 D=29 
02340 [L1622] KSTR     A=33 B=1 C=43 D=299 'arial'
02341 [L1622] KSHORT   A=34 B=0 C=26 D=26 26
02342 [L1622] UGET     A=35 B=0 C=21 D=21 CCSizeMake
02343 [L1622] TGETS    A=36 B=5 C=28 D=1308 'width'
02344 [L1622] MULVN    A=36 B=36 C=39 D=9255 
02345 [L1622] KSHORT   A=37 B=0 C=0 D=0 0
02346 [L1622] CALL     A=35 B=2 C=3 D=515 
02347 [L1622] UGET     A=36 B=0 C=22 D=22 kCCTextAlignmentLeft
02348 [L1622] CALL     A=30 B=2 C=7 D=519 
02349 [L1623] MOV      A=32 B=0 C=30 D=30 
02350 [L1623] TGETS    A=31 B=30 C=63 D=7743 'setAnchorPoint'
02351 [L1623] UGET     A=33 B=0 C=8 D=8 CCPointMake
02352 [L1623] KNUM     A=34 B=0 C=8 D=8 0.5
02353 [L1623] KSHORT   A=35 B=0 C=1 D=1 1
02354 [L1623] CALL     A=33 B=0 C=3 D=3 
02355 [L1623] CALLM    A=31 B=1 C=1 D=257 
02356 [L1624] GGET     A=31 B=0 C=11 D=11 'd_ms'
02357 [L1624] TGETS    A=31 B=31 C=12 D=7948 'd_u'
02358 [L1624] TGETS    A=31 B=31 C=13 D=7949 'setStyles'
02359 [L1624] MOV      A=32 B=0 C=30 D=30 
02360 [L1624] TDUP     A=33 B=1 C=44 D=300 {'kind': 'table', 'value': {'x': 0.5}}
02361 [L1624] SUBVV    A=34 B=28 C=27 D=7195 
02362 [L1624] TSETS    A=34 B=33 C=32 D=8480 'y'
02363 [L1624] CALL     A=31 B=1 C=3 D=259 
02364 [L1625] MOV      A=32 B=0 C=18 D=18 
02365 [L1625] TGETS    A=31 B=18 C=7 D=4615 'addChild'
02366 [L1625] MOV      A=33 B=0 C=30 D=30 
02367 [L1625] CALL     A=31 B=1 C=3 D=259 
02368 [L1626] GGET     A=31 B=0 C=11 D=11 'd_ms'
02369 [L1626] TGETS    A=31 B=31 C=12 D=7948 'd_u'
02370 [L1626] TGETS    A=31 B=31 C=171 D=8107 'getRealScale'
02371 [L1626] MOV      A=32 B=0 C=30 D=30 
02372 [L1626] CALL     A=31 B=3 C=2 D=770 
02373 [L1627] ADDVV    A=33 B=27 C=32 D=6944 
02374 [L1627] ADDVN    A=27 B=33 C=46 D=8494 
02375 [L1630] TGETS    A=33 B=0 C=45 D=45 'csvInfo'
02376 [L1630] KSTR     A=34 B=1 C=45 D=301 'product_desc'
02377 [L1630] TGETV    A=33 B=33 C=34 D=8482 
02378 [L1630] IST      A=0 B=0 C=33 D=33 
02379 [L1630] JMP      A=34 B=128 C=1 D=32769 target=2381
02380 [L1630] KSTR     A=33 B=1 C=37 D=293 ''
02381 [L1631] LEN      A=34 B=0 C=33 D=33 
02382 [L1631] KSHORT   A=35 B=0 C=0 D=0 0
02383 [L1631] ISGE     A=35 B=0 C=34 D=34 
02384 [L1631] JMP      A=34 B=128 C=42 D=32810 target=2427
02385 [L1632] UGET     A=34 B=0 C=20 D=20 CCLabelTTF
02386 [L1632] MOV      A=35 B=0 C=34 D=34 
02387 [L1632] TGETS    A=34 B=34 C=3 D=8707 'create'
02388 [L1632] GGET     A=36 B=0 C=11 D=11 'd_ms'
02389 [L1632] TGETS    A=36 B=36 C=79 D=9295 'd_hz'
02390 [L1632] TGETS    A=36 B=36 C=80 D=9296 'gethz'
02391 [L1632] KSTR     A=37 B=1 C=46 D=302 'product_from'
02392 [L1632] CALL     A=36 B=2 C=2 D=514 
02393 [L1632] MOV      A=37 B=0 C=33 D=33 
02394 [L1632] CAT      A=36 B=36 C=37 D=9253 
02395 [L1632] KSTR     A=37 B=1 C=43 D=299 'arial'
02396 [L1632] KSHORT   A=38 B=0 C=22 D=22 22
02397 [L1632] UGET     A=39 B=0 C=21 D=21 CCSizeMake
02398 [L1632] TGETS    A=40 B=5 C=28 D=1308 'width'
02399 [L1632] MULVN    A=40 B=40 C=39 D=10279 
02400 [L1632] KSHORT   A=41 B=0 C=0 D=0 0
02401 [L1632] CALL     A=39 B=2 C=3 D=515 
02402 [L1632] UGET     A=40 B=0 C=22 D=22 kCCTextAlignmentLeft
02403 [L1632] CALL     A=34 B=2 C=7 D=519 
02404 [L1633] GGET     A=35 B=0 C=11 D=11 'd_ms'
02405 [L1633] TGETS    A=35 B=35 C=12 D=8972 'd_u'
02406 [L1633] TGETS    A=35 B=35 C=13 D=8973 'setStyles'
02407 [L1633] MOV      A=36 B=0 C=34 D=34 
02408 [L1633] TDUP     A=37 B=1 C=48 D=304 {'kind': 'table', 'value': {'x': 0.5}}
02409 [L1633] TDUP     A=38 B=1 C=47 D=303 {'kind': 'table', 'value': {1: 0.5, 2: 1}}
02410 [L1633] TSETS    A=38 B=37 C=93 D=9565 'anchor'
02411 [L1633] SUBVV    A=38 B=28 C=27 D=7195 
02412 [L1633] TSETS    A=38 B=37 C=32 D=9504 'y'
02413 [L1633] TDUP     A=38 B=1 C=49 D=305 {'kind': 'table', 'value': {1: 80, 2: 180, 3: 80}}
02414 [L1633] TSETS    A=38 B=37 C=76 D=9548 'color'
02415 [L1633] CALL     A=35 B=1 C=3 D=259 
02416 [L1634] MOV      A=36 B=0 C=18 D=18 
02417 [L1634] TGETS    A=35 B=18 C=7 D=4615 'addChild'
02418 [L1634] MOV      A=37 B=0 C=34 D=34 
02419 [L1634] CALL     A=35 B=1 C=3 D=259 
02420 [L1635] GGET     A=35 B=0 C=11 D=11 'd_ms'
02421 [L1635] TGETS    A=35 B=35 C=12 D=8972 'd_u'
02422 [L1635] TGETS    A=35 B=35 C=171 D=9131 'getRealScale'
02423 [L1635] MOV      A=36 B=0 C=34 D=34 
02424 [L1635] CALL     A=35 B=3 C=2 D=770 
02425 [L1636] ADDVV    A=37 B=27 C=36 D=6948 
02426 [L1636] ADDVN    A=27 B=37 C=46 D=9518 
02427 [L1663] FNEW     A=34 B=1 C=50 D=306 {'kind': 'proto', 'id': 43}
02428 [L1667] TGETS    A=35 B=0 C=45 D=45 'csvInfo'
02429 [L1667] TGETS    A=35 B=35 C=51 D=9011 'packageTag'
02430 [L1667] GGET     A=36 B=0 C=54 D=54 'packageTagDef'
02431 [L1667] TGETS    A=36 B=36 C=55 D=9271 'props'
02432 [L1667] ISEQV    A=35 B=0 C=36 D=36 
02433 [L1667] JMP      A=35 B=129 C=209 D=33233 target=2899
02434 [L1667] TGETS    A=35 B=0 C=45 D=45 'csvInfo'
02435 [L1667] TGETS    A=35 B=35 C=51 D=9011 'packageTag'
02436 [L1667] GGET     A=36 B=0 C=54 D=54 'packageTagDef'
02437 [L1667] TGETS    A=36 B=36 C=57 D=9273 'stone'
02438 [L1667] ISEQV    A=35 B=0 C=36 D=36 
02439 [L1667] JMP      A=35 B=129 C=203 D=33227 target=2899
02440 [L1669] TGETS    A=35 B=5 C=31 D=1311 'height'
02441 [L1669] MULVV    A=35 B=27 C=35 D=6947 
02442 [L1670] ADDVV    A=16 B=16 C=35 D=4131 
02443 [L1671] MOV      A=36 B=0 C=34 D=34 
02444 [L1671] MOV      A=37 B=0 C=35 D=35 
02445 [L1671] TDUP     A=38 B=1 C=51 D=307 {'kind': 'table', 'value': {}}
02446 [L1671] TGETS    A=39 B=5 C=28 D=1308 'width'
02447 [L1671] MULNV    A=39 B=39 C=8 D=9992 
02448 [L1671] TSETS    A=39 B=38 C=30 D=9758 'x'
02449 [L1671] TGETS    A=39 B=5 C=31 D=1311 'height'
02450 [L1671] MULNV    A=39 B=39 C=22 D=10006 
02451 [L1671] TSETS    A=39 B=38 C=32 D=9760 'y'
02452 [L1671] CALL     A=36 B=1 C=3 D=259 
02453 [L1674] TDUP     A=36 B=1 C=52 D=308 {'kind': 'table', 'value': {}}
02454 [L1674] TGETS    A=37 B=5 C=28 D=1308 'width'
02455 [L1674] MULNV    A=37 B=37 C=8 D=9480 
02456 [L1674] TSETS    A=37 B=36 C=30 D=9246 'x'
02457 [L1674] SUBVV    A=37 B=28 C=27 D=7195 
02458 [L1674] SUBVN    A=37 B=37 C=19 D=9491 
02459 [L1674] TGETS    A=38 B=5 C=31 D=1311 'height'
02460 [L1674] MULVV    A=37 B=37 C=38 D=9510 
02461 [L1674] TSETS    A=37 B=36 C=32 D=9248 'y'
02462 [L1675] UGET     A=37 B=0 C=5 D=5 CCSprite
02463 [L1675] MOV      A=38 B=0 C=37 D=37 
02464 [L1675] TGETS    A=37 B=37 C=3 D=9475 'create'
02465 [L1675] KSTR     A=39 B=0 C=39 D=39 'v2/newIntroUI/head_bkg.png'
02466 [L1675] CALL     A=37 B=2 C=3 D=515 
02467 [L1676] MOV      A=39 B=0 C=37 D=37 
02468 [L1676] TGETS    A=38 B=37 C=27 D=9499 'setPosition'
02469 [L1676] TGETS    A=40 B=36 C=30 D=9246 'x'
02470 [L1676] TGETS    A=41 B=36 C=32 D=9248 'y'
02471 [L1676] CALL     A=38 B=1 C=4 D=260 
02472 [L1677] MOV      A=39 B=0 C=18 D=18 
02473 [L1677] TGETS    A=38 B=18 C=7 D=4615 'addChild'
02474 [L1677] MOV      A=40 B=0 C=37 D=37 
02475 [L1677] CALL     A=38 B=1 C=3 D=259 
02476 [L1678] MOV      A=39 B=0 C=37 D=37 
02477 [L1678] TGETS    A=38 B=37 C=63 D=9535 'setAnchorPoint'
02478 [L1678] UGET     A=40 B=0 C=8 D=8 CCPointMake
02479 [L1678] KNUM     A=41 B=0 C=8 D=8 0.5
02480 [L1678] KSHORT   A=42 B=0 C=1 D=1 1
02481 [L1678] CALL     A=40 B=0 C=3 D=3 
02482 [L1678] CALLM    A=38 B=1 C=1 D=257 
02483 [L1679] MOV      A=39 B=0 C=37 D=37 
02484 [L1679] TGETS    A=38 B=37 C=43 D=9515 'getContentSize'
02485 [L1679] CALL     A=38 B=2 C=2 D=514 
02486 [L1682] TGETS    A=39 B=38 C=31 D=9759 'height'
02487 [L1682] ADDVV    A=16 B=16 C=39 D=4135 
02488 [L1684] UGET     A=39 B=0 C=5 D=5 CCSprite
02489 [L1684] MOV      A=40 B=0 C=39 D=39 
02490 [L1684] TGETS    A=39 B=39 C=3 D=9987 'create'
02491 [L1684] KSTR     A=41 B=1 C=53 D=309 'v2/introUI/yuanfen_label.png'
02492 [L1684] CALL     A=39 B=2 C=3 D=515 
02493 [L1685] MOV      A=41 B=0 C=39 D=39 
02494 [L1685] TGETS    A=40 B=39 C=27 D=10011 'setPosition'
02495 [L1685] TGETS    A=42 B=36 C=30 D=9246 'x'
02496 [L1685] TGETS    A=43 B=36 C=32 D=9248 'y'
02497 [L1685] TGETS    A=44 B=38 C=31 D=9759 'height'
02498 [L1685] MULVN    A=44 B=44 C=39 D=11303 
02499 [L1685] SUBVV    A=43 B=43 C=44 D=11052 
02500 [L1685] CALL     A=40 B=1 C=4 D=260 
02501 [L1686] MOV      A=41 B=0 C=18 D=18 
02502 [L1686] TGETS    A=40 B=18 C=7 D=4615 'addChild'
02503 [L1686] MOV      A=42 B=0 C=39 D=39 
02504 [L1686] CALL     A=40 B=1 C=3 D=259 
02505 [L1689] TGETS    A=40 B=0 C=120 D=120 'type_id'
02506 [L1690] GGET     A=41 B=0 C=11 D=11 'd_ms'
02507 [L1690] KSTR     A=42 B=1 C=54 D=310 'd_lineupUI'
02508 [L1690] TGETV    A=41 B=41 C=42 D=10538 
02509 [L1690] KSTR     A=42 B=1 C=55 D=311 'g_fateAttrTable'
02510 [L1690] TGETV    A=41 B=41 C=42 D=10538 
02511 [L1690] TGETS    A=41 B=41 C=49 D=10545 'item'
02512 [L1690] TGETV    A=41 B=41 C=40 D=10536 
02513 [L1691] TDUP     A=42 B=1 C=56 D=312 {'kind': 'table', 'value': {}}
02514 [L1691] TGETS    A=43 B=5 C=28 D=1308 'width'
02515 [L1691] MULVN    A=43 B=43 C=47 D=11055 
02516 [L1691] TSETS    A=43 B=42 C=30 D=10782 'x'
02517 [L1691] TGETS    A=43 B=36 C=32 D=9248 'y'
02518 [L1691] TGETS    A=44 B=38 C=31 D=9759 'height'
02519 [L1691] SUBVV    A=43 B=43 C=44 D=11052 
02520 [L1691] TSETS    A=43 B=42 C=32 D=10784 'y'
02521 [L1692] TGETS    A=43 B=5 C=31 D=1311 'height'
02522 [L1692] MULNV    A=43 B=43 C=19 D=11027 
02523 [L1693] ISEQP    A=41 B=0 C=0 D=0 
02524 [L1693] JMP      A=44 B=129 C=3 D=33027 target=2784
02525 [L1694] GGET     A=44 B=0 C=11 D=11 'd_ms'
02526 [L1694] TGETS    A=44 B=44 C=79 D=11343 'd_hz'
02527 [L1694] TGETS    A=44 B=44 C=80 D=11344 'gethz'
02528 [L1694] KSTR     A=45 B=1 C=57 D=313 'connection'
02529 [L1694] CALL     A=44 B=2 C=2 D=514 
02530 [L1695] UGET     A=45 B=0 C=20 D=20 CCLabelTTF
02531 [L1695] MOV      A=46 B=0 C=45 D=45 
02532 [L1695] TGETS    A=45 B=45 C=3 D=11523 'create'
02533 [L1695] MOV      A=47 B=0 C=44 D=44 
02534 [L1695] KSTR     A=48 B=1 C=58 D=314 ':'
02535 [L1695] CAT      A=47 B=47 C=48 D=12080 
02536 [L1695] KSTR     A=48 B=1 C=43 D=299 'arial'
02537 [L1695] KSHORT   A=49 B=0 C=30 D=30 30
02538 [L1695] CALL     A=45 B=2 C=5 D=517 
02539 [L1697] TGETS    A=46 B=42 C=32 D=10784 'y'
02540 [L1697] SUBVV    A=46 B=46 C=43 D=11819 
02541 [L1698] MOV      A=48 B=0 C=45 D=45 
02542 [L1698] TGETS    A=47 B=45 C=27 D=11547 'setPosition'
02543 [L1698] TGETS    A=49 B=42 C=30 D=10782 'x'
02544 [L1698] MOV      A=50 B=0 C=46 D=46 
02545 [L1698] CALL     A=47 B=1 C=4 D=260 
02546 [L1699] MOV      A=48 B=0 C=45 D=45 
02547 [L1699] TGETS    A=47 B=45 C=63 D=11583 'setAnchorPoint'
02548 [L1699] UGET     A=49 B=0 C=8 D=8 CCPointMake
02549 [L1699] KSHORT   A=50 B=0 C=0 D=0 0
02550 [L1699] KSHORT   A=51 B=0 C=1 D=1 1
02551 [L1699] CALL     A=49 B=0 C=3 D=3 
02552 [L1699] CALLM    A=47 B=1 C=1 D=257 
02553 [L1700] MOV      A=48 B=0 C=18 D=18 
02554 [L1700] TGETS    A=47 B=18 C=7 D=4615 'addChild'
02555 [L1700] MOV      A=49 B=0 C=45 D=45 
02556 [L1700] CALL     A=47 B=1 C=3 D=259 
02557 [L1701] MOV      A=48 B=0 C=45 D=45 
02558 [L1701] TGETS    A=47 B=45 C=71 D=11591 'setColor'
02559 [L1701] UGET     A=49 B=0 C=14 D=14 ccc3
02560 [L1701] KSHORT   A=50 B=0 C=253 D=253 253
02561 [L1701] KSHORT   A=51 B=0 C=190 D=190 190
02562 [L1701] KSHORT   A=52 B=0 C=37 D=37 37
02563 [L1701] CALL     A=49 B=0 C=4 D=4 
02564 [L1701] CALLM    A=47 B=1 C=1 D=257 
02565 [L1703] MOV      A=48 B=0 C=45 D=45 
02566 [L1703] TGETS    A=47 B=45 C=43 D=11563 'getContentSize'
02567 [L1703] CALL     A=47 B=2 C=2 D=514 
02568 [L1705] KPRI     A=48 B=0 C=0 D=0 
02569 [L1706] KSHORT   A=49 B=0 C=1 D=1 1
02570 [L1706] LEN      A=50 B=0 C=41 D=41 
02571 [L1706] KSHORT   A=51 B=0 C=1 D=1 1
02572 [L1706] FORI     A=49 B=128 C=28 D=32796 target=2601
02573 [L1707] GGET     A=53 B=0 C=11 D=11 'd_ms'
02574 [L1707] KSTR     A=54 B=1 C=54 D=310 'd_lineupUI'
02575 [L1707] TGETV    A=53 B=53 C=54 D=13622 
02576 [L1707] KSTR     A=54 B=1 C=59 D=315 'g_characterAttrTable'
02577 [L1707] TGETV    A=53 B=53 C=54 D=13622 
02578 [L1707] TGETV    A=54 B=41 C=52 D=10548 
02579 [L1707] KSTR     A=55 B=1 C=60 D=316 'character'
02580 [L1707] TGETV    A=54 B=54 C=55 D=13879 
02581 [L1707] TGETV    A=53 B=53 C=54 D=13622 
02582 [L1707] TGETS    A=53 B=53 C=75 D=13643 'name'
02583 [L1708] KSHORT   A=54 B=0 C=1 D=1 1
02584 [L1708] ISGE     A=54 B=0 C=52 D=52 
02585 [L1708] JMP      A=54 B=128 C=7 D=32775 target=2593
02586 [L1709] MOV      A=54 B=0 C=48 D=48 
02587 [L1709] GGET     A=55 B=0 C=11 D=11 'd_ms'
02588 [L1709] TGETS    A=55 B=55 C=79 D=14159 'd_hz'
02589 [L1709] TGETS    A=55 B=55 C=80 D=14160 'gethz'
02590 [L1709] KSTR     A=56 B=1 C=61 D=317 'comma'
02591 [L1709] CALL     A=55 B=2 C=2 D=514 
02592 [L1709] CAT      A=48 B=54 C=55 D=13879 
02593 [L1712] ISNEP    A=48 B=0 C=0 D=0 
02594 [L1712] JMP      A=54 B=128 C=2 D=32770 target=2597
02595 [L1713] MOV      A=48 B=0 C=53 D=53 
02596 [L1713] JMP      A=54 B=128 C=3 D=32771 target=2600
02597 [L1715] MOV      A=54 B=0 C=48 D=48 
02598 [L1715] MOV      A=55 B=0 C=53 D=53 
02599 [L1715] CAT      A=48 B=54 C=55 D=13879 
02600 [L1706] FORL     A=49 B=127 C=228 D=32740 target=2573
02601 [L1720] UGET     A=49 B=0 C=20 D=20 CCLabelTTF
02602 [L1720] MOV      A=50 B=0 C=49 D=49 
02603 [L1720] TGETS    A=49 B=49 C=3 D=12547 'create'
02604 [L1720] MOV      A=51 B=0 C=48 D=48 
02605 [L1720] KSTR     A=52 B=1 C=43 D=299 'arial'
02606 [L1720] KSHORT   A=53 B=0 C=26 D=26 26
02607 [L1720] UGET     A=54 B=0 C=21 D=21 CCSizeMake
02608 [L1720] TGETS    A=55 B=5 C=28 D=1308 'width'
02609 [L1720] MULVN    A=55 B=55 C=39 D=14119 
02610 [L1720] KSHORT   A=56 B=0 C=0 D=0 0
02611 [L1720] CALL     A=54 B=2 C=3 D=515 
02612 [L1720] UGET     A=55 B=0 C=22 D=22 kCCTextAlignmentLeft
02613 [L1720] CALL     A=49 B=2 C=7 D=519 
02614 [L1722] TGETS    A=50 B=5 C=31 D=1311 'height'
02615 [L1722] MULNV    A=50 B=50 C=19 D=12819 
02616 [L1722] SUBVV    A=50 B=46 C=50 D=11826 
02617 [L1722] TGETS    A=51 B=47 C=31 D=12063 'height'
02618 [L1722] SUBVV    A=46 B=50 C=51 D=12851 
02619 [L1723] MOV      A=51 B=0 C=49 D=49 
02620 [L1723] TGETS    A=50 B=49 C=27 D=12571 'setPosition'
02621 [L1723] TGETS    A=52 B=42 C=30 D=10782 'x'
02622 [L1723] MOV      A=53 B=0 C=46 D=46 
02623 [L1723] CALL     A=50 B=1 C=4 D=260 
02624 [L1724] MOV      A=51 B=0 C=49 D=49 
02625 [L1724] TGETS    A=50 B=49 C=63 D=12607 'setAnchorPoint'
02626 [L1724] UGET     A=52 B=0 C=8 D=8 CCPointMake
02627 [L1724] KSHORT   A=53 B=0 C=0 D=0 0
02628 [L1724] KSHORT   A=54 B=0 C=1 D=1 1
02629 [L1724] CALL     A=52 B=0 C=3 D=3 
02630 [L1724] CALLM    A=50 B=1 C=1 D=257 
02631 [L1725] MOV      A=51 B=0 C=18 D=18 
02632 [L1725] TGETS    A=50 B=18 C=7 D=4615 'addChild'
02633 [L1725] MOV      A=52 B=0 C=49 D=49 
02634 [L1725] CALL     A=50 B=1 C=3 D=259 
02635 [L1727] MOV      A=51 B=0 C=49 D=49 
02636 [L1727] TGETS    A=50 B=49 C=43 D=12587 'getContentSize'
02637 [L1727] CALL     A=50 B=2 C=2 D=514 
02638 [L1727] MOV      A=47 B=0 C=50 D=50 
02639 [L1729] UGET     A=50 B=0 C=20 D=20 CCLabelTTF
02640 [L1729] MOV      A=51 B=0 C=50 D=50 
02641 [L1729] TGETS    A=50 B=50 C=3 D=12803 'create'
02642 [L1729] GGET     A=52 B=0 C=11 D=11 'd_ms'
02643 [L1729] TGETS    A=52 B=52 C=79 D=13391 'd_hz'
02644 [L1729] TGETS    A=52 B=52 C=80 D=13392 'gethz'
02645 [L1729] KSTR     A=53 B=1 C=62 D=318 'connectEffect'
02646 [L1729] CALL     A=52 B=2 C=2 D=514 
02647 [L1729] KSTR     A=53 B=1 C=58 D=314 ':'
02648 [L1729] CAT      A=52 B=52 C=53 D=13365 
02649 [L1729] KSTR     A=53 B=1 C=43 D=299 'arial'
02650 [L1729] KSHORT   A=54 B=0 C=30 D=30 30
02651 [L1729] CALL     A=50 B=2 C=5 D=517 
02652 [L1731] MOV      A=52 B=0 C=50 D=50 
02653 [L1731] TGETS    A=51 B=50 C=63 D=12863 'setAnchorPoint'
02654 [L1731] UGET     A=53 B=0 C=8 D=8 CCPointMake
02655 [L1731] KSHORT   A=54 B=0 C=0 D=0 0
02656 [L1731] KSHORT   A=55 B=0 C=1 D=1 1
02657 [L1731] CALL     A=53 B=0 C=3 D=3 
02658 [L1731] CALLM    A=51 B=1 C=1 D=257 
02659 [L1733] TGETS    A=51 B=5 C=31 D=1311 'height'
02660 [L1733] MULNV    A=51 B=51 C=19 D=13075 
02661 [L1733] SUBVV    A=51 B=46 C=51 D=11827 
02662 [L1733] TGETS    A=52 B=47 C=31 D=12063 'height'
02663 [L1733] SUBVV    A=46 B=51 C=52 D=13108 
02664 [L1734] MOV      A=52 B=0 C=50 D=50 
02665 [L1734] TGETS    A=51 B=50 C=27 D=12827 'setPosition'
02666 [L1734] TGETS    A=53 B=42 C=30 D=10782 'x'
02667 [L1734] MOV      A=54 B=0 C=46 D=46 
02668 [L1734] CALL     A=51 B=1 C=4 D=260 
02669 [L1735] MOV      A=52 B=0 C=50 D=50 
02670 [L1735] TGETS    A=51 B=50 C=71 D=12871 'setColor'
02671 [L1735] UGET     A=53 B=0 C=14 D=14 ccc3
02672 [L1735] KSHORT   A=54 B=0 C=253 D=253 253
02673 [L1735] KSHORT   A=55 B=0 C=190 D=190 190
02674 [L1735] KSHORT   A=56 B=0 C=37 D=37 37
02675 [L1735] CALL     A=53 B=0 C=4 D=4 
02676 [L1735] CALLM    A=51 B=1 C=1 D=257 
02677 [L1736] MOV      A=52 B=0 C=18 D=18 
02678 [L1736] TGETS    A=51 B=18 C=7 D=4615 'addChild'
02679 [L1736] MOV      A=53 B=0 C=50 D=50 
02680 [L1736] CALL     A=51 B=1 C=3 D=259 
02681 [L1738] MOV      A=52 B=0 C=50 D=50 
02682 [L1738] TGETS    A=51 B=50 C=43 D=12843 'getContentSize'
02683 [L1738] CALL     A=51 B=2 C=2 D=514 
02684 [L1738] MOV      A=47 B=0 C=51 D=51 
02685 [L1741] GGET     A=51 B=0 C=11 D=11 'd_ms'
02686 [L1741] TGETS    A=51 B=51 C=79 D=13135 'd_hz'
02687 [L1741] TGETS    A=51 B=51 C=80 D=13136 'gethz'
02688 [L1741] KSTR     A=52 B=1 C=63 D=319 'increase'
02689 [L1741] CALL     A=51 B=2 C=2 D=514 
02690 [L1742] TGETB    A=52 B=41 C=1 D=10497 
02691 [L1742] KSTR     A=53 B=1 C=64 D=320 'effectField'
02692 [L1742] TGETV    A=52 B=52 C=53 D=13365 
02693 [L1743] TGETB    A=53 B=41 C=1 D=10497 
02694 [L1743] KSTR     A=54 B=1 C=65 D=321 'effectValue'
02695 [L1743] TGETV    A=53 B=53 C=54 D=13622 
02696 [L1744] ISNEN    A=52 B=0 C=14 D=14 1
02697 [L1744] JMP      A=54 B=128 C=12 D=32780 target=2710
02698 [L1745] GGET     A=54 B=0 C=11 D=11 'd_ms'
02699 [L1745] TGETS    A=54 B=54 C=79 D=13903 'd_hz'
02700 [L1745] TGETS    A=54 B=54 C=80 D=13904 'gethz'
02701 [L1745] KSTR     A=55 B=1 C=66 D=322 'healthPoint'
02702 [L1745] CALL     A=54 B=2 C=2 D=514 
02703 [L1745] MOV      A=55 B=0 C=51 D=51 
02704 [L1745] UGET     A=56 B=0 C=13 D=13 tostring
02705 [L1745] MOV      A=57 B=0 C=53 D=53 
02706 [L1745] CALL     A=56 B=2 C=2 D=514 
02707 [L1745] KSTR     A=57 B=0 C=69 D=69 '%'
02708 [L1745] CAT      A=51 B=54 C=57 D=13881 
02709 [L1745] JMP      A=54 B=128 C=41 D=32809 target=2751
02710 [L1746] ISNEN    A=52 B=0 C=11 D=11 2
02711 [L1746] JMP      A=54 B=128 C=12 D=32780 target=2724
02712 [L1747] GGET     A=54 B=0 C=11 D=11 'd_ms'
02713 [L1747] TGETS    A=54 B=54 C=79 D=13903 'd_hz'
02714 [L1747] TGETS    A=54 B=54 C=80 D=13904 'gethz'
02715 [L1747] KSTR     A=55 B=1 C=67 D=323 'neili'
02716 [L1747] CALL     A=54 B=2 C=2 D=514 
02717 [L1747] MOV      A=55 B=0 C=51 D=51 
02718 [L1747] UGET     A=56 B=0 C=13 D=13 tostring
02719 [L1747] MOV      A=57 B=0 C=53 D=53 
02720 [L1747] CALL     A=56 B=2 C=2 D=514 
02721 [L1747] KSTR     A=57 B=0 C=69 D=69 '%'
02722 [L1747] CAT      A=51 B=54 C=57 D=13881 
02723 [L1747] JMP      A=54 B=128 C=27 D=32795 target=2751
02724 [L1748] ISNEN    A=52 B=0 C=42 D=42 3
02725 [L1748] JMP      A=54 B=128 C=12 D=32780 target=2738
02726 [L1749] GGET     A=54 B=0 C=11 D=11 'd_ms'
02727 [L1749] TGETS    A=54 B=54 C=79 D=13903 'd_hz'
02728 [L1749] TGETS    A=54 B=54 C=80 D=13904 'gethz'
02729 [L1749] KSTR     A=55 B=1 C=68 D=324 'damage'
02730 [L1749] CALL     A=54 B=2 C=2 D=514 
02731 [L1749] MOV      A=55 B=0 C=51 D=51 
02732 [L1749] UGET     A=56 B=0 C=13 D=13 tostring
02733 [L1749] MOV      A=57 B=0 C=53 D=53 
02734 [L1749] CALL     A=56 B=2 C=2 D=514 
02735 [L1749] KSTR     A=57 B=0 C=69 D=69 '%'
02736 [L1749] CAT      A=51 B=54 C=57 D=13881 
02737 [L1749] JMP      A=54 B=128 C=13 D=32781 target=2751
02738 [L1750] ISNEN    A=52 B=0 C=48 D=48 4
02739 [L1750] JMP      A=54 B=128 C=11 D=32779 target=2751
02740 [L1751] GGET     A=54 B=0 C=11 D=11 'd_ms'
02741 [L1751] TGETS    A=54 B=54 C=79 D=13903 'd_hz'
02742 [L1751] TGETS    A=54 B=54 C=80 D=13904 'gethz'
02743 [L1751] KSTR     A=55 B=1 C=69 D=325 'defense'
02744 [L1751] CALL     A=54 B=2 C=2 D=514 
02745 [L1751] MOV      A=55 B=0 C=51 D=51 
02746 [L1751] UGET     A=56 B=0 C=13 D=13 tostring
02747 [L1751] MOV      A=57 B=0 C=53 D=53 
02748 [L1751] CALL     A=56 B=2 C=2 D=514 
02749 [L1751] KSTR     A=57 B=0 C=69 D=69 '%'
02750 [L1751] CAT      A=51 B=54 C=57 D=13881 
02751 [L1753] UGET     A=54 B=0 C=20 D=20 CCLabelTTF
02752 [L1753] MOV      A=55 B=0 C=54 D=54 
02753 [L1753] TGETS    A=54 B=54 C=3 D=13827 'create'
02754 [L1753] MOV      A=56 B=0 C=51 D=51 
02755 [L1753] KSTR     A=57 B=1 C=43 D=299 'arial'
02756 [L1753] KSHORT   A=58 B=0 C=26 D=26 26
02757 [L1753] CALL     A=54 B=2 C=5 D=517 
02758 [L1755] TGETS    A=55 B=5 C=31 D=1311 'height'
02759 [L1755] MULNV    A=55 B=55 C=19 D=14099 
02760 [L1755] SUBVV    A=55 B=46 C=55 D=11831 
02761 [L1755] TGETS    A=56 B=47 C=31 D=12063 'height'
02762 [L1755] SUBVV    A=46 B=55 C=56 D=14136 
02763 [L1756] MOV      A=56 B=0 C=54 D=54 
02764 [L1756] TGETS    A=55 B=54 C=27 D=13851 'setPosition'
02765 [L1756] TGETS    A=57 B=42 C=30 D=10782 'x'
02766 [L1756] MOV      A=58 B=0 C=46 D=46 
02767 [L1756] CALL     A=55 B=1 C=4 D=260 
02768 [L1757] MOV      A=56 B=0 C=54 D=54 
02769 [L1757] TGETS    A=55 B=54 C=63 D=13887 'setAnchorPoint'
02770 [L1757] UGET     A=57 B=0 C=8 D=8 CCPointMake
02771 [L1757] KSHORT   A=58 B=0 C=0 D=0 0
02772 [L1757] KSHORT   A=59 B=0 C=1 D=1 1
02773 [L1757] CALL     A=57 B=0 C=3 D=3 
02774 [L1757] CALLM    A=55 B=1 C=1 D=257 
02775 [L1758] MOV      A=56 B=0 C=18 D=18 
02776 [L1758] TGETS    A=55 B=18 C=7 D=4615 'addChild'
02777 [L1758] MOV      A=57 B=0 C=54 D=54 
02778 [L1758] CALL     A=55 B=1 C=3 D=259 
02779 [L1761] MOV      A=56 B=0 C=50 D=50 
02780 [L1761] TGETS    A=55 B=50 C=43 D=12843 'getContentSize'
02781 [L1761] CALL     A=55 B=2 C=2 D=514 
02782 [L1761] MOV      A=47 B=0 C=55 D=55 
02783 [L1761] JMP      A=44 B=128 C=39 D=32807 target=2823
02784 [L1763] GGET     A=44 B=0 C=11 D=11 'd_ms'
02785 [L1763] TGETS    A=44 B=44 C=79 D=11343 'd_hz'
02786 [L1763] TGETS    A=44 B=44 C=80 D=11344 'gethz'
02787 [L1763] KSTR     A=45 B=1 C=70 D=326 'noConnect'
02788 [L1763] CALL     A=44 B=2 C=2 D=514 
02789 [L1764] UGET     A=45 B=0 C=20 D=20 CCLabelTTF
02790 [L1764] MOV      A=46 B=0 C=45 D=45 
02791 [L1764] TGETS    A=45 B=45 C=3 D=11523 'create'
02792 [L1764] MOV      A=47 B=0 C=44 D=44 
02793 [L1764] KSTR     A=48 B=1 C=43 D=299 'arial'
02794 [L1764] KSHORT   A=49 B=0 C=30 D=30 30
02795 [L1764] CALL     A=45 B=2 C=5 D=517 
02796 [L1765] MOV      A=47 B=0 C=45 D=45 
02797 [L1765] TGETS    A=46 B=45 C=27 D=11547 'setPosition'
02798 [L1765] TGETS    A=48 B=42 C=30 D=10782 'x'
02799 [L1765] TGETS    A=49 B=42 C=32 D=10784 'y'
02800 [L1765] TGETS    A=50 B=5 C=31 D=1311 'height'
02801 [L1765] MULNV    A=50 B=50 C=19 D=12819 
02802 [L1765] SUBVV    A=49 B=49 C=50 D=12594 
02803 [L1765] CALL     A=46 B=1 C=4 D=260 
02804 [L1766] MOV      A=47 B=0 C=45 D=45 
02805 [L1766] TGETS    A=46 B=45 C=63 D=11583 'setAnchorPoint'
02806 [L1766] UGET     A=48 B=0 C=8 D=8 CCPointMake
02807 [L1766] KSHORT   A=49 B=0 C=0 D=0 0
02808 [L1766] KSHORT   A=50 B=0 C=1 D=1 1
02809 [L1766] CALL     A=48 B=0 C=3 D=3 
02810 [L1766] CALLM    A=46 B=1 C=1 D=257 
02811 [L1767] MOV      A=47 B=0 C=18 D=18 
02812 [L1767] TGETS    A=46 B=18 C=7 D=4615 'addChild'
02813 [L1767] MOV      A=48 B=0 C=45 D=45 
02814 [L1767] CALL     A=46 B=1 C=3 D=259 
02815 [L1768] MOV      A=47 B=0 C=45 D=45 
02816 [L1768] TGETS    A=46 B=45 C=71 D=11591 'setColor'
02817 [L1768] UGET     A=48 B=0 C=14 D=14 ccc3
02818 [L1768] KSHORT   A=49 B=0 C=253 D=253 253
02819 [L1768] KSHORT   A=50 B=0 C=190 D=190 190
02820 [L1768] KSHORT   A=51 B=0 C=37 D=37 37
02821 [L1768] CALL     A=48 B=0 C=4 D=4 
02822 [L1768] CALLM    A=46 B=1 C=1 D=257 
02823 [L1771] TGETS    A=44 B=5 C=31 D=1311 'height'
02824 [L1771] MULNV    A=44 B=44 C=49 D=11313 
02825 [L1772] MOV      A=45 B=0 C=34 D=34 
02826 [L1772] MOV      A=46 B=0 C=44 D=44 
02827 [L1772] TDUP     A=47 B=1 C=71 D=327 {'kind': 'table', 'value': {}}
02828 [L1772] TGETS    A=48 B=36 C=30 D=9246 'x'
02829 [L1772] TSETS    A=48 B=47 C=30 D=12062 'x'
02830 [L1772] TGETS    A=48 B=36 C=32 D=9248 'y'
02831 [L1772] TGETS    A=49 B=38 C=31 D=9759 'height'
02832 [L1772] MULNV    A=49 B=49 C=13 D=12557 
02833 [L1772] SUBVV    A=48 B=48 C=49 D=12337 
02834 [L1772] TSETS    A=48 B=47 C=32 D=12064 'y'
02835 [L1772] CALL     A=45 B=1 C=3 D=259 
02836 [L1775] ADDVV    A=16 B=16 C=44 D=4140 
02837 [L1777] ISF      A=0 B=0 C=2 D=2 
02838 [L1777] JMP      A=45 B=128 C=55 D=32823 target=2894
02839 [L1777] GGET     A=45 B=0 C=11 D=11 'd_ms'
02840 [L1777] KSTR     A=46 B=1 C=72 D=328 'd_loginUI'
02841 [L1777] TGETV    A=45 B=45 C=46 D=11566 
02842 [L1777] KSTR     A=46 B=1 C=73 D=329 'g_currentSence'
02843 [L1777] TGETV    A=45 B=45 C=46 D=11566 
02844 [L1777] GGET     A=46 B=0 C=11 D=11 'd_ms'
02845 [L1777] KSTR     A=47 B=1 C=72 D=328 'd_loginUI'
02846 [L1777] TGETV    A=46 B=46 C=47 D=11823 
02847 [L1777] KSTR     A=47 B=1 C=74 D=330 'senceID'
02848 [L1777] TGETV    A=46 B=46 C=47 D=11823 
02849 [L1777] KSTR     A=47 B=1 C=75 D=331 'mainUI'
02850 [L1777] TGETV    A=46 B=46 C=47 D=11823 
02851 [L1777] ISNEV    A=45 B=0 C=46 D=46 
02852 [L1777] JMP      A=45 B=128 C=41 D=32809 target=2894
02853 [L1778] SUBVV    A=45 B=28 C=27 D=7195 
02854 [L1778] SUBVN    A=45 B=45 C=19 D=11539 
02855 [L1778] SUBVN    A=45 B=45 C=49 D=11569 
02856 [L1778] TGETS    A=46 B=38 C=31 D=9759 'height'
02857 [L1778] TGETS    A=47 B=5 C=31 D=1311 'height'
02858 [L1778] DIVVV    A=46 B=46 C=47 D=11823 
02859 [L1778] SUBVV    A=45 B=45 C=46 D=11566 
02860 [L1779] UGET     A=46 B=0 C=6 D=6 CCMenuItemImage
02861 [L1779] MOV      A=47 B=0 C=46 D=46 
02862 [L1779] TGETS    A=46 B=46 C=3 D=11779 'create'
02863 [L1779] KSTR     A=48 B=1 C=76 D=332 'v2/handbook/tj_btn1.png'
02864 [L1779] KSTR     A=49 B=1 C=77 D=333 'v2/handbook/tj_btn2.png'
02865 [L1779] CALL     A=46 B=2 C=4 D=516 
02866 [L1780] GGET     A=47 B=0 C=11 D=11 'd_ms'
02867 [L1780] TGETS    A=47 B=47 C=12 D=12044 'd_u'
02868 [L1780] TGETS    A=47 B=47 C=13 D=12045 'setStyles'
02869 [L1780] MOV      A=48 B=0 C=46 D=46 
02870 [L1780] TDUP     A=49 B=1 C=78 D=334 {'kind': 'table', 'value': {'x': 0.5}}
02871 [L1780] TSETS    A=45 B=49 C=32 D=12576 'y'
02872 [L1780] TDUP     A=50 B=1 C=79 D=335 {'kind': 'table', 'value': {1: 0.5, 2: 1}}
02873 [L1780] TSETS    A=50 B=49 C=93 D=12637 'anchor'
02874 [L1780] CALL     A=47 B=1 C=3 D=259 
02875 [L1781] MOV      A=48 B=0 C=46 D=46 
02876 [L1781] TGETS    A=47 B=46 C=21 D=11797 'setTag'
02877 [L1781] GGET     A=49 B=0 C=22 D=22 'g_introButtonType'
02878 [L1781] KSTR     A=50 B=1 C=80 D=336 'handbook'
02879 [L1781] TGETV    A=49 B=49 C=50 D=12594 
02880 [L1781] CALL     A=47 B=1 C=3 D=259 
02881 [L1782] MOV      A=48 B=0 C=46 D=46 
02882 [L1782] TGETS    A=47 B=46 C=25 D=11801 'registerScriptTapHandler'
02883 [L1782] MOV      A=49 B=0 C=1 D=1 
02884 [L1782] CALL     A=47 B=1 C=3 D=259 
02885 [L1783] MOV      A=48 B=0 C=7 D=7 
02886 [L1783] TGETS    A=47 B=7 C=154 D=1946 'addObject'
02887 [L1783] MOV      A=49 B=0 C=46 D=46 
02888 [L1783] CALL     A=47 B=1 C=3 D=259 
02889 [L1785] MOV      A=48 B=0 C=46 D=46 
02890 [L1785] TGETS    A=47 B=46 C=43 D=11819 'getContentSize'
02891 [L1785] CALL     A=47 B=2 C=2 D=514 
02892 [L1785] TGETS    A=47 B=47 C=31 D=12063 'height'
02893 [L1785] ADDVV    A=16 B=16 C=47 D=4143 
02894 [L1789] MOV      A=46 B=0 C=17 D=17 
02895 [L1789] KSTR     A=47 B=1 C=81 D=337 'createInertiaMove'
02896 [L1789] TGETV    A=45 B=17 C=47 D=4399 
02897 [L1789] CALL     A=45 B=1 C=2 D=258 
02898 [L1789] JMP      A=35 B=128 C=14 D=32782 target=2913
02899 [L1792] ADDVN    A=35 B=27 C=36 D=6948 
02900 [L1792] TGETS    A=36 B=5 C=31 D=1311 'height'
02901 [L1792] MULVV    A=35 B=35 C=36 D=8996 
02902 [L1793] MOV      A=36 B=0 C=34 D=34 
02903 [L1793] MOV      A=37 B=0 C=35 D=35 
02904 [L1793] TDUP     A=38 B=1 C=82 D=338 {'kind': 'table', 'value': {}}
02905 [L1793] TGETS    A=39 B=5 C=28 D=1308 'width'
02906 [L1793] MULNV    A=39 B=39 C=8 D=9992 
02907 [L1793] TSETS    A=39 B=38 C=30 D=9758 'x'
02908 [L1793] TGETS    A=39 B=5 C=31 D=1311 'height'
02909 [L1793] MULNV    A=39 B=39 C=22 D=10006 
02910 [L1793] TSETS    A=39 B=38 C=32 D=9760 'y'
02911 [L1793] CALL     A=36 B=1 C=3 D=259 
02912 [L1796] ADDVV    A=16 B=16 C=35 D=4131 
02913 [L1799] UGET     A=35 B=0 C=7 D=7 CCMenu
02914 [L1799] MOV      A=36 B=0 C=35 D=35 
02915 [L1799] KSTR     A=37 B=1 C=83 D=339 'createWithArray'
02916 [L1799] TGETV    A=35 B=35 C=37 D=8997 
02917 [L1799] MOV      A=37 B=0 C=7 D=7 
02918 [L1799] CALL     A=35 B=2 C=3 D=515 
02919 [L1800] MOV      A=37 B=0 C=35 D=35 
02920 [L1800] TGETS    A=36 B=35 C=27 D=8987 'setPosition'
02921 [L1800] UGET     A=38 B=0 C=8 D=8 CCPointMake
02922 [L1800] KSHORT   A=39 B=0 C=0 D=0 0
02923 [L1800] KSHORT   A=40 B=0 C=0 D=0 0
02924 [L1800] CALL     A=38 B=0 C=3 D=3 
02925 [L1800] CALLM    A=36 B=1 C=1 D=257 
02926 [L1801] MOV      A=37 B=0 C=18 D=18 
02927 [L1801] TGETS    A=36 B=18 C=7 D=4615 'addChild'
02928 [L1801] MOV      A=38 B=0 C=35 D=35 
02929 [L1801] KSHORT   A=39 B=0 C=5 D=5 5
02930 [L1801] CALL     A=36 B=1 C=4 D=260 
02931 [L1803] MOV      A=37 B=0 C=17 D=17 
02932 [L1803] KSTR     A=38 B=1 C=84 D=340 'addCell'
02933 [L1803] TGETV    A=36 B=17 C=38 D=4390 
02934 [L1803] MOV      A=38 B=0 C=18 D=18 
02935 [L1803] TDUP     A=39 B=1 C=85 D=341 {'kind': 'table', 'value': {}}
02936 [L1803] TGETS    A=40 B=15 C=28 D=3868 'width'
02937 [L1803] TSETS    A=40 B=39 C=28 D=10012 'width'
02938 [L1803] TSETS    A=16 B=39 C=31 D=10015 'height'
02939 [L1803] CALL     A=36 B=1 C=4 D=260 
02940 [L1805] UCLO     A=0 B=128 C=0 D=32768 target=2941
02941 [L1805] RET1     A=6 B=0 C=2 D=2 

FUNCTION proto45 offset=0xc423 source_lines=1809-1812 params=1
UPVALUES []
00001 [L1810] GGET     A=1 B=0 C=0 D=0 'g_currentPackageItems'
00002 [L1810] TGETV    A=1 B=1 C=0 D=256 
00003 [L1811] GGET     A=2 B=0 C=1 D=1 'requestUseItem'
00004 [L1811] MOV      A=3 B=0 C=1 D=1 
00005 [L1811] CALL     A=2 B=1 C=2 D=258 
00006 [L1812] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto46 offset=0xc484 source_lines=1820-1852 params=1
UPVALUES ['item', 'cclog']
00001 [L1821] UGET     A=1 B=0 C=0 D=0 item
00002 [L1821] TGETS    A=1 B=1 C=0 D=256 'id'
00003 [L1821] IST      A=0 B=0 C=1 D=1 
00004 [L1821] JMP      A=1 B=128 C=6 D=32774 target=11
00005 [L1822] UGET     A=1 B=0 C=0 D=0 item
00006 [L1822] GGET     A=2 B=0 C=1 D=1 'getPropIDByTypeId'
00007 [L1822] UGET     A=3 B=0 C=0 D=0 item
00008 [L1822] TGETS    A=3 B=3 C=2 D=770 'type_id'
00009 [L1822] CALL     A=2 B=2 C=2 D=514 
00010 [L1822] TSETS    A=2 B=1 C=0 D=256 'id'
00011 [L1824] UGET     A=1 B=0 C=1 D=1 cclog
00012 [L1824] KSTR     A=2 B=0 C=3 D=3 'item_main_type.gift_bag , id = %f'
00013 [L1824] UGET     A=3 B=0 C=0 D=0 item
00014 [L1824] TGETS    A=3 B=3 C=0 D=768 'id'
00015 [L1824] CALL     A=1 B=1 C=3 D=259 
00016 [L1827] UGET     A=1 B=0 C=0 D=0 item
00017 [L1827] TGETS    A=1 B=1 C=2 D=258 'type_id'
00018 [L1827] ISNEN    A=1 B=0 C=0 D=0 1031
00019 [L1827] JMP      A=1 B=128 C=17 D=32785 target=37
00020 [L1829] GGET     A=1 B=0 C=4 D=4 'd_ms'
00021 [L1829] TGETS    A=1 B=1 C=5 D=261 'd_mainUI'
00022 [L1829] TGETS    A=1 B=1 C=6 D=262 'g_playerInfo'
00023 [L1829] TGETS    A=1 B=1 C=7 D=263 'vip_level'
00024 [L1829] KSHORT   A=2 B=0 C=1 D=1 1
00025 [L1829] ISGE     A=1 B=0 C=2 D=2 
00026 [L1829] JMP      A=1 B=128 C=10 D=32778 target=37
00027 [L1830] GGET     A=1 B=0 C=4 D=4 'd_ms'
00028 [L1830] TGETS    A=1 B=1 C=8 D=264 'd_info'
00029 [L1830] TGETS    A=1 B=1 C=9 D=265 'show'
00030 [L1830] GGET     A=2 B=0 C=4 D=4 'd_ms'
00031 [L1830] TGETS    A=2 B=2 C=10 D=522 'd_hz'
00032 [L1830] TGETS    A=2 B=2 C=11 D=523 'gethz'
00033 [L1830] KSTR     A=3 B=0 C=12 D=12 'not_vip'
00034 [L1830] CALL     A=2 B=0 C=2 D=2 
00035 [L1830] CALLM    A=1 B=1 C=0 D=256 
00036 [L1831] RET0     A=0 B=0 C=1 D=1 
00037 [L1841] GGET     A=1 B=0 C=13 D=13 'g_lastRequestUsedItem'
00038 [L1841] UGET     A=2 B=0 C=0 D=0 item
00039 [L1841] TSETS    A=2 B=1 C=14 D=270 'item'
00040 [L1842] GGET     A=1 B=0 C=13 D=13 'g_lastRequestUsedItem'
00041 [L1842] ISTC     A=2 B=0 C=0 D=0 
00042 [L1842] JMP      A=2 B=128 C=1 D=32769 target=44
00043 [L1842] KSHORT   A=2 B=0 C=1 D=1 1
00044 [L1842] TSETS    A=2 B=1 C=15 D=271 'count'
00045 [L1844] TDUP     A=1 B=0 C=16 D=16 {'kind': 'table', 'value': {'des_id': 0}}
00046 [L1845] UGET     A=2 B=0 C=0 D=0 item
00047 [L1845] TGETS    A=2 B=2 C=2 D=514 'type_id'
00048 [L1845] TSETS    A=2 B=1 C=17 D=273 'item_type'
00049 [L1846] UGET     A=2 B=0 C=0 D=0 item
00050 [L1846] TGETS    A=2 B=2 C=0 D=512 'id'
00051 [L1846] TSETS    A=2 B=1 C=18 D=274 'item_id'
00052 [L1847] GGET     A=2 B=0 C=4 D=4 'd_ms'
00053 [L1847] TGETS    A=2 B=2 C=19 D=531 'd_common_def'
00054 [L1847] TGETS    A=2 B=2 C=20 D=532 'object_type'
00055 [L1847] TGETS    A=2 B=2 C=21 D=533 'role'
00056 [L1847] TSETS    A=2 B=1 C=22 D=278 'des_type'
00057 [L1849] ISTC     A=2 B=0 C=0 D=0 
00058 [L1849] JMP      A=2 B=128 C=1 D=32769 target=60
00059 [L1849] KSHORT   A=2 B=0 C=1 D=1 1
00060 [L1849] TSETS    A=2 B=1 C=23 D=279 'item_count'
00061 [L1851] GGET     A=2 B=0 C=4 D=4 'd_ms'
00062 [L1851] TGETS    A=2 B=2 C=24 D=536 'd_u'
00063 [L1851] TGETS    A=2 B=2 C=25 D=537 'main_server_send_msg'
00064 [L1851] GGET     A=3 B=0 C=4 D=4 'd_ms'
00065 [L1851] TGETS    A=3 B=3 C=26 D=794 'd_msg_def'
00066 [L1851] TGETS    A=3 B=3 C=27 D=795 'gscl_msg_id'
00067 [L1851] TGETS    A=3 B=3 C=28 D=796 'msg_use_item'
00068 [L1851] MOV      A=4 B=0 C=1 D=1 
00069 [L1851] CALL     A=2 B=1 C=3 D=259 
00070 [L1852] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto47 offset=0xc74a source_lines=1945-1952 params=0
UPVALUES ['pairs']
00001 [L1946] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L1946] TGETS    A=0 B=0 C=1 D=1 'd_jpChangeUI'
00003 [L1946] TGETS    A=0 B=0 C=2 D=2 'initCsvConfig'
00004 [L1946] CALL     A=0 B=1 C=1 D=257 
00005 [L1947] UGET     A=0 B=0 C=0 D=0 pairs
00006 [L1947] GGET     A=1 B=0 C=0 D=0 'd_ms'
00007 [L1947] TGETS    A=1 B=1 C=1 D=257 'd_jpChangeUI'
00008 [L1947] TGETS    A=1 B=1 C=3 D=259 'g_self'
00009 [L1947] TGETS    A=1 B=1 C=4 D=260 'csv'
00010 [L1947] CALL     A=0 B=4 C=2 D=1026 
00011 [L1947] ISNEXT   A=3 B=128 C=4 D=32772 target=16
00012 [L1948] ISF      A=0 B=0 C=4 D=4 
00013 [L1948] JMP      A=5 B=128 C=2 D=32770 target=16
00014 [L1949] TGETS    A=5 B=4 C=5 D=1029 'min_role_level'
00015 [L1949] RET1     A=5 B=0 C=2 D=2 
00016 [L1947] ITERN    A=3 B=3 C=3 D=771 
00017 [L1947] ITERL    A=3 B=127 C=250 D=32762 target=12
00018 [L1952] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto48 offset=0xc805 source_lines=1814-1977 params=1
UPVALUES ['cclog', 'm_t', 'math', 'string', 'pairs', 'showAdvance']
00001 [L1815] TGETS    A=1 B=0 C=0 D=0 'count'
00002 [L1815] KSHORT   A=2 B=0 C=0 D=0 0
00003 [L1815] ISGT     A=1 B=0 C=2 D=2 
00004 [L1815] JMP      A=1 B=128 C=10 D=32778 target=15
00005 [L1816] GGET     A=1 B=0 C=1 D=1 'd_ms'
00006 [L1816] TGETS    A=1 B=1 C=2 D=258 'd_info'
00007 [L1816] TGETS    A=1 B=1 C=3 D=259 'show'
00008 [L1816] GGET     A=2 B=0 C=1 D=1 'd_ms'
00009 [L1816] TGETS    A=2 B=2 C=4 D=516 'd_hz'
00010 [L1816] TGETS    A=2 B=2 C=5 D=517 'gethz'
00011 [L1816] KSTR     A=3 B=0 C=6 D=6 'noCount'
00012 [L1816] CALL     A=2 B=0 C=2 D=2 
00013 [L1816] CALLM    A=1 B=1 C=0 D=256 
00014 [L1817] UCLO     A=0 B=129 C=246 D=33270 target=517
00015 [L1852] FNEW     A=1 B=0 C=7 D=7 {'kind': 'proto', 'id': 46}
00016 [L1854] TGETS    A=2 B=0 C=8 D=8 'type_id'
00017 [L1854] ISEQN    A=2 B=0 C=0 D=0 1150
00018 [L1854] JMP      A=2 B=128 C=3 D=32771 target=22
00019 [L1854] TGETS    A=2 B=0 C=8 D=8 'type_id'
00020 [L1854] ISNEN    A=2 B=0 C=1 D=1 1151
00021 [L1854] JMP      A=2 B=128 C=3 D=32771 target=25
00022 [L1855] MOV      A=2 B=0 C=1 D=1 
00023 [L1855] CALL     A=2 B=1 C=1 D=257 
00024 [L1855] JMP      A=2 B=129 C=234 D=33258 target=515
00025 [L1856] TGETS    A=2 B=0 C=8 D=8 'type_id'
00026 [L1856] ISNEN    A=2 B=0 C=2 D=2 1005
00027 [L1856] JMP      A=2 B=128 C=8 D=32776 target=36
00028 [L1858] GGET     A=2 B=0 C=1 D=1 'd_ms'
00029 [L1858] TGETS    A=2 B=2 C=9 D=521 'd_commonLayerUI'
00030 [L1858] TGETS    A=2 B=2 C=10 D=522 'showModityNameCard'
00031 [L1858] GGET     A=3 B=0 C=11 D=11 'g_packageUI'
00032 [L1858] TGETS    A=3 B=3 C=12 D=780 'parent'
00033 [L1858] KSHORT   A=4 B=0 C=40 D=40 40
00034 [L1858] CALL     A=2 B=1 C=3 D=259 
00035 [L1858] JMP      A=2 B=129 C=223 D=33247 target=515
00036 [L1859] TGETS    A=2 B=0 C=8 D=8 'type_id'
00037 [L1859] ISNEN    A=2 B=0 C=3 D=3 1246
00038 [L1859] JMP      A=2 B=128 C=8 D=32776 target=47
00039 [L1860] GGET     A=2 B=0 C=1 D=1 'd_ms'
00040 [L1860] TGETS    A=2 B=2 C=13 D=525 'd_kickUI'
00041 [L1860] TGETS    A=2 B=2 C=14 D=526 'showFruitUseLayer'
00042 [L1860] GGET     A=3 B=0 C=11 D=11 'g_packageUI'
00043 [L1860] TGETS    A=3 B=3 C=12 D=780 'parent'
00044 [L1860] KSHORT   A=4 B=0 C=30 D=30 30
00045 [L1860] CALL     A=2 B=1 C=3 D=259 
00046 [L1860] JMP      A=2 B=129 C=212 D=33236 target=515
00047 [L1861] TGETS    A=2 B=0 C=8 D=8 'type_id'
00048 [L1861] ISNEN    A=2 B=0 C=4 D=4 1249
00049 [L1861] JMP      A=2 B=128 C=8 D=32776 target=58
00050 [L1862] GGET     A=2 B=0 C=1 D=1 'd_ms'
00051 [L1862] TGETS    A=2 B=2 C=15 D=527 'd_xianlingShopUI'
00052 [L1862] TGETS    A=2 B=2 C=16 D=528 'showBoxUseLayer'
00053 [L1862] GGET     A=3 B=0 C=11 D=11 'g_packageUI'
00054 [L1862] TGETS    A=3 B=3 C=12 D=780 'parent'
00055 [L1862] KSHORT   A=4 B=0 C=30 D=30 30
00056 [L1862] CALL     A=2 B=1 C=3 D=259 
00057 [L1862] JMP      A=2 B=129 C=201 D=33225 target=515
00058 [L1863] TGETS    A=2 B=0 C=8 D=8 'type_id'
00059 [L1863] ISEQN    A=2 B=0 C=5 D=5 1367
00060 [L1863] JMP      A=2 B=128 C=3 D=32771 target=64
00061 [L1863] TGETS    A=2 B=0 C=8 D=8 'type_id'
00062 [L1863] ISNEN    A=2 B=0 C=6 D=6 1368
00063 [L1863] JMP      A=2 B=128 C=9 D=32777 target=73
00064 [L1864] GGET     A=2 B=0 C=1 D=1 'd_ms'
00065 [L1864] TGETS    A=2 B=2 C=17 D=529 'd_turntableUI'
00066 [L1864] TGETS    A=2 B=2 C=16 D=528 'showBoxUseLayer'
00067 [L1864] GGET     A=3 B=0 C=11 D=11 'g_packageUI'
00068 [L1864] TGETS    A=3 B=3 C=12 D=780 'parent'
00069 [L1864] KSHORT   A=4 B=0 C=30 D=30 30
00070 [L1864] TGETS    A=5 B=0 C=8 D=8 'type_id'
00071 [L1864] CALL     A=2 B=1 C=4 D=260 
00072 [L1864] JMP      A=2 B=129 C=186 D=33210 target=515
00073 [L1865] TGETS    A=2 B=0 C=18 D=18 'csvInfo'
00074 [L1865] TGETS    A=2 B=2 C=19 D=531 'mainType'
00075 [L1865] UGET     A=3 B=0 C=1 D=1 m_t
00076 [L1865] TGETS    A=3 B=3 C=20 D=788 'gift_bag'
00077 [L1865] ISEQV    A=2 B=0 C=3 D=3 
00078 [L1865] JMP      A=2 B=128 C=15 D=32783 target=94
00079 [L1866] TGETS    A=2 B=0 C=18 D=18 'csvInfo'
00080 [L1866] TGETS    A=2 B=2 C=19 D=531 'mainType'
00081 [L1866] UGET     A=3 B=0 C=1 D=1 m_t
00082 [L1866] TGETS    A=3 B=3 C=21 D=789 'lottery_bag'
00083 [L1866] ISEQV    A=2 B=0 C=3 D=3 
00084 [L1866] JMP      A=2 B=128 C=9 D=32777 target=94
00085 [L1867] TGETS    A=2 B=0 C=18 D=18 'csvInfo'
00086 [L1867] TGETS    A=2 B=2 C=19 D=531 'mainType'
00087 [L1867] UGET     A=3 B=0 C=1 D=1 m_t
00088 [L1867] TGETS    A=3 B=3 C=22 D=790 'vip_bag'
00089 [L1867] ISEQV    A=2 B=0 C=3 D=3 
00090 [L1867] JMP      A=2 B=128 C=3 D=32771 target=94
00091 [L1868] TGETS    A=2 B=0 C=8 D=8 'type_id'
00092 [L1868] ISNEN    A=2 B=0 C=7 D=7 1036
00093 [L1868] JMP      A=2 B=128 C=25 D=32793 target=119
00094 [L1869] TGETS    A=2 B=0 C=0 D=0 'count'
00095 [L1869] KSHORT   A=3 B=0 C=10 D=10 10
00096 [L1869] ISGT     A=3 B=0 C=2 D=2 
00097 [L1869] JMP      A=2 B=128 C=18 D=32786 target=116
00098 [L1870] TDUP     A=2 B=0 C=24 D=24 {'kind': 'table', 'value': {'min': 1}}
00099 [L1870] UGET     A=3 B=0 C=2 D=2 math
00100 [L1870] TGETS    A=3 B=3 C=23 D=791 'min'
00101 [L1870] KSHORT   A=4 B=0 C=15 D=15 15
00102 [L1870] TGETS    A=5 B=0 C=0 D=0 'count'
00103 [L1870] CALL     A=3 B=2 C=3 D=515 
00104 [L1870] TSETS    A=3 B=2 C=25 D=537 'max'
00105 [L1871] GGET     A=3 B=0 C=1 D=1 'd_ms'
00106 [L1871] TGETS    A=3 B=3 C=26 D=794 'd_data'
00107 [L1871] TGETS    A=3 B=3 C=27 D=795 'createBatchUse'
00108 [L1871] GGET     A=4 B=0 C=1 D=1 'd_ms'
00109 [L1871] TGETS    A=4 B=4 C=28 D=1052 'd_mainUI'
00110 [L1871] TGETS    A=4 B=4 C=29 D=1053 'g_mainUI'
00111 [L1871] TGETS    A=4 B=4 C=30 D=1054 'main_layer'
00112 [L1871] MOV      A=5 B=0 C=2 D=2 
00113 [L1871] MOV      A=6 B=0 C=1 D=1 
00114 [L1871] CALL     A=3 B=1 C=4 D=260 
00115 [L1871] JMP      A=2 B=129 C=143 D=33167 target=515
00116 [L1873] MOV      A=2 B=0 C=1 D=1 
00117 [L1873] CALL     A=2 B=1 C=1 D=257 
00118 [L1874] JMP      A=2 B=129 C=140 D=33164 target=515
00119 [L1875] TGETS    A=2 B=0 C=8 D=8 'type_id'
00120 [L1875] ISNEN    A=2 B=0 C=8 D=8 1029
00121 [L1875] JMP      A=2 B=128 C=42 D=32810 target=164
00122 [L1876] GGET     A=2 B=0 C=1 D=1 'd_ms'
00123 [L1876] TGETS    A=2 B=2 C=28 D=540 'd_mainUI'
00124 [L1876] TGETS    A=2 B=2 C=31 D=543 'g_playerInfo'
00125 [L1876] TGETS    A=2 B=2 C=32 D=544 'union_id'
00126 [L1876] KSHORT   A=3 B=0 C=0 D=0 0
00127 [L1876] ISGE     A=3 B=0 C=2 D=2 
00128 [L1876] JMP      A=2 B=128 C=25 D=32793 target=154
00129 [L1877] TGETS    A=2 B=0 C=0 D=0 'count'
00130 [L1877] KSHORT   A=3 B=0 C=10 D=10 10
00131 [L1877] ISGT     A=3 B=0 C=2 D=2 
00132 [L1877] JMP      A=2 B=128 C=18 D=32786 target=151
00133 [L1878] TDUP     A=2 B=0 C=33 D=33 {'kind': 'table', 'value': {'min': 1}}
00134 [L1878] UGET     A=3 B=0 C=2 D=2 math
00135 [L1878] TGETS    A=3 B=3 C=23 D=791 'min'
00136 [L1878] KSHORT   A=4 B=0 C=15 D=15 15
00137 [L1878] TGETS    A=5 B=0 C=0 D=0 'count'
00138 [L1878] CALL     A=3 B=2 C=3 D=515 
00139 [L1878] TSETS    A=3 B=2 C=25 D=537 'max'
00140 [L1879] GGET     A=3 B=0 C=1 D=1 'd_ms'
00141 [L1879] TGETS    A=3 B=3 C=26 D=794 'd_data'
00142 [L1879] TGETS    A=3 B=3 C=27 D=795 'createBatchUse'
00143 [L1879] GGET     A=4 B=0 C=1 D=1 'd_ms'
00144 [L1879] TGETS    A=4 B=4 C=28 D=1052 'd_mainUI'
00145 [L1879] TGETS    A=4 B=4 C=29 D=1053 'g_mainUI'
00146 [L1879] TGETS    A=4 B=4 C=30 D=1054 'main_layer'
00147 [L1879] MOV      A=5 B=0 C=2 D=2 
00148 [L1879] MOV      A=6 B=0 C=1 D=1 
00149 [L1879] CALL     A=3 B=1 C=4 D=260 
00150 [L1879] JMP      A=2 B=129 C=108 D=33132 target=515
00151 [L1881] MOV      A=2 B=0 C=1 D=1 
00152 [L1881] CALL     A=2 B=1 C=1 D=257 
00153 [L1882] JMP      A=2 B=129 C=105 D=33129 target=515
00154 [L1884] GGET     A=2 B=0 C=1 D=1 'd_ms'
00155 [L1884] TGETS    A=2 B=2 C=2 D=514 'd_info'
00156 [L1884] TGETS    A=2 B=2 C=3 D=515 'show'
00157 [L1884] GGET     A=3 B=0 C=1 D=1 'd_ms'
00158 [L1884] TGETS    A=3 B=3 C=4 D=772 'd_hz'
00159 [L1884] TGETS    A=3 B=3 C=5 D=773 'gethz'
00160 [L1884] KSTR     A=4 B=0 C=34 D=34 'contribution_need_union'
00161 [L1884] CALL     A=3 B=0 C=2 D=2 
00162 [L1884] CALLM    A=2 B=1 C=0 D=256 
00163 [L1885] JMP      A=2 B=129 C=95 D=33119 target=515
00164 [L1886] TGETS    A=2 B=0 C=8 D=8 'type_id'
00165 [L1886] ISEQN    A=2 B=0 C=9 D=9 1021
00166 [L1886] JMP      A=2 B=128 C=27 D=32795 target=194
00167 [L1887] TGETS    A=2 B=0 C=8 D=8 'type_id'
00168 [L1887] ISEQN    A=2 B=0 C=10 D=10 1022
00169 [L1887] JMP      A=2 B=128 C=24 D=32792 target=194
00170 [L1888] TGETS    A=2 B=0 C=8 D=8 'type_id'
00171 [L1888] ISEQN    A=2 B=0 C=11 D=11 1020
00172 [L1888] JMP      A=2 B=128 C=21 D=32789 target=194
00173 [L1889] TGETS    A=2 B=0 C=8 D=8 'type_id'
00174 [L1889] ISEQN    A=2 B=0 C=12 D=12 1023
00175 [L1889] JMP      A=2 B=128 C=18 D=32786 target=194
00176 [L1890] TGETS    A=2 B=0 C=8 D=8 'type_id'
00177 [L1890] ISEQN    A=2 B=0 C=13 D=13 1096
00178 [L1890] JMP      A=2 B=128 C=15 D=32783 target=194
00179 [L1891] TGETS    A=2 B=0 C=8 D=8 'type_id'
00180 [L1891] ISEQN    A=2 B=0 C=7 D=7 1036
00181 [L1891] JMP      A=2 B=128 C=12 D=32780 target=194
00182 [L1892] TGETS    A=2 B=0 C=8 D=8 'type_id'
00183 [L1892] ISEQN    A=2 B=0 C=14 D=14 1133
00184 [L1892] JMP      A=2 B=128 C=9 D=32777 target=194
00185 [L1893] TGETS    A=2 B=0 C=8 D=8 'type_id'
00186 [L1893] ISEQN    A=2 B=0 C=15 D=15 1132
00187 [L1893] JMP      A=2 B=128 C=6 D=32774 target=194
00188 [L1894] TGETS    A=2 B=0 C=8 D=8 'type_id'
00189 [L1894] ISEQN    A=2 B=0 C=16 D=16 1131
00190 [L1894] JMP      A=2 B=128 C=3 D=32771 target=194
00191 [L1895] TGETS    A=2 B=0 C=8 D=8 'type_id'
00192 [L1895] ISNEN    A=2 B=0 C=17 D=17 1130
00193 [L1895] JMP      A=2 B=128 C=3 D=32771 target=197
00194 [L1898] MOV      A=2 B=0 C=1 D=1 
00195 [L1898] CALL     A=2 B=1 C=1 D=257 
00196 [L1898] JMP      A=2 B=129 C=62 D=33086 target=515
00197 [L1900] TGETS    A=2 B=0 C=8 D=8 'type_id'
00198 [L1900] ISNEN    A=2 B=0 C=18 D=18 1002
00199 [L1900] JMP      A=2 B=128 C=8 D=32776 target=208
00200 [L1902] GGET     A=2 B=0 C=1 D=1 'd_ms'
00201 [L1902] TGETS    A=2 B=2 C=35 D=547 'd_inheritUI'
00202 [L1902] TGETS    A=2 B=2 C=36 D=548 'showInheritLayer'
00203 [L1902] GGET     A=3 B=0 C=11 D=11 'g_packageUI'
00204 [L1902] TGETS    A=3 B=3 C=12 D=780 'parent'
00205 [L1902] KSHORT   A=4 B=0 C=30 D=30 30
00206 [L1902] CALL     A=2 B=1 C=3 D=259 
00207 [L1902] JMP      A=2 B=129 C=51 D=33075 target=515
00208 [L1903] TGETS    A=2 B=0 C=8 D=8 'type_id'
00209 [L1903] ISNEN    A=2 B=0 C=19 D=19 1003
00210 [L1903] JMP      A=2 B=128 C=5 D=32773 target=216
00211 [L1904] GGET     A=2 B=0 C=1 D=1 'd_ms'
00212 [L1904] TGETS    A=2 B=2 C=37 D=549 'd_forgeUI'
00213 [L1904] TGETS    A=2 B=2 C=3 D=515 'show'
00214 [L1904] CALL     A=2 B=1 C=1 D=257 
00215 [L1904] JMP      A=2 B=129 C=43 D=33067 target=515
00216 [L1906] TGETS    A=2 B=0 C=8 D=8 'type_id'
00217 [L1906] ISNEN    A=2 B=0 C=20 D=20 1004
00218 [L1906] JMP      A=2 B=128 C=23 D=32791 target=242
00219 [L1908] GGET     A=2 B=0 C=1 D=1 'd_ms'
00220 [L1908] TGETS    A=2 B=2 C=28 D=540 'd_mainUI'
00221 [L1908] TGETS    A=2 B=2 C=31 D=543 'g_playerInfo'
00222 [L1908] TGETS    A=2 B=2 C=38 D=550 'level'
00223 [L1908] KSHORT   A=3 B=0 C=8 D=8 8
00224 [L1908] ISGE     A=2 B=0 C=3 D=3 
00225 [L1908] JMP      A=2 B=128 C=11 D=32779 target=237
00226 [L1909] GGET     A=2 B=0 C=1 D=1 'd_ms'
00227 [L1909] TGETS    A=2 B=2 C=2 D=514 'd_info'
00228 [L1909] TGETS    A=2 B=2 C=3 D=515 'show'
00229 [L1909] GGET     A=3 B=0 C=1 D=1 'd_ms'
00230 [L1909] TGETS    A=3 B=3 C=4 D=772 'd_hz'
00231 [L1909] TGETS    A=3 B=3 C=5 D=773 'gethz'
00232 [L1909] KSTR     A=4 B=0 C=39 D=39 'canUseWorldMsg'
00233 [L1909] CALL     A=3 B=0 C=2 D=2 
00234 [L1909] CALLM    A=2 B=1 C=0 D=256 
00235 [L1910] UCLO     A=0 B=128 C=0 D=32768 target=236
00236 [L1910] RET0     A=0 B=0 C=1 D=1 
00237 [L1912] GGET     A=2 B=0 C=1 D=1 'd_ms'
00238 [L1912] TGETS    A=2 B=2 C=40 D=552 'd_newChatUI'
00239 [L1912] TGETS    A=2 B=2 C=3 D=515 'show'
00240 [L1912] CALL     A=2 B=1 C=1 D=257 
00241 [L1912] JMP      A=2 B=129 C=17 D=33041 target=515
00242 [L1913] TGETS    A=2 B=0 C=8 D=8 'type_id'
00243 [L1913] ISNEN    A=2 B=0 C=21 D=21 1024
00244 [L1913] JMP      A=2 B=128 C=27 D=32795 target=272
00245 [L1915] GGET     A=2 B=0 C=1 D=1 'd_ms'
00246 [L1915] TGETS    A=2 B=2 C=28 D=540 'd_mainUI'
00247 [L1915] TGETS    A=2 B=2 C=31 D=543 'g_playerInfo'
00248 [L1915] TGETS    A=2 B=2 C=38 D=550 'level'
00249 [L1915] KSHORT   A=3 B=0 C=16 D=16 16
00250 [L1915] ISGE     A=2 B=0 C=3 D=3 
00251 [L1915] JMP      A=2 B=128 C=11 D=32779 target=263
00252 [L1916] GGET     A=2 B=0 C=1 D=1 'd_ms'
00253 [L1916] TGETS    A=2 B=2 C=2 D=514 'd_info'
00254 [L1916] TGETS    A=2 B=2 C=3 D=515 'show'
00255 [L1916] GGET     A=3 B=0 C=1 D=1 'd_ms'
00256 [L1916] TGETS    A=3 B=3 C=4 D=772 'd_hz'
00257 [L1916] TGETS    A=3 B=3 C=5 D=773 'gethz'
00258 [L1916] KSTR     A=4 B=0 C=41 D=41 'canNotUseHyd'
00259 [L1916] CALL     A=3 B=0 C=2 D=2 
00260 [L1916] CALLM    A=2 B=1 C=0 D=256 
00261 [L1917] UCLO     A=0 B=128 C=0 D=32768 target=262
00262 [L1917] RET0     A=0 B=0 C=1 D=1 
00263 [L1920] GGET     A=2 B=0 C=1 D=1 'd_ms'
00264 [L1920] TGETS    A=2 B=2 C=42 D=554 'd_activityUI'
00265 [L1920] TGETS    A=2 B=2 C=3 D=515 'show'
00266 [L1920] CALL     A=2 B=1 C=1 D=257 
00267 [L1921] GGET     A=2 B=0 C=1 D=1 'd_ms'
00268 [L1921] TGETS    A=2 B=2 C=42 D=554 'd_activityUI'
00269 [L1921] TGETS    A=2 B=2 C=43 D=555 'backToCortCallUI'
00270 [L1921] CALL     A=2 B=1 C=1 D=257 
00271 [L1921] JMP      A=2 B=128 C=243 D=33011 target=515
00272 [L1922] TGETS    A=2 B=0 C=18 D=18 'csvInfo'
00273 [L1922] TGETS    A=2 B=2 C=44 D=556 'base_experience_plus'
00274 [L1922] KSHORT   A=3 B=0 C=0 D=0 0
00275 [L1922] ISGE     A=3 B=0 C=2 D=2 
00276 [L1922] JMP      A=2 B=128 C=93 D=32861 target=370
00277 [L1923] TGETS    A=2 B=0 C=18 D=18 'csvInfo'
00278 [L1923] TGETS    A=2 B=2 C=45 D=557 'sub_type'
00279 [L1923] GGET     A=3 B=0 C=1 D=1 'd_ms'
00280 [L1923] TGETS    A=3 B=3 C=46 D=814 'd_common_def'
00281 [L1923] TGETS    A=3 B=3 C=47 D=815 'item_sub_type'
00282 [L1923] TGETS    A=3 B=3 C=48 D=816 'exp_pill'
00283 [L1923] ISNEV    A=2 B=0 C=3 D=3 
00284 [L1923] JMP      A=2 B=128 C=31 D=32799 target=316
00285 [L1924] GGET     A=2 B=0 C=1 D=1 'd_ms'
00286 [L1924] TGETS    A=2 B=2 C=28 D=540 'd_mainUI'
00287 [L1924] TGETS    A=2 B=2 C=31 D=543 'g_playerInfo'
00288 [L1924] TGETS    A=2 B=2 C=38 D=550 'level'
00289 [L1924] KSHORT   A=3 B=0 C=65 D=65 65
00290 [L1924] ISGE     A=2 B=0 C=3 D=3 
00291 [L1924] JMP      A=2 B=128 C=15 D=32783 target=307
00292 [L1925] GGET     A=2 B=0 C=1 D=1 'd_ms'
00293 [L1925] TGETS    A=2 B=2 C=2 D=514 'd_info'
00294 [L1925] TGETS    A=2 B=2 C=3 D=515 'show'
00295 [L1925] UGET     A=3 B=0 C=3 D=3 string
00296 [L1925] TGETS    A=3 B=3 C=49 D=817 'format'
00297 [L1925] GGET     A=4 B=0 C=1 D=1 'd_ms'
00298 [L1925] TGETS    A=4 B=4 C=4 D=1028 'd_hz'
00299 [L1925] TGETS    A=4 B=4 C=5 D=1029 'gethz'
00300 [L1925] KSTR     A=5 B=0 C=50 D=50 'abyss_tip6'
00301 [L1925] CALL     A=4 B=2 C=2 D=514 
00302 [L1925] KSHORT   A=5 B=0 C=65 D=65 65
00303 [L1925] CALL     A=3 B=0 C=3 D=3 
00304 [L1925] CALLM    A=2 B=1 C=0 D=256 
00305 [L1926] UCLO     A=0 B=128 C=0 D=32768 target=306
00306 [L1926] RET0     A=0 B=0 C=1 D=1 
00307 [L1928] GGET     A=2 B=0 C=1 D=1 'd_ms'
00308 [L1928] TGETS    A=2 B=2 C=51 D=563 'd_expbookUI'
00309 [L1928] TGETS    A=2 B=2 C=52 D=564 'showExpbookLayer'
00310 [L1928] GGET     A=3 B=0 C=11 D=11 'g_packageUI'
00311 [L1928] TGETS    A=3 B=3 C=12 D=780 'parent'
00312 [L1928] KSHORT   A=4 B=0 C=40 D=40 40
00313 [L1928] KSHORT   A=5 B=0 C=2 D=2 2
00314 [L1928] CALL     A=2 B=1 C=4 D=260 
00315 [L1928] JMP      A=2 B=128 C=199 D=32967 target=515
00316 [L1929] TGETS    A=2 B=0 C=18 D=18 'csvInfo'
00317 [L1929] TGETS    A=2 B=2 C=45 D=557 'sub_type'
00318 [L1929] GGET     A=3 B=0 C=1 D=1 'd_ms'
00319 [L1929] TGETS    A=3 B=3 C=46 D=814 'd_common_def'
00320 [L1929] TGETS    A=3 B=3 C=47 D=815 'item_sub_type'
00321 [L1929] TGETS    A=3 B=3 C=53 D=821 'roll'
00322 [L1929] ISNEV    A=2 B=0 C=3 D=3 
00323 [L1929] JMP      A=2 B=128 C=9 D=32777 target=333
00324 [L1930] GGET     A=2 B=0 C=1 D=1 'd_ms'
00325 [L1930] TGETS    A=2 B=2 C=51 D=563 'd_expbookUI'
00326 [L1930] TGETS    A=2 B=2 C=52 D=564 'showExpbookLayer'
00327 [L1930] GGET     A=3 B=0 C=11 D=11 'g_packageUI'
00328 [L1930] TGETS    A=3 B=3 C=12 D=780 'parent'
00329 [L1930] KSHORT   A=4 B=0 C=40 D=40 40
00330 [L1930] KSHORT   A=5 B=0 C=1 D=1 1
00331 [L1930] CALL     A=2 B=1 C=4 D=260 
00332 [L1930] JMP      A=2 B=128 C=182 D=32950 target=515
00333 [L1931] TGETS    A=2 B=0 C=18 D=18 'csvInfo'
00334 [L1931] TGETS    A=2 B=2 C=45 D=557 'sub_type'
00335 [L1931] GGET     A=3 B=0 C=1 D=1 'd_ms'
00336 [L1931] TGETS    A=3 B=3 C=46 D=814 'd_common_def'
00337 [L1931] TGETS    A=3 B=3 C=47 D=815 'item_sub_type'
00338 [L1931] TGETS    A=3 B=3 C=54 D=822 'exp_drug'
00339 [L1931] ISNEV    A=2 B=0 C=3 D=3 
00340 [L1931] JMP      A=2 B=128 C=174 D=32942 target=515
00341 [L1932] GGET     A=2 B=0 C=1 D=1 'd_ms'
00342 [L1932] TGETS    A=2 B=2 C=28 D=540 'd_mainUI'
00343 [L1932] TGETS    A=2 B=2 C=31 D=543 'g_playerInfo'
00344 [L1932] TGETS    A=2 B=2 C=38 D=550 'level'
00345 [L1932] KSHORT   A=3 B=0 C=70 D=70 70
00346 [L1932] ISGE     A=2 B=0 C=3 D=3 
00347 [L1932] JMP      A=2 B=128 C=15 D=32783 target=363
00348 [L1933] GGET     A=2 B=0 C=1 D=1 'd_ms'
00349 [L1933] TGETS    A=2 B=2 C=2 D=514 'd_info'
00350 [L1933] TGETS    A=2 B=2 C=3 D=515 'show'
00351 [L1933] UGET     A=3 B=0 C=3 D=3 string
00352 [L1933] TGETS    A=3 B=3 C=49 D=817 'format'
00353 [L1933] GGET     A=4 B=0 C=1 D=1 'd_ms'
00354 [L1933] TGETS    A=4 B=4 C=4 D=1028 'd_hz'
00355 [L1933] TGETS    A=4 B=4 C=5 D=1029 'gethz'
00356 [L1933] KSTR     A=5 B=0 C=50 D=50 'abyss_tip6'
00357 [L1933] CALL     A=4 B=2 C=2 D=514 
00358 [L1933] KSHORT   A=5 B=0 C=70 D=70 70
00359 [L1933] CALL     A=3 B=0 C=3 D=3 
00360 [L1933] CALLM    A=2 B=1 C=0 D=256 
00361 [L1934] UCLO     A=0 B=128 C=0 D=32768 target=362
00362 [L1934] RET0     A=0 B=0 C=1 D=1 
00363 [L1936] GGET     A=2 B=0 C=1 D=1 'd_ms'
00364 [L1936] TGETS    A=2 B=2 C=55 D=567 'd_yaoshendianUI'
00365 [L1936] TGETS    A=2 B=2 C=56 D=568 'showExpDrugLayer'
00366 [L1936] GGET     A=3 B=0 C=11 D=11 'g_packageUI'
00367 [L1936] TGETS    A=3 B=3 C=12 D=780 'parent'
00368 [L1936] CALL     A=2 B=1 C=2 D=258 
00369 [L1937] JMP      A=2 B=128 C=145 D=32913 target=515
00370 [L1938] TGETS    A=2 B=0 C=8 D=8 'type_id'
00371 [L1938] ISNEN    A=2 B=0 C=22 D=22 1093
00372 [L1938] JMP      A=2 B=128 C=15 D=32783 target=388
00373 [L1939] GGET     A=2 B=0 C=1 D=1 'd_ms'
00374 [L1939] TGETS    A=2 B=2 C=57 D=569 'd_stoneUI'
00375 [L1939] TGETS    A=2 B=2 C=58 D=570 'canJoin'
00376 [L1939] KPRI     A=3 B=0 C=2 D=2 
00377 [L1939] CALL     A=2 B=2 C=2 D=514 
00378 [L1939] ISF      A=0 B=0 C=2 D=2 
00379 [L1939] JMP      A=3 B=128 C=135 D=32903 target=515
00380 [L1940] GGET     A=2 B=0 C=1 D=1 'd_ms'
00381 [L1940] TGETS    A=2 B=2 C=57 D=569 'd_stoneUI'
00382 [L1940] TGETS    A=2 B=2 C=59 D=571 'showStoneLayer'
00383 [L1940] GGET     A=3 B=0 C=11 D=11 'g_packageUI'
00384 [L1940] TGETS    A=3 B=3 C=12 D=780 'parent'
00385 [L1940] KSHORT   A=4 B=0 C=40 D=40 40
00386 [L1940] CALL     A=2 B=1 C=3 D=259 
00387 [L1941] JMP      A=2 B=128 C=127 D=32895 target=515
00388 [L1942] TGETS    A=2 B=0 C=8 D=8 'type_id'
00389 [L1942] ISNEN    A=2 B=0 C=23 D=23 1095
00390 [L1942] JMP      A=2 B=128 C=5 D=32773 target=396
00391 [L1943] GGET     A=2 B=0 C=1 D=1 'd_ms'
00392 [L1943] TGETS    A=2 B=2 C=60 D=572 'd_qiankunnizhuan'
00393 [L1943] TGETS    A=2 B=2 C=3 D=515 'show'
00394 [L1943] CALL     A=2 B=1 C=1 D=257 
00395 [L1943] JMP      A=2 B=128 C=119 D=32887 target=515
00396 [L1944] TGETS    A=2 B=0 C=8 D=8 'type_id'
00397 [L1944] ISNEN    A=2 B=0 C=24 D=24 1342
00398 [L1944] JMP      A=2 B=128 C=34 D=32802 target=433
00399 [L1952] FNEW     A=2 B=0 C=61 D=61 {'kind': 'proto', 'id': 47}
00400 [L1953] MOV      A=3 B=0 C=2 D=2 
00401 [L1953] CALL     A=3 B=2 C=1 D=513 
00402 [L1953] IST      A=0 B=0 C=3 D=3 
00403 [L1953] JMP      A=4 B=128 C=1 D=32769 target=405
00404 [L1953] KSHORT   A=3 B=0 C=0 D=0 0
00405 [L1954] GGET     A=4 B=0 C=1 D=1 'd_ms'
00406 [L1954] TGETS    A=4 B=4 C=28 D=1052 'd_mainUI'
00407 [L1954] TGETS    A=4 B=4 C=31 D=1055 'g_playerInfo'
00408 [L1954] TGETS    A=4 B=4 C=38 D=1062 'level'
00409 [L1954] ISGE     A=4 B=0 C=3 D=3 
00410 [L1954] JMP      A=4 B=128 C=15 D=32783 target=426
00411 [L1955] GGET     A=4 B=0 C=1 D=1 'd_ms'
00412 [L1955] TGETS    A=4 B=4 C=2 D=1026 'd_info'
00413 [L1955] TGETS    A=4 B=4 C=3 D=1027 'show'
00414 [L1955] UGET     A=5 B=0 C=3 D=3 string
00415 [L1955] TGETS    A=5 B=5 C=49 D=1329 'format'
00416 [L1955] GGET     A=6 B=0 C=1 D=1 'd_ms'
00417 [L1955] TGETS    A=6 B=6 C=4 D=1540 'd_hz'
00418 [L1955] TGETS    A=6 B=6 C=5 D=1541 'gethz'
00419 [L1955] KSTR     A=7 B=0 C=50 D=50 'abyss_tip6'
00420 [L1955] CALL     A=6 B=2 C=2 D=514 
00421 [L1955] MOV      A=7 B=0 C=3 D=3 
00422 [L1955] CALL     A=5 B=0 C=3 D=3 
00423 [L1955] CALLM    A=4 B=1 C=0 D=256 
00424 [L1956] UCLO     A=0 B=128 C=0 D=32768 target=425
00425 [L1956] RET0     A=0 B=0 C=1 D=1 
00426 [L1958] GGET     A=4 B=0 C=1 D=1 'd_ms'
00427 [L1958] TGETS    A=4 B=4 C=62 D=1086 'd_jpChangeUI'
00428 [L1958] TGETS    A=4 B=4 C=3 D=1027 'show'
00429 [L1958] GGET     A=5 B=0 C=11 D=11 'g_packageUI'
00430 [L1958] TGETS    A=5 B=5 C=12 D=1292 'parent'
00431 [L1958] CALL     A=4 B=1 C=2 D=258 
00432 [L1958] JMP      A=2 B=128 C=82 D=32850 target=515
00433 [L1959] TGETS    A=2 B=0 C=8 D=8 'type_id'
00434 [L1959] ISNEN    A=2 B=0 C=25 D=25 1100
00435 [L1959] JMP      A=2 B=128 C=5 D=32773 target=441
00436 [L1960] GGET     A=2 B=0 C=1 D=1 'd_ms'
00437 [L1960] TGETS    A=2 B=2 C=63 D=575 'd_equipTransUI'
00438 [L1960] TGETS    A=2 B=2 C=3 D=515 'show'
00439 [L1960] CALL     A=2 B=1 C=1 D=257 
00440 [L1960] JMP      A=2 B=128 C=74 D=32842 target=515
00441 [L1961] TGETS    A=2 B=0 C=18 D=18 'csvInfo'
00442 [L1961] TGETS    A=2 B=2 C=19 D=531 'mainType'
00443 [L1961] UGET     A=3 B=0 C=1 D=1 m_t
00444 [L1961] TGETS    A=3 B=3 C=64 D=832 'compose_material'
00445 [L1961] ISNEV    A=2 B=0 C=3 D=3 
00446 [L1961] JMP      A=2 B=128 C=8 D=32776 target=455
00447 [L1962] GGET     A=2 B=0 C=1 D=1 'd_ms'
00448 [L1962] TGETS    A=2 B=2 C=65 D=577 'd_equipPieceUI'
00449 [L1962] TGETS    A=2 B=2 C=3 D=515 'show'
00450 [L1962] GGET     A=3 B=0 C=11 D=11 'g_packageUI'
00451 [L1962] TGETS    A=3 B=3 C=12 D=780 'parent'
00452 [L1962] TGETS    A=4 B=0 C=8 D=8 'type_id'
00453 [L1962] CALL     A=2 B=1 C=3 D=259 
00454 [L1962] JMP      A=2 B=128 C=60 D=32828 target=515
00455 [L1963] TGETS    A=2 B=0 C=8 D=8 'type_id'
00456 [L1963] ISEQN    A=2 B=0 C=26 D=26 1310
00457 [L1963] JMP      A=2 B=128 C=6 D=32774 target=464
00458 [L1963] TGETS    A=2 B=0 C=8 D=8 'type_id'
00459 [L1963] ISEQN    A=2 B=0 C=27 D=27 1311
00460 [L1963] JMP      A=2 B=128 C=3 D=32771 target=464
00461 [L1963] TGETS    A=2 B=0 C=8 D=8 'type_id'
00462 [L1963] ISNEN    A=2 B=0 C=28 D=28 1312
00463 [L1963] JMP      A=2 B=128 C=3 D=32771 target=467
00464 [L1964] UGET     A=2 B=0 C=5 D=5 showAdvance
00465 [L1964] CALL     A=2 B=1 C=1 D=257 
00466 [L1964] JMP      A=2 B=128 C=48 D=32816 target=515
00467 [L1965] TGETS    A=2 B=0 C=8 D=8 'type_id'
00468 [L1965] ISNEN    A=2 B=0 C=29 D=29 1035
00469 [L1965] JMP      A=2 B=128 C=1 D=32769 target=471
00470 [L1965] JMP      A=2 B=128 C=44 D=32812 target=515
00471 [L1967] TGETS    A=2 B=0 C=8 D=8 'type_id'
00472 [L1967] ISNEN    A=2 B=0 C=30 D=30 1016
00473 [L1967] JMP      A=2 B=128 C=1 D=32769 target=475
00474 [L1967] JMP      A=2 B=128 C=40 D=32808 target=515
00475 [L1969] TGETS    A=2 B=0 C=8 D=8 'type_id'
00476 [L1969] KSHORT   A=3 B=5 C=160 D=1440 1440
00477 [L1969] ISGT     A=2 B=0 C=3 D=3 
00478 [L1969] JMP      A=2 B=128 C=12 D=32780 target=491
00479 [L1969] TGETS    A=2 B=0 C=8 D=8 'type_id'
00480 [L1969] KSHORT   A=3 B=5 C=151 D=1431 1431
00481 [L1969] ISGT     A=3 B=0 C=2 D=2 
00482 [L1969] JMP      A=2 B=128 C=8 D=32776 target=491
00483 [L1970] GGET     A=2 B=0 C=1 D=1 'd_ms'
00484 [L1970] TGETS    A=2 B=2 C=66 D=578 'd_treasureMapUI'
00485 [L1970] TGETS    A=2 B=2 C=67 D=579 'requestUseTreasureMap'
00486 [L1970] GGET     A=3 B=0 C=11 D=11 'g_packageUI'
00487 [L1970] TGETS    A=3 B=3 C=12 D=780 'parent'
00488 [L1970] TGETS    A=4 B=0 C=8 D=8 'type_id'
00489 [L1970] CALL     A=2 B=1 C=3 D=259 
00490 [L1970] JMP      A=2 B=128 C=24 D=32792 target=515
00491 [L1971] TGETS    A=2 B=0 C=8 D=8 'type_id'
00492 [L1971] ISNEN    A=2 B=0 C=31 D=31 1363
00493 [L1971] JMP      A=2 B=128 C=18 D=32786 target=512
00494 [L1972] TDUP     A=2 B=0 C=68 D=68 {'kind': 'table', 'value': {'min': 1}}
00495 [L1972] UGET     A=3 B=0 C=2 D=2 math
00496 [L1972] TGETS    A=3 B=3 C=23 D=791 'min'
00497 [L1972] KSHORT   A=4 B=0 C=15 D=15 15
00498 [L1972] TGETS    A=5 B=0 C=0 D=0 'count'
00499 [L1972] CALL     A=3 B=2 C=3 D=515 
00500 [L1972] TSETS    A=3 B=2 C=25 D=537 'max'
00501 [L1973] GGET     A=3 B=0 C=1 D=1 'd_ms'
00502 [L1973] TGETS    A=3 B=3 C=26 D=794 'd_data'
00503 [L1973] TGETS    A=3 B=3 C=27 D=795 'createBatchUse'
00504 [L1973] GGET     A=4 B=0 C=1 D=1 'd_ms'
00505 [L1973] TGETS    A=4 B=4 C=28 D=1052 'd_mainUI'
00506 [L1973] TGETS    A=4 B=4 C=29 D=1053 'g_mainUI'
00507 [L1973] TGETS    A=4 B=4 C=30 D=1054 'main_layer'
00508 [L1973] MOV      A=5 B=0 C=2 D=2 
00509 [L1973] MOV      A=6 B=0 C=1 D=1 
00510 [L1973] CALL     A=3 B=1 C=4 D=260 
00511 [L1973] JMP      A=2 B=128 C=3 D=32771 target=515
00512 [L1975] UGET     A=2 B=0 C=0 D=0 cclog
00513 [L1975] KSTR     A=3 B=0 C=69 D=69 'play used other item'
00514 [L1975] CALL     A=2 B=1 C=2 D=258 
00515 [L1977] UCLO     A=0 B=128 C=0 D=32768 target=516
00516 [L1977] RET0     A=0 B=0 C=1 D=1 
00517 [L1977] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto49 offset=0xd617 source_lines=1979-1987 params=1
UPVALUES []
00001 [L1980] KSHORT   A=1 B=0 C=1 D=1 1
00002 [L1980] GGET     A=2 B=0 C=0 D=0 'g_propsTable'
00003 [L1980] LEN      A=2 B=0 C=2 D=2 
00004 [L1980] KSHORT   A=3 B=0 C=1 D=1 1
00005 [L1980] FORI     A=1 B=128 C=16 D=32784 target=22
00006 [L1981] GGET     A=5 B=0 C=0 D=0 'g_propsTable'
00007 [L1981] TGETV    A=5 B=5 C=4 D=1284 
00008 [L1981] TGETS    A=5 B=5 C=1 D=1281 'type_id'
00009 [L1981] ISNEV    A=5 B=0 C=0 D=0 
00010 [L1981] JMP      A=5 B=128 C=10 D=32778 target=21
00011 [L1981] GGET     A=5 B=0 C=0 D=0 'g_propsTable'
00012 [L1981] TGETV    A=5 B=5 C=4 D=1284 
00013 [L1981] TGETS    A=5 B=5 C=2 D=1282 'count'
00014 [L1981] KSHORT   A=6 B=0 C=0 D=0 0
00015 [L1981] ISGE     A=6 B=0 C=5 D=5 
00016 [L1981] JMP      A=5 B=128 C=4 D=32772 target=21
00017 [L1982] GGET     A=5 B=0 C=0 D=0 'g_propsTable'
00018 [L1982] TGETV    A=5 B=5 C=4 D=1284 
00019 [L1982] TGETS    A=5 B=5 C=3 D=1283 'id'
00020 [L1982] RET1     A=5 B=0 C=2 D=2 
00021 [L1980] FORL     A=1 B=127 C=240 D=32752 target=6
00022 [L1986] KSHORT   A=1 B=0 C=0 D=0 0
00023 [L1986] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto50 offset=0xd6cd source_lines=1989-1992 params=1
UPVALUES []
00001 [L1990] GGET     A=1 B=0 C=0 D=0 'd_ms'
00002 [L1990] TGETS    A=1 B=1 C=1 D=257 'd_info'
00003 [L1990] TGETS    A=1 B=1 C=2 D=258 'show'
00004 [L1990] GGET     A=2 B=0 C=0 D=0 'd_ms'
00005 [L1990] TGETS    A=2 B=2 C=3 D=515 'd_hz'
00006 [L1990] TGETS    A=2 B=2 C=4 D=516 'gethz'
00007 [L1990] KSTR     A=3 B=0 C=5 D=5 'getHZ'
00008 [L1990] CALL     A=2 B=2 C=2 D=514 
00009 [L1990] GGET     A=3 B=0 C=0 D=0 'd_ms'
00010 [L1990] TGETS    A=3 B=3 C=3 D=771 'd_hz'
00011 [L1990] TGETS    A=3 B=3 C=4 D=772 'gethz'
00012 [L1990] KSTR     A=4 B=0 C=6 D=6 'money'
00013 [L1990] CALL     A=3 B=2 C=2 D=514 
00014 [L1990] TGETS    A=4 B=0 C=7 D=7 'silver_count'
00015 [L1990] CAT      A=2 B=2 C=4 D=516 
00016 [L1990] KSHORT   A=3 B=0 C=2 D=2 2
00017 [L1990] CALL     A=1 B=1 C=3 D=259 
00018 [L1991] GGET     A=1 B=0 C=8 D=8 'refreshPackage'
00019 [L1991] CALL     A=1 B=1 C=1 D=257 
00020 [L1992] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto51 offset=0xd790 source_lines=1994-2048 params=1
UPVALUES ['cclog']
00001 [L1995] UGET     A=1 B=0 C=0 D=0 cclog
00002 [L1995] KSTR     A=2 B=0 C=0 D=0 'call getDateFormServer'
00003 [L1995] CALL     A=1 B=1 C=2 D=258 
00004 [L1996] GGET     A=1 B=0 C=1 D=1 'd_ms'
00005 [L1996] TGETS    A=1 B=1 C=2 D=258 'd_alert'
00006 [L1996] TGETS    A=1 B=1 C=3 D=259 'stop_wait'
00007 [L1996] CALL     A=1 B=1 C=1 D=257 
00008 [L1997] KSHORT   A=1 B=0 C=1 D=1 1
00009 [L1997] TGETS    A=2 B=0 C=4 D=4 'attach_list'
00010 [L1997] LEN      A=2 B=0 C=2 D=2 
00011 [L1997] KSHORT   A=3 B=0 C=1 D=1 1
00012 [L1997] FORI     A=1 B=128 C=13 D=32781 target=26
00013 [L1998] TGETS    A=5 B=0 C=4 D=4 'attach_list'
00014 [L1998] TGETV    A=5 B=5 C=4 D=1284 
00015 [L1998] ISEQP    A=5 B=0 C=0 D=0 
00016 [L1998] JMP      A=5 B=128 C=8 D=32776 target=25
00017 [L1998] TGETS    A=5 B=0 C=4 D=4 'attach_list'
00018 [L1998] TGETV    A=5 B=5 C=4 D=1284 
00019 [L1998] TGETS    A=5 B=5 C=5 D=1285 'star_level'
00020 [L1998] ISF      A=0 B=0 C=5 D=5 
00021 [L1998] JMP      A=6 B=128 C=3 D=32771 target=25
00022 [L1999] UGET     A=5 B=0 C=0 D=0 cclog
00023 [L1999] KSTR     A=6 B=0 C=6 D=6 ''
00024 [L1999] CALL     A=5 B=1 C=2 D=258 
00025 [L1997] FORL     A=1 B=127 C=243 D=32755 target=13
00026 [L2002] TGETS    A=1 B=0 C=7 D=7 'first_send'
00027 [L2002] ISNEP    A=1 B=0 C=2 D=2 
00028 [L2002] JMP      A=1 B=128 C=8 D=32776 target=37
00029 [L2003] UGET     A=1 B=0 C=0 D=0 cclog
00030 [L2003] KSTR     A=2 B=0 C=8 D=8 'getDateFormServer:first_send is true'
00031 [L2003] CALL     A=1 B=1 C=2 D=258 
00032 [L2004] TNEW     A=1 B=0 C=0 D=0 
00033 [L2004] GSET     A=1 B=0 C=9 D=9 'g_packageItemsInfo'
00034 [L2005] TGETS    A=1 B=0 C=4 D=4 'attach_list'
00035 [L2005] GSET     A=1 B=0 C=9 D=9 'g_packageItemsInfo'
00036 [L2005] JMP      A=1 B=128 C=39 D=32807 target=76
00037 [L2007] GGET     A=1 B=0 C=9 D=9 'g_packageItemsInfo'
00038 [L2007] ISNEP    A=1 B=0 C=0 D=0 
00039 [L2007] JMP      A=1 B=128 C=20 D=32788 target=60
00040 [L2008] UGET     A=1 B=0 C=0 D=0 cclog
00041 [L2008] KSTR     A=2 B=0 C=10 D=10 'g_packageItemsInfo is nil request again'
00042 [L2008] CALL     A=1 B=1 C=2 D=258 
00043 [L2009] TNEW     A=1 B=0 C=0 D=0 
00044 [L2010] KSHORT   A=2 B=255 C=255 D=65535 -1
00045 [L2010] TSETS    A=2 B=1 C=11 D=267 'flag'
00046 [L2011] UGET     A=2 B=0 C=0 D=0 cclog
00047 [L2011] KSTR     A=3 B=0 C=12 D=12 'send ST_msg_query_cortege_list_1033 to BS.'
00048 [L2011] CALL     A=2 B=1 C=2 D=258 
00049 [L2012] GGET     A=2 B=0 C=1 D=1 'd_ms'
00050 [L2012] TGETS    A=2 B=2 C=13 D=525 'd_u'
00051 [L2012] TGETS    A=2 B=2 C=14 D=526 'main_server_send_msg'
00052 [L2012] GGET     A=3 B=0 C=1 D=1 'd_ms'
00053 [L2012] TGETS    A=3 B=3 C=15 D=783 'd_msg_def'
00054 [L2012] TGETS    A=3 B=3 C=16 D=784 'gscl_msg_id'
00055 [L2012] TGETS    A=3 B=3 C=17 D=785 'msg_query_cortege_list'
00056 [L2012] MOV      A=4 B=0 C=1 D=1 
00057 [L2012] CALL     A=2 B=1 C=3 D=259 
00058 [L2013] RET0     A=0 B=0 C=1 D=1 
00059 [L2013] JMP      A=1 B=128 C=16 D=32784 target=76
00060 [L2015] UGET     A=1 B=0 C=0 D=0 cclog
00061 [L2015] KSTR     A=2 B=0 C=18 D=18 'get g_packageItemsInfo data'
00062 [L2015] CALL     A=1 B=1 C=2 D=258 
00063 [L2016] KSHORT   A=1 B=0 C=1 D=1 1
00064 [L2016] TGETS    A=2 B=0 C=4 D=4 'attach_list'
00065 [L2016] LEN      A=2 B=0 C=2 D=2 
00066 [L2016] KSHORT   A=3 B=0 C=1 D=1 1
00067 [L2016] FORI     A=1 B=128 C=8 D=32776 target=76
00068 [L2017] GGET     A=5 B=0 C=9 D=9 'g_packageItemsInfo'
00069 [L2017] GGET     A=6 B=0 C=9 D=9 'g_packageItemsInfo'
00070 [L2017] LEN      A=6 B=0 C=6 D=6 
00071 [L2017] ADDVN    A=6 B=6 C=0 D=1536 
00072 [L2017] TGETS    A=7 B=0 C=4 D=4 'attach_list'
00073 [L2017] TGETV    A=7 B=7 C=4 D=1796 
00074 [L2017] TSETV    A=7 B=5 C=6 D=1286 
00075 [L2016] FORL     A=1 B=127 C=248 D=32760 target=68
00076 [L2021] UGET     A=1 B=0 C=0 D=0 cclog
00077 [L2021] KSTR     A=2 B=0 C=19 D=19 'getDateFormServer1035 get data end'
00078 [L2021] CALL     A=1 B=1 C=2 D=258 
00079 [L2038] GGET     A=1 B=0 C=1 D=1 'd_ms'
00080 [L2038] TGETS    A=1 B=1 C=20 D=276 'd_event_mgr'
00081 [L2038] TGETS    A=1 B=1 C=21 D=277 'getNextPackageType'
00082 [L2038] CALL     A=1 B=2 C=1 D=513 
00083 [L2039] ISNEN    A=1 B=0 C=1 D=1 1035
00084 [L2039] JMP      A=2 B=128 C=6 D=32774 target=91
00085 [L2040] UGET     A=2 B=0 C=0 D=0 cclog
00086 [L2040] KSTR     A=3 B=0 C=22 D=22 '1035, next is 1035, go on...'
00087 [L2040] CALL     A=2 B=1 C=2 D=258 
00088 [L2041] KPRI     A=2 B=0 C=1 D=1 
00089 [L2041] GSET     A=2 B=0 C=23 D=23 'g_isPackageSorted'
00090 [L2041] JMP      A=2 B=128 C=6 D=32774 target=97
00091 [L2043] GGET     A=2 B=0 C=24 D=24 'sortItems'
00092 [L2043] CALL     A=2 B=1 C=1 D=257 
00093 [L2044] GGET     A=2 B=0 C=1 D=1 'd_ms'
00094 [L2044] TGETS    A=2 B=2 C=20 D=532 'd_event_mgr'
00095 [L2044] KPRI     A=3 B=0 C=0 D=0 
00096 [L2044] TSETS    A=3 B=2 C=25 D=537 'g_next_msg_type'
00097 [L2047] UGET     A=2 B=0 C=0 D=0 cclog
00098 [L2047] KSTR     A=3 B=0 C=26 D=26 'getDateFormServer1035 end '
00099 [L2047] CALL     A=2 B=1 C=2 D=258 
00100 [L2048] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto52 offset=0xdbc9 source_lines=2050-2074 params=0
UPVALUES ['o_t', 'pairs', 'm_t', 'table']
00001 [L2051] GGET     A=0 B=0 C=0 D=0 'g_reorgItemsInfo'
00002 [L2051] UGET     A=1 B=0 C=0 D=0 o_t
00003 [L2051] TGETS    A=1 B=1 C=1 D=257 'item'
00004 [L2051] TGETV    A=0 B=0 C=1 D=1 
00005 [L2052] TNEW     A=1 B=0 C=0 D=0 
00006 [L2052] GSET     A=1 B=0 C=2 D=2 'g_propsTable'
00007 [L2053] UGET     A=1 B=0 C=1 D=1 pairs
00008 [L2053] UGET     A=2 B=0 C=2 D=2 m_t
00009 [L2053] CALL     A=1 B=4 C=2 D=1026 
00010 [L2053] ISNEXT   A=4 B=128 C=50 D=32818 target=61
00011 [L2054] UGET     A=6 B=0 C=2 D=2 m_t
00012 [L2054] TGETS    A=6 B=6 C=3 D=1539 'talismans'
00013 [L2054] ISGE     A=6 B=0 C=5 D=5 
00014 [L2054] JMP      A=6 B=128 C=46 D=32814 target=61
00015 [L2055] UGET     A=6 B=0 C=2 D=2 m_t
00016 [L2055] TGETS    A=6 B=6 C=4 D=1540 'stone'
00017 [L2055] ISEQV    A=5 B=0 C=6 D=6 
00018 [L2055] JMP      A=6 B=128 C=42 D=32810 target=61
00019 [L2056] UGET     A=6 B=0 C=2 D=2 m_t
00020 [L2056] TGETS    A=6 B=6 C=5 D=1541 'adaptive_spirit'
00021 [L2056] ISEQV    A=5 B=0 C=6 D=6 
00022 [L2056] JMP      A=6 B=128 C=38 D=32806 target=61
00023 [L2057] UGET     A=6 B=0 C=2 D=2 m_t
00024 [L2057] TGETS    A=6 B=6 C=6 D=1542 'fragment'
00025 [L2057] ISEQV    A=5 B=0 C=6 D=6 
00026 [L2057] JMP      A=6 B=128 C=34 D=32802 target=61
00027 [L2058] UGET     A=6 B=0 C=2 D=2 m_t
00028 [L2058] TGETS    A=6 B=6 C=7 D=1543 'ext_skill'
00029 [L2058] ISEQV    A=5 B=0 C=6 D=6 
00030 [L2058] JMP      A=6 B=128 C=30 D=32798 target=61
00031 [L2059] UGET     A=6 B=0 C=2 D=2 m_t
00032 [L2059] TGETS    A=6 B=6 C=8 D=1544 'summer_card'
00033 [L2059] ISEQV    A=5 B=0 C=6 D=6 
00034 [L2059] JMP      A=6 B=128 C=26 D=32794 target=61
00035 [L2060] UGET     A=6 B=0 C=2 D=2 m_t
00036 [L2060] TGETS    A=6 B=6 C=9 D=1545 'awaken_star'
00037 [L2060] ISEQV    A=5 B=0 C=6 D=6 
00038 [L2060] JMP      A=6 B=128 C=22 D=32790 target=61
00039 [L2061] UGET     A=6 B=0 C=2 D=2 m_t
00040 [L2061] TGETS    A=6 B=6 C=10 D=1546 'invisible_card'
00041 [L2061] ISEQV    A=5 B=0 C=6 D=6 
00042 [L2061] JMP      A=6 B=128 C=18 D=32786 target=61
00043 [L2062] UGET     A=6 B=0 C=2 D=2 m_t
00044 [L2062] TGETS    A=6 B=6 C=11 D=1547 'dan_bagua'
00045 [L2062] ISEQV    A=5 B=0 C=6 D=6 
00046 [L2062] JMP      A=6 B=128 C=14 D=32782 target=61
00047 [L2064] TGETV    A=6 B=0 C=5 D=5 
00048 [L2065] ISF      A=0 B=0 C=6 D=6 
00049 [L2065] JMP      A=7 B=128 C=11 D=32779 target=61
00050 [L2066] KSHORT   A=7 B=0 C=1 D=1 1
00051 [L2066] LEN      A=8 B=0 C=6 D=6 
00052 [L2066] KSHORT   A=9 B=0 C=1 D=1 1
00053 [L2066] FORI     A=7 B=128 C=7 D=32775 target=61
00054 [L2067] GGET     A=11 B=0 C=2 D=2 'g_propsTable'
00055 [L2067] GGET     A=12 B=0 C=2 D=2 'g_propsTable'
00056 [L2067] LEN      A=12 B=0 C=12 D=12 
00057 [L2067] ADDVN    A=12 B=12 C=0 D=3072 
00058 [L2067] TGETV    A=13 B=6 C=10 D=1546 
00059 [L2067] TSETV    A=13 B=11 C=12 D=2828 
00060 [L2066] FORL     A=7 B=127 C=249 D=32761 target=54
00061 [L2053] ITERN    A=4 B=3 C=3 D=771 
00062 [L2053] ITERL    A=4 B=127 C=204 D=32716 target=11
00063 [L2073] UGET     A=1 B=0 C=3 D=3 table
00064 [L2073] TGETS    A=1 B=1 C=12 D=268 'sort'
00065 [L2073] GGET     A=2 B=0 C=2 D=2 'g_propsTable'
00066 [L2073] GGET     A=3 B=0 C=13 D=13 'sortProps'
00067 [L2073] CALL     A=1 B=1 C=3 D=259 
00068 [L2074] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto53 offset=0xde13 source_lines=2076-2147 params=0
UPVALUES ['cclog', 'o_t']
00001 [L2077] UGET     A=0 B=0 C=0 D=0 cclog
00002 [L2077] KSTR     A=1 B=0 C=0 D=0 'in sortItems'
00003 [L2077] CALL     A=0 B=1 C=2 D=258 
00004 [L2078] GGET     A=0 B=0 C=1 D=1 'g_packageItemsInfo'
00005 [L2080] ISNEP    A=0 B=0 C=0 D=0 
00006 [L2080] JMP      A=1 B=128 C=4 D=32772 target=11
00007 [L2081] UGET     A=1 B=0 C=0 D=0 cclog
00008 [L2081] KSTR     A=2 B=0 C=2 D=2 'can use item table'
00009 [L2081] CALL     A=1 B=1 C=2 D=258 
00010 [L2082] RET0     A=0 B=0 C=1 D=1 
00011 [L2085] TNEW     A=1 B=8 C=0 D=2048 
00012 [L2085] UGET     A=2 B=0 C=1 D=1 o_t
00013 [L2085] TGETS    A=2 B=2 C=3 D=515 'item'
00014 [L2085] TNEW     A=3 B=0 C=0 D=0 
00015 [L2085] TSETV    A=3 B=1 C=2 D=258 
00016 [L2085] UGET     A=2 B=0 C=1 D=1 o_t
00017 [L2085] TGETS    A=2 B=2 C=4 D=516 'skill'
00018 [L2085] TNEW     A=3 B=0 C=0 D=0 
00019 [L2085] TSETV    A=3 B=1 C=2 D=258 
00020 [L2085] GSET     A=1 B=0 C=5 D=5 'g_reorgItemsInfo'
00021 [L2087] KPRI     A=1 B=0 C=0 D=0 
00022 [L2088] TNEW     A=2 B=0 C=9 D=9 
00023 [L2088] TNEW     A=3 B=0 C=0 D=0 
00024 [L2088] TSETB    A=3 B=2 C=1 D=513 
00025 [L2088] TNEW     A=3 B=0 C=0 D=0 
00026 [L2088] TSETB    A=3 B=2 C=2 D=514 
00027 [L2088] TNEW     A=3 B=0 C=0 D=0 
00028 [L2088] TSETB    A=3 B=2 C=3 D=515 
00029 [L2088] TNEW     A=3 B=0 C=0 D=0 
00030 [L2088] TSETB    A=3 B=2 C=4 D=516 
00031 [L2088] TNEW     A=3 B=0 C=0 D=0 
00032 [L2088] TSETB    A=3 B=2 C=5 D=517 
00033 [L2088] TNEW     A=3 B=0 C=0 D=0 
00034 [L2088] TSETB    A=3 B=2 C=6 D=518 
00035 [L2088] TNEW     A=3 B=0 C=0 D=0 
00036 [L2088] TSETB    A=3 B=2 C=7 D=519 
00037 [L2088] TNEW     A=3 B=0 C=0 D=0 
00038 [L2088] TSETB    A=3 B=2 C=8 D=520 
00039 [L2088] GSET     A=2 B=0 C=6 D=6 'g_usedItems'
00040 [L2089] TNEW     A=2 B=0 C=17 D=17 
00041 [L2089] TNEW     A=3 B=0 C=0 D=0 
00042 [L2089] TSETB    A=3 B=2 C=1 D=513 
00043 [L2089] TNEW     A=3 B=0 C=0 D=0 
00044 [L2089] TSETB    A=3 B=2 C=2 D=514 
00045 [L2089] TNEW     A=3 B=0 C=0 D=0 
00046 [L2089] TSETB    A=3 B=2 C=3 D=515 
00047 [L2089] TNEW     A=3 B=0 C=0 D=0 
00048 [L2089] TSETB    A=3 B=2 C=4 D=516 
00049 [L2089] TNEW     A=3 B=0 C=0 D=0 
00050 [L2089] TSETB    A=3 B=2 C=5 D=517 
00051 [L2089] TNEW     A=3 B=0 C=0 D=0 
00052 [L2089] TSETB    A=3 B=2 C=6 D=518 
00053 [L2089] TNEW     A=3 B=0 C=0 D=0 
00054 [L2089] TSETB    A=3 B=2 C=7 D=519 
00055 [L2089] TNEW     A=3 B=0 C=0 D=0 
00056 [L2089] TSETB    A=3 B=2 C=8 D=520 
00057 [L2090] TNEW     A=3 B=0 C=0 D=0 
00058 [L2090] TSETB    A=3 B=2 C=9 D=521 
00059 [L2090] TNEW     A=3 B=0 C=0 D=0 
00060 [L2090] TSETB    A=3 B=2 C=10 D=522 
00061 [L2090] TNEW     A=3 B=0 C=0 D=0 
00062 [L2090] TSETB    A=3 B=2 C=11 D=523 
00063 [L2090] TNEW     A=3 B=0 C=0 D=0 
00064 [L2090] TSETB    A=3 B=2 C=12 D=524 
00065 [L2090] TNEW     A=3 B=0 C=0 D=0 
00066 [L2090] TSETB    A=3 B=2 C=13 D=525 
00067 [L2090] TNEW     A=3 B=0 C=0 D=0 
00068 [L2090] TSETB    A=3 B=2 C=14 D=526 
00069 [L2090] TNEW     A=3 B=0 C=0 D=0 
00070 [L2090] TSETB    A=3 B=2 C=15 D=527 
00071 [L2090] TNEW     A=3 B=0 C=0 D=0 
00072 [L2090] TSETB    A=3 B=2 C=16 D=528 
00073 [L2090] GSET     A=2 B=0 C=7 D=7 'g_cheer_items'
00074 [L2092] UGET     A=2 B=0 C=0 D=0 cclog
00075 [L2092] KSTR     A=3 B=0 C=8 D=8 'start get csvInfo'
00076 [L2092] CALL     A=2 B=1 C=2 D=258 
00077 [L2093] GGET     A=2 B=0 C=9 D=9 'getPackageCSVConfig'
00078 [L2093] CALL     A=2 B=1 C=1 D=257 
00079 [L2094] GGET     A=2 B=0 C=10 D=10 'getItembasePriceCSVConfig'
00080 [L2094] CALL     A=2 B=1 C=1 D=257 
00081 [L2095] GGET     A=2 B=0 C=11 D=11 'getItemLevelPriceCSVConfig'
00082 [L2095] CALL     A=2 B=1 C=1 D=257 
00083 [L2097] UGET     A=2 B=0 C=0 D=0 cclog
00084 [L2097] KSTR     A=3 B=0 C=12 D=12 'end get csvInfo'
00085 [L2097] CALL     A=2 B=1 C=2 D=258 
00086 [L2099] UGET     A=2 B=0 C=0 D=0 cclog
00087 [L2099] KSTR     A=3 B=0 C=13 D=13 'start reorgItemsInfo'
00088 [L2099] CALL     A=2 B=1 C=2 D=258 
00089 [L2101] KSHORT   A=2 B=0 C=1 D=1 1
00090 [L2101] LEN      A=3 B=0 C=0 D=0 
00091 [L2101] KSHORT   A=4 B=0 C=1 D=1 1
00092 [L2101] FORI     A=2 B=128 C=85 D=32853 target=178
00093 [L2104] TGETV    A=6 B=0 C=5 D=5 
00094 [L2104] TGETS    A=6 B=6 C=14 D=1550 'attach_type'
00095 [L2105] TGETV    A=7 B=0 C=5 D=5 
00096 [L2105] TGETS    A=7 B=7 C=15 D=1807 'type_id'
00097 [L2106] UGET     A=8 B=0 C=1 D=1 o_t
00098 [L2106] TGETS    A=8 B=8 C=3 D=2051 'item'
00099 [L2106] ISNEV    A=6 B=0 C=8 D=8 
00100 [L2106] JMP      A=8 B=128 C=21 D=32789 target=122
00101 [L2107] TGETV    A=8 B=0 C=5 D=5 
00102 [L2107] GGET     A=9 B=0 C=17 D=17 'g_itemAttrTable'
00103 [L2107] TGETV    A=9 B=9 C=7 D=2311 
00104 [L2107] TSETS    A=9 B=8 C=16 D=2064 'csvInfo'
00105 [L2108] TGETV    A=8 B=0 C=5 D=5 
00106 [L2108] TGETS    A=8 B=8 C=16 D=2064 'csvInfo'
00107 [L2108] TGETS    A=8 B=8 C=18 D=2066 'mainType'
00108 [L2109] GGET     A=9 B=0 C=5 D=5 'g_reorgItemsInfo'
00109 [L2109] TGETV    A=9 B=9 C=6 D=2310 
00110 [L2110] TGETV    A=10 B=9 C=8 D=2312 
00111 [L2110] IST      A=0 B=0 C=10 D=10 
00112 [L2110] JMP      A=10 B=128 C=2 D=32770 target=115
00113 [L2111] TNEW     A=10 B=0 C=0 D=0 
00114 [L2111] TSETV    A=10 B=9 C=8 D=2312 
00115 [L2113] TGETV    A=10 B=9 C=8 D=2312 
00116 [L2113] LEN      A=10 B=0 C=10 D=10 
00117 [L2114] TGETV    A=11 B=9 C=8 D=2312 
00118 [L2114] ADDVN    A=12 B=10 C=0 D=2560 
00119 [L2114] TGETV    A=13 B=0 C=5 D=5 
00120 [L2114] TSETV    A=13 B=11 C=12 D=2828 
00121 [L2114] JMP      A=8 B=128 C=14 D=32782 target=136
00122 [L2116] UGET     A=8 B=0 C=1 D=1 o_t
00123 [L2116] TGETS    A=8 B=8 C=4 D=2052 'skill'
00124 [L2116] ISNEV    A=6 B=0 C=8 D=8 
00125 [L2116] JMP      A=8 B=128 C=10 D=32778 target=136
00126 [L2117] TGETV    A=8 B=0 C=5 D=5 
00127 [L2117] GGET     A=9 B=0 C=19 D=19 'g_itemSkillTable'
00128 [L2117] TGETV    A=9 B=9 C=7 D=2311 
00129 [L2117] TSETS    A=9 B=8 C=16 D=2064 'csvInfo'
00130 [L2118] GGET     A=8 B=0 C=5 D=5 'g_reorgItemsInfo'
00131 [L2118] TGETV    A=8 B=8 C=6 D=2054 
00132 [L2119] LEN      A=9 B=0 C=8 D=8 
00133 [L2120] ADDVN    A=10 B=9 C=0 D=2304 
00134 [L2120] TGETV    A=11 B=0 C=5 D=5 
00135 [L2120] TSETV    A=11 B=8 C=10 D=2058 
00136 [L2122] TGETV    A=8 B=0 C=5 D=5 
00137 [L2122] TGETS    A=8 B=8 C=20 D=2068 'equip_order'
00138 [L2122] KSHORT   A=9 B=0 C=0 D=0 0
00139 [L2122] ISGE     A=9 B=0 C=8 D=8 
00140 [L2122] JMP      A=8 B=128 C=17 D=32785 target=158
00141 [L2122] TGETV    A=8 B=0 C=5 D=5 
00142 [L2122] TGETS    A=8 B=8 C=20 D=2068 'equip_order'
00143 [L2122] KSHORT   A=9 B=0 C=8 D=8 8
00144 [L2122] ISGT     A=8 B=0 C=9 D=9 
00145 [L2122] JMP      A=8 B=128 C=12 D=32780 target=158
00146 [L2123] TGETV    A=8 B=0 C=5 D=5 
00147 [L2123] TGETS    A=8 B=8 C=20 D=2068 'equip_order'
00148 [L2124] GGET     A=9 B=0 C=6 D=6 'g_usedItems'
00149 [L2124] TGETV    A=9 B=9 C=8 D=2312 
00150 [L2125] TNEW     A=10 B=0 C=0 D=0 
00151 [L2126] TGETV    A=11 B=0 C=5 D=5 
00152 [L2126] TSETS    A=11 B=10 C=3 D=2563 'item'
00153 [L2127] TSETS    A=5 B=10 C=21 D=2581 'index'
00154 [L2128] LEN      A=11 B=0 C=9 D=9 
00155 [L2128] ADDVN    A=11 B=11 C=0 D=2816 
00156 [L2128] TSETV    A=10 B=9 C=11 D=2315 
00157 [L2128] JMP      A=8 B=128 C=19 D=32787 target=177
00158 [L2129] TGETV    A=8 B=0 C=5 D=5 
00159 [L2129] TGETS    A=8 B=8 C=20 D=2068 'equip_order'
00160 [L2129] KSHORT   A=9 B=0 C=8 D=8 8
00161 [L2129] ISGE     A=9 B=0 C=8 D=8 
00162 [L2129] JMP      A=8 B=128 C=14 D=32782 target=177
00163 [L2129] TGETV    A=8 B=0 C=5 D=5 
00164 [L2129] TGETS    A=8 B=8 C=20 D=2068 'equip_order'
00165 [L2129] KSHORT   A=9 B=0 C=24 D=24 24
00166 [L2129] ISGT     A=8 B=0 C=9 D=9 
00167 [L2129] JMP      A=8 B=128 C=9 D=32777 target=177
00168 [L2130] TGETV    A=8 B=0 C=5 D=5 
00169 [L2130] TGETS    A=8 B=8 C=20 D=2068 'equip_order'
00170 [L2131] GGET     A=9 B=0 C=7 D=7 'g_cheer_items'
00171 [L2131] SUBVN    A=10 B=8 C=1 D=2049 
00172 [L2131] TGETV    A=9 B=9 C=10 D=2314 
00173 [L2132] LEN      A=10 B=0 C=9 D=9 
00174 [L2132] ADDVN    A=10 B=10 C=0 D=2560 
00175 [L2132] TGETV    A=11 B=0 C=5 D=5 
00176 [L2132] TSETV    A=11 B=9 C=10 D=2314 
00177 [L2101] FORL     A=2 B=127 C=171 D=32683 target=93
00178 [L2136] UGET     A=2 B=0 C=0 D=0 cclog
00179 [L2136] KSTR     A=3 B=0 C=22 D=22 'end reorgItemsInfo'
00180 [L2136] CALL     A=2 B=1 C=2 D=258 
00181 [L2139] GGET     A=2 B=0 C=23 D=23 'd_ms'
00182 [L2139] TGETS    A=2 B=2 C=24 D=536 'd_lineupUI'
00183 [L2139] TGETS    A=2 B=2 C=25 D=537 'g_displayLineupInfo'
00184 [L2139] GGET     A=3 B=0 C=6 D=6 'g_usedItems'
00185 [L2139] TSETS    A=3 B=2 C=26 D=538 'allUsedItems'
00186 [L2141] UGET     A=2 B=0 C=0 D=0 cclog
00187 [L2141] KSTR     A=3 B=0 C=27 D=27 'start sort'
00188 [L2141] CALL     A=2 B=1 C=2 D=258 
00189 [L2144] GGET     A=2 B=0 C=28 D=28 'sortPackage'
00190 [L2144] CALL     A=2 B=1 C=1 D=257 
00191 [L2146] UGET     A=2 B=0 C=0 D=0 cclog
00192 [L2146] KSTR     A=3 B=0 C=29 D=29 'end sort'
00193 [L2146] CALL     A=2 B=1 C=2 D=258 
00194 [L2147] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto54 offset=0xe471 source_lines=2149-2154 params=2
UPVALUES []
00001 [L2150] TGETS    A=2 B=0 C=0 D=0 'csvInfo'
00002 [L2150] TGETS    A=2 B=2 C=1 D=513 'sortOrder'
00003 [L2150] IST      A=0 B=0 C=2 D=2 
00004 [L2150] JMP      A=3 B=128 C=1 D=32769 target=6
00005 [L2150] KSHORT   A=2 B=0 C=0 D=0 0
00006 [L2151] TGETS    A=3 B=1 C=0 D=256 'csvInfo'
00007 [L2151] TGETS    A=3 B=3 C=1 D=769 'sortOrder'
00008 [L2151] IST      A=0 B=0 C=3 D=3 
00009 [L2151] JMP      A=4 B=128 C=1 D=32769 target=11
00010 [L2151] KSHORT   A=3 B=0 C=0 D=0 0
00011 [L2153] ISLT     A=2 B=0 C=3 D=3 
00012 [L2153] JMP      A=4 B=128 C=2 D=32770 target=15
00013 [L2153] KPRI     A=4 B=0 C=1 D=1 
00014 [L2153] JMP      A=5 B=128 C=1 D=32769 target=16
00015 [L2153] KPRI     A=4 B=0 C=2 D=2 
00016 [L2153] RET1     A=4 B=0 C=2 D=2 

FUNCTION proto55 offset=0xe4fb source_lines=2156-2178 params=0
UPVALUES ['o_t', 'm_t', 'table']
00001 [L2157] GGET     A=0 B=0 C=0 D=0 'g_reorgItemsInfo'
00002 [L2157] UGET     A=1 B=0 C=0 D=0 o_t
00003 [L2157] TGETS    A=1 B=1 C=1 D=257 'item'
00004 [L2157] TGETV    A=0 B=0 C=1 D=1 
00005 [L2157] UGET     A=1 B=0 C=1 D=1 m_t
00006 [L2157] TGETS    A=1 B=1 C=2 D=258 'weapon'
00007 [L2157] TGETV    A=0 B=0 C=1 D=1 
00008 [L2157] ISF      A=0 B=0 C=0 D=0 
00009 [L2157] JMP      A=1 B=128 C=11 D=32779 target=21
00010 [L2158] UGET     A=0 B=0 C=2 D=2 table
00011 [L2158] TGETS    A=0 B=0 C=3 D=3 'sort'
00012 [L2158] GGET     A=1 B=0 C=0 D=0 'g_reorgItemsInfo'
00013 [L2158] UGET     A=2 B=0 C=0 D=0 o_t
00014 [L2158] TGETS    A=2 B=2 C=1 D=513 'item'
00015 [L2158] TGETV    A=1 B=1 C=2 D=258 
00016 [L2158] UGET     A=2 B=0 C=1 D=1 m_t
00017 [L2158] TGETS    A=2 B=2 C=2 D=514 'weapon'
00018 [L2158] TGETV    A=1 B=1 C=2 D=258 
00019 [L2158] GGET     A=2 B=0 C=4 D=4 'packageSortFunc'
00020 [L2158] CALL     A=0 B=1 C=3 D=259 
00021 [L2161] GGET     A=0 B=0 C=0 D=0 'g_reorgItemsInfo'
00022 [L2161] UGET     A=1 B=0 C=0 D=0 o_t
00023 [L2161] TGETS    A=1 B=1 C=1 D=257 'item'
00024 [L2161] TGETV    A=0 B=0 C=1 D=1 
00025 [L2161] UGET     A=1 B=0 C=1 D=1 m_t
00026 [L2161] TGETS    A=1 B=1 C=5 D=261 'guard'
00027 [L2161] TGETV    A=0 B=0 C=1 D=1 
00028 [L2161] ISF      A=0 B=0 C=0 D=0 
00029 [L2161] JMP      A=1 B=128 C=11 D=32779 target=41
00030 [L2162] UGET     A=0 B=0 C=2 D=2 table
00031 [L2162] TGETS    A=0 B=0 C=3 D=3 'sort'
00032 [L2162] GGET     A=1 B=0 C=0 D=0 'g_reorgItemsInfo'
00033 [L2162] UGET     A=2 B=0 C=0 D=0 o_t
00034 [L2162] TGETS    A=2 B=2 C=1 D=513 'item'
00035 [L2162] TGETV    A=1 B=1 C=2 D=258 
00036 [L2162] UGET     A=2 B=0 C=1 D=1 m_t
00037 [L2162] TGETS    A=2 B=2 C=5 D=517 'guard'
00038 [L2162] TGETV    A=1 B=1 C=2 D=258 
00039 [L2162] GGET     A=2 B=0 C=4 D=4 'packageSortFunc'
00040 [L2162] CALL     A=0 B=1 C=3 D=259 
00041 [L2165] GGET     A=0 B=0 C=0 D=0 'g_reorgItemsInfo'
00042 [L2165] UGET     A=1 B=0 C=0 D=0 o_t
00043 [L2165] TGETS    A=1 B=1 C=1 D=257 'item'
00044 [L2165] TGETV    A=0 B=0 C=1 D=1 
00045 [L2165] UGET     A=1 B=0 C=1 D=1 m_t
00046 [L2165] TGETS    A=1 B=1 C=6 D=262 'talismans'
00047 [L2165] TGETV    A=0 B=0 C=1 D=1 
00048 [L2165] ISF      A=0 B=0 C=0 D=0 
00049 [L2165] JMP      A=1 B=128 C=11 D=32779 target=61
00050 [L2166] UGET     A=0 B=0 C=2 D=2 table
00051 [L2166] TGETS    A=0 B=0 C=3 D=3 'sort'
00052 [L2166] GGET     A=1 B=0 C=0 D=0 'g_reorgItemsInfo'
00053 [L2166] UGET     A=2 B=0 C=0 D=0 o_t
00054 [L2166] TGETS    A=2 B=2 C=1 D=513 'item'
00055 [L2166] TGETV    A=1 B=1 C=2 D=258 
00056 [L2166] UGET     A=2 B=0 C=1 D=1 m_t
00057 [L2166] TGETS    A=2 B=2 C=6 D=518 'talismans'
00058 [L2166] TGETV    A=1 B=1 C=2 D=258 
00059 [L2166] GGET     A=2 B=0 C=4 D=4 'packageSortFunc'
00060 [L2166] CALL     A=0 B=1 C=3 D=259 
00061 [L2169] GGET     A=0 B=0 C=0 D=0 'g_reorgItemsInfo'
00062 [L2169] UGET     A=1 B=0 C=0 D=0 o_t
00063 [L2169] TGETS    A=1 B=1 C=1 D=257 'item'
00064 [L2169] TGETV    A=0 B=0 C=1 D=1 
00065 [L2169] UGET     A=1 B=0 C=1 D=1 m_t
00066 [L2169] TGETS    A=1 B=1 C=7 D=263 'stone'
00067 [L2169] TGETV    A=0 B=0 C=1 D=1 
00068 [L2169] ISF      A=0 B=0 C=0 D=0 
00069 [L2169] JMP      A=1 B=128 C=11 D=32779 target=81
00070 [L2170] UGET     A=0 B=0 C=2 D=2 table
00071 [L2170] TGETS    A=0 B=0 C=3 D=3 'sort'
00072 [L2170] GGET     A=1 B=0 C=0 D=0 'g_reorgItemsInfo'
00073 [L2170] UGET     A=2 B=0 C=0 D=0 o_t
00074 [L2170] TGETS    A=2 B=2 C=1 D=513 'item'
00075 [L2170] TGETV    A=1 B=1 C=2 D=258 
00076 [L2170] UGET     A=2 B=0 C=1 D=1 m_t
00077 [L2170] TGETS    A=2 B=2 C=7 D=519 'stone'
00078 [L2170] TGETV    A=1 B=1 C=2 D=258 
00079 [L2170] GGET     A=2 B=0 C=8 D=8 'stoneSort'
00080 [L2170] CALL     A=0 B=1 C=3 D=259 
00081 [L2173] GGET     A=0 B=0 C=0 D=0 'g_reorgItemsInfo'
00082 [L2173] UGET     A=1 B=0 C=0 D=0 o_t
00083 [L2173] TGETS    A=1 B=1 C=9 D=265 'skill'
00084 [L2173] TGETV    A=0 B=0 C=1 D=1 
00085 [L2173] ISF      A=0 B=0 C=0 D=0 
00086 [L2173] JMP      A=1 B=128 C=8 D=32776 target=95
00087 [L2174] UGET     A=0 B=0 C=2 D=2 table
00088 [L2174] TGETS    A=0 B=0 C=3 D=3 'sort'
00089 [L2174] GGET     A=1 B=0 C=0 D=0 'g_reorgItemsInfo'
00090 [L2174] UGET     A=2 B=0 C=0 D=0 o_t
00091 [L2174] TGETS    A=2 B=2 C=9 D=521 'skill'
00092 [L2174] TGETV    A=1 B=1 C=2 D=258 
00093 [L2174] GGET     A=2 B=0 C=10 D=10 'skillSortFunc'
00094 [L2174] CALL     A=0 B=1 C=3 D=259 
00095 [L2177] KPRI     A=0 B=0 C=2 D=2 
00096 [L2177] GSET     A=0 B=0 C=11 D=11 'g_isPackageSorted'
00097 [L2178] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto56 offset=0xe77a source_lines=2180-2192 params=2
UPVALUES []
00001 [L2181] TGETS    A=2 B=0 C=0 D=0 'owner_id'
00002 [L2181] KSHORT   A=3 B=0 C=0 D=0 0
00003 [L2181] ISGE     A=3 B=0 C=2 D=2 
00004 [L2181] JMP      A=2 B=128 C=6 D=32774 target=11
00005 [L2181] TGETS    A=2 B=1 C=0 D=256 'owner_id'
00006 [L2181] ISNEN    A=2 B=0 C=0 D=0 0
00007 [L2181] JMP      A=2 B=128 C=3 D=32771 target=11
00008 [L2182] KPRI     A=2 B=0 C=2 D=2 
00009 [L2182] RET1     A=2 B=0 C=2 D=2 
00010 [L2182] JMP      A=2 B=128 C=33 D=32801 target=44
00011 [L2183] TGETS    A=2 B=0 C=0 D=0 'owner_id'
00012 [L2183] ISNEN    A=2 B=0 C=0 D=0 0
00013 [L2183] JMP      A=2 B=128 C=7 D=32775 target=21
00014 [L2183] TGETS    A=2 B=1 C=0 D=256 'owner_id'
00015 [L2183] KSHORT   A=3 B=0 C=0 D=0 0
00016 [L2183] ISGE     A=3 B=0 C=2 D=2 
00017 [L2183] JMP      A=2 B=128 C=3 D=32771 target=21
00018 [L2184] KPRI     A=2 B=0 C=1 D=1 
00019 [L2184] RET1     A=2 B=0 C=2 D=2 
00020 [L2184] JMP      A=2 B=128 C=23 D=32791 target=44
00021 [L2186] TGETS    A=2 B=0 C=1 D=1 'level'
00022 [L2186] TGETS    A=3 B=1 C=1 D=257 'level'
00023 [L2186] ISNEV    A=2 B=0 C=3 D=3 
00024 [L2186] JMP      A=2 B=128 C=11 D=32779 target=36
00025 [L2187] TGETS    A=2 B=0 C=2 D=2 'csvInfo'
00026 [L2187] TGETS    A=2 B=2 C=3 D=515 'sub_type'
00027 [L2187] TGETS    A=3 B=1 C=2 D=258 'csvInfo'
00028 [L2187] TGETS    A=3 B=3 C=3 D=771 'sub_type'
00029 [L2187] ISLT     A=2 B=0 C=3 D=3 
00030 [L2187] JMP      A=2 B=128 C=2 D=32770 target=33
00031 [L2187] KPRI     A=2 B=0 C=1 D=1 
00032 [L2187] JMP      A=3 B=128 C=1 D=32769 target=34
00033 [L2187] KPRI     A=2 B=0 C=2 D=2 
00034 [L2187] RET1     A=2 B=0 C=2 D=2 
00035 [L2187] JMP      A=2 B=128 C=8 D=32776 target=44
00036 [L2189] TGETS    A=2 B=0 C=1 D=1 'level'
00037 [L2189] TGETS    A=3 B=1 C=1 D=257 'level'
00038 [L2189] ISLT     A=3 B=0 C=2 D=2 
00039 [L2189] JMP      A=2 B=128 C=2 D=32770 target=42
00040 [L2189] KPRI     A=2 B=0 C=1 D=1 
00041 [L2189] JMP      A=3 B=128 C=1 D=32769 target=43
00042 [L2189] KPRI     A=2 B=0 C=2 D=2 
00043 [L2189] RET1     A=2 B=0 C=2 D=2 
00044 [L2192] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto57 offset=0xe88d source_lines=2195-2217 params=2
UPVALUES []
00001 [L2196] TGETS    A=2 B=0 C=0 D=0 'equip_order'
00002 [L2196] KSHORT   A=3 B=0 C=0 D=0 0
00003 [L2196] ISLT     A=3 B=0 C=2 D=2 
00004 [L2196] JMP      A=2 B=128 C=2 D=32770 target=7
00005 [L2196] KPRI     A=2 B=0 C=1 D=1 
00006 [L2196] JMP      A=3 B=128 C=1 D=32769 target=8
00007 [L2196] KPRI     A=2 B=0 C=2 D=2 
00008 [L2197] TGETS    A=3 B=1 C=0 D=256 'equip_order'
00009 [L2197] KSHORT   A=4 B=0 C=0 D=0 0
00010 [L2197] ISLT     A=4 B=0 C=3 D=3 
00011 [L2197] JMP      A=3 B=128 C=2 D=32770 target=14
00012 [L2197] KPRI     A=3 B=0 C=1 D=1 
00013 [L2197] JMP      A=4 B=128 C=1 D=32769 target=15
00014 [L2197] KPRI     A=3 B=0 C=2 D=2 
00015 [L2198] ISF      A=0 B=0 C=2 D=2 
00016 [L2198] JMP      A=4 B=128 C=5 D=32773 target=22
00017 [L2198] IST      A=0 B=0 C=3 D=3 
00018 [L2198] JMP      A=4 B=128 C=3 D=32771 target=22
00019 [L2199] KPRI     A=4 B=0 C=2 D=2 
00020 [L2199] RET1     A=4 B=0 C=2 D=2 
00021 [L2199] JMP      A=4 B=128 C=60 D=32828 target=82
00022 [L2200] IST      A=0 B=0 C=2 D=2 
00023 [L2200] JMP      A=4 B=128 C=5 D=32773 target=29
00024 [L2200] ISF      A=0 B=0 C=3 D=3 
00025 [L2200] JMP      A=4 B=128 C=3 D=32771 target=29
00026 [L2201] KPRI     A=4 B=0 C=1 D=1 
00027 [L2201] RET1     A=4 B=0 C=2 D=2 
00028 [L2201] JMP      A=4 B=128 C=53 D=32821 target=82
00029 [L2203] TGETS    A=4 B=0 C=1 D=1 'csvInfo'
00030 [L2203] TGETS    A=4 B=4 C=2 D=1026 'quality'
00031 [L2203] TGETS    A=5 B=1 C=1 D=257 'csvInfo'
00032 [L2203] TGETS    A=5 B=5 C=2 D=1282 'quality'
00033 [L2203] ISNEV    A=4 B=0 C=5 D=5 
00034 [L2203] JMP      A=4 B=128 C=37 D=32805 target=72
00035 [L2204] TGETS    A=4 B=0 C=3 D=3 'advance_level'
00036 [L2204] TGETS    A=5 B=1 C=3 D=259 'advance_level'
00037 [L2204] ISNEV    A=4 B=0 C=5 D=5 
00038 [L2204] JMP      A=4 B=128 C=24 D=32792 target=63
00039 [L2205] TGETS    A=4 B=0 C=4 D=4 'level'
00040 [L2205] TGETS    A=5 B=1 C=4 D=260 'level'
00041 [L2205] ISNEV    A=4 B=0 C=5 D=5 
00042 [L2205] JMP      A=4 B=128 C=11 D=32779 target=54
00043 [L2206] TGETS    A=4 B=0 C=1 D=1 'csvInfo'
00044 [L2206] TGETS    A=4 B=4 C=5 D=1029 'name'
00045 [L2206] TGETS    A=5 B=1 C=1 D=257 'csvInfo'
00046 [L2206] TGETS    A=5 B=5 C=5 D=1285 'name'
00047 [L2206] ISLT     A=5 B=0 C=4 D=4 
00048 [L2206] JMP      A=4 B=128 C=2 D=32770 target=51
00049 [L2206] KPRI     A=4 B=0 C=1 D=1 
00050 [L2206] JMP      A=5 B=128 C=1 D=32769 target=52
00051 [L2206] KPRI     A=4 B=0 C=2 D=2 
00052 [L2206] RET1     A=4 B=0 C=2 D=2 
00053 [L2206] JMP      A=4 B=128 C=28 D=32796 target=82
00054 [L2208] TGETS    A=4 B=0 C=4 D=4 'level'
00055 [L2208] TGETS    A=5 B=1 C=4 D=260 'level'
00056 [L2208] ISLT     A=5 B=0 C=4 D=4 
00057 [L2208] JMP      A=4 B=128 C=2 D=32770 target=60
00058 [L2208] KPRI     A=4 B=0 C=1 D=1 
00059 [L2208] JMP      A=5 B=128 C=1 D=32769 target=61
00060 [L2208] KPRI     A=4 B=0 C=2 D=2 
00061 [L2208] RET1     A=4 B=0 C=2 D=2 
00062 [L2209] JMP      A=4 B=128 C=19 D=32787 target=82
00063 [L2211] TGETS    A=4 B=0 C=3 D=3 'advance_level'
00064 [L2211] TGETS    A=5 B=1 C=3 D=259 'advance_level'
00065 [L2211] ISLT     A=5 B=0 C=4 D=4 
00066 [L2211] JMP      A=4 B=128 C=2 D=32770 target=69
00067 [L2211] KPRI     A=4 B=0 C=1 D=1 
00068 [L2211] JMP      A=5 B=128 C=1 D=32769 target=70
00069 [L2211] KPRI     A=4 B=0 C=2 D=2 
00070 [L2211] RET1     A=4 B=0 C=2 D=2 
00071 [L2212] JMP      A=4 B=128 C=10 D=32778 target=82
00072 [L2214] TGETS    A=4 B=0 C=1 D=1 'csvInfo'
00073 [L2214] TGETS    A=4 B=4 C=2 D=1026 'quality'
00074 [L2214] TGETS    A=5 B=1 C=1 D=257 'csvInfo'
00075 [L2214] TGETS    A=5 B=5 C=2 D=1282 'quality'
00076 [L2214] ISLT     A=5 B=0 C=4 D=4 
00077 [L2214] JMP      A=4 B=128 C=2 D=32770 target=80
00078 [L2214] KPRI     A=4 B=0 C=1 D=1 
00079 [L2214] JMP      A=5 B=128 C=1 D=32769 target=81
00080 [L2214] KPRI     A=4 B=0 C=2 D=2 
00081 [L2214] RET1     A=4 B=0 C=2 D=2 
00082 [L2217] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto58 offset=0xea88 source_lines=2220-2248 params=2
UPVALUES []
00001 [L2222] TGETS    A=2 B=0 C=0 D=0 'equip_order'
00002 [L2223] TGETS    A=3 B=1 C=0 D=256 'equip_order'
00003 [L2224] ISEQV    A=2 B=0 C=3 D=3 
00004 [L2224] JMP      A=4 B=128 C=16 D=32784 target=21
00005 [L2225] ISNEN    A=2 B=0 C=0 D=0 0
00006 [L2225] JMP      A=4 B=128 C=3 D=32771 target=10
00007 [L2226] KPRI     A=4 B=0 C=1 D=1 
00008 [L2226] RET1     A=4 B=0 C=2 D=2 
00009 [L2226] JMP      A=4 B=128 C=11 D=32779 target=21
00010 [L2227] ISNEN    A=3 B=0 C=0 D=0 0
00011 [L2227] JMP      A=4 B=128 C=3 D=32771 target=15
00012 [L2228] KPRI     A=4 B=0 C=2 D=2 
00013 [L2228] RET1     A=4 B=0 C=2 D=2 
00014 [L2228] JMP      A=4 B=128 C=6 D=32774 target=21
00015 [L2230] ISLT     A=2 B=0 C=3 D=3 
00016 [L2230] JMP      A=4 B=128 C=2 D=32770 target=19
00017 [L2230] KPRI     A=4 B=0 C=1 D=1 
00018 [L2230] JMP      A=5 B=128 C=1 D=32769 target=20
00019 [L2230] KPRI     A=4 B=0 C=2 D=2 
00020 [L2230] RET1     A=4 B=0 C=2 D=2 
00021 [L2234] TGETS    A=4 B=0 C=1 D=1 'csvInfo'
00022 [L2234] TGETS    A=4 B=4 C=2 D=1026 'quality'
00023 [L2234] TGETS    A=5 B=1 C=1 D=257 'csvInfo'
00024 [L2234] TGETS    A=5 B=5 C=2 D=1282 'quality'
00025 [L2234] ISNEV    A=4 B=0 C=5 D=5 
00026 [L2234] JMP      A=4 B=128 C=41 D=32809 target=68
00027 [L2235] TGETS    A=4 B=0 C=3 D=3 'level'
00028 [L2235] TGETS    A=5 B=1 C=3 D=259 'level'
00029 [L2235] ISNEV    A=4 B=0 C=5 D=5 
00030 [L2235] JMP      A=4 B=128 C=28 D=32796 target=59
00031 [L2237] TGETS    A=4 B=0 C=1 D=1 'csvInfo'
00032 [L2237] TGETS    A=4 B=4 C=4 D=1028 'effectField'
00033 [L2237] TGETS    A=5 B=1 C=1 D=257 'csvInfo'
00034 [L2237] TGETS    A=5 B=5 C=4 D=1284 'effectField'
00035 [L2237] ISNEV    A=4 B=0 C=5 D=5 
00036 [L2237] JMP      A=4 B=128 C=11 D=32779 target=48
00037 [L2238] TGETS    A=4 B=0 C=1 D=1 'csvInfo'
00038 [L2238] TGETS    A=4 B=4 C=5 D=1029 'name'
00039 [L2238] TGETS    A=5 B=1 C=1 D=257 'csvInfo'
00040 [L2238] TGETS    A=5 B=5 C=5 D=1285 'name'
00041 [L2238] ISLT     A=5 B=0 C=4 D=4 
00042 [L2238] JMP      A=4 B=128 C=2 D=32770 target=45
00043 [L2238] KPRI     A=4 B=0 C=1 D=1 
00044 [L2238] JMP      A=5 B=128 C=1 D=32769 target=46
00045 [L2238] KPRI     A=4 B=0 C=2 D=2 
00046 [L2238] RET1     A=4 B=0 C=2 D=2 
00047 [L2238] JMP      A=4 B=128 C=30 D=32798 target=78
00048 [L2240] TGETS    A=4 B=0 C=1 D=1 'csvInfo'
00049 [L2240] TGETS    A=4 B=4 C=4 D=1028 'effectField'
00050 [L2240] TGETS    A=5 B=1 C=1 D=257 'csvInfo'
00051 [L2240] TGETS    A=5 B=5 C=4 D=1284 'effectField'
00052 [L2240] ISLT     A=4 B=0 C=5 D=5 
00053 [L2240] JMP      A=4 B=128 C=2 D=32770 target=56
00054 [L2240] KPRI     A=4 B=0 C=1 D=1 
00055 [L2240] JMP      A=5 B=128 C=1 D=32769 target=57
00056 [L2240] KPRI     A=4 B=0 C=2 D=2 
00057 [L2240] RET1     A=4 B=0 C=2 D=2 
00058 [L2241] JMP      A=4 B=128 C=19 D=32787 target=78
00059 [L2243] TGETS    A=4 B=0 C=3 D=3 'level'
00060 [L2243] TGETS    A=5 B=1 C=3 D=259 'level'
00061 [L2243] ISLT     A=5 B=0 C=4 D=4 
00062 [L2243] JMP      A=4 B=128 C=2 D=32770 target=65
00063 [L2243] KPRI     A=4 B=0 C=1 D=1 
00064 [L2243] JMP      A=5 B=128 C=1 D=32769 target=66
00065 [L2243] KPRI     A=4 B=0 C=2 D=2 
00066 [L2243] RET1     A=4 B=0 C=2 D=2 
00067 [L2244] JMP      A=4 B=128 C=10 D=32778 target=78
00068 [L2246] TGETS    A=4 B=0 C=1 D=1 'csvInfo'
00069 [L2246] TGETS    A=4 B=4 C=2 D=1026 'quality'
00070 [L2246] TGETS    A=5 B=1 C=1 D=257 'csvInfo'
00071 [L2246] TGETS    A=5 B=5 C=2 D=1282 'quality'
00072 [L2246] ISLT     A=5 B=0 C=4 D=4 
00073 [L2246] JMP      A=4 B=128 C=2 D=32770 target=76
00074 [L2246] KPRI     A=4 B=0 C=1 D=1 
00075 [L2246] JMP      A=5 B=128 C=1 D=32769 target=77
00076 [L2246] KPRI     A=4 B=0 C=2 D=2 
00077 [L2246] RET1     A=4 B=0 C=2 D=2 
00078 [L2248] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto59 offset=0xec70 source_lines=2251-2258 params=2
UPVALUES ['string']
00001 [L2252] UGET     A=2 B=0 C=0 D=0 string
00002 [L2252] TGETS    A=2 B=2 C=0 D=512 'len'
00003 [L2252] MOV      A=3 B=0 C=0 D=0 
00004 [L2252] CALL     A=2 B=2 C=2 D=514 
00005 [L2253] UGET     A=3 B=0 C=0 D=0 string
00006 [L2253] TGETS    A=3 B=3 C=0 D=768 'len'
00007 [L2253] MOV      A=4 B=0 C=1 D=1 
00008 [L2253] CALL     A=3 B=2 C=2 D=514 
00009 [L2254] UGET     A=4 B=0 C=0 D=0 string
00010 [L2254] TGETS    A=4 B=4 C=1 D=1025 'byte'
00011 [L2254] MOV      A=5 B=0 C=0 D=0 
00012 [L2254] MOV      A=6 B=0 C=2 D=2 
00013 [L2254] CALL     A=4 B=2 C=3 D=515 
00014 [L2255] UGET     A=5 B=0 C=0 D=0 string
00015 [L2255] TGETS    A=5 B=5 C=1 D=1281 'byte'
00016 [L2255] MOV      A=6 B=0 C=1 D=1 
00017 [L2255] MOV      A=7 B=0 C=3 D=3 
00018 [L2255] CALL     A=5 B=2 C=3 D=515 
00019 [L2257] SUBVV    A=6 B=4 C=5 D=1029 
00020 [L2257] RET1     A=6 B=0 C=2 D=2 

FUNCTION proto60 offset=0xed1e source_lines=2260-2269 params=1
UPVALUES []
00001 [L2261] TGETS    A=1 B=0 C=0 D=0 'equip_order'
00002 [L2261] ISF      A=0 B=0 C=1 D=1 
00003 [L2261] JMP      A=2 B=128 C=13 D=32781 target=17
00004 [L2261] TGETS    A=1 B=0 C=0 D=0 'equip_order'
00005 [L2261] KSHORT   A=2 B=0 C=0 D=0 0
00006 [L2261] ISGE     A=2 B=0 C=1 D=1 
00007 [L2261] JMP      A=1 B=128 C=9 D=32777 target=17
00008 [L2264] GGET     A=1 B=0 C=1 D=1 'd_ms'
00009 [L2264] TGETS    A=1 B=1 C=2 D=258 'd_lineupUI'
00010 [L2264] TGETS    A=1 B=1 C=3 D=259 'g_usedCharacters'
00011 [L2264] TGETS    A=2 B=0 C=0 D=0 'equip_order'
00012 [L2264] TGETV    A=1 B=1 C=2 D=258 
00013 [L2264] TGETS    A=1 B=1 C=4 D=260 'character'
00014 [L2264] TGETS    A=1 B=1 C=5 D=261 'csvInfo'
00015 [L2264] TGETS    A=1 B=1 C=6 D=262 'name'
00016 [L2265] RET1     A=1 B=0 C=2 D=2 
00017 [L2268] KSTR     A=1 B=0 C=7 D=7 ' '
00018 [L2268] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto61 offset=0xeddb source_lines=2271-2291 params=0
UPVALUES ['pairs', 'tonumber']
00001 [L2272] GGET     A=0 B=0 C=0 D=0 'g_itemLevelPriceTable'
00002 [L2272] ISNEP    A=0 B=0 C=0 D=0 
00003 [L2272] JMP      A=0 B=128 C=43 D=32811 target=47
00004 [L2273] GGET     A=0 B=0 C=1 D=1 'd_ms'
00005 [L2273] TGETS    A=0 B=0 C=2 D=2 'd_csv'
00006 [L2273] TGETS    A=0 B=0 C=3 D=3 'open'
00007 [L2273] KSTR     A=1 B=0 C=4 D=4 'csv_config/equip_enhance_cost.csv'
00008 [L2273] CALL     A=0 B=2 C=2 D=514 
00009 [L2274] TNEW     A=1 B=0 C=0 D=0 
00010 [L2274] GSET     A=1 B=0 C=0 D=0 'g_itemLevelPriceTable'
00011 [L2275] GGET     A=1 B=0 C=0 D=0 'g_itemLevelPriceTable'
00012 [L2277] UGET     A=2 B=0 C=0 D=0 pairs
00013 [L2277] TGETS    A=3 B=0 C=5 D=5 'records'
00014 [L2277] CALL     A=2 B=4 C=2 D=1026 
00015 [L2277] ISNEXT   A=5 B=128 C=29 D=32797 target=45
00016 [L2278] UGET     A=7 B=0 C=1 D=1 tonumber
00017 [L2278] TGETB    A=8 B=6 C=1 D=1537 
00018 [L2278] CALL     A=7 B=2 C=2 D=514 
00019 [L2279] TGETV    A=8 B=1 C=7 D=263 
00020 [L2279] IST      A=0 B=0 C=8 D=8 
00021 [L2279] JMP      A=8 B=128 C=2 D=32770 target=24
00022 [L2280] TNEW     A=8 B=0 C=0 D=0 
00023 [L2280] TSETV    A=8 B=1 C=7 D=263 
00024 [L2283] TGETV    A=8 B=1 C=7 D=263 
00025 [L2284] UGET     A=9 B=0 C=1 D=1 tonumber
00026 [L2284] TGETB    A=10 B=6 C=2 D=1538 
00027 [L2284] CALL     A=9 B=2 C=2 D=514 
00028 [L2284] TSETB    A=9 B=8 C=1 D=2049 
00029 [L2285] UGET     A=9 B=0 C=1 D=1 tonumber
00030 [L2285] TGETB    A=10 B=6 C=3 D=1539 
00031 [L2285] CALL     A=9 B=2 C=2 D=514 
00032 [L2285] TSETB    A=9 B=8 C=2 D=2050 
00033 [L2286] UGET     A=9 B=0 C=1 D=1 tonumber
00034 [L2286] TGETB    A=10 B=6 C=4 D=1540 
00035 [L2286] CALL     A=9 B=2 C=2 D=514 
00036 [L2286] TSETB    A=9 B=8 C=3 D=2051 
00037 [L2287] UGET     A=9 B=0 C=1 D=1 tonumber
00038 [L2287] TGETB    A=10 B=6 C=5 D=1541 
00039 [L2287] CALL     A=9 B=2 C=2 D=514 
00040 [L2287] TSETB    A=9 B=8 C=4 D=2052 
00041 [L2288] UGET     A=9 B=0 C=1 D=1 tonumber
00042 [L2288] TGETB    A=10 B=6 C=6 D=1542 
00043 [L2288] CALL     A=9 B=2 C=2 D=514 
00044 [L2288] TSETB    A=9 B=8 C=5 D=2053 
00045 [L2277] ITERN    A=5 B=3 C=3 D=771 
00046 [L2277] ITERL    A=5 B=127 C=225 D=32737 target=16
00047 [L2291] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto62 offset=0xef84 source_lines=2293-2310 params=0
UPVALUES ['pairs', 'tonumber']
00001 [L2294] GGET     A=0 B=0 C=0 D=0 'g_itemBasePriceTable'
00002 [L2294] ISNEP    A=0 B=0 C=0 D=0 
00003 [L2294] JMP      A=0 B=128 C=31 D=32799 target=35
00004 [L2295] GGET     A=0 B=0 C=1 D=1 'd_ms'
00005 [L2295] TGETS    A=0 B=0 C=2 D=2 'd_csv'
00006 [L2295] TGETS    A=0 B=0 C=3 D=3 'open'
00007 [L2295] KSTR     A=1 B=0 C=4 D=4 'csv_config/item_sell_config.csv'
00008 [L2295] CALL     A=0 B=2 C=2 D=514 
00009 [L2296] TNEW     A=1 B=0 C=0 D=0 
00010 [L2296] GSET     A=1 B=0 C=0 D=0 'g_itemBasePriceTable'
00011 [L2297] GGET     A=1 B=0 C=0 D=0 'g_itemBasePriceTable'
00012 [L2299] UGET     A=2 B=0 C=0 D=0 pairs
00013 [L2299] TGETS    A=3 B=0 C=5 D=5 'records'
00014 [L2299] CALL     A=2 B=4 C=2 D=1026 
00015 [L2299] ISNEXT   A=5 B=128 C=17 D=32785 target=33
00016 [L2300] UGET     A=7 B=0 C=1 D=1 tonumber
00017 [L2300] TGETB    A=8 B=6 C=1 D=1537 
00018 [L2300] CALL     A=7 B=2 C=2 D=514 
00019 [L2301] TGETV    A=8 B=1 C=7 D=263 
00020 [L2301] IST      A=0 B=0 C=8 D=8 
00021 [L2301] JMP      A=8 B=128 C=2 D=32770 target=24
00022 [L2302] TNEW     A=8 B=0 C=0 D=0 
00023 [L2302] TSETV    A=8 B=1 C=7 D=263 
00024 [L2305] TGETV    A=8 B=1 C=7 D=263 
00025 [L2306] UGET     A=9 B=0 C=1 D=1 tonumber
00026 [L2306] TGETB    A=10 B=6 C=2 D=1538 
00027 [L2306] CALL     A=9 B=2 C=2 D=514 
00028 [L2306] TSETS    A=9 B=8 C=6 D=2054 'base'
00029 [L2307] UGET     A=9 B=0 C=1 D=1 tonumber
00030 [L2307] TGETB    A=10 B=6 C=3 D=1539 
00031 [L2307] CALL     A=9 B=2 C=2 D=514 
00032 [L2307] TSETS    A=9 B=8 C=7 D=2055 'ratio'
00033 [L2299] ITERN    A=5 B=3 C=3 D=771 
00034 [L2299] ITERL    A=5 B=127 C=237 D=32749 target=16
00035 [L2310] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto63 offset=0xf0f7 source_lines=2312-2446 params=0
UPVALUES ['pairs', 'tonumber', 'm_t']
00001 [L2314] GGET     A=0 B=0 C=0 D=0 'g_itemAttrTable'
00002 [L2314] ISNEP    A=0 B=0 C=0 D=0 
00003 [L2314] JMP      A=0 B=128 C=198 D=32966 target=202
00004 [L2317] GGET     A=0 B=0 C=1 D=1 'd_ms'
00005 [L2317] TGETS    A=0 B=0 C=2 D=2 'd_csv'
00006 [L2317] TGETS    A=0 B=0 C=3 D=3 'open'
00007 [L2317] KSTR     A=1 B=0 C=4 D=4 'csv_config/item_name.csv'
00008 [L2317] CALL     A=0 B=2 C=2 D=514 
00009 [L2318] TNEW     A=1 B=0 C=0 D=0 
00010 [L2319] UGET     A=2 B=0 C=0 D=0 pairs
00011 [L2319] TGETS    A=3 B=0 C=5 D=5 'records'
00012 [L2319] CALL     A=2 B=4 C=2 D=1026 
00013 [L2319] ISNEXT   A=5 B=128 C=24 D=32792 target=38
00014 [L2320] UGET     A=7 B=0 C=1 D=1 tonumber
00015 [L2320] TGETB    A=8 B=6 C=1 D=1537 
00016 [L2320] CALL     A=7 B=2 C=2 D=514 
00017 [L2321] TGETV    A=8 B=1 C=7 D=263 
00018 [L2321] IST      A=0 B=0 C=8 D=8 
00019 [L2321] JMP      A=8 B=128 C=2 D=32770 target=22
00020 [L2322] TNEW     A=8 B=0 C=0 D=0 
00021 [L2322] TSETV    A=8 B=1 C=7 D=263 
00022 [L2325] TGETV    A=8 B=1 C=7 D=263 
00023 [L2326] TGETB    A=9 B=6 C=2 D=1538 
00024 [L2326] TSETS    A=9 B=8 C=6 D=2054 'name'
00025 [L2327] TGETB    A=9 B=6 C=3 D=1539 
00026 [L2327] TSETS    A=9 B=8 C=7 D=2055 'description'
00027 [L2328] TGETB    A=9 B=6 C=4 D=1540 
00028 [L2328] TSETS    A=9 B=8 C=8 D=2056 'introduction'
00029 [L2329] UGET     A=9 B=0 C=1 D=1 tonumber
00030 [L2329] TGETB    A=10 B=6 C=5 D=1541 
00031 [L2329] CALL     A=9 B=2 C=2 D=514 
00032 [L2329] TSETS    A=9 B=8 C=9 D=2057 'sortOrder'
00033 [L2330] TGETB    A=9 B=6 C=6 D=1542 
00034 [L2330] IST      A=0 B=0 C=9 D=9 
00035 [L2330] JMP      A=10 B=128 C=1 D=32769 target=37
00036 [L2330] KSTR     A=9 B=0 C=11 D=11 ''
00037 [L2330] TSETS    A=9 B=8 C=10 D=2058 'product_desc'
00038 [L2319] ITERN    A=5 B=3 C=3 D=771 
00039 [L2319] ITERL    A=5 B=127 C=230 D=32742 target=14
00040 [L2333] GGET     A=2 B=0 C=1 D=1 'd_ms'
00041 [L2333] TGETS    A=2 B=2 C=2 D=514 'd_csv'
00042 [L2333] TGETS    A=2 B=2 C=3 D=515 'open'
00043 [L2333] KSTR     A=3 B=0 C=12 D=12 'csv_config/item_base.csv'
00044 [L2333] CALL     A=2 B=2 C=2 D=514 
00045 [L2334] TNEW     A=3 B=0 C=0 D=0 
00046 [L2334] GSET     A=3 B=0 C=0 D=0 'g_itemAttrTable'
00047 [L2335] GGET     A=3 B=0 C=0 D=0 'g_itemAttrTable'
00048 [L2337] UGET     A=4 B=0 C=0 D=0 pairs
00049 [L2337] TGETS    A=5 B=2 C=5 D=517 'records'
00050 [L2337] CALL     A=4 B=4 C=2 D=1026 
00051 [L2337] ISNEXT   A=7 B=128 C=148 D=32916 target=200
00052 [L2338] UGET     A=9 B=0 C=1 D=1 tonumber
00053 [L2338] TGETB    A=10 B=8 C=1 D=2049 
00054 [L2338] CALL     A=9 B=2 C=2 D=514 
00055 [L2339] TGETV    A=10 B=3 C=9 D=777 
00056 [L2339] IST      A=0 B=0 C=10 D=10 
00057 [L2339] JMP      A=10 B=128 C=2 D=32770 target=60
00058 [L2340] TNEW     A=10 B=0 C=0 D=0 
00059 [L2340] TSETV    A=10 B=3 C=9 D=777 
00060 [L2343] TGETV    A=10 B=3 C=9 D=777 
00061 [L2344] TGETV    A=11 B=1 C=9 D=265 
00062 [L2344] TGETS    A=11 B=11 C=6 D=2822 'name'
00063 [L2344] TSETS    A=11 B=10 C=6 D=2566 'name'
00064 [L2345] TGETV    A=11 B=1 C=9 D=265 
00065 [L2345] TGETS    A=11 B=11 C=9 D=2825 'sortOrder'
00066 [L2345] TSETS    A=11 B=10 C=9 D=2569 'sortOrder'
00067 [L2346] TGETB    A=11 B=8 C=2 D=2050 
00068 [L2346] TSETS    A=11 B=10 C=13 D=2573 'file'
00069 [L2347] UGET     A=11 B=0 C=1 D=1 tonumber
00070 [L2347] TGETB    A=12 B=8 C=3 D=2051 
00071 [L2347] CALL     A=11 B=2 C=2 D=514 
00072 [L2347] TSETS    A=11 B=10 C=14 D=2574 'quality'
00073 [L2348] UGET     A=11 B=0 C=1 D=1 tonumber
00074 [L2348] TGETB    A=12 B=8 C=4 D=2052 
00075 [L2348] CALL     A=11 B=2 C=2 D=514 
00076 [L2348] TSETS    A=11 B=10 C=15 D=2575 'mainType'
00077 [L2349] UGET     A=11 B=0 C=1 D=1 tonumber
00078 [L2349] TGETB    A=12 B=8 C=5 D=2053 
00079 [L2349] CALL     A=11 B=2 C=2 D=514 
00080 [L2349] TSETS    A=11 B=10 C=16 D=2576 'sub_type'
00081 [L2350] UGET     A=11 B=0 C=1 D=1 tonumber
00082 [L2350] TGETB    A=12 B=8 C=6 D=2054 
00083 [L2350] CALL     A=11 B=2 C=2 D=514 
00084 [L2350] TSETS    A=11 B=10 C=17 D=2577 'top_level'
00085 [L2351] UGET     A=11 B=0 C=1 D=1 tonumber
00086 [L2351] TGETB    A=12 B=8 C=7 D=2055 
00087 [L2351] CALL     A=11 B=2 C=2 D=514 
00088 [L2351] TSETS    A=11 B=10 C=18 D=2578 'isStackable'
00089 [L2352] UGET     A=11 B=0 C=1 D=1 tonumber
00090 [L2352] TGETB    A=12 B=8 C=8 D=2056 
00091 [L2352] CALL     A=11 B=2 C=2 D=514 
00092 [L2352] TSETS    A=11 B=10 C=19 D=2579 'equipPos'
00093 [L2353] UGET     A=11 B=0 C=1 D=1 tonumber
00094 [L2353] TGETB    A=12 B=8 C=9 D=2057 
00095 [L2353] CALL     A=11 B=2 C=2 D=514 
00096 [L2353] TSETS    A=11 B=10 C=20 D=2580 'effectField'
00097 [L2354] UGET     A=11 B=0 C=1 D=1 tonumber
00098 [L2354] TGETB    A=12 B=8 C=10 D=2058 
00099 [L2354] CALL     A=11 B=2 C=2 D=514 
00100 [L2354] TSETS    A=11 B=10 C=21 D=2581 'base_gongji_plus'
00101 [L2355] UGET     A=11 B=0 C=1 D=1 tonumber
00102 [L2355] TGETB    A=12 B=8 C=11 D=2059 
00103 [L2355] CALL     A=11 B=2 C=2 D=514 
00104 [L2355] TSETS    A=11 B=10 C=22 D=2582 'base_fangyu_plus'
00105 [L2356] UGET     A=11 B=0 C=1 D=1 tonumber
00106 [L2356] TGETB    A=12 B=8 C=12 D=2060 
00107 [L2356] CALL     A=11 B=2 C=2 D=514 
00108 [L2356] TSETS    A=11 B=10 C=23 D=2583 'base_maxhp_plus'
00109 [L2357] UGET     A=11 B=0 C=1 D=1 tonumber
00110 [L2357] TGETB    A=12 B=8 C=13 D=2061 
00111 [L2357] CALL     A=11 B=2 C=2 D=514 
00112 [L2357] TSETS    A=11 B=10 C=24 D=2584 'base_strength_plus'
00113 [L2358] UGET     A=11 B=0 C=1 D=1 tonumber
00114 [L2358] TGETB    A=12 B=8 C=14 D=2062 
00115 [L2358] CALL     A=11 B=2 C=2 D=514 
00116 [L2358] TSETS    A=11 B=10 C=25 D=2585 'base_energy_plus'
00117 [L2359] UGET     A=11 B=0 C=1 D=1 tonumber
00118 [L2359] TGETB    A=12 B=8 C=15 D=2063 
00119 [L2359] CALL     A=11 B=2 C=2 D=514 
00120 [L2359] TSETS    A=11 B=10 C=26 D=2586 'base_top_fight_count_plus'
00121 [L2360] UGET     A=11 B=0 C=1 D=1 tonumber
00122 [L2360] TGETB    A=12 B=8 C=16 D=2064 
00123 [L2360] CALL     A=11 B=2 C=2 D=514 
00124 [L2360] TSETS    A=11 B=10 C=27 D=2587 'base_experience_plus'
00125 [L2361] UGET     A=11 B=0 C=1 D=1 tonumber
00126 [L2361] TGETB    A=12 B=8 C=17 D=2065 
00127 [L2361] CALL     A=11 B=2 C=2 D=514 
00128 [L2361] TSETS    A=11 B=10 C=28 D=2588 'script_id'
00129 [L2362] UGET     A=11 B=0 C=1 D=1 tonumber
00130 [L2362] TGETB    A=12 B=8 C=18 D=2066 
00131 [L2362] CALL     A=11 B=2 C=2 D=514 
00132 [L2362] TSETS    A=11 B=10 C=29 D=2589 'effect_plus'
00133 [L2363] UGET     A=11 B=0 C=1 D=1 tonumber
00134 [L2363] TGETB    A=12 B=8 C=19 D=2067 
00135 [L2363] CALL     A=11 B=2 C=2 D=514 
00136 [L2363] TSETS    A=11 B=10 C=30 D=2590 'ownerType'
00137 [L2364] UGET     A=11 B=0 C=1 D=1 tonumber
00138 [L2364] TGETB    A=12 B=8 C=20 D=2068 
00139 [L2364] CALL     A=11 B=2 C=2 D=514 
00140 [L2364] TSETS    A=11 B=10 C=31 D=2591 'random_weight'
00141 [L2365] UGET     A=11 B=0 C=1 D=1 tonumber
00142 [L2365] TGETB    A=12 B=8 C=21 D=2069 
00143 [L2365] CALL     A=11 B=2 C=2 D=514 
00144 [L2365] TSETS    A=11 B=10 C=32 D=2592 'use_limit'
00145 [L2366] UGET     A=11 B=0 C=1 D=1 tonumber
00146 [L2366] TGETB    A=12 B=8 C=22 D=2070 
00147 [L2366] CALL     A=11 B=2 C=2 D=514 
00148 [L2366] TSETS    A=11 B=10 C=33 D=2593 'show_level'
00149 [L2367] UGET     A=11 B=0 C=1 D=1 tonumber
00150 [L2367] TGETB    A=12 B=8 C=23 D=2071 
00151 [L2367] CALL     A=11 B=2 C=2 D=514 
00152 [L2367] TSETS    A=11 B=10 C=34 D=2594 'base_contrib_plus'
00153 [L2368] TGETV    A=11 B=1 C=9 D=265 
00154 [L2368] TGETS    A=11 B=11 C=8 D=2824 'introduction'
00155 [L2368] TSETS    A=11 B=10 C=8 D=2568 'introduction'
00156 [L2369] TGETV    A=11 B=1 C=9 D=265 
00157 [L2369] TGETS    A=11 B=11 C=7 D=2823 'description'
00158 [L2369] TSETS    A=11 B=10 C=7 D=2567 'description'
00159 [L2370] TGETV    A=11 B=1 C=9 D=265 
00160 [L2370] TGETS    A=11 B=11 C=10 D=2826 'product_desc'
00161 [L2370] TSETS    A=11 B=10 C=10 D=2570 'product_desc'
00162 [L2372] KSHORT   A=11 B=39 C=16 D=10000 10000
00163 [L2372] ISGE     A=11 B=0 C=9 D=9 
00164 [L2372] JMP      A=11 B=128 C=10 D=32778 target=175
00165 [L2372] KSHORT   A=11 B=40 C=60 D=10300 10300
00166 [L2372] ISGE     A=9 B=0 C=11 D=11 
00167 [L2372] JMP      A=11 B=128 C=7 D=32775 target=175
00168 [L2372] TGETS    A=11 B=10 C=15 D=2575 'mainType'
00169 [L2372] ISNEN    A=11 B=0 C=0 D=0 15
00170 [L2372] JMP      A=11 B=128 C=4 D=32772 target=175
00171 [L2373] GGET     A=11 B=0 C=36 D=36 'getExtSkillDesc'
00172 [L2373] MOV      A=12 B=0 C=9 D=9 
00173 [L2373] CALL     A=11 B=2 C=2 D=514 
00174 [L2373] TSETS    A=11 B=10 C=35 D=2595 'ext_skill_desc'
00175 [L2377] TGETS    A=11 B=10 C=15 D=2575 'mainType'
00176 [L2377] UGET     A=12 B=0 C=2 D=2 m_t
00177 [L2377] TGETS    A=12 B=12 C=37 D=3109 'talismans'
00178 [L2377] ISGE     A=12 B=0 C=11 D=11 
00179 [L2377] JMP      A=11 B=128 C=9 D=32777 target=189
00180 [L2377] TGETS    A=11 B=10 C=15 D=2575 'mainType'
00181 [L2377] UGET     A=12 B=0 C=2 D=2 m_t
00182 [L2377] TGETS    A=12 B=12 C=38 D=3110 'stone'
00183 [L2377] ISEQV    A=11 B=0 C=12 D=12 
00184 [L2377] JMP      A=11 B=128 C=4 D=32772 target=189
00185 [L2378] GGET     A=11 B=0 C=40 D=40 'packageTagDef'
00186 [L2378] TGETS    A=11 B=11 C=41 D=2857 'props'
00187 [L2378] TSETS    A=11 B=10 C=39 D=2599 'packageTag'
00188 [L2378] JMP      A=11 B=128 C=11 D=32779 target=200
00189 [L2379] TGETS    A=11 B=10 C=15 D=2575 'mainType'
00190 [L2379] UGET     A=12 B=0 C=2 D=2 m_t
00191 [L2379] TGETS    A=12 B=12 C=38 D=3110 'stone'
00192 [L2379] ISNEV    A=11 B=0 C=12 D=12 
00193 [L2379] JMP      A=11 B=128 C=4 D=32772 target=198
00194 [L2380] GGET     A=11 B=0 C=40 D=40 'packageTagDef'
00195 [L2380] TGETS    A=11 B=11 C=38 D=2854 'stone'
00196 [L2380] TSETS    A=11 B=10 C=39 D=2599 'packageTag'
00197 [L2380] JMP      A=11 B=128 C=2 D=32770 target=200
00198 [L2383] TGETS    A=11 B=10 C=15 D=2575 'mainType'
00199 [L2383] TSETS    A=11 B=10 C=39 D=2599 'packageTag'
00200 [L2337] ITERN    A=7 B=3 C=3 D=771 
00201 [L2337] ITERL    A=7 B=127 C=106 D=32618 target=52
00202 [L2388] GGET     A=0 B=0 C=42 D=42 'g_itemSkillTable'
00203 [L2388] ISNEP    A=0 B=0 C=0 D=0 
00204 [L2388] JMP      A=0 B=128 C=132 D=32900 target=337
00205 [L2390] GGET     A=0 B=0 C=1 D=1 'd_ms'
00206 [L2390] TGETS    A=0 B=0 C=2 D=2 'd_csv'
00207 [L2390] TGETS    A=0 B=0 C=3 D=3 'open'
00208 [L2390] KSTR     A=1 B=0 C=43 D=43 'csv_config/skill_name.csv'
00209 [L2390] CALL     A=0 B=2 C=2 D=514 
00210 [L2391] TNEW     A=1 B=0 C=0 D=0 
00211 [L2392] UGET     A=2 B=0 C=0 D=0 pairs
00212 [L2392] TGETS    A=3 B=0 C=5 D=5 'records'
00213 [L2392] CALL     A=2 B=4 C=2 D=1026 
00214 [L2392] ISNEXT   A=5 B=128 C=20 D=32788 target=235
00215 [L2393] UGET     A=7 B=0 C=1 D=1 tonumber
00216 [L2393] TGETB    A=8 B=6 C=1 D=1537 
00217 [L2393] CALL     A=7 B=2 C=2 D=514 
00218 [L2394] TGETV    A=8 B=1 C=7 D=263 
00219 [L2394] IST      A=0 B=0 C=8 D=8 
00220 [L2394] JMP      A=8 B=128 C=2 D=32770 target=223
00221 [L2395] TNEW     A=8 B=0 C=0 D=0 
00222 [L2395] TSETV    A=8 B=1 C=7 D=263 
00223 [L2398] TGETV    A=8 B=1 C=7 D=263 
00224 [L2399] TGETB    A=9 B=6 C=2 D=1538 
00225 [L2399] TSETS    A=9 B=8 C=6 D=2054 'name'
00226 [L2400] TGETB    A=9 B=6 C=3 D=1539 
00227 [L2400] TSETS    A=9 B=8 C=7 D=2055 'description'
00228 [L2401] TGETB    A=9 B=6 C=4 D=1540 
00229 [L2401] TSETS    A=9 B=8 C=8 D=2056 'introduction'
00230 [L2402] TGETB    A=9 B=6 C=5 D=1541 
00231 [L2402] IST      A=0 B=0 C=9 D=9 
00232 [L2402] JMP      A=10 B=128 C=1 D=32769 target=234
00233 [L2402] KSTR     A=9 B=0 C=11 D=11 ''
00234 [L2402] TSETS    A=9 B=8 C=10 D=2058 'product_desc'
00235 [L2392] ITERN    A=5 B=3 C=3 D=771 
00236 [L2392] ITERL    A=5 B=127 C=234 D=32746 target=215
00237 [L2405] GGET     A=2 B=0 C=1 D=1 'd_ms'
00238 [L2405] TGETS    A=2 B=2 C=2 D=514 'd_csv'
00239 [L2405] TGETS    A=2 B=2 C=3 D=515 'open'
00240 [L2405] KSTR     A=3 B=0 C=44 D=44 'csv_config/skill_base.csv'
00241 [L2405] CALL     A=2 B=2 C=2 D=514 
00242 [L2406] TNEW     A=3 B=0 C=0 D=0 
00243 [L2406] GSET     A=3 B=0 C=42 D=42 'g_itemSkillTable'
00244 [L2407] GGET     A=3 B=0 C=42 D=42 'g_itemSkillTable'
00245 [L2409] UGET     A=4 B=0 C=0 D=0 pairs
00246 [L2409] TGETS    A=5 B=2 C=5 D=517 'records'
00247 [L2409] CALL     A=4 B=4 C=2 D=1026 
00248 [L2409] ISNEXT   A=7 B=128 C=86 D=32854 target=335
00249 [L2410] UGET     A=9 B=0 C=1 D=1 tonumber
00250 [L2410] TGETB    A=10 B=8 C=1 D=2049 
00251 [L2410] CALL     A=9 B=2 C=2 D=514 
00252 [L2411] TGETV    A=10 B=3 C=9 D=777 
00253 [L2411] IST      A=0 B=0 C=10 D=10 
00254 [L2411] JMP      A=10 B=128 C=2 D=32770 target=257
00255 [L2412] TNEW     A=10 B=0 C=0 D=0 
00256 [L2412] TSETV    A=10 B=3 C=9 D=777 
00257 [L2415] TGETV    A=10 B=3 C=9 D=777 
00258 [L2417] TGETV    A=11 B=1 C=9 D=265 
00259 [L2417] TGETS    A=11 B=11 C=6 D=2822 'name'
00260 [L2417] TSETS    A=11 B=10 C=6 D=2566 'name'
00261 [L2418] TGETB    A=11 B=8 C=2 D=2050 
00262 [L2418] TSETS    A=11 B=10 C=13 D=2573 'file'
00263 [L2419] UGET     A=11 B=0 C=1 D=1 tonumber
00264 [L2419] TGETB    A=12 B=8 C=3 D=2051 
00265 [L2419] CALL     A=11 B=2 C=2 D=514 
00266 [L2419] TSETS    A=11 B=10 C=14 D=2574 'quality'
00267 [L2420] UGET     A=11 B=0 C=1 D=1 tonumber
00268 [L2420] TGETB    A=12 B=8 C=4 D=2052 
00269 [L2420] CALL     A=11 B=2 C=2 D=514 
00270 [L2420] TSETS    A=11 B=10 C=45 D=2605 'formula_id'
00271 [L2421] UGET     A=11 B=0 C=1 D=1 tonumber
00272 [L2421] TGETB    A=12 B=8 C=5 D=2053 
00273 [L2421] CALL     A=11 B=2 C=2 D=514 
00274 [L2421] TSETS    A=11 B=10 C=46 D=2606 'formula_id_ext'
00275 [L2422] UGET     A=11 B=0 C=1 D=1 tonumber
00276 [L2422] TGETB    A=12 B=8 C=6 D=2054 
00277 [L2422] CALL     A=11 B=2 C=2 D=514 
00278 [L2422] TSETS    A=11 B=10 C=47 D=2607 'skillType'
00279 [L2423] UGET     A=11 B=0 C=1 D=1 tonumber
00280 [L2423] TGETB    A=12 B=8 C=7 D=2055 
00281 [L2423] CALL     A=11 B=2 C=2 D=514 
00282 [L2423] TSETS    A=11 B=10 C=48 D=2608 'attackType'
00283 [L2424] UGET     A=11 B=0 C=1 D=1 tonumber
00284 [L2424] TGETB    A=12 B=8 C=8 D=2056 
00285 [L2424] CALL     A=11 B=2 C=2 D=514 
00286 [L2424] TSETS    A=11 B=10 C=20 D=2580 'effectField'
00287 [L2425] UGET     A=11 B=0 C=1 D=1 tonumber
00288 [L2425] TGETB    A=12 B=8 C=9 D=2057 
00289 [L2425] CALL     A=11 B=2 C=2 D=514 
00290 [L2425] TSETS    A=11 B=10 C=21 D=2581 'base_gongji_plus'
00291 [L2426] UGET     A=11 B=0 C=1 D=1 tonumber
00292 [L2426] TGETB    A=12 B=8 C=10 D=2058 
00293 [L2426] CALL     A=11 B=2 C=2 D=514 
00294 [L2426] TSETS    A=11 B=10 C=22 D=2582 'base_fangyu_plus'
00295 [L2427] UGET     A=11 B=0 C=1 D=1 tonumber
00296 [L2427] TGETB    A=12 B=8 C=11 D=2059 
00297 [L2427] CALL     A=11 B=2 C=2 D=514 
00298 [L2427] TSETS    A=11 B=10 C=49 D=2609 'base_maxmagic_plus'
00299 [L2428] UGET     A=11 B=0 C=1 D=1 tonumber
00300 [L2428] TGETB    A=12 B=8 C=12 D=2060 
00301 [L2428] CALL     A=11 B=2 C=2 D=514 
00302 [L2428] TSETS    A=11 B=10 C=50 D=2610 'base_intensity'
00303 [L2429] UGET     A=11 B=0 C=1 D=1 tonumber
00304 [L2429] TGETB    A=12 B=8 C=13 D=2061 
00305 [L2429] CALL     A=11 B=2 C=2 D=514 
00306 [L2429] TSETS    A=11 B=10 C=51 D=2611 'hp_plus'
00307 [L2430] UGET     A=11 B=0 C=1 D=1 tonumber
00308 [L2430] TGETB    A=12 B=8 C=14 D=2062 
00309 [L2430] CALL     A=11 B=2 C=2 D=514 
00310 [L2430] TSETS    A=11 B=10 C=29 D=2589 'effect_plus'
00311 [L2431] UGET     A=11 B=0 C=1 D=1 tonumber
00312 [L2431] TGETB    A=12 B=8 C=15 D=2063 
00313 [L2431] CALL     A=11 B=2 C=2 D=514 
00314 [L2431] TSETS    A=11 B=10 C=52 D=2612 'startLevel'
00315 [L2432] UGET     A=11 B=0 C=1 D=1 tonumber
00316 [L2432] TGETB    A=12 B=8 C=16 D=2064 
00317 [L2432] CALL     A=11 B=2 C=2 D=514 
00318 [L2432] TSETS    A=11 B=10 C=53 D=2613 'highestLevel'
00319 [L2433] UGET     A=11 B=0 C=1 D=1 tonumber
00320 [L2433] TGETB    A=12 B=8 C=17 D=2065 
00321 [L2433] CALL     A=11 B=2 C=2 D=514 
00322 [L2433] TSETS    A=11 B=10 C=54 D=2614 'procRate'
00323 [L2434] TGETV    A=11 B=1 C=9 D=265 
00324 [L2434] TGETS    A=11 B=11 C=7 D=2823 'description'
00325 [L2434] TSETS    A=11 B=10 C=7 D=2567 'description'
00326 [L2435] TGETV    A=11 B=1 C=9 D=265 
00327 [L2435] TGETS    A=11 B=11 C=8 D=2824 'introduction'
00328 [L2435] TSETS    A=11 B=10 C=8 D=2568 'introduction'
00329 [L2436] TGETV    A=11 B=1 C=9 D=265 
00330 [L2436] TGETS    A=11 B=11 C=10 D=2826 'product_desc'
00331 [L2436] TSETS    A=11 B=10 C=10 D=2570 'product_desc'
00332 [L2443] GGET     A=11 B=0 C=40 D=40 'packageTagDef'
00333 [L2443] TGETS    A=11 B=11 C=55 D=2871 'skill'
00334 [L2443] TSETS    A=11 B=10 C=39 D=2599 'packageTag'
00335 [L2409] ITERN    A=7 B=3 C=3 D=771 
00336 [L2409] ITERL    A=7 B=127 C=168 D=32680 target=249
00337 [L2446] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto64 offset=0xfb98 source_lines=2455-2486 params=0
UPVALUES ['pairs', 'tonumber', 'string']
00001 [L2456] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L2456] TGETS    A=0 B=0 C=1 D=1 'd_csv'
00003 [L2456] TGETS    A=0 B=0 C=2 D=2 'open2'
00004 [L2456] KSTR     A=1 B=0 C=3 D=3 'csv_config/ext_skill.csv'
00005 [L2456] CALL     A=0 B=2 C=2 D=514 
00006 [L2457] TNEW     A=1 B=0 C=0 D=0 
00007 [L2457] GSET     A=1 B=0 C=4 D=4 'g_ext_skill_desc'
00008 [L2458] UGET     A=1 B=0 C=0 D=0 pairs
00009 [L2458] MOV      A=2 B=0 C=0 D=0 
00010 [L2458] CALL     A=1 B=4 C=2 D=1026 
00011 [L2458] ISNEXT   A=4 B=128 C=83 D=32851 target=95
00012 [L2459] TGETS    A=6 B=5 C=5 D=1285 'id'
00013 [L2459] LEN      A=6 B=0 C=6 D=6 
00014 [L2459] KSHORT   A=7 B=0 C=0 D=0 0
00015 [L2459] ISGE     A=7 B=0 C=6 D=6 
00016 [L2459] JMP      A=6 B=128 C=78 D=32846 target=95
00017 [L2460] UGET     A=6 B=0 C=1 D=1 tonumber
00018 [L2460] TGETS    A=7 B=5 C=5 D=1285 'id'
00019 [L2460] CALL     A=6 B=2 C=2 D=514 
00020 [L2461] KSHORT   A=7 B=0 C=5 D=5 5
00021 [L2462] GGET     A=8 B=0 C=0 D=0 'd_ms'
00022 [L2462] TGETS    A=8 B=8 C=6 D=2054 'd_jpmkUI'
00023 [L2462] TGETS    A=8 B=8 C=7 D=2055 'MAX_LV'
00024 [L2463] TNEW     A=9 B=0 C=0 D=0 
00025 [L2464] KSHORT   A=10 B=0 C=1 D=1 1
00026 [L2464] MOV      A=11 B=0 C=7 D=7 
00027 [L2464] KSHORT   A=12 B=0 C=1 D=1 1
00028 [L2464] FORI     A=10 B=128 C=3 D=32771 target=32
00029 [L2465] TNEW     A=14 B=0 C=0 D=0 
00030 [L2465] TSETV    A=14 B=9 C=13 D=2317 
00031 [L2464] FORL     A=10 B=127 C=253 D=32765 target=29
00032 [L2467] GGET     A=10 B=0 C=0 D=0 'd_ms'
00033 [L2467] TGETS    A=10 B=10 C=8 D=2568 'd_str'
00034 [L2467] TGETS    A=10 B=10 C=9 D=2569 'split'
00035 [L2467] TGETS    A=11 B=5 C=10 D=1290 'parameter'
00036 [L2467] KSTR     A=12 B=0 C=11 D=11 '/'
00037 [L2467] CALL     A=10 B=2 C=3 D=515 
00038 [L2468] KSHORT   A=11 B=0 C=1 D=1 1
00039 [L2468] LEN      A=12 B=0 C=10 D=10 
00040 [L2468] KSHORT   A=13 B=0 C=1 D=1 1
00041 [L2468] FORI     A=11 B=128 C=15 D=32783 target=57
00042 [L2469] GGET     A=15 B=0 C=0 D=0 'd_ms'
00043 [L2469] TGETS    A=15 B=15 C=8 D=3848 'd_str'
00044 [L2469] TGETS    A=15 B=15 C=9 D=3849 'split'
00045 [L2469] TGETV    A=16 B=10 C=14 D=2574 
00046 [L2469] KSTR     A=17 B=0 C=12 D=12 '|'
00047 [L2469] CALL     A=15 B=2 C=3 D=515 
00048 [L2470] KSHORT   A=16 B=0 C=1 D=1 1
00049 [L2470] LEN      A=17 B=0 C=15 D=15 
00050 [L2470] KSHORT   A=18 B=0 C=1 D=1 1
00051 [L2470] FORI     A=16 B=128 C=4 D=32772 target=56
00052 [L2471] TGETV    A=20 B=9 C=14 D=2318 
00053 [L2471] TGETV    A=21 B=15 C=19 D=3859 
00054 [L2471] TSETV    A=21 B=20 C=19 D=5139 
00055 [L2470] FORL     A=16 B=127 C=252 D=32764 target=52
00056 [L2468] FORL     A=11 B=127 C=241 D=32753 target=42
00057 [L2475] TNEW     A=11 B=0 C=0 D=0 
00058 [L2476] KSHORT   A=12 B=0 C=1 D=1 1
00059 [L2476] MOV      A=13 B=0 C=8 D=8 
00060 [L2476] KSHORT   A=14 B=0 C=1 D=1 1
00061 [L2476] FORI     A=12 B=128 C=31 D=32799 target=93
00062 [L2477] UGET     A=16 B=0 C=2 D=2 string
00063 [L2477] TGETS    A=16 B=16 C=13 D=4109 'format'
00064 [L2477] TGETS    A=17 B=5 C=14 D=1294 'introduction'
00065 [L2477] TGETB    A=18 B=9 C=1 D=2305 
00066 [L2477] TGETV    A=18 B=18 C=15 D=4623 
00067 [L2477] IST      A=0 B=0 C=18 D=18 
00068 [L2477] JMP      A=19 B=128 C=1 D=32769 target=70
00069 [L2477] KSTR     A=18 B=0 C=15 D=15 ''
00070 [L2478] TGETB    A=19 B=9 C=2 D=2306 
00071 [L2478] TGETV    A=19 B=19 C=15 D=4879 
00072 [L2478] IST      A=0 B=0 C=19 D=19 
00073 [L2478] JMP      A=20 B=128 C=1 D=32769 target=75
00074 [L2478] KSTR     A=19 B=0 C=15 D=15 ''
00075 [L2479] TGETB    A=20 B=9 C=3 D=2307 
00076 [L2479] TGETV    A=20 B=20 C=15 D=5135 
00077 [L2479] IST      A=0 B=0 C=20 D=20 
00078 [L2479] JMP      A=21 B=128 C=1 D=32769 target=80
00079 [L2479] KSTR     A=20 B=0 C=15 D=15 ''
00080 [L2480] TGETB    A=21 B=9 C=4 D=2308 
00081 [L2480] TGETV    A=21 B=21 C=15 D=5391 
00082 [L2480] IST      A=0 B=0 C=21 D=21 
00083 [L2480] JMP      A=22 B=128 C=1 D=32769 target=85
00084 [L2480] KSTR     A=21 B=0 C=15 D=15 ''
00085 [L2481] TGETB    A=22 B=9 C=5 D=2309 
00086 [L2481] TGETV    A=22 B=22 C=15 D=5647 
00087 [L2481] IST      A=0 B=0 C=22 D=22 
00088 [L2481] JMP      A=23 B=128 C=1 D=32769 target=90
00089 [L2481] KSTR     A=22 B=0 C=15 D=15 ''
00090 [L2477] CALL     A=16 B=2 C=7 D=519 
00091 [L2481] TSETV    A=16 B=11 C=15 D=2831 
00092 [L2476] FORL     A=12 B=127 C=225 D=32737 target=62
00093 [L2483] GGET     A=12 B=0 C=4 D=4 'g_ext_skill_desc'
00094 [L2483] TSETV    A=11 B=12 C=6 D=3078 
00095 [L2458] ITERN    A=4 B=3 C=3 D=771 
00096 [L2458] ITERL    A=4 B=127 C=171 D=32683 target=12
00097 [L2486] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto65 offset=0xfeb9 source_lines=2490-2496 params=1
UPVALUES []
00001 [L2491] GGET     A=1 B=0 C=0 D=0 'g_ext_skill_desc'
00002 [L2491] IST      A=0 B=0 C=1 D=1 
00003 [L2491] JMP      A=1 B=128 C=2 D=32770 target=6
00004 [L2492] GGET     A=1 B=0 C=1 D=1 'initExtSkillDesc'
00005 [L2492] CALL     A=1 B=1 C=1 D=257 
00006 [L2495] GGET     A=1 B=0 C=0 D=0 'g_ext_skill_desc'
00007 [L2495] TGETV    A=1 B=1 C=0 D=256 
00008 [L2495] IST      A=0 B=0 C=1 D=1 
00009 [L2495] JMP      A=2 B=128 C=1 D=32769 target=11
00010 [L2495] TNEW     A=1 B=0 C=0 D=0 
00011 [L2495] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto66 offset=0xff25 source_lines=2498-2505 params=1
UPVALUES ['pairs']
00001 [L2499] UGET     A=1 B=0 C=0 D=0 pairs
00002 [L2499] GGET     A=2 B=0 C=0 D=0 'g_packageItemsInfo'
00003 [L2499] CALL     A=1 B=4 C=2 D=1026 
00004 [L2499] ISNEXT   A=4 B=128 C=4 D=32772 target=9
00005 [L2500] TGETS    A=6 B=5 C=1 D=1281 'type_id'
00006 [L2500] ISNEV    A=6 B=0 C=0 D=0 
00007 [L2500] JMP      A=6 B=128 C=1 D=32769 target=9
00008 [L2501] RET1     A=5 B=0 C=2 D=2 
00009 [L2499] ITERN    A=4 B=3 C=3 D=771 
00010 [L2499] ITERL    A=4 B=127 C=250 D=32762 target=5
00011 [L2504] KPRI     A=1 B=0 C=0 D=0 
00012 [L2504] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto67 offset=0xffad source_lines=0-2507 params=0
UPVALUES []
00001 [L2] GGET     A=0 B=0 C=0 D=0 'require'
00002 [L3] GGET     A=1 B=0 C=1 D=1 'bits'
00003 [L4] GGET     A=2 B=0 C=2 D=2 'sqlite'
00004 [L5] GGET     A=3 B=0 C=3 D=3 'type'
00005 [L6] GGET     A=4 B=0 C=4 D=4 'print'
00006 [L7] GGET     A=5 B=0 C=5 D=5 'tostring'
00007 [L8] GGET     A=6 B=0 C=6 D=6 'pairs'
00008 [L9] GGET     A=7 B=0 C=7 D=7 'string'
00009 [L10] GGET     A=8 B=0 C=8 D=8 'table'
00010 [L11] GGET     A=9 B=0 C=9 D=9 'math'
00011 [L12] GGET     A=10 B=0 C=10 D=10 'package'
00012 [L14] GGET     A=11 B=0 C=11 D=11 'main_server'
00013 [L15] GGET     A=12 B=0 C=12 D=12 '_G'
00014 [L16] MOV      A=13 B=0 C=1 D=1 
00015 [L17] GGET     A=14 B=0 C=13 D=13 'tonumber'
00016 [L18] GGET     A=15 B=0 C=14 D=14 'os'
00017 [L19] GGET     A=16 B=0 C=15 D=15 'io'
00018 [L20] GGET     A=17 B=0 C=16 D=16 'tolua'
00019 [L25] GGET     A=18 B=0 C=17 D=17 'class'
00020 [L26] GGET     A=19 B=0 C=18 D=18 'CCArray'
00021 [L27] GGET     A=20 B=0 C=19 D=19 'CCDirector'
00022 [L28] GGET     A=21 B=0 C=20 D=20 'CCLayer'
00023 [L29] GGET     A=22 B=0 C=21 D=21 'CCMenu'
00024 [L30] GGET     A=23 B=0 C=22 D=22 'CCMenuItemImage'
00025 [L31] GGET     A=24 B=0 C=23 D=23 'CCSprite'
00026 [L32] GGET     A=25 B=0 C=24 D=24 'CCScene'
00027 [L33] GGET     A=26 B=0 C=25 D=25 'CCTextFieldTTF'
00028 [L34] GGET     A=27 B=0 C=26 D=26 'CCTOUCHBEGAN'
00029 [L35] GGET     A=28 B=0 C=27 D=27 'CCTOUCHMOVED'
00030 [L36] GGET     A=29 B=0 C=28 D=28 'CCLayerColor'
00031 [L37] GGET     A=30 B=0 C=29 D=29 'ccc4'
00032 [L38] GGET     A=31 B=0 C=30 D=30 'ccc3'
00033 [L39] GGET     A=32 B=0 C=31 D=31 'CCMenuItemSprite'
00034 [L40] MOV      A=33 B=0 C=23 D=23 
00035 [L41] GGET     A=34 B=0 C=32 D=32 'CCRectMake'
00036 [L42] GGET     A=35 B=0 C=33 D=33 'CCPointMake'
00037 [L43] GGET     A=36 B=0 C=34 D=34 'ccpAdd'
00038 [L44] GGET     A=37 B=0 C=35 D=35 'CCMoveBy'
00039 [L45] GGET     A=38 B=0 C=36 D=36 'CCMenuItemFont'
00040 [L46] GGET     A=39 B=0 C=37 D=37 'kCCMenuHandlerPriority'
00041 [L47] GGET     A=40 B=0 C=38 D=38 'CCSequence'
00042 [L48] GGET     A=41 B=0 C=39 D=39 'CCCallFuncN'
00043 [L49] GGET     A=42 B=0 C=40 D=40 'CCDelayTime'
00044 [L50] GGET     A=43 B=0 C=41 D=41 'CCEaseOut'
00045 [L51] GGET     A=44 B=0 C=42 D=42 'CCSpawn'
00046 [L52] GGET     A=45 B=0 C=43 D=43 'CCEaseInOut'
00047 [L53] GGET     A=46 B=0 C=44 D=44 'CCEaseElasticInOut'
00048 [L54] GGET     A=47 B=0 C=45 D=45 'CCLuaLog'
00049 [L55] GGET     A=48 B=0 C=46 D=46 'CCFileUtils'
00050 [L56] GGET     A=49 B=0 C=47 D=47 'CCVerticalTextAlignment'
00051 [L57] GGET     A=50 B=0 C=48 D=48 'CCMoveTo'
00052 [L58] GGET     A=51 B=0 C=49 D=49 'CCEaseElasticOut'
00053 [L59] GGET     A=52 B=0 C=50 D=50 'CCEaseElastic'
00054 [L60] GGET     A=53 B=0 C=51 D=51 'CCEaseBounce'
00055 [L61] GGET     A=54 B=0 C=52 D=52 'CCEaseBounceInOut'
00056 [L62] GGET     A=55 B=0 C=53 D=53 'CCEaseBounceOut'
00057 [L63] GGET     A=56 B=0 C=54 D=54 'CCEaseBackInOut'
00058 [L64] GGET     A=57 B=0 C=55 D=55 'CCSizeMake'
00059 [L65] GGET     A=58 B=0 C=56 D=56 'CCScrollView'
00060 [L66] GGET     A=59 B=0 C=57 D=57 'CCTargetedAction'
00061 [L67] GGET     A=60 B=0 C=58 D=58 'CCNode'
00062 [L68] GGET     A=61 B=0 C=59 D=59 'CCLabelTTF'
00063 [L69] GGET     A=62 B=0 C=60 D=60 'kCCTextAlignmentLeft'
00064 [L70] GGET     A=63 B=0 C=61 D=61 'CCFadeOut'
00065 [L71] GGET     A=64 B=0 C=62 D=62 'ccp'
00066 [L76] GGET     A=65 B=0 C=63 D=63 'module'
00067 [L76] KSTR     A=66 B=0 C=64 D=64 'ui.packageUI'
00068 [L76] CALL     A=65 B=1 C=2 D=258 
00069 [L79] MOV      A=65 B=0 C=0 D=0 
00070 [L79] KSTR     A=66 B=0 C=65 D=65 'ms'
00071 [L79] CALL     A=65 B=2 C=2 D=514 
00072 [L79] GSET     A=65 B=0 C=66 D=66 'd_ms'
00073 [L80] GGET     A=65 B=0 C=66 D=66 'd_ms'
00074 [L80] IST      A=0 B=0 C=65 D=65 
00075 [L80] JMP      A=65 B=128 C=3 D=32771 target=79
00076 [L81] MOV      A=65 B=0 C=4 D=4 
00077 [L81] KSTR     A=66 B=0 C=67 D=67 'packageUI load d_ms fail.\n'
00078 [L81] CALL     A=65 B=1 C=2 D=258 
00079 [L88] FNEW     A=65 B=0 C=68 D=68 {'kind': 'proto', 'id': 0}
00080 [L92] MOV      A=67 B=0 C=20 D=20 
00081 [L92] TGETS    A=66 B=20 C=69 D=5189 'sharedDirector'
00082 [L92] CALL     A=66 B=2 C=2 D=514 
00083 [L92] MOV      A=67 B=0 C=66 D=66 
00084 [L92] TGETS    A=66 B=66 C=70 D=16966 'getVisibleSize'
00085 [L92] CALL     A=66 B=2 C=2 D=514 
00086 [L94] GGET     A=67 B=0 C=66 D=66 'd_ms'
00087 [L94] TGETS    A=67 B=67 C=71 D=17223 'd_common_def'
00088 [L94] TGETS    A=67 B=67 C=72 D=17224 'object_type'
00089 [L97] GGET     A=68 B=0 C=66 D=66 'd_ms'
00090 [L97] TGETS    A=68 B=68 C=71 D=17479 'd_common_def'
00091 [L97] TGETS    A=68 B=68 C=73 D=17481 'item_main_type'
00092 [L98] GGET     A=69 B=0 C=66 D=66 'd_ms'
00093 [L98] TGETS    A=69 B=69 C=74 D=17738 'd_hz'
00094 [L98] TGETS    A=69 B=69 C=75 D=17739 'gethz'
00095 [L100] TNEW     A=70 B=0 C=0 D=0 
00096 [L100] GSET     A=70 B=0 C=76 D=76 'g_packageUI'
00097 [L102] TNEW     A=70 B=0 C=9 D=9 
00098 [L102] TNEW     A=71 B=0 C=0 D=0 
00099 [L102] TSETB    A=71 B=70 C=1 D=17921 
00100 [L102] TNEW     A=71 B=0 C=0 D=0 
00101 [L102] TSETB    A=71 B=70 C=2 D=17922 
00102 [L102] TNEW     A=71 B=0 C=0 D=0 
00103 [L102] TSETB    A=71 B=70 C=3 D=17923 
00104 [L102] TNEW     A=71 B=0 C=0 D=0 
00105 [L102] TSETB    A=71 B=70 C=4 D=17924 
00106 [L102] TNEW     A=71 B=0 C=0 D=0 
00107 [L102] TSETB    A=71 B=70 C=5 D=17925 
00108 [L102] TNEW     A=71 B=0 C=0 D=0 
00109 [L102] TSETB    A=71 B=70 C=6 D=17926 
00110 [L102] TNEW     A=71 B=0 C=0 D=0 
00111 [L102] TSETB    A=71 B=70 C=7 D=17927 
00112 [L102] TNEW     A=71 B=0 C=0 D=0 
00113 [L102] TSETB    A=71 B=70 C=8 D=17928 
00114 [L102] GSET     A=70 B=0 C=77 D=77 'g_usedItems'
00115 [L104] TNEW     A=70 B=0 C=17 D=17 
00116 [L104] TNEW     A=71 B=0 C=0 D=0 
00117 [L104] TSETB    A=71 B=70 C=1 D=17921 
00118 [L104] TNEW     A=71 B=0 C=0 D=0 
00119 [L104] TSETB    A=71 B=70 C=2 D=17922 
00120 [L104] TNEW     A=71 B=0 C=0 D=0 
00121 [L104] TSETB    A=71 B=70 C=3 D=17923 
00122 [L104] TNEW     A=71 B=0 C=0 D=0 
00123 [L104] TSETB    A=71 B=70 C=4 D=17924 
00124 [L104] TNEW     A=71 B=0 C=0 D=0 
00125 [L104] TSETB    A=71 B=70 C=5 D=17925 
00126 [L104] TNEW     A=71 B=0 C=0 D=0 
00127 [L104] TSETB    A=71 B=70 C=6 D=17926 
00128 [L104] TNEW     A=71 B=0 C=0 D=0 
00129 [L104] TSETB    A=71 B=70 C=7 D=17927 
00130 [L104] TNEW     A=71 B=0 C=0 D=0 
00131 [L104] TSETB    A=71 B=70 C=8 D=17928 
00132 [L105] TNEW     A=71 B=0 C=0 D=0 
00133 [L105] TSETB    A=71 B=70 C=9 D=17929 
00134 [L105] TNEW     A=71 B=0 C=0 D=0 
00135 [L105] TSETB    A=71 B=70 C=10 D=17930 
00136 [L105] TNEW     A=71 B=0 C=0 D=0 
00137 [L105] TSETB    A=71 B=70 C=11 D=17931 
00138 [L105] TNEW     A=71 B=0 C=0 D=0 
00139 [L105] TSETB    A=71 B=70 C=12 D=17932 
00140 [L105] TNEW     A=71 B=0 C=0 D=0 
00141 [L105] TSETB    A=71 B=70 C=13 D=17933 
00142 [L105] TNEW     A=71 B=0 C=0 D=0 
00143 [L105] TSETB    A=71 B=70 C=14 D=17934 
00144 [L105] TNEW     A=71 B=0 C=0 D=0 
00145 [L105] TSETB    A=71 B=70 C=15 D=17935 
00146 [L105] TNEW     A=71 B=0 C=0 D=0 
00147 [L105] TSETB    A=71 B=70 C=16 D=17936 
00148 [L105] GSET     A=70 B=0 C=78 D=78 'g_cheer_items'
00149 [L106] KPRI     A=70 B=0 C=0 D=0 
00150 [L106] GSET     A=70 B=0 C=79 D=79 'g_itemAttrTable'
00151 [L107] KPRI     A=70 B=0 C=0 D=0 
00152 [L107] GSET     A=70 B=0 C=80 D=80 'g_itemSkillTable'
00153 [L108] TNEW     A=70 B=0 C=0 D=0 
00154 [L108] GSET     A=70 B=0 C=81 D=81 'g_itemButton'
00155 [L109] KSHORT   A=70 B=0 C=0 D=0 0
00156 [L109] GSET     A=70 B=0 C=82 D=82 'g_lastSelectedItemButton'
00157 [L112] TDUP     A=70 B=0 C=83 D=83 {'kind': 'table', 'value': {'enhanceSkill': 5, 'advance': 8, 'asc': 10, 'cast': 11, 'stoneUpgrade': 6, 'close': -1, 'enhance': 4, 'none': 0, 'slot': 7, 'sale': 2, 'handbook': 9, 'choose': 3, 'change': 1}}
00158 [L112] GSET     A=70 B=0 C=84 D=84 'g_introButtonType'
00159 [L115] KPRI     A=70 B=0 C=0 D=0 
00160 [L115] GSET     A=70 B=0 C=85 D=85 'g_packageItemsInfo'
00161 [L118] TNEW     A=70 B=8 C=0 D=2048 
00162 [L119] TGETS    A=71 B=67 C=86 D=17238 'item'
00163 [L119] TNEW     A=72 B=0 C=0 D=0 
00164 [L119] TSETV    A=72 B=70 C=71 D=17991 
00165 [L120] TGETS    A=71 B=67 C=87 D=17239 'skill'
00166 [L120] TNEW     A=72 B=0 C=0 D=0 
00167 [L120] TSETV    A=72 B=70 C=71 D=17991 
00168 [L121] GSET     A=70 B=0 C=88 D=88 'g_reorgItemsInfo'
00169 [L124] TNEW     A=70 B=0 C=0 D=0 
00170 [L124] GSET     A=70 B=0 C=89 D=89 'g_propsTable'
00171 [L126] TDUP     A=70 B=0 C=90 D=90 {'kind': 'table', 'value': {'weapon': 1, 'stone': 5, 'props': 6, 'cortege': 7, 'fabao': 3, 'invisible': 8, 'none': 0, 'armor': 2, 'skill': 4}}
00172 [L136] GSET     A=70 B=0 C=91 D=91 'packageTagDef'
00173 [L138] TDUP     A=70 B=0 C=92 D=92 {'kind': 'table', 'value': {'packageLayerTag': 300008, 'cellsLayer': 3}}
00174 [L141] GSET     A=70 B=0 C=93 D=93 'tagDef'
00175 [L144] KPRI     A=70 B=0 C=1 D=1 
00176 [L144] GSET     A=70 B=0 C=94 D=94 'g_isPackageSorted'
00177 [L148] TNEW     A=70 B=0 C=0 D=0 
00178 [L148] GSET     A=70 B=0 C=95 D=95 'g_updatePackageFunc'
00179 [L150] KPRI     A=70 B=0 C=1 D=1 
00180 [L150] GSET     A=70 B=0 C=96 D=96 'g_isInPackage'
00181 [L153] TNEW     A=70 B=0 C=0 D=0 
00182 [L153] GSET     A=70 B=0 C=97 D=97 'g_lastRequestUsedItem'
00183 [L155] TDUP     A=70 B=0 C=99 D=99 {'kind': 'table', 'value': {}}
00184 [L156] TDUP     A=71 B=0 C=98 D=98 {'kind': 'table', 'value': {1: 0, 2: 0, 3: 0}}
00185 [L156] TSETS    A=71 B=70 C=100 D=18020 'black'
00186 [L157] TDUP     A=71 B=0 C=101 D=101 {'kind': 'table', 'value': {1: 255, 2: 255, 3: 255}}
00187 [L157] TSETS    A=71 B=70 C=102 D=18022 'white'
00188 [L158] TDUP     A=71 B=0 C=103 D=103 {'kind': 'table', 'value': {1: 0, 2: 255, 3: 0}}
00189 [L158] TSETS    A=71 B=70 C=104 D=18024 'green'
00190 [L159] TDUP     A=71 B=0 C=105 D=105 {'kind': 'table', 'value': {1: 255, 2: 0, 3: 0}}
00191 [L159] TSETS    A=71 B=70 C=106 D=18026 'red'
00192 [L160] TDUP     A=71 B=0 C=107 D=107 {'kind': 'table', 'value': {1: 255, 2: 255, 3: 0}}
00193 [L160] TSETS    A=71 B=70 C=108 D=18028 'yellow'
00194 [L161] TDUP     A=71 B=0 C=109 D=109 {'kind': 'table', 'value': {1: 230, 2: 230, 3: 230}}
00195 [L161] TSETS    A=71 B=70 C=110 D=18030 'gray'
00196 [L162] GSET     A=70 B=0 C=111 D=111 'g_Color'
00197 [L185] FNEW     A=70 B=0 C=112 D=112 {'kind': 'proto', 'id': 1}
00198 [L165] GSET     A=70 B=0 C=113 D=113 'show'
00199 [L259] FNEW     A=70 B=0 C=114 D=114 {'kind': 'proto', 'id': 3}
00200 [L188] GSET     A=70 B=0 C=115 D=115 'create'
00201 [L264] FNEW     A=70 B=0 C=116 D=116 {'kind': 'proto', 'id': 4}
00202 [L261] GSET     A=70 B=0 C=117 D=117 'pressSmith'
00203 [L270] FNEW     A=70 B=0 C=118 D=118 {'kind': 'proto', 'id': 5}
00204 [L267] GSET     A=70 B=0 C=119 D=119 'pressHandBook'
00205 [L272] TDUP     A=70 B=0 C=120 D=120 {'kind': 'table', 'value': {1: 1001, 2: 1006, 3: 1007, 4: 1024, 5: 1008, 6: 1009, 7: 1010, 8: 1035, 9: 1011, 10: 1012, 11: 1013, 12: 1004, 13: 1026, 14: 1027, 15: 1028, 16: 1015, 17: 1030, 18: 1315, 19: 1016, 20: 1017, 21: 1219, 22: 1332, 23: 1336, 24: 1329, 25: 1334, 26: 1335, 27: 1337, 28: 1333, 29: 10000, 30: 1343, 37: 1807, 38: 1140, 39: 1366, 40: 10300, 41: 1345}}
00206 [L276] TDUP     A=71 B=0 C=121 D=121 {'kind': 'table', 'value': {1: 1310, 2: 1314}}
00207 [L277] TSETB    A=71 B=70 C=31 D=17951 
00208 [L277] TDUP     A=71 B=0 C=122 D=122 {'kind': 'table', 'value': {1: 1320, 2: 1323}}
00209 [L278] TSETB    A=71 B=70 C=32 D=17952 
00210 [L278] TDUP     A=71 B=0 C=123 D=123 {'kind': 'table', 'value': {1: 1208, 2: 1212}}
00211 [L279] TSETB    A=71 B=70 C=33 D=17953 
00212 [L279] TDUP     A=71 B=0 C=124 D=124 {'kind': 'table', 'value': {1: 1113, 2: 1117}}
00213 [L280] TSETB    A=71 B=70 C=34 D=17954 
00214 [L280] TDUP     A=71 B=0 C=125 D=125 {'kind': 'table', 'value': {1: 1338, 2: 1341}}
00215 [L281] TSETB    A=71 B=70 C=35 D=17955 
00216 [L281] TDUP     A=71 B=0 C=126 D=126 {'kind': 'table', 'value': {1: 1134, 2: 1138}}
00217 [L282] TSETB    A=71 B=70 C=36 D=17956 
00218 [L287] TDUP     A=71 B=0 C=127 D=127 {'kind': 'table', 'value': {1: 1347, 2: 1349}}
00219 [L287] TSETB    A=71 B=70 C=42 D=17962 
00220 [L287] TDUP     A=71 B=0 C=128 D=128 {'kind': 'table', 'value': {1: 1141, 2: 1143}}
00221 [L288] TSETB    A=71 B=70 C=43 D=17963 
00222 [L288] TDUP     A=71 B=0 C=129 D=129 {'kind': 'table', 'value': {1: 1350, 2: 1356}}
00223 [L289] TSETB    A=71 B=70 C=44 D=17964 
00224 [L289] TDUP     A=71 B=0 C=130 D=130 {'kind': 'table', 'value': {1: 1361, 2: 1362}}
00225 [L290] TSETB    A=71 B=70 C=45 D=17965 
00226 [L290] TDUP     A=71 B=0 C=131 D=131 {'kind': 'table', 'value': {1: 1364, 2: 1365}}
00227 [L291] TSETB    A=71 B=70 C=46 D=17966 
00228 [L304] FNEW     A=71 B=0 C=132 D=132 {'kind': 'proto', 'id': 6}
00229 [L321] FNEW     A=72 B=0 C=133 D=133 {'kind': 'proto', 'id': 7}
00230 [L305] GSET     A=72 B=0 C=134 D=134 'checkEquipmentCanFenjie'
00231 [L528] FNEW     A=72 B=0 C=135 D=135 {'kind': 'proto', 'id': 19}
00232 [L530] TNEW     A=73 B=0 C=0 D=0 
00233 [L539] FNEW     A=74 B=0 C=136 D=136 {'kind': 'proto', 'id': 20}
00234 [L546] FNEW     A=75 B=0 C=137 D=137 {'kind': 'proto', 'id': 21}
00235 [L584] FNEW     A=76 B=0 C=138 D=138 {'kind': 'proto', 'id': 24}
00236 [L586] GGET     A=77 B=0 C=66 D=66 'd_ms'
00237 [L586] TGETS    A=77 B=77 C=139 D=19851 'd_u'
00238 [L586] TGETS    A=77 B=77 C=140 D=19852 'ccSizeMake'
00239 [L586] KNUM     A=78 B=0 C=0 D=0 0.7
00240 [L586] KNUM     A=79 B=0 C=1 D=1 0.1
00241 [L586] CALL     A=77 B=2 C=3 D=515 
00242 [L633] FNEW     A=78 B=0 C=141 D=141 {'kind': 'proto', 'id': 28}
00243 [L654] FNEW     A=79 B=0 C=142 D=142 {'kind': 'proto', 'id': 29}
00244 [L635] GSET     A=79 B=0 C=143 D=143 'ensureFilter'
00245 [L695] FNEW     A=79 B=0 C=144 D=144 {'kind': 'proto', 'id': 30}
00246 [L747] FNEW     A=80 B=0 C=145 D=145 {'kind': 'proto', 'id': 32}
00247 [L698] GSET     A=80 B=0 C=146 D=146 'showPackage'
00248 [L791] FNEW     A=80 B=0 C=147 D=147 {'kind': 'proto', 'id': 33}
00249 [L750] GSET     A=80 B=0 C=148 D=148 'updateItemCellInfo'
00250 [L859] FNEW     A=80 B=0 C=149 D=149 {'kind': 'proto', 'id': 34}
00251 [L811] GSET     A=80 B=0 C=150 D=150 'addNewPropsToPackage'
00252 [L879] FNEW     A=80 B=0 C=151 D=151 {'kind': 'proto', 'id': 35}
00253 [L861] GSET     A=80 B=0 C=152 D=152 'refreshPackage'
00254 [L947] FNEW     A=80 B=0 C=153 D=153 {'kind': 'proto', 'id': 36}
00255 [L882] GSET     A=80 B=0 C=154 D=154 'createSkillLabel'
00256 [L993] FNEW     A=80 B=0 C=155 D=155 {'kind': 'proto', 'id': 37}
00257 [L949] GSET     A=80 B=0 C=156 D=156 'removeItemsFromPackage'
00258 [L1020] FNEW     A=80 B=0 C=157 D=157 {'kind': 'proto', 'id': 39}
00259 [L995] GSET     A=80 B=0 C=158 D=158 'addStarLockInfo'
00260 [L1806] FNEW     A=80 B=0 C=159 D=159 {'kind': 'proto', 'id': 44}
00261 [L1023] GSET     A=80 B=0 C=160 D=160 'createItemIntroLayer'
00262 [L1812] FNEW     A=80 B=0 C=161 D=161 {'kind': 'proto', 'id': 45}
00263 [L1809] GSET     A=80 B=0 C=162 D=162 'useItem'
00264 [L1977] FNEW     A=80 B=0 C=163 D=163 {'kind': 'proto', 'id': 48}
00265 [L1814] GSET     A=80 B=0 C=164 D=164 'requestUseItem'
00266 [L1987] FNEW     A=80 B=0 C=165 D=165 {'kind': 'proto', 'id': 49}
00267 [L1979] GSET     A=80 B=0 C=166 D=166 'getPropIDByTypeId'
00268 [L1992] FNEW     A=80 B=0 C=167 D=167 {'kind': 'proto', 'id': 50}
00269 [L1989] GSET     A=80 B=0 C=168 D=168 'onGetSaleResult'
00270 [L2048] FNEW     A=80 B=0 C=169 D=169 {'kind': 'proto', 'id': 51}
00271 [L1994] GSET     A=80 B=0 C=170 D=170 'getDateFormServer'
00272 [L2074] FNEW     A=80 B=0 C=171 D=171 {'kind': 'proto', 'id': 52}
00273 [L2050] GSET     A=80 B=0 C=172 D=172 'getAllProps'
00274 [L2147] FNEW     A=80 B=0 C=173 D=173 {'kind': 'proto', 'id': 53}
00275 [L2076] GSET     A=80 B=0 C=174 D=174 'sortItems'
00276 [L2154] FNEW     A=80 B=0 C=175 D=175 {'kind': 'proto', 'id': 54}
00277 [L2149] GSET     A=80 B=0 C=176 D=176 'sortProps'
00278 [L2178] FNEW     A=80 B=0 C=177 D=177 {'kind': 'proto', 'id': 55}
00279 [L2156] GSET     A=80 B=0 C=178 D=178 'sortPackage'
00280 [L2192] FNEW     A=80 B=0 C=179 D=179 {'kind': 'proto', 'id': 56}
00281 [L2180] GSET     A=80 B=0 C=180 D=180 'stoneSort'
00282 [L2217] FNEW     A=80 B=0 C=181 D=181 {'kind': 'proto', 'id': 57}
00283 [L2195] GSET     A=80 B=0 C=182 D=182 'packageSortFunc'
00284 [L2248] FNEW     A=80 B=0 C=183 D=183 {'kind': 'proto', 'id': 58}
00285 [L2220] GSET     A=80 B=0 C=184 D=184 'skillSortFunc'
00286 [L2258] FNEW     A=80 B=0 C=185 D=185 {'kind': 'proto', 'id': 59}
00287 [L2251] GSET     A=80 B=0 C=186 D=186 'compareHZ'
00288 [L2269] FNEW     A=80 B=0 C=187 D=187 {'kind': 'proto', 'id': 60}
00289 [L2260] GSET     A=80 B=0 C=188 D=188 'findItemUser'
00290 [L2291] FNEW     A=80 B=0 C=189 D=189 {'kind': 'proto', 'id': 61}
00291 [L2271] GSET     A=80 B=0 C=190 D=190 'getItemLevelPriceCSVConfig'
00292 [L2310] FNEW     A=80 B=0 C=191 D=191 {'kind': 'proto', 'id': 62}
00293 [L2293] GSET     A=80 B=0 C=192 D=192 'getItembasePriceCSVConfig'
00294 [L2446] FNEW     A=80 B=0 C=193 D=193 {'kind': 'proto', 'id': 63}
00295 [L2312] GSET     A=80 B=0 C=194 D=194 'getPackageCSVConfig'
00296 [L2450] KPRI     A=80 B=0 C=0 D=0 
00297 [L2450] GSET     A=80 B=0 C=195 D=195 'g_ext_skill_desc'
00298 [L2486] FNEW     A=80 B=0 C=196 D=196 {'kind': 'proto', 'id': 64}
00299 [L2455] GSET     A=80 B=0 C=197 D=197 'initExtSkillDesc'
00300 [L2496] FNEW     A=80 B=0 C=198 D=198 {'kind': 'proto', 'id': 65}
00301 [L2490] GSET     A=80 B=0 C=199 D=199 'getExtSkillDesc'
00302 [L2505] FNEW     A=80 B=0 C=200 D=200 {'kind': 'proto', 'id': 66}
00303 [L2498] GSET     A=80 B=0 C=201 D=201 'getItemInfoByTypeId'
00304 [L2505] UCLO     A=0 B=128 C=0 D=32768 target=305
00305 [L2505] RET0     A=0 B=0 C=1 D=1 
