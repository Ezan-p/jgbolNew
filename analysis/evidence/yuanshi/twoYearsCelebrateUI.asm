LuaJIT dump version=1; source='@D:\\mg_update_\\lua_cache\\lua1\\d46fac5d3e86cff98adaf18ae1434625.data'; root=proto24

FUNCTION proto0 offset=0x4a source_lines=62-64 params=0
UPVALUES ['print', 'string']
00001 [L63] UGET     A=0 B=0 C=0 D=0 print
00002 [L63] UGET     A=1 B=0 C=1 D=1 string
00003 [L63] TGETS    A=1 B=1 C=0 D=256 'format'
00004 [L63] VARG     A=2 B=0 C=0 D=0 
00005 [L63] CALLM    A=1 B=0 C=0 D=0 
00006 [L63] CALLM    A=0 B=1 C=0 D=256 
00007 [L64] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto1 offset=0x92 source_lines=90-106 params=1
UPVALUES ['cclog', 'y_o_t']
00001 [L91] UGET     A=1 B=0 C=0 D=0 cclog
00002 [L91] KSTR     A=2 B=0 C=0 D=0 'call twoYearsCelebrateUI show()'
00003 [L91] CALL     A=1 B=1 C=2 D=258 
00004 [L94] GGET     A=1 B=0 C=1 D=1 'g_twoYearsCelebrateUI'
00005 [L94] IST      A=0 B=0 C=1 D=1 
00006 [L94] JMP      A=1 B=128 C=7 D=32775 target=14
00007 [L95] GGET     A=1 B=0 C=2 D=2 'd_ms'
00008 [L95] TGETS    A=1 B=1 C=3 D=259 'd_c'
00009 [L95] TGETS    A=1 B=1 C=4 D=260 'g_tags'
00010 [L95] TGETS    A=1 B=1 C=5 D=261 'TAG_twoYearsCelebrateUI'
00011 [L95] GSET     A=1 B=0 C=1 D=1 'g_twoYearsCelebrateUI'
00012 [L96] TNEW     A=1 B=0 C=0 D=0 
00013 [L96] GSET     A=1 B=0 C=6 D=6 'g_self'
00014 [L99] MOV      A=2 B=0 C=0 D=0 
00015 [L99] TGETS    A=1 B=0 C=7 D=7 'removeChildByTag'
00016 [L99] GGET     A=3 B=0 C=1 D=1 'g_twoYearsCelebrateUI'
00017 [L99] KPRI     A=4 B=0 C=2 D=2 
00018 [L99] CALL     A=1 B=1 C=4 D=260 
00019 [L100] GGET     A=1 B=0 C=8 D=8 'create'
00020 [L100] MOV      A=2 B=0 C=0 D=0 
00021 [L100] CALL     A=1 B=1 C=2 D=258 
00022 [L101] TNEW     A=1 B=0 C=0 D=0 
00023 [L101] GSET     A=1 B=0 C=9 D=9 'tmp_req'
00024 [L102] GGET     A=1 B=0 C=9 D=9 'tmp_req'
00025 [L102] UGET     A=2 B=0 C=1 D=1 y_o_t
00026 [L102] TGETS    A=2 B=2 C=11 D=523 'enter_activity'
00027 [L102] TSETS    A=2 B=1 C=10 D=266 'flag'
00028 [L103] GGET     A=1 B=0 C=9 D=9 'tmp_req'
00029 [L103] KSHORT   A=2 B=0 C=0 D=0 0
00030 [L103] TSETS    A=2 B=1 C=12 D=268 'index'
00031 [L104] GGET     A=1 B=0 C=2 D=2 'd_ms'
00032 [L104] TGETS    A=1 B=1 C=13 D=269 'd_u'
00033 [L104] TGETS    A=1 B=1 C=14 D=270 'main_server_send_msg'
00034 [L104] GGET     A=2 B=0 C=2 D=2 'd_ms'
00035 [L104] TGETS    A=2 B=2 C=15 D=527 'd_msg_def'
00036 [L104] TGETS    A=2 B=2 C=16 D=528 'gscl_msg_id'
00037 [L104] TGETS    A=2 B=2 C=17 D=529 'msg_yuanshi_activity'
00038 [L104] GGET     A=3 B=0 C=9 D=9 'tmp_req'
00039 [L104] CALL     A=1 B=1 C=3 D=259 
00040 [L106] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto2 offset=0x263 source_lines=108-111 params=1
UPVALUES []
00001 [L109] GGET     A=1 B=0 C=0 D=0 'g_self'
00002 [L109] GGET     A=2 B=0 C=2 D=2 'd_ms'
00003 [L109] TGETS    A=2 B=2 C=3 D=515 'd_u'
00004 [L109] TGETS    A=2 B=2 C=4 D=516 'createSwallowTouchLayer'
00005 [L109] MOV      A=3 B=0 C=0 D=0 
00006 [L109] CALL     A=2 B=2 C=2 D=514 
00007 [L109] TSETS    A=2 B=1 C=1 D=257 'main_layer'
00008 [L110] GGET     A=1 B=0 C=5 D=5 'createMainFrame'
00009 [L110] GGET     A=2 B=0 C=0 D=0 'g_self'
00010 [L110] TGETS    A=2 B=2 C=1 D=513 'main_layer'
00011 [L110] CALL     A=1 B=1 C=2 D=258 
00012 [L111] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto3 offset=0x2f8 source_lines=113-169 params=1
UPVALUES ['CCSprite', 'string', 'CCSizeMake']
00001 [L118] GGET     A=1 B=0 C=0 D=0 'd_ms'
00002 [L118] TGETS    A=1 B=1 C=1 D=257 'd_u'
00003 [L118] TGETS    A=1 B=1 C=2 D=258 'createByStyles'
00004 [L118] TDUP     A=2 B=0 C=3 D=3 {'kind': 'table', 'value': {'pic': 'v2/twoYearsCelebrateUI/bkg.jpg', 'y': 0.5, 'scaleX': 1, 'x': 0.5, 'scaleY': 1}}
00005 [L118] CALL     A=1 B=2 C=2 D=514 
00006 [L119] MOV      A=3 B=0 C=0 D=0 
00007 [L119] TGETS    A=2 B=0 C=4 D=4 'addChild'
00008 [L119] MOV      A=4 B=0 C=1 D=1 
00009 [L119] KSHORT   A=5 B=255 C=255 D=65535 -1
00010 [L119] CALL     A=2 B=1 C=4 D=260 
00011 [L121] KNUM     A=2 B=0 C=0 D=0 0.226
00012 [L121] GSET     A=2 B=0 C=5 D=5 'w'
00013 [L122] KNUM     A=2 B=0 C=1 D=1 0.09
00014 [L122] GSET     A=2 B=0 C=6 D=6 'h'
00015 [L123] KNUM     A=2 B=0 C=2 D=2 0.5
00016 [L123] GGET     A=3 B=0 C=6 D=6 'h'
00017 [L123] SUBNV    A=3 B=3 C=3 D=771 
00018 [L123] MULNV    A=3 B=3 C=2 D=770 
00019 [L123] GSET     A=3 B=0 C=7 D=7 'my'
00020 [L123] GSET     A=2 B=0 C=8 D=8 'mx'
00021 [L125] GGET     A=2 B=0 C=0 D=0 'd_ms'
00022 [L125] TGETS    A=2 B=2 C=1 D=513 'd_u'
00023 [L125] TGETS    A=2 B=2 C=2 D=514 'createByStyles'
00024 [L125] TDUP     A=3 B=0 C=9 D=9 {'kind': 'table', 'value': {'pic': 'v2/twoYearsCelebrateUI/title.png', 'x': 0.5, 'y': 1}}
00025 [L125] TDUP     A=4 B=0 C=10 D=10 {'kind': 'table', 'value': {1: 0.5, 2: 1}}
00026 [L125] TSETS    A=4 B=3 C=11 D=779 'anchor'
00027 [L125] CALL     A=2 B=2 C=2 D=514 
00028 [L126] MOV      A=4 B=0 C=0 D=0 
00029 [L126] TGETS    A=3 B=0 C=4 D=4 'addChild'
00030 [L126] MOV      A=5 B=0 C=2 D=2 
00031 [L126] CALL     A=3 B=1 C=3 D=259 
00032 [L133] UGET     A=3 B=0 C=0 D=0 CCSprite
00033 [L133] MOV      A=4 B=0 C=3 D=3 
00034 [L133] TGETS    A=3 B=3 C=12 D=780 'create'
00035 [L133] KSTR     A=5 B=0 C=13 D=13 'v2/twoYearsCelebrateUI/left.png'
00036 [L133] CALL     A=3 B=2 C=3 D=515 
00037 [L134] GGET     A=4 B=0 C=0 D=0 'd_ms'
00038 [L134] TGETS    A=4 B=4 C=1 D=1025 'd_u'
00039 [L134] TGETS    A=4 B=4 C=14 D=1038 'setStyles'
00040 [L134] MOV      A=5 B=0 C=3 D=3 
00041 [L134] TDUP     A=6 B=0 C=15 D=15 {'kind': 'table', 'value': {}}
00042 [L134] GGET     A=7 B=0 C=8 D=8 'mx'
00043 [L134] GGET     A=8 B=0 C=5 D=5 'w'
00044 [L134] MULNV    A=8 B=8 C=4 D=2052 
00045 [L134] SUBVV    A=7 B=7 C=8 D=1800 
00046 [L134] TSETS    A=7 B=6 C=16 D=1552 'x'
00047 [L134] GGET     A=7 B=0 C=7 D=7 'my'
00048 [L134] GGET     A=8 B=0 C=6 D=6 'h'
00049 [L134] MULNV    A=8 B=8 C=5 D=2053 
00050 [L134] ADDVV    A=7 B=7 C=8 D=1800 
00051 [L134] TSETS    A=7 B=6 C=17 D=1553 'y'
00052 [L134] CALL     A=4 B=1 C=3 D=259 
00053 [L135] MOV      A=5 B=0 C=0 D=0 
00054 [L135] TGETS    A=4 B=0 C=4 D=4 'addChild'
00055 [L135] MOV      A=6 B=0 C=3 D=3 
00056 [L135] CALL     A=4 B=1 C=3 D=259 
00057 [L138] GGET     A=4 B=0 C=0 D=0 'd_ms'
00058 [L138] TGETS    A=4 B=4 C=1 D=1025 'd_u'
00059 [L138] TGETS    A=4 B=4 C=18 D=1042 'getRealScale'
00060 [L138] MOV      A=5 B=0 C=3 D=3 
00061 [L138] CALL     A=4 B=3 C=2 D=770 
00062 [L141] GGET     A=6 B=0 C=0 D=0 'd_ms'
00063 [L141] TGETS    A=6 B=6 C=19 D=1555 'd_hz'
00064 [L141] TGETS    A=6 B=6 C=20 D=1556 'gethz'
00065 [L141] KSTR     A=7 B=0 C=21 D=21 'twoyears_info10'
00066 [L141] CALL     A=6 B=2 C=2 D=514 
00067 [L142] GGET     A=7 B=0 C=0 D=0 'd_ms'
00068 [L142] TGETS    A=7 B=7 C=1 D=1793 'd_u'
00069 [L142] TGETS    A=7 B=7 C=2 D=1794 'createByStyles'
00070 [L142] TDUP     A=8 B=0 C=22 D=22 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 22}}
00071 [L142] UGET     A=9 B=0 C=1 D=1 string
00072 [L142] TGETS    A=9 B=9 C=23 D=2327 'format'
00073 [L142] MOV      A=10 B=0 C=6 D=6 
00074 [L142] CALL     A=9 B=2 C=2 D=514 
00075 [L142] TSETS    A=9 B=8 C=24 D=2072 'string'
00076 [L142] GGET     A=9 B=0 C=25 D=25 'g_Color'
00077 [L142] TGETS    A=9 B=9 C=26 D=2330 'black'
00078 [L142] TSETS    A=9 B=8 C=27 D=2075 'color'
00079 [L142] UGET     A=9 B=0 C=2 D=2 CCSizeMake
00080 [L142] KSHORT   A=10 B=1 C=14 D=270 270
00081 [L142] KSHORT   A=11 B=0 C=0 D=0 0
00082 [L142] CALL     A=9 B=2 C=3 D=515 
00083 [L142] TSETS    A=9 B=8 C=28 D=2076 'size'
00084 [L142] CALL     A=7 B=2 C=2 D=514 
00085 [L143] GGET     A=8 B=0 C=0 D=0 'd_ms'
00086 [L143] TGETS    A=8 B=8 C=1 D=2049 'd_u'
00087 [L143] TGETS    A=8 B=8 C=14 D=2062 'setStyles'
00088 [L143] MOV      A=9 B=0 C=7 D=7 
00089 [L143] TDUP     A=10 B=0 C=29 D=29 {'kind': 'table', 'value': {}}
00090 [L143] GGET     A=11 B=0 C=8 D=8 'mx'
00091 [L143] GGET     A=12 B=0 C=5 D=5 'w'
00092 [L143] MULNV    A=12 B=12 C=4 D=3076 
00093 [L143] SUBVV    A=11 B=11 C=12 D=2828 
00094 [L143] TSETS    A=11 B=10 C=16 D=2576 'x'
00095 [L143] GGET     A=11 B=0 C=7 D=7 'my'
00096 [L143] MULNV    A=12 B=5 C=6 D=1286 
00097 [L143] ADDVV    A=11 B=11 C=12 D=2828 
00098 [L143] TSETS    A=11 B=10 C=17 D=2577 'y'
00099 [L143] CALL     A=8 B=1 C=3 D=259 
00100 [L144] MOV      A=9 B=0 C=0 D=0 
00101 [L144] TGETS    A=8 B=0 C=4 D=4 'addChild'
00102 [L144] MOV      A=10 B=0 C=7 D=7 
00103 [L144] CALL     A=8 B=1 C=3 D=259 
00104 [L146] GGET     A=8 B=0 C=0 D=0 'd_ms'
00105 [L146] TGETS    A=8 B=8 C=19 D=2067 'd_hz'
00106 [L146] TGETS    A=8 B=8 C=20 D=2068 'gethz'
00107 [L146] KSTR     A=9 B=0 C=30 D=30 'twoyears_info24'
00108 [L146] CALL     A=8 B=2 C=2 D=514 
00109 [L147] GGET     A=9 B=0 C=0 D=0 'd_ms'
00110 [L147] TGETS    A=9 B=9 C=1 D=2305 'd_u'
00111 [L147] TGETS    A=9 B=9 C=2 D=2306 'createByStyles'
00112 [L147] TDUP     A=10 B=0 C=31 D=31 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 22}}
00113 [L147] UGET     A=11 B=0 C=1 D=1 string
00114 [L147] TGETS    A=11 B=11 C=23 D=2839 'format'
00115 [L147] MOV      A=12 B=0 C=8 D=8 
00116 [L147] CALL     A=11 B=2 C=2 D=514 
00117 [L147] TSETS    A=11 B=10 C=24 D=2584 'string'
00118 [L147] GGET     A=11 B=0 C=25 D=25 'g_Color'
00119 [L147] TGETS    A=11 B=11 C=26 D=2842 'black'
00120 [L147] TSETS    A=11 B=10 C=27 D=2587 'color'
00121 [L147] UGET     A=11 B=0 C=2 D=2 CCSizeMake
00122 [L147] KSHORT   A=12 B=1 C=14 D=270 270
00123 [L147] KSHORT   A=13 B=0 C=0 D=0 0
00124 [L147] CALL     A=11 B=2 C=3 D=515 
00125 [L147] TSETS    A=11 B=10 C=28 D=2588 'size'
00126 [L147] CALL     A=9 B=2 C=2 D=514 
00127 [L148] GGET     A=10 B=0 C=0 D=0 'd_ms'
00128 [L148] TGETS    A=10 B=10 C=1 D=2561 'd_u'
00129 [L148] TGETS    A=10 B=10 C=14 D=2574 'setStyles'
00130 [L148] MOV      A=11 B=0 C=9 D=9 
00131 [L148] TDUP     A=12 B=0 C=32 D=32 {'kind': 'table', 'value': {}}
00132 [L148] GGET     A=13 B=0 C=8 D=8 'mx'
00133 [L148] GGET     A=14 B=0 C=5 D=5 'w'
00134 [L148] MULNV    A=14 B=14 C=4 D=3588 
00135 [L148] SUBVV    A=13 B=13 C=14 D=3342 
00136 [L148] TSETS    A=13 B=12 C=16 D=3088 'x'
00137 [L148] GGET     A=13 B=0 C=7 D=7 'my'
00138 [L148] MULNV    A=14 B=5 C=6 D=1286 
00139 [L148] ADDVV    A=13 B=13 C=14 D=3342 
00140 [L148] SUBVN    A=13 B=13 C=7 D=3335 
00141 [L148] TSETS    A=13 B=12 C=17 D=3089 'y'
00142 [L148] CALL     A=10 B=1 C=3 D=259 
00143 [L149] MOV      A=11 B=0 C=0 D=0 
00144 [L149] TGETS    A=10 B=0 C=4 D=4 'addChild'
00145 [L149] MOV      A=12 B=0 C=9 D=9 
00146 [L149] CALL     A=10 B=1 C=3 D=259 
00147 [L153] GGET     A=10 B=0 C=0 D=0 'd_ms'
00148 [L153] TGETS    A=10 B=10 C=1 D=2561 'd_u'
00149 [L153] TGETS    A=10 B=10 C=2 D=2562 'createByStyles'
00150 [L153] TDUP     A=11 B=0 C=33 D=33 {'kind': 'table', 'value': {'pic': 'v2/moonCakeUI/time.png', 'x': 0.13}}
00151 [L153] GGET     A=12 B=0 C=7 D=7 'my'
00152 [L153] GGET     A=13 B=0 C=6 D=6 'h'
00153 [L153] MULNV    A=13 B=13 C=8 D=3336 
00154 [L153] ADDVV    A=12 B=12 C=13 D=3085 
00155 [L153] TSETS    A=12 B=11 C=17 D=2833 'y'
00156 [L153] TDUP     A=12 B=0 C=34 D=34 {'kind': 'table', 'value': {1: 0.5, 2: 0.5}}
00157 [L153] TSETS    A=12 B=11 C=11 D=2827 'anchor'
00158 [L153] CALL     A=10 B=2 C=2 D=514 
00159 [L154] MOV      A=12 B=0 C=0 D=0 
00160 [L154] TGETS    A=11 B=0 C=4 D=4 'addChild'
00161 [L154] MOV      A=13 B=0 C=10 D=10 
00162 [L154] CALL     A=11 B=1 C=3 D=259 
00163 [L155] GGET     A=11 B=0 C=0 D=0 'd_ms'
00164 [L155] TGETS    A=11 B=11 C=1 D=2817 'd_u'
00165 [L155] TGETS    A=11 B=11 C=2 D=2818 'createByStyles'
00166 [L155] TDUP     A=12 B=0 C=35 D=35 {'kind': 'table', 'value': {'pic': 'v2/towerUI/b_bkg4.png', 'scale_x': 1.6, 'scale_y': 1, 'x': 0.13}}
00167 [L155] GGET     A=13 B=0 C=7 D=7 'my'
00168 [L155] GGET     A=14 B=0 C=6 D=6 'h'
00169 [L155] MULNV    A=14 B=14 C=9 D=3593 
00170 [L155] ADDVV    A=13 B=13 C=14 D=3342 
00171 [L155] TSETS    A=13 B=12 C=17 D=3089 'y'
00172 [L155] TDUP     A=13 B=0 C=36 D=36 {'kind': 'table', 'value': {1: 0.5, 2: 0.5}}
00173 [L155] TSETS    A=13 B=12 C=11 D=3083 'anchor'
00174 [L155] CALL     A=11 B=2 C=2 D=514 
00175 [L156] MOV      A=13 B=0 C=0 D=0 
00176 [L156] TGETS    A=12 B=0 C=4 D=4 'addChild'
00177 [L156] MOV      A=14 B=0 C=11 D=11 
00178 [L156] CALL     A=12 B=1 C=3 D=259 
00179 [L157] GGET     A=12 B=0 C=37 D=37 'tickTime'
00180 [L157] CALL     A=12 B=1 C=1 D=257 
00181 [L159] TDUP     A=12 B=0 C=38 D=38 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00182 [L162] TDUP     A=13 B=0 C=39 D=39 {'kind': 'table', 'value': {'npic': 'v2/common/close1.png', 'spic': 'v2/common/close2.png', 'y': 0.9, 'x': 0.9}}
00183 [L163] GGET     A=14 B=0 C=40 D=40 'call_back_close'
00184 [L163] TSETS    A=14 B=13 C=41 D=3369 'call_back'
00185 [L163] TSETB    A=13 B=12 C=1 D=3073 
00186 [L163] TDUP     A=13 B=0 C=42 D=42 {'kind': 'table', 'value': {'npic': 'v2/twoYearsCelebrateUI/shop1.png', 'spic': 'v2/twoYearsCelebrateUI/shop2.png', 'x': 0.8}}
00187 [L164] GGET     A=14 B=0 C=6 D=6 'h'
00188 [L164] MULVN    A=14 B=14 C=10 D=3594 
00189 [L164] ADDNV    A=14 B=14 C=2 D=3586 
00190 [L164] TSETS    A=14 B=13 C=17 D=3345 'y'
00191 [L164] GGET     A=14 B=0 C=43 D=43 'createShop'
00192 [L164] TSETS    A=14 B=13 C=41 D=3369 'call_back'
00193 [L164] TSETB    A=13 B=12 C=2 D=3074 
00194 [L164] TDUP     A=13 B=0 C=44 D=44 {'kind': 'table', 'value': {'npic': 'v2/twoYearsCelebrateUI/luck1.png', 'spic': 'v2/twoYearsCelebrateUI/luck2.png', 'x': 0.8}}
00195 [L165] GGET     A=14 B=0 C=6 D=6 'h'
00196 [L165] MULVN    A=14 B=14 C=11 D=3595 
00197 [L165] ADDNV    A=14 B=14 C=2 D=3586 
00198 [L165] TSETS    A=14 B=13 C=17 D=3345 'y'
00199 [L165] GGET     A=14 B=0 C=45 D=45 'pray'
00200 [L165] TSETS    A=14 B=13 C=41 D=3369 'call_back'
00201 [L165] TSETB    A=13 B=12 C=3 D=3075 
00202 [L167] MOV      A=14 B=0 C=0 D=0 
00203 [L167] TGETS    A=13 B=0 C=4 D=4 'addChild'
00204 [L167] GGET     A=15 B=0 C=0 D=0 'd_ms'
00205 [L167] TGETS    A=15 B=15 C=1 D=3841 'd_u'
00206 [L167] TGETS    A=15 B=15 C=46 D=3886 'createMenu'
00207 [L167] MOV      A=16 B=0 C=12 D=12 
00208 [L167] CALL     A=15 B=0 C=2 D=2 
00209 [L167] CALLM    A=13 B=1 C=1 D=257 
00210 [L168] GGET     A=13 B=0 C=47 D=47 'showNews'
00211 [L168] CALL     A=13 B=1 C=1 D=257 
00212 [L169] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto4 offset=0xbc1 source_lines=171-178 params=0
UPVALUES []
00001 [L172] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L172] TGETS    A=0 B=0 C=1 D=1 'd_music_mgr'
00003 [L172] TGETS    A=0 B=0 C=2 D=2 'playClickEffect'
00004 [L172] CALL     A=0 B=1 C=1 D=257 
00005 [L174] GGET     A=0 B=0 C=0 D=0 'd_ms'
00006 [L174] TGETS    A=0 B=0 C=3 D=3 'd_activityUI'
00007 [L174] TGETS    A=0 B=0 C=4 D=4 'returnBack'
00008 [L174] CALL     A=0 B=1 C=1 D=257 
00009 [L178] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto5 offset=0xc35 source_lines=180-190 params=0
UPVALUES ['y_o_t']
00001 [L183] TNEW     A=0 B=0 C=0 D=0 
00002 [L183] GSET     A=0 B=0 C=0 D=0 'tmp_req'
00003 [L184] GGET     A=0 B=0 C=0 D=0 'tmp_req'
00004 [L184] UGET     A=1 B=0 C=0 D=0 y_o_t
00005 [L184] TGETS    A=1 B=1 C=2 D=258 'enter_shop'
00006 [L184] TSETS    A=1 B=0 C=1 D=1 'flag'
00007 [L185] GGET     A=0 B=0 C=0 D=0 'tmp_req'
00008 [L185] KSHORT   A=1 B=0 C=0 D=0 0
00009 [L185] TSETS    A=1 B=0 C=3 D=3 'index'
00010 [L187] GGET     A=0 B=0 C=4 D=4 'd_ms'
00011 [L187] TGETS    A=0 B=0 C=5 D=5 'd_u'
00012 [L187] TGETS    A=0 B=0 C=6 D=6 'main_server_send_msg'
00013 [L187] GGET     A=1 B=0 C=4 D=4 'd_ms'
00014 [L187] TGETS    A=1 B=1 C=7 D=263 'd_msg_def'
00015 [L187] TGETS    A=1 B=1 C=8 D=264 'gscl_msg_id'
00016 [L187] TGETS    A=1 B=1 C=9 D=265 'msg_yuanshi_activity'
00017 [L187] GGET     A=2 B=0 C=0 D=0 'tmp_req'
00018 [L187] CALL     A=0 B=1 C=3 D=259 
00019 [L190] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto6 offset=0xd11 source_lines=191-207 params=0
UPVALUES ['y_o_t', 'o_t']
00001 [L193] GGET     A=0 B=0 C=0 D=0 'g_self'
00002 [L193] UGET     A=1 B=0 C=0 D=0 y_o_t
00003 [L193] TGETS    A=1 B=1 C=1 D=257 'enter_activity'
00004 [L193] TGETV    A=0 B=0 C=1 D=1 
00005 [L193] TGETS    A=0 B=0 C=2 D=2 'free_times'
00006 [L193] IST      A=0 B=0 C=0 D=0 
00007 [L193] JMP      A=1 B=128 C=1 D=32769 target=9
00008 [L193] KSHORT   A=0 B=0 C=0 D=0 0
00009 [L194] GGET     A=1 B=0 C=3 D=3 'd_ms'
00010 [L194] TGETS    A=1 B=1 C=4 D=260 'd_smithUI'
00011 [L194] TGETS    A=1 B=1 C=5 D=261 'getMaterialCount'
00012 [L194] UGET     A=2 B=0 C=1 D=1 o_t
00013 [L194] TGETS    A=2 B=2 C=6 D=518 'item'
00014 [L194] KSHORT   A=3 B=7 C=15 D=1807 1807
00015 [L194] CALL     A=1 B=2 C=3 D=515 
00016 [L195] KSHORT   A=2 B=0 C=0 D=0 0
00017 [L195] ISGT     A=0 B=0 C=2 D=2 
00018 [L195] JMP      A=2 B=128 C=13 D=32781 target=32
00019 [L195] KSHORT   A=2 B=0 C=0 D=0 0
00020 [L195] ISGT     A=1 B=0 C=2 D=2 
00021 [L195] JMP      A=2 B=128 C=10 D=32778 target=32
00022 [L196] GGET     A=2 B=0 C=3 D=3 'd_ms'
00023 [L196] TGETS    A=2 B=2 C=7 D=519 'd_info'
00024 [L196] TGETS    A=2 B=2 C=8 D=520 'show'
00025 [L196] GGET     A=3 B=0 C=3 D=3 'd_ms'
00026 [L196] TGETS    A=3 B=3 C=9 D=777 'd_hz'
00027 [L196] TGETS    A=3 B=3 C=10 D=778 'gethz'
00028 [L196] KSTR     A=4 B=0 C=11 D=11 'twoyears_info19'
00029 [L196] CALL     A=3 B=0 C=2 D=2 
00030 [L196] CALLM    A=2 B=1 C=0 D=256 
00031 [L197] RET0     A=0 B=0 C=1 D=1 
00032 [L200] TNEW     A=2 B=0 C=0 D=0 
00033 [L200] GSET     A=2 B=0 C=12 D=12 'tmp_req'
00034 [L201] GGET     A=2 B=0 C=12 D=12 'tmp_req'
00035 [L201] UGET     A=3 B=0 C=0 D=0 y_o_t
00036 [L201] TGETS    A=3 B=3 C=14 D=782 'wish_yuanshi'
00037 [L201] TSETS    A=3 B=2 C=13 D=525 'flag'
00038 [L202] GGET     A=2 B=0 C=12 D=12 'tmp_req'
00039 [L202] KSHORT   A=3 B=0 C=0 D=0 0
00040 [L202] TSETS    A=3 B=2 C=15 D=527 'index'
00041 [L204] GGET     A=2 B=0 C=3 D=3 'd_ms'
00042 [L204] TGETS    A=2 B=2 C=16 D=528 'd_u'
00043 [L204] TGETS    A=2 B=2 C=17 D=529 'main_server_send_msg'
00044 [L204] GGET     A=3 B=0 C=3 D=3 'd_ms'
00045 [L204] TGETS    A=3 B=3 C=18 D=786 'd_msg_def'
00046 [L204] TGETS    A=3 B=3 C=19 D=787 'gscl_msg_id'
00047 [L204] TGETS    A=3 B=3 C=20 D=788 'msg_yuanshi_activity'
00048 [L204] GGET     A=4 B=0 C=12 D=12 'tmp_req'
00049 [L204] CALL     A=2 B=1 C=3 D=259 
00050 [L207] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto7 offset=0xf0d source_lines=210-221 params=0
UPVALUES []
00001 [L211] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L211] TGETS    A=0 B=0 C=1 D=1 'd_data'
00003 [L211] TGETS    A=0 B=0 C=2 D=2 'g_new_config'
00004 [L211] GGET     A=1 B=0 C=0 D=0 'd_ms'
00005 [L211] TGETS    A=1 B=1 C=3 D=259 'd_common_def'
00006 [L211] TGETS    A=1 B=1 C=4 D=260 'client_config_type'
00007 [L211] TGETS    A=1 B=1 C=5 D=261 'common_config'
00008 [L211] TGETV    A=0 B=0 C=1 D=1 
00009 [L211] ISF      A=0 B=0 C=0 D=0 
00010 [L211] JMP      A=0 B=128 C=11 D=32779 target=22
00011 [L211] GGET     A=0 B=0 C=0 D=0 'd_ms'
00012 [L211] TGETS    A=0 B=0 C=1 D=1 'd_data'
00013 [L211] TGETS    A=0 B=0 C=2 D=2 'g_new_config'
00014 [L211] GGET     A=1 B=0 C=0 D=0 'd_ms'
00015 [L211] TGETS    A=1 B=1 C=3 D=259 'd_common_def'
00016 [L211] TGETS    A=1 B=1 C=4 D=260 'client_config_type'
00017 [L211] TGETS    A=1 B=1 C=5 D=261 'common_config'
00018 [L211] TGETV    A=0 B=0 C=1 D=1 
00019 [L211] TGETS    A=0 B=0 C=6 D=6 'yuanshi_info'
00020 [L211] IST      A=0 B=0 C=0 D=0 
00021 [L211] JMP      A=0 B=128 C=2 D=32770 target=24
00022 [L212] KPRI     A=0 B=0 C=1 D=1 
00023 [L212] RET1     A=0 B=0 C=2 D=2 
00024 [L214] GGET     A=0 B=0 C=0 D=0 'd_ms'
00025 [L214] TGETS    A=0 B=0 C=1 D=1 'd_data'
00026 [L214] TGETS    A=0 B=0 C=2 D=2 'g_new_config'
00027 [L214] GGET     A=1 B=0 C=0 D=0 'd_ms'
00028 [L214] TGETS    A=1 B=1 C=3 D=259 'd_common_def'
00029 [L214] TGETS    A=1 B=1 C=4 D=260 'client_config_type'
00030 [L214] TGETS    A=1 B=1 C=5 D=261 'common_config'
00031 [L214] TGETV    A=0 B=0 C=1 D=1 
00032 [L214] TGETS    A=0 B=0 C=6 D=6 'yuanshi_info'
00033 [L215] GGET     A=1 B=0 C=0 D=0 'd_ms'
00034 [L215] TGETS    A=1 B=1 C=7 D=263 'd_time'
00035 [L215] TGETS    A=1 B=1 C=8 D=264 'getTime'
00036 [L215] CALL     A=1 B=2 C=1 D=513 
00037 [L216] TGETS    A=2 B=0 C=9 D=9 'begin_time'
00038 [L216] ISGE     A=2 B=0 C=1 D=1 
00039 [L216] JMP      A=2 B=128 C=6 D=32774 target=46
00040 [L216] TGETS    A=2 B=0 C=10 D=10 'end_time'
00041 [L216] ISGE     A=1 B=0 C=2 D=2 
00042 [L216] JMP      A=2 B=128 C=3 D=32771 target=46
00043 [L217] KPRI     A=2 B=0 C=2 D=2 
00044 [L217] RET1     A=2 B=0 C=2 D=2 
00045 [L217] JMP      A=2 B=128 C=2 D=32770 target=48
00046 [L219] KPRI     A=2 B=0 C=1 D=1 
00047 [L219] RET1     A=2 B=0 C=2 D=2 
00048 [L221] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto8 offset=0x1094 source_lines=224-229 params=0
UPVALUES []
00001 [L225] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L225] TGETS    A=0 B=0 C=1 D=1 'd_music_mgr'
00003 [L225] TGETS    A=0 B=0 C=2 D=2 'playClickEffect'
00004 [L225] CALL     A=0 B=1 C=1 D=257 
00005 [L226] GGET     A=0 B=0 C=0 D=0 'd_ms'
00006 [L226] TGETS    A=0 B=0 C=3 D=3 'd_u'
00007 [L226] TGETS    A=0 B=0 C=4 D=4 'remove'
00008 [L226] GGET     A=1 B=0 C=5 D=5 'g_self'
00009 [L226] TGETS    A=1 B=1 C=6 D=262 'shoplayer'
00010 [L226] CALL     A=0 B=1 C=2 D=258 
00011 [L227] GGET     A=0 B=0 C=5 D=5 'g_self'
00012 [L227] KPRI     A=1 B=0 C=0 D=0 
00013 [L227] TSETS    A=1 B=0 C=6 D=6 'shoplayer'
00014 [L228] GGET     A=0 B=0 C=7 D=7 'showNews'
00015 [L228] CALL     A=0 B=1 C=1 D=257 
00016 [L229] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto9 offset=0x1137 source_lines=258-260 params=1
UPVALUES ['shoplayer', 'config']
00001 [L259] GGET     A=1 B=0 C=0 D=0 'd_ms'
00002 [L259] TGETS    A=1 B=1 C=1 D=257 'd_data'
00003 [L259] TGETS    A=1 B=1 C=2 D=258 'showItemIntro'
00004 [L259] UGET     A=2 B=0 C=0 D=0 shoplayer
00005 [L259] UGET     A=3 B=0 C=1 D=1 config
00006 [L259] TGETV    A=3 B=3 C=0 D=768 
00007 [L259] CALL     A=1 B=1 C=3 D=259 
00008 [L260] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto10 offset=0x11a2 source_lines=232-331 params=1
UPVALUES ['CCSprite', 'y_o_t', 'table']
00001 [L234] UGET     A=1 B=0 C=0 D=0 CCSprite
00002 [L234] MOV      A=2 B=0 C=1 D=1 
00003 [L234] TGETS    A=1 B=1 C=0 D=256 'create'
00004 [L234] KSTR     A=3 B=0 C=1 D=1 'v2/twoYearsCelebrateUI/shop.png'
00005 [L234] CALL     A=1 B=2 C=3 D=515 
00006 [L235] GGET     A=2 B=0 C=2 D=2 'd_ms'
00007 [L235] TGETS    A=2 B=2 C=3 D=515 'd_u'
00008 [L235] TGETS    A=2 B=2 C=4 D=516 'setStyles'
00009 [L235] MOV      A=3 B=0 C=1 D=1 
00010 [L235] TDUP     A=4 B=0 C=5 D=5 {'kind': 'table', 'value': {'x': 0.5, 'y': 0.5}}
00011 [L235] CALL     A=2 B=1 C=3 D=259 
00012 [L236] MOV      A=3 B=0 C=0 D=0 
00013 [L236] TGETS    A=2 B=0 C=6 D=6 'addChild'
00014 [L236] MOV      A=4 B=0 C=1 D=1 
00015 [L236] CALL     A=2 B=1 C=3 D=259 
00016 [L238] GGET     A=2 B=0 C=2 D=2 'd_ms'
00017 [L238] TGETS    A=2 B=2 C=3 D=515 'd_u'
00018 [L238] TGETS    A=2 B=2 C=7 D=519 'getRealScale'
00019 [L238] MOV      A=3 B=0 C=1 D=1 
00020 [L238] CALL     A=2 B=3 C=2 D=770 
00021 [L239] GGET     A=4 B=0 C=8 D=8 'g_self'
00022 [L239] TSETS    A=3 B=4 C=9 D=1033 'shop_h'
00023 [L240] GGET     A=4 B=0 C=8 D=8 'g_self'
00024 [L240] TSETS    A=2 B=4 C=10 D=1034 'shop_w'
00025 [L241] GGET     A=4 B=0 C=8 D=8 'g_self'
00026 [L241] UGET     A=5 B=0 C=1 D=1 y_o_t
00027 [L241] TGETS    A=5 B=5 C=11 D=1291 'enter_shop'
00028 [L241] TGETV    A=4 B=4 C=5 D=1029 
00029 [L241] TGETS    A=4 B=4 C=12 D=1036 'shop_config'
00030 [L242] UGET     A=5 B=0 C=0 D=0 CCSprite
00031 [L242] MOV      A=6 B=0 C=5 D=5 
00032 [L242] TGETS    A=5 B=5 C=0 D=1280 'create'
00033 [L242] KSTR     A=7 B=0 C=13 D=13 'v2/twoYearsCelebrateUI/shop_title.png'
00034 [L242] CALL     A=5 B=2 C=3 D=515 
00035 [L243] GGET     A=6 B=0 C=2 D=2 'd_ms'
00036 [L243] TGETS    A=6 B=6 C=3 D=1539 'd_u'
00037 [L243] TGETS    A=6 B=6 C=4 D=1540 'setStyles'
00038 [L243] MOV      A=7 B=0 C=5 D=5 
00039 [L243] TDUP     A=8 B=0 C=14 D=14 {'kind': 'table', 'value': {'x': 0.5}}
00040 [L243] MULVN    A=9 B=3 C=0 D=768 
00041 [L243] ADDNV    A=9 B=9 C=1 D=2305 
00042 [L243] TSETS    A=9 B=8 C=15 D=2063 'y'
00043 [L243] CALL     A=6 B=1 C=3 D=259 
00044 [L244] MOV      A=7 B=0 C=0 D=0 
00045 [L244] TGETS    A=6 B=0 C=6 D=6 'addChild'
00046 [L244] MOV      A=8 B=0 C=5 D=5 
00047 [L244] CALL     A=6 B=1 C=3 D=259 
00048 [L245] IST      A=0 B=0 C=4 D=4 
00049 [L245] JMP      A=6 B=128 C=1 D=32769 target=51
00050 [L246] UCLO     A=0 B=129 C=128 D=33152 target=435
00051 [L250] TDUP     A=6 B=0 C=16 D=16 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00052 [L253] TDUP     A=7 B=0 C=17 D=17 {'kind': 'table', 'value': {'npic': 'v2/common/close1.png', 'spic': 'v2/common/close2.png', 'y': 0.83, 'x': 0.75}}
00053 [L254] GGET     A=8 B=0 C=18 D=18 'closeShop'
00054 [L254] TSETS    A=8 B=7 C=19 D=1811 'call_back'
00055 [L254] TSETB    A=7 B=6 C=1 D=1537 
00056 [L260] FNEW     A=7 B=0 C=20 D=20 {'kind': 'proto', 'id': 9}
00057 [L258] GSET     A=7 B=0 C=21 D=21 'showIntro'
00058 [L261] GGET     A=7 B=0 C=2 D=2 'd_ms'
00059 [L261] TGETS    A=7 B=7 C=22 D=1814 'd_data'
00060 [L261] TGETS    A=7 B=7 C=23 D=1815 'getCertainSmallSprite'
00061 [L261] TGETB    A=8 B=4 C=1 D=1025 
00062 [L261] TGETS    A=8 B=8 C=24 D=2072 'object_type'
00063 [L261] TGETB    A=9 B=4 C=1 D=1025 
00064 [L261] TGETS    A=9 B=9 C=25 D=2329 'attach_type'
00065 [L261] CALL     A=7 B=2 C=3 D=515 
00066 [L261] GSET     A=7 B=0 C=26 D=26 'icon'
00067 [L262] UGET     A=7 B=0 C=2 D=2 table
00068 [L262] TGETS    A=7 B=7 C=27 D=1819 'insert'
00069 [L262] MOV      A=8 B=0 C=6 D=6 
00070 [L262] TDUP     A=9 B=0 C=28 D=28 {'kind': 'table', 'value': {'tag': 1}}
00071 [L262] GGET     A=10 B=0 C=26 D=26 'icon'
00072 [L262] TSETS    A=10 B=9 C=29 D=2333 'nsprite'
00073 [L262] GGET     A=10 B=0 C=26 D=26 'icon'
00074 [L262] TSETS    A=10 B=9 C=30 D=2334 'ssprite'
00075 [L262] MULVN    A=10 B=2 C=2 D=514 
00076 [L262] SUBNV    A=10 B=10 C=1 D=2561 
00077 [L262] TSETS    A=10 B=9 C=31 D=2335 'x'
00078 [L262] MULVN    A=10 B=3 C=3 D=771 
00079 [L262] ADDNV    A=10 B=10 C=1 D=2561 
00080 [L262] TSETS    A=10 B=9 C=15 D=2319 'y'
00081 [L262] GGET     A=10 B=0 C=21 D=21 'showIntro'
00082 [L262] TSETS    A=10 B=9 C=19 D=2323 'call_back'
00083 [L262] CALL     A=7 B=1 C=3 D=259 
00084 [L263] GGET     A=7 B=0 C=2 D=2 'd_ms'
00085 [L263] TGETS    A=7 B=7 C=22 D=1814 'd_data'
00086 [L263] TGETS    A=7 B=7 C=23 D=1815 'getCertainSmallSprite'
00087 [L263] TGETB    A=8 B=4 C=2 D=1026 
00088 [L263] TGETS    A=8 B=8 C=24 D=2072 'object_type'
00089 [L263] TGETB    A=9 B=4 C=2 D=1026 
00090 [L263] TGETS    A=9 B=9 C=25 D=2329 'attach_type'
00091 [L263] CALL     A=7 B=2 C=3 D=515 
00092 [L263] GSET     A=7 B=0 C=26 D=26 'icon'
00093 [L264] UGET     A=7 B=0 C=2 D=2 table
00094 [L264] TGETS    A=7 B=7 C=27 D=1819 'insert'
00095 [L264] MOV      A=8 B=0 C=6 D=6 
00096 [L264] TDUP     A=9 B=0 C=32 D=32 {'kind': 'table', 'value': {'tag': 2}}
00097 [L264] GGET     A=10 B=0 C=26 D=26 'icon'
00098 [L264] TSETS    A=10 B=9 C=29 D=2333 'nsprite'
00099 [L264] GGET     A=10 B=0 C=26 D=26 'icon'
00100 [L264] TSETS    A=10 B=9 C=30 D=2334 'ssprite'
00101 [L264] MULVN    A=10 B=2 C=2 D=514 
00102 [L264] ADDNV    A=10 B=10 C=1 D=2561 
00103 [L264] TSETS    A=10 B=9 C=31 D=2335 'x'
00104 [L264] MULVN    A=10 B=3 C=3 D=771 
00105 [L264] ADDNV    A=10 B=10 C=1 D=2561 
00106 [L264] TSETS    A=10 B=9 C=15 D=2319 'y'
00107 [L264] GGET     A=10 B=0 C=21 D=21 'showIntro'
00108 [L264] TSETS    A=10 B=9 C=19 D=2323 'call_back'
00109 [L264] CALL     A=7 B=1 C=3 D=259 
00110 [L269] UGET     A=7 B=0 C=0 D=0 CCSprite
00111 [L269] MOV      A=8 B=0 C=7 D=7 
00112 [L269] TGETS    A=7 B=7 C=0 D=1792 'create'
00113 [L269] KSTR     A=9 B=0 C=33 D=33 'v2/twoYearsCelebrateUI/gift_name_bkg.png'
00114 [L269] CALL     A=7 B=2 C=3 D=515 
00115 [L270] GGET     A=8 B=0 C=2 D=2 'd_ms'
00116 [L270] TGETS    A=8 B=8 C=3 D=2051 'd_u'
00117 [L270] TGETS    A=8 B=8 C=4 D=2052 'setStyles'
00118 [L270] MOV      A=9 B=0 C=7 D=7 
00119 [L270] TDUP     A=10 B=0 C=34 D=34 {'kind': 'table', 'value': {}}
00120 [L270] MULVN    A=11 B=2 C=2 D=514 
00121 [L270] SUBNV    A=11 B=11 C=1 D=2817 
00122 [L270] TSETS    A=11 B=10 C=31 D=2591 'x'
00123 [L270] MULVN    A=11 B=3 C=4 D=772 
00124 [L270] ADDNV    A=11 B=11 C=1 D=2817 
00125 [L270] TSETS    A=11 B=10 C=15 D=2575 'y'
00126 [L270] CALL     A=8 B=1 C=3 D=259 
00127 [L271] MOV      A=9 B=0 C=0 D=0 
00128 [L271] TGETS    A=8 B=0 C=6 D=6 'addChild'
00129 [L271] MOV      A=10 B=0 C=7 D=7 
00130 [L271] CALL     A=8 B=1 C=3 D=259 
00131 [L273] GGET     A=8 B=0 C=2 D=2 'd_ms'
00132 [L273] TGETS    A=8 B=8 C=22 D=2070 'd_data'
00133 [L273] TGETS    A=8 B=8 C=35 D=2083 'getNameByTypeId'
00134 [L273] TGETB    A=9 B=4 C=1 D=1025 
00135 [L273] TGETS    A=9 B=9 C=24 D=2328 'object_type'
00136 [L273] TGETB    A=10 B=4 C=1 D=1025 
00137 [L273] TGETS    A=10 B=10 C=25 D=2585 'attach_type'
00138 [L273] CALL     A=8 B=2 C=3 D=515 
00139 [L274] GGET     A=9 B=0 C=2 D=2 'd_ms'
00140 [L274] TGETS    A=9 B=9 C=3 D=2307 'd_u'
00141 [L274] TGETS    A=9 B=9 C=36 D=2340 'createByStyles'
00142 [L274] TDUP     A=10 B=0 C=37 D=37 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 22}}
00143 [L274] TSETS    A=8 B=10 C=38 D=2598 'string'
00144 [L274] GGET     A=11 B=0 C=39 D=39 'g_Color'
00145 [L274] TGETS    A=11 B=11 C=40 D=2856 'white'
00146 [L274] TSETS    A=11 B=10 C=41 D=2601 'color'
00147 [L274] CALL     A=9 B=2 C=2 D=514 
00148 [L275] GGET     A=10 B=0 C=2 D=2 'd_ms'
00149 [L275] TGETS    A=10 B=10 C=3 D=2563 'd_u'
00150 [L275] TGETS    A=10 B=10 C=4 D=2564 'setStyles'
00151 [L275] MOV      A=11 B=0 C=9 D=9 
00152 [L275] TDUP     A=12 B=0 C=42 D=42 {'kind': 'table', 'value': {}}
00153 [L275] MULVN    A=13 B=2 C=2 D=514 
00154 [L275] SUBNV    A=13 B=13 C=1 D=3329 
00155 [L275] TSETS    A=13 B=12 C=31 D=3103 'x'
00156 [L275] MULVN    A=13 B=3 C=4 D=772 
00157 [L275] ADDNV    A=13 B=13 C=1 D=3329 
00158 [L275] TSETS    A=13 B=12 C=15 D=3087 'y'
00159 [L275] CALL     A=10 B=1 C=3 D=259 
00160 [L276] MOV      A=11 B=0 C=0 D=0 
00161 [L276] TGETS    A=10 B=0 C=6 D=6 'addChild'
00162 [L276] MOV      A=12 B=0 C=9 D=9 
00163 [L276] CALL     A=10 B=1 C=3 D=259 
00164 [L279] UGET     A=10 B=0 C=0 D=0 CCSprite
00165 [L279] MOV      A=11 B=0 C=10 D=10 
00166 [L279] TGETS    A=10 B=10 C=0 D=2560 'create'
00167 [L279] KSTR     A=12 B=0 C=33 D=33 'v2/twoYearsCelebrateUI/gift_name_bkg.png'
00168 [L279] CALL     A=10 B=2 C=3 D=515 
00169 [L280] GGET     A=11 B=0 C=2 D=2 'd_ms'
00170 [L280] TGETS    A=11 B=11 C=3 D=2819 'd_u'
00171 [L280] TGETS    A=11 B=11 C=4 D=2820 'setStyles'
00172 [L280] MOV      A=12 B=0 C=10 D=10 
00173 [L280] TDUP     A=13 B=0 C=43 D=43 {'kind': 'table', 'value': {}}
00174 [L280] MULVN    A=14 B=2 C=2 D=514 
00175 [L280] ADDNV    A=14 B=14 C=1 D=3585 
00176 [L280] TSETS    A=14 B=13 C=31 D=3359 'x'
00177 [L280] MULVN    A=14 B=3 C=4 D=772 
00178 [L280] ADDNV    A=14 B=14 C=1 D=3585 
00179 [L280] TSETS    A=14 B=13 C=15 D=3343 'y'
00180 [L280] CALL     A=11 B=1 C=3 D=259 
00181 [L281] MOV      A=12 B=0 C=0 D=0 
00182 [L281] TGETS    A=11 B=0 C=6 D=6 'addChild'
00183 [L281] MOV      A=13 B=0 C=10 D=10 
00184 [L281] CALL     A=11 B=1 C=3 D=259 
00185 [L283] GGET     A=11 B=0 C=2 D=2 'd_ms'
00186 [L283] TGETS    A=11 B=11 C=22 D=2838 'd_data'
00187 [L283] TGETS    A=11 B=11 C=35 D=2851 'getNameByTypeId'
00188 [L283] TGETB    A=12 B=4 C=2 D=1026 
00189 [L283] TGETS    A=12 B=12 C=24 D=3096 'object_type'
00190 [L283] TGETB    A=13 B=4 C=2 D=1026 
00191 [L283] TGETS    A=13 B=13 C=25 D=3353 'attach_type'
00192 [L283] CALL     A=11 B=2 C=3 D=515 
00193 [L284] GGET     A=12 B=0 C=2 D=2 'd_ms'
00194 [L284] TGETS    A=12 B=12 C=3 D=3075 'd_u'
00195 [L284] TGETS    A=12 B=12 C=36 D=3108 'createByStyles'
00196 [L284] TDUP     A=13 B=0 C=44 D=44 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 22}}
00197 [L284] TSETS    A=11 B=13 C=38 D=3366 'string'
00198 [L284] GGET     A=14 B=0 C=39 D=39 'g_Color'
00199 [L284] TGETS    A=14 B=14 C=40 D=3624 'white'
00200 [L284] TSETS    A=14 B=13 C=41 D=3369 'color'
00201 [L284] CALL     A=12 B=2 C=2 D=514 
00202 [L285] GGET     A=13 B=0 C=2 D=2 'd_ms'
00203 [L285] TGETS    A=13 B=13 C=3 D=3331 'd_u'
00204 [L285] TGETS    A=13 B=13 C=4 D=3332 'setStyles'
00205 [L285] MOV      A=14 B=0 C=12 D=12 
00206 [L285] TDUP     A=15 B=0 C=45 D=45 {'kind': 'table', 'value': {}}
00207 [L285] MULVN    A=16 B=2 C=2 D=514 
00208 [L285] ADDNV    A=16 B=16 C=1 D=4097 
00209 [L285] TSETS    A=16 B=15 C=31 D=3871 'x'
00210 [L285] MULVN    A=16 B=3 C=4 D=772 
00211 [L285] ADDNV    A=16 B=16 C=1 D=4097 
00212 [L285] TSETS    A=16 B=15 C=15 D=3855 'y'
00213 [L285] CALL     A=13 B=1 C=3 D=259 
00214 [L286] MOV      A=14 B=0 C=0 D=0 
00215 [L286] TGETS    A=13 B=0 C=6 D=6 'addChild'
00216 [L286] MOV      A=15 B=0 C=12 D=12 
00217 [L286] CALL     A=13 B=1 C=3 D=259 
00218 [L289] MULNV    A=13 B=3 C=5 D=773 
00219 [L290] KNUM     A=14 B=0 C=6 D=6 -0.02
00220 [L291] GGET     A=15 B=0 C=2 D=2 'd_ms'
00221 [L291] TGETS    A=15 B=15 C=46 D=3886 'd_hz'
00222 [L291] TGETS    A=15 B=15 C=47 D=3887 'gethz'
00223 [L291] KSTR     A=16 B=0 C=48 D=48 'twoyears_info7'
00224 [L291] CALL     A=15 B=2 C=2 D=514 
00225 [L292] GGET     A=16 B=0 C=2 D=2 'd_ms'
00226 [L292] TGETS    A=16 B=16 C=3 D=4099 'd_u'
00227 [L292] TGETS    A=16 B=16 C=36 D=4132 'createByStyles'
00228 [L292] TDUP     A=17 B=0 C=49 D=49 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 22}}
00229 [L292] MOV      A=18 B=0 C=15 D=15 
00230 [L292] TGETB    A=19 B=4 C=1 D=1025 
00231 [L292] TGETS    A=19 B=19 C=50 D=4914 'need_gold'
00232 [L292] CAT      A=18 B=18 C=19 D=4627 
00233 [L292] TSETS    A=18 B=17 C=38 D=4390 'string'
00234 [L292] GGET     A=18 B=0 C=39 D=39 'g_Color'
00235 [L292] TGETS    A=18 B=18 C=40 D=4648 'white'
00236 [L292] TSETS    A=18 B=17 C=41 D=4393 'color'
00237 [L292] CALL     A=16 B=2 C=2 D=514 
00238 [L293] GGET     A=17 B=0 C=2 D=2 'd_ms'
00239 [L293] TGETS    A=17 B=17 C=3 D=4355 'd_u'
00240 [L293] TGETS    A=17 B=17 C=4 D=4356 'setStyles'
00241 [L293] MOV      A=18 B=0 C=16 D=16 
00242 [L293] TDUP     A=19 B=0 C=51 D=51 {'kind': 'table', 'value': {}}
00243 [L293] MULVN    A=20 B=2 C=2 D=514 
00244 [L293] SUBNV    A=20 B=20 C=1 D=5121 
00245 [L293] ADDVV    A=20 B=20 C=14 D=5134 
00246 [L293] TSETS    A=20 B=19 C=31 D=4895 'x'
00247 [L293] MULVN    A=20 B=3 C=7 D=775 
00248 [L293] SUBNV    A=20 B=20 C=1 D=5121 
00249 [L293] TSETS    A=20 B=19 C=15 D=4879 'y'
00250 [L293] CALL     A=17 B=1 C=3 D=259 
00251 [L294] MOV      A=18 B=0 C=0 D=0 
00252 [L294] TGETS    A=17 B=0 C=6 D=6 'addChild'
00253 [L294] MOV      A=19 B=0 C=16 D=16 
00254 [L294] CALL     A=17 B=1 C=3 D=259 
00255 [L297] GGET     A=17 B=0 C=2 D=2 'd_ms'
00256 [L297] TGETS    A=17 B=17 C=3 D=4355 'd_u'
00257 [L297] TGETS    A=17 B=17 C=36 D=4388 'createByStyles'
00258 [L297] TDUP     A=18 B=0 C=52 D=52 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 22}}
00259 [L297] MOV      A=19 B=0 C=15 D=15 
00260 [L297] TGETB    A=20 B=4 C=2 D=1026 
00261 [L297] TGETS    A=20 B=20 C=50 D=5170 'need_gold'
00262 [L297] CAT      A=19 B=19 C=20 D=4884 
00263 [L297] TSETS    A=19 B=18 C=38 D=4646 'string'
00264 [L297] GGET     A=19 B=0 C=39 D=39 'g_Color'
00265 [L297] TGETS    A=19 B=19 C=40 D=4904 'white'
00266 [L297] TSETS    A=19 B=18 C=41 D=4649 'color'
00267 [L297] CALL     A=17 B=2 C=2 D=514 
00268 [L298] GGET     A=18 B=0 C=2 D=2 'd_ms'
00269 [L298] TGETS    A=18 B=18 C=3 D=4611 'd_u'
00270 [L298] TGETS    A=18 B=18 C=4 D=4612 'setStyles'
00271 [L298] MOV      A=19 B=0 C=17 D=17 
00272 [L298] TDUP     A=20 B=0 C=53 D=53 {'kind': 'table', 'value': {}}
00273 [L298] MULVN    A=21 B=2 C=2 D=514 
00274 [L298] ADDNV    A=21 B=21 C=1 D=5377 
00275 [L298] ADDVV    A=21 B=21 C=14 D=5390 
00276 [L298] TSETS    A=21 B=20 C=31 D=5151 'x'
00277 [L298] MULVN    A=21 B=3 C=7 D=775 
00278 [L298] SUBNV    A=21 B=21 C=1 D=5377 
00279 [L298] TSETS    A=21 B=20 C=15 D=5135 'y'
00280 [L298] CALL     A=18 B=1 C=3 D=259 
00281 [L299] MOV      A=19 B=0 C=0 D=0 
00282 [L299] TGETS    A=18 B=0 C=6 D=6 'addChild'
00283 [L299] MOV      A=20 B=0 C=17 D=17 
00284 [L299] CALL     A=18 B=1 C=3 D=259 
00285 [L303] UGET     A=18 B=0 C=0 D=0 CCSprite
00286 [L303] MOV      A=19 B=0 C=18 D=18 
00287 [L303] TGETS    A=18 B=18 C=0 D=4608 'create'
00288 [L303] KSTR     A=20 B=0 C=54 D=54 'v2/money_gold.png'
00289 [L303] CALL     A=18 B=2 C=3 D=515 
00290 [L303] GSET     A=18 B=0 C=55 D=55 'gold_icon'
00291 [L304] GGET     A=18 B=0 C=2 D=2 'd_ms'
00292 [L304] TGETS    A=18 B=18 C=3 D=4611 'd_u'
00293 [L304] TGETS    A=18 B=18 C=4 D=4612 'setStyles'
00294 [L304] GGET     A=19 B=0 C=55 D=55 'gold_icon'
00295 [L304] TDUP     A=20 B=0 C=56 D=56 {'kind': 'table', 'value': {}}
00296 [L304] MULVN    A=21 B=2 C=2 D=514 
00297 [L304] SUBNV    A=21 B=21 C=1 D=5377 
00298 [L304] ADDVV    A=21 B=21 C=14 D=5390 
00299 [L304] ADDVN    A=21 B=21 C=8 D=5384 
00300 [L304] TSETS    A=21 B=20 C=31 D=5151 'x'
00301 [L304] MULVN    A=21 B=3 C=7 D=775 
00302 [L304] SUBNV    A=21 B=21 C=1 D=5377 
00303 [L304] TSETS    A=21 B=20 C=15 D=5135 'y'
00304 [L304] CALL     A=18 B=1 C=3 D=259 
00305 [L305] MOV      A=19 B=0 C=0 D=0 
00306 [L305] TGETS    A=18 B=0 C=6 D=6 'addChild'
00307 [L305] GGET     A=20 B=0 C=55 D=55 'gold_icon'
00308 [L305] CALL     A=18 B=1 C=3 D=259 
00309 [L307] UGET     A=18 B=0 C=0 D=0 CCSprite
00310 [L307] MOV      A=19 B=0 C=18 D=18 
00311 [L307] TGETS    A=18 B=18 C=0 D=4608 'create'
00312 [L307] KSTR     A=20 B=0 C=54 D=54 'v2/money_gold.png'
00313 [L307] CALL     A=18 B=2 C=3 D=515 
00314 [L307] GSET     A=18 B=0 C=55 D=55 'gold_icon'
00315 [L308] GGET     A=18 B=0 C=2 D=2 'd_ms'
00316 [L308] TGETS    A=18 B=18 C=3 D=4611 'd_u'
00317 [L308] TGETS    A=18 B=18 C=4 D=4612 'setStyles'
00318 [L308] GGET     A=19 B=0 C=55 D=55 'gold_icon'
00319 [L308] TDUP     A=20 B=0 C=57 D=57 {'kind': 'table', 'value': {}}
00320 [L308] MULVN    A=21 B=2 C=2 D=514 
00321 [L308] ADDNV    A=21 B=21 C=1 D=5377 
00322 [L308] ADDVV    A=21 B=21 C=14 D=5390 
00323 [L308] ADDVN    A=21 B=21 C=8 D=5384 
00324 [L308] TSETS    A=21 B=20 C=31 D=5151 'x'
00325 [L308] MULVN    A=21 B=3 C=7 D=775 
00326 [L308] SUBNV    A=21 B=21 C=1 D=5377 
00327 [L308] TSETS    A=21 B=20 C=15 D=5135 'y'
00328 [L308] CALL     A=18 B=1 C=3 D=259 
00329 [L309] MOV      A=19 B=0 C=0 D=0 
00330 [L309] TGETS    A=18 B=0 C=6 D=6 'addChild'
00331 [L309] GGET     A=20 B=0 C=55 D=55 'gold_icon'
00332 [L309] CALL     A=18 B=1 C=3 D=259 
00333 [L314] UGET     A=18 B=0 C=2 D=2 table
00334 [L314] TGETS    A=18 B=18 C=27 D=4635 'insert'
00335 [L314] MOV      A=19 B=0 C=6 D=6 
00336 [L314] TDUP     A=20 B=0 C=58 D=58 {'kind': 'table', 'value': {'npic': 'v2/shopUI/buy_1.png', 'scale': 0.1, 'spic': 'v2/shopUI/buy_2.png', 'tag': 1}}
00337 [L314] MULVN    A=21 B=2 C=2 D=514 
00338 [L314] SUBNV    A=21 B=21 C=1 D=5377 
00339 [L314] TSETS    A=21 B=20 C=31 D=5151 'x'
00340 [L314] MULVN    A=21 B=3 C=9 D=777 
00341 [L314] SUBNV    A=21 B=21 C=1 D=5377 
00342 [L314] TSETS    A=21 B=20 C=15 D=5135 'y'
00343 [L314] GGET     A=21 B=0 C=59 D=59 'buy'
00344 [L314] TSETS    A=21 B=20 C=19 D=5139 'call_back'
00345 [L314] CALL     A=18 B=1 C=3 D=259 
00346 [L315] UGET     A=18 B=0 C=2 D=2 table
00347 [L315] TGETS    A=18 B=18 C=27 D=4635 'insert'
00348 [L315] MOV      A=19 B=0 C=6 D=6 
00349 [L315] TDUP     A=20 B=0 C=60 D=60 {'kind': 'table', 'value': {'npic': 'v2/shopUI/buy_1.png', 'scale': 0.1, 'spic': 'v2/shopUI/buy_2.png', 'tag': 2}}
00350 [L315] MULVN    A=21 B=2 C=2 D=514 
00351 [L315] ADDNV    A=21 B=21 C=1 D=5377 
00352 [L315] TSETS    A=21 B=20 C=31 D=5151 'x'
00353 [L315] MULVN    A=21 B=3 C=9 D=777 
00354 [L315] SUBNV    A=21 B=21 C=1 D=5377 
00355 [L315] TSETS    A=21 B=20 C=15 D=5135 'y'
00356 [L315] GGET     A=21 B=0 C=59 D=59 'buy'
00357 [L315] TSETS    A=21 B=20 C=19 D=5139 'call_back'
00358 [L315] CALL     A=18 B=1 C=3 D=259 
00359 [L318] GGET     A=18 B=0 C=2 D=2 'd_ms'
00360 [L318] TGETS    A=18 B=18 C=46 D=4654 'd_hz'
00361 [L318] TGETS    A=18 B=18 C=47 D=4655 'gethz'
00362 [L318] KSTR     A=19 B=0 C=61 D=61 'twoyears_info5'
00363 [L318] CALL     A=18 B=2 C=2 D=514 
00364 [L319] GGET     A=19 B=0 C=2 D=2 'd_ms'
00365 [L319] TGETS    A=19 B=19 C=3 D=4867 'd_u'
00366 [L319] TGETS    A=19 B=19 C=36 D=4900 'createByStyles'
00367 [L319] TDUP     A=20 B=0 C=62 D=62 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 22}}
00368 [L319] MOV      A=21 B=0 C=18 D=18 
00369 [L319] GGET     A=22 B=0 C=8 D=8 'g_self'
00370 [L319] UGET     A=23 B=0 C=1 D=1 y_o_t
00371 [L319] TGETS    A=23 B=23 C=11 D=5899 'enter_shop'
00372 [L319] TGETV    A=22 B=22 C=23 D=5655 
00373 [L319] TGETS    A=22 B=22 C=63 D=5695 'wish_times'
00374 [L319] CAT      A=21 B=21 C=22 D=5398 
00375 [L319] TSETS    A=21 B=20 C=38 D=5158 'string'
00376 [L319] GGET     A=21 B=0 C=39 D=39 'g_Color'
00377 [L319] TGETS    A=21 B=21 C=64 D=5440 'green'
00378 [L319] TSETS    A=21 B=20 C=41 D=5161 'color'
00379 [L319] CALL     A=19 B=2 C=2 D=514 
00380 [L320] GGET     A=20 B=0 C=2 D=2 'd_ms'
00381 [L320] TGETS    A=20 B=20 C=3 D=5123 'd_u'
00382 [L320] TGETS    A=20 B=20 C=4 D=5124 'setStyles'
00383 [L320] MOV      A=21 B=0 C=19 D=19 
00384 [L320] TDUP     A=22 B=0 C=65 D=65 {'kind': 'table', 'value': {'x': 0.5}}
00385 [L320] MULVN    A=23 B=3 C=10 D=778 
00386 [L320] SUBNV    A=23 B=23 C=1 D=5889 
00387 [L320] TSETS    A=23 B=22 C=15 D=5647 'y'
00388 [L320] CALL     A=20 B=1 C=3 D=259 
00389 [L321] MOV      A=21 B=0 C=0 D=0 
00390 [L321] TGETS    A=20 B=0 C=6 D=6 'addChild'
00391 [L321] MOV      A=22 B=0 C=19 D=19 
00392 [L321] CALL     A=20 B=1 C=3 D=259 
00393 [L324] GGET     A=20 B=0 C=2 D=2 'd_ms'
00394 [L324] TGETS    A=20 B=20 C=46 D=5166 'd_hz'
00395 [L324] TGETS    A=20 B=20 C=47 D=5167 'gethz'
00396 [L324] KSTR     A=21 B=0 C=66 D=66 'twoyears_info6'
00397 [L324] CALL     A=20 B=2 C=2 D=514 
00398 [L325] GGET     A=21 B=0 C=2 D=2 'd_ms'
00399 [L325] TGETS    A=21 B=21 C=3 D=5379 'd_u'
00400 [L325] TGETS    A=21 B=21 C=36 D=5412 'createByStyles'
00401 [L325] TDUP     A=22 B=0 C=67 D=67 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 22}}
00402 [L325] TSETS    A=20 B=22 C=38 D=5670 'string'
00403 [L325] GGET     A=23 B=0 C=39 D=39 'g_Color'
00404 [L325] TGETS    A=23 B=23 C=40 D=5928 'white'
00405 [L325] TSETS    A=23 B=22 C=41 D=5673 'color'
00406 [L325] CALL     A=21 B=2 C=2 D=514 
00407 [L326] GGET     A=22 B=0 C=2 D=2 'd_ms'
00408 [L326] TGETS    A=22 B=22 C=3 D=5635 'd_u'
00409 [L326] TGETS    A=22 B=22 C=4 D=5636 'setStyles'
00410 [L326] MOV      A=23 B=0 C=21 D=21 
00411 [L326] TDUP     A=24 B=0 C=68 D=68 {'kind': 'table', 'value': {'x': 0.5}}
00412 [L326] MULVN    A=25 B=3 C=11 D=779 
00413 [L326] SUBNV    A=25 B=25 C=1 D=6401 
00414 [L326] TSETS    A=25 B=24 C=15 D=6159 'y'
00415 [L326] CALL     A=22 B=1 C=3 D=259 
00416 [L327] MOV      A=23 B=0 C=0 D=0 
00417 [L327] TGETS    A=22 B=0 C=6 D=6 'addChild'
00418 [L327] MOV      A=24 B=0 C=21 D=21 
00419 [L327] CALL     A=22 B=1 C=3 D=259 
00420 [L329] GGET     A=22 B=0 C=69 D=69 'updateShopNews'
00421 [L329] MOV      A=23 B=0 C=0 D=0 
00422 [L329] UGET     A=24 B=0 C=1 D=1 y_o_t
00423 [L329] TGETS    A=24 B=24 C=11 D=6155 'enter_shop'
00424 [L329] CALL     A=22 B=1 C=3 D=259 
00425 [L330] MOV      A=23 B=0 C=0 D=0 
00426 [L330] TGETS    A=22 B=0 C=6 D=6 'addChild'
00427 [L330] GGET     A=24 B=0 C=2 D=2 'd_ms'
00428 [L330] TGETS    A=24 B=24 C=3 D=6147 'd_u'
00429 [L330] TGETS    A=24 B=24 C=70 D=6214 'createMenu'
00430 [L330] MOV      A=25 B=0 C=6 D=6 
00431 [L330] CALL     A=24 B=0 C=2 D=2 
00432 [L330] CALLM    A=22 B=1 C=1 D=257 
00433 [L331] UCLO     A=0 B=128 C=0 D=32768 target=434
00434 [L331] RET0     A=0 B=0 C=1 D=1 
00435 [L331] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto11 offset=0x1ffa source_lines=333-358 params=1
UPVALUES ['y_o_t']
00001 [L335] GGET     A=1 B=0 C=0 D=0 'g_self'
00002 [L335] TGETS    A=2 B=0 C=1 D=1 'flag'
00003 [L335] TSETV    A=0 B=1 C=2 D=258 
00004 [L336] TGETS    A=1 B=0 C=1 D=1 'flag'
00005 [L336] UGET     A=2 B=0 C=0 D=0 y_o_t
00006 [L336] TGETS    A=2 B=2 C=2 D=514 'enter_activity'
00007 [L336] ISNEV    A=1 B=0 C=2 D=2 
00008 [L336] JMP      A=1 B=128 C=3 D=32771 target=12
00009 [L337] GGET     A=1 B=0 C=3 D=3 'showNews'
00010 [L337] CALL     A=1 B=1 C=1 D=257 
00011 [L337] JMP      A=1 B=128 C=94 D=32862 target=106
00012 [L338] TGETS    A=1 B=0 C=1 D=1 'flag'
00013 [L338] UGET     A=2 B=0 C=0 D=0 y_o_t
00014 [L338] TGETS    A=2 B=2 C=4 D=516 'enter_shop'
00015 [L338] ISNEV    A=1 B=0 C=2 D=2 
00016 [L338] JMP      A=1 B=128 C=14 D=32782 target=31
00017 [L339] GGET     A=1 B=0 C=0 D=0 'g_self'
00018 [L339] GGET     A=2 B=0 C=6 D=6 'd_ms'
00019 [L339] TGETS    A=2 B=2 C=7 D=519 'd_u'
00020 [L339] TGETS    A=2 B=2 C=8 D=520 'createSwallowTouchLayer'
00021 [L339] GGET     A=3 B=0 C=0 D=0 'g_self'
00022 [L339] TGETS    A=3 B=3 C=9 D=777 'main_layer'
00023 [L339] KSHORT   A=4 B=0 C=200 D=200 200
00024 [L339] CALL     A=2 B=2 C=3 D=515 
00025 [L339] TSETS    A=2 B=1 C=5 D=261 'shoplayer'
00026 [L340] GGET     A=1 B=0 C=10 D=10 'showShop'
00027 [L340] GGET     A=2 B=0 C=0 D=0 'g_self'
00028 [L340] TGETS    A=2 B=2 C=5 D=517 'shoplayer'
00029 [L340] CALL     A=1 B=1 C=2 D=258 
00030 [L340] JMP      A=1 B=128 C=75 D=32843 target=106
00031 [L341] TGETS    A=1 B=0 C=1 D=1 'flag'
00032 [L341] UGET     A=2 B=0 C=0 D=0 y_o_t
00033 [L341] TGETS    A=2 B=2 C=11 D=523 'buy_shop'
00034 [L341] ISNEV    A=1 B=0 C=2 D=2 
00035 [L341] JMP      A=1 B=128 C=14 D=32782 target=50
00036 [L343] GGET     A=1 B=0 C=6 D=6 'd_ms'
00037 [L343] TGETS    A=1 B=1 C=12 D=268 'd_commonLayerUI'
00038 [L343] TGETS    A=1 B=1 C=13 D=269 'showPrizeResLayer'
00039 [L343] GGET     A=2 B=0 C=0 D=0 'g_self'
00040 [L343] TGETS    A=2 B=2 C=5 D=517 'shoplayer'
00041 [L343] TGETS    A=3 B=0 C=14 D=14 'shop_list'
00042 [L343] CALL     A=1 B=1 C=3 D=259 
00043 [L344] GGET     A=1 B=0 C=15 D=15 'updateShopNews'
00044 [L344] GGET     A=2 B=0 C=0 D=0 'g_self'
00045 [L344] TGETS    A=2 B=2 C=5 D=517 'shoplayer'
00046 [L344] UGET     A=3 B=0 C=0 D=0 y_o_t
00047 [L344] TGETS    A=3 B=3 C=11 D=779 'buy_shop'
00048 [L344] CALL     A=1 B=1 C=3 D=259 
00049 [L344] JMP      A=1 B=128 C=56 D=32824 target=106
00050 [L346] TGETS    A=1 B=0 C=1 D=1 'flag'
00051 [L346] UGET     A=2 B=0 C=0 D=0 y_o_t
00052 [L346] TGETS    A=2 B=2 C=16 D=528 'take_prize'
00053 [L346] ISNEV    A=1 B=0 C=2 D=2 
00054 [L346] JMP      A=1 B=128 C=16 D=32784 target=71
00055 [L348] GGET     A=1 B=0 C=0 D=0 'g_self'
00056 [L348] UGET     A=2 B=0 C=0 D=0 y_o_t
00057 [L348] TGETS    A=2 B=2 C=2 D=514 'enter_activity'
00058 [L348] TGETV    A=1 B=1 C=2 D=258 
00059 [L348] TGETS    A=2 B=0 C=17 D=17 'gift_list'
00060 [L348] TSETS    A=2 B=1 C=17 D=273 'gift_list'
00061 [L349] GGET     A=1 B=0 C=3 D=3 'showNews'
00062 [L349] CALL     A=1 B=1 C=1 D=257 
00063 [L350] GGET     A=1 B=0 C=6 D=6 'd_ms'
00064 [L350] TGETS    A=1 B=1 C=12 D=268 'd_commonLayerUI'
00065 [L350] TGETS    A=1 B=1 C=13 D=269 'showPrizeResLayer'
00066 [L350] GGET     A=2 B=0 C=0 D=0 'g_self'
00067 [L350] TGETS    A=2 B=2 C=9 D=521 'main_layer'
00068 [L350] TGETS    A=3 B=0 C=18 D=18 'prize_list'
00069 [L350] CALL     A=1 B=1 C=3 D=259 
00070 [L350] JMP      A=1 B=128 C=35 D=32803 target=106
00071 [L351] TGETS    A=1 B=0 C=1 D=1 'flag'
00072 [L351] UGET     A=2 B=0 C=0 D=0 y_o_t
00073 [L351] TGETS    A=2 B=2 C=19 D=531 'wish_yuanshi'
00074 [L351] ISNEV    A=1 B=0 C=2 D=2 
00075 [L351] JMP      A=1 B=128 C=30 D=32798 target=106
00076 [L352] GGET     A=1 B=0 C=0 D=0 'g_self'
00077 [L352] UGET     A=2 B=0 C=0 D=0 y_o_t
00078 [L352] TGETS    A=2 B=2 C=2 D=514 'enter_activity'
00079 [L352] TGETV    A=1 B=1 C=2 D=258 
00080 [L352] TGETS    A=2 B=0 C=20 D=20 'cur_progress'
00081 [L352] TSETS    A=2 B=1 C=20 D=276 'cur_progress'
00082 [L353] GGET     A=1 B=0 C=0 D=0 'g_self'
00083 [L353] UGET     A=2 B=0 C=0 D=0 y_o_t
00084 [L353] TGETS    A=2 B=2 C=2 D=514 'enter_activity'
00085 [L353] TGETV    A=1 B=1 C=2 D=258 
00086 [L353] TGETS    A=2 B=0 C=21 D=21 'free_times'
00087 [L353] TSETS    A=2 B=1 C=21 D=277 'free_times'
00088 [L354] GGET     A=1 B=0 C=6 D=6 'd_ms'
00089 [L354] TGETS    A=1 B=1 C=22 D=278 'd_info'
00090 [L354] TGETS    A=1 B=1 C=23 D=279 'show'
00091 [L354] GGET     A=2 B=0 C=6 D=6 'd_ms'
00092 [L354] TGETS    A=2 B=2 C=24 D=536 'd_hz'
00093 [L354] TGETS    A=2 B=2 C=25 D=537 'gethz'
00094 [L354] KSTR     A=3 B=0 C=26 D=26 'twoyears_info11'
00095 [L354] CALL     A=2 B=0 C=2 D=2 
00096 [L354] CALLM    A=1 B=1 C=0 D=256 
00097 [L355] GGET     A=1 B=0 C=3 D=3 'showNews'
00098 [L355] CALL     A=1 B=1 C=1 D=257 
00099 [L356] GGET     A=1 B=0 C=6 D=6 'd_ms'
00100 [L356] TGETS    A=1 B=1 C=12 D=268 'd_commonLayerUI'
00101 [L356] TGETS    A=1 B=1 C=13 D=269 'showPrizeResLayer'
00102 [L356] GGET     A=2 B=0 C=0 D=0 'g_self'
00103 [L356] TGETS    A=2 B=2 C=9 D=521 'main_layer'
00104 [L356] TGETS    A=3 B=0 C=18 D=18 'prize_list'
00105 [L356] CALL     A=1 B=1 C=3 D=259 
00106 [L358] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto12 offset=0x234d source_lines=359-381 params=2
UPVALUES []
00001 [L362] GGET     A=2 B=0 C=0 D=0 'd_ms'
00002 [L362] TGETS    A=2 B=2 C=1 D=513 'd_u'
00003 [L362] TGETS    A=2 B=2 C=2 D=514 'clearLayer'
00004 [L362] MOV      A=3 B=0 C=0 D=0 
00005 [L362] KSHORT   A=4 B=0 C=1 D=1 1
00006 [L362] GGET     A=5 B=0 C=3 D=3 'g_self'
00007 [L362] TGETS    A=5 B=5 C=4 D=1284 'shopTag'
00008 [L362] CALL     A=2 B=2 C=4 D=516 
00009 [L363] IST      A=0 B=0 C=2 D=2 
00010 [L363] JMP      A=3 B=128 C=1 D=32769 target=12
00011 [L364] RET0     A=0 B=0 C=1 D=1 
00012 [L367] GGET     A=3 B=0 C=3 D=3 'g_self'
00013 [L367] TGETV    A=3 B=3 C=1 D=769 
00014 [L367] TGETS    A=3 B=3 C=5 D=773 'shop_config'
00015 [L368] IST      A=0 B=0 C=3 D=3 
00016 [L368] JMP      A=4 B=128 C=1 D=32769 target=18
00017 [L369] RET0     A=0 B=0 C=1 D=1 
00018 [L373] GGET     A=4 B=0 C=0 D=0 'd_ms'
00019 [L373] TGETS    A=4 B=4 C=6 D=1030 'd_hz'
00020 [L373] TGETS    A=4 B=4 C=7 D=1031 'gethz'
00021 [L373] KSTR     A=5 B=0 C=8 D=8 'twoyears_info4'
00022 [L373] CALL     A=4 B=2 C=2 D=514 
00023 [L374] GGET     A=5 B=0 C=0 D=0 'd_ms'
00024 [L374] TGETS    A=5 B=5 C=1 D=1281 'd_u'
00025 [L374] TGETS    A=5 B=5 C=9 D=1289 'createByStyles'
00026 [L374] TDUP     A=6 B=0 C=10 D=10 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 22}}
00027 [L374] MOV      A=7 B=0 C=4 D=4 
00028 [L374] TGETB    A=8 B=3 C=1 D=769 
00029 [L374] TGETS    A=8 B=8 C=11 D=2059 'buy_times'
00030 [L374] CAT      A=7 B=7 C=8 D=1800 
00031 [L374] TSETS    A=7 B=6 C=12 D=1548 'string'
00032 [L374] GGET     A=7 B=0 C=13 D=13 'g_Color'
00033 [L374] TGETS    A=7 B=7 C=14 D=1806 'green'
00034 [L374] TSETS    A=7 B=6 C=15 D=1551 'color'
00035 [L374] CALL     A=5 B=2 C=2 D=514 
00036 [L375] GGET     A=6 B=0 C=0 D=0 'd_ms'
00037 [L375] TGETS    A=6 B=6 C=1 D=1537 'd_u'
00038 [L375] TGETS    A=6 B=6 C=16 D=1552 'setStyles'
00039 [L375] MOV      A=7 B=0 C=5 D=5 
00040 [L375] TDUP     A=8 B=0 C=18 D=18 {'kind': 'table', 'value': {}}
00041 [L375] GGET     A=9 B=0 C=3 D=3 'g_self'
00042 [L375] TGETS    A=9 B=9 C=17 D=2321 'shop_w'
00043 [L375] MULVN    A=9 B=9 C=0 D=2304 
00044 [L375] SUBNV    A=9 B=9 C=1 D=2305 
00045 [L375] TSETS    A=9 B=8 C=19 D=2067 'x'
00046 [L375] GGET     A=9 B=0 C=3 D=3 'g_self'
00047 [L375] TGETS    A=9 B=9 C=20 D=2324 'shop_h'
00048 [L375] MULVN    A=9 B=9 C=2 D=2306 
00049 [L375] SUBNV    A=9 B=9 C=1 D=2305 
00050 [L375] TSETS    A=9 B=8 C=21 D=2069 'y'
00051 [L375] CALL     A=6 B=1 C=3 D=259 
00052 [L376] MOV      A=7 B=0 C=2 D=2 
00053 [L376] TGETS    A=6 B=2 C=22 D=534 'addChild'
00054 [L376] MOV      A=8 B=0 C=5 D=5 
00055 [L376] CALL     A=6 B=1 C=3 D=259 
00056 [L378] GGET     A=6 B=0 C=0 D=0 'd_ms'
00057 [L378] TGETS    A=6 B=6 C=1 D=1537 'd_u'
00058 [L378] TGETS    A=6 B=6 C=9 D=1545 'createByStyles'
00059 [L378] TDUP     A=7 B=0 C=23 D=23 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 22}}
00060 [L378] MOV      A=8 B=0 C=4 D=4 
00061 [L378] TGETB    A=9 B=3 C=2 D=770 
00062 [L378] TGETS    A=9 B=9 C=11 D=2315 'buy_times'
00063 [L378] CAT      A=8 B=8 C=9 D=2057 
00064 [L378] TSETS    A=8 B=7 C=12 D=1804 'string'
00065 [L378] GGET     A=8 B=0 C=13 D=13 'g_Color'
00066 [L378] TGETS    A=8 B=8 C=14 D=2062 'green'
00067 [L378] TSETS    A=8 B=7 C=15 D=1807 'color'
00068 [L378] CALL     A=6 B=2 C=2 D=514 
00069 [L379] GGET     A=7 B=0 C=0 D=0 'd_ms'
00070 [L379] TGETS    A=7 B=7 C=1 D=1793 'd_u'
00071 [L379] TGETS    A=7 B=7 C=16 D=1808 'setStyles'
00072 [L379] MOV      A=8 B=0 C=6 D=6 
00073 [L379] TDUP     A=9 B=0 C=24 D=24 {'kind': 'table', 'value': {}}
00074 [L379] GGET     A=10 B=0 C=3 D=3 'g_self'
00075 [L379] TGETS    A=10 B=10 C=17 D=2577 'shop_w'
00076 [L379] MULVN    A=10 B=10 C=0 D=2560 
00077 [L379] ADDNV    A=10 B=10 C=1 D=2561 
00078 [L379] TSETS    A=10 B=9 C=19 D=2323 'x'
00079 [L379] GGET     A=10 B=0 C=3 D=3 'g_self'
00080 [L379] TGETS    A=10 B=10 C=20 D=2580 'shop_h'
00081 [L379] MULVN    A=10 B=10 C=2 D=2562 
00082 [L379] SUBNV    A=10 B=10 C=1 D=2561 
00083 [L379] TSETS    A=10 B=9 C=21 D=2325 'y'
00084 [L379] CALL     A=7 B=1 C=3 D=259 
00085 [L380] MOV      A=8 B=0 C=2 D=2 
00086 [L380] TGETS    A=7 B=2 C=22 D=534 'addChild'
00087 [L380] MOV      A=9 B=0 C=6 D=6 
00088 [L380] CALL     A=7 B=1 C=3 D=259 
00089 [L381] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto13 offset=0x2668 source_lines=383-533 params=0
UPVALUES ['CCSprite', 'scrSize', 'CCRectMake', 'CCPointMake', 'string', 'o_t', 'y_o_t', 'table']
00001 [L384] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L384] TGETS    A=0 B=0 C=1 D=1 'd_u'
00003 [L384] TGETS    A=0 B=0 C=2 D=2 'clearLayer'
00004 [L384] GGET     A=1 B=0 C=3 D=3 'g_self'
00005 [L384] TGETS    A=1 B=1 C=4 D=260 'main_layer'
00006 [L384] KSHORT   A=2 B=0 C=1 D=1 1
00007 [L384] GGET     A=3 B=0 C=3 D=3 'g_self'
00008 [L384] TGETS    A=3 B=3 C=5 D=773 'newTag'
00009 [L384] CALL     A=0 B=2 C=4 D=516 
00010 [L385] IST      A=0 B=0 C=0 D=0 
00011 [L385] JMP      A=1 B=128 C=1 D=32769 target=13
00012 [L386] RET0     A=0 B=0 C=1 D=1 
00013 [L388] GGET     A=1 B=0 C=3 D=3 'g_self'
00014 [L388] TGETB    A=1 B=1 C=0 D=256 
00015 [L388] IST      A=0 B=0 C=1 D=1 
00016 [L388] JMP      A=1 B=128 C=1 D=32769 target=18
00017 [L389] RET0     A=0 B=0 C=1 D=1 
00018 [L391] GGET     A=1 B=0 C=3 D=3 'g_self'
00019 [L391] TGETB    A=1 B=1 C=0 D=256 
00020 [L391] TGETS    A=1 B=1 C=6 D=262 'cur_progress'
00021 [L391] IST      A=0 B=0 C=1 D=1 
00022 [L391] JMP      A=2 B=128 C=1 D=32769 target=24
00023 [L391] KSHORT   A=1 B=0 C=0 D=0 0
00024 [L391] GSET     A=1 B=0 C=7 D=7 'percent'
00025 [L392] GGET     A=1 B=0 C=3 D=3 'g_self'
00026 [L392] TGETB    A=1 B=1 C=0 D=256 
00027 [L392] TGETS    A=1 B=1 C=8 D=264 'free_times'
00028 [L392] IST      A=0 B=0 C=1 D=1 
00029 [L392] JMP      A=2 B=128 C=1 D=32769 target=31
00030 [L392] KSHORT   A=1 B=0 C=0 D=0 0
00031 [L392] GSET     A=1 B=0 C=8 D=8 'free_times'
00032 [L394] GGET     A=1 B=0 C=9 D=9 'w'
00033 [L394] MULNV    A=1 B=1 C=0 D=256 
00034 [L394] GSET     A=1 B=0 C=10 D=10 'sx'
00035 [L397] GGET     A=1 B=0 C=7 D=7 'percent'
00036 [L397] DIVVN    A=1 B=1 C=1 D=257 
00037 [L397] MULVN    A=1 B=1 C=2 D=258 
00038 [L397] ADDVN    A=1 B=1 C=3 D=259 
00039 [L397] SUBNV    A=1 B=1 C=4 D=260 
00040 [L398] KSHORT   A=2 B=0 C=0 D=0 0
00041 [L398] ISGE     A=1 B=0 C=2 D=2 
00042 [L398] JMP      A=2 B=128 C=1 D=32769 target=44
00043 [L399] KSHORT   A=1 B=0 C=0 D=0 0
00044 [L401] KSHORT   A=2 B=0 C=1 D=1 1
00045 [L401] ISGE     A=2 B=0 C=1 D=1 
00046 [L401] JMP      A=2 B=128 C=1 D=32769 target=48
00047 [L402] KSHORT   A=1 B=0 C=1 D=1 1
00048 [L405] UGET     A=2 B=0 C=0 D=0 CCSprite
00049 [L405] MOV      A=3 B=0 C=2 D=2 
00050 [L405] TGETS    A=2 B=2 C=11 D=523 'create'
00051 [L405] KSTR     A=4 B=0 C=12 D=12 'v2/twoYearsCelebrateUI/char.png'
00052 [L405] CALL     A=2 B=2 C=3 D=515 
00053 [L406] GGET     A=3 B=0 C=0 D=0 'd_ms'
00054 [L406] TGETS    A=3 B=3 C=1 D=769 'd_u'
00055 [L406] TGETS    A=3 B=3 C=13 D=781 'getRealScale'
00056 [L406] MOV      A=4 B=0 C=2 D=2 
00057 [L406] CALL     A=3 B=3 C=2 D=770 
00058 [L407] MOV      A=6 B=0 C=2 D=2 
00059 [L407] TGETS    A=5 B=2 C=14 D=526 'getContentSize'
00060 [L407] CALL     A=5 B=2 C=2 D=514 
00061 [L408] TGETS    A=6 B=5 C=15 D=1295 'height'
00062 [L408] MULVV    A=6 B=6 C=1 D=1537 
00063 [L408] UGET     A=7 B=0 C=1 D=1 scrSize
00064 [L408] TGETS    A=7 B=7 C=15 D=1807 'height'
00065 [L408] DIVVV    A=6 B=6 C=7 D=1543 
00066 [L408] SUBNV    A=6 B=6 C=5 D=1541 
00067 [L411] UGET     A=7 B=0 C=0 D=0 CCSprite
00068 [L411] MOV      A=8 B=0 C=7 D=7 
00069 [L411] TGETS    A=7 B=7 C=11 D=1803 'create'
00070 [L411] KSTR     A=9 B=0 C=12 D=12 'v2/twoYearsCelebrateUI/char.png'
00071 [L411] UGET     A=10 B=0 C=2 D=2 CCRectMake
00072 [L411] KSHORT   A=11 B=0 C=0 D=0 0
00073 [L411] TGETS    A=12 B=5 C=15 D=1295 'height'
00074 [L411] MULVV    A=12 B=12 C=1 D=3073 
00075 [L411] TGETS    A=13 B=5 C=16 D=1296 'width'
00076 [L411] TGETS    A=14 B=5 C=15 D=1295 'height'
00077 [L411] CALL     A=10 B=0 C=5 D=5 
00078 [L411] CALLM    A=7 B=2 C=2 D=514 
00079 [L412] GGET     A=8 B=0 C=0 D=0 'd_ms'
00080 [L412] TGETS    A=8 B=8 C=1 D=2049 'd_u'
00081 [L412] TGETS    A=8 B=8 C=17 D=2065 'setStyles'
00082 [L412] MOV      A=9 B=0 C=7 D=7 
00083 [L412] TDUP     A=10 B=0 C=18 D=18 {'kind': 'table', 'value': {'x': 0.5}}
00084 [L412] TSETS    A=6 B=10 C=19 D=2579 'y'
00085 [L412] CALL     A=8 B=1 C=3 D=259 
00086 [L413] MOV      A=9 B=0 C=7 D=7 
00087 [L413] TGETS    A=8 B=7 C=20 D=1812 'setAnchorPoint'
00088 [L413] UGET     A=10 B=0 C=3 D=3 CCPointMake
00089 [L413] KNUM     A=11 B=0 C=6 D=6 0.5
00090 [L413] KSHORT   A=12 B=0 C=1 D=1 1
00091 [L413] CALL     A=10 B=0 C=3 D=3 
00092 [L413] CALLM    A=8 B=1 C=1 D=257 
00093 [L414] MOV      A=9 B=0 C=0 D=0 
00094 [L414] TGETS    A=8 B=0 C=21 D=21 'addChild'
00095 [L414] MOV      A=10 B=0 C=7 D=7 
00096 [L414] CALL     A=8 B=1 C=3 D=259 
00097 [L417] UGET     A=8 B=0 C=0 D=0 CCSprite
00098 [L417] MOV      A=9 B=0 C=8 D=8 
00099 [L417] TGETS    A=8 B=8 C=11 D=2059 'create'
00100 [L417] KSTR     A=10 B=0 C=22 D=22 'v2/twoYearsCelebrateUI/char2.png'
00101 [L417] UGET     A=11 B=0 C=2 D=2 CCRectMake
00102 [L417] KSHORT   A=12 B=0 C=0 D=0 0
00103 [L417] KSHORT   A=13 B=0 C=0 D=0 0
00104 [L417] TGETS    A=14 B=5 C=16 D=1296 'width'
00105 [L417] TGETS    A=15 B=5 C=15 D=1295 'height'
00106 [L417] MULVV    A=15 B=15 C=1 D=3841 
00107 [L417] CALL     A=11 B=0 C=5 D=5 
00108 [L417] CALLM    A=8 B=2 C=2 D=514 
00109 [L418] GGET     A=9 B=0 C=0 D=0 'd_ms'
00110 [L418] TGETS    A=9 B=9 C=1 D=2305 'd_u'
00111 [L418] TGETS    A=9 B=9 C=17 D=2321 'setStyles'
00112 [L418] MOV      A=10 B=0 C=8 D=8 
00113 [L418] TDUP     A=11 B=0 C=23 D=23 {'kind': 'table', 'value': {'x': 0.5}}
00114 [L418] TSETS    A=6 B=11 C=19 D=2835 'y'
00115 [L418] CALL     A=9 B=1 C=3 D=259 
00116 [L419] MOV      A=10 B=0 C=8 D=8 
00117 [L419] TGETS    A=9 B=8 C=20 D=2068 'setAnchorPoint'
00118 [L419] UGET     A=11 B=0 C=3 D=3 CCPointMake
00119 [L419] KNUM     A=12 B=0 C=6 D=6 0.5
00120 [L419] KSHORT   A=13 B=0 C=0 D=0 0
00121 [L419] CALL     A=11 B=0 C=3 D=3 
00122 [L419] CALLM    A=9 B=1 C=1 D=257 
00123 [L420] MOV      A=10 B=0 C=0 D=0 
00124 [L420] TGETS    A=9 B=0 C=21 D=21 'addChild'
00125 [L420] MOV      A=11 B=0 C=8 D=8 
00126 [L420] CALL     A=9 B=1 C=3 D=259 
00127 [L425] UGET     A=9 B=0 C=0 D=0 CCSprite
00128 [L425] MOV      A=10 B=0 C=9 D=9 
00129 [L425] TGETS    A=9 B=9 C=11 D=2315 'create'
00130 [L425] KSTR     A=11 B=0 C=24 D=24 'v2/twoYearsCelebrateUI/progress.png'
00131 [L425] CALL     A=9 B=2 C=3 D=515 
00132 [L426] GGET     A=10 B=0 C=0 D=0 'd_ms'
00133 [L426] TGETS    A=10 B=10 C=1 D=2561 'd_u'
00134 [L426] TGETS    A=10 B=10 C=17 D=2577 'setStyles'
00135 [L426] MOV      A=11 B=0 C=9 D=9 
00136 [L426] TDUP     A=12 B=0 C=25 D=25 {'kind': 'table', 'value': {'x': 0.5, 'y': 0.32}}
00137 [L426] CALL     A=10 B=1 C=3 D=259 
00138 [L427] MOV      A=11 B=0 C=0 D=0 
00139 [L427] TGETS    A=10 B=0 C=21 D=21 'addChild'
00140 [L427] MOV      A=12 B=0 C=9 D=9 
00141 [L427] CALL     A=10 B=1 C=3 D=259 
00142 [L429] GGET     A=10 B=0 C=0 D=0 'd_ms'
00143 [L429] TGETS    A=10 B=10 C=26 D=2586 'd_hz'
00144 [L429] TGETS    A=10 B=10 C=27 D=2587 'gethz'
00145 [L429] KSTR     A=11 B=0 C=28 D=28 'twoyears_info1'
00146 [L429] CALL     A=10 B=2 C=2 D=514 
00147 [L429] GSET     A=10 B=0 C=29 D=29 'str'
00148 [L430] GGET     A=10 B=0 C=0 D=0 'd_ms'
00149 [L430] TGETS    A=10 B=10 C=1 D=2561 'd_u'
00150 [L430] TGETS    A=10 B=10 C=30 D=2590 'createByStyles'
00151 [L430] TDUP     A=11 B=0 C=31 D=31 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 22}}
00152 [L430] UGET     A=12 B=0 C=4 D=4 string
00153 [L430] TGETS    A=12 B=12 C=32 D=3104 'format'
00154 [L430] GGET     A=13 B=0 C=29 D=29 'str'
00155 [L430] GGET     A=14 B=0 C=7 D=7 'percent'
00156 [L430] CALL     A=12 B=2 C=3 D=515 
00157 [L430] TSETS    A=12 B=11 C=33 D=2849 'string'
00158 [L430] GGET     A=12 B=0 C=34 D=34 'g_Color'
00159 [L430] TGETS    A=12 B=12 C=35 D=3107 'white'
00160 [L430] TSETS    A=12 B=11 C=36 D=2852 'color'
00161 [L430] CALL     A=10 B=2 C=2 D=514 
00162 [L431] MOV      A=12 B=0 C=0 D=0 
00163 [L431] TGETS    A=11 B=0 C=21 D=21 'addChild'
00164 [L431] MOV      A=13 B=0 C=10 D=10 
00165 [L431] CALL     A=11 B=1 C=3 D=259 
00166 [L432] GGET     A=11 B=0 C=0 D=0 'd_ms'
00167 [L432] TGETS    A=11 B=11 C=1 D=2817 'd_u'
00168 [L432] TGETS    A=11 B=11 C=17 D=2833 'setStyles'
00169 [L432] MOV      A=12 B=0 C=10 D=10 
00170 [L432] TDUP     A=13 B=0 C=37 D=37 {'kind': 'table', 'value': {'x': 0.5, 'y': 0.32}}
00171 [L432] CALL     A=11 B=1 C=3 D=259 
00172 [L436] UGET     A=11 B=0 C=0 D=0 CCSprite
00173 [L436] MOV      A=12 B=0 C=11 D=11 
00174 [L436] TGETS    A=11 B=11 C=11 D=2827 'create'
00175 [L436] KSTR     A=13 B=0 C=38 D=38 'v2/twoYearsCelebrateUI/free.png'
00176 [L436] CALL     A=11 B=2 C=3 D=515 
00177 [L437] GGET     A=12 B=0 C=0 D=0 'd_ms'
00178 [L437] TGETS    A=12 B=12 C=1 D=3073 'd_u'
00179 [L437] TGETS    A=12 B=12 C=17 D=3089 'setStyles'
00180 [L437] MOV      A=13 B=0 C=11 D=11 
00181 [L437] TDUP     A=14 B=0 C=39 D=39 {'kind': 'table', 'value': {'x': 0.8, 'y': 0.32}}
00182 [L437] CALL     A=12 B=1 C=3 D=259 
00183 [L438] MOV      A=13 B=0 C=0 D=0 
00184 [L438] TGETS    A=12 B=0 C=21 D=21 'addChild'
00185 [L438] MOV      A=14 B=0 C=11 D=11 
00186 [L438] CALL     A=12 B=1 C=3 D=259 
00187 [L440] GGET     A=12 B=0 C=8 D=8 'free_times'
00188 [L440] KSHORT   A=13 B=0 C=0 D=0 0
00189 [L440] ISGE     A=13 B=0 C=12 D=12 
00190 [L440] JMP      A=12 B=128 C=29 D=32797 target=220
00191 [L441] GGET     A=12 B=0 C=0 D=0 'd_ms'
00192 [L441] TGETS    A=12 B=12 C=26 D=3098 'd_hz'
00193 [L441] TGETS    A=12 B=12 C=27 D=3099 'gethz'
00194 [L441] KSTR     A=13 B=0 C=40 D=40 'twoyears_info2'
00195 [L441] CALL     A=12 B=2 C=2 D=514 
00196 [L441] GSET     A=12 B=0 C=29 D=29 'str'
00197 [L442] GGET     A=12 B=0 C=0 D=0 'd_ms'
00198 [L442] TGETS    A=12 B=12 C=1 D=3073 'd_u'
00199 [L442] TGETS    A=12 B=12 C=30 D=3102 'createByStyles'
00200 [L442] TDUP     A=13 B=0 C=41 D=41 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 22}}
00201 [L442] GGET     A=14 B=0 C=29 D=29 'str'
00202 [L442] GGET     A=15 B=0 C=8 D=8 'free_times'
00203 [L442] CAT      A=14 B=14 C=15 D=3599 
00204 [L442] TSETS    A=14 B=13 C=33 D=3361 'string'
00205 [L442] GGET     A=14 B=0 C=34 D=34 'g_Color'
00206 [L442] TGETS    A=14 B=14 C=35 D=3619 'white'
00207 [L442] TSETS    A=14 B=13 C=36 D=3364 'color'
00208 [L442] CALL     A=12 B=2 C=2 D=514 
00209 [L443] GGET     A=13 B=0 C=0 D=0 'd_ms'
00210 [L443] TGETS    A=13 B=13 C=1 D=3329 'd_u'
00211 [L443] TGETS    A=13 B=13 C=17 D=3345 'setStyles'
00212 [L443] MOV      A=14 B=0 C=12 D=12 
00213 [L443] TDUP     A=15 B=0 C=42 D=42 {'kind': 'table', 'value': {'x': 0.8, 'y': 0.32}}
00214 [L443] CALL     A=13 B=1 C=3 D=259 
00215 [L444] MOV      A=14 B=0 C=0 D=0 
00216 [L444] TGETS    A=13 B=0 C=21 D=21 'addChild'
00217 [L444] MOV      A=15 B=0 C=12 D=12 
00218 [L444] CALL     A=13 B=1 C=3 D=259 
00219 [L444] JMP      A=12 B=128 C=35 D=32803 target=255
00220 [L446] GGET     A=12 B=0 C=0 D=0 'd_ms'
00221 [L446] TGETS    A=12 B=12 C=43 D=3115 'd_smithUI'
00222 [L446] TGETS    A=12 B=12 C=44 D=3116 'getMaterialCount'
00223 [L446] UGET     A=13 B=0 C=5 D=5 o_t
00224 [L446] TGETS    A=13 B=13 C=45 D=3373 'item'
00225 [L446] KSHORT   A=14 B=7 C=15 D=1807 1807
00226 [L446] CALL     A=12 B=2 C=3 D=515 
00227 [L447] GGET     A=13 B=0 C=0 D=0 'd_ms'
00228 [L447] TGETS    A=13 B=13 C=26 D=3354 'd_hz'
00229 [L447] TGETS    A=13 B=13 C=27 D=3355 'gethz'
00230 [L447] KSTR     A=14 B=0 C=46 D=46 'twoyears_info13'
00231 [L447] CALL     A=13 B=2 C=2 D=514 
00232 [L447] GSET     A=13 B=0 C=29 D=29 'str'
00233 [L448] GGET     A=13 B=0 C=0 D=0 'd_ms'
00234 [L448] TGETS    A=13 B=13 C=1 D=3329 'd_u'
00235 [L448] TGETS    A=13 B=13 C=30 D=3358 'createByStyles'
00236 [L448] TDUP     A=14 B=0 C=47 D=47 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 22}}
00237 [L448] GGET     A=15 B=0 C=29 D=29 'str'
00238 [L448] MOV      A=16 B=0 C=12 D=12 
00239 [L448] CAT      A=15 B=15 C=16 D=3856 
00240 [L448] TSETS    A=15 B=14 C=33 D=3617 'string'
00241 [L448] GGET     A=15 B=0 C=34 D=34 'g_Color'
00242 [L448] TGETS    A=15 B=15 C=35 D=3875 'white'
00243 [L448] TSETS    A=15 B=14 C=36 D=3620 'color'
00244 [L448] CALL     A=13 B=2 C=2 D=514 
00245 [L449] GGET     A=14 B=0 C=0 D=0 'd_ms'
00246 [L449] TGETS    A=14 B=14 C=1 D=3585 'd_u'
00247 [L449] TGETS    A=14 B=14 C=17 D=3601 'setStyles'
00248 [L449] MOV      A=15 B=0 C=13 D=13 
00249 [L449] TDUP     A=16 B=0 C=48 D=48 {'kind': 'table', 'value': {'x': 0.8, 'y': 0.32}}
00250 [L449] CALL     A=14 B=1 C=3 D=259 
00251 [L450] MOV      A=15 B=0 C=0 D=0 
00252 [L450] TGETS    A=14 B=0 C=21 D=21 'addChild'
00253 [L450] MOV      A=16 B=0 C=13 D=13 
00254 [L450] CALL     A=14 B=1 C=3 D=259 
00255 [L454] MULNV    A=12 B=3 C=7 D=775 
00256 [L455] KNUM     A=13 B=0 C=8 D=8 0.24
00257 [L458] UGET     A=14 B=0 C=0 D=0 CCSprite
00258 [L458] MOV      A=15 B=0 C=14 D=14 
00259 [L458] TGETS    A=14 B=14 C=11 D=3595 'create'
00260 [L458] KSTR     A=16 B=0 C=49 D=49 'v2/twoYearsCelebrateUI/bottum.png'
00261 [L458] CALL     A=14 B=2 C=3 D=515 
00262 [L459] GGET     A=15 B=0 C=0 D=0 'd_ms'
00263 [L459] TGETS    A=15 B=15 C=1 D=3841 'd_u'
00264 [L459] TGETS    A=15 B=15 C=17 D=3857 'setStyles'
00265 [L459] MOV      A=16 B=0 C=14 D=14 
00266 [L459] TDUP     A=17 B=0 C=50 D=50 {'kind': 'table', 'value': {}}
00267 [L459] GGET     A=18 B=0 C=51 D=51 'mx'
00268 [L459] TSETS    A=18 B=17 C=52 D=4404 'x'
00269 [L459] GGET     A=18 B=0 C=53 D=53 'my'
00270 [L459] SUBVV    A=18 B=18 C=13 D=4621 
00271 [L459] MULNV    A=19 B=4 C=9 D=1033 
00272 [L459] ADDVV    A=18 B=18 C=19 D=4627 
00273 [L459] TSETS    A=18 B=17 C=19 D=4371 'y'
00274 [L459] TDUP     A=18 B=0 C=54 D=54 {'kind': 'table', 'value': {1: 0.5, 2: 1}}
00275 [L459] TSETS    A=18 B=17 C=55 D=4407 'anchor'
00276 [L459] CALL     A=15 B=1 C=3 D=259 
00277 [L460] MOV      A=16 B=0 C=0 D=0 
00278 [L460] TGETS    A=15 B=0 C=21 D=21 'addChild'
00279 [L460] MOV      A=17 B=0 C=14 D=14 
00280 [L460] CALL     A=15 B=1 C=3 D=259 
00281 [L464] GGET     A=15 B=0 C=0 D=0 'd_ms'
00282 [L464] TGETS    A=15 B=15 C=26 D=3866 'd_hz'
00283 [L464] TGETS    A=15 B=15 C=27 D=3867 'gethz'
00284 [L464] KSTR     A=16 B=0 C=56 D=56 'twoyears_info8'
00285 [L464] CALL     A=15 B=2 C=2 D=514 
00286 [L465] GGET     A=16 B=0 C=0 D=0 'd_ms'
00287 [L465] TGETS    A=16 B=16 C=1 D=4097 'd_u'
00288 [L465] TGETS    A=16 B=16 C=30 D=4126 'createByStyles'
00289 [L465] TDUP     A=17 B=0 C=57 D=57 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 22}}
00290 [L465] TSETS    A=15 B=17 C=33 D=4385 'string'
00291 [L465] GGET     A=18 B=0 C=34 D=34 'g_Color'
00292 [L465] TGETS    A=18 B=18 C=35 D=4643 'white'
00293 [L465] TSETS    A=18 B=17 C=36 D=4388 'color'
00294 [L465] CALL     A=16 B=2 C=2 D=514 
00295 [L466] GGET     A=17 B=0 C=0 D=0 'd_ms'
00296 [L466] TGETS    A=17 B=17 C=1 D=4353 'd_u'
00297 [L466] TGETS    A=17 B=17 C=17 D=4369 'setStyles'
00298 [L466] MOV      A=18 B=0 C=16 D=16 
00299 [L466] TDUP     A=19 B=0 C=58 D=58 {'kind': 'table', 'value': {'x': 0.5, 'y': 0.04}}
00300 [L466] TDUP     A=20 B=0 C=59 D=59 {'kind': 'table', 'value': {1: 0.5, 2: 0.5}}
00301 [L466] TSETS    A=20 B=19 C=55 D=4919 'anchor'
00302 [L466] CALL     A=17 B=1 C=3 D=259 
00303 [L467] MOV      A=18 B=0 C=14 D=14 
00304 [L467] TGETS    A=17 B=14 C=21 D=3605 'addChild'
00305 [L467] MOV      A=19 B=0 C=16 D=16 
00306 [L467] CALL     A=17 B=1 C=3 D=259 
00307 [L469] GGET     A=17 B=0 C=0 D=0 'd_ms'
00308 [L469] TGETS    A=17 B=17 C=26 D=4378 'd_hz'
00309 [L469] TGETS    A=17 B=17 C=27 D=4379 'gethz'
00310 [L469] KSTR     A=18 B=0 C=60 D=60 'twoyears_info9'
00311 [L469] CALL     A=17 B=2 C=2 D=514 
00312 [L470] GGET     A=18 B=0 C=0 D=0 'd_ms'
00313 [L470] TGETS    A=18 B=18 C=1 D=4609 'd_u'
00314 [L470] TGETS    A=18 B=18 C=30 D=4638 'createByStyles'
00315 [L470] TDUP     A=19 B=0 C=61 D=61 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 22}}
00316 [L470] TSETS    A=17 B=19 C=33 D=4897 'string'
00317 [L470] GGET     A=20 B=0 C=34 D=34 'g_Color'
00318 [L470] TGETS    A=20 B=20 C=62 D=5182 'red'
00319 [L470] TSETS    A=20 B=19 C=36 D=4900 'color'
00320 [L470] CALL     A=18 B=2 C=2 D=514 
00321 [L471] GGET     A=19 B=0 C=0 D=0 'd_ms'
00322 [L471] TGETS    A=19 B=19 C=1 D=4865 'd_u'
00323 [L471] TGETS    A=19 B=19 C=17 D=4881 'setStyles'
00324 [L471] MOV      A=20 B=0 C=18 D=18 
00325 [L471] TDUP     A=21 B=0 C=63 D=63 {'kind': 'table', 'value': {'x': 0.2, 'y': 0.04}}
00326 [L471] TDUP     A=22 B=0 C=64 D=64 {'kind': 'table', 'value': {1: 0.5, 2: 0.5}}
00327 [L471] TSETS    A=22 B=21 C=55 D=5431 'anchor'
00328 [L471] CALL     A=19 B=1 C=3 D=259 
00329 [L472] MOV      A=20 B=0 C=14 D=14 
00330 [L472] TGETS    A=19 B=14 C=21 D=3605 'addChild'
00331 [L472] MOV      A=21 B=0 C=18 D=18 
00332 [L472] CALL     A=19 B=1 C=3 D=259 
00333 [L476] TNEW     A=19 B=0 C=0 D=0 
00334 [L476] GSET     A=19 B=0 C=65 D=65 'sp1'
00335 [L477] TNEW     A=19 B=0 C=0 D=0 
00336 [L477] GSET     A=19 B=0 C=66 D=66 'sp2'
00337 [L478] MOV      A=20 B=0 C=0 D=0 
00338 [L478] TGETS    A=19 B=0 C=67 D=67 'removeChildByTag'
00339 [L478] GGET     A=21 B=0 C=3 D=3 'g_self'
00340 [L478] TGETS    A=21 B=21 C=68 D=5444 'redPointTag'
00341 [L478] KPRI     A=22 B=0 C=2 D=2 
00342 [L478] CALL     A=19 B=1 C=4 D=260 
00343 [L479] KSHORT   A=19 B=0 C=1 D=1 1
00344 [L479] KSHORT   A=20 B=0 C=5 D=5 5
00345 [L479] KSHORT   A=21 B=0 C=1 D=1 1
00346 [L479] FORI     A=19 B=128 C=135 D=32903 target=482
00347 [L480] GGET     A=23 B=0 C=65 D=65 'sp1'
00348 [L480] UGET     A=24 B=0 C=0 D=0 CCSprite
00349 [L480] MOV      A=25 B=0 C=24 D=24 
00350 [L480] TGETS    A=24 B=24 C=11 D=6155 'create'
00351 [L480] KSTR     A=26 B=0 C=69 D=69 'v2/twoYearsCelebrateUI/gift'
00352 [L480] MOV      A=27 B=0 C=22 D=22 
00353 [L480] KSTR     A=28 B=0 C=70 D=70 '_1.png'
00354 [L480] CAT      A=26 B=26 C=28 D=6684 
00355 [L480] CALL     A=24 B=2 C=3 D=515 
00356 [L480] TSETV    A=24 B=23 C=22 D=5910 
00357 [L481] GGET     A=23 B=0 C=66 D=66 'sp2'
00358 [L481] UGET     A=24 B=0 C=0 D=0 CCSprite
00359 [L481] MOV      A=25 B=0 C=24 D=24 
00360 [L481] TGETS    A=24 B=24 C=11 D=6155 'create'
00361 [L481] KSTR     A=26 B=0 C=71 D=71 'v2/twoYearsCelebrateUI/gift1_2.png'
00362 [L481] CALL     A=24 B=2 C=3 D=515 
00363 [L481] TSETV    A=24 B=23 C=22 D=5910 
00364 [L482] GGET     A=23 B=0 C=3 D=3 'g_self'
00365 [L482] UGET     A=24 B=0 C=6 D=6 y_o_t
00366 [L482] TGETS    A=24 B=24 C=72 D=6216 'enter_activity'
00367 [L482] TGETV    A=23 B=23 C=24 D=5912 
00368 [L482] ISF      A=0 B=0 C=23 D=23 
00369 [L482] JMP      A=23 B=128 C=15 D=32783 target=385
00370 [L482] GGET     A=23 B=0 C=3 D=3 'g_self'
00371 [L482] UGET     A=24 B=0 C=6 D=6 y_o_t
00372 [L482] TGETS    A=24 B=24 C=72 D=6216 'enter_activity'
00373 [L482] TGETV    A=23 B=23 C=24 D=5912 
00374 [L482] TGETS    A=23 B=23 C=73 D=5961 'gift_list'
00375 [L482] ISF      A=0 B=0 C=23 D=23 
00376 [L482] JMP      A=23 B=128 C=8 D=32776 target=385
00377 [L482] GGET     A=23 B=0 C=3 D=3 'g_self'
00378 [L482] UGET     A=24 B=0 C=6 D=6 y_o_t
00379 [L482] TGETS    A=24 B=24 C=72 D=6216 'enter_activity'
00380 [L482] TGETV    A=23 B=23 C=24 D=5912 
00381 [L482] TGETS    A=23 B=23 C=73 D=5961 'gift_list'
00382 [L482] TGETV    A=23 B=23 C=22 D=5910 
00383 [L482] IST      A=0 B=0 C=23 D=23 
00384 [L482] JMP      A=23 B=128 C=13 D=32781 target=398
00385 [L485] GGET     A=23 B=0 C=0 D=0 'd_ms'
00386 [L485] TGETS    A=23 B=23 C=1 D=5889 'd_u'
00387 [L485] TGETS    A=23 B=23 C=74 D=5962 'graySprite'
00388 [L485] GGET     A=24 B=0 C=65 D=65 'sp1'
00389 [L485] TGETV    A=24 B=24 C=22 D=6166 
00390 [L485] CALL     A=23 B=1 C=2 D=258 
00391 [L486] GGET     A=23 B=0 C=0 D=0 'd_ms'
00392 [L486] TGETS    A=23 B=23 C=1 D=5889 'd_u'
00393 [L486] TGETS    A=23 B=23 C=74 D=5962 'graySprite'
00394 [L486] GGET     A=24 B=0 C=66 D=66 'sp2'
00395 [L486] TGETV    A=24 B=24 C=22 D=6166 
00396 [L486] CALL     A=23 B=1 C=2 D=258 
00397 [L486] JMP      A=23 B=128 C=83 D=32851 target=481
00398 [L487] GGET     A=23 B=0 C=3 D=3 'g_self'
00399 [L487] UGET     A=24 B=0 C=6 D=6 y_o_t
00400 [L487] TGETS    A=24 B=24 C=72 D=6216 'enter_activity'
00401 [L487] TGETV    A=23 B=23 C=24 D=5912 
00402 [L487] TGETS    A=23 B=23 C=73 D=5961 'gift_list'
00403 [L487] TGETV    A=23 B=23 C=22 D=5910 
00404 [L487] KSHORT   A=24 B=0 C=0 D=0 0
00405 [L487] ISGE     A=24 B=0 C=23 D=23 
00406 [L487] JMP      A=23 B=128 C=66 D=32834 target=473
00407 [L488] GGET     A=23 B=0 C=0 D=0 'd_ms'
00408 [L488] TGETS    A=23 B=23 C=75 D=5963 'd_mainUI'
00409 [L488] TGETS    A=23 B=23 C=76 D=5964 'createHintNum'
00410 [L488] GGET     A=24 B=0 C=3 D=3 'g_self'
00411 [L488] UGET     A=25 B=0 C=6 D=6 y_o_t
00412 [L488] TGETS    A=25 B=25 C=72 D=6472 'enter_activity'
00413 [L488] TGETV    A=24 B=24 C=25 D=6169 
00414 [L488] TGETS    A=24 B=24 C=73 D=6217 'gift_list'
00415 [L488] TGETV    A=24 B=24 C=22 D=6166 
00416 [L488] GGET     A=25 B=0 C=0 D=0 'd_ms'
00417 [L488] TGETS    A=25 B=25 C=1 D=6401 'd_u'
00418 [L488] TGETS    A=25 B=25 C=77 D=6477 'makePoint'
00419 [L488] GGET     A=26 B=0 C=10 D=10 'sx'
00420 [L488] MULVV    A=26 B=22 C=26 D=5658 
00421 [L488] GGET     A=27 B=0 C=51 D=51 'mx'
00422 [L488] ADDVV    A=26 B=26 C=27 D=6683 
00423 [L488] SUBVV    A=26 B=26 C=12 D=6668 
00424 [L488] ADDVN    A=26 B=26 C=10 D=6666 
00425 [L488] GGET     A=27 B=0 C=53 D=53 'my'
00426 [L488] SUBVV    A=27 B=27 C=13 D=6925 
00427 [L488] CALL     A=25 B=0 C=3 D=3 
00428 [L488] CALLM    A=23 B=2 C=1 D=513 
00429 [L489] MOV      A=25 B=0 C=0 D=0 
00430 [L489] TGETS    A=24 B=0 C=21 D=21 'addChild'
00431 [L489] MOV      A=26 B=0 C=23 D=23 
00432 [L489] KSHORT   A=27 B=0 C=10 D=10 10
00433 [L489] GGET     A=28 B=0 C=3 D=3 'g_self'
00434 [L489] TGETS    A=28 B=28 C=68 D=7236 'redPointTag'
00435 [L489] CALL     A=24 B=1 C=5 D=261 
00436 [L490] GGET     A=24 B=0 C=0 D=0 'd_ms'
00437 [L490] TGETS    A=24 B=24 C=1 D=6145 'd_u'
00438 [L490] TGETS    A=24 B=24 C=30 D=6174 'createByStyles'
00439 [L490] TDUP     A=25 B=0 C=78 D=78 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 24}}
00440 [L490] GGET     A=26 B=0 C=0 D=0 'd_ms'
00441 [L490] TGETS    A=26 B=26 C=26 D=6682 'd_hz'
00442 [L490] TGETS    A=26 B=26 C=27 D=6683 'gethz'
00443 [L490] KSTR     A=27 B=0 C=79 D=79 'twoyears_info22'
00444 [L490] CALL     A=26 B=2 C=2 D=514 
00445 [L490] TSETS    A=26 B=25 C=33 D=6433 'string'
00446 [L490] GGET     A=26 B=0 C=34 D=34 'g_Color'
00447 [L490] TGETS    A=26 B=26 C=80 D=6736 'green'
00448 [L490] TSETS    A=26 B=25 C=36 D=6436 'color'
00449 [L490] CALL     A=24 B=2 C=2 D=514 
00450 [L491] GGET     A=25 B=0 C=0 D=0 'd_ms'
00451 [L491] TGETS    A=25 B=25 C=1 D=6401 'd_u'
00452 [L491] TGETS    A=25 B=25 C=17 D=6417 'setStyles'
00453 [L491] MOV      A=26 B=0 C=24 D=24 
00454 [L491] TDUP     A=27 B=0 C=81 D=81 {'kind': 'table', 'value': {}}
00455 [L491] GGET     A=28 B=0 C=10 D=10 'sx'
00456 [L491] MULVV    A=28 B=22 C=28 D=5660 
00457 [L491] GGET     A=29 B=0 C=51 D=51 'mx'
00458 [L491] ADDVV    A=28 B=28 C=29 D=7197 
00459 [L491] SUBVV    A=28 B=28 C=12 D=7180 
00460 [L491] TSETS    A=28 B=27 C=52 D=6964 'x'
00461 [L491] GGET     A=28 B=0 C=53 D=53 'my'
00462 [L491] SUBVV    A=28 B=28 C=13 D=7181 
00463 [L491] MULNV    A=29 B=4 C=11 D=1035 
00464 [L491] SUBVV    A=28 B=28 C=29 D=7197 
00465 [L491] TSETS    A=28 B=27 C=19 D=6931 'y'
00466 [L491] CALL     A=25 B=1 C=3 D=259 
00467 [L492] MOV      A=26 B=0 C=0 D=0 
00468 [L492] TGETS    A=25 B=0 C=21 D=21 'addChild'
00469 [L492] MOV      A=27 B=0 C=24 D=24 
00470 [L492] KSHORT   A=28 B=0 C=10 D=10 10
00471 [L492] CALL     A=25 B=1 C=4 D=260 
00472 [L492] JMP      A=23 B=128 C=8 D=32776 target=481
00473 [L493] GGET     A=23 B=0 C=3 D=3 'g_self'
00474 [L493] UGET     A=24 B=0 C=6 D=6 y_o_t
00475 [L493] TGETS    A=24 B=24 C=72 D=6216 'enter_activity'
00476 [L493] TGETV    A=23 B=23 C=24 D=5912 
00477 [L493] TGETS    A=23 B=23 C=73 D=5961 'gift_list'
00478 [L493] TGETV    A=23 B=23 C=22 D=5910 
00479 [L493] ISNEN    A=23 B=0 C=12 D=12 0
00480 [L493] JMP      A=23 B=128 C=0 D=32768 target=481
00481 [L479] FORL     A=19 B=127 C=121 D=32633 target=347
00482 [L501] TDUP     A=19 B=0 C=82 D=82 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00483 [L504] TDUP     A=20 B=0 C=83 D=83 {'kind': 'table', 'value': {'tag': 1}}
00484 [L505] GGET     A=21 B=0 C=10 D=10 'sx'
00485 [L505] MULNV    A=21 B=21 C=4 D=5380 
00486 [L505] GGET     A=22 B=0 C=51 D=51 'mx'
00487 [L505] ADDVV    A=21 B=21 C=22 D=5398 
00488 [L505] SUBVV    A=21 B=21 C=12 D=5388 
00489 [L505] TSETS    A=21 B=20 C=52 D=5172 'x'
00490 [L505] GGET     A=21 B=0 C=53 D=53 'my'
00491 [L505] SUBVV    A=21 B=21 C=13 D=5389 
00492 [L505] MULNV    A=22 B=4 C=13 D=1037 
00493 [L505] ADDVV    A=21 B=21 C=22 D=5398 
00494 [L505] TSETS    A=21 B=20 C=19 D=5139 'y'
00495 [L505] GGET     A=21 B=0 C=65 D=65 'sp1'
00496 [L505] TGETB    A=21 B=21 C=1 D=5377 
00497 [L505] TSETS    A=21 B=20 C=84 D=5204 'nsprite'
00498 [L505] GGET     A=21 B=0 C=66 D=66 'sp2'
00499 [L505] TGETB    A=21 B=21 C=1 D=5377 
00500 [L505] TSETS    A=21 B=20 C=85 D=5205 'ssprite'
00501 [L505] GGET     A=21 B=0 C=86 D=86 'openGiftPack'
00502 [L505] TSETS    A=21 B=20 C=87 D=5207 'call_back'
00503 [L505] TDUP     A=21 B=0 C=88 D=88 {'kind': 'table', 'value': {1: 0.5, 2: 1}}
00504 [L505] TSETS    A=21 B=20 C=55 D=5175 'anchor'
00505 [L505] TSETB    A=20 B=19 C=1 D=4865 
00506 [L505] TDUP     A=20 B=0 C=89 D=89 {'kind': 'table', 'value': {'tag': 2}}
00507 [L506] GGET     A=21 B=0 C=10 D=10 'sx'
00508 [L506] MULNV    A=21 B=21 C=14 D=5390 
00509 [L506] GGET     A=22 B=0 C=51 D=51 'mx'
00510 [L506] ADDVV    A=21 B=21 C=22 D=5398 
00511 [L506] SUBVV    A=21 B=21 C=12 D=5388 
00512 [L506] TSETS    A=21 B=20 C=52 D=5172 'x'
00513 [L506] GGET     A=21 B=0 C=53 D=53 'my'
00514 [L506] SUBVV    A=21 B=21 C=13 D=5389 
00515 [L506] MULNV    A=22 B=4 C=13 D=1037 
00516 [L506] ADDVV    A=21 B=21 C=22 D=5398 
00517 [L506] TSETS    A=21 B=20 C=19 D=5139 'y'
00518 [L506] GGET     A=21 B=0 C=65 D=65 'sp1'
00519 [L506] TGETB    A=21 B=21 C=2 D=5378 
00520 [L506] TSETS    A=21 B=20 C=84 D=5204 'nsprite'
00521 [L506] GGET     A=21 B=0 C=66 D=66 'sp2'
00522 [L506] TGETB    A=21 B=21 C=2 D=5378 
00523 [L506] TSETS    A=21 B=20 C=85 D=5205 'ssprite'
00524 [L506] GGET     A=21 B=0 C=86 D=86 'openGiftPack'
00525 [L506] TSETS    A=21 B=20 C=87 D=5207 'call_back'
00526 [L506] TDUP     A=21 B=0 C=90 D=90 {'kind': 'table', 'value': {1: 0.5, 2: 1}}
00527 [L506] TSETS    A=21 B=20 C=55 D=5175 'anchor'
00528 [L506] TSETB    A=20 B=19 C=2 D=4866 
00529 [L506] TDUP     A=20 B=0 C=91 D=91 {'kind': 'table', 'value': {'tag': 3}}
00530 [L507] GGET     A=21 B=0 C=10 D=10 'sx'
00531 [L507] MULNV    A=21 B=21 C=15 D=5391 
00532 [L507] GGET     A=22 B=0 C=51 D=51 'mx'
00533 [L507] ADDVV    A=21 B=21 C=22 D=5398 
00534 [L507] SUBVV    A=21 B=21 C=12 D=5388 
00535 [L507] TSETS    A=21 B=20 C=52 D=5172 'x'
00536 [L507] GGET     A=21 B=0 C=53 D=53 'my'
00537 [L507] SUBVV    A=21 B=21 C=13 D=5389 
00538 [L507] MULNV    A=22 B=4 C=13 D=1037 
00539 [L507] ADDVV    A=21 B=21 C=22 D=5398 
00540 [L507] TSETS    A=21 B=20 C=19 D=5139 'y'
00541 [L507] GGET     A=21 B=0 C=65 D=65 'sp1'
00542 [L507] TGETB    A=21 B=21 C=3 D=5379 
00543 [L507] TSETS    A=21 B=20 C=84 D=5204 'nsprite'
00544 [L507] GGET     A=21 B=0 C=66 D=66 'sp2'
00545 [L507] TGETB    A=21 B=21 C=3 D=5379 
00546 [L507] TSETS    A=21 B=20 C=85 D=5205 'ssprite'
00547 [L507] GGET     A=21 B=0 C=86 D=86 'openGiftPack'
00548 [L507] TSETS    A=21 B=20 C=87 D=5207 'call_back'
00549 [L507] TDUP     A=21 B=0 C=92 D=92 {'kind': 'table', 'value': {1: 0.5, 2: 1}}
00550 [L507] TSETS    A=21 B=20 C=55 D=5175 'anchor'
00551 [L507] TSETB    A=20 B=19 C=3 D=4867 
00552 [L507] TDUP     A=20 B=0 C=93 D=93 {'kind': 'table', 'value': {'tag': 4}}
00553 [L508] GGET     A=21 B=0 C=10 D=10 'sx'
00554 [L508] MULNV    A=21 B=21 C=16 D=5392 
00555 [L508] GGET     A=22 B=0 C=51 D=51 'mx'
00556 [L508] ADDVV    A=21 B=21 C=22 D=5398 
00557 [L508] SUBVV    A=21 B=21 C=12 D=5388 
00558 [L508] TSETS    A=21 B=20 C=52 D=5172 'x'
00559 [L508] GGET     A=21 B=0 C=53 D=53 'my'
00560 [L508] SUBVV    A=21 B=21 C=13 D=5389 
00561 [L508] MULNV    A=22 B=4 C=13 D=1037 
00562 [L508] ADDVV    A=21 B=21 C=22 D=5398 
00563 [L508] TSETS    A=21 B=20 C=19 D=5139 'y'
00564 [L508] GGET     A=21 B=0 C=65 D=65 'sp1'
00565 [L508] TGETB    A=21 B=21 C=4 D=5380 
00566 [L508] TSETS    A=21 B=20 C=84 D=5204 'nsprite'
00567 [L508] GGET     A=21 B=0 C=66 D=66 'sp2'
00568 [L508] TGETB    A=21 B=21 C=4 D=5380 
00569 [L508] TSETS    A=21 B=20 C=85 D=5205 'ssprite'
00570 [L508] GGET     A=21 B=0 C=86 D=86 'openGiftPack'
00571 [L508] TSETS    A=21 B=20 C=87 D=5207 'call_back'
00572 [L508] TDUP     A=21 B=0 C=94 D=94 {'kind': 'table', 'value': {1: 0.5, 2: 1}}
00573 [L508] TSETS    A=21 B=20 C=55 D=5175 'anchor'
00574 [L508] TSETB    A=20 B=19 C=4 D=4868 
00575 [L508] TDUP     A=20 B=0 C=95 D=95 {'kind': 'table', 'value': {'tag': 5}}
00576 [L509] GGET     A=21 B=0 C=10 D=10 'sx'
00577 [L509] MULNV    A=21 B=21 C=17 D=5393 
00578 [L509] GGET     A=22 B=0 C=51 D=51 'mx'
00579 [L509] ADDVV    A=21 B=21 C=22 D=5398 
00580 [L509] SUBVV    A=21 B=21 C=12 D=5388 
00581 [L509] TSETS    A=21 B=20 C=52 D=5172 'x'
00582 [L509] GGET     A=21 B=0 C=53 D=53 'my'
00583 [L509] SUBVV    A=21 B=21 C=13 D=5389 
00584 [L509] MULNV    A=22 B=4 C=13 D=1037 
00585 [L509] ADDVV    A=21 B=21 C=22 D=5398 
00586 [L509] TSETS    A=21 B=20 C=19 D=5139 'y'
00587 [L509] GGET     A=21 B=0 C=65 D=65 'sp1'
00588 [L509] TGETB    A=21 B=21 C=5 D=5381 
00589 [L509] TSETS    A=21 B=20 C=84 D=5204 'nsprite'
00590 [L509] GGET     A=21 B=0 C=66 D=66 'sp2'
00591 [L509] TGETB    A=21 B=21 C=5 D=5381 
00592 [L509] TSETS    A=21 B=20 C=85 D=5205 'ssprite'
00593 [L509] GGET     A=21 B=0 C=86 D=86 'openGiftPack'
00594 [L509] TSETS    A=21 B=20 C=87 D=5207 'call_back'
00595 [L509] TDUP     A=21 B=0 C=96 D=96 {'kind': 'table', 'value': {1: 0.5, 2: 1}}
00596 [L509] TSETS    A=21 B=20 C=55 D=5175 'anchor'
00597 [L509] TSETB    A=20 B=19 C=5 D=4869 
00598 [L512] GGET     A=20 B=0 C=3 D=3 'g_self'
00599 [L512] UGET     A=21 B=0 C=6 D=6 y_o_t
00600 [L512] TGETS    A=21 B=21 C=72 D=5448 'enter_activity'
00601 [L512] TGETV    A=20 B=20 C=21 D=5141 
00602 [L512] ISF      A=0 B=0 C=20 D=20 
00603 [L512] JMP      A=20 B=128 C=16 D=32784 target=620
00604 [L512] GGET     A=20 B=0 C=3 D=3 'g_self'
00605 [L512] UGET     A=21 B=0 C=6 D=6 y_o_t
00606 [L512] TGETS    A=21 B=21 C=72 D=5448 'enter_activity'
00607 [L512] TGETV    A=20 B=20 C=21 D=5141 
00608 [L512] TGETS    A=20 B=20 C=73 D=5193 'gift_list'
00609 [L512] ISF      A=0 B=0 C=20 D=20 
00610 [L512] JMP      A=20 B=128 C=9 D=32777 target=620
00611 [L512] GGET     A=20 B=0 C=3 D=3 'g_self'
00612 [L512] UGET     A=21 B=0 C=6 D=6 y_o_t
00613 [L512] TGETS    A=21 B=21 C=72 D=5448 'enter_activity'
00614 [L512] TGETV    A=20 B=20 C=21 D=5141 
00615 [L512] TGETS    A=20 B=20 C=73 D=5193 'gift_list'
00616 [L512] LEN      A=20 B=0 C=20 D=20 
00617 [L512] KSHORT   A=21 B=0 C=5 D=5 5
00618 [L512] ISGE     A=20 B=0 C=21 D=21 
00619 [L512] JMP      A=20 B=128 C=20 D=32788 target=640
00620 [L513] UGET     A=20 B=0 C=7 D=7 table
00621 [L513] TGETS    A=20 B=20 C=97 D=5217 'insert'
00622 [L513] MOV      A=21 B=0 C=19 D=19 
00623 [L513] TDUP     A=22 B=0 C=98 D=98 {'kind': 'table', 'value': {'npic': 'v2/rechargeUI/recharge1.png', 'spic': 'v2/rechargeUI/recharge2.png'}}
00624 [L513] GGET     A=23 B=0 C=10 D=10 'sx'
00625 [L513] MULNV    A=23 B=23 C=18 D=5906 
00626 [L513] GGET     A=24 B=0 C=51 D=51 'mx'
00627 [L513] ADDVV    A=23 B=23 C=24 D=5912 
00628 [L513] SUBVV    A=23 B=23 C=12 D=5900 
00629 [L513] TSETS    A=23 B=22 C=52 D=5684 'x'
00630 [L513] GGET     A=23 B=0 C=53 D=53 'my'
00631 [L513] SUBVV    A=23 B=23 C=13 D=5901 
00632 [L513] MULNV    A=24 B=4 C=10 D=1034 
00633 [L513] SUBVV    A=23 B=23 C=24 D=5912 
00634 [L513] TSETS    A=23 B=22 C=19 D=5651 'y'
00635 [L513] TDUP     A=23 B=0 C=99 D=99 {'kind': 'table', 'value': {1: 0.5, 2: 1}}
00636 [L513] TSETS    A=23 B=22 C=55 D=5687 'anchor'
00637 [L513] GGET     A=23 B=0 C=100 D=100 'recharge'
00638 [L513] TSETS    A=23 B=22 C=87 D=5719 'call_back'
00639 [L513] CALL     A=20 B=1 C=3 D=259 
00640 [L515] MOV      A=21 B=0 C=0 D=0 
00641 [L515] TGETS    A=20 B=0 C=21 D=21 'addChild'
00642 [L515] GGET     A=22 B=0 C=0 D=0 'd_ms'
00643 [L515] TGETS    A=22 B=22 C=1 D=5633 'd_u'
00644 [L515] TGETS    A=22 B=22 C=101 D=5733 'createMenu'
00645 [L515] MOV      A=23 B=0 C=19 D=19 
00646 [L515] CALL     A=22 B=0 C=2 D=2 
00647 [L515] CALLM    A=20 B=1 C=1 D=257 
00648 [L517] KSTR     A=20 B=0 C=102 D=102 ''
00649 [L518] GGET     A=21 B=0 C=3 D=3 'g_self'
00650 [L518] UGET     A=22 B=0 C=6 D=6 y_o_t
00651 [L518] TGETS    A=22 B=22 C=72 D=5704 'enter_activity'
00652 [L518] TGETV    A=21 B=21 C=22 D=5398 
00653 [L518] ISF      A=0 B=0 C=21 D=21 
00654 [L518] JMP      A=21 B=128 C=15 D=32783 target=670
00655 [L518] GGET     A=21 B=0 C=3 D=3 'g_self'
00656 [L518] UGET     A=22 B=0 C=6 D=6 y_o_t
00657 [L518] TGETS    A=22 B=22 C=72 D=5704 'enter_activity'
00658 [L518] TGETV    A=21 B=21 C=22 D=5398 
00659 [L518] TGETS    A=21 B=21 C=73 D=5449 'gift_list'
00660 [L518] ISF      A=0 B=0 C=21 D=21 
00661 [L518] JMP      A=21 B=128 C=8 D=32776 target=670
00662 [L518] GGET     A=21 B=0 C=3 D=3 'g_self'
00663 [L518] UGET     A=22 B=0 C=6 D=6 y_o_t
00664 [L518] TGETS    A=22 B=22 C=72 D=5704 'enter_activity'
00665 [L518] TGETV    A=21 B=21 C=22 D=5398 
00666 [L518] TGETS    A=21 B=21 C=73 D=5449 'gift_list'
00667 [L518] LEN      A=21 B=0 C=21 D=21 
00668 [L518] ISNEN    A=21 B=0 C=12 D=12 0
00669 [L518] JMP      A=21 B=128 C=7 D=32775 target=677
00670 [L519] GGET     A=21 B=0 C=0 D=0 'd_ms'
00671 [L519] TGETS    A=21 B=21 C=26 D=5402 'd_hz'
00672 [L519] TGETS    A=21 B=21 C=27 D=5403 'gethz'
00673 [L519] KSTR     A=22 B=0 C=103 D=103 'twoyears_info16'
00674 [L519] CALL     A=21 B=2 C=2 D=514 
00675 [L519] MOV      A=20 B=0 C=21 D=21 
00676 [L519] JMP      A=21 B=128 C=52 D=32820 target=729
00677 [L520] GGET     A=21 B=0 C=3 D=3 'g_self'
00678 [L520] UGET     A=22 B=0 C=6 D=6 y_o_t
00679 [L520] TGETS    A=22 B=22 C=72 D=5704 'enter_activity'
00680 [L520] TGETV    A=21 B=21 C=22 D=5398 
00681 [L520] TGETS    A=21 B=21 C=73 D=5449 'gift_list'
00682 [L520] TGETB    A=21 B=21 C=2 D=5378 
00683 [L520] ISF      A=0 B=0 C=21 D=21 
00684 [L520] JMP      A=21 B=128 C=8 D=32776 target=693
00685 [L520] GGET     A=21 B=0 C=3 D=3 'g_self'
00686 [L520] UGET     A=22 B=0 C=6 D=6 y_o_t
00687 [L520] TGETS    A=22 B=22 C=72 D=5704 'enter_activity'
00688 [L520] TGETV    A=21 B=21 C=22 D=5398 
00689 [L520] TGETS    A=21 B=21 C=73 D=5449 'gift_list'
00690 [L520] TGETB    A=21 B=21 C=3 D=5379 
00691 [L520] IST      A=0 B=0 C=21 D=21 
00692 [L520] JMP      A=21 B=128 C=7 D=32775 target=700
00693 [L521] GGET     A=21 B=0 C=0 D=0 'd_ms'
00694 [L521] TGETS    A=21 B=21 C=26 D=5402 'd_hz'
00695 [L521] TGETS    A=21 B=21 C=27 D=5403 'gethz'
00696 [L521] KSTR     A=22 B=0 C=104 D=104 'twoyears_info17'
00697 [L521] CALL     A=21 B=2 C=2 D=514 
00698 [L521] MOV      A=20 B=0 C=21 D=21 
00699 [L521] JMP      A=21 B=128 C=29 D=32797 target=729
00700 [L522] GGET     A=21 B=0 C=3 D=3 'g_self'
00701 [L522] UGET     A=22 B=0 C=6 D=6 y_o_t
00702 [L522] TGETS    A=22 B=22 C=72 D=5704 'enter_activity'
00703 [L522] TGETV    A=21 B=21 C=22 D=5398 
00704 [L522] TGETS    A=21 B=21 C=73 D=5449 'gift_list'
00705 [L522] TGETB    A=21 B=21 C=4 D=5380 
00706 [L522] ISF      A=0 B=0 C=21 D=21 
00707 [L522] JMP      A=21 B=128 C=8 D=32776 target=716
00708 [L522] GGET     A=21 B=0 C=3 D=3 'g_self'
00709 [L522] UGET     A=22 B=0 C=6 D=6 y_o_t
00710 [L522] TGETS    A=22 B=22 C=72 D=5704 'enter_activity'
00711 [L522] TGETV    A=21 B=21 C=22 D=5398 
00712 [L522] TGETS    A=21 B=21 C=73 D=5449 'gift_list'
00713 [L522] TGETB    A=21 B=21 C=5 D=5381 
00714 [L522] IST      A=0 B=0 C=21 D=21 
00715 [L522] JMP      A=21 B=128 C=7 D=32775 target=723
00716 [L523] GGET     A=21 B=0 C=0 D=0 'd_ms'
00717 [L523] TGETS    A=21 B=21 C=26 D=5402 'd_hz'
00718 [L523] TGETS    A=21 B=21 C=27 D=5403 'gethz'
00719 [L523] KSTR     A=22 B=0 C=105 D=105 'twoyears_info18'
00720 [L523] CALL     A=21 B=2 C=2 D=514 
00721 [L523] MOV      A=20 B=0 C=21 D=21 
00722 [L523] JMP      A=21 B=128 C=6 D=32774 target=729
00723 [L525] GGET     A=21 B=0 C=0 D=0 'd_ms'
00724 [L525] TGETS    A=21 B=21 C=26 D=5402 'd_hz'
00725 [L525] TGETS    A=21 B=21 C=27 D=5403 'gethz'
00726 [L525] KSTR     A=22 B=0 C=106 D=106 'twoyears_info21'
00727 [L525] CALL     A=21 B=2 C=2 D=514 
00728 [L525] MOV      A=20 B=0 C=21 D=21 
00729 [L527] GGET     A=21 B=0 C=3 D=3 'g_self'
00730 [L527] UGET     A=22 B=0 C=6 D=6 y_o_t
00731 [L527] TGETS    A=22 B=22 C=72 D=5704 'enter_activity'
00732 [L527] TGETV    A=21 B=21 C=22 D=5398 
00733 [L527] TGETS    A=21 B=21 C=107 D=5483 'is_today_charge'
00734 [L527] ISF      A=0 B=0 C=21 D=21 
00735 [L527] JMP      A=22 B=128 C=1 D=32769 target=737
00736 [L528] KSTR     A=20 B=0 C=102 D=102 ''
00737 [L530] GGET     A=21 B=0 C=0 D=0 'd_ms'
00738 [L530] TGETS    A=21 B=21 C=1 D=5377 'd_u'
00739 [L530] TGETS    A=21 B=21 C=30 D=5406 'createByStyles'
00740 [L530] TDUP     A=22 B=0 C=108 D=108 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 22}}
00741 [L530] TSETS    A=20 B=22 C=33 D=5665 'string'
00742 [L530] GGET     A=23 B=0 C=34 D=34 'g_Color'
00743 [L530] TGETS    A=23 B=23 C=35 D=5923 'white'
00744 [L530] TSETS    A=23 B=22 C=36 D=5668 'color'
00745 [L530] CALL     A=21 B=2 C=2 D=514 
00746 [L531] GGET     A=22 B=0 C=0 D=0 'd_ms'
00747 [L531] TGETS    A=22 B=22 C=1 D=5633 'd_u'
00748 [L531] TGETS    A=22 B=22 C=17 D=5649 'setStyles'
00749 [L531] MOV      A=23 B=0 C=21 D=21 
00750 [L531] TDUP     A=24 B=0 C=109 D=109 {'kind': 'table', 'value': {}}
00751 [L531] GGET     A=25 B=0 C=10 D=10 'sx'
00752 [L531] MULNV    A=25 B=25 C=18 D=6418 
00753 [L531] GGET     A=26 B=0 C=51 D=51 'mx'
00754 [L531] ADDVV    A=25 B=25 C=26 D=6426 
00755 [L531] SUBVV    A=25 B=25 C=12 D=6412 
00756 [L531] TSETS    A=25 B=24 C=52 D=6196 'x'
00757 [L531] GGET     A=25 B=0 C=53 D=53 'my'
00758 [L531] SUBVV    A=25 B=25 C=13 D=6413 
00759 [L531] MULNV    A=26 B=4 C=19 D=1043 
00760 [L531] ADDVV    A=25 B=25 C=26 D=6426 
00761 [L531] TSETS    A=25 B=24 C=19 D=6163 'y'
00762 [L531] TDUP     A=25 B=0 C=110 D=110 {'kind': 'table', 'value': {1: 0.5, 2: 1}}
00763 [L531] TSETS    A=25 B=24 C=55 D=6199 'anchor'
00764 [L531] CALL     A=22 B=1 C=3 D=259 
00765 [L532] MOV      A=23 B=0 C=0 D=0 
00766 [L532] TGETS    A=22 B=0 C=21 D=21 'addChild'
00767 [L532] MOV      A=24 B=0 C=21 D=21 
00768 [L532] CALL     A=22 B=1 C=3 D=259 
00769 [L533] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto14 offset=0x3dcc source_lines=535-552 params=1
UPVALUES ['y_o_t']
00001 [L537] GGET     A=1 B=0 C=0 D=0 'g_self'
00002 [L537] UGET     A=2 B=0 C=0 D=0 y_o_t
00003 [L537] TGETS    A=2 B=2 C=1 D=513 'enter_shop'
00004 [L537] TGETV    A=1 B=1 C=2 D=258 
00005 [L537] TGETS    A=1 B=1 C=2 D=258 'shop_config'
00006 [L537] TGETV    A=1 B=1 C=0 D=256 
00007 [L537] TGETS    A=1 B=1 C=3 D=259 'buy_times'
00008 [L537] KSHORT   A=2 B=0 C=0 D=0 0
00009 [L537] ISGT     A=1 B=0 C=2 D=2 
00010 [L537] JMP      A=1 B=128 C=10 D=32778 target=21
00011 [L538] GGET     A=1 B=0 C=4 D=4 'd_ms'
00012 [L538] TGETS    A=1 B=1 C=5 D=261 'd_info'
00013 [L538] TGETS    A=1 B=1 C=6 D=262 'show'
00014 [L538] GGET     A=2 B=0 C=4 D=4 'd_ms'
00015 [L538] TGETS    A=2 B=2 C=7 D=519 'd_hz'
00016 [L538] TGETS    A=2 B=2 C=8 D=520 'gethz'
00017 [L538] KSTR     A=3 B=0 C=9 D=9 'twoyears_info12'
00018 [L538] CALL     A=2 B=0 C=2 D=2 
00019 [L538] CALLM    A=1 B=1 C=0 D=256 
00020 [L539] RET0     A=0 B=0 C=1 D=1 
00021 [L542] GGET     A=1 B=0 C=0 D=0 'g_self'
00022 [L542] UGET     A=2 B=0 C=0 D=0 y_o_t
00023 [L542] TGETS    A=2 B=2 C=1 D=513 'enter_shop'
00024 [L542] TGETV    A=1 B=1 C=2 D=258 
00025 [L542] TGETS    A=1 B=1 C=2 D=258 'shop_config'
00026 [L542] TGETV    A=1 B=1 C=0 D=256 
00027 [L542] TGETS    A=1 B=1 C=10 D=266 'need_gold'
00028 [L542] GGET     A=2 B=0 C=4 D=4 'd_ms'
00029 [L542] TGETS    A=2 B=2 C=11 D=523 'd_mainUI'
00030 [L542] TGETS    A=2 B=2 C=12 D=524 'g_playerInfo'
00031 [L542] TGETS    A=2 B=2 C=13 D=525 'gold_coin'
00032 [L542] ISGE     A=2 B=0 C=1 D=1 
00033 [L542] JMP      A=1 B=128 C=10 D=32778 target=44
00034 [L543] GGET     A=1 B=0 C=4 D=4 'd_ms'
00035 [L543] TGETS    A=1 B=1 C=5 D=261 'd_info'
00036 [L543] TGETS    A=1 B=1 C=6 D=262 'show'
00037 [L543] GGET     A=2 B=0 C=4 D=4 'd_ms'
00038 [L543] TGETS    A=2 B=2 C=7 D=519 'd_hz'
00039 [L543] TGETS    A=2 B=2 C=8 D=520 'gethz'
00040 [L543] KSTR     A=3 B=0 C=14 D=14 'noGold'
00041 [L543] CALL     A=2 B=0 C=2 D=2 
00042 [L543] CALLM    A=1 B=1 C=0 D=256 
00043 [L544] RET0     A=0 B=0 C=1 D=1 
00044 [L547] TNEW     A=1 B=0 C=0 D=0 
00045 [L547] GSET     A=1 B=0 C=15 D=15 'tmp_req'
00046 [L548] GGET     A=1 B=0 C=15 D=15 'tmp_req'
00047 [L548] UGET     A=2 B=0 C=0 D=0 y_o_t
00048 [L548] TGETS    A=2 B=2 C=17 D=529 'buy_shop'
00049 [L548] TSETS    A=2 B=1 C=16 D=272 'flag'
00050 [L549] GGET     A=1 B=0 C=15 D=15 'tmp_req'
00051 [L549] TSETS    A=0 B=1 C=18 D=274 'index'
00052 [L551] GGET     A=1 B=0 C=4 D=4 'd_ms'
00053 [L551] TGETS    A=1 B=1 C=19 D=275 'd_u'
00054 [L551] TGETS    A=1 B=1 C=20 D=276 'main_server_send_msg'
00055 [L551] GGET     A=2 B=0 C=4 D=4 'd_ms'
00056 [L551] TGETS    A=2 B=2 C=21 D=533 'd_msg_def'
00057 [L551] TGETS    A=2 B=2 C=22 D=534 'gscl_msg_id'
00058 [L551] TGETS    A=2 B=2 C=23 D=535 'msg_yuanshi_activity'
00059 [L551] GGET     A=3 B=0 C=15 D=15 'tmp_req'
00060 [L551] CALL     A=1 B=1 C=3 D=259 
00061 [L552] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto15 offset=0x3ffd source_lines=554-560 params=1
UPVALUES ['y_o_t']
00001 [L555] GGET     A=1 B=0 C=0 D=0 'g_self'
00002 [L555] UGET     A=2 B=0 C=0 D=0 y_o_t
00003 [L555] TGETS    A=2 B=2 C=1 D=513 'enter_activity'
00004 [L555] TGETV    A=1 B=1 C=2 D=258 
00005 [L555] IST      A=0 B=0 C=1 D=1 
00006 [L555] JMP      A=1 B=128 C=1 D=32769 target=8
00007 [L556] RET0     A=0 B=0 C=1 D=1 
00008 [L558] GGET     A=1 B=0 C=2 D=2 'showGiftDetail'
00009 [L558] MOV      A=2 B=0 C=0 D=0 
00010 [L558] CALL     A=1 B=1 C=2 D=258 
00011 [L560] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto16 offset=0x4075 source_lines=561-576 params=2
UPVALUES ['y_o_t']
00001 [L562] GGET     A=2 B=0 C=0 D=0 'g_self'
00002 [L562] UGET     A=3 B=0 C=0 D=0 y_o_t
00003 [L562] TGETS    A=3 B=3 C=1 D=769 'enter_activity'
00004 [L562] TGETV    A=2 B=2 C=3 D=515 
00005 [L562] IST      A=0 B=0 C=2 D=2 
00006 [L562] JMP      A=2 B=128 C=1 D=32769 target=8
00007 [L563] RET0     A=0 B=0 C=1 D=1 
00008 [L565] GGET     A=2 B=0 C=0 D=0 'g_self'
00009 [L565] UGET     A=3 B=0 C=0 D=0 y_o_t
00010 [L565] TGETS    A=3 B=3 C=1 D=769 'enter_activity'
00011 [L565] TGETV    A=2 B=2 C=3 D=515 
00012 [L565] TGETS    A=2 B=2 C=2 D=514 'gift_list'
00013 [L565] ISF      A=0 B=0 C=2 D=2 
00014 [L565] JMP      A=2 B=128 C=17 D=32785 target=32
00015 [L565] GGET     A=2 B=0 C=0 D=0 'g_self'
00016 [L565] UGET     A=3 B=0 C=0 D=0 y_o_t
00017 [L565] TGETS    A=3 B=3 C=1 D=769 'enter_activity'
00018 [L565] TGETV    A=2 B=2 C=3 D=515 
00019 [L565] TGETS    A=2 B=2 C=2 D=514 'gift_list'
00020 [L565] TGETV    A=2 B=2 C=0 D=512 
00021 [L565] ISF      A=0 B=0 C=2 D=2 
00022 [L565] JMP      A=2 B=128 C=9 D=32777 target=32
00023 [L565] GGET     A=2 B=0 C=0 D=0 'g_self'
00024 [L565] UGET     A=3 B=0 C=0 D=0 y_o_t
00025 [L565] TGETS    A=3 B=3 C=1 D=769 'enter_activity'
00026 [L565] TGETV    A=2 B=2 C=3 D=515 
00027 [L565] TGETS    A=2 B=2 C=2 D=514 'gift_list'
00028 [L565] TGETV    A=2 B=2 C=0 D=512 
00029 [L565] KSHORT   A=3 B=0 C=0 D=0 0
00030 [L565] ISGT     A=2 B=0 C=3 D=3 
00031 [L565] JMP      A=2 B=128 C=1 D=32769 target=33
00032 [L566] RET0     A=0 B=0 C=1 D=1 
00033 [L568] TNEW     A=2 B=0 C=0 D=0 
00034 [L568] GSET     A=2 B=0 C=3 D=3 'tmp_req'
00035 [L569] GGET     A=2 B=0 C=3 D=3 'tmp_req'
00036 [L569] UGET     A=3 B=0 C=0 D=0 y_o_t
00037 [L569] TGETS    A=3 B=3 C=5 D=773 'take_prize'
00038 [L569] TSETS    A=3 B=2 C=4 D=516 'flag'
00039 [L570] GGET     A=2 B=0 C=3 D=3 'tmp_req'
00040 [L570] TSETS    A=0 B=2 C=6 D=518 'index'
00041 [L572] GGET     A=2 B=0 C=7 D=7 'd_ms'
00042 [L572] TGETS    A=2 B=2 C=8 D=520 'd_u'
00043 [L572] TGETS    A=2 B=2 C=9 D=521 'main_server_send_msg'
00044 [L572] GGET     A=3 B=0 C=7 D=7 'd_ms'
00045 [L572] TGETS    A=3 B=3 C=10 D=778 'd_msg_def'
00046 [L572] TGETS    A=3 B=3 C=11 D=779 'gscl_msg_id'
00047 [L572] TGETS    A=3 B=3 C=12 D=780 'msg_yuanshi_activity'
00048 [L572] GGET     A=4 B=0 C=3 D=3 'tmp_req'
00049 [L572] CALL     A=2 B=1 C=3 D=259 
00050 [L573] ISF      A=0 B=0 C=1 D=1 
00051 [L573] JMP      A=2 B=128 C=2 D=32770 target=54
00052 [L574] MOV      A=2 B=0 C=1 D=1 
00053 [L574] CALL     A=2 B=1 C=1 D=257 
00054 [L576] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto17 offset=0x4236 source_lines=578-582 params=0
UPVALUES []
00001 [L581] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L581] TGETS    A=0 B=0 C=1 D=1 'd_rechargeUI'
00003 [L581] TGETS    A=0 B=0 C=2 D=2 'show'
00004 [L581] CALL     A=0 B=1 C=1 D=257 
00005 [L582] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto18 offset=0x4274 source_lines=584-604 params=0
UPVALUES []
00001 [L585] GGET     A=0 B=0 C=0 D=0 'g_self'
00002 [L585] TGETS    A=0 B=0 C=1 D=1 'main_layer'
00003 [L585] IST      A=0 B=0 C=0 D=0 
00004 [L585] JMP      A=0 B=128 C=1 D=32769 target=6
00005 [L586] RET0     A=0 B=0 C=1 D=1 
00006 [L588] GGET     A=0 B=0 C=0 D=0 'g_self'
00007 [L588] TGETS    A=0 B=0 C=1 D=1 'main_layer'
00008 [L590] MOV      A=2 B=0 C=0 D=0 
00009 [L590] TGETS    A=1 B=0 C=2 D=2 'removeChildByTag'
00010 [L590] GGET     A=3 B=0 C=0 D=0 'g_self'
00011 [L590] TGETS    A=3 B=3 C=3 D=771 'timeTag'
00012 [L590] KPRI     A=4 B=0 C=2 D=2 
00013 [L590] CALL     A=1 B=1 C=4 D=260 
00014 [L591] GGET     A=1 B=0 C=4 D=4 'canJoin'
00015 [L591] CALL     A=1 B=2 C=1 D=513 
00016 [L591] IST      A=0 B=0 C=1 D=1 
00017 [L591] JMP      A=1 B=128 C=3 D=32771 target=21
00018 [L592] GGET     A=1 B=0 C=5 D=5 'call_back_close'
00019 [L592] CALL     A=1 B=1 C=1 D=257 
00020 [L593] RET0     A=0 B=0 C=1 D=1 
00021 [L595] GGET     A=1 B=0 C=6 D=6 'd_ms'
00022 [L595] TGETS    A=1 B=1 C=7 D=263 'd_data'
00023 [L595] TGETS    A=1 B=1 C=8 D=264 'g_new_config'
00024 [L595] GGET     A=2 B=0 C=6 D=6 'd_ms'
00025 [L595] TGETS    A=2 B=2 C=9 D=521 'd_common_def'
00026 [L595] TGETS    A=2 B=2 C=10 D=522 'client_config_type'
00027 [L595] TGETS    A=2 B=2 C=11 D=523 'common_config'
00028 [L595] TGETV    A=1 B=1 C=2 D=258 
00029 [L595] TGETS    A=1 B=1 C=12 D=268 'yuanshi_info'
00030 [L597] GGET     A=2 B=0 C=6 D=6 'd_ms'
00031 [L597] TGETS    A=2 B=2 C=13 D=525 'd_time'
00032 [L597] TGETS    A=2 B=2 C=14 D=526 'getRestTime'
00033 [L597] TGETS    A=3 B=1 C=15 D=271 'end_time'
00034 [L597] GGET     A=4 B=0 C=6 D=6 'd_ms'
00035 [L597] TGETS    A=4 B=4 C=13 D=1037 'd_time'
00036 [L597] TGETS    A=4 B=4 C=16 D=1040 'g_format'
00037 [L597] TGETS    A=4 B=4 C=17 D=1041 'hz'
00038 [L597] CALL     A=2 B=2 C=3 D=515 
00039 [L598] ISF      A=0 B=0 C=2 D=2 
00040 [L598] JMP      A=3 B=128 C=29 D=32797 target=70
00041 [L599] GGET     A=3 B=0 C=6 D=6 'd_ms'
00042 [L599] TGETS    A=3 B=3 C=18 D=786 'd_u'
00043 [L599] TGETS    A=3 B=3 C=19 D=787 'createByStyles'
00044 [L599] TDUP     A=4 B=0 C=20 D=20 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'x': 0.13, 'fontsize': 24}}
00045 [L599] TSETS    A=2 B=4 C=21 D=1045 'string'
00046 [L599] GGET     A=5 B=0 C=22 D=22 'my'
00047 [L599] GGET     A=6 B=0 C=23 D=23 'h'
00048 [L599] MULNV    A=6 B=6 C=0 D=1536 
00049 [L599] ADDVV    A=5 B=5 C=6 D=1286 
00050 [L599] TSETS    A=5 B=4 C=24 D=1048 'y'
00051 [L599] TDUP     A=5 B=0 C=25 D=25 {'kind': 'table', 'value': {1: 0.5, 2: 0.5}}
00052 [L599] TSETS    A=5 B=4 C=26 D=1050 'anchor'
00053 [L599] TDUP     A=5 B=0 C=27 D=27 {'kind': 'table', 'value': {1: 255, 2: 255, 3: 255}}
00054 [L599] TSETS    A=5 B=4 C=28 D=1052 'color'
00055 [L599] CALL     A=3 B=2 C=2 D=514 
00056 [L600] MOV      A=5 B=0 C=0 D=0 
00057 [L600] TGETS    A=4 B=0 C=29 D=29 'addChild'
00058 [L600] MOV      A=6 B=0 C=3 D=3 
00059 [L600] KSHORT   A=7 B=0 C=1 D=1 1
00060 [L600] GGET     A=8 B=0 C=0 D=0 'g_self'
00061 [L600] TGETS    A=8 B=8 C=3 D=2051 'timeTag'
00062 [L600] CALL     A=4 B=1 C=5 D=261 
00063 [L602] GGET     A=4 B=0 C=6 D=6 'd_ms'
00064 [L602] TGETS    A=4 B=4 C=18 D=1042 'd_u'
00065 [L602] TGETS    A=4 B=4 C=30 D=1054 'delay'
00066 [L602] MOV      A=5 B=0 C=0 D=0 
00067 [L602] KSHORT   A=6 B=0 C=1 D=1 1
00068 [L602] GGET     A=7 B=0 C=31 D=31 'tickTime'
00069 [L602] CALL     A=4 B=1 C=4 D=260 
00070 [L604] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto19 offset=0x4562 source_lines=687-689 params=0
UPVALUES ['layer']
00001 [L688] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L688] TGETS    A=0 B=0 C=1 D=1 'd_u'
00003 [L688] TGETS    A=0 B=0 C=2 D=2 'remove'
00004 [L688] UGET     A=1 B=0 C=0 D=0 layer
00005 [L688] CALL     A=0 B=1 C=2 D=258 
00006 [L689] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto20 offset=0x45a6 source_lines=692-697 params=1
UPVALUES ['items']
00001 [L693] UGET     A=1 B=0 C=0 D=0 items
00002 [L693] TGETV    A=1 B=1 C=0 D=256 
00003 [L694] ISF      A=0 B=0 C=1 D=1 
00004 [L694] JMP      A=2 B=128 C=7 D=32775 target=12
00005 [L695] GGET     A=2 B=0 C=0 D=0 'd_ms'
00006 [L695] TGETS    A=2 B=2 C=1 D=513 'd_data'
00007 [L695] TGETS    A=2 B=2 C=2 D=514 'showItemIntro'
00008 [L695] GGET     A=3 B=0 C=3 D=3 'g_self'
00009 [L695] TGETS    A=3 B=3 C=4 D=772 'main_layer'
00010 [L695] MOV      A=4 B=0 C=1 D=1 
00011 [L695] CALL     A=2 B=1 C=3 D=259 
00012 [L697] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto21 offset=0x4632 source_lines=699-701 params=0
UPVALUES ['tag', 'close']
00001 [L700] GGET     A=0 B=0 C=0 D=0 'openGiftPackEnsure'
00002 [L700] UGET     A=1 B=0 C=0 D=0 tag
00003 [L700] UGET     A=2 B=0 C=1 D=1 close
00004 [L700] CALL     A=0 B=1 C=3 D=259 
00005 [L701] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto22 offset=0x467a source_lines=608-721 params=1
UPVALUES ['y_o_t', 'CCSprite', 'math', 'table']
00001 [L609] GGET     A=1 B=0 C=0 D=0 'g_self'
00002 [L609] TGETS    A=1 B=1 C=1 D=257 'main_layer'
00003 [L610] GGET     A=2 B=0 C=0 D=0 'g_self'
00004 [L610] UGET     A=3 B=0 C=0 D=0 y_o_t
00005 [L610] TGETS    A=3 B=3 C=2 D=770 'enter_activity'
00006 [L610] TGETV    A=2 B=2 C=3 D=515 
00007 [L610] TGETS    A=2 B=2 C=3 D=515 'gift_config'
00008 [L610] TGETV    A=2 B=2 C=0 D=512 
00009 [L610] TGETS    A=2 B=2 C=4 D=516 'prize_list'
00010 [L611] ISF      A=0 B=0 C=1 D=1 
00011 [L611] JMP      A=3 B=128 C=2 D=32770 target=14
00012 [L611] IST      A=0 B=0 C=2 D=2 
00013 [L611] JMP      A=3 B=128 C=1 D=32769 target=15
00014 [L612] UCLO     A=0 B=129 C=132 D=33156 target=403
00015 [L615] GGET     A=3 B=0 C=5 D=5 'd_ms'
00016 [L615] TGETS    A=3 B=3 C=6 D=774 'd_u'
00017 [L615] TGETS    A=3 B=3 C=7 D=775 'clearLayer'
00018 [L615] MOV      A=4 B=0 C=1 D=1 
00019 [L615] KSHORT   A=5 B=0 C=20 D=20 20
00020 [L615] GGET     A=6 B=0 C=0 D=0 'g_self'
00021 [L615] TGETS    A=6 B=6 C=8 D=1544 'detailTag'
00022 [L615] CALL     A=3 B=2 C=4 D=516 
00023 [L615] MOV      A=1 B=0 C=3 D=3 
00024 [L616] GGET     A=3 B=0 C=5 D=5 'd_ms'
00025 [L616] TGETS    A=3 B=3 C=6 D=774 'd_u'
00026 [L616] TGETS    A=3 B=3 C=9 D=777 'createSwallowTouchLayer'
00027 [L616] MOV      A=4 B=0 C=1 D=1 
00028 [L616] CALL     A=3 B=1 C=2 D=258 
00029 [L618] GGET     A=3 B=0 C=5 D=5 'd_ms'
00030 [L618] TGETS    A=3 B=3 C=6 D=774 'd_u'
00031 [L618] TGETS    A=3 B=3 C=10 D=778 'createByStyle'
00032 [L618] TDUP     A=4 B=0 C=11 D=11 {'kind': 'table', 'value': {'pic': 'v2/turnTableUI/bkg2.png', 'x': 0.5, 'y': 0.5}}
00033 [L618] CALL     A=3 B=2 C=2 D=514 
00034 [L619] MOV      A=5 B=0 C=1 D=1 
00035 [L619] TGETS    A=4 B=1 C=12 D=268 'addChild'
00036 [L619] MOV      A=6 B=0 C=3 D=3 
00037 [L619] CALL     A=4 B=1 C=3 D=259 
00038 [L620] GGET     A=4 B=0 C=5 D=5 'd_ms'
00039 [L620] TGETS    A=4 B=4 C=6 D=1030 'd_u'
00040 [L620] TGETS    A=4 B=4 C=13 D=1037 'getRealScale'
00041 [L620] MOV      A=5 B=0 C=3 D=3 
00042 [L620] CALL     A=4 B=3 C=2 D=770 
00043 [L622] MOV      A=7 B=0 C=1 D=1 
00044 [L622] TGETS    A=6 B=1 C=12 D=268 'addChild'
00045 [L622] GGET     A=8 B=0 C=5 D=5 'd_ms'
00046 [L622] TGETS    A=8 B=8 C=6 D=2054 'd_u'
00047 [L622] TGETS    A=8 B=8 C=10 D=2058 'createByStyle'
00048 [L622] TDUP     A=9 B=0 C=14 D=14 {'kind': 'table', 'value': {'pic': 'v2/turnTableUI/title.png', 'x': 0.5}}
00049 [L622] MULNV    A=10 B=5 C=0 D=1280 
00050 [L622] ADDNV    A=10 B=10 C=1 D=2561 
00051 [L622] TSETS    A=10 B=9 C=15 D=2319 'y'
00052 [L622] CALL     A=8 B=0 C=2 D=2 
00053 [L622] CALLM    A=6 B=1 C=1 D=257 
00054 [L627] TNEW     A=6 B=24 C=0 D=6144 
00055 [L628] GGET     A=7 B=0 C=5 D=5 'd_ms'
00056 [L628] TGETS    A=7 B=7 C=16 D=1808 'd_hz'
00057 [L628] TGETS    A=7 B=7 C=17 D=1809 'gethz'
00058 [L628] KSTR     A=8 B=0 C=18 D=18 'twoyears_info16'
00059 [L628] CALL     A=7 B=2 C=2 D=514 
00060 [L628] TSETB    A=7 B=6 C=1 D=1537 
00061 [L629] GGET     A=7 B=0 C=5 D=5 'd_ms'
00062 [L629] TGETS    A=7 B=7 C=16 D=1808 'd_hz'
00063 [L629] TGETS    A=7 B=7 C=17 D=1809 'gethz'
00064 [L629] KSTR     A=8 B=0 C=19 D=19 'twoyears_info17'
00065 [L629] CALL     A=7 B=2 C=2 D=514 
00066 [L629] TSETB    A=7 B=6 C=2 D=1538 
00067 [L630] GGET     A=7 B=0 C=5 D=5 'd_ms'
00068 [L630] TGETS    A=7 B=7 C=16 D=1808 'd_hz'
00069 [L630] TGETS    A=7 B=7 C=17 D=1809 'gethz'
00070 [L630] KSTR     A=8 B=0 C=19 D=19 'twoyears_info17'
00071 [L630] CALL     A=7 B=2 C=2 D=514 
00072 [L630] TSETB    A=7 B=6 C=3 D=1539 
00073 [L631] GGET     A=7 B=0 C=5 D=5 'd_ms'
00074 [L631] TGETS    A=7 B=7 C=16 D=1808 'd_hz'
00075 [L631] TGETS    A=7 B=7 C=17 D=1809 'gethz'
00076 [L631] KSTR     A=8 B=0 C=20 D=20 'twoyears_info18'
00077 [L631] CALL     A=7 B=2 C=2 D=514 
00078 [L631] TSETB    A=7 B=6 C=4 D=1540 
00079 [L632] GGET     A=7 B=0 C=5 D=5 'd_ms'
00080 [L632] TGETS    A=7 B=7 C=16 D=1808 'd_hz'
00081 [L632] TGETS    A=7 B=7 C=17 D=1809 'gethz'
00082 [L632] KSTR     A=8 B=0 C=20 D=20 'twoyears_info18'
00083 [L632] CALL     A=7 B=2 C=2 D=514 
00084 [L632] TSETB    A=7 B=6 C=5 D=1541 
00085 [L634] GGET     A=7 B=0 C=5 D=5 'd_ms'
00086 [L634] TGETS    A=7 B=7 C=16 D=1808 'd_hz'
00087 [L634] TGETS    A=7 B=7 C=17 D=1809 'gethz'
00088 [L634] KSTR     A=8 B=0 C=21 D=21 'twoyears_info25'
00089 [L634] CALL     A=7 B=2 C=2 D=514 
00090 [L635] GGET     A=8 B=0 C=5 D=5 'd_ms'
00091 [L635] TGETS    A=8 B=8 C=16 D=2064 'd_hz'
00092 [L635] TGETS    A=8 B=8 C=17 D=2065 'gethz'
00093 [L635] KSTR     A=9 B=0 C=22 D=22 'twoyears_info26'
00094 [L635] CALL     A=8 B=2 C=2 D=514 
00095 [L636] GGET     A=9 B=0 C=5 D=5 'd_ms'
00096 [L636] TGETS    A=9 B=9 C=16 D=2320 'd_hz'
00097 [L636] TGETS    A=9 B=9 C=17 D=2321 'gethz'
00098 [L636] KSTR     A=10 B=0 C=23 D=23 'twoyears_info27'
00099 [L636] CALL     A=9 B=2 C=2 D=514 
00100 [L638] UGET     A=10 B=0 C=1 D=1 CCSprite
00101 [L638] MOV      A=11 B=0 C=10 D=10 
00102 [L638] TGETS    A=10 B=10 C=24 D=2584 'create'
00103 [L638] KSTR     A=12 B=0 C=25 D=25 'v2/soulHuntUI/r_btn_prize1.png'
00104 [L638] CALL     A=10 B=2 C=3 D=515 
00105 [L639] UGET     A=11 B=0 C=1 D=1 CCSprite
00106 [L639] MOV      A=12 B=0 C=11 D=11 
00107 [L639] TGETS    A=11 B=11 C=24 D=2840 'create'
00108 [L639] KSTR     A=13 B=0 C=26 D=26 'v2/soulHuntUI/r_btn_prize2.png'
00109 [L639] CALL     A=11 B=2 C=3 D=515 
00110 [L641] GGET     A=12 B=0 C=0 D=0 'g_self'
00111 [L641] UGET     A=13 B=0 C=0 D=0 y_o_t
00112 [L641] TGETS    A=13 B=13 C=2 D=3330 'enter_activity'
00113 [L641] TGETV    A=12 B=12 C=13 D=3085 
00114 [L641] ISF      A=0 B=0 C=12 D=12 
00115 [L641] JMP      A=12 B=128 C=16 D=32784 target=132
00116 [L641] GGET     A=12 B=0 C=0 D=0 'g_self'
00117 [L641] UGET     A=13 B=0 C=0 D=0 y_o_t
00118 [L641] TGETS    A=13 B=13 C=2 D=3330 'enter_activity'
00119 [L641] TGETV    A=12 B=12 C=13 D=3085 
00120 [L641] TGETS    A=12 B=12 C=27 D=3099 'gift_list'
00121 [L641] ISF      A=0 B=0 C=12 D=12 
00122 [L641] JMP      A=12 B=128 C=9 D=32777 target=132
00123 [L641] GGET     A=12 B=0 C=0 D=0 'g_self'
00124 [L641] UGET     A=13 B=0 C=0 D=0 y_o_t
00125 [L641] TGETS    A=13 B=13 C=2 D=3330 'enter_activity'
00126 [L641] TGETV    A=12 B=12 C=13 D=3085 
00127 [L641] TGETS    A=12 B=12 C=27 D=3099 'gift_list'
00128 [L641] LEN      A=12 B=0 C=12 D=12 
00129 [L641] KSHORT   A=13 B=0 C=0 D=0 0
00130 [L641] ISGT     A=12 B=0 C=13 D=13 
00131 [L641] JMP      A=12 B=128 C=35 D=32803 target=167
00132 [L642] KSTR     A=12 B=0 C=28 D=28 ''
00133 [L643] GGET     A=13 B=0 C=29 D=29 'g_Color'
00134 [L643] TGETS    A=13 B=13 C=30 D=3358 'red'
00135 [L644] ISNEN    A=0 B=0 C=2 D=2 1
00136 [L644] JMP      A=14 B=128 C=2 D=32770 target=139
00137 [L645] TGETB    A=12 B=6 C=1 D=1537 
00138 [L645] JMP      A=14 B=128 C=3 D=32771 target=142
00139 [L647] MOV      A=12 B=0 C=7 D=7 
00140 [L648] GGET     A=14 B=0 C=29 D=29 'g_Color'
00141 [L648] TGETS    A=13 B=14 C=31 D=3615 'white'
00142 [L650] MOV      A=15 B=0 C=1 D=1 
00143 [L650] TGETS    A=14 B=1 C=12 D=268 'addChild'
00144 [L650] GGET     A=16 B=0 C=5 D=5 'd_ms'
00145 [L650] TGETS    A=16 B=16 C=6 D=4102 'd_u'
00146 [L650] TGETS    A=16 B=16 C=10 D=4106 'createByStyle'
00147 [L650] TDUP     A=17 B=0 C=32 D=32 {'kind': 'table', 'value': {'type': 'label', 'x': 0.5, 'fontsize': 26}}
00148 [L650] TSETS    A=12 B=17 C=33 D=4385 'string'
00149 [L650] MULVN    A=18 B=5 C=3 D=1283 
00150 [L650] SUBNV    A=18 B=18 C=1 D=4609 
00151 [L650] TSETS    A=18 B=17 C=15 D=4367 'y'
00152 [L650] TSETS    A=13 B=17 C=34 D=4386 'color'
00153 [L650] CALL     A=16 B=2 C=2 D=514 
00154 [L650] KSHORT   A=17 B=0 C=1 D=1 1
00155 [L650] CALL     A=14 B=1 C=4 D=260 
00156 [L654] GGET     A=14 B=0 C=5 D=5 'd_ms'
00157 [L654] TGETS    A=14 B=14 C=6 D=3590 'd_u'
00158 [L654] TGETS    A=14 B=14 C=35 D=3619 'graySprite'
00159 [L654] MOV      A=15 B=0 C=10 D=10 
00160 [L654] CALL     A=14 B=1 C=2 D=258 
00161 [L655] GGET     A=14 B=0 C=5 D=5 'd_ms'
00162 [L655] TGETS    A=14 B=14 C=6 D=3590 'd_u'
00163 [L655] TGETS    A=14 B=14 C=35 D=3619 'graySprite'
00164 [L655] MOV      A=15 B=0 C=11 D=11 
00165 [L655] CALL     A=14 B=1 C=2 D=258 
00166 [L655] JMP      A=12 B=128 C=148 D=32916 target=315
00167 [L656] GGET     A=12 B=0 C=0 D=0 'g_self'
00168 [L656] UGET     A=13 B=0 C=0 D=0 y_o_t
00169 [L656] TGETS    A=13 B=13 C=2 D=3330 'enter_activity'
00170 [L656] TGETV    A=12 B=12 C=13 D=3085 
00171 [L656] TGETS    A=12 B=12 C=27 D=3099 'gift_list'
00172 [L656] TGETV    A=12 B=12 C=0 D=3072 
00173 [L656] IST      A=0 B=0 C=12 D=12 
00174 [L656] JMP      A=12 B=128 C=62 D=32830 target=237
00175 [L657] KSTR     A=12 B=0 C=28 D=28 ''
00176 [L658] GGET     A=13 B=0 C=29 D=29 'g_Color'
00177 [L658] TGETS    A=13 B=13 C=30 D=3358 'red'
00178 [L659] GGET     A=14 B=0 C=0 D=0 'g_self'
00179 [L659] UGET     A=15 B=0 C=0 D=0 y_o_t
00180 [L659] TGETS    A=15 B=15 C=2 D=3842 'enter_activity'
00181 [L659] TGETV    A=14 B=14 C=15 D=3599 
00182 [L659] TGETS    A=14 B=14 C=27 D=3611 'gift_list'
00183 [L659] SUBVN    A=15 B=0 C=2 D=2 
00184 [L659] TGETV    A=14 B=14 C=15 D=3599 
00185 [L659] IST      A=0 B=0 C=14 D=14 
00186 [L659] JMP      A=14 B=128 C=4 D=32772 target=191
00187 [L660] MOV      A=12 B=0 C=7 D=7 
00188 [L661] GGET     A=14 B=0 C=29 D=29 'g_Color'
00189 [L661] TGETS    A=13 B=14 C=31 D=3615 'white'
00190 [L661] JMP      A=14 B=128 C=21 D=32789 target=212
00191 [L662] GGET     A=14 B=0 C=0 D=0 'g_self'
00192 [L662] UGET     A=15 B=0 C=0 D=0 y_o_t
00193 [L662] TGETS    A=15 B=15 C=2 D=3842 'enter_activity'
00194 [L662] TGETV    A=14 B=14 C=15 D=3599 
00195 [L662] TGETS    A=14 B=14 C=27 D=3611 'gift_list'
00196 [L662] SUBVN    A=15 B=0 C=2 D=2 
00197 [L662] TGETV    A=14 B=14 C=15 D=3599 
00198 [L662] ISF      A=0 B=0 C=14 D=14 
00199 [L662] JMP      A=15 B=128 C=11 D=32779 target=211
00200 [L662] GGET     A=14 B=0 C=0 D=0 'g_self'
00201 [L662] UGET     A=15 B=0 C=0 D=0 y_o_t
00202 [L662] TGETS    A=15 B=15 C=2 D=3842 'enter_activity'
00203 [L662] TGETV    A=14 B=14 C=15 D=3599 
00204 [L662] TGETS    A=14 B=14 C=36 D=3620 'is_today_charge'
00205 [L662] ISF      A=0 B=0 C=14 D=14 
00206 [L662] JMP      A=15 B=128 C=4 D=32772 target=211
00207 [L663] MOV      A=12 B=0 C=7 D=7 
00208 [L664] GGET     A=14 B=0 C=29 D=29 'g_Color'
00209 [L664] TGETS    A=13 B=14 C=31 D=3615 'white'
00210 [L664] JMP      A=14 B=128 C=1 D=32769 target=212
00211 [L666] TGETV    A=12 B=6 C=0 D=1536 
00212 [L668] MOV      A=15 B=0 C=1 D=1 
00213 [L668] TGETS    A=14 B=1 C=12 D=268 'addChild'
00214 [L668] GGET     A=16 B=0 C=5 D=5 'd_ms'
00215 [L668] TGETS    A=16 B=16 C=6 D=4102 'd_u'
00216 [L668] TGETS    A=16 B=16 C=10 D=4106 'createByStyle'
00217 [L668] TDUP     A=17 B=0 C=37 D=37 {'kind': 'table', 'value': {'type': 'label', 'x': 0.5, 'fontsize': 26}}
00218 [L668] TSETS    A=12 B=17 C=33 D=4385 'string'
00219 [L668] MULVN    A=18 B=5 C=3 D=1283 
00220 [L668] SUBNV    A=18 B=18 C=1 D=4609 
00221 [L668] TSETS    A=18 B=17 C=15 D=4367 'y'
00222 [L668] TSETS    A=13 B=17 C=34 D=4386 'color'
00223 [L668] CALL     A=16 B=2 C=2 D=514 
00224 [L668] KSHORT   A=17 B=0 C=1 D=1 1
00225 [L668] CALL     A=14 B=1 C=4 D=260 
00226 [L671] GGET     A=14 B=0 C=5 D=5 'd_ms'
00227 [L671] TGETS    A=14 B=14 C=6 D=3590 'd_u'
00228 [L671] TGETS    A=14 B=14 C=35 D=3619 'graySprite'
00229 [L671] MOV      A=15 B=0 C=10 D=10 
00230 [L671] CALL     A=14 B=1 C=2 D=258 
00231 [L672] GGET     A=14 B=0 C=5 D=5 'd_ms'
00232 [L672] TGETS    A=14 B=14 C=6 D=3590 'd_u'
00233 [L672] TGETS    A=14 B=14 C=35 D=3619 'graySprite'
00234 [L672] MOV      A=15 B=0 C=11 D=11 
00235 [L672] CALL     A=14 B=1 C=2 D=258 
00236 [L672] JMP      A=12 B=128 C=78 D=32846 target=315
00237 [L673] GGET     A=12 B=0 C=0 D=0 'g_self'
00238 [L673] UGET     A=13 B=0 C=0 D=0 y_o_t
00239 [L673] TGETS    A=13 B=13 C=2 D=3330 'enter_activity'
00240 [L673] TGETV    A=12 B=12 C=13 D=3085 
00241 [L673] TGETS    A=12 B=12 C=27 D=3099 'gift_list'
00242 [L673] TGETV    A=12 B=12 C=0 D=3072 
00243 [L673] ISF      A=0 B=0 C=12 D=12 
00244 [L673] JMP      A=13 B=128 C=36 D=32804 target=281
00245 [L673] GGET     A=12 B=0 C=0 D=0 'g_self'
00246 [L673] UGET     A=13 B=0 C=0 D=0 y_o_t
00247 [L673] TGETS    A=13 B=13 C=2 D=3330 'enter_activity'
00248 [L673] TGETV    A=12 B=12 C=13 D=3085 
00249 [L673] TGETS    A=12 B=12 C=27 D=3099 'gift_list'
00250 [L673] TGETV    A=12 B=12 C=0 D=3072 
00251 [L673] ISNEN    A=12 B=0 C=4 D=4 0
00252 [L673] JMP      A=12 B=128 C=28 D=32796 target=281
00253 [L674] MOV      A=12 B=0 C=9 D=9 
00254 [L675] GGET     A=13 B=0 C=29 D=29 'g_Color'
00255 [L675] TGETS    A=13 B=13 C=31 D=3359 'white'
00256 [L678] GGET     A=14 B=0 C=5 D=5 'd_ms'
00257 [L678] TGETS    A=14 B=14 C=6 D=3590 'd_u'
00258 [L678] TGETS    A=14 B=14 C=35 D=3619 'graySprite'
00259 [L678] MOV      A=15 B=0 C=10 D=10 
00260 [L678] CALL     A=14 B=1 C=2 D=258 
00261 [L679] GGET     A=14 B=0 C=5 D=5 'd_ms'
00262 [L679] TGETS    A=14 B=14 C=6 D=3590 'd_u'
00263 [L679] TGETS    A=14 B=14 C=35 D=3619 'graySprite'
00264 [L679] MOV      A=15 B=0 C=11 D=11 
00265 [L679] CALL     A=14 B=1 C=2 D=258 
00266 [L680] MOV      A=15 B=0 C=1 D=1 
00267 [L680] TGETS    A=14 B=1 C=12 D=268 'addChild'
00268 [L680] GGET     A=16 B=0 C=5 D=5 'd_ms'
00269 [L680] TGETS    A=16 B=16 C=6 D=4102 'd_u'
00270 [L680] TGETS    A=16 B=16 C=10 D=4106 'createByStyle'
00271 [L680] TDUP     A=17 B=0 C=38 D=38 {'kind': 'table', 'value': {'type': 'label', 'x': 0.5, 'fontsize': 26}}
00272 [L680] TSETS    A=12 B=17 C=33 D=4385 'string'
00273 [L680] MULVN    A=18 B=5 C=3 D=1283 
00274 [L680] SUBNV    A=18 B=18 C=1 D=4609 
00275 [L680] TSETS    A=18 B=17 C=15 D=4367 'y'
00276 [L680] TSETS    A=13 B=17 C=34 D=4386 'color'
00277 [L680] CALL     A=16 B=2 C=2 D=514 
00278 [L680] KSHORT   A=17 B=0 C=1 D=1 1
00279 [L680] CALL     A=14 B=1 C=4 D=260 
00280 [L680] JMP      A=12 B=128 C=34 D=32802 target=315
00281 [L681] GGET     A=12 B=0 C=0 D=0 'g_self'
00282 [L681] UGET     A=13 B=0 C=0 D=0 y_o_t
00283 [L681] TGETS    A=13 B=13 C=2 D=3330 'enter_activity'
00284 [L681] TGETV    A=12 B=12 C=13 D=3085 
00285 [L681] TGETS    A=12 B=12 C=27 D=3099 'gift_list'
00286 [L681] TGETV    A=12 B=12 C=0 D=3072 
00287 [L681] ISF      A=0 B=0 C=12 D=12 
00288 [L681] JMP      A=13 B=128 C=26 D=32794 target=315
00289 [L681] GGET     A=12 B=0 C=0 D=0 'g_self'
00290 [L681] UGET     A=13 B=0 C=0 D=0 y_o_t
00291 [L681] TGETS    A=13 B=13 C=2 D=3330 'enter_activity'
00292 [L681] TGETV    A=12 B=12 C=13 D=3085 
00293 [L681] TGETS    A=12 B=12 C=27 D=3099 'gift_list'
00294 [L681] TGETV    A=12 B=12 C=0 D=3072 
00295 [L681] KSHORT   A=13 B=0 C=0 D=0 0
00296 [L681] ISGE     A=13 B=0 C=12 D=12 
00297 [L681] JMP      A=12 B=128 C=17 D=32785 target=315
00298 [L682] MOV      A=12 B=0 C=8 D=8 
00299 [L683] GGET     A=13 B=0 C=29 D=29 'g_Color'
00300 [L683] TGETS    A=13 B=13 C=39 D=3367 'green'
00301 [L684] MOV      A=15 B=0 C=1 D=1 
00302 [L684] TGETS    A=14 B=1 C=12 D=268 'addChild'
00303 [L684] GGET     A=16 B=0 C=5 D=5 'd_ms'
00304 [L684] TGETS    A=16 B=16 C=6 D=4102 'd_u'
00305 [L684] TGETS    A=16 B=16 C=10 D=4106 'createByStyle'
00306 [L684] TDUP     A=17 B=0 C=40 D=40 {'kind': 'table', 'value': {'type': 'label', 'x': 0.5, 'fontsize': 26}}
00307 [L684] TSETS    A=12 B=17 C=33 D=4385 'string'
00308 [L684] MULVN    A=18 B=5 C=3 D=1283 
00309 [L684] SUBNV    A=18 B=18 C=1 D=4609 
00310 [L684] TSETS    A=18 B=17 C=15 D=4367 'y'
00311 [L684] TSETS    A=13 B=17 C=34 D=4386 'color'
00312 [L684] CALL     A=16 B=2 C=2 D=514 
00313 [L684] KSHORT   A=17 B=0 C=1 D=1 1
00314 [L684] CALL     A=14 B=1 C=4 D=260 
00315 [L689] FNEW     A=12 B=0 C=41 D=41 {'kind': 'proto', 'id': 19}
00316 [L691] MOV      A=13 B=0 C=2 D=2 
00317 [L697] FNEW     A=14 B=0 C=42 D=42 {'kind': 'proto', 'id': 20}
00318 [L701] FNEW     A=15 B=0 C=43 D=43 {'kind': 'proto', 'id': 21}
00319 [L699] GSET     A=15 B=0 C=44 D=44 'getGift'
00320 [L702] TDUP     A=15 B=0 C=45 D=45 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00321 [L705] TDUP     A=16 B=0 C=46 D=46 {'kind': 'table', 'value': {'x': 0.5}}
00322 [L706] TSETS    A=10 B=16 C=47 D=4143 'nsprite'
00323 [L706] TSETS    A=11 B=16 C=48 D=4144 'ssprite'
00324 [L706] MULNV    A=17 B=5 C=5 D=1285 
00325 [L706] SUBNV    A=17 B=17 C=1 D=4353 
00326 [L706] TSETS    A=17 B=16 C=15 D=4111 'y'
00327 [L706] GGET     A=17 B=0 C=44 D=44 'getGift'
00328 [L706] TSETS    A=17 B=16 C=49 D=4145 'call_back'
00329 [L706] TSETB    A=16 B=15 C=1 D=3841 
00330 [L706] TDUP     A=16 B=0 C=50 D=50 {'kind': 'table', 'value': {'npic': 'v2/common/close1.png', 'spic': 'v2/common/close2.png'}}
00331 [L707] MULVN    A=17 B=4 C=5 D=1029 
00332 [L707] ADDNV    A=17 B=17 C=1 D=4353 
00333 [L707] TSETS    A=17 B=16 C=51 D=4147 'x'
00334 [L707] MULVN    A=17 B=5 C=0 D=1280 
00335 [L707] ADDNV    A=17 B=17 C=1 D=4353 
00336 [L707] TSETS    A=17 B=16 C=15 D=4111 'y'
00337 [L707] TSETS    A=12 B=16 C=49 D=4145 'call_back'
00338 [L707] TSETB    A=16 B=15 C=2 D=3842 
00339 [L710] KSHORT   A=16 B=0 C=1 D=1 1
00340 [L710] LEN      A=17 B=0 C=13 D=13 
00341 [L710] KSHORT   A=18 B=0 C=1 D=1 1
00342 [L710] FORI     A=16 B=128 C=47 D=32815 target=390
00343 [L711] MULNV    A=20 B=4 C=6 D=1030 
00344 [L711] SUBNV    A=20 B=20 C=1 D=5121 
00345 [L711] SUBVN    A=21 B=19 C=2 D=4866 
00346 [L711] MODVN    A=21 B=21 C=7 D=5383 
00347 [L711] MULVN    A=21 B=21 C=6 D=5382 
00348 [L711] MULVV    A=21 B=21 C=4 D=5380 
00349 [L711] ADDVV    A=20 B=20 C=21 D=5141 
00350 [L711] MULNV    A=21 B=5 C=8 D=1288 
00351 [L711] ADDNV    A=21 B=21 C=1 D=5377 
00352 [L711] UGET     A=22 B=0 C=2 D=2 math
00353 [L711] TGETS    A=22 B=22 C=52 D=5684 'floor'
00354 [L711] SUBVN    A=23 B=19 C=2 D=4866 
00355 [L711] DIVVN    A=23 B=23 C=7 D=5895 
00356 [L711] CALL     A=22 B=2 C=2 D=514 
00357 [L711] MULVN    A=22 B=22 C=9 D=5641 
00358 [L711] MULVV    A=22 B=22 C=5 D=5637 
00359 [L711] SUBVV    A=21 B=21 C=22 D=5398 
00360 [L712] MOV      A=23 B=0 C=1 D=1 
00361 [L712] TGETS    A=22 B=1 C=12 D=268 'addChild'
00362 [L712] GGET     A=24 B=0 C=5 D=5 'd_ms'
00363 [L712] TGETS    A=24 B=24 C=6 D=6150 'd_u'
00364 [L712] TGETS    A=24 B=24 C=10 D=6154 'createByStyle'
00365 [L712] TDUP     A=25 B=0 C=53 D=53 {'kind': 'table', 'value': {'pic': 'v2/turnTableUI/icon_bkg.png'}}
00366 [L712] TSETS    A=20 B=25 C=51 D=6451 'x'
00367 [L712] TSETS    A=21 B=25 C=15 D=6415 'y'
00368 [L712] CALL     A=24 B=2 C=2 D=514 
00369 [L712] KSHORT   A=25 B=0 C=1 D=1 1
00370 [L712] CALL     A=22 B=1 C=4 D=260 
00371 [L714] GGET     A=22 B=0 C=5 D=5 'd_ms'
00372 [L714] TGETS    A=22 B=22 C=54 D=5686 'd_actNoticeUI'
00373 [L714] TGETS    A=22 B=22 C=55 D=5687 'getSprite'
00374 [L714] TGETV    A=23 B=13 C=19 D=3347 
00375 [L714] CALL     A=22 B=2 C=2 D=514 
00376 [L716] UGET     A=23 B=0 C=3 D=3 table
00377 [L716] TGETS    A=23 B=23 C=56 D=5944 'insert'
00378 [L716] MOV      A=24 B=0 C=15 D=15 
00379 [L716] TDUP     A=25 B=0 C=57 D=57 {'kind': 'table', 'value': {}}
00380 [L716] TSETS    A=22 B=25 C=47 D=6447 'nsprite'
00381 [L716] TSETS    A=22 B=25 C=48 D=6448 'ssprite'
00382 [L716] MULNV    A=26 B=4 C=10 D=1034 
00383 [L716] TSETS    A=26 B=25 C=58 D=6458 'scale'
00384 [L716] TSETS    A=20 B=25 C=51 D=6451 'x'
00385 [L716] TSETS    A=21 B=25 C=15 D=6415 'y'
00386 [L716] TSETS    A=19 B=25 C=59 D=6459 'tag'
00387 [L716] TSETS    A=14 B=25 C=49 D=6449 'call_back'
00388 [L716] CALL     A=23 B=1 C=3 D=259 
00389 [L710] FORL     A=16 B=127 C=209 D=32721 target=343
00390 [L718] TNEW     A=16 B=0 C=0 D=0 
00391 [L719] MOV      A=18 B=0 C=1 D=1 
00392 [L719] TGETS    A=17 B=1 C=12 D=268 'addChild'
00393 [L719] GGET     A=19 B=0 C=5 D=5 'd_ms'
00394 [L719] TGETS    A=19 B=19 C=6 D=4870 'd_u'
00395 [L719] TGETS    A=19 B=19 C=60 D=4924 'createMenu'
00396 [L719] MOV      A=20 B=0 C=15 D=15 
00397 [L719] MOV      A=21 B=0 C=16 D=16 
00398 [L719] CALL     A=19 B=2 C=3 D=515 
00399 [L719] KSHORT   A=20 B=0 C=10 D=10 10
00400 [L719] CALL     A=17 B=1 C=4 D=260 
00401 [L721] UCLO     A=0 B=128 C=0 D=32768 target=402
00402 [L721] RET0     A=0 B=0 C=1 D=1 
00403 [L721] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto23 offset=0x533b source_lines=722-729 params=0
UPVALUES ['y_o_t']
00001 [L723] TNEW     A=0 B=0 C=0 D=0 
00002 [L723] GSET     A=0 B=0 C=0 D=0 'tmp_req'
00003 [L724] GGET     A=0 B=0 C=0 D=0 'tmp_req'
00004 [L724] UGET     A=1 B=0 C=0 D=0 y_o_t
00005 [L724] TGETS    A=1 B=1 C=2 D=258 'wish_yuanshi'
00006 [L724] TSETS    A=1 B=0 C=1 D=1 'flag'
00007 [L725] GGET     A=0 B=0 C=0 D=0 'tmp_req'
00008 [L725] KSHORT   A=1 B=0 C=0 D=0 0
00009 [L725] TSETS    A=1 B=0 C=3 D=3 'index'
00010 [L727] GGET     A=0 B=0 C=4 D=4 'd_ms'
00011 [L727] TGETS    A=0 B=0 C=5 D=5 'd_u'
00012 [L727] TGETS    A=0 B=0 C=6 D=6 'main_server_send_msg'
00013 [L727] GGET     A=1 B=0 C=4 D=4 'd_ms'
00014 [L727] TGETS    A=1 B=1 C=7 D=263 'd_msg_def'
00015 [L727] TGETS    A=1 B=1 C=8 D=264 'gscl_msg_id'
00016 [L727] TGETS    A=1 B=1 C=9 D=265 'msg_yuanshi_activity'
00017 [L727] GGET     A=2 B=0 C=0 D=0 'tmp_req'
00018 [L727] CALL     A=0 B=1 C=3 D=259 
00019 [L729] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto24 offset=0x5419 source_lines=0-729 params=0
UPVALUES []
00001 [L1] GGET     A=0 B=0 C=0 D=0 'require'
00002 [L2] GGET     A=1 B=0 C=1 D=1 'type'
00003 [L3] GGET     A=2 B=0 C=2 D=2 'print'
00004 [L4] GGET     A=3 B=0 C=3 D=3 'tostring'
00005 [L5] GGET     A=4 B=0 C=4 D=4 'pairs'
00006 [L6] GGET     A=5 B=0 C=5 D=5 'string'
00007 [L7] GGET     A=6 B=0 C=6 D=6 'table'
00008 [L8] GGET     A=7 B=0 C=7 D=7 'math'
00009 [L10] GGET     A=8 B=0 C=8 D=8 'main_server'
00010 [L11] GGET     A=9 B=0 C=9 D=9 '_G'
00011 [L12] GGET     A=10 B=0 C=10 D=10 'bits'
00012 [L13] GGET     A=11 B=0 C=11 D=11 'tonumber'
00013 [L14] GGET     A=12 B=0 C=12 D=12 'os'
00014 [L15] GGET     A=13 B=0 C=13 D=13 'io'
00015 [L16] GGET     A=14 B=0 C=14 D=14 'tolua'
00016 [L17] GGET     A=15 B=0 C=15 D=15 'package'
00017 [L18] GGET     A=16 B=0 C=16 D=16 'CCFadeIn'
00018 [L24] GGET     A=17 B=0 C=17 D=17 'CCArray'
00019 [L25] GGET     A=18 B=0 C=18 D=18 'CCDirector'
00020 [L26] GGET     A=19 B=0 C=19 D=19 'CCLayer'
00021 [L27] GGET     A=20 B=0 C=20 D=20 'CCMenu'
00022 [L28] GGET     A=21 B=0 C=21 D=21 'CCSprite'
00023 [L29] GGET     A=22 B=0 C=22 D=22 'CCMenuItemImage'
00024 [L30] GGET     A=23 B=0 C=23 D=23 'ccp'
00025 [L31] GGET     A=24 B=0 C=24 D=24 'ccpAdd'
00026 [L32] GGET     A=25 B=0 C=25 D=25 'CCLuaLog'
00027 [L33] GGET     A=26 B=0 C=26 D=26 'CCSizeMake'
00028 [L34] GGET     A=27 B=0 C=27 D=27 'ccc3'
00029 [L35] GGET     A=28 B=0 C=28 D=28 'CCNode'
00030 [L36] GGET     A=29 B=0 C=29 D=29 'CCScene'
00031 [L37] GGET     A=30 B=0 C=30 D=30 'CCRectMake'
00032 [L38] GGET     A=31 B=0 C=31 D=31 'CCTOUCHBEGAN'
00033 [L39] GGET     A=32 B=0 C=32 D=32 'CCTOUCHMOVED'
00034 [L40] GGET     A=33 B=0 C=33 D=33 'CCTOUCHENDED'
00035 [L41] GGET     A=34 B=0 C=34 D=34 'CCMoveBy'
00036 [L42] GGET     A=35 B=0 C=35 D=35 'CCCallFuncN'
00037 [L43] GGET     A=36 B=0 C=36 D=36 'CCSequence'
00038 [L44] GGET     A=37 B=0 C=37 D=37 'CCLayerColor'
00039 [L45] GGET     A=38 B=0 C=38 D=38 'ccc4'
00040 [L46] GGET     A=39 B=0 C=39 D=39 'CCTextFieldTTF'
00041 [L47] GGET     A=40 B=0 C=40 D=40 'kCCTextAlignmentLeft'
00042 [L48] GGET     A=41 B=0 C=41 D=41 'CCMenuItemLabel'
00043 [L49] GGET     A=42 B=0 C=42 D=42 'CCLabelTTF'
00044 [L50] GGET     A=43 B=0 C=43 D=43 'CCMenuItemSprite'
00045 [L51] GGET     A=44 B=0 C=44 D=44 'CCRenderTexture'
00046 [L52] GGET     A=45 B=0 C=45 D=45 'CCPointMake'
00047 [L54] GGET     A=46 B=0 C=46 D=46 'module'
00048 [L54] KSTR     A=47 B=0 C=47 D=47 'ui.twoYearsCelebrateUI'
00049 [L54] CALL     A=46 B=1 C=2 D=258 
00050 [L57] MOV      A=46 B=0 C=0 D=0 
00051 [L57] KSTR     A=47 B=0 C=48 D=48 'ms'
00052 [L57] CALL     A=46 B=2 C=2 D=514 
00053 [L57] GSET     A=46 B=0 C=49 D=49 'd_ms'
00054 [L58] GGET     A=46 B=0 C=49 D=49 'd_ms'
00055 [L58] IST      A=0 B=0 C=46 D=46 
00056 [L58] JMP      A=46 B=128 C=3 D=32771 target=60
00057 [L59] MOV      A=46 B=0 C=2 D=2 
00058 [L59] KSTR     A=47 B=0 C=50 D=50 'twoYearsCelebrateUI load d_ms fail.\n'
00059 [L59] CALL     A=46 B=1 C=2 D=258 
00060 [L64] FNEW     A=46 B=0 C=51 D=51 {'kind': 'proto', 'id': 0}
00061 [L67] GGET     A=47 B=0 C=49 D=49 'd_ms'
00062 [L67] TGETS    A=47 B=47 C=52 D=12084 'd_common_def'
00063 [L67] TGETS    A=47 B=47 C=53 D=12085 'yuanshi_operate'
00064 [L68] GGET     A=48 B=0 C=49 D=49 'd_ms'
00065 [L68] TGETS    A=48 B=48 C=52 D=12340 'd_common_def'
00066 [L68] TGETS    A=48 B=48 C=54 D=12342 'object_type'
00067 [L70] MOV      A=50 B=0 C=18 D=18 
00068 [L70] TGETS    A=49 B=18 C=55 D=4663 'sharedDirector'
00069 [L70] CALL     A=49 B=2 C=2 D=514 
00070 [L70] MOV      A=50 B=0 C=49 D=49 
00071 [L70] TGETS    A=49 B=49 C=56 D=12600 'getVisibleSize'
00072 [L70] CALL     A=49 B=2 C=2 D=514 
00073 [L71] GGET     A=50 B=0 C=49 D=49 'd_ms'
00074 [L71] TGETS    A=50 B=50 C=57 D=12857 'd_c'
00075 [L71] TGETS    A=50 B=50 C=58 D=12858 'g_tags'
00076 [L71] TGETS    A=50 B=50 C=59 D=12859 'TAG_twoYearsCelebrateUI'
00077 [L71] GSET     A=50 B=0 C=60 D=60 'g_twoYearsCelebrateUI'
00078 [L72] TNEW     A=50 B=0 C=0 D=0 
00079 [L72] GSET     A=50 B=0 C=61 D=61 'g_self'
00080 [L73] TNEW     A=50 B=0 C=0 D=0 
00081 [L73] GSET     A=50 B=0 C=62 D=62 'g_Color'
00082 [L74] GGET     A=50 B=0 C=62 D=62 'g_Color'
00083 [L74] TDUP     A=51 B=0 C=64 D=64 {'kind': 'table', 'value': {1: 0, 2: 0, 3: 0}}
00084 [L74] TSETS    A=51 B=50 C=63 D=12863 'black'
00085 [L75] GGET     A=50 B=0 C=62 D=62 'g_Color'
00086 [L75] TDUP     A=51 B=0 C=66 D=66 {'kind': 'table', 'value': {1: 255, 2: 255, 3: 255}}
00087 [L75] TSETS    A=51 B=50 C=65 D=12865 'white'
00088 [L76] GGET     A=50 B=0 C=62 D=62 'g_Color'
00089 [L76] TDUP     A=51 B=0 C=68 D=68 {'kind': 'table', 'value': {1: 0, 2: 255, 3: 0}}
00090 [L76] TSETS    A=51 B=50 C=67 D=12867 'green'
00091 [L77] GGET     A=50 B=0 C=62 D=62 'g_Color'
00092 [L77] TDUP     A=51 B=0 C=70 D=70 {'kind': 'table', 'value': {1: 255, 2: 0, 3: 0}}
00093 [L77] TSETS    A=51 B=50 C=69 D=12869 'red'
00094 [L79] GGET     A=50 B=0 C=61 D=61 'g_self'
00095 [L79] KSHORT   A=51 B=48 C=57 D=12345 12345
00096 [L79] TSETS    A=51 B=50 C=71 D=12871 'newTag'
00097 [L80] GGET     A=50 B=0 C=61 D=61 'g_self'
00098 [L80] KSHORT   A=51 B=48 C=58 D=12346 12346
00099 [L80] TSETS    A=51 B=50 C=72 D=12872 'shopTag'
00100 [L81] GGET     A=50 B=0 C=61 D=61 'g_self'
00101 [L81] KSHORT   A=51 B=48 C=59 D=12347 12347
00102 [L81] TSETS    A=51 B=50 C=73 D=12873 'redPointTag'
00103 [L82] GGET     A=50 B=0 C=61 D=61 'g_self'
00104 [L82] KSHORT   A=51 B=48 C=60 D=12348 12348
00105 [L82] TSETS    A=51 B=50 C=74 D=12874 'timeTag'
00106 [L83] GGET     A=50 B=0 C=61 D=61 'g_self'
00107 [L83] KSHORT   A=51 B=5 C=69 D=1349 1349
00108 [L83] TSETS    A=51 B=50 C=75 D=12875 'detailTag'
00109 [L84] GGET     A=50 B=0 C=61 D=61 'g_self'
00110 [L84] KNUM     A=51 B=0 C=0 D=0 0.38
00111 [L84] TSETS    A=51 B=50 C=76 D=12876 'x1'
00112 [L85] GGET     A=50 B=0 C=61 D=61 'g_self'
00113 [L85] KNUM     A=51 B=0 C=1 D=1 0.62
00114 [L85] TSETS    A=51 B=50 C=77 D=12877 'x2'
00115 [L86] GGET     A=50 B=0 C=61 D=61 'g_self'
00116 [L86] KNUM     A=51 B=0 C=2 D=2 0.5
00117 [L86] TSETS    A=51 B=50 C=78 D=12878 'y1'
00118 [L106] FNEW     A=50 B=0 C=79 D=79 {'kind': 'proto', 'id': 1}
00119 [L90] GSET     A=50 B=0 C=80 D=80 'show'
00120 [L111] FNEW     A=50 B=0 C=81 D=81 {'kind': 'proto', 'id': 2}
00121 [L108] GSET     A=50 B=0 C=82 D=82 'create'
00122 [L169] FNEW     A=50 B=0 C=83 D=83 {'kind': 'proto', 'id': 3}
00123 [L113] GSET     A=50 B=0 C=84 D=84 'createMainFrame'
00124 [L178] FNEW     A=50 B=0 C=85 D=85 {'kind': 'proto', 'id': 4}
00125 [L171] GSET     A=50 B=0 C=86 D=86 'call_back_close'
00126 [L190] FNEW     A=50 B=0 C=87 D=87 {'kind': 'proto', 'id': 5}
00127 [L180] GSET     A=50 B=0 C=88 D=88 'createShop'
00128 [L207] FNEW     A=50 B=0 C=89 D=89 {'kind': 'proto', 'id': 6}
00129 [L191] GSET     A=50 B=0 C=90 D=90 'pray'
00130 [L221] FNEW     A=50 B=0 C=91 D=91 {'kind': 'proto', 'id': 7}
00131 [L210] GSET     A=50 B=0 C=92 D=92 'canJoin'
00132 [L229] FNEW     A=50 B=0 C=93 D=93 {'kind': 'proto', 'id': 8}
00133 [L224] GSET     A=50 B=0 C=94 D=94 'closeShop'
00134 [L331] FNEW     A=50 B=0 C=95 D=95 {'kind': 'proto', 'id': 10}
00135 [L232] GSET     A=50 B=0 C=96 D=96 'showShop'
00136 [L358] FNEW     A=50 B=0 C=97 D=97 {'kind': 'proto', 'id': 11}
00137 [L333] GSET     A=50 B=0 C=98 D=98 'onGetResult'
00138 [L381] FNEW     A=50 B=0 C=99 D=99 {'kind': 'proto', 'id': 12}
00139 [L359] GSET     A=50 B=0 C=100 D=100 'updateShopNews'
00140 [L533] FNEW     A=50 B=0 C=101 D=101 {'kind': 'proto', 'id': 13}
00141 [L383] GSET     A=50 B=0 C=102 D=102 'showNews'
00142 [L552] FNEW     A=50 B=0 C=103 D=103 {'kind': 'proto', 'id': 14}
00143 [L535] GSET     A=50 B=0 C=104 D=104 'buy'
00144 [L560] FNEW     A=50 B=0 C=105 D=105 {'kind': 'proto', 'id': 15}
00145 [L554] GSET     A=50 B=0 C=106 D=106 'openGiftPack'
00146 [L576] FNEW     A=50 B=0 C=107 D=107 {'kind': 'proto', 'id': 16}
00147 [L561] GSET     A=50 B=0 C=108 D=108 'openGiftPackEnsure'
00148 [L582] FNEW     A=50 B=0 C=109 D=109 {'kind': 'proto', 'id': 17}
00149 [L578] GSET     A=50 B=0 C=110 D=110 'recharge'
00150 [L604] FNEW     A=50 B=0 C=111 D=111 {'kind': 'proto', 'id': 18}
00151 [L584] GSET     A=50 B=0 C=112 D=112 'tickTime'
00152 [L721] FNEW     A=50 B=0 C=113 D=113 {'kind': 'proto', 'id': 22}
00153 [L608] GSET     A=50 B=0 C=114 D=114 'showGiftDetail'
00154 [L729] FNEW     A=50 B=0 C=115 D=115 {'kind': 'proto', 'id': 23}
00155 [L722] GSET     A=50 B=0 C=116 D=116 'getChar'
00156 [L729] UCLO     A=0 B=128 C=0 D=32768 target=157
00157 [L729] RET0     A=0 B=0 C=1 D=1 
