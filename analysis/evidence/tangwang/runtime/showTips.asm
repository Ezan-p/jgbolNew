LuaJIT dump version=1; source='@D:\\mg_update_\\lua_cache\\lua1\\0aaf9138ef79f4065afb567aa3dec130.data'; root=proto1

FUNCTION proto0 offset=0x4a source_lines=819-822 params=0
UPVALUES ['layer']
00001 [L820] GGET     A=0 B=0 C=0 D=0 'g_cardUI'
00002 [L820] TGETS    A=0 B=0 C=1 D=1 'main_layer'
00003 [L820] MOV      A=1 B=0 C=0 D=0 
00004 [L820] TGETS    A=0 B=0 C=2 D=2 'removeChild'
00005 [L820] UGET     A=2 B=0 C=0 D=0 layer
00006 [L820] KPRI     A=3 B=0 C=2 D=2 
00007 [L820] CALL     A=0 B=1 C=4 D=260 
00008 [L821] KPRI     A=0 B=0 C=2 D=2 
00009 [L821] RET1     A=0 B=0 C=2 D=2 

FUNCTION proto1 offset=0xad source_lines=800-832 params=0
UPVALUES ['CCLayer']
00001 [L801] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L801] TGETS    A=0 B=0 C=1 D=1 'd_data'
00003 [L801] TGETS    A=0 B=0 C=2 D=2 'getCardTipConfig'
00004 [L801] CALL     A=0 B=1 C=1 D=257 
00005 [L802] GGET     A=0 B=0 C=0 D=0 'd_ms'
00006 [L802] TGETS    A=0 B=0 C=1 D=1 'd_data'
00007 [L802] TGETS    A=0 B=0 C=3 D=3 'g_card_tip'
00008 [L803] UGET     A=1 B=0 C=0 D=0 CCLayer
00009 [L803] MOV      A=2 B=0 C=1 D=1 
00010 [L803] TGETS    A=1 B=1 C=4 D=260 'create'
00011 [L803] CALL     A=1 B=2 C=2 D=514 
00012 [L805] GGET     A=2 B=0 C=0 D=0 'd_ms'
00013 [L805] TGETS    A=2 B=2 C=5 D=517 'd_u'
00014 [L805] TGETS    A=2 B=2 C=6 D=518 'createByStyles'
00015 [L805] TDUP     A=3 B=0 C=7 D=7 {'kind': 'table', 'value': {'x': 0.5, 'pic': 'v2/CardUI/tip_bkg.png', 'y': 0.5}}
00016 [L805] CALL     A=2 B=2 C=2 D=514 
00017 [L806] MOV      A=4 B=0 C=1 D=1 
00018 [L806] TGETS    A=3 B=1 C=8 D=264 'addChild'
00019 [L806] MOV      A=5 B=0 C=2 D=2 
00020 [L806] CALL     A=3 B=1 C=3 D=259 
00021 [L807] GGET     A=3 B=0 C=0 D=0 'd_ms'
00022 [L807] TGETS    A=3 B=3 C=5 D=773 'd_u'
00023 [L807] TGETS    A=3 B=3 C=9 D=777 'getRealScale'
00024 [L807] MOV      A=4 B=0 C=2 D=2 
00025 [L807] CALL     A=3 B=3 C=2 D=770 
00026 [L808] MOV      A=6 B=0 C=1 D=1 
00027 [L808] TGETS    A=5 B=1 C=8 D=264 'addChild'
00028 [L808] GGET     A=7 B=0 C=0 D=0 'd_ms'
00029 [L808] TGETS    A=7 B=7 C=5 D=1797 'd_u'
00030 [L808] TGETS    A=7 B=7 C=10 D=1802 'createByStyle'
00031 [L808] TDUP     A=8 B=0 C=11 D=11 {'kind': 'table', 'value': {'fontsize': 30, 'font': 'arial', 'type': 'label'}}
00032 [L808] GGET     A=9 B=0 C=0 D=0 'd_ms'
00033 [L808] TGETS    A=9 B=9 C=12 D=2316 'd_hz'
00034 [L808] TGETS    A=9 B=9 C=13 D=2317 'gethz'
00035 [L808] KSTR     A=10 B=0 C=14 D=14 'springCardTip6'
00036 [L808] CALL     A=9 B=2 C=2 D=514 
00037 [L808] TSETS    A=9 B=8 C=15 D=2063 'string'
00038 [L808] TDUP     A=9 B=0 C=16 D=16 {'kind': 'table', 'value': {1: 248, 2: 180, 3: 57}}
00039 [L808] TSETS    A=9 B=8 C=17 D=2065 'color'
00040 [L809] MULNV    A=9 B=3 C=0 D=768 
00041 [L809] SUBNV    A=9 B=9 C=1 D=2305 
00042 [L809] TSETS    A=9 B=8 C=18 D=2066 'x'
00043 [L809] MULNV    A=9 B=4 C=2 D=1026 
00044 [L809] ADDNV    A=9 B=9 C=1 D=2305 
00045 [L809] TSETS    A=9 B=8 C=19 D=2067 'y'
00046 [L809] TDUP     A=9 B=0 C=20 D=20 {'kind': 'table', 'value': {1: 0, 2: 0}}
00047 [L809] TSETS    A=9 B=8 C=21 D=2069 'anchor'
00048 [L808] CALL     A=7 B=0 C=2 D=2 
00049 [L808] CALLM    A=5 B=1 C=1 D=257 
00050 [L810] MOV      A=6 B=0 C=1 D=1 
00051 [L810] TGETS    A=5 B=1 C=8 D=264 'addChild'
00052 [L810] GGET     A=7 B=0 C=0 D=0 'd_ms'
00053 [L810] TGETS    A=7 B=7 C=5 D=1797 'd_u'
00054 [L810] TGETS    A=7 B=7 C=10 D=1802 'createByStyle'
00055 [L810] TDUP     A=8 B=0 C=22 D=22 {'kind': 'table', 'value': {'fontsize': 26, 'font': 'arial', 'x': 0.5, 'type': 'label'}}
00056 [L810] GGET     A=9 B=0 C=0 D=0 'd_ms'
00057 [L810] TGETS    A=9 B=9 C=12 D=2316 'd_hz'
00058 [L810] TGETS    A=9 B=9 C=13 D=2317 'gethz'
00059 [L810] KSTR     A=10 B=0 C=23 D=23 'springCardTip7'
00060 [L810] CALL     A=9 B=2 C=2 D=514 
00061 [L810] TSETS    A=9 B=8 C=15 D=2063 'string'
00062 [L810] TDUP     A=9 B=0 C=24 D=24 {'kind': 'table', 'value': {1: 200, 2: 160, 3: 100}}
00063 [L810] TSETS    A=9 B=8 C=17 D=2065 'color'
00064 [L811] MULNV    A=9 B=4 C=3 D=1027 
00065 [L811] SUBNV    A=9 B=9 C=1 D=2305 
00066 [L811] TSETS    A=9 B=8 C=19 D=2067 'y'
00067 [L810] CALL     A=7 B=0 C=2 D=2 
00068 [L810] CALLM    A=5 B=1 C=1 D=257 
00069 [L812] LEN      A=5 B=0 C=0 D=0 
00070 [L813] MULNV    A=6 B=4 C=4 D=1028 
00071 [L813] SUBVN    A=7 B=5 C=5 D=1285 
00072 [L813] DIVVV    A=6 B=6 C=7 D=1543 
00073 [L814] KSHORT   A=7 B=0 C=1 D=1 1
00074 [L814] MOV      A=8 B=0 C=5 D=5 
00075 [L814] KSHORT   A=9 B=0 C=1 D=1 1
00076 [L814] FORI     A=7 B=128 C=24 D=32792 target=101
00077 [L815] MOV      A=12 B=0 C=1 D=1 
00078 [L815] TGETS    A=11 B=1 C=8 D=264 'addChild'
00079 [L815] GGET     A=13 B=0 C=0 D=0 'd_ms'
00080 [L815] TGETS    A=13 B=13 C=5 D=3333 'd_u'
00081 [L815] TGETS    A=13 B=13 C=10 D=3338 'createByStyle'
00082 [L815] TDUP     A=14 B=0 C=25 D=25 {'kind': 'table', 'value': {'fontsize': 26, 'font': 'arial', 'type': 'label'}}
00083 [L815] TGETV    A=15 B=0 C=10 D=10 
00084 [L815] TSETS    A=15 B=14 C=15 D=3599 'string'
00085 [L815] TDUP     A=15 B=0 C=26 D=26 {'kind': 'table', 'value': {1: 242, 2: 209, 3: 155}}
00086 [L815] TSETS    A=15 B=14 C=17 D=3601 'color'
00087 [L816] MULNV    A=15 B=3 C=3 D=771 
00088 [L816] SUBNV    A=15 B=15 C=1 D=3841 
00089 [L816] TSETS    A=15 B=14 C=18 D=3602 'x'
00090 [L816] ADDVN    A=15 B=5 C=5 D=1285 
00091 [L816] MULNV    A=15 B=15 C=1 D=3841 
00092 [L816] SUBVV    A=15 B=15 C=10 D=3850 
00093 [L816] MULVV    A=15 B=6 C=15 D=1551 
00094 [L816] ADDNV    A=15 B=15 C=1 D=3841 
00095 [L816] TSETS    A=15 B=14 C=19 D=3603 'y'
00096 [L816] TDUP     A=15 B=0 C=27 D=27 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00097 [L816] TSETS    A=15 B=14 C=21 D=3605 'anchor'
00098 [L815] CALL     A=13 B=0 C=2 D=2 
00099 [L815] CALLM    A=11 B=1 C=1 D=257 
00100 [L814] FORL     A=7 B=127 C=232 D=32744 target=77
00101 [L822] FNEW     A=7 B=0 C=28 D=28 {'kind': 'proto', 'id': 0}
00102 [L824] TNEW     A=8 B=0 C=0 D=0 
00103 [L825] KSHORT   A=9 B=0 C=100 D=100 100
00104 [L825] TSETS    A=9 B=8 C=29 D=2077 'z'
00105 [L827] TSETS    A=7 B=8 C=30 D=2078 'outFunc'
00106 [L828] GGET     A=9 B=0 C=0 D=0 'd_ms'
00107 [L828] TGETS    A=9 B=9 C=5 D=2309 'd_u'
00108 [L828] TGETS    A=9 B=9 C=32 D=2336 'getRealRect'
00109 [L828] MOV      A=10 B=0 C=2 D=2 
00110 [L828] CALL     A=9 B=2 C=2 D=514 
00111 [L828] TSETS    A=9 B=8 C=31 D=2079 'rect'
00112 [L829] GGET     A=9 B=0 C=0 D=0 'd_ms'
00113 [L829] TGETS    A=9 B=9 C=5 D=2309 'd_u'
00114 [L829] TGETS    A=9 B=9 C=33 D=2337 'createSwallowTouchLayerFunc'
00115 [L829] MOV      A=10 B=0 C=1 D=1 
00116 [L829] MOV      A=11 B=0 C=8 D=8 
00117 [L829] CALL     A=9 B=1 C=3 D=259 
00118 [L831] GGET     A=9 B=0 C=34 D=34 'g_cardUI'
00119 [L831] TGETS    A=9 B=9 C=35 D=2339 'main_layer'
00120 [L831] MOV      A=10 B=0 C=9 D=9 
00121 [L831] TGETS    A=9 B=9 C=8 D=2312 'addChild'
00122 [L831] MOV      A=11 B=0 C=1 D=1 
00123 [L831] KSHORT   A=12 B=0 C=12 D=12 12
00124 [L831] CALL     A=9 B=1 C=4 D=260 
00125 [L832] UCLO     A=0 B=128 C=0 D=32768 target=126
00126 [L832] RET0     A=0 B=0 C=1 D=1 
