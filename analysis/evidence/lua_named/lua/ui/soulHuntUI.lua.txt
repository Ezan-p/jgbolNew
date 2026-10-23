LuaJIT dump version=1; source='@D:\\mg_update_\\lua_cache\\lua1\\5fe75526ab1e9de76fe8eeb42c476482.data'; root=proto79

FUNCTION proto0 offset=0x4a source_lines=58-60 params=0
UPVALUES ['CCLuaLog', 'string']
00001 [L59] UGET     A=0 B=0 C=0 D=0 CCLuaLog
00002 [L59] UGET     A=1 B=0 C=1 D=1 string
00003 [L59] TGETS    A=1 B=1 C=0 D=256 'format'
00004 [L59] KSTR     A=2 B=0 C=1 D=1 'Lua : soulHuntUI >>%s'
00005 [L59] UGET     A=3 B=0 C=1 D=1 string
00006 [L59] TGETS    A=3 B=3 C=0 D=768 'format'
00007 [L59] VARG     A=4 B=0 C=0 D=0 
00008 [L59] CALLM    A=3 B=0 C=0 D=0 
00009 [L59] CALLM    A=1 B=0 C=1 D=1 
00010 [L59] CALLM    A=0 B=1 C=0 D=256 
00011 [L60] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto1 offset=0xbe source_lines=85-87 params=1
UPVALUES []
00001 [L86] GGET     A=1 B=0 C=0 D=0 'd_ms'
00002 [L86] TGETS    A=1 B=1 C=1 D=257 'd_hz'
00003 [L86] TGETS    A=1 B=1 C=2 D=258 'gethz'
00004 [L86] MOV      A=2 B=0 C=0 D=0 
00005 [L86] CALLT    A=1 B=0 C=2 D=2 

FUNCTION proto2 offset=0xfa source_lines=89-96 params=1
UPVALUES ['g_self', 'pairs']
00001 [L90] UGET     A=1 B=0 C=0 D=0 g_self
00002 [L90] TGETS    A=1 B=1 C=0 D=256 'role_hunt_data'
00003 [L90] ISF      A=0 B=0 C=1 D=1 
00004 [L90] JMP      A=1 B=128 C=5 D=32773 target=10
00005 [L90] ISF      A=0 B=0 C=0 D=0 
00006 [L90] JMP      A=1 B=128 C=3 D=32771 target=10
00007 [L90] TGETS    A=1 B=0 C=0 D=0 'role_hunt_data'
00008 [L90] IST      A=0 B=0 C=1 D=1 
00009 [L90] JMP      A=1 B=128 C=1 D=32769 target=11
00010 [L91] RET0     A=0 B=0 C=1 D=1 
00011 [L93] UGET     A=1 B=0 C=1 D=1 pairs
00012 [L93] TGETS    A=2 B=0 C=0 D=0 'role_hunt_data'
00013 [L93] CALL     A=1 B=4 C=2 D=1026 
00014 [L93] ISNEXT   A=4 B=128 C=3 D=32771 target=18
00015 [L94] UGET     A=6 B=0 C=0 D=0 g_self
00016 [L94] TGETS    A=6 B=6 C=0 D=1536 'role_hunt_data'
00017 [L94] TSETV    A=5 B=6 C=4 D=1540 
00018 [L93] ITERN    A=4 B=3 C=3 D=771 
00019 [L93] ITERL    A=4 B=127 C=251 D=32763 target=15
00020 [L96] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto3 offset=0x1a9 source_lines=98-168 params=1
UPVALUES ['h_o_t', 'g_self', 'modify', 'g_soulHuntUI']
00001 [L99] TGETS    A=1 B=0 C=0 D=0 'flag'
00002 [L99] UGET     A=2 B=0 C=0 D=0 h_o_t
00003 [L99] TGETS    A=2 B=2 C=1 D=513 'hit_ball'
00004 [L99] ISNEV    A=1 B=0 C=2 D=2 
00005 [L99] JMP      A=1 B=128 C=31 D=32799 target=37
00006 [L100] UGET     A=1 B=0 C=1 D=1 g_self
00007 [L100] UGET     A=2 B=0 C=1 D=1 g_self
00008 [L100] TGETS    A=2 B=2 C=3 D=515 'role_hunt_data'
00009 [L100] TGETS    A=2 B=2 C=4 D=516 'left_soul_count'
00010 [L100] TSETS    A=2 B=1 C=2 D=258 'last_soul_count'
00011 [L101] TGETS    A=1 B=0 C=3 D=3 'role_hunt_data'
00012 [L101] TGETS    A=1 B=1 C=5 D=261 'point_list'
00013 [L101] ISF      A=0 B=0 C=1 D=1 
00014 [L101] JMP      A=2 B=128 C=8 D=32776 target=23
00015 [L102] UGET     A=1 B=0 C=1 D=1 g_self
00016 [L102] TGETS    A=2 B=0 C=3 D=3 'role_hunt_data'
00017 [L102] TGETS    A=2 B=2 C=5 D=517 'point_list'
00018 [L102] TSETS    A=2 B=1 C=6 D=262 'new_point_list'
00019 [L103] TGETS    A=1 B=0 C=3 D=3 'role_hunt_data'
00020 [L103] KPRI     A=2 B=0 C=0 D=0 
00021 [L103] TSETS    A=2 B=1 C=5 D=261 'point_list'
00022 [L103] JMP      A=1 B=128 C=3 D=32771 target=26
00023 [L105] UGET     A=1 B=0 C=1 D=1 g_self
00024 [L105] KPRI     A=2 B=0 C=0 D=0 
00025 [L105] TSETS    A=2 B=1 C=6 D=262 'new_point_list'
00026 [L107] UGET     A=1 B=0 C=2 D=2 modify
00027 [L107] MOV      A=2 B=0 C=0 D=0 
00028 [L107] CALL     A=1 B=1 C=2 D=258 
00029 [L108] GGET     A=1 B=0 C=7 D=7 'showEnergy'
00030 [L108] CALL     A=1 B=1 C=1 D=257 
00031 [L109] GGET     A=1 B=0 C=8 D=8 'showShootTimes'
00032 [L109] CALL     A=1 B=1 C=1 D=257 
00033 [L111] GGET     A=1 B=0 C=9 D=9 'showBallTrack'
00034 [L111] TGETS    A=2 B=0 C=10 D=10 'move_result'
00035 [L111] CALL     A=1 B=1 C=2 D=258 
00036 [L111] JMP      A=1 B=128 C=209 D=32977 target=246
00037 [L112] TGETS    A=1 B=0 C=0 D=0 'flag'
00038 [L112] UGET     A=2 B=0 C=0 D=0 h_o_t
00039 [L112] TGETS    A=2 B=2 C=11 D=523 'enter_map'
00040 [L112] ISNEV    A=1 B=0 C=2 D=2 
00041 [L112] JMP      A=1 B=128 C=17 D=32785 target=59
00042 [L113] UGET     A=1 B=0 C=1 D=1 g_self
00043 [L113] TGETS    A=2 B=0 C=3 D=3 'role_hunt_data'
00044 [L113] TSETS    A=2 B=1 C=3 D=259 'role_hunt_data'
00045 [L114] UGET     A=1 B=0 C=1 D=1 g_self
00046 [L114] TGETS    A=2 B=0 C=12 D=12 'hunt_const_config'
00047 [L114] TSETS    A=2 B=1 C=12 D=268 'hunt_const_config'
00048 [L115] GGET     A=1 B=0 C=13 D=13 'd_ms'
00049 [L115] TGETS    A=1 B=1 C=14 D=270 'd_activityUI'
00050 [L115] TGETS    A=1 B=1 C=15 D=271 'show'
00051 [L115] CALL     A=1 B=1 C=1 D=257 
00052 [L116] GGET     A=1 B=0 C=15 D=15 'show'
00053 [L116] GGET     A=2 B=0 C=13 D=13 'd_ms'
00054 [L116] TGETS    A=2 B=2 C=14 D=526 'd_activityUI'
00055 [L116] TGETS    A=2 B=2 C=16 D=528 'g_self'
00056 [L116] TGETS    A=2 B=2 C=17 D=529 'main_layer'
00057 [L116] CALL     A=1 B=1 C=2 D=258 
00058 [L116] JMP      A=1 B=128 C=187 D=32955 target=246
00059 [L117] TGETS    A=1 B=0 C=0 D=0 'flag'
00060 [L117] UGET     A=2 B=0 C=0 D=0 h_o_t
00061 [L117] TGETS    A=2 B=2 C=18 D=530 'enter_store'
00062 [L117] ISNEV    A=1 B=0 C=2 D=2 
00063 [L117] JMP      A=1 B=128 C=6 D=32774 target=70
00064 [L118] UGET     A=1 B=0 C=1 D=1 g_self
00065 [L118] TGETS    A=2 B=0 C=19 D=19 'store_data'
00066 [L118] TSETS    A=2 B=1 C=19 D=275 'store_data'
00067 [L119] GGET     A=1 B=0 C=20 D=20 'showShop'
00068 [L119] CALL     A=1 B=1 C=1 D=257 
00069 [L119] JMP      A=1 B=128 C=176 D=32944 target=246
00070 [L120] TGETS    A=1 B=0 C=0 D=0 'flag'
00071 [L120] UGET     A=2 B=0 C=0 D=0 h_o_t
00072 [L120] TGETS    A=2 B=2 C=21 D=533 'query_day_top'
00073 [L120] ISEQV    A=1 B=0 C=2 D=2 
00074 [L120] JMP      A=1 B=128 C=20 D=32788 target=95
00075 [L121] TGETS    A=1 B=0 C=0 D=0 'flag'
00076 [L121] UGET     A=2 B=0 C=0 D=0 h_o_t
00077 [L121] TGETS    A=2 B=2 C=22 D=534 'query_week_top'
00078 [L121] ISEQV    A=1 B=0 C=2 D=2 
00079 [L121] JMP      A=1 B=128 C=15 D=32783 target=95
00080 [L122] TGETS    A=1 B=0 C=0 D=0 'flag'
00081 [L122] UGET     A=2 B=0 C=0 D=0 h_o_t
00082 [L122] TGETS    A=2 B=2 C=23 D=535 'query_history_day_top'
00083 [L122] ISEQV    A=1 B=0 C=2 D=2 
00084 [L122] JMP      A=1 B=128 C=10 D=32778 target=95
00085 [L123] TGETS    A=1 B=0 C=0 D=0 'flag'
00086 [L123] UGET     A=2 B=0 C=0 D=0 h_o_t
00087 [L123] TGETS    A=2 B=2 C=24 D=536 'query_history_week_top'
00088 [L123] ISEQV    A=1 B=0 C=2 D=2 
00089 [L123] JMP      A=1 B=128 C=5 D=32773 target=95
00090 [L124] TGETS    A=1 B=0 C=0 D=0 'flag'
00091 [L124] UGET     A=2 B=0 C=0 D=0 h_o_t
00092 [L124] TGETS    A=2 B=2 C=25 D=537 'query_last_week_top'
00093 [L124] ISNEV    A=1 B=0 C=2 D=2 
00094 [L124] JMP      A=1 B=128 C=59 D=32827 target=154
00095 [L125] UGET     A=1 B=0 C=1 D=1 g_self
00096 [L125] TDUP     A=2 B=0 C=28 D=28 {'kind': 'table', 'value': {}}
00097 [L127] TGETS    A=3 B=0 C=27 D=27 'my_order'
00098 [L127] TSETS    A=3 B=2 C=29 D=541 'my_data'
00099 [L128] TGETS    A=3 B=0 C=30 D=30 'top_list'
00100 [L128] TSETS    A=3 B=2 C=30 D=542 'top_list'
00101 [L129] TSETS    A=2 B=1 C=26 D=282 'rank_data'
00102 [L130] TGETS    A=1 B=0 C=0 D=0 'flag'
00103 [L130] UGET     A=2 B=0 C=0 D=0 h_o_t
00104 [L130] TGETS    A=2 B=2 C=21 D=533 'query_day_top'
00105 [L130] ISNEV    A=1 B=0 C=2 D=2 
00106 [L130] JMP      A=1 B=128 C=6 D=32774 target=113
00107 [L131] GGET     A=1 B=0 C=31 D=31 'showRank'
00108 [L131] CALL     A=1 B=1 C=1 D=257 
00109 [L132] GGET     A=1 B=0 C=32 D=32 'showRankDetail'
00110 [L132] KSHORT   A=2 B=0 C=1 D=1 1
00111 [L132] CALL     A=1 B=1 C=2 D=258 
00112 [L132] JMP      A=1 B=128 C=133 D=32901 target=246
00113 [L133] TGETS    A=1 B=0 C=0 D=0 'flag'
00114 [L133] UGET     A=2 B=0 C=0 D=0 h_o_t
00115 [L133] TGETS    A=2 B=2 C=22 D=534 'query_week_top'
00116 [L133] ISNEV    A=1 B=0 C=2 D=2 
00117 [L133] JMP      A=1 B=128 C=4 D=32772 target=122
00118 [L134] GGET     A=1 B=0 C=32 D=32 'showRankDetail'
00119 [L134] KSHORT   A=2 B=0 C=2 D=2 2
00120 [L134] CALL     A=1 B=1 C=2 D=258 
00121 [L134] JMP      A=1 B=128 C=124 D=32892 target=246
00122 [L135] TGETS    A=1 B=0 C=0 D=0 'flag'
00123 [L135] UGET     A=2 B=0 C=0 D=0 h_o_t
00124 [L135] TGETS    A=2 B=2 C=23 D=535 'query_history_day_top'
00125 [L135] ISNEV    A=1 B=0 C=2 D=2 
00126 [L135] JMP      A=1 B=128 C=4 D=32772 target=131
00127 [L136] GGET     A=1 B=0 C=32 D=32 'showRankDetail'
00128 [L136] KSHORT   A=2 B=0 C=6 D=6 6
00129 [L136] CALL     A=1 B=1 C=2 D=258 
00130 [L136] JMP      A=1 B=128 C=115 D=32883 target=246
00131 [L137] TGETS    A=1 B=0 C=0 D=0 'flag'
00132 [L137] UGET     A=2 B=0 C=0 D=0 h_o_t
00133 [L137] TGETS    A=2 B=2 C=24 D=536 'query_history_week_top'
00134 [L137] ISNEV    A=1 B=0 C=2 D=2 
00135 [L137] JMP      A=1 B=128 C=4 D=32772 target=140
00136 [L138] GGET     A=1 B=0 C=32 D=32 'showRankDetail'
00137 [L138] KSHORT   A=2 B=0 C=7 D=7 7
00138 [L138] CALL     A=1 B=1 C=2 D=258 
00139 [L138] JMP      A=1 B=128 C=106 D=32874 target=246
00140 [L140] UGET     A=1 B=0 C=1 D=1 g_self
00141 [L140] TGETS    A=1 B=1 C=26 D=282 'rank_data'
00142 [L140] TGETS    A=1 B=1 C=29 D=285 'my_data'
00143 [L140] TGETS    A=2 B=0 C=33 D=33 'had_got_prize'
00144 [L140] TSETS    A=2 B=1 C=33 D=289 'had_got_prize'
00145 [L141] UGET     A=1 B=0 C=1 D=1 g_self
00146 [L141] TGETS    A=1 B=1 C=26 D=282 'rank_data'
00147 [L141] TGETS    A=1 B=1 C=29 D=285 'my_data'
00148 [L141] TGETS    A=2 B=0 C=34 D=34 'had_prize'
00149 [L141] TSETS    A=2 B=1 C=34 D=290 'had_prize'
00150 [L142] GGET     A=1 B=0 C=32 D=32 'showRankDetail'
00151 [L142] KSHORT   A=2 B=0 C=3 D=3 3
00152 [L142] CALL     A=1 B=1 C=2 D=258 
00153 [L143] JMP      A=1 B=128 C=92 D=32860 target=246
00154 [L144] TGETS    A=1 B=0 C=0 D=0 'flag'
00155 [L144] UGET     A=2 B=0 C=0 D=0 h_o_t
00156 [L144] TGETS    A=2 B=2 C=35 D=547 'convert_energy'
00157 [L144] ISNEV    A=1 B=0 C=2 D=2 
00158 [L144] JMP      A=1 B=128 C=8 D=32776 target=167
00159 [L145] UGET     A=1 B=0 C=2 D=2 modify
00160 [L145] MOV      A=2 B=0 C=0 D=0 
00161 [L145] CALL     A=1 B=1 C=2 D=258 
00162 [L146] GGET     A=1 B=0 C=7 D=7 'showEnergy'
00163 [L146] CALL     A=1 B=1 C=1 D=257 
00164 [L147] GGET     A=1 B=0 C=36 D=36 'showSoulCount'
00165 [L147] CALL     A=1 B=1 C=1 D=257 
00166 [L147] JMP      A=1 B=128 C=79 D=32847 target=246
00167 [L148] TGETS    A=1 B=0 C=0 D=0 'flag'
00168 [L148] UGET     A=2 B=0 C=0 D=0 h_o_t
00169 [L148] TGETS    A=2 B=2 C=37 D=549 'flush_soul'
00170 [L148] ISNEV    A=1 B=0 C=2 D=2 
00171 [L148] JMP      A=1 B=128 C=9 D=32777 target=181
00172 [L149] UGET     A=1 B=0 C=2 D=2 modify
00173 [L149] MOV      A=2 B=0 C=0 D=0 
00174 [L149] CALL     A=1 B=1 C=2 D=258 
00175 [L150] GGET     A=1 B=0 C=38 D=38 'showFreshTimes'
00176 [L150] CALL     A=1 B=1 C=1 D=257 
00177 [L151] GGET     A=1 B=0 C=39 D=39 'showSouls'
00178 [L151] KPRI     A=2 B=0 C=2 D=2 
00179 [L151] CALL     A=1 B=1 C=2 D=258 
00180 [L151] JMP      A=1 B=128 C=65 D=32833 target=246
00181 [L152] TGETS    A=1 B=0 C=0 D=0 'flag'
00182 [L152] UGET     A=2 B=0 C=0 D=0 h_o_t
00183 [L152] TGETS    A=2 B=2 C=40 D=552 'buy_store'
00184 [L152] ISNEV    A=1 B=0 C=2 D=2 
00185 [L152] JMP      A=1 B=128 C=21 D=32789 target=207
00186 [L153] UGET     A=1 B=0 C=2 D=2 modify
00187 [L153] MOV      A=2 B=0 C=0 D=0 
00188 [L153] CALL     A=1 B=1 C=2 D=258 
00189 [L154] GGET     A=1 B=0 C=36 D=36 'showSoulCount'
00190 [L154] CALL     A=1 B=1 C=1 D=257 
00191 [L155] UGET     A=1 B=0 C=1 D=1 g_self
00192 [L155] TGETS    A=1 B=1 C=19 D=275 'store_data'
00193 [L155] TGETS    A=1 B=1 C=41 D=297 'item_list'
00194 [L155] TGETS    A=2 B=0 C=42 D=42 'item_index'
00195 [L155] TGETV    A=1 B=1 C=2 D=258 
00196 [L155] TGETS    A=2 B=0 C=43 D=43 'buy_times'
00197 [L155] TSETS    A=2 B=1 C=43 D=299 'buy_times'
00198 [L156] GGET     A=1 B=0 C=13 D=13 'd_ms'
00199 [L156] TGETS    A=1 B=1 C=44 D=300 'd_commonLayerUI'
00200 [L156] TGETS    A=1 B=1 C=45 D=301 'showPrizeResLayer'
00201 [L156] UGET     A=2 B=0 C=3 D=3 g_soulHuntUI
00202 [L156] TGETS    A=2 B=2 C=17 D=529 'main_layer'
00203 [L156] TGETS    A=3 B=0 C=46 D=46 'attach_list'
00204 [L156] GGET     A=4 B=0 C=20 D=20 'showShop'
00205 [L156] CALL     A=1 B=1 C=4 D=260 
00206 [L156] JMP      A=1 B=128 C=39 D=32807 target=246
00207 [L157] TGETS    A=1 B=0 C=0 D=0 'flag'
00208 [L157] UGET     A=2 B=0 C=0 D=0 h_o_t
00209 [L157] TGETS    A=2 B=2 C=47 D=559 'flush_store'
00210 [L157] ISNEV    A=1 B=0 C=2 D=2 
00211 [L157] JMP      A=1 B=128 C=11 D=32779 target=223
00212 [L158] UGET     A=1 B=0 C=2 D=2 modify
00213 [L158] MOV      A=2 B=0 C=0 D=0 
00214 [L158] CALL     A=1 B=1 C=2 D=258 
00215 [L159] UGET     A=1 B=0 C=1 D=1 g_self
00216 [L159] TGETS    A=2 B=0 C=19 D=19 'store_data'
00217 [L159] TSETS    A=2 B=1 C=19 D=275 'store_data'
00218 [L160] GGET     A=1 B=0 C=36 D=36 'showSoulCount'
00219 [L160] CALL     A=1 B=1 C=1 D=257 
00220 [L161] GGET     A=1 B=0 C=20 D=20 'showShop'
00221 [L161] CALL     A=1 B=1 C=1 D=257 
00222 [L161] JMP      A=1 B=128 C=23 D=32791 target=246
00223 [L162] TGETS    A=1 B=0 C=0 D=0 'flag'
00224 [L162] UGET     A=2 B=0 C=0 D=0 h_o_t
00225 [L162] TGETS    A=2 B=2 C=48 D=560 'take_week_prize'
00226 [L162] ISNEV    A=1 B=0 C=2 D=2 
00227 [L162] JMP      A=1 B=128 C=18 D=32786 target=246
00228 [L163] UGET     A=1 B=0 C=1 D=1 g_self
00229 [L163] TGETS    A=1 B=1 C=26 D=282 'rank_data'
00230 [L163] TGETS    A=1 B=1 C=29 D=285 'my_data'
00231 [L163] KPRI     A=2 B=0 C=2 D=2 
00232 [L163] TSETS    A=2 B=1 C=33 D=289 'had_got_prize'
00233 [L164] UGET     A=1 B=0 C=1 D=1 g_self
00234 [L164] KPRI     A=2 B=0 C=1 D=1 
00235 [L164] TSETS    A=2 B=1 C=49 D=305 'has_week_prize'
00236 [L165] GGET     A=1 B=0 C=50 D=50 'showHint'
00237 [L165] CALL     A=1 B=1 C=1 D=257 
00238 [L166] GGET     A=1 B=0 C=13 D=13 'd_ms'
00239 [L166] TGETS    A=1 B=1 C=44 D=300 'd_commonLayerUI'
00240 [L166] TGETS    A=1 B=1 C=45 D=301 'showPrizeResLayer'
00241 [L166] UGET     A=2 B=0 C=3 D=3 g_soulHuntUI
00242 [L166] TGETS    A=2 B=2 C=17 D=529 'main_layer'
00243 [L166] TGETS    A=3 B=0 C=51 D=51 'prize_list'
00244 [L166] GGET     A=4 B=0 C=32 D=32 'showRankDetail'
00245 [L166] CALL     A=1 B=1 C=4 D=260 
00246 [L168] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto4 offset=0x939 source_lines=170-179 params=1
UPVALUES ['cclog', 'g_self']
00001 [L171] UGET     A=1 B=0 C=0 D=0 cclog
00002 [L171] KSTR     A=2 B=0 C=0 D=0 'hehe'
00003 [L171] CALL     A=1 B=1 C=2 D=258 
00004 [L172] IST      A=0 B=0 C=0 D=0 
00005 [L172] JMP      A=1 B=128 C=1 D=32769 target=7
00006 [L173] RET0     A=0 B=0 C=1 D=1 
00007 [L175] UGET     A=1 B=0 C=1 D=1 g_self
00008 [L175] TGETS    A=2 B=0 C=1 D=1 'begin_time'
00009 [L175] TSETS    A=2 B=1 C=1 D=257 'begin_time'
00010 [L176] UGET     A=1 B=0 C=1 D=1 g_self
00011 [L176] TGETS    A=2 B=0 C=2 D=2 'end_time'
00012 [L176] TSETS    A=2 B=1 C=2 D=258 'end_time'
00013 [L177] UGET     A=1 B=0 C=1 D=1 g_self
00014 [L177] TGETS    A=2 B=0 C=3 D=3 'is_open'
00015 [L177] TSETS    A=2 B=1 C=3 D=259 'is_open'
00016 [L178] UGET     A=1 B=0 C=1 D=1 g_self
00017 [L178] TGETS    A=2 B=0 C=4 D=4 'has_week_prize'
00018 [L178] TSETS    A=2 B=1 C=4 D=260 'has_week_prize'
00019 [L179] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto5 offset=0x9f3 source_lines=181-183 params=0
UPVALUES ['g_self']
00001 [L182] UGET     A=0 B=0 C=0 D=0 g_self
00002 [L182] TGETS    A=0 B=0 C=0 D=0 'begin_time'
00003 [L182] ISF      A=0 B=0 C=0 D=0 
00004 [L182] JMP      A=1 B=128 C=6 D=32774 target=11
00005 [L182] UGET     A=0 B=0 C=0 D=0 g_self
00006 [L182] TGETS    A=0 B=0 C=1 D=1 'end_time'
00007 [L182] ISF      A=0 B=0 C=0 D=0 
00008 [L182] JMP      A=1 B=128 C=2 D=32770 target=11
00009 [L182] UGET     A=0 B=0 C=0 D=0 g_self
00010 [L182] TGETS    A=0 B=0 C=2 D=2 'is_open'
00011 [L182] RET1     A=0 B=0 C=2 D=2 

FUNCTION proto6 offset=0xa5d source_lines=185-195 params=0
UPVALUES ['g_self', 'tonumber']
00001 [L186] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L186] TGETS    A=0 B=0 C=1 D=1 'd_activityUI'
00003 [L186] TGETS    A=0 B=0 C=2 D=2 'getRequireLevel'
00004 [L186] GGET     A=1 B=0 C=0 D=0 'd_ms'
00005 [L186] TGETS    A=1 B=1 C=1 D=257 'd_activityUI'
00006 [L186] TGETS    A=1 B=1 C=3 D=259 'activityID'
00007 [L186] TGETS    A=1 B=1 C=4 D=260 'soulHunt'
00008 [L186] CALL     A=0 B=2 C=2 D=514 
00009 [L186] GGET     A=1 B=0 C=0 D=0 'd_ms'
00010 [L186] TGETS    A=1 B=1 C=5 D=261 'd_mainUI'
00011 [L186] TGETS    A=1 B=1 C=6 D=262 'g_playerInfo'
00012 [L186] TGETS    A=1 B=1 C=7 D=263 'level'
00013 [L186] ISLT     A=1 B=0 C=0 D=0 
00014 [L186] JMP      A=0 B=128 C=4 D=32772 target=19
00015 [L187] GGET     A=0 B=0 C=8 D=8 'canEnter'
00016 [L187] CALL     A=0 B=2 C=1 D=513 
00017 [L187] IST      A=0 B=0 C=0 D=0 
00018 [L187] JMP      A=0 B=128 C=3 D=32771 target=22
00019 [L188] KPRI     A=0 B=0 C=1 D=1 
00020 [L188] RET1     A=0 B=0 C=2 D=2 
00021 [L188] JMP      A=0 B=128 C=26 D=32794 target=48
00022 [L189] UGET     A=0 B=0 C=0 D=0 g_self
00023 [L189] TGETS    A=0 B=0 C=9 D=9 'has_week_prize'
00024 [L189] ISF      A=0 B=0 C=0 D=0 
00025 [L189] JMP      A=1 B=128 C=3 D=32771 target=29
00026 [L190] KPRI     A=0 B=0 C=2 D=2 
00027 [L190] RET1     A=0 B=0 C=2 D=2 
00028 [L190] JMP      A=0 B=128 C=19 D=32787 target=48
00029 [L192] UGET     A=0 B=0 C=1 D=1 tonumber
00030 [L192] GGET     A=1 B=0 C=0 D=0 'd_ms'
00031 [L192] TGETS    A=1 B=1 C=10 D=266 'd_file'
00032 [L192] TGETS    A=1 B=1 C=11 D=267 'get'
00033 [L192] KSTR     A=2 B=0 C=12 D=12 'soul_hunt_time'
00034 [L192] GGET     A=3 B=0 C=0 D=0 'd_ms'
00035 [L192] TGETS    A=3 B=3 C=5 D=773 'd_mainUI'
00036 [L192] TGETS    A=3 B=3 C=6 D=774 'g_playerInfo'
00037 [L192] TGETS    A=3 B=3 C=13 D=781 'role_id'
00038 [L192] CALL     A=1 B=0 C=3 D=3 
00039 [L192] CALLM    A=0 B=2 C=0 D=512 
00040 [L192] IST      A=0 B=0 C=0 D=0 
00041 [L192] JMP      A=1 B=128 C=1 D=32769 target=43
00042 [L192] KSHORT   A=0 B=0 C=0 D=0 0
00043 [L193] GGET     A=1 B=0 C=0 D=0 'd_ms'
00044 [L193] TGETS    A=1 B=1 C=14 D=270 'd_time'
00045 [L193] TGETS    A=1 B=1 C=15 D=271 'isCrossDay'
00046 [L193] MOV      A=2 B=0 C=0 D=0 
00047 [L193] CALLT    A=1 B=0 C=2 D=2 
00048 [L195] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto7 offset=0xc1f source_lines=197-212 params=0
UPVALUES ['g_self']
00001 [L198] UGET     A=0 B=0 C=0 D=0 g_self
00002 [L198] TGETS    A=0 B=0 C=0 D=0 'begin_time'
00003 [L198] ISF      A=0 B=0 C=0 D=0 
00004 [L198] JMP      A=0 B=128 C=4 D=32772 target=9
00005 [L198] UGET     A=0 B=0 C=0 D=0 g_self
00006 [L198] TGETS    A=0 B=0 C=1 D=1 'end_time'
00007 [L198] IST      A=0 B=0 C=0 D=0 
00008 [L198] JMP      A=0 B=128 C=2 D=32770 target=11
00009 [L199] KPRI     A=0 B=0 C=1 D=1 
00010 [L199] RET1     A=0 B=0 C=2 D=2 
00011 [L201] GGET     A=0 B=0 C=2 D=2 'd_ms'
00012 [L201] TGETS    A=0 B=0 C=3 D=3 'd_time'
00013 [L201] TGETS    A=0 B=0 C=4 D=4 'getTime'
00014 [L201] CALL     A=0 B=2 C=1 D=513 
00015 [L202] LOOP     A=1 B=128 C=29 D=32797 target=45
00016 [L203] UGET     A=1 B=0 C=0 D=0 g_self
00017 [L203] TGETS    A=1 B=1 C=0 D=256 'begin_time'
00018 [L203] ISGE     A=0 B=0 C=1 D=1 
00019 [L203] JMP      A=1 B=128 C=5 D=32773 target=25
00020 [L204] KPRI     A=1 B=0 C=1 D=1 
00021 [L204] UGET     A=2 B=0 C=0 D=0 g_self
00022 [L204] TGETS    A=2 B=2 C=0 D=512 'begin_time'
00023 [L204] RET      A=1 B=0 C=3 D=3 
00024 [L204] JMP      A=1 B=127 C=246 D=32758 target=15
00025 [L205] UGET     A=1 B=0 C=0 D=0 g_self
00026 [L205] TGETS    A=1 B=1 C=1 D=257 'end_time'
00027 [L205] ISGE     A=0 B=0 C=1 D=1 
00028 [L205] JMP      A=1 B=128 C=5 D=32773 target=34
00029 [L206] KPRI     A=1 B=0 C=2 D=2 
00030 [L206] UGET     A=2 B=0 C=0 D=0 g_self
00031 [L206] TGETS    A=2 B=2 C=1 D=513 'end_time'
00032 [L206] RET      A=1 B=0 C=3 D=3 
00033 [L206] JMP      A=1 B=127 C=237 D=32749 target=15
00034 [L208] UGET     A=1 B=0 C=0 D=0 g_self
00035 [L208] UGET     A=2 B=0 C=0 D=0 g_self
00036 [L208] TGETS    A=2 B=2 C=0 D=512 'begin_time'
00037 [L208] ADDVN    A=2 B=2 C=0 D=512 
00038 [L208] TSETS    A=2 B=1 C=0 D=256 'begin_time'
00039 [L209] UGET     A=1 B=0 C=0 D=0 g_self
00040 [L209] UGET     A=2 B=0 C=0 D=0 g_self
00041 [L209] TGETS    A=2 B=2 C=1 D=513 'end_time'
00042 [L209] ADDVN    A=2 B=2 C=0 D=512 
00043 [L209] TSETS    A=2 B=1 C=1 D=257 'end_time'
00044 [L210] JMP      A=1 B=127 C=226 D=32738 target=15
00045 [L212] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto8 offset=0xd48 source_lines=214-228 params=1
UPVALUES ['g_self', 'g_soulHuntUI']
00001 [L215] IST      A=0 B=0 C=0 D=0 
00002 [L215] JMP      A=1 B=128 C=1 D=32769 target=4
00003 [L216] RET0     A=0 B=0 C=1 D=1 
00004 [L218] UGET     A=1 B=0 C=0 D=0 g_self
00005 [L218] TGETS    A=1 B=1 C=0 D=256 'BallPrice'
00006 [L218] IST      A=0 B=0 C=1 D=1 
00007 [L218] JMP      A=1 B=128 C=24 D=32792 target=32
00008 [L219] GGET     A=1 B=0 C=1 D=1 'd_ms'
00009 [L219] TGETS    A=1 B=1 C=2 D=258 'd_data'
00010 [L219] TGETS    A=1 B=1 C=3 D=259 'getSoulHuntConfig'
00011 [L219] CALL     A=1 B=1 C=1 D=257 
00012 [L220] UGET     A=1 B=0 C=0 D=0 g_self
00013 [L220] GGET     A=2 B=0 C=1 D=1 'd_ms'
00014 [L220] TGETS    A=2 B=2 C=2 D=514 'd_data'
00015 [L220] TGETS    A=2 B=2 C=4 D=516 'g_hunt_price'
00016 [L220] TSETS    A=2 B=1 C=0 D=256 'BallPrice'
00017 [L221] UGET     A=1 B=0 C=0 D=0 g_self
00018 [L221] GGET     A=2 B=0 C=1 D=1 'd_ms'
00019 [L221] TGETS    A=2 B=2 C=2 D=514 'd_data'
00020 [L221] TGETS    A=2 B=2 C=6 D=518 'g_hunt_soul'
00021 [L221] TSETS    A=2 B=1 C=5 D=261 'SoulValue'
00022 [L222] UGET     A=1 B=0 C=0 D=0 g_self
00023 [L222] GGET     A=2 B=0 C=1 D=1 'd_ms'
00024 [L222] TGETS    A=2 B=2 C=2 D=514 'd_data'
00025 [L222] TGETS    A=2 B=2 C=8 D=520 'g_hunt_day_prize'
00026 [L222] TSETS    A=2 B=1 C=7 D=263 'DayPrize'
00027 [L223] UGET     A=1 B=0 C=0 D=0 g_self
00028 [L223] GGET     A=2 B=0 C=1 D=1 'd_ms'
00029 [L223] TGETS    A=2 B=2 C=2 D=514 'd_data'
00030 [L223] TGETS    A=2 B=2 C=10 D=522 'g_hunt_week_prize'
00031 [L223] TSETS    A=2 B=1 C=9 D=265 'WeekPrize'
00032 [L226] GGET     A=1 B=0 C=11 D=11 'create'
00033 [L226] CALL     A=1 B=1 C=1 D=257 
00034 [L227] MOV      A=2 B=0 C=0 D=0 
00035 [L227] TGETS    A=1 B=0 C=12 D=12 'addChild'
00036 [L227] UGET     A=3 B=0 C=1 D=1 g_soulHuntUI
00037 [L227] TGETS    A=3 B=3 C=13 D=781 'main_layer'
00038 [L227] KSHORT   A=4 B=3 C=232 D=1000 1000
00039 [L227] CALL     A=1 B=1 C=4 D=260 
00040 [L228] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto9 offset=0xee1 source_lines=230-301 params=0
UPVALUES ['CCLayer', 'g_soulHuntUI', 'g_self', 'scrSize']
00001 [L231] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L231] TGETS    A=0 B=0 C=1 D=1 'd_file'
00003 [L231] TGETS    A=0 B=0 C=2 D=2 'set'
00004 [L231] KSTR     A=1 B=0 C=3 D=3 'soul_hunt_time'
00005 [L231] GGET     A=2 B=0 C=0 D=0 'd_ms'
00006 [L231] TGETS    A=2 B=2 C=4 D=516 'd_time'
00007 [L231] TGETS    A=2 B=2 C=5 D=517 'getTime'
00008 [L231] CALL     A=2 B=2 C=1 D=513 
00009 [L231] GGET     A=3 B=0 C=0 D=0 'd_ms'
00010 [L231] TGETS    A=3 B=3 C=6 D=774 'd_mainUI'
00011 [L231] TGETS    A=3 B=3 C=7 D=775 'g_playerInfo'
00012 [L231] TGETS    A=3 B=3 C=8 D=776 'role_id'
00013 [L231] CALL     A=0 B=1 C=4 D=260 
00014 [L232] UGET     A=0 B=0 C=0 D=0 CCLayer
00015 [L232] MOV      A=1 B=0 C=0 D=0 
00016 [L232] TGETS    A=0 B=0 C=9 D=9 'create'
00017 [L232] CALL     A=0 B=2 C=2 D=514 
00018 [L233] MOV      A=2 B=0 C=0 D=0 
00019 [L233] TGETS    A=1 B=0 C=10 D=10 'registerScriptTouchHandler'
00020 [L233] GGET     A=3 B=0 C=11 D=11 'onTouch'
00021 [L233] KPRI     A=4 B=0 C=1 D=1 
00022 [L233] KSHORT   A=5 B=255 C=128 D=65408 -128
00023 [L233] KPRI     A=6 B=0 C=2 D=2 
00024 [L233] CALL     A=1 B=1 C=6 D=262 
00025 [L234] MOV      A=2 B=0 C=0 D=0 
00026 [L234] TGETS    A=1 B=0 C=12 D=12 'setTouchEnabled'
00027 [L234] KPRI     A=3 B=0 C=2 D=2 
00028 [L234] CALL     A=1 B=1 C=3 D=259 
00029 [L236] UGET     A=1 B=0 C=1 D=1 g_soulHuntUI
00030 [L236] TSETS    A=0 B=1 C=13 D=269 'main_layer'
00031 [L238] GGET     A=1 B=0 C=0 D=0 'd_ms'
00032 [L238] TGETS    A=1 B=1 C=14 D=270 'd_u'
00033 [L238] TGETS    A=1 B=1 C=15 D=271 'createByStyles'
00034 [L238] TDUP     A=2 B=0 C=16 D=16 {'kind': 'table', 'value': {'pic': 'v2/soulHuntUI/bkg.jpg', 'y': 0.5, 'scaleX': 1, 'x': 0.5, 'scaleY': 1}}
00035 [L238] CALL     A=1 B=2 C=2 D=514 
00036 [L239] MOV      A=3 B=0 C=0 D=0 
00037 [L239] TGETS    A=2 B=0 C=17 D=17 'addChild'
00038 [L239] MOV      A=4 B=0 C=1 D=1 
00039 [L239] KSHORT   A=5 B=255 C=255 D=65535 -1
00040 [L239] CALL     A=2 B=1 C=4 D=260 
00041 [L241] GGET     A=2 B=0 C=0 D=0 'd_ms'
00042 [L241] TGETS    A=2 B=2 C=14 D=526 'd_u'
00043 [L241] TGETS    A=2 B=2 C=15 D=527 'createByStyles'
00044 [L241] TDUP     A=3 B=0 C=18 D=18 {'kind': 'table', 'value': {'pic': 'v2/soulHuntUI/bkg2.png', 'scale': 1, 'y': 0, 'x': 0.5}}
00045 [L241] TDUP     A=4 B=0 C=19 D=19 {'kind': 'table', 'value': {1: 0.5, 2: 0}}
00046 [L241] TSETS    A=4 B=3 C=20 D=788 'anchor'
00047 [L241] CALL     A=2 B=2 C=2 D=514 
00048 [L242] MOV      A=4 B=0 C=0 D=0 
00049 [L242] TGETS    A=3 B=0 C=17 D=17 'addChild'
00050 [L242] MOV      A=5 B=0 C=2 D=2 
00051 [L242] CALL     A=3 B=1 C=3 D=259 
00052 [L243] GGET     A=3 B=0 C=0 D=0 'd_ms'
00053 [L243] TGETS    A=3 B=3 C=14 D=782 'd_u'
00054 [L243] TGETS    A=3 B=3 C=21 D=789 'getRealScale'
00055 [L243] MOV      A=4 B=0 C=2 D=2 
00056 [L243] CALL     A=3 B=3 C=2 D=770 
00057 [L244] MULNV    A=4 B=4 C=0 D=1024 
00058 [L246] GGET     A=5 B=0 C=0 D=0 'd_ms'
00059 [L246] TGETS    A=5 B=5 C=14 D=1294 'd_u'
00060 [L246] TGETS    A=5 B=5 C=15 D=1295 'createByStyles'
00061 [L246] TDUP     A=6 B=0 C=22 D=22 {'kind': 'table', 'value': {'pic': 'v2/soulHuntUI/ground.png', 'scale': 1, 'x': 0.5}}
00062 [L246] TSETS    A=4 B=6 C=23 D=1559 'y'
00063 [L246] TDUP     A=7 B=0 C=24 D=24 {'kind': 'table', 'value': {1: 0.5, 2: 0}}
00064 [L246] TSETS    A=7 B=6 C=20 D=1556 'anchor'
00065 [L246] CALL     A=5 B=2 C=2 D=514 
00066 [L247] MOV      A=7 B=0 C=0 D=0 
00067 [L247] TGETS    A=6 B=0 C=17 D=17 'addChild'
00068 [L247] MOV      A=8 B=0 C=5 D=5 
00069 [L247] CALL     A=6 B=1 C=3 D=259 
00070 [L248] GGET     A=6 B=0 C=0 D=0 'd_ms'
00071 [L248] TGETS    A=6 B=6 C=14 D=1550 'd_u'
00072 [L248] TGETS    A=6 B=6 C=21 D=1557 'getRealScale'
00073 [L248] MOV      A=7 B=0 C=5 D=5 
00074 [L248] CALL     A=6 B=3 C=2 D=770 
00075 [L249] UGET     A=8 B=0 C=1 D=1 g_soulHuntUI
00076 [L249] MOV      A=10 B=0 C=5 D=5 
00077 [L249] TGETS    A=9 B=5 C=26 D=1306 'boundingBox'
00078 [L249] CALL     A=9 B=2 C=2 D=514 
00079 [L249] TSETS    A=9 B=8 C=25 D=2073 'groundBound'
00080 [L251] ADDNV    A=8 B=7 C=1 D=1793 
00081 [L251] ADDVV    A=8 B=8 C=4 D=2052 
00082 [L251] MULNV    A=8 B=8 C=2 D=2050 
00083 [L253] GGET     A=9 B=0 C=0 D=0 'd_ms'
00084 [L253] TGETS    A=9 B=9 C=14 D=2318 'd_u'
00085 [L253] TGETS    A=9 B=9 C=15 D=2319 'createByStyles'
00086 [L253] TDUP     A=10 B=0 C=27 D=27 {'kind': 'table', 'value': {'pic': 'v2/soulHuntUI/title.png', 'x': 0.5}}
00087 [L253] TSETS    A=8 B=10 C=23 D=2583 'y'
00088 [L253] CALL     A=9 B=2 C=2 D=514 
00089 [L254] MOV      A=11 B=0 C=0 D=0 
00090 [L254] TGETS    A=10 B=0 C=17 D=17 'addChild'
00091 [L254] MOV      A=12 B=0 C=9 D=9 
00092 [L254] KSHORT   A=13 B=0 C=1 D=1 1
00093 [L254] CALL     A=10 B=1 C=4 D=260 
00094 [L256] MOV      A=11 B=0 C=0 D=0 
00095 [L256] TGETS    A=10 B=0 C=17 D=17 'addChild'
00096 [L256] GGET     A=12 B=0 C=0 D=0 'd_ms'
00097 [L256] TGETS    A=12 B=12 C=14 D=3086 'd_u'
00098 [L256] TGETS    A=12 B=12 C=15 D=3087 'createByStyles'
00099 [L256] TDUP     A=13 B=0 C=28 D=28 {'kind': 'table', 'value': {'pic': 'v2/soulHuntUI/label1.png', 'x': 0.08}}
00100 [L256] MULNV    A=14 B=4 C=2 D=1026 
00101 [L256] TSETS    A=14 B=13 C=23 D=3351 'y'
00102 [L256] CALL     A=12 B=2 C=2 D=514 
00103 [L256] KSHORT   A=13 B=0 C=1 D=1 1
00104 [L256] CALL     A=10 B=1 C=4 D=260 
00105 [L257] MOV      A=11 B=0 C=0 D=0 
00106 [L257] TGETS    A=10 B=0 C=17 D=17 'addChild'
00107 [L257] GGET     A=12 B=0 C=0 D=0 'd_ms'
00108 [L257] TGETS    A=12 B=12 C=14 D=3086 'd_u'
00109 [L257] TGETS    A=12 B=12 C=15 D=3087 'createByStyles'
00110 [L257] TDUP     A=13 B=0 C=29 D=29 {'kind': 'table', 'value': {'pic': 'v2/soulHuntUI/bkg6.png', 'x': 0.22}}
00111 [L257] MULNV    A=14 B=4 C=2 D=1026 
00112 [L257] TSETS    A=14 B=13 C=23 D=3351 'y'
00113 [L257] CALL     A=12 B=2 C=2 D=514 
00114 [L257] KSHORT   A=13 B=0 C=1 D=1 1
00115 [L257] CALL     A=10 B=1 C=4 D=260 
00116 [L258] MOV      A=11 B=0 C=0 D=0 
00117 [L258] TGETS    A=10 B=0 C=17 D=17 'addChild'
00118 [L258] GGET     A=12 B=0 C=0 D=0 'd_ms'
00119 [L258] TGETS    A=12 B=12 C=14 D=3086 'd_u'
00120 [L258] TGETS    A=12 B=12 C=15 D=3087 'createByStyles'
00121 [L258] TDUP     A=13 B=0 C=30 D=30 {'kind': 'table', 'value': {'pic': 'v2/soulHuntUI/label2.png', 'x': 0.74}}
00122 [L258] MULNV    A=14 B=4 C=2 D=1026 
00123 [L258] TSETS    A=14 B=13 C=23 D=3351 'y'
00124 [L258] TDUP     A=14 B=0 C=31 D=31 {'kind': 'table', 'value': {1: 0.6, 2: 0.5}}
00125 [L258] TSETS    A=14 B=13 C=20 D=3348 'anchor'
00126 [L258] CALL     A=12 B=2 C=2 D=514 
00127 [L258] KSHORT   A=13 B=0 C=1 D=1 1
00128 [L258] CALL     A=10 B=1 C=4 D=260 
00129 [L260] MOV      A=11 B=0 C=0 D=0 
00130 [L260] TGETS    A=10 B=0 C=17 D=17 'addChild'
00131 [L260] GGET     A=12 B=0 C=0 D=0 'd_ms'
00132 [L260] TGETS    A=12 B=12 C=14 D=3086 'd_u'
00133 [L260] TGETS    A=12 B=12 C=15 D=3087 'createByStyles'
00134 [L260] TDUP     A=13 B=0 C=32 D=32 {'kind': 'table', 'value': {'pic': 'v2/soulHuntUI/bkg4.png', 'x': 0.14}}
00135 [L260] TSETS    A=8 B=13 C=23 D=3351 'y'
00136 [L260] CALL     A=12 B=2 C=2 D=514 
00137 [L260] KSHORT   A=13 B=0 C=1 D=1 1
00138 [L260] CALL     A=10 B=1 C=4 D=260 
00139 [L261] MOV      A=11 B=0 C=0 D=0 
00140 [L261] TGETS    A=10 B=0 C=17 D=17 'addChild'
00141 [L261] GGET     A=12 B=0 C=0 D=0 'd_ms'
00142 [L261] TGETS    A=12 B=12 C=14 D=3086 'd_u'
00143 [L261] TGETS    A=12 B=12 C=15 D=3087 'createByStyles'
00144 [L261] TDUP     A=13 B=0 C=33 D=33 {'kind': 'table', 'value': {'pic': 'v2/soulHuntUI/label3.png', 'x': 0.09}}
00145 [L261] TSETS    A=8 B=13 C=23 D=3351 'y'
00146 [L261] CALL     A=12 B=2 C=2 D=514 
00147 [L261] KSHORT   A=13 B=0 C=1 D=1 1
00148 [L261] CALL     A=10 B=1 C=4 D=260 
00149 [L263] TDUP     A=10 B=0 C=34 D=34 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00150 [L265] TDUP     A=11 B=0 C=35 D=35 {'kind': 'table', 'value': {'npic': 'v2/introUI/close1.png', 'spic': 'v2/introUI/close2.png', 'x': 0.95}}
00151 [L266] TSETS    A=8 B=11 C=23 D=2839 'y'
00152 [L266] GGET     A=12 B=0 C=36 D=36 'pressClose'
00153 [L266] TSETS    A=12 B=11 C=37 D=2853 'call_back'
00154 [L266] TSETB    A=11 B=10 C=1 D=2561 
00155 [L266] TDUP     A=11 B=0 C=38 D=38 {'kind': 'table', 'value': {'npic': 'v2/soulHuntUI/btn_question.png', 'spic': 'v2/soulHuntUI/btn_question.png', 'x': 0.03}}
00156 [L267] TSETS    A=8 B=11 C=23 D=2839 'y'
00157 [L267] GGET     A=12 B=0 C=39 D=39 'pressQuestion'
00158 [L267] TSETS    A=12 B=11 C=37 D=2853 'call_back'
00159 [L267] TSETB    A=11 B=10 C=2 D=2562 
00160 [L267] TDUP     A=11 B=0 C=40 D=40 {'kind': 'table', 'value': {'npic': 'v2/soulHuntUI/btn_add.png', 'spic': 'v2/soulHuntUI/btn_add.png', 'x': 0.3}}
00161 [L268] MULNV    A=12 B=4 C=2 D=1026 
00162 [L268] TSETS    A=12 B=11 C=23 D=2839 'y'
00163 [L268] GGET     A=12 B=0 C=41 D=41 'pressBuyEnergy'
00164 [L268] TSETS    A=12 B=11 C=37 D=2853 'call_back'
00165 [L268] TSETB    A=11 B=10 C=3 D=2563 
00166 [L268] TDUP     A=11 B=0 C=42 D=42 {'kind': 'table', 'value': {'npic': 'v2/soulHuntUI/btn_choose.png', 'spic': 'v2/soulHuntUI/btn_choose.png', 'x': 0.6}}
00167 [L269] MULNV    A=12 B=4 C=2 D=1026 
00168 [L269] TSETS    A=12 B=11 C=23 D=2839 'y'
00169 [L269] GGET     A=12 B=0 C=43 D=43 'pressChoose'
00170 [L269] TSETS    A=12 B=11 C=37 D=2853 'call_back'
00171 [L269] TSETB    A=11 B=10 C=4 D=2564 
00172 [L269] TDUP     A=11 B=0 C=44 D=44 {'kind': 'table', 'value': {'npic': 'v2/soulHuntUI/refresh1.png', 'spic': 'v2/soulHuntUI/refresh2.png', 'x': 0.9}}
00173 [L270] MULNV    A=12 B=4 C=2 D=1026 
00174 [L270] TSETS    A=12 B=11 C=23 D=2839 'y'
00175 [L270] GGET     A=12 B=0 C=45 D=45 'pressRefresh'
00176 [L270] TSETS    A=12 B=11 C=37 D=2853 'call_back'
00177 [L270] TSETB    A=11 B=10 C=5 D=2565 
00178 [L270] TDUP     A=11 B=0 C=46 D=46 {'kind': 'table', 'value': {'npic': 'v2/soulHuntUI/btn_rank1.png', 'spic': 'v2/soulHuntUI/btn_rank2.png', 'x': 0.94}}
00179 [L271] MULNV    A=12 B=7 C=3 D=1795 
00180 [L271] ADDVV    A=12 B=4 C=12 D=1036 
00181 [L271] TSETS    A=12 B=11 C=23 D=2839 'y'
00182 [L271] GGET     A=12 B=0 C=47 D=47 'pressRank'
00183 [L271] TSETS    A=12 B=11 C=37 D=2853 'call_back'
00184 [L271] TSETB    A=11 B=10 C=6 D=2566 
00185 [L271] TDUP     A=11 B=0 C=48 D=48 {'kind': 'table', 'value': {'npic': 'v2/soulHuntUI/btn_shop1.png', 'spic': 'v2/soulHuntUI/btn_shop2.png', 'x': 0.94}}
00186 [L272] MULNV    A=12 B=7 C=4 D=1796 
00187 [L272] ADDVV    A=12 B=4 C=12 D=1036 
00188 [L272] TSETS    A=12 B=11 C=23 D=2839 'y'
00189 [L272] GGET     A=12 B=0 C=49 D=49 'pressShop'
00190 [L272] TSETS    A=12 B=11 C=37 D=2853 'call_back'
00191 [L272] TSETB    A=11 B=10 C=7 D=2567 
00192 [L272] TDUP     A=11 B=0 C=50 D=50 {'kind': 'table', 'value': {'npic': 'v2/soulHuntUI/ball0.png', 'spic': 'v2/soulHuntUI/ball0.png', 'x': 0.5}}
00193 [L273] UGET     A=12 B=0 C=2 D=2 g_self
00194 [L273] TGETS    A=12 B=12 C=51 D=3123 'Below'
00195 [L273] UGET     A=13 B=0 C=3 D=3 scrSize
00196 [L273] TGETS    A=13 B=13 C=52 D=3380 'height'
00197 [L273] DIVVV    A=12 B=12 C=13 D=3085 
00198 [L273] ADDVV    A=12 B=4 C=12 D=1036 
00199 [L273] TSETS    A=12 B=11 C=23 D=2839 'y'
00200 [L273] GGET     A=12 B=0 C=53 D=53 'pressShoot'
00201 [L273] TSETS    A=12 B=11 C=37 D=2853 'call_back'
00202 [L273] TSETB    A=11 B=10 C=8 D=2568 
00203 [L275] TNEW     A=11 B=0 C=0 D=0 
00204 [L276] MOV      A=13 B=0 C=0 D=0 
00205 [L276] TGETS    A=12 B=0 C=17 D=17 'addChild'
00206 [L276] GGET     A=14 B=0 C=0 D=0 'd_ms'
00207 [L276] TGETS    A=14 B=14 C=14 D=3598 'd_u'
00208 [L276] TGETS    A=14 B=14 C=54 D=3638 'createMenu'
00209 [L276] MOV      A=15 B=0 C=10 D=10 
00210 [L276] MOV      A=16 B=0 C=11 D=11 
00211 [L276] CALL     A=14 B=2 C=3 D=515 
00212 [L276] KSHORT   A=15 B=0 C=5 D=5 5
00213 [L276] CALL     A=12 B=1 C=4 D=260 
00214 [L277] UGET     A=12 B=0 C=1 D=1 g_soulHuntUI
00215 [L277] TGETB    A=13 B=11 C=5 D=2821 
00216 [L277] TSETS    A=13 B=12 C=55 D=3127 'refreshBtn'
00217 [L278] UGET     A=12 B=0 C=2 D=2 g_self
00218 [L278] TGETS    A=12 B=12 C=56 D=3128 'h1'
00219 [L278] IST      A=0 B=0 C=12 D=12 
00220 [L278] JMP      A=12 B=128 C=19 D=32787 target=240
00221 [L279] UGET     A=12 B=0 C=2 D=2 g_self
00222 [L279] TSETS    A=7 B=12 C=56 D=3128 'h1'
00223 [L280] UGET     A=12 B=0 C=2 D=2 g_self
00224 [L280] TSETS    A=4 B=12 C=57 D=3129 'h2'
00225 [L281] UGET     A=12 B=0 C=2 D=2 g_self
00226 [L281] TSETS    A=8 B=12 C=58 D=3130 'top_y'
00227 [L282] UGET     A=12 B=0 C=2 D=2 g_self
00228 [L282] UGET     A=13 B=0 C=3 D=3 scrSize
00229 [L282] TGETS    A=13 B=13 C=60 D=3388 'width'
00230 [L282] MULNV    A=13 B=13 C=2 D=3330 
00231 [L282] TSETS    A=13 B=12 C=59 D=3131 'cannon_x'
00232 [L283] UGET     A=12 B=0 C=2 D=2 g_self
00233 [L283] UGET     A=13 B=0 C=3 D=3 scrSize
00234 [L283] TGETS    A=13 B=13 C=52 D=3380 'height'
00235 [L283] MULVV    A=13 B=4 C=13 D=1037 
00236 [L283] UGET     A=14 B=0 C=2 D=2 g_self
00237 [L283] TGETS    A=14 B=14 C=51 D=3635 'Below'
00238 [L283] ADDVV    A=13 B=13 C=14 D=3342 
00239 [L283] TSETS    A=13 B=12 C=61 D=3133 'cannon_y'
00240 [L286] GGET     A=12 B=0 C=62 D=62 'showFreshTimes'
00241 [L286] CALL     A=12 B=1 C=1 D=257 
00242 [L287] GGET     A=12 B=0 C=63 D=63 'showEnergy'
00243 [L287] CALL     A=12 B=1 C=1 D=257 
00244 [L288] GGET     A=12 B=0 C=64 D=64 'showSoulCount'
00245 [L288] CALL     A=12 B=1 C=1 D=257 
00246 [L289] GGET     A=12 B=0 C=65 D=65 'showCannon'
00247 [L289] CALL     A=12 B=1 C=1 D=257 
00248 [L290] GGET     A=12 B=0 C=66 D=66 'showShootTimes'
00249 [L290] CALL     A=12 B=1 C=1 D=257 
00250 [L291] GGET     A=12 B=0 C=67 D=67 'showSouls'
00251 [L291] CALL     A=12 B=1 C=1 D=257 
00252 [L292] GGET     A=12 B=0 C=68 D=68 'showBall'
00253 [L292] CALL     A=12 B=1 C=1 D=257 
00254 [L294] UGET     A=12 B=0 C=2 D=2 g_self
00255 [L294] TGETS    A=12 B=12 C=69 D=3141 'end_time'
00256 [L294] GGET     A=13 B=0 C=0 D=0 'd_ms'
00257 [L294] TGETS    A=13 B=13 C=4 D=3332 'd_time'
00258 [L294] TGETS    A=13 B=13 C=5 D=3333 'getTime'
00259 [L294] CALL     A=13 B=2 C=1 D=513 
00260 [L294] SUBVV    A=12 B=12 C=13 D=3085 
00261 [L295] KSHORT   A=13 B=0 C=0 D=0 0
00262 [L295] ISGE     A=13 B=0 C=12 D=12 
00263 [L295] JMP      A=13 B=128 C=7 D=32775 target=271
00264 [L296] GGET     A=13 B=0 C=0 D=0 'd_ms'
00265 [L296] TGETS    A=13 B=13 C=14 D=3342 'd_u'
00266 [L296] TGETS    A=13 B=13 C=70 D=3398 'delay'
00267 [L296] MOV      A=14 B=0 C=0 D=0 
00268 [L296] MOV      A=15 B=0 C=12 D=12 
00269 [L296] GGET     A=16 B=0 C=36 D=36 'pressClose'
00270 [L296] CALL     A=13 B=1 C=4 D=260 
00271 [L299] GGET     A=13 B=0 C=71 D=71 'showSoulHuntGuide'
00272 [L299] CALL     A=13 B=1 C=1 D=257 
00273 [L300] GGET     A=13 B=0 C=72 D=72 'showHint'
00274 [L300] CALL     A=13 B=1 C=1 D=257 
00275 [L301] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto10 offset=0x1b7c source_lines=303-314 params=0
UPVALUES ['g_soulHuntUI', 'tags', 'g_self', 'CCPointMake', 'scrSize']
00001 [L304] UGET     A=0 B=0 C=0 D=0 g_soulHuntUI
00002 [L304] TGETS    A=0 B=0 C=0 D=0 'main_layer'
00003 [L304] IST      A=0 B=0 C=0 D=0 
00004 [L304] JMP      A=0 B=128 C=1 D=32769 target=6
00005 [L305] RET0     A=0 B=0 C=1 D=1 
00006 [L307] UGET     A=0 B=0 C=0 D=0 g_soulHuntUI
00007 [L307] TGETS    A=0 B=0 C=0 D=0 'main_layer'
00008 [L307] MOV      A=1 B=0 C=0 D=0 
00009 [L307] TGETS    A=0 B=0 C=1 D=1 'getChildByTag'
00010 [L307] UGET     A=2 B=0 C=1 D=1 tags
00011 [L307] TGETS    A=2 B=2 C=2 D=514 'Hint'
00012 [L307] CALL     A=0 B=2 C=3 D=515 
00013 [L308] IST      A=0 B=0 C=0 D=0 
00014 [L308] JMP      A=1 B=128 C=34 D=32802 target=49
00015 [L308] UGET     A=1 B=0 C=2 D=2 g_self
00016 [L308] TGETS    A=1 B=1 C=3 D=259 'has_week_prize'
00017 [L308] ISF      A=0 B=0 C=1 D=1 
00018 [L308] JMP      A=2 B=128 C=30 D=32798 target=49
00019 [L309] GGET     A=1 B=0 C=4 D=4 'd_ms'
00020 [L309] TGETS    A=1 B=1 C=5 D=261 'd_mainUI'
00021 [L309] TGETS    A=1 B=1 C=6 D=262 'createHintNum'
00022 [L309] KSHORT   A=2 B=0 C=1 D=1 1
00023 [L309] UGET     A=3 B=0 C=3 D=3 CCPointMake
00024 [L309] UGET     A=4 B=0 C=4 D=4 scrSize
00025 [L309] TGETS    A=4 B=4 C=7 D=1031 'width'
00026 [L309] MULNV    A=4 B=4 C=0 D=1024 
00027 [L309] UGET     A=5 B=0 C=2 D=2 g_self
00028 [L309] TGETS    A=5 B=5 C=8 D=1288 'h2'
00029 [L309] UGET     A=6 B=0 C=2 D=2 g_self
00030 [L309] TGETS    A=6 B=6 C=9 D=1545 'h1'
00031 [L309] MULNV    A=6 B=6 C=1 D=1537 
00032 [L309] ADDVV    A=5 B=5 C=6 D=1286 
00033 [L309] UGET     A=6 B=0 C=4 D=4 scrSize
00034 [L309] TGETS    A=6 B=6 C=10 D=1546 'height'
00035 [L309] MULVV    A=5 B=5 C=6 D=1286 
00036 [L309] CALL     A=3 B=0 C=3 D=3 
00037 [L309] CALLM    A=1 B=2 C=1 D=513 
00038 [L309] MOV      A=0 B=0 C=1 D=1 
00039 [L310] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00040 [L310] TGETS    A=1 B=1 C=0 D=256 'main_layer'
00041 [L310] MOV      A=2 B=0 C=1 D=1 
00042 [L310] TGETS    A=1 B=1 C=11 D=267 'addChild'
00043 [L310] MOV      A=3 B=0 C=0 D=0 
00044 [L310] KSHORT   A=4 B=0 C=6 D=6 6
00045 [L310] UGET     A=5 B=0 C=1 D=1 tags
00046 [L310] TGETS    A=5 B=5 C=2 D=1282 'Hint'
00047 [L310] CALL     A=1 B=1 C=5 D=261 
00048 [L310] JMP      A=1 B=128 C=13 D=32781 target=62
00049 [L311] ISF      A=0 B=0 C=0 D=0 
00050 [L311] JMP      A=1 B=128 C=11 D=32779 target=62
00051 [L311] UGET     A=1 B=0 C=2 D=2 g_self
00052 [L311] TGETS    A=1 B=1 C=3 D=259 'has_week_prize'
00053 [L311] IST      A=0 B=0 C=1 D=1 
00054 [L311] JMP      A=1 B=128 C=7 D=32775 target=62
00055 [L312] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00056 [L312] TGETS    A=1 B=1 C=0 D=256 'main_layer'
00057 [L312] MOV      A=2 B=0 C=1 D=1 
00058 [L312] TGETS    A=1 B=1 C=12 D=268 'removeChild'
00059 [L312] MOV      A=3 B=0 C=0 D=0 
00060 [L312] KPRI     A=4 B=0 C=2 D=2 
00061 [L312] CALL     A=1 B=1 C=4 D=260 
00062 [L314] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto11 offset=0x1d83 source_lines=316-318 params=2
UPVALUES ['CCPointMake', 'scrSize', 'g_self']
00001 [L317] UGET     A=2 B=0 C=0 D=0 CCPointMake
00002 [L317] UGET     A=3 B=0 C=1 D=1 scrSize
00003 [L317] TGETS    A=3 B=3 C=0 D=768 'width'
00004 [L317] MULNV    A=3 B=3 C=0 D=768 
00005 [L317] ADDVV    A=3 B=0 C=3 D=3 
00006 [L317] UGET     A=4 B=0 C=2 D=2 g_self
00007 [L317] TGETS    A=4 B=4 C=1 D=1025 'h2'
00008 [L317] UGET     A=5 B=0 C=1 D=1 scrSize
00009 [L317] TGETS    A=5 B=5 C=2 D=1282 'height'
00010 [L317] MULVV    A=4 B=4 C=5 D=1029 
00011 [L317] ADDVV    A=4 B=1 C=4 D=260 
00012 [L317] CALLT    A=2 B=0 C=3 D=3 

FUNCTION proto12 offset=0x1e0c source_lines=337-349 params=0
UPVALUES ['index', 'list', 'points', 'CCSprite', 'getWorldPosition', 'layer', 'addSoul', 'sLayer']
00001 [L338] UGET     A=0 B=0 C=0 D=0 index
00002 [L338] ADDVN    A=0 B=0 C=0 D=0 
00003 [L338] USETV    A=0 B=0 C=0 D=0 index
00004 [L339] UGET     A=0 B=0 C=1 D=1 list
00005 [L339] UGET     A=1 B=0 C=0 D=0 index
00006 [L339] TGETV    A=0 B=0 C=1 D=1 
00007 [L339] ISF      A=0 B=0 C=0 D=0 
00008 [L339] JMP      A=1 B=128 C=37 D=32805 target=46
00009 [L340] UGET     A=0 B=0 C=2 D=2 points
00010 [L340] UGET     A=1 B=0 C=1 D=1 list
00011 [L340] UGET     A=2 B=0 C=0 D=0 index
00012 [L340] TGETV    A=1 B=1 C=2 D=258 
00013 [L340] TGETV    A=0 B=0 C=1 D=1 
00014 [L341] UGET     A=1 B=0 C=3 D=3 CCSprite
00015 [L341] MOV      A=2 B=0 C=1 D=1 
00016 [L341] TGETS    A=1 B=1 C=0 D=256 'create'
00017 [L341] KSTR     A=3 B=0 C=1 D=1 'v2/soulHuntUI/soul'
00018 [L341] TGETS    A=4 B=0 C=2 D=2 'soul_type'
00019 [L341] KSTR     A=5 B=0 C=3 D=3 '.png'
00020 [L341] CAT      A=3 B=3 C=5 D=773 
00021 [L341] CALL     A=1 B=2 C=3 D=515 
00022 [L342] MOV      A=3 B=0 C=1 D=1 
00023 [L342] TGETS    A=2 B=1 C=4 D=260 'setPosition'
00024 [L342] UGET     A=4 B=0 C=4 D=4 getWorldPosition
00025 [L342] TGETS    A=5 B=0 C=5 D=5 'x'
00026 [L342] TGETS    A=6 B=0 C=6 D=6 'y'
00027 [L342] CALL     A=4 B=0 C=3 D=3 
00028 [L342] CALLM    A=2 B=1 C=1 D=257 
00029 [L343] UGET     A=2 B=0 C=5 D=5 layer
00030 [L343] MOV      A=3 B=0 C=2 D=2 
00031 [L343] TGETS    A=2 B=2 C=7 D=519 'addChild'
00032 [L343] MOV      A=4 B=0 C=1 D=1 
00033 [L343] KSHORT   A=5 B=0 C=1 D=1 1
00034 [L343] UGET     A=6 B=0 C=1 D=1 list
00035 [L343] UGET     A=7 B=0 C=0 D=0 index
00036 [L343] TGETV    A=6 B=6 C=7 D=1543 
00037 [L343] CALL     A=2 B=1 C=5 D=261 
00038 [L345] GGET     A=2 B=0 C=8 D=8 'd_ms'
00039 [L345] TGETS    A=2 B=2 C=9 D=521 'd_u'
00040 [L345] TGETS    A=2 B=2 C=10 D=522 'delay'
00041 [L345] UGET     A=3 B=0 C=5 D=5 layer
00042 [L345] KNUM     A=4 B=0 C=1 D=1 0.1
00043 [L345] UGET     A=5 B=0 C=6 D=6 addSoul
00044 [L345] CALL     A=2 B=1 C=4 D=260 
00045 [L345] JMP      A=0 B=128 C=6 D=32774 target=52
00046 [L347] UGET     A=0 B=0 C=5 D=5 layer
00047 [L347] MOV      A=1 B=0 C=0 D=0 
00048 [L347] TGETS    A=0 B=0 C=11 D=11 'removeChild'
00049 [L347] UGET     A=2 B=0 C=7 D=7 sLayer
00050 [L347] KPRI     A=3 B=0 C=2 D=2 
00051 [L347] CALL     A=0 B=1 C=4 D=260 
00052 [L349] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto13 offset=0x1fe3 source_lines=320-358 params=1
UPVALUES ['g_soulHuntUI', 'tags', 'g_self', 'pairs', 'table', 'CCSprite', 'getWorldPosition']
00001 [L321] GGET     A=1 B=0 C=0 D=0 'd_ms'
00002 [L321] TGETS    A=1 B=1 C=1 D=257 'd_u'
00003 [L321] TGETS    A=1 B=1 C=2 D=258 'clearLayer'
00004 [L321] UGET     A=2 B=0 C=0 D=0 g_soulHuntUI
00005 [L321] TGETS    A=2 B=2 C=3 D=515 'main_layer'
00006 [L321] KSHORT   A=3 B=0 C=1 D=1 1
00007 [L321] UGET     A=4 B=0 C=1 D=1 tags
00008 [L321] TGETS    A=4 B=4 C=4 D=1028 'Soul'
00009 [L321] CALL     A=1 B=2 C=4 D=516 
00010 [L322] IST      A=0 B=0 C=1 D=1 
00011 [L322] JMP      A=2 B=128 C=1 D=32769 target=13
00012 [L323] UCLO     A=0 B=128 C=62 D=32830 target=75
00013 [L325] UGET     A=2 B=0 C=2 D=2 g_self
00014 [L325] TGETS    A=2 B=2 C=5 D=517 'role_hunt_data'
00015 [L325] TGETS    A=2 B=2 C=6 D=518 'point_list'
00016 [L326] ISF      A=0 B=0 C=2 D=2 
00017 [L326] JMP      A=3 B=128 C=3 D=32771 target=21
00018 [L326] LEN      A=3 B=0 C=2 D=2 
00019 [L326] ISNEN    A=3 B=0 C=0 D=0 0
00020 [L326] JMP      A=3 B=128 C=1 D=32769 target=22
00021 [L327] UCLO     A=0 B=128 C=54 D=32822 target=76
00022 [L329] ISF      A=0 B=0 C=0 D=0 
00023 [L329] JMP      A=3 B=128 C=22 D=32790 target=46
00024 [L330] GGET     A=3 B=0 C=0 D=0 'd_ms'
00025 [L330] TGETS    A=3 B=3 C=1 D=769 'd_u'
00026 [L330] TGETS    A=3 B=3 C=7 D=775 'createSwallowTouchLayer'
00027 [L330] MOV      A=4 B=0 C=1 D=1 
00028 [L330] CALL     A=3 B=2 C=2 D=514 
00029 [L331] TNEW     A=4 B=0 C=0 D=0 
00030 [L332] UGET     A=5 B=0 C=3 D=3 pairs
00031 [L332] MOV      A=6 B=0 C=2 D=2 
00032 [L332] CALL     A=5 B=4 C=2 D=1026 
00033 [L332] ISNEXT   A=8 B=128 C=5 D=32773 target=39
00034 [L333] UGET     A=10 B=0 C=4 D=4 table
00035 [L333] TGETS    A=10 B=10 C=8 D=2568 'insert'
00036 [L333] MOV      A=11 B=0 C=4 D=4 
00037 [L333] MOV      A=12 B=0 C=8 D=8 
00038 [L333] CALL     A=10 B=1 C=3 D=259 
00039 [L332] ITERN    A=8 B=3 C=3 D=771 
00040 [L332] ITERL    A=8 B=127 C=249 D=32761 target=34
00041 [L336] KSHORT   A=5 B=0 C=0 D=0 0
00042 [L349] FNEW     A=6 B=0 C=9 D=9 {'kind': 'proto', 'id': 12}
00043 [L350] MOV      A=7 B=0 C=6 D=6 
00044 [L350] CALL     A=7 B=1 C=1 D=257 
00045 [L350] UCLO     A=3 B=128 C=27 D=32795 target=73
00046 [L352] UGET     A=3 B=0 C=3 D=3 pairs
00047 [L352] MOV      A=4 B=0 C=2 D=2 
00048 [L352] CALL     A=3 B=4 C=2 D=1026 
00049 [L352] ISNEXT   A=6 B=128 C=21 D=32789 target=71
00050 [L353] UGET     A=8 B=0 C=5 D=5 CCSprite
00051 [L353] MOV      A=9 B=0 C=8 D=8 
00052 [L353] TGETS    A=8 B=8 C=10 D=2058 'create'
00053 [L353] KSTR     A=10 B=0 C=11 D=11 'v2/soulHuntUI/soul'
00054 [L353] TGETS    A=11 B=7 C=12 D=1804 'soul_type'
00055 [L353] KSTR     A=12 B=0 C=13 D=13 '.png'
00056 [L353] CAT      A=10 B=10 C=12 D=2572 
00057 [L353] CALL     A=8 B=2 C=3 D=515 
00058 [L354] MOV      A=10 B=0 C=8 D=8 
00059 [L354] TGETS    A=9 B=8 C=14 D=2062 'setPosition'
00060 [L354] UGET     A=11 B=0 C=6 D=6 getWorldPosition
00061 [L354] TGETS    A=12 B=7 C=15 D=1807 'x'
00062 [L354] TGETS    A=13 B=7 C=16 D=1808 'y'
00063 [L354] CALL     A=11 B=0 C=3 D=3 
00064 [L354] CALLM    A=9 B=1 C=1 D=257 
00065 [L355] MOV      A=10 B=0 C=1 D=1 
00066 [L355] TGETS    A=9 B=1 C=17 D=273 'addChild'
00067 [L355] MOV      A=11 B=0 C=8 D=8 
00068 [L355] KSHORT   A=12 B=0 C=1 D=1 1
00069 [L355] MOV      A=13 B=0 C=6 D=6 
00070 [L355] CALL     A=9 B=1 C=5 D=261 
00071 [L352] ITERN    A=6 B=3 C=3 D=771 
00072 [L352] ITERL    A=6 B=127 C=233 D=32745 target=50
00073 [L358] UCLO     A=0 B=128 C=0 D=32768 target=74
00074 [L358] RET0     A=0 B=0 C=1 D=1 
00075 [L358] RET0     A=0 B=0 C=1 D=1 
00076 [L358] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto14 offset=0x22c6 source_lines=361-376 params=0
UPVALUES ['g_self', 'g_soulHuntUI']
00001 [L362] UGET     A=0 B=0 C=0 D=0 g_self
00002 [L362] TGETS    A=0 B=0 C=0 D=0 'role_hunt_data'
00003 [L362] TGETS    A=0 B=0 C=1 D=1 'left_flush_times'
00004 [L362] ISNEN    A=0 B=0 C=0 D=0 0
00005 [L362] JMP      A=0 B=128 C=10 D=32778 target=16
00006 [L363] GGET     A=0 B=0 C=2 D=2 'd_ms'
00007 [L363] TGETS    A=0 B=0 C=3 D=3 'd_info'
00008 [L363] TGETS    A=0 B=0 C=4 D=4 'show'
00009 [L363] GGET     A=1 B=0 C=2 D=2 'd_ms'
00010 [L363] TGETS    A=1 B=1 C=5 D=261 'd_hz'
00011 [L363] TGETS    A=1 B=1 C=6 D=262 'gethz'
00012 [L363] KSTR     A=2 B=0 C=7 D=7 'hunt8'
00013 [L363] CALL     A=1 B=0 C=2 D=2 
00014 [L363] CALLM    A=0 B=1 C=0 D=256 
00015 [L363] JMP      A=0 B=128 C=31 D=32799 target=47
00016 [L365] TDUP     A=0 B=0 C=8 D=8 {'kind': 'table', 'value': {'string': ''}}
00017 [L368] TNEW     A=1 B=0 C=3 D=3 
00018 [L369] TDUP     A=2 B=0 C=9 D=9 {'kind': 'table', 'value': {'y': 0.05, 'type': 'label', 'x': 0, 'fontsize': 30}}
00019 [L370] GGET     A=3 B=0 C=2 D=2 'd_ms'
00020 [L370] TGETS    A=3 B=3 C=5 D=773 'd_hz'
00021 [L370] TGETS    A=3 B=3 C=6 D=774 'gethz'
00022 [L370] KSTR     A=4 B=0 C=10 D=10 'hunt17'
00023 [L370] CALL     A=3 B=2 C=2 D=514 
00024 [L370] TSETS    A=3 B=2 C=11 D=523 'string'
00025 [L370] TDUP     A=3 B=0 C=12 D=12 {'kind': 'table', 'value': {1: 250, 2: 150, 3: 50}}
00026 [L370] TSETS    A=3 B=2 C=13 D=525 'color'
00027 [L370] TSETB    A=2 B=1 C=1 D=257 
00028 [L370] TDUP     A=2 B=0 C=14 D=14 {'kind': 'table', 'value': {'y': -0.1, 'type': 'label', 'x': 0, 'fontsize': 26}}
00029 [L371] GGET     A=3 B=0 C=2 D=2 'd_ms'
00030 [L371] TGETS    A=3 B=3 C=5 D=773 'd_hz'
00031 [L371] TGETS    A=3 B=3 C=6 D=774 'gethz'
00032 [L371] KSTR     A=4 B=0 C=15 D=15 'hunt18'
00033 [L371] CALL     A=3 B=2 C=2 D=514 
00034 [L371] TSETS    A=3 B=2 C=11 D=523 'string'
00035 [L371] TDUP     A=3 B=0 C=16 D=16 {'kind': 'table', 'value': {1: 200, 2: 200, 3: 200}}
00036 [L371] TSETS    A=3 B=2 C=13 D=525 'color'
00037 [L371] TSETB    A=2 B=1 C=2 D=258 
00038 [L372] TSETS    A=1 B=0 C=17 D=17 'txt_styles'
00039 [L374] GGET     A=1 B=0 C=2 D=2 'd_ms'
00040 [L374] TGETS    A=1 B=1 C=18 D=274 'd_quitUI'
00041 [L374] TGETS    A=1 B=1 C=19 D=275 'createYesNoByStyle'
00042 [L374] UGET     A=2 B=0 C=1 D=1 g_soulHuntUI
00043 [L374] TGETS    A=2 B=2 C=20 D=532 'main_layer'
00044 [L374] MOV      A=3 B=0 C=0 D=0 
00045 [L374] GGET     A=4 B=0 C=21 D=21 'sendSoulFlushRequest'
00046 [L374] CALL     A=1 B=1 C=4 D=260 
00047 [L376] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto15 offset=0x2502 source_lines=392-395 params=0
UPVALUES ['layer']
00001 [L393] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L393] TGETS    A=0 B=0 C=1 D=1 'd_u'
00003 [L393] TGETS    A=0 B=0 C=2 D=2 'remove'
00004 [L393] UGET     A=1 B=0 C=0 D=0 layer
00005 [L393] CALL     A=0 B=1 C=2 D=258 
00006 [L394] KPRI     A=0 B=0 C=2 D=2 
00007 [L394] RET1     A=0 B=0 C=2 D=2 

FUNCTION proto16 offset=0x254a source_lines=402-406 params=1
UPVALUES ['g_self', 'layer']
00001 [L403] UGET     A=1 B=0 C=0 D=0 g_self
00002 [L403] TSETS    A=0 B=1 C=0 D=256 'ball'
00003 [L404] GGET     A=1 B=0 C=1 D=1 'showBall'
00004 [L404] CALL     A=1 B=1 C=1 D=257 
00005 [L405] GGET     A=1 B=0 C=2 D=2 'd_ms'
00006 [L405] TGETS    A=1 B=1 C=3 D=259 'd_u'
00007 [L405] TGETS    A=1 B=1 C=4 D=260 'remove'
00008 [L405] UGET     A=2 B=0 C=1 D=1 layer
00009 [L405] CALL     A=1 B=1 C=2 D=258 
00010 [L406] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto17 offset=0x25bf source_lines=379-428 params=0
UPVALUES ['g_soulHuntUI', 'tags', 'CCLayerColor', 'ccc4', 'CCRectMake', 'scrSize', 'g_self', 'table', 'string']
00001 [L380] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L380] TGETS    A=0 B=0 C=1 D=1 'd_u'
00003 [L380] TGETS    A=0 B=0 C=2 D=2 'clearLayer'
00004 [L380] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00005 [L380] TGETS    A=1 B=1 C=3 D=259 'main_layer'
00006 [L380] KSHORT   A=2 B=0 C=4 D=4 4
00007 [L380] UGET     A=3 B=0 C=1 D=1 tags
00008 [L380] TGETS    A=3 B=3 C=4 D=772 'BallChoose'
00009 [L380] CALL     A=0 B=2 C=4 D=516 
00010 [L381] IST      A=0 B=0 C=0 D=0 
00011 [L381] JMP      A=1 B=128 C=1 D=32769 target=13
00012 [L382] UCLO     A=0 B=128 C=175 D=32943 target=188
00013 [L384] UGET     A=1 B=0 C=2 D=2 CCLayerColor
00014 [L384] MOV      A=2 B=0 C=1 D=1 
00015 [L384] TGETS    A=1 B=1 C=5 D=261 'create'
00016 [L384] UGET     A=3 B=0 C=3 D=3 ccc4
00017 [L384] KSHORT   A=4 B=0 C=0 D=0 0
00018 [L384] KSHORT   A=5 B=0 C=0 D=0 0
00019 [L384] KSHORT   A=6 B=0 C=0 D=0 0
00020 [L384] KSHORT   A=7 B=0 C=100 D=100 100
00021 [L384] CALL     A=3 B=0 C=5 D=5 
00022 [L384] CALLM    A=1 B=2 C=1 D=513 
00023 [L385] MOV      A=3 B=0 C=0 D=0 
00024 [L385] TGETS    A=2 B=0 C=6 D=6 'addChild'
00025 [L385] MOV      A=4 B=0 C=1 D=1 
00026 [L385] KSHORT   A=5 B=255 C=255 D=65535 -1
00027 [L385] CALL     A=2 B=1 C=4 D=260 
00028 [L387] GGET     A=2 B=0 C=0 D=0 'd_ms'
00029 [L387] TGETS    A=2 B=2 C=1 D=513 'd_u'
00030 [L387] TGETS    A=2 B=2 C=7 D=519 'createByStyles'
00031 [L387] TDUP     A=3 B=0 C=8 D=8 {'kind': 'table', 'value': {'pic': 'v2/soulHuntUI/bkg3.png', 'x': 0.6, 'y': 0}}
00032 [L387] TDUP     A=4 B=0 C=9 D=9 {'kind': 'table', 'value': {1: 0.18, 2: 0}}
00033 [L387] TSETS    A=4 B=3 C=10 D=778 'anchor'
00034 [L387] CALL     A=2 B=2 C=2 D=514 
00035 [L388] MOV      A=4 B=0 C=0 D=0 
00036 [L388] TGETS    A=3 B=0 C=6 D=6 'addChild'
00037 [L388] MOV      A=5 B=0 C=2 D=2 
00038 [L388] CALL     A=3 B=1 C=3 D=259 
00039 [L389] GGET     A=3 B=0 C=0 D=0 'd_ms'
00040 [L389] TGETS    A=3 B=3 C=1 D=769 'd_u'
00041 [L389] TGETS    A=3 B=3 C=11 D=779 'getRealScale'
00042 [L389] MOV      A=4 B=0 C=2 D=2 
00043 [L389] CALL     A=3 B=3 C=2 D=770 
00044 [L390] MULNV    A=5 B=3 C=0 D=768 
00045 [L390] SUBNV    A=5 B=5 C=1 D=1281 
00046 [L395] FNEW     A=6 B=0 C=12 D=12 {'kind': 'proto', 'id': 15}
00047 [L396] TNEW     A=7 B=0 C=0 D=0 
00048 [L397] KSHORT   A=8 B=0 C=100 D=100 100
00049 [L397] TSETS    A=8 B=7 C=13 D=1805 'z'
00050 [L398] TSETS    A=6 B=7 C=14 D=1806 'outFunc'
00051 [L399] UGET     A=8 B=0 C=4 D=4 CCRectMake
00052 [L399] UGET     A=9 B=0 C=5 D=5 scrSize
00053 [L399] TGETS    A=9 B=9 C=16 D=2320 'width'
00054 [L399] MULVV    A=9 B=5 C=9 D=1289 
00055 [L399] UGET     A=10 B=0 C=5 D=5 scrSize
00056 [L399] TGETS    A=10 B=10 C=17 D=2577 'height'
00057 [L399] MULNV    A=10 B=10 C=2 D=2562 
00058 [L399] UGET     A=11 B=0 C=5 D=5 scrSize
00059 [L399] TGETS    A=11 B=11 C=16 D=2832 'width'
00060 [L399] MULVV    A=11 B=3 C=11 D=779 
00061 [L399] UGET     A=12 B=0 C=5 D=5 scrSize
00062 [L399] TGETS    A=12 B=12 C=17 D=3089 'height'
00063 [L399] MULVV    A=12 B=4 C=12 D=1036 
00064 [L399] CALL     A=8 B=2 C=5 D=517 
00065 [L399] TSETS    A=8 B=7 C=15 D=1807 'rect'
00066 [L400] GGET     A=8 B=0 C=0 D=0 'd_ms'
00067 [L400] TGETS    A=8 B=8 C=1 D=2049 'd_u'
00068 [L400] TGETS    A=8 B=8 C=18 D=2066 'createSwallowTouchLayerFunc'
00069 [L400] MOV      A=9 B=0 C=0 D=0 
00070 [L400] MOV      A=10 B=0 C=7 D=7 
00071 [L400] CALL     A=8 B=1 C=3 D=259 
00072 [L406] FNEW     A=8 B=0 C=19 D=19 {'kind': 'proto', 'id': 16}
00073 [L408] TDUP     A=9 B=0 C=20 D=20 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00074 [L412] TNEW     A=10 B=0 C=4 D=4 
00075 [L412] TDUP     A=11 B=0 C=21 D=21 {'kind': 'table', 'value': {1: 60, 2: 180, 3: 230}}
00076 [L412] TSETB    A=11 B=10 C=1 D=2561 
00077 [L412] TDUP     A=11 B=0 C=22 D=22 {'kind': 'table', 'value': {1: 240, 2: 220, 3: 0}}
00078 [L412] TSETB    A=11 B=10 C=2 D=2562 
00079 [L412] TDUP     A=11 B=0 C=23 D=23 {'kind': 'table', 'value': {1: 200, 2: 80, 3: 255}}
00080 [L412] TSETB    A=11 B=10 C=3 D=2563 
00081 [L413] KSHORT   A=11 B=0 C=1 D=1 1
00082 [L413] KSHORT   A=12 B=0 C=3 D=3 3
00083 [L413] KSHORT   A=13 B=0 C=1 D=1 1
00084 [L413] FORI     A=11 B=128 C=92 D=32860 target=177
00085 [L414] MULNV    A=15 B=14 C=3 D=3587 
00086 [L414] ADDNV    A=15 B=15 C=4 D=3844 
00087 [L414] MULVV    A=15 B=15 C=4 D=3844 
00088 [L415] UGET     A=16 B=0 C=6 D=6 g_self
00089 [L415] TGETS    A=16 B=16 C=24 D=4120 'BallPrice'
00090 [L415] TGETV    A=16 B=16 C=14 D=4110 
00091 [L417] UGET     A=17 B=0 C=7 D=7 table
00092 [L417] TGETS    A=17 B=17 C=25 D=4377 'insert'
00093 [L417] MOV      A=18 B=0 C=9 D=9 
00094 [L417] TDUP     A=19 B=0 C=26 D=26 {'kind': 'table', 'value': {'npic': 'v2/soulHuntUI/bkg5.png', 'spic': 'v2/soulHuntUI/bkg5.png'}}
00095 [L417] MULNV    A=20 B=3 C=5 D=773 
00096 [L417] ADDVV    A=20 B=5 C=20 D=1300 
00097 [L417] TSETS    A=20 B=19 C=27 D=4891 'x'
00098 [L417] TSETS    A=15 B=19 C=28 D=4892 'y'
00099 [L417] MULNV    A=20 B=3 C=6 D=774 
00100 [L417] TSETS    A=20 B=19 C=29 D=4893 'scaleX'
00101 [L417] TSETS    A=14 B=19 C=30 D=4894 'tag'
00102 [L417] TSETS    A=8 B=19 C=31 D=4895 'call_back'
00103 [L417] CALL     A=17 B=1 C=3 D=259 
00104 [L419] MOV      A=18 B=0 C=0 D=0 
00105 [L419] TGETS    A=17 B=0 C=6 D=6 'addChild'
00106 [L419] GGET     A=19 B=0 C=0 D=0 'd_ms'
00107 [L419] TGETS    A=19 B=19 C=1 D=4865 'd_u'
00108 [L419] TGETS    A=19 B=19 C=7 D=4871 'createByStyles'
00109 [L419] TDUP     A=20 B=0 C=34 D=34 {'kind': 'table', 'value': {}}
00110 [L419] KSTR     A=21 B=0 C=32 D=32 'v2/soulHuntUI/ball'
00111 [L419] MOV      A=22 B=0 C=14 D=14 
00112 [L419] KSTR     A=23 B=0 C=33 D=33 '1.png'
00113 [L419] CAT      A=21 B=21 C=23 D=5399 
00114 [L419] TSETS    A=21 B=20 C=35 D=5155 'pic'
00115 [L419] MULNV    A=21 B=3 C=7 D=775 
00116 [L419] ADDVV    A=21 B=5 C=21 D=1301 
00117 [L419] TSETS    A=21 B=20 C=27 D=5147 'x'
00118 [L419] TSETS    A=15 B=20 C=28 D=5148 'y'
00119 [L419] CALL     A=19 B=2 C=2 D=514 
00120 [L419] KSHORT   A=20 B=0 C=2 D=2 2
00121 [L419] CALL     A=17 B=1 C=4 D=260 
00122 [L421] GGET     A=17 B=0 C=0 D=0 'd_ms'
00123 [L421] TGETS    A=17 B=17 C=1 D=4353 'd_u'
00124 [L421] TGETS    A=17 B=17 C=36 D=4388 'createByStyle'
00125 [L421] TDUP     A=18 B=0 C=37 D=37 {'kind': 'table', 'value': {'type': 'label', 'fontsize': 26}}
00126 [L421] UGET     A=19 B=0 C=8 D=8 string
00127 [L421] TGETS    A=19 B=19 C=38 D=4902 'format'
00128 [L421] GGET     A=20 B=0 C=0 D=0 'd_ms'
00129 [L421] TGETS    A=20 B=20 C=39 D=5159 'd_hz'
00130 [L421] TGETS    A=20 B=20 C=40 D=5160 'gethz'
00131 [L421] KSTR     A=21 B=0 C=41 D=41 'hunt2'
00132 [L421] CALL     A=20 B=2 C=2 D=514 
00133 [L421] TGETS    A=21 B=16 C=42 D=4138 'need_energy'
00134 [L421] CALL     A=19 B=2 C=3 D=515 
00135 [L421] TSETS    A=19 B=18 C=43 D=4651 'string'
00136 [L421] MULNV    A=19 B=3 C=8 D=776 
00137 [L421] ADDVV    A=19 B=5 C=19 D=1299 
00138 [L421] TSETS    A=19 B=18 C=27 D=4635 'x'
00139 [L421] MULNV    A=19 B=4 C=9 D=1033 
00140 [L421] ADDVV    A=19 B=15 C=19 D=3859 
00141 [L421] TSETS    A=19 B=18 C=28 D=4636 'y'
00142 [L421] CALL     A=17 B=2 C=2 D=514 
00143 [L422] MOV      A=19 B=0 C=0 D=0 
00144 [L422] TGETS    A=18 B=0 C=6 D=6 'addChild'
00145 [L422] MOV      A=20 B=0 C=17 D=17 
00146 [L422] KSHORT   A=21 B=0 C=2 D=2 2
00147 [L422] CALL     A=18 B=1 C=4 D=260 
00148 [L424] GGET     A=18 B=0 C=0 D=0 'd_ms'
00149 [L424] TGETS    A=18 B=18 C=1 D=4609 'd_u'
00150 [L424] TGETS    A=18 B=18 C=36 D=4644 'createByStyle'
00151 [L424] TDUP     A=19 B=0 C=44 D=44 {'kind': 'table', 'value': {'type': 'label', 'fontsize': 26}}
00152 [L424] UGET     A=20 B=0 C=8 D=8 string
00153 [L424] TGETS    A=20 B=20 C=38 D=5158 'format'
00154 [L424] GGET     A=21 B=0 C=0 D=0 'd_ms'
00155 [L424] TGETS    A=21 B=21 C=39 D=5415 'd_hz'
00156 [L424] TGETS    A=21 B=21 C=40 D=5416 'gethz'
00157 [L424] KSTR     A=22 B=0 C=45 D=45 'hunt3'
00158 [L424] CALL     A=21 B=2 C=2 D=514 
00159 [L424] TGETS    A=22 B=16 C=46 D=4142 'bump_times'
00160 [L424] CALL     A=20 B=2 C=3 D=515 
00161 [L424] TSETS    A=20 B=19 C=43 D=4907 'string'
00162 [L424] MULNV    A=20 B=3 C=8 D=776 
00163 [L424] ADDVV    A=20 B=5 C=20 D=1300 
00164 [L424] TSETS    A=20 B=19 C=27 D=4891 'x'
00165 [L424] MULNV    A=20 B=4 C=9 D=1033 
00166 [L424] SUBVV    A=20 B=15 C=20 D=3860 
00167 [L424] TSETS    A=20 B=19 C=28 D=4892 'y'
00168 [L424] TGETV    A=20 B=10 C=14 D=2574 
00169 [L424] TSETS    A=20 B=19 C=47 D=4911 'color'
00170 [L424] CALL     A=18 B=2 C=2 D=514 
00171 [L425] MOV      A=20 B=0 C=0 D=0 
00172 [L425] TGETS    A=19 B=0 C=6 D=6 'addChild'
00173 [L425] MOV      A=21 B=0 C=18 D=18 
00174 [L425] KSHORT   A=22 B=0 C=2 D=2 2
00175 [L425] CALL     A=19 B=1 C=4 D=260 
00176 [L413] FORL     A=11 B=127 C=164 D=32676 target=85
00177 [L427] MOV      A=12 B=0 C=0 D=0 
00178 [L427] TGETS    A=11 B=0 C=6 D=6 'addChild'
00179 [L427] GGET     A=13 B=0 C=0 D=0 'd_ms'
00180 [L427] TGETS    A=13 B=13 C=1 D=3329 'd_u'
00181 [L427] TGETS    A=13 B=13 C=48 D=3376 'createMenu'
00182 [L427] MOV      A=14 B=0 C=9 D=9 
00183 [L427] CALL     A=13 B=2 C=2 D=514 
00184 [L427] KSHORT   A=14 B=0 C=1 D=1 1
00185 [L427] CALL     A=11 B=1 C=4 D=260 
00186 [L428] UCLO     A=0 B=128 C=0 D=32768 target=187
00187 [L428] RET0     A=0 B=0 C=1 D=1 
00188 [L428] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto18 offset=0x2ccf source_lines=473-477 params=0
UPVALUES ['layer', 'tostring', 'rate', 'count', 'w', 'h']
00001 [L474] UGET     A=0 B=0 C=0 D=0 layer
00002 [L474] MOV      A=1 B=0 C=0 D=0 
00003 [L474] TGETS    A=0 B=0 C=0 D=0 'removeChildByTag'
00004 [L474] KSHORT   A=2 B=0 C=111 D=111 111
00005 [L474] KPRI     A=3 B=0 C=2 D=2 
00006 [L474] CALL     A=0 B=1 C=4 D=260 
00007 [L475] GGET     A=0 B=0 C=1 D=1 'd_ms'
00008 [L475] TGETS    A=0 B=0 C=2 D=2 'd_u'
00009 [L475] TGETS    A=0 B=0 C=3 D=3 'createByStyles'
00010 [L475] TDUP     A=1 B=0 C=4 D=4 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 30}}
00011 [L475] UGET     A=2 B=0 C=1 D=1 tostring
00012 [L475] UGET     A=3 B=0 C=2 D=2 rate
00013 [L475] UGET     A=4 B=0 C=3 D=3 count
00014 [L475] MULVV    A=3 B=3 C=4 D=772 
00015 [L475] CALL     A=2 B=2 C=2 D=514 
00016 [L475] TSETS    A=2 B=1 C=5 D=261 'string'
00017 [L475] UGET     A=2 B=0 C=4 D=4 w
00018 [L475] MULNV    A=2 B=2 C=0 D=512 
00019 [L475] ADDNV    A=2 B=2 C=1 D=513 
00020 [L475] TSETS    A=2 B=1 C=6 D=262 'x'
00021 [L475] UGET     A=2 B=0 C=5 D=5 h
00022 [L475] MULNV    A=2 B=2 C=2 D=514 
00023 [L475] SUBNV    A=2 B=2 C=1 D=513 
00024 [L475] TSETS    A=2 B=1 C=7 D=263 'y'
00025 [L475] TDUP     A=2 B=0 C=8 D=8 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00026 [L475] TSETS    A=2 B=1 C=9 D=265 'anchor'
00027 [L475] TDUP     A=2 B=0 C=10 D=10 {'kind': 'table', 'value': {1: 200, 2: 200, 3: 200}}
00028 [L475] TSETS    A=2 B=1 C=11 D=267 'color'
00029 [L475] CALL     A=0 B=2 C=2 D=514 
00030 [L476] UGET     A=1 B=0 C=0 D=0 layer
00031 [L476] MOV      A=2 B=0 C=1 D=1 
00032 [L476] TGETS    A=1 B=1 C=12 D=268 'addChild'
00033 [L476] MOV      A=3 B=0 C=0 D=0 
00034 [L476] KSHORT   A=4 B=0 C=1 D=1 1
00035 [L476] KSHORT   A=5 B=0 C=111 D=111 111
00036 [L476] CALL     A=1 B=1 C=5 D=261 
00037 [L477] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto19 offset=0x2e6e source_lines=479-485 params=2
UPVALUES ['count', 'showDesc']
00001 [L480] USETV    A=0 B=0 C=0 D=0 count
00002 [L481] UGET     A=2 B=0 C=1 D=1 showDesc
00003 [L481] CALL     A=2 B=1 C=1 D=257 
00004 [L482] KSHORT   A=2 B=0 C=0 D=0 0
00005 [L482] ISGE     A=2 B=0 C=1 D=1 
00006 [L482] JMP      A=2 B=128 C=5 D=32773 target=12
00007 [L483] GGET     A=2 B=0 C=0 D=0 'd_ms'
00008 [L483] TGETS    A=2 B=2 C=1 D=513 'd_info'
00009 [L483] TGETS    A=2 B=2 C=2 D=514 'show'
00010 [L483] GGET     A=3 B=0 C=3 D=3 'tip'
00011 [L483] CALL     A=2 B=1 C=2 D=258 
00012 [L485] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto20 offset=0x2ef4 source_lines=492-497 params=1
UPVALUES ['layer', 'count']
00001 [L493] GGET     A=1 B=0 C=0 D=0 'd_ms'
00002 [L493] TGETS    A=1 B=1 C=1 D=257 'd_u'
00003 [L493] TGETS    A=1 B=1 C=2 D=258 'remove'
00004 [L493] UGET     A=2 B=0 C=0 D=0 layer
00005 [L493] CALL     A=1 B=1 C=2 D=258 
00006 [L494] ISNEN    A=0 B=0 C=0 D=0 2
00007 [L494] JMP      A=1 B=128 C=3 D=32771 target=11
00008 [L495] GGET     A=1 B=0 C=3 D=3 'sendBuyEnergyRequest'
00009 [L495] UGET     A=2 B=0 C=1 D=1 count
00010 [L495] CALL     A=1 B=1 C=2 D=258 
00011 [L497] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto21 offset=0x2f75 source_lines=431-509 params=0
UPVALUES ['g_soulHuntUI', 'g_self', 'math', 'CCLayer', 'CCLayerColor', 'ccc4', 'tostring']
00001 [L432] UGET     A=0 B=0 C=0 D=0 g_soulHuntUI
00002 [L432] TGETS    A=0 B=0 C=0 D=0 'main_layer'
00003 [L432] IST      A=0 B=0 C=0 D=0 
00004 [L432] JMP      A=0 B=128 C=1 D=32769 target=6
00005 [L433] UCLO     A=0 B=128 C=236 D=33004 target=242
00006 [L435] UGET     A=0 B=0 C=1 D=1 g_self
00007 [L435] TGETS    A=0 B=0 C=1 D=1 'hunt_const_config'
00008 [L435] TGETS    A=0 B=0 C=2 D=2 'max_energy'
00009 [L435] UGET     A=1 B=0 C=1 D=1 g_self
00010 [L435] TGETS    A=1 B=1 C=3 D=259 'role_hunt_data'
00011 [L435] TGETS    A=1 B=1 C=4 D=260 'left_energy'
00012 [L435] SUBVV    A=0 B=0 C=1 D=1 
00013 [L436] KSHORT   A=1 B=0 C=0 D=0 0
00014 [L436] ISGT     A=0 B=0 C=1 D=1 
00015 [L436] JMP      A=1 B=128 C=10 D=32778 target=26
00016 [L437] GGET     A=1 B=0 C=5 D=5 'd_ms'
00017 [L437] TGETS    A=1 B=1 C=6 D=262 'd_info'
00018 [L437] TGETS    A=1 B=1 C=7 D=263 'show'
00019 [L437] GGET     A=2 B=0 C=5 D=5 'd_ms'
00020 [L437] TGETS    A=2 B=2 C=8 D=520 'd_hz'
00021 [L437] TGETS    A=2 B=2 C=9 D=521 'gethz'
00022 [L437] KSTR     A=3 B=0 C=10 D=10 'hunt11'
00023 [L437] CALL     A=2 B=0 C=2 D=2 
00024 [L437] CALLM    A=1 B=1 C=0 D=256 
00025 [L438] UCLO     A=0 B=128 C=217 D=32985 target=243
00026 [L440] UGET     A=1 B=0 C=2 D=2 math
00027 [L440] TGETS    A=1 B=1 C=11 D=267 'floor'
00028 [L440] UGET     A=2 B=0 C=1 D=1 g_self
00029 [L440] TGETS    A=2 B=2 C=3 D=515 'role_hunt_data'
00030 [L440] TGETS    A=2 B=2 C=12 D=524 'left_soul_count'
00031 [L440] UGET     A=3 B=0 C=1 D=1 g_self
00032 [L440] TGETS    A=3 B=3 C=1 D=769 'hunt_const_config'
00033 [L440] TGETS    A=3 B=3 C=13 D=781 'energy_exchange_rate'
00034 [L440] DIVVV    A=2 B=2 C=3 D=515 
00035 [L440] CALL     A=1 B=2 C=2 D=514 
00036 [L441] ISNEN    A=1 B=0 C=0 D=0 0
00037 [L441] JMP      A=2 B=128 C=10 D=32778 target=48
00038 [L442] GGET     A=2 B=0 C=5 D=5 'd_ms'
00039 [L442] TGETS    A=2 B=2 C=6 D=518 'd_info'
00040 [L442] TGETS    A=2 B=2 C=7 D=519 'show'
00041 [L442] GGET     A=3 B=0 C=5 D=5 'd_ms'
00042 [L442] TGETS    A=3 B=3 C=8 D=776 'd_hz'
00043 [L442] TGETS    A=3 B=3 C=9 D=777 'gethz'
00044 [L442] KSTR     A=4 B=0 C=14 D=14 'hunt5'
00045 [L442] CALL     A=3 B=0 C=2 D=2 
00046 [L442] CALLM    A=2 B=1 C=0 D=256 
00047 [L443] UCLO     A=0 B=128 C=196 D=32964 target=244
00048 [L445] ISGE     A=1 B=0 C=0 D=0 
00049 [L445] JMP      A=2 B=128 C=8 D=32776 target=58
00050 [L446] MOV      A=0 B=0 C=1 D=1 
00051 [L447] GGET     A=2 B=0 C=5 D=5 'd_ms'
00052 [L447] TGETS    A=2 B=2 C=8 D=520 'd_hz'
00053 [L447] TGETS    A=2 B=2 C=9 D=521 'gethz'
00054 [L447] KSTR     A=3 B=0 C=14 D=14 'hunt5'
00055 [L447] CALL     A=2 B=2 C=2 D=514 
00056 [L447] GSET     A=2 B=0 C=15 D=15 'tip'
00057 [L447] JMP      A=2 B=128 C=6 D=32774 target=64
00058 [L449] GGET     A=2 B=0 C=5 D=5 'd_ms'
00059 [L449] TGETS    A=2 B=2 C=8 D=520 'd_hz'
00060 [L449] TGETS    A=2 B=2 C=9 D=521 'gethz'
00061 [L449] KSTR     A=3 B=0 C=10 D=10 'hunt11'
00062 [L449] CALL     A=2 B=2 C=2 D=514 
00063 [L449] GSET     A=2 B=0 C=15 D=15 'tip'
00064 [L452] UGET     A=2 B=0 C=3 D=3 CCLayer
00065 [L452] MOV      A=3 B=0 C=2 D=2 
00066 [L452] TGETS    A=2 B=2 C=16 D=528 'create'
00067 [L452] CALL     A=2 B=2 C=2 D=514 
00068 [L453] GGET     A=3 B=0 C=5 D=5 'd_ms'
00069 [L453] TGETS    A=3 B=3 C=17 D=785 'd_u'
00070 [L453] TGETS    A=3 B=3 C=18 D=786 'createSwallowTouchLayer'
00071 [L453] MOV      A=4 B=0 C=2 D=2 
00072 [L453] CALL     A=3 B=1 C=2 D=258 
00073 [L455] UGET     A=3 B=0 C=4 D=4 CCLayerColor
00074 [L455] MOV      A=4 B=0 C=3 D=3 
00075 [L455] TGETS    A=3 B=3 C=16 D=784 'create'
00076 [L455] UGET     A=5 B=0 C=5 D=5 ccc4
00077 [L455] KSHORT   A=6 B=0 C=0 D=0 0
00078 [L455] KSHORT   A=7 B=0 C=0 D=0 0
00079 [L455] KSHORT   A=8 B=0 C=0 D=0 0
00080 [L455] KSHORT   A=9 B=0 C=100 D=100 100
00081 [L455] CALL     A=5 B=0 C=5 D=5 
00082 [L455] CALLM    A=3 B=2 C=1 D=513 
00083 [L456] MOV      A=5 B=0 C=2 D=2 
00084 [L456] TGETS    A=4 B=2 C=19 D=531 'addChild'
00085 [L456] MOV      A=6 B=0 C=3 D=3 
00086 [L456] KSHORT   A=7 B=255 C=255 D=65535 -1
00087 [L456] CALL     A=4 B=1 C=4 D=260 
00088 [L458] GGET     A=4 B=0 C=5 D=5 'd_ms'
00089 [L458] TGETS    A=4 B=4 C=17 D=1041 'd_u'
00090 [L458] TGETS    A=4 B=4 C=20 D=1044 'createByStyle'
00091 [L458] TDUP     A=5 B=0 C=21 D=21 {'kind': 'table', 'value': {'pic': 'v2/batchBuyUI/frame.png', 'x': 0.5, 'y': 0.5}}
00092 [L458] CALL     A=4 B=2 C=2 D=514 
00093 [L459] MOV      A=6 B=0 C=2 D=2 
00094 [L459] TGETS    A=5 B=2 C=19 D=531 'addChild'
00095 [L459] MOV      A=7 B=0 C=4 D=4 
00096 [L459] CALL     A=5 B=1 C=3 D=259 
00097 [L460] GGET     A=5 B=0 C=5 D=5 'd_ms'
00098 [L460] TGETS    A=5 B=5 C=17 D=1297 'd_u'
00099 [L460] TGETS    A=5 B=5 C=22 D=1302 'getRealScale'
00100 [L460] MOV      A=6 B=0 C=4 D=4 
00101 [L460] CALL     A=5 B=3 C=2 D=770 
00102 [L462] GGET     A=7 B=0 C=5 D=5 'd_ms'
00103 [L462] TGETS    A=7 B=7 C=17 D=1809 'd_u'
00104 [L462] TGETS    A=7 B=7 C=20 D=1812 'createByStyle'
00105 [L462] TDUP     A=8 B=0 C=23 D=23 {'kind': 'table', 'value': {'pic': 'v2/checkinUI/tink.png', 'x': 0.5}}
00106 [L462] MULNV    A=9 B=6 C=1 D=1537 
00107 [L462] ADDNV    A=9 B=9 C=2 D=2306 
00108 [L462] TSETS    A=9 B=8 C=24 D=2072 'y'
00109 [L462] CALL     A=7 B=2 C=2 D=514 
00110 [L463] MOV      A=9 B=0 C=2 D=2 
00111 [L463] TGETS    A=8 B=2 C=19 D=531 'addChild'
00112 [L463] MOV      A=10 B=0 C=7 D=7 
00113 [L463] KSHORT   A=11 B=0 C=1 D=1 1
00114 [L463] CALL     A=8 B=1 C=4 D=260 
00115 [L465] GGET     A=8 B=0 C=5 D=5 'd_ms'
00116 [L465] TGETS    A=8 B=8 C=17 D=2065 'd_u'
00117 [L465] TGETS    A=8 B=8 C=25 D=2073 'createByStyles'
00118 [L465] TDUP     A=9 B=0 C=26 D=26 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 30}}
00119 [L465] GGET     A=10 B=0 C=5 D=5 'd_ms'
00120 [L465] TGETS    A=10 B=10 C=8 D=2568 'd_hz'
00121 [L465] TGETS    A=10 B=10 C=9 D=2569 'gethz'
00122 [L465] KSTR     A=11 B=0 C=27 D=27 'hunt4'
00123 [L465] CALL     A=10 B=2 C=2 D=514 
00124 [L465] TSETS    A=10 B=9 C=28 D=2332 'string'
00125 [L465] MULNV    A=10 B=5 C=3 D=1283 
00126 [L465] SUBNV    A=10 B=10 C=2 D=2562 
00127 [L465] TSETS    A=10 B=9 C=29 D=2333 'x'
00128 [L465] MULNV    A=10 B=6 C=4 D=1540 
00129 [L465] ADDNV    A=10 B=10 C=2 D=2562 
00130 [L465] TSETS    A=10 B=9 C=24 D=2328 'y'
00131 [L465] TDUP     A=10 B=0 C=30 D=30 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00132 [L465] TSETS    A=10 B=9 C=31 D=2335 'anchor'
00133 [L465] TDUP     A=10 B=0 C=32 D=32 {'kind': 'table', 'value': {1: 230, 2: 160, 3: 100}}
00134 [L465] TSETS    A=10 B=9 C=33 D=2337 'color'
00135 [L465] CALL     A=8 B=2 C=2 D=514 
00136 [L466] MOV      A=10 B=0 C=2 D=2 
00137 [L466] TGETS    A=9 B=2 C=19 D=531 'addChild'
00138 [L466] MOV      A=11 B=0 C=8 D=8 
00139 [L466] KSHORT   A=12 B=0 C=1 D=1 1
00140 [L466] CALL     A=9 B=1 C=4 D=260 
00141 [L468] GGET     A=9 B=0 C=5 D=5 'd_ms'
00142 [L468] TGETS    A=9 B=9 C=17 D=2321 'd_u'
00143 [L468] TGETS    A=9 B=9 C=25 D=2329 'createByStyles'
00144 [L468] TDUP     A=10 B=0 C=34 D=34 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 30}}
00145 [L468] GGET     A=11 B=0 C=5 D=5 'd_ms'
00146 [L468] TGETS    A=11 B=11 C=8 D=2824 'd_hz'
00147 [L468] TGETS    A=11 B=11 C=9 D=2825 'gethz'
00148 [L468] KSTR     A=12 B=0 C=35 D=35 'consumeHZ'
00149 [L468] CALL     A=11 B=2 C=2 D=514 
00150 [L468] GGET     A=12 B=0 C=5 D=5 'd_ms'
00151 [L468] TGETS    A=12 B=12 C=8 D=3080 'd_hz'
00152 [L468] TGETS    A=12 B=12 C=9 D=3081 'gethz'
00153 [L468] KSTR     A=13 B=0 C=36 D=36 'hunt1'
00154 [L468] CALL     A=12 B=2 C=2 D=514 
00155 [L468] KSTR     A=13 B=0 C=37 D=37 ': '
00156 [L468] CAT      A=11 B=11 C=13 D=2829 
00157 [L468] TSETS    A=11 B=10 C=28 D=2588 'string'
00158 [L468] MULNV    A=11 B=5 C=5 D=1285 
00159 [L468] ADDNV    A=11 B=11 C=2 D=2818 
00160 [L468] TSETS    A=11 B=10 C=29 D=2589 'x'
00161 [L468] MULNV    A=11 B=6 C=6 D=1542 
00162 [L468] SUBNV    A=11 B=11 C=2 D=2818 
00163 [L468] TSETS    A=11 B=10 C=24 D=2584 'y'
00164 [L468] TDUP     A=11 B=0 C=38 D=38 {'kind': 'table', 'value': {1: 1, 2: 0.5}}
00165 [L468] TSETS    A=11 B=10 C=31 D=2591 'anchor'
00166 [L468] TDUP     A=11 B=0 C=39 D=39 {'kind': 'table', 'value': {1: 230, 2: 160, 3: 100}}
00167 [L468] TSETS    A=11 B=10 C=33 D=2593 'color'
00168 [L468] CALL     A=9 B=2 C=2 D=514 
00169 [L469] MOV      A=11 B=0 C=2 D=2 
00170 [L469] TGETS    A=10 B=2 C=19 D=531 'addChild'
00171 [L469] MOV      A=12 B=0 C=9 D=9 
00172 [L469] KSHORT   A=13 B=0 C=1 D=1 1
00173 [L469] CALL     A=10 B=1 C=4 D=260 
00174 [L471] KSHORT   A=10 B=0 C=0 D=0 0
00175 [L472] UGET     A=11 B=0 C=1 D=1 g_self
00176 [L472] TGETS    A=11 B=11 C=1 D=2817 'hunt_const_config'
00177 [L472] TGETS    A=11 B=11 C=13 D=2829 'energy_exchange_rate'
00178 [L477] FNEW     A=12 B=0 C=40 D=40 {'kind': 'proto', 'id': 18}
00179 [L485] FNEW     A=13 B=0 C=41 D=41 {'kind': 'proto', 'id': 19}
00180 [L487] GGET     A=14 B=0 C=5 D=5 'd_ms'
00181 [L487] TGETS    A=14 B=14 C=42 D=3626 'd_guildPartyUI'
00182 [L487] TGETS    A=14 B=14 C=43 D=3627 'getCalc'
00183 [L487] MOV      A=15 B=0 C=13 D=13 
00184 [L487] MOV      A=16 B=0 C=0 D=0 
00185 [L487] CALL     A=14 B=2 C=3 D=515 
00186 [L488] GGET     A=15 B=0 C=5 D=5 'd_ms'
00187 [L488] TGETS    A=15 B=15 C=17 D=3857 'd_u'
00188 [L488] TGETS    A=15 B=15 C=44 D=3884 'setStyles'
00189 [L488] MOV      A=16 B=0 C=14 D=14 
00190 [L488] TDUP     A=17 B=0 C=45 D=45 {'kind': 'table', 'value': {'x': 0.5}}
00191 [L488] MULNV    A=18 B=6 C=7 D=1543 
00192 [L488] ADDNV    A=18 B=18 C=2 D=4610 
00193 [L488] TSETS    A=18 B=17 C=24 D=4376 'y'
00194 [L488] CALL     A=15 B=1 C=3 D=259 
00195 [L489] MOV      A=16 B=0 C=2 D=2 
00196 [L489] TGETS    A=15 B=2 C=19 D=531 'addChild'
00197 [L489] MOV      A=17 B=0 C=14 D=14 
00198 [L489] KSHORT   A=18 B=0 C=1 D=1 1
00199 [L489] CALL     A=15 B=1 C=4 D=260 
00200 [L490] MOV      A=15 B=0 C=13 D=13 
00201 [L490] KSHORT   A=16 B=0 C=1 D=1 1
00202 [L490] KSHORT   A=17 B=0 C=0 D=0 0
00203 [L490] CALL     A=15 B=1 C=3 D=259 
00204 [L497] FNEW     A=15 B=0 C=46 D=46 {'kind': 'proto', 'id': 20}
00205 [L499] TDUP     A=16 B=0 C=47 D=47 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00206 [L502] TDUP     A=17 B=0 C=48 D=48 {'kind': 'table', 'value': {'npic': 'v2/batchBuyUI/cancel1.png', 'spic': 'v2/batchBuyUI/cancel2.png', 'tag': 1}}
00207 [L503] MULNV    A=18 B=5 C=8 D=1288 
00208 [L503] SUBNV    A=18 B=18 C=2 D=4610 
00209 [L503] TSETS    A=18 B=17 C=29 D=4381 'x'
00210 [L503] MULNV    A=18 B=6 C=9 D=1545 
00211 [L503] SUBNV    A=18 B=18 C=2 D=4610 
00212 [L503] TSETS    A=18 B=17 C=24 D=4376 'y'
00213 [L503] TSETS    A=15 B=17 C=49 D=4401 'call_back'
00214 [L503] TSETB    A=17 B=16 C=1 D=4097 
00215 [L503] TDUP     A=17 B=0 C=50 D=50 {'kind': 'table', 'value': {'npic': 'v2/batchBuyUI/ensure1.png', 'spic': 'v2/batchBuyUI/ensure2.png', 'tag': 2}}
00216 [L504] MULNV    A=18 B=5 C=8 D=1288 
00217 [L504] ADDNV    A=18 B=18 C=2 D=4610 
00218 [L504] TSETS    A=18 B=17 C=29 D=4381 'x'
00219 [L504] MULNV    A=18 B=6 C=9 D=1545 
00220 [L504] SUBNV    A=18 B=18 C=2 D=4610 
00221 [L504] TSETS    A=18 B=17 C=24 D=4376 'y'
00222 [L504] TSETS    A=15 B=17 C=49 D=4401 'call_back'
00223 [L504] TSETB    A=17 B=16 C=2 D=4098 
00224 [L506] MOV      A=18 B=0 C=2 D=2 
00225 [L506] TGETS    A=17 B=2 C=19 D=531 'addChild'
00226 [L506] GGET     A=19 B=0 C=5 D=5 'd_ms'
00227 [L506] TGETS    A=19 B=19 C=17 D=4881 'd_u'
00228 [L506] TGETS    A=19 B=19 C=51 D=4915 'createMenu'
00229 [L506] MOV      A=20 B=0 C=16 D=16 
00230 [L506] CALL     A=19 B=2 C=2 D=514 
00231 [L506] KSHORT   A=20 B=0 C=5 D=5 5
00232 [L506] CALL     A=17 B=1 C=4 D=260 
00233 [L508] UGET     A=17 B=0 C=0 D=0 g_soulHuntUI
00234 [L508] TGETS    A=17 B=17 C=0 D=4352 'main_layer'
00235 [L508] MOV      A=18 B=0 C=17 D=17 
00236 [L508] TGETS    A=17 B=17 C=19 D=4371 'addChild'
00237 [L508] MOV      A=19 B=0 C=2 D=2 
00238 [L508] KSHORT   A=20 B=0 C=25 D=25 25
00239 [L508] CALL     A=17 B=1 C=4 D=260 
00240 [L509] UCLO     A=0 B=128 C=0 D=32768 target=241
00241 [L509] RET0     A=0 B=0 C=1 D=1 
00242 [L509] RET0     A=0 B=0 C=1 D=1 
00243 [L509] RET0     A=0 B=0 C=1 D=1 
00244 [L509] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto22 offset=0x385b source_lines=512-530 params=0
UPVALUES ['g_self', 'h_o_t', 'math']
00001 [L513] UGET     A=0 B=0 C=0 D=0 g_self
00002 [L513] TGETS    A=0 B=0 C=0 D=0 'ball'
00003 [L513] ISF      A=0 B=0 C=0 D=0 
00004 [L513] JMP      A=0 B=128 C=4 D=32772 target=9
00005 [L513] UGET     A=0 B=0 C=0 D=0 g_self
00006 [L513] TGETS    A=0 B=0 C=1 D=1 'degree'
00007 [L513] IST      A=0 B=0 C=0 D=0 
00008 [L513] JMP      A=0 B=128 C=1 D=32769 target=10
00009 [L514] RET0     A=0 B=0 C=1 D=1 
00010 [L516] UGET     A=0 B=0 C=0 D=0 g_self
00011 [L516] TGETS    A=0 B=0 C=2 D=2 'role_hunt_data'
00012 [L516] TGETS    A=0 B=0 C=3 D=3 'left_ball_times'
00013 [L516] ISNEN    A=0 B=0 C=0 D=0 0
00014 [L516] JMP      A=0 B=128 C=11 D=32779 target=26
00015 [L517] GGET     A=0 B=0 C=4 D=4 'd_ms'
00016 [L517] TGETS    A=0 B=0 C=5 D=5 'd_info'
00017 [L517] TGETS    A=0 B=0 C=6 D=6 'show'
00018 [L517] GGET     A=1 B=0 C=4 D=4 'd_ms'
00019 [L517] TGETS    A=1 B=1 C=7 D=263 'd_hz'
00020 [L517] TGETS    A=1 B=1 C=8 D=264 'gethz'
00021 [L517] KSTR     A=2 B=0 C=9 D=9 'hunt10'
00022 [L517] CALL     A=1 B=0 C=2 D=2 
00023 [L517] CALLM    A=0 B=1 C=0 D=256 
00024 [L518] RET0     A=0 B=0 C=1 D=1 
00025 [L518] JMP      A=0 B=128 C=21 D=32789 target=47
00026 [L519] UGET     A=0 B=0 C=0 D=0 g_self
00027 [L519] TGETS    A=0 B=0 C=10 D=10 'BallPrice'
00028 [L519] UGET     A=1 B=0 C=0 D=0 g_self
00029 [L519] TGETS    A=1 B=1 C=0 D=256 'ball'
00030 [L519] TGETV    A=0 B=0 C=1 D=1 
00031 [L519] TGETS    A=0 B=0 C=11 D=11 'need_energy'
00032 [L519] UGET     A=1 B=0 C=0 D=0 g_self
00033 [L519] TGETS    A=1 B=1 C=2 D=258 'role_hunt_data'
00034 [L519] TGETS    A=1 B=1 C=12 D=268 'left_energy'
00035 [L519] ISGE     A=1 B=0 C=0 D=0 
00036 [L519] JMP      A=0 B=128 C=10 D=32778 target=47
00037 [L520] GGET     A=0 B=0 C=4 D=4 'd_ms'
00038 [L520] TGETS    A=0 B=0 C=5 D=5 'd_info'
00039 [L520] TGETS    A=0 B=0 C=6 D=6 'show'
00040 [L520] GGET     A=1 B=0 C=4 D=4 'd_ms'
00041 [L520] TGETS    A=1 B=1 C=7 D=263 'd_hz'
00042 [L520] TGETS    A=1 B=1 C=8 D=264 'gethz'
00043 [L520] KSTR     A=2 B=0 C=13 D=13 'hunt9'
00044 [L520] CALL     A=1 B=0 C=2 D=2 
00045 [L520] CALLM    A=0 B=1 C=0 D=256 
00046 [L521] RET0     A=0 B=0 C=1 D=1 
00047 [L523] TNEW     A=0 B=0 C=0 D=0 
00048 [L524] UGET     A=1 B=0 C=1 D=1 h_o_t
00049 [L524] TGETS    A=1 B=1 C=15 D=271 'hit_ball'
00050 [L524] TSETS    A=1 B=0 C=14 D=14 'flag'
00051 [L525] UGET     A=1 B=0 C=0 D=0 g_self
00052 [L525] TGETS    A=1 B=1 C=0 D=256 'ball'
00053 [L525] TSETS    A=1 B=0 C=16 D=16 'count'
00054 [L526] UGET     A=1 B=0 C=2 D=2 math
00055 [L526] TGETS    A=1 B=1 C=17 D=273 'floor'
00056 [L526] UGET     A=2 B=0 C=0 D=0 g_self
00057 [L526] TGETS    A=2 B=2 C=1 D=513 'degree'
00058 [L526] CALL     A=1 B=2 C=2 D=514 
00059 [L527] ADDVN    A=2 B=1 C=1 D=257 
00060 [L527] UGET     A=3 B=0 C=0 D=0 g_self
00061 [L527] TGETS    A=3 B=3 C=1 D=769 'degree'
00062 [L527] ISGE     A=3 B=0 C=2 D=2 
00063 [L527] JMP      A=2 B=128 C=2 D=32770 target=66
00064 [L527] ISTC     A=2 B=0 C=1 D=1 
00065 [L527] JMP      A=2 B=128 C=1 D=32769 target=67
00066 [L527] ADDVN    A=2 B=1 C=2 D=258 
00067 [L527] TSETS    A=2 B=0 C=18 D=18 'index'
00068 [L529] GGET     A=2 B=0 C=4 D=4 'd_ms'
00069 [L529] TGETS    A=2 B=2 C=19 D=531 'd_u'
00070 [L529] TGETS    A=2 B=2 C=20 D=532 'main_server_send_msg'
00071 [L529] GGET     A=3 B=0 C=4 D=4 'd_ms'
00072 [L529] TGETS    A=3 B=3 C=21 D=789 'd_msg_def'
00073 [L529] TGETS    A=3 B=3 C=22 D=790 'gscl_msg_id'
00074 [L529] TGETS    A=3 B=3 C=23 D=791 'msg_hunt_soul'
00075 [L529] MOV      A=4 B=0 C=0 D=0 
00076 [L529] CALL     A=2 B=1 C=3 D=259 
00077 [L530] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto23 offset=0x3aef source_lines=533-548 params=0
UPVALUES ['g_soulHuntUI', 'tags', 'g_self', 'CCSprite']
00001 [L534] UGET     A=0 B=0 C=0 D=0 g_soulHuntUI
00002 [L534] TGETS    A=0 B=0 C=0 D=0 'main_layer'
00003 [L534] IST      A=0 B=0 C=0 D=0 
00004 [L534] JMP      A=0 B=128 C=1 D=32769 target=6
00005 [L535] RET0     A=0 B=0 C=1 D=1 
00006 [L537] UGET     A=0 B=0 C=0 D=0 g_soulHuntUI
00007 [L537] TGETS    A=0 B=0 C=0 D=0 'main_layer'
00008 [L537] MOV      A=1 B=0 C=0 D=0 
00009 [L537] TGETS    A=0 B=0 C=1 D=1 'removeChildByTag'
00010 [L537] UGET     A=2 B=0 C=1 D=1 tags
00011 [L537] TGETS    A=2 B=2 C=2 D=514 'Ball'
00012 [L537] KPRI     A=3 B=0 C=2 D=2 
00013 [L537] CALL     A=0 B=1 C=4 D=260 
00014 [L538] UGET     A=0 B=0 C=2 D=2 g_self
00015 [L538] TGETS    A=0 B=0 C=3 D=3 'ball'
00016 [L538] ISF      A=0 B=0 C=0 D=0 
00017 [L538] JMP      A=1 B=128 C=42 D=32810 target=60
00018 [L539] KPRI     A=0 B=0 C=0 D=0 
00019 [L540] UGET     A=1 B=0 C=2 D=2 g_self
00020 [L540] TGETS    A=1 B=1 C=4 D=260 'degree'
00021 [L540] ISF      A=0 B=0 C=1 D=1 
00022 [L540] JMP      A=2 B=128 C=11 D=32779 target=34
00023 [L541] UGET     A=1 B=0 C=3 D=3 CCSprite
00024 [L541] MOV      A=2 B=0 C=1 D=1 
00025 [L541] TGETS    A=1 B=1 C=5 D=261 'create'
00026 [L541] KSTR     A=3 B=0 C=6 D=6 'v2/soulHuntUI/ball'
00027 [L541] UGET     A=4 B=0 C=2 D=2 g_self
00028 [L541] TGETS    A=4 B=4 C=3 D=1027 'ball'
00029 [L541] KSTR     A=5 B=0 C=7 D=7 '2.png'
00030 [L541] CAT      A=3 B=3 C=5 D=773 
00031 [L541] CALL     A=1 B=2 C=3 D=515 
00032 [L541] MOV      A=0 B=0 C=1 D=1 
00033 [L541] JMP      A=1 B=128 C=10 D=32778 target=44
00034 [L543] UGET     A=1 B=0 C=3 D=3 CCSprite
00035 [L543] MOV      A=2 B=0 C=1 D=1 
00036 [L543] TGETS    A=1 B=1 C=5 D=261 'create'
00037 [L543] KSTR     A=3 B=0 C=6 D=6 'v2/soulHuntUI/ball'
00038 [L543] UGET     A=4 B=0 C=2 D=2 g_self
00039 [L543] TGETS    A=4 B=4 C=3 D=1027 'ball'
00040 [L543] KSTR     A=5 B=0 C=8 D=8 '1.png'
00041 [L543] CAT      A=3 B=3 C=5 D=773 
00042 [L543] CALL     A=1 B=2 C=3 D=515 
00043 [L543] MOV      A=0 B=0 C=1 D=1 
00044 [L545] MOV      A=2 B=0 C=0 D=0 
00045 [L545] TGETS    A=1 B=0 C=9 D=9 'setPosition'
00046 [L545] UGET     A=3 B=0 C=2 D=2 g_self
00047 [L545] TGETS    A=3 B=3 C=10 D=778 'cannon_x'
00048 [L545] UGET     A=4 B=0 C=2 D=2 g_self
00049 [L545] TGETS    A=4 B=4 C=11 D=1035 'cannon_y'
00050 [L545] CALL     A=1 B=1 C=4 D=260 
00051 [L546] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00052 [L546] TGETS    A=1 B=1 C=0 D=256 'main_layer'
00053 [L546] MOV      A=2 B=0 C=1 D=1 
00054 [L546] TGETS    A=1 B=1 C=12 D=268 'addChild'
00055 [L546] MOV      A=3 B=0 C=0 D=0 
00056 [L546] KSHORT   A=4 B=0 C=6 D=6 6
00057 [L546] UGET     A=5 B=0 C=1 D=1 tags
00058 [L546] TGETS    A=5 B=5 C=2 D=1282 'Ball'
00059 [L546] CALL     A=1 B=1 C=5 D=261 
00060 [L548] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto24 offset=0x3cd4 source_lines=550-558 params=1
UPVALUES ['pairs', 'g_self']
00001 [L551] UGET     A=1 B=0 C=0 D=0 pairs
00002 [L551] UGET     A=2 B=0 C=1 D=1 g_self
00003 [L551] TGETS    A=2 B=2 C=0 D=512 'role_hunt_data'
00004 [L551] TGETS    A=2 B=2 C=1 D=513 'point_list'
00005 [L551] CALL     A=1 B=4 C=2 D=1026 
00006 [L551] ISNEXT   A=4 B=128 C=29 D=32797 target=36
00007 [L552] TGETS    A=6 B=5 C=2 D=1282 'x'
00008 [L552] TGETS    A=7 B=0 C=2 D=2 'x'
00009 [L552] SUBVV    A=6 B=6 C=7 D=1543 
00010 [L552] KNUM     A=7 B=0 C=0 D=0 0.001
00011 [L552] ISGE     A=6 B=0 C=7 D=7 
00012 [L552] JMP      A=6 B=128 C=23 D=32791 target=36
00013 [L552] TGETS    A=6 B=5 C=2 D=1282 'x'
00014 [L552] TGETS    A=7 B=0 C=2 D=2 'x'
00015 [L552] SUBVV    A=6 B=6 C=7 D=1543 
00016 [L552] KNUM     A=7 B=0 C=1 D=1 -0.001
00017 [L552] ISGE     A=7 B=0 C=6 D=6 
00018 [L552] JMP      A=6 B=128 C=17 D=32785 target=36
00019 [L553] TGETS    A=6 B=5 C=3 D=1283 'y'
00020 [L553] TGETS    A=7 B=0 C=3 D=3 'y'
00021 [L553] SUBVV    A=6 B=6 C=7 D=1543 
00022 [L553] KNUM     A=7 B=0 C=0 D=0 0.001
00023 [L553] ISGE     A=6 B=0 C=7 D=7 
00024 [L553] JMP      A=6 B=128 C=11 D=32779 target=36
00025 [L553] TGETS    A=6 B=5 C=3 D=1283 'y'
00026 [L553] TGETS    A=7 B=0 C=3 D=3 'y'
00027 [L553] SUBVV    A=6 B=6 C=7 D=1543 
00028 [L553] KNUM     A=7 B=0 C=1 D=1 -0.001
00029 [L553] ISGE     A=7 B=0 C=6 D=6 
00030 [L553] JMP      A=6 B=128 C=5 D=32773 target=36
00031 [L554] TGETS    A=6 B=5 C=4 D=1284 'soul_type'
00032 [L554] TGETS    A=7 B=0 C=4 D=4 'soul_type'
00033 [L554] ISNEV    A=6 B=0 C=7 D=7 
00034 [L554] JMP      A=6 B=128 C=1 D=32769 target=36
00035 [L555] RET1     A=4 B=0 C=2 D=2 
00036 [L551] ITERN    A=4 B=3 C=3 D=771 
00037 [L551] ITERL    A=4 B=127 C=225 D=32737 target=7
00038 [L558] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto25 offset=0x3e05 source_lines=560-585 params=1
UPVALUES ['g_soulHuntUI', 'tags', 'g_self', 'getWorldPosition', 'CCArray', 'CCMoveBy', 'CCFadeOut', 'CCSequence', 'CCSpawn', 'CCCallFuncN']
00001 [L561] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00002 [L561] TGETS    A=1 B=1 C=0 D=256 'main_layer'
00003 [L561] IST      A=0 B=0 C=1 D=1 
00004 [L561] JMP      A=1 B=128 C=1 D=32769 target=6
00005 [L562] RET0     A=0 B=0 C=1 D=1 
00006 [L564] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00007 [L564] TGETS    A=1 B=1 C=0 D=256 'main_layer'
00008 [L564] MOV      A=2 B=0 C=1 D=1 
00009 [L564] TGETS    A=1 B=1 C=1 D=257 'getChildByTag'
00010 [L564] UGET     A=3 B=0 C=1 D=1 tags
00011 [L564] TGETS    A=3 B=3 C=2 D=770 'Soul'
00012 [L564] CALL     A=1 B=2 C=3 D=515 
00013 [L565] IST      A=0 B=0 C=1 D=1 
00014 [L565] JMP      A=2 B=128 C=1 D=32769 target=16
00015 [L566] RET0     A=0 B=0 C=1 D=1 
00016 [L568] UGET     A=2 B=0 C=2 D=2 g_self
00017 [L568] TGETS    A=2 B=2 C=3 D=515 'role_hunt_data'
00018 [L568] TGETS    A=2 B=2 C=4 D=516 'point_list'
00019 [L568] TGETV    A=2 B=2 C=0 D=512 
00020 [L569] MOV      A=4 B=0 C=1 D=1 
00021 [L569] TGETS    A=3 B=1 C=1 D=257 'getChildByTag'
00022 [L569] MOV      A=5 B=0 C=0 D=0 
00023 [L569] CALL     A=3 B=2 C=3 D=515 
00024 [L570] ISF      A=0 B=0 C=2 D=2 
00025 [L570] JMP      A=4 B=128 C=2 D=32770 target=28
00026 [L570] IST      A=0 B=0 C=3 D=3 
00027 [L570] JMP      A=4 B=128 C=1 D=32769 target=29
00028 [L571] RET0     A=0 B=0 C=1 D=1 
00029 [L573] MOV      A=5 B=0 C=1 D=1 
00030 [L573] TGETS    A=4 B=1 C=5 D=261 'removeChild'
00031 [L573] MOV      A=6 B=0 C=3 D=3 
00032 [L573] KPRI     A=7 B=0 C=2 D=2 
00033 [L573] CALL     A=4 B=1 C=4 D=260 
00034 [L574] UGET     A=4 B=0 C=2 D=2 g_self
00035 [L574] TGETS    A=4 B=4 C=6 D=1030 'SoulValue'
00036 [L574] TGETS    A=5 B=2 C=7 D=519 'soul_type'
00037 [L574] TGETV    A=4 B=4 C=5 D=1029 
00038 [L574] TGETS    A=4 B=4 C=8 D=1032 'soul_value'
00039 [L575] UGET     A=5 B=0 C=2 D=2 g_self
00040 [L575] UGET     A=6 B=0 C=2 D=2 g_self
00041 [L575] TGETS    A=6 B=6 C=9 D=1545 'last_soul_count'
00042 [L575] ADDVV    A=6 B=6 C=4 D=1540 
00043 [L575] TSETS    A=6 B=5 C=9 D=1289 'last_soul_count'
00044 [L576] GGET     A=5 B=0 C=10 D=10 'showSoulCount'
00045 [L576] UGET     A=6 B=0 C=2 D=2 g_self
00046 [L576] TGETS    A=6 B=6 C=9 D=1545 'last_soul_count'
00047 [L576] CALL     A=5 B=1 C=2 D=258 
00048 [L578] GGET     A=5 B=0 C=11 D=11 'd_ms'
00049 [L578] TGETS    A=5 B=5 C=12 D=1292 'd_u'
00050 [L578] TGETS    A=5 B=5 C=13 D=1293 'createByStyle'
00051 [L578] TDUP     A=6 B=0 C=14 D=14 {'kind': 'table', 'value': {'fontsize': 34, 'type': 'label'}}
00052 [L578] KSTR     A=7 B=0 C=15 D=15 '+'
00053 [L578] MOV      A=8 B=0 C=4 D=4 
00054 [L578] CAT      A=7 B=7 C=8 D=1800 
00055 [L578] TSETS    A=7 B=6 C=16 D=1552 'string'
00056 [L578] TDUP     A=7 B=0 C=17 D=17 {'kind': 'table', 'value': {1: 100, 2: 255, 3: 100}}
00057 [L578] TSETS    A=7 B=6 C=18 D=1554 'color'
00058 [L578] CALL     A=5 B=2 C=2 D=514 
00059 [L579] MOV      A=7 B=0 C=5 D=5 
00060 [L579] TGETS    A=6 B=5 C=19 D=1299 'setPosition'
00061 [L579] UGET     A=8 B=0 C=3 D=3 getWorldPosition
00062 [L579] TGETS    A=9 B=2 C=20 D=532 'x'
00063 [L579] TGETS    A=10 B=2 C=21 D=533 'y'
00064 [L579] CALL     A=8 B=0 C=3 D=3 
00065 [L579] CALLM    A=6 B=1 C=1 D=257 
00066 [L580] MOV      A=7 B=0 C=1 D=1 
00067 [L580] TGETS    A=6 B=1 C=22 D=278 'addChild'
00068 [L580] MOV      A=8 B=0 C=5 D=5 
00069 [L580] KSHORT   A=9 B=0 C=1 D=1 1
00070 [L580] CALL     A=6 B=1 C=4 D=260 
00071 [L581] UGET     A=6 B=0 C=4 D=4 CCArray
00072 [L581] MOV      A=7 B=0 C=6 D=6 
00073 [L581] TGETS    A=6 B=6 C=23 D=1559 'create'
00074 [L581] CALL     A=6 B=2 C=2 D=514 
00075 [L582] MOV      A=8 B=0 C=6 D=6 
00076 [L582] TGETS    A=7 B=6 C=24 D=1560 'addObject'
00077 [L582] UGET     A=9 B=0 C=5 D=5 CCMoveBy
00078 [L582] MOV      A=10 B=0 C=9 D=9 
00079 [L582] TGETS    A=9 B=9 C=23 D=2327 'create'
00080 [L582] KSHORT   A=11 B=0 C=1 D=1 1
00081 [L582] GGET     A=12 B=0 C=11 D=11 'd_ms'
00082 [L582] TGETS    A=12 B=12 C=12 D=3084 'd_u'
00083 [L582] TGETS    A=12 B=12 C=25 D=3097 'makePoint'
00084 [L582] KSHORT   A=13 B=0 C=0 D=0 0
00085 [L582] KNUM     A=14 B=0 C=0 D=0 0.03
00086 [L582] CALL     A=12 B=0 C=3 D=3 
00087 [L582] CALLM    A=9 B=0 C=2 D=2 
00088 [L582] CALLM    A=7 B=1 C=1 D=257 
00089 [L583] MOV      A=8 B=0 C=6 D=6 
00090 [L583] TGETS    A=7 B=6 C=24 D=1560 'addObject'
00091 [L583] UGET     A=9 B=0 C=6 D=6 CCFadeOut
00092 [L583] MOV      A=10 B=0 C=9 D=9 
00093 [L583] TGETS    A=9 B=9 C=23 D=2327 'create'
00094 [L583] KSHORT   A=11 B=0 C=1 D=1 1
00095 [L583] CALL     A=9 B=0 C=3 D=3 
00096 [L583] CALLM    A=7 B=1 C=1 D=257 
00097 [L584] MOV      A=8 B=0 C=5 D=5 
00098 [L584] TGETS    A=7 B=5 C=26 D=1306 'runAction'
00099 [L584] UGET     A=9 B=0 C=7 D=7 CCSequence
00100 [L584] MOV      A=10 B=0 C=9 D=9 
00101 [L584] TGETS    A=9 B=9 C=27 D=2331 'createWithTwoActions'
00102 [L584] UGET     A=11 B=0 C=8 D=8 CCSpawn
00103 [L584] MOV      A=12 B=0 C=11 D=11 
00104 [L584] TGETS    A=11 B=11 C=23 D=2839 'create'
00105 [L584] MOV      A=13 B=0 C=6 D=6 
00106 [L584] CALL     A=11 B=2 C=3 D=515 
00107 [L584] UGET     A=12 B=0 C=9 D=9 CCCallFuncN
00108 [L584] MOV      A=13 B=0 C=12 D=12 
00109 [L584] TGETS    A=12 B=12 C=23 D=3095 'create'
00110 [L584] GGET     A=14 B=0 C=11 D=11 'd_ms'
00111 [L584] TGETS    A=14 B=14 C=12 D=3596 'd_u'
00112 [L584] TGETS    A=14 B=14 C=28 D=3612 'remove'
00113 [L584] CALL     A=12 B=0 C=3 D=3 
00114 [L584] CALLM    A=9 B=0 C=2 D=2 
00115 [L584] CALLM    A=7 B=1 C=1 D=257 
00116 [L585] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto26 offset=0x4243 source_lines=588-601 params=1
UPVALUES ['math', 'cclog', 'pairs', 'g_self', 'table']
00001 [L589] TGETS    A=1 B=0 C=0 D=0 'move_path'
00002 [L590] KSHORT   A=2 B=0 C=2 D=2 2
00003 [L590] LEN      A=3 B=0 C=1 D=1 
00004 [L590] KSHORT   A=4 B=0 C=1 D=1 1
00005 [L590] FORI     A=2 B=128 C=62 D=32830 target=68
00006 [L591] SUBVN    A=6 B=5 C=0 D=1280 
00007 [L591] TGETV    A=6 B=1 C=6 D=262 
00008 [L591] TGETS    A=6 B=6 C=1 D=1537 'x'
00009 [L591] TGETV    A=7 B=1 C=5 D=261 
00010 [L591] TGETS    A=7 B=7 C=1 D=1793 'x'
00011 [L591] SUBVN    A=8 B=5 C=0 D=1280 
00012 [L591] TGETV    A=8 B=1 C=8 D=264 
00013 [L591] TGETS    A=8 B=8 C=2 D=2050 'y'
00014 [L591] TGETV    A=9 B=1 C=5 D=261 
00015 [L591] TGETS    A=9 B=9 C=2 D=2306 'y'
00016 [L592] TDUP     A=10 B=0 C=3 D=3 {'kind': 'table', 'value': {}}
00017 [L592] SUBVV    A=11 B=9 C=8 D=2312 
00018 [L592] TSETS    A=11 B=10 C=4 D=2564 'A'
00019 [L592] SUBVV    A=11 B=6 C=7 D=1543 
00020 [L592] TSETS    A=11 B=10 C=5 D=2565 'B'
00021 [L592] SUBVV    A=11 B=8 C=9 D=2057 
00022 [L592] MULVV    A=11 B=6 C=11 D=1547 
00023 [L592] SUBVV    A=12 B=7 C=6 D=1798 
00024 [L592] MULVV    A=12 B=8 C=12 D=2060 
00025 [L592] ADDVV    A=11 B=11 C=12 D=2828 
00026 [L592] TSETS    A=11 B=10 C=6 D=2566 'C'
00027 [L593] UGET     A=11 B=0 C=0 D=0 math
00028 [L593] TGETS    A=11 B=11 C=7 D=2823 'sqrt'
00029 [L593] TGETS    A=12 B=10 C=4 D=2564 'A'
00030 [L593] TGETS    A=13 B=10 C=4 D=2564 'A'
00031 [L593] MULVV    A=12 B=12 C=13 D=3085 
00032 [L593] TGETS    A=13 B=10 C=5 D=2565 'B'
00033 [L593] TGETS    A=14 B=10 C=5 D=2565 'B'
00034 [L593] MULVV    A=13 B=13 C=14 D=3342 
00035 [L593] ADDVV    A=12 B=12 C=13 D=3085 
00036 [L593] CALL     A=11 B=2 C=2 D=514 
00037 [L594] UGET     A=12 B=0 C=1 D=1 cclog
00038 [L594] KSTR     A=13 B=0 C=8 D=8 'ERROR: path'
00039 [L594] MOV      A=14 B=0 C=5 D=5 
00040 [L594] CAT      A=13 B=13 C=14 D=3342 
00041 [L594] CALL     A=12 B=1 C=2 D=258 
00042 [L595] UGET     A=12 B=0 C=2 D=2 pairs
00043 [L595] UGET     A=13 B=0 C=3 D=3 g_self
00044 [L595] TGETS    A=13 B=13 C=9 D=3337 'role_hunt_data'
00045 [L595] TGETS    A=13 B=13 C=10 D=3338 'point_list'
00046 [L595] CALL     A=12 B=4 C=2 D=1026 
00047 [L595] ISNEXT   A=15 B=128 C=17 D=32785 target=65
00048 [L596] TGETS    A=17 B=10 C=4 D=2564 'A'
00049 [L596] TGETS    A=18 B=16 C=1 D=4097 'x'
00050 [L596] MULVV    A=17 B=17 C=18 D=4370 
00051 [L596] TGETS    A=18 B=10 C=5 D=2565 'B'
00052 [L596] TGETS    A=19 B=16 C=2 D=4098 'y'
00053 [L596] MULVV    A=18 B=18 C=19 D=4627 
00054 [L596] ADDVV    A=17 B=17 C=18 D=4370 
00055 [L596] TGETS    A=18 B=10 C=6 D=2566 'C'
00056 [L596] ADDVV    A=17 B=17 C=18 D=4370 
00057 [L596] DIVVV    A=17 B=17 C=11 D=4363 
00058 [L597] UGET     A=18 B=0 C=1 D=1 cclog
00059 [L597] KSTR     A=19 B=0 C=11 D=11 '    ERROR: index = '
00060 [L597] MOV      A=20 B=0 C=15 D=15 
00061 [L597] KSTR     A=21 B=0 C=12 D=12 'distance='
00062 [L597] MOV      A=22 B=0 C=17 D=17 
00063 [L597] CAT      A=19 B=19 C=22 D=4886 
00064 [L597] CALL     A=18 B=1 C=2 D=258 
00065 [L595] ITERN    A=15 B=3 C=3 D=771 
00066 [L595] ITERL    A=15 B=127 C=237 D=32749 target=48
00067 [L590] FORL     A=2 B=127 C=194 D=32706 target=6
00068 [L600] UGET     A=2 B=0 C=1 D=1 cclog
00069 [L600] KSTR     A=3 B=0 C=13 D=13 'ERROR: result'
00070 [L600] UGET     A=4 B=0 C=4 D=4 table
00071 [L600] TGETS    A=4 B=4 C=14 D=1038 'tostring'
00072 [L600] MOV      A=5 B=0 C=1 D=1 
00073 [L600] CALL     A=4 B=2 C=2 D=514 
00074 [L600] CAT      A=3 B=3 C=4 D=772 
00075 [L600] CALL     A=2 B=1 C=2 D=258 
00076 [L601] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto27 offset=0x44cc source_lines=641-643 params=0
UPVALUES ['v']
00001 [L642] GGET     A=0 B=0 C=0 D=0 'soulAbsorb'
00002 [L642] UGET     A=1 B=0 C=0 D=0 v
00003 [L642] TGETS    A=1 B=1 C=1 D=257 'index'
00004 [L642] CALL     A=0 B=1 C=2 D=258 
00005 [L643] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto28 offset=0x4508 source_lines=649-675 params=0
UPVALUES ['g_soulHuntUI', 'ball', 'sLayer', 'g_self', 'pairs', 'soul_absorb_list', 'data_table', 'getWorldPosition', 'scrSize', 'CCArray', 'CCMoveBy', 'CCFadeOut', 'CCSequence', 'CCSpawn', 'CCCallFuncN']
00001 [L650] GGET     A=0 B=0 C=0 D=0 'showSoulCount'
00002 [L650] CALL     A=0 B=1 C=1 D=257 
00003 [L651] UGET     A=0 B=0 C=0 D=0 g_soulHuntUI
00004 [L651] TGETS    A=0 B=0 C=1 D=1 'main_layer'
00005 [L651] MOV      A=1 B=0 C=0 D=0 
00006 [L651] TGETS    A=0 B=0 C=2 D=2 'removeChild'
00007 [L651] UGET     A=2 B=0 C=1 D=1 ball
00008 [L651] KPRI     A=3 B=0 C=2 D=2 
00009 [L651] CALL     A=0 B=1 C=4 D=260 
00010 [L652] UGET     A=0 B=0 C=0 D=0 g_soulHuntUI
00011 [L652] TGETS    A=0 B=0 C=1 D=1 'main_layer'
00012 [L652] MOV      A=1 B=0 C=0 D=0 
00013 [L652] TGETS    A=0 B=0 C=2 D=2 'removeChild'
00014 [L652] UGET     A=2 B=0 C=2 D=2 sLayer
00015 [L652] KPRI     A=3 B=0 C=2 D=2 
00016 [L652] CALL     A=0 B=1 C=4 D=260 
00017 [L654] UGET     A=0 B=0 C=3 D=3 g_self
00018 [L654] TGETS    A=0 B=0 C=3 D=3 'new_point_list'
00019 [L654] ISF      A=0 B=0 C=0 D=0 
00020 [L654] JMP      A=1 B=128 C=9 D=32777 target=30
00021 [L655] UGET     A=0 B=0 C=3 D=3 g_self
00022 [L655] TGETS    A=0 B=0 C=4 D=4 'role_hunt_data'
00023 [L655] UGET     A=1 B=0 C=3 D=3 g_self
00024 [L655] TGETS    A=1 B=1 C=3 D=259 'new_point_list'
00025 [L655] TSETS    A=1 B=0 C=5 D=5 'point_list'
00026 [L656] GGET     A=0 B=0 C=6 D=6 'showSouls'
00027 [L656] KPRI     A=1 B=0 C=2 D=2 
00028 [L656] CALL     A=0 B=1 C=2 D=258 
00029 [L656] JMP      A=0 B=128 C=15 D=32783 target=45
00030 [L658] UGET     A=0 B=0 C=3 D=3 g_self
00031 [L658] TGETS    A=0 B=0 C=4 D=4 'role_hunt_data'
00032 [L658] TGETS    A=0 B=0 C=5 D=5 'point_list'
00033 [L659] UGET     A=1 B=0 C=4 D=4 pairs
00034 [L659] UGET     A=2 B=0 C=5 D=5 soul_absorb_list
00035 [L659] CALL     A=1 B=4 C=2 D=1026 
00036 [L659] ISNEXT   A=4 B=128 C=6 D=32774 target=43
00037 [L660] TGETS    A=6 B=5 C=7 D=1287 'index'
00038 [L660] ISF      A=0 B=0 C=6 D=6 
00039 [L660] JMP      A=7 B=128 C=3 D=32771 target=43
00040 [L661] TGETS    A=6 B=5 C=7 D=1287 'index'
00041 [L661] KPRI     A=7 B=0 C=0 D=0 
00042 [L661] TSETV    A=7 B=0 C=6 D=6 
00043 [L659] ITERN    A=4 B=3 C=3 D=771 
00044 [L659] ITERL    A=4 B=127 C=248 D=32760 target=37
00045 [L666] UGET     A=0 B=0 C=6 D=6 data_table
00046 [L666] TGETS    A=0 B=0 C=8 D=8 'extra_soul'
00047 [L666] ISF      A=0 B=0 C=0 D=0 
00048 [L666] JMP      A=1 B=128 C=86 D=32854 target=135
00049 [L666] UGET     A=0 B=0 C=6 D=6 data_table
00050 [L666] TGETS    A=0 B=0 C=8 D=8 'extra_soul'
00051 [L666] KSHORT   A=1 B=0 C=0 D=0 0
00052 [L666] ISGE     A=1 B=0 C=0 D=0 
00053 [L666] JMP      A=0 B=128 C=81 D=32849 target=135
00054 [L667] GGET     A=0 B=0 C=9 D=9 'd_ms'
00055 [L667] TGETS    A=0 B=0 C=10 D=10 'd_u'
00056 [L667] TGETS    A=0 B=0 C=11 D=11 'createByStyle'
00057 [L667] TDUP     A=1 B=0 C=12 D=12 {'kind': 'table', 'value': {'fontsize': 38, 'type': 'label'}}
00058 [L667] GGET     A=2 B=0 C=9 D=9 'd_ms'
00059 [L667] TGETS    A=2 B=2 C=13 D=525 'd_hz'
00060 [L667] TGETS    A=2 B=2 C=14 D=526 'gethz'
00061 [L667] KSTR     A=3 B=0 C=15 D=15 'hunt12'
00062 [L667] CALL     A=2 B=2 C=2 D=514 
00063 [L667] KSTR     A=3 B=0 C=16 D=16 ': +'
00064 [L667] UGET     A=4 B=0 C=6 D=6 data_table
00065 [L667] TGETS    A=4 B=4 C=8 D=1032 'extra_soul'
00066 [L667] CAT      A=2 B=2 C=4 D=516 
00067 [L667] TSETS    A=2 B=1 C=17 D=273 'string'
00068 [L667] TDUP     A=2 B=0 C=18 D=18 {'kind': 'table', 'value': {1: 100, 2: 255, 3: 100}}
00069 [L667] TSETS    A=2 B=1 C=19 D=275 'color'
00070 [L667] CALL     A=0 B=2 C=2 D=514 
00071 [L668] MOV      A=2 B=0 C=0 D=0 
00072 [L668] TGETS    A=1 B=0 C=20 D=20 'setPosition'
00073 [L668] UGET     A=3 B=0 C=7 D=7 getWorldPosition
00074 [L668] KSHORT   A=4 B=0 C=0 D=0 0
00075 [L668] UGET     A=5 B=0 C=3 D=3 g_self
00076 [L668] TGETS    A=5 B=5 C=21 D=1301 'h1'
00077 [L668] MULNV    A=5 B=5 C=0 D=1280 
00078 [L668] UGET     A=6 B=0 C=8 D=8 scrSize
00079 [L668] TGETS    A=6 B=6 C=22 D=1558 'height'
00080 [L668] MULVV    A=5 B=5 C=6 D=1286 
00081 [L668] CALL     A=3 B=0 C=3 D=3 
00082 [L668] CALLM    A=1 B=1 C=1 D=257 
00083 [L669] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00084 [L669] TGETS    A=1 B=1 C=1 D=257 'main_layer'
00085 [L669] MOV      A=2 B=0 C=1 D=1 
00086 [L669] TGETS    A=1 B=1 C=23 D=279 'addChild'
00087 [L669] MOV      A=3 B=0 C=0 D=0 
00088 [L669] KSHORT   A=4 B=0 C=1 D=1 1
00089 [L669] CALL     A=1 B=1 C=4 D=260 
00090 [L670] UGET     A=1 B=0 C=9 D=9 CCArray
00091 [L670] MOV      A=2 B=0 C=1 D=1 
00092 [L670] TGETS    A=1 B=1 C=24 D=280 'create'
00093 [L670] CALL     A=1 B=2 C=2 D=514 
00094 [L671] MOV      A=3 B=0 C=1 D=1 
00095 [L671] TGETS    A=2 B=1 C=25 D=281 'addObject'
00096 [L671] UGET     A=4 B=0 C=10 D=10 CCMoveBy
00097 [L671] MOV      A=5 B=0 C=4 D=4 
00098 [L671] TGETS    A=4 B=4 C=24 D=1048 'create'
00099 [L671] KSHORT   A=6 B=0 C=1 D=1 1
00100 [L671] GGET     A=7 B=0 C=9 D=9 'd_ms'
00101 [L671] TGETS    A=7 B=7 C=10 D=1802 'd_u'
00102 [L671] TGETS    A=7 B=7 C=26 D=1818 'makePoint'
00103 [L671] KSHORT   A=8 B=0 C=0 D=0 0
00104 [L671] KNUM     A=9 B=0 C=1 D=1 0.03
00105 [L671] CALL     A=7 B=0 C=3 D=3 
00106 [L671] CALLM    A=4 B=0 C=2 D=2 
00107 [L671] CALLM    A=2 B=1 C=1 D=257 
00108 [L672] MOV      A=3 B=0 C=1 D=1 
00109 [L672] TGETS    A=2 B=1 C=25 D=281 'addObject'
00110 [L672] UGET     A=4 B=0 C=11 D=11 CCFadeOut
00111 [L672] MOV      A=5 B=0 C=4 D=4 
00112 [L672] TGETS    A=4 B=4 C=24 D=1048 'create'
00113 [L672] KSHORT   A=6 B=0 C=1 D=1 1
00114 [L672] CALL     A=4 B=0 C=3 D=3 
00115 [L672] CALLM    A=2 B=1 C=1 D=257 
00116 [L673] MOV      A=3 B=0 C=0 D=0 
00117 [L673] TGETS    A=2 B=0 C=27 D=27 'runAction'
00118 [L673] UGET     A=4 B=0 C=12 D=12 CCSequence
00119 [L673] MOV      A=5 B=0 C=4 D=4 
00120 [L673] TGETS    A=4 B=4 C=28 D=1052 'createWithTwoActions'
00121 [L673] UGET     A=6 B=0 C=13 D=13 CCSpawn
00122 [L673] MOV      A=7 B=0 C=6 D=6 
00123 [L673] TGETS    A=6 B=6 C=24 D=1560 'create'
00124 [L673] MOV      A=8 B=0 C=1 D=1 
00125 [L673] CALL     A=6 B=2 C=3 D=515 
00126 [L673] UGET     A=7 B=0 C=14 D=14 CCCallFuncN
00127 [L673] MOV      A=8 B=0 C=7 D=7 
00128 [L673] TGETS    A=7 B=7 C=24 D=1816 'create'
00129 [L673] GGET     A=9 B=0 C=9 D=9 'd_ms'
00130 [L673] TGETS    A=9 B=9 C=10 D=2314 'd_u'
00131 [L673] TGETS    A=9 B=9 C=29 D=2333 'remove'
00132 [L673] CALL     A=7 B=0 C=3 D=3 
00133 [L673] CALLM    A=4 B=0 C=2 D=2 
00134 [L673] CALLM    A=2 B=1 C=1 D=257 
00135 [L675] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto29 offset=0x49d1 source_lines=604-680 params=1
UPVALUES ['g_soulHuntUI', 'g_self', 'CCSprite', 'CCArray', 'getWorldPosition', 'pairs', 'math', 'table', 'CCMoveBy', 'CCPointMake', 'cclog', 'scrSize', 'CCFadeOut', 'CCSequence', 'CCSpawn', 'CCCallFuncN', 'CCDelayTime']
00001 [L605] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00002 [L605] TGETS    A=1 B=1 C=0 D=256 'main_layer'
00003 [L605] ISF      A=0 B=0 C=1 D=1 
00004 [L605] JMP      A=1 B=128 C=4 D=32772 target=9
00005 [L605] UGET     A=1 B=0 C=1 D=1 g_self
00006 [L605] TGETS    A=1 B=1 C=1 D=257 'ball'
00007 [L605] IST      A=0 B=0 C=1 D=1 
00008 [L605] JMP      A=1 B=128 C=1 D=32769 target=10
00009 [L606] UCLO     A=0 B=128 C=180 D=32948 target=190
00010 [L608] GGET     A=1 B=0 C=2 D=2 'd_ms'
00011 [L608] TGETS    A=1 B=1 C=3 D=259 'd_u'
00012 [L608] TGETS    A=1 B=1 C=4 D=260 'createSwallowTouchLayer'
00013 [L608] UGET     A=2 B=0 C=0 D=0 g_soulHuntUI
00014 [L608] TGETS    A=2 B=2 C=0 D=512 'main_layer'
00015 [L608] CALL     A=1 B=2 C=2 D=514 
00016 [L609] UGET     A=2 B=0 C=2 D=2 CCSprite
00017 [L609] MOV      A=3 B=0 C=2 D=2 
00018 [L609] TGETS    A=2 B=2 C=5 D=517 'create'
00019 [L609] KSTR     A=4 B=0 C=6 D=6 'v2/soulHuntUI/ball'
00020 [L609] UGET     A=5 B=0 C=1 D=1 g_self
00021 [L609] TGETS    A=5 B=5 C=1 D=1281 'ball'
00022 [L609] KSTR     A=6 B=0 C=7 D=7 '1.png'
00023 [L609] CAT      A=4 B=4 C=6 D=1030 
00024 [L609] CALL     A=2 B=2 C=3 D=515 
00025 [L610] MOV      A=4 B=0 C=2 D=2 
00026 [L610] TGETS    A=3 B=2 C=8 D=520 'setPosition'
00027 [L610] UGET     A=5 B=0 C=1 D=1 g_self
00028 [L610] TGETS    A=5 B=5 C=9 D=1289 'cannon_x'
00029 [L610] UGET     A=6 B=0 C=1 D=1 g_self
00030 [L610] TGETS    A=6 B=6 C=10 D=1546 'cannon_y'
00031 [L610] CALL     A=3 B=1 C=4 D=260 
00032 [L611] UGET     A=3 B=0 C=0 D=0 g_soulHuntUI
00033 [L611] TGETS    A=3 B=3 C=0 D=768 'main_layer'
00034 [L611] MOV      A=4 B=0 C=3 D=3 
00035 [L611] TGETS    A=3 B=3 C=11 D=779 'addChild'
00036 [L611] MOV      A=5 B=0 C=2 D=2 
00037 [L611] KSHORT   A=6 B=0 C=2 D=2 2
00038 [L611] CALL     A=3 B=1 C=4 D=260 
00039 [L613] TGETS    A=3 B=0 C=12 D=12 'move_path'
00040 [L614] KNIL     A=4 B=0 C=6 D=6 
00041 [L615] TNEW     A=7 B=0 C=0 D=0 
00042 [L616] KSHORT   A=8 B=0 C=0 D=0 0
00043 [L617] UGET     A=9 B=0 C=3 D=3 CCArray
00044 [L617] MOV      A=10 B=0 C=9 D=9 
00045 [L617] TGETS    A=9 B=9 C=5 D=2309 'create'
00046 [L617] CALL     A=9 B=2 C=2 D=514 
00047 [L618] KSHORT   A=10 B=0 C=1 D=1 1
00048 [L618] LEN      A=11 B=0 C=3 D=3 
00049 [L618] KSHORT   A=12 B=0 C=1 D=1 1
00050 [L618] FORI     A=10 B=128 C=90 D=32858 target=141
00051 [L619] SUBVN    A=14 B=13 C=0 D=3328 
00052 [L619] TGETV    A=14 B=3 C=14 D=782 
00053 [L619] IST      A=0 B=0 C=14 D=14 
00054 [L619] JMP      A=14 B=128 C=10 D=32778 target=65
00055 [L620] MOV      A=15 B=0 C=2 D=2 
00056 [L620] TGETS    A=14 B=2 C=8 D=520 'setPosition'
00057 [L620] UGET     A=16 B=0 C=4 D=4 getWorldPosition
00058 [L620] TGETV    A=17 B=3 C=13 D=781 
00059 [L620] TGETS    A=17 B=17 C=13 D=4365 'x'
00060 [L620] TGETV    A=18 B=3 C=13 D=781 
00061 [L620] TGETS    A=18 B=18 C=14 D=4622 'y'
00062 [L620] CALL     A=16 B=0 C=3 D=3 
00063 [L620] CALLM    A=14 B=1 C=1 D=257 
00064 [L620] JMP      A=14 B=128 C=75 D=32843 target=140
00065 [L623] UGET     A=14 B=0 C=5 D=5 pairs
00066 [L623] TGETV    A=15 B=3 C=13 D=781 
00067 [L623] TGETS    A=15 B=15 C=15 D=3855 'soul_list'
00068 [L623] CALL     A=14 B=4 C=2 D=1026 
00069 [L623] ISNEXT   A=17 B=128 C=31 D=32799 target=101
00070 [L624] TGETS    A=19 B=18 C=13 D=4621 'x'
00071 [L624] SUBVN    A=20 B=13 C=0 D=3328 
00072 [L624] TGETV    A=20 B=3 C=20 D=788 
00073 [L624] TGETS    A=20 B=20 C=13 D=5133 'x'
00074 [L624] SUBVV    A=4 B=19 C=20 D=4884 
00075 [L625] TGETS    A=19 B=18 C=14 D=4622 'y'
00076 [L625] SUBVN    A=20 B=13 C=0 D=3328 
00077 [L625] TGETV    A=20 B=3 C=20 D=788 
00078 [L625] TGETS    A=20 B=20 C=14 D=5134 'y'
00079 [L625] SUBVV    A=5 B=19 C=20 D=4884 
00080 [L626] UGET     A=19 B=0 C=6 D=6 math
00081 [L626] TGETS    A=19 B=19 C=16 D=4880 'sqrt'
00082 [L626] MULVV    A=20 B=4 C=4 D=1028 
00083 [L626] MULVV    A=21 B=5 C=5 D=1285 
00084 [L626] ADDVV    A=20 B=20 C=21 D=5141 
00085 [L626] CALL     A=19 B=2 C=2 D=514 
00086 [L626] MOV      A=6 B=0 C=19 D=19 
00087 [L627] UGET     A=19 B=0 C=7 D=7 table
00088 [L627] TGETS    A=19 B=19 C=17 D=4881 'insert'
00089 [L627] MOV      A=20 B=0 C=7 D=7 
00090 [L627] TDUP     A=21 B=0 C=19 D=19 {'kind': 'table', 'value': {}}
00091 [L627] UGET     A=22 B=0 C=1 D=1 g_self
00092 [L627] TGETS    A=22 B=22 C=18 D=5650 'Speed'
00093 [L627] DIVVV    A=22 B=6 C=22 D=1558 
00094 [L627] ADDVV    A=22 B=8 C=22 D=2070 
00095 [L627] TSETS    A=22 B=21 C=20 D=5396 'dtime'
00096 [L627] GGET     A=22 B=0 C=21 D=21 'getSoulIndex'
00097 [L627] MOV      A=23 B=0 C=18 D=18 
00098 [L627] CALL     A=22 B=2 C=2 D=514 
00099 [L627] TSETS    A=22 B=21 C=22 D=5398 'index'
00100 [L627] CALL     A=19 B=1 C=3 D=259 
00101 [L623] ITERN    A=17 B=3 C=3 D=771 
00102 [L623] ITERL    A=17 B=127 C=223 D=32735 target=70
00103 [L630] TGETV    A=14 B=3 C=13 D=781 
00104 [L630] TGETS    A=14 B=14 C=13 D=3597 'x'
00105 [L630] SUBVN    A=15 B=13 C=0 D=3328 
00106 [L630] TGETV    A=15 B=3 C=15 D=783 
00107 [L630] TGETS    A=15 B=15 C=13 D=3853 'x'
00108 [L630] SUBVV    A=4 B=14 C=15 D=3599 
00109 [L631] TGETV    A=14 B=3 C=13 D=781 
00110 [L631] TGETS    A=14 B=14 C=14 D=3598 'y'
00111 [L631] SUBVN    A=15 B=13 C=0 D=3328 
00112 [L631] TGETV    A=15 B=3 C=15 D=783 
00113 [L631] TGETS    A=15 B=15 C=14 D=3854 'y'
00114 [L631] SUBVV    A=5 B=14 C=15 D=3599 
00115 [L632] UGET     A=14 B=0 C=6 D=6 math
00116 [L632] TGETS    A=14 B=14 C=16 D=3600 'sqrt'
00117 [L632] MULVV    A=15 B=4 C=4 D=1028 
00118 [L632] MULVV    A=16 B=5 C=5 D=1285 
00119 [L632] ADDVV    A=15 B=15 C=16 D=3856 
00120 [L632] CALL     A=14 B=2 C=2 D=514 
00121 [L632] MOV      A=6 B=0 C=14 D=14 
00122 [L633] MOV      A=15 B=0 C=9 D=9 
00123 [L633] TGETS    A=14 B=9 C=23 D=2327 'addObject'
00124 [L633] UGET     A=16 B=0 C=8 D=8 CCMoveBy
00125 [L633] MOV      A=17 B=0 C=16 D=16 
00126 [L633] TGETS    A=16 B=16 C=5 D=4101 'create'
00127 [L633] UGET     A=18 B=0 C=1 D=1 g_self
00128 [L633] TGETS    A=18 B=18 C=18 D=4626 'Speed'
00129 [L633] DIVVV    A=18 B=6 C=18 D=1554 
00130 [L633] UGET     A=19 B=0 C=9 D=9 CCPointMake
00131 [L633] MOV      A=20 B=0 C=4 D=4 
00132 [L633] MOV      A=21 B=0 C=5 D=5 
00133 [L633] CALL     A=19 B=0 C=3 D=3 
00134 [L633] CALLM    A=16 B=0 C=2 D=2 
00135 [L633] CALLM    A=14 B=1 C=1 D=257 
00136 [L635] UGET     A=14 B=0 C=1 D=1 g_self
00137 [L635] TGETS    A=14 B=14 C=18 D=3602 'Speed'
00138 [L635] DIVVV    A=14 B=6 C=14 D=1550 
00139 [L635] ADDVV    A=8 B=8 C=14 D=2062 
00140 [L618] FORL     A=10 B=127 C=166 D=32678 target=51
00141 [L639] UGET     A=10 B=0 C=5 D=5 pairs
00142 [L639] MOV      A=11 B=0 C=7 D=7 
00143 [L639] CALL     A=10 B=4 C=2 D=1026 
00144 [L639] ISNEXT   A=13 B=128 C=16 D=32784 target=161
00145 [L640] TGETS    A=15 B=14 C=22 D=3606 'index'
00146 [L640] ISF      A=0 B=0 C=15 D=15 
00147 [L640] JMP      A=16 B=128 C=9 D=32777 target=157
00148 [L643] FNEW     A=15 B=0 C=24 D=24 {'kind': 'proto', 'id': 27}
00149 [L644] GGET     A=16 B=0 C=2 D=2 'd_ms'
00150 [L644] TGETS    A=16 B=16 C=3 D=4099 'd_u'
00151 [L644] TGETS    A=16 B=16 C=25 D=4121 'delay'
00152 [L644] MOV      A=17 B=0 C=2 D=2 
00153 [L644] TGETS    A=18 B=14 C=20 D=3604 'dtime'
00154 [L644] MOV      A=19 B=0 C=15 D=15 
00155 [L644] CALL     A=16 B=1 C=4 D=260 
00156 [L644] JMP      A=15 B=128 C=3 D=32771 target=160
00157 [L646] UGET     A=15 B=0 C=10 D=10 cclog
00158 [L646] KSTR     A=16 B=0 C=26 D=26 'ERROR: an unknown ball'
00159 [L646] CALL     A=15 B=1 C=2 D=258 
00160 [L647] UCLO     A=13 B=128 C=0 D=32768 target=161
00161 [L639] ITERN    A=13 B=3 C=3 D=771 
00162 [L639] ITERL    A=13 B=127 C=238 D=32750 target=145
00163 [L675] FNEW     A=10 B=0 C=27 D=27 {'kind': 'proto', 'id': 28}
00164 [L677] MOV      A=12 B=0 C=9 D=9 
00165 [L677] TGETS    A=11 B=9 C=23 D=2327 'addObject'
00166 [L677] UGET     A=13 B=0 C=16 D=16 CCDelayTime
00167 [L677] MOV      A=14 B=0 C=13 D=13 
00168 [L677] TGETS    A=13 B=13 C=5 D=3333 'create'
00169 [L677] KNUM     A=15 B=0 C=1 D=1 0.05
00170 [L677] CALL     A=13 B=0 C=3 D=3 
00171 [L677] CALLM    A=11 B=1 C=1 D=257 
00172 [L678] MOV      A=12 B=0 C=9 D=9 
00173 [L678] TGETS    A=11 B=9 C=23 D=2327 'addObject'
00174 [L678] UGET     A=13 B=0 C=15 D=15 CCCallFuncN
00175 [L678] MOV      A=14 B=0 C=13 D=13 
00176 [L678] TGETS    A=13 B=13 C=5 D=3333 'create'
00177 [L678] MOV      A=15 B=0 C=10 D=10 
00178 [L678] CALL     A=13 B=0 C=3 D=3 
00179 [L678] CALLM    A=11 B=1 C=1 D=257 
00180 [L679] MOV      A=12 B=0 C=2 D=2 
00181 [L679] TGETS    A=11 B=2 C=28 D=540 'runAction'
00182 [L679] UGET     A=13 B=0 C=13 D=13 CCSequence
00183 [L679] MOV      A=14 B=0 C=13 D=13 
00184 [L679] TGETS    A=13 B=13 C=5 D=3333 'create'
00185 [L679] MOV      A=15 B=0 C=9 D=9 
00186 [L679] CALL     A=13 B=0 C=3 D=3 
00187 [L679] CALLM    A=11 B=1 C=1 D=257 
00188 [L680] UCLO     A=0 B=128 C=0 D=32768 target=189
00189 [L680] RET0     A=0 B=0 C=1 D=1 
00190 [L680] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto30 offset=0x4ffe source_lines=683-690 params=0
UPVALUES ['g_soulHuntUI', 'tags', 'tostring', 'g_self']
00001 [L684] UGET     A=0 B=0 C=0 D=0 g_soulHuntUI
00002 [L684] TGETS    A=0 B=0 C=0 D=0 'main_layer'
00003 [L684] IST      A=0 B=0 C=0 D=0 
00004 [L684] JMP      A=0 B=128 C=1 D=32769 target=6
00005 [L685] RET0     A=0 B=0 C=1 D=1 
00006 [L687] UGET     A=0 B=0 C=0 D=0 g_soulHuntUI
00007 [L687] TGETS    A=0 B=0 C=0 D=0 'main_layer'
00008 [L687] MOV      A=1 B=0 C=0 D=0 
00009 [L687] TGETS    A=0 B=0 C=1 D=1 'removeChildByTag'
00010 [L687] UGET     A=2 B=0 C=1 D=1 tags
00011 [L687] TGETS    A=2 B=2 C=2 D=514 'ShootTimes'
00012 [L687] KPRI     A=3 B=0 C=2 D=2 
00013 [L687] CALL     A=0 B=1 C=4 D=260 
00014 [L688] GGET     A=0 B=0 C=3 D=3 'd_ms'
00015 [L688] TGETS    A=0 B=0 C=4 D=4 'd_u'
00016 [L688] TGETS    A=0 B=0 C=5 D=5 'createByStyle'
00017 [L688] TDUP     A=1 B=0 C=6 D=6 {'kind': 'table', 'value': {'type': 'label', 'x': 0.74, 'fontsize': 30}}
00018 [L688] UGET     A=2 B=0 C=2 D=2 tostring
00019 [L688] UGET     A=3 B=0 C=3 D=3 g_self
00020 [L688] TGETS    A=3 B=3 C=7 D=775 'role_hunt_data'
00021 [L688] TGETS    A=3 B=3 C=8 D=776 'left_ball_times'
00022 [L688] CALL     A=2 B=2 C=2 D=514 
00023 [L688] TSETS    A=2 B=1 C=9 D=265 'string'
00024 [L688] UGET     A=2 B=0 C=3 D=3 g_self
00025 [L688] TGETS    A=2 B=2 C=10 D=522 'h2'
00026 [L688] MULNV    A=2 B=2 C=0 D=512 
00027 [L688] TSETS    A=2 B=1 C=11 D=267 'y'
00028 [L688] TDUP     A=2 B=0 C=12 D=12 {'kind': 'table', 'value': {1: 255, 2: 255, 3: 100}}
00029 [L688] TSETS    A=2 B=1 C=13 D=269 'color'
00030 [L688] CALL     A=0 B=2 C=2 D=514 
00031 [L689] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00032 [L689] TGETS    A=1 B=1 C=0 D=256 'main_layer'
00033 [L689] MOV      A=2 B=0 C=1 D=1 
00034 [L689] TGETS    A=1 B=1 C=14 D=270 'addChild'
00035 [L689] MOV      A=3 B=0 C=0 D=0 
00036 [L689] KSHORT   A=4 B=0 C=5 D=5 5
00037 [L689] UGET     A=5 B=0 C=1 D=1 tags
00038 [L689] TGETS    A=5 B=5 C=2 D=1282 'ShootTimes'
00039 [L689] CALL     A=1 B=1 C=5 D=261 
00040 [L690] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto31 offset=0x51bb source_lines=693-705 params=0
UPVALUES ['g_soulHuntUI', 'g_self', 'tags', 'tostring']
00001 [L694] UGET     A=0 B=0 C=0 D=0 g_soulHuntUI
00002 [L694] TGETS    A=0 B=0 C=0 D=0 'main_layer'
00003 [L694] IST      A=0 B=0 C=0 D=0 
00004 [L694] JMP      A=0 B=128 C=1 D=32769 target=6
00005 [L695] RET0     A=0 B=0 C=1 D=1 
00006 [L697] UGET     A=0 B=0 C=1 D=1 g_self
00007 [L697] TGETS    A=0 B=0 C=1 D=1 'role_hunt_data'
00008 [L697] TGETS    A=0 B=0 C=2 D=2 'left_flush_times'
00009 [L697] KSHORT   A=1 B=0 C=0 D=0 0
00010 [L697] ISGE     A=1 B=0 C=0 D=0 
00011 [L697] JMP      A=0 B=128 C=3 D=32771 target=15
00012 [L697] TDUP     A=0 B=0 C=3 D=3 {'kind': 'table', 'value': {1: 255, 2: 255, 3: 100}}
00013 [L697] IST      A=0 B=0 C=0 D=0 
00014 [L697] JMP      A=1 B=128 C=1 D=32769 target=16
00015 [L697] TDUP     A=0 B=0 C=4 D=4 {'kind': 'table', 'value': {1: 200, 2: 200, 3: 200}}
00016 [L698] UGET     A=1 B=0 C=1 D=1 g_self
00017 [L698] TGETS    A=1 B=1 C=1 D=257 'role_hunt_data'
00018 [L698] TGETS    A=1 B=1 C=2 D=258 'left_flush_times'
00019 [L698] ISNEN    A=1 B=0 C=0 D=0 0
00020 [L698] JMP      A=1 B=128 C=10 D=32778 target=31
00021 [L698] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00022 [L698] TGETS    A=1 B=1 C=5 D=261 'refreshBtn'
00023 [L698] ISF      A=0 B=0 C=1 D=1 
00024 [L698] JMP      A=2 B=128 C=6 D=32774 target=31
00025 [L699] GGET     A=1 B=0 C=6 D=6 'd_ms'
00026 [L699] TGETS    A=1 B=1 C=7 D=263 'd_u'
00027 [L699] TGETS    A=1 B=1 C=8 D=264 'grayMenuItem'
00028 [L699] UGET     A=2 B=0 C=0 D=0 g_soulHuntUI
00029 [L699] TGETS    A=2 B=2 C=5 D=517 'refreshBtn'
00030 [L699] CALL     A=1 B=1 C=2 D=258 
00031 [L701] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00032 [L701] TGETS    A=1 B=1 C=0 D=256 'main_layer'
00033 [L701] MOV      A=2 B=0 C=1 D=1 
00034 [L701] TGETS    A=1 B=1 C=9 D=265 'removeChildByTag'
00035 [L701] UGET     A=3 B=0 C=2 D=2 tags
00036 [L701] TGETS    A=3 B=3 C=10 D=778 'FreshTimes'
00037 [L701] KPRI     A=4 B=0 C=2 D=2 
00038 [L701] CALL     A=1 B=1 C=4 D=260 
00039 [L702] GGET     A=1 B=0 C=6 D=6 'd_ms'
00040 [L702] TGETS    A=1 B=1 C=7 D=263 'd_u'
00041 [L702] TGETS    A=1 B=1 C=11 D=267 'createByStyle'
00042 [L702] TDUP     A=2 B=0 C=12 D=12 {'kind': 'table', 'value': {'type': 'label', 'x': 0.94, 'fontsize': 30}}
00043 [L702] UGET     A=3 B=0 C=3 D=3 tostring
00044 [L702] UGET     A=4 B=0 C=1 D=1 g_self
00045 [L702] TGETS    A=4 B=4 C=1 D=1025 'role_hunt_data'
00046 [L702] TGETS    A=4 B=4 C=2 D=1026 'left_flush_times'
00047 [L702] CALL     A=3 B=2 C=2 D=514 
00048 [L702] TSETS    A=3 B=2 C=13 D=525 'string'
00049 [L702] UGET     A=3 B=0 C=1 D=1 g_self
00050 [L702] TGETS    A=3 B=3 C=14 D=782 'h2'
00051 [L702] MULNV    A=3 B=3 C=1 D=769 
00052 [L702] TSETS    A=3 B=2 C=15 D=527 'y'
00053 [L702] TSETS    A=0 B=2 C=16 D=528 'color'
00054 [L702] CALL     A=1 B=2 C=2 D=514 
00055 [L703] UGET     A=2 B=0 C=0 D=0 g_soulHuntUI
00056 [L703] TGETS    A=2 B=2 C=0 D=512 'main_layer'
00057 [L703] MOV      A=3 B=0 C=2 D=2 
00058 [L703] TGETS    A=2 B=2 C=17 D=529 'addChild'
00059 [L703] MOV      A=4 B=0 C=1 D=1 
00060 [L703] KSHORT   A=5 B=0 C=5 D=5 5
00061 [L703] UGET     A=6 B=0 C=2 D=2 tags
00062 [L703] TGETS    A=6 B=6 C=10 D=1546 'FreshTimes'
00063 [L703] CALL     A=2 B=1 C=5 D=261 
00064 [L705] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto32 offset=0x5423 source_lines=708-715 params=0
UPVALUES ['g_soulHuntUI', 'tags', 'tostring', 'g_self']
00001 [L709] UGET     A=0 B=0 C=0 D=0 g_soulHuntUI
00002 [L709] TGETS    A=0 B=0 C=0 D=0 'main_layer'
00003 [L709] IST      A=0 B=0 C=0 D=0 
00004 [L709] JMP      A=0 B=128 C=1 D=32769 target=6
00005 [L710] RET0     A=0 B=0 C=1 D=1 
00006 [L712] UGET     A=0 B=0 C=0 D=0 g_soulHuntUI
00007 [L712] TGETS    A=0 B=0 C=0 D=0 'main_layer'
00008 [L712] MOV      A=1 B=0 C=0 D=0 
00009 [L712] TGETS    A=0 B=0 C=1 D=1 'removeChildByTag'
00010 [L712] UGET     A=2 B=0 C=1 D=1 tags
00011 [L712] TGETS    A=2 B=2 C=2 D=514 'Energy'
00012 [L712] KPRI     A=3 B=0 C=2 D=2 
00013 [L712] CALL     A=0 B=1 C=4 D=260 
00014 [L713] GGET     A=0 B=0 C=3 D=3 'd_ms'
00015 [L713] TGETS    A=0 B=0 C=4 D=4 'd_u'
00016 [L713] TGETS    A=0 B=0 C=5 D=5 'createByStyle'
00017 [L713] TDUP     A=1 B=0 C=6 D=6 {'kind': 'table', 'value': {'type': 'label', 'x': 0.22, 'fontsize': 30}}
00018 [L713] UGET     A=2 B=0 C=2 D=2 tostring
00019 [L713] UGET     A=3 B=0 C=3 D=3 g_self
00020 [L713] TGETS    A=3 B=3 C=7 D=775 'role_hunt_data'
00021 [L713] TGETS    A=3 B=3 C=8 D=776 'left_energy'
00022 [L713] CALL     A=2 B=2 C=2 D=514 
00023 [L713] TSETS    A=2 B=1 C=9 D=265 'string'
00024 [L713] UGET     A=2 B=0 C=3 D=3 g_self
00025 [L713] TGETS    A=2 B=2 C=10 D=522 'h2'
00026 [L713] MULNV    A=2 B=2 C=0 D=512 
00027 [L713] TSETS    A=2 B=1 C=11 D=267 'y'
00028 [L713] TDUP     A=2 B=0 C=12 D=12 {'kind': 'table', 'value': {1: 255, 2: 255, 3: 100}}
00029 [L713] TSETS    A=2 B=1 C=13 D=269 'color'
00030 [L713] CALL     A=0 B=2 C=2 D=514 
00031 [L714] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00032 [L714] TGETS    A=1 B=1 C=0 D=256 'main_layer'
00033 [L714] MOV      A=2 B=0 C=1 D=1 
00034 [L714] TGETS    A=1 B=1 C=14 D=270 'addChild'
00035 [L714] MOV      A=3 B=0 C=0 D=0 
00036 [L714] KSHORT   A=4 B=0 C=5 D=5 5
00037 [L714] UGET     A=5 B=0 C=1 D=1 tags
00038 [L714] TGETS    A=5 B=5 C=2 D=1282 'Energy'
00039 [L714] CALL     A=1 B=1 C=5 D=261 
00040 [L715] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto33 offset=0x55d8 source_lines=718-727 params=1
UPVALUES ['g_soulHuntUI', 'tags', 'g_self']
00001 [L719] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00002 [L719] TGETS    A=1 B=1 C=0 D=256 'main_layer'
00003 [L719] IST      A=0 B=0 C=1 D=1 
00004 [L719] JMP      A=1 B=128 C=1 D=32769 target=6
00005 [L720] RET0     A=0 B=0 C=1 D=1 
00006 [L722] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00007 [L722] TGETS    A=1 B=1 C=0 D=256 'main_layer'
00008 [L722] MOV      A=2 B=0 C=1 D=1 
00009 [L722] TGETS    A=1 B=1 C=1 D=257 'removeChildByTag'
00010 [L722] UGET     A=3 B=0 C=1 D=1 tags
00011 [L722] TGETS    A=3 B=3 C=2 D=770 'SoulCount'
00012 [L722] KPRI     A=4 B=0 C=2 D=2 
00013 [L722] CALL     A=1 B=1 C=4 D=260 
00014 [L723] GGET     A=1 B=0 C=3 D=3 'd_ms'
00015 [L723] TGETS    A=1 B=1 C=4 D=260 'd_playerInfoUI'
00016 [L723] TGETS    A=1 B=1 C=5 D=261 'getNumNode'
00017 [L723] ISTC     A=2 B=0 C=0 D=0 
00018 [L723] JMP      A=2 B=128 C=3 D=32771 target=22
00019 [L723] UGET     A=2 B=0 C=2 D=2 g_self
00020 [L723] TGETS    A=2 B=2 C=6 D=518 'role_hunt_data'
00021 [L723] TGETS    A=2 B=2 C=7 D=519 'left_soul_count'
00022 [L723] CALL     A=1 B=2 C=2 D=514 
00023 [L724] MOV      A=3 B=0 C=1 D=1 
00024 [L724] TGETS    A=2 B=1 C=8 D=264 'setPosition'
00025 [L724] GGET     A=4 B=0 C=3 D=3 'd_ms'
00026 [L724] TGETS    A=4 B=4 C=9 D=1033 'd_u'
00027 [L724] TGETS    A=4 B=4 C=10 D=1034 'makePoint'
00028 [L724] KNUM     A=5 B=0 C=0 D=0 0.19
00029 [L724] UGET     A=6 B=0 C=2 D=2 g_self
00030 [L724] TGETS    A=6 B=6 C=11 D=1547 'top_y'
00031 [L724] CALL     A=4 B=0 C=3 D=3 
00032 [L724] CALLM    A=2 B=1 C=1 D=257 
00033 [L725] MOV      A=3 B=0 C=1 D=1 
00034 [L725] TGETS    A=2 B=1 C=12 D=268 'setScale'
00035 [L725] KNUM     A=4 B=0 C=1 D=1 0.65
00036 [L725] CALL     A=2 B=1 C=3 D=259 
00037 [L726] UGET     A=2 B=0 C=0 D=0 g_soulHuntUI
00038 [L726] TGETS    A=2 B=2 C=0 D=512 'main_layer'
00039 [L726] MOV      A=3 B=0 C=2 D=2 
00040 [L726] TGETS    A=2 B=2 C=13 D=525 'addChild'
00041 [L726] MOV      A=4 B=0 C=1 D=1 
00042 [L726] KSHORT   A=5 B=0 C=5 D=5 5
00043 [L726] UGET     A=6 B=0 C=1 D=1 tags
00044 [L726] TGETS    A=6 B=6 C=2 D=1538 'SoulCount'
00045 [L726] CALL     A=2 B=1 C=5 D=261 
00046 [L727] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto34 offset=0x57a8 source_lines=730-751 params=0
UPVALUES ['g_soulHuntUI', 'tags', 'g_self']
00001 [L731] UGET     A=0 B=0 C=0 D=0 g_soulHuntUI
00002 [L731] TGETS    A=0 B=0 C=0 D=0 'main_layer'
00003 [L731] IST      A=0 B=0 C=0 D=0 
00004 [L731] JMP      A=0 B=128 C=1 D=32769 target=6
00005 [L732] RET0     A=0 B=0 C=1 D=1 
00006 [L734] UGET     A=0 B=0 C=0 D=0 g_soulHuntUI
00007 [L734] TGETS    A=0 B=0 C=0 D=0 'main_layer'
00008 [L734] MOV      A=1 B=0 C=0 D=0 
00009 [L734] TGETS    A=0 B=0 C=1 D=1 'getChildByTag'
00010 [L734] UGET     A=2 B=0 C=1 D=1 tags
00011 [L734] TGETS    A=2 B=2 C=2 D=514 'Cannon'
00012 [L734] CALL     A=0 B=2 C=3 D=515 
00013 [L735] IST      A=0 B=0 C=0 D=0 
00014 [L735] JMP      A=1 B=128 C=24 D=32792 target=39
00015 [L736] GGET     A=1 B=0 C=3 D=3 'd_ms'
00016 [L736] TGETS    A=1 B=1 C=4 D=260 'd_u'
00017 [L736] TGETS    A=1 B=1 C=5 D=261 'createByStyles'
00018 [L736] TDUP     A=2 B=0 C=6 D=6 {'kind': 'table', 'value': {'pic': 'v2/soulHuntUI/cannon.png'}}
00019 [L736] TDUP     A=3 B=0 C=7 D=7 {'kind': 'table', 'value': {1: 0.5, 2: 0.4}}
00020 [L736] TSETS    A=3 B=2 C=8 D=520 'anchor'
00021 [L736] CALL     A=1 B=2 C=2 D=514 
00022 [L736] MOV      A=0 B=0 C=1 D=1 
00023 [L737] MOV      A=2 B=0 C=0 D=0 
00024 [L737] TGETS    A=1 B=0 C=9 D=9 'setPosition'
00025 [L737] UGET     A=3 B=0 C=2 D=2 g_self
00026 [L737] TGETS    A=3 B=3 C=10 D=778 'cannon_x'
00027 [L737] UGET     A=4 B=0 C=2 D=2 g_self
00028 [L737] TGETS    A=4 B=4 C=11 D=1035 'cannon_y'
00029 [L737] CALL     A=1 B=1 C=4 D=260 
00030 [L738] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00031 [L738] TGETS    A=1 B=1 C=0 D=256 'main_layer'
00032 [L738] MOV      A=2 B=0 C=1 D=1 
00033 [L738] TGETS    A=1 B=1 C=12 D=268 'addChild'
00034 [L738] MOV      A=3 B=0 C=0 D=0 
00035 [L738] KSHORT   A=4 B=0 C=3 D=3 3
00036 [L738] UGET     A=5 B=0 C=1 D=1 tags
00037 [L738] TGETS    A=5 B=5 C=2 D=1282 'Cannon'
00038 [L738] CALL     A=1 B=1 C=5 D=261 
00039 [L740] UGET     A=1 B=0 C=2 D=2 g_self
00040 [L740] TGETS    A=1 B=1 C=13 D=269 'degree'
00041 [L740] ISF      A=0 B=0 C=1 D=1 
00042 [L740] JMP      A=2 B=128 C=36 D=32804 target=79
00043 [L741] MOV      A=2 B=0 C=0 D=0 
00044 [L741] TGETS    A=1 B=0 C=14 D=14 'setRotation'
00045 [L741] UGET     A=3 B=0 C=2 D=2 g_self
00046 [L741] TGETS    A=3 B=3 C=13 D=781 'degree'
00047 [L741] SUBNV    A=3 B=3 C=0 D=768 
00048 [L741] CALL     A=1 B=1 C=3 D=259 
00049 [L743] MOV      A=2 B=0 C=0 D=0 
00050 [L743] TGETS    A=1 B=0 C=1 D=1 'getChildByTag'
00051 [L743] KSHORT   A=3 B=0 C=1 D=1 1
00052 [L743] CALL     A=1 B=2 C=3 D=515 
00053 [L744] IST      A=0 B=0 C=1 D=1 
00054 [L744] JMP      A=2 B=128 C=24 D=32792 target=79
00055 [L745] MOV      A=3 B=0 C=0 D=0 
00056 [L745] TGETS    A=2 B=0 C=15 D=15 'getContentSize'
00057 [L745] CALL     A=2 B=2 C=2 D=514 
00058 [L746] GGET     A=3 B=0 C=3 D=3 'd_ms'
00059 [L746] TGETS    A=3 B=3 C=4 D=772 'd_u'
00060 [L746] TGETS    A=3 B=3 C=5 D=773 'createByStyles'
00061 [L746] TDUP     A=4 B=0 C=16 D=16 {'kind': 'table', 'value': {'pic': 'v2/monthCard/line.png', 'rotation': 270}}
00062 [L746] TDUP     A=5 B=0 C=17 D=17 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00063 [L746] TSETS    A=5 B=4 C=8 D=1032 'anchor'
00064 [L746] CALL     A=3 B=2 C=2 D=514 
00065 [L746] MOV      A=1 B=0 C=3 D=3 
00066 [L747] MOV      A=4 B=0 C=1 D=1 
00067 [L747] TGETS    A=3 B=1 C=9 D=265 'setPosition'
00068 [L747] TGETS    A=5 B=2 C=18 D=530 'width'
00069 [L747] MULNV    A=5 B=5 C=1 D=1281 
00070 [L747] TGETS    A=6 B=2 C=19 D=531 'height'
00071 [L747] MULNV    A=6 B=6 C=2 D=1538 
00072 [L747] CALL     A=3 B=1 C=4 D=260 
00073 [L748] MOV      A=4 B=0 C=0 D=0 
00074 [L748] TGETS    A=3 B=0 C=12 D=12 'addChild'
00075 [L748] MOV      A=5 B=0 C=1 D=1 
00076 [L748] KSHORT   A=6 B=0 C=1 D=1 1
00077 [L748] KSHORT   A=7 B=0 C=1 D=1 1
00078 [L748] CALL     A=3 B=1 C=5 D=261 
00079 [L751] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto35 offset=0x5a8b source_lines=754-772 params=2
UPVALUES ['g_soulHuntUI', 'CCPointMake', 'g_self', 'math']
00001 [L755] UGET     A=2 B=0 C=0 D=0 g_soulHuntUI
00002 [L755] TGETS    A=2 B=2 C=0 D=512 'groundBound'
00003 [L755] IST      A=0 B=0 C=2 D=2 
00004 [L755] JMP      A=2 B=128 C=1 D=32769 target=6
00005 [L756] RET0     A=0 B=0 C=1 D=1 
00006 [L758] UGET     A=2 B=0 C=1 D=1 CCPointMake
00007 [L758] MOV      A=3 B=0 C=0 D=0 
00008 [L758] MOV      A=4 B=0 C=1 D=1 
00009 [L758] CALL     A=2 B=2 C=3 D=515 
00010 [L759] UGET     A=3 B=0 C=0 D=0 g_soulHuntUI
00011 [L759] TGETS    A=3 B=3 C=0 D=768 'groundBound'
00012 [L759] MOV      A=4 B=0 C=3 D=3 
00013 [L759] TGETS    A=3 B=3 C=1 D=769 'containsPoint'
00014 [L759] MOV      A=5 B=0 C=2 D=2 
00015 [L759] CALL     A=3 B=2 C=3 D=515 
00016 [L759] ISF      A=0 B=0 C=3 D=3 
00017 [L759] JMP      A=4 B=128 C=33 D=32801 target=51
00018 [L760] UGET     A=3 B=0 C=2 D=2 g_self
00019 [L760] TGETS    A=3 B=3 C=2 D=770 'cannon_x'
00020 [L760] SUBVV    A=3 B=0 C=3 D=3 
00021 [L760] UGET     A=4 B=0 C=2 D=2 g_self
00022 [L760] TGETS    A=4 B=4 C=3 D=1027 'cannon_y'
00023 [L760] SUBVV    A=4 B=1 C=4 D=260 
00024 [L761] KSHORT   A=5 B=0 C=0 D=0 0
00025 [L761] ISGT     A=4 B=0 C=5 D=5 
00026 [L761] JMP      A=5 B=128 C=1 D=32769 target=28
00027 [L762] RET0     A=0 B=0 C=1 D=1 
00028 [L764] UGET     A=5 B=0 C=3 D=3 math
00029 [L764] TGETS    A=5 B=5 C=4 D=1284 'deg'
00030 [L764] UGET     A=6 B=0 C=3 D=3 math
00031 [L764] TGETS    A=6 B=6 C=5 D=1541 'acos'
00032 [L764] UGET     A=7 B=0 C=3 D=3 math
00033 [L764] TGETS    A=7 B=7 C=6 D=1798 'sqrt'
00034 [L764] MULVV    A=8 B=3 C=3 D=771 
00035 [L764] MULVV    A=9 B=4 C=4 D=1028 
00036 [L764] ADDVV    A=8 B=8 C=9 D=2057 
00037 [L764] CALL     A=7 B=2 C=2 D=514 
00038 [L764] DIVVV    A=7 B=3 C=7 D=775 
00039 [L764] CALL     A=6 B=0 C=2 D=2 
00040 [L764] CALLM    A=5 B=2 C=0 D=512 
00041 [L765] KSHORT   A=6 B=0 C=30 D=30 30
00042 [L765] ISGE     A=5 B=0 C=6 D=6 
00043 [L765] JMP      A=6 B=128 C=2 D=32770 target=46
00044 [L766] KSHORT   A=5 B=0 C=30 D=30 30
00045 [L766] JMP      A=6 B=128 C=4 D=32772 target=50
00046 [L767] KSHORT   A=6 B=0 C=150 D=150 150
00047 [L767] ISGE     A=6 B=0 C=5 D=5 
00048 [L767] JMP      A=6 B=128 C=1 D=32769 target=50
00049 [L768] KSHORT   A=5 B=0 C=150 D=150 150
00050 [L770] RET1     A=5 B=0 C=2 D=2 
00051 [L772] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto36 offset=0x5c22 source_lines=774-787 params=2
UPVALUES ['g_soulHuntUI', 'g_self']
00001 [L775] UGET     A=2 B=0 C=0 D=0 g_soulHuntUI
00002 [L775] TGETS    A=2 B=2 C=0 D=512 'hasTouch'
00003 [L775] ISF      A=0 B=0 C=2 D=2 
00004 [L775] JMP      A=3 B=128 C=2 D=32770 target=7
00005 [L776] KPRI     A=2 B=0 C=1 D=1 
00006 [L776] RET1     A=2 B=0 C=2 D=2 
00007 [L778] GGET     A=2 B=0 C=1 D=1 'getDegree'
00008 [L778] MOV      A=3 B=0 C=0 D=0 
00009 [L778] MOV      A=4 B=0 C=1 D=1 
00010 [L778] CALL     A=2 B=2 C=3 D=515 
00011 [L779] ISF      A=0 B=0 C=2 D=2 
00012 [L779] JMP      A=3 B=128 C=11 D=32779 target=24
00013 [L780] UGET     A=3 B=0 C=1 D=1 g_self
00014 [L780] TSETS    A=2 B=3 C=2 D=770 'degree'
00015 [L781] GGET     A=3 B=0 C=3 D=3 'showCannon'
00016 [L781] CALL     A=3 B=1 C=1 D=257 
00017 [L782] GGET     A=3 B=0 C=4 D=4 'showBall'
00018 [L782] CALL     A=3 B=1 C=1 D=257 
00019 [L783] UGET     A=3 B=0 C=0 D=0 g_soulHuntUI
00020 [L783] KPRI     A=4 B=0 C=2 D=2 
00021 [L783] TSETS    A=4 B=3 C=0 D=768 'hasTouch'
00022 [L784] KPRI     A=3 B=0 C=2 D=2 
00023 [L784] RET1     A=3 B=0 C=2 D=2 
00024 [L786] KPRI     A=3 B=0 C=1 D=1 
00025 [L786] RET1     A=3 B=0 C=2 D=2 

FUNCTION proto37 offset=0x5d04 source_lines=789-797 params=2
UPVALUES ['g_self']
00001 [L790] GGET     A=2 B=0 C=0 D=0 'getDegree'
00002 [L790] MOV      A=3 B=0 C=0 D=0 
00003 [L790] MOV      A=4 B=0 C=1 D=1 
00004 [L790] CALL     A=2 B=2 C=3 D=515 
00005 [L791] ISF      A=0 B=0 C=2 D=2 
00006 [L791] JMP      A=3 B=128 C=6 D=32774 target=13
00007 [L792] UGET     A=3 B=0 C=0 D=0 g_self
00008 [L792] TSETS    A=2 B=3 C=1 D=769 'degree'
00009 [L793] GGET     A=3 B=0 C=2 D=2 'showCannon'
00010 [L793] CALL     A=3 B=1 C=1 D=257 
00011 [L794] KPRI     A=3 B=0 C=2 D=2 
00012 [L794] RET1     A=3 B=0 C=2 D=2 
00013 [L796] KPRI     A=3 B=0 C=1 D=1 
00014 [L796] RET1     A=3 B=0 C=2 D=2 

FUNCTION proto38 offset=0x5d8d source_lines=799-802 params=2
UPVALUES ['g_soulHuntUI']
00001 [L800] UGET     A=2 B=0 C=0 D=0 g_soulHuntUI
00002 [L800] KPRI     A=3 B=0 C=1 D=1 
00003 [L800] TSETS    A=3 B=2 C=0 D=512 'hasTouch'
00004 [L801] KPRI     A=2 B=0 C=2 D=2 
00005 [L801] RET1     A=2 B=0 C=2 D=2 

FUNCTION proto39 offset=0x5dd3 source_lines=804-807 params=2
UPVALUES ['g_soulHuntUI']
00001 [L805] UGET     A=2 B=0 C=0 D=0 g_soulHuntUI
00002 [L805] KPRI     A=3 B=0 C=1 D=1 
00003 [L805] TSETS    A=3 B=2 C=0 D=512 'hasTouch'
00004 [L806] KPRI     A=2 B=0 C=2 D=2 
00005 [L806] RET1     A=2 B=0 C=2 D=2 

FUNCTION proto40 offset=0x5e1a source_lines=809-819 params=3
UPVALUES ['CCTOUCHBEGAN', 'CCTOUCHMOVED', 'CCTOUCHENDED']
00001 [L810] UGET     A=3 B=0 C=0 D=0 CCTOUCHBEGAN
00002 [L810] ISNEV    A=0 B=0 C=3 D=3 
00003 [L810] JMP      A=3 B=128 C=5 D=32773 target=9
00004 [L811] GGET     A=3 B=0 C=0 D=0 'onTouchBegan'
00005 [L811] MOV      A=4 B=0 C=1 D=1 
00006 [L811] MOV      A=5 B=0 C=2 D=2 
00007 [L811] CALLT    A=3 B=0 C=3 D=3 
00008 [L811] JMP      A=3 B=128 C=20 D=32788 target=29
00009 [L812] UGET     A=3 B=0 C=1 D=1 CCTOUCHMOVED
00010 [L812] ISNEV    A=0 B=0 C=3 D=3 
00011 [L812] JMP      A=3 B=128 C=5 D=32773 target=17
00012 [L813] GGET     A=3 B=0 C=1 D=1 'onTouchMoved'
00013 [L813] MOV      A=4 B=0 C=1 D=1 
00014 [L813] MOV      A=5 B=0 C=2 D=2 
00015 [L813] CALLT    A=3 B=0 C=3 D=3 
00016 [L813] JMP      A=3 B=128 C=12 D=32780 target=29
00017 [L814] UGET     A=3 B=0 C=2 D=2 CCTOUCHENDED
00018 [L814] ISNEV    A=0 B=0 C=3 D=3 
00019 [L814] JMP      A=3 B=128 C=5 D=32773 target=25
00020 [L815] GGET     A=3 B=0 C=2 D=2 'onTouchEnded'
00021 [L815] MOV      A=4 B=0 C=1 D=1 
00022 [L815] MOV      A=5 B=0 C=2 D=2 
00023 [L815] CALLT    A=3 B=0 C=3 D=3 
00024 [L815] JMP      A=3 B=128 C=4 D=32772 target=29
00025 [L817] GGET     A=3 B=0 C=3 D=3 'onTouchCancel'
00026 [L817] MOV      A=4 B=0 C=1 D=1 
00027 [L817] MOV      A=5 B=0 C=2 D=2 
00028 [L817] CALLT    A=3 B=0 C=3 D=3 
00029 [L819] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto41 offset=0x5f2e source_lines=869-875 params=2
UPVALUES ['count', 'tip']
00001 [L870] USETV    A=0 B=0 C=0 D=0 count
00002 [L872] KSHORT   A=2 B=0 C=0 D=0 0
00003 [L872] ISGE     A=2 B=0 C=1 D=1 
00004 [L872] JMP      A=2 B=128 C=5 D=32773 target=10
00005 [L873] GGET     A=2 B=0 C=0 D=0 'd_ms'
00006 [L873] TGETS    A=2 B=2 C=1 D=513 'd_info'
00007 [L873] TGETS    A=2 B=2 C=2 D=514 'show'
00008 [L873] UGET     A=3 B=0 C=1 D=1 tip
00009 [L873] CALL     A=2 B=1 C=2 D=258 
00010 [L875] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto42 offset=0x5fa2 source_lines=882-887 params=1
UPVALUES ['layer', 'tag', 'count']
00001 [L883] GGET     A=1 B=0 C=0 D=0 'd_ms'
00002 [L883] TGETS    A=1 B=1 C=1 D=257 'd_u'
00003 [L883] TGETS    A=1 B=1 C=2 D=258 'remove'
00004 [L883] UGET     A=2 B=0 C=0 D=0 layer
00005 [L883] CALL     A=1 B=1 C=2 D=258 
00006 [L884] ISNEN    A=0 B=0 C=0 D=0 2
00007 [L884] JMP      A=1 B=128 C=4 D=32772 target=12
00008 [L885] GGET     A=1 B=0 C=3 D=3 'sendBuyItemRequest'
00009 [L885] UGET     A=2 B=0 C=1 D=1 tag
00010 [L885] UGET     A=3 B=0 C=2 D=2 count
00011 [L885] CALL     A=1 B=1 C=3 D=259 
00012 [L887] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto43 offset=0x602d source_lines=822-899 params=1
UPVALUES ['g_soulHuntUI', 'g_self', 'math', 'CCLayer', 'CCLayerColor', 'ccc4']
00001 [L823] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00002 [L823] TGETS    A=1 B=1 C=0 D=256 'main_layer'
00003 [L823] IST      A=0 B=0 C=1 D=1 
00004 [L823] JMP      A=1 B=128 C=1 D=32769 target=6
00005 [L824] UCLO     A=0 B=128 C=173 D=32941 target=179
00006 [L826] UGET     A=1 B=0 C=1 D=1 g_self
00007 [L826] TGETS    A=1 B=1 C=1 D=257 'store_data'
00008 [L826] TGETS    A=1 B=1 C=2 D=258 'item_list'
00009 [L826] TGETV    A=1 B=1 C=0 D=256 
00010 [L827] IST      A=0 B=0 C=1 D=1 
00011 [L827] JMP      A=2 B=128 C=1 D=32769 target=13
00012 [L828] UCLO     A=0 B=128 C=167 D=32935 target=180
00013 [L830] TGETS    A=2 B=1 C=3 D=259 'buy_times'
00014 [L830] ISNEN    A=2 B=0 C=0 D=0 0
00015 [L830] JMP      A=2 B=128 C=10 D=32778 target=26
00016 [L831] GGET     A=2 B=0 C=4 D=4 'd_ms'
00017 [L831] TGETS    A=2 B=2 C=5 D=517 'd_info'
00018 [L831] TGETS    A=2 B=2 C=6 D=518 'show'
00019 [L831] GGET     A=3 B=0 C=4 D=4 'd_ms'
00020 [L831] TGETS    A=3 B=3 C=7 D=775 'd_hz'
00021 [L831] TGETS    A=3 B=3 C=8 D=776 'gethz'
00022 [L831] KSTR     A=4 B=0 C=9 D=9 'richman5'
00023 [L831] CALL     A=3 B=0 C=2 D=2 
00024 [L831] CALLM    A=2 B=1 C=0 D=256 
00025 [L832] UCLO     A=0 B=128 C=155 D=32923 target=181
00026 [L834] UGET     A=2 B=0 C=2 D=2 math
00027 [L834] TGETS    A=2 B=2 C=10 D=522 'floor'
00028 [L834] UGET     A=3 B=0 C=1 D=1 g_self
00029 [L834] TGETS    A=3 B=3 C=11 D=779 'role_hunt_data'
00030 [L834] TGETS    A=3 B=3 C=12 D=780 'left_soul_count'
00031 [L834] TGETS    A=4 B=1 C=13 D=269 'need_soul'
00032 [L834] DIVVV    A=3 B=3 C=4 D=772 
00033 [L834] CALL     A=2 B=2 C=2 D=514 
00034 [L835] ISNEN    A=2 B=0 C=0 D=0 0
00035 [L835] JMP      A=3 B=128 C=10 D=32778 target=46
00036 [L836] GGET     A=3 B=0 C=4 D=4 'd_ms'
00037 [L836] TGETS    A=3 B=3 C=5 D=773 'd_info'
00038 [L836] TGETS    A=3 B=3 C=6 D=774 'show'
00039 [L836] GGET     A=4 B=0 C=4 D=4 'd_ms'
00040 [L836] TGETS    A=4 B=4 C=7 D=1031 'd_hz'
00041 [L836] TGETS    A=4 B=4 C=8 D=1032 'gethz'
00042 [L836] KSTR     A=5 B=0 C=14 D=14 'hunt5'
00043 [L836] CALL     A=4 B=0 C=2 D=2 
00044 [L836] CALLM    A=3 B=1 C=0 D=256 
00045 [L837] UCLO     A=0 B=128 C=136 D=32904 target=182
00046 [L839] KPRI     A=3 B=0 C=0 D=0 
00047 [L840] TGETS    A=4 B=1 C=3 D=259 'buy_times'
00048 [L840] ISGE     A=2 B=0 C=4 D=4 
00049 [L840] JMP      A=4 B=128 C=7 D=32775 target=57
00050 [L841] GGET     A=4 B=0 C=4 D=4 'd_ms'
00051 [L841] TGETS    A=4 B=4 C=7 D=1031 'd_hz'
00052 [L841] TGETS    A=4 B=4 C=8 D=1032 'gethz'
00053 [L841] KSTR     A=5 B=0 C=14 D=14 'hunt5'
00054 [L841] CALL     A=4 B=2 C=2 D=514 
00055 [L841] MOV      A=3 B=0 C=4 D=4 
00056 [L841] JMP      A=4 B=128 C=7 D=32775 target=64
00057 [L843] GGET     A=4 B=0 C=4 D=4 'd_ms'
00058 [L843] TGETS    A=4 B=4 C=7 D=1031 'd_hz'
00059 [L843] TGETS    A=4 B=4 C=8 D=1032 'gethz'
00060 [L843] KSTR     A=5 B=0 C=15 D=15 'hunt7'
00061 [L843] CALL     A=4 B=2 C=2 D=514 
00062 [L843] MOV      A=3 B=0 C=4 D=4 
00063 [L844] TGETS    A=2 B=1 C=3 D=259 'buy_times'
00064 [L847] UGET     A=4 B=0 C=3 D=3 CCLayer
00065 [L847] MOV      A=5 B=0 C=4 D=4 
00066 [L847] TGETS    A=4 B=4 C=16 D=1040 'create'
00067 [L847] CALL     A=4 B=2 C=2 D=514 
00068 [L848] GGET     A=5 B=0 C=4 D=4 'd_ms'
00069 [L848] TGETS    A=5 B=5 C=17 D=1297 'd_u'
00070 [L848] TGETS    A=5 B=5 C=18 D=1298 'createSwallowTouchLayer'
00071 [L848] MOV      A=6 B=0 C=4 D=4 
00072 [L848] CALL     A=5 B=1 C=2 D=258 
00073 [L850] UGET     A=5 B=0 C=4 D=4 CCLayerColor
00074 [L850] MOV      A=6 B=0 C=5 D=5 
00075 [L850] TGETS    A=5 B=5 C=16 D=1296 'create'
00076 [L850] UGET     A=7 B=0 C=5 D=5 ccc4
00077 [L850] KSHORT   A=8 B=0 C=0 D=0 0
00078 [L850] KSHORT   A=9 B=0 C=0 D=0 0
00079 [L850] KSHORT   A=10 B=0 C=0 D=0 0
00080 [L850] KSHORT   A=11 B=0 C=100 D=100 100
00081 [L850] CALL     A=7 B=0 C=5 D=5 
00082 [L850] CALLM    A=5 B=2 C=1 D=513 
00083 [L851] MOV      A=7 B=0 C=4 D=4 
00084 [L851] TGETS    A=6 B=4 C=19 D=1043 'addChild'
00085 [L851] MOV      A=8 B=0 C=5 D=5 
00086 [L851] KSHORT   A=9 B=255 C=255 D=65535 -1
00087 [L851] CALL     A=6 B=1 C=4 D=260 
00088 [L853] GGET     A=6 B=0 C=4 D=4 'd_ms'
00089 [L853] TGETS    A=6 B=6 C=17 D=1553 'd_u'
00090 [L853] TGETS    A=6 B=6 C=20 D=1556 'createByStyle'
00091 [L853] TDUP     A=7 B=0 C=21 D=21 {'kind': 'table', 'value': {'pic': 'v2/batchBuyUI/frame.png', 'x': 0.5, 'y': 0.5}}
00092 [L853] CALL     A=6 B=2 C=2 D=514 
00093 [L854] MOV      A=8 B=0 C=4 D=4 
00094 [L854] TGETS    A=7 B=4 C=19 D=1043 'addChild'
00095 [L854] MOV      A=9 B=0 C=6 D=6 
00096 [L854] CALL     A=7 B=1 C=3 D=259 
00097 [L855] GGET     A=7 B=0 C=4 D=4 'd_ms'
00098 [L855] TGETS    A=7 B=7 C=17 D=1809 'd_u'
00099 [L855] TGETS    A=7 B=7 C=22 D=1814 'getRealScale'
00100 [L855] MOV      A=8 B=0 C=6 D=6 
00101 [L855] CALL     A=7 B=3 C=2 D=770 
00102 [L857] GGET     A=9 B=0 C=4 D=4 'd_ms'
00103 [L857] TGETS    A=9 B=9 C=17 D=2321 'd_u'
00104 [L857] TGETS    A=9 B=9 C=20 D=2324 'createByStyle'
00105 [L857] TDUP     A=10 B=0 C=23 D=23 {'kind': 'table', 'value': {'pic': 'v2/checkinUI/tink.png', 'x': 0.5}}
00106 [L857] MULNV    A=11 B=8 C=1 D=2049 
00107 [L857] ADDNV    A=11 B=11 C=2 D=2818 
00108 [L857] TSETS    A=11 B=10 C=24 D=2584 'y'
00109 [L857] CALL     A=9 B=2 C=2 D=514 
00110 [L858] MOV      A=11 B=0 C=4 D=4 
00111 [L858] TGETS    A=10 B=4 C=19 D=1043 'addChild'
00112 [L858] MOV      A=12 B=0 C=9 D=9 
00113 [L858] KSHORT   A=13 B=0 C=1 D=1 1
00114 [L858] CALL     A=10 B=1 C=4 D=260 
00115 [L860] KSHORT   A=10 B=0 C=0 D=0 0
00116 [L875] FNEW     A=11 B=0 C=25 D=25 {'kind': 'proto', 'id': 41}
00117 [L877] GGET     A=12 B=0 C=4 D=4 'd_ms'
00118 [L877] TGETS    A=12 B=12 C=26 D=3098 'd_guildPartyUI'
00119 [L877] TGETS    A=12 B=12 C=27 D=3099 'getCalc'
00120 [L877] MOV      A=13 B=0 C=11 D=11 
00121 [L877] MOV      A=14 B=0 C=2 D=2 
00122 [L877] CALL     A=12 B=2 C=3 D=515 
00123 [L878] GGET     A=13 B=0 C=4 D=4 'd_ms'
00124 [L878] TGETS    A=13 B=13 C=17 D=3345 'd_u'
00125 [L878] TGETS    A=13 B=13 C=28 D=3356 'setStyles'
00126 [L878] MOV      A=14 B=0 C=12 D=12 
00127 [L878] TDUP     A=15 B=0 C=29 D=29 {'kind': 'table', 'value': {'x': 0.5}}
00128 [L878] MULNV    A=16 B=8 C=3 D=2051 
00129 [L878] ADDNV    A=16 B=16 C=2 D=4098 
00130 [L878] TSETS    A=16 B=15 C=24 D=3864 'y'
00131 [L878] CALL     A=13 B=1 C=3 D=259 
00132 [L879] MOV      A=14 B=0 C=4 D=4 
00133 [L879] TGETS    A=13 B=4 C=19 D=1043 'addChild'
00134 [L879] MOV      A=15 B=0 C=12 D=12 
00135 [L879] KSHORT   A=16 B=0 C=1 D=1 1
00136 [L879] CALL     A=13 B=1 C=4 D=260 
00137 [L880] MOV      A=13 B=0 C=11 D=11 
00138 [L880] KSHORT   A=14 B=0 C=1 D=1 1
00139 [L880] KSHORT   A=15 B=0 C=0 D=0 0
00140 [L880] CALL     A=13 B=1 C=3 D=259 
00141 [L887] FNEW     A=13 B=0 C=30 D=30 {'kind': 'proto', 'id': 42}
00142 [L889] TDUP     A=14 B=0 C=31 D=31 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00143 [L892] TDUP     A=15 B=0 C=32 D=32 {'kind': 'table', 'value': {'npic': 'v2/batchBuyUI/cancel1.png', 'spic': 'v2/batchBuyUI/cancel2.png', 'tag': 1}}
00144 [L893] MULNV    A=16 B=7 C=4 D=1796 
00145 [L893] SUBNV    A=16 B=16 C=2 D=4098 
00146 [L893] TSETS    A=16 B=15 C=33 D=3873 'x'
00147 [L893] MULNV    A=16 B=8 C=5 D=2053 
00148 [L893] SUBNV    A=16 B=16 C=2 D=4098 
00149 [L893] TSETS    A=16 B=15 C=24 D=3864 'y'
00150 [L893] TSETS    A=13 B=15 C=34 D=3874 'call_back'
00151 [L893] TSETB    A=15 B=14 C=1 D=3585 
00152 [L893] TDUP     A=15 B=0 C=35 D=35 {'kind': 'table', 'value': {'npic': 'v2/batchBuyUI/ensure1.png', 'spic': 'v2/batchBuyUI/ensure2.png', 'tag': 2}}
00153 [L894] MULNV    A=16 B=7 C=4 D=1796 
00154 [L894] ADDNV    A=16 B=16 C=2 D=4098 
00155 [L894] TSETS    A=16 B=15 C=33 D=3873 'x'
00156 [L894] MULNV    A=16 B=8 C=5 D=2053 
00157 [L894] SUBNV    A=16 B=16 C=2 D=4098 
00158 [L894] TSETS    A=16 B=15 C=24 D=3864 'y'
00159 [L894] TSETS    A=13 B=15 C=34 D=3874 'call_back'
00160 [L894] TSETB    A=15 B=14 C=2 D=3586 
00161 [L896] MOV      A=16 B=0 C=4 D=4 
00162 [L896] TGETS    A=15 B=4 C=19 D=1043 'addChild'
00163 [L896] GGET     A=17 B=0 C=4 D=4 'd_ms'
00164 [L896] TGETS    A=17 B=17 C=17 D=4369 'd_u'
00165 [L896] TGETS    A=17 B=17 C=36 D=4388 'createMenu'
00166 [L896] MOV      A=18 B=0 C=14 D=14 
00167 [L896] CALL     A=17 B=2 C=2 D=514 
00168 [L896] KSHORT   A=18 B=0 C=5 D=5 5
00169 [L896] CALL     A=15 B=1 C=4 D=260 
00170 [L898] UGET     A=15 B=0 C=0 D=0 g_soulHuntUI
00171 [L898] TGETS    A=15 B=15 C=0 D=3840 'main_layer'
00172 [L898] MOV      A=16 B=0 C=15 D=15 
00173 [L898] TGETS    A=15 B=15 C=19 D=3859 'addChild'
00174 [L898] MOV      A=17 B=0 C=4 D=4 
00175 [L898] KSHORT   A=18 B=0 C=25 D=25 25
00176 [L898] CALL     A=15 B=1 C=4 D=260 
00177 [L899] UCLO     A=0 B=128 C=0 D=32768 target=178
00178 [L899] RET0     A=0 B=0 C=1 D=1 
00179 [L899] RET0     A=0 B=0 C=1 D=1 
00180 [L899] RET0     A=0 B=0 C=1 D=1 
00181 [L899] RET0     A=0 B=0 C=1 D=1 
00182 [L899] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto44 offset=0x66bc source_lines=933-935 params=0
UPVALUES ['layer']
00001 [L934] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L934] TGETS    A=0 B=0 C=1 D=1 'd_u'
00003 [L934] TGETS    A=0 B=0 C=2 D=2 'remove'
00004 [L934] UGET     A=1 B=0 C=0 D=0 layer
00005 [L934] CALL     A=0 B=1 C=2 D=258 
00006 [L935] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto45 offset=0x6700 source_lines=936-942 params=0
UPVALUES ['g_self', 'own_soul']
00001 [L937] UGET     A=0 B=0 C=0 D=0 g_self
00002 [L937] TGETS    A=0 B=0 C=0 D=0 'store_data'
00003 [L937] TGETS    A=0 B=0 C=1 D=1 'flush_need_soul'
00004 [L937] UGET     A=1 B=0 C=1 D=1 own_soul
00005 [L937] ISGE     A=1 B=0 C=0 D=0 
00006 [L937] JMP      A=0 B=128 C=10 D=32778 target=17
00007 [L938] GGET     A=0 B=0 C=2 D=2 'd_ms'
00008 [L938] TGETS    A=0 B=0 C=3 D=3 'd_info'
00009 [L938] TGETS    A=0 B=0 C=4 D=4 'show'
00010 [L938] GGET     A=1 B=0 C=2 D=2 'd_ms'
00011 [L938] TGETS    A=1 B=1 C=5 D=261 'd_hz'
00012 [L938] TGETS    A=1 B=1 C=6 D=262 'gethz'
00013 [L938] KSTR     A=2 B=0 C=7 D=7 'hunt5'
00014 [L938] CALL     A=1 B=0 C=2 D=2 
00015 [L938] CALLM    A=0 B=1 C=0 D=256 
00016 [L938] JMP      A=0 B=128 C=2 D=32770 target=19
00017 [L940] GGET     A=0 B=0 C=8 D=8 'sendStoreFlushRequest'
00018 [L940] CALL     A=0 B=1 C=1 D=257 
00019 [L942] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto46 offset=0x67d4 source_lines=944-949 params=1
UPVALUES ['items', 'g_soulHuntUI']
00001 [L945] UGET     A=1 B=0 C=0 D=0 items
00002 [L945] TGETV    A=1 B=1 C=0 D=256 
00003 [L946] ISF      A=0 B=0 C=1 D=1 
00004 [L946] JMP      A=2 B=128 C=7 D=32775 target=12
00005 [L947] GGET     A=2 B=0 C=0 D=0 'd_ms'
00006 [L947] TGETS    A=2 B=2 C=1 D=513 'd_data'
00007 [L947] TGETS    A=2 B=2 C=2 D=514 'showItemIntro'
00008 [L947] UGET     A=3 B=0 C=1 D=1 g_soulHuntUI
00009 [L947] TGETS    A=3 B=3 C=3 D=771 'main_layer'
00010 [L947] MOV      A=4 B=0 C=1 D=1 
00011 [L947] CALL     A=2 B=1 C=3 D=259 
00012 [L949] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto47 offset=0x6867 source_lines=902-999 params=0
UPVALUES ['g_soulHuntUI', 'tags', 'g_self', 'tostring', 'math', 'table', 'pairs']
00001 [L903] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L903] TGETS    A=0 B=0 C=1 D=1 'd_u'
00003 [L903] TGETS    A=0 B=0 C=2 D=2 'clearLayer'
00004 [L903] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00005 [L903] TGETS    A=1 B=1 C=3 D=259 'main_layer'
00006 [L903] KSHORT   A=2 B=0 C=20 D=20 20
00007 [L903] UGET     A=3 B=0 C=1 D=1 tags
00008 [L903] TGETS    A=3 B=3 C=4 D=772 'Shop'
00009 [L903] CALL     A=0 B=2 C=4 D=516 
00010 [L904] IST      A=0 B=0 C=0 D=0 
00011 [L904] JMP      A=1 B=128 C=1 D=32769 target=13
00012 [L905] UCLO     A=0 B=129 C=75 D=33099 target=344
00013 [L907] GGET     A=1 B=0 C=0 D=0 'd_ms'
00014 [L907] TGETS    A=1 B=1 C=1 D=257 'd_u'
00015 [L907] TGETS    A=1 B=1 C=5 D=261 'createSwallowTouchLayer'
00016 [L907] MOV      A=2 B=0 C=0 D=0 
00017 [L907] CALL     A=1 B=1 C=2 D=258 
00018 [L909] GGET     A=1 B=0 C=0 D=0 'd_ms'
00019 [L909] TGETS    A=1 B=1 C=1 D=257 'd_u'
00020 [L909] TGETS    A=1 B=1 C=6 D=262 'createByStyle'
00021 [L909] TDUP     A=2 B=0 C=7 D=7 {'kind': 'table', 'value': {'pic': 'v2/soulHuntUI/bkg7.png', 'x': 0.5, 'y': 0.5}}
00022 [L909] CALL     A=1 B=2 C=2 D=514 
00023 [L910] MOV      A=3 B=0 C=0 D=0 
00024 [L910] TGETS    A=2 B=0 C=8 D=8 'addChild'
00025 [L910] MOV      A=4 B=0 C=1 D=1 
00026 [L910] CALL     A=2 B=1 C=3 D=259 
00027 [L911] GGET     A=2 B=0 C=0 D=0 'd_ms'
00028 [L911] TGETS    A=2 B=2 C=1 D=513 'd_u'
00029 [L911] TGETS    A=2 B=2 C=9 D=521 'getRealScale'
00030 [L911] MOV      A=3 B=0 C=1 D=1 
00031 [L911] CALL     A=2 B=3 C=2 D=770 
00032 [L913] GGET     A=4 B=0 C=0 D=0 'd_ms'
00033 [L913] TGETS    A=4 B=4 C=1 D=1025 'd_u'
00034 [L913] TGETS    A=4 B=4 C=6 D=1030 'createByStyle'
00035 [L913] TDUP     A=5 B=0 C=10 D=10 {'kind': 'table', 'value': {'pic': 'v2/soulHuntUI/title2.png', 'x': 0.5}}
00036 [L913] MULNV    A=6 B=3 C=0 D=768 
00037 [L913] ADDNV    A=6 B=6 C=1 D=1537 
00038 [L913] TSETS    A=6 B=5 C=11 D=1291 'y'
00039 [L913] CALL     A=4 B=2 C=2 D=514 
00040 [L914] MOV      A=6 B=0 C=0 D=0 
00041 [L914] TGETS    A=5 B=0 C=8 D=8 'addChild'
00042 [L914] MOV      A=7 B=0 C=4 D=4 
00043 [L914] KSHORT   A=8 B=0 C=1 D=1 1
00044 [L914] CALL     A=5 B=1 C=4 D=260 
00045 [L916] MULNV    A=5 B=3 C=2 D=770 
00046 [L916] SUBNV    A=5 B=5 C=1 D=1281 
00047 [L917] UGET     A=6 B=0 C=2 D=2 g_self
00048 [L917] TGETS    A=6 B=6 C=12 D=1548 'role_hunt_data'
00049 [L917] TGETS    A=6 B=6 C=13 D=1549 'left_soul_count'
00050 [L919] GGET     A=7 B=0 C=0 D=0 'd_ms'
00051 [L919] TGETS    A=7 B=7 C=14 D=1806 'd_hz'
00052 [L919] TGETS    A=7 B=7 C=15 D=1807 'gethz'
00053 [L919] KSTR     A=8 B=0 C=16 D=16 'currenGold'
00054 [L919] CALL     A=7 B=2 C=2 D=514 
00055 [L919] GGET     A=8 B=0 C=0 D=0 'd_ms'
00056 [L919] TGETS    A=8 B=8 C=14 D=2062 'd_hz'
00057 [L919] TGETS    A=8 B=8 C=15 D=2063 'gethz'
00058 [L919] KSTR     A=9 B=0 C=17 D=17 'hunt1'
00059 [L919] CALL     A=8 B=2 C=2 D=514 
00060 [L919] KSTR     A=9 B=0 C=18 D=18 ': '
00061 [L919] CAT      A=7 B=7 C=9 D=1801 
00062 [L920] GGET     A=8 B=0 C=0 D=0 'd_ms'
00063 [L920] TGETS    A=8 B=8 C=1 D=2049 'd_u'
00064 [L920] TGETS    A=8 B=8 C=6 D=2054 'createByStyle'
00065 [L920] TDUP     A=9 B=0 C=19 D=19 {'kind': 'table', 'value': {'type': 'label', 'fontsize': 30}}
00066 [L920] TSETS    A=7 B=9 C=20 D=2324 'string'
00067 [L920] MULNV    A=10 B=2 C=3 D=515 
00068 [L920] SUBNV    A=10 B=10 C=1 D=2561 
00069 [L920] TSETS    A=10 B=9 C=21 D=2325 'x'
00070 [L920] TSETS    A=5 B=9 C=11 D=2315 'y'
00071 [L920] TDUP     A=10 B=0 C=22 D=22 {'kind': 'table', 'value': {1: 1, 2: 0.5}}
00072 [L920] TSETS    A=10 B=9 C=23 D=2327 'anchor'
00073 [L920] TDUP     A=10 B=0 C=24 D=24 {'kind': 'table', 'value': {1: 255, 2: 255, 3: 100}}
00074 [L920] TSETS    A=10 B=9 C=25 D=2329 'color'
00075 [L920] CALL     A=8 B=2 C=2 D=514 
00076 [L921] MOV      A=10 B=0 C=0 D=0 
00077 [L921] TGETS    A=9 B=0 C=8 D=8 'addChild'
00078 [L921] MOV      A=11 B=0 C=8 D=8 
00079 [L921] KSHORT   A=12 B=0 C=1 D=1 1
00080 [L921] CALL     A=9 B=1 C=4 D=260 
00081 [L922] GGET     A=9 B=0 C=0 D=0 'd_ms'
00082 [L922] TGETS    A=9 B=9 C=1 D=2305 'd_u'
00083 [L922] TGETS    A=9 B=9 C=6 D=2310 'createByStyle'
00084 [L922] TDUP     A=10 B=0 C=26 D=26 {'kind': 'table', 'value': {'type': 'label', 'fontsize': 30}}
00085 [L922] UGET     A=11 B=0 C=3 D=3 tostring
00086 [L922] MOV      A=12 B=0 C=6 D=6 
00087 [L922] CALL     A=11 B=2 C=2 D=514 
00088 [L922] TSETS    A=11 B=10 C=20 D=2580 'string'
00089 [L922] MULNV    A=11 B=2 C=3 D=515 
00090 [L922] SUBNV    A=11 B=11 C=1 D=2817 
00091 [L922] TSETS    A=11 B=10 C=21 D=2581 'x'
00092 [L922] TSETS    A=5 B=10 C=11 D=2571 'y'
00093 [L922] TDUP     A=11 B=0 C=27 D=27 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00094 [L922] TSETS    A=11 B=10 C=23 D=2583 'anchor'
00095 [L922] CALL     A=9 B=2 C=2 D=514 
00096 [L923] MOV      A=11 B=0 C=0 D=0 
00097 [L923] TGETS    A=10 B=0 C=8 D=8 'addChild'
00098 [L923] MOV      A=12 B=0 C=9 D=9 
00099 [L923] KSHORT   A=13 B=0 C=1 D=1 1
00100 [L923] CALL     A=10 B=1 C=4 D=260 
00101 [L925] GGET     A=10 B=0 C=0 D=0 'd_ms'
00102 [L925] TGETS    A=10 B=10 C=1 D=2561 'd_u'
00103 [L925] TGETS    A=10 B=10 C=6 D=2566 'createByStyle'
00104 [L925] TDUP     A=11 B=0 C=28 D=28 {'kind': 'table', 'value': {'type': 'label', 'fontsize': 30}}
00105 [L925] GGET     A=12 B=0 C=0 D=0 'd_ms'
00106 [L925] TGETS    A=12 B=12 C=14 D=3086 'd_hz'
00107 [L925] TGETS    A=12 B=12 C=15 D=3087 'gethz'
00108 [L925] KSTR     A=13 B=0 C=29 D=29 'hunt6'
00109 [L925] CALL     A=12 B=2 C=2 D=514 
00110 [L925] TSETS    A=12 B=11 C=20 D=2836 'string'
00111 [L925] MULNV    A=12 B=2 C=4 D=516 
00112 [L925] ADDNV    A=12 B=12 C=1 D=3073 
00113 [L925] TSETS    A=12 B=11 C=21 D=2837 'x'
00114 [L925] TSETS    A=5 B=11 C=11 D=2827 'y'
00115 [L925] TDUP     A=12 B=0 C=30 D=30 {'kind': 'table', 'value': {1: 255, 2: 255, 3: 100}}
00116 [L925] TSETS    A=12 B=11 C=25 D=2841 'color'
00117 [L925] CALL     A=10 B=2 C=2 D=514 
00118 [L926] MOV      A=12 B=0 C=0 D=0 
00119 [L926] TGETS    A=11 B=0 C=8 D=8 'addChild'
00120 [L926] MOV      A=13 B=0 C=10 D=10 
00121 [L926] KSHORT   A=14 B=0 C=1 D=1 1
00122 [L926] CALL     A=11 B=1 C=4 D=260 
00123 [L931] UGET     A=11 B=0 C=2 D=2 g_self
00124 [L931] TGETS    A=11 B=11 C=31 D=2847 'store_data'
00125 [L931] TGETS    A=11 B=11 C=32 D=2848 'item_list'
00126 [L935] FNEW     A=12 B=0 C=33 D=33 {'kind': 'proto', 'id': 44}
00127 [L942] FNEW     A=13 B=0 C=34 D=34 {'kind': 'proto', 'id': 45}
00128 [L949] FNEW     A=14 B=0 C=35 D=35 {'kind': 'proto', 'id': 46}
00129 [L951] TDUP     A=15 B=0 C=36 D=36 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00130 [L954] TDUP     A=16 B=0 C=37 D=37 {'kind': 'table', 'value': {'npic': 'v2/introUI/close1.png', 'spic': 'v2/introUI/close2.png'}}
00131 [L955] MULNV    A=17 B=2 C=5 D=517 
00132 [L955] ADDNV    A=17 B=17 C=1 D=4353 
00133 [L955] TSETS    A=17 B=16 C=21 D=4117 'x'
00134 [L955] MULNV    A=17 B=3 C=0 D=768 
00135 [L955] ADDNV    A=17 B=17 C=1 D=4353 
00136 [L955] TSETS    A=17 B=16 C=11 D=4107 'y'
00137 [L955] TSETS    A=12 B=16 C=38 D=4134 'call_back'
00138 [L955] TSETB    A=16 B=15 C=1 D=3841 
00139 [L958] TDUP     A=16 B=0 C=39 D=39 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00140 [L963] KSHORT   A=17 B=0 C=1 D=1 1
00141 [L963] KSHORT   A=18 B=0 C=6 D=6 6
00142 [L963] KSHORT   A=19 B=0 C=1 D=1 1
00143 [L963] FORI     A=17 B=128 C=164 D=32932 target=308
00144 [L964] SUBVN    A=21 B=20 C=6 D=5126 
00145 [L964] MODVN    A=21 B=21 C=7 D=5383 
00146 [L964] ADDVN    A=21 B=21 C=6 D=5382 
00147 [L964] SUBVN    A=21 B=21 C=8 D=5384 
00148 [L964] MULVN    A=21 B=21 C=9 D=5385 
00149 [L964] MULVV    A=21 B=21 C=2 D=5378 
00150 [L964] ADDNV    A=21 B=21 C=1 D=5377 
00151 [L965] UGET     A=22 B=0 C=4 D=4 math
00152 [L965] TGETS    A=22 B=22 C=40 D=5672 'ceil'
00153 [L965] DIVVN    A=23 B=20 C=7 D=5127 
00154 [L965] CALL     A=22 B=2 C=2 D=514 
00155 [L965] SUBNV    A=22 B=22 C=10 D=5642 
00156 [L965] MULVN    A=22 B=22 C=3 D=5635 
00157 [L965] MULVV    A=22 B=22 C=3 D=5635 
00158 [L965] ADDNV    A=22 B=22 C=1 D=5633 
00159 [L967] MOV      A=24 B=0 C=0 D=0 
00160 [L967] TGETS    A=23 B=0 C=8 D=8 'addChild'
00161 [L967] GGET     A=25 B=0 C=0 D=0 'd_ms'
00162 [L967] TGETS    A=25 B=25 C=1 D=6401 'd_u'
00163 [L967] TGETS    A=25 B=25 C=6 D=6406 'createByStyle'
00164 [L967] TDUP     A=26 B=0 C=41 D=41 {'kind': 'table', 'value': {'pic': 'v2/soulHuntUI/shop_bkg.png'}}
00165 [L967] TSETS    A=21 B=26 C=21 D=6677 'x'
00166 [L967] TSETS    A=22 B=26 C=11 D=6667 'y'
00167 [L967] CALL     A=25 B=2 C=2 D=514 
00168 [L967] KSHORT   A=26 B=0 C=1 D=1 1
00169 [L967] CALL     A=23 B=1 C=4 D=260 
00170 [L968] TGETV    A=23 B=11 C=20 D=2836 
00171 [L968] ISF      A=0 B=0 C=23 D=23 
00172 [L968] JMP      A=24 B=128 C=134 D=32902 target=307
00173 [L969] TGETV    A=23 B=11 C=20 D=2836 
00174 [L970] GGET     A=24 B=0 C=0 D=0 'd_ms'
00175 [L970] TGETS    A=24 B=24 C=42 D=6186 'd_data'
00176 [L970] TGETS    A=24 B=24 C=43 D=6187 'getCertainInfo'
00177 [L970] TGETS    A=25 B=23 C=44 D=5932 'object_type'
00178 [L970] TGETS    A=26 B=23 C=45 D=5933 'attach_type'
00179 [L970] CALL     A=24 B=2 C=3 D=515 
00180 [L972] GGET     A=25 B=0 C=0 D=0 'd_ms'
00181 [L972] TGETS    A=25 B=25 C=42 D=6442 'd_data'
00182 [L972] TGETS    A=25 B=25 C=46 D=6446 'getCertainSmallSprite'
00183 [L972] TGETS    A=26 B=23 C=44 D=5932 'object_type'
00184 [L972] TGETS    A=27 B=23 C=45 D=5933 'attach_type'
00185 [L972] TGETS    A=28 B=23 C=47 D=5935 'attach_level'
00186 [L972] CALL     A=25 B=2 C=4 D=516 
00187 [L973] UGET     A=26 B=0 C=5 D=5 table
00188 [L973] TGETS    A=26 B=26 C=48 D=6704 'insert'
00189 [L973] MOV      A=27 B=0 C=15 D=15 
00190 [L973] TDUP     A=28 B=0 C=49 D=49 {'kind': 'table', 'value': {}}
00191 [L973] TSETS    A=25 B=28 C=50 D=7218 'nsprite'
00192 [L973] TSETS    A=25 B=28 C=51 D=7219 'ssprite'
00193 [L973] MULNV    A=29 B=2 C=11 D=523 
00194 [L973] SUBVV    A=29 B=21 C=29 D=5405 
00195 [L973] TSETS    A=29 B=28 C=21 D=7189 'x'
00196 [L973] MULNV    A=29 B=3 C=12 D=780 
00197 [L973] ADDVV    A=29 B=22 C=29 D=5661 
00198 [L973] TSETS    A=29 B=28 C=11 D=7179 'y'
00199 [L973] TSETS    A=20 B=28 C=52 D=7220 'tag'
00200 [L973] TSETS    A=14 B=28 C=38 D=7206 'call_back'
00201 [L973] CALL     A=26 B=1 C=3 D=259 
00202 [L975] TGETS    A=26 B=24 C=53 D=6197 'name'
00203 [L976] TGETS    A=27 B=23 C=54 D=5942 'attach_count'
00204 [L976] KSHORT   A=28 B=0 C=1 D=1 1
00205 [L976] ISGE     A=28 B=0 C=27 D=27 
00206 [L976] JMP      A=27 B=128 C=4 D=32772 target=211
00207 [L977] MOV      A=27 B=0 C=26 D=26 
00208 [L977] KSTR     A=28 B=0 C=55 D=55 'X'
00209 [L977] TGETS    A=29 B=23 C=54 D=5942 'attach_count'
00210 [L977] CAT      A=26 B=27 C=29 D=6941 
00211 [L979] GGET     A=27 B=0 C=0 D=0 'd_ms'
00212 [L979] TGETS    A=27 B=27 C=1 D=6913 'd_u'
00213 [L979] TGETS    A=27 B=27 C=6 D=6918 'createByStyle'
00214 [L979] TDUP     A=28 B=0 C=56 D=56 {'kind': 'table', 'value': {'type': 'label', 'fontsize': 26}}
00215 [L979] TSETS    A=26 B=28 C=20 D=7188 'string'
00216 [L979] MULNV    A=29 B=2 C=13 D=525 
00217 [L979] SUBVV    A=29 B=21 C=29 D=5405 
00218 [L979] TSETS    A=29 B=28 C=21 D=7189 'x'
00219 [L979] MULNV    A=29 B=3 C=14 D=782 
00220 [L979] ADDVV    A=29 B=22 C=29 D=5661 
00221 [L979] TSETS    A=29 B=28 C=11 D=7179 'y'
00222 [L979] TDUP     A=29 B=0 C=57 D=57 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00223 [L979] TSETS    A=29 B=28 C=23 D=7191 'anchor'
00224 [L979] TDUP     A=29 B=0 C=58 D=58 {'kind': 'table', 'value': {1: 255, 2: 255, 3: 100}}
00225 [L979] TSETS    A=29 B=28 C=25 D=7193 'color'
00226 [L979] CALL     A=27 B=2 C=2 D=514 
00227 [L980] MOV      A=29 B=0 C=0 D=0 
00228 [L980] TGETS    A=28 B=0 C=8 D=8 'addChild'
00229 [L980] MOV      A=30 B=0 C=27 D=27 
00230 [L980] KSHORT   A=31 B=0 C=1 D=1 1
00231 [L980] CALL     A=28 B=1 C=4 D=260 
00232 [L982] GGET     A=28 B=0 C=0 D=0 'd_ms'
00233 [L982] TGETS    A=28 B=28 C=1 D=7169 'd_u'
00234 [L982] TGETS    A=28 B=28 C=6 D=7174 'createByStyle'
00235 [L982] TDUP     A=29 B=0 C=59 D=59 {'kind': 'table', 'value': {'type': 'label', 'fontsize': 26}}
00236 [L982] GGET     A=30 B=0 C=0 D=0 'd_ms'
00237 [L982] TGETS    A=30 B=30 C=14 D=7694 'd_hz'
00238 [L982] TGETS    A=30 B=30 C=15 D=7695 'gethz'
00239 [L982] KSTR     A=31 B=0 C=60 D=60 'hunt15'
00240 [L982] CALL     A=30 B=2 C=2 D=514 
00241 [L982] KSTR     A=31 B=0 C=18 D=18 ': '
00242 [L982] TGETS    A=32 B=23 C=61 D=5949 'buy_times'
00243 [L982] GGET     A=33 B=0 C=0 D=0 'd_ms'
00244 [L982] TGETS    A=33 B=33 C=14 D=8462 'd_hz'
00245 [L982] TGETS    A=33 B=33 C=15 D=8463 'gethz'
00246 [L982] KSTR     A=34 B=0 C=62 D=62 'lunHZ'
00247 [L982] CALL     A=33 B=2 C=2 D=514 
00248 [L982] CAT      A=30 B=30 C=33 D=7713 
00249 [L982] TSETS    A=30 B=29 C=20 D=7444 'string'
00250 [L982] MULNV    A=30 B=2 C=13 D=525 
00251 [L982] SUBVV    A=30 B=21 C=30 D=5406 
00252 [L982] TSETS    A=30 B=29 C=21 D=7445 'x'
00253 [L982] MULNV    A=30 B=3 C=12 D=780 
00254 [L982] ADDVV    A=30 B=22 C=30 D=5662 
00255 [L982] TSETS    A=30 B=29 C=11 D=7435 'y'
00256 [L982] TDUP     A=30 B=0 C=63 D=63 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00257 [L982] TSETS    A=30 B=29 C=23 D=7447 'anchor'
00258 [L982] TDUP     A=30 B=0 C=64 D=64 {'kind': 'table', 'value': {1: 150, 2: 150, 3: 150}}
00259 [L982] TSETS    A=30 B=29 C=25 D=7449 'color'
00260 [L982] CALL     A=28 B=2 C=2 D=514 
00261 [L983] MOV      A=30 B=0 C=0 D=0 
00262 [L983] TGETS    A=29 B=0 C=8 D=8 'addChild'
00263 [L983] MOV      A=31 B=0 C=28 D=28 
00264 [L983] KSHORT   A=32 B=0 C=1 D=1 1
00265 [L983] CALL     A=29 B=1 C=4 D=260 
00266 [L985] GGET     A=29 B=0 C=0 D=0 'd_ms'
00267 [L985] TGETS    A=29 B=29 C=1 D=7425 'd_u'
00268 [L985] TGETS    A=29 B=29 C=6 D=7430 'createByStyle'
00269 [L985] TDUP     A=30 B=0 C=65 D=65 {'kind': 'table', 'value': {'type': 'label', 'fontsize': 26}}
00270 [L985] GGET     A=31 B=0 C=0 D=0 'd_ms'
00271 [L985] TGETS    A=31 B=31 C=14 D=7950 'd_hz'
00272 [L985] TGETS    A=31 B=31 C=15 D=7951 'gethz'
00273 [L985] KSTR     A=32 B=0 C=66 D=66 'hunt16'
00274 [L985] CALL     A=31 B=2 C=2 D=514 
00275 [L985] KSTR     A=32 B=0 C=18 D=18 ': '
00276 [L985] TGETS    A=33 B=23 C=67 D=5955 'need_soul'
00277 [L985] CAT      A=31 B=31 C=33 D=7969 
00278 [L985] TSETS    A=31 B=30 C=20 D=7700 'string'
00279 [L985] MULNV    A=31 B=2 C=13 D=525 
00280 [L985] SUBVV    A=31 B=21 C=31 D=5407 
00281 [L985] TSETS    A=31 B=30 C=21 D=7701 'x'
00282 [L985] MULNV    A=31 B=3 C=15 D=783 
00283 [L985] ADDVV    A=31 B=22 C=31 D=5663 
00284 [L985] TSETS    A=31 B=30 C=11 D=7691 'y'
00285 [L985] TDUP     A=31 B=0 C=68 D=68 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00286 [L985] TSETS    A=31 B=30 C=23 D=7703 'anchor'
00287 [L985] TDUP     A=31 B=0 C=69 D=69 {'kind': 'table', 'value': {1: 150, 2: 150, 3: 150}}
00288 [L985] TSETS    A=31 B=30 C=25 D=7705 'color'
00289 [L985] CALL     A=29 B=2 C=2 D=514 
00290 [L986] MOV      A=31 B=0 C=0 D=0 
00291 [L986] TGETS    A=30 B=0 C=8 D=8 'addChild'
00292 [L986] MOV      A=32 B=0 C=29 D=29 
00293 [L986] KSHORT   A=33 B=0 C=1 D=1 1
00294 [L986] CALL     A=30 B=1 C=4 D=260 
00295 [L988] UGET     A=30 B=0 C=5 D=5 table
00296 [L988] TGETS    A=30 B=30 C=48 D=7728 'insert'
00297 [L988] MOV      A=31 B=0 C=16 D=16 
00298 [L988] TDUP     A=32 B=0 C=70 D=70 {'kind': 'table', 'value': {'npic': 'v2/soulHuntUI/btn_buy1.png', 'spic': 'v2/soulHuntUI/btn_buy2.png'}}
00299 [L988] TSETS    A=21 B=32 C=21 D=8213 'x'
00300 [L988] MULNV    A=33 B=3 C=16 D=784 
00301 [L988] SUBVV    A=33 B=22 C=33 D=5665 
00302 [L988] TSETS    A=33 B=32 C=11 D=8203 'y'
00303 [L988] TSETS    A=20 B=32 C=52 D=8244 'tag'
00304 [L988] GGET     A=33 B=0 C=71 D=71 'pressBuyItem'
00305 [L988] TSETS    A=33 B=32 C=38 D=8230 'call_back'
00306 [L988] CALL     A=30 B=1 C=3 D=259 
00307 [L963] FORL     A=17 B=127 C=92 D=32604 target=144
00308 [L991] MOV      A=18 B=0 C=0 D=0 
00309 [L991] TGETS    A=17 B=0 C=8 D=8 'addChild'
00310 [L991] GGET     A=19 B=0 C=0 D=0 'd_ms'
00311 [L991] TGETS    A=19 B=19 C=1 D=4865 'd_u'
00312 [L991] TGETS    A=19 B=19 C=72 D=4936 'createMenu'
00313 [L991] MOV      A=20 B=0 C=15 D=15 
00314 [L991] CALL     A=19 B=2 C=2 D=514 
00315 [L991] KSHORT   A=20 B=0 C=5 D=5 5
00316 [L991] CALL     A=17 B=1 C=4 D=260 
00317 [L992] TNEW     A=17 B=0 C=0 D=0 
00318 [L993] MOV      A=19 B=0 C=0 D=0 
00319 [L993] TGETS    A=18 B=0 C=8 D=8 'addChild'
00320 [L993] GGET     A=20 B=0 C=0 D=0 'd_ms'
00321 [L993] TGETS    A=20 B=20 C=1 D=5121 'd_u'
00322 [L993] TGETS    A=20 B=20 C=72 D=5192 'createMenu'
00323 [L993] MOV      A=21 B=0 C=16 D=16 
00324 [L993] MOV      A=22 B=0 C=17 D=17 
00325 [L993] CALL     A=20 B=2 C=3 D=515 
00326 [L993] KSHORT   A=21 B=0 C=5 D=5 5
00327 [L993] CALL     A=18 B=1 C=4 D=260 
00328 [L994] UGET     A=18 B=0 C=6 D=6 pairs
00329 [L994] MOV      A=19 B=0 C=11 D=11 
00330 [L994] CALL     A=18 B=4 C=2 D=1026 
00331 [L994] ISNEXT   A=21 B=128 C=8 D=32776 target=340
00332 [L995] TGETS    A=23 B=22 C=61 D=5693 'buy_times'
00333 [L995] ISNEN    A=23 B=0 C=15 D=15 0
00334 [L995] JMP      A=23 B=128 C=5 D=32773 target=340
00335 [L996] GGET     A=23 B=0 C=0 D=0 'd_ms'
00336 [L996] TGETS    A=23 B=23 C=1 D=5889 'd_u'
00337 [L996] TGETS    A=23 B=23 C=73 D=5961 'grayMenuItem'
00338 [L996] TGETV    A=24 B=17 C=21 D=4373 
00339 [L996] CALL     A=23 B=1 C=2 D=258 
00340 [L994] ITERN    A=21 B=3 C=3 D=771 
00341 [L994] ITERL    A=21 B=127 C=246 D=32758 target=332
00342 [L999] UCLO     A=0 B=128 C=0 D=32768 target=343
00343 [L999] RET0     A=0 B=0 C=1 D=1 
00344 [L999] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto48 offset=0x74dc source_lines=1021-1023 params=0
UPVALUES ['layer']
00001 [L1022] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L1022] TGETS    A=0 B=0 C=1 D=1 'd_u'
00003 [L1022] TGETS    A=0 B=0 C=2 D=2 'remove'
00004 [L1022] UGET     A=1 B=0 C=0 D=0 layer
00005 [L1022] CALL     A=0 B=1 C=2 D=258 
00006 [L1023] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto49 offset=0x7520 source_lines=1002-1035 params=0
UPVALUES ['g_soulHuntUI', 'tags', 'CCLayer', 'g_self']
00001 [L1003] UGET     A=0 B=0 C=0 D=0 g_soulHuntUI
00002 [L1003] TGETS    A=0 B=0 C=0 D=0 'main_layer'
00003 [L1003] IST      A=0 B=0 C=0 D=0 
00004 [L1003] JMP      A=0 B=128 C=1 D=32769 target=6
00005 [L1004] UCLO     A=0 B=128 C=87 D=32855 target=93
00006 [L1006] UGET     A=0 B=0 C=0 D=0 g_soulHuntUI
00007 [L1006] TGETS    A=0 B=0 C=0 D=0 'main_layer'
00008 [L1006] MOV      A=1 B=0 C=0 D=0 
00009 [L1006] TGETS    A=0 B=0 C=1 D=1 'getChildByTag'
00010 [L1006] UGET     A=2 B=0 C=1 D=1 tags
00011 [L1006] TGETS    A=2 B=2 C=2 D=514 'Rank'
00012 [L1006] CALL     A=0 B=2 C=3 D=515 
00013 [L1007] ISF      A=0 B=0 C=0 D=0 
00014 [L1007] JMP      A=1 B=128 C=1 D=32769 target=16
00015 [L1008] UCLO     A=0 B=128 C=78 D=32846 target=94
00016 [L1010] UGET     A=1 B=0 C=2 D=2 CCLayer
00017 [L1010] MOV      A=2 B=0 C=1 D=1 
00018 [L1010] TGETS    A=1 B=1 C=3 D=259 'create'
00019 [L1010] CALL     A=1 B=2 C=2 D=514 
00020 [L1010] MOV      A=0 B=0 C=1 D=1 
00021 [L1011] GGET     A=1 B=0 C=4 D=4 'd_ms'
00022 [L1011] TGETS    A=1 B=1 C=5 D=261 'd_u'
00023 [L1011] TGETS    A=1 B=1 C=6 D=262 'createSwallowTouchLayer'
00024 [L1011] MOV      A=2 B=0 C=0 D=0 
00025 [L1011] CALL     A=1 B=1 C=2 D=258 
00026 [L1013] GGET     A=1 B=0 C=4 D=4 'd_ms'
00027 [L1013] TGETS    A=1 B=1 C=5 D=261 'd_u'
00028 [L1013] TGETS    A=1 B=1 C=7 D=263 'createByStyle'
00029 [L1013] TDUP     A=2 B=0 C=8 D=8 {'kind': 'table', 'value': {'pic': 'v2/soulHuntUI/bkg8.png', 'x': 0.5, 'y': 0.5}}
00030 [L1013] CALL     A=1 B=2 C=2 D=514 
00031 [L1014] MOV      A=3 B=0 C=0 D=0 
00032 [L1014] TGETS    A=2 B=0 C=9 D=9 'addChild'
00033 [L1014] MOV      A=4 B=0 C=1 D=1 
00034 [L1014] CALL     A=2 B=1 C=3 D=259 
00035 [L1015] GGET     A=2 B=0 C=4 D=4 'd_ms'
00036 [L1015] TGETS    A=2 B=2 C=5 D=517 'd_u'
00037 [L1015] TGETS    A=2 B=2 C=10 D=522 'getRealScale'
00038 [L1015] MOV      A=3 B=0 C=1 D=1 
00039 [L1015] CALL     A=2 B=3 C=2 D=770 
00040 [L1016] UGET     A=4 B=0 C=3 D=3 g_self
00041 [L1016] TDUP     A=5 B=0 C=12 D=12 {'kind': 'table', 'value': {}}
00042 [L1016] TSETS    A=2 B=5 C=13 D=1293 'width'
00043 [L1016] TSETS    A=3 B=5 C=14 D=1294 'height'
00044 [L1016] TSETS    A=5 B=4 C=11 D=1035 'RankSize'
00045 [L1018] GGET     A=4 B=0 C=4 D=4 'd_ms'
00046 [L1018] TGETS    A=4 B=4 C=5 D=1029 'd_u'
00047 [L1018] TGETS    A=4 B=4 C=7 D=1031 'createByStyle'
00048 [L1018] TDUP     A=5 B=0 C=15 D=15 {'kind': 'table', 'value': {'pic': 'v2/soulHuntUI/title3.png', 'x': 0.5}}
00049 [L1018] MULNV    A=6 B=3 C=0 D=768 
00050 [L1018] ADDNV    A=6 B=6 C=1 D=1537 
00051 [L1018] TSETS    A=6 B=5 C=16 D=1296 'y'
00052 [L1018] CALL     A=4 B=2 C=2 D=514 
00053 [L1019] MOV      A=6 B=0 C=0 D=0 
00054 [L1019] TGETS    A=5 B=0 C=9 D=9 'addChild'
00055 [L1019] MOV      A=7 B=0 C=4 D=4 
00056 [L1019] KSHORT   A=8 B=0 C=1 D=1 1
00057 [L1019] CALL     A=5 B=1 C=4 D=260 
00058 [L1023] FNEW     A=5 B=0 C=17 D=17 {'kind': 'proto', 'id': 48}
00059 [L1025] GGET     A=6 B=0 C=18 D=18 'createLeftBtnsSlid'
00060 [L1025] MOV      A=7 B=0 C=0 D=0 
00061 [L1025] GGET     A=8 B=0 C=19 D=19 'mtag'
00062 [L1025] CALL     A=6 B=1 C=3 D=259 
00063 [L1028] TDUP     A=6 B=0 C=20 D=20 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00064 [L1030] TDUP     A=7 B=0 C=21 D=21 {'kind': 'table', 'value': {'npic': 'v2/introUI/close1.png', 'spic': 'v2/introUI/close2.png'}}
00065 [L1031] MULNV    A=8 B=2 C=2 D=514 
00066 [L1031] ADDNV    A=8 B=8 C=1 D=2049 
00067 [L1031] TSETS    A=8 B=7 C=22 D=1814 'x'
00068 [L1031] MULNV    A=8 B=3 C=0 D=768 
00069 [L1031] ADDNV    A=8 B=8 C=1 D=2049 
00070 [L1031] TSETS    A=8 B=7 C=16 D=1808 'y'
00071 [L1031] TSETS    A=5 B=7 C=23 D=1815 'call_back'
00072 [L1031] TSETB    A=7 B=6 C=1 D=1537 
00073 [L1033] MOV      A=8 B=0 C=0 D=0 
00074 [L1033] TGETS    A=7 B=0 C=9 D=9 'addChild'
00075 [L1033] GGET     A=9 B=0 C=4 D=4 'd_ms'
00076 [L1033] TGETS    A=9 B=9 C=5 D=2309 'd_u'
00077 [L1033] TGETS    A=9 B=9 C=24 D=2328 'createMenu'
00078 [L1033] MOV      A=10 B=0 C=6 D=6 
00079 [L1033] CALL     A=9 B=2 C=2 D=514 
00080 [L1033] KSHORT   A=10 B=0 C=5 D=5 5
00081 [L1033] CALL     A=7 B=1 C=4 D=260 
00082 [L1034] UGET     A=7 B=0 C=0 D=0 g_soulHuntUI
00083 [L1034] TGETS    A=7 B=7 C=0 D=1792 'main_layer'
00084 [L1034] MOV      A=8 B=0 C=7 D=7 
00085 [L1034] TGETS    A=7 B=7 C=9 D=1801 'addChild'
00086 [L1034] MOV      A=9 B=0 C=0 D=0 
00087 [L1034] KSHORT   A=10 B=0 C=20 D=20 20
00088 [L1034] UGET     A=11 B=0 C=1 D=1 tags
00089 [L1034] TGETS    A=11 B=11 C=2 D=2818 'Rank'
00090 [L1034] CALL     A=7 B=1 C=5 D=261 
00091 [L1035] UCLO     A=0 B=128 C=0 D=32768 target=92
00092 [L1035] RET0     A=0 B=0 C=1 D=1 
00093 [L1035] RET0     A=0 B=0 C=1 D=1 
00094 [L1035] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto50 offset=0x78d3 source_lines=1038-1042 params=0
UPVALUES ['CCSprite', 'g_self']
00001 [L1039] UGET     A=0 B=0 C=0 D=0 CCSprite
00002 [L1039] MOV      A=1 B=0 C=0 D=0 
00003 [L1039] TGETS    A=0 B=0 C=0 D=0 'create'
00004 [L1039] KSTR     A=2 B=0 C=1 D=1 'v2/newbieManualUI/btn1.png'
00005 [L1039] CALL     A=0 B=2 C=3 D=515 
00006 [L1040] UGET     A=1 B=0 C=1 D=1 g_self
00007 [L1040] UGET     A=2 B=0 C=1 D=1 g_self
00008 [L1040] GGET     A=3 B=0 C=4 D=4 'd_ms'
00009 [L1040] TGETS    A=3 B=3 C=5 D=773 'd_u'
00010 [L1040] TGETS    A=3 B=3 C=6 D=774 'getPicScale'
00011 [L1040] MOV      A=4 B=0 C=0 D=0 
00012 [L1040] CALL     A=3 B=3 C=2 D=770 
00013 [L1040] TSETS    A=4 B=2 C=3 D=515 'btn_h1'
00014 [L1040] TSETS    A=3 B=1 C=2 D=258 'btn_w1'
00015 [L1041] UGET     A=1 B=0 C=1 D=1 g_self
00016 [L1041] UGET     A=2 B=0 C=1 D=1 g_self
00017 [L1041] TGETS    A=2 B=2 C=3 D=515 'btn_h1'
00018 [L1041] MULVN    A=2 B=2 C=0 D=512 
00019 [L1041] TSETS    A=2 B=1 C=3 D=259 'btn_h1'
00020 [L1042] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto51 offset=0x79b2 source_lines=1047-1059 params=1
UPVALUES ['g_soulHuntUI']
00001 [L1048] GGET     A=1 B=0 C=0 D=0 'd_ms'
00002 [L1048] TGETS    A=1 B=1 C=1 D=257 'd_music_mgr'
00003 [L1048] TGETS    A=1 B=1 C=2 D=258 'playClickEffect'
00004 [L1048] CALL     A=1 B=1 C=1 D=257 
00005 [L1049] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00006 [L1049] TGETS    A=1 B=1 C=3 D=259 'btns'
00007 [L1049] ISF      A=0 B=0 C=1 D=1 
00008 [L1049] JMP      A=2 B=128 C=27 D=32795 target=36
00009 [L1050] KSHORT   A=1 B=0 C=1 D=1 1
00010 [L1050] UGET     A=2 B=0 C=0 D=0 g_soulHuntUI
00011 [L1050] TGETS    A=2 B=2 C=3 D=515 'btns'
00012 [L1050] LEN      A=2 B=0 C=2 D=2 
00013 [L1050] KSHORT   A=3 B=0 C=1 D=1 1
00014 [L1050] FORI     A=1 B=128 C=21 D=32789 target=36
00015 [L1051] ISNEV    A=4 B=0 C=0 D=0 
00016 [L1051] JMP      A=5 B=128 C=11 D=32779 target=28
00017 [L1052] UGET     A=5 B=0 C=0 D=0 g_soulHuntUI
00018 [L1052] TGETS    A=5 B=5 C=3 D=1283 'btns'
00019 [L1052] TGETV    A=5 B=5 C=4 D=1284 
00020 [L1052] MOV      A=6 B=0 C=5 D=5 
00021 [L1052] TGETS    A=5 B=5 C=4 D=1284 'setEnabled'
00022 [L1052] KPRI     A=7 B=0 C=1 D=1 
00023 [L1052] CALL     A=5 B=1 C=3 D=259 
00024 [L1053] GGET     A=5 B=0 C=5 D=5 'pressRank'
00025 [L1053] MOV      A=6 B=0 C=0 D=0 
00026 [L1053] CALL     A=5 B=1 C=2 D=258 
00027 [L1053] JMP      A=5 B=128 C=7 D=32775 target=35
00028 [L1055] UGET     A=5 B=0 C=0 D=0 g_soulHuntUI
00029 [L1055] TGETS    A=5 B=5 C=3 D=1283 'btns'
00030 [L1055] TGETV    A=5 B=5 C=4 D=1284 
00031 [L1055] MOV      A=6 B=0 C=5 D=5 
00032 [L1055] TGETS    A=5 B=5 C=4 D=1284 'setEnabled'
00033 [L1055] KPRI     A=7 B=0 C=2 D=2 
00034 [L1055] CALL     A=5 B=1 C=3 D=259 
00035 [L1050] FORL     A=1 B=127 C=235 D=32747 target=15
00036 [L1059] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto52 offset=0x7ad1 source_lines=1045-1120 params=2
UPVALUES ['g_soulHuntUI', 'g_self', 'CCLayer', 'CCScrollView', 'gethz']
00001 [L1059] FNEW     A=2 B=0 C=0 D=0 {'kind': 'proto', 'id': 51}
00002 [L1062] GGET     A=3 B=0 C=1 D=1 'calculateBtnSize'
00003 [L1062] CALL     A=3 B=1 C=1 D=257 
00004 [L1064] TDUP     A=3 B=0 C=4 D=4 {'kind': 'table', 'value': {}}
00005 [L1064] UGET     A=4 B=0 C=1 D=1 g_self
00006 [L1064] TGETS    A=4 B=4 C=2 D=1026 'RankSize'
00007 [L1064] TGETS    A=4 B=4 C=3 D=1027 'width'
00008 [L1064] MULVN    A=4 B=4 C=0 D=1024 
00009 [L1064] SUBNV    A=4 B=4 C=1 D=1025 
00010 [L1064] TSETS    A=4 B=3 C=5 D=773 'x'
00011 [L1064] UGET     A=4 B=0 C=1 D=1 g_self
00012 [L1064] TGETS    A=4 B=4 C=2 D=1026 'RankSize'
00013 [L1064] TGETS    A=4 B=4 C=6 D=1030 'height'
00014 [L1064] MULVN    A=4 B=4 C=2 D=1026 
00015 [L1064] SUBNV    A=4 B=4 C=1 D=1025 
00016 [L1064] TSETS    A=4 B=3 C=7 D=775 'y'
00017 [L1064] UGET     A=4 B=0 C=1 D=1 g_self
00018 [L1064] TGETS    A=4 B=4 C=2 D=1026 'RankSize'
00019 [L1064] TGETS    A=4 B=4 C=3 D=1027 'width'
00020 [L1064] MULVN    A=4 B=4 C=3 D=1027 
00021 [L1064] TSETS    A=4 B=3 C=3 D=771 'width'
00022 [L1064] UGET     A=4 B=0 C=1 D=1 g_self
00023 [L1064] TGETS    A=4 B=4 C=2 D=1026 'RankSize'
00024 [L1064] TGETS    A=4 B=4 C=6 D=1030 'height'
00025 [L1064] MULVN    A=4 B=4 C=4 D=1028 
00026 [L1064] TSETS    A=4 B=3 C=6 D=774 'height'
00027 [L1066] UGET     A=4 B=0 C=2 D=2 CCLayer
00028 [L1066] MOV      A=5 B=0 C=4 D=4 
00029 [L1066] TGETS    A=4 B=4 C=8 D=1032 'create'
00030 [L1066] CALL     A=4 B=2 C=2 D=514 
00031 [L1067] UGET     A=5 B=0 C=3 D=3 CCScrollView
00032 [L1067] MOV      A=6 B=0 C=5 D=5 
00033 [L1067] TGETS    A=5 B=5 C=8 D=1288 'create'
00034 [L1067] GGET     A=7 B=0 C=9 D=9 'd_ms'
00035 [L1067] TGETS    A=7 B=7 C=10 D=1802 'd_u'
00036 [L1067] TGETS    A=7 B=7 C=11 D=1803 'ccSizeMake'
00037 [L1067] TGETS    A=8 B=3 C=3 D=771 'width'
00038 [L1067] TGETS    A=9 B=3 C=6 D=774 'height'
00039 [L1067] CALL     A=7 B=2 C=3 D=515 
00040 [L1067] MOV      A=8 B=0 C=4 D=4 
00041 [L1067] CALL     A=5 B=2 C=4 D=516 
00042 [L1068] GGET     A=6 B=0 C=9 D=9 'd_ms'
00043 [L1068] TGETS    A=6 B=6 C=10 D=1546 'd_u'
00044 [L1068] TGETS    A=6 B=6 C=12 D=1548 'setStyles'
00045 [L1068] MOV      A=7 B=0 C=5 D=5 
00046 [L1068] TDUP     A=8 B=0 C=13 D=13 {'kind': 'table', 'value': {}}
00047 [L1068] TGETS    A=9 B=3 C=5 D=773 'x'
00048 [L1068] TSETS    A=9 B=8 C=5 D=2053 'x'
00049 [L1068] TGETS    A=9 B=3 C=7 D=775 'y'
00050 [L1068] TSETS    A=9 B=8 C=7 D=2055 'y'
00051 [L1068] CALL     A=6 B=1 C=3 D=259 
00052 [L1070] MOV      A=7 B=0 C=0 D=0 
00053 [L1070] TGETS    A=6 B=0 C=14 D=14 'addChild'
00054 [L1070] MOV      A=8 B=0 C=5 D=5 
00055 [L1070] CALL     A=6 B=1 C=3 D=259 
00056 [L1072] TNEW     A=6 B=0 C=0 D=0 
00057 [L1073] KSHORT   A=7 B=0 C=7 D=7 7
00058 [L1074] KSHORT   A=8 B=0 C=0 D=0 0
00059 [L1074] TSETS    A=8 B=6 C=15 D=1551 'y_limit_down'
00060 [L1075] UGET     A=8 B=0 C=1 D=1 g_self
00061 [L1075] TGETS    A=8 B=8 C=16 D=2064 'btn_h1'
00062 [L1075] MULVV    A=8 B=8 C=7 D=2055 
00063 [L1075] TGETS    A=9 B=3 C=6 D=774 'height'
00064 [L1075] SUBVV    A=8 B=8 C=9 D=2057 
00065 [L1075] KSHORT   A=9 B=0 C=0 D=0 0
00066 [L1075] ISGE     A=9 B=0 C=8 D=8 
00067 [L1075] JMP      A=8 B=128 C=7 D=32775 target=75
00068 [L1076] UGET     A=8 B=0 C=1 D=1 g_self
00069 [L1076] TGETS    A=8 B=8 C=16 D=2064 'btn_h1'
00070 [L1076] MULVV    A=8 B=8 C=7 D=2055 
00071 [L1076] TGETS    A=9 B=3 C=6 D=774 'height'
00072 [L1076] SUBVV    A=8 B=8 C=9 D=2057 
00073 [L1076] TSETS    A=8 B=6 C=17 D=1553 'y_limit_top'
00074 [L1076] JMP      A=8 B=128 C=2 D=32770 target=77
00075 [L1078] KSHORT   A=8 B=0 C=0 D=0 0
00076 [L1078] TSETS    A=8 B=6 C=17 D=1553 'y_limit_top'
00077 [L1080] UGET     A=8 B=0 C=1 D=1 g_self
00078 [L1080] TGETS    A=8 B=8 C=2 D=2050 'RankSize'
00079 [L1080] TGETS    A=8 B=8 C=6 D=2054 'height'
00080 [L1080] MULNV    A=8 B=8 C=5 D=2053 
00081 [L1080] TSETS    A=8 B=6 C=18 D=1554 'limit_springback'
00082 [L1081] KSHORT   A=8 B=255 C=127 D=65407 -129
00083 [L1081] TSETS    A=8 B=6 C=19 D=1555 'btn_pri'
00084 [L1082] KPRI     A=8 B=0 C=1 D=1 
00085 [L1082] TSETS    A=8 B=6 C=20 D=1556 'isSwallow'
00086 [L1085] GGET     A=8 B=0 C=9 D=9 'd_ms'
00087 [L1085] TGETS    A=8 B=8 C=10 D=2058 'd_u'
00088 [L1085] TGETS    A=8 B=8 C=21 D=2069 'ccRectMake'
00089 [L1085] UGET     A=9 B=0 C=1 D=1 g_self
00090 [L1085] TGETS    A=9 B=9 C=2 D=2306 'RankSize'
00091 [L1085] TGETS    A=9 B=9 C=3 D=2307 'width'
00092 [L1085] MULVN    A=9 B=9 C=1 D=2305 
00093 [L1085] SUBNV    A=9 B=9 C=1 D=2305 
00094 [L1085] UGET     A=10 B=0 C=1 D=1 g_self
00095 [L1085] TGETS    A=10 B=10 C=2 D=2562 'RankSize'
00096 [L1085] TGETS    A=10 B=10 C=6 D=2566 'height'
00097 [L1085] MULVN    A=10 B=10 C=1 D=2561 
00098 [L1085] SUBNV    A=10 B=10 C=1 D=2561 
00099 [L1085] UGET     A=11 B=0 C=1 D=1 g_self
00100 [L1085] TGETS    A=11 B=11 C=2 D=2818 'RankSize'
00101 [L1085] TGETS    A=11 B=11 C=3 D=2819 'width'
00102 [L1085] MULVN    A=11 B=11 C=6 D=2822 
00103 [L1085] DIVVN    A=11 B=11 C=7 D=2823 
00104 [L1085] UGET     A=12 B=0 C=1 D=1 g_self
00105 [L1085] TGETS    A=12 B=12 C=2 D=3074 'RankSize'
00106 [L1085] TGETS    A=12 B=12 C=6 D=3078 'height'
00107 [L1085] MULVN    A=12 B=12 C=8 D=3080 
00108 [L1085] DIVVN    A=12 B=12 C=9 D=3081 
00109 [L1085] CALL     A=8 B=2 C=5 D=517 
00110 [L1086] GGET     A=9 B=0 C=9 D=9 'd_ms'
00111 [L1086] TGETS    A=9 B=9 C=22 D=2326 'd_touch_event'
00112 [L1086] TGETS    A=9 B=9 C=23 D=2327 'enableSlideY'
00113 [L1086] MOV      A=10 B=0 C=4 D=4 
00114 [L1086] MOV      A=11 B=0 C=8 D=8 
00115 [L1086] MOV      A=12 B=0 C=6 D=6 
00116 [L1086] CALL     A=9 B=1 C=4 D=260 
00117 [L1089] UGET     A=9 B=0 C=0 D=0 g_soulHuntUI
00118 [L1089] TNEW     A=10 B=0 C=0 D=0 
00119 [L1089] TSETS    A=10 B=9 C=24 D=2328 'btns'
00120 [L1090] TDUP     A=9 B=0 C=25 D=25 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00121 [L1096] KSHORT   A=10 B=0 C=1 D=1 1
00122 [L1096] MOV      A=11 B=0 C=7 D=7 
00123 [L1096] KSHORT   A=12 B=0 C=1 D=1 1
00124 [L1096] FORI     A=10 B=128 C=37 D=32805 target=162
00125 [L1097] TGETS    A=14 B=3 C=3 D=771 'width'
00126 [L1097] MULVN    A=14 B=14 C=10 D=3594 
00127 [L1098] TGETS    A=15 B=3 C=6 D=774 'height'
00128 [L1098] MULVN    A=15 B=15 C=11 D=3851 
00129 [L1098] UGET     A=16 B=0 C=1 D=1 g_self
00130 [L1098] TGETS    A=16 B=16 C=16 D=4112 'btn_h1'
00131 [L1098] SUBVN    A=17 B=13 C=12 D=3340 
00132 [L1098] MULVV    A=16 B=16 C=17 D=4113 
00133 [L1098] SUBVV    A=15 B=15 C=16 D=3856 
00134 [L1099] TDUP     A=16 B=0 C=26 D=26 {'kind': 'table', 'value': {'npic': 'v2/newbieManualUI/btn1.png', 'dispic': 'v2/newbieManualUI/btn3.png', 'spic': 'v2/newbieManualUI/btn2.png'}}
00135 [L1099] TSETS    A=14 B=16 C=5 D=4101 'x'
00136 [L1099] TSETS    A=15 B=16 C=7 D=4103 'y'
00137 [L1099] TSETS    A=2 B=16 C=27 D=4123 'call_back'
00138 [L1099] TSETS    A=13 B=16 C=28 D=4124 'tag'
00139 [L1099] TSETV    A=16 B=9 C=13 D=2317 
00140 [L1102] UGET     A=16 B=0 C=4 D=4 gethz
00141 [L1102] KSTR     A=17 B=0 C=29 D=29 'hunt_rank'
00142 [L1102] MOV      A=18 B=0 C=13 D=13 
00143 [L1102] CAT      A=17 B=17 C=18 D=4370 
00144 [L1102] CALL     A=16 B=2 C=2 D=514 
00145 [L1103] GGET     A=17 B=0 C=9 D=9 'd_ms'
00146 [L1103] TGETS    A=17 B=17 C=10 D=4362 'd_u'
00147 [L1103] TGETS    A=17 B=17 C=30 D=4382 'createByStyles'
00148 [L1103] TDUP     A=18 B=0 C=31 D=31 {'kind': 'table', 'value': {'type': 'label', 'fontsize': 32}}
00149 [L1103] TSETS    A=16 B=18 C=32 D=4640 'string'
00150 [L1103] TSETS    A=14 B=18 C=5 D=4613 'x'
00151 [L1103] ADDVN    A=19 B=15 C=13 D=3853 
00152 [L1103] TSETS    A=19 B=18 C=7 D=4615 'y'
00153 [L1103] TDUP     A=19 B=0 C=33 D=33 {'kind': 'table', 'value': {1: 255, 2: 156, 3: 0}}
00154 [L1103] TSETS    A=19 B=18 C=34 D=4642 'color'
00155 [L1103] CALL     A=17 B=2 C=2 D=514 
00156 [L1104] MOV      A=19 B=0 C=4 D=4 
00157 [L1104] TGETS    A=18 B=4 C=14 D=1038 'addChild'
00158 [L1104] MOV      A=20 B=0 C=17 D=17 
00159 [L1104] KSHORT   A=21 B=0 C=11 D=11 11
00160 [L1104] CALL     A=18 B=1 C=4 D=260 
00161 [L1096] FORL     A=10 B=127 C=219 D=32731 target=125
00162 [L1107] MOV      A=11 B=0 C=4 D=4 
00163 [L1107] TGETS    A=10 B=4 C=14 D=1038 'addChild'
00164 [L1107] GGET     A=12 B=0 C=9 D=9 'd_ms'
00165 [L1107] TGETS    A=12 B=12 C=10 D=3082 'd_u'
00166 [L1107] TGETS    A=12 B=12 C=35 D=3107 'createMenu'
00167 [L1107] MOV      A=13 B=0 C=9 D=9 
00168 [L1107] UGET     A=14 B=0 C=0 D=0 g_soulHuntUI
00169 [L1107] TGETS    A=14 B=14 C=24 D=3608 'btns'
00170 [L1107] CALL     A=12 B=2 C=3 D=515 
00171 [L1107] KSHORT   A=13 B=0 C=10 D=10 10
00172 [L1107] CALL     A=10 B=1 C=4 D=260 
00173 [L1109] ISF      A=0 B=0 C=1 D=1 
00174 [L1109] JMP      A=10 B=128 C=39 D=32807 target=214
00175 [L1110] UGET     A=10 B=0 C=1 D=1 g_self
00176 [L1110] TGETS    A=10 B=10 C=2 D=2562 'RankSize'
00177 [L1110] TGETS    A=10 B=10 C=6 D=2566 'height'
00178 [L1110] MULVN    A=10 B=10 C=1 D=2561 
00179 [L1110] SUBNV    A=10 B=10 C=1 D=2561 
00180 [L1110] UGET     A=11 B=0 C=1 D=1 g_self
00181 [L1110] TGETS    A=11 B=11 C=2 D=2818 'RankSize'
00182 [L1110] TGETS    A=11 B=11 C=6 D=2822 'height'
00183 [L1110] MULVN    A=11 B=11 C=8 D=2824 
00184 [L1110] DIVVN    A=11 B=11 C=9 D=2825 
00185 [L1110] MULNV    A=11 B=11 C=1 D=2817 
00186 [L1110] ADDVV    A=10 B=10 C=11 D=2571 
00187 [L1110] UGET     A=11 B=0 C=1 D=1 g_self
00188 [L1110] TGETS    A=11 B=11 C=2 D=2818 'RankSize'
00189 [L1110] TGETS    A=11 B=11 C=6 D=2822 'height'
00190 [L1110] MULVN    A=11 B=11 C=11 D=2827 
00191 [L1110] UGET     A=12 B=0 C=1 D=1 g_self
00192 [L1110] TGETS    A=12 B=12 C=16 D=3088 'btn_h1'
00193 [L1110] MULVV    A=12 B=12 C=1 D=3073 
00194 [L1110] SUBVV    A=11 B=11 C=12 D=2828 
00195 [L1110] SUBVV    A=10 B=10 C=11 D=2571 
00196 [L1111] TGETS    A=11 B=6 C=15 D=1551 'y_limit_down'
00197 [L1111] ISGE     A=10 B=0 C=11 D=11 
00198 [L1111] JMP      A=11 B=128 C=2 D=32770 target=201
00199 [L1112] TGETS    A=10 B=6 C=15 D=1551 'y_limit_down'
00200 [L1112] JMP      A=11 B=128 C=4 D=32772 target=205
00201 [L1113] TGETS    A=11 B=6 C=17 D=1553 'y_limit_top'
00202 [L1113] ISGE     A=11 B=0 C=10 D=10 
00203 [L1113] JMP      A=11 B=128 C=1 D=32769 target=205
00204 [L1114] TGETS    A=10 B=6 C=17 D=1553 'y_limit_top'
00205 [L1116] MOV      A=12 B=0 C=4 D=4 
00206 [L1116] TGETS    A=11 B=4 C=36 D=1060 'setPosition'
00207 [L1116] GGET     A=13 B=0 C=9 D=9 'd_ms'
00208 [L1116] TGETS    A=13 B=13 C=10 D=3338 'd_u'
00209 [L1116] TGETS    A=13 B=13 C=37 D=3365 'makePoint'
00210 [L1116] KSHORT   A=14 B=0 C=0 D=0 0
00211 [L1116] MOV      A=15 B=0 C=10 D=10 
00212 [L1116] CALL     A=13 B=0 C=3 D=3 
00213 [L1116] CALLM    A=11 B=1 C=1 D=257 
00214 [L1120] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto53 offset=0x822f source_lines=1122-1141 params=4
UPVALUES ['CCSprite', 'tostring']
00001 [L1123] UGET     A=4 B=0 C=0 D=0 CCSprite
00002 [L1123] MOV      A=5 B=0 C=4 D=4 
00003 [L1123] TGETS    A=4 B=4 C=0 D=1024 'create'
00004 [L1123] KSTR     A=6 B=0 C=1 D=1 'v2/friendsUI/line.png'
00005 [L1123] CALL     A=4 B=2 C=3 D=515 
00006 [L1124] MOV      A=6 B=0 C=4 D=4 
00007 [L1124] TGETS    A=5 B=4 C=2 D=1026 'setPosition'
00008 [L1124] TGETS    A=7 B=3 C=3 D=771 'width'
00009 [L1124] MULVN    A=7 B=7 C=0 D=1792 
00010 [L1124] KSHORT   A=8 B=0 C=0 D=0 0
00011 [L1124] CALL     A=5 B=1 C=4 D=260 
00012 [L1125] MOV      A=6 B=0 C=0 D=0 
00013 [L1125] TGETS    A=5 B=0 C=4 D=4 'addChild'
00014 [L1125] MOV      A=7 B=0 C=4 D=4 
00015 [L1125] CALL     A=5 B=1 C=3 D=259 
00016 [L1127] MOV      A=6 B=0 C=4 D=4 
00017 [L1127] TGETS    A=5 B=4 C=5 D=1029 'getContentSize'
00018 [L1127] CALL     A=5 B=2 C=2 D=514 
00019 [L1128] MOV      A=7 B=0 C=4 D=4 
00020 [L1128] TGETS    A=6 B=4 C=6 D=1030 'setScale'
00021 [L1128] TGETS    A=8 B=3 C=3 D=771 'width'
00022 [L1128] TGETS    A=9 B=5 C=3 D=1283 'width'
00023 [L1128] DIVVV    A=8 B=8 C=9 D=2057 
00024 [L1128] CALL     A=6 B=1 C=3 D=259 
00025 [L1130] GGET     A=6 B=0 C=7 D=7 'd_ms'
00026 [L1130] TGETS    A=6 B=6 C=8 D=1544 'd_u'
00027 [L1130] TGETS    A=6 B=6 C=9 D=1545 'createByStyle'
00028 [L1130] TDUP     A=7 B=0 C=10 D=10 {'kind': 'table', 'value': {'fontsize': 30, 'type': 'label'}}
00029 [L1130] UGET     A=8 B=0 C=1 D=1 tostring
00030 [L1130] MOV      A=9 B=0 C=2 D=2 
00031 [L1130] CALL     A=8 B=2 C=2 D=514 
00032 [L1130] TSETS    A=8 B=7 C=11 D=1803 'string'
00033 [L1130] TDUP     A=8 B=0 C=12 D=12 {'kind': 'table', 'value': {1: 255, 2: 255, 3: 100}}
00034 [L1130] TSETS    A=8 B=7 C=13 D=1805 'color'
00035 [L1130] CALL     A=6 B=2 C=2 D=514 
00036 [L1131] MOV      A=8 B=0 C=6 D=6 
00037 [L1131] TGETS    A=7 B=6 C=2 D=1538 'setPosition'
00038 [L1131] TGETS    A=9 B=3 C=3 D=771 'width'
00039 [L1131] MULVN    A=9 B=9 C=1 D=2305 
00040 [L1131] TGETS    A=10 B=3 C=14 D=782 'height'
00041 [L1131] MULNV    A=10 B=10 C=0 D=2560 
00042 [L1131] CALL     A=7 B=1 C=4 D=260 
00043 [L1132] MOV      A=8 B=0 C=0 D=0 
00044 [L1132] TGETS    A=7 B=0 C=4 D=4 'addChild'
00045 [L1132] MOV      A=9 B=0 C=6 D=6 
00046 [L1132] CALL     A=7 B=1 C=3 D=259 
00047 [L1134] GGET     A=7 B=0 C=7 D=7 'd_ms'
00048 [L1134] TGETS    A=7 B=7 C=8 D=1800 'd_u'
00049 [L1134] TGETS    A=7 B=7 C=9 D=1801 'createByStyle'
00050 [L1134] TDUP     A=8 B=0 C=15 D=15 {'kind': 'table', 'value': {'fontsize': 30, 'type': 'label'}}
00051 [L1134] TGETS    A=9 B=1 C=16 D=272 'name'
00052 [L1134] TSETS    A=9 B=8 C=11 D=2059 'string'
00053 [L1134] TDUP     A=9 B=0 C=17 D=17 {'kind': 'table', 'value': {1: 255, 2: 255, 3: 100}}
00054 [L1134] TSETS    A=9 B=8 C=13 D=2061 'color'
00055 [L1134] CALL     A=7 B=2 C=2 D=514 
00056 [L1135] MOV      A=9 B=0 C=7 D=7 
00057 [L1135] TGETS    A=8 B=7 C=2 D=1794 'setPosition'
00058 [L1135] TGETS    A=10 B=3 C=3 D=771 'width'
00059 [L1135] MULVN    A=10 B=10 C=2 D=2562 
00060 [L1135] TGETS    A=11 B=3 C=14 D=782 'height'
00061 [L1135] MULNV    A=11 B=11 C=0 D=2816 
00062 [L1135] CALL     A=8 B=1 C=4 D=260 
00063 [L1136] MOV      A=9 B=0 C=0 D=0 
00064 [L1136] TGETS    A=8 B=0 C=4 D=4 'addChild'
00065 [L1136] MOV      A=10 B=0 C=7 D=7 
00066 [L1136] CALL     A=8 B=1 C=3 D=259 
00067 [L1138] GGET     A=8 B=0 C=7 D=7 'd_ms'
00068 [L1138] TGETS    A=8 B=8 C=8 D=2056 'd_u'
00069 [L1138] TGETS    A=8 B=8 C=9 D=2057 'createByStyle'
00070 [L1138] TDUP     A=9 B=0 C=18 D=18 {'kind': 'table', 'value': {'fontsize': 30, 'type': 'label'}}
00071 [L1138] UGET     A=10 B=0 C=1 D=1 tostring
00072 [L1138] TGETS    A=11 B=1 C=19 D=275 'soul_count'
00073 [L1138] CALL     A=10 B=2 C=2 D=514 
00074 [L1138] TSETS    A=10 B=9 C=11 D=2315 'string'
00075 [L1138] TDUP     A=10 B=0 C=20 D=20 {'kind': 'table', 'value': {1: 255, 2: 255, 3: 100}}
00076 [L1138] TSETS    A=10 B=9 C=13 D=2317 'color'
00077 [L1138] CALL     A=8 B=2 C=2 D=514 
00078 [L1139] MOV      A=10 B=0 C=8 D=8 
00079 [L1139] TGETS    A=9 B=8 C=2 D=2050 'setPosition'
00080 [L1139] TGETS    A=11 B=3 C=3 D=771 'width'
00081 [L1139] MULVN    A=11 B=11 C=3 D=2819 
00082 [L1139] TGETS    A=12 B=3 C=14 D=782 'height'
00083 [L1139] MULNV    A=12 B=12 C=0 D=3072 
00084 [L1139] CALL     A=9 B=1 C=4 D=260 
00085 [L1140] MOV      A=10 B=0 C=0 D=0 
00086 [L1140] TGETS    A=9 B=0 C=4 D=4 'addChild'
00087 [L1140] MOV      A=11 B=0 C=8 D=8 
00088 [L1140] CALL     A=9 B=1 C=3 D=259 
00089 [L1141] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto54 offset=0x8575 source_lines=1147-1149 params=0
UPVALUES ['num']
00001 [L1148] UGET     A=0 B=0 C=0 D=0 num
00002 [L1148] RET1     A=0 B=0 C=2 D=2 

FUNCTION proto55 offset=0x8593 source_lines=1151-1157 params=1
UPVALUES ['CCNode', 'list', 'cellSize']
00001 [L1152] UGET     A=1 B=0 C=0 D=0 CCNode
00002 [L1152] MOV      A=2 B=0 C=1 D=1 
00003 [L1152] TGETS    A=1 B=1 C=0 D=256 'create'
00004 [L1152] CALL     A=1 B=2 C=2 D=514 
00005 [L1153] UGET     A=2 B=0 C=1 D=1 list
00006 [L1153] TGETV    A=2 B=2 C=0 D=512 
00007 [L1153] ISF      A=0 B=0 C=2 D=2 
00008 [L1153] JMP      A=3 B=128 C=7 D=32775 target=16
00009 [L1154] GGET     A=2 B=0 C=1 D=1 'createRankCell'
00010 [L1154] MOV      A=3 B=0 C=1 D=1 
00011 [L1154] UGET     A=4 B=0 C=1 D=1 list
00012 [L1154] TGETV    A=4 B=4 C=0 D=1024 
00013 [L1154] MOV      A=5 B=0 C=0 D=0 
00014 [L1154] UGET     A=6 B=0 C=2 D=2 cellSize
00015 [L1154] CALL     A=2 B=1 C=5 D=261 
00016 [L1156] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto56 offset=0x8630 source_lines=1159-1161 params=1
UPVALUES ['cellSize']
00001 [L1160] UGET     A=1 B=0 C=0 D=0 cellSize
00002 [L1160] TGETS    A=1 B=1 C=0 D=256 'height'
00003 [L1160] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto57 offset=0x8667 source_lines=1143-1164 params=2
UPVALUES ['CCNode']
00001 [L1144] TNEW     A=2 B=0 C=0 D=0 
00002 [L1145] LEN      A=3 B=0 C=0 D=0 
00003 [L1149] FNEW     A=4 B=0 C=1 D=1 {'kind': 'proto', 'id': 54}
00004 [L1149] TSETS    A=4 B=2 C=0 D=512 'tableViewNumberOfRows'
00005 [L1157] FNEW     A=4 B=0 C=3 D=3 {'kind': 'proto', 'id': 55}
00006 [L1157] TSETS    A=4 B=2 C=2 D=514 'drawCellAtIndex'
00007 [L1161] FNEW     A=4 B=0 C=5 D=5 {'kind': 'proto', 'id': 56}
00008 [L1161] TSETS    A=4 B=2 C=4 D=516 'heightForRowAtIndex'
00009 [L1163] UCLO     A=0 B=128 C=0 D=32768 target=10
00010 [L1163] RET1     A=2 B=0 C=2 D=2 

FUNCTION proto58 offset=0x8712 source_lines=1166-1183 params=4
UPVALUES ['string']
00001 [L1167] GGET     A=4 B=0 C=0 D=0 'd_ms'
00002 [L1167] TGETS    A=4 B=4 C=1 D=1025 'd_crossRankUI'
00003 [L1167] TGETS    A=4 B=4 C=2 D=1026 'createCommonRewardCell'
00004 [L1167] MOV      A=5 B=0 C=0 D=0 
00005 [L1167] MOV      A=6 B=0 C=1 D=1 
00006 [L1167] MOV      A=7 B=0 C=2 D=2 
00007 [L1167] MOV      A=8 B=0 C=3 D=3 
00008 [L1167] CALL     A=4 B=1 C=5 D=261 
00009 [L1169] KPRI     A=4 B=0 C=0 D=0 
00010 [L1170] TGETS    A=5 B=1 C=3 D=259 'max'
00011 [L1170] TGETS    A=6 B=1 C=4 D=260 'min'
00012 [L1170] ISGE     A=5 B=0 C=6 D=6 
00013 [L1170] JMP      A=5 B=128 C=8 D=32776 target=22
00014 [L1171] TGETS    A=5 B=1 C=4 D=260 'min'
00015 [L1171] GGET     A=6 B=0 C=0 D=0 'd_ms'
00016 [L1171] TGETS    A=6 B=6 C=5 D=1541 'd_hz'
00017 [L1171] TGETS    A=6 B=6 C=6 D=1542 'gethz'
00018 [L1171] KSTR     A=7 B=0 C=7 D=7 'rankPrizeHZ3'
00019 [L1171] CALL     A=6 B=2 C=2 D=514 
00020 [L1171] CAT      A=4 B=5 C=6 D=1286 
00021 [L1171] JMP      A=5 B=128 C=24 D=32792 target=46
00022 [L1172] TGETS    A=5 B=1 C=3 D=259 'max'
00023 [L1172] TGETS    A=6 B=1 C=4 D=260 'min'
00024 [L1172] ISNEV    A=5 B=0 C=6 D=6 
00025 [L1172] JMP      A=5 B=128 C=11 D=32779 target=37
00026 [L1173] UGET     A=5 B=0 C=0 D=0 string
00027 [L1173] TGETS    A=5 B=5 C=8 D=1288 'format'
00028 [L1173] GGET     A=6 B=0 C=0 D=0 'd_ms'
00029 [L1173] TGETS    A=6 B=6 C=5 D=1541 'd_hz'
00030 [L1173] TGETS    A=6 B=6 C=6 D=1542 'gethz'
00031 [L1173] KSTR     A=7 B=0 C=9 D=9 'rankPrizeHZ'
00032 [L1173] CALL     A=6 B=2 C=2 D=514 
00033 [L1173] TGETS    A=7 B=1 C=4 D=260 'min'
00034 [L1173] CALL     A=5 B=2 C=3 D=515 
00035 [L1173] MOV      A=4 B=0 C=5 D=5 
00036 [L1173] JMP      A=5 B=128 C=9 D=32777 target=46
00037 [L1175] TGETS    A=5 B=1 C=4 D=260 'min'
00038 [L1175] KSTR     A=6 B=0 C=10 D=10 '-'
00039 [L1175] TGETS    A=7 B=1 C=3 D=259 'max'
00040 [L1175] GGET     A=8 B=0 C=0 D=0 'd_ms'
00041 [L1175] TGETS    A=8 B=8 C=5 D=2053 'd_hz'
00042 [L1175] TGETS    A=8 B=8 C=6 D=2054 'gethz'
00043 [L1175] KSTR     A=9 B=0 C=11 D=11 'rankPrizeHZ2'
00044 [L1175] CALL     A=8 B=2 C=2 D=514 
00045 [L1175] CAT      A=4 B=5 C=8 D=1288 
00046 [L1178] ISF      A=0 B=0 C=4 D=4 
00047 [L1178] JMP      A=5 B=128 C=22 D=32790 target=70
00048 [L1179] GGET     A=5 B=0 C=0 D=0 'd_ms'
00049 [L1179] TGETS    A=5 B=5 C=12 D=1292 'd_u'
00050 [L1179] TGETS    A=5 B=5 C=13 D=1293 'createByStyle'
00051 [L1179] TDUP     A=6 B=0 C=14 D=14 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 26}}
00052 [L1179] TSETS    A=4 B=6 C=15 D=1551 'string'
00053 [L1179] TDUP     A=7 B=0 C=16 D=16 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00054 [L1179] TSETS    A=7 B=6 C=17 D=1553 'anchor'
00055 [L1179] TDUP     A=7 B=0 C=18 D=18 {'kind': 'table', 'value': {1: 80, 2: 36, 3: 1}}
00056 [L1179] TSETS    A=7 B=6 C=19 D=1555 'color'
00057 [L1179] CALL     A=5 B=2 C=2 D=514 
00058 [L1180] MOV      A=7 B=0 C=5 D=5 
00059 [L1180] TGETS    A=6 B=5 C=20 D=1300 'setPosition'
00060 [L1180] TGETS    A=8 B=2 C=21 D=533 'width'
00061 [L1180] MULVN    A=8 B=8 C=0 D=2048 
00062 [L1180] TGETS    A=9 B=2 C=22 D=534 'height'
00063 [L1180] MULVN    A=9 B=9 C=1 D=2305 
00064 [L1180] CALL     A=6 B=1 C=4 D=260 
00065 [L1181] MOV      A=7 B=0 C=0 D=0 
00066 [L1181] TGETS    A=6 B=0 C=23 D=23 'addChild'
00067 [L1181] MOV      A=8 B=0 C=5 D=5 
00068 [L1181] KSHORT   A=9 B=0 C=1 D=1 1
00069 [L1181] CALL     A=6 B=1 C=4 D=260 
00070 [L1183] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto59 offset=0x89c6 source_lines=1189-1191 params=0
UPVALUES ['num']
00001 [L1190] UGET     A=0 B=0 C=0 D=0 num
00002 [L1190] RET1     A=0 B=0 C=2 D=2 

FUNCTION proto60 offset=0x89e4 source_lines=1193-1199 params=1
UPVALUES ['CCNode', 'prizeInfo', 'cellSize', 'touchRect']
00001 [L1194] UGET     A=1 B=0 C=0 D=0 CCNode
00002 [L1194] MOV      A=2 B=0 C=1 D=1 
00003 [L1194] TGETS    A=1 B=1 C=0 D=256 'create'
00004 [L1194] CALL     A=1 B=2 C=2 D=514 
00005 [L1195] UGET     A=2 B=0 C=1 D=1 prizeInfo
00006 [L1195] TGETV    A=2 B=2 C=0 D=512 
00007 [L1195] ISF      A=0 B=0 C=2 D=2 
00008 [L1195] JMP      A=3 B=128 C=7 D=32775 target=16
00009 [L1196] GGET     A=2 B=0 C=1 D=1 'createPrizeCell'
00010 [L1196] MOV      A=3 B=0 C=1 D=1 
00011 [L1196] UGET     A=4 B=0 C=1 D=1 prizeInfo
00012 [L1196] TGETV    A=4 B=4 C=0 D=1024 
00013 [L1196] UGET     A=5 B=0 C=2 D=2 cellSize
00014 [L1196] UGET     A=6 B=0 C=3 D=3 touchRect
00015 [L1196] CALL     A=2 B=1 C=5 D=261 
00016 [L1198] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto61 offset=0x8a93 source_lines=1201-1203 params=1
UPVALUES ['cellSize']
00001 [L1202] UGET     A=1 B=0 C=0 D=0 cellSize
00002 [L1202] TGETS    A=1 B=1 C=0 D=256 'height'
00003 [L1202] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto62 offset=0x8aca source_lines=1185-1206 params=3
UPVALUES ['CCNode']
00001 [L1186] TNEW     A=3 B=0 C=0 D=0 
00002 [L1187] LEN      A=4 B=0 C=0 D=0 
00003 [L1191] FNEW     A=5 B=0 C=1 D=1 {'kind': 'proto', 'id': 59}
00004 [L1191] TSETS    A=5 B=3 C=0 D=768 'tableViewNumberOfRows'
00005 [L1199] FNEW     A=5 B=0 C=3 D=3 {'kind': 'proto', 'id': 60}
00006 [L1199] TSETS    A=5 B=3 C=2 D=770 'drawCellAtIndex'
00007 [L1203] FNEW     A=5 B=0 C=5 D=5 {'kind': 'proto', 'id': 61}
00008 [L1203] TSETS    A=5 B=3 C=4 D=772 'heightForRowAtIndex'
00009 [L1205] UCLO     A=0 B=128 C=0 D=32768 target=10
00010 [L1205] RET1     A=3 B=0 C=2 D=2 

FUNCTION proto63 offset=0x8b86 source_lines=1253-1259 params=0
UPVALUES ['my_data']
00001 [L1254] UGET     A=0 B=0 C=0 D=0 my_data
00002 [L1254] TGETS    A=0 B=0 C=0 D=0 'had_got_prize'
00003 [L1254] ISF      A=0 B=0 C=0 D=0 
00004 [L1254] JMP      A=1 B=128 C=10 D=32778 target=15
00005 [L1255] GGET     A=0 B=0 C=1 D=1 'd_ms'
00006 [L1255] TGETS    A=0 B=0 C=2 D=2 'd_info'
00007 [L1255] TGETS    A=0 B=0 C=3 D=3 'show'
00008 [L1255] GGET     A=1 B=0 C=1 D=1 'd_ms'
00009 [L1255] TGETS    A=1 B=1 C=4 D=260 'd_hz'
00010 [L1255] TGETS    A=1 B=1 C=5 D=261 'gethz'
00011 [L1255] KSTR     A=2 B=0 C=6 D=6 'has_take_promotion_prize'
00012 [L1255] CALL     A=1 B=0 C=2 D=2 
00013 [L1255] CALLM    A=0 B=1 C=0 D=256 
00014 [L1255] JMP      A=0 B=128 C=2 D=32770 target=17
00015 [L1257] GGET     A=0 B=0 C=7 D=7 'sendTakeRewardRequest'
00016 [L1257] CALL     A=0 B=1 C=1 D=257 
00017 [L1259] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto64 offset=0x8c4c source_lines=1207-1290 params=1
UPVALUES ['g_soulHuntUI', 'tags', 'g_self', 'tostring', 'scrSize', 'CCSizeMake', 'CCRectMake']
00001 [L1208] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00002 [L1208] TGETS    A=1 B=1 C=0 D=256 'main_layer'
00003 [L1208] IST      A=0 B=0 C=1 D=1 
00004 [L1208] JMP      A=1 B=128 C=1 D=32769 target=6
00005 [L1209] UCLO     A=0 B=129 C=102 D=33126 target=364
00006 [L1211] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00007 [L1211] TGETS    A=1 B=1 C=0 D=256 'main_layer'
00008 [L1211] MOV      A=2 B=0 C=1 D=1 
00009 [L1211] TGETS    A=1 B=1 C=1 D=257 'getChildByTag'
00010 [L1211] UGET     A=3 B=0 C=1 D=1 tags
00011 [L1211] TGETS    A=3 B=3 C=2 D=770 'Rank'
00012 [L1211] CALL     A=1 B=2 C=3 D=515 
00013 [L1212] IST      A=0 B=0 C=1 D=1 
00014 [L1212] JMP      A=2 B=128 C=1 D=32769 target=16
00015 [L1213] UCLO     A=0 B=129 C=93 D=33117 target=365
00016 [L1215] ISF      A=0 B=0 C=0 D=0 
00017 [L1215] JMP      A=2 B=128 C=30 D=32798 target=48
00018 [L1216] UGET     A=2 B=0 C=0 D=0 g_soulHuntUI
00019 [L1216] TGETS    A=2 B=2 C=3 D=515 'lastIndex'
00020 [L1216] ISF      A=0 B=0 C=2 D=2 
00021 [L1216] JMP      A=3 B=128 C=16 D=32784 target=38
00022 [L1216] UGET     A=2 B=0 C=0 D=0 g_soulHuntUI
00023 [L1216] TGETS    A=2 B=2 C=4 D=516 'btns'
00024 [L1216] UGET     A=3 B=0 C=0 D=0 g_soulHuntUI
00025 [L1216] TGETS    A=3 B=3 C=3 D=771 'lastIndex'
00026 [L1216] TGETV    A=2 B=2 C=3 D=515 
00027 [L1216] ISF      A=0 B=0 C=2 D=2 
00028 [L1216] JMP      A=3 B=128 C=9 D=32777 target=38
00029 [L1217] UGET     A=2 B=0 C=0 D=0 g_soulHuntUI
00030 [L1217] TGETS    A=2 B=2 C=4 D=516 'btns'
00031 [L1217] UGET     A=3 B=0 C=0 D=0 g_soulHuntUI
00032 [L1217] TGETS    A=3 B=3 C=3 D=771 'lastIndex'
00033 [L1217] TGETV    A=2 B=2 C=3 D=515 
00034 [L1217] MOV      A=3 B=0 C=2 D=2 
00035 [L1217] TGETS    A=2 B=2 C=5 D=517 'setEnabled'
00036 [L1217] KPRI     A=4 B=0 C=2 D=2 
00037 [L1217] CALL     A=2 B=1 C=3 D=259 
00038 [L1219] UGET     A=2 B=0 C=0 D=0 g_soulHuntUI
00039 [L1219] TGETS    A=2 B=2 C=4 D=516 'btns'
00040 [L1219] TGETV    A=2 B=2 C=0 D=512 
00041 [L1219] MOV      A=3 B=0 C=2 D=2 
00042 [L1219] TGETS    A=2 B=2 C=5 D=517 'setEnabled'
00043 [L1219] KPRI     A=4 B=0 C=1 D=1 
00044 [L1219] CALL     A=2 B=1 C=3 D=259 
00045 [L1220] UGET     A=2 B=0 C=0 D=0 g_soulHuntUI
00046 [L1220] TSETS    A=0 B=2 C=3 D=515 'lastIndex'
00047 [L1220] JMP      A=2 B=128 C=2 D=32770 target=50
00048 [L1222] UGET     A=2 B=0 C=0 D=0 g_soulHuntUI
00049 [L1222] TGETS    A=0 B=2 C=3 D=515 'lastIndex'
00050 [L1225] GGET     A=2 B=0 C=6 D=6 'd_ms'
00051 [L1225] TGETS    A=2 B=2 C=7 D=519 'd_u'
00052 [L1225] TGETS    A=2 B=2 C=8 D=520 'clearLayer'
00053 [L1225] MOV      A=3 B=0 C=1 D=1 
00054 [L1225] KSHORT   A=4 B=0 C=20 D=20 20
00055 [L1225] UGET     A=5 B=0 C=1 D=1 tags
00056 [L1225] TGETS    A=5 B=5 C=9 D=1289 'RankDetail'
00057 [L1225] CALL     A=2 B=2 C=4 D=516 
00058 [L1226] UGET     A=3 B=0 C=2 D=2 g_self
00059 [L1226] TGETS    A=3 B=3 C=10 D=778 'RankSize'
00060 [L1226] TGETS    A=3 B=3 C=11 D=779 'width'
00061 [L1226] UGET     A=4 B=0 C=2 D=2 g_self
00062 [L1226] TGETS    A=4 B=4 C=10 D=1034 'RankSize'
00063 [L1226] TGETS    A=4 B=4 C=12 D=1036 'height'
00064 [L1227] MULNV    A=5 B=4 C=0 D=1024 
00065 [L1227] SUBNV    A=5 B=5 C=1 D=1281 
00066 [L1228] ISEQN    A=0 B=0 C=2 D=2 4
00067 [L1228] JMP      A=6 B=128 C=231 D=32999 target=299
00068 [L1228] ISEQN    A=0 B=0 C=3 D=3 5
00069 [L1228] JMP      A=6 B=128 C=229 D=32997 target=299
00070 [L1229] MULNV    A=6 B=4 C=4 D=1028 
00071 [L1229] ADDNV    A=6 B=6 C=1 D=1537 
00072 [L1231] TNEW     A=7 B=0 C=4 D=4 
00073 [L1231] MULNV    A=8 B=3 C=5 D=773 
00074 [L1231] SUBNV    A=8 B=8 C=1 D=2049 
00075 [L1231] TSETB    A=8 B=7 C=1 D=1793 
00076 [L1231] MULNV    A=8 B=3 C=6 D=774 
00077 [L1231] ADDNV    A=8 B=8 C=1 D=2049 
00078 [L1231] TSETB    A=8 B=7 C=2 D=1794 
00079 [L1231] MULNV    A=8 B=3 C=7 D=775 
00080 [L1231] ADDNV    A=8 B=8 C=1 D=2049 
00081 [L1231] TSETB    A=8 B=7 C=3 D=1795 
00082 [L1232] TDUP     A=8 B=0 C=13 D=13 {'kind': 'table', 'value': {1: 'v2/soulHuntUI/r_label1.png', 2: 'v2/soulHuntUI/r_label2.png', 3: 'v2/soulHuntUI/r_label3.png'}}
00083 [L1233] KSHORT   A=9 B=0 C=5 D=5 5
00084 [L1233] ISGE     A=9 B=0 C=0 D=0 
00085 [L1233] JMP      A=9 B=128 C=2 D=32770 target=88
00086 [L1234] KSTR     A=9 B=0 C=14 D=14 'v2/soulHuntUI/r_label7.png'
00087 [L1234] TSETB    A=9 B=8 C=3 D=2051 
00088 [L1236] KSHORT   A=9 B=0 C=1 D=1 1
00089 [L1236] KSHORT   A=10 B=0 C=3 D=3 3
00090 [L1236] KSHORT   A=11 B=0 C=1 D=1 1
00091 [L1236] FORI     A=9 B=128 C=16 D=32784 target=108
00092 [L1237] GGET     A=13 B=0 C=6 D=6 'd_ms'
00093 [L1237] TGETS    A=13 B=13 C=7 D=3335 'd_u'
00094 [L1237] TGETS    A=13 B=13 C=15 D=3343 'createByStyle'
00095 [L1237] TDUP     A=14 B=0 C=16 D=16 {'kind': 'table', 'value': {}}
00096 [L1237] TGETV    A=15 B=8 C=12 D=2060 
00097 [L1237] TSETS    A=15 B=14 C=17 D=3601 'pic'
00098 [L1237] TGETV    A=15 B=7 C=12 D=1804 
00099 [L1237] TSETS    A=15 B=14 C=18 D=3602 'x'
00100 [L1237] TSETS    A=6 B=14 C=19 D=3603 'y'
00101 [L1237] CALL     A=13 B=2 C=2 D=514 
00102 [L1238] MOV      A=15 B=0 C=2 D=2 
00103 [L1238] TGETS    A=14 B=2 C=20 D=532 'addChild'
00104 [L1238] MOV      A=16 B=0 C=13 D=13 
00105 [L1238] KSHORT   A=17 B=0 C=1 D=1 1
00106 [L1238] CALL     A=14 B=1 C=4 D=260 
00107 [L1236] FORL     A=9 B=127 C=240 D=32752 target=92
00108 [L1241] UGET     A=9 B=0 C=2 D=2 g_self
00109 [L1241] TGETS    A=9 B=9 C=21 D=2325 'rank_data'
00110 [L1241] TGETS    A=9 B=9 C=22 D=2326 'my_data'
00111 [L1243] MOV      A=11 B=0 C=2 D=2 
00112 [L1243] TGETS    A=10 B=2 C=20 D=532 'addChild'
00113 [L1243] GGET     A=12 B=0 C=6 D=6 'd_ms'
00114 [L1243] TGETS    A=12 B=12 C=7 D=3079 'd_u'
00115 [L1243] TGETS    A=12 B=12 C=15 D=3087 'createByStyle'
00116 [L1243] TDUP     A=13 B=0 C=24 D=24 {'kind': 'table', 'value': {}}
00117 [L1243] KSHORT   A=14 B=0 C=5 D=5 5
00118 [L1243] ISGE     A=14 B=0 C=0 D=0 
00119 [L1243] JMP      A=14 B=128 C=2 D=32770 target=122
00120 [L1243] KSTR     A=14 B=0 C=23 D=23 'v2/soulHuntUI/r_label8.png'
00121 [L1243] JMP      A=15 B=128 C=1 D=32769 target=123
00122 [L1243] KSTR     A=14 B=0 C=25 D=25 'v2/soulHuntUI/r_label5.png'
00123 [L1243] TSETS    A=14 B=13 C=17 D=3345 'pic'
00124 [L1243] MULNV    A=14 B=3 C=8 D=776 
00125 [L1243] SUBNV    A=14 B=14 C=1 D=3585 
00126 [L1243] TSETS    A=14 B=13 C=18 D=3346 'x'
00127 [L1243] TSETS    A=5 B=13 C=19 D=3347 'y'
00128 [L1243] TDUP     A=14 B=0 C=26 D=26 {'kind': 'table', 'value': {1: 1, 2: 0.5}}
00129 [L1243] TSETS    A=14 B=13 C=27 D=3355 'anchor'
00130 [L1243] CALL     A=12 B=0 C=2 D=2 
00131 [L1243] CALLM    A=10 B=1 C=1 D=257 
00132 [L1244] MOV      A=11 B=0 C=2 D=2 
00133 [L1244] TGETS    A=10 B=2 C=20 D=532 'addChild'
00134 [L1244] GGET     A=12 B=0 C=6 D=6 'd_ms'
00135 [L1244] TGETS    A=12 B=12 C=7 D=3079 'd_u'
00136 [L1244] TGETS    A=12 B=12 C=15 D=3087 'createByStyle'
00137 [L1244] TDUP     A=13 B=0 C=28 D=28 {'kind': 'table', 'value': {'type': 'label', 'fontsize': 26}}
00138 [L1244] UGET     A=14 B=0 C=3 D=3 tostring
00139 [L1244] TGETS    A=15 B=9 C=29 D=2333 'soul_count'
00140 [L1244] IST      A=0 B=0 C=15 D=15 
00141 [L1244] JMP      A=16 B=128 C=1 D=32769 target=143
00142 [L1244] KSHORT   A=15 B=0 C=0 D=0 0
00143 [L1244] CALL     A=14 B=2 C=2 D=514 
00144 [L1244] TSETS    A=14 B=13 C=30 D=3358 'string'
00145 [L1244] MULNV    A=14 B=3 C=8 D=776 
00146 [L1244] SUBNV    A=14 B=14 C=1 D=3585 
00147 [L1244] TSETS    A=14 B=13 C=18 D=3346 'x'
00148 [L1244] TSETS    A=5 B=13 C=19 D=3347 'y'
00149 [L1244] TDUP     A=14 B=0 C=31 D=31 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00150 [L1244] TSETS    A=14 B=13 C=27 D=3355 'anchor'
00151 [L1244] TDUP     A=14 B=0 C=32 D=32 {'kind': 'table', 'value': {1: 250, 2: 250, 3: 150}}
00152 [L1244] TSETS    A=14 B=13 C=33 D=3361 'color'
00153 [L1244] CALL     A=12 B=0 C=2 D=2 
00154 [L1244] CALLM    A=10 B=1 C=1 D=257 
00155 [L1246] MOV      A=11 B=0 C=2 D=2 
00156 [L1246] TGETS    A=10 B=2 C=20 D=532 'addChild'
00157 [L1246] GGET     A=12 B=0 C=6 D=6 'd_ms'
00158 [L1246] TGETS    A=12 B=12 C=7 D=3079 'd_u'
00159 [L1246] TGETS    A=12 B=12 C=15 D=3087 'createByStyle'
00160 [L1246] TDUP     A=13 B=0 C=34 D=34 {'kind': 'table', 'value': {'pic': 'v2/soulHuntUI/r_label4.png'}}
00161 [L1246] MULNV    A=14 B=3 C=9 D=777 
00162 [L1246] ADDNV    A=14 B=14 C=1 D=3585 
00163 [L1246] TSETS    A=14 B=13 C=18 D=3346 'x'
00164 [L1246] TSETS    A=5 B=13 C=19 D=3347 'y'
00165 [L1246] TDUP     A=14 B=0 C=35 D=35 {'kind': 'table', 'value': {1: 1, 2: 0.5}}
00166 [L1246] TSETS    A=14 B=13 C=27 D=3355 'anchor'
00167 [L1246] CALL     A=12 B=0 C=2 D=2 
00168 [L1246] CALLM    A=10 B=1 C=1 D=257 
00169 [L1247] MOV      A=11 B=0 C=2 D=2 
00170 [L1247] TGETS    A=10 B=2 C=20 D=532 'addChild'
00171 [L1247] GGET     A=12 B=0 C=6 D=6 'd_ms'
00172 [L1247] TGETS    A=12 B=12 C=7 D=3079 'd_u'
00173 [L1247] TGETS    A=12 B=12 C=15 D=3087 'createByStyle'
00174 [L1247] TDUP     A=13 B=0 C=36 D=36 {'kind': 'table', 'value': {'type': 'label', 'fontsize': 26}}
00175 [L1247] TGETS    A=14 B=9 C=37 D=2341 'order'
00176 [L1247] ISF      A=0 B=0 C=14 D=14 
00177 [L1247] JMP      A=15 B=128 C=9 D=32777 target=187
00178 [L1247] TGETS    A=14 B=9 C=37 D=2341 'order'
00179 [L1247] KSHORT   A=15 B=0 C=0 D=0 0
00180 [L1247] ISGE     A=15 B=0 C=14 D=14 
00181 [L1247] JMP      A=14 B=128 C=5 D=32773 target=187
00182 [L1247] UGET     A=14 B=0 C=3 D=3 tostring
00183 [L1247] TGETS    A=15 B=9 C=37 D=2341 'order'
00184 [L1247] CALL     A=14 B=2 C=2 D=514 
00185 [L1247] IST      A=0 B=0 C=14 D=14 
00186 [L1247] JMP      A=15 B=128 C=5 D=32773 target=192
00187 [L1247] GGET     A=14 B=0 C=6 D=6 'd_ms'
00188 [L1247] TGETS    A=14 B=14 C=38 D=3622 'd_hz'
00189 [L1247] TGETS    A=14 B=14 C=39 D=3623 'gethz'
00190 [L1247] KSTR     A=15 B=0 C=40 D=40 'cross_doom_not_in_fsb'
00191 [L1247] CALL     A=14 B=2 C=2 D=514 
00192 [L1247] TSETS    A=14 B=13 C=30 D=3358 'string'
00193 [L1247] MULNV    A=14 B=3 C=9 D=777 
00194 [L1247] ADDNV    A=14 B=14 C=1 D=3585 
00195 [L1247] TSETS    A=14 B=13 C=18 D=3346 'x'
00196 [L1247] TSETS    A=5 B=13 C=19 D=3347 'y'
00197 [L1247] TDUP     A=14 B=0 C=41 D=41 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00198 [L1247] TSETS    A=14 B=13 C=27 D=3355 'anchor'
00199 [L1247] TDUP     A=14 B=0 C=42 D=42 {'kind': 'table', 'value': {1: 250, 2: 250, 3: 150}}
00200 [L1247] TSETS    A=14 B=13 C=33 D=3361 'color'
00201 [L1247] CALL     A=12 B=0 C=2 D=2 
00202 [L1247] CALLM    A=10 B=1 C=1 D=257 
00203 [L1249] ISNEN    A=0 B=0 C=10 D=10 1
00204 [L1249] JMP      A=10 B=128 C=13 D=32781 target=218
00205 [L1250] MOV      A=11 B=0 C=2 D=2 
00206 [L1250] TGETS    A=10 B=2 C=20 D=532 'addChild'
00207 [L1250] GGET     A=12 B=0 C=6 D=6 'd_ms'
00208 [L1250] TGETS    A=12 B=12 C=7 D=3079 'd_u'
00209 [L1250] TGETS    A=12 B=12 C=15 D=3087 'createByStyle'
00210 [L1250] TDUP     A=13 B=0 C=43 D=43 {'kind': 'table', 'value': {'pic': 'v2/soulHuntUI/r_label6.png'}}
00211 [L1250] MULNV    A=14 B=3 C=11 D=779 
00212 [L1250] ADDNV    A=14 B=14 C=1 D=3585 
00213 [L1250] TSETS    A=14 B=13 C=18 D=3346 'x'
00214 [L1250] TSETS    A=5 B=13 C=19 D=3347 'y'
00215 [L1250] CALL     A=12 B=0 C=2 D=2 
00216 [L1250] CALLM    A=10 B=1 C=1 D=257 
00217 [L1250] JMP      A=10 B=128 C=33 D=32801 target=251
00218 [L1251] ISNEN    A=0 B=0 C=12 D=12 3
00219 [L1251] JMP      A=10 B=128 C=31 D=32799 target=251
00220 [L1252] TGETS    A=10 B=9 C=44 D=2348 'had_prize'
00221 [L1252] ISF      A=0 B=0 C=10 D=10 
00222 [L1252] JMP      A=11 B=128 C=28 D=32796 target=251
00223 [L1259] FNEW     A=10 B=0 C=45 D=45 {'kind': 'proto', 'id': 63}
00224 [L1260] TDUP     A=11 B=0 C=46 D=46 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00225 [L1263] TDUP     A=12 B=0 C=47 D=47 {'kind': 'table', 'value': {'npic': 'v2/soulHuntUI/r_btn_prize1.png', 'spic': 'v2/soulHuntUI/r_btn_prize2.png'}}
00226 [L1264] MULNV    A=13 B=3 C=11 D=779 
00227 [L1264] ADDNV    A=13 B=13 C=1 D=3329 
00228 [L1264] TSETS    A=13 B=12 C=18 D=3090 'x'
00229 [L1264] TSETS    A=5 B=12 C=19 D=3091 'y'
00230 [L1264] TSETS    A=10 B=12 C=48 D=3120 'call_back'
00231 [L1264] TSETB    A=12 B=11 C=1 D=2817 
00232 [L1266] TNEW     A=12 B=0 C=0 D=0 
00233 [L1267] MOV      A=14 B=0 C=2 D=2 
00234 [L1267] TGETS    A=13 B=2 C=20 D=532 'addChild'
00235 [L1267] GGET     A=15 B=0 C=6 D=6 'd_ms'
00236 [L1267] TGETS    A=15 B=15 C=7 D=3847 'd_u'
00237 [L1267] TGETS    A=15 B=15 C=49 D=3889 'createMenu'
00238 [L1267] MOV      A=16 B=0 C=11 D=11 
00239 [L1267] MOV      A=17 B=0 C=12 D=12 
00240 [L1267] CALL     A=15 B=2 C=3 D=515 
00241 [L1267] KSHORT   A=16 B=0 C=5 D=5 5
00242 [L1267] CALL     A=13 B=1 C=4 D=260 
00243 [L1268] TGETS    A=13 B=9 C=50 D=2354 'had_got_prize'
00244 [L1268] ISF      A=0 B=0 C=13 D=13 
00245 [L1268] JMP      A=14 B=128 C=5 D=32773 target=251
00246 [L1269] GGET     A=13 B=0 C=6 D=6 'd_ms'
00247 [L1269] TGETS    A=13 B=13 C=7 D=3335 'd_u'
00248 [L1269] TGETS    A=13 B=13 C=51 D=3379 'grayMenuItem'
00249 [L1269] TGETB    A=14 B=12 C=1 D=3073 
00250 [L1269] CALL     A=13 B=1 C=2 D=258 
00251 [L1274] TDUP     A=10 B=0 C=52 D=52 {'kind': 'table', 'value': {}}
00252 [L1274] MULNV    A=11 B=3 C=13 D=781 
00253 [L1274] SUBNV    A=11 B=11 C=1 D=2817 
00254 [L1274] UGET     A=12 B=0 C=4 D=4 scrSize
00255 [L1274] TGETS    A=12 B=12 C=11 D=3083 'width'
00256 [L1274] MULVV    A=11 B=11 C=12 D=2828 
00257 [L1274] TSETS    A=11 B=10 C=18 D=2578 'x'
00258 [L1274] MULNV    A=11 B=4 C=14 D=1038 
00259 [L1274] SUBNV    A=11 B=11 C=1 D=2817 
00260 [L1274] UGET     A=12 B=0 C=4 D=4 scrSize
00261 [L1274] TGETS    A=12 B=12 C=12 D=3084 'height'
00262 [L1274] MULVV    A=11 B=11 C=12 D=2828 
00263 [L1274] TSETS    A=11 B=10 C=19 D=2579 'y'
00264 [L1274] MULNV    A=11 B=3 C=15 D=783 
00265 [L1274] UGET     A=12 B=0 C=4 D=4 scrSize
00266 [L1274] TGETS    A=12 B=12 C=11 D=3083 'width'
00267 [L1274] MULVV    A=11 B=11 C=12 D=2828 
00268 [L1274] TSETS    A=11 B=10 C=11 D=2571 'width'
00269 [L1274] MULNV    A=11 B=4 C=15 D=1039 
00270 [L1274] UGET     A=12 B=0 C=4 D=4 scrSize
00271 [L1274] TGETS    A=12 B=12 C=12 D=3084 'height'
00272 [L1274] MULVV    A=11 B=11 C=12 D=2828 
00273 [L1274] TSETS    A=11 B=10 C=12 D=2572 'height'
00274 [L1275] UGET     A=11 B=0 C=5 D=5 CCSizeMake
00275 [L1275] TGETS    A=12 B=10 C=11 D=2571 'width'
00276 [L1275] TGETS    A=13 B=10 C=12 D=2572 'height'
00277 [L1275] DIVVN    A=13 B=13 C=16 D=3344 
00278 [L1275] CALL     A=11 B=2 C=3 D=515 
00279 [L1276] GGET     A=12 B=0 C=6 D=6 'd_ms'
00280 [L1276] TGETS    A=12 B=12 C=53 D=3125 'd_tableView'
00281 [L1276] TGETS    A=12 B=12 C=54 D=3126 'tableView'
00282 [L1276] MOV      A=13 B=0 C=2 D=2 
00283 [L1276] MOV      A=14 B=0 C=10 D=10 
00284 [L1276] CALL     A=12 B=2 C=3 D=515 
00285 [L1277] GGET     A=13 B=0 C=55 D=55 'getRankDataSource'
00286 [L1277] UGET     A=14 B=0 C=2 D=2 g_self
00287 [L1277] TGETS    A=14 B=14 C=21 D=3605 'rank_data'
00288 [L1277] TGETS    A=14 B=14 C=56 D=3640 'top_list'
00289 [L1277] MOV      A=15 B=0 C=11 D=11 
00290 [L1277] CALL     A=13 B=2 C=3 D=515 
00291 [L1278] MOV      A=15 B=0 C=12 D=12 
00292 [L1278] TGETS    A=14 B=12 C=57 D=3129 'startScroll'
00293 [L1278] CALL     A=14 B=1 C=2 D=258 
00294 [L1279] MOV      A=15 B=0 C=12 D=12 
00295 [L1279] TGETS    A=14 B=12 C=58 D=3130 'setDataSource'
00296 [L1279] MOV      A=16 B=0 C=13 D=13 
00297 [L1279] CALL     A=14 B=1 C=3 D=259 
00298 [L1279] UCLO     A=6 B=128 C=64 D=32832 target=363
00299 [L1280] ISEQN    A=0 B=0 C=2 D=2 4
00300 [L1280] JMP      A=6 B=128 C=2 D=32770 target=303
00301 [L1280] ISNEN    A=0 B=0 C=3 D=3 5
00302 [L1280] JMP      A=6 B=128 C=60 D=32828 target=363
00303 [L1281] ISNEN    A=0 B=0 C=2 D=2 4
00304 [L1281] JMP      A=6 B=128 C=4 D=32772 target=309
00305 [L1281] UGET     A=6 B=0 C=2 D=2 g_self
00306 [L1281] TGETS    A=6 B=6 C=59 D=1595 'DayPrize'
00307 [L1281] IST      A=0 B=0 C=6 D=6 
00308 [L1281] JMP      A=7 B=128 C=2 D=32770 target=311
00309 [L1281] UGET     A=6 B=0 C=2 D=2 g_self
00310 [L1281] TGETS    A=6 B=6 C=60 D=1596 'WeekPrize'
00311 [L1282] TDUP     A=7 B=0 C=61 D=61 {'kind': 'table', 'value': {}}
00312 [L1282] MULNV    A=8 B=3 C=13 D=781 
00313 [L1282] SUBNV    A=8 B=8 C=1 D=2049 
00314 [L1282] UGET     A=9 B=0 C=4 D=4 scrSize
00315 [L1282] TGETS    A=9 B=9 C=11 D=2315 'width'
00316 [L1282] MULVV    A=8 B=8 C=9 D=2057 
00317 [L1282] TSETS    A=8 B=7 C=18 D=1810 'x'
00318 [L1282] MULNV    A=8 B=4 C=14 D=1038 
00319 [L1282] SUBNV    A=8 B=8 C=1 D=2049 
00320 [L1282] UGET     A=9 B=0 C=4 D=4 scrSize
00321 [L1282] TGETS    A=9 B=9 C=12 D=2316 'height'
00322 [L1282] MULVV    A=8 B=8 C=9 D=2057 
00323 [L1282] TSETS    A=8 B=7 C=19 D=1811 'y'
00324 [L1282] MULNV    A=8 B=3 C=15 D=783 
00325 [L1282] UGET     A=9 B=0 C=4 D=4 scrSize
00326 [L1282] TGETS    A=9 B=9 C=11 D=2315 'width'
00327 [L1282] MULVV    A=8 B=8 C=9 D=2057 
00328 [L1282] TSETS    A=8 B=7 C=11 D=1803 'width'
00329 [L1282] MULNV    A=8 B=4 C=15 D=1039 
00330 [L1282] UGET     A=9 B=0 C=4 D=4 scrSize
00331 [L1282] TGETS    A=9 B=9 C=12 D=2316 'height'
00332 [L1282] MULVV    A=8 B=8 C=9 D=2057 
00333 [L1282] TSETS    A=8 B=7 C=12 D=1804 'height'
00334 [L1283] UGET     A=8 B=0 C=5 D=5 CCSizeMake
00335 [L1283] TGETS    A=9 B=7 C=11 D=1803 'width'
00336 [L1283] TGETS    A=10 B=7 C=12 D=1804 'height'
00337 [L1283] DIVVN    A=10 B=10 C=17 D=2577 
00338 [L1283] CALL     A=8 B=2 C=3 D=515 
00339 [L1284] UGET     A=9 B=0 C=6 D=6 CCRectMake
00340 [L1284] TGETS    A=10 B=7 C=18 D=1810 'x'
00341 [L1284] TGETS    A=11 B=7 C=19 D=1811 'y'
00342 [L1284] TGETS    A=12 B=7 C=11 D=1803 'width'
00343 [L1284] TGETS    A=13 B=7 C=12 D=1804 'height'
00344 [L1284] CALL     A=9 B=2 C=5 D=517 
00345 [L1285] GGET     A=10 B=0 C=6 D=6 'd_ms'
00346 [L1285] TGETS    A=10 B=10 C=53 D=2613 'd_tableView'
00347 [L1285] TGETS    A=10 B=10 C=54 D=2614 'tableView'
00348 [L1285] MOV      A=11 B=0 C=2 D=2 
00349 [L1285] MOV      A=12 B=0 C=7 D=7 
00350 [L1285] CALL     A=10 B=2 C=3 D=515 
00351 [L1286] GGET     A=11 B=0 C=62 D=62 'getRankPrizeDataSource'
00352 [L1286] MOV      A=12 B=0 C=6 D=6 
00353 [L1286] MOV      A=13 B=0 C=8 D=8 
00354 [L1286] MOV      A=14 B=0 C=9 D=9 
00355 [L1286] CALL     A=11 B=2 C=4 D=516 
00356 [L1287] MOV      A=13 B=0 C=10 D=10 
00357 [L1287] TGETS    A=12 B=10 C=58 D=2618 'setDataSource'
00358 [L1287] MOV      A=14 B=0 C=11 D=11 
00359 [L1287] CALL     A=12 B=1 C=3 D=259 
00360 [L1288] MOV      A=13 B=0 C=10 D=10 
00361 [L1288] TGETS    A=12 B=10 C=57 D=2617 'startScroll'
00362 [L1288] CALL     A=12 B=1 C=2 D=258 
00363 [L1290] RET0     A=0 B=0 C=1 D=1 
00364 [L1290] RET0     A=0 B=0 C=1 D=1 
00365 [L1290] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto65 offset=0x98c4 source_lines=1292-1299 params=0
UPVALUES ['h_o_t']
00001 [L1293] TNEW     A=0 B=0 C=0 D=0 
00002 [L1294] UGET     A=1 B=0 C=0 D=0 h_o_t
00003 [L1294] TGETS    A=1 B=1 C=1 D=257 'enter_map'
00004 [L1294] TSETS    A=1 B=0 C=0 D=0 'flag'
00005 [L1295] KSHORT   A=1 B=0 C=0 D=0 0
00006 [L1295] TSETS    A=1 B=0 C=2 D=2 'count'
00007 [L1296] KSHORT   A=1 B=0 C=0 D=0 0
00008 [L1296] TSETS    A=1 B=0 C=3 D=3 'index'
00009 [L1298] GGET     A=1 B=0 C=4 D=4 'd_ms'
00010 [L1298] TGETS    A=1 B=1 C=5 D=261 'd_u'
00011 [L1298] TGETS    A=1 B=1 C=6 D=262 'main_server_send_msg'
00012 [L1298] GGET     A=2 B=0 C=4 D=4 'd_ms'
00013 [L1298] TGETS    A=2 B=2 C=7 D=519 'd_msg_def'
00014 [L1298] TGETS    A=2 B=2 C=8 D=520 'gscl_msg_id'
00015 [L1298] TGETS    A=2 B=2 C=9 D=521 'msg_hunt_soul'
00016 [L1298] MOV      A=3 B=0 C=0 D=0 
00017 [L1298] CALL     A=1 B=1 C=3 D=259 
00018 [L1299] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto66 offset=0x999f source_lines=1301-1308 params=0
UPVALUES ['h_o_t']
00001 [L1302] TNEW     A=0 B=0 C=0 D=0 
00002 [L1303] UGET     A=1 B=0 C=0 D=0 h_o_t
00003 [L1303] TGETS    A=1 B=1 C=1 D=257 'enter_store'
00004 [L1303] TSETS    A=1 B=0 C=0 D=0 'flag'
00005 [L1304] KSHORT   A=1 B=0 C=0 D=0 0
00006 [L1304] TSETS    A=1 B=0 C=2 D=2 'count'
00007 [L1305] KSHORT   A=1 B=0 C=0 D=0 0
00008 [L1305] TSETS    A=1 B=0 C=3 D=3 'index'
00009 [L1307] GGET     A=1 B=0 C=4 D=4 'd_ms'
00010 [L1307] TGETS    A=1 B=1 C=5 D=261 'd_u'
00011 [L1307] TGETS    A=1 B=1 C=6 D=262 'main_server_send_msg'
00012 [L1307] GGET     A=2 B=0 C=4 D=4 'd_ms'
00013 [L1307] TGETS    A=2 B=2 C=7 D=519 'd_msg_def'
00014 [L1307] TGETS    A=2 B=2 C=8 D=520 'gscl_msg_id'
00015 [L1307] TGETS    A=2 B=2 C=9 D=521 'msg_hunt_soul'
00016 [L1307] MOV      A=3 B=0 C=0 D=0 
00017 [L1307] CALL     A=1 B=1 C=3 D=259 
00018 [L1308] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto67 offset=0x9a7c source_lines=1311-1331 params=1
UPVALUES ['h_o_t']
00001 [L1312] ISF      A=0 B=0 C=0 D=0 
00002 [L1312] JMP      A=1 B=128 C=7 D=32775 target=10
00003 [L1312] KSHORT   A=1 B=0 C=3 D=3 3
00004 [L1312] ISLE     A=0 B=0 C=1 D=1 
00005 [L1312] JMP      A=1 B=128 C=4 D=32772 target=10
00006 [L1312] ISEQN    A=0 B=0 C=0 D=0 6
00007 [L1312] JMP      A=1 B=128 C=2 D=32770 target=10
00008 [L1312] ISNEN    A=0 B=0 C=1 D=1 7
00009 [L1312] JMP      A=1 B=128 C=41 D=32809 target=51
00010 [L1313] TNEW     A=1 B=0 C=0 D=0 
00011 [L1314] UGET     A=2 B=0 C=0 D=0 h_o_t
00012 [L1314] TGETS    A=2 B=2 C=1 D=513 'query_day_top'
00013 [L1314] TSETS    A=2 B=1 C=0 D=256 'flag'
00014 [L1315] ISNEN    A=0 B=0 C=2 D=2 2
00015 [L1315] JMP      A=2 B=128 C=4 D=32772 target=20
00016 [L1316] UGET     A=2 B=0 C=0 D=0 h_o_t
00017 [L1316] TGETS    A=2 B=2 C=2 D=514 'query_week_top'
00018 [L1316] TSETS    A=2 B=1 C=0 D=256 'flag'
00019 [L1316] JMP      A=2 B=128 C=17 D=32785 target=37
00020 [L1317] ISNEN    A=0 B=0 C=3 D=3 3
00021 [L1317] JMP      A=2 B=128 C=4 D=32772 target=26
00022 [L1318] UGET     A=2 B=0 C=0 D=0 h_o_t
00023 [L1318] TGETS    A=2 B=2 C=3 D=515 'query_last_week_top'
00024 [L1318] TSETS    A=2 B=1 C=0 D=256 'flag'
00025 [L1318] JMP      A=2 B=128 C=11 D=32779 target=37
00026 [L1319] ISNEN    A=0 B=0 C=0 D=0 6
00027 [L1319] JMP      A=2 B=128 C=4 D=32772 target=32
00028 [L1320] UGET     A=2 B=0 C=0 D=0 h_o_t
00029 [L1320] TGETS    A=2 B=2 C=4 D=516 'query_history_day_top'
00030 [L1320] TSETS    A=2 B=1 C=0 D=256 'flag'
00031 [L1320] JMP      A=2 B=128 C=5 D=32773 target=37
00032 [L1321] ISNEN    A=0 B=0 C=1 D=1 7
00033 [L1321] JMP      A=2 B=128 C=3 D=32771 target=37
00034 [L1322] UGET     A=2 B=0 C=0 D=0 h_o_t
00035 [L1322] TGETS    A=2 B=2 C=5 D=517 'query_history_week_top'
00036 [L1322] TSETS    A=2 B=1 C=0 D=256 'flag'
00037 [L1324] KSHORT   A=2 B=0 C=0 D=0 0
00038 [L1324] TSETS    A=2 B=1 C=6 D=262 'count'
00039 [L1325] KSHORT   A=2 B=0 C=0 D=0 0
00040 [L1325] TSETS    A=2 B=1 C=7 D=263 'index'
00041 [L1327] GGET     A=2 B=0 C=8 D=8 'd_ms'
00042 [L1327] TGETS    A=2 B=2 C=9 D=521 'd_u'
00043 [L1327] TGETS    A=2 B=2 C=10 D=522 'main_server_send_msg'
00044 [L1327] GGET     A=3 B=0 C=8 D=8 'd_ms'
00045 [L1327] TGETS    A=3 B=3 C=11 D=779 'd_msg_def'
00046 [L1327] TGETS    A=3 B=3 C=12 D=780 'gscl_msg_id'
00047 [L1327] TGETS    A=3 B=3 C=13 D=781 'msg_hunt_soul'
00048 [L1327] MOV      A=4 B=0 C=1 D=1 
00049 [L1327] CALL     A=2 B=1 C=3 D=259 
00050 [L1327] JMP      A=1 B=128 C=3 D=32771 target=54
00051 [L1329] GGET     A=1 B=0 C=14 D=14 'showRankDetail'
00052 [L1329] MOV      A=2 B=0 C=0 D=0 
00053 [L1329] CALL     A=1 B=1 C=2 D=258 
00054 [L1331] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto68 offset=0x9c78 source_lines=1333-1340 params=0
UPVALUES ['h_o_t']
00001 [L1334] TNEW     A=0 B=0 C=0 D=0 
00002 [L1335] UGET     A=1 B=0 C=0 D=0 h_o_t
00003 [L1335] TGETS    A=1 B=1 C=1 D=257 'take_week_prize'
00004 [L1335] TSETS    A=1 B=0 C=0 D=0 'flag'
00005 [L1336] KSHORT   A=1 B=0 C=0 D=0 0
00006 [L1336] TSETS    A=1 B=0 C=2 D=2 'count'
00007 [L1337] KSHORT   A=1 B=0 C=0 D=0 0
00008 [L1337] TSETS    A=1 B=0 C=3 D=3 'index'
00009 [L1339] GGET     A=1 B=0 C=4 D=4 'd_ms'
00010 [L1339] TGETS    A=1 B=1 C=5 D=261 'd_u'
00011 [L1339] TGETS    A=1 B=1 C=6 D=262 'main_server_send_msg'
00012 [L1339] GGET     A=2 B=0 C=4 D=4 'd_ms'
00013 [L1339] TGETS    A=2 B=2 C=7 D=519 'd_msg_def'
00014 [L1339] TGETS    A=2 B=2 C=8 D=520 'gscl_msg_id'
00015 [L1339] TGETS    A=2 B=2 C=9 D=521 'msg_hunt_soul'
00016 [L1339] MOV      A=3 B=0 C=0 D=0 
00017 [L1339] CALL     A=1 B=1 C=3 D=259 
00018 [L1340] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto69 offset=0x9d59 source_lines=1342-1349 params=0
UPVALUES ['h_o_t']
00001 [L1343] TNEW     A=0 B=0 C=0 D=0 
00002 [L1344] UGET     A=1 B=0 C=0 D=0 h_o_t
00003 [L1344] TGETS    A=1 B=1 C=1 D=257 'flush_soul'
00004 [L1344] TSETS    A=1 B=0 C=0 D=0 'flag'
00005 [L1345] KSHORT   A=1 B=0 C=0 D=0 0
00006 [L1345] TSETS    A=1 B=0 C=2 D=2 'count'
00007 [L1346] KSHORT   A=1 B=0 C=0 D=0 0
00008 [L1346] TSETS    A=1 B=0 C=3 D=3 'index'
00009 [L1348] GGET     A=1 B=0 C=4 D=4 'd_ms'
00010 [L1348] TGETS    A=1 B=1 C=5 D=261 'd_u'
00011 [L1348] TGETS    A=1 B=1 C=6 D=262 'main_server_send_msg'
00012 [L1348] GGET     A=2 B=0 C=4 D=4 'd_ms'
00013 [L1348] TGETS    A=2 B=2 C=7 D=519 'd_msg_def'
00014 [L1348] TGETS    A=2 B=2 C=8 D=520 'gscl_msg_id'
00015 [L1348] TGETS    A=2 B=2 C=9 D=521 'msg_hunt_soul'
00016 [L1348] MOV      A=3 B=0 C=0 D=0 
00017 [L1348] CALL     A=1 B=1 C=3 D=259 
00018 [L1349] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto70 offset=0x9e35 source_lines=1351-1358 params=0
UPVALUES ['h_o_t']
00001 [L1352] TNEW     A=0 B=0 C=0 D=0 
00002 [L1353] UGET     A=1 B=0 C=0 D=0 h_o_t
00003 [L1353] TGETS    A=1 B=1 C=1 D=257 'flush_store'
00004 [L1353] TSETS    A=1 B=0 C=0 D=0 'flag'
00005 [L1354] KSHORT   A=1 B=0 C=0 D=0 0
00006 [L1354] TSETS    A=1 B=0 C=2 D=2 'count'
00007 [L1355] KSHORT   A=1 B=0 C=0 D=0 0
00008 [L1355] TSETS    A=1 B=0 C=3 D=3 'index'
00009 [L1357] GGET     A=1 B=0 C=4 D=4 'd_ms'
00010 [L1357] TGETS    A=1 B=1 C=5 D=261 'd_u'
00011 [L1357] TGETS    A=1 B=1 C=6 D=262 'main_server_send_msg'
00012 [L1357] GGET     A=2 B=0 C=4 D=4 'd_ms'
00013 [L1357] TGETS    A=2 B=2 C=7 D=519 'd_msg_def'
00014 [L1357] TGETS    A=2 B=2 C=8 D=520 'gscl_msg_id'
00015 [L1357] TGETS    A=2 B=2 C=9 D=521 'msg_hunt_soul'
00016 [L1357] MOV      A=3 B=0 C=0 D=0 
00017 [L1357] CALL     A=1 B=1 C=3 D=259 
00018 [L1358] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto71 offset=0x9f12 source_lines=1360-1367 params=1
UPVALUES ['h_o_t']
00001 [L1361] TNEW     A=1 B=0 C=0 D=0 
00002 [L1362] UGET     A=2 B=0 C=0 D=0 h_o_t
00003 [L1362] TGETS    A=2 B=2 C=1 D=513 'convert_energy'
00004 [L1362] TSETS    A=2 B=1 C=0 D=256 'flag'
00005 [L1363] TSETS    A=0 B=1 C=2 D=258 'count'
00006 [L1364] KSHORT   A=2 B=0 C=0 D=0 0
00007 [L1364] TSETS    A=2 B=1 C=3 D=259 'index'
00008 [L1366] GGET     A=2 B=0 C=4 D=4 'd_ms'
00009 [L1366] TGETS    A=2 B=2 C=5 D=517 'd_u'
00010 [L1366] TGETS    A=2 B=2 C=6 D=518 'main_server_send_msg'
00011 [L1366] GGET     A=3 B=0 C=4 D=4 'd_ms'
00012 [L1366] TGETS    A=3 B=3 C=7 D=775 'd_msg_def'
00013 [L1366] TGETS    A=3 B=3 C=8 D=776 'gscl_msg_id'
00014 [L1366] TGETS    A=3 B=3 C=9 D=777 'msg_hunt_soul'
00015 [L1366] MOV      A=4 B=0 C=1 D=1 
00016 [L1366] CALL     A=2 B=1 C=3 D=259 
00017 [L1367] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto72 offset=0x9ff5 source_lines=1369-1376 params=2
UPVALUES ['h_o_t']
00001 [L1370] TNEW     A=2 B=0 C=0 D=0 
00002 [L1371] UGET     A=3 B=0 C=0 D=0 h_o_t
00003 [L1371] TGETS    A=3 B=3 C=1 D=769 'buy_store'
00004 [L1371] TSETS    A=3 B=2 C=0 D=512 'flag'
00005 [L1372] TSETS    A=1 B=2 C=2 D=514 'count'
00006 [L1373] TSETS    A=0 B=2 C=3 D=515 'index'
00007 [L1375] GGET     A=3 B=0 C=4 D=4 'd_ms'
00008 [L1375] TGETS    A=3 B=3 C=5 D=773 'd_u'
00009 [L1375] TGETS    A=3 B=3 C=6 D=774 'main_server_send_msg'
00010 [L1375] GGET     A=4 B=0 C=4 D=4 'd_ms'
00011 [L1375] TGETS    A=4 B=4 C=7 D=1031 'd_msg_def'
00012 [L1375] TGETS    A=4 B=4 C=8 D=1032 'gscl_msg_id'
00013 [L1375] TGETS    A=4 B=4 C=9 D=1033 'msg_hunt_soul'
00014 [L1375] MOV      A=5 B=0 C=2 D=2 
00015 [L1375] CALL     A=3 B=1 C=3 D=259 
00016 [L1376] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto73 offset=0xa0d5 source_lines=1378-1381 params=0
UPVALUES ['g_soulHuntUI']
00001 [L1379] TNEW     A=0 B=0 C=0 D=0 
00002 [L1379] USETV    A=0 B=0 C=0 D=0 g_soulHuntUI
00003 [L1380] GGET     A=0 B=0 C=0 D=0 'd_ms'
00004 [L1380] TGETS    A=0 B=0 C=1 D=1 'd_activityUI'
00005 [L1380] TGETS    A=0 B=0 C=2 D=2 'returnBack'
00006 [L1380] CALL     A=0 B=1 C=1 D=257 
00007 [L1381] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto74 offset=0xa131 source_lines=1383-1385 params=0
UPVALUES ['g_soulHuntUI']
00001 [L1384] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L1384] TGETS    A=0 B=0 C=1 D=1 'd_newbieManualUI'
00003 [L1384] TGETS    A=0 B=0 C=2 D=2 'show'
00004 [L1384] UGET     A=1 B=0 C=0 D=0 g_soulHuntUI
00005 [L1384] TGETS    A=1 B=1 C=3 D=259 'main_layer'
00006 [L1384] KPRI     A=2 B=0 C=2 D=2 
00007 [L1384] KSHORT   A=3 B=0 C=6 D=6 6
00008 [L1384] CALL     A=0 B=1 C=4 D=260 
00009 [L1385] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto75 offset=0xa1a1 source_lines=1387-1414 params=2
UPVALUES []
00001 [L1388] TDUP     A=2 B=0 C=0 D=0 {'kind': 'table', 'value': {}}
00002 [L1388] TGETB    A=3 B=1 C=2 D=258 
00003 [L1388] TGETB    A=4 B=1 C=1 D=257 
00004 [L1388] SUBVV    A=3 B=3 C=4 D=772 
00005 [L1388] TSETS    A=3 B=2 C=1 D=513 'A'
00006 [L1388] TGETB    A=3 B=0 C=1 D=1 
00007 [L1388] TGETB    A=4 B=0 C=2 D=2 
00008 [L1388] SUBVV    A=3 B=3 C=4 D=772 
00009 [L1388] TSETS    A=3 B=2 C=2 D=514 'B'
00010 [L1388] TGETB    A=3 B=0 C=1 D=1 
00011 [L1388] TGETB    A=4 B=1 C=1 D=257 
00012 [L1388] TGETB    A=5 B=1 C=2 D=258 
00013 [L1388] SUBVV    A=4 B=4 C=5 D=1029 
00014 [L1388] MULVV    A=3 B=3 C=4 D=772 
00015 [L1388] TGETB    A=4 B=1 C=1 D=257 
00016 [L1388] TGETB    A=5 B=0 C=2 D=2 
00017 [L1388] TGETB    A=6 B=0 C=1 D=1 
00018 [L1388] SUBVV    A=5 B=5 C=6 D=1286 
00019 [L1388] MULVV    A=4 B=4 C=5 D=1029 
00020 [L1388] ADDVV    A=3 B=3 C=4 D=772 
00021 [L1388] TSETS    A=3 B=2 C=3 D=515 'C'
00022 [L1389] TDUP     A=3 B=0 C=4 D=4 {'kind': 'table', 'value': {}}
00023 [L1389] TGETB    A=4 B=0 C=1 D=1 
00024 [L1389] TGETB    A=5 B=0 C=2 D=2 
00025 [L1389] SUBVV    A=4 B=4 C=5 D=1029 
00026 [L1389] TSETS    A=4 B=3 C=1 D=769 'A'
00027 [L1389] TGETB    A=4 B=1 C=1 D=257 
00028 [L1389] TGETB    A=5 B=1 C=2 D=258 
00029 [L1389] SUBVV    A=4 B=4 C=5 D=1029 
00030 [L1389] TSETS    A=4 B=3 C=2 D=770 'B'
00031 [L1389] TGETB    A=4 B=0 C=0 D=0 
00032 [L1389] TGETB    A=5 B=0 C=2 D=2 
00033 [L1389] TGETB    A=6 B=0 C=1 D=1 
00034 [L1389] SUBVV    A=5 B=5 C=6 D=1286 
00035 [L1389] MULVV    A=4 B=4 C=5 D=1029 
00036 [L1389] TGETB    A=5 B=1 C=0 D=256 
00037 [L1389] TGETB    A=6 B=1 C=2 D=258 
00038 [L1389] TGETB    A=7 B=1 C=1 D=257 
00039 [L1389] SUBVV    A=6 B=6 C=7 D=1543 
00040 [L1389] MULVV    A=5 B=5 C=6 D=1286 
00041 [L1389] ADDVV    A=4 B=4 C=5 D=1029 
00042 [L1389] TSETS    A=4 B=3 C=3 D=771 'C'
00043 [L1390] TGETB    A=4 B=1 C=2 D=258 
00044 [L1390] TGETB    A=5 B=1 C=1 D=257 
00045 [L1390] ISNEV    A=4 B=0 C=5 D=5 
00046 [L1390] JMP      A=4 B=128 C=10 D=32778 target=57
00047 [L1391] TGETS    A=4 B=3 C=3 D=771 'C'
00048 [L1391] MULNV    A=4 B=4 C=0 D=1024 
00049 [L1391] TGETS    A=5 B=3 C=1 D=769 'A'
00050 [L1391] DIVVV    A=4 B=4 C=5 D=1029 
00051 [L1391] TGETS    A=5 B=2 C=3 D=515 'C'
00052 [L1391] MULNV    A=5 B=5 C=0 D=1280 
00053 [L1391] TGETS    A=6 B=2 C=2 D=514 'B'
00054 [L1391] DIVVV    A=5 B=5 C=6 D=1286 
00055 [L1391] RET      A=4 B=0 C=3 D=3 
00056 [L1391] JMP      A=4 B=128 C=57 D=32825 target=114
00057 [L1392] TGETB    A=4 B=0 C=2 D=2 
00058 [L1392] TGETB    A=5 B=0 C=1 D=1 
00059 [L1392] ISNEV    A=4 B=0 C=5 D=5 
00060 [L1392] JMP      A=4 B=128 C=10 D=32778 target=71
00061 [L1393] TGETS    A=4 B=2 C=3 D=515 'C'
00062 [L1393] MULNV    A=4 B=4 C=0 D=1024 
00063 [L1393] TGETS    A=5 B=2 C=1 D=513 'A'
00064 [L1393] DIVVV    A=4 B=4 C=5 D=1029 
00065 [L1393] TGETS    A=5 B=3 C=3 D=771 'C'
00066 [L1393] MULNV    A=5 B=5 C=0 D=1280 
00067 [L1393] TGETS    A=6 B=3 C=2 D=770 'B'
00068 [L1393] DIVVV    A=5 B=5 C=6 D=1286 
00069 [L1393] RET      A=4 B=0 C=3 D=3 
00070 [L1393] JMP      A=4 B=128 C=43 D=32811 target=114
00071 [L1395] TGETS    A=4 B=2 C=1 D=513 'A'
00072 [L1395] TGETS    A=5 B=3 C=1 D=769 'A'
00073 [L1396] TGETS    A=6 B=2 C=1 D=513 'A'
00074 [L1396] MULVV    A=6 B=6 C=5 D=1541 
00075 [L1396] TSETS    A=6 B=2 C=1 D=513 'A'
00076 [L1397] TGETS    A=6 B=2 C=2 D=514 'B'
00077 [L1397] MULVV    A=6 B=6 C=5 D=1541 
00078 [L1397] TSETS    A=6 B=2 C=2 D=514 'B'
00079 [L1398] TGETS    A=6 B=2 C=3 D=515 'C'
00080 [L1398] MULVV    A=6 B=6 C=5 D=1541 
00081 [L1398] TSETS    A=6 B=2 C=3 D=515 'C'
00082 [L1400] TGETS    A=6 B=3 C=1 D=769 'A'
00083 [L1400] MULVV    A=6 B=6 C=4 D=1540 
00084 [L1400] TSETS    A=6 B=3 C=1 D=769 'A'
00085 [L1401] TGETS    A=6 B=3 C=2 D=770 'B'
00086 [L1401] MULVV    A=6 B=6 C=4 D=1540 
00087 [L1401] TSETS    A=6 B=3 C=2 D=770 'B'
00088 [L1402] TGETS    A=6 B=3 C=3 D=771 'C'
00089 [L1402] MULVV    A=6 B=6 C=4 D=1540 
00090 [L1402] TSETS    A=6 B=3 C=2 D=770 'B'
00091 [L1404] TDUP     A=6 B=0 C=5 D=5 {'kind': 'table', 'value': {'A': 0}}
00092 [L1407] TGETS    A=7 B=3 C=2 D=770 'B'
00093 [L1407] TGETS    A=8 B=2 C=2 D=514 'B'
00094 [L1407] SUBVV    A=7 B=7 C=8 D=1800 
00095 [L1407] TSETS    A=7 B=6 C=2 D=1538 'B'
00096 [L1408] TGETS    A=7 B=3 C=3 D=771 'C'
00097 [L1408] TGETS    A=8 B=2 C=3 D=515 'C'
00098 [L1408] SUBVV    A=7 B=7 C=8 D=1800 
00099 [L1408] TSETS    A=7 B=6 C=3 D=1539 'C'
00100 [L1410] TGETS    A=7 B=6 C=3 D=1539 'C'
00101 [L1410] MULNV    A=7 B=7 C=0 D=1792 
00102 [L1410] TGETS    A=8 B=6 C=2 D=1538 'B'
00103 [L1410] DIVVV    A=7 B=7 C=8 D=1800 
00104 [L1411] TGETS    A=8 B=2 C=3 D=515 'C'
00105 [L1411] TGETS    A=9 B=2 C=2 D=514 'B'
00106 [L1411] MULVV    A=9 B=9 C=7 D=2311 
00107 [L1411] ADDVV    A=8 B=8 C=9 D=2057 
00108 [L1411] MULNV    A=8 B=8 C=0 D=2048 
00109 [L1411] TGETS    A=9 B=2 C=1 D=513 'A'
00110 [L1411] DIVVV    A=8 B=8 C=9 D=2057 
00111 [L1412] MOV      A=9 B=0 C=8 D=8 
00112 [L1412] MOV      A=10 B=0 C=7 D=7 
00113 [L1412] RET      A=9 B=0 C=3 D=3 
00114 [L1414] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto76 offset=0xa436 source_lines=1432-1436 params=3
UPVALUES ['layer']
00001 [L1433] GGET     A=3 B=0 C=0 D=0 'd_ms'
00002 [L1433] TGETS    A=3 B=3 C=1 D=769 'd_file'
00003 [L1433] TGETS    A=3 B=3 C=2 D=770 'set'
00004 [L1433] KSTR     A=4 B=0 C=3 D=3 'soul_hunt_guide'
00005 [L1433] KSTR     A=5 B=0 C=4 D=4 '1'
00006 [L1433] GGET     A=6 B=0 C=0 D=0 'd_ms'
00007 [L1433] TGETS    A=6 B=6 C=5 D=1541 'd_mainUI'
00008 [L1433] TGETS    A=6 B=6 C=6 D=1542 'g_playerInfo'
00009 [L1433] TGETS    A=6 B=6 C=7 D=1543 'role_id'
00010 [L1433] CALL     A=3 B=1 C=4 D=260 
00011 [L1434] GGET     A=3 B=0 C=0 D=0 'd_ms'
00012 [L1434] TGETS    A=3 B=3 C=8 D=776 'd_u'
00013 [L1434] TGETS    A=3 B=3 C=9 D=777 'remove'
00014 [L1434] UGET     A=4 B=0 C=0 D=0 layer
00015 [L1434] CALL     A=3 B=1 C=2 D=258 
00016 [L1435] KPRI     A=3 B=0 C=2 D=2 
00017 [L1435] RET1     A=3 B=0 C=2 D=2 

FUNCTION proto77 offset=0xa500 source_lines=1416-1490 params=0
UPVALUES ['g_self', 'g_soulHuntUI', 'tags', 'CCRenderTexture', 'scrSize', 'CCPointMake', 'ccBlendFunc', 'CCSizeMake', 'kCCVerticalTextAlignmentCenter']
00001 [L1417] UGET     A=0 B=0 C=0 D=0 g_self
00002 [L1417] TGETS    A=0 B=0 C=0 D=0 'hasDone'
00003 [L1417] ISF      A=0 B=0 C=0 D=0 
00004 [L1417] JMP      A=1 B=128 C=1 D=32769 target=6
00005 [L1418] UCLO     A=0 B=129 C=14 D=33038 target=276
00006 [L1421] GGET     A=0 B=0 C=1 D=1 'd_ms'
00007 [L1421] TGETS    A=0 B=0 C=2 D=2 'd_file'
00008 [L1421] TGETS    A=0 B=0 C=3 D=3 'get'
00009 [L1421] KSTR     A=1 B=0 C=4 D=4 'soul_hunt_guide'
00010 [L1421] GGET     A=2 B=0 C=1 D=1 'd_ms'
00011 [L1421] TGETS    A=2 B=2 C=5 D=517 'd_mainUI'
00012 [L1421] TGETS    A=2 B=2 C=6 D=518 'g_playerInfo'
00013 [L1421] TGETS    A=2 B=2 C=7 D=519 'role_id'
00014 [L1421] CALL     A=0 B=2 C=3 D=515 
00015 [L1422] ISF      A=0 B=0 C=0 D=0 
00016 [L1422] JMP      A=1 B=128 C=4 D=32772 target=21
00017 [L1423] UGET     A=1 B=0 C=0 D=0 g_self
00018 [L1423] KPRI     A=2 B=0 C=2 D=2 
00019 [L1423] TSETS    A=2 B=1 C=0 D=256 'hasDone'
00020 [L1424] UCLO     A=0 B=129 C=0 D=33024 target=277
00021 [L1427] GGET     A=1 B=0 C=1 D=1 'd_ms'
00022 [L1427] TGETS    A=1 B=1 C=8 D=264 'd_u'
00023 [L1427] TGETS    A=1 B=1 C=9 D=265 'clearLayer'
00024 [L1427] UGET     A=2 B=0 C=1 D=1 g_soulHuntUI
00025 [L1427] TGETS    A=2 B=2 C=10 D=522 'main_layer'
00026 [L1427] KSHORT   A=3 B=0 C=100 D=100 100
00027 [L1427] UGET     A=4 B=0 C=2 D=2 tags
00028 [L1427] TGETS    A=4 B=4 C=11 D=1035 'Guide'
00029 [L1427] CALL     A=1 B=2 C=4 D=516 
00030 [L1428] IST      A=0 B=0 C=1 D=1 
00031 [L1428] JMP      A=2 B=128 C=1 D=32769 target=33
00032 [L1429] UCLO     A=0 B=128 C=245 D=33013 target=278
00033 [L1436] FNEW     A=2 B=0 C=12 D=12 {'kind': 'proto', 'id': 76}
00034 [L1437] MOV      A=4 B=0 C=1 D=1 
00035 [L1437] TGETS    A=3 B=1 C=13 D=269 'registerScriptTouchHandler'
00036 [L1437] MOV      A=5 B=0 C=2 D=2 
00037 [L1437] KPRI     A=6 B=0 C=1 D=1 
00038 [L1437] KSHORT   A=7 B=255 C=128 D=65408 -128
00039 [L1437] KPRI     A=8 B=0 C=2 D=2 
00040 [L1437] CALL     A=3 B=1 C=6 D=262 
00041 [L1438] MOV      A=4 B=0 C=1 D=1 
00042 [L1438] TGETS    A=3 B=1 C=14 D=270 'setTouchEnabled'
00043 [L1438] KPRI     A=5 B=0 C=2 D=2 
00044 [L1438] CALL     A=3 B=1 C=3 D=259 
00045 [L1440] UGET     A=3 B=0 C=0 D=0 g_self
00046 [L1440] TGETS    A=3 B=3 C=15 D=783 'h1'
00047 [L1440] UGET     A=4 B=0 C=0 D=0 g_self
00048 [L1440] TGETS    A=4 B=4 C=16 D=1040 'h2'
00049 [L1440] UGET     A=5 B=0 C=0 D=0 g_self
00050 [L1440] TGETS    A=5 B=5 C=17 D=1297 'top_y'
00051 [L1442] UGET     A=6 B=0 C=3 D=3 CCRenderTexture
00052 [L1442] MOV      A=7 B=0 C=6 D=6 
00053 [L1442] TGETS    A=6 B=6 C=18 D=1554 'create'
00054 [L1442] UGET     A=8 B=0 C=4 D=4 scrSize
00055 [L1442] TGETS    A=8 B=8 C=19 D=2067 'width'
00056 [L1442] UGET     A=9 B=0 C=4 D=4 scrSize
00057 [L1442] TGETS    A=9 B=9 C=20 D=2324 'height'
00058 [L1442] CALL     A=6 B=2 C=4 D=516 
00059 [L1443] MOV      A=8 B=0 C=6 D=6 
00060 [L1443] TGETS    A=7 B=6 C=21 D=1557 'setPosition'
00061 [L1443] UGET     A=9 B=0 C=5 D=5 CCPointMake
00062 [L1443] UGET     A=10 B=0 C=4 D=4 scrSize
00063 [L1443] TGETS    A=10 B=10 C=19 D=2579 'width'
00064 [L1443] MULNV    A=10 B=10 C=0 D=2560 
00065 [L1443] UGET     A=11 B=0 C=4 D=4 scrSize
00066 [L1443] TGETS    A=11 B=11 C=20 D=2836 'height'
00067 [L1443] MULNV    A=11 B=11 C=0 D=2816 
00068 [L1443] CALL     A=9 B=0 C=3 D=3 
00069 [L1443] CALLM    A=7 B=1 C=1 D=257 
00070 [L1444] MOV      A=8 B=0 C=1 D=1 
00071 [L1444] TGETS    A=7 B=1 C=22 D=278 'addChild'
00072 [L1444] MOV      A=9 B=0 C=6 D=6 
00073 [L1444] CALL     A=7 B=1 C=3 D=259 
00074 [L1446] MOV      A=8 B=0 C=6 D=6 
00075 [L1446] TGETS    A=7 B=6 C=23 D=1559 'clear'
00076 [L1446] KSHORT   A=9 B=0 C=0 D=0 0
00077 [L1446] KSHORT   A=10 B=0 C=0 D=0 0
00078 [L1446] KSHORT   A=11 B=0 C=0 D=0 0
00079 [L1446] KNUM     A=12 B=0 C=1 D=1 0.7
00080 [L1446] CALL     A=7 B=1 C=6 D=262 
00081 [L1448] UGET     A=7 B=0 C=6 D=6 ccBlendFunc
00082 [L1448] MOV      A=8 B=0 C=7 D=7 
00083 [L1448] TGETS    A=7 B=7 C=24 D=1816 'new'
00084 [L1448] CALL     A=7 B=2 C=2 D=514 
00085 [L1449] KSHORT   A=8 B=0 C=1 D=1 1
00086 [L1449] TSETS    A=8 B=7 C=25 D=1817 'src'
00087 [L1450] KSHORT   A=8 B=0 C=0 D=0 0
00088 [L1450] TSETS    A=8 B=7 C=26 D=1818 'des'
00089 [L1452] MOV      A=9 B=0 C=6 D=6 
00090 [L1452] TGETS    A=8 B=6 C=27 D=1563 'begin'
00091 [L1452] CALL     A=8 B=1 C=2 D=258 
00092 [L1454] GGET     A=8 B=0 C=1 D=1 'd_ms'
00093 [L1454] TGETS    A=8 B=8 C=8 D=2056 'd_u'
00094 [L1454] TGETS    A=8 B=8 C=28 D=2076 'createByStyle'
00095 [L1454] TDUP     A=9 B=0 C=29 D=29 {'kind': 'table', 'value': {'pic': 'v2/guideUI/hint.png', 'scale': 0.06, 'x': 0.6}}
00096 [L1454] MULNV    A=10 B=4 C=0 D=1024 
00097 [L1454] TSETS    A=10 B=9 C=30 D=2334 'y'
00098 [L1454] CALL     A=8 B=2 C=2 D=514 
00099 [L1455] MOV      A=10 B=0 C=8 D=8 
00100 [L1455] TGETS    A=9 B=8 C=31 D=2079 'setBlendFunc'
00101 [L1455] MOV      A=11 B=0 C=7 D=7 
00102 [L1455] CALL     A=9 B=1 C=3 D=259 
00103 [L1456] MOV      A=10 B=0 C=8 D=8 
00104 [L1456] TGETS    A=9 B=8 C=32 D=2080 'visit'
00105 [L1456] CALL     A=9 B=1 C=2 D=258 
00106 [L1458] GGET     A=9 B=0 C=1 D=1 'd_ms'
00107 [L1458] TGETS    A=9 B=9 C=8 D=2312 'd_u'
00108 [L1458] TGETS    A=9 B=9 C=28 D=2332 'createByStyle'
00109 [L1458] TDUP     A=10 B=0 C=33 D=33 {'kind': 'table', 'value': {'pic': 'v2/guideUI/hint.png', 'scale': 0.06, 'x': 0.5}}
00110 [L1458] UGET     A=11 B=0 C=0 D=0 g_self
00111 [L1458] TGETS    A=11 B=11 C=34 D=2850 'Below'
00112 [L1458] UGET     A=12 B=0 C=4 D=4 scrSize
00113 [L1458] TGETS    A=12 B=12 C=20 D=3092 'height'
00114 [L1458] DIVVV    A=11 B=11 C=12 D=2828 
00115 [L1458] ADDVV    A=11 B=4 C=11 D=1035 
00116 [L1458] TSETS    A=11 B=10 C=30 D=2590 'y'
00117 [L1458] CALL     A=9 B=2 C=2 D=514 
00118 [L1458] MOV      A=8 B=0 C=9 D=9 
00119 [L1459] MOV      A=10 B=0 C=8 D=8 
00120 [L1459] TGETS    A=9 B=8 C=31 D=2079 'setBlendFunc'
00121 [L1459] MOV      A=11 B=0 C=7 D=7 
00122 [L1459] CALL     A=9 B=1 C=3 D=259 
00123 [L1460] MOV      A=10 B=0 C=8 D=8 
00124 [L1460] TGETS    A=9 B=8 C=32 D=2080 'visit'
00125 [L1460] CALL     A=9 B=1 C=2 D=258 
00126 [L1462] GGET     A=9 B=0 C=1 D=1 'd_ms'
00127 [L1462] TGETS    A=9 B=9 C=8 D=2312 'd_u'
00128 [L1462] TGETS    A=9 B=9 C=28 D=2332 'createByStyle'
00129 [L1462] TDUP     A=10 B=0 C=35 D=35 {'kind': 'table', 'value': {'pic': 'v2/guideUI/hint.png', 'scale': 0.06, 'x': 0.03}}
00130 [L1462] TSETS    A=5 B=10 C=30 D=2590 'y'
00131 [L1462] CALL     A=9 B=2 C=2 D=514 
00132 [L1462] MOV      A=8 B=0 C=9 D=9 
00133 [L1463] MOV      A=10 B=0 C=8 D=8 
00134 [L1463] TGETS    A=9 B=8 C=31 D=2079 'setBlendFunc'
00135 [L1463] MOV      A=11 B=0 C=7 D=7 
00136 [L1463] CALL     A=9 B=1 C=3 D=259 
00137 [L1464] MOV      A=10 B=0 C=8 D=8 
00138 [L1464] TGETS    A=9 B=8 C=32 D=2080 'visit'
00139 [L1464] CALL     A=9 B=1 C=2 D=258 
00140 [L1466] MOV      A=10 B=0 C=6 D=6 
00141 [L1466] TGETS    A=9 B=6 C=36 D=1572 'endToLua'
00142 [L1466] CALL     A=9 B=1 C=2 D=258 
00143 [L1469] GGET     A=9 B=0 C=37 D=37 'getSoulHuntGuideArrow'
00144 [L1469] GGET     A=10 B=0 C=1 D=1 'd_ms'
00145 [L1469] TGETS    A=10 B=10 C=38 D=2598 'd_hz'
00146 [L1469] TGETS    A=10 B=10 C=39 D=2599 'gethz'
00147 [L1469] KSTR     A=11 B=0 C=40 D=40 'hunt_guide1'
00148 [L1469] CALL     A=10 B=0 C=2 D=2 
00149 [L1469] CALLM    A=9 B=2 C=0 D=512 
00150 [L1470] GGET     A=10 B=0 C=1 D=1 'd_ms'
00151 [L1470] TGETS    A=10 B=10 C=8 D=2568 'd_u'
00152 [L1470] TGETS    A=10 B=10 C=41 D=2601 'setStyles'
00153 [L1470] MOV      A=11 B=0 C=9 D=9 
00154 [L1470] TDUP     A=12 B=0 C=42 D=42 {'kind': 'table', 'value': {'x': 0.63}}
00155 [L1470] MULNV    A=13 B=4 C=0 D=1024 
00156 [L1470] TSETS    A=13 B=12 C=30 D=3102 'y'
00157 [L1470] TDUP     A=13 B=0 C=43 D=43 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00158 [L1470] TSETS    A=13 B=12 C=44 D=3116 'anchor'
00159 [L1470] CALL     A=10 B=1 C=3 D=259 
00160 [L1471] MOV      A=11 B=0 C=1 D=1 
00161 [L1471] TGETS    A=10 B=1 C=22 D=278 'addChild'
00162 [L1471] MOV      A=12 B=0 C=9 D=9 
00163 [L1471] KSHORT   A=13 B=0 C=1 D=1 1
00164 [L1471] CALL     A=10 B=1 C=4 D=260 
00165 [L1474] MOV      A=11 B=0 C=1 D=1 
00166 [L1474] TGETS    A=10 B=1 C=22 D=278 'addChild'
00167 [L1474] GGET     A=12 B=0 C=1 D=1 'd_ms'
00168 [L1474] TGETS    A=12 B=12 C=8 D=3080 'd_u'
00169 [L1474] TGETS    A=12 B=12 C=28 D=3100 'createByStyle'
00170 [L1474] TDUP     A=13 B=0 C=45 D=45 {'kind': 'table', 'value': {'pic': 'v2/guideUI/hand2.png', 'x': 0.5}}
00171 [L1474] MULNV    A=14 B=3 C=0 D=768 
00172 [L1474] ADDVV    A=14 B=4 C=14 D=1038 
00173 [L1474] TSETS    A=14 B=13 C=30 D=3358 'y'
00174 [L1474] CALL     A=12 B=2 C=2 D=514 
00175 [L1474] KSHORT   A=13 B=0 C=1 D=1 1
00176 [L1474] CALL     A=10 B=1 C=4 D=260 
00177 [L1475] GGET     A=10 B=0 C=1 D=1 'd_ms'
00178 [L1475] TGETS    A=10 B=10 C=8 D=2568 'd_u'
00179 [L1475] TGETS    A=10 B=10 C=28 D=2588 'createByStyle'
00180 [L1475] TDUP     A=11 B=0 C=46 D=46 {'kind': 'table', 'value': {'type': 'label', 'fontsize': 26, 'font': 'arial', 'x': 0.75}}
00181 [L1475] GGET     A=12 B=0 C=1 D=1 'd_ms'
00182 [L1475] TGETS    A=12 B=12 C=38 D=3110 'd_hz'
00183 [L1475] TGETS    A=12 B=12 C=39 D=3111 'gethz'
00184 [L1475] KSTR     A=13 B=0 C=47 D=47 'hunt_guide2'
00185 [L1475] CALL     A=12 B=2 C=2 D=514 
00186 [L1475] TSETS    A=12 B=11 C=48 D=2864 'string'
00187 [L1475] MULNV    A=12 B=3 C=0 D=768 
00188 [L1475] ADDVV    A=12 B=4 C=12 D=1036 
00189 [L1475] TSETS    A=12 B=11 C=30 D=2846 'y'
00190 [L1475] UGET     A=12 B=0 C=7 D=7 CCSizeMake
00191 [L1475] UGET     A=13 B=0 C=4 D=4 scrSize
00192 [L1475] TGETS    A=13 B=13 C=19 D=3347 'width'
00193 [L1475] MULNV    A=13 B=13 C=2 D=3330 
00194 [L1475] KSHORT   A=14 B=0 C=0 D=0 0
00195 [L1475] CALL     A=12 B=2 C=3 D=515 
00196 [L1475] TSETS    A=12 B=11 C=49 D=2865 'size'
00197 [L1475] UGET     A=12 B=0 C=8 D=8 kCCVerticalTextAlignmentCenter
00198 [L1475] TSETS    A=12 B=11 C=50 D=2866 'h_align'
00199 [L1475] TDUP     A=12 B=0 C=51 D=51 {'kind': 'table', 'value': {1: 255, 2: 255, 3: 100}}
00200 [L1475] TSETS    A=12 B=11 C=52 D=2868 'color'
00201 [L1475] CALL     A=10 B=2 C=2 D=514 
00202 [L1476] MOV      A=12 B=0 C=1 D=1 
00203 [L1476] TGETS    A=11 B=1 C=22 D=278 'addChild'
00204 [L1476] MOV      A=13 B=0 C=10 D=10 
00205 [L1476] KSHORT   A=14 B=0 C=1 D=1 1
00206 [L1476] CALL     A=11 B=1 C=4 D=260 
00207 [L1479] GGET     A=11 B=0 C=37 D=37 'getSoulHuntGuideArrow'
00208 [L1479] GGET     A=12 B=0 C=1 D=1 'd_ms'
00209 [L1479] TGETS    A=12 B=12 C=38 D=3110 'd_hz'
00210 [L1479] TGETS    A=12 B=12 C=39 D=3111 'gethz'
00211 [L1479] KSTR     A=13 B=0 C=53 D=53 'hunt_guide3'
00212 [L1479] CALL     A=12 B=2 C=2 D=514 
00213 [L1479] KPRI     A=13 B=0 C=2 D=2 
00214 [L1479] CALL     A=11 B=2 C=3 D=515 
00215 [L1480] GGET     A=12 B=0 C=1 D=1 'd_ms'
00216 [L1480] TGETS    A=12 B=12 C=8 D=3080 'd_u'
00217 [L1480] TGETS    A=12 B=12 C=41 D=3113 'setStyles'
00218 [L1480] MOV      A=13 B=0 C=11 D=11 
00219 [L1480] TDUP     A=14 B=0 C=54 D=54 {'kind': 'table', 'value': {'x': 0.47}}
00220 [L1480] UGET     A=15 B=0 C=0 D=0 g_self
00221 [L1480] TGETS    A=15 B=15 C=34 D=3874 'Below'
00222 [L1480] UGET     A=16 B=0 C=4 D=4 scrSize
00223 [L1480] TGETS    A=16 B=16 C=20 D=4116 'height'
00224 [L1480] DIVVV    A=15 B=15 C=16 D=3856 
00225 [L1480] ADDVV    A=15 B=4 C=15 D=1039 
00226 [L1480] TSETS    A=15 B=14 C=30 D=3614 'y'
00227 [L1480] TDUP     A=15 B=0 C=55 D=55 {'kind': 'table', 'value': {1: 1, 2: 0.5}}
00228 [L1480] TSETS    A=15 B=14 C=44 D=3628 'anchor'
00229 [L1480] CALL     A=12 B=1 C=3 D=259 
00230 [L1481] MOV      A=13 B=0 C=1 D=1 
00231 [L1481] TGETS    A=12 B=1 C=22 D=278 'addChild'
00232 [L1481] MOV      A=14 B=0 C=11 D=11 
00233 [L1481] KSHORT   A=15 B=0 C=1 D=1 1
00234 [L1481] CALL     A=12 B=1 C=4 D=260 
00235 [L1484] GGET     A=12 B=0 C=37 D=37 'getSoulHuntGuideArrow'
00236 [L1484] GGET     A=13 B=0 C=1 D=1 'd_ms'
00237 [L1484] TGETS    A=13 B=13 C=38 D=3366 'd_hz'
00238 [L1484] TGETS    A=13 B=13 C=39 D=3367 'gethz'
00239 [L1484] KSTR     A=14 B=0 C=56 D=56 'hunt_guide4'
00240 [L1484] CALL     A=13 B=0 C=2 D=2 
00241 [L1484] CALLM    A=12 B=2 C=0 D=512 
00242 [L1485] GGET     A=13 B=0 C=1 D=1 'd_ms'
00243 [L1485] TGETS    A=13 B=13 C=8 D=3336 'd_u'
00244 [L1485] TGETS    A=13 B=13 C=41 D=3369 'setStyles'
00245 [L1485] MOV      A=14 B=0 C=12 D=12 
00246 [L1485] TDUP     A=15 B=0 C=57 D=57 {'kind': 'table', 'value': {'x': 0.06}}
00247 [L1485] TSETS    A=5 B=15 C=30 D=3870 'y'
00248 [L1485] TDUP     A=16 B=0 C=58 D=58 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00249 [L1485] TSETS    A=16 B=15 C=44 D=3884 'anchor'
00250 [L1485] CALL     A=13 B=1 C=3 D=259 
00251 [L1486] MOV      A=14 B=0 C=1 D=1 
00252 [L1486] TGETS    A=13 B=1 C=22 D=278 'addChild'
00253 [L1486] MOV      A=15 B=0 C=12 D=12 
00254 [L1486] KSHORT   A=16 B=0 C=1 D=1 1
00255 [L1486] CALL     A=13 B=1 C=4 D=260 
00256 [L1488] MOV      A=14 B=0 C=1 D=1 
00257 [L1488] TGETS    A=13 B=1 C=22 D=278 'addChild'
00258 [L1488] GGET     A=15 B=0 C=1 D=1 'd_ms'
00259 [L1488] TGETS    A=15 B=15 C=8 D=3848 'd_u'
00260 [L1488] TGETS    A=15 B=15 C=28 D=3868 'createByStyle'
00261 [L1488] TDUP     A=16 B=0 C=59 D=59 {'kind': 'table', 'value': {'type': 'label', 'x': 0.8, 'fontsize': 26}}
00262 [L1488] TSETS    A=5 B=16 C=30 D=4126 'y'
00263 [L1488] GGET     A=17 B=0 C=1 D=1 'd_ms'
00264 [L1488] TGETS    A=17 B=17 C=38 D=4390 'd_hz'
00265 [L1488] TGETS    A=17 B=17 C=39 D=4391 'gethz'
00266 [L1488] KSTR     A=18 B=0 C=60 D=60 'hunt_guide5'
00267 [L1488] CALL     A=17 B=2 C=2 D=514 
00268 [L1488] TSETS    A=17 B=16 C=48 D=4144 'string'
00269 [L1488] TDUP     A=17 B=0 C=61 D=61 {'kind': 'table', 'value': {1: 255, 2: 255, 3: 100}}
00270 [L1488] TSETS    A=17 B=16 C=52 D=4148 'color'
00271 [L1488] CALL     A=15 B=2 C=2 D=514 
00272 [L1488] KSHORT   A=16 B=0 C=1 D=1 1
00273 [L1488] CALL     A=13 B=1 C=4 D=260 
00274 [L1490] UCLO     A=0 B=128 C=0 D=32768 target=275
00275 [L1490] RET0     A=0 B=0 C=1 D=1 
00276 [L1490] RET0     A=0 B=0 C=1 D=1 
00277 [L1490] RET0     A=0 B=0 C=1 D=1 
00278 [L1490] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto78 offset=0xaeb1 source_lines=1492-1505 params=2
UPVALUES ['CCSprite']
00001 [L1493] UGET     A=2 B=0 C=0 D=0 CCSprite
00002 [L1493] MOV      A=3 B=0 C=2 D=2 
00003 [L1493] TGETS    A=2 B=2 C=0 D=512 'create'
00004 [L1493] KSTR     A=4 B=0 C=1 D=1 'v2/guideUI/arrow3.png'
00005 [L1493] CALL     A=2 B=2 C=3 D=515 
00006 [L1494] MOV      A=4 B=0 C=2 D=2 
00007 [L1494] TGETS    A=3 B=2 C=2 D=514 'getContentSize'
00008 [L1494] CALL     A=3 B=2 C=2 D=514 
00009 [L1496] GGET     A=4 B=0 C=3 D=3 'd_ms'
00010 [L1496] TGETS    A=4 B=4 C=4 D=1028 'd_u'
00011 [L1496] TGETS    A=4 B=4 C=5 D=1029 'createByStyle'
00012 [L1496] TDUP     A=5 B=0 C=6 D=6 {'kind': 'table', 'value': {'fontsize': 26, 'type': 'label'}}
00013 [L1496] TSETS    A=0 B=5 C=7 D=1287 'string'
00014 [L1496] TDUP     A=6 B=0 C=8 D=8 {'kind': 'table', 'value': {1: 255, 2: 255, 3: 100}}
00015 [L1496] TSETS    A=6 B=5 C=9 D=1289 'color'
00016 [L1496] CALL     A=4 B=2 C=2 D=514 
00017 [L1497] MOV      A=6 B=0 C=4 D=4 
00018 [L1497] TGETS    A=5 B=4 C=10 D=1034 'setPosition'
00019 [L1497] TGETS    A=7 B=3 C=11 D=779 'width'
00020 [L1497] MULVN    A=7 B=7 C=0 D=1792 
00021 [L1497] TGETS    A=8 B=3 C=12 D=780 'height'
00022 [L1497] MULVN    A=8 B=8 C=0 D=2048 
00023 [L1497] CALL     A=5 B=1 C=4 D=260 
00024 [L1498] MOV      A=6 B=0 C=2 D=2 
00025 [L1498] TGETS    A=5 B=2 C=13 D=525 'addChild'
00026 [L1498] MOV      A=7 B=0 C=4 D=4 
00027 [L1498] CALL     A=5 B=1 C=3 D=259 
00028 [L1500] ISF      A=0 B=0 C=1 D=1 
00029 [L1500] JMP      A=5 B=128 C=4 D=32772 target=34
00030 [L1501] MOV      A=6 B=0 C=2 D=2 
00031 [L1501] TGETS    A=5 B=2 C=14 D=526 'setFlipX'
00032 [L1501] KPRI     A=7 B=0 C=2 D=2 
00033 [L1501] CALL     A=5 B=1 C=3 D=259 
00034 [L1504] RET1     A=2 B=0 C=2 D=2 

FUNCTION proto79 offset=0xb045 source_lines=0-1505 params=0
UPVALUES []
00001 [L7] GGET     A=0 B=0 C=0 D=0 'require'
00002 [L8] GGET     A=1 B=0 C=1 D=1 'string'
00003 [L9] GGET     A=2 B=0 C=2 D=2 'math'
00004 [L10] GGET     A=3 B=0 C=3 D=3 'pairs'
00005 [L11] GGET     A=4 B=0 C=4 D=4 'os'
00006 [L12] GGET     A=5 B=0 C=5 D=5 'io'
00007 [L13] GGET     A=6 B=0 C=6 D=6 'table'
00008 [L14] GGET     A=7 B=0 C=7 D=7 'tolua'
00009 [L15] GGET     A=8 B=0 C=8 D=8 'tostring'
00010 [L16] GGET     A=9 B=0 C=9 D=9 'ccc3'
00011 [L17] GGET     A=10 B=0 C=10 D=10 'ccc4'
00012 [L18] GGET     A=11 B=0 C=11 D=11 'ccp'
00013 [L19] GGET     A=12 B=0 C=12 D=12 'tonumber'
00014 [L21] GGET     A=13 B=0 C=13 D=13 'main_server'
00015 [L23] GGET     A=14 B=0 C=14 D=14 'CCNode'
00016 [L24] GGET     A=15 B=0 C=15 D=15 'CCSprite'
00017 [L25] GGET     A=16 B=0 C=16 D=16 'CCLayer'
00018 [L26] GGET     A=17 B=0 C=17 D=17 'CCLayerColor'
00019 [L27] GGET     A=18 B=0 C=18 D=18 'CCLuaLog'
00020 [L28] GGET     A=19 B=0 C=19 D=19 'CCDirector'
00021 [L29] GGET     A=20 B=0 C=20 D=20 'CCArray'
00022 [L30] GGET     A=21 B=0 C=21 D=21 'CCMenu'
00023 [L31] GGET     A=22 B=0 C=22 D=22 'CCScrollView'
00024 [L32] GGET     A=23 B=0 C=23 D=23 'CCRectMake'
00025 [L33] GGET     A=24 B=0 C=24 D=24 'CCSizeMake'
00026 [L34] GGET     A=25 B=0 C=25 D=25 'CCPointMake'
00027 [L36] GGET     A=26 B=0 C=26 D=26 'CCTOUCHBEGAN'
00028 [L37] GGET     A=27 B=0 C=27 D=27 'CCTOUCHMOVED'
00029 [L38] GGET     A=28 B=0 C=28 D=28 'CCTOUCHENDED'
00030 [L40] GGET     A=29 B=0 C=29 D=29 'CCMoveBy'
00031 [L41] GGET     A=30 B=0 C=30 D=30 'CCSequence'
00032 [L42] GGET     A=31 B=0 C=31 D=31 'CCCallFuncN'
00033 [L43] GGET     A=32 B=0 C=32 D=32 'CCFadeOut'
00034 [L44] GGET     A=33 B=0 C=33 D=33 'CCSpawn'
00035 [L45] GGET     A=34 B=0 C=34 D=34 'CCDelayTime'
00036 [L46] GGET     A=35 B=0 C=35 D=35 'kCCVerticalTextAlignmentCenter'
00037 [L48] GGET     A=36 B=0 C=36 D=36 'ccBlendFunc'
00038 [L49] GGET     A=37 B=0 C=37 D=37 'CCRenderTexture'
00039 [L51] GGET     A=38 B=0 C=38 D=38 'module'
00040 [L51] KSTR     A=39 B=0 C=39 D=39 'ui.soulHuntUI'
00041 [L51] CALL     A=38 B=1 C=2 D=258 
00042 [L53] MOV      A=38 B=0 C=0 D=0 
00043 [L53] KSTR     A=39 B=0 C=40 D=40 'ms'
00044 [L53] CALL     A=38 B=2 C=2 D=514 
00045 [L53] GSET     A=38 B=0 C=41 D=41 'd_ms'
00046 [L54] GGET     A=38 B=0 C=41 D=41 'd_ms'
00047 [L54] IST      A=0 B=0 C=38 D=38 
00048 [L54] JMP      A=38 B=128 C=3 D=32771 target=52
00049 [L55] MOV      A=38 B=0 C=18 D=18 
00050 [L55] KSTR     A=39 B=0 C=42 D=42 'soulHuntUI load d_ms fail.\n'
00051 [L55] CALL     A=38 B=1 C=2 D=258 
00052 [L60] FNEW     A=38 B=0 C=43 D=43 {'kind': 'proto', 'id': 0}
00053 [L62] MOV      A=40 B=0 C=19 D=19 
00054 [L62] TGETS    A=39 B=19 C=44 D=4908 'sharedDirector'
00055 [L62] CALL     A=39 B=2 C=2 D=514 
00056 [L62] MOV      A=40 B=0 C=39 D=39 
00057 [L62] TGETS    A=39 B=39 C=45 D=10029 'getVisibleSize'
00058 [L62] CALL     A=39 B=2 C=2 D=514 
00059 [L63] TNEW     A=40 B=0 C=0 D=0 
00060 [L64] TNEW     A=41 B=0 C=0 D=0 
00061 [L65] TDUP     A=42 B=0 C=46 D=46 {'kind': 'table', 'value': {'Cannon': 5, 'Shop': 8, 'Rank': 9, 'Guide': 12, 'BallChoose': 4, 'SoulCount': 1, 'RankDetail': 10, 'Soul': 7, 'Ball': 6, 'FreshTimes': 11, 'ShootTimes': 3, 'Hint': 13, 'Energy': 2}}
00062 [L81] GGET     A=43 B=0 C=41 D=41 'd_ms'
00063 [L81] TGETS    A=43 B=43 C=47 D=11055 'd_common_def'
00064 [L81] TGETS    A=43 B=43 C=48 D=11056 'hunt_op_type'
00065 [L82] KSHORT   A=44 B=255 C=236 D=65516 -20
00066 [L82] TSETS    A=44 B=40 C=49 D=10289 'Below'
00067 [L83] KSHORT   A=44 B=1 C=244 D=500 500
00068 [L83] TSETS    A=44 B=40 C=50 D=10290 'Speed'
00069 [L87] FNEW     A=44 B=0 C=51 D=51 {'kind': 'proto', 'id': 1}
00070 [L96] FNEW     A=45 B=0 C=52 D=52 {'kind': 'proto', 'id': 2}
00071 [L168] FNEW     A=46 B=0 C=53 D=53 {'kind': 'proto', 'id': 3}
00072 [L98] GSET     A=46 B=0 C=54 D=54 'onGetResponse'
00073 [L179] FNEW     A=46 B=0 C=55 D=55 {'kind': 'proto', 'id': 4}
00074 [L170] GSET     A=46 B=0 C=56 D=56 'updateActivityStatus'
00075 [L183] FNEW     A=46 B=0 C=57 D=57 {'kind': 'proto', 'id': 5}
00076 [L181] GSET     A=46 B=0 C=58 D=58 'canJoin'
00077 [L195] FNEW     A=46 B=0 C=59 D=59 {'kind': 'proto', 'id': 6}
00078 [L185] GSET     A=46 B=0 C=60 D=60 'isShowHint'
00079 [L212] FNEW     A=46 B=0 C=61 D=61 {'kind': 'proto', 'id': 7}
00080 [L197] GSET     A=46 B=0 C=62 D=62 'canEnter'
00081 [L228] FNEW     A=46 B=0 C=63 D=63 {'kind': 'proto', 'id': 8}
00082 [L214] GSET     A=46 B=0 C=64 D=64 'show'
00083 [L301] FNEW     A=46 B=0 C=65 D=65 {'kind': 'proto', 'id': 9}
00084 [L230] GSET     A=46 B=0 C=66 D=66 'create'
00085 [L314] FNEW     A=46 B=0 C=67 D=67 {'kind': 'proto', 'id': 10}
00086 [L303] GSET     A=46 B=0 C=68 D=68 'showHint'
00087 [L318] FNEW     A=46 B=0 C=69 D=69 {'kind': 'proto', 'id': 11}
00088 [L358] FNEW     A=47 B=0 C=70 D=70 {'kind': 'proto', 'id': 13}
00089 [L320] GSET     A=47 B=0 C=71 D=71 'showSouls'
00090 [L376] FNEW     A=47 B=0 C=72 D=72 {'kind': 'proto', 'id': 14}
00091 [L361] GSET     A=47 B=0 C=73 D=73 'pressRefresh'
00092 [L428] FNEW     A=47 B=0 C=74 D=74 {'kind': 'proto', 'id': 17}
00093 [L379] GSET     A=47 B=0 C=75 D=75 'pressChoose'
00094 [L509] FNEW     A=47 B=0 C=76 D=76 {'kind': 'proto', 'id': 21}
00095 [L431] GSET     A=47 B=0 C=77 D=77 'pressBuyEnergy'
00096 [L530] FNEW     A=47 B=0 C=78 D=78 {'kind': 'proto', 'id': 22}
00097 [L512] GSET     A=47 B=0 C=79 D=79 'pressShoot'
00098 [L548] FNEW     A=47 B=0 C=80 D=80 {'kind': 'proto', 'id': 23}
00099 [L533] GSET     A=47 B=0 C=81 D=81 'showBall'
00100 [L558] FNEW     A=47 B=0 C=82 D=82 {'kind': 'proto', 'id': 24}
00101 [L550] GSET     A=47 B=0 C=83 D=83 'getSoulIndex'
00102 [L585] FNEW     A=47 B=0 C=84 D=84 {'kind': 'proto', 'id': 25}
00103 [L560] GSET     A=47 B=0 C=85 D=85 'soulAbsorb'
00104 [L601] FNEW     A=47 B=0 C=86 D=86 {'kind': 'proto', 'id': 26}
00105 [L588] GSET     A=47 B=0 C=87 D=87 'verify'
00106 [L680] FNEW     A=47 B=0 C=88 D=88 {'kind': 'proto', 'id': 29}
00107 [L604] GSET     A=47 B=0 C=89 D=89 'showBallTrack'
00108 [L690] FNEW     A=47 B=0 C=90 D=90 {'kind': 'proto', 'id': 30}
00109 [L683] GSET     A=47 B=0 C=91 D=91 'showShootTimes'
00110 [L705] FNEW     A=47 B=0 C=92 D=92 {'kind': 'proto', 'id': 31}
00111 [L693] GSET     A=47 B=0 C=93 D=93 'showFreshTimes'
00112 [L715] FNEW     A=47 B=0 C=94 D=94 {'kind': 'proto', 'id': 32}
00113 [L708] GSET     A=47 B=0 C=95 D=95 'showEnergy'
00114 [L727] FNEW     A=47 B=0 C=96 D=96 {'kind': 'proto', 'id': 33}
00115 [L718] GSET     A=47 B=0 C=97 D=97 'showSoulCount'
00116 [L751] FNEW     A=47 B=0 C=98 D=98 {'kind': 'proto', 'id': 34}
00117 [L730] GSET     A=47 B=0 C=99 D=99 'showCannon'
00118 [L772] FNEW     A=47 B=0 C=100 D=100 {'kind': 'proto', 'id': 35}
00119 [L754] GSET     A=47 B=0 C=101 D=101 'getDegree'
00120 [L787] FNEW     A=47 B=0 C=102 D=102 {'kind': 'proto', 'id': 36}
00121 [L774] GSET     A=47 B=0 C=103 D=103 'onTouchBegan'
00122 [L797] FNEW     A=47 B=0 C=104 D=104 {'kind': 'proto', 'id': 37}
00123 [L789] GSET     A=47 B=0 C=105 D=105 'onTouchMoved'
00124 [L802] FNEW     A=47 B=0 C=106 D=106 {'kind': 'proto', 'id': 38}
00125 [L799] GSET     A=47 B=0 C=107 D=107 'onTouchEnded'
00126 [L807] FNEW     A=47 B=0 C=108 D=108 {'kind': 'proto', 'id': 39}
00127 [L804] GSET     A=47 B=0 C=109 D=109 'onTouchCancel'
00128 [L819] FNEW     A=47 B=0 C=110 D=110 {'kind': 'proto', 'id': 40}
00129 [L809] GSET     A=47 B=0 C=111 D=111 'onTouch'
00130 [L899] FNEW     A=47 B=0 C=112 D=112 {'kind': 'proto', 'id': 43}
00131 [L822] GSET     A=47 B=0 C=113 D=113 'pressBuyItem'
00132 [L999] FNEW     A=47 B=0 C=114 D=114 {'kind': 'proto', 'id': 47}
00133 [L902] GSET     A=47 B=0 C=115 D=115 'showShop'
00134 [L1035] FNEW     A=47 B=0 C=116 D=116 {'kind': 'proto', 'id': 49}
00135 [L1002] GSET     A=47 B=0 C=117 D=117 'showRank'
00136 [L1042] FNEW     A=47 B=0 C=118 D=118 {'kind': 'proto', 'id': 50}
00137 [L1038] GSET     A=47 B=0 C=119 D=119 'calculateBtnSize'
00138 [L1120] FNEW     A=47 B=0 C=120 D=120 {'kind': 'proto', 'id': 52}
00139 [L1045] GSET     A=47 B=0 C=121 D=121 'createLeftBtnsSlid'
00140 [L1141] FNEW     A=47 B=0 C=122 D=122 {'kind': 'proto', 'id': 53}
00141 [L1122] GSET     A=47 B=0 C=123 D=123 'createRankCell'
00142 [L1164] FNEW     A=47 B=0 C=124 D=124 {'kind': 'proto', 'id': 57}
00143 [L1143] GSET     A=47 B=0 C=125 D=125 'getRankDataSource'
00144 [L1183] FNEW     A=47 B=0 C=126 D=126 {'kind': 'proto', 'id': 58}
00145 [L1166] GSET     A=47 B=0 C=127 D=127 'createPrizeCell'
00146 [L1206] FNEW     A=47 B=0 C=128 D=128 {'kind': 'proto', 'id': 62}
00147 [L1185] GSET     A=47 B=0 C=129 D=129 'getRankPrizeDataSource'
00148 [L1290] FNEW     A=47 B=0 C=130 D=130 {'kind': 'proto', 'id': 64}
00149 [L1207] GSET     A=47 B=0 C=131 D=131 'showRankDetail'
00150 [L1299] FNEW     A=47 B=0 C=132 D=132 {'kind': 'proto', 'id': 65}
00151 [L1292] GSET     A=47 B=0 C=133 D=133 'enterActivity'
00152 [L1308] FNEW     A=47 B=0 C=134 D=134 {'kind': 'proto', 'id': 66}
00153 [L1301] GSET     A=47 B=0 C=135 D=135 'pressShop'
00154 [L1331] FNEW     A=47 B=0 C=136 D=136 {'kind': 'proto', 'id': 67}
00155 [L1311] GSET     A=47 B=0 C=137 D=137 'pressRank'
00156 [L1340] FNEW     A=47 B=0 C=138 D=138 {'kind': 'proto', 'id': 68}
00157 [L1333] GSET     A=47 B=0 C=139 D=139 'sendTakeRewardRequest'
00158 [L1349] FNEW     A=47 B=0 C=140 D=140 {'kind': 'proto', 'id': 69}
00159 [L1342] GSET     A=47 B=0 C=141 D=141 'sendSoulFlushRequest'
00160 [L1358] FNEW     A=47 B=0 C=142 D=142 {'kind': 'proto', 'id': 70}
00161 [L1351] GSET     A=47 B=0 C=143 D=143 'sendStoreFlushRequest'
00162 [L1367] FNEW     A=47 B=0 C=144 D=144 {'kind': 'proto', 'id': 71}
00163 [L1360] GSET     A=47 B=0 C=145 D=145 'sendBuyEnergyRequest'
00164 [L1376] FNEW     A=47 B=0 C=146 D=146 {'kind': 'proto', 'id': 72}
00165 [L1369] GSET     A=47 B=0 C=147 D=147 'sendBuyItemRequest'
00166 [L1381] FNEW     A=47 B=0 C=148 D=148 {'kind': 'proto', 'id': 73}
00167 [L1378] GSET     A=47 B=0 C=149 D=149 'pressClose'
00168 [L1385] FNEW     A=47 B=0 C=150 D=150 {'kind': 'proto', 'id': 74}
00169 [L1383] GSET     A=47 B=0 C=151 D=151 'pressQuestion'
00170 [L1414] FNEW     A=47 B=0 C=152 D=152 {'kind': 'proto', 'id': 75}
00171 [L1387] GSET     A=47 B=0 C=153 D=153 'getCrossPoint'
00172 [L1490] FNEW     A=47 B=0 C=154 D=154 {'kind': 'proto', 'id': 77}
00173 [L1416] GSET     A=47 B=0 C=155 D=155 'showSoulHuntGuide'
00174 [L1505] FNEW     A=47 B=0 C=156 D=156 {'kind': 'proto', 'id': 78}
00175 [L1492] GSET     A=47 B=0 C=157 D=157 'getSoulHuntGuideArrow'
00176 [L1505] UCLO     A=0 B=128 C=0 D=32768 target=177
00177 [L1505] RET0     A=0 B=0 C=1 D=1 
