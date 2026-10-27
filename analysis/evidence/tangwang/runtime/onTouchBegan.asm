LuaJIT dump version=1; source='@D:\\mg_update_\\lua_cache\\lua1\\0aaf9138ef79f4065afb567aa3dec130.data'; root=proto1

FUNCTION proto0 offset=0x4b source_lines=326-345 params=0
UPVALUES ['waitForIndex', 'index', 'point1']
00001 [L328] GGET     A=0 B=0 C=0 D=0 'isNotMove'
00002 [L328] CALL     A=0 B=2 C=1 D=513 
00003 [L328] ISF      A=0 B=0 C=0 D=0 
00004 [L328] JMP      A=1 B=128 C=43 D=32811 target=48
00005 [L328] UGET     A=0 B=0 C=0 D=0 waitForIndex
00006 [L328] GGET     A=1 B=0 C=1 D=1 'g_cardUI'
00007 [L328] TGETS    A=1 B=1 C=2 D=258 'TouchCount'
00008 [L328] ISNEV    A=0 B=0 C=1 D=1 
00009 [L328] JMP      A=0 B=128 C=38 D=32806 target=48
00010 [L331] GGET     A=0 B=0 C=3 D=3 'getCardSprite'
00011 [L331] GGET     A=1 B=0 C=1 D=1 'g_cardUI'
00012 [L331] TGETS    A=1 B=1 C=4 D=260 'UnusedCards'
00013 [L331] UGET     A=2 B=0 C=1 D=1 index
00014 [L331] TGETV    A=1 B=1 C=2 D=258 
00015 [L331] TGETS    A=1 B=1 C=5 D=261 'level'
00016 [L331] CALL     A=0 B=2 C=2 D=514 
00017 [L332] GGET     A=1 B=0 C=6 D=6 'ChangeScaleH'
00018 [L332] MOV      A=2 B=0 C=0 D=0 
00019 [L332] KNUM     A=3 B=0 C=0 D=0 0.26
00020 [L332] TDUP     A=4 B=0 C=7 D=7 {'kind': 'table', 'value': {1: 0.7, 2: 0.3}}
00021 [L332] CALL     A=1 B=1 C=4 D=260 
00022 [L334] MOV      A=2 B=0 C=0 D=0 
00023 [L334] TGETS    A=1 B=0 C=8 D=8 'setPosition'
00024 [L334] UGET     A=3 B=0 C=2 D=2 point1
00025 [L334] CALL     A=1 B=1 C=3 D=259 
00026 [L335] GGET     A=1 B=0 C=1 D=1 'g_cardUI'
00027 [L335] TGETS    A=1 B=1 C=9 D=265 'main_layer'
00028 [L335] MOV      A=2 B=0 C=1 D=1 
00029 [L335] TGETS    A=1 B=1 C=10 D=266 'addChild'
00030 [L335] MOV      A=3 B=0 C=0 D=0 
00031 [L335] KSHORT   A=4 B=0 C=11 D=11 11
00032 [L335] CALL     A=1 B=1 C=4 D=260 
00033 [L337] GGET     A=1 B=0 C=1 D=1 'g_cardUI'
00034 [L337] TDUP     A=2 B=0 C=12 D=12 {'kind': 'table', 'value': {'position': -1, 'isMoved': False}}
00035 [L337] GGET     A=3 B=0 C=1 D=1 'g_cardUI'
00036 [L337] TGETS    A=3 B=3 C=4 D=772 'UnusedCards'
00037 [L337] UGET     A=4 B=0 C=1 D=1 index
00038 [L337] TGETV    A=3 B=3 C=4 D=772 
00039 [L337] TGETS    A=3 B=3 C=5 D=773 'level'
00040 [L337] TSETS    A=3 B=2 C=5 D=517 'level'
00041 [L338] TSETS    A=0 B=2 C=13 D=525 'sprite'
00042 [L341] UGET     A=3 B=0 C=2 D=2 point1
00043 [L341] TSETS    A=3 B=2 C=14 D=526 'startPoint'
00044 [L341] TSETS    A=2 B=1 C=11 D=267 'Chosen'
00045 [L343] GGET     A=1 B=0 C=15 D=15 'takeout'
00046 [L343] UGET     A=2 B=0 C=1 D=1 index
00047 [L343] CALL     A=1 B=1 C=2 D=258 
00048 [L345] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto1 offset=0x241 source_lines=287-354 params=2
UPVALUES ['CCPointMake', 'pairs', 'CCDirector', 'math']
00001 [L289] GGET     A=2 B=0 C=0 D=0 'g_self'
00002 [L289] TGETS    A=2 B=2 C=1 D=513 'touch'
00003 [L289] ISF      A=0 B=0 C=2 D=2 
00004 [L289] JMP      A=3 B=128 C=2 D=32770 target=7
00005 [L290] KPRI     A=2 B=0 C=1 D=1 
00006 [L290] UCLO     A=0 B=128 C=151 D=32919 target=158
00007 [L292] GGET     A=2 B=0 C=2 D=2 'g_cardUI'
00008 [L292] TGETS    A=2 B=2 C=3 D=515 'main_layer'
00009 [L292] IST      A=0 B=0 C=2 D=2 
00010 [L292] JMP      A=2 B=128 C=2 D=32770 target=13
00011 [L293] KPRI     A=2 B=0 C=1 D=1 
00012 [L293] UCLO     A=0 B=128 C=146 D=32914 target=159
00013 [L295] GGET     A=2 B=0 C=2 D=2 'g_cardUI'
00014 [L295] KPRI     A=3 B=0 C=0 D=0 
00015 [L295] TSETS    A=3 B=2 C=4 D=516 'Chosen'
00016 [L296] GGET     A=2 B=0 C=2 D=2 'g_cardUI'
00017 [L296] TGETS    A=2 B=2 C=3 D=515 'main_layer'
00018 [L296] MOV      A=3 B=0 C=2 D=2 
00019 [L296] TGETS    A=2 B=2 C=5 D=517 'convertToNodeSpace'
00020 [L296] UGET     A=4 B=0 C=0 D=0 CCPointMake
00021 [L296] MOV      A=5 B=0 C=0 D=0 
00022 [L296] MOV      A=6 B=0 C=1 D=1 
00023 [L296] CALL     A=4 B=0 C=3 D=3 
00024 [L296] CALLM    A=2 B=2 C=1 D=513 
00025 [L298] GGET     A=3 B=0 C=2 D=2 'g_cardUI'
00026 [L298] TSETS    A=2 B=3 C=6 D=774 'begin_pos'
00027 [L300] UGET     A=3 B=0 C=1 D=1 pairs
00028 [L300] GGET     A=4 B=0 C=0 D=0 'g_self'
00029 [L300] TGETS    A=4 B=4 C=7 D=1031 'touchRect'
00030 [L300] CALL     A=3 B=4 C=2 D=1026 
00031 [L300] ISNEXT   A=6 B=128 C=121 D=32889 target=153
00032 [L301] MOV      A=9 B=0 C=7 D=7 
00033 [L301] TGETS    A=8 B=7 C=8 D=1800 'containsPoint'
00034 [L301] MOV      A=10 B=0 C=2 D=2 
00035 [L301] CALL     A=8 B=2 C=3 D=515 
00036 [L301] ISF      A=0 B=0 C=8 D=8 
00037 [L301] JMP      A=9 B=128 C=115 D=32883 target=153
00038 [L302] GGET     A=8 B=0 C=0 D=0 'g_self'
00039 [L302] TGETS    A=8 B=8 C=9 D=2057 'LetterCount'
00040 [L302] ISGT     A=6 B=0 C=8 D=8 
00041 [L302] JMP      A=8 B=128 C=56 D=32824 target=98
00042 [L303] GGET     A=8 B=0 C=2 D=2 'g_cardUI'
00043 [L303] TGETS    A=8 B=8 C=10 D=2058 'UsedCards'
00044 [L303] TGETV    A=8 B=8 C=6 D=2054 
00045 [L303] ISF      A=0 B=0 C=8 D=8 
00046 [L303] JMP      A=9 B=128 C=106 D=32874 target=153
00047 [L304] GGET     A=8 B=0 C=2 D=2 'g_cardUI'
00048 [L304] TDUP     A=9 B=0 C=12 D=12 {'kind': 'table', 'value': {'isMoved': False}}
00049 [L304] GGET     A=10 B=0 C=2 D=2 'g_cardUI'
00050 [L304] TGETS    A=10 B=10 C=10 D=2570 'UsedCards'
00051 [L304] TGETV    A=10 B=10 C=6 D=2566 
00052 [L304] TGETS    A=10 B=10 C=11 D=2571 'level'
00053 [L304] TSETS    A=10 B=9 C=11 D=2315 'level'
00054 [L305] GGET     A=10 B=0 C=2 D=2 'g_cardUI'
00055 [L305] TGETS    A=10 B=10 C=10 D=2570 'UsedCards'
00056 [L305] TGETV    A=10 B=10 C=6 D=2566 
00057 [L305] TGETS    A=10 B=10 C=13 D=2573 'sprite'
00058 [L305] TSETS    A=10 B=9 C=13 D=2317 'sprite'
00059 [L306] TSETS    A=6 B=9 C=14 D=2318 'position'
00060 [L308] TSETS    A=2 B=9 C=15 D=2319 'startPoint'
00061 [L308] TSETS    A=9 B=8 C=4 D=2052 'Chosen'
00062 [L310] GGET     A=8 B=0 C=2 D=2 'g_cardUI'
00063 [L310] TGETS    A=8 B=8 C=4 D=2052 'Chosen'
00064 [L310] TGETS    A=8 B=8 C=13 D=2061 'sprite'
00065 [L310] MOV      A=9 B=0 C=8 D=8 
00066 [L310] TGETS    A=8 B=8 C=16 D=2064 'setPosition'
00067 [L310] MOV      A=10 B=0 C=2 D=2 
00068 [L310] CALL     A=8 B=1 C=3 D=259 
00069 [L311] GGET     A=8 B=0 C=17 D=17 'ChangeScaleH'
00070 [L311] GGET     A=9 B=0 C=2 D=2 'g_cardUI'
00071 [L311] TGETS    A=9 B=9 C=4 D=2308 'Chosen'
00072 [L311] TGETS    A=9 B=9 C=13 D=2317 'sprite'
00073 [L311] KNUM     A=10 B=0 C=0 D=0 0.26
00074 [L311] TDUP     A=11 B=0 C=18 D=18 {'kind': 'table', 'value': {1: 0.7, 2: 0.3}}
00075 [L311] CALL     A=8 B=1 C=4 D=260 
00076 [L312] GGET     A=8 B=0 C=2 D=2 'g_cardUI'
00077 [L312] TGETS    A=8 B=8 C=3 D=2051 'main_layer'
00078 [L312] MOV      A=9 B=0 C=8 D=8 
00079 [L312] TGETS    A=8 B=8 C=19 D=2067 'reorderChild'
00080 [L312] GGET     A=10 B=0 C=2 D=2 'g_cardUI'
00081 [L312] TGETS    A=10 B=10 C=4 D=2564 'Chosen'
00082 [L312] TGETS    A=10 B=10 C=13 D=2573 'sprite'
00083 [L312] KSHORT   A=11 B=0 C=11 D=11 11
00084 [L312] CALL     A=8 B=1 C=4 D=260 
00085 [L313] GGET     A=8 B=0 C=2 D=2 'g_cardUI'
00086 [L313] TGETS    A=8 B=8 C=10 D=2058 'UsedCards'
00087 [L313] KPRI     A=9 B=0 C=0 D=0 
00088 [L313] TSETV    A=9 B=8 C=6 D=2054 
00089 [L314] GGET     A=8 B=0 C=2 D=2 'g_cardUI'
00090 [L314] TGETS    A=8 B=8 C=20 D=2068 'tipLabel'
00091 [L314] MOV      A=9 B=0 C=8 D=8 
00092 [L314] TGETS    A=8 B=8 C=21 D=2069 'setVisible'
00093 [L314] KPRI     A=10 B=0 C=1 D=1 
00094 [L314] CALL     A=8 B=1 C=3 D=259 
00095 [L315] KPRI     A=8 B=0 C=2 D=2 
00096 [L315] UCLO     A=0 B=128 C=63 D=32831 target=160
00097 [L316] JMP      A=8 B=128 C=55 D=32823 target=153
00098 [L317] GGET     A=8 B=0 C=0 D=0 'g_self'
00099 [L317] TGETS    A=8 B=8 C=9 D=2057 'LetterCount'
00100 [L317] ADDVN    A=8 B=8 C=1 D=2049 
00101 [L317] ISNEV    A=6 B=0 C=8 D=8 
00102 [L317] JMP      A=8 B=128 C=50 D=32818 target=153
00103 [L318] GGET     A=8 B=0 C=2 D=2 'g_cardUI'
00104 [L318] TGETS    A=8 B=8 C=22 D=2070 'cardsContainer'
00105 [L318] IST      A=0 B=0 C=8 D=8 
00106 [L318] JMP      A=8 B=128 C=2 D=32770 target=109
00107 [L319] KPRI     A=8 B=0 C=1 D=1 
00108 [L319] UCLO     A=0 B=128 C=52 D=32820 target=161
00109 [L321] UGET     A=8 B=0 C=2 D=2 CCDirector
00110 [L321] MOV      A=9 B=0 C=8 D=8 
00111 [L321] TGETS    A=8 B=8 C=23 D=2071 'sharedDirector'
00112 [L321] CALL     A=8 B=2 C=2 D=514 
00113 [L321] MOV      A=9 B=0 C=8 D=8 
00114 [L321] TGETS    A=8 B=8 C=24 D=2072 'getVisibleSize'
00115 [L321] CALL     A=8 B=2 C=2 D=514 
00116 [L322] TGETS    A=9 B=8 C=25 D=2073 'height'
00117 [L322] MULNV    A=9 B=9 C=2 D=2306 
00118 [L323] GGET     A=10 B=0 C=2 D=2 'g_cardUI'
00119 [L323] TGETS    A=10 B=10 C=22 D=2582 'cardsContainer'
00120 [L323] MOV      A=11 B=0 C=10 D=10 
00121 [L323] TGETS    A=10 B=10 C=5 D=2565 'convertToNodeSpace'
00122 [L323] UGET     A=12 B=0 C=0 D=0 CCPointMake
00123 [L323] MOV      A=13 B=0 C=0 D=0 
00124 [L323] MOV      A=14 B=0 C=1 D=1 
00125 [L323] CALL     A=12 B=0 C=3 D=3 
00126 [L323] CALLM    A=10 B=2 C=1 D=513 
00127 [L324] UGET     A=11 B=0 C=3 D=3 math
00128 [L324] TGETS    A=11 B=11 C=26 D=2842 'ceil'
00129 [L324] TGETS    A=12 B=10 C=27 D=2587 'x'
00130 [L324] DIVVV    A=12 B=12 C=9 D=3081 
00131 [L324] CALL     A=11 B=2 C=2 D=514 
00132 [L325] GGET     A=12 B=0 C=2 D=2 'g_cardUI'
00133 [L325] TGETS    A=12 B=12 C=28 D=3100 'TouchCount'
00134 [L325] ADDVN    A=12 B=12 C=1 D=3073 
00135 [L345] FNEW     A=13 B=0 C=29 D=29 {'kind': 'proto', 'id': 0}
00136 [L346] GGET     A=14 B=0 C=2 D=2 'g_cardUI'
00137 [L346] TGETS    A=14 B=14 C=30 D=3614 'UnusedCards'
00138 [L346] TGETV    A=14 B=14 C=11 D=3595 
00139 [L346] ISF      A=0 B=0 C=14 D=14 
00140 [L346] JMP      A=15 B=128 C=11 D=32779 target=152
00141 [L347] GGET     A=14 B=0 C=31 D=31 'd_ms'
00142 [L347] TGETS    A=14 B=14 C=32 D=3616 'd_u'
00143 [L347] TGETS    A=14 B=14 C=33 D=3617 'delay'
00144 [L347] GGET     A=15 B=0 C=2 D=2 'g_cardUI'
00145 [L347] TGETS    A=15 B=15 C=3 D=3843 'main_layer'
00146 [L347] KNUM     A=16 B=0 C=3 D=3 0.2
00147 [L347] MOV      A=17 B=0 C=13 D=13 
00148 [L347] CALL     A=14 B=1 C=4 D=260 
00149 [L348] KPRI     A=14 B=0 C=2 D=2 
00150 [L348] UCLO     A=0 B=128 C=0 D=32768 target=151
00151 [L348] RET1     A=14 B=0 C=2 D=2 
00152 [L349] UCLO     A=8 B=128 C=0 D=32768 target=153
00153 [L300] ITERN    A=6 B=3 C=3 D=771 
00154 [L300] ITERL    A=6 B=127 C=133 D=32645 target=32
00155 [L353] KPRI     A=3 B=0 C=1 D=1 
00156 [L353] UCLO     A=0 B=128 C=0 D=32768 target=157
00157 [L353] RET1     A=3 B=0 C=2 D=2 
00158 [L354] RET1     A=2 B=0 C=2 D=2 
00159 [L354] RET1     A=2 B=0 C=2 D=2 
00160 [L354] RET1     A=8 B=0 C=2 D=2 
00161 [L354] RET1     A=8 B=0 C=2 D=2 
