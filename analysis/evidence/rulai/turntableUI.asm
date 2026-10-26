LuaJIT dump version=1; source='@D:\\mg_update_\\lua_cache\\lua1\\12826e552728da7442927bd96b4c7f04.data'; root=proto51

FUNCTION proto0 offset=0x4a source_lines=66-68 params=0
UPVALUES ['print', 'string']
00001 [L67] UGET     A=0 B=0 C=0 D=0 print
00002 [L67] UGET     A=1 B=0 C=1 D=1 string
00003 [L67] TGETS    A=1 B=1 C=0 D=256 'format'
00004 [L67] VARG     A=2 B=0 C=0 D=0 
00005 [L67] CALLM    A=1 B=0 C=0 D=0 
00006 [L67] CALLM    A=0 B=1 C=0 D=256 
00007 [L68] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto1 offset=0x92 source_lines=97-145 params=1
UPVALUES []
00001 [L98] IST      A=0 B=0 C=0 D=0 
00002 [L98] JMP      A=1 B=128 C=1 D=32769 target=4
00003 [L99] RET0     A=0 B=0 C=1 D=1 
00004 [L102] TGETS    A=1 B=0 C=0 D=0 'id'
00005 [L102] ISNEN    A=1 B=0 C=0 D=0 0
00006 [L102] JMP      A=1 B=128 C=65 D=32833 target=72
00007 [L103] TGETS    A=1 B=0 C=1 D=1 'pack_data'
00008 [L104] IST      A=0 B=0 C=1 D=1 
00009 [L104] JMP      A=2 B=128 C=1 D=32769 target=11
00010 [L105] RET0     A=0 B=0 C=1 D=1 
00011 [L107] GGET     A=2 B=0 C=2 D=2 'g_self'
00012 [L107] TNEW     A=3 B=0 C=0 D=0 
00013 [L107] TSETS    A=3 B=2 C=3 D=515 'data'
00014 [L108] GGET     A=2 B=0 C=2 D=2 'g_self'
00015 [L108] TGETS    A=2 B=2 C=3 D=515 'data'
00016 [L108] TGETS    A=3 B=1 C=5 D=261 'cur_count'
00017 [L108] IST      A=0 B=0 C=3 D=3 
00018 [L108] JMP      A=4 B=128 C=1 D=32769 target=20
00019 [L108] KSHORT   A=3 B=0 C=0 D=0 0
00020 [L108] TSETS    A=3 B=2 C=4 D=516 'total_time'
00021 [L109] GGET     A=2 B=0 C=2 D=2 'g_self'
00022 [L109] TGETS    A=2 B=2 C=3 D=515 'data'
00023 [L109] TGETS    A=3 B=1 C=7 D=263 'order_pay'
00024 [L109] IST      A=0 B=0 C=3 D=3 
00025 [L109] JMP      A=4 B=128 C=1 D=32769 target=27
00026 [L109] KSHORT   A=3 B=0 C=0 D=0 0
00027 [L109] TSETS    A=3 B=2 C=6 D=518 'total_charge'
00028 [L113] GGET     A=2 B=0 C=2 D=2 'g_self'
00029 [L113] TGETS    A=2 B=2 C=3 D=515 'data'
00030 [L113] TGETS    A=3 B=1 C=9 D=265 'order_list'
00031 [L113] TSETS    A=3 B=2 C=8 D=520 'charge_his'
00032 [L115] GGET     A=2 B=0 C=2 D=2 'g_self'
00033 [L115] TGETS    A=2 B=2 C=3 D=515 'data'
00034 [L115] TGETS    A=3 B=1 C=11 D=267 'random_table'
00035 [L115] TSETS    A=3 B=2 C=10 D=522 'reward_list'
00036 [L117] TGETS    A=2 B=1 C=12 D=268 'ext_info'
00037 [L117] IST      A=0 B=0 C=2 D=2 
00038 [L117] JMP      A=3 B=128 C=1 D=32769 target=40
00039 [L117] TNEW     A=2 B=0 C=0 D=0 
00040 [L118] GGET     A=3 B=0 C=2 D=2 'g_self'
00041 [L118] TGETS    A=3 B=3 C=3 D=771 'data'
00042 [L118] TGETS    A=4 B=2 C=14 D=526 'item'
00043 [L118] IST      A=0 B=0 C=4 D=4 
00044 [L118] JMP      A=5 B=128 C=1 D=32769 target=46
00045 [L118] TNEW     A=4 B=0 C=0 D=0 
00046 [L118] TSETS    A=4 B=3 C=13 D=781 'itemInfo'
00047 [L119] GGET     A=3 B=0 C=2 D=2 'g_self'
00048 [L119] TGETS    A=3 B=3 C=3 D=771 'data'
00049 [L119] TGETS    A=4 B=2 C=16 D=528 'attach_list'
00050 [L119] TSETS    A=4 B=3 C=15 D=783 'itemList'
00051 [L120] GGET     A=3 B=0 C=2 D=2 'g_self'
00052 [L120] TGETS    A=3 B=3 C=3 D=771 'data'
00053 [L120] TGETS    A=4 B=2 C=18 D=530 'prize_flag'
00054 [L120] TSETS    A=4 B=3 C=17 D=785 'prize_status'
00055 [L121] GGET     A=3 B=0 C=2 D=2 'g_self'
00056 [L121] TGETS    A=3 B=3 C=3 D=771 'data'
00057 [L121] TGETS    A=4 B=2 C=20 D=532 'reach_money'
00058 [L121] IST      A=0 B=0 C=4 D=4 
00059 [L121] JMP      A=5 B=128 C=1 D=32769 target=61
00060 [L121] KSHORT   A=4 B=0 C=0 D=0 0
00061 [L121] TSETS    A=4 B=3 C=19 D=787 'special_need_charge'
00062 [L123] GGET     A=3 B=0 C=2 D=2 'g_self'
00063 [L123] TGETS    A=4 B=1 C=21 D=277 'end_time'
00064 [L123] IST      A=0 B=0 C=4 D=4 
00065 [L123] JMP      A=5 B=128 C=2 D=32770 target=68
00066 [L123] GGET     A=4 B=0 C=2 D=2 'g_self'
00067 [L123] TGETS    A=4 B=4 C=21 D=1045 'end_time'
00068 [L123] TSETS    A=4 B=3 C=21 D=789 'end_time'
00069 [L124] GGET     A=3 B=0 C=22 D=22 'show'
00070 [L124] CALL     A=3 B=1 C=1 D=257 
00071 [L124] JMP      A=1 B=128 C=70 D=32838 target=142
00072 [L125] TGETS    A=1 B=0 C=0 D=0 'id'
00073 [L125] ISNEN    A=1 B=0 C=1 D=1 1
00074 [L125] JMP      A=1 B=128 C=30 D=32798 target=105
00075 [L126] IST      A=0 B=0 C=0 D=0 
00076 [L126] JMP      A=1 B=128 C=1 D=32769 target=78
00077 [L127] RET0     A=0 B=0 C=1 D=1 
00078 [L129] GGET     A=1 B=0 C=2 D=2 'g_self'
00079 [L129] TGETS    A=2 B=0 C=24 D=24 'flag'
00080 [L129] TSETS    A=2 B=1 C=23 D=279 'showtime'
00081 [L130] GGET     A=1 B=0 C=2 D=2 'g_self'
00082 [L130] TGETS    A=1 B=1 C=3 D=259 'data'
00083 [L130] GGET     A=2 B=0 C=2 D=2 'g_self'
00084 [L130] TGETS    A=2 B=2 C=3 D=515 'data'
00085 [L130] TGETS    A=2 B=2 C=4 D=516 'total_time'
00086 [L130] SUBVN    A=2 B=2 C=1 D=513 
00087 [L130] TSETS    A=2 B=1 C=4 D=260 'total_time'
00088 [L131] GGET     A=1 B=0 C=2 D=2 'g_self'
00089 [L131] GGET     A=2 B=0 C=2 D=2 'g_self'
00090 [L131] TGETS    A=2 B=2 C=3 D=515 'data'
00091 [L131] IST      A=0 B=0 C=2 D=2 
00092 [L131] JMP      A=3 B=128 C=1 D=32769 target=94
00093 [L131] TNEW     A=2 B=0 C=0 D=0 
00094 [L131] TSETS    A=2 B=1 C=3 D=259 'data'
00095 [L132] GGET     A=1 B=0 C=2 D=2 'g_self'
00096 [L132] TGETS    A=1 B=1 C=3 D=259 'data'
00097 [L132] TGETS    A=2 B=0 C=26 D=26 'prize_index'
00098 [L132] IST      A=0 B=0 C=2 D=2 
00099 [L132] JMP      A=3 B=128 C=1 D=32769 target=101
00100 [L132] KSHORT   A=2 B=0 C=1 D=1 1
00101 [L132] TSETS    A=2 B=1 C=25 D=281 'result_index'
00102 [L133] GGET     A=1 B=0 C=27 D=27 'start_turntable_anim'
00103 [L133] CALL     A=1 B=1 C=1 D=257 
00104 [L133] JMP      A=1 B=128 C=37 D=32805 target=142
00105 [L134] TGETS    A=1 B=0 C=0 D=0 'id'
00106 [L134] ISNEN    A=1 B=0 C=2 D=2 2
00107 [L134] JMP      A=1 B=128 C=27 D=32795 target=135
00108 [L135] GGET     A=1 B=0 C=2 D=2 'g_self'
00109 [L135] TGETS    A=2 B=0 C=24 D=24 'flag'
00110 [L135] TSETS    A=2 B=1 C=23 D=279 'showtime'
00111 [L136] GGET     A=1 B=0 C=2 D=2 'g_self'
00112 [L136] GGET     A=2 B=0 C=2 D=2 'g_self'
00113 [L136] TGETS    A=2 B=2 C=3 D=515 'data'
00114 [L136] IST      A=0 B=0 C=2 D=2 
00115 [L136] JMP      A=3 B=128 C=1 D=32769 target=117
00116 [L136] TNEW     A=2 B=0 C=0 D=0 
00117 [L136] TSETS    A=2 B=1 C=3 D=259 'data'
00118 [L137] GGET     A=1 B=0 C=2 D=2 'g_self'
00119 [L137] TGETS    A=1 B=1 C=3 D=259 'data'
00120 [L137] GGET     A=2 B=0 C=28 D=28 'd_ms'
00121 [L137] TGETS    A=2 B=2 C=29 D=541 'd_common_def'
00122 [L137] TGETS    A=2 B=2 C=17 D=529 'prize_status'
00123 [L137] TGETS    A=2 B=2 C=30 D=542 'has_got'
00124 [L137] TSETS    A=2 B=1 C=17 D=273 'prize_status'
00125 [L138] GGET     A=1 B=0 C=31 D=31 'update_rewarded_show'
00126 [L138] CALL     A=1 B=1 C=1 D=257 
00127 [L139] GGET     A=1 B=0 C=28 D=28 'd_ms'
00128 [L139] TGETS    A=1 B=1 C=32 D=288 'd_commonLayerUI'
00129 [L139] TGETS    A=1 B=1 C=33 D=289 'showPrizeResLayer'
00130 [L139] GGET     A=2 B=0 C=2 D=2 'g_self'
00131 [L139] TGETS    A=2 B=2 C=34 D=546 'main_layer'
00132 [L139] TGETS    A=3 B=0 C=35 D=35 'prize_list'
00133 [L139] CALL     A=1 B=1 C=3 D=259 
00134 [L139] JMP      A=1 B=128 C=7 D=32775 target=142
00135 [L140] TGETS    A=1 B=0 C=0 D=0 'id'
00136 [L140] ISNEN    A=1 B=0 C=3 D=3 3
00137 [L140] JMP      A=1 B=128 C=4 D=32772 target=142
00138 [L141] GGET     A=1 B=0 C=2 D=2 'g_self'
00139 [L141] KPRI     A=2 B=0 C=2 D=2 
00140 [L141] TSETS    A=2 B=1 C=23 D=279 'showtime'
00141 [L141] JMP      A=1 B=128 C=0 D=32768 target=142
00142 [L145] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto2 offset=0x518 source_lines=147-158 params=0
UPVALUES []
00001 [L148] GGET     A=0 B=0 C=0 D=0 'g_self'
00002 [L148] ISF      A=0 B=0 C=0 D=0 
00003 [L148] JMP      A=0 B=128 C=8 D=32776 target=12
00004 [L148] GGET     A=0 B=0 C=0 D=0 'g_self'
00005 [L148] TGETS    A=0 B=0 C=1 D=1 'start_time'
00006 [L148] ISF      A=0 B=0 C=0 D=0 
00007 [L148] JMP      A=0 B=128 C=4 D=32772 target=12
00008 [L148] GGET     A=0 B=0 C=0 D=0 'g_self'
00009 [L148] TGETS    A=0 B=0 C=2 D=2 'end_time'
00010 [L148] IST      A=0 B=0 C=0 D=0 
00011 [L148] JMP      A=0 B=128 C=2 D=32770 target=14
00012 [L149] KPRI     A=0 B=0 C=1 D=1 
00013 [L149] RET1     A=0 B=0 C=2 D=2 
00014 [L151] GGET     A=0 B=0 C=3 D=3 'd_ms'
00015 [L151] TGETS    A=0 B=0 C=4 D=4 'd_time'
00016 [L151] TGETS    A=0 B=0 C=5 D=5 'getTime'
00017 [L151] CALL     A=0 B=2 C=1 D=513 
00018 [L152] GGET     A=1 B=0 C=0 D=0 'g_self'
00019 [L152] TGETS    A=1 B=1 C=1 D=257 'start_time'
00020 [L152] ISGE     A=1 B=0 C=0 D=0 
00021 [L152] JMP      A=1 B=128 C=7 D=32775 target=29
00022 [L152] GGET     A=1 B=0 C=0 D=0 'g_self'
00023 [L152] TGETS    A=1 B=1 C=2 D=258 'end_time'
00024 [L152] ISGE     A=0 B=0 C=1 D=1 
00025 [L152] JMP      A=1 B=128 C=3 D=32771 target=29
00026 [L153] KPRI     A=1 B=0 C=2 D=2 
00027 [L153] RET1     A=1 B=0 C=2 D=2 
00028 [L153] JMP      A=1 B=128 C=2 D=32770 target=31
00029 [L155] KPRI     A=1 B=0 C=1 D=1 
00030 [L155] RET1     A=1 B=0 C=2 D=2 
00031 [L157] KPRI     A=1 B=0 C=2 D=2 
00032 [L157] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto3 offset=0x5ff source_lines=159-165 params=0
UPVALUES []
00001 [L160] GGET     A=0 B=0 C=0 D=0 'g_self'
00002 [L160] ISF      A=0 B=0 C=0 D=0 
00003 [L160] JMP      A=1 B=128 C=7 D=32775 target=11
00004 [L160] GGET     A=0 B=0 C=0 D=0 'g_self'
00005 [L160] TGETS    A=0 B=0 C=1 D=1 'showtime'
00006 [L160] ISF      A=0 B=0 C=0 D=0 
00007 [L160] JMP      A=1 B=128 C=3 D=32771 target=11
00008 [L161] KSHORT   A=0 B=0 C=1 D=1 1
00009 [L161] RET1     A=0 B=0 C=2 D=2 
00010 [L161] JMP      A=0 B=128 C=2 D=32770 target=13
00011 [L163] KSHORT   A=0 B=0 C=0 D=0 0
00012 [L163] RET1     A=0 B=0 C=2 D=2 
00013 [L165] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto4 offset=0x65e source_lines=166-176 params=1
UPVALUES []
00001 [L167] IST      A=0 B=0 C=0 D=0 
00002 [L167] JMP      A=1 B=128 C=1 D=32769 target=4
00003 [L168] RET0     A=0 B=0 C=1 D=1 
00004 [L170] GGET     A=1 B=0 C=0 D=0 'd_ms'
00005 [L170] TGETS    A=1 B=1 C=1 D=257 'd_time'
00006 [L170] TGETS    A=1 B=1 C=2 D=258 'getTime'
00007 [L170] CALL     A=1 B=2 C=1 D=513 
00008 [L171] KSHORT   A=2 B=0 C=1 D=1 1
00009 [L171] LEN      A=3 B=0 C=0 D=0 
00010 [L171] KSHORT   A=4 B=0 C=1 D=1 1
00011 [L171] FORI     A=2 B=128 C=8 D=32776 target=20
00012 [L172] TGETV    A=6 B=0 C=5 D=5 
00013 [L173] GGET     A=7 B=0 C=3 D=3 'g_self'
00014 [L173] TGETS    A=8 B=6 C=4 D=1540 'start_time'
00015 [L173] TSETS    A=8 B=7 C=4 D=1796 'start_time'
00016 [L174] GGET     A=7 B=0 C=3 D=3 'g_self'
00017 [L174] TGETS    A=8 B=6 C=5 D=1541 'end_time'
00018 [L174] TSETS    A=8 B=7 C=5 D=1797 'end_time'
00019 [L171] FORL     A=2 B=127 C=248 D=32760 target=12
00020 [L176] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto5 offset=0x72b source_lines=177-182 params=0
UPVALUES ['table']
00001 [L178] TNEW     A=0 B=0 C=0 D=0 
00002 [L178] GSET     A=0 B=0 C=0 D=0 'tmp_req'
00003 [L179] GGET     A=0 B=0 C=0 D=0 'tmp_req'
00004 [L179] KSHORT   A=1 B=0 C=0 D=0 0
00005 [L179] TSETS    A=1 B=0 C=1 D=1 'id'
00006 [L180] GGET     A=0 B=0 C=0 D=0 'tmp_req'
00007 [L180] UGET     A=1 B=0 C=0 D=0 table
00008 [L180] TGETS    A=1 B=1 C=3 D=259 'tostring'
00009 [L180] TNEW     A=2 B=0 C=0 D=0 
00010 [L180] CALL     A=1 B=2 C=2 D=514 
00011 [L180] TSETS    A=1 B=0 C=2 D=2 'data'
00012 [L181] GGET     A=0 B=0 C=4 D=4 'd_ms'
00013 [L181] TGETS    A=0 B=0 C=5 D=5 'd_u'
00014 [L181] TGETS    A=0 B=0 C=6 D=6 'main_server_send_msg'
00015 [L181] GGET     A=1 B=0 C=4 D=4 'd_ms'
00016 [L181] TGETS    A=1 B=1 C=7 D=263 'd_msg_def'
00017 [L181] TGETS    A=1 B=1 C=8 D=264 'gscl_msg_id'
00018 [L181] TGETS    A=1 B=1 C=9 D=265 'msg_rulai_activity'
00019 [L181] GGET     A=2 B=0 C=0 D=0 'tmp_req'
00020 [L181] CALL     A=0 B=1 C=3 D=259 
00021 [L182] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto6 offset=0x80a source_lines=184-190 params=0
UPVALUES ['cclog']
00001 [L185] UGET     A=0 B=0 C=0 D=0 cclog
00002 [L185] KSTR     A=1 B=0 C=0 D=0 'call turntableUI show()'
00003 [L185] CALL     A=0 B=1 C=2 D=258 
00004 [L186] GGET     A=0 B=0 C=1 D=1 'g_self'
00005 [L186] GGET     A=1 B=0 C=3 D=3 'd_ms'
00006 [L186] TGETS    A=1 B=1 C=4 D=260 'd_u'
00007 [L186] TGETS    A=1 B=1 C=5 D=261 'createScene'
00008 [L186] CALL     A=1 B=2 C=1 D=513 
00009 [L186] TSETS    A=1 B=0 C=2 D=2 'main_scene'
00010 [L187] GGET     A=0 B=0 C=3 D=3 'd_ms'
00011 [L187] TGETS    A=0 B=0 C=6 D=6 'd_loginUI'
00012 [L187] GGET     A=1 B=0 C=3 D=3 'd_ms'
00013 [L187] TGETS    A=1 B=1 C=6 D=262 'd_loginUI'
00014 [L187] TGETS    A=1 B=1 C=8 D=264 'senceID'
00015 [L187] TGETS    A=1 B=1 C=9 D=265 'rulaitable'
00016 [L187] TSETS    A=1 B=0 C=7 D=7 'g_currentSence'
00017 [L188] GGET     A=0 B=0 C=3 D=3 'd_ms'
00018 [L188] TGETS    A=0 B=0 C=4 D=4 'd_u'
00019 [L188] TGETS    A=0 B=0 C=10 D=10 'runScene'
00020 [L188] GGET     A=1 B=0 C=1 D=1 'g_self'
00021 [L188] TGETS    A=1 B=1 C=2 D=258 'main_scene'
00022 [L188] CALL     A=0 B=1 C=2 D=258 
00023 [L189] GGET     A=0 B=0 C=11 D=11 'create'
00024 [L189] GGET     A=1 B=0 C=1 D=1 'g_self'
00025 [L189] TGETS    A=1 B=1 C=2 D=258 'main_scene'
00026 [L189] CALL     A=0 B=1 C=2 D=258 
00027 [L190] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto7 offset=0x922 source_lines=191-197 params=0
UPVALUES ['cclog']
00001 [L192] UGET     A=0 B=0 C=0 D=0 cclog
00002 [L192] KSTR     A=1 B=0 C=0 D=0 'call turntableUI update()'
00003 [L192] CALL     A=0 B=1 C=2 D=258 
00004 [L193] GGET     A=0 B=0 C=1 D=1 'g_self'
00005 [L193] TGETS    A=0 B=0 C=2 D=2 'main_scene'
00006 [L193] ISF      A=0 B=0 C=0 D=0 
00007 [L193] JMP      A=1 B=128 C=11 D=32779 target=19
00008 [L194] GGET     A=0 B=0 C=1 D=1 'g_self'
00009 [L194] TGETS    A=0 B=0 C=2 D=2 'main_scene'
00010 [L194] MOV      A=1 B=0 C=0 D=0 
00011 [L194] TGETS    A=0 B=0 C=3 D=3 'removeChildByTag'
00012 [L194] GGET     A=2 B=0 C=4 D=4 'g_turntableUI'
00013 [L194] KPRI     A=3 B=0 C=2 D=2 
00014 [L194] CALL     A=0 B=1 C=4 D=260 
00015 [L195] GGET     A=0 B=0 C=5 D=5 'create'
00016 [L195] GGET     A=1 B=0 C=1 D=1 'g_self'
00017 [L195] TGETS    A=1 B=1 C=2 D=258 'main_scene'
00018 [L195] CALL     A=0 B=1 C=2 D=258 
00019 [L197] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto8 offset=0x9e9 source_lines=221-233 params=0
UPVALUES ['w', 'h', 'tick']
00001 [L222] GGET     A=0 B=0 C=0 D=0 'g_self'
00002 [L222] TGETS    A=0 B=0 C=1 D=1 'main_layer'
00003 [L222] MOV      A=1 B=0 C=0 D=0 
00004 [L222] TGETS    A=0 B=0 C=2 D=2 'removeChildByTag'
00005 [L222] GGET     A=2 B=0 C=0 D=0 'g_self'
00006 [L222] TGETS    A=2 B=2 C=3 D=515 'timetip_tag'
00007 [L222] KPRI     A=3 B=0 C=2 D=2 
00008 [L222] CALL     A=0 B=1 C=4 D=260 
00009 [L223] GGET     A=0 B=0 C=4 D=4 'd_ms'
00010 [L223] TGETS    A=0 B=0 C=5 D=5 'd_time'
00011 [L223] TGETS    A=0 B=0 C=6 D=6 'getRestTime'
00012 [L223] GGET     A=1 B=0 C=0 D=0 'g_self'
00013 [L223] TGETS    A=1 B=1 C=7 D=263 'end_time'
00014 [L223] GGET     A=2 B=0 C=4 D=4 'd_ms'
00015 [L223] TGETS    A=2 B=2 C=5 D=517 'd_time'
00016 [L223] TGETS    A=2 B=2 C=8 D=520 'g_format'
00017 [L223] TGETS    A=2 B=2 C=9 D=521 'hz'
00018 [L223] CALL     A=0 B=2 C=3 D=515 
00019 [L224] ISF      A=0 B=0 C=0 D=0 
00020 [L224] JMP      A=1 B=128 C=36 D=32804 target=57
00021 [L225] GGET     A=1 B=0 C=4 D=4 'd_ms'
00022 [L225] TGETS    A=1 B=1 C=10 D=266 'd_u'
00023 [L225] TGETS    A=1 B=1 C=11 D=267 'createByStyles'
00024 [L225] TDUP     A=2 B=0 C=12 D=12 {'kind': 'table', 'value': {'type': 'label', 'fontsize': 26}}
00025 [L225] TSETS    A=0 B=2 C=13 D=525 'string'
00026 [L225] UGET     A=3 B=0 C=0 D=0 w
00027 [L225] MULNV    A=3 B=3 C=0 D=768 
00028 [L225] ADDNV    A=3 B=3 C=1 D=769 
00029 [L225] TSETS    A=3 B=2 C=14 D=526 'x'
00030 [L225] UGET     A=3 B=0 C=1 D=1 h
00031 [L225] MULNV    A=3 B=3 C=2 D=770 
00032 [L225] ADDNV    A=3 B=3 C=1 D=769 
00033 [L225] TSETS    A=3 B=2 C=15 D=527 'y'
00034 [L225] TDUP     A=3 B=0 C=16 D=16 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00035 [L225] TSETS    A=3 B=2 C=17 D=529 'anchor'
00036 [L225] GGET     A=3 B=0 C=18 D=18 'g_Color'
00037 [L225] TGETS    A=3 B=3 C=19 D=787 'green'
00038 [L225] TSETS    A=3 B=2 C=20 D=532 'color'
00039 [L225] CALL     A=1 B=2 C=2 D=514 
00040 [L226] GGET     A=2 B=0 C=0 D=0 'g_self'
00041 [L226] TGETS    A=2 B=2 C=1 D=513 'main_layer'
00042 [L226] MOV      A=3 B=0 C=2 D=2 
00043 [L226] TGETS    A=2 B=2 C=21 D=533 'addChild'
00044 [L226] MOV      A=4 B=0 C=1 D=1 
00045 [L226] KSHORT   A=5 B=0 C=1 D=1 1
00046 [L226] GGET     A=6 B=0 C=0 D=0 'g_self'
00047 [L226] TGETS    A=6 B=6 C=3 D=1539 'timetip_tag'
00048 [L226] CALL     A=2 B=1 C=5 D=261 
00049 [L228] GGET     A=2 B=0 C=4 D=4 'd_ms'
00050 [L228] TGETS    A=2 B=2 C=10 D=522 'd_u'
00051 [L228] TGETS    A=2 B=2 C=22 D=534 'delay'
00052 [L228] GGET     A=3 B=0 C=0 D=0 'g_self'
00053 [L228] TGETS    A=3 B=3 C=1 D=769 'main_layer'
00054 [L228] KSHORT   A=4 B=0 C=1 D=1 1
00055 [L228] UGET     A=5 B=0 C=2 D=2 tick
00056 [L228] CALL     A=2 B=1 C=4 D=260 
00057 [L230] GGET     A=1 B=0 C=0 D=0 'g_self'
00058 [L230] TGETS    A=1 B=1 C=7 D=263 'end_time'
00059 [L230] GGET     A=2 B=0 C=4 D=4 'd_ms'
00060 [L230] TGETS    A=2 B=2 C=5 D=517 'd_time'
00061 [L230] TGETS    A=2 B=2 C=23 D=535 'getTime'
00062 [L230] CALL     A=2 B=2 C=1 D=513 
00063 [L230] SUBVV    A=1 B=1 C=2 D=258 
00064 [L230] KSHORT   A=2 B=0 C=0 D=0 0
00065 [L230] ISGT     A=1 B=0 C=2 D=2 
00066 [L230] JMP      A=1 B=128 C=2 D=32770 target=69
00067 [L231] GGET     A=1 B=0 C=24 D=24 'call_back_close'
00068 [L231] CALL     A=1 B=1 C=1 D=257 
00069 [L233] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto9 offset=0xc71 source_lines=244-249 params=0
UPVALUES ['table']
00001 [L245] TNEW     A=0 B=0 C=0 D=0 
00002 [L245] GSET     A=0 B=0 C=0 D=0 'tmp_req'
00003 [L246] GGET     A=0 B=0 C=0 D=0 'tmp_req'
00004 [L246] KSHORT   A=1 B=0 C=2 D=2 2
00005 [L246] TSETS    A=1 B=0 C=1 D=1 'id'
00006 [L247] GGET     A=0 B=0 C=0 D=0 'tmp_req'
00007 [L247] UGET     A=1 B=0 C=0 D=0 table
00008 [L247] TGETS    A=1 B=1 C=3 D=259 'tostring'
00009 [L247] TNEW     A=2 B=0 C=0 D=0 
00010 [L247] CALL     A=1 B=2 C=2 D=514 
00011 [L247] TSETS    A=1 B=0 C=2 D=2 'data'
00012 [L248] GGET     A=0 B=0 C=4 D=4 'd_ms'
00013 [L248] TGETS    A=0 B=0 C=5 D=5 'd_u'
00014 [L248] TGETS    A=0 B=0 C=6 D=6 'main_server_send_msg'
00015 [L248] GGET     A=1 B=0 C=4 D=4 'd_ms'
00016 [L248] TGETS    A=1 B=1 C=7 D=263 'd_msg_def'
00017 [L248] TGETS    A=1 B=1 C=8 D=264 'gscl_msg_id'
00018 [L248] TGETS    A=1 B=1 C=9 D=265 'msg_rulai_activity'
00019 [L248] GGET     A=2 B=0 C=0 D=0 'tmp_req'
00020 [L248] CALL     A=0 B=1 C=3 D=259 
00021 [L249] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto10 offset=0xd50 source_lines=267-276 params=1
UPVALUES ['itemInfo']
00001 [L268] GGET     A=1 B=0 C=0 D=0 'g_progressSchedule'
00002 [L268] ISEQP    A=1 B=0 C=0 D=0 
00003 [L268] JMP      A=1 B=128 C=4 D=32772 target=8
00004 [L268] GGET     A=1 B=0 C=0 D=0 'g_progressSchedule'
00005 [L268] ISEQN    A=1 B=0 C=0 D=0 0
00006 [L268] JMP      A=1 B=128 C=1 D=32769 target=8
00007 [L269] RET0     A=0 B=0 C=1 D=1 
00008 [L271] GGET     A=1 B=0 C=1 D=1 'g_self'
00009 [L271] TGETS    A=1 B=1 C=2 D=258 'data'
00010 [L271] ISF      A=0 B=0 C=1 D=1 
00011 [L271] JMP      A=2 B=128 C=11 D=32779 target=23
00012 [L271] GGET     A=1 B=0 C=1 D=1 'g_self'
00013 [L271] TGETS    A=1 B=1 C=2 D=258 'data'
00014 [L271] TGETS    A=1 B=1 C=3 D=259 'itemList'
00015 [L271] ISF      A=0 B=0 C=1 D=1 
00016 [L271] JMP      A=2 B=128 C=6 D=32774 target=23
00017 [L272] GGET     A=1 B=0 C=4 D=4 'showRewardDetail'
00018 [L272] GGET     A=2 B=0 C=1 D=1 'g_self'
00019 [L272] TGETS    A=2 B=2 C=2 D=514 'data'
00020 [L272] TGETS    A=2 B=2 C=3 D=515 'itemList'
00021 [L272] CALL     A=1 B=1 C=2 D=258 
00022 [L272] JMP      A=1 B=128 C=7 D=32775 target=30
00023 [L274] GGET     A=1 B=0 C=5 D=5 'd_ms'
00024 [L274] TGETS    A=1 B=1 C=6 D=262 'd_data'
00025 [L274] TGETS    A=1 B=1 C=7 D=263 'showItemIntro'
00026 [L274] GGET     A=2 B=0 C=1 D=1 'g_self'
00027 [L274] TGETS    A=2 B=2 C=8 D=520 'main_layer'
00028 [L274] UGET     A=3 B=0 C=0 D=0 itemInfo
00029 [L274] CALL     A=1 B=1 C=3 D=259 
00030 [L276] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto11 offset=0xe64 source_lines=199-319 params=1
UPVALUES ['table', 'kCCVerticalTextAlignmentCenter', 'tostring', 'string', 'scrSize', 'CCSizeMake']
00001 [L201] GGET     A=1 B=0 C=0 D=0 'g_self'
00002 [L201] GGET     A=2 B=0 C=2 D=2 'd_ms'
00003 [L201] TGETS    A=2 B=2 C=3 D=515 'd_u'
00004 [L201] TGETS    A=2 B=2 C=4 D=516 'createSwallowTouchLayer'
00005 [L201] MOV      A=3 B=0 C=0 D=0 
00006 [L201] KSHORT   A=4 B=0 C=50 D=50 50
00007 [L201] GGET     A=5 B=0 C=5 D=5 'g_turntableUI'
00008 [L201] CALL     A=2 B=2 C=4 D=516 
00009 [L201] TSETS    A=2 B=1 C=1 D=257 'main_layer'
00010 [L202] GGET     A=1 B=0 C=0 D=0 'g_self'
00011 [L202] TGETS    A=1 B=1 C=1 D=257 'main_layer'
00012 [L202] IST      A=0 B=0 C=1 D=1 
00013 [L202] JMP      A=1 B=128 C=1 D=32769 target=15
00014 [L203] UCLO     A=0 B=130 C=30 D=33310 target=557
00015 [L205] GGET     A=1 B=0 C=0 D=0 'g_self'
00016 [L205] TGETS    A=1 B=1 C=6 D=262 'data'
00017 [L208] GGET     A=2 B=0 C=0 D=0 'g_self'
00018 [L208] TGETS    A=2 B=2 C=1 D=513 'main_layer'
00019 [L208] MOV      A=3 B=0 C=2 D=2 
00020 [L208] TGETS    A=2 B=2 C=7 D=519 'addChild'
00021 [L208] GGET     A=4 B=0 C=2 D=2 'd_ms'
00022 [L208] TGETS    A=4 B=4 C=3 D=1027 'd_u'
00023 [L208] TGETS    A=4 B=4 C=8 D=1032 'createByStyles'
00024 [L208] TDUP     A=5 B=0 C=9 D=9 {'kind': 'table', 'value': {'scale_pic': 1, 'pic': 'v2/newTurnTableUI/man_bkg.png', 'x': 0.5, 'y': 0.5}}
00025 [L208] CALL     A=4 B=2 C=2 D=514 
00026 [L208] KSHORT   A=5 B=255 C=246 D=65526 -10
00027 [L208] CALL     A=2 B=1 C=4 D=260 
00028 [L210] GGET     A=2 B=0 C=2 D=2 'd_ms'
00029 [L210] TGETS    A=2 B=2 C=3 D=515 'd_u'
00030 [L210] TGETS    A=2 B=2 C=8 D=520 'createByStyles'
00031 [L210] TDUP     A=3 B=0 C=10 D=10 {'kind': 'table', 'value': {'pic': 'v2/newTurnTableUI/bkg1.png', 'x': 0.61, 'y': 0.5}}
00032 [L210] CALL     A=2 B=2 C=2 D=514 
00033 [L211] GGET     A=3 B=0 C=0 D=0 'g_self'
00034 [L211] TGETS    A=3 B=3 C=1 D=769 'main_layer'
00035 [L211] MOV      A=4 B=0 C=3 D=3 
00036 [L211] TGETS    A=3 B=3 C=7 D=775 'addChild'
00037 [L211] MOV      A=5 B=0 C=2 D=2 
00038 [L211] KSHORT   A=6 B=255 C=254 D=65534 -2
00039 [L211] CALL     A=3 B=1 C=4 D=260 
00040 [L212] GGET     A=3 B=0 C=2 D=2 'd_ms'
00041 [L212] TGETS    A=3 B=3 C=3 D=771 'd_u'
00042 [L212] TGETS    A=3 B=3 C=11 D=779 'getRealScale'
00043 [L212] MOV      A=4 B=0 C=2 D=2 
00044 [L212] CALL     A=3 B=3 C=2 D=770 
00045 [L213] GGET     A=5 B=0 C=0 D=0 'g_self'
00046 [L213] GGET     A=6 B=0 C=0 D=0 'g_self'
00047 [L213] MOV      A=7 B=0 C=3 D=3 
00048 [L213] TSETS    A=4 B=6 C=13 D=1549 'height'
00049 [L213] TSETS    A=7 B=5 C=12 D=1292 'width'
00050 [L215] GGET     A=5 B=0 C=14 D=14 'showTurntableLayer'
00051 [L215] CALL     A=5 B=1 C=1 D=257 
00052 [L217] GGET     A=5 B=0 C=2 D=2 'd_ms'
00053 [L217] TGETS    A=5 B=5 C=3 D=1283 'd_u'
00054 [L217] TGETS    A=5 B=5 C=8 D=1288 'createByStyles'
00055 [L217] TDUP     A=6 B=0 C=15 D=15 {'kind': 'table', 'value': {'pic': 'v2/newTurnTableUI/time_bkg.png'}}
00056 [L217] MULNV    A=7 B=3 C=0 D=768 
00057 [L217] ADDNV    A=7 B=7 C=1 D=1793 
00058 [L217] TSETS    A=7 B=6 C=16 D=1552 'x'
00059 [L217] MULNV    A=7 B=4 C=2 D=1026 
00060 [L217] ADDNV    A=7 B=7 C=1 D=1793 
00061 [L217] TSETS    A=7 B=6 C=17 D=1553 'y'
00062 [L217] TDUP     A=7 B=0 C=18 D=18 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00063 [L217] TSETS    A=7 B=6 C=19 D=1555 'anchor'
00064 [L217] CALL     A=5 B=2 C=2 D=514 
00065 [L218] GGET     A=6 B=0 C=0 D=0 'g_self'
00066 [L218] TGETS    A=6 B=6 C=1 D=1537 'main_layer'
00067 [L218] MOV      A=7 B=0 C=6 D=6 
00068 [L218] TGETS    A=6 B=6 C=7 D=1543 'addChild'
00069 [L218] MOV      A=8 B=0 C=5 D=5 
00070 [L218] CALL     A=6 B=1 C=3 D=259 
00071 [L219] GGET     A=6 B=0 C=2 D=2 'd_ms'
00072 [L219] TGETS    A=6 B=6 C=3 D=1539 'd_u'
00073 [L219] TGETS    A=6 B=6 C=8 D=1544 'createByStyles'
00074 [L219] TDUP     A=7 B=0 C=20 D=20 {'kind': 'table', 'value': {'type': 'label', 'fontsize': 26}}
00075 [L219] GGET     A=8 B=0 C=2 D=2 'd_ms'
00076 [L219] TGETS    A=8 B=8 C=21 D=2069 'd_hz'
00077 [L219] TGETS    A=8 B=8 C=22 D=2070 'gethz'
00078 [L219] KSTR     A=9 B=0 C=23 D=23 'turntable_1'
00079 [L219] CALL     A=8 B=2 C=2 D=514 
00080 [L219] TSETS    A=8 B=7 C=24 D=1816 'string'
00081 [L219] MULNV    A=8 B=3 C=3 D=771 
00082 [L219] ADDNV    A=8 B=8 C=1 D=2049 
00083 [L219] TSETS    A=8 B=7 C=16 D=1808 'x'
00084 [L219] MULNV    A=8 B=4 C=2 D=1026 
00085 [L219] ADDNV    A=8 B=8 C=1 D=2049 
00086 [L219] TSETS    A=8 B=7 C=17 D=1809 'y'
00087 [L219] TDUP     A=8 B=0 C=25 D=25 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00088 [L219] TSETS    A=8 B=7 C=19 D=1811 'anchor'
00089 [L219] CALL     A=6 B=2 C=2 D=514 
00090 [L220] GGET     A=7 B=0 C=0 D=0 'g_self'
00091 [L220] TGETS    A=7 B=7 C=1 D=1793 'main_layer'
00092 [L220] MOV      A=8 B=0 C=7 D=7 
00093 [L220] TGETS    A=7 B=7 C=7 D=1799 'addChild'
00094 [L220] MOV      A=9 B=0 C=6 D=6 
00095 [L220] KSHORT   A=10 B=0 C=1 D=1 1
00096 [L220] CALL     A=7 B=1 C=4 D=260 
00097 [L233] FNEW     A=7 B=0 C=26 D=26 {'kind': 'proto', 'id': 8}
00098 [L234] MOV      A=8 B=0 C=7 D=7 
00099 [L234] CALL     A=8 B=1 C=1 D=257 
00100 [L236] TGETS    A=8 B=1 C=27 D=283 'itemInfo'
00101 [L237] GGET     A=9 B=0 C=0 D=0 'g_self'
00102 [L237] TGETS    A=9 B=9 C=1 D=2305 'main_layer'
00103 [L237] MOV      A=10 B=0 C=9 D=9 
00104 [L237] TGETS    A=9 B=9 C=7 D=2311 'addChild'
00105 [L237] GGET     A=11 B=0 C=2 D=2 'd_ms'
00106 [L237] TGETS    A=11 B=11 C=3 D=2819 'd_u'
00107 [L237] TGETS    A=11 B=11 C=8 D=2824 'createByStyles'
00108 [L237] TDUP     A=12 B=0 C=28 D=28 {'kind': 'table', 'value': {'pic': 'v2/newTurnTableUI/reward_bkg.png'}}
00109 [L237] MULNV    A=13 B=3 C=4 D=772 
00110 [L237] ADDNV    A=13 B=13 C=1 D=3329 
00111 [L237] TSETS    A=13 B=12 C=16 D=3088 'x'
00112 [L237] MULNV    A=13 B=4 C=3 D=1027 
00113 [L237] ADDNV    A=13 B=13 C=1 D=3329 
00114 [L237] TSETS    A=13 B=12 C=17 D=3089 'y'
00115 [L237] CALL     A=11 B=0 C=2 D=2 
00116 [L237] CALLM    A=9 B=1 C=1 D=257 
00117 [L238] GGET     A=9 B=0 C=0 D=0 'g_self'
00118 [L238] TGETS    A=9 B=9 C=1 D=2305 'main_layer'
00119 [L238] MOV      A=10 B=0 C=9 D=9 
00120 [L238] TGETS    A=9 B=9 C=7 D=2311 'addChild'
00121 [L238] GGET     A=11 B=0 C=2 D=2 'd_ms'
00122 [L238] TGETS    A=11 B=11 C=3 D=2819 'd_u'
00123 [L238] TGETS    A=11 B=11 C=8 D=2824 'createByStyles'
00124 [L238] TDUP     A=12 B=0 C=29 D=29 {'kind': 'table', 'value': {'type': 'label', 'fontsize': 26}}
00125 [L238] GGET     A=13 B=0 C=2 D=2 'd_ms'
00126 [L238] TGETS    A=13 B=13 C=21 D=3349 'd_hz'
00127 [L238] TGETS    A=13 B=13 C=22 D=3350 'gethz'
00128 [L238] KSTR     A=14 B=0 C=30 D=30 'turntable_2'
00129 [L238] CALL     A=13 B=2 C=2 D=514 
00130 [L238] TSETS    A=13 B=12 C=24 D=3096 'string'
00131 [L238] MULNV    A=13 B=3 C=4 D=772 
00132 [L238] ADDNV    A=13 B=13 C=1 D=3329 
00133 [L238] TSETS    A=13 B=12 C=16 D=3088 'x'
00134 [L238] MULNV    A=13 B=4 C=5 D=1029 
00135 [L238] ADDNV    A=13 B=13 C=1 D=3329 
00136 [L238] TSETS    A=13 B=12 C=17 D=3089 'y'
00137 [L238] TDUP     A=13 B=0 C=31 D=31 {'kind': 'table', 'value': {1: 0.5, 2: 0.5}}
00138 [L238] TSETS    A=13 B=12 C=19 D=3091 'anchor'
00139 [L238] CALL     A=11 B=2 C=2 D=514 
00140 [L238] KSHORT   A=12 B=0 C=1 D=1 1
00141 [L238] CALL     A=9 B=1 C=4 D=260 
00142 [L240] TDUP     A=9 B=0 C=32 D=32 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00143 [L249] FNEW     A=10 B=0 C=33 D=33 {'kind': 'proto', 'id': 9}
00144 [L250] TGETS    A=11 B=1 C=34 D=290 'prize_status'
00145 [L250] ISF      A=0 B=0 C=11 D=11 
00146 [L250] JMP      A=11 B=128 C=7 D=32775 target=154
00147 [L250] GGET     A=11 B=0 C=2 D=2 'd_ms'
00148 [L250] TGETS    A=11 B=11 C=35 D=2851 'd_common_def'
00149 [L250] TGETS    A=11 B=11 C=34 D=2850 'prize_status'
00150 [L250] TGETS    A=11 B=11 C=36 D=2852 'unable_to_get'
00151 [L250] TGETS    A=12 B=1 C=34 D=290 'prize_status'
00152 [L250] ISNEV    A=11 B=0 C=12 D=12 
00153 [L250] JMP      A=11 B=128 C=67 D=32835 target=221
00154 [L251] GGET     A=11 B=0 C=0 D=0 'g_self'
00155 [L251] GGET     A=12 B=0 C=2 D=2 'd_ms'
00156 [L251] TGETS    A=12 B=12 C=3 D=3075 'd_u'
00157 [L251] TGETS    A=12 B=12 C=8 D=3080 'createByStyles'
00158 [L251] TDUP     A=13 B=0 C=38 D=38 {'kind': 'table', 'value': {'type': 'label', 'fontsize': 22, 'font': 'arial'}}
00159 [L251] GGET     A=14 B=0 C=2 D=2 'd_ms'
00160 [L251] TGETS    A=14 B=14 C=21 D=3605 'd_hz'
00161 [L251] TGETS    A=14 B=14 C=22 D=3606 'gethz'
00162 [L251] KSTR     A=15 B=0 C=39 D=39 'turntable_3'
00163 [L251] CALL     A=14 B=2 C=2 D=514 
00164 [L251] TSETS    A=14 B=13 C=24 D=3352 'string'
00165 [L251] MULNV    A=14 B=3 C=6 D=774 
00166 [L251] ADDNV    A=14 B=14 C=1 D=3585 
00167 [L251] TSETS    A=14 B=13 C=16 D=3344 'x'
00168 [L251] MULNV    A=14 B=4 C=0 D=1024 
00169 [L251] SUBNV    A=14 B=14 C=1 D=3585 
00170 [L251] TSETS    A=14 B=13 C=17 D=3345 'y'
00171 [L251] TDUP     A=14 B=0 C=40 D=40 {'kind': 'table', 'value': {1: 0, 2: 1}}
00172 [L251] TSETS    A=14 B=13 C=19 D=3347 'anchor'
00173 [L252] TDUP     A=14 B=0 C=41 D=41 {'kind': 'table', 'value': {2: 0}}
00174 [L252] MULVN    A=15 B=3 C=7 D=775 
00175 [L252] TSETB    A=15 B=14 C=1 D=3585 
00176 [L252] TSETS    A=14 B=13 C=42 D=3370 'font_rect'
00177 [L252] UGET     A=14 B=0 C=1 D=1 kCCVerticalTextAlignmentCenter
00178 [L252] TSETS    A=14 B=13 C=43 D=3371 'h_align'
00179 [L252] GGET     A=14 B=0 C=44 D=44 'g_Color'
00180 [L252] TGETS    A=14 B=14 C=45 D=3629 'black'
00181 [L252] TSETS    A=14 B=13 C=46 D=3374 'color'
00182 [L251] CALL     A=12 B=2 C=2 D=514 
00183 [L252] TSETS    A=12 B=11 C=37 D=2853 'reward_info'
00184 [L253] GGET     A=11 B=0 C=0 D=0 'g_self'
00185 [L253] TGETS    A=11 B=11 C=1 D=2817 'main_layer'
00186 [L253] MOV      A=12 B=0 C=11 D=11 
00187 [L253] TGETS    A=11 B=11 C=7 D=2823 'addChild'
00188 [L253] GGET     A=13 B=0 C=0 D=0 'g_self'
00189 [L253] TGETS    A=13 B=13 C=37 D=3365 'reward_info'
00190 [L253] CALL     A=11 B=1 C=3 D=259 
00191 [L254] GGET     A=11 B=0 C=0 D=0 'g_self'
00192 [L254] GGET     A=12 B=0 C=2 D=2 'd_ms'
00193 [L254] TGETS    A=12 B=12 C=3 D=3075 'd_u'
00194 [L254] TGETS    A=12 B=12 C=8 D=3080 'createByStyles'
00195 [L254] TDUP     A=13 B=0 C=48 D=48 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 22}}
00196 [L254] UGET     A=14 B=0 C=2 D=2 tostring
00197 [L254] TGETS    A=15 B=1 C=49 D=305 'special_need_charge'
00198 [L254] CALL     A=14 B=2 C=2 D=514 
00199 [L254] TSETS    A=14 B=13 C=24 D=3352 'string'
00200 [L254] MULNV    A=14 B=3 C=8 D=776 
00201 [L254] ADDNV    A=14 B=14 C=1 D=3585 
00202 [L254] TSETS    A=14 B=13 C=16 D=3344 'x'
00203 [L254] MULNV    A=14 B=4 C=6 D=1030 
00204 [L254] SUBNV    A=14 B=14 C=1 D=3585 
00205 [L254] TSETS    A=14 B=13 C=17 D=3345 'y'
00206 [L254] TDUP     A=14 B=0 C=50 D=50 {'kind': 'table', 'value': {1: 0, 2: 1}}
00207 [L254] TSETS    A=14 B=13 C=19 D=3347 'anchor'
00208 [L254] GGET     A=14 B=0 C=44 D=44 'g_Color'
00209 [L254] TGETS    A=14 B=14 C=51 D=3635 'white'
00210 [L254] TSETS    A=14 B=13 C=46 D=3374 'color'
00211 [L254] CALL     A=12 B=2 C=2 D=514 
00212 [L254] TSETS    A=12 B=11 C=47 D=2863 'reward_gold'
00213 [L255] GGET     A=11 B=0 C=0 D=0 'g_self'
00214 [L255] TGETS    A=11 B=11 C=1 D=2817 'main_layer'
00215 [L255] MOV      A=12 B=0 C=11 D=11 
00216 [L255] TGETS    A=11 B=11 C=7 D=2823 'addChild'
00217 [L255] GGET     A=13 B=0 C=0 D=0 'g_self'
00218 [L255] TGETS    A=13 B=13 C=47 D=3375 'reward_gold'
00219 [L255] CALL     A=11 B=1 C=3 D=259 
00220 [L255] JMP      A=11 B=128 C=26 D=32794 target=247
00221 [L256] GGET     A=11 B=0 C=2 D=2 'd_ms'
00222 [L256] TGETS    A=11 B=11 C=35 D=2851 'd_common_def'
00223 [L256] TGETS    A=11 B=11 C=34 D=2850 'prize_status'
00224 [L256] TGETS    A=11 B=11 C=52 D=2868 'wait_to_get'
00225 [L256] TGETS    A=12 B=1 C=34 D=290 'prize_status'
00226 [L256] ISEQV    A=11 B=0 C=12 D=12 
00227 [L256] JMP      A=11 B=128 C=7 D=32775 target=235
00228 [L256] GGET     A=11 B=0 C=2 D=2 'd_ms'
00229 [L256] TGETS    A=11 B=11 C=35 D=2851 'd_common_def'
00230 [L256] TGETS    A=11 B=11 C=34 D=2850 'prize_status'
00231 [L256] TGETS    A=11 B=11 C=53 D=2869 'has_got'
00232 [L256] TGETS    A=12 B=1 C=34 D=290 'prize_status'
00233 [L256] ISNEV    A=11 B=0 C=12 D=12 
00234 [L256] JMP      A=11 B=128 C=12 D=32780 target=247
00235 [L258] UGET     A=11 B=0 C=0 D=0 table
00236 [L258] TGETS    A=11 B=11 C=54 D=2870 'insert'
00237 [L258] MOV      A=12 B=0 C=9 D=9 
00238 [L258] TDUP     A=13 B=0 C=55 D=55 {'kind': 'table', 'value': {'npic': 'v2/actNoticeUI/get1.png', 'dispic': 'v2/actNoticeUI/get3.png', 'spic': 'v2/actNoticeUI/get2.png'}}
00239 [L258] MULNV    A=14 B=3 C=4 D=772 
00240 [L258] ADDNV    A=14 B=14 C=1 D=3585 
00241 [L258] TSETS    A=14 B=13 C=16 D=3344 'x'
00242 [L258] MULNV    A=14 B=4 C=9 D=1033 
00243 [L258] SUBNV    A=14 B=14 C=1 D=3585 
00244 [L258] TSETS    A=14 B=13 C=17 D=3345 'y'
00245 [L258] TSETS    A=10 B=13 C=56 D=3384 'call_back'
00246 [L258] CALL     A=11 B=1 C=3 D=259 
00247 [L260] TNEW     A=11 B=0 C=0 D=0 
00248 [L261] GGET     A=12 B=0 C=0 D=0 'g_self'
00249 [L261] TGETS    A=12 B=12 C=1 D=3073 'main_layer'
00250 [L261] MOV      A=13 B=0 C=12 D=12 
00251 [L261] TGETS    A=12 B=12 C=7 D=3079 'addChild'
00252 [L261] GGET     A=14 B=0 C=2 D=2 'd_ms'
00253 [L261] TGETS    A=14 B=14 C=3 D=3587 'd_u'
00254 [L261] TGETS    A=14 B=14 C=57 D=3641 'createMenu'
00255 [L261] MOV      A=15 B=0 C=9 D=9 
00256 [L261] MOV      A=16 B=0 C=11 D=11 
00257 [L261] CALL     A=14 B=0 C=3 D=3 
00258 [L261] CALLM    A=12 B=1 C=1 D=257 
00259 [L262] GGET     A=12 B=0 C=0 D=0 'g_self'
00260 [L262] TGETB    A=13 B=11 C=1 D=2817 
00261 [L262] TSETS    A=13 B=12 C=58 D=3130 'reward_btn'
00262 [L263] GGET     A=12 B=0 C=0 D=0 'g_self'
00263 [L263] TGETS    A=12 B=12 C=58 D=3130 'reward_btn'
00264 [L263] ISF      A=0 B=0 C=12 D=12 
00265 [L263] JMP      A=13 B=128 C=13 D=32781 target=279
00266 [L263] GGET     A=12 B=0 C=2 D=2 'd_ms'
00267 [L263] TGETS    A=12 B=12 C=35 D=3107 'd_common_def'
00268 [L263] TGETS    A=12 B=12 C=34 D=3106 'prize_status'
00269 [L263] TGETS    A=12 B=12 C=53 D=3125 'has_got'
00270 [L263] TGETS    A=13 B=1 C=34 D=290 'prize_status'
00271 [L263] ISNEV    A=12 B=0 C=13 D=13 
00272 [L263] JMP      A=12 B=128 C=6 D=32774 target=279
00273 [L264] GGET     A=12 B=0 C=0 D=0 'g_self'
00274 [L264] TGETS    A=12 B=12 C=58 D=3130 'reward_btn'
00275 [L264] MOV      A=13 B=0 C=12 D=12 
00276 [L264] TGETS    A=12 B=12 C=59 D=3131 'setEnabled'
00277 [L264] KPRI     A=14 B=0 C=1 D=1 
00278 [L264] CALL     A=12 B=1 C=3 D=259 
00279 [L276] FNEW     A=12 B=0 C=60 D=60 {'kind': 'proto', 'id': 10}
00280 [L277] TDUP     A=13 B=0 C=61 D=61 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00281 [L282] GGET     A=14 B=0 C=2 D=2 'd_ms'
00282 [L282] TGETS    A=14 B=14 C=62 D=3646 'd_data'
00283 [L282] TGETS    A=14 B=14 C=63 D=3647 'getCertainSmallSprite'
00284 [L282] TGETS    A=15 B=8 C=64 D=2112 'object_type'
00285 [L282] TGETS    A=16 B=8 C=65 D=2113 'attach_type'
00286 [L282] TGETS    A=17 B=8 C=66 D=2114 'attach_level'
00287 [L282] CALL     A=14 B=2 C=4 D=516 
00288 [L283] UGET     A=15 B=0 C=0 D=0 table
00289 [L283] TGETS    A=15 B=15 C=54 D=3894 'insert'
00290 [L283] MOV      A=16 B=0 C=13 D=13 
00291 [L283] TDUP     A=17 B=0 C=67 D=67 {'kind': 'table', 'value': {'scale_pic': 0.9}}
00292 [L283] TSETS    A=14 B=17 C=68 D=4420 'nsprite'
00293 [L283] TSETS    A=14 B=17 C=69 D=4421 'ssprite'
00294 [L283] MULNV    A=18 B=3 C=10 D=778 
00295 [L283] ADDNV    A=18 B=18 C=1 D=4609 
00296 [L283] TSETS    A=18 B=17 C=16 D=4368 'x'
00297 [L283] MULNV    A=18 B=4 C=11 D=1035 
00298 [L283] ADDNV    A=18 B=18 C=1 D=4609 
00299 [L283] TSETS    A=18 B=17 C=17 D=4369 'y'
00300 [L283] TSETS    A=12 B=17 C=56 D=4408 'call_back'
00301 [L283] CALL     A=15 B=1 C=3 D=259 
00302 [L284] GGET     A=15 B=0 C=2 D=2 'd_ms'
00303 [L284] TGETS    A=15 B=15 C=62 D=3902 'd_data'
00304 [L284] TGETS    A=15 B=15 C=70 D=3910 'getNameByTypeId'
00305 [L284] TGETS    A=16 B=8 C=64 D=2112 'object_type'
00306 [L284] TGETS    A=17 B=8 C=65 D=2113 'attach_type'
00307 [L284] CALL     A=15 B=2 C=3 D=515 
00308 [L285] GGET     A=16 B=0 C=0 D=0 'g_self'
00309 [L285] TGETS    A=16 B=16 C=1 D=4097 'main_layer'
00310 [L285] MOV      A=17 B=0 C=16 D=16 
00311 [L285] TGETS    A=16 B=16 C=7 D=4103 'addChild'
00312 [L285] GGET     A=18 B=0 C=2 D=2 'd_ms'
00313 [L285] TGETS    A=18 B=18 C=3 D=4611 'd_u'
00314 [L285] TGETS    A=18 B=18 C=8 D=4616 'createByStyles'
00315 [L285] TDUP     A=19 B=0 C=71 D=71 {'kind': 'table', 'value': {'y': 0.5, 'font': 'arial', 'type': 'label', 'fontsize': 22}}
00316 [L285] TSETS    A=15 B=19 C=24 D=4888 'string'
00317 [L285] MULNV    A=20 B=3 C=4 D=772 
00318 [L285] ADDNV    A=20 B=20 C=1 D=5121 
00319 [L285] TSETS    A=20 B=19 C=16 D=4880 'x'
00320 [L285] TDUP     A=20 B=0 C=72 D=72 {'kind': 'table', 'value': {1: 0.5, 2: 0.5}}
00321 [L285] TSETS    A=20 B=19 C=19 D=4883 'anchor'
00322 [L285] GGET     A=20 B=0 C=44 D=44 'g_Color'
00323 [L285] TGETS    A=20 B=20 C=51 D=5171 'white'
00324 [L285] TSETS    A=20 B=19 C=46 D=4910 'color'
00325 [L285] CALL     A=18 B=0 C=2 D=2 
00326 [L285] CALLM    A=16 B=1 C=1 D=257 
00327 [L288] GGET     A=16 B=0 C=0 D=0 'g_self'
00328 [L288] TGETS    A=16 B=16 C=1 D=4097 'main_layer'
00329 [L288] MOV      A=17 B=0 C=16 D=16 
00330 [L288] TGETS    A=16 B=16 C=7 D=4103 'addChild'
00331 [L288] GGET     A=18 B=0 C=2 D=2 'd_ms'
00332 [L288] TGETS    A=18 B=18 C=3 D=4611 'd_u'
00333 [L288] TGETS    A=18 B=18 C=8 D=4616 'createByStyles'
00334 [L288] TDUP     A=19 B=0 C=73 D=73 {'kind': 'table', 'value': {'type': 'label', 'fontsize': 28, 'font': 'arial'}}
00335 [L288] UGET     A=20 B=0 C=3 D=3 string
00336 [L288] TGETS    A=20 B=20 C=74 D=5194 'format'
00337 [L288] GGET     A=21 B=0 C=2 D=2 'd_ms'
00338 [L288] TGETS    A=21 B=21 C=21 D=5397 'd_hz'
00339 [L288] TGETS    A=21 B=21 C=22 D=5398 'gethz'
00340 [L288] KSTR     A=22 B=0 C=75 D=75 'turntable_4'
00341 [L288] CALL     A=21 B=2 C=2 D=514 
00342 [L288] TGETS    A=22 B=1 C=76 D=332 'total_charge'
00343 [L288] CALL     A=20 B=2 C=3 D=515 
00344 [L288] TSETS    A=20 B=19 C=24 D=4888 'string'
00345 [L289] MULNV    A=20 B=3 C=12 D=780 
00346 [L289] ADDNV    A=20 B=20 C=1 D=5121 
00347 [L289] TSETS    A=20 B=19 C=16 D=4880 'x'
00348 [L289] MULNV    A=20 B=3 C=13 D=781 
00349 [L289] ADDNV    A=20 B=20 C=1 D=5121 
00350 [L289] TSETS    A=20 B=19 C=17 D=4881 'y'
00351 [L289] UGET     A=20 B=0 C=1 D=1 kCCVerticalTextAlignmentCenter
00352 [L289] TSETS    A=20 B=19 C=43 D=4907 'h_align'
00353 [L289] TDUP     A=20 B=0 C=77 D=77 {'kind': 'table', 'value': {1: 0, 2: 1}}
00354 [L289] TSETS    A=20 B=19 C=19 D=4883 'anchor'
00355 [L289] TDUP     A=20 B=0 C=78 D=78 {'kind': 'table', 'value': {2: 0}}
00356 [L289] MULVN    A=21 B=3 C=14 D=782 
00357 [L289] TSETB    A=21 B=20 C=1 D=5121 
00358 [L289] TSETS    A=20 B=19 C=42 D=4906 'font_rect'
00359 [L289] GGET     A=20 B=0 C=44 D=44 'g_Color'
00360 [L289] TGETS    A=20 B=20 C=79 D=5199 'yellow'
00361 [L289] TSETS    A=20 B=19 C=46 D=4910 'color'
00362 [L288] CALL     A=18 B=0 C=2 D=2 
00363 [L288] CALLM    A=16 B=1 C=1 D=257 
00364 [L291] GGET     A=16 B=0 C=0 D=0 'g_self'
00365 [L291] TGETS    A=16 B=16 C=1 D=4097 'main_layer'
00366 [L291] MOV      A=17 B=0 C=16 D=16 
00367 [L291] TGETS    A=16 B=16 C=7 D=4103 'addChild'
00368 [L291] GGET     A=18 B=0 C=2 D=2 'd_ms'
00369 [L291] TGETS    A=18 B=18 C=3 D=4611 'd_u'
00370 [L291] TGETS    A=18 B=18 C=8 D=4616 'createByStyles'
00371 [L291] TDUP     A=19 B=0 C=80 D=80 {'kind': 'table', 'value': {'type': 'label', 'fontsize': 24, 'font': 'arial'}}
00372 [L291] GGET     A=20 B=0 C=2 D=2 'd_ms'
00373 [L291] TGETS    A=20 B=20 C=21 D=5141 'd_hz'
00374 [L291] TGETS    A=20 B=20 C=22 D=5142 'gethz'
00375 [L291] KSTR     A=21 B=0 C=81 D=81 'turntable_5'
00376 [L291] CALL     A=20 B=2 C=2 D=514 
00377 [L291] TSETS    A=20 B=19 C=24 D=4888 'string'
00378 [L291] MULNV    A=20 B=3 C=13 D=781 
00379 [L291] ADDNV    A=20 B=20 C=1 D=5121 
00380 [L291] TSETS    A=20 B=19 C=16 D=4880 'x'
00381 [L291] MULNV    A=20 B=4 C=15 D=1039 
00382 [L291] SUBNV    A=20 B=20 C=1 D=5121 
00383 [L291] TSETS    A=20 B=19 C=17 D=4881 'y'
00384 [L291] TDUP     A=20 B=0 C=82 D=82 {'kind': 'table', 'value': {1: 0, 2: 1}}
00385 [L291] TSETS    A=20 B=19 C=19 D=4883 'anchor'
00386 [L292] TDUP     A=20 B=0 C=83 D=83 {'kind': 'table', 'value': {2: 0}}
00387 [L292] MULVN    A=21 B=3 C=16 D=784 
00388 [L292] TSETB    A=21 B=20 C=1 D=5121 
00389 [L292] TSETS    A=20 B=19 C=42 D=4906 'font_rect'
00390 [L292] GGET     A=20 B=0 C=44 D=44 'g_Color'
00391 [L292] TGETS    A=20 B=20 C=51 D=5171 'white'
00392 [L292] TSETS    A=20 B=19 C=46 D=4910 'color'
00393 [L291] CALL     A=18 B=0 C=2 D=2 
00394 [L291] CALLM    A=16 B=1 C=1 D=257 
00395 [L294] UGET     A=16 B=0 C=0 D=0 table
00396 [L294] TGETS    A=16 B=16 C=54 D=4150 'insert'
00397 [L294] MOV      A=17 B=0 C=13 D=13 
00398 [L294] TDUP     A=18 B=0 C=84 D=84 {'kind': 'table', 'value': {'npic': 'v2/common/close1.png', 'spic': 'v2/common/close2.png'}}
00399 [L294] MULNV    A=19 B=3 C=17 D=785 
00400 [L294] ADDNV    A=19 B=19 C=1 D=4865 
00401 [L294] TSETS    A=19 B=18 C=16 D=4624 'x'
00402 [L294] MULNV    A=19 B=4 C=18 D=1042 
00403 [L294] ADDNV    A=19 B=19 C=1 D=4865 
00404 [L294] TSETS    A=19 B=18 C=17 D=4625 'y'
00405 [L294] GGET     A=19 B=0 C=85 D=85 'call_back_close'
00406 [L294] TSETS    A=19 B=18 C=56 D=4664 'call_back'
00407 [L294] CALL     A=16 B=1 C=3 D=259 
00408 [L295] GGET     A=16 B=0 C=0 D=0 'g_self'
00409 [L295] GGET     A=17 B=0 C=2 D=2 'd_ms'
00410 [L295] TGETS    A=17 B=17 C=3 D=4355 'd_u'
00411 [L295] TGETS    A=17 B=17 C=8 D=4360 'createByStyles'
00412 [L295] TDUP     A=18 B=0 C=87 D=87 {'kind': 'table', 'value': {'pic': 'v2/newTurnTableUI/info_bkg.png'}}
00413 [L295] MULNV    A=19 B=3 C=19 D=787 
00414 [L295] ADDNV    A=19 B=19 C=1 D=4865 
00415 [L295] TSETS    A=19 B=18 C=16 D=4624 'x'
00416 [L295] MULNV    A=19 B=4 C=4 D=1028 
00417 [L295] ADDNV    A=19 B=19 C=1 D=4865 
00418 [L295] TSETS    A=19 B=18 C=17 D=4625 'y'
00419 [L295] CALL     A=17 B=2 C=2 D=514 
00420 [L295] TSETS    A=17 B=16 C=86 D=4182 'info_bkg'
00421 [L296] GGET     A=16 B=0 C=0 D=0 'g_self'
00422 [L296] TGETS    A=16 B=16 C=1 D=4097 'main_layer'
00423 [L296] MOV      A=17 B=0 C=16 D=16 
00424 [L296] TGETS    A=16 B=16 C=7 D=4103 'addChild'
00425 [L296] GGET     A=18 B=0 C=0 D=0 'g_self'
00426 [L296] TGETS    A=18 B=18 C=86 D=4694 'info_bkg'
00427 [L296] CALL     A=16 B=1 C=3 D=259 
00428 [L297] UGET     A=16 B=0 C=0 D=0 table
00429 [L297] TGETS    A=16 B=16 C=54 D=4150 'insert'
00430 [L297] MOV      A=17 B=0 C=13 D=13 
00431 [L297] TDUP     A=18 B=0 C=88 D=88 {'kind': 'table', 'value': {'npic': 'v2/newTurnTableUI/charge1.png', 'dispic': 'v2/newTurnTableUI/charge3.png', 'spic': 'v2/newTurnTableUI/charge2.png'}}
00432 [L297] MULNV    A=19 B=3 C=19 D=787 
00433 [L297] ADDNV    A=19 B=19 C=1 D=4865 
00434 [L297] TSETS    A=19 B=18 C=16 D=4624 'x'
00435 [L297] MULNV    A=19 B=4 C=20 D=1044 
00436 [L297] SUBNV    A=19 B=19 C=1 D=4865 
00437 [L297] TSETS    A=19 B=18 C=17 D=4625 'y'
00438 [L297] TDUP     A=19 B=0 C=89 D=89 {'kind': 'table', 'value': {1: 0.5, 2: 0.5}}
00439 [L297] TSETS    A=19 B=18 C=19 D=4627 'anchor'
00440 [L297] GGET     A=19 B=0 C=90 D=90 'recharge'
00441 [L297] TSETS    A=19 B=18 C=56 D=4664 'call_back'
00442 [L297] CALL     A=16 B=1 C=3 D=259 
00443 [L298] GGET     A=16 B=0 C=0 D=0 'g_self'
00444 [L298] TGETS    A=16 B=16 C=1 D=4097 'main_layer'
00445 [L298] MOV      A=17 B=0 C=16 D=16 
00446 [L298] TGETS    A=16 B=16 C=7 D=4103 'addChild'
00447 [L298] GGET     A=18 B=0 C=2 D=2 'd_ms'
00448 [L298] TGETS    A=18 B=18 C=3 D=4611 'd_u'
00449 [L298] TGETS    A=18 B=18 C=57 D=4665 'createMenu'
00450 [L298] MOV      A=19 B=0 C=13 D=13 
00451 [L298] CALL     A=18 B=0 C=2 D=2 
00452 [L298] CALLM    A=16 B=1 C=1 D=257 
00453 [L300] ISF      A=0 B=0 C=8 D=8 
00454 [L300] JMP      A=16 B=128 C=32 D=32800 target=487
00455 [L300] TGETS    A=16 B=8 C=91 D=2139 'attach_count'
00456 [L300] ISF      A=0 B=0 C=16 D=16 
00457 [L300] JMP      A=17 B=128 C=29 D=32797 target=487
00458 [L300] TGETS    A=16 B=8 C=91 D=2139 'attach_count'
00459 [L300] KSHORT   A=17 B=0 C=1 D=1 1
00460 [L300] ISGE     A=17 B=0 C=16 D=16 
00461 [L300] JMP      A=16 B=128 C=25 D=32793 target=487
00462 [L301] GGET     A=16 B=0 C=0 D=0 'g_self'
00463 [L301] TGETS    A=16 B=16 C=1 D=4097 'main_layer'
00464 [L301] MOV      A=17 B=0 C=16 D=16 
00465 [L301] TGETS    A=16 B=16 C=7 D=4103 'addChild'
00466 [L301] GGET     A=18 B=0 C=2 D=2 'd_ms'
00467 [L301] TGETS    A=18 B=18 C=3 D=4611 'd_u'
00468 [L301] TGETS    A=18 B=18 C=8 D=4616 'createByStyles'
00469 [L301] TDUP     A=19 B=0 C=92 D=92 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 18}}
00470 [L301] UGET     A=20 B=0 C=2 D=2 tostring
00471 [L301] TGETS    A=21 B=8 C=91 D=2139 'attach_count'
00472 [L301] CALL     A=20 B=2 C=2 D=514 
00473 [L301] TSETS    A=20 B=19 C=24 D=4888 'string'
00474 [L301] MULNV    A=20 B=3 C=21 D=789 
00475 [L301] ADDNV    A=20 B=20 C=1 D=5121 
00476 [L301] TSETS    A=20 B=19 C=16 D=4880 'x'
00477 [L301] MULNV    A=20 B=4 C=22 D=1046 
00478 [L301] ADDNV    A=20 B=20 C=1 D=5121 
00479 [L301] TSETS    A=20 B=19 C=17 D=4881 'y'
00480 [L301] TDUP     A=20 B=0 C=93 D=93 {'kind': 'table', 'value': {1: 1, 2: 0}}
00481 [L301] TSETS    A=20 B=19 C=19 D=4883 'anchor'
00482 [L301] GGET     A=20 B=0 C=44 D=44 'g_Color'
00483 [L301] TGETS    A=20 B=20 C=94 D=5214 'green'
00484 [L301] TSETS    A=20 B=19 C=46 D=4910 'color'
00485 [L301] CALL     A=18 B=0 C=2 D=2 
00486 [L301] CALLM    A=16 B=1 C=1 D=257 
00487 [L305] TGETS    A=16 B=1 C=95 D=351 'charge_his'
00488 [L305] IST      A=0 B=0 C=16 D=16 
00489 [L305] JMP      A=17 B=128 C=1 D=32769 target=491
00490 [L305] TNEW     A=16 B=0 C=0 D=0 
00491 [L306] TDUP     A=17 B=0 C=96 D=96 {'kind': 'table', 'value': {}}
00492 [L306] MULNV    A=18 B=3 C=23 D=791 
00493 [L306] ADDNV    A=18 B=18 C=1 D=4609 
00494 [L306] UGET     A=19 B=0 C=4 D=4 scrSize
00495 [L306] TGETS    A=19 B=19 C=12 D=4876 'width'
00496 [L306] MULVV    A=18 B=18 C=19 D=4627 
00497 [L306] TSETS    A=18 B=17 C=16 D=4368 'x'
00498 [L306] MULNV    A=18 B=4 C=24 D=1048 
00499 [L306] ADDNV    A=18 B=18 C=1 D=4609 
00500 [L306] UGET     A=19 B=0 C=4 D=4 scrSize
00501 [L306] TGETS    A=19 B=19 C=13 D=4877 'height'
00502 [L306] MULVV    A=18 B=18 C=19 D=4627 
00503 [L306] TSETS    A=18 B=17 C=17 D=4369 'y'
00504 [L306] MULNV    A=18 B=3 C=12 D=780 
00505 [L306] UGET     A=19 B=0 C=4 D=4 scrSize
00506 [L306] TGETS    A=19 B=19 C=12 D=4876 'width'
00507 [L306] MULVV    A=18 B=18 C=19 D=4627 
00508 [L306] TSETS    A=18 B=17 C=12 D=4364 'width'
00509 [L306] MULNV    A=18 B=4 C=25 D=1049 
00510 [L306] UGET     A=19 B=0 C=4 D=4 scrSize
00511 [L306] TGETS    A=19 B=19 C=13 D=4877 'height'
00512 [L306] MULVV    A=18 B=18 C=19 D=4627 
00513 [L306] TSETS    A=18 B=17 C=13 D=4365 'height'
00514 [L307] UGET     A=18 B=0 C=5 D=5 CCSizeMake
00515 [L307] TGETS    A=19 B=17 C=12 D=4364 'width'
00516 [L307] TGETS    A=20 B=17 C=13 D=4365 'height'
00517 [L307] MULNV    A=20 B=20 C=26 D=5146 
00518 [L307] CALL     A=18 B=2 C=3 D=515 
00519 [L308] GGET     A=19 B=0 C=2 D=2 'd_ms'
00520 [L308] TGETS    A=19 B=19 C=97 D=4961 'd_tableView'
00521 [L308] TGETS    A=19 B=19 C=98 D=4962 'tableView'
00522 [L308] GGET     A=20 B=0 C=0 D=0 'g_self'
00523 [L308] TGETS    A=20 B=20 C=1 D=5121 'main_layer'
00524 [L308] MOV      A=21 B=0 C=17 D=17 
00525 [L308] CALL     A=19 B=2 C=3 D=515 
00526 [L309] GGET     A=20 B=0 C=99 D=99 'getHistoryCellsDataSource'
00527 [L309] MOV      A=21 B=0 C=16 D=16 
00528 [L309] MOV      A=22 B=0 C=18 D=18 
00529 [L309] CALL     A=20 B=2 C=3 D=515 
00530 [L310] MOV      A=22 B=0 C=19 D=19 
00531 [L310] TGETS    A=21 B=19 C=100 D=4964 'startScroll'
00532 [L310] CALL     A=21 B=1 C=2 D=258 
00533 [L311] MOV      A=22 B=0 C=19 D=19 
00534 [L311] TGETS    A=21 B=19 C=101 D=4965 'setDataSource'
00535 [L311] MOV      A=23 B=0 C=20 D=20 
00536 [L311] CALL     A=21 B=1 C=3 D=259 
00537 [L312] KSHORT   A=21 B=0 C=1 D=1 1
00538 [L313] KSHORT   A=22 B=0 C=1 D=1 1
00539 [L313] LEN      A=23 B=0 C=16 D=16 
00540 [L313] KSHORT   A=24 B=0 C=1 D=1 1
00541 [L313] FORI     A=22 B=128 C=9 D=32777 target=551
00542 [L314] TGETV    A=26 B=16 C=25 D=4121 
00543 [L314] ISF      A=0 B=0 C=26 D=26 
00544 [L314] JMP      A=27 B=128 C=5 D=32773 target=550
00545 [L314] TGETV    A=26 B=16 C=25 D=4121 
00546 [L314] TGETS    A=26 B=26 C=102 D=6758 'status'
00547 [L314] ISF      A=0 B=0 C=26 D=26 
00548 [L314] JMP      A=27 B=128 C=1 D=32769 target=550
00549 [L315] MOV      A=21 B=0 C=25 D=25 
00550 [L313] FORL     A=22 B=127 C=247 D=32759 target=542
00551 [L318] MOV      A=23 B=0 C=19 D=19 
00552 [L318] TGETS    A=22 B=19 C=103 D=4967 'showIndexAtCenter'
00553 [L318] MOV      A=24 B=0 C=21 D=21 
00554 [L318] CALL     A=22 B=1 C=3 D=259 
00555 [L319] UCLO     A=0 B=128 C=0 D=32768 target=556
00556 [L319] RET0     A=0 B=0 C=1 D=1 
00557 [L319] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto12 offset=0x2250 source_lines=325-327 params=0
UPVALUES ['num']
00001 [L326] UGET     A=0 B=0 C=0 D=0 num
00002 [L326] RET1     A=0 B=0 C=2 D=2 

FUNCTION proto13 offset=0x226e source_lines=329-335 params=1
UPVALUES ['CCNode', 'list', 'cellSize']
00001 [L330] UGET     A=1 B=0 C=0 D=0 CCNode
00002 [L330] MOV      A=2 B=0 C=1 D=1 
00003 [L330] TGETS    A=1 B=1 C=0 D=256 'create'
00004 [L330] CALL     A=1 B=2 C=2 D=514 
00005 [L331] UGET     A=2 B=0 C=1 D=1 list
00006 [L331] TGETV    A=2 B=2 C=0 D=512 
00007 [L331] ISF      A=0 B=0 C=2 D=2 
00008 [L331] JMP      A=3 B=128 C=6 D=32774 target=15
00009 [L332] GGET     A=2 B=0 C=1 D=1 'createHistoryCell'
00010 [L332] MOV      A=3 B=0 C=1 D=1 
00011 [L332] UGET     A=4 B=0 C=1 D=1 list
00012 [L332] TGETV    A=4 B=4 C=0 D=1024 
00013 [L332] UGET     A=5 B=0 C=2 D=2 cellSize
00014 [L332] CALL     A=2 B=1 C=4 D=260 
00015 [L334] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto14 offset=0x2309 source_lines=337-339 params=1
UPVALUES ['cellSize']
00001 [L338] UGET     A=1 B=0 C=0 D=0 cellSize
00002 [L338] TGETS    A=1 B=1 C=0 D=256 'height'
00003 [L338] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto15 offset=0x2340 source_lines=321-342 params=2
UPVALUES ['CCNode']
00001 [L322] TNEW     A=2 B=0 C=0 D=0 
00002 [L324] LEN      A=3 B=0 C=0 D=0 
00003 [L327] FNEW     A=4 B=0 C=1 D=1 {'kind': 'proto', 'id': 12}
00004 [L327] TSETS    A=4 B=2 C=0 D=512 'tableViewNumberOfRows'
00005 [L335] FNEW     A=4 B=0 C=3 D=3 {'kind': 'proto', 'id': 13}
00006 [L335] TSETS    A=4 B=2 C=2 D=514 'drawCellAtIndex'
00007 [L339] FNEW     A=4 B=0 C=5 D=5 {'kind': 'proto', 'id': 14}
00008 [L339] TSETS    A=4 B=2 C=4 D=516 'heightForRowAtIndex'
00009 [L341] UCLO     A=0 B=128 C=0 D=32768 target=10
00010 [L341] RET1     A=2 B=0 C=2 D=2 

FUNCTION proto16 offset=0x23eb source_lines=344-354 params=3
UPVALUES []
00001 [L345] KPRI     A=3 B=0 C=0 D=0 
00002 [L346] TGETS    A=4 B=1 C=0 D=256 'status'
00003 [L346] ISF      A=0 B=0 C=4 D=4 
00004 [L346] JMP      A=5 B=128 C=3 D=32771 target=8
00005 [L347] GGET     A=4 B=0 C=1 D=1 'g_Color'
00006 [L347] TGETS    A=3 B=4 C=2 D=1026 'green'
00007 [L347] JMP      A=4 B=128 C=2 D=32770 target=10
00008 [L349] GGET     A=4 B=0 C=1 D=1 'g_Color'
00009 [L349] TGETS    A=3 B=4 C=3 D=1027 'white'
00010 [L351] GGET     A=4 B=0 C=4 D=4 'd_ms'
00011 [L351] TGETS    A=4 B=4 C=5 D=1029 'd_u'
00012 [L351] TGETS    A=4 B=4 C=6 D=1030 'createByStyle'
00013 [L351] TDUP     A=5 B=0 C=7 D=7 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 23}}
00014 [L351] TGETS    A=6 B=1 C=8 D=264 'desc'
00015 [L351] IST      A=0 B=0 C=6 D=6 
00016 [L351] JMP      A=7 B=128 C=1 D=32769 target=18
00017 [L351] KSTR     A=6 B=0 C=9 D=9 ''
00018 [L351] TSETS    A=6 B=5 C=10 D=1290 'string'
00019 [L351] TDUP     A=6 B=0 C=11 D=11 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00020 [L351] TSETS    A=6 B=5 C=12 D=1292 'anchor'
00021 [L351] TSETS    A=3 B=5 C=13 D=1293 'color'
00022 [L351] CALL     A=4 B=2 C=2 D=514 
00023 [L352] MOV      A=6 B=0 C=4 D=4 
00024 [L352] TGETS    A=5 B=4 C=14 D=1038 'setPosition'
00025 [L352] TGETS    A=7 B=2 C=15 D=527 'width'
00026 [L352] MULVN    A=7 B=7 C=0 D=1792 
00027 [L352] TGETS    A=8 B=2 C=16 D=528 'height'
00028 [L352] MULVN    A=8 B=8 C=1 D=2049 
00029 [L352] CALL     A=5 B=1 C=4 D=260 
00030 [L353] MOV      A=6 B=0 C=0 D=0 
00031 [L353] TGETS    A=5 B=0 C=17 D=17 'addChild'
00032 [L353] MOV      A=7 B=0 C=4 D=4 
00033 [L353] CALL     A=5 B=1 C=3 D=259 
00034 [L354] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto17 offset=0x2580 source_lines=356-364 params=0
UPVALUES []
00001 [L357] GGET     A=0 B=0 C=0 D=0 'g_progressSchedule'
00002 [L357] ISEQP    A=0 B=0 C=0 D=0 
00003 [L357] JMP      A=0 B=128 C=4 D=32772 target=8
00004 [L357] GGET     A=0 B=0 C=0 D=0 'g_progressSchedule'
00005 [L357] ISEQN    A=0 B=0 C=0 D=0 0
00006 [L357] JMP      A=0 B=128 C=1 D=32769 target=8
00007 [L358] RET0     A=0 B=0 C=1 D=1 
00008 [L360] GGET     A=0 B=0 C=1 D=1 'd_ms'
00009 [L360] TGETS    A=0 B=0 C=2 D=2 'd_music_mgr'
00010 [L360] TGETS    A=0 B=0 C=3 D=3 'playClickEffect'
00011 [L360] CALL     A=0 B=1 C=1 D=257 
00012 [L361] GGET     A=0 B=0 C=1 D=1 'd_ms'
00013 [L361] TGETS    A=0 B=0 C=4 D=4 'd_u'
00014 [L361] TGETS    A=0 B=0 C=5 D=5 'remove'
00015 [L361] GGET     A=1 B=0 C=6 D=6 'g_self'
00016 [L361] TGETS    A=1 B=1 C=7 D=263 'main_layer'
00017 [L361] CALL     A=0 B=1 C=2 D=258 
00018 [L362] GGET     A=0 B=0 C=6 D=6 'g_self'
00019 [L362] KPRI     A=1 B=0 C=0 D=0 
00020 [L362] TSETS    A=1 B=0 C=7 D=7 'main_layer'
00021 [L363] GGET     A=0 B=0 C=1 D=1 'd_ms'
00022 [L363] TGETS    A=0 B=0 C=8 D=8 'd_activityUI'
00023 [L363] TGETS    A=0 B=0 C=9 D=9 'returnBack'
00024 [L363] CALL     A=0 B=1 C=1 D=257 
00025 [L364] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto18 offset=0x2674 source_lines=366-371 params=0
UPVALUES []
00001 [L367] GGET     A=0 B=0 C=0 D=0 'g_progressSchedule'
00002 [L367] ISEQP    A=0 B=0 C=0 D=0 
00003 [L367] JMP      A=0 B=128 C=4 D=32772 target=8
00004 [L367] GGET     A=0 B=0 C=0 D=0 'g_progressSchedule'
00005 [L367] ISEQN    A=0 B=0 C=0 D=0 0
00006 [L367] JMP      A=0 B=128 C=1 D=32769 target=8
00007 [L368] RET0     A=0 B=0 C=1 D=1 
00008 [L370] GGET     A=0 B=0 C=1 D=1 'd_ms'
00009 [L370] TGETS    A=0 B=0 C=2 D=2 'd_rechargeUI'
00010 [L370] TGETS    A=0 B=0 C=3 D=3 'show'
00011 [L370] CALL     A=0 B=1 C=1 D=257 
00012 [L371] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto19 offset=0x26e9 source_lines=374-389 params=0
UPVALUES []
00001 [L375] GGET     A=0 B=0 C=0 D=0 'g_self'
00002 [L375] TGETS    A=0 B=0 C=1 D=1 'main_layer'
00003 [L375] ISF      A=0 B=0 C=0 D=0 
00004 [L375] JMP      A=0 B=128 C=9 D=32777 target=14
00005 [L375] GGET     A=0 B=0 C=0 D=0 'g_self'
00006 [L375] TGETS    A=0 B=0 C=2 D=2 'data'
00007 [L375] ISF      A=0 B=0 C=0 D=0 
00008 [L375] JMP      A=0 B=128 C=5 D=32773 target=14
00009 [L375] GGET     A=0 B=0 C=0 D=0 'g_self'
00010 [L375] TGETS    A=0 B=0 C=2 D=2 'data'
00011 [L375] TGETS    A=0 B=0 C=3 D=3 'prize_status'
00012 [L375] IST      A=0 B=0 C=0 D=0 
00013 [L375] JMP      A=0 B=128 C=1 D=32769 target=15
00014 [L376] RET0     A=0 B=0 C=1 D=1 
00015 [L378] GGET     A=0 B=0 C=0 D=0 'g_self'
00016 [L378] TGETS    A=0 B=0 C=4 D=4 'reward_info'
00017 [L378] ISF      A=0 B=0 C=0 D=0 
00018 [L378] JMP      A=1 B=128 C=8 D=32776 target=27
00019 [L379] GGET     A=0 B=0 C=0 D=0 'g_self'
00020 [L379] TGETS    A=0 B=0 C=1 D=1 'main_layer'
00021 [L379] MOV      A=1 B=0 C=0 D=0 
00022 [L379] TGETS    A=0 B=0 C=5 D=5 'removeChild'
00023 [L379] GGET     A=2 B=0 C=0 D=0 'g_self'
00024 [L379] TGETS    A=2 B=2 C=4 D=516 'reward_info'
00025 [L379] KPRI     A=3 B=0 C=2 D=2 
00026 [L379] CALL     A=0 B=1 C=4 D=260 
00027 [L382] GGET     A=0 B=0 C=0 D=0 'g_self'
00028 [L382] TGETS    A=0 B=0 C=6 D=6 'reward_gold'
00029 [L382] ISF      A=0 B=0 C=0 D=0 
00030 [L382] JMP      A=1 B=128 C=8 D=32776 target=39
00031 [L383] GGET     A=0 B=0 C=0 D=0 'g_self'
00032 [L383] TGETS    A=0 B=0 C=1 D=1 'main_layer'
00033 [L383] MOV      A=1 B=0 C=0 D=0 
00034 [L383] TGETS    A=0 B=0 C=5 D=5 'removeChild'
00035 [L383] GGET     A=2 B=0 C=0 D=0 'g_self'
00036 [L383] TGETS    A=2 B=2 C=6 D=518 'reward_gold'
00037 [L383] KPRI     A=3 B=0 C=2 D=2 
00038 [L383] CALL     A=0 B=1 C=4 D=260 
00039 [L386] GGET     A=0 B=0 C=0 D=0 'g_self'
00040 [L386] TGETS    A=0 B=0 C=7 D=7 'reward_btn'
00041 [L386] ISF      A=0 B=0 C=0 D=0 
00042 [L386] JMP      A=1 B=128 C=6 D=32774 target=49
00043 [L387] GGET     A=0 B=0 C=0 D=0 'g_self'
00044 [L387] TGETS    A=0 B=0 C=7 D=7 'reward_btn'
00045 [L387] MOV      A=1 B=0 C=0 D=0 
00046 [L387] TGETS    A=0 B=0 C=8 D=8 'setEnabled'
00047 [L387] KPRI     A=2 B=0 C=1 D=1 
00048 [L387] CALL     A=0 B=1 C=3 D=259 
00049 [L389] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto20 offset=0x284a source_lines=433-438 params=1
UPVALUES ['reward_list']
00001 [L434] GGET     A=1 B=0 C=0 D=0 'g_progressSchedule'
00002 [L434] ISEQP    A=1 B=0 C=0 D=0 
00003 [L434] JMP      A=1 B=128 C=4 D=32772 target=8
00004 [L434] GGET     A=1 B=0 C=0 D=0 'g_progressSchedule'
00005 [L434] ISEQN    A=1 B=0 C=0 D=0 0
00006 [L434] JMP      A=1 B=128 C=1 D=32769 target=8
00007 [L435] RET0     A=0 B=0 C=1 D=1 
00008 [L437] GGET     A=1 B=0 C=1 D=1 'd_ms'
00009 [L437] TGETS    A=1 B=1 C=2 D=258 'd_data'
00010 [L437] TGETS    A=1 B=1 C=3 D=259 'showItemIntro'
00011 [L437] GGET     A=2 B=0 C=4 D=4 'g_self'
00012 [L437] TGETS    A=2 B=2 C=5 D=517 'main_layer'
00013 [L437] UGET     A=3 B=0 C=0 D=0 reward_list
00014 [L437] TGETV    A=3 B=3 C=0 D=768 
00015 [L437] CALL     A=1 B=1 C=3 D=259 
00016 [L438] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto21 offset=0x28fc source_lines=469-491 params=0
UPVALUES ['table']
00001 [L470] GGET     A=0 B=0 C=0 D=0 'g_self'
00002 [L470] TGETS    A=0 B=0 C=1 D=1 'data'
00003 [L470] TGETS    A=0 B=0 C=2 D=2 'total_time'
00004 [L470] IST      A=0 B=0 C=0 D=0 
00005 [L470] JMP      A=1 B=128 C=1 D=32769 target=7
00006 [L470] KSHORT   A=0 B=0 C=0 D=0 0
00007 [L471] GGET     A=1 B=0 C=0 D=0 'g_self'
00008 [L471] TGETS    A=1 B=1 C=1 D=257 'data'
00009 [L471] TGETS    A=1 B=1 C=3 D=259 'result_index'
00010 [L471] IST      A=0 B=0 C=1 D=1 
00011 [L471] JMP      A=2 B=128 C=1 D=32769 target=13
00012 [L471] KSHORT   A=1 B=0 C=1 D=1 1
00013 [L472] KSHORT   A=2 B=0 C=0 D=0 0
00014 [L472] ISGT     A=0 B=0 C=2 D=2 
00015 [L472] JMP      A=2 B=128 C=10 D=32778 target=26
00016 [L473] GGET     A=2 B=0 C=4 D=4 'd_ms'
00017 [L473] TGETS    A=2 B=2 C=5 D=517 'd_info'
00018 [L473] TGETS    A=2 B=2 C=6 D=518 'show'
00019 [L473] GGET     A=3 B=0 C=4 D=4 'd_ms'
00020 [L473] TGETS    A=3 B=3 C=7 D=775 'd_hz'
00021 [L473] TGETS    A=3 B=3 C=8 D=776 'gethz'
00022 [L473] KSTR     A=4 B=0 C=9 D=9 'turntable_tips_1'
00023 [L473] CALL     A=3 B=0 C=2 D=2 
00024 [L473] CALLM    A=2 B=1 C=0 D=256 
00025 [L474] RET0     A=0 B=0 C=1 D=1 
00026 [L477] GGET     A=2 B=0 C=10 D=10 'g_progressSchedule'
00027 [L477] ISEQP    A=2 B=0 C=0 D=0 
00028 [L477] JMP      A=2 B=128 C=29 D=32797 target=58
00029 [L477] GGET     A=2 B=0 C=10 D=10 'g_progressSchedule'
00030 [L477] ISEQN    A=2 B=0 C=0 D=0 0
00031 [L477] JMP      A=2 B=128 C=26 D=32794 target=58
00032 [L478] GGET     A=2 B=0 C=11 D=11 'close_schedulescriptfunc'
00033 [L478] CALL     A=2 B=1 C=1 D=257 
00034 [L479] KSHORT   A=2 B=0 C=1 D=1 1
00035 [L479] KSHORT   A=3 B=0 C=8 D=8 8
00036 [L479] KSHORT   A=4 B=0 C=1 D=1 1
00037 [L479] FORI     A=2 B=128 C=8 D=32776 target=46
00038 [L480] GGET     A=6 B=0 C=0 D=0 'g_self'
00039 [L480] TGETS    A=6 B=6 C=12 D=1548 'tt_reward_splash'
00040 [L480] TGETV    A=6 B=6 C=5 D=1541 
00041 [L480] MOV      A=7 B=0 C=6 D=6 
00042 [L480] TGETS    A=6 B=6 C=13 D=1549 'setVisible'
00043 [L480] KPRI     A=8 B=0 C=1 D=1 
00044 [L480] CALL     A=6 B=1 C=3 D=259 
00045 [L479] FORL     A=2 B=127 C=248 D=32760 target=38
00046 [L482] GGET     A=2 B=0 C=0 D=0 'g_self'
00047 [L482] TSETS    A=1 B=2 C=14 D=526 'index'
00048 [L483] GGET     A=2 B=0 C=0 D=0 'g_self'
00049 [L483] TGETS    A=2 B=2 C=12 D=524 'tt_reward_splash'
00050 [L483] TGETV    A=2 B=2 C=1 D=513 
00051 [L483] MOV      A=3 B=0 C=2 D=2 
00052 [L483] TGETS    A=2 B=2 C=13 D=525 'setVisible'
00053 [L483] KPRI     A=4 B=0 C=2 D=2 
00054 [L483] CALL     A=2 B=1 C=3 D=259 
00055 [L484] GGET     A=2 B=0 C=15 D=15 'showreward'
00056 [L484] CALL     A=2 B=1 C=1 D=257 
00057 [L485] RET0     A=0 B=0 C=1 D=1 
00058 [L487] TNEW     A=2 B=0 C=0 D=0 
00059 [L487] GSET     A=2 B=0 C=16 D=16 'tmp_req'
00060 [L488] GGET     A=2 B=0 C=16 D=16 'tmp_req'
00061 [L488] KSHORT   A=3 B=0 C=1 D=1 1
00062 [L488] TSETS    A=3 B=2 C=17 D=529 'id'
00063 [L489] GGET     A=2 B=0 C=16 D=16 'tmp_req'
00064 [L489] UGET     A=3 B=0 C=0 D=0 table
00065 [L489] TGETS    A=3 B=3 C=18 D=786 'tostring'
00066 [L489] TNEW     A=4 B=0 C=0 D=0 
00067 [L489] CALL     A=3 B=2 C=2 D=514 
00068 [L489] TSETS    A=3 B=2 C=1 D=513 'data'
00069 [L490] GGET     A=2 B=0 C=4 D=4 'd_ms'
00070 [L490] TGETS    A=2 B=2 C=19 D=531 'd_u'
00071 [L490] TGETS    A=2 B=2 C=20 D=532 'main_server_send_msg'
00072 [L490] GGET     A=3 B=0 C=4 D=4 'd_ms'
00073 [L490] TGETS    A=3 B=3 C=21 D=789 'd_msg_def'
00074 [L490] TGETS    A=3 B=3 C=22 D=790 'gscl_msg_id'
00075 [L490] TGETS    A=3 B=3 C=23 D=791 'msg_rulai_activity'
00076 [L490] GGET     A=4 B=0 C=16 D=16 'tmp_req'
00077 [L490] CALL     A=2 B=1 C=3 D=259 
00078 [L491] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto22 offset=0x2bc1 source_lines=505-509 params=1
UPVALUES []
00001 [L506] TGETS    A=1 B=0 C=0 D=0 'name'
00002 [L506] ISNES    A=1 B=0 C=1 D=1 'exit'
00003 [L506] JMP      A=1 B=128 C=2 D=32770 target=6
00004 [L507] GGET     A=1 B=0 C=2 D=2 'close_schedulescriptfunc'
00005 [L507] CALL     A=1 B=1 C=1 D=257 
00006 [L509] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto23 offset=0x2c1c source_lines=391-512 params=0
UPVALUES ['table', 'tostring', 'CCSprite', 'string']
00001 [L392] GGET     A=0 B=0 C=0 D=0 'g_self'
00002 [L392] TGETS    A=0 B=0 C=1 D=1 'main_layer'
00003 [L392] IST      A=0 B=0 C=0 D=0 
00004 [L392] JMP      A=0 B=128 C=1 D=32769 target=6
00005 [L393] UCLO     A=0 B=129 C=62 D=33086 target=324
00006 [L395] GGET     A=0 B=0 C=2 D=2 'd_ms'
00007 [L395] TGETS    A=0 B=0 C=3 D=3 'd_u'
00008 [L395] TGETS    A=0 B=0 C=4 D=4 'createSwallowTouchLayer'
00009 [L395] GGET     A=1 B=0 C=0 D=0 'g_self'
00010 [L395] TGETS    A=1 B=1 C=1 D=257 'main_layer'
00011 [L395] CALL     A=0 B=2 C=2 D=514 
00012 [L396] GGET     A=1 B=0 C=2 D=2 'd_ms'
00013 [L396] TGETS    A=1 B=1 C=3 D=259 'd_u'
00014 [L396] TGETS    A=1 B=1 C=5 D=261 'setStyle'
00015 [L396] MOV      A=2 B=0 C=0 D=0 
00016 [L396] TDUP     A=3 B=0 C=7 D=7 {'kind': 'table', 'value': {'y': 0.5}}
00017 [L396] GGET     A=4 B=0 C=0 D=0 'g_self'
00018 [L396] TGETS    A=4 B=4 C=6 D=1030 'width'
00019 [L396] MULNV    A=4 B=4 C=0 D=1024 
00020 [L396] SUBNV    A=4 B=4 C=1 D=1025 
00021 [L396] TSETS    A=4 B=3 C=8 D=776 'x'
00022 [L396] CALL     A=1 B=1 C=3 D=259 
00023 [L397] GGET     A=1 B=0 C=2 D=2 'd_ms'
00024 [L397] TGETS    A=1 B=1 C=3 D=259 'd_u'
00025 [L397] TGETS    A=1 B=1 C=9 D=265 'createByStyles'
00026 [L397] TDUP     A=2 B=0 C=10 D=10 {'kind': 'table', 'value': {'pic': 'v2/newTurnTableUI/turntable_bkg.png'}}
00027 [L397] CALL     A=1 B=2 C=2 D=514 
00028 [L398] MOV      A=3 B=0 C=0 D=0 
00029 [L398] TGETS    A=2 B=0 C=11 D=11 'addChild'
00030 [L398] MOV      A=4 B=0 C=1 D=1 
00031 [L398] KSHORT   A=5 B=255 C=255 D=65535 -1
00032 [L398] CALL     A=2 B=1 C=4 D=260 
00033 [L399] GGET     A=2 B=0 C=2 D=2 'd_ms'
00034 [L399] TGETS    A=2 B=2 C=3 D=515 'd_u'
00035 [L399] TGETS    A=2 B=2 C=12 D=524 'getRealScale'
00036 [L399] MOV      A=3 B=0 C=1 D=1 
00037 [L399] CALL     A=2 B=3 C=2 D=770 
00038 [L400] GGET     A=4 B=0 C=0 D=0 'g_self'
00039 [L400] GGET     A=5 B=0 C=0 D=0 'g_self'
00040 [L400] MOV      A=6 B=0 C=2 D=2 
00041 [L400] TSETS    A=3 B=5 C=14 D=1294 'tth'
00042 [L400] TSETS    A=6 B=4 C=13 D=1037 'ttw'
00043 [L402] GGET     A=4 B=0 C=0 D=0 'g_self'
00044 [L402] TGETS    A=4 B=4 C=15 D=1039 'data'
00045 [L402] TGETS    A=4 B=4 C=16 D=1040 'total_time'
00046 [L402] IST      A=0 B=0 C=4 D=4 
00047 [L402] JMP      A=5 B=128 C=1 D=32769 target=49
00048 [L402] KSHORT   A=4 B=0 C=0 D=0 0
00049 [L403] GGET     A=5 B=0 C=0 D=0 'g_self'
00050 [L403] TGETS    A=5 B=5 C=15 D=1295 'data'
00051 [L403] TGETS    A=5 B=5 C=17 D=1297 'reward_list'
00052 [L403] IST      A=0 B=0 C=5 D=5 
00053 [L403] JMP      A=6 B=128 C=1 D=32769 target=55
00054 [L403] TNEW     A=5 B=0 C=0 D=0 
00055 [L406] TNEW     A=6 B=0 C=9 D=9 
00056 [L406] TDUP     A=7 B=0 C=18 D=18 {'kind': 'table', 'value': {}}
00057 [L407] MULNV    A=8 B=2 C=2 D=514 
00058 [L407] TSETS    A=8 B=7 C=8 D=1800 'x'
00059 [L407] MULNV    A=8 B=3 C=3 D=771 
00060 [L407] TSETS    A=8 B=7 C=19 D=1811 'y'
00061 [L407] TSETB    A=7 B=6 C=1 D=1537 
00062 [L407] TDUP     A=7 B=0 C=20 D=20 {'kind': 'table', 'value': {}}
00063 [L408] MULNV    A=8 B=2 C=4 D=516 
00064 [L408] TSETS    A=8 B=7 C=8 D=1800 'x'
00065 [L408] MULNV    A=8 B=3 C=5 D=773 
00066 [L408] TSETS    A=8 B=7 C=19 D=1811 'y'
00067 [L408] TSETB    A=7 B=6 C=2 D=1538 
00068 [L408] TDUP     A=7 B=0 C=21 D=21 {'kind': 'table', 'value': {}}
00069 [L409] MULNV    A=8 B=2 C=6 D=518 
00070 [L409] TSETS    A=8 B=7 C=8 D=1800 'x'
00071 [L409] MULNV    A=8 B=3 C=7 D=775 
00072 [L409] TSETS    A=8 B=7 C=19 D=1811 'y'
00073 [L409] TSETB    A=7 B=6 C=3 D=1539 
00074 [L409] TDUP     A=7 B=0 C=22 D=22 {'kind': 'table', 'value': {}}
00075 [L410] MULNV    A=8 B=2 C=8 D=520 
00076 [L410] TSETS    A=8 B=7 C=8 D=1800 'x'
00077 [L410] MULNV    A=8 B=3 C=9 D=777 
00078 [L410] TSETS    A=8 B=7 C=19 D=1811 'y'
00079 [L410] TSETB    A=7 B=6 C=4 D=1540 
00080 [L410] TDUP     A=7 B=0 C=23 D=23 {'kind': 'table', 'value': {}}
00081 [L411] MULNV    A=8 B=2 C=2 D=514 
00082 [L411] TSETS    A=8 B=7 C=8 D=1800 'x'
00083 [L411] MULNV    A=8 B=3 C=10 D=778 
00084 [L411] TSETS    A=8 B=7 C=19 D=1811 'y'
00085 [L411] TSETB    A=7 B=6 C=5 D=1541 
00086 [L411] TDUP     A=7 B=0 C=24 D=24 {'kind': 'table', 'value': {}}
00087 [L412] MULNV    A=8 B=2 C=11 D=523 
00088 [L412] TSETS    A=8 B=7 C=8 D=1800 'x'
00089 [L412] MULNV    A=8 B=3 C=9 D=777 
00090 [L412] TSETS    A=8 B=7 C=19 D=1811 'y'
00091 [L412] TSETB    A=7 B=6 C=6 D=1542 
00092 [L412] TDUP     A=7 B=0 C=25 D=25 {'kind': 'table', 'value': {}}
00093 [L413] MULNV    A=8 B=2 C=12 D=524 
00094 [L413] TSETS    A=8 B=7 C=8 D=1800 'x'
00095 [L413] MULNV    A=8 B=3 C=7 D=775 
00096 [L413] TSETS    A=8 B=7 C=19 D=1811 'y'
00097 [L413] TSETB    A=7 B=6 C=7 D=1543 
00098 [L413] TDUP     A=7 B=0 C=26 D=26 {'kind': 'table', 'value': {}}
00099 [L414] MULNV    A=8 B=2 C=13 D=525 
00100 [L414] TSETS    A=8 B=7 C=8 D=1800 'x'
00101 [L414] MULNV    A=8 B=3 C=5 D=773 
00102 [L414] TSETS    A=8 B=7 C=19 D=1811 'y'
00103 [L414] TSETB    A=7 B=6 C=8 D=1544 
00104 [L416] GGET     A=7 B=0 C=0 D=0 'g_self'
00105 [L416] TSETS    A=6 B=7 C=27 D=1819 'tt_reward_pos'
00106 [L419] TDUP     A=7 B=0 C=28 D=28 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00107 [L424] KSHORT   A=8 B=0 C=1 D=1 1
00108 [L424] KSHORT   A=9 B=0 C=8 D=8 8
00109 [L424] KSHORT   A=10 B=0 C=1 D=1 1
00110 [L424] FORI     A=8 B=128 C=12 D=32780 target=123
00111 [L425] UGET     A=12 B=0 C=0 D=0 table
00112 [L425] TGETS    A=12 B=12 C=29 D=3101 'insert'
00113 [L425] MOV      A=13 B=0 C=7 D=7 
00114 [L425] TDUP     A=14 B=0 C=30 D=30 {'kind': 'table', 'value': {'spic': 'v2/newTurnTableUI/select.png', 'visible': False, 'npic': 'v2/newTurnTableUI/select.png'}}
00115 [L425] TGETV    A=15 B=6 C=11 D=1547 
00116 [L425] TGETS    A=15 B=15 C=8 D=3848 'x'
00117 [L425] TSETS    A=15 B=14 C=8 D=3592 'x'
00118 [L425] TGETV    A=15 B=6 C=11 D=1547 
00119 [L425] TGETS    A=15 B=15 C=19 D=3859 'y'
00120 [L425] TSETS    A=15 B=14 C=19 D=3603 'y'
00121 [L425] CALL     A=12 B=1 C=3 D=259 
00122 [L424] FORL     A=8 B=127 C=244 D=32756 target=111
00123 [L427] TNEW     A=8 B=0 C=0 D=0 
00124 [L428] MOV      A=10 B=0 C=0 D=0 
00125 [L428] TGETS    A=9 B=0 C=11 D=11 'addChild'
00126 [L428] GGET     A=11 B=0 C=2 D=2 'd_ms'
00127 [L428] TGETS    A=11 B=11 C=3 D=2819 'd_u'
00128 [L428] TGETS    A=11 B=11 C=31 D=2847 'createMenu'
00129 [L428] MOV      A=12 B=0 C=7 D=7 
00130 [L428] MOV      A=13 B=0 C=8 D=8 
00131 [L428] CALL     A=11 B=0 C=3 D=3 
00132 [L428] CALLM    A=9 B=1 C=1 D=257 
00133 [L429] GGET     A=9 B=0 C=0 D=0 'g_self'
00134 [L429] TSETS    A=8 B=9 C=32 D=2336 'tt_reward_splash'
00135 [L430] GGET     A=9 B=0 C=0 D=0 'g_self'
00136 [L430] KSHORT   A=10 B=0 C=3 D=3 3
00137 [L430] TSETS    A=10 B=9 C=33 D=2337 'index'
00138 [L431] GGET     A=9 B=0 C=0 D=0 'g_self'
00139 [L431] TGETS    A=9 B=9 C=32 D=2336 'tt_reward_splash'
00140 [L431] GGET     A=10 B=0 C=0 D=0 'g_self'
00141 [L431] TGETS    A=10 B=10 C=33 D=2593 'index'
00142 [L431] TGETV    A=9 B=9 C=10 D=2314 
00143 [L431] MOV      A=10 B=0 C=9 D=9 
00144 [L431] TGETS    A=9 B=9 C=34 D=2338 'setVisible'
00145 [L431] KPRI     A=11 B=0 C=2 D=2 
00146 [L431] CALL     A=9 B=1 C=3 D=259 
00147 [L438] FNEW     A=9 B=0 C=35 D=35 {'kind': 'proto', 'id': 20}
00148 [L440] TDUP     A=10 B=0 C=36 D=36 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00149 [L445] KSHORT   A=11 B=0 C=1 D=1 1
00150 [L445] KSHORT   A=12 B=0 C=8 D=8 8
00151 [L445] KSHORT   A=13 B=0 C=1 D=1 1
00152 [L445] FORI     A=11 B=128 C=38 D=32806 target=191
00153 [L446] KPRI     A=15 B=0 C=0 D=0 
00154 [L447] TGETV    A=16 B=5 C=14 D=1294 
00155 [L447] ISF      A=0 B=0 C=16 D=16 
00156 [L447] JMP      A=17 B=128 C=12 D=32780 target=169
00157 [L448] GGET     A=16 B=0 C=2 D=2 'd_ms'
00158 [L448] TGETS    A=16 B=16 C=37 D=4133 'd_data'
00159 [L448] TGETS    A=16 B=16 C=38 D=4134 'getCertainSmallSprite'
00160 [L448] TGETV    A=17 B=5 C=14 D=1294 
00161 [L448] TGETS    A=17 B=17 C=39 D=4391 'object_type'
00162 [L448] TGETV    A=18 B=5 C=14 D=1294 
00163 [L448] TGETS    A=18 B=18 C=40 D=4648 'attach_type'
00164 [L448] TGETV    A=19 B=5 C=14 D=1294 
00165 [L448] TGETS    A=19 B=19 C=41 D=4905 'attach_level'
00166 [L448] CALL     A=16 B=2 C=4 D=516 
00167 [L448] MOV      A=15 B=0 C=16 D=16 
00168 [L448] JMP      A=16 B=128 C=6 D=32774 target=175
00169 [L450] GGET     A=16 B=0 C=2 D=2 'd_ms'
00170 [L450] TGETS    A=16 B=16 C=37 D=4133 'd_data'
00171 [L450] TGETS    A=16 B=16 C=38 D=4134 'getCertainSmallSprite'
00172 [L450] KSHORT   A=17 B=39 C=15 D=9999 9999
00173 [L450] CALL     A=16 B=2 C=2 D=514 
00174 [L450] MOV      A=15 B=0 C=16 D=16 
00175 [L452] UGET     A=16 B=0 C=0 D=0 table
00176 [L452] TGETS    A=16 B=16 C=29 D=4125 'insert'
00177 [L452] MOV      A=17 B=0 C=10 D=10 
00178 [L452] TDUP     A=18 B=0 C=42 D=42 {'kind': 'table', 'value': {'scale_pic': 0.75}}
00179 [L452] TSETS    A=15 B=18 C=43 D=4651 'nsprite'
00180 [L452] TSETS    A=15 B=18 C=44 D=4652 'ssprite'
00181 [L452] TGETV    A=19 B=6 C=14 D=1550 
00182 [L452] TGETS    A=19 B=19 C=8 D=4872 'x'
00183 [L452] TSETS    A=19 B=18 C=8 D=4616 'x'
00184 [L452] TGETV    A=19 B=6 C=14 D=1550 
00185 [L452] TGETS    A=19 B=19 C=19 D=4883 'y'
00186 [L452] TSETS    A=19 B=18 C=19 D=4627 'y'
00187 [L452] TSETS    A=14 B=18 C=45 D=4653 'tag'
00188 [L452] TSETS    A=9 B=18 C=46 D=4654 'call_back'
00189 [L452] CALL     A=16 B=1 C=3 D=259 
00190 [L445] FORL     A=11 B=127 C=218 D=32730 target=153
00191 [L454] TNEW     A=11 B=0 C=0 D=0 
00192 [L455] MOV      A=13 B=0 C=0 D=0 
00193 [L455] TGETS    A=12 B=0 C=11 D=11 'addChild'
00194 [L455] GGET     A=14 B=0 C=2 D=2 'd_ms'
00195 [L455] TGETS    A=14 B=14 C=3 D=3587 'd_u'
00196 [L455] TGETS    A=14 B=14 C=31 D=3615 'createMenu'
00197 [L455] MOV      A=15 B=0 C=10 D=10 
00198 [L455] MOV      A=16 B=0 C=11 D=11 
00199 [L455] CALL     A=14 B=0 C=3 D=3 
00200 [L455] CALLM    A=12 B=1 C=1 D=257 
00201 [L458] KSHORT   A=12 B=0 C=1 D=1 1
00202 [L458] KSHORT   A=13 B=0 C=8 D=8 8
00203 [L458] KSHORT   A=14 B=0 C=1 D=1 1
00204 [L458] FORI     A=12 B=128 C=39 D=32807 target=244
00205 [L459] TGETV    A=16 B=5 C=15 D=1295 
00206 [L459] ISF      A=0 B=0 C=16 D=16 
00207 [L459] JMP      A=17 B=128 C=4 D=32772 target=212
00208 [L459] TGETV    A=16 B=5 C=15 D=1295 
00209 [L459] TGETS    A=16 B=16 C=47 D=4143 'attach_count'
00210 [L459] IST      A=0 B=0 C=16 D=16 
00211 [L459] JMP      A=17 B=128 C=1 D=32769 target=213
00212 [L459] KSHORT   A=16 B=0 C=0 D=0 0
00213 [L460] KSHORT   A=17 B=0 C=1 D=1 1
00214 [L460] ISGE     A=17 B=0 C=16 D=16 
00215 [L460] JMP      A=17 B=128 C=27 D=32795 target=243
00216 [L461] MOV      A=18 B=0 C=0 D=0 
00217 [L461] TGETS    A=17 B=0 C=11 D=11 'addChild'
00218 [L461] GGET     A=19 B=0 C=2 D=2 'd_ms'
00219 [L461] TGETS    A=19 B=19 C=3 D=4867 'd_u'
00220 [L461] TGETS    A=19 B=19 C=9 D=4873 'createByStyles'
00221 [L461] TDUP     A=20 B=0 C=48 D=48 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 18}}
00222 [L461] UGET     A=21 B=0 C=1 D=1 tostring
00223 [L461] MOV      A=22 B=0 C=16 D=16 
00224 [L461] CALL     A=21 B=2 C=2 D=514 
00225 [L461] TSETS    A=21 B=20 C=49 D=5169 'string'
00226 [L461] TGETV    A=21 B=6 C=15 D=1551 
00227 [L461] TGETS    A=21 B=21 C=8 D=5384 'x'
00228 [L461] MULNV    A=22 B=2 C=14 D=526 
00229 [L461] ADDVV    A=21 B=21 C=22 D=5398 
00230 [L461] TSETS    A=21 B=20 C=8 D=5128 'x'
00231 [L461] TGETV    A=21 B=6 C=15 D=1551 
00232 [L461] TGETS    A=21 B=21 C=19 D=5395 'y'
00233 [L461] MULNV    A=22 B=3 C=14 D=782 
00234 [L461] SUBVV    A=21 B=21 C=22 D=5398 
00235 [L461] TSETS    A=21 B=20 C=19 D=5139 'y'
00236 [L462] TDUP     A=21 B=0 C=50 D=50 {'kind': 'table', 'value': {1: 1, 2: 0}}
00237 [L462] TSETS    A=21 B=20 C=51 D=5171 'anchor'
00238 [L462] GGET     A=21 B=0 C=52 D=52 'g_Color'
00239 [L462] TGETS    A=21 B=21 C=53 D=5429 'green'
00240 [L462] TSETS    A=21 B=20 C=54 D=5174 'color'
00241 [L461] CALL     A=19 B=0 C=2 D=2 
00242 [L461] CALLM    A=17 B=1 C=1 D=257 
00243 [L458] FORL     A=12 B=127 C=217 D=32729 target=205
00244 [L465] UGET     A=12 B=0 C=2 D=2 CCSprite
00245 [L465] MOV      A=13 B=0 C=12 D=12 
00246 [L465] TGETS    A=12 B=12 C=55 D=3127 'create'
00247 [L465] KSTR     A=14 B=0 C=56 D=56 'v2/loginGameUI/bagua.png'
00248 [L465] CALL     A=12 B=2 C=3 D=515 
00249 [L465] GSET     A=12 B=0 C=57 D=57 'g_bagua'
00250 [L466] GGET     A=12 B=0 C=2 D=2 'd_ms'
00251 [L466] TGETS    A=12 B=12 C=3 D=3075 'd_u'
00252 [L466] TGETS    A=12 B=12 C=58 D=3130 'setStyles'
00253 [L466] GGET     A=13 B=0 C=57 D=57 'g_bagua'
00254 [L466] TDUP     A=14 B=0 C=59 D=59 {'kind': 'table', 'value': {}}
00255 [L466] MULNV    A=15 B=2 C=2 D=514 
00256 [L466] TSETS    A=15 B=14 C=8 D=3592 'x'
00257 [L466] MULNV    A=15 B=3 C=7 D=775 
00258 [L466] TSETS    A=15 B=14 C=19 D=3603 'y'
00259 [L466] CALL     A=12 B=1 C=3 D=259 
00260 [L467] GGET     A=12 B=0 C=57 D=57 'g_bagua'
00261 [L467] MOV      A=13 B=0 C=12 D=12 
00262 [L467] TGETS    A=12 B=12 C=34 D=3106 'setVisible'
00263 [L467] KPRI     A=14 B=0 C=1 D=1 
00264 [L467] CALL     A=12 B=1 C=3 D=259 
00265 [L468] MOV      A=13 B=0 C=0 D=0 
00266 [L468] TGETS    A=12 B=0 C=11 D=11 'addChild'
00267 [L468] GGET     A=14 B=0 C=57 D=57 'g_bagua'
00268 [L468] CALL     A=12 B=1 C=3 D=259 
00269 [L491] FNEW     A=12 B=0 C=60 D=60 {'kind': 'proto', 'id': 21}
00270 [L493] TDUP     A=13 B=0 C=61 D=61 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00271 [L496] TDUP     A=14 B=0 C=62 D=62 {'kind': 'table', 'value': {'npic': 'v2/newTurnTableUI/luckdraw1.png', 'spic': 'v2/newTurnTableUI/luckdraw2.png'}}
00272 [L497] MULNV    A=15 B=2 C=2 D=514 
00273 [L497] TSETS    A=15 B=14 C=8 D=3592 'x'
00274 [L497] MULNV    A=15 B=3 C=7 D=775 
00275 [L497] TSETS    A=15 B=14 C=19 D=3603 'y'
00276 [L497] TSETS    A=12 B=14 C=46 D=3630 'call_back'
00277 [L497] TSETB    A=14 B=13 C=1 D=3329 
00278 [L499] MOV      A=15 B=0 C=0 D=0 
00279 [L499] TGETS    A=14 B=0 C=11 D=11 'addChild'
00280 [L499] GGET     A=16 B=0 C=2 D=2 'd_ms'
00281 [L499] TGETS    A=16 B=16 C=3 D=4099 'd_u'
00282 [L499] TGETS    A=16 B=16 C=31 D=4127 'createMenu'
00283 [L499] MOV      A=17 B=0 C=13 D=13 
00284 [L499] CALL     A=16 B=0 C=2 D=2 
00285 [L499] CALLM    A=14 B=1 C=1 D=257 
00286 [L501] GGET     A=14 B=0 C=0 D=0 'g_self'
00287 [L501] GGET     A=15 B=0 C=2 D=2 'd_ms'
00288 [L501] TGETS    A=15 B=15 C=3 D=3843 'd_u'
00289 [L501] TGETS    A=15 B=15 C=9 D=3849 'createByStyles'
00290 [L501] TDUP     A=16 B=0 C=64 D=64 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 18}}
00291 [L501] UGET     A=17 B=0 C=3 D=3 string
00292 [L501] TGETS    A=17 B=17 C=65 D=4417 'format'
00293 [L501] GGET     A=18 B=0 C=2 D=2 'd_ms'
00294 [L501] TGETS    A=18 B=18 C=66 D=4674 'd_hz'
00295 [L501] TGETS    A=18 B=18 C=67 D=4675 'gethz'
00296 [L501] KSTR     A=19 B=0 C=68 D=68 'turntable_tt_1'
00297 [L501] CALL     A=18 B=2 C=2 D=514 
00298 [L501] MOV      A=19 B=0 C=4 D=4 
00299 [L501] CALL     A=17 B=2 C=3 D=515 
00300 [L501] TSETS    A=17 B=16 C=49 D=4145 'string'
00301 [L501] MULNV    A=17 B=2 C=2 D=514 
00302 [L501] TSETS    A=17 B=16 C=8 D=4104 'x'
00303 [L501] MULNV    A=17 B=3 C=15 D=783 
00304 [L501] TSETS    A=17 B=16 C=19 D=4115 'y'
00305 [L501] TDUP     A=17 B=0 C=69 D=69 {'kind': 'table', 'value': {1: 0.5, 2: 1}}
00306 [L501] TSETS    A=17 B=16 C=51 D=4147 'anchor'
00307 [L501] GGET     A=17 B=0 C=52 D=52 'g_Color'
00308 [L501] TGETS    A=17 B=17 C=70 D=4422 'white'
00309 [L501] TSETS    A=17 B=16 C=54 D=4150 'color'
00310 [L501] CALL     A=15 B=2 C=2 D=514 
00311 [L501] TSETS    A=15 B=14 C=63 D=3647 'tt_totaltime_label'
00312 [L502] MOV      A=15 B=0 C=0 D=0 
00313 [L502] TGETS    A=14 B=0 C=11 D=11 'addChild'
00314 [L502] GGET     A=16 B=0 C=0 D=0 'g_self'
00315 [L502] TGETS    A=16 B=16 C=63 D=4159 'tt_totaltime_label'
00316 [L502] CALL     A=14 B=1 C=3 D=259 
00317 [L509] FNEW     A=14 B=0 C=71 D=71 {'kind': 'proto', 'id': 22}
00318 [L511] MOV      A=16 B=0 C=0 D=0 
00319 [L511] TGETS    A=15 B=0 C=72 D=72 'registerScriptHandler'
00320 [L511] MOV      A=17 B=0 C=14 D=14 
00321 [L511] CALL     A=15 B=1 C=3 D=259 
00322 [L512] UCLO     A=0 B=128 C=0 D=32768 target=323
00323 [L512] RET0     A=0 B=0 C=1 D=1 
00324 [L512] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto24 offset=0x37b4 source_lines=514-517 params=0
UPVALUES ['string']
00001 [L515] GGET     A=0 B=0 C=0 D=0 'g_self'
00002 [L515] TGETS    A=0 B=0 C=1 D=1 'data'
00003 [L515] TGETS    A=0 B=0 C=2 D=2 'total_time'
00004 [L515] IST      A=0 B=0 C=0 D=0 
00005 [L515] JMP      A=1 B=128 C=1 D=32769 target=7
00006 [L515] KSHORT   A=0 B=0 C=0 D=0 0
00007 [L516] GGET     A=1 B=0 C=0 D=0 'g_self'
00008 [L516] TGETS    A=1 B=1 C=3 D=259 'tt_totaltime_label'
00009 [L516] MOV      A=2 B=0 C=1 D=1 
00010 [L516] TGETS    A=1 B=1 C=4 D=260 'setString'
00011 [L516] UGET     A=3 B=0 C=0 D=0 string
00012 [L516] TGETS    A=3 B=3 C=5 D=773 'format'
00013 [L516] GGET     A=4 B=0 C=6 D=6 'd_ms'
00014 [L516] TGETS    A=4 B=4 C=7 D=1031 'd_hz'
00015 [L516] TGETS    A=4 B=4 C=8 D=1032 'gethz'
00016 [L516] KSTR     A=5 B=0 C=9 D=9 'turntable_tt_1'
00017 [L516] CALL     A=4 B=2 C=2 D=514 
00018 [L516] MOV      A=5 B=0 C=0 D=0 
00019 [L516] CALL     A=3 B=0 C=3 D=3 
00020 [L516] CALLM    A=1 B=1 C=1 D=257 
00021 [L517] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto25 offset=0x389a source_lines=527-530 params=0
UPVALUES []
00001 [L528] GGET     A=0 B=0 C=0 D=0 'close_schedulescriptfunc'
00002 [L528] CALL     A=0 B=1 C=1 D=257 
00003 [L529] GGET     A=0 B=0 C=1 D=1 'showreward'
00004 [L529] CALL     A=0 B=1 C=1 D=257 
00005 [L530] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto26 offset=0x38e5 source_lines=536-551 params=0
UPVALUES ['start_anger', 'math']
00001 [L537] GGET     A=0 B=0 C=0 D=0 'g_self'
00002 [L537] TGETS    A=0 B=0 C=1 D=1 'main_layer'
00003 [L537] IST      A=0 B=0 C=0 D=0 
00004 [L537] JMP      A=0 B=128 C=3 D=32771 target=8
00005 [L538] GGET     A=0 B=0 C=2 D=2 'close_schedulescriptfunc'
00006 [L538] CALL     A=0 B=1 C=1 D=257 
00007 [L539] RET0     A=0 B=0 C=1 D=1 
00008 [L541] GGET     A=0 B=0 C=3 D=3 'g_bagua'
00009 [L541] MOV      A=1 B=0 C=0 D=0 
00010 [L541] TGETS    A=0 B=0 C=4 D=4 'getRotation'
00011 [L541] CALL     A=0 B=2 C=2 D=514 
00012 [L541] UGET     A=1 B=0 C=0 D=0 start_anger
00013 [L541] ADDVV    A=0 B=0 C=1 D=1 
00014 [L541] SUBVN    A=0 B=0 C=0 D=0 
00015 [L542] UGET     A=1 B=0 C=1 D=1 math
00016 [L542] TGETS    A=1 B=1 C=5 D=261 'floor'
00017 [L542] DIVVN    A=2 B=0 C=1 D=1 
00018 [L542] CALL     A=1 B=2 C=2 D=514 
00019 [L543] KSHORT   A=2 B=0 C=8 D=8 8
00020 [L543] ISGT     A=2 B=0 C=1 D=1 
00021 [L543] JMP      A=2 B=128 C=1 D=32769 target=23
00022 [L544] MODVN    A=1 B=1 C=2 D=258 
00023 [L546] GGET     A=2 B=0 C=0 D=0 'g_self'
00024 [L546] TGETS    A=2 B=2 C=6 D=518 'index'
00025 [L546] ADDNV    A=3 B=1 C=3 D=259 
00026 [L546] ISEQV    A=2 B=0 C=3 D=3 
00027 [L546] JMP      A=2 B=128 C=21 D=32789 target=49
00028 [L547] GGET     A=2 B=0 C=0 D=0 'g_self'
00029 [L547] TGETS    A=2 B=2 C=7 D=519 'tt_reward_splash'
00030 [L547] GGET     A=3 B=0 C=0 D=0 'g_self'
00031 [L547] TGETS    A=3 B=3 C=6 D=774 'index'
00032 [L547] TGETV    A=2 B=2 C=3 D=515 
00033 [L547] MOV      A=3 B=0 C=2 D=2 
00034 [L547] TGETS    A=2 B=2 C=8 D=520 'setVisible'
00035 [L547] KPRI     A=4 B=0 C=1 D=1 
00036 [L547] CALL     A=2 B=1 C=3 D=259 
00037 [L548] GGET     A=2 B=0 C=0 D=0 'g_self'
00038 [L548] ADDNV    A=3 B=1 C=3 D=259 
00039 [L548] TSETS    A=3 B=2 C=6 D=518 'index'
00040 [L549] GGET     A=2 B=0 C=0 D=0 'g_self'
00041 [L549] TGETS    A=2 B=2 C=7 D=519 'tt_reward_splash'
00042 [L549] GGET     A=3 B=0 C=0 D=0 'g_self'
00043 [L549] TGETS    A=3 B=3 C=6 D=774 'index'
00044 [L549] TGETV    A=2 B=2 C=3 D=515 
00045 [L549] MOV      A=3 B=0 C=2 D=2 
00046 [L549] TGETS    A=2 B=2 C=8 D=520 'setVisible'
00047 [L549] KPRI     A=4 B=0 C=2 D=2 
00048 [L549] CALL     A=2 B=1 C=3 D=259 
00049 [L551] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto27 offset=0x3a78 source_lines=519-553 params=0
UPVALUES ['math', 'CCRotateBy', 'CCEaseOut', 'CCCallFunc', 'CCSequence', 'CCDirector']
00001 [L520] GGET     A=0 B=0 C=0 D=0 'g_bagua'
00002 [L520] MOV      A=1 B=0 C=0 D=0 
00003 [L520] TGETS    A=0 B=0 C=1 D=1 'setRotation'
00004 [L520] KSHORT   A=2 B=0 C=0 D=0 0
00005 [L520] CALL     A=0 B=1 C=3 D=259 
00006 [L522] GGET     A=0 B=0 C=2 D=2 'g_self'
00007 [L522] TGETS    A=0 B=0 C=3 D=3 'data'
00008 [L522] TGETS    A=0 B=0 C=4 D=4 'result_index'
00009 [L522] IST      A=0 B=0 C=0 D=0 
00010 [L522] JMP      A=1 B=128 C=1 D=32769 target=12
00011 [L522] KSHORT   A=0 B=0 C=1 D=1 1
00012 [L523] GGET     A=1 B=0 C=2 D=2 'g_self'
00013 [L523] TGETS    A=1 B=1 C=5 D=261 'index'
00014 [L523] MULVN    A=1 B=1 C=0 D=256 
00015 [L524] UGET     A=2 B=0 C=0 D=0 math
00016 [L524] TGETS    A=2 B=2 C=6 D=518 'random'
00017 [L524] KSHORT   A=3 B=0 C=3 D=3 3
00018 [L524] KSHORT   A=4 B=0 C=6 D=6 6
00019 [L524] CALL     A=2 B=2 C=3 D=515 
00020 [L524] MULVN    A=2 B=2 C=1 D=513 
00021 [L524] MULVN    A=3 B=0 C=0 D=0 
00022 [L524] ADDVV    A=2 B=2 C=3 D=515 
00023 [L524] SUBVV    A=2 B=2 C=1 D=513 
00024 [L525] UGET     A=3 B=0 C=1 D=1 CCRotateBy
00025 [L525] MOV      A=4 B=0 C=3 D=3 
00026 [L525] TGETS    A=3 B=3 C=7 D=775 'create'
00027 [L525] KSHORT   A=5 B=0 C=5 D=5 5
00028 [L525] MOV      A=6 B=0 C=2 D=2 
00029 [L525] CALL     A=3 B=2 C=4 D=516 
00030 [L526] UGET     A=4 B=0 C=2 D=2 CCEaseOut
00031 [L526] MOV      A=5 B=0 C=4 D=4 
00032 [L526] TGETS    A=4 B=4 C=7 D=1031 'create'
00033 [L526] MOV      A=6 B=0 C=3 D=3 
00034 [L526] KSHORT   A=7 B=0 C=3 D=3 3
00035 [L526] CALL     A=4 B=2 C=4 D=516 
00036 [L530] FNEW     A=5 B=0 C=8 D=8 {'kind': 'proto', 'id': 25}
00037 [L527] GSET     A=5 B=0 C=9 D=9 'unSchedule'
00038 [L531] UGET     A=5 B=0 C=3 D=3 CCCallFunc
00039 [L531] MOV      A=6 B=0 C=5 D=5 
00040 [L531] TGETS    A=5 B=5 C=7 D=1287 'create'
00041 [L531] GGET     A=7 B=0 C=9 D=9 'unSchedule'
00042 [L531] CALL     A=5 B=2 C=3 D=515 
00043 [L532] UGET     A=6 B=0 C=4 D=4 CCSequence
00044 [L532] MOV      A=7 B=0 C=6 D=6 
00045 [L532] TGETS    A=6 B=6 C=10 D=1546 'createWithTwoActions'
00046 [L532] MOV      A=8 B=0 C=4 D=4 
00047 [L532] MOV      A=9 B=0 C=5 D=5 
00048 [L532] CALL     A=6 B=2 C=4 D=516 
00049 [L533] GGET     A=7 B=0 C=0 D=0 'g_bagua'
00050 [L533] MOV      A=8 B=0 C=7 D=7 
00051 [L533] TGETS    A=7 B=7 C=11 D=1803 'runAction'
00052 [L533] MOV      A=9 B=0 C=6 D=6 
00053 [L533] CALL     A=7 B=1 C=3 D=259 
00054 [L551] FNEW     A=7 B=0 C=12 D=12 {'kind': 'proto', 'id': 26}
00055 [L552] UGET     A=8 B=0 C=5 D=5 CCDirector
00056 [L552] MOV      A=9 B=0 C=8 D=8 
00057 [L552] TGETS    A=8 B=8 C=13 D=2061 'sharedDirector'
00058 [L552] CALL     A=8 B=2 C=2 D=514 
00059 [L552] MOV      A=9 B=0 C=8 D=8 
00060 [L552] TGETS    A=8 B=8 C=14 D=2062 'getScheduler'
00061 [L552] CALL     A=8 B=2 C=2 D=514 
00062 [L552] MOV      A=9 B=0 C=8 D=8 
00063 [L552] TGETS    A=8 B=8 C=15 D=2063 'scheduleScriptFunc'
00064 [L552] MOV      A=10 B=0 C=7 D=7 
00065 [L552] KSHORT   A=11 B=0 C=0 D=0 0
00066 [L552] KPRI     A=12 B=0 C=1 D=1 
00067 [L552] CALL     A=8 B=2 C=5 D=517 
00068 [L552] GSET     A=8 B=0 C=16 D=16 'g_progressSchedule'
00069 [L553] UCLO     A=0 B=128 C=0 D=32768 target=70
00070 [L553] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto28 offset=0x3d5c source_lines=555-563 params=0
UPVALUES ['CCDirector']
00001 [L556] GGET     A=0 B=0 C=0 D=0 'g_progressSchedule'
00002 [L556] ISEQP    A=0 B=0 C=0 D=0 
00003 [L556] JMP      A=0 B=128 C=16 D=32784 target=20
00004 [L556] GGET     A=0 B=0 C=0 D=0 'g_progressSchedule'
00005 [L556] ISEQN    A=0 B=0 C=0 D=0 0
00006 [L556] JMP      A=0 B=128 C=13 D=32781 target=20
00007 [L557] UGET     A=0 B=0 C=0 D=0 CCDirector
00008 [L557] MOV      A=1 B=0 C=0 D=0 
00009 [L557] TGETS    A=0 B=0 C=1 D=1 'sharedDirector'
00010 [L557] CALL     A=0 B=2 C=2 D=514 
00011 [L557] MOV      A=1 B=0 C=0 D=0 
00012 [L557] TGETS    A=0 B=0 C=2 D=2 'getScheduler'
00013 [L557] CALL     A=0 B=2 C=2 D=514 
00014 [L557] MOV      A=1 B=0 C=0 D=0 
00015 [L557] TGETS    A=0 B=0 C=3 D=3 'unscheduleScriptEntry'
00016 [L557] GGET     A=2 B=0 C=0 D=0 'g_progressSchedule'
00017 [L557] CALL     A=0 B=1 C=3 D=259 
00018 [L558] KPRI     A=0 B=0 C=0 D=0 
00019 [L558] GSET     A=0 B=0 C=0 D=0 'g_progressSchedule'
00020 [L560] GGET     A=0 B=0 C=4 D=4 'g_bagua'
00021 [L560] MOV      A=1 B=0 C=0 D=0 
00022 [L560] TGETS    A=0 B=0 C=5 D=5 'stopAllActions'
00023 [L560] CALL     A=0 B=1 C=2 D=258 
00024 [L561] GGET     A=0 B=0 C=6 D=6 'g_self'
00025 [L561] TGETS    A=0 B=0 C=7 D=7 'data'
00026 [L561] TGETS    A=0 B=0 C=8 D=8 'result_index'
00027 [L561] IST      A=0 B=0 C=0 D=0 
00028 [L561] JMP      A=1 B=128 C=1 D=32769 target=30
00029 [L561] KSHORT   A=0 B=0 C=1 D=1 1
00030 [L562] GGET     A=1 B=0 C=4 D=4 'g_bagua'
00031 [L562] MOV      A=2 B=0 C=1 D=1 
00032 [L562] TGETS    A=1 B=1 C=9 D=265 'setRotation'
00033 [L562] KSHORT   A=3 B=0 C=0 D=0 0
00034 [L562] CALL     A=1 B=1 C=3 D=259 
00035 [L563] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto29 offset=0x3eb6 source_lines=576-578 params=3
UPVALUES []
00001 [L577] KPRI     A=3 B=0 C=2 D=2 
00002 [L577] RET1     A=3 B=0 C=2 D=2 

FUNCTION proto30 offset=0x3ee1 source_lines=603-605 params=0
UPVALUES ['prizeLayer']
00001 [L604] GGET     A=0 B=0 C=0 D=0 'g_self'
00002 [L604] TGETS    A=0 B=0 C=1 D=1 'main_layer'
00003 [L604] MOV      A=1 B=0 C=0 D=0 
00004 [L604] TGETS    A=0 B=0 C=2 D=2 'removeChild'
00005 [L604] UGET     A=2 B=0 C=0 D=0 prizeLayer
00006 [L604] KPRI     A=3 B=0 C=2 D=2 
00007 [L604] CALL     A=0 B=1 C=4 D=260 
00008 [L605] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto31 offset=0x3f41 source_lines=619-621 params=0
UPVALUES ['prize']
00001 [L620] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L620] TGETS    A=0 B=0 C=1 D=1 'd_data'
00003 [L620] TGETS    A=0 B=0 C=2 D=2 'showItemIntro'
00004 [L620] GGET     A=1 B=0 C=3 D=3 'g_self'
00005 [L620] TGETS    A=1 B=1 C=4 D=260 'main_layer'
00006 [L620] UGET     A=2 B=0 C=0 D=0 prize
00007 [L620] CALL     A=0 B=1 C=3 D=259 
00008 [L621] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto32 offset=0x3fab source_lines=565-645 params=0
UPVALUES ['CCLayer', 'CCSprite', 'CCArray', 'CCMenuItemImage', 'CCMenu', 'ccc3', 'CCMenuItemSprite', 'string']
00001 [L567] GGET     A=0 B=0 C=0 D=0 'update_tt_totaltime_label'
00002 [L567] CALL     A=0 B=1 C=1 D=257 
00003 [L568] GGET     A=0 B=0 C=1 D=1 'g_self'
00004 [L568] TGETS    A=0 B=0 C=2 D=2 'data'
00005 [L568] ISF      A=0 B=0 C=0 D=0 
00006 [L568] JMP      A=0 B=128 C=13 D=32781 target=20
00007 [L568] GGET     A=0 B=0 C=1 D=1 'g_self'
00008 [L568] TGETS    A=0 B=0 C=2 D=2 'data'
00009 [L568] TGETS    A=0 B=0 C=3 D=3 'reward_list'
00010 [L568] ISF      A=0 B=0 C=0 D=0 
00011 [L568] JMP      A=0 B=128 C=8 D=32776 target=20
00012 [L568] GGET     A=0 B=0 C=1 D=1 'g_self'
00013 [L568] TGETS    A=0 B=0 C=2 D=2 'data'
00014 [L568] TGETS    A=0 B=0 C=3 D=3 'reward_list'
00015 [L568] GGET     A=1 B=0 C=1 D=1 'g_self'
00016 [L568] TGETS    A=1 B=1 C=4 D=260 'index'
00017 [L568] TGETV    A=0 B=0 C=1 D=1 
00018 [L568] IST      A=0 B=0 C=0 D=0 
00019 [L568] JMP      A=0 B=128 C=1 D=32769 target=21
00020 [L569] UCLO     A=0 B=128 C=234 D=33002 target=255
00021 [L571] GGET     A=0 B=0 C=1 D=1 'g_self'
00022 [L571] TGETS    A=0 B=0 C=2 D=2 'data'
00023 [L571] TGETS    A=0 B=0 C=3 D=3 'reward_list'
00024 [L571] GGET     A=1 B=0 C=1 D=1 'g_self'
00025 [L571] TGETS    A=1 B=1 C=4 D=260 'index'
00026 [L571] TGETV    A=0 B=0 C=1 D=1 
00027 [L573] UGET     A=1 B=0 C=0 D=0 CCLayer
00028 [L573] MOV      A=2 B=0 C=1 D=1 
00029 [L573] TGETS    A=1 B=1 C=5 D=261 'create'
00030 [L573] CALL     A=1 B=2 C=2 D=514 
00031 [L574] GGET     A=2 B=0 C=1 D=1 'g_self'
00032 [L574] TGETS    A=2 B=2 C=6 D=518 'main_layer'
00033 [L574] MOV      A=3 B=0 C=2 D=2 
00034 [L574] TGETS    A=2 B=2 C=7 D=519 'addChild'
00035 [L574] MOV      A=4 B=0 C=1 D=1 
00036 [L574] KSHORT   A=5 B=0 C=50 D=50 50
00037 [L574] CALL     A=2 B=1 C=4 D=260 
00038 [L578] FNEW     A=2 B=0 C=8 D=8 {'kind': 'proto', 'id': 29}
00039 [L580] MOV      A=4 B=0 C=1 D=1 
00040 [L580] TGETS    A=3 B=1 C=9 D=265 'registerScriptTouchHandler'
00041 [L580] MOV      A=5 B=0 C=2 D=2 
00042 [L580] KPRI     A=6 B=0 C=1 D=1 
00043 [L580] KSHORT   A=7 B=255 C=128 D=65408 -128
00044 [L580] KPRI     A=8 B=0 C=2 D=2 
00045 [L580] CALL     A=3 B=1 C=6 D=262 
00046 [L581] MOV      A=4 B=0 C=1 D=1 
00047 [L581] TGETS    A=3 B=1 C=10 D=266 'setTouchEnabled'
00048 [L581] KPRI     A=5 B=0 C=2 D=2 
00049 [L581] CALL     A=3 B=1 C=3 D=259 
00050 [L583] UGET     A=3 B=0 C=1 D=1 CCSprite
00051 [L583] MOV      A=4 B=0 C=3 D=3 
00052 [L583] TGETS    A=3 B=3 C=5 D=773 'create'
00053 [L583] KSTR     A=5 B=0 C=11 D=11 'v2/messageUI/frame1.png'
00054 [L583] CALL     A=3 B=2 C=3 D=515 
00055 [L584] GGET     A=4 B=0 C=12 D=12 'd_ms'
00056 [L584] TGETS    A=4 B=4 C=13 D=1037 'd_u'
00057 [L584] TGETS    A=4 B=4 C=14 D=1038 'setStyles'
00058 [L584] MOV      A=5 B=0 C=3 D=3 
00059 [L584] TDUP     A=6 B=0 C=15 D=15 {'kind': 'table', 'value': {'x': 0.5, 'y': 0.5}}
00060 [L584] GGET     A=7 B=0 C=16 D=16 'scale'
00061 [L584] TSETS    A=7 B=6 C=17 D=1553 'scaleH'
00062 [L584] CALL     A=4 B=1 C=3 D=259 
00063 [L585] MOV      A=5 B=0 C=1 D=1 
00064 [L585] TGETS    A=4 B=1 C=7 D=263 'addChild'
00065 [L585] MOV      A=6 B=0 C=3 D=3 
00066 [L585] CALL     A=4 B=1 C=3 D=259 
00067 [L586] MOV      A=5 B=0 C=3 D=3 
00068 [L586] TGETS    A=4 B=3 C=18 D=786 'getScale'
00069 [L586] CALL     A=4 B=2 C=2 D=514 
00070 [L588] MOV      A=6 B=0 C=3 D=3 
00071 [L588] TGETS    A=5 B=3 C=19 D=787 'getContentSize'
00072 [L588] CALL     A=5 B=2 C=2 D=514 
00073 [L589] MOV      A=7 B=0 C=3 D=3 
00074 [L589] TGETS    A=6 B=3 C=20 D=788 'getPositionLua'
00075 [L589] CALL     A=6 B=2 C=2 D=514 
00076 [L591] UGET     A=7 B=0 C=1 D=1 CCSprite
00077 [L591] MOV      A=8 B=0 C=7 D=7 
00078 [L591] TGETS    A=7 B=7 C=5 D=1797 'create'
00079 [L591] KSTR     A=9 B=0 C=21 D=21 'v2/messageUI/frame2.png'
00080 [L591] CALL     A=7 B=2 C=3 D=515 
00081 [L592] GGET     A=8 B=0 C=12 D=12 'd_ms'
00082 [L592] TGETS    A=8 B=8 C=13 D=2061 'd_u'
00083 [L592] TGETS    A=8 B=8 C=14 D=2062 'setStyles'
00084 [L592] MOV      A=9 B=0 C=7 D=7 
00085 [L592] TDUP     A=10 B=0 C=22 D=22 {'kind': 'table', 'value': {'x': 0.5, 'y': 0.5}}
00086 [L592] CALL     A=8 B=1 C=3 D=259 
00087 [L593] MOV      A=9 B=0 C=1 D=1 
00088 [L593] TGETS    A=8 B=1 C=7 D=263 'addChild'
00089 [L593] MOV      A=10 B=0 C=7 D=7 
00090 [L593] CALL     A=8 B=1 C=3 D=259 
00091 [L594] MOV      A=9 B=0 C=7 D=7 
00092 [L594] TGETS    A=8 B=7 C=23 D=1815 'setScale'
00093 [L594] MOV      A=10 B=0 C=4 D=4 
00094 [L594] CALL     A=8 B=1 C=3 D=259 
00095 [L596] TGETS    A=8 B=5 C=24 D=1304 'height'
00096 [L596] MULNV    A=8 B=8 C=0 D=2048 
00097 [L596] MULVV    A=8 B=8 C=4 D=2052 
00098 [L597] UGET     A=9 B=0 C=1 D=1 CCSprite
00099 [L597] MOV      A=10 B=0 C=9 D=9 
00100 [L597] TGETS    A=9 B=9 C=5 D=2309 'create'
00101 [L597] KSTR     A=11 B=0 C=25 D=25 'v2/messageUI/title.png'
00102 [L597] CALL     A=9 B=2 C=3 D=515 
00103 [L598] MOV      A=11 B=0 C=9 D=9 
00104 [L598] TGETS    A=10 B=9 C=26 D=2330 'setPosition'
00105 [L598] TGETS    A=12 B=6 C=27 D=1563 'x'
00106 [L598] TGETS    A=13 B=6 C=28 D=1564 'y'
00107 [L598] ADDVV    A=13 B=13 C=8 D=3336 
00108 [L598] CALL     A=10 B=1 C=4 D=260 
00109 [L599] MOV      A=11 B=0 C=1 D=1 
00110 [L599] TGETS    A=10 B=1 C=7 D=263 'addChild'
00111 [L599] MOV      A=12 B=0 C=9 D=9 
00112 [L599] CALL     A=10 B=1 C=3 D=259 
00113 [L600] MOV      A=11 B=0 C=9 D=9 
00114 [L600] TGETS    A=10 B=9 C=23 D=2327 'setScale'
00115 [L600] MOV      A=12 B=0 C=4 D=4 
00116 [L600] CALL     A=10 B=1 C=3 D=259 
00117 [L605] FNEW     A=10 B=0 C=29 D=29 {'kind': 'proto', 'id': 30}
00118 [L607] UGET     A=11 B=0 C=2 D=2 CCArray
00119 [L607] MOV      A=12 B=0 C=11 D=11 
00120 [L607] TGETS    A=11 B=11 C=5 D=2821 'create'
00121 [L607] CALL     A=11 B=2 C=2 D=514 
00122 [L609] UGET     A=12 B=0 C=3 D=3 CCMenuItemImage
00123 [L609] MOV      A=13 B=0 C=12 D=12 
00124 [L609] TGETS    A=12 B=12 C=5 D=3077 'create'
00125 [L609] KSTR     A=14 B=0 C=30 D=30 'v2/multi-selectUI/ensure1.png'
00126 [L609] KSTR     A=15 B=0 C=31 D=31 'v2/multi-selectUI/ensure2.png'
00127 [L609] CALL     A=12 B=2 C=4 D=516 
00128 [L611] MOV      A=14 B=0 C=12 D=12 
00129 [L611] TGETS    A=13 B=12 C=26 D=3098 'setPosition'
00130 [L611] TGETS    A=15 B=6 C=27 D=1563 'x'
00131 [L611] TGETS    A=16 B=6 C=28 D=1564 'y'
00132 [L611] SUBVV    A=16 B=16 C=8 D=4104 
00133 [L611] CALL     A=13 B=1 C=4 D=260 
00134 [L612] MOV      A=14 B=0 C=12 D=12 
00135 [L612] TGETS    A=13 B=12 C=32 D=3104 'registerScriptTapHandler'
00136 [L612] MOV      A=15 B=0 C=10 D=10 
00137 [L612] CALL     A=13 B=1 C=3 D=259 
00138 [L613] MOV      A=14 B=0 C=11 D=11 
00139 [L613] TGETS    A=13 B=11 C=33 D=2849 'addObject'
00140 [L613] MOV      A=15 B=0 C=12 D=12 
00141 [L613] CALL     A=13 B=1 C=3 D=259 
00142 [L615] UGET     A=13 B=0 C=4 D=4 CCMenu
00143 [L615] MOV      A=14 B=0 C=13 D=13 
00144 [L615] TGETS    A=13 B=13 C=34 D=3362 'createWithArray'
00145 [L615] MOV      A=15 B=0 C=11 D=11 
00146 [L615] CALL     A=13 B=2 C=3 D=515 
00147 [L616] MOV      A=15 B=0 C=13 D=13 
00148 [L616] TGETS    A=14 B=13 C=26 D=3354 'setPosition'
00149 [L616] KSHORT   A=16 B=0 C=0 D=0 0
00150 [L616] KSHORT   A=17 B=0 C=0 D=0 0
00151 [L616] CALL     A=14 B=1 C=4 D=260 
00152 [L617] MOV      A=15 B=0 C=1 D=1 
00153 [L617] TGETS    A=14 B=1 C=7 D=263 'addChild'
00154 [L617] MOV      A=16 B=0 C=13 D=13 
00155 [L617] CALL     A=14 B=1 C=3 D=259 
00156 [L621] FNEW     A=14 B=0 C=35 D=35 {'kind': 'proto', 'id': 31}
00157 [L623] GGET     A=15 B=0 C=12 D=12 'd_ms'
00158 [L623] TGETS    A=15 B=15 C=36 D=3876 'd_data'
00159 [L623] TGETS    A=15 B=15 C=37 D=3877 'getCertainSmallSprite'
00160 [L623] TGETS    A=16 B=0 C=38 D=38 'object_type'
00161 [L623] TGETS    A=17 B=0 C=39 D=39 'attach_type'
00162 [L623] CALL     A=15 B=2 C=3 D=515 
00163 [L624] GGET     A=16 B=0 C=12 D=12 'd_ms'
00164 [L624] TGETS    A=16 B=16 C=36 D=4132 'd_data'
00165 [L624] TGETS    A=16 B=16 C=37 D=4133 'getCertainSmallSprite'
00166 [L624] TGETS    A=17 B=0 C=38 D=38 'object_type'
00167 [L624] TGETS    A=18 B=0 C=39 D=39 'attach_type'
00168 [L624] CALL     A=16 B=2 C=3 D=515 
00169 [L625] MOV      A=18 B=0 C=16 D=16 
00170 [L625] TGETS    A=17 B=16 C=40 D=4136 'setColor'
00171 [L625] UGET     A=19 B=0 C=5 D=5 ccc3
00172 [L625] KSHORT   A=20 B=0 C=100 D=100 100
00173 [L625] KSHORT   A=21 B=0 C=100 D=100 100
00174 [L625] KSHORT   A=22 B=0 C=100 D=100 100
00175 [L625] CALL     A=19 B=0 C=4 D=4 
00176 [L625] CALLM    A=17 B=1 C=1 D=257 
00177 [L626] UGET     A=17 B=0 C=6 D=6 CCMenuItemSprite
00178 [L626] MOV      A=18 B=0 C=17 D=17 
00179 [L626] TGETS    A=17 B=17 C=5 D=4357 'create'
00180 [L626] MOV      A=19 B=0 C=15 D=15 
00181 [L626] MOV      A=20 B=0 C=16 D=16 
00182 [L626] CALL     A=17 B=2 C=4 D=516 
00183 [L627] GGET     A=18 B=0 C=12 D=12 'd_ms'
00184 [L627] TGETS    A=18 B=18 C=13 D=4621 'd_u'
00185 [L627] TGETS    A=18 B=18 C=14 D=4622 'setStyles'
00186 [L627] MOV      A=19 B=0 C=17 D=17 
00187 [L627] TDUP     A=20 B=0 C=41 D=41 {'kind': 'table', 'value': {'scale': 0.09, 'x': 0.5, 'y': 0.5}}
00188 [L627] CALL     A=18 B=1 C=3 D=259 
00189 [L628] MOV      A=19 B=0 C=17 D=17 
00190 [L628] TGETS    A=18 B=17 C=32 D=4384 'registerScriptTapHandler'
00191 [L628] MOV      A=20 B=0 C=14 D=14 
00192 [L628] CALL     A=18 B=1 C=3 D=259 
00193 [L630] UGET     A=18 B=0 C=4 D=4 CCMenu
00194 [L630] MOV      A=19 B=0 C=18 D=18 
00195 [L630] TGETS    A=18 B=18 C=42 D=4650 'createWithItem'
00196 [L630] MOV      A=20 B=0 C=17 D=17 
00197 [L630] CALL     A=18 B=2 C=3 D=515 
00198 [L631] MOV      A=20 B=0 C=18 D=18 
00199 [L631] TGETS    A=19 B=18 C=26 D=4634 'setPosition'
00200 [L631] KSHORT   A=21 B=0 C=0 D=0 0
00201 [L631] KSHORT   A=22 B=0 C=0 D=0 0
00202 [L631] CALL     A=19 B=1 C=4 D=260 
00203 [L632] MOV      A=20 B=0 C=1 D=1 
00204 [L632] TGETS    A=19 B=1 C=7 D=263 'addChild'
00205 [L632] MOV      A=21 B=0 C=18 D=18 
00206 [L632] CALL     A=19 B=1 C=3 D=259 
00207 [L634] GGET     A=19 B=0 C=12 D=12 'd_ms'
00208 [L634] TGETS    A=19 B=19 C=36 D=4900 'd_data'
00209 [L634] TGETS    A=19 B=19 C=43 D=4907 'getCertainInfo'
00210 [L634] TGETS    A=20 B=0 C=38 D=38 'object_type'
00211 [L634] TGETS    A=21 B=0 C=39 D=39 'attach_type'
00212 [L634] CALL     A=19 B=2 C=3 D=515 
00213 [L635] TGETS    A=20 B=19 C=44 D=4908 'name'
00214 [L636] TGETS    A=21 B=0 C=45 D=45 'attach_count'
00215 [L636] KSHORT   A=22 B=0 C=0 D=0 0
00216 [L636] ISGE     A=22 B=0 C=21 D=21 
00217 [L636] JMP      A=21 B=128 C=4 D=32772 target=222
00218 [L637] MOV      A=21 B=0 C=20 D=20 
00219 [L637] KSTR     A=22 B=0 C=46 D=46 ' x'
00220 [L637] TGETS    A=23 B=0 C=45 D=45 'attach_count'
00221 [L637] CAT      A=20 B=21 C=23 D=5399 
00222 [L639] GGET     A=21 B=0 C=12 D=12 'd_ms'
00223 [L639] TGETS    A=21 B=21 C=13 D=5389 'd_u'
00224 [L639] TGETS    A=21 B=21 C=47 D=5423 'createByStyle'
00225 [L639] TDUP     A=22 B=0 C=48 D=48 {'kind': 'table', 'value': {'y': 0.4, 'font': 'arial', 'type': 'label', 'x': 0.5, 'fontsize': 30}}
00226 [L639] TSETS    A=20 B=22 C=49 D=5681 'string'
00227 [L639] CALL     A=21 B=2 C=2 D=514 
00228 [L640] MOV      A=23 B=0 C=1 D=1 
00229 [L640] TGETS    A=22 B=1 C=7 D=263 'addChild'
00230 [L640] MOV      A=24 B=0 C=21 D=21 
00231 [L640] KSHORT   A=25 B=0 C=5 D=5 5
00232 [L640] CALL     A=22 B=1 C=4 D=260 
00233 [L642] UGET     A=22 B=0 C=7 D=7 string
00234 [L642] TGETS    A=22 B=22 C=50 D=5682 'format'
00235 [L642] GGET     A=23 B=0 C=12 D=12 'd_ms'
00236 [L642] TGETS    A=23 B=23 C=51 D=5939 'd_hz'
00237 [L642] TGETS    A=23 B=23 C=52 D=5940 'gethz'
00238 [L642] KSTR     A=24 B=0 C=53 D=53 'treasure_congratulaton'
00239 [L642] CALL     A=23 B=2 C=2 D=514 
00240 [L642] TGETS    A=24 B=19 C=44 D=4908 'name'
00241 [L642] CALL     A=22 B=2 C=3 D=515 
00242 [L643] GGET     A=23 B=0 C=12 D=12 'd_ms'
00243 [L643] TGETS    A=23 B=23 C=13 D=5901 'd_u'
00244 [L643] TGETS    A=23 B=23 C=47 D=5935 'createByStyle'
00245 [L643] TDUP     A=24 B=0 C=54 D=54 {'kind': 'table', 'value': {'y': 0.64, 'font': 'arial', 'type': 'label', 'x': 0.5, 'fontsize': 30}}
00246 [L643] TSETS    A=22 B=24 C=49 D=6193 'string'
00247 [L643] CALL     A=23 B=2 C=2 D=514 
00248 [L644] MOV      A=25 B=0 C=1 D=1 
00249 [L644] TGETS    A=24 B=1 C=7 D=263 'addChild'
00250 [L644] MOV      A=26 B=0 C=23 D=23 
00251 [L644] KSHORT   A=27 B=0 C=5 D=5 5
00252 [L644] CALL     A=24 B=1 C=4 D=260 
00253 [L645] UCLO     A=0 B=128 C=0 D=32768 target=254
00254 [L645] RET0     A=0 B=0 C=1 D=1 
00255 [L645] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto33 offset=0x4945 source_lines=663-665 params=0
UPVALUES ['layer']
00001 [L664] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L664] TGETS    A=0 B=0 C=1 D=1 'd_u'
00003 [L664] TGETS    A=0 B=0 C=2 D=2 'remove'
00004 [L664] UGET     A=1 B=0 C=0 D=0 layer
00005 [L664] CALL     A=0 B=1 C=2 D=258 
00006 [L665] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto34 offset=0x4988 source_lines=666-668 params=0
UPVALUES ['layer']
00001 [L667] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L667] TGETS    A=0 B=0 C=1 D=1 'd_u'
00003 [L667] TGETS    A=0 B=0 C=2 D=2 'remove'
00004 [L667] UGET     A=1 B=0 C=0 D=0 layer
00005 [L667] CALL     A=0 B=1 C=2 D=258 
00006 [L668] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto35 offset=0x49cc source_lines=670-675 params=1
UPVALUES ['items']
00001 [L671] UGET     A=1 B=0 C=0 D=0 items
00002 [L671] TGETV    A=1 B=1 C=0 D=256 
00003 [L672] ISF      A=0 B=0 C=1 D=1 
00004 [L672] JMP      A=2 B=128 C=7 D=32775 target=12
00005 [L673] GGET     A=2 B=0 C=0 D=0 'd_ms'
00006 [L673] TGETS    A=2 B=2 C=1 D=513 'd_data'
00007 [L673] TGETS    A=2 B=2 C=2 D=514 'showItemIntro'
00008 [L673] GGET     A=3 B=0 C=3 D=3 'g_self'
00009 [L673] TGETS    A=3 B=3 C=4 D=772 'main_layer'
00010 [L673] MOV      A=4 B=0 C=1 D=1 
00011 [L673] CALL     A=2 B=1 C=3 D=259 
00012 [L675] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto36 offset=0x4a59 source_lines=648-700 params=1
UPVALUES ['CCSprite', 'math', 'table']
00001 [L649] GGET     A=1 B=0 C=0 D=0 'g_self'
00002 [L649] TGETS    A=1 B=1 C=1 D=257 'main_layer'
00003 [L649] ISF      A=0 B=0 C=1 D=1 
00004 [L649] JMP      A=1 B=128 C=2 D=32770 target=7
00005 [L649] IST      A=0 B=0 C=0 D=0 
00006 [L649] JMP      A=1 B=128 C=1 D=32769 target=8
00007 [L650] UCLO     A=0 B=128 C=138 D=32906 target=146
00008 [L653] GGET     A=1 B=0 C=2 D=2 'd_ms'
00009 [L653] TGETS    A=1 B=1 C=3 D=259 'd_u'
00010 [L653] TGETS    A=1 B=1 C=4 D=260 'clearLayer'
00011 [L653] GGET     A=2 B=0 C=0 D=0 'g_self'
00012 [L653] TGETS    A=2 B=2 C=1 D=513 'main_layer'
00013 [L653] KSHORT   A=3 B=0 C=100 D=100 100
00014 [L653] GGET     A=4 B=0 C=0 D=0 'g_self'
00015 [L653] TGETS    A=4 B=4 C=5 D=1029 'giftDetailTag'
00016 [L653] CALL     A=1 B=2 C=4 D=516 
00017 [L654] GGET     A=2 B=0 C=2 D=2 'd_ms'
00018 [L654] TGETS    A=2 B=2 C=3 D=515 'd_u'
00019 [L654] TGETS    A=2 B=2 C=6 D=518 'createSwallowTouchLayer'
00020 [L654] MOV      A=3 B=0 C=1 D=1 
00021 [L654] CALL     A=2 B=1 C=2 D=258 
00022 [L656] GGET     A=2 B=0 C=2 D=2 'd_ms'
00023 [L656] TGETS    A=2 B=2 C=3 D=515 'd_u'
00024 [L656] TGETS    A=2 B=2 C=7 D=519 'createByStyle'
00025 [L656] TDUP     A=3 B=0 C=8 D=8 {'kind': 'table', 'value': {'pic': 'v2/turnTableUI/bkg2.png', 'x': 0.5, 'y': 0.5}}
00026 [L656] CALL     A=2 B=2 C=2 D=514 
00027 [L657] MOV      A=4 B=0 C=1 D=1 
00028 [L657] TGETS    A=3 B=1 C=9 D=265 'addChild'
00029 [L657] MOV      A=5 B=0 C=2 D=2 
00030 [L657] CALL     A=3 B=1 C=3 D=259 
00031 [L658] GGET     A=3 B=0 C=2 D=2 'd_ms'
00032 [L658] TGETS    A=3 B=3 C=3 D=771 'd_u'
00033 [L658] TGETS    A=3 B=3 C=10 D=778 'getRealScale'
00034 [L658] MOV      A=4 B=0 C=2 D=2 
00035 [L658] CALL     A=3 B=3 C=2 D=770 
00036 [L660] MOV      A=6 B=0 C=1 D=1 
00037 [L660] TGETS    A=5 B=1 C=9 D=265 'addChild'
00038 [L660] GGET     A=7 B=0 C=2 D=2 'd_ms'
00039 [L660] TGETS    A=7 B=7 C=3 D=1795 'd_u'
00040 [L660] TGETS    A=7 B=7 C=7 D=1799 'createByStyle'
00041 [L660] TDUP     A=8 B=0 C=11 D=11 {'kind': 'table', 'value': {'pic': 'v2/turnTableUI/title.png', 'x': 0.5}}
00042 [L660] MULNV    A=9 B=4 C=0 D=1024 
00043 [L660] ADDNV    A=9 B=9 C=1 D=2305 
00044 [L660] TSETS    A=9 B=8 C=12 D=2060 'y'
00045 [L660] CALL     A=7 B=0 C=2 D=2 
00046 [L660] CALLM    A=5 B=1 C=1 D=257 
00047 [L665] FNEW     A=5 B=0 C=13 D=13 {'kind': 'proto', 'id': 33}
00048 [L668] FNEW     A=6 B=0 C=14 D=14 {'kind': 'proto', 'id': 34}
00049 [L675] FNEW     A=7 B=0 C=15 D=15 {'kind': 'proto', 'id': 35}
00050 [L677] UGET     A=8 B=0 C=0 D=0 CCSprite
00051 [L677] MOV      A=9 B=0 C=8 D=8 
00052 [L677] TGETS    A=8 B=8 C=16 D=2064 'create'
00053 [L677] KSTR     A=10 B=0 C=17 D=17 'v2/batchBuyUI/ensure1.png'
00054 [L677] CALL     A=8 B=2 C=3 D=515 
00055 [L677] GSET     A=8 B=0 C=18 D=18 'npic'
00056 [L678] UGET     A=8 B=0 C=0 D=0 CCSprite
00057 [L678] MOV      A=9 B=0 C=8 D=8 
00058 [L678] TGETS    A=8 B=8 C=16 D=2064 'create'
00059 [L678] KSTR     A=10 B=0 C=17 D=17 'v2/batchBuyUI/ensure1.png'
00060 [L678] CALL     A=8 B=2 C=3 D=515 
00061 [L678] GSET     A=8 B=0 C=19 D=19 'spic'
00062 [L681] TDUP     A=8 B=0 C=20 D=20 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00063 [L684] TDUP     A=9 B=0 C=21 D=21 {'kind': 'table', 'value': {'x': 0.5}}
00064 [L685] GGET     A=10 B=0 C=18 D=18 'npic'
00065 [L685] TSETS    A=10 B=9 C=22 D=2326 'nsprite'
00066 [L685] GGET     A=10 B=0 C=19 D=19 'spic'
00067 [L685] TSETS    A=10 B=9 C=23 D=2327 'ssprite'
00068 [L685] MULNV    A=10 B=4 C=2 D=1026 
00069 [L685] SUBNV    A=10 B=10 C=1 D=2561 
00070 [L685] TSETS    A=10 B=9 C=12 D=2316 'y'
00071 [L685] TSETS    A=5 B=9 C=24 D=2328 'call_back'
00072 [L685] TSETB    A=9 B=8 C=1 D=2049 
00073 [L685] TDUP     A=9 B=0 C=25 D=25 {'kind': 'table', 'value': {'npic': 'v2/common/close1.png', 'spic': 'v2/common/close2.png'}}
00074 [L686] MULVN    A=10 B=3 C=2 D=770 
00075 [L686] ADDNV    A=10 B=10 C=1 D=2561 
00076 [L686] TSETS    A=10 B=9 C=26 D=2330 'x'
00077 [L686] MULVN    A=10 B=4 C=0 D=1024 
00078 [L686] ADDNV    A=10 B=10 C=1 D=2561 
00079 [L686] TSETS    A=10 B=9 C=12 D=2316 'y'
00080 [L686] TSETS    A=6 B=9 C=24 D=2328 'call_back'
00081 [L686] TSETB    A=9 B=8 C=2 D=2050 
00082 [L689] KSHORT   A=9 B=0 C=1 D=1 1
00083 [L689] LEN      A=10 B=0 C=0 D=0 
00084 [L689] KSHORT   A=11 B=0 C=1 D=1 1
00085 [L689] FORI     A=9 B=128 C=47 D=32815 target=133
00086 [L690] MULNV    A=13 B=3 C=3 D=771 
00087 [L690] SUBNV    A=13 B=13 C=1 D=3329 
00088 [L690] SUBVN    A=14 B=12 C=4 D=3076 
00089 [L690] MODVN    A=14 B=14 C=5 D=3589 
00090 [L690] MULVN    A=14 B=14 C=3 D=3587 
00091 [L690] MULVV    A=14 B=14 C=3 D=3587 
00092 [L690] ADDVV    A=13 B=13 C=14 D=3342 
00093 [L690] MULNV    A=14 B=4 C=6 D=1030 
00094 [L690] ADDNV    A=14 B=14 C=1 D=3585 
00095 [L690] UGET     A=15 B=0 C=1 D=1 math
00096 [L690] TGETS    A=15 B=15 C=27 D=3867 'floor'
00097 [L690] SUBVN    A=16 B=12 C=4 D=3076 
00098 [L690] DIVVN    A=16 B=16 C=5 D=4101 
00099 [L690] CALL     A=15 B=2 C=2 D=514 
00100 [L690] MULVN    A=15 B=15 C=7 D=3847 
00101 [L690] MULVV    A=15 B=15 C=4 D=3844 
00102 [L690] SUBVV    A=14 B=14 C=15 D=3599 
00103 [L691] MOV      A=16 B=0 C=1 D=1 
00104 [L691] TGETS    A=15 B=1 C=9 D=265 'addChild'
00105 [L691] GGET     A=17 B=0 C=2 D=2 'd_ms'
00106 [L691] TGETS    A=17 B=17 C=3 D=4355 'd_u'
00107 [L691] TGETS    A=17 B=17 C=7 D=4359 'createByStyle'
00108 [L691] TDUP     A=18 B=0 C=28 D=28 {'kind': 'table', 'value': {'pic': 'v2/turnTableUI/icon_bkg.png'}}
00109 [L691] TSETS    A=13 B=18 C=26 D=4634 'x'
00110 [L691] TSETS    A=14 B=18 C=12 D=4620 'y'
00111 [L691] CALL     A=17 B=2 C=2 D=514 
00112 [L691] KSHORT   A=18 B=0 C=1 D=1 1
00113 [L691] CALL     A=15 B=1 C=4 D=260 
00114 [L693] GGET     A=15 B=0 C=2 D=2 'd_ms'
00115 [L693] TGETS    A=15 B=15 C=29 D=3869 'd_actNoticeUI'
00116 [L693] TGETS    A=15 B=15 C=30 D=3870 'getSprite'
00117 [L693] TGETV    A=16 B=0 C=12 D=12 
00118 [L693] CALL     A=15 B=2 C=2 D=514 
00119 [L695] UGET     A=16 B=0 C=2 D=2 table
00120 [L695] TGETS    A=16 B=16 C=31 D=4127 'insert'
00121 [L695] MOV      A=17 B=0 C=8 D=8 
00122 [L695] TDUP     A=18 B=0 C=32 D=32 {'kind': 'table', 'value': {}}
00123 [L695] TSETS    A=15 B=18 C=22 D=4630 'nsprite'
00124 [L695] TSETS    A=15 B=18 C=23 D=4631 'ssprite'
00125 [L695] MULNV    A=19 B=3 C=8 D=776 
00126 [L695] TSETS    A=19 B=18 C=33 D=4641 'scale'
00127 [L695] TSETS    A=13 B=18 C=26 D=4634 'x'
00128 [L695] TSETS    A=14 B=18 C=12 D=4620 'y'
00129 [L695] TSETS    A=12 B=18 C=34 D=4642 'tag'
00130 [L695] TSETS    A=7 B=18 C=24 D=4632 'call_back'
00131 [L695] CALL     A=16 B=1 C=3 D=259 
00132 [L689] FORL     A=9 B=127 C=209 D=32721 target=86
00133 [L697] TNEW     A=9 B=0 C=0 D=0 
00134 [L698] MOV      A=11 B=0 C=1 D=1 
00135 [L698] TGETS    A=10 B=1 C=9 D=265 'addChild'
00136 [L698] GGET     A=12 B=0 C=2 D=2 'd_ms'
00137 [L698] TGETS    A=12 B=12 C=3 D=3075 'd_u'
00138 [L698] TGETS    A=12 B=12 C=35 D=3107 'createMenu'
00139 [L698] MOV      A=13 B=0 C=8 D=8 
00140 [L698] MOV      A=14 B=0 C=9 D=9 
00141 [L698] CALL     A=12 B=2 C=3 D=515 
00142 [L698] KSHORT   A=13 B=0 C=10 D=10 10
00143 [L698] CALL     A=10 B=1 C=4 D=260 
00144 [L700] UCLO     A=0 B=128 C=0 D=32768 target=145
00145 [L700] RET0     A=0 B=0 C=1 D=1 
00146 [L700] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto37 offset=0x4fd5 source_lines=702-737 params=1
UPVALUES ['pairs', 'o_t', 'table', 'm_t']
00001 [L703] TNEW     A=1 B=0 C=0 D=0 
00002 [L704] IST      A=0 B=0 C=0 D=0 
00003 [L704] JMP      A=2 B=128 C=1 D=32769 target=5
00004 [L705] RET1     A=1 B=0 C=2 D=2 
00005 [L707] GGET     A=2 B=0 C=0 D=0 'd_ms'
00006 [L707] TGETS    A=2 B=2 C=1 D=513 'd_data'
00007 [L707] TGETS    A=2 B=2 C=2 D=514 'g_specialItemUseTable'
00008 [L707] ISF      A=0 B=0 C=2 D=2 
00009 [L707] JMP      A=2 B=128 C=11 D=32779 target=21
00010 [L707] GGET     A=2 B=0 C=0 D=0 'd_ms'
00011 [L707] TGETS    A=2 B=2 C=1 D=513 'd_data'
00012 [L707] TGETS    A=2 B=2 C=2 D=514 'g_specialItemUseTable'
00013 [L707] ISF      A=0 B=0 C=2 D=2 
00014 [L707] JMP      A=2 B=128 C=6 D=32774 target=21
00015 [L707] GGET     A=2 B=0 C=0 D=0 'd_ms'
00016 [L707] TGETS    A=2 B=2 C=1 D=513 'd_data'
00017 [L707] TGETS    A=2 B=2 C=2 D=514 'g_specialItemUseTable'
00018 [L707] TGETV    A=2 B=2 C=0 D=512 
00019 [L707] IST      A=0 B=0 C=2 D=2 
00020 [L707] JMP      A=2 B=128 C=1 D=32769 target=22
00021 [L708] RET1     A=1 B=0 C=2 D=2 
00022 [L710] UGET     A=2 B=0 C=0 D=0 pairs
00023 [L710] GGET     A=3 B=0 C=0 D=0 'd_ms'
00024 [L710] TGETS    A=3 B=3 C=1 D=769 'd_data'
00025 [L710] TGETS    A=3 B=3 C=2 D=770 'g_specialItemUseTable'
00026 [L710] TGETV    A=3 B=3 C=0 D=768 
00027 [L710] CALL     A=2 B=4 C=2 D=1026 
00028 [L710] ISNEXT   A=5 B=128 C=94 D=32862 target=123
00029 [L711] TGETS    A=7 B=6 C=3 D=1539 'object_type'
00030 [L711] UGET     A=8 B=0 C=1 D=1 o_t
00031 [L711] TGETS    A=8 B=8 C=4 D=2052 'spirit'
00032 [L711] ISNEV    A=7 B=0 C=8 D=8 
00033 [L711] JMP      A=7 B=128 C=39 D=32807 target=73
00034 [L712] KPRI     A=7 B=0 C=1 D=1 
00035 [L713] UGET     A=8 B=0 C=0 D=0 pairs
00036 [L713] GGET     A=9 B=0 C=0 D=0 'd_ms'
00037 [L713] TGETS    A=9 B=9 C=5 D=2309 'd_lineupUI'
00038 [L713] TGETS    A=9 B=9 C=6 D=2310 'g_characterInfo'
00039 [L713] CALL     A=8 B=4 C=2 D=1026 
00040 [L713] ISNEXT   A=11 B=128 C=13 D=32781 target=54
00041 [L714] TGETS    A=13 B=12 C=7 D=3079 'type'
00042 [L714] TGETS    A=14 B=6 C=8 D=1544 'attach_type'
00043 [L714] ISNEV    A=13 B=0 C=14 D=14 
00044 [L714] JMP      A=13 B=128 C=9 D=32777 target=54
00045 [L715] UGET     A=13 B=0 C=2 D=2 table
00046 [L715] TGETS    A=13 B=13 C=9 D=3337 'insert'
00047 [L715] MOV      A=14 B=0 C=1 D=1 
00048 [L715] TDUP     A=15 B=0 C=10 D=10 {'kind': 'table', 'value': {'hasGot': True}}
00049 [L715] TGETS    A=16 B=6 C=11 D=1547 'attach_count'
00050 [L715] TSETS    A=16 B=15 C=12 D=3852 'ratio'
00051 [L715] TSETS    A=12 B=15 C=13 D=3853 'char'
00052 [L715] CALL     A=13 B=1 C=3 D=259 
00053 [L716] KPRI     A=7 B=0 C=2 D=2 
00054 [L713] ITERN    A=11 B=3 C=3 D=771 
00055 [L713] ITERL    A=11 B=127 C=241 D=32753 target=41
00056 [L719] IST      A=0 B=0 C=7 D=7 
00057 [L719] JMP      A=8 B=128 C=65 D=32833 target=123
00058 [L720] UGET     A=8 B=0 C=2 D=2 table
00059 [L720] TGETS    A=8 B=8 C=9 D=2057 'insert'
00060 [L720] MOV      A=9 B=0 C=1 D=1 
00061 [L720] TDUP     A=10 B=0 C=14 D=14 {'kind': 'table', 'value': {'hasGot': False}}
00062 [L720] TGETS    A=11 B=6 C=11 D=1547 'attach_count'
00063 [L720] TSETS    A=11 B=10 C=12 D=2572 'ratio'
00064 [L720] TDUP     A=11 B=0 C=15 D=15 {'kind': 'table', 'value': {}}
00065 [L720] UGET     A=12 B=0 C=1 D=1 o_t
00066 [L720] TGETS    A=12 B=12 C=4 D=3076 'spirit'
00067 [L720] TSETS    A=12 B=11 C=3 D=2819 'object_type'
00068 [L720] TGETS    A=12 B=6 C=8 D=1544 'attach_type'
00069 [L720] TSETS    A=12 B=11 C=16 D=2832 'type_id'
00070 [L720] TSETS    A=11 B=10 C=13 D=2573 'char'
00071 [L720] CALL     A=8 B=1 C=3 D=259 
00072 [L721] JMP      A=7 B=128 C=50 D=32818 target=123
00073 [L722] TGETS    A=7 B=6 C=3 D=1539 'object_type'
00074 [L722] UGET     A=8 B=0 C=1 D=1 o_t
00075 [L722] TGETS    A=8 B=8 C=17 D=2065 'item'
00076 [L722] ISNEV    A=7 B=0 C=8 D=8 
00077 [L722] JMP      A=7 B=128 C=45 D=32813 target=123
00078 [L723] KPRI     A=7 B=0 C=1 D=1 
00079 [L724] GGET     A=8 B=0 C=0 D=0 'd_ms'
00080 [L724] TGETS    A=8 B=8 C=18 D=2066 'd_packageUI'
00081 [L724] TGETS    A=8 B=8 C=19 D=2067 'g_reorgItemsInfo'
00082 [L724] UGET     A=9 B=0 C=1 D=1 o_t
00083 [L724] TGETS    A=9 B=9 C=17 D=2321 'item'
00084 [L724] TGETV    A=8 B=8 C=9 D=2057 
00085 [L724] UGET     A=9 B=0 C=3 D=3 m_t
00086 [L724] TGETS    A=9 B=9 C=20 D=2324 'adaptive_spirit'
00087 [L724] TGETV    A=8 B=8 C=9 D=2057 
00088 [L724] IST      A=0 B=0 C=8 D=8 
00089 [L724] JMP      A=9 B=128 C=1 D=32769 target=91
00090 [L724] TNEW     A=8 B=0 C=0 D=0 
00091 [L725] UGET     A=9 B=0 C=0 D=0 pairs
00092 [L725] MOV      A=10 B=0 C=8 D=8 
00093 [L725] CALL     A=9 B=4 C=2 D=1026 
00094 [L725] ISNEXT   A=12 B=128 C=13 D=32781 target=108
00095 [L726] TGETS    A=14 B=13 C=16 D=3344 'type_id'
00096 [L726] TGETS    A=15 B=6 C=8 D=1544 'attach_type'
00097 [L726] ISNEV    A=14 B=0 C=15 D=15 
00098 [L726] JMP      A=14 B=128 C=9 D=32777 target=108
00099 [L727] UGET     A=14 B=0 C=2 D=2 table
00100 [L727] TGETS    A=14 B=14 C=9 D=3593 'insert'
00101 [L727] MOV      A=15 B=0 C=1 D=1 
00102 [L727] TDUP     A=16 B=0 C=21 D=21 {'kind': 'table', 'value': {'isItem': True, 'hasGot': True}}
00103 [L727] TGETS    A=17 B=6 C=11 D=1547 'attach_count'
00104 [L727] TSETS    A=17 B=16 C=12 D=4108 'ratio'
00105 [L727] TSETS    A=13 B=16 C=17 D=4113 'item'
00106 [L727] CALL     A=14 B=1 C=3 D=259 
00107 [L728] KPRI     A=7 B=0 C=2 D=2 
00108 [L725] ITERN    A=12 B=3 C=3 D=771 
00109 [L725] ITERL    A=12 B=127 C=241 D=32753 target=95
00110 [L731] IST      A=0 B=0 C=7 D=7 
00111 [L731] JMP      A=9 B=128 C=11 D=32779 target=123
00112 [L732] UGET     A=9 B=0 C=2 D=2 table
00113 [L732] TGETS    A=9 B=9 C=9 D=2313 'insert'
00114 [L732] MOV      A=10 B=0 C=1 D=1 
00115 [L732] TDUP     A=11 B=0 C=22 D=22 {'kind': 'table', 'value': {'isItem': True, 'hasGot': False}}
00116 [L732] TGETS    A=12 B=6 C=11 D=1547 'attach_count'
00117 [L732] TSETS    A=12 B=11 C=12 D=2828 'ratio'
00118 [L732] TDUP     A=12 B=0 C=23 D=23 {'kind': 'table', 'value': {}}
00119 [L732] TGETS    A=13 B=6 C=8 D=1544 'attach_type'
00120 [L732] TSETS    A=13 B=12 C=16 D=3088 'type_id'
00121 [L732] TSETS    A=12 B=11 C=17 D=2833 'item'
00122 [L732] CALL     A=9 B=1 C=3 D=259 
00123 [L710] ITERN    A=5 B=3 C=3 D=771 
00124 [L710] ITERL    A=5 B=127 C=160 D=32672 target=29
00125 [L736] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto38 offset=0x53ca source_lines=785-796 params=2
UPVALUES ['convertCount', 'layer', 'w1', 'h1', 'tostring']
00001 [L786] USETV    A=0 B=0 C=0 D=0 convertCount
00002 [L787] UGET     A=2 B=0 C=1 D=1 layer
00003 [L787] MOV      A=3 B=0 C=2 D=2 
00004 [L787] TGETS    A=2 B=2 C=0 D=512 'removeChildByTag'
00005 [L787] KSHORT   A=4 B=0 C=3 D=3 3
00006 [L787] KPRI     A=5 B=0 C=2 D=2 
00007 [L787] CALL     A=2 B=1 C=4 D=260 
00008 [L788] KSHORT   A=2 B=0 C=1 D=1 1
00009 [L789] GGET     A=3 B=0 C=1 D=1 'g_boxUI'
00010 [L789] TGETS    A=3 B=3 C=2 D=770 'lastTouchIndex'
00011 [L789] ISF      A=0 B=0 C=3 D=3 
00012 [L789] JMP      A=4 B=128 C=9 D=32777 target=22
00013 [L790] GGET     A=3 B=0 C=1 D=1 'g_boxUI'
00014 [L790] TGETS    A=3 B=3 C=3 D=771 'data_list'
00015 [L790] GGET     A=4 B=0 C=1 D=1 'g_boxUI'
00016 [L790] TGETS    A=4 B=4 C=2 D=1026 'lastTouchIndex'
00017 [L790] TGETV    A=3 B=3 C=4 D=772 
00018 [L791] TGETS    A=4 B=3 C=4 D=772 'ratio'
00019 [L791] ISF      A=0 B=0 C=4 D=4 
00020 [L791] JMP      A=5 B=128 C=1 D=32769 target=22
00021 [L792] TGETS    A=2 B=3 C=4 D=772 'ratio'
00022 [L795] UGET     A=3 B=0 C=1 D=1 layer
00023 [L795] MOV      A=4 B=0 C=3 D=3 
00024 [L795] TGETS    A=3 B=3 C=5 D=773 'addChild'
00025 [L795] GGET     A=5 B=0 C=6 D=6 'd_ms'
00026 [L795] TGETS    A=5 B=5 C=7 D=1287 'd_u'
00027 [L795] TGETS    A=5 B=5 C=8 D=1288 'createByStyle'
00028 [L795] TDUP     A=6 B=0 C=9 D=9 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 26}}
00029 [L795] UGET     A=7 B=0 C=2 D=2 w1
00030 [L795] MULNV    A=7 B=7 C=0 D=1792 
00031 [L795] ADDNV    A=7 B=7 C=1 D=1793 
00032 [L795] TSETS    A=7 B=6 C=10 D=1546 'x'
00033 [L795] UGET     A=7 B=0 C=3 D=3 h1
00034 [L795] MULNV    A=7 B=7 C=2 D=1794 
00035 [L795] SUBNV    A=7 B=7 C=1 D=1793 
00036 [L795] TSETS    A=7 B=6 C=11 D=1547 'y'
00037 [L795] TDUP     A=7 B=0 C=12 D=12 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00038 [L795] TSETS    A=7 B=6 C=13 D=1549 'anchor'
00039 [L795] UGET     A=7 B=0 C=4 D=4 tostring
00040 [L795] MULVV    A=8 B=0 C=2 D=2 
00041 [L795] CALL     A=7 B=2 C=2 D=514 
00042 [L795] TSETS    A=7 B=6 C=14 D=1550 'string'
00043 [L795] GGET     A=7 B=0 C=15 D=15 'g_Color'
00044 [L795] TGETS    A=7 B=7 C=16 D=1808 'gray'
00045 [L795] TSETS    A=7 B=6 C=17 D=1553 'color'
00046 [L795] CALL     A=5 B=2 C=2 D=514 
00047 [L795] KSHORT   A=6 B=0 C=1 D=1 1
00048 [L795] KSHORT   A=7 B=0 C=3 D=3 3
00049 [L795] CALL     A=3 B=1 C=5 D=261 
00050 [L796] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto39 offset=0x55f3 source_lines=804-810 params=1
UPVALUES ['cortTableView', 'onNumChanged', 'convertCount']
00001 [L805] GGET     A=1 B=0 C=0 D=0 'g_boxUI'
00002 [L805] TGETS    A=1 B=1 C=1 D=257 'lastTouchIndex'
00003 [L805] ISEQV    A=0 B=0 C=1 D=1 
00004 [L805] JMP      A=1 B=128 C=13 D=32781 target=18
00005 [L805] UGET     A=1 B=0 C=0 D=0 cortTableView
00006 [L805] ISF      A=0 B=0 C=1 D=1 
00007 [L805] JMP      A=2 B=128 C=10 D=32778 target=18
00008 [L806] GGET     A=1 B=0 C=0 D=0 'g_boxUI'
00009 [L806] TSETS    A=0 B=1 C=1 D=257 'lastTouchIndex'
00010 [L807] UGET     A=1 B=0 C=0 D=0 cortTableView
00011 [L807] MOV      A=2 B=0 C=1 D=1 
00012 [L807] TGETS    A=1 B=1 C=2 D=258 'reloadData'
00013 [L807] CALL     A=1 B=1 C=2 D=258 
00014 [L808] UGET     A=1 B=0 C=1 D=1 onNumChanged
00015 [L808] UGET     A=2 B=0 C=2 D=2 convertCount
00016 [L808] KSHORT   A=3 B=0 C=0 D=0 0
00017 [L808] CALL     A=1 B=1 C=3 D=259 
00018 [L810] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto40 offset=0x56b3 source_lines=824-828 params=0
UPVALUES ['layer']
00001 [L825] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L825] TGETS    A=0 B=0 C=1 D=1 'd_u'
00003 [L825] TGETS    A=0 B=0 C=2 D=2 'remove'
00004 [L825] UGET     A=1 B=0 C=0 D=0 layer
00005 [L825] CALL     A=0 B=1 C=2 D=258 
00006 [L826] TNEW     A=0 B=0 C=0 D=0 
00007 [L826] GSET     A=0 B=0 C=3 D=3 'g_boxUI'
00008 [L827] GGET     A=0 B=0 C=0 D=0 'd_ms'
00009 [L827] TGETS    A=0 B=0 C=4 D=4 'd_packageUI'
00010 [L827] TGETS    A=0 B=0 C=5 D=5 'updateItemCellInfo'
00011 [L827] GGET     A=1 B=0 C=3 D=3 'g_boxUI'
00012 [L827] TGETS    A=1 B=1 C=6 D=262 'usetype'
00013 [L827] CALL     A=0 B=1 C=2 D=258 
00014 [L828] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto41 offset=0x574e source_lines=829-858 params=0
UPVALUES ['printf', 'gethz', 'o_t', 'convertCount']
00001 [L830] GGET     A=0 B=0 C=0 D=0 'g_boxUI'
00002 [L830] TGETS    A=0 B=0 C=1 D=1 'lastTouchIndex'
00003 [L830] IST      A=0 B=0 C=0 D=0 
00004 [L830] JMP      A=0 B=128 C=6 D=32774 target=11
00005 [L831] UGET     A=0 B=0 C=0 D=0 printf
00006 [L831] UGET     A=1 B=0 C=1 D=1 gethz
00007 [L831] KSTR     A=2 B=0 C=2 D=2 'kick22'
00008 [L831] CALL     A=1 B=0 C=2 D=2 
00009 [L831] CALLM    A=0 B=1 C=0 D=256 
00010 [L831] JMP      A=0 B=128 C=66 D=32834 target=77
00011 [L833] GGET     A=0 B=0 C=3 D=3 'd_ms'
00012 [L833] TGETS    A=0 B=0 C=4 D=4 'd_data'
00013 [L833] TGETS    A=0 B=0 C=5 D=5 'getItemCountByType'
00014 [L833] UGET     A=1 B=0 C=2 D=2 o_t
00015 [L833] TGETS    A=1 B=1 C=6 D=262 'item'
00016 [L833] GGET     A=2 B=0 C=0 D=0 'g_boxUI'
00017 [L833] TGETS    A=2 B=2 C=7 D=519 'usetype'
00018 [L833] CALL     A=0 B=2 C=3 D=515 
00019 [L834] UGET     A=1 B=0 C=3 D=3 convertCount
00020 [L834] ISGE     A=0 B=0 C=1 D=1 
00021 [L834] JMP      A=1 B=128 C=6 D=32774 target=28
00022 [L835] UGET     A=1 B=0 C=0 D=0 printf
00023 [L835] UGET     A=2 B=0 C=1 D=1 gethz
00024 [L835] KSTR     A=3 B=0 C=8 D=8 'noCount'
00025 [L835] CALL     A=2 B=0 C=2 D=2 
00026 [L835] CALLM    A=1 B=1 C=0 D=256 
00027 [L835] JMP      A=1 B=128 C=49 D=32817 target=77
00028 [L837] GGET     A=1 B=0 C=0 D=0 'g_boxUI'
00029 [L837] TGETS    A=1 B=1 C=9 D=265 'data_list'
00030 [L837] GGET     A=2 B=0 C=0 D=0 'g_boxUI'
00031 [L837] TGETS    A=2 B=2 C=1 D=513 'lastTouchIndex'
00032 [L837] TGETV    A=1 B=1 C=2 D=258 
00033 [L838] KNIL     A=2 B=0 C=3 D=3 
00034 [L839] TGETS    A=4 B=1 C=10 D=266 'isItem'
00035 [L839] ISF      A=0 B=0 C=4 D=4 
00036 [L839] JMP      A=5 B=128 C=5 D=32773 target=42
00037 [L840] UGET     A=4 B=0 C=2 D=2 o_t
00038 [L840] TGETS    A=2 B=4 C=6 D=1030 'item'
00039 [L841] TGETS    A=4 B=1 C=6 D=262 'item'
00040 [L841] TGETS    A=3 B=4 C=11 D=1035 'type_id'
00041 [L841] JMP      A=4 B=128 C=11 D=32779 target=53
00042 [L843] UGET     A=4 B=0 C=2 D=2 o_t
00043 [L843] TGETS    A=2 B=4 C=12 D=1036 'spirit'
00044 [L844] TGETS    A=4 B=1 C=13 D=269 'hasGot'
00045 [L844] ISF      A=0 B=0 C=4 D=4 
00046 [L844] JMP      A=5 B=128 C=4 D=32772 target=51
00047 [L844] TGETS    A=4 B=1 C=14 D=270 'char'
00048 [L844] TGETS    A=4 B=4 C=15 D=1039 'type'
00049 [L844] ISTC     A=3 B=0 C=4 D=4 
00050 [L844] JMP      A=5 B=128 C=2 D=32770 target=53
00051 [L844] TGETS    A=4 B=1 C=14 D=270 'char'
00052 [L844] TGETS    A=3 B=4 C=11 D=1035 'type_id'
00053 [L846] TDUP     A=4 B=0 C=16 D=16 {'kind': 'table', 'value': {}}
00054 [L848] GGET     A=5 B=0 C=0 D=0 'g_boxUI'
00055 [L848] TGETS    A=5 B=5 C=7 D=1287 'usetype'
00056 [L848] TSETS    A=5 B=4 C=17 D=1041 'item_type'
00057 [L849] GGET     A=5 B=0 C=3 D=3 'd_ms'
00058 [L849] TGETS    A=5 B=5 C=4 D=1284 'd_data'
00059 [L849] TGETS    A=5 B=5 C=18 D=1298 'getPropsID'
00060 [L849] GGET     A=6 B=0 C=0 D=0 'g_boxUI'
00061 [L849] TGETS    A=6 B=6 C=7 D=1543 'usetype'
00062 [L849] CALL     A=5 B=2 C=2 D=514 
00063 [L849] TSETS    A=5 B=4 C=19 D=1043 'item_id'
00064 [L850] TSETS    A=2 B=4 C=20 D=1044 'des_type'
00065 [L851] TSETS    A=3 B=4 C=21 D=1045 'des_id'
00066 [L852] UGET     A=5 B=0 C=3 D=3 convertCount
00067 [L852] TSETS    A=5 B=4 C=22 D=1046 'item_count'
00068 [L854] GGET     A=5 B=0 C=3 D=3 'd_ms'
00069 [L854] TGETS    A=5 B=5 C=23 D=1303 'd_u'
00070 [L854] TGETS    A=5 B=5 C=24 D=1304 'main_server_send_msg'
00071 [L854] GGET     A=6 B=0 C=3 D=3 'd_ms'
00072 [L854] TGETS    A=6 B=6 C=25 D=1561 'd_msg_def'
00073 [L854] TGETS    A=6 B=6 C=26 D=1562 'gscl_msg_id'
00074 [L854] TGETS    A=6 B=6 C=27 D=1563 'msg_use_item'
00075 [L854] MOV      A=7 B=0 C=4 D=4 
00076 [L854] CALL     A=5 B=1 C=3 D=259 
00077 [L858] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto42 offset=0x5a35 source_lines=739-869 params=3
UPVALUES ['CCLayer', 'o_t', 'tostring', 'scrSize', 'CCRectMake', 'printf', 'gethz']
00001 [L740] ISF      A=0 B=0 C=2 D=2 
00002 [L740] JMP      A=3 B=128 C=6 D=32774 target=9
00003 [L740] GGET     A=3 B=0 C=0 D=0 'g_littlerulaibag'
00004 [L740] ISEQV    A=2 B=0 C=3 D=3 
00005 [L740] JMP      A=3 B=128 C=4 D=32772 target=10
00006 [L740] GGET     A=3 B=0 C=1 D=1 'g_bigrulaibag'
00007 [L740] ISEQV    A=2 B=0 C=3 D=3 
00008 [L740] JMP      A=3 B=128 C=1 D=32769 target=10
00009 [L741] UCLO     A=0 B=129 C=65 D=33089 target=331
00010 [L743] ISEQN    A=2 B=0 C=0 D=0 1367
00011 [L743] JMP      A=3 B=128 C=2 D=32770 target=14
00012 [L743] ISNEN    A=2 B=0 C=1 D=1 1368
00013 [L743] JMP      A=3 B=128 C=3 D=32771 target=17
00014 [L744] KPRI     A=3 B=0 C=2 D=2 
00015 [L744] GSET     A=3 B=0 C=2 D=2 'g_showBoxUseLayer_maxnum'
00016 [L744] JMP      A=3 B=128 C=2 D=32770 target=19
00017 [L746] KPRI     A=3 B=0 C=1 D=1 
00018 [L746] GSET     A=3 B=0 C=2 D=2 'g_showBoxUseLayer_maxnum'
00019 [L748] GGET     A=3 B=0 C=3 D=3 'g_boxUI'
00020 [L748] TSETS    A=2 B=3 C=4 D=772 'usetype'
00021 [L749] UGET     A=3 B=0 C=0 D=0 CCLayer
00022 [L749] MOV      A=4 B=0 C=3 D=3 
00023 [L749] TGETS    A=3 B=3 C=5 D=773 'create'
00024 [L749] CALL     A=3 B=2 C=2 D=514 
00025 [L750] GGET     A=4 B=0 C=6 D=6 'd_ms'
00026 [L750] TGETS    A=4 B=4 C=7 D=1031 'd_u'
00027 [L750] TGETS    A=4 B=4 C=8 D=1032 'createSwallowTouchLayer'
00028 [L750] MOV      A=5 B=0 C=3 D=3 
00029 [L750] CALL     A=4 B=1 C=2 D=258 
00030 [L752] GGET     A=4 B=0 C=6 D=6 'd_ms'
00031 [L752] TGETS    A=4 B=4 C=7 D=1031 'd_u'
00032 [L752] TGETS    A=4 B=4 C=9 D=1033 'createByStyles'
00033 [L752] TDUP     A=5 B=0 C=10 D=10 {'kind': 'table', 'value': {'pic': 'v2/kickUI/bkg4.png', 'x': 0.5, 'y': 0.5}}
00034 [L752] CALL     A=4 B=2 C=2 D=514 
00035 [L753] MOV      A=6 B=0 C=3 D=3 
00036 [L753] TGETS    A=5 B=3 C=11 D=779 'addChild'
00037 [L753] MOV      A=7 B=0 C=4 D=4 
00038 [L753] CALL     A=5 B=1 C=3 D=259 
00039 [L754] GGET     A=5 B=0 C=6 D=6 'd_ms'
00040 [L754] TGETS    A=5 B=5 C=7 D=1287 'd_u'
00041 [L754] TGETS    A=5 B=5 C=12 D=1292 'getRealScale'
00042 [L754] MOV      A=6 B=0 C=4 D=4 
00043 [L754] CALL     A=5 B=3 C=2 D=770 
00044 [L755] GGET     A=7 B=0 C=3 D=3 'g_boxUI'
00045 [L755] GGET     A=8 B=0 C=3 D=3 'g_boxUI'
00046 [L755] MOV      A=9 B=0 C=5 D=5 
00047 [L755] TSETS    A=6 B=8 C=14 D=2062 'h1'
00048 [L755] TSETS    A=9 B=7 C=13 D=1805 'w1'
00049 [L757] GGET     A=7 B=0 C=6 D=6 'd_ms'
00050 [L757] TGETS    A=7 B=7 C=7 D=1799 'd_u'
00051 [L757] TGETS    A=7 B=7 C=9 D=1801 'createByStyles'
00052 [L757] TDUP     A=8 B=0 C=15 D=15 {'kind': 'table', 'value': {'pic': 'v2/kickUI/title4.png', 'x': 0.5}}
00053 [L757] MULNV    A=9 B=6 C=2 D=1538 
00054 [L757] ADDNV    A=9 B=9 C=3 D=2307 
00055 [L757] TSETS    A=9 B=8 C=16 D=2064 'y'
00056 [L757] CALL     A=7 B=2 C=2 D=514 
00057 [L758] MOV      A=9 B=0 C=3 D=3 
00058 [L758] TGETS    A=8 B=3 C=11 D=779 'addChild'
00059 [L758] MOV      A=10 B=0 C=7 D=7 
00060 [L758] KSHORT   A=11 B=0 C=1 D=1 1
00061 [L758] CALL     A=8 B=1 C=4 D=260 
00062 [L761] KSTR     A=8 B=0 C=17 D=17 ''
00063 [L762] GGET     A=9 B=0 C=0 D=0 'g_littlerulaibag'
00064 [L762] ISNEV    A=2 B=0 C=9 D=9 
00065 [L762] JMP      A=9 B=128 C=7 D=32775 target=73
00066 [L763] GGET     A=9 B=0 C=6 D=6 'd_ms'
00067 [L763] TGETS    A=9 B=9 C=18 D=2322 'd_hz'
00068 [L763] TGETS    A=9 B=9 C=19 D=2323 'gethz'
00069 [L763] KSTR     A=10 B=0 C=20 D=20 'turntable_info_1'
00070 [L763] CALL     A=9 B=2 C=2 D=514 
00071 [L763] MOV      A=8 B=0 C=9 D=9 
00072 [L763] JMP      A=9 B=128 C=9 D=32777 target=82
00073 [L764] GGET     A=9 B=0 C=1 D=1 'g_bigrulaibag'
00074 [L764] ISNEV    A=2 B=0 C=9 D=9 
00075 [L764] JMP      A=9 B=128 C=6 D=32774 target=82
00076 [L765] GGET     A=9 B=0 C=6 D=6 'd_ms'
00077 [L765] TGETS    A=9 B=9 C=18 D=2322 'd_hz'
00078 [L765] TGETS    A=9 B=9 C=19 D=2323 'gethz'
00079 [L765] KSTR     A=10 B=0 C=21 D=21 'turntable_info_2'
00080 [L765] CALL     A=9 B=2 C=2 D=514 
00081 [L765] MOV      A=8 B=0 C=9 D=9 
00082 [L768] GGET     A=9 B=0 C=6 D=6 'd_ms'
00083 [L768] TGETS    A=9 B=9 C=22 D=2326 'd_data'
00084 [L768] TGETS    A=9 B=9 C=23 D=2327 'getItemCountByType'
00085 [L768] UGET     A=10 B=0 C=1 D=1 o_t
00086 [L768] TGETS    A=10 B=10 C=24 D=2584 'item'
00087 [L768] MOV      A=11 B=0 C=2 D=2 
00088 [L768] CALL     A=9 B=2 C=3 D=515 
00089 [L769] MOV      A=11 B=0 C=3 D=3 
00090 [L769] TGETS    A=10 B=3 C=11 D=779 'addChild'
00091 [L769] GGET     A=12 B=0 C=6 D=6 'd_ms'
00092 [L769] TGETS    A=12 B=12 C=7 D=3079 'd_u'
00093 [L769] TGETS    A=12 B=12 C=25 D=3097 'createByStyle'
00094 [L769] TDUP     A=13 B=0 C=26 D=26 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 26}}
00095 [L769] MULNV    A=14 B=5 C=4 D=1284 
00096 [L769] SUBNV    A=14 B=14 C=3 D=3587 
00097 [L769] TSETS    A=14 B=13 C=27 D=3355 'x'
00098 [L769] MULNV    A=14 B=6 C=5 D=1541 
00099 [L769] SUBNV    A=14 B=14 C=3 D=3587 
00100 [L769] TSETS    A=14 B=13 C=16 D=3344 'y'
00101 [L769] TDUP     A=14 B=0 C=28 D=28 {'kind': 'table', 'value': {1: 1, 2: 0.5}}
00102 [L769] TSETS    A=14 B=13 C=29 D=3357 'anchor'
00103 [L769] GGET     A=14 B=0 C=6 D=6 'd_ms'
00104 [L769] TGETS    A=14 B=14 C=18 D=3602 'd_hz'
00105 [L769] TGETS    A=14 B=14 C=19 D=3603 'gethz'
00106 [L769] KSTR     A=15 B=0 C=30 D=30 'kick15'
00107 [L769] CALL     A=14 B=2 C=2 D=514 
00108 [L769] KSTR     A=15 B=0 C=31 D=31 ': '
00109 [L769] CAT      A=14 B=14 C=15 D=3599 
00110 [L769] TSETS    A=14 B=13 C=32 D=3360 'string'
00111 [L769] GGET     A=14 B=0 C=33 D=33 'g_Color'
00112 [L769] TGETS    A=14 B=14 C=34 D=3618 'gray'
00113 [L769] TSETS    A=14 B=13 C=35 D=3363 'color'
00114 [L769] CALL     A=12 B=0 C=2 D=2 
00115 [L769] CALLM    A=10 B=1 C=1 D=257 
00116 [L770] MOV      A=11 B=0 C=3 D=3 
00117 [L770] TGETS    A=10 B=3 C=11 D=779 'addChild'
00118 [L770] GGET     A=12 B=0 C=6 D=6 'd_ms'
00119 [L770] TGETS    A=12 B=12 C=7 D=3079 'd_u'
00120 [L770] TGETS    A=12 B=12 C=25 D=3097 'createByStyle'
00121 [L770] TDUP     A=13 B=0 C=36 D=36 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 26}}
00122 [L770] MULNV    A=14 B=5 C=6 D=1286 
00123 [L770] ADDNV    A=14 B=14 C=3 D=3587 
00124 [L770] TSETS    A=14 B=13 C=27 D=3355 'x'
00125 [L770] MULNV    A=14 B=6 C=5 D=1541 
00126 [L770] SUBNV    A=14 B=14 C=3 D=3587 
00127 [L770] TSETS    A=14 B=13 C=16 D=3344 'y'
00128 [L770] TDUP     A=14 B=0 C=37 D=37 {'kind': 'table', 'value': {1: 1, 2: 0.5}}
00129 [L770] TSETS    A=14 B=13 C=29 D=3357 'anchor'
00130 [L770] MOV      A=14 B=0 C=8 D=8 
00131 [L770] KSTR     A=15 B=0 C=31 D=31 ': '
00132 [L770] CAT      A=14 B=14 C=15 D=3599 
00133 [L770] TSETS    A=14 B=13 C=32 D=3360 'string'
00134 [L770] GGET     A=14 B=0 C=33 D=33 'g_Color'
00135 [L770] TGETS    A=14 B=14 C=34 D=3618 'gray'
00136 [L770] TSETS    A=14 B=13 C=35 D=3363 'color'
00137 [L770] CALL     A=12 B=0 C=2 D=2 
00138 [L770] CALLM    A=10 B=1 C=1 D=257 
00139 [L771] MOV      A=11 B=0 C=3 D=3 
00140 [L771] TGETS    A=10 B=3 C=11 D=779 'addChild'
00141 [L771] GGET     A=12 B=0 C=6 D=6 'd_ms'
00142 [L771] TGETS    A=12 B=12 C=7 D=3079 'd_u'
00143 [L771] TGETS    A=12 B=12 C=25 D=3097 'createByStyle'
00144 [L771] TDUP     A=13 B=0 C=38 D=38 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 26}}
00145 [L771] MULNV    A=14 B=5 C=6 D=1286 
00146 [L771] ADDNV    A=14 B=14 C=3 D=3587 
00147 [L771] TSETS    A=14 B=13 C=27 D=3355 'x'
00148 [L771] MULNV    A=14 B=6 C=5 D=1541 
00149 [L771] SUBNV    A=14 B=14 C=3 D=3587 
00150 [L771] TSETS    A=14 B=13 C=16 D=3344 'y'
00151 [L771] TDUP     A=14 B=0 C=39 D=39 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00152 [L771] TSETS    A=14 B=13 C=29 D=3357 'anchor'
00153 [L771] UGET     A=14 B=0 C=2 D=2 tostring
00154 [L771] MOV      A=15 B=0 C=9 D=9 
00155 [L771] CALL     A=14 B=2 C=2 D=514 
00156 [L771] TSETS    A=14 B=13 C=32 D=3360 'string'
00157 [L771] GGET     A=14 B=0 C=33 D=33 'g_Color'
00158 [L771] TGETS    A=14 B=14 C=34 D=3618 'gray'
00159 [L771] TSETS    A=14 B=13 C=35 D=3363 'color'
00160 [L771] CALL     A=12 B=0 C=2 D=2 
00161 [L771] CALLM    A=10 B=1 C=1 D=257 
00162 [L772] MOV      A=11 B=0 C=3 D=3 
00163 [L772] TGETS    A=10 B=3 C=11 D=779 'addChild'
00164 [L772] GGET     A=12 B=0 C=6 D=6 'd_ms'
00165 [L772] TGETS    A=12 B=12 C=7 D=3079 'd_u'
00166 [L772] TGETS    A=12 B=12 C=25 D=3097 'createByStyle'
00167 [L772] TDUP     A=13 B=0 C=40 D=40 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 26}}
00168 [L772] MULNV    A=14 B=5 C=6 D=1286 
00169 [L772] ADDNV    A=14 B=14 C=3 D=3587 
00170 [L772] TSETS    A=14 B=13 C=27 D=3355 'x'
00171 [L772] MULNV    A=14 B=6 C=7 D=1543 
00172 [L772] SUBNV    A=14 B=14 C=3 D=3587 
00173 [L772] TSETS    A=14 B=13 C=16 D=3344 'y'
00174 [L772] TDUP     A=14 B=0 C=41 D=41 {'kind': 'table', 'value': {1: 1, 2: 0.5}}
00175 [L772] TSETS    A=14 B=13 C=29 D=3357 'anchor'
00176 [L772] GGET     A=14 B=0 C=6 D=6 'd_ms'
00177 [L772] TGETS    A=14 B=14 C=18 D=3602 'd_hz'
00178 [L772] TGETS    A=14 B=14 C=19 D=3603 'gethz'
00179 [L772] KSTR     A=15 B=0 C=42 D=42 'kick17'
00180 [L772] CALL     A=14 B=2 C=2 D=514 
00181 [L772] KSTR     A=15 B=0 C=31 D=31 ': '
00182 [L772] CAT      A=14 B=14 C=15 D=3599 
00183 [L772] TSETS    A=14 B=13 C=32 D=3360 'string'
00184 [L772] GGET     A=14 B=0 C=33 D=33 'g_Color'
00185 [L772] TGETS    A=14 B=14 C=34 D=3618 'gray'
00186 [L772] TSETS    A=14 B=13 C=35 D=3363 'color'
00187 [L772] CALL     A=12 B=0 C=2 D=2 
00188 [L772] CALLM    A=10 B=1 C=1 D=257 
00189 [L774] KSHORT   A=10 B=0 C=1 D=1 1
00190 [L774] ISGE     A=9 B=0 C=10 D=10 
00191 [L774] JMP      A=10 B=128 C=2 D=32770 target=194
00192 [L775] KSHORT   A=9 B=0 C=1 D=1 1
00193 [L775] JMP      A=10 B=128 C=4 D=32772 target=198
00194 [L776] KSHORT   A=10 B=0 C=99 D=99 99
00195 [L776] ISGE     A=10 B=0 C=9 D=9 
00196 [L776] JMP      A=10 B=128 C=1 D=32769 target=198
00197 [L777] KSHORT   A=9 B=0 C=99 D=99 99
00198 [L779] GGET     A=10 B=0 C=2 D=2 'g_showBoxUseLayer_maxnum'
00199 [L779] ISF      A=0 B=0 C=10 D=10 
00200 [L779] JMP      A=11 B=128 C=1 D=32769 target=202
00201 [L780] KSHORT   A=9 B=0 C=15 D=15 15
00202 [L782] KSHORT   A=10 B=0 C=1 D=1 1
00203 [L783] GGET     A=11 B=0 C=43 D=43 'getBoxTransConfig'
00204 [L783] MOV      A=12 B=0 C=2 D=2 
00205 [L783] CALL     A=11 B=2 C=2 D=514 
00206 [L784] GGET     A=12 B=0 C=3 D=3 'g_boxUI'
00207 [L784] TSETS    A=11 B=12 C=44 D=3116 'data_list'
00208 [L796] FNEW     A=12 B=0 C=45 D=45 {'kind': 'proto', 'id': 38}
00209 [L798] GGET     A=13 B=0 C=6 D=6 'd_ms'
00210 [L798] TGETS    A=13 B=13 C=46 D=3374 'd_guildPartyUI'
00211 [L798] TGETS    A=13 B=13 C=47 D=3375 'getCalc'
00212 [L798] MOV      A=14 B=0 C=12 D=12 
00213 [L798] MOV      A=15 B=0 C=9 D=9 
00214 [L798] CALL     A=13 B=2 C=3 D=515 
00215 [L799] GGET     A=14 B=0 C=6 D=6 'd_ms'
00216 [L799] TGETS    A=14 B=14 C=7 D=3591 'd_u'
00217 [L799] TGETS    A=14 B=14 C=48 D=3632 'setStyles'
00218 [L799] MOV      A=15 B=0 C=13 D=13 
00219 [L799] TDUP     A=16 B=0 C=49 D=49 {'kind': 'table', 'value': {'x': 0.5}}
00220 [L799] MULNV    A=17 B=6 C=8 D=1544 
00221 [L799] SUBNV    A=17 B=17 C=3 D=4355 
00222 [L799] TSETS    A=17 B=16 C=16 D=4112 'y'
00223 [L799] CALL     A=14 B=1 C=3 D=259 
00224 [L800] MOV      A=15 B=0 C=3 D=3 
00225 [L800] TGETS    A=14 B=3 C=11 D=779 'addChild'
00226 [L800] MOV      A=16 B=0 C=13 D=13 
00227 [L800] KSHORT   A=17 B=0 C=1 D=1 1
00228 [L800] CALL     A=14 B=1 C=4 D=260 
00229 [L801] MOV      A=14 B=0 C=12 D=12 
00230 [L801] MOV      A=15 B=0 C=10 D=10 
00231 [L801] KSHORT   A=16 B=0 C=0 D=0 0
00232 [L801] CALL     A=14 B=1 C=3 D=259 
00233 [L803] KPRI     A=14 B=0 C=0 D=0 
00234 [L810] FNEW     A=15 B=0 C=50 D=50 {'kind': 'proto', 'id': 39}
00235 [L812] TDUP     A=16 B=0 C=52 D=52 {'kind': 'table', 'value': {}}
00236 [L812] MULNV    A=17 B=5 C=9 D=1289 
00237 [L812] SUBNV    A=17 B=17 C=3 D=4355 
00238 [L812] UGET     A=18 B=0 C=3 D=3 scrSize
00239 [L812] TGETS    A=18 B=18 C=51 D=4659 'width'
00240 [L812] MULVV    A=17 B=17 C=18 D=4370 
00241 [L812] TSETS    A=17 B=16 C=27 D=4123 'x'
00242 [L812] MULNV    A=17 B=6 C=10 D=1546 
00243 [L812] SUBNV    A=17 B=17 C=3 D=4355 
00244 [L812] UGET     A=18 B=0 C=3 D=3 scrSize
00245 [L812] TGETS    A=18 B=18 C=53 D=4661 'height'
00246 [L812] MULVV    A=17 B=17 C=18 D=4370 
00247 [L812] TSETS    A=17 B=16 C=16 D=4112 'y'
00248 [L812] MULNV    A=17 B=5 C=11 D=1291 
00249 [L812] UGET     A=18 B=0 C=3 D=3 scrSize
00250 [L812] TGETS    A=18 B=18 C=51 D=4659 'width'
00251 [L812] MULVV    A=17 B=17 C=18 D=4370 
00252 [L812] TSETS    A=17 B=16 C=51 D=4147 'width'
00253 [L812] MULNV    A=17 B=6 C=12 D=1548 
00254 [L812] UGET     A=18 B=0 C=3 D=3 scrSize
00255 [L812] TGETS    A=18 B=18 C=53 D=4661 'height'
00256 [L812] MULVV    A=17 B=17 C=18 D=4370 
00257 [L812] TSETS    A=17 B=16 C=53 D=4149 'height'
00258 [L813] TDUP     A=17 B=0 C=54 D=54 {'kind': 'table', 'value': {}}
00259 [L813] TGETS    A=18 B=16 C=51 D=4147 'width'
00260 [L813] TSETS    A=18 B=17 C=51 D=4403 'width'
00261 [L813] TGETS    A=18 B=16 C=53 D=4149 'height'
00262 [L813] MULNV    A=18 B=18 C=13 D=4621 
00263 [L813] TSETS    A=18 B=17 C=53 D=4405 'height'
00264 [L814] UGET     A=18 B=0 C=4 D=4 CCRectMake
00265 [L814] TGETS    A=19 B=16 C=27 D=4123 'x'
00266 [L814] TGETS    A=20 B=16 C=16 D=4112 'y'
00267 [L814] TGETS    A=21 B=16 C=51 D=4147 'width'
00268 [L814] TGETS    A=22 B=16 C=53 D=4149 'height'
00269 [L814] CALL     A=18 B=2 C=5 D=517 
00270 [L816] GGET     A=19 B=0 C=6 D=6 'd_ms'
00271 [L816] TGETS    A=19 B=19 C=55 D=4919 'd_tableView'
00272 [L816] TGETS    A=19 B=19 C=56 D=4920 'tableView'
00273 [L816] MOV      A=20 B=0 C=3 D=3 
00274 [L816] MOV      A=21 B=0 C=16 D=16 
00275 [L816] CALL     A=19 B=2 C=3 D=515 
00276 [L816] MOV      A=14 B=0 C=19 D=19 
00277 [L817] GGET     A=19 B=0 C=57 D=57 'getCortDataSource'
00278 [L817] MOV      A=20 B=0 C=11 D=11 
00279 [L817] MOV      A=21 B=0 C=17 D=17 
00280 [L817] MOV      A=22 B=0 C=18 D=18 
00281 [L817] CALL     A=19 B=2 C=4 D=516 
00282 [L818] MOV      A=21 B=0 C=14 D=14 
00283 [L818] TGETS    A=20 B=14 C=58 D=3642 'startScroll'
00284 [L818] CALL     A=20 B=1 C=2 D=258 
00285 [L819] MOV      A=21 B=0 C=14 D=14 
00286 [L819] TGETS    A=20 B=14 C=59 D=3643 'setDataSource'
00287 [L819] MOV      A=22 B=0 C=19 D=19 
00288 [L819] CALL     A=20 B=1 C=3 D=259 
00289 [L821] TDUP     A=20 B=0 C=60 D=60 {'kind': 'table', 'value': {}}
00290 [L821] TSETS    A=15 B=20 C=61 D=5181 'touchCellAtIndex'
00291 [L822] MOV      A=22 B=0 C=14 D=14 
00292 [L822] TGETS    A=21 B=14 C=62 D=3646 'setDelegate'
00293 [L822] MOV      A=23 B=0 C=20 D=20 
00294 [L822] CALL     A=21 B=1 C=3 D=259 
00295 [L828] FNEW     A=21 B=0 C=63 D=63 {'kind': 'proto', 'id': 40}
00296 [L858] FNEW     A=22 B=0 C=64 D=64 {'kind': 'proto', 'id': 41}
00297 [L859] TDUP     A=23 B=0 C=65 D=65 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00298 [L862] TDUP     A=24 B=0 C=66 D=66 {'kind': 'table', 'value': {'npic': 'v2/introUI/close1.png', 'spic': 'v2/introUI/close2.png'}}
00299 [L863] MULNV    A=25 B=5 C=14 D=1294 
00300 [L863] ADDNV    A=25 B=25 C=3 D=6403 
00301 [L863] TSETS    A=25 B=24 C=27 D=6171 'x'
00302 [L863] MULNV    A=25 B=6 C=2 D=1538 
00303 [L863] ADDNV    A=25 B=25 C=3 D=6403 
00304 [L863] TSETS    A=25 B=24 C=16 D=6160 'y'
00305 [L863] TSETS    A=21 B=24 C=67 D=6211 'call_back'
00306 [L863] TSETB    A=24 B=23 C=1 D=5889 
00307 [L863] TDUP     A=24 B=0 C=68 D=68 {'kind': 'table', 'value': {'npic': 'v2/kickUI/btn11.png', 'spic': 'v2/kickUI/btn12.png', 'x': 0.5}}
00308 [L864] MULNV    A=25 B=6 C=7 D=1543 
00309 [L864] SUBNV    A=25 B=25 C=3 D=6403 
00310 [L864] TSETS    A=25 B=24 C=16 D=6160 'y'
00311 [L864] TSETS    A=22 B=24 C=67 D=6211 'call_back'
00312 [L864] TSETB    A=24 B=23 C=2 D=5890 
00313 [L866] MOV      A=25 B=0 C=3 D=3 
00314 [L866] TGETS    A=24 B=3 C=11 D=779 'addChild'
00315 [L866] GGET     A=26 B=0 C=6 D=6 'd_ms'
00316 [L866] TGETS    A=26 B=26 C=7 D=6663 'd_u'
00317 [L866] TGETS    A=26 B=26 C=69 D=6725 'createMenu'
00318 [L866] MOV      A=27 B=0 C=23 D=23 
00319 [L866] CALL     A=26 B=2 C=2 D=514 
00320 [L866] KSHORT   A=27 B=0 C=5 D=5 5
00321 [L866] CALL     A=24 B=1 C=4 D=260 
00322 [L867] MOV      A=25 B=0 C=0 D=0 
00323 [L867] TGETS    A=24 B=0 C=11 D=11 'addChild'
00324 [L867] MOV      A=26 B=0 C=3 D=3 
00325 [L867] MOV      A=27 B=0 C=1 D=1 
00326 [L867] CALL     A=24 B=1 C=4 D=260 
00327 [L868] GGET     A=24 B=0 C=3 D=3 'g_boxUI'
00328 [L868] TSETS    A=3 B=24 C=70 D=6214 'main_layer'
00329 [L869] UCLO     A=0 B=128 C=0 D=32768 target=330
00330 [L869] RET0     A=0 B=0 C=1 D=1 
00331 [L869] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto43 offset=0x6634 source_lines=934-941 params=0
UPVALUES ['CCDirector', 'info', 'type_id']
00001 [L935] UGET     A=0 B=0 C=0 D=0 CCDirector
00002 [L935] MOV      A=1 B=0 C=0 D=0 
00003 [L935] TGETS    A=0 B=0 C=0 D=0 'sharedDirector'
00004 [L935] CALL     A=0 B=2 C=2 D=514 
00005 [L935] MOV      A=1 B=0 C=0 D=0 
00006 [L935] TGETS    A=0 B=0 C=1 D=1 'getRunningScene'
00007 [L935] CALL     A=0 B=2 C=2 D=514 
00008 [L936] UGET     A=1 B=0 C=1 D=1 info
00009 [L936] TGETS    A=1 B=1 C=2 D=258 'hasGot'
00010 [L936] ISF      A=0 B=0 C=1 D=1 
00011 [L936] JMP      A=2 B=128 C=9 D=32777 target=21
00012 [L937] GGET     A=1 B=0 C=3 D=3 'd_ms'
00013 [L937] TGETS    A=1 B=1 C=4 D=260 'd_formationUI'
00014 [L937] TGETS    A=1 B=1 C=5 D=261 'showIntroduceLayer'
00015 [L937] MOV      A=2 B=0 C=0 D=0 
00016 [L937] UGET     A=3 B=0 C=1 D=1 info
00017 [L937] TGETS    A=3 B=3 C=6 D=774 'char'
00018 [L937] KSHORT   A=4 B=0 C=0 D=0 0
00019 [L937] CALL     A=1 B=1 C=4 D=260 
00020 [L937] JMP      A=1 B=128 C=6 D=32774 target=27
00021 [L939] GGET     A=1 B=0 C=3 D=3 'd_ms'
00022 [L939] TGETS    A=1 B=1 C=7 D=263 'd_data'
00023 [L939] TGETS    A=1 B=1 C=8 D=264 'showCharacterIntroByTypeId'
00024 [L939] UGET     A=2 B=0 C=2 D=2 type_id
00025 [L939] MOV      A=3 B=0 C=0 D=0 
00026 [L939] CALL     A=1 B=1 C=3 D=259 
00027 [L941] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto44 offset=0x6763 source_lines=871-949 params=6
UPVALUES ['CCSprite', 'ccp', 'ccc3', 'CCPointMake', 'gethz', 'string', 'CCDirector']
00001 [L872] UGET     A=6 B=0 C=0 D=0 CCSprite
00002 [L872] MOV      A=7 B=0 C=6 D=6 
00003 [L872] TGETS    A=6 B=6 C=0 D=1536 'create'
00004 [L872] KSTR     A=8 B=0 C=1 D=1 'v2/godBlessUI/line.png'
00005 [L872] CALL     A=6 B=2 C=3 D=515 
00006 [L873] MOV      A=8 B=0 C=6 D=6 
00007 [L873] TGETS    A=7 B=6 C=2 D=1538 'setPosition'
00008 [L873] TGETS    A=9 B=4 C=3 D=1027 'width'
00009 [L873] MULVN    A=9 B=9 C=0 D=2304 
00010 [L873] KSHORT   A=10 B=0 C=0 D=0 0
00011 [L873] CALL     A=7 B=1 C=4 D=260 
00012 [L874] MOV      A=8 B=0 C=0 D=0 
00013 [L874] TGETS    A=7 B=0 C=4 D=4 'addChild'
00014 [L874] MOV      A=9 B=0 C=6 D=6 
00015 [L874] CALL     A=7 B=1 C=3 D=259 
00016 [L875] MOV      A=8 B=0 C=6 D=6 
00017 [L875] TGETS    A=7 B=6 C=5 D=1541 'setScaleX'
00018 [L875] TGETS    A=9 B=4 C=3 D=1027 'width'
00019 [L875] MOV      A=11 B=0 C=6 D=6 
00020 [L875] TGETS    A=10 B=6 C=6 D=1542 'getContentSize'
00021 [L875] CALL     A=10 B=2 C=2 D=514 
00022 [L875] TGETS    A=10 B=10 C=3 D=2563 'width'
00023 [L875] DIVVV    A=9 B=9 C=10 D=2314 
00024 [L875] CALL     A=7 B=1 C=3 D=259 
00025 [L877] TGETS    A=7 B=2 C=7 D=519 'hasGot'
00026 [L877] ISF      A=0 B=0 C=7 D=7 
00027 [L877] JMP      A=8 B=128 C=4 D=32772 target=32
00028 [L877] TGETS    A=7 B=2 C=8 D=520 'char'
00029 [L877] TGETS    A=7 B=7 C=9 D=1801 'type'
00030 [L877] IST      A=0 B=0 C=7 D=7 
00031 [L877] JMP      A=8 B=128 C=2 D=32770 target=34
00032 [L877] TGETS    A=7 B=2 C=8 D=520 'char'
00033 [L877] TGETS    A=7 B=7 C=10 D=1802 'type_id'
00034 [L878] TGETS    A=8 B=2 C=7 D=519 'hasGot'
00035 [L878] ISF      A=0 B=0 C=8 D=8 
00036 [L878] JMP      A=9 B=128 C=12 D=32780 target=49
00037 [L878] TGETS    A=8 B=2 C=8 D=520 'char'
00038 [L878] TGETS    A=8 B=8 C=11 D=2059 'reborn_layer'
00039 [L878] ISF      A=0 B=0 C=8 D=8 
00040 [L878] JMP      A=9 B=128 C=8 D=32776 target=49
00041 [L878] TGETS    A=8 B=2 C=8 D=520 'char'
00042 [L878] TGETS    A=8 B=8 C=11 D=2059 'reborn_layer'
00043 [L878] KSHORT   A=9 B=0 C=0 D=0 0
00044 [L878] ISLT     A=9 B=0 C=8 D=8 
00045 [L878] JMP      A=8 B=128 C=2 D=32770 target=48
00046 [L878] KPRI     A=8 B=0 C=1 D=1 
00047 [L878] JMP      A=9 B=128 C=1 D=32769 target=49
00048 [L878] KPRI     A=8 B=0 C=2 D=2 
00049 [L880] GGET     A=9 B=0 C=12 D=12 'd_ms'
00050 [L880] TGETS    A=9 B=9 C=13 D=2317 'd_data'
00051 [L880] TGETS    A=9 B=9 C=14 D=2318 'getNameTxt'
00052 [L880] MOV      A=10 B=0 C=7 D=7 
00053 [L880] MOV      A=11 B=0 C=8 D=8 
00054 [L880] CALL     A=9 B=2 C=3 D=515 
00055 [L881] GGET     A=10 B=0 C=12 D=12 'd_ms'
00056 [L881] TGETS    A=10 B=10 C=15 D=2575 'd_u'
00057 [L881] TGETS    A=10 B=10 C=16 D=2576 'createByStyle'
00058 [L881] TDUP     A=11 B=0 C=17 D=17 {'kind': 'table', 'value': {'font': 'arial', 'fontsize': 30, 'type': 'label'}}
00059 [L881] TSETS    A=9 B=11 C=18 D=2834 'string'
00060 [L881] CALL     A=10 B=2 C=2 D=514 
00061 [L882] MOV      A=12 B=0 C=0 D=0 
00062 [L882] TGETS    A=11 B=0 C=4 D=4 'addChild'
00063 [L882] MOV      A=13 B=0 C=10 D=10 
00064 [L882] KSHORT   A=14 B=0 C=1 D=1 1
00065 [L882] CALL     A=11 B=1 C=4 D=260 
00066 [L883] MOV      A=12 B=0 C=10 D=10 
00067 [L883] TGETS    A=11 B=10 C=19 D=2579 'setAnchorPoint'
00068 [L883] UGET     A=13 B=0 C=1 D=1 ccp
00069 [L883] KSHORT   A=14 B=0 C=0 D=0 0
00070 [L883] KNUM     A=15 B=0 C=0 D=0 0.5
00071 [L883] CALL     A=13 B=0 C=3 D=3 
00072 [L883] CALLM    A=11 B=1 C=1 D=257 
00073 [L884] MOV      A=12 B=0 C=10 D=10 
00074 [L884] TGETS    A=11 B=10 C=20 D=2580 'setColor'
00075 [L884] UGET     A=13 B=0 C=2 D=2 ccc3
00076 [L884] KSHORT   A=14 B=0 C=254 D=254 254
00077 [L884] KSHORT   A=15 B=0 C=235 D=235 235
00078 [L884] KSHORT   A=16 B=0 C=192 D=192 192
00079 [L884] CALL     A=13 B=0 C=4 D=4 
00080 [L884] CALLM    A=11 B=1 C=1 D=257 
00081 [L885] MOV      A=12 B=0 C=10 D=10 
00082 [L885] TGETS    A=11 B=10 C=2 D=2562 'setPosition'
00083 [L885] TGETS    A=13 B=4 C=3 D=1027 'width'
00084 [L885] MULVN    A=13 B=13 C=1 D=3329 
00085 [L885] TGETS    A=14 B=4 C=21 D=1045 'height'
00086 [L885] MULVN    A=14 B=14 C=2 D=3586 
00087 [L885] CALL     A=11 B=1 C=4 D=260 
00088 [L886] MOV      A=12 B=0 C=10 D=10 
00089 [L886] TGETS    A=11 B=10 C=19 D=2579 'setAnchorPoint'
00090 [L886] UGET     A=13 B=0 C=3 D=3 CCPointMake
00091 [L886] KSHORT   A=14 B=0 C=0 D=0 0
00092 [L886] KNUM     A=15 B=0 C=0 D=0 0.5
00093 [L886] CALL     A=13 B=0 C=3 D=3 
00094 [L886] CALLM    A=11 B=1 C=1 D=257 
00095 [L888] TGETS    A=11 B=2 C=7 D=519 'hasGot'
00096 [L888] ISF      A=0 B=0 C=11 D=11 
00097 [L888] JMP      A=12 B=128 C=5 D=32773 target=103
00098 [L888] UGET     A=11 B=0 C=4 D=4 gethz
00099 [L888] KSTR     A=12 B=0 C=22 D=22 'gotHZ'
00100 [L888] CALL     A=11 B=2 C=2 D=514 
00101 [L888] IST      A=0 B=0 C=11 D=11 
00102 [L888] JMP      A=12 B=128 C=3 D=32771 target=106
00103 [L888] UGET     A=11 B=0 C=4 D=4 gethz
00104 [L888] KSTR     A=12 B=0 C=23 D=23 'notGotHZ'
00105 [L888] CALL     A=11 B=2 C=2 D=514 
00106 [L889] GGET     A=12 B=0 C=12 D=12 'd_ms'
00107 [L889] TGETS    A=12 B=12 C=15 D=3087 'd_u'
00108 [L889] TGETS    A=12 B=12 C=16 D=3088 'createByStyle'
00109 [L889] TDUP     A=13 B=0 C=24 D=24 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 26}}
00110 [L889] TSETS    A=11 B=13 C=18 D=3346 'string'
00111 [L889] TDUP     A=14 B=0 C=25 D=25 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00112 [L889] TSETS    A=14 B=13 C=26 D=3354 'anchor'
00113 [L889] TDUP     A=14 B=0 C=27 D=27 {'kind': 'table', 'value': {1: 230, 2: 170, 3: 20}}
00114 [L889] TSETS    A=14 B=13 C=28 D=3356 'color'
00115 [L889] CALL     A=12 B=2 C=2 D=514 
00116 [L890] MOV      A=14 B=0 C=0 D=0 
00117 [L890] TGETS    A=13 B=0 C=4 D=4 'addChild'
00118 [L890] MOV      A=15 B=0 C=12 D=12 
00119 [L890] CALL     A=13 B=1 C=3 D=259 
00120 [L891] MOV      A=14 B=0 C=12 D=12 
00121 [L891] TGETS    A=13 B=12 C=2 D=3074 'setPosition'
00122 [L891] TGETS    A=15 B=4 C=3 D=1027 'width'
00123 [L891] MULVN    A=15 B=15 C=0 D=3840 
00124 [L891] TGETS    A=16 B=4 C=21 D=1045 'height'
00125 [L891] MULVN    A=16 B=16 C=2 D=4098 
00126 [L891] CALL     A=13 B=1 C=4 D=260 
00127 [L893] GGET     A=13 B=0 C=12 D=12 'd_ms'
00128 [L893] TGETS    A=13 B=13 C=29 D=3357 'd_soulExchangeUI'
00129 [L893] TGETS    A=13 B=13 C=30 D=3358 'getSoulCountByCortegeType'
00130 [L893] MOV      A=14 B=0 C=7 D=7 
00131 [L893] CALL     A=13 B=2 C=2 D=514 
00132 [L894] GGET     A=14 B=0 C=12 D=12 'd_ms'
00133 [L894] TGETS    A=14 B=14 C=13 D=3597 'd_data'
00134 [L894] TGETS    A=14 B=14 C=31 D=3615 'getSoulInfo'
00135 [L894] MOV      A=15 B=0 C=7 D=7 
00136 [L894] MOV      A=16 B=0 C=13 D=13 
00137 [L894] CALL     A=14 B=2 C=3 D=515 
00138 [L896] KPRI     A=15 B=0 C=0 D=0 
00139 [L897] TGETS    A=16 B=2 C=7 D=519 'hasGot'
00140 [L897] ISF      A=0 B=0 C=16 D=16 
00141 [L897] JMP      A=17 B=128 C=36 D=32804 target=178
00142 [L898] UGET     A=16 B=0 C=5 D=5 string
00143 [L898] TGETS    A=16 B=16 C=32 D=4128 'format'
00144 [L898] UGET     A=17 B=0 C=4 D=4 gethz
00145 [L898] KSTR     A=18 B=0 C=33 D=33 'soul_ex_str6'
00146 [L898] CALL     A=17 B=2 C=2 D=514 
00147 [L898] TGETS    A=18 B=2 C=8 D=520 'char'
00148 [L898] TGETS    A=18 B=18 C=34 D=4642 'evolve_level'
00149 [L898] CALL     A=16 B=2 C=3 D=515 
00150 [L898] KSTR     A=17 B=0 C=35 D=35 ', '
00151 [L898] CAT      A=15 B=16 C=17 D=4113 
00152 [L899] TGETS    A=16 B=14 C=36 D=3620 'feiShengCount'
00153 [L899] KSHORT   A=17 B=0 C=0 D=0 0
00154 [L899] ISGE     A=17 B=0 C=16 D=16 
00155 [L899] JMP      A=16 B=128 C=13 D=32781 target=169
00156 [L900] MOV      A=16 B=0 C=15 D=15 
00157 [L900] UGET     A=17 B=0 C=5 D=5 string
00158 [L900] TGETS    A=17 B=17 C=32 D=4384 'format'
00159 [L900] UGET     A=18 B=0 C=4 D=4 gethz
00160 [L900] KSTR     A=19 B=0 C=37 D=37 'need_souls'
00161 [L900] CALL     A=18 B=2 C=2 D=514 
00162 [L900] TGETS    A=19 B=14 C=36 D=3620 'feiShengCount'
00163 [L900] UGET     A=20 B=0 C=4 D=4 gethz
00164 [L900] KSTR     A=21 B=0 C=38 D=38 'feiShengHZ'
00165 [L900] CALL     A=20 B=0 C=2 D=2 
00166 [L900] CALLM    A=17 B=2 C=2 D=514 
00167 [L900] CAT      A=15 B=16 C=17 D=4113 
00168 [L900] JMP      A=16 B=128 C=32 D=32800 target=201
00169 [L902] MOV      A=16 B=0 C=15 D=15 
00170 [L902] UGET     A=17 B=0 C=4 D=4 gethz
00171 [L902] KSTR     A=18 B=0 C=39 D=39 'canHZ'
00172 [L902] CALL     A=17 B=2 C=2 D=514 
00173 [L902] UGET     A=18 B=0 C=4 D=4 gethz
00174 [L902] KSTR     A=19 B=0 C=38 D=38 'feiShengHZ'
00175 [L902] CALL     A=18 B=2 C=2 D=514 
00176 [L902] CAT      A=15 B=16 C=18 D=4114 
00177 [L903] JMP      A=16 B=128 C=23 D=32791 target=201
00178 [L905] TGETS    A=16 B=14 C=40 D=3624 'huanHunCount'
00179 [L905] KSHORT   A=17 B=0 C=0 D=0 0
00180 [L905] ISGE     A=17 B=0 C=16 D=16 
00181 [L905] JMP      A=16 B=128 C=12 D=32780 target=194
00182 [L906] UGET     A=16 B=0 C=5 D=5 string
00183 [L906] TGETS    A=16 B=16 C=32 D=4128 'format'
00184 [L906] UGET     A=17 B=0 C=4 D=4 gethz
00185 [L906] KSTR     A=18 B=0 C=37 D=37 'need_souls'
00186 [L906] CALL     A=17 B=2 C=2 D=514 
00187 [L906] TGETS    A=18 B=14 C=40 D=3624 'huanHunCount'
00188 [L906] UGET     A=19 B=0 C=4 D=4 gethz
00189 [L906] KSTR     A=20 B=0 C=41 D=41 'huanHunHZ'
00190 [L906] CALL     A=19 B=0 C=2 D=2 
00191 [L906] CALLM    A=16 B=2 C=2 D=514 
00192 [L906] MOV      A=15 B=0 C=16 D=16 
00193 [L906] JMP      A=16 B=128 C=7 D=32775 target=201
00194 [L908] UGET     A=16 B=0 C=4 D=4 gethz
00195 [L908] KSTR     A=17 B=0 C=39 D=39 'canHZ'
00196 [L908] CALL     A=16 B=2 C=2 D=514 
00197 [L908] UGET     A=17 B=0 C=4 D=4 gethz
00198 [L908] KSTR     A=18 B=0 C=41 D=41 'huanHunHZ'
00199 [L908] CALL     A=17 B=2 C=2 D=514 
00200 [L908] CAT      A=15 B=16 C=17 D=4113 
00201 [L911] GGET     A=16 B=0 C=12 D=12 'd_ms'
00202 [L911] TGETS    A=16 B=16 C=15 D=4111 'd_u'
00203 [L911] TGETS    A=16 B=16 C=16 D=4112 'createByStyle'
00204 [L911] TDUP     A=17 B=0 C=42 D=42 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 26}}
00205 [L911] TSETS    A=15 B=17 C=18 D=4370 'string'
00206 [L911] TDUP     A=18 B=0 C=43 D=43 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00207 [L911] TSETS    A=18 B=17 C=26 D=4378 'anchor'
00208 [L911] TDUP     A=18 B=0 C=44 D=44 {'kind': 'table', 'value': {1: 230, 2: 170, 3: 20}}
00209 [L911] TSETS    A=18 B=17 C=28 D=4380 'color'
00210 [L911] CALL     A=16 B=2 C=2 D=514 
00211 [L912] MOV      A=18 B=0 C=0 D=0 
00212 [L912] TGETS    A=17 B=0 C=4 D=4 'addChild'
00213 [L912] MOV      A=19 B=0 C=16 D=16 
00214 [L912] KSHORT   A=20 B=0 C=1 D=1 1
00215 [L912] CALL     A=17 B=1 C=4 D=260 
00216 [L913] MOV      A=18 B=0 C=16 D=16 
00217 [L913] TGETS    A=17 B=16 C=2 D=4098 'setPosition'
00218 [L913] TGETS    A=19 B=4 C=3 D=1027 'width'
00219 [L913] MULVN    A=19 B=19 C=1 D=4865 
00220 [L913] TGETS    A=20 B=4 C=21 D=1045 'height'
00221 [L913] MULVN    A=20 B=20 C=3 D=5123 
00222 [L913] CALL     A=17 B=1 C=4 D=260 
00223 [L915] UGET     A=17 B=0 C=0 D=0 CCSprite
00224 [L915] MOV      A=18 B=0 C=17 D=17 
00225 [L915] TGETS    A=17 B=17 C=0 D=4352 'create'
00226 [L915] KSTR     A=19 B=0 C=45 D=45 'v2/multi-selectUI/check_frame.png'
00227 [L915] CALL     A=17 B=2 C=3 D=515 
00228 [L916] MOV      A=19 B=0 C=17 D=17 
00229 [L916] TGETS    A=18 B=17 C=2 D=4354 'setPosition'
00230 [L916] TGETS    A=20 B=4 C=3 D=1027 'width'
00231 [L916] MULVN    A=20 B=20 C=4 D=5124 
00232 [L916] TGETS    A=21 B=4 C=21 D=1045 'height'
00233 [L916] MULVN    A=21 B=21 C=0 D=5376 
00234 [L916] CALL     A=18 B=1 C=4 D=260 
00235 [L917] MOV      A=19 B=0 C=0 D=0 
00236 [L917] TGETS    A=18 B=0 C=4 D=4 'addChild'
00237 [L917] MOV      A=20 B=0 C=17 D=17 
00238 [L917] KSHORT   A=21 B=0 C=1 D=1 1
00239 [L917] CALL     A=18 B=1 C=4 D=260 
00240 [L918] TGETS    A=18 B=4 C=21 D=1045 'height'
00241 [L918] MULVN    A=18 B=18 C=2 D=4610 
00242 [L918] MOV      A=20 B=0 C=17 D=17 
00243 [L918] TGETS    A=19 B=17 C=6 D=4358 'getContentSize'
00244 [L918] CALL     A=19 B=2 C=2 D=514 
00245 [L918] TGETS    A=19 B=19 C=21 D=4885 'height'
00246 [L918] DIVVV    A=18 B=18 C=19 D=4627 
00247 [L919] MOV      A=20 B=0 C=17 D=17 
00248 [L919] TGETS    A=19 B=17 C=46 D=4398 'setScale'
00249 [L919] MOV      A=21 B=0 C=18 D=18 
00250 [L919] CALL     A=19 B=1 C=3 D=259 
00251 [L921] GGET     A=19 B=0 C=47 D=47 'g_boxUI'
00252 [L921] TGETS    A=19 B=19 C=48 D=4912 'lastTouchIndex'
00253 [L921] ISNEV    A=19 B=0 C=1 D=1 
00254 [L921] JMP      A=19 B=128 C=21 D=32789 target=276
00255 [L922] UGET     A=19 B=0 C=0 D=0 CCSprite
00256 [L922] MOV      A=20 B=0 C=19 D=19 
00257 [L922] TGETS    A=19 B=19 C=0 D=4864 'create'
00258 [L922] KSTR     A=21 B=0 C=49 D=49 'v2/multi-selectUI/check.png'
00259 [L922] CALL     A=19 B=2 C=3 D=515 
00260 [L923] MOV      A=21 B=0 C=19 D=19 
00261 [L923] TGETS    A=20 B=19 C=2 D=4866 'setPosition'
00262 [L923] TGETS    A=22 B=4 C=3 D=1027 'width'
00263 [L923] MULVN    A=22 B=22 C=4 D=5636 
00264 [L923] TGETS    A=23 B=4 C=21 D=1045 'height'
00265 [L923] MULVN    A=23 B=23 C=0 D=5888 
00266 [L923] CALL     A=20 B=1 C=4 D=260 
00267 [L924] MOV      A=21 B=0 C=0 D=0 
00268 [L924] TGETS    A=20 B=0 C=4 D=4 'addChild'
00269 [L924] MOV      A=22 B=0 C=19 D=19 
00270 [L924] KSHORT   A=23 B=0 C=2 D=2 2
00271 [L924] CALL     A=20 B=1 C=4 D=260 
00272 [L925] MOV      A=21 B=0 C=19 D=19 
00273 [L925] TGETS    A=20 B=19 C=46 D=4910 'setScale'
00274 [L925] MOV      A=22 B=0 C=18 D=18 
00275 [L925] CALL     A=20 B=1 C=3 D=259 
00276 [L928] GGET     A=19 B=0 C=12 D=12 'd_ms'
00277 [L928] TGETS    A=19 B=19 C=13 D=4877 'd_data'
00278 [L928] TGETS    A=19 B=19 C=50 D=4914 'getHeadSprite'
00279 [L928] MOV      A=20 B=0 C=7 D=7 
00280 [L928] MOV      A=21 B=0 C=8 D=8 
00281 [L928] CALL     A=19 B=2 C=3 D=515 
00282 [L929] GGET     A=20 B=0 C=12 D=12 'd_ms'
00283 [L929] TGETS    A=20 B=20 C=13 D=5133 'd_data'
00284 [L929] TGETS    A=20 B=20 C=50 D=5170 'getHeadSprite'
00285 [L929] MOV      A=21 B=0 C=7 D=7 
00286 [L929] MOV      A=22 B=0 C=8 D=8 
00287 [L929] CALL     A=20 B=2 C=3 D=515 
00288 [L930] TGETS    A=21 B=4 C=21 D=1045 'height'
00289 [L930] MULNV    A=21 B=21 C=5 D=5381 
00290 [L930] MOV      A=23 B=0 C=19 D=19 
00291 [L930] TGETS    A=22 B=19 C=6 D=4870 'getContentSize'
00292 [L930] CALL     A=22 B=2 C=2 D=514 
00293 [L930] TGETS    A=22 B=22 C=21 D=5653 'height'
00294 [L930] DIVVV    A=21 B=21 C=22 D=5398 
00295 [L931] MOV      A=23 B=0 C=19 D=19 
00296 [L931] TGETS    A=22 B=19 C=46 D=4910 'setScale'
00297 [L931] MOV      A=24 B=0 C=21 D=21 
00298 [L931] CALL     A=22 B=1 C=3 D=259 
00299 [L932] MOV      A=23 B=0 C=20 D=20 
00300 [L932] TGETS    A=22 B=20 C=46 D=5166 'setScale'
00301 [L932] MOV      A=24 B=0 C=21 D=21 
00302 [L932] CALL     A=22 B=1 C=3 D=259 
00303 [L941] FNEW     A=22 B=0 C=51 D=51 {'kind': 'proto', 'id': 43}
00304 [L943] TNEW     A=23 B=0 C=0 D=0 
00305 [L944] TNEW     A=24 B=8 C=0 D=2048 
00306 [L944] TDUP     A=25 B=0 C=53 D=53 {'kind': 'table', 'value': {}}
00307 [L944] TSETS    A=19 B=25 C=54 D=6454 'nSprite'
00308 [L944] TSETS    A=20 B=25 C=55 D=6455 'sSprite'
00309 [L944] TSETS    A=22 B=25 C=56 D=6456 'tapHandler'
00310 [L945] UGET     A=26 B=0 C=1 D=1 ccp
00311 [L945] TGETS    A=27 B=4 C=3 D=1027 'width'
00312 [L945] MULVN    A=27 B=27 C=6 D=6918 
00313 [L945] TGETS    A=28 B=4 C=21 D=1045 'height'
00314 [L945] MULVN    A=28 B=28 C=0 D=7168 
00315 [L945] CALL     A=26 B=2 C=3 D=515 
00316 [L945] TSETS    A=26 B=25 C=57 D=6457 'pos'
00317 [L945] TSETB    A=25 B=24 C=1 D=6145 
00318 [L945] TSETS    A=24 B=23 C=52 D=5940 'menuItems'
00319 [L946] TSETS    A=5 B=23 C=58 D=5946 'touchRect'
00320 [L947] GGET     A=24 B=0 C=12 D=12 'd_ms'
00321 [L947] TGETS    A=24 B=24 C=59 D=6203 'd_tableView'
00322 [L947] TGETS    A=24 B=24 C=60 D=6204 'createTableViewMenu'
00323 [L947] MOV      A=25 B=0 C=23 D=23 
00324 [L947] CALL     A=24 B=2 C=2 D=514 
00325 [L948] MOV      A=26 B=0 C=0 D=0 
00326 [L948] TGETS    A=25 B=0 C=4 D=4 'addChild'
00327 [L948] MOV      A=27 B=0 C=24 D=24 
00328 [L948] CALL     A=25 B=1 C=3 D=259 
00329 [L949] UCLO     A=0 B=128 C=0 D=32768 target=330
00330 [L949] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto45 offset=0x7280 source_lines=992-996 params=0
UPVALUES ['o_t', 'type_id', 'CCDirector']
00001 [L993] TDUP     A=0 B=0 C=1 D=1 {'kind': 'table', 'value': {}}
00002 [L993] UGET     A=1 B=0 C=0 D=0 o_t
00003 [L993] TGETS    A=1 B=1 C=0 D=256 'item'
00004 [L993] TSETS    A=1 B=0 C=2 D=2 'object_type'
00005 [L993] UGET     A=1 B=0 C=1 D=1 type_id
00006 [L993] TSETS    A=1 B=0 C=3 D=3 'attach_type'
00007 [L994] UGET     A=1 B=0 C=2 D=2 CCDirector
00008 [L994] MOV      A=2 B=0 C=1 D=1 
00009 [L994] TGETS    A=1 B=1 C=4 D=260 'sharedDirector'
00010 [L994] CALL     A=1 B=2 C=2 D=514 
00011 [L994] MOV      A=2 B=0 C=1 D=1 
00012 [L994] TGETS    A=1 B=1 C=5 D=261 'getRunningScene'
00013 [L994] CALL     A=1 B=2 C=2 D=514 
00014 [L995] GGET     A=2 B=0 C=6 D=6 'd_ms'
00015 [L995] TGETS    A=2 B=2 C=7 D=519 'd_data'
00016 [L995] TGETS    A=2 B=2 C=8 D=520 'showItemIntro'
00017 [L995] MOV      A=3 B=0 C=1 D=1 
00018 [L995] MOV      A=4 B=0 C=0 D=0 
00019 [L995] CALL     A=2 B=1 C=3 D=259 
00020 [L996] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto46 offset=0x7377 source_lines=951-1004 params=5
UPVALUES ['CCSprite', 'ccp', 'ccc3', 'CCPointMake', 'gethz', 'o_t', 'CCDirector']
00001 [L952] UGET     A=5 B=0 C=0 D=0 CCSprite
00002 [L952] MOV      A=6 B=0 C=5 D=5 
00003 [L952] TGETS    A=5 B=5 C=0 D=1280 'create'
00004 [L952] KSTR     A=7 B=0 C=1 D=1 'v2/godBlessUI/line.png'
00005 [L952] CALL     A=5 B=2 C=3 D=515 
00006 [L953] MOV      A=7 B=0 C=5 D=5 
00007 [L953] TGETS    A=6 B=5 C=2 D=1282 'setPosition'
00008 [L953] TGETS    A=8 B=3 C=3 D=771 'width'
00009 [L953] MULVN    A=8 B=8 C=0 D=2048 
00010 [L953] KSHORT   A=9 B=0 C=0 D=0 0
00011 [L953] CALL     A=6 B=1 C=4 D=260 
00012 [L954] MOV      A=7 B=0 C=0 D=0 
00013 [L954] TGETS    A=6 B=0 C=4 D=4 'addChild'
00014 [L954] MOV      A=8 B=0 C=5 D=5 
00015 [L954] CALL     A=6 B=1 C=3 D=259 
00016 [L955] MOV      A=7 B=0 C=5 D=5 
00017 [L955] TGETS    A=6 B=5 C=5 D=1285 'setScaleX'
00018 [L955] TGETS    A=8 B=3 C=3 D=771 'width'
00019 [L955] MOV      A=10 B=0 C=5 D=5 
00020 [L955] TGETS    A=9 B=5 C=6 D=1286 'getContentSize'
00021 [L955] CALL     A=9 B=2 C=2 D=514 
00022 [L955] TGETS    A=9 B=9 C=3 D=2307 'width'
00023 [L955] DIVVV    A=8 B=8 C=9 D=2057 
00024 [L955] CALL     A=6 B=1 C=3 D=259 
00025 [L957] TGETS    A=6 B=2 C=7 D=519 'item'
00026 [L957] TGETS    A=6 B=6 C=8 D=1544 'type_id'
00027 [L959] GGET     A=7 B=0 C=9 D=9 'd_ms'
00028 [L959] TGETS    A=7 B=7 C=10 D=1802 'd_data'
00029 [L959] TGETS    A=7 B=7 C=11 D=1803 'getItemName'
00030 [L959] MOV      A=8 B=0 C=6 D=6 
00031 [L959] CALL     A=7 B=2 C=2 D=514 
00032 [L960] GGET     A=8 B=0 C=9 D=9 'd_ms'
00033 [L960] TGETS    A=8 B=8 C=12 D=2060 'd_u'
00034 [L960] TGETS    A=8 B=8 C=13 D=2061 'createByStyle'
00035 [L960] TDUP     A=9 B=0 C=14 D=14 {'kind': 'table', 'value': {'font': 'arial', 'fontsize': 30, 'type': 'label'}}
00036 [L960] TSETS    A=7 B=9 C=15 D=2319 'string'
00037 [L960] CALL     A=8 B=2 C=2 D=514 
00038 [L961] MOV      A=10 B=0 C=0 D=0 
00039 [L961] TGETS    A=9 B=0 C=4 D=4 'addChild'
00040 [L961] MOV      A=11 B=0 C=8 D=8 
00041 [L961] KSHORT   A=12 B=0 C=1 D=1 1
00042 [L961] CALL     A=9 B=1 C=4 D=260 
00043 [L962] MOV      A=10 B=0 C=8 D=8 
00044 [L962] TGETS    A=9 B=8 C=16 D=2064 'setAnchorPoint'
00045 [L962] UGET     A=11 B=0 C=1 D=1 ccp
00046 [L962] KSHORT   A=12 B=0 C=0 D=0 0
00047 [L962] KNUM     A=13 B=0 C=0 D=0 0.5
00048 [L962] CALL     A=11 B=0 C=3 D=3 
00049 [L962] CALLM    A=9 B=1 C=1 D=257 
00050 [L963] MOV      A=10 B=0 C=8 D=8 
00051 [L963] TGETS    A=9 B=8 C=17 D=2065 'setColor'
00052 [L963] UGET     A=11 B=0 C=2 D=2 ccc3
00053 [L963] KSHORT   A=12 B=0 C=254 D=254 254
00054 [L963] KSHORT   A=13 B=0 C=235 D=235 235
00055 [L963] KSHORT   A=14 B=0 C=192 D=192 192
00056 [L963] CALL     A=11 B=0 C=4 D=4 
00057 [L963] CALLM    A=9 B=1 C=1 D=257 
00058 [L964] MOV      A=10 B=0 C=8 D=8 
00059 [L964] TGETS    A=9 B=8 C=2 D=2050 'setPosition'
00060 [L964] TGETS    A=11 B=3 C=3 D=771 'width'
00061 [L964] MULVN    A=11 B=11 C=1 D=2817 
00062 [L964] TGETS    A=12 B=3 C=18 D=786 'height'
00063 [L964] MULVN    A=12 B=12 C=0 D=3072 
00064 [L964] CALL     A=9 B=1 C=4 D=260 
00065 [L965] MOV      A=10 B=0 C=8 D=8 
00066 [L965] TGETS    A=9 B=8 C=16 D=2064 'setAnchorPoint'
00067 [L965] UGET     A=11 B=0 C=3 D=3 CCPointMake
00068 [L965] KSHORT   A=12 B=0 C=0 D=0 0
00069 [L965] KNUM     A=13 B=0 C=0 D=0 0.5
00070 [L965] CALL     A=11 B=0 C=3 D=3 
00071 [L965] CALLM    A=9 B=1 C=1 D=257 
00072 [L967] TGETS    A=9 B=2 C=19 D=531 'hasGot'
00073 [L967] ISF      A=0 B=0 C=9 D=9 
00074 [L967] JMP      A=10 B=128 C=11 D=32779 target=86
00075 [L967] UGET     A=9 B=0 C=4 D=4 gethz
00076 [L967] KSTR     A=10 B=0 C=20 D=20 'gotHZ'
00077 [L967] CALL     A=9 B=2 C=2 D=514 
00078 [L967] TGETS    A=10 B=2 C=7 D=519 'item'
00079 [L967] TGETS    A=10 B=10 C=21 D=2581 'count'
00080 [L967] UGET     A=11 B=0 C=4 D=4 gethz
00081 [L967] KSTR     A=12 B=0 C=22 D=22 'countHZ'
00082 [L967] CALL     A=11 B=2 C=2 D=514 
00083 [L967] CAT      A=9 B=9 C=11 D=2315 
00084 [L967] IST      A=0 B=0 C=9 D=9 
00085 [L967] JMP      A=10 B=128 C=3 D=32771 target=89
00086 [L967] UGET     A=9 B=0 C=4 D=4 gethz
00087 [L967] KSTR     A=10 B=0 C=23 D=23 'notGotHZ'
00088 [L967] CALL     A=9 B=2 C=2 D=514 
00089 [L968] GGET     A=10 B=0 C=9 D=9 'd_ms'
00090 [L968] TGETS    A=10 B=10 C=12 D=2572 'd_u'
00091 [L968] TGETS    A=10 B=10 C=13 D=2573 'createByStyle'
00092 [L968] TDUP     A=11 B=0 C=24 D=24 {'kind': 'table', 'value': {'font': 'arial', 'type': 'label', 'fontsize': 26}}
00093 [L968] TSETS    A=9 B=11 C=15 D=2831 'string'
00094 [L968] TDUP     A=12 B=0 C=25 D=25 {'kind': 'table', 'value': {1: 0, 2: 0.5}}
00095 [L968] TSETS    A=12 B=11 C=26 D=2842 'anchor'
00096 [L968] TDUP     A=12 B=0 C=27 D=27 {'kind': 'table', 'value': {1: 230, 2: 170, 3: 20}}
00097 [L968] TSETS    A=12 B=11 C=28 D=2844 'color'
00098 [L968] CALL     A=10 B=2 C=2 D=514 
00099 [L969] MOV      A=12 B=0 C=0 D=0 
00100 [L969] TGETS    A=11 B=0 C=4 D=4 'addChild'
00101 [L969] MOV      A=13 B=0 C=10 D=10 
00102 [L969] CALL     A=11 B=1 C=3 D=259 
00103 [L970] MOV      A=12 B=0 C=10 D=10 
00104 [L970] TGETS    A=11 B=10 C=2 D=2562 'setPosition'
00105 [L970] TGETS    A=13 B=3 C=3 D=771 'width'
00106 [L970] MULVN    A=13 B=13 C=0 D=3328 
00107 [L970] TGETS    A=14 B=3 C=18 D=786 'height'
00108 [L970] MULVN    A=14 B=14 C=0 D=3584 
00109 [L970] CALL     A=11 B=1 C=4 D=260 
00110 [L973] UGET     A=11 B=0 C=0 D=0 CCSprite
00111 [L973] MOV      A=12 B=0 C=11 D=11 
00112 [L973] TGETS    A=11 B=11 C=0 D=2816 'create'
00113 [L973] KSTR     A=13 B=0 C=29 D=29 'v2/multi-selectUI/check_frame.png'
00114 [L973] CALL     A=11 B=2 C=3 D=515 
00115 [L974] MOV      A=13 B=0 C=11 D=11 
00116 [L974] TGETS    A=12 B=11 C=2 D=2818 'setPosition'
00117 [L974] TGETS    A=14 B=3 C=3 D=771 'width'
00118 [L974] MULVN    A=14 B=14 C=2 D=3586 
00119 [L974] TGETS    A=15 B=3 C=18 D=786 'height'
00120 [L974] MULVN    A=15 B=15 C=0 D=3840 
00121 [L974] CALL     A=12 B=1 C=4 D=260 
00122 [L975] MOV      A=13 B=0 C=0 D=0 
00123 [L975] TGETS    A=12 B=0 C=4 D=4 'addChild'
00124 [L975] MOV      A=14 B=0 C=11 D=11 
00125 [L975] KSHORT   A=15 B=0 C=1 D=1 1
00126 [L975] CALL     A=12 B=1 C=4 D=260 
00127 [L976] TGETS    A=12 B=3 C=18 D=786 'height'
00128 [L976] MULVN    A=12 B=12 C=3 D=3075 
00129 [L976] MOV      A=14 B=0 C=11 D=11 
00130 [L976] TGETS    A=13 B=11 C=6 D=2822 'getContentSize'
00131 [L976] CALL     A=13 B=2 C=2 D=514 
00132 [L976] TGETS    A=13 B=13 C=18 D=3346 'height'
00133 [L976] DIVVV    A=12 B=12 C=13 D=3085 
00134 [L977] MOV      A=14 B=0 C=11 D=11 
00135 [L977] TGETS    A=13 B=11 C=30 D=2846 'setScale'
00136 [L977] MOV      A=15 B=0 C=12 D=12 
00137 [L977] CALL     A=13 B=1 C=3 D=259 
00138 [L979] GGET     A=13 B=0 C=31 D=31 'g_boxUI'
00139 [L979] TGETS    A=13 B=13 C=32 D=3360 'lastTouchIndex'
00140 [L979] ISNEV    A=13 B=0 C=1 D=1 
00141 [L979] JMP      A=13 B=128 C=21 D=32789 target=163
00142 [L980] UGET     A=13 B=0 C=0 D=0 CCSprite
00143 [L980] MOV      A=14 B=0 C=13 D=13 
00144 [L980] TGETS    A=13 B=13 C=0 D=3328 'create'
00145 [L980] KSTR     A=15 B=0 C=33 D=33 'v2/multi-selectUI/check.png'
00146 [L980] CALL     A=13 B=2 C=3 D=515 
00147 [L981] MOV      A=15 B=0 C=13 D=13 
00148 [L981] TGETS    A=14 B=13 C=2 D=3330 'setPosition'
00149 [L981] TGETS    A=16 B=3 C=3 D=771 'width'
00150 [L981] MULVN    A=16 B=16 C=2 D=4098 
00151 [L981] TGETS    A=17 B=3 C=18 D=786 'height'
00152 [L981] MULVN    A=17 B=17 C=0 D=4352 
00153 [L981] CALL     A=14 B=1 C=4 D=260 
00154 [L982] MOV      A=15 B=0 C=0 D=0 
00155 [L982] TGETS    A=14 B=0 C=4 D=4 'addChild'
00156 [L982] MOV      A=16 B=0 C=13 D=13 
00157 [L982] KSHORT   A=17 B=0 C=2 D=2 2
00158 [L982] CALL     A=14 B=1 C=4 D=260 
00159 [L983] MOV      A=15 B=0 C=13 D=13 
00160 [L983] TGETS    A=14 B=13 C=30 D=3358 'setScale'
00161 [L983] MOV      A=16 B=0 C=12 D=12 
00162 [L983] CALL     A=14 B=1 C=3 D=259 
00163 [L986] GGET     A=13 B=0 C=9 D=9 'd_ms'
00164 [L986] TGETS    A=13 B=13 C=10 D=3338 'd_data'
00165 [L986] TGETS    A=13 B=13 C=34 D=3362 'getSmallItemSprite'
00166 [L986] MOV      A=14 B=0 C=6 D=6 
00167 [L986] CALL     A=13 B=2 C=2 D=514 
00168 [L987] GGET     A=14 B=0 C=9 D=9 'd_ms'
00169 [L987] TGETS    A=14 B=14 C=10 D=3594 'd_data'
00170 [L987] TGETS    A=14 B=14 C=34 D=3618 'getSmallItemSprite'
00171 [L987] MOV      A=15 B=0 C=6 D=6 
00172 [L987] CALL     A=14 B=2 C=2 D=514 
00173 [L988] TGETS    A=15 B=3 C=18 D=786 'height'
00174 [L988] MULNV    A=15 B=15 C=4 D=3844 
00175 [L988] MOV      A=17 B=0 C=13 D=13 
00176 [L988] TGETS    A=16 B=13 C=6 D=3334 'getContentSize'
00177 [L988] CALL     A=16 B=2 C=2 D=514 
00178 [L988] TGETS    A=16 B=16 C=18 D=4114 'height'
00179 [L988] DIVVV    A=15 B=15 C=16 D=3856 
00180 [L989] MOV      A=17 B=0 C=13 D=13 
00181 [L989] TGETS    A=16 B=13 C=30 D=3358 'setScale'
00182 [L989] MOV      A=18 B=0 C=15 D=15 
00183 [L989] CALL     A=16 B=1 C=3 D=259 
00184 [L990] MOV      A=17 B=0 C=14 D=14 
00185 [L990] TGETS    A=16 B=14 C=30 D=3614 'setScale'
00186 [L990] MOV      A=18 B=0 C=15 D=15 
00187 [L990] CALL     A=16 B=1 C=3 D=259 
00188 [L996] FNEW     A=16 B=0 C=35 D=35 {'kind': 'proto', 'id': 45}
00189 [L998] TNEW     A=17 B=0 C=0 D=0 
00190 [L999] TNEW     A=18 B=8 C=0 D=2048 
00191 [L999] TDUP     A=19 B=0 C=37 D=37 {'kind': 'table', 'value': {}}
00192 [L999] TSETS    A=13 B=19 C=38 D=4902 'nSprite'
00193 [L999] TSETS    A=14 B=19 C=39 D=4903 'sSprite'
00194 [L999] TSETS    A=16 B=19 C=40 D=4904 'tapHandler'
00195 [L1000] UGET     A=20 B=0 C=1 D=1 ccp
00196 [L1000] TGETS    A=21 B=3 C=3 D=771 'width'
00197 [L1000] MULVN    A=21 B=21 C=5 D=5381 
00198 [L1000] TGETS    A=22 B=3 C=18 D=786 'height'
00199 [L1000] MULVN    A=22 B=22 C=0 D=5632 
00200 [L1000] CALL     A=20 B=2 C=3 D=515 
00201 [L1000] TSETS    A=20 B=19 C=41 D=4905 'pos'
00202 [L1000] TSETB    A=19 B=18 C=1 D=4609 
00203 [L1000] TSETS    A=18 B=17 C=36 D=4388 'menuItems'
00204 [L1001] TSETS    A=4 B=17 C=42 D=4394 'touchRect'
00205 [L1002] GGET     A=18 B=0 C=9 D=9 'd_ms'
00206 [L1002] TGETS    A=18 B=18 C=43 D=4651 'd_tableView'
00207 [L1002] TGETS    A=18 B=18 C=44 D=4652 'createTableViewMenu'
00208 [L1002] MOV      A=19 B=0 C=17 D=17 
00209 [L1002] CALL     A=18 B=2 C=2 D=514 
00210 [L1003] MOV      A=20 B=0 C=0 D=0 
00211 [L1003] TGETS    A=19 B=0 C=4 D=4 'addChild'
00212 [L1003] MOV      A=21 B=0 C=18 D=18 
00213 [L1003] CALL     A=19 B=1 C=3 D=259 
00214 [L1004] UCLO     A=0 B=128 C=0 D=32768 target=215
00215 [L1004] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto47 offset=0x7b29 source_lines=1009-1011 params=0
UPVALUES ['num']
00001 [L1010] UGET     A=0 B=0 C=0 D=0 num
00002 [L1010] RET1     A=0 B=0 C=2 D=2 

FUNCTION proto48 offset=0x7b47 source_lines=1013-1023 params=1
UPVALUES ['CCNode', 'list', 'createItemCell', 'cellSize', 'touchRect', 'createCharCell']
00001 [L1014] UGET     A=1 B=0 C=0 D=0 CCNode
00002 [L1014] MOV      A=2 B=0 C=1 D=1 
00003 [L1014] TGETS    A=1 B=1 C=0 D=256 'create'
00004 [L1014] CALL     A=1 B=2 C=2 D=514 
00005 [L1015] UGET     A=2 B=0 C=1 D=1 list
00006 [L1015] TGETV    A=2 B=2 C=0 D=512 
00007 [L1015] ISF      A=0 B=0 C=2 D=2 
00008 [L1015] JMP      A=3 B=128 C=23 D=32791 target=32
00009 [L1016] UGET     A=2 B=0 C=1 D=1 list
00010 [L1016] TGETV    A=2 B=2 C=0 D=512 
00011 [L1016] TGETS    A=2 B=2 C=1 D=513 'isItem'
00012 [L1016] ISF      A=0 B=0 C=2 D=2 
00013 [L1016] JMP      A=3 B=128 C=9 D=32777 target=23
00014 [L1017] UGET     A=2 B=0 C=2 D=2 createItemCell
00015 [L1017] MOV      A=3 B=0 C=1 D=1 
00016 [L1017] MOV      A=4 B=0 C=0 D=0 
00017 [L1017] UGET     A=5 B=0 C=1 D=1 list
00018 [L1017] TGETV    A=5 B=5 C=0 D=1280 
00019 [L1017] UGET     A=6 B=0 C=3 D=3 cellSize
00020 [L1017] UGET     A=7 B=0 C=4 D=4 touchRect
00021 [L1017] CALL     A=2 B=1 C=6 D=262 
00022 [L1017] JMP      A=2 B=128 C=9 D=32777 target=32
00023 [L1019] UGET     A=2 B=0 C=5 D=5 createCharCell
00024 [L1019] MOV      A=3 B=0 C=1 D=1 
00025 [L1019] MOV      A=4 B=0 C=0 D=0 
00026 [L1019] UGET     A=5 B=0 C=1 D=1 list
00027 [L1019] TGETV    A=5 B=5 C=0 D=1280 
00028 [L1019] KSTR     A=6 B=0 C=2 D=2 'v2/charPositionUI/char_info.png'
00029 [L1019] UGET     A=7 B=0 C=3 D=3 cellSize
00030 [L1019] UGET     A=8 B=0 C=4 D=4 touchRect
00031 [L1019] CALL     A=2 B=1 C=7 D=263 
00032 [L1022] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto49 offset=0x7c7a source_lines=1025-1027 params=1
UPVALUES ['cellSize']
00001 [L1026] UGET     A=1 B=0 C=0 D=0 cellSize
00002 [L1026] TGETS    A=1 B=1 C=0 D=256 'height'
00003 [L1026] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto50 offset=0x7cb1 source_lines=1006-1030 params=3
UPVALUES ['CCNode', 'createItemCell', 'createCharCell']
00001 [L1007] TNEW     A=3 B=0 C=0 D=0 
00002 [L1008] LEN      A=4 B=0 C=0 D=0 
00003 [L1011] FNEW     A=5 B=0 C=1 D=1 {'kind': 'proto', 'id': 47}
00004 [L1011] TSETS    A=5 B=3 C=0 D=768 'tableViewNumberOfRows'
00005 [L1023] FNEW     A=5 B=0 C=3 D=3 {'kind': 'proto', 'id': 48}
00006 [L1023] TSETS    A=5 B=3 C=2 D=770 'drawCellAtIndex'
00007 [L1027] FNEW     A=5 B=0 C=5 D=5 {'kind': 'proto', 'id': 49}
00008 [L1027] TSETS    A=5 B=3 C=4 D=772 'heightForRowAtIndex'
00009 [L1029] UCLO     A=0 B=128 C=0 D=32768 target=10
00010 [L1029] RET1     A=3 B=0 C=2 D=2 

FUNCTION proto51 offset=0x7d8a source_lines=0-1040 params=0
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
00042 [L48] GGET     A=41 B=0 C=41 D=41 'kCCVerticalTextAlignmentCenter'
00043 [L49] GGET     A=42 B=0 C=42 D=42 'CCMenuItemLabel'
00044 [L50] GGET     A=43 B=0 C=43 D=43 'CCLabelTTF'
00045 [L51] GGET     A=44 B=0 C=44 D=44 'CCMenuItemSprite'
00046 [L52] GGET     A=45 B=0 C=45 D=45 'CCRenderTexture'
00047 [L53] GGET     A=46 B=0 C=46 D=46 'CCPointMake'
00048 [L54] GGET     A=47 B=0 C=47 D=47 'CCRotateBy'
00049 [L55] GGET     A=48 B=0 C=48 D=48 'CCEaseOut'
00050 [L56] GGET     A=49 B=0 C=49 D=49 'CCCallFunc'
00051 [L58] GGET     A=50 B=0 C=50 D=50 'module'
00052 [L58] KSTR     A=51 B=0 C=51 D=51 'ui.turntableUI'
00053 [L58] CALL     A=50 B=1 C=2 D=258 
00054 [L61] MOV      A=50 B=0 C=0 D=0 
00055 [L61] KSTR     A=51 B=0 C=52 D=52 'ms'
00056 [L61] CALL     A=50 B=2 C=2 D=514 
00057 [L61] GSET     A=50 B=0 C=53 D=53 'd_ms'
00058 [L62] GGET     A=50 B=0 C=53 D=53 'd_ms'
00059 [L62] IST      A=0 B=0 C=50 D=50 
00060 [L62] JMP      A=50 B=128 C=3 D=32771 target=64
00061 [L63] MOV      A=50 B=0 C=2 D=2 
00062 [L63] KSTR     A=51 B=0 C=54 D=54 'turntableUI load d_ms fail.\n'
00063 [L63] CALL     A=50 B=1 C=2 D=258 
00064 [L68] FNEW     A=50 B=0 C=55 D=55 {'kind': 'proto', 'id': 0}
00065 [L71] GGET     A=51 B=0 C=53 D=53 'd_ms'
00066 [L71] TGETS    A=51 B=51 C=56 D=13112 'd_hz'
00067 [L71] TGETS    A=51 B=51 C=57 D=13113 'gethz'
00068 [L72] GGET     A=52 B=0 C=53 D=53 'd_ms'
00069 [L72] TGETS    A=52 B=52 C=58 D=13370 'd_info'
00070 [L72] TGETS    A=52 B=52 C=59 D=13371 'show'
00071 [L73] GGET     A=53 B=0 C=53 D=53 'd_ms'
00072 [L73] TGETS    A=53 B=53 C=60 D=13628 'd_common_def'
00073 [L73] TGETS    A=53 B=53 C=61 D=13629 'object_type'
00074 [L74] GGET     A=54 B=0 C=53 D=53 'd_ms'
00075 [L74] TGETS    A=54 B=54 C=60 D=13884 'd_common_def'
00076 [L74] TGETS    A=54 B=54 C=62 D=13886 'item_main_type'
00077 [L75] MOV      A=56 B=0 C=18 D=18 
00078 [L75] TGETS    A=55 B=18 C=63 D=4671 'sharedDirector'
00079 [L75] CALL     A=55 B=2 C=2 D=514 
00080 [L75] MOV      A=56 B=0 C=55 D=55 
00081 [L75] TGETS    A=55 B=55 C=64 D=14144 'getVisibleSize'
00082 [L75] CALL     A=55 B=2 C=2 D=514 
00083 [L76] GGET     A=56 B=0 C=53 D=53 'd_ms'
00084 [L76] TGETS    A=56 B=56 C=65 D=14401 'd_c'
00085 [L76] TGETS    A=56 B=56 C=66 D=14402 'g_tags'
00086 [L76] TGETS    A=56 B=56 C=67 D=14403 'TAG_turntableUI'
00087 [L76] GSET     A=56 B=0 C=68 D=68 'g_turntableUI'
00088 [L77] TNEW     A=56 B=0 C=0 D=0 
00089 [L77] GSET     A=56 B=0 C=69 D=69 'g_self'
00090 [L78] TNEW     A=56 B=0 C=0 D=0 
00091 [L78] GSET     A=56 B=0 C=70 D=70 'g_boxUI'
00092 [L79] TNEW     A=56 B=0 C=0 D=0 
00093 [L79] GSET     A=56 B=0 C=71 D=71 'g_Color'
00094 [L80] GGET     A=56 B=0 C=71 D=71 'g_Color'
00095 [L80] TDUP     A=57 B=0 C=73 D=73 {'kind': 'table', 'value': {1: 0, 2: 0, 3: 0}}
00096 [L80] TSETS    A=57 B=56 C=72 D=14408 'black'
00097 [L81] GGET     A=56 B=0 C=71 D=71 'g_Color'
00098 [L81] TDUP     A=57 B=0 C=75 D=75 {'kind': 'table', 'value': {1: 255, 2: 255, 3: 255}}
00099 [L81] TSETS    A=57 B=56 C=74 D=14410 'white'
00100 [L82] GGET     A=56 B=0 C=71 D=71 'g_Color'
00101 [L82] TDUP     A=57 B=0 C=77 D=77 {'kind': 'table', 'value': {1: 0, 2: 255, 3: 0}}
00102 [L82] TSETS    A=57 B=56 C=76 D=14412 'green'
00103 [L83] GGET     A=56 B=0 C=71 D=71 'g_Color'
00104 [L83] TDUP     A=57 B=0 C=79 D=79 {'kind': 'table', 'value': {1: 255, 2: 0, 3: 0}}
00105 [L83] TSETS    A=57 B=56 C=78 D=14414 'red'
00106 [L84] GGET     A=56 B=0 C=71 D=71 'g_Color'
00107 [L84] TDUP     A=57 B=0 C=81 D=81 {'kind': 'table', 'value': {1: 253, 2: 255, 3: 0}}
00108 [L84] TSETS    A=57 B=56 C=80 D=14416 'yellow'
00109 [L85] KPRI     A=56 B=0 C=1 D=1 
00110 [L85] GSET     A=56 B=0 C=82 D=82 'g_showBoxUseLayer_maxnum'
00111 [L87] GGET     A=56 B=0 C=69 D=69 'g_self'
00112 [L87] KSHORT   A=57 B=0 C=1 D=1 1
00113 [L87] TSETS    A=57 B=56 C=83 D=14419 'main_tag'
00114 [L88] GGET     A=56 B=0 C=69 D=69 'g_self'
00115 [L88] KSHORT   A=57 B=0 C=2 D=2 2
00116 [L88] TSETS    A=57 B=56 C=84 D=14420 'timetip_tag'
00117 [L89] GGET     A=56 B=0 C=69 D=69 'g_self'
00118 [L89] KSHORT   A=57 B=0 C=3 D=3 3
00119 [L89] TSETS    A=57 B=56 C=85 D=14421 'giftDetailTag'
00120 [L92] KSHORT   A=56 B=5 C=87 D=1367 1367
00121 [L92] GSET     A=56 B=0 C=86 D=86 'g_littlerulaibag'
00122 [L93] KSHORT   A=56 B=5 C=88 D=1368 1368
00123 [L93] GSET     A=56 B=0 C=87 D=87 'g_bigrulaibag'
00124 [L145] FNEW     A=56 B=0 C=88 D=88 {'kind': 'proto', 'id': 1}
00125 [L97] GSET     A=56 B=0 C=89 D=89 'onGetResult'
00126 [L158] FNEW     A=56 B=0 C=90 D=90 {'kind': 'proto', 'id': 2}
00127 [L147] GSET     A=56 B=0 C=91 D=91 'canJoin'
00128 [L165] FNEW     A=56 B=0 C=92 D=92 {'kind': 'proto', 'id': 3}
00129 [L159] GSET     A=56 B=0 C=93 D=93 'getShowHint'
00130 [L176] FNEW     A=56 B=0 C=94 D=94 {'kind': 'proto', 'id': 4}
00131 [L166] GSET     A=56 B=0 C=95 D=95 'getActivityTime'
00132 [L182] FNEW     A=56 B=0 C=96 D=96 {'kind': 'proto', 'id': 5}
00133 [L177] GSET     A=56 B=0 C=97 D=97 'enter'
00134 [L190] FNEW     A=56 B=0 C=98 D=98 {'kind': 'proto', 'id': 6}
00135 [L184] GSET     A=56 B=0 C=59 D=59 'show'
00136 [L197] FNEW     A=56 B=0 C=99 D=99 {'kind': 'proto', 'id': 7}
00137 [L191] GSET     A=56 B=0 C=100 D=100 'update'
00138 [L319] FNEW     A=56 B=0 C=101 D=101 {'kind': 'proto', 'id': 11}
00139 [L199] GSET     A=56 B=0 C=102 D=102 'create'
00140 [L342] FNEW     A=56 B=0 C=103 D=103 {'kind': 'proto', 'id': 15}
00141 [L321] GSET     A=56 B=0 C=104 D=104 'getHistoryCellsDataSource'
00142 [L354] FNEW     A=56 B=0 C=105 D=105 {'kind': 'proto', 'id': 16}
00143 [L344] GSET     A=56 B=0 C=106 D=106 'createHistoryCell'
00144 [L364] FNEW     A=56 B=0 C=107 D=107 {'kind': 'proto', 'id': 17}
00145 [L356] GSET     A=56 B=0 C=108 D=108 'call_back_close'
00146 [L371] FNEW     A=56 B=0 C=109 D=109 {'kind': 'proto', 'id': 18}
00147 [L366] GSET     A=56 B=0 C=110 D=110 'recharge'
00148 [L389] FNEW     A=56 B=0 C=111 D=111 {'kind': 'proto', 'id': 19}
00149 [L374] GSET     A=56 B=0 C=112 D=112 'update_rewarded_show'
00150 [L512] FNEW     A=56 B=0 C=113 D=113 {'kind': 'proto', 'id': 23}
00151 [L391] GSET     A=56 B=0 C=114 D=114 'showTurntableLayer'
00152 [L517] FNEW     A=56 B=0 C=115 D=115 {'kind': 'proto', 'id': 24}
00153 [L514] GSET     A=56 B=0 C=116 D=116 'update_tt_totaltime_label'
00154 [L553] FNEW     A=56 B=0 C=117 D=117 {'kind': 'proto', 'id': 27}
00155 [L519] GSET     A=56 B=0 C=118 D=118 'start_turntable_anim'
00156 [L563] FNEW     A=56 B=0 C=119 D=119 {'kind': 'proto', 'id': 28}
00157 [L555] GSET     A=56 B=0 C=120 D=120 'close_schedulescriptfunc'
00158 [L645] FNEW     A=56 B=0 C=121 D=121 {'kind': 'proto', 'id': 32}
00159 [L565] GSET     A=56 B=0 C=122 D=122 'showreward'
00160 [L700] FNEW     A=56 B=0 C=123 D=123 {'kind': 'proto', 'id': 36}
00161 [L648] GSET     A=56 B=0 C=124 D=124 'showRewardDetail'
00162 [L737] FNEW     A=56 B=0 C=125 D=125 {'kind': 'proto', 'id': 37}
00163 [L702] GSET     A=56 B=0 C=126 D=126 'getBoxTransConfig'
00164 [L869] FNEW     A=56 B=0 C=127 D=127 {'kind': 'proto', 'id': 42}
00165 [L739] GSET     A=56 B=0 C=128 D=128 'showBoxUseLayer'
00166 [L949] FNEW     A=56 B=0 C=129 D=129 {'kind': 'proto', 'id': 44}
00167 [L1004] FNEW     A=57 B=0 C=130 D=130 {'kind': 'proto', 'id': 46}
00168 [L1030] FNEW     A=58 B=0 C=131 D=131 {'kind': 'proto', 'id': 50}
00169 [L1006] GSET     A=58 B=0 C=132 D=132 'getCortDataSource'
00170 [L1030] UCLO     A=0 B=128 C=0 D=32768 target=171
00171 [L1030] RET0     A=0 B=0 C=1 D=1 
