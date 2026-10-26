LuaJIT dump version=1; source='@D:\\mg_update_\\lua_cache\\lua1\\ae0f40d1631f06ad6e89a50dc5ea4c26.data'; root=proto66

FUNCTION proto0 offset=0x4a source_lines=43-45 params=0
UPVALUES ['CCLuaLog', 'string']
00001 [L44] UGET     A=0 B=0 C=0 D=0 CCLuaLog
00002 [L44] UGET     A=1 B=0 C=1 D=1 string
00003 [L44] TGETS    A=1 B=1 C=0 D=256 'format'
00004 [L44] VARG     A=2 B=0 C=0 D=0 
00005 [L44] CALLM    A=1 B=0 C=0 D=0 
00006 [L44] CALLM    A=0 B=1 C=0 D=256 
00007 [L45] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto1 offset=0x95 source_lines=69-77 params=0
UPVALUES []
00001 [L71] GGET     A=0 B=0 C=0 D=0 'g_self'
00002 [L71] TGETS    A=0 B=0 C=1 D=1 'specialFightType'
00003 [L71] GGET     A=1 B=0 C=2 D=2 'd_ms'
00004 [L71] TGETS    A=1 B=1 C=3 D=259 'd_common_def'
00005 [L71] TGETS    A=1 B=1 C=4 D=260 'fight_type'
00006 [L71] TGETS    A=1 B=1 C=5 D=261 'team_fight'
00007 [L71] ISNEV    A=0 B=0 C=1 D=1 
00008 [L71] JMP      A=0 B=128 C=5 D=32773 target=14
00009 [L73] GGET     A=0 B=0 C=2 D=2 'd_ms'
00010 [L73] TGETS    A=0 B=0 C=6 D=6 'd_secretAreaUI'
00011 [L73] TGETS    A=0 B=0 C=7 D=7 'getLastFightInfo'
00012 [L73] CALLT    A=0 B=0 C=1 D=1 
00013 [L73] JMP      A=0 B=128 C=7 D=32775 target=21
00014 [L75] GGET     A=0 B=0 C=8 D=8 'g_fight_info'
00015 [L75] GGET     A=1 B=0 C=9 D=9 'g_fight_id_list'
00016 [L75] GGET     A=2 B=0 C=9 D=9 'g_fight_id_list'
00017 [L75] LEN      A=2 B=0 C=2 D=2 
00018 [L75] TGETV    A=1 B=1 C=2 D=258 
00019 [L75] TGETV    A=0 B=0 C=1 D=1 
00020 [L75] RET1     A=0 B=0 C=2 D=2 
00021 [L77] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto2 offset=0x187 source_lines=81-86 params=1
UPVALUES []
00001 [L82] ISNEP    A=0 B=0 C=0 D=0 
00002 [L82] JMP      A=1 B=128 C=1 D=32769 target=4
00003 [L83] RET0     A=0 B=0 C=1 D=1 
00004 [L85] GGET     A=1 B=0 C=0 D=0 'g_self'
00005 [L85] TSETS    A=0 B=1 C=1 D=257 'specialFightType'
00006 [L86] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto3 offset=0x1d3 source_lines=90-102 params=0
UPVALUES []
00001 [L92] GGET     A=0 B=0 C=0 D=0 'g_self'
00002 [L92] TGETS    A=0 B=0 C=1 D=1 'specialFightType'
00003 [L92] KSHORT   A=1 B=0 C=0 D=0 0
00004 [L92] ISGE     A=1 B=0 C=0 D=0 
00005 [L92] JMP      A=0 B=128 C=3 D=32771 target=9
00006 [L93] GGET     A=0 B=0 C=0 D=0 'g_self'
00007 [L93] TGETS    A=0 B=0 C=1 D=1 'specialFightType'
00008 [L93] RET1     A=0 B=0 C=2 D=2 
00009 [L96] GGET     A=0 B=0 C=2 D=2 'g_fight_info'
00010 [L96] GGET     A=1 B=0 C=3 D=3 'g_fight_id_list'
00011 [L96] GGET     A=2 B=0 C=3 D=3 'g_fight_id_list'
00012 [L96] LEN      A=2 B=0 C=2 D=2 
00013 [L96] TGETV    A=1 B=1 C=2 D=258 
00014 [L96] TGETV    A=0 B=0 C=1 D=1 
00015 [L97] ISF      A=0 B=0 C=0 D=0 
00016 [L97] JMP      A=1 B=128 C=10 D=32778 target=27
00017 [L97] TGETS    A=1 B=0 C=4 D=4 'fight_result_msg'
00018 [L97] ISF      A=0 B=0 C=1 D=1 
00019 [L97] JMP      A=2 B=128 C=7 D=32775 target=27
00020 [L97] TGETS    A=1 B=0 C=4 D=4 'fight_result_msg'
00021 [L97] TGETS    A=1 B=1 C=5 D=261 'fight_type'
00022 [L97] ISF      A=0 B=0 C=1 D=1 
00023 [L97] JMP      A=2 B=128 C=3 D=32771 target=27
00024 [L98] TGETS    A=1 B=0 C=4 D=4 'fight_result_msg'
00025 [L98] TGETS    A=1 B=1 C=5 D=261 'fight_type'
00026 [L98] RET1     A=1 B=0 C=2 D=2 
00027 [L101] GGET     A=1 B=0 C=6 D=6 'd_ms'
00028 [L101] TGETS    A=1 B=1 C=7 D=263 'd_common_def'
00029 [L101] TGETS    A=1 B=1 C=5 D=261 'fight_type'
00030 [L101] TGETS    A=1 B=1 C=8 D=264 'tollgate_guide'
00031 [L101] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto4 offset=0x2f3 source_lines=106-112 params=0
UPVALUES []
00001 [L107] GGET     A=0 B=0 C=0 D=0 'getLastFightInfo'
00002 [L107] CALL     A=0 B=2 C=1 D=513 
00003 [L108] ISF      A=0 B=0 C=0 D=0 
00004 [L108] JMP      A=1 B=128 C=9 D=32777 target=14
00005 [L108] TGETS    A=1 B=0 C=1 D=1 'line_up_msg'
00006 [L108] ISF      A=0 B=0 C=1 D=1 
00007 [L108] JMP      A=2 B=128 C=6 D=32774 target=14
00008 [L109] TGETS    A=1 B=0 C=1 D=1 'line_up_msg'
00009 [L109] TGETS    A=1 B=1 C=2 D=258 'src_name'
00010 [L109] IST      A=0 B=0 C=1 D=1 
00011 [L109] JMP      A=2 B=128 C=1 D=32769 target=13
00012 [L109] KSTR     A=1 B=0 C=3 D=3 ''
00013 [L109] RET1     A=1 B=0 C=2 D=2 
00014 [L111] KSTR     A=1 B=0 C=3 D=3 ''
00015 [L111] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto5 offset=0x37e source_lines=116-122 params=0
UPVALUES []
00001 [L117] GGET     A=0 B=0 C=0 D=0 'getLastFightInfo'
00002 [L117] CALL     A=0 B=2 C=1 D=513 
00003 [L118] ISF      A=0 B=0 C=0 D=0 
00004 [L118] JMP      A=1 B=128 C=9 D=32777 target=14
00005 [L118] TGETS    A=1 B=0 C=1 D=1 'line_up_msg'
00006 [L118] ISF      A=0 B=0 C=1 D=1 
00007 [L118] JMP      A=2 B=128 C=6 D=32774 target=14
00008 [L119] TGETS    A=1 B=0 C=1 D=1 'line_up_msg'
00009 [L119] TGETS    A=1 B=1 C=2 D=258 'des_name'
00010 [L119] IST      A=0 B=0 C=1 D=1 
00011 [L119] JMP      A=2 B=128 C=1 D=32769 target=13
00012 [L119] KSTR     A=1 B=0 C=3 D=3 ''
00013 [L119] RET1     A=1 B=0 C=2 D=2 
00014 [L121] KSTR     A=1 B=0 C=3 D=3 ''
00015 [L121] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto6 offset=0x409 source_lines=129-142 params=1
UPVALUES ['cclog', 'table']
00001 [L130] UGET     A=1 B=0 C=0 D=0 cclog
00002 [L130] KSTR     A=2 B=0 C=0 D=0 'callback_fight_extra_logic'
00003 [L130] CALL     A=1 B=1 C=2 D=258 
00004 [L131] TNEW     A=1 B=0 C=0 D=0 
00005 [L131] GSET     A=1 B=0 C=1 D=1 'g_fight_events'
00006 [L132] TGETS    A=1 B=0 C=2 D=2 'fight_id'
00007 [L132] ISF      A=0 B=0 C=1 D=1 
00008 [L132] JMP      A=2 B=128 C=21 D=32789 target=30
00009 [L133] GSET     A=0 B=0 C=1 D=1 'g_fight_events'
00010 [L135] GGET     A=1 B=0 C=3 D=3 'g_all_fight_events'
00011 [L135] LEN      A=1 B=0 C=1 D=1 
00012 [L135] KSHORT   A=2 B=0 C=20 D=20 20
00013 [L135] ISGE     A=2 B=0 C=1 D=1 
00014 [L135] JMP      A=1 B=128 C=10 D=32778 target=25
00015 [L136] KSHORT   A=1 B=0 C=1 D=1 1
00016 [L136] KSHORT   A=2 B=0 C=5 D=5 5
00017 [L136] KSHORT   A=3 B=0 C=1 D=1 1
00018 [L136] FORI     A=1 B=128 C=6 D=32774 target=25
00019 [L137] UGET     A=5 B=0 C=1 D=1 table
00020 [L137] TGETS    A=5 B=5 C=4 D=1284 'remove'
00021 [L137] GGET     A=6 B=0 C=3 D=3 'g_all_fight_events'
00022 [L137] KSHORT   A=7 B=0 C=1 D=1 1
00023 [L137] CALL     A=5 B=1 C=3 D=259 
00024 [L136] FORL     A=1 B=127 C=250 D=32762 target=19
00025 [L140] UGET     A=1 B=0 C=1 D=1 table
00026 [L140] TGETS    A=1 B=1 C=5 D=261 'insert'
00027 [L140] GGET     A=2 B=0 C=3 D=3 'g_all_fight_events'
00028 [L140] MOV      A=3 B=0 C=0 D=0 
00029 [L140] CALL     A=1 B=1 C=3 D=259 
00030 [L142] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto7 offset=0x525 source_lines=147-154 params=1
UPVALUES []
00001 [L148] GGET     A=1 B=0 C=0 D=0 'g_all_fight_events'
00002 [L148] LEN      A=1 B=0 C=1 D=1 
00003 [L148] KSHORT   A=2 B=0 C=1 D=1 1
00004 [L148] KSHORT   A=3 B=255 C=255 D=65535 -1
00005 [L148] FORI     A=1 B=128 C=9 D=32777 target=15
00006 [L149] GGET     A=5 B=0 C=0 D=0 'g_all_fight_events'
00007 [L149] TGETV    A=5 B=5 C=4 D=1284 
00008 [L149] TGETS    A=5 B=5 C=1 D=1281 'fight_id'
00009 [L149] ISNEV    A=5 B=0 C=0 D=0 
00010 [L149] JMP      A=5 B=128 C=3 D=32771 target=14
00011 [L150] GGET     A=5 B=0 C=0 D=0 'g_all_fight_events'
00012 [L150] TGETV    A=5 B=5 C=4 D=1284 
00013 [L150] RET1     A=5 B=0 C=2 D=2 
00014 [L148] FORL     A=1 B=127 C=247 D=32759 target=6
00015 [L153] TNEW     A=1 B=0 C=0 D=0 
00016 [L153] RET1     A=1 B=0 C=2 D=2 

FUNCTION proto8 offset=0x5b6 source_lines=158-160 params=0
UPVALUES []
00001 [L159] TNEW     A=0 B=0 C=0 D=0 
00002 [L159] GSET     A=0 B=0 C=0 D=0 'g_all_fight_events'
00003 [L160] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto9 offset=0x5e6 source_lines=164-214 params=3
UPVALUES ['cclog', 'main_server', 'table', 'string']
00001 [L165] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L165] KSTR     A=4 B=0 C=0 D=0 'call dispatch_event'
00003 [L165] CALL     A=3 B=1 C=2 D=258 
00004 [L167] TNEW     A=3 B=0 C=0 D=0 
00005 [L168] UGET     A=4 B=0 C=1 D=1 main_server
00006 [L168] TGETS    A=4 B=4 C=1 D=1025 'recv_msg'
00007 [L168] MOV      A=5 B=0 C=0 D=0 
00008 [L168] MOV      A=6 B=0 C=1 D=1 
00009 [L168] MOV      A=7 B=0 C=3 D=3 
00010 [L168] CALL     A=4 B=1 C=4 D=260 
00011 [L170] GGET     A=4 B=0 C=2 D=2 'g_msg_fun'
00012 [L170] TGETV    A=4 B=4 C=0 D=1024 
00013 [L170] ISEQP    A=4 B=0 C=0 D=0 
00014 [L170] JMP      A=4 B=128 C=70 D=32838 target=85
00015 [L172] ISNEN    A=0 B=0 C=0 D=0 20
00016 [L172] JMP      A=4 B=128 C=4 D=32772 target=21
00017 [L172] TGETS    A=4 B=3 C=3 D=771 'type'
00018 [L172] ISNEN    A=4 B=0 C=1 D=1 100
00019 [L172] JMP      A=4 B=128 C=1 D=32769 target=21
00020 [L172] JMP      A=4 B=128 C=57 D=32825 target=78
00021 [L176] UGET     A=4 B=0 C=0 D=0 cclog
00022 [L176] KSTR     A=5 B=0 C=4 D=4 '<----------%d-----------%d'
00023 [L176] MOV      A=6 B=0 C=0 D=0 
00024 [L176] TGETS    A=7 B=3 C=5 D=773 'serial_num'
00025 [L176] IST      A=0 B=0 C=7 D=7 
00026 [L176] JMP      A=8 B=128 C=1 D=32769 target=28
00027 [L176] KSHORT   A=7 B=0 C=0 D=0 0
00028 [L176] CALL     A=4 B=1 C=4 D=260 
00029 [L177] GGET     A=4 B=0 C=6 D=6 'd_ms'
00030 [L177] TGETS    A=4 B=4 C=7 D=1031 'd_u'
00031 [L177] TGETS    A=4 B=4 C=8 D=1032 'packageReturn'
00032 [L177] MOV      A=5 B=0 C=0 D=0 
00033 [L177] TGETS    A=6 B=3 C=5 D=773 'serial_num'
00034 [L177] CALL     A=4 B=2 C=3 D=515 
00035 [L177] ISNEP    A=4 B=0 C=1 D=1 
00036 [L177] JMP      A=4 B=128 C=1 D=32769 target=38
00037 [L179] RET0     A=0 B=0 C=1 D=1 
00038 [L182] TGETS    A=4 B=3 C=5 D=773 'serial_num'
00039 [L182] ISF      A=0 B=0 C=4 D=4 
00040 [L182] JMP      A=5 B=128 C=5 D=32773 target=46
00041 [L182] TGETS    A=4 B=3 C=5 D=773 'serial_num'
00042 [L182] KNUM     A=5 B=0 C=2 D=2 200000
00043 [L182] ISGT     A=5 B=0 C=4 D=4 
00044 [L182] JMP      A=4 B=128 C=1 D=32769 target=46
00045 [L183] GSET     A=0 B=0 C=9 D=9 'g_next_msg_type'
00046 [L186] GGET     A=4 B=0 C=6 D=6 'd_ms'
00047 [L186] TGETS    A=4 B=4 C=10 D=1034 'd_msg_def'
00048 [L186] TGETS    A=4 B=4 C=11 D=1035 'gscl_msg_id'
00049 [L186] TGETS    A=4 B=4 C=12 D=1036 'msg_process_done'
00050 [L186] ISNEV    A=0 B=0 C=4 D=4 
00051 [L186] JMP      A=4 B=128 C=1 D=32769 target=53
00052 [L186] JMP      A=4 B=128 C=25 D=32793 target=78
00053 [L188] GGET     A=4 B=0 C=6 D=6 'd_ms'
00054 [L188] TGETS    A=4 B=4 C=7 D=1031 'd_u'
00055 [L188] TGETS    A=4 B=4 C=13 D=1037 'g_is_waiting_1106'
00056 [L188] ISNEP    A=4 B=0 C=2 D=2 
00057 [L188] JMP      A=4 B=128 C=20 D=32788 target=78
00058 [L188] TGETS    A=4 B=3 C=5 D=773 'serial_num'
00059 [L188] ISF      A=0 B=0 C=4 D=4 
00060 [L188] JMP      A=5 B=128 C=17 D=32785 target=78
00061 [L188] TGETS    A=4 B=3 C=5 D=773 'serial_num'
00062 [L188] KNUM     A=5 B=0 C=2 D=2 200000
00063 [L188] ISGT     A=5 B=0 C=4 D=4 
00064 [L188] JMP      A=4 B=128 C=13 D=32781 target=78
00065 [L191] TNEW     A=4 B=0 C=0 D=0 
00066 [L192] TSETS    A=0 B=4 C=14 D=1038 'msgid'
00067 [L193] TSETS    A=3 B=4 C=15 D=1039 'msg_table'
00068 [L194] TSETS    A=2 B=4 C=16 D=1040 'time'
00069 [L195] UGET     A=5 B=0 C=2 D=2 table
00070 [L195] TGETS    A=5 B=5 C=17 D=1297 'insert'
00071 [L195] GGET     A=6 B=0 C=18 D=18 'g_net_package_list'
00072 [L195] MOV      A=7 B=0 C=4 D=4 
00073 [L195] CALL     A=5 B=1 C=3 D=259 
00074 [L196] GGET     A=5 B=0 C=6 D=6 'd_ms'
00075 [L196] TGETS    A=5 B=5 C=19 D=1299 'func_ret'
00076 [L196] TGETS    A=5 B=5 C=20 D=1300 'ok'
00077 [L196] RET1     A=5 B=0 C=2 D=2 
00078 [L201] GGET     A=4 B=0 C=2 D=2 'g_msg_fun'
00079 [L201] TGETV    A=4 B=4 C=0 D=1024 
00080 [L201] MOV      A=5 B=0 C=0 D=0 
00081 [L201] MOV      A=6 B=0 C=3 D=3 
00082 [L201] MOV      A=7 B=0 C=2 D=2 
00083 [L201] CALL     A=4 B=1 C=4 D=260 
00084 [L201] JMP      A=4 B=128 C=31 D=32799 target=116
00085 [L203] UGET     A=4 B=0 C=0 D=0 cclog
00086 [L203] KSTR     A=5 B=0 C=4 D=4 '<----------%d-----------%d'
00087 [L203] MOV      A=6 B=0 C=0 D=0 
00088 [L203] TGETS    A=7 B=3 C=5 D=773 'serial_num'
00089 [L203] IST      A=0 B=0 C=7 D=7 
00090 [L203] JMP      A=8 B=128 C=1 D=32769 target=92
00091 [L203] KSHORT   A=7 B=0 C=0 D=0 0
00092 [L203] CALL     A=4 B=1 C=4 D=260 
00093 [L204] UGET     A=4 B=0 C=0 D=0 cclog
00094 [L204] KSTR     A=5 B=0 C=21 D=21 'ERROR: unhandle msg=%d'
00095 [L204] MOV      A=6 B=0 C=0 D=0 
00096 [L204] CALL     A=4 B=1 C=3 D=259 
00097 [L205] GGET     A=4 B=0 C=6 D=6 'd_ms'
00098 [L205] TGETS    A=4 B=4 C=22 D=1046 'MS__G__TRACKBACK__'
00099 [L205] UGET     A=5 B=0 C=3 D=3 string
00100 [L205] TGETS    A=5 B=5 C=23 D=1303 'format'
00101 [L205] KSTR     A=6 B=0 C=21 D=21 'ERROR: unhandle msg=%d'
00102 [L205] MOV      A=7 B=0 C=0 D=0 
00103 [L205] CALL     A=5 B=0 C=3 D=3 
00104 [L205] CALLM    A=4 B=1 C=0 D=256 
00105 [L208] ISF      A=0 B=0 C=3 D=3 
00106 [L208] JMP      A=4 B=128 C=9 D=32777 target=116
00107 [L208] TGETS    A=4 B=3 C=5 D=773 'serial_num'
00108 [L208] ISF      A=0 B=0 C=4 D=4 
00109 [L208] JMP      A=5 B=128 C=6 D=32774 target=116
00110 [L209] GGET     A=4 B=0 C=6 D=6 'd_ms'
00111 [L209] TGETS    A=4 B=4 C=7 D=1031 'd_u'
00112 [L209] TGETS    A=4 B=4 C=8 D=1032 'packageReturn'
00113 [L209] MOV      A=5 B=0 C=0 D=0 
00114 [L209] TGETS    A=6 B=3 C=5 D=773 'serial_num'
00115 [L209] CALL     A=4 B=1 C=3 D=259 
00116 [L213] GGET     A=4 B=0 C=6 D=6 'd_ms'
00117 [L213] TGETS    A=4 B=4 C=19 D=1043 'func_ret'
00118 [L213] TGETS    A=4 B=4 C=20 D=1044 'ok'
00119 [L213] RET1     A=4 B=0 C=2 D=2 

FUNCTION proto10 offset=0x9c1 source_lines=233-235 params=0
UPVALUES ['tmp_package']
00001 [L234] GGET     A=0 B=0 C=0 D=0 'g_msg_fun'
00002 [L234] UGET     A=1 B=0 C=0 D=0 tmp_package
00003 [L234] TGETS    A=1 B=1 C=1 D=257 'msgid'
00004 [L234] TGETV    A=0 B=0 C=1 D=1 
00005 [L234] UGET     A=1 B=0 C=0 D=0 tmp_package
00006 [L234] TGETS    A=1 B=1 C=1 D=257 'msgid'
00007 [L234] UGET     A=2 B=0 C=0 D=0 tmp_package
00008 [L234] TGETS    A=2 B=2 C=2 D=514 'msg_table'
00009 [L234] UGET     A=3 B=0 C=0 D=0 tmp_package
00010 [L234] TGETS    A=3 B=3 C=3 D=771 'time'
00011 [L234] CALL     A=0 B=1 C=4 D=260 
00012 [L235] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto11 offset=0xa38 source_lines=219-242 params=0
UPVALUES ['cclog', 'table', 'xpcall']
00001 [L221] GGET     A=0 B=0 C=0 D=0 'g_net_package_list'
00002 [L221] LEN      A=0 B=0 C=0 D=0 
00003 [L221] KSHORT   A=1 B=0 C=0 D=0 0
00004 [L221] ISGT     A=0 B=0 C=1 D=1 
00005 [L221] JMP      A=0 B=128 C=4 D=32772 target=10
00006 [L222] UGET     A=0 B=0 C=0 D=0 cclog
00007 [L222] KSTR     A=1 B=0 C=1 D=1 'g_net_package_list.length=0, no msg new'
00008 [L222] CALL     A=0 B=1 C=2 D=258 
00009 [L223] UCLO     A=0 B=128 C=37 D=32805 target=47
00010 [L226] GGET     A=0 B=0 C=0 D=0 'g_net_package_list'
00011 [L226] LEN      A=0 B=0 C=0 D=0 
00012 [L226] KSHORT   A=1 B=0 C=0 D=0 0
00013 [L226] ISGE     A=1 B=0 C=0 D=0 
00014 [L226] JMP      A=0 B=128 C=26 D=32794 target=41
00015 [L226] LOOP     A=0 B=128 C=25 D=32793 target=41
00016 [L227] GGET     A=0 B=0 C=0 D=0 'g_net_package_list'
00017 [L227] TGETB    A=0 B=0 C=1 D=1 
00018 [L228] UGET     A=1 B=0 C=1 D=1 table
00019 [L228] TGETS    A=1 B=1 C=2 D=258 'remove'
00020 [L228] GGET     A=2 B=0 C=0 D=0 'g_net_package_list'
00021 [L228] KSHORT   A=3 B=0 C=1 D=1 1
00022 [L228] CALL     A=1 B=1 C=3 D=259 
00023 [L230] UGET     A=1 B=0 C=0 D=0 cclog
00024 [L230] KSTR     A=2 B=0 C=3 D=3 'handleSavedPackages: id='
00025 [L230] TGETS    A=3 B=0 C=4 D=4 'msgid'
00026 [L230] CAT      A=2 B=2 C=3 D=515 
00027 [L230] CALL     A=1 B=1 C=2 D=258 
00028 [L232] GGET     A=1 B=0 C=5 D=5 'g_msg_fun'
00029 [L232] TGETS    A=2 B=0 C=4 D=4 'msgid'
00030 [L232] TGETV    A=1 B=1 C=2 D=258 
00031 [L232] ISEQP    A=1 B=0 C=0 D=0 
00032 [L232] JMP      A=1 B=128 C=7 D=32775 target=40
00033 [L235] FNEW     A=1 B=0 C=6 D=6 {'kind': 'proto', 'id': 10}
00034 [L233] GSET     A=1 B=0 C=7 D=7 'xpcall_handler'
00035 [L236] UGET     A=1 B=0 C=2 D=2 xpcall
00036 [L236] GGET     A=2 B=0 C=7 D=7 'xpcall_handler'
00037 [L236] GGET     A=3 B=0 C=8 D=8 'd_ms'
00038 [L236] TGETS    A=3 B=3 C=9 D=777 'MS__G__TRACKBACK__'
00039 [L236] CALL     A=1 B=1 C=3 D=259 
00040 [L237] UCLO     A=0 B=127 C=225 D=32737 target=10
00041 [L240] UGET     A=0 B=0 C=0 D=0 cclog
00042 [L240] KSTR     A=1 B=0 C=10 D=10 '===========handleSavedPackages ok==========='
00043 [L240] CALL     A=0 B=1 C=2 D=258 
00044 [L241] TNEW     A=0 B=0 C=0 D=0 
00045 [L241] GSET     A=0 B=0 C=0 D=0 'g_net_package_list'
00046 [L242] RET0     A=0 B=0 C=1 D=1 
00047 [L242] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto12 offset=0xc18 source_lines=246-255 params=0
UPVALUES []
00001 [L247] KSHORT   A=0 B=0 C=0 D=0 0
00002 [L248] GGET     A=1 B=0 C=0 D=0 'g_next_msg_type'
00003 [L248] ISF      A=0 B=0 C=1 D=1 
00004 [L248] JMP      A=2 B=128 C=2 D=32770 target=7
00005 [L249] GGET     A=1 B=0 C=0 D=0 'g_next_msg_type'
00006 [L249] RET1     A=1 B=0 C=2 D=2 
00007 [L251] GGET     A=1 B=0 C=1 D=1 'g_net_package_list'
00008 [L251] ISF      A=0 B=0 C=1 D=1 
00009 [L251] JMP      A=2 B=128 C=7 D=32775 target=17
00010 [L251] GGET     A=1 B=0 C=1 D=1 'g_net_package_list'
00011 [L251] TGETB    A=1 B=1 C=1 D=257 
00012 [L251] ISF      A=0 B=0 C=1 D=1 
00013 [L251] JMP      A=2 B=128 C=3 D=32771 target=17
00014 [L252] GGET     A=1 B=0 C=1 D=1 'g_net_package_list'
00015 [L252] TGETB    A=1 B=1 C=1 D=257 
00016 [L252] TGETS    A=0 B=1 C=2 D=258 'msgid'
00017 [L254] RET1     A=0 B=0 C=2 D=2 

FUNCTION proto13 offset=0xcaa source_lines=259-277 params=3
UPVALUES ['cclog']
00001 [L260] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L260] KSTR     A=4 B=0 C=0 D=0 '1106------------r_id=%d, s_id=%d--------'
00003 [L260] TGETS    A=5 B=1 C=1 D=257 'req_serial_num'
00004 [L260] IST      A=0 B=0 C=5 D=5 
00005 [L260] JMP      A=6 B=128 C=1 D=32769 target=7
00006 [L260] KSHORT   A=5 B=255 C=255 D=65535 -1
00007 [L260] TGETS    A=6 B=1 C=2 D=258 'serial_num'
00008 [L260] IST      A=0 B=0 C=6 D=6 
00009 [L260] JMP      A=7 B=128 C=1 D=32769 target=11
00010 [L260] KSHORT   A=6 B=255 C=255 D=65535 -1
00011 [L260] CALL     A=3 B=1 C=4 D=260 
00012 [L263] TGETS    A=3 B=1 C=1 D=257 'req_serial_num'
00013 [L263] ISEQN    A=3 B=0 C=0 D=0 0
00014 [L263] JMP      A=3 B=128 C=13 D=32781 target=28
00015 [L263] GGET     A=3 B=0 C=3 D=3 'd_ms'
00016 [L263] TGETS    A=3 B=3 C=4 D=772 'd_u'
00017 [L263] TGETS    A=3 B=3 C=5 D=773 'g_client_req_serial_num'
00018 [L263] TGETS    A=4 B=1 C=1 D=257 'req_serial_num'
00019 [L263] ISEQV    A=3 B=0 C=4 D=4 
00020 [L263] JMP      A=3 B=128 C=7 D=32775 target=28
00021 [L265] UGET     A=3 B=0 C=0 D=0 cclog
00022 [L265] KSTR     A=4 B=0 C=6 D=6 'WARNNING: d_u.g_client_req_serial_num ~= server.req_serial_num [%d] vs [%d]'
00023 [L265] GGET     A=5 B=0 C=3 D=3 'd_ms'
00024 [L265] TGETS    A=5 B=5 C=4 D=1284 'd_u'
00025 [L265] TGETS    A=5 B=5 C=5 D=1285 'g_client_req_serial_num'
00026 [L265] TGETS    A=6 B=1 C=1 D=257 'req_serial_num'
00027 [L265] CALL     A=3 B=1 C=4 D=260 
00028 [L267] GGET     A=3 B=0 C=3 D=3 'd_ms'
00029 [L267] TGETS    A=3 B=3 C=4 D=772 'd_u'
00030 [L267] GGET     A=4 B=0 C=3 D=3 'd_ms'
00031 [L267] TGETS    A=4 B=4 C=4 D=1028 'd_u'
00032 [L267] TGETS    A=4 B=4 C=5 D=1029 'g_client_req_serial_num'
00033 [L267] ADDVN    A=4 B=4 C=1 D=1025 
00034 [L267] TSETS    A=4 B=3 C=5 D=773 'g_client_req_serial_num'
00035 [L269] GGET     A=3 B=0 C=3 D=3 'd_ms'
00036 [L269] TGETS    A=3 B=3 C=7 D=775 'd_alert'
00037 [L269] TGETS    A=3 B=3 C=8 D=776 'stop_wait'
00038 [L269] KPRI     A=4 B=0 C=2 D=2 
00039 [L269] CALL     A=3 B=1 C=2 D=258 
00040 [L270] GGET     A=3 B=0 C=3 D=3 'd_ms'
00041 [L270] TGETS    A=3 B=3 C=4 D=772 'd_u'
00042 [L270] KSHORT   A=4 B=0 C=0 D=0 0
00043 [L270] TSETS    A=4 B=3 C=9 D=777 'g_last_send_msg_id'
00044 [L272] GGET     A=3 B=0 C=3 D=3 'd_ms'
00045 [L272] TGETS    A=3 B=3 C=4 D=772 'd_u'
00046 [L272] KPRI     A=4 B=0 C=1 D=1 
00047 [L272] TSETS    A=4 B=3 C=10 D=778 'g_is_waiting_1106'
00048 [L273] GGET     A=3 B=0 C=11 D=11 'handleSavedPackages'
00049 [L273] CALL     A=3 B=1 C=1 D=257 
00050 [L276] GGET     A=3 B=0 C=3 D=3 'd_ms'
00051 [L276] TGETS    A=3 B=3 C=4 D=772 'd_u'
00052 [L276] TGETS    A=3 B=3 C=12 D=780 'sendLastSaveReq'
00053 [L276] CALL     A=3 B=1 C=1 D=257 
00054 [L277] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto14 offset=0xef5 source_lines=280-285 params=2
UPVALUES []
00001 [L281] GGET     A=2 B=0 C=0 D=0 'g_msg_fun'
00002 [L281] ISEQP    A=2 B=0 C=0 D=0 
00003 [L281] JMP      A=2 B=128 C=3 D=32771 target=7
00004 [L281] GGET     A=2 B=0 C=0 D=0 'g_msg_fun'
00005 [L281] ISNEN    A=2 B=0 C=0 D=0 0
00006 [L281] JMP      A=2 B=128 C=2 D=32770 target=9
00007 [L282] TNEW     A=2 B=0 C=0 D=0 
00008 [L282] GSET     A=2 B=0 C=0 D=0 'g_msg_fun'
00009 [L284] GGET     A=2 B=0 C=0 D=0 'g_msg_fun'
00010 [L284] TSETV    A=1 B=2 C=0 D=512 
00011 [L285] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto15 offset=0xf53 source_lines=288-298 params=3
UPVALUES ['cclog']
00001 [L289] TGETS    A=3 B=1 C=0 D=256 'result'
00002 [L289] GGET     A=4 B=0 C=1 D=1 'd_ms'
00003 [L289] TGETS    A=4 B=4 C=2 D=1026 'd_common_def'
00004 [L289] TGETS    A=4 B=4 C=3 D=1027 'login_code'
00005 [L289] TGETS    A=4 B=4 C=4 D=1028 'success'
00006 [L289] ISNEV    A=3 B=0 C=4 D=4 
00007 [L289] JMP      A=3 B=128 C=4 D=32772 target=12
00008 [L290] UGET     A=3 B=0 C=0 D=0 cclog
00009 [L290] KSTR     A=4 B=0 C=5 D=5 'call msg_login_rsp_1002 ok.'
00010 [L290] CALL     A=3 B=1 C=2 D=258 
00011 [L290] JMP      A=3 B=128 C=25 D=32793 target=37
00012 [L292] UGET     A=3 B=0 C=0 D=0 cclog
00013 [L292] KSTR     A=4 B=0 C=6 D=6 'call msg_login_rsp_1002, ret=%d'
00014 [L292] TGETS    A=5 B=1 C=0 D=256 'result'
00015 [L292] CALL     A=3 B=1 C=3 D=259 
00016 [L294] GGET     A=3 B=0 C=1 D=1 'd_ms'
00017 [L294] TGETS    A=3 B=3 C=7 D=775 'd_alert'
00018 [L294] TGETS    A=3 B=3 C=8 D=776 'stop_wait'
00019 [L294] CALL     A=3 B=1 C=1 D=257 
00020 [L295] GGET     A=3 B=0 C=1 D=1 'd_ms'
00021 [L295] TGETS    A=3 B=3 C=9 D=777 'd_info'
00022 [L295] TGETS    A=3 B=3 C=10 D=778 'show'
00023 [L295] GGET     A=4 B=0 C=1 D=1 'd_ms'
00024 [L295] TGETS    A=4 B=4 C=11 D=1035 'd_hz'
00025 [L295] TGETS    A=4 B=4 C=12 D=1036 'gethz'
00026 [L295] KSTR     A=5 B=0 C=13 D=13 'login_code_'
00027 [L295] TGETS    A=6 B=1 C=0 D=256 'result'
00028 [L295] CAT      A=5 B=5 C=6 D=1286 
00029 [L295] CALL     A=4 B=2 C=2 D=514 
00030 [L295] KSHORT   A=5 B=0 C=5 D=5 5
00031 [L295] KNUM     A=6 B=0 C=0 D=0 0.35
00032 [L295] CALL     A=3 B=1 C=4 D=260 
00033 [L296] GGET     A=3 B=0 C=1 D=1 'd_ms'
00034 [L296] TGETS    A=3 B=3 C=14 D=782 'd_net'
00035 [L296] TGETS    A=3 B=3 C=15 D=783 'kick'
00036 [L296] CALL     A=3 B=1 C=1 D=257 
00037 [L298] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto16 offset=0x10ee source_lines=300-312 params=3
UPVALUES []
00001 [L311] GGET     A=3 B=0 C=0 D=0 'd_ms'
00002 [L311] TGETS    A=3 B=3 C=1 D=769 'd_net'
00003 [L311] TGETS    A=3 B=3 C=2 D=770 'inside_game_1017'
00004 [L311] MOV      A=4 B=0 C=0 D=0 
00005 [L311] MOV      A=5 B=0 C=1 D=1 
00006 [L311] MOV      A=6 B=0 C=2 D=2 
00007 [L311] CALL     A=3 B=1 C=4 D=260 
00008 [L312] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto17 offset=0x115b source_lines=316-322 params=3
UPVALUES ['cclog']
00001 [L317] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L317] KSTR     A=4 B=0 C=0 D=0 'call msg_reconnect_notify_2996'
00003 [L317] CALL     A=3 B=1 C=2 D=258 
00004 [L318] GGET     A=3 B=0 C=1 D=1 'd_ms'
00005 [L318] TGETS    A=3 B=3 C=2 D=770 'd_net'
00006 [L318] TGETS    A=3 B=3 C=3 D=771 'set_net_status'
00007 [L318] KSTR     A=4 B=0 C=4 D=4 'INSIDE_GAME'
00008 [L318] CALL     A=3 B=1 C=2 D=258 
00009 [L319] GGET     A=3 B=0 C=1 D=1 'd_ms'
00010 [L319] TGETS    A=3 B=3 C=2 D=770 'd_net'
00011 [L319] KSHORT   A=4 B=0 C=0 D=0 0
00012 [L319] TSETS    A=4 B=3 C=5 D=773 'g_try_reconnect_begin'
00013 [L320] GGET     A=3 B=0 C=1 D=1 'd_ms'
00014 [L320] TGETS    A=3 B=3 C=2 D=770 'd_net'
00015 [L320] KPRI     A=4 B=0 C=2 D=2 
00016 [L320] TSETS    A=4 B=3 C=6 D=774 'g_has_inside_game'
00017 [L321] GGET     A=3 B=0 C=1 D=1 'd_ms'
00018 [L321] TGETS    A=3 B=3 C=7 D=775 'd_u'
00019 [L321] TGETS    A=3 B=3 C=8 D=776 'tryRetranReq'
00020 [L321] CALL     A=3 B=1 C=1 D=257 
00021 [L322] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto18 offset=0x1273 source_lines=325-330 params=3
UPVALUES ['cclog', 'os']
00001 [L327] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L327] KSTR     A=4 B=0 C=0 D=0 'recv msg_keep_alive_2999, t=%d, r=%d, t=%d'
00003 [L327] TGETS    A=5 B=1 C=1 D=257 'time'
00004 [L327] TGETS    A=6 B=1 C=2 D=258 'random_key'
00005 [L327] TGETS    A=7 B=1 C=3 D=259 'delay_time'
00006 [L327] CALL     A=3 B=1 C=5 D=261 
00007 [L328] GGET     A=3 B=0 C=4 D=4 'd_ms'
00008 [L328] TGETS    A=3 B=3 C=5 D=773 'd_net'
00009 [L328] TGETS    A=3 B=3 C=6 D=774 'g_self'
00010 [L328] UGET     A=4 B=0 C=1 D=1 os
00011 [L328] TGETS    A=4 B=4 C=1 D=1025 'time'
00012 [L328] CALL     A=4 B=2 C=1 D=513 
00013 [L328] TGETS    A=5 B=1 C=1 D=257 'time'
00014 [L328] SUBVV    A=4 B=4 C=5 D=1029 
00015 [L328] TSETS    A=4 B=3 C=3 D=771 'delay_time'
00016 [L329] GGET     A=3 B=0 C=4 D=4 'd_ms'
00017 [L329] TGETS    A=3 B=3 C=5 D=773 'd_net'
00018 [L329] TGETS    A=3 B=3 C=6 D=774 'g_self'
00019 [L329] TGETS    A=4 B=1 C=2 D=258 'random_key'
00020 [L329] TSETS    A=4 B=3 C=2 D=770 'random_key'
00021 [L330] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto19 offset=0x136a source_lines=333-349 params=3
UPVALUES ['cclog', 'pairs']
00001 [L334] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L334] KSTR     A=4 B=0 C=0 D=0 'call update_item_list_1056, time=%d'
00003 [L334] MOV      A=5 B=0 C=2 D=2 
00004 [L334] CALL     A=3 B=1 C=3 D=259 
00005 [L339] UGET     A=3 B=0 C=0 D=0 cclog
00006 [L339] KSTR     A=4 B=0 C=1 D=1 'bag_index=%d, bag_type=%f, item_count=%s'
00007 [L339] TGETS    A=5 B=1 C=2 D=258 'bag_index'
00008 [L339] TGETS    A=6 B=1 C=3 D=259 'bag_type'
00009 [L339] TGETS    A=7 B=1 C=4 D=260 'item_count'
00010 [L339] CALL     A=3 B=1 C=5 D=261 
00011 [L341] UGET     A=3 B=0 C=1 D=1 pairs
00012 [L341] TGETS    A=4 B=1 C=5 D=261 'item_list'
00013 [L341] CALL     A=3 B=4 C=2 D=1026 
00014 [L341] ISNEXT   A=6 B=128 C=13 D=32781 target=28
00015 [L343] UGET     A=8 B=0 C=0 D=0 cclog
00016 [L343] KSTR     A=9 B=0 C=6 D=6 '    ----type_id=%0.0f, count=%d, level=%d, quality=%d, bag=%d'
00017 [L343] TGETS    A=10 B=7 C=7 D=1799 'type_id'
00018 [L343] TGETS    A=11 B=7 C=8 D=1800 'count'
00019 [L343] TGETS    A=12 B=7 C=9 D=1801 'level'
00020 [L343] TGETS    A=13 B=7 C=10 D=1802 'quality'
00021 [L343] TGETS    A=14 B=7 C=2 D=1794 'bag_index'
00022 [L343] CALL     A=8 B=1 C=7 D=263 
00023 [L346] GGET     A=8 B=0 C=11 D=11 'd_ms'
00024 [L346] TGETS    A=8 B=8 C=12 D=2060 'd_packageUI'
00025 [L346] TGETS    A=8 B=8 C=13 D=2061 'putItem'
00026 [L346] MOV      A=9 B=0 C=7 D=7 
00027 [L346] CALL     A=8 B=1 C=2 D=258 
00028 [L341] ITERN    A=6 B=3 C=3 D=771 
00029 [L341] ITERL    A=6 B=127 C=241 D=32753 target=15
00030 [L349] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto20 offset=0x1532 source_lines=353-366 params=3
UPVALUES ['cclog', 'pairs']
00001 [L355] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L355] KSTR     A=4 B=0 C=0 D=0 'call msg_update_label_list_1044'
00003 [L355] CALL     A=3 B=1 C=2 D=258 
00004 [L357] GGET     A=3 B=0 C=1 D=1 'd_ms'
00005 [L357] TGETS    A=3 B=3 C=2 D=770 'd_data'
00006 [L357] TGETS    A=3 B=3 C=3 D=771 'g_handbook_status'
00007 [L357] TGETS    A=4 B=1 C=4 D=260 'object_type'
00008 [L357] TGETV    A=3 B=3 C=4 D=772 
00009 [L357] IST      A=0 B=0 C=3 D=3 
00010 [L357] JMP      A=3 B=128 C=6 D=32774 target=17
00011 [L358] GGET     A=3 B=0 C=1 D=1 'd_ms'
00012 [L358] TGETS    A=3 B=3 C=2 D=770 'd_data'
00013 [L358] TGETS    A=3 B=3 C=3 D=771 'g_handbook_status'
00014 [L358] TGETS    A=4 B=1 C=4 D=260 'object_type'
00015 [L358] TNEW     A=5 B=0 C=0 D=0 
00016 [L358] TSETV    A=5 B=3 C=4 D=772 
00017 [L361] UGET     A=3 B=0 C=1 D=1 pairs
00018 [L361] TGETS    A=4 B=1 C=5 D=261 'label_list'
00019 [L361] CALL     A=3 B=4 C=2 D=1026 
00020 [L361] ISNEXT   A=6 B=128 C=8 D=32776 target=29
00021 [L362] GGET     A=8 B=0 C=1 D=1 'd_ms'
00022 [L362] TGETS    A=8 B=8 C=2 D=2050 'd_data'
00023 [L362] TGETS    A=8 B=8 C=3 D=2051 'g_handbook_status'
00024 [L362] TGETS    A=9 B=1 C=4 D=260 'object_type'
00025 [L362] TGETV    A=8 B=8 C=9 D=2057 
00026 [L362] TGETS    A=9 B=7 C=6 D=1798 'type_id'
00027 [L362] TGETS    A=10 B=7 C=7 D=1799 'status'
00028 [L362] TSETV    A=10 B=8 C=9 D=2057 
00029 [L361] ITERN    A=6 B=3 C=3 D=771 
00030 [L361] ITERL    A=6 B=127 C=246 D=32758 target=21
00031 [L365] GGET     A=3 B=0 C=1 D=1 'd_ms'
00032 [L365] TGETS    A=3 B=3 C=8 D=776 'd_alert'
00033 [L365] TGETS    A=3 B=3 C=9 D=777 'stop_wait'
00034 [L365] CALL     A=3 B=1 C=1 D=257 
00035 [L366] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto21 offset=0x16a1 source_lines=370-379 params=3
UPVALUES ['cclog']
00001 [L372] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L372] KSTR     A=4 B=0 C=0 D=0 'call msg_update_label_status_1045'
00003 [L372] CALL     A=3 B=1 C=2 D=258 
00004 [L374] GGET     A=3 B=0 C=1 D=1 'd_ms'
00005 [L374] TGETS    A=3 B=3 C=2 D=770 'd_data'
00006 [L374] TGETS    A=3 B=3 C=3 D=771 'g_handbook_status'
00007 [L374] TGETS    A=4 B=1 C=4 D=260 'object_type'
00008 [L374] TGETV    A=3 B=3 C=4 D=772 
00009 [L374] IST      A=0 B=0 C=3 D=3 
00010 [L374] JMP      A=3 B=128 C=6 D=32774 target=17
00011 [L375] GGET     A=3 B=0 C=1 D=1 'd_ms'
00012 [L375] TGETS    A=3 B=3 C=2 D=770 'd_data'
00013 [L375] TGETS    A=3 B=3 C=3 D=771 'g_handbook_status'
00014 [L375] TGETS    A=4 B=1 C=4 D=260 'object_type'
00015 [L375] TNEW     A=5 B=0 C=0 D=0 
00016 [L375] TSETV    A=5 B=3 C=4 D=772 
00017 [L378] GGET     A=3 B=0 C=1 D=1 'd_ms'
00018 [L378] TGETS    A=3 B=3 C=2 D=770 'd_data'
00019 [L378] TGETS    A=3 B=3 C=3 D=771 'g_handbook_status'
00020 [L378] TGETS    A=4 B=1 C=4 D=260 'object_type'
00021 [L378] TGETV    A=3 B=3 C=4 D=772 
00022 [L378] TGETS    A=4 B=1 C=5 D=261 'type_id'
00023 [L378] TGETS    A=5 B=1 C=6 D=262 'status'
00024 [L378] TSETV    A=5 B=3 C=4 D=772 
00025 [L379] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto22 offset=0x17aa source_lines=383-398 params=3
UPVALUES ['cclog', 'table']
00001 [L384] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L384] KSTR     A=4 B=0 C=0 D=0 'call fight_lineup_1028, time=%d, fight_id=%d'
00003 [L384] MOV      A=5 B=0 C=2 D=2 
00004 [L384] TGETS    A=6 B=1 C=1 D=257 'fight_id'
00005 [L384] CALL     A=3 B=1 C=4 D=260 
00006 [L385] GGET     A=3 B=0 C=2 D=2 'd_ms'
00007 [L385] TGETS    A=3 B=3 C=3 D=771 'd_u'
00008 [L385] TGETS    A=3 B=3 C=4 D=772 'print_table'
00009 [L385] MOV      A=4 B=0 C=1 D=1 
00010 [L385] CALL     A=3 B=1 C=2 D=258 
00011 [L387] TGETS    A=3 B=1 C=5 D=261 'lineup_count'
00012 [L387] ISNEN    A=3 B=0 C=0 D=0 0
00013 [L387] JMP      A=3 B=128 C=4 D=32772 target=18
00014 [L388] UGET     A=3 B=0 C=0 D=0 cclog
00015 [L388] KSTR     A=4 B=0 C=6 D=6 'ERROR: lineup_count=0'
00016 [L388] CALL     A=3 B=1 C=2 D=258 
00017 [L389] RET0     A=0 B=0 C=1 D=1 
00018 [L392] TGETS    A=3 B=1 C=1 D=257 'fight_id'
00019 [L392] ISF      A=0 B=0 C=3 D=3 
00020 [L392] JMP      A=4 B=128 C=13 D=32781 target=34
00021 [L393] GGET     A=3 B=0 C=7 D=7 'g_fight_info'
00022 [L393] TGETS    A=4 B=1 C=1 D=257 'fight_id'
00023 [L393] TNEW     A=5 B=0 C=0 D=0 
00024 [L393] TSETV    A=5 B=3 C=4 D=772 
00025 [L395] GGET     A=3 B=0 C=7 D=7 'g_fight_info'
00026 [L395] TGETS    A=4 B=1 C=1 D=257 'fight_id'
00027 [L395] TGETV    A=3 B=3 C=4 D=772 
00028 [L395] TSETS    A=1 B=3 C=8 D=776 'line_up_msg'
00029 [L396] UGET     A=3 B=0 C=1 D=1 table
00030 [L396] TGETS    A=3 B=3 C=9 D=777 'insert'
00031 [L396] GGET     A=4 B=0 C=10 D=10 'g_fight_id_list'
00032 [L396] TGETS    A=5 B=1 C=1 D=257 'fight_id'
00033 [L396] CALL     A=3 B=1 C=3 D=259 
00034 [L398] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto23 offset=0x192c source_lines=400-415 params=3
UPVALUES ['cclog', 'table']
00001 [L401] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L401] KSTR     A=4 B=0 C=0 D=0 'call fight_lineup_1028, time=%d, fight_id=%d'
00003 [L401] MOV      A=5 B=0 C=2 D=2 
00004 [L401] TGETS    A=6 B=1 C=1 D=257 'fight_id'
00005 [L401] CALL     A=3 B=1 C=4 D=260 
00006 [L402] GGET     A=3 B=0 C=2 D=2 'd_ms'
00007 [L402] TGETS    A=3 B=3 C=3 D=771 'd_u'
00008 [L402] TGETS    A=3 B=3 C=4 D=772 'print_table'
00009 [L402] MOV      A=4 B=0 C=1 D=1 
00010 [L402] CALL     A=3 B=1 C=2 D=258 
00011 [L404] TGETS    A=3 B=1 C=5 D=261 'lineup_count'
00012 [L404] ISNEN    A=3 B=0 C=0 D=0 0
00013 [L404] JMP      A=3 B=128 C=4 D=32772 target=18
00014 [L405] UGET     A=3 B=0 C=0 D=0 cclog
00015 [L405] KSTR     A=4 B=0 C=6 D=6 'ERROR: lineup_count=0'
00016 [L405] CALL     A=3 B=1 C=2 D=258 
00017 [L406] RET0     A=0 B=0 C=1 D=1 
00018 [L409] TGETS    A=3 B=1 C=1 D=257 'fight_id'
00019 [L409] ISF      A=0 B=0 C=3 D=3 
00020 [L409] JMP      A=4 B=128 C=13 D=32781 target=34
00021 [L410] GGET     A=3 B=0 C=7 D=7 'g_fight_info'
00022 [L410] TGETS    A=4 B=1 C=1 D=257 'fight_id'
00023 [L410] TNEW     A=5 B=0 C=0 D=0 
00024 [L410] TSETV    A=5 B=3 C=4 D=772 
00025 [L412] GGET     A=3 B=0 C=7 D=7 'g_fight_info'
00026 [L412] TGETS    A=4 B=1 C=1 D=257 'fight_id'
00027 [L412] TGETV    A=3 B=3 C=4 D=772 
00028 [L412] TSETS    A=1 B=3 C=8 D=776 'line_up_msg'
00029 [L413] UGET     A=3 B=0 C=1 D=1 table
00030 [L413] TGETS    A=3 B=3 C=9 D=777 'insert'
00031 [L413] GGET     A=4 B=0 C=10 D=10 'g_fight_id_list'
00032 [L413] TGETS    A=5 B=1 C=1 D=257 'fight_id'
00033 [L413] CALL     A=3 B=1 C=3 D=259 
00034 [L415] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto24 offset=0x1aae source_lines=417-558 params=3
UPVALUES ['cclog', 'os', 'table', 'CCFileUtils', 'string']
00001 [L418] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L418] KSTR     A=4 B=0 C=0 D=0 'call fight_result_1027, time=%d, fight_id=%d, ret=%d, type=%d'
00003 [L418] MOV      A=5 B=0 C=2 D=2 
00004 [L418] TGETS    A=6 B=1 C=1 D=257 'fight_id'
00005 [L418] TGETS    A=7 B=1 C=2 D=258 'final_result'
00006 [L418] TGETS    A=8 B=1 C=3 D=259 'fight_type'
00007 [L418] CALL     A=3 B=1 C=6 D=262 
00008 [L439] TGETS    A=3 B=1 C=1 D=257 'fight_id'
00009 [L439] ISF      A=0 B=0 C=3 D=3 
00010 [L439] JMP      A=4 B=129 C=138 D=33162 target=405
00011 [L439] GGET     A=3 B=0 C=4 D=4 'g_fight_info'
00012 [L439] TGETS    A=4 B=1 C=1 D=257 'fight_id'
00013 [L439] TGETV    A=3 B=3 C=4 D=772 
00014 [L439] ISF      A=0 B=0 C=3 D=3 
00015 [L439] JMP      A=4 B=129 C=133 D=33157 target=405
00016 [L440] GGET     A=3 B=0 C=4 D=4 'g_fight_info'
00017 [L440] TGETS    A=4 B=1 C=1 D=257 'fight_id'
00018 [L440] TGETV    A=3 B=3 C=4 D=772 
00019 [L440] TSETS    A=1 B=3 C=5 D=773 'fight_result_msg'
00020 [L443] GGET     A=3 B=0 C=4 D=4 'g_fight_info'
00021 [L443] TGETS    A=4 B=1 C=1 D=257 'fight_id'
00022 [L443] TGETV    A=3 B=3 C=4 D=772 
00023 [L443] TGETS    A=3 B=3 C=6 D=774 'line_up_msg'
00024 [L444] KSTR     A=4 B=0 C=7 D=7 '==============================='
00025 [L444] UGET     A=5 B=0 C=1 D=1 os
00026 [L444] TGETS    A=5 B=5 C=8 D=1288 'date'
00027 [L444] CALL     A=5 B=2 C=1 D=513 
00028 [L444] KSTR     A=6 B=0 C=9 D=9 ' ['
00029 [L444] TGETS    A=7 B=3 C=10 D=778 'des_name'
00030 [L444] KSTR     A=8 B=0 C=11 D=11 '] fight_id='
00031 [L444] TGETS    A=9 B=3 C=1 D=769 'fight_id'
00032 [L444] KSTR     A=10 B=0 C=12 D=12 '\n'
00033 [L444] CAT      A=4 B=4 C=10 D=1034 
00034 [L445] KSHORT   A=5 B=0 C=1 D=1 1
00035 [L445] TGETS    A=6 B=3 C=13 D=781 'lineup_count'
00036 [L445] KSHORT   A=7 B=0 C=1 D=1 1
00037 [L445] FORI     A=5 B=128 C=61 D=32829 target=99
00038 [L446] TGETS    A=9 B=3 C=14 D=782 'lineup'
00039 [L446] TGETV    A=9 B=9 C=8 D=2312 
00040 [L446] TGETS    A=9 B=9 C=15 D=2319 'src_type'
00041 [L446] KSHORT   A=10 B=0 C=0 D=0 0
00042 [L446] ISLT     A=10 B=0 C=9 D=9 
00043 [L446] JMP      A=9 B=128 C=6 D=32774 target=50
00044 [L446] TGETS    A=9 B=3 C=14 D=782 'lineup'
00045 [L446] TGETV    A=9 B=9 C=8 D=2312 
00046 [L446] TGETS    A=9 B=9 C=16 D=2320 'des_type'
00047 [L446] KSHORT   A=10 B=0 C=0 D=0 0
00048 [L446] ISGE     A=10 B=0 C=9 D=9 
00049 [L446] JMP      A=9 B=128 C=48 D=32816 target=98
00050 [L448] TGETS    A=9 B=1 C=3 D=259 'fight_type'
00051 [L448] GGET     A=10 B=0 C=17 D=17 'd_ms'
00052 [L448] TGETS    A=10 B=10 C=18 D=2578 'd_common_def'
00053 [L448] TGETS    A=10 B=10 C=3 D=2563 'fight_type'
00054 [L448] TGETS    A=10 B=10 C=19 D=2579 'convert'
00055 [L448] ISNEV    A=9 B=0 C=10 D=10 
00056 [L448] JMP      A=9 B=128 C=23 D=32791 target=80
00057 [L449] TGETS    A=9 B=3 C=14 D=782 'lineup'
00058 [L449] TGETV    A=9 B=9 C=8 D=2312 
00059 [L449] TGETS    A=9 B=9 C=16 D=2320 'des_type'
00060 [L449] KSHORT   A=10 B=23 C=112 D=6000 6000
00061 [L449] ISGE     A=10 B=0 C=9 D=9 
00062 [L449] JMP      A=9 B=128 C=17 D=32785 target=80
00063 [L449] TGETS    A=9 B=3 C=14 D=782 'lineup'
00064 [L449] TGETV    A=9 B=9 C=8 D=2312 
00065 [L449] TGETS    A=9 B=9 C=16 D=2320 'des_type'
00066 [L449] KSHORT   A=10 B=23 C=122 D=6010 6010
00067 [L449] ISGE     A=9 B=0 C=10 D=10 
00068 [L449] JMP      A=9 B=128 C=11 D=32779 target=80
00069 [L450] TGETS    A=9 B=3 C=14 D=782 'lineup'
00070 [L450] TGETV    A=9 B=9 C=8 D=2312 
00071 [L450] TGETS    A=10 B=3 C=14 D=782 'lineup'
00072 [L450] TGETV    A=10 B=10 C=8 D=2568 
00073 [L450] GGET     A=11 B=0 C=17 D=17 'd_ms'
00074 [L450] TGETS    A=11 B=11 C=21 D=2837 'd_cortCallUI'
00075 [L450] TGETS    A=11 B=11 C=22 D=2838 'getLastRightTypeAndName'
00076 [L450] CALL     A=11 B=4 C=1 D=1025 
00077 [L450] TSETS    A=13 B=10 C=20 D=2580 'des_reborn'
00078 [L450] TSETS    A=12 B=3 C=10 D=778 'des_name'
00079 [L450] TSETS    A=11 B=9 C=16 D=2320 'des_type'
00080 [L454] MOV      A=9 B=0 C=4 D=4 
00081 [L454] KSTR     A=10 B=0 C=23 D=23 'o'
00082 [L454] MOV      A=11 B=0 C=8 D=8 
00083 [L454] KSTR     A=12 B=0 C=24 D=24 ' hp='
00084 [L454] TGETS    A=13 B=3 C=14 D=782 'lineup'
00085 [L454] TGETV    A=13 B=13 C=8 D=3336 
00086 [L454] TGETS    A=13 B=13 C=25 D=3353 'src_hp'
00087 [L454] KSTR     A=14 B=0 C=26 D=26 '\t'
00088 [L454] CAT      A=4 B=9 C=14 D=2318 
00089 [L455] MOV      A=9 B=0 C=4 D=4 
00090 [L455] KSTR     A=10 B=0 C=27 D=27 'e'
00091 [L455] MOV      A=11 B=0 C=8 D=8 
00092 [L455] KSTR     A=12 B=0 C=24 D=24 ' hp='
00093 [L455] TGETS    A=13 B=3 C=14 D=782 'lineup'
00094 [L455] TGETV    A=13 B=13 C=8 D=3336 
00095 [L455] TGETS    A=13 B=13 C=28 D=3356 'des_hp'
00096 [L455] KSTR     A=14 B=0 C=12 D=12 '\n'
00097 [L455] CAT      A=4 B=9 C=14 D=2318 
00098 [L445] FORL     A=5 B=127 C=195 D=32707 target=38
00099 [L461] GGET     A=5 B=0 C=17 D=17 'd_ms'
00100 [L461] TGETS    A=5 B=5 C=29 D=1309 'd_u'
00101 [L461] TGETS    A=5 B=5 C=30 D=1310 'isWin32'
00102 [L461] CALL     A=5 B=2 C=1 D=513 
00103 [L461] IST      A=0 B=0 C=5 D=5 
00104 [L461] JMP      A=6 B=128 C=5 D=32773 target=110
00105 [L461] GGET     A=5 B=0 C=17 D=17 'd_ms'
00106 [L461] TGETS    A=5 B=5 C=31 D=1311 'd_c'
00107 [L461] TGETS    A=5 B=5 C=32 D=1312 'g_fight_log'
00108 [L461] ISNEP    A=5 B=0 C=2 D=2 
00109 [L461] JMP      A=5 B=129 C=19 D=33043 target=385
00110 [L463] MOV      A=5 B=0 C=4 D=4 
00111 [L463] KSTR     A=6 B=0 C=33 D=33 '=================steps======================\n'
00112 [L463] CAT      A=4 B=5 C=6 D=1286 
00113 [L464] KSHORT   A=5 B=0 C=1 D=1 1
00114 [L464] TGETS    A=6 B=1 C=34 D=290 'fight_round'
00115 [L464] KSHORT   A=7 B=0 C=1 D=1 1
00116 [L464] FORI     A=5 B=128 C=10 D=32778 target=127
00117 [L465] TGETS    A=9 B=1 C=35 D=291 'fight_result'
00118 [L465] TGETV    A=9 B=9 C=8 D=2312 
00119 [L466] MOV      A=10 B=0 C=4 D=4 
00120 [L466] UGET     A=11 B=0 C=2 D=2 table
00121 [L466] TGETS    A=11 B=11 C=36 D=2852 'tostring'
00122 [L466] MOV      A=12 B=0 C=9 D=9 
00123 [L466] CALL     A=11 B=2 C=2 D=514 
00124 [L466] KSTR     A=12 B=0 C=12 D=12 '\n'
00125 [L466] CAT      A=4 B=10 C=12 D=2572 
00126 [L464] FORL     A=5 B=127 C=246 D=32758 target=117
00127 [L470] MOV      A=5 B=0 C=4 D=4 
00128 [L470] KSTR     A=6 B=0 C=37 D=37 '=================events======================\n'
00129 [L470] CAT      A=4 B=5 C=6 D=1286 
00130 [L471] GGET     A=5 B=0 C=38 D=38 'get_fight_events'
00131 [L471] TGETS    A=6 B=3 C=1 D=769 'fight_id'
00132 [L471] CALL     A=5 B=2 C=2 D=514 
00133 [L472] KSHORT   A=6 B=0 C=1 D=1 1
00134 [L472] LEN      A=7 B=0 C=5 D=5 
00135 [L472] KSHORT   A=8 B=0 C=1 D=1 1
00136 [L472] FORI     A=6 B=128 C=8 D=32776 target=145
00137 [L473] MOV      A=10 B=0 C=4 D=4 
00138 [L473] UGET     A=11 B=0 C=2 D=2 table
00139 [L473] TGETS    A=11 B=11 C=36 D=2852 'tostring'
00140 [L473] TGETV    A=12 B=5 C=9 D=1289 
00141 [L473] CALL     A=11 B=2 C=2 D=514 
00142 [L473] KSTR     A=12 B=0 C=12 D=12 '\n'
00143 [L473] CAT      A=4 B=10 C=12 D=2572 
00144 [L472] FORL     A=6 B=127 C=248 D=32760 target=137
00145 [L477] MOV      A=6 B=0 C=4 D=4 
00146 [L477] KSTR     A=7 B=0 C=39 D=39 '=================detail======================\n'
00147 [L477] CAT      A=4 B=6 C=7 D=1543 
00148 [L478] KSHORT   A=6 B=0 C=1 D=1 1
00149 [L478] TGETS    A=7 B=1 C=34 D=290 'fight_round'
00150 [L478] KSHORT   A=8 B=0 C=1 D=1 1
00151 [L478] FORI     A=6 B=128 C=206 D=32974 target=358
00152 [L479] UGET     A=10 B=0 C=0 D=0 cclog
00153 [L479] KSTR     A=11 B=0 C=40 D=40 'fight step %2d, [%d-%d], %d, [%d]'
00154 [L479] MOV      A=12 B=0 C=9 D=9 
00155 [L479] TGETS    A=13 B=1 C=35 D=291 'fight_result'
00156 [L479] TGETV    A=13 B=13 C=9 D=3337 
00157 [L479] TGETS    A=13 B=13 C=41 D=3369 'src_order'
00158 [L480] TGETS    A=14 B=1 C=35 D=291 'fight_result'
00159 [L480] TGETV    A=14 B=14 C=9 D=3593 
00160 [L480] TGETS    A=14 B=14 C=42 D=3626 'des_order'
00161 [L481] TGETS    A=15 B=1 C=35 D=291 'fight_result'
00162 [L481] TGETV    A=15 B=15 C=9 D=3849 
00163 [L481] TGETS    A=15 B=15 C=43 D=3883 'skill_type'
00164 [L482] TGETS    A=16 B=1 C=35 D=291 'fight_result'
00165 [L482] TGETV    A=16 B=16 C=9 D=4105 
00166 [L482] TGETS    A=16 B=16 C=44 D=4140 'damage_list'
00167 [L482] LEN      A=16 B=0 C=16 D=16 
00168 [L479] CALL     A=10 B=1 C=7 D=263 
00169 [L484] KSHORT   A=10 B=0 C=1 D=1 1
00170 [L484] LEN      A=11 B=0 C=5 D=5 
00171 [L484] KSHORT   A=12 B=0 C=1 D=1 1
00172 [L484] FORI     A=10 B=128 C=104 D=32872 target=277
00173 [L485] TGETV    A=14 B=5 C=13 D=1293 
00174 [L485] TGETS    A=14 B=14 C=45 D=3629 'cur_action'
00175 [L485] ISNEV    A=14 B=0 C=9 D=9 
00176 [L485] JMP      A=14 B=128 C=99 D=32867 target=276
00177 [L486] MOV      A=14 B=0 C=4 D=4 
00178 [L486] KSTR     A=15 B=0 C=46 D=46 '--'
00179 [L486] MOV      A=16 B=0 C=9 D=9 
00180 [L486] KSTR     A=17 B=0 C=47 D=47 '--\t'
00181 [L486] CAT      A=4 B=14 C=17 D=3601 
00182 [L487] MOV      A=14 B=0 C=4 D=4 
00183 [L487] KSTR     A=15 B=0 C=48 D=48 '['
00184 [L487] TGETV    A=16 B=5 C=13 D=1293 
00185 [L487] TGETS    A=16 B=16 C=49 D=4145 'logic_type'
00186 [L487] KSTR     A=17 B=0 C=50 D=50 ']\t'
00187 [L487] CAT      A=4 B=14 C=17 D=3601 
00188 [L489] KPRI     A=14 B=0 C=0 D=0 
00189 [L490] TGETV    A=15 B=5 C=13 D=1293 
00190 [L490] TGETS    A=15 B=15 C=51 D=3891 'who_use'
00191 [L490] ISNEN    A=15 B=0 C=0 D=0 1
00192 [L490] JMP      A=15 B=128 C=12 D=32780 target=205
00193 [L490] TGETV    A=15 B=5 C=13 D=1293 
00194 [L490] TGETS    A=15 B=15 C=52 D=3892 'self_use'
00195 [L490] ISNEP    A=15 B=0 C=2 D=2 
00196 [L490] JMP      A=15 B=128 C=8 D=32776 target=205
00197 [L491] MOV      A=15 B=0 C=4 D=4 
00198 [L491] KSTR     A=16 B=0 C=23 D=23 'o'
00199 [L491] TGETV    A=17 B=5 C=13 D=1293 
00200 [L491] TGETS    A=17 B=17 C=41 D=4393 'src_order'
00201 [L491] KSTR     A=18 B=0 C=53 D=53 ' -> '
00202 [L491] CAT      A=4 B=15 C=18 D=3858 
00203 [L492] KSTR     A=14 B=0 C=23 D=23 'o'
00204 [L492] JMP      A=15 B=128 C=39 D=32807 target=244
00205 [L493] TGETV    A=15 B=5 C=13 D=1293 
00206 [L493] TGETS    A=15 B=15 C=51 D=3891 'who_use'
00207 [L493] ISNEN    A=15 B=0 C=0 D=0 1
00208 [L493] JMP      A=15 B=128 C=12 D=32780 target=221
00209 [L493] TGETV    A=15 B=5 C=13 D=1293 
00210 [L493] TGETS    A=15 B=15 C=52 D=3892 'self_use'
00211 [L493] ISNEP    A=15 B=0 C=1 D=1 
00212 [L493] JMP      A=15 B=128 C=8 D=32776 target=221
00213 [L494] MOV      A=15 B=0 C=4 D=4 
00214 [L494] KSTR     A=16 B=0 C=23 D=23 'o'
00215 [L494] TGETV    A=17 B=5 C=13 D=1293 
00216 [L494] TGETS    A=17 B=17 C=41 D=4393 'src_order'
00217 [L494] KSTR     A=18 B=0 C=53 D=53 ' -> '
00218 [L494] CAT      A=4 B=15 C=18 D=3858 
00219 [L495] KSTR     A=14 B=0 C=27 D=27 'e'
00220 [L495] JMP      A=15 B=128 C=23 D=32791 target=244
00221 [L496] TGETV    A=15 B=5 C=13 D=1293 
00222 [L496] TGETS    A=15 B=15 C=51 D=3891 'who_use'
00223 [L496] ISNEN    A=15 B=0 C=1 D=1 2
00224 [L496] JMP      A=15 B=128 C=12 D=32780 target=237
00225 [L496] TGETV    A=15 B=5 C=13 D=1293 
00226 [L496] TGETS    A=15 B=15 C=52 D=3892 'self_use'
00227 [L496] ISNEP    A=15 B=0 C=2 D=2 
00228 [L496] JMP      A=15 B=128 C=8 D=32776 target=237
00229 [L497] MOV      A=15 B=0 C=4 D=4 
00230 [L497] KSTR     A=16 B=0 C=27 D=27 'e'
00231 [L497] TGETV    A=17 B=5 C=13 D=1293 
00232 [L497] TGETS    A=17 B=17 C=41 D=4393 'src_order'
00233 [L497] KSTR     A=18 B=0 C=53 D=53 ' -> '
00234 [L497] CAT      A=4 B=15 C=18 D=3858 
00235 [L498] KSTR     A=14 B=0 C=27 D=27 'e'
00236 [L498] JMP      A=15 B=128 C=7 D=32775 target=244
00237 [L500] MOV      A=15 B=0 C=4 D=4 
00238 [L500] KSTR     A=16 B=0 C=27 D=27 'e'
00239 [L500] TGETV    A=17 B=5 C=13 D=1293 
00240 [L500] TGETS    A=17 B=17 C=41 D=4393 'src_order'
00241 [L500] KSTR     A=18 B=0 C=53 D=53 ' -> '
00242 [L500] CAT      A=4 B=15 C=18 D=3858 
00243 [L501] KSTR     A=14 B=0 C=23 D=23 'o'
00244 [L504] KSHORT   A=15 B=0 C=1 D=1 1
00245 [L504] TGETV    A=16 B=5 C=13 D=1293 
00246 [L504] TGETS    A=16 B=16 C=54 D=4150 'skill_result_list'
00247 [L504] LEN      A=16 B=0 C=16 D=16 
00248 [L504] KSHORT   A=17 B=0 C=1 D=1 1
00249 [L504] FORI     A=15 B=128 C=23 D=32791 target=273
00250 [L505] MOV      A=19 B=0 C=4 D=4 
00251 [L505] KSTR     A=20 B=0 C=48 D=48 '['
00252 [L505] MOV      A=21 B=0 C=14 D=14 
00253 [L505] TGETV    A=22 B=5 C=13 D=1293 
00254 [L505] TGETS    A=22 B=22 C=54 D=5686 'skill_result_list'
00255 [L505] TGETV    A=22 B=22 C=18 D=5650 
00256 [L505] TGETS    A=22 B=22 C=42 D=5674 'des_order'
00257 [L505] KSTR     A=23 B=0 C=55 D=55 '='
00258 [L505] TGETV    A=24 B=5 C=13 D=1293 
00259 [L505] TGETS    A=24 B=24 C=54 D=6198 'skill_result_list'
00260 [L505] TGETV    A=24 B=24 C=18 D=6162 
00261 [L505] TGETS    A=24 B=24 C=56 D=6200 'field_plus'
00262 [L505] KSTR     A=25 B=0 C=57 D=57 '('
00263 [L505] TGETV    A=26 B=5 C=13 D=1293 
00264 [L505] TGETS    A=26 B=26 C=54 D=6710 'skill_result_list'
00265 [L505] TGETV    A=26 B=26 C=18 D=6674 
00266 [L505] TGETS    A=26 B=26 C=58 D=6714 'field'
00267 [L505] IST      A=0 B=0 C=26 D=26 
00268 [L505] JMP      A=27 B=128 C=1 D=32769 target=270
00269 [L505] KSHORT   A=26 B=0 C=0 D=0 0
00270 [L505] KSTR     A=27 B=0 C=59 D=59 ')]'
00271 [L505] CAT      A=4 B=19 C=27 D=4891 
00272 [L504] FORL     A=15 B=127 C=233 D=32745 target=250
00273 [L508] MOV      A=15 B=0 C=4 D=4 
00274 [L508] KSTR     A=16 B=0 C=12 D=12 '\n'
00275 [L508] CAT      A=4 B=15 C=16 D=3856 
00276 [L484] FORL     A=10 B=127 C=152 D=32664 target=173
00277 [L513] MOV      A=10 B=0 C=4 D=4 
00278 [L513] KSTR     A=11 B=0 C=46 D=46 '--'
00279 [L513] MOV      A=12 B=0 C=9 D=9 
00280 [L513] KSTR     A=13 B=0 C=47 D=47 '--\t'
00281 [L513] CAT      A=4 B=10 C=13 D=2573 
00282 [L515] TGETS    A=10 B=1 C=35 D=291 'fight_result'
00283 [L515] TGETV    A=10 B=10 C=9 D=2569 
00284 [L516] MOV      A=11 B=0 C=4 D=4 
00285 [L516] KSTR     A=12 B=0 C=48 D=48 '['
00286 [L516] TGETS    A=13 B=10 C=43 D=2603 'skill_type'
00287 [L516] KSTR     A=14 B=0 C=50 D=50 ']\t'
00288 [L516] CAT      A=4 B=11 C=14 D=2830 
00289 [L518] KPRI     A=11 B=0 C=0 D=0 
00290 [L519] TGETS    A=12 B=10 C=60 D=2620 'is_src'
00291 [L519] ISNEP    A=12 B=0 C=2 D=2 
00292 [L519] JMP      A=12 B=128 C=10 D=32778 target=303
00293 [L519] TGETS    A=12 B=10 C=52 D=2612 'self_use'
00294 [L519] ISNEP    A=12 B=0 C=2 D=2 
00295 [L519] JMP      A=12 B=128 C=7 D=32775 target=303
00296 [L520] MOV      A=12 B=0 C=4 D=4 
00297 [L520] KSTR     A=13 B=0 C=23 D=23 'o'
00298 [L520] TGETS    A=14 B=10 C=41 D=2601 'src_order'
00299 [L520] KSTR     A=15 B=0 C=53 D=53 ' -> '
00300 [L520] CAT      A=4 B=12 C=15 D=3087 
00301 [L521] KSTR     A=11 B=0 C=23 D=23 'o'
00302 [L521] JMP      A=12 B=128 C=32 D=32800 target=335
00303 [L522] TGETS    A=12 B=10 C=60 D=2620 'is_src'
00304 [L522] ISNEP    A=12 B=0 C=2 D=2 
00305 [L522] JMP      A=12 B=128 C=10 D=32778 target=316
00306 [L522] TGETS    A=12 B=10 C=52 D=2612 'self_use'
00307 [L522] ISNEP    A=12 B=0 C=1 D=1 
00308 [L522] JMP      A=12 B=128 C=7 D=32775 target=316
00309 [L523] MOV      A=12 B=0 C=4 D=4 
00310 [L523] KSTR     A=13 B=0 C=23 D=23 'o'
00311 [L523] TGETS    A=14 B=10 C=41 D=2601 'src_order'
00312 [L523] KSTR     A=15 B=0 C=53 D=53 ' -> '
00313 [L523] CAT      A=4 B=12 C=15 D=3087 
00314 [L524] KSTR     A=11 B=0 C=27 D=27 'e'
00315 [L524] JMP      A=12 B=128 C=19 D=32787 target=335
00316 [L525] TGETS    A=12 B=10 C=60 D=2620 'is_src'
00317 [L525] ISNEP    A=12 B=0 C=1 D=1 
00318 [L525] JMP      A=12 B=128 C=10 D=32778 target=329
00319 [L525] TGETS    A=12 B=10 C=52 D=2612 'self_use'
00320 [L525] ISNEP    A=12 B=0 C=2 D=2 
00321 [L525] JMP      A=12 B=128 C=7 D=32775 target=329
00322 [L526] MOV      A=12 B=0 C=4 D=4 
00323 [L526] KSTR     A=13 B=0 C=27 D=27 'e'
00324 [L526] TGETS    A=14 B=10 C=41 D=2601 'src_order'
00325 [L526] KSTR     A=15 B=0 C=53 D=53 ' -> '
00326 [L526] CAT      A=4 B=12 C=15 D=3087 
00327 [L527] KSTR     A=11 B=0 C=27 D=27 'e'
00328 [L527] JMP      A=12 B=128 C=6 D=32774 target=335
00329 [L529] MOV      A=12 B=0 C=4 D=4 
00330 [L529] KSTR     A=13 B=0 C=27 D=27 'e'
00331 [L529] TGETS    A=14 B=10 C=41 D=2601 'src_order'
00332 [L529] KSTR     A=15 B=0 C=53 D=53 ' -> '
00333 [L529] CAT      A=4 B=12 C=15 D=3087 
00334 [L530] KSTR     A=11 B=0 C=23 D=23 'o'
00335 [L533] KSHORT   A=12 B=0 C=1 D=1 1
00336 [L533] TGETS    A=13 B=10 C=61 D=2621 'damage_count'
00337 [L533] KSHORT   A=14 B=0 C=1 D=1 1
00338 [L533] FORI     A=12 B=128 C=15 D=32783 target=354
00339 [L534] TGETS    A=16 B=10 C=44 D=2604 'damage_list'
00340 [L534] TGETV    A=16 B=16 C=15 D=4111 
00341 [L534] KSHORT   A=17 B=0 C=0 D=0 0
00342 [L534] ISGE     A=17 B=0 C=16 D=16 
00343 [L534] JMP      A=16 B=128 C=9 D=32777 target=353
00344 [L535] MOV      A=16 B=0 C=4 D=4 
00345 [L535] KSTR     A=17 B=0 C=48 D=48 '['
00346 [L535] MOV      A=18 B=0 C=11 D=11 
00347 [L535] MOV      A=19 B=0 C=15 D=15 
00348 [L535] KSTR     A=20 B=0 C=55 D=55 '='
00349 [L535] TGETS    A=21 B=10 C=44 D=2604 'damage_list'
00350 [L535] TGETV    A=21 B=21 C=15 D=5391 
00351 [L535] KSTR     A=22 B=0 C=62 D=62 ']'
00352 [L535] CAT      A=4 B=16 C=22 D=4118 
00353 [L533] FORL     A=12 B=127 C=241 D=32753 target=339
00354 [L538] MOV      A=12 B=0 C=4 D=4 
00355 [L538] KSTR     A=13 B=0 C=12 D=12 '\n'
00356 [L538] CAT      A=4 B=12 C=13 D=3085 
00357 [L478] FORL     A=6 B=127 C=50 D=32562 target=152
00358 [L541] MOV      A=6 B=0 C=4 D=4 
00359 [L541] KSTR     A=7 B=0 C=63 D=63 '=================end======================\n\n\n\n'
00360 [L541] CAT      A=4 B=6 C=7 D=1543 
00361 [L544] UGET     A=6 B=0 C=3 D=3 CCFileUtils
00362 [L544] MOV      A=7 B=0 C=6 D=6 
00363 [L544] TGETS    A=6 B=6 C=64 D=1600 'sharedFileUtils'
00364 [L544] CALL     A=6 B=2 C=2 D=514 
00365 [L544] MOV      A=7 B=0 C=6 D=6 
00366 [L544] TGETS    A=6 B=6 C=65 D=1601 'getWriteablePath'
00367 [L544] CALL     A=6 B=2 C=2 D=514 
00368 [L544] KSTR     A=7 B=0 C=66 D=66 'setting_w/'
00369 [L544] UGET     A=8 B=0 C=4 D=4 string
00370 [L544] TGETS    A=8 B=8 C=67 D=2115 'format'
00371 [L544] KSTR     A=9 B=0 C=68 D=68 '%0.0f'
00372 [L544] GGET     A=10 B=0 C=17 D=17 'd_ms'
00373 [L544] TGETS    A=10 B=10 C=69 D=2629 'd_mainUI'
00374 [L544] TGETS    A=10 B=10 C=70 D=2630 'g_playerInfo'
00375 [L544] TGETS    A=10 B=10 C=71 D=2631 'role_id'
00376 [L544] CALL     A=8 B=2 C=3 D=515 
00377 [L544] KSTR     A=9 B=0 C=72 D=72 '_fight.log'
00378 [L544] CAT      A=6 B=6 C=9 D=1545 
00379 [L545] GGET     A=7 B=0 C=17 D=17 'd_ms'
00380 [L545] TGETS    A=7 B=7 C=73 D=1865 'd_file'
00381 [L545] TGETS    A=7 B=7 C=74 D=1866 'appendFile'
00382 [L545] MOV      A=8 B=0 C=6 D=6 
00383 [L545] MOV      A=9 B=0 C=4 D=4 
00384 [L545] CALL     A=7 B=1 C=3 D=259 
00385 [L550] GGET     A=5 B=0 C=4 D=4 'g_fight_info'
00386 [L550] LEN      A=5 B=0 C=5 D=5 
00387 [L550] KSHORT   A=6 B=0 C=3 D=3 3
00388 [L550] ISGE     A=6 B=0 C=5 D=5 
00389 [L550] JMP      A=5 B=128 C=8 D=32776 target=398
00390 [L551] UGET     A=5 B=0 C=2 D=2 table
00391 [L551] TGETS    A=5 B=5 C=75 D=1355 'remove'
00392 [L551] GGET     A=6 B=0 C=76 D=76 'g_fight_id_list'
00393 [L551] KSHORT   A=7 B=0 C=1 D=1 1
00394 [L551] CALL     A=5 B=2 C=3 D=515 
00395 [L552] GGET     A=6 B=0 C=4 D=4 'g_fight_info'
00396 [L552] KPRI     A=7 B=0 C=0 D=0 
00397 [L552] TSETV    A=7 B=6 C=5 D=1541 
00398 [L555] GGET     A=5 B=0 C=17 D=17 'd_ms'
00399 [L555] TGETS    A=5 B=5 C=77 D=1357 'd_loginUI'
00400 [L555] GGET     A=6 B=0 C=17 D=17 'd_ms'
00401 [L555] TGETS    A=6 B=6 C=77 D=1613 'd_loginUI'
00402 [L555] TGETS    A=6 B=6 C=79 D=1615 'senceID'
00403 [L555] TGETS    A=6 B=6 C=80 D=1616 'fightUI'
00404 [L555] TSETS    A=6 B=5 C=78 D=1358 'g_currentSence'
00405 [L558] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto25 offset=0x277b source_lines=561-692 params=3
UPVALUES ['cclog', 'os', 'table', 'CCFileUtils', 'string']
00001 [L562] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L562] KSTR     A=4 B=0 C=0 D=0 'call fight_result_1027, time=%d, fight_id=%d, ret=%d, type=%d'
00003 [L562] MOV      A=5 B=0 C=2 D=2 
00004 [L562] TGETS    A=6 B=1 C=1 D=257 'fight_id'
00005 [L562] TGETS    A=7 B=1 C=2 D=258 'final_result'
00006 [L562] TGETS    A=8 B=1 C=3 D=259 'fight_type'
00007 [L562] CALL     A=3 B=1 C=6 D=262 
00008 [L583] TGETS    A=3 B=1 C=1 D=257 'fight_id'
00009 [L583] ISF      A=0 B=0 C=3 D=3 
00010 [L583] JMP      A=4 B=129 C=138 D=33162 target=405
00011 [L583] GGET     A=3 B=0 C=4 D=4 'g_fight_info'
00012 [L583] TGETS    A=4 B=1 C=1 D=257 'fight_id'
00013 [L583] TGETV    A=3 B=3 C=4 D=772 
00014 [L583] ISF      A=0 B=0 C=3 D=3 
00015 [L583] JMP      A=4 B=129 C=133 D=33157 target=405
00016 [L584] GGET     A=3 B=0 C=4 D=4 'g_fight_info'
00017 [L584] TGETS    A=4 B=1 C=1 D=257 'fight_id'
00018 [L584] TGETV    A=3 B=3 C=4 D=772 
00019 [L584] TSETS    A=1 B=3 C=5 D=773 'fight_result_msg'
00020 [L587] GGET     A=3 B=0 C=4 D=4 'g_fight_info'
00021 [L587] TGETS    A=4 B=1 C=1 D=257 'fight_id'
00022 [L587] TGETV    A=3 B=3 C=4 D=772 
00023 [L587] TGETS    A=3 B=3 C=6 D=774 'line_up_msg'
00024 [L588] KSTR     A=4 B=0 C=7 D=7 '==============================='
00025 [L588] UGET     A=5 B=0 C=1 D=1 os
00026 [L588] TGETS    A=5 B=5 C=8 D=1288 'date'
00027 [L588] CALL     A=5 B=2 C=1 D=513 
00028 [L588] KSTR     A=6 B=0 C=9 D=9 ' ['
00029 [L588] TGETS    A=7 B=3 C=10 D=778 'des_name'
00030 [L588] KSTR     A=8 B=0 C=11 D=11 '] fight_id='
00031 [L588] TGETS    A=9 B=3 C=1 D=769 'fight_id'
00032 [L588] KSTR     A=10 B=0 C=12 D=12 '\n'
00033 [L588] CAT      A=4 B=4 C=10 D=1034 
00034 [L589] KSHORT   A=5 B=0 C=1 D=1 1
00035 [L589] TGETS    A=6 B=3 C=13 D=781 'lineup_count'
00036 [L589] KSHORT   A=7 B=0 C=1 D=1 1
00037 [L589] FORI     A=5 B=128 C=61 D=32829 target=99
00038 [L590] TGETS    A=9 B=3 C=14 D=782 'lineup'
00039 [L590] TGETV    A=9 B=9 C=8 D=2312 
00040 [L590] TGETS    A=9 B=9 C=15 D=2319 'src_type'
00041 [L590] KSHORT   A=10 B=0 C=0 D=0 0
00042 [L590] ISLT     A=10 B=0 C=9 D=9 
00043 [L590] JMP      A=9 B=128 C=6 D=32774 target=50
00044 [L590] TGETS    A=9 B=3 C=14 D=782 'lineup'
00045 [L590] TGETV    A=9 B=9 C=8 D=2312 
00046 [L590] TGETS    A=9 B=9 C=16 D=2320 'des_type'
00047 [L590] KSHORT   A=10 B=0 C=0 D=0 0
00048 [L590] ISGE     A=10 B=0 C=9 D=9 
00049 [L590] JMP      A=9 B=128 C=48 D=32816 target=98
00050 [L592] TGETS    A=9 B=1 C=3 D=259 'fight_type'
00051 [L592] GGET     A=10 B=0 C=17 D=17 'd_ms'
00052 [L592] TGETS    A=10 B=10 C=18 D=2578 'd_common_def'
00053 [L592] TGETS    A=10 B=10 C=3 D=2563 'fight_type'
00054 [L592] TGETS    A=10 B=10 C=19 D=2579 'convert'
00055 [L592] ISNEV    A=9 B=0 C=10 D=10 
00056 [L592] JMP      A=9 B=128 C=23 D=32791 target=80
00057 [L593] TGETS    A=9 B=3 C=14 D=782 'lineup'
00058 [L593] TGETV    A=9 B=9 C=8 D=2312 
00059 [L593] TGETS    A=9 B=9 C=16 D=2320 'des_type'
00060 [L593] KSHORT   A=10 B=23 C=112 D=6000 6000
00061 [L593] ISGE     A=10 B=0 C=9 D=9 
00062 [L593] JMP      A=9 B=128 C=17 D=32785 target=80
00063 [L593] TGETS    A=9 B=3 C=14 D=782 'lineup'
00064 [L593] TGETV    A=9 B=9 C=8 D=2312 
00065 [L593] TGETS    A=9 B=9 C=16 D=2320 'des_type'
00066 [L593] KSHORT   A=10 B=23 C=122 D=6010 6010
00067 [L593] ISGE     A=9 B=0 C=10 D=10 
00068 [L593] JMP      A=9 B=128 C=11 D=32779 target=80
00069 [L594] TGETS    A=9 B=3 C=14 D=782 'lineup'
00070 [L594] TGETV    A=9 B=9 C=8 D=2312 
00071 [L594] TGETS    A=10 B=3 C=14 D=782 'lineup'
00072 [L594] TGETV    A=10 B=10 C=8 D=2568 
00073 [L594] GGET     A=11 B=0 C=17 D=17 'd_ms'
00074 [L594] TGETS    A=11 B=11 C=21 D=2837 'd_cortCallUI'
00075 [L594] TGETS    A=11 B=11 C=22 D=2838 'getLastRightTypeAndName'
00076 [L594] CALL     A=11 B=4 C=1 D=1025 
00077 [L594] TSETS    A=13 B=10 C=20 D=2580 'des_reborn'
00078 [L594] TSETS    A=12 B=3 C=10 D=778 'des_name'
00079 [L594] TSETS    A=11 B=9 C=16 D=2320 'des_type'
00080 [L597] MOV      A=9 B=0 C=4 D=4 
00081 [L597] KSTR     A=10 B=0 C=23 D=23 'o'
00082 [L597] MOV      A=11 B=0 C=8 D=8 
00083 [L597] KSTR     A=12 B=0 C=24 D=24 ' hp='
00084 [L597] TGETS    A=13 B=3 C=14 D=782 'lineup'
00085 [L597] TGETV    A=13 B=13 C=8 D=3336 
00086 [L597] TGETS    A=13 B=13 C=25 D=3353 'src_hp'
00087 [L597] KSTR     A=14 B=0 C=26 D=26 '\t'
00088 [L597] CAT      A=4 B=9 C=14 D=2318 
00089 [L598] MOV      A=9 B=0 C=4 D=4 
00090 [L598] KSTR     A=10 B=0 C=27 D=27 'e'
00091 [L598] MOV      A=11 B=0 C=8 D=8 
00092 [L598] KSTR     A=12 B=0 C=24 D=24 ' hp='
00093 [L598] TGETS    A=13 B=3 C=14 D=782 'lineup'
00094 [L598] TGETV    A=13 B=13 C=8 D=3336 
00095 [L598] TGETS    A=13 B=13 C=28 D=3356 'des_hp'
00096 [L598] KSTR     A=14 B=0 C=12 D=12 '\n'
00097 [L598] CAT      A=4 B=9 C=14 D=2318 
00098 [L589] FORL     A=5 B=127 C=195 D=32707 target=38
00099 [L602] GGET     A=5 B=0 C=17 D=17 'd_ms'
00100 [L602] TGETS    A=5 B=5 C=29 D=1309 'd_u'
00101 [L602] TGETS    A=5 B=5 C=30 D=1310 'isWin32'
00102 [L602] CALL     A=5 B=2 C=1 D=513 
00103 [L602] IST      A=0 B=0 C=5 D=5 
00104 [L602] JMP      A=6 B=128 C=5 D=32773 target=110
00105 [L602] GGET     A=5 B=0 C=17 D=17 'd_ms'
00106 [L602] TGETS    A=5 B=5 C=31 D=1311 'd_c'
00107 [L602] TGETS    A=5 B=5 C=32 D=1312 'g_fight_log'
00108 [L602] ISNEP    A=5 B=0 C=2 D=2 
00109 [L602] JMP      A=5 B=129 C=19 D=33043 target=385
00110 [L603] MOV      A=5 B=0 C=4 D=4 
00111 [L603] KSTR     A=6 B=0 C=33 D=33 '=================steps======================\n'
00112 [L603] CAT      A=4 B=5 C=6 D=1286 
00113 [L604] KSHORT   A=5 B=0 C=1 D=1 1
00114 [L604] TGETS    A=6 B=1 C=34 D=290 'fight_round'
00115 [L604] KSHORT   A=7 B=0 C=1 D=1 1
00116 [L604] FORI     A=5 B=128 C=10 D=32778 target=127
00117 [L605] TGETS    A=9 B=1 C=35 D=291 'fight_result'
00118 [L605] TGETV    A=9 B=9 C=8 D=2312 
00119 [L606] MOV      A=10 B=0 C=4 D=4 
00120 [L606] UGET     A=11 B=0 C=2 D=2 table
00121 [L606] TGETS    A=11 B=11 C=36 D=2852 'tostring'
00122 [L606] MOV      A=12 B=0 C=9 D=9 
00123 [L606] CALL     A=11 B=2 C=2 D=514 
00124 [L606] KSTR     A=12 B=0 C=12 D=12 '\n'
00125 [L606] CAT      A=4 B=10 C=12 D=2572 
00126 [L604] FORL     A=5 B=127 C=246 D=32758 target=117
00127 [L609] MOV      A=5 B=0 C=4 D=4 
00128 [L609] KSTR     A=6 B=0 C=37 D=37 '=================events======================\n'
00129 [L609] CAT      A=4 B=5 C=6 D=1286 
00130 [L610] GGET     A=5 B=0 C=38 D=38 'get_fight_events'
00131 [L610] TGETS    A=6 B=3 C=1 D=769 'fight_id'
00132 [L610] CALL     A=5 B=2 C=2 D=514 
00133 [L611] KSHORT   A=6 B=0 C=1 D=1 1
00134 [L611] LEN      A=7 B=0 C=5 D=5 
00135 [L611] KSHORT   A=8 B=0 C=1 D=1 1
00136 [L611] FORI     A=6 B=128 C=8 D=32776 target=145
00137 [L612] MOV      A=10 B=0 C=4 D=4 
00138 [L612] UGET     A=11 B=0 C=2 D=2 table
00139 [L612] TGETS    A=11 B=11 C=36 D=2852 'tostring'
00140 [L612] TGETV    A=12 B=5 C=9 D=1289 
00141 [L612] CALL     A=11 B=2 C=2 D=514 
00142 [L612] KSTR     A=12 B=0 C=12 D=12 '\n'
00143 [L612] CAT      A=4 B=10 C=12 D=2572 
00144 [L611] FORL     A=6 B=127 C=248 D=32760 target=137
00145 [L615] MOV      A=6 B=0 C=4 D=4 
00146 [L615] KSTR     A=7 B=0 C=39 D=39 '=================detail======================\n'
00147 [L615] CAT      A=4 B=6 C=7 D=1543 
00148 [L616] KSHORT   A=6 B=0 C=1 D=1 1
00149 [L616] TGETS    A=7 B=1 C=34 D=290 'fight_round'
00150 [L616] KSHORT   A=8 B=0 C=1 D=1 1
00151 [L616] FORI     A=6 B=128 C=206 D=32974 target=358
00152 [L617] UGET     A=10 B=0 C=0 D=0 cclog
00153 [L617] KSTR     A=11 B=0 C=40 D=40 'fight step %2d, [%d-%d], %d, [%d]'
00154 [L617] MOV      A=12 B=0 C=9 D=9 
00155 [L617] TGETS    A=13 B=1 C=35 D=291 'fight_result'
00156 [L617] TGETV    A=13 B=13 C=9 D=3337 
00157 [L617] TGETS    A=13 B=13 C=41 D=3369 'src_order'
00158 [L618] TGETS    A=14 B=1 C=35 D=291 'fight_result'
00159 [L618] TGETV    A=14 B=14 C=9 D=3593 
00160 [L618] TGETS    A=14 B=14 C=42 D=3626 'des_order'
00161 [L619] TGETS    A=15 B=1 C=35 D=291 'fight_result'
00162 [L619] TGETV    A=15 B=15 C=9 D=3849 
00163 [L619] TGETS    A=15 B=15 C=43 D=3883 'skill_type'
00164 [L620] TGETS    A=16 B=1 C=35 D=291 'fight_result'
00165 [L620] TGETV    A=16 B=16 C=9 D=4105 
00166 [L620] TGETS    A=16 B=16 C=44 D=4140 'damage_list'
00167 [L620] LEN      A=16 B=0 C=16 D=16 
00168 [L617] CALL     A=10 B=1 C=7 D=263 
00169 [L621] KSHORT   A=10 B=0 C=1 D=1 1
00170 [L621] LEN      A=11 B=0 C=5 D=5 
00171 [L621] KSHORT   A=12 B=0 C=1 D=1 1
00172 [L621] FORI     A=10 B=128 C=104 D=32872 target=277
00173 [L622] TGETV    A=14 B=5 C=13 D=1293 
00174 [L622] TGETS    A=14 B=14 C=45 D=3629 'cur_action'
00175 [L622] ISNEV    A=14 B=0 C=9 D=9 
00176 [L622] JMP      A=14 B=128 C=99 D=32867 target=276
00177 [L623] MOV      A=14 B=0 C=4 D=4 
00178 [L623] KSTR     A=15 B=0 C=46 D=46 '--'
00179 [L623] MOV      A=16 B=0 C=9 D=9 
00180 [L623] KSTR     A=17 B=0 C=47 D=47 '--\t'
00181 [L623] CAT      A=4 B=14 C=17 D=3601 
00182 [L624] MOV      A=14 B=0 C=4 D=4 
00183 [L624] KSTR     A=15 B=0 C=48 D=48 '['
00184 [L624] TGETV    A=16 B=5 C=13 D=1293 
00185 [L624] TGETS    A=16 B=16 C=49 D=4145 'logic_type'
00186 [L624] KSTR     A=17 B=0 C=50 D=50 ']\t'
00187 [L624] CAT      A=4 B=14 C=17 D=3601 
00188 [L626] KPRI     A=14 B=0 C=0 D=0 
00189 [L627] TGETV    A=15 B=5 C=13 D=1293 
00190 [L627] TGETS    A=15 B=15 C=51 D=3891 'who_use'
00191 [L627] ISNEN    A=15 B=0 C=0 D=0 1
00192 [L627] JMP      A=15 B=128 C=12 D=32780 target=205
00193 [L627] TGETV    A=15 B=5 C=13 D=1293 
00194 [L627] TGETS    A=15 B=15 C=52 D=3892 'self_use'
00195 [L627] ISNEP    A=15 B=0 C=2 D=2 
00196 [L627] JMP      A=15 B=128 C=8 D=32776 target=205
00197 [L628] MOV      A=15 B=0 C=4 D=4 
00198 [L628] KSTR     A=16 B=0 C=23 D=23 'o'
00199 [L628] TGETV    A=17 B=5 C=13 D=1293 
00200 [L628] TGETS    A=17 B=17 C=41 D=4393 'src_order'
00201 [L628] KSTR     A=18 B=0 C=53 D=53 ' -> '
00202 [L628] CAT      A=4 B=15 C=18 D=3858 
00203 [L629] KSTR     A=14 B=0 C=23 D=23 'o'
00204 [L629] JMP      A=15 B=128 C=39 D=32807 target=244
00205 [L630] TGETV    A=15 B=5 C=13 D=1293 
00206 [L630] TGETS    A=15 B=15 C=51 D=3891 'who_use'
00207 [L630] ISNEN    A=15 B=0 C=0 D=0 1
00208 [L630] JMP      A=15 B=128 C=12 D=32780 target=221
00209 [L630] TGETV    A=15 B=5 C=13 D=1293 
00210 [L630] TGETS    A=15 B=15 C=52 D=3892 'self_use'
00211 [L630] ISNEP    A=15 B=0 C=1 D=1 
00212 [L630] JMP      A=15 B=128 C=8 D=32776 target=221
00213 [L631] MOV      A=15 B=0 C=4 D=4 
00214 [L631] KSTR     A=16 B=0 C=23 D=23 'o'
00215 [L631] TGETV    A=17 B=5 C=13 D=1293 
00216 [L631] TGETS    A=17 B=17 C=41 D=4393 'src_order'
00217 [L631] KSTR     A=18 B=0 C=53 D=53 ' -> '
00218 [L631] CAT      A=4 B=15 C=18 D=3858 
00219 [L632] KSTR     A=14 B=0 C=27 D=27 'e'
00220 [L632] JMP      A=15 B=128 C=23 D=32791 target=244
00221 [L633] TGETV    A=15 B=5 C=13 D=1293 
00222 [L633] TGETS    A=15 B=15 C=51 D=3891 'who_use'
00223 [L633] ISNEN    A=15 B=0 C=1 D=1 2
00224 [L633] JMP      A=15 B=128 C=12 D=32780 target=237
00225 [L633] TGETV    A=15 B=5 C=13 D=1293 
00226 [L633] TGETS    A=15 B=15 C=52 D=3892 'self_use'
00227 [L633] ISNEP    A=15 B=0 C=2 D=2 
00228 [L633] JMP      A=15 B=128 C=8 D=32776 target=237
00229 [L634] MOV      A=15 B=0 C=4 D=4 
00230 [L634] KSTR     A=16 B=0 C=27 D=27 'e'
00231 [L634] TGETV    A=17 B=5 C=13 D=1293 
00232 [L634] TGETS    A=17 B=17 C=41 D=4393 'src_order'
00233 [L634] KSTR     A=18 B=0 C=53 D=53 ' -> '
00234 [L634] CAT      A=4 B=15 C=18 D=3858 
00235 [L635] KSTR     A=14 B=0 C=27 D=27 'e'
00236 [L635] JMP      A=15 B=128 C=7 D=32775 target=244
00237 [L637] MOV      A=15 B=0 C=4 D=4 
00238 [L637] KSTR     A=16 B=0 C=27 D=27 'e'
00239 [L637] TGETV    A=17 B=5 C=13 D=1293 
00240 [L637] TGETS    A=17 B=17 C=41 D=4393 'src_order'
00241 [L637] KSTR     A=18 B=0 C=53 D=53 ' -> '
00242 [L637] CAT      A=4 B=15 C=18 D=3858 
00243 [L638] KSTR     A=14 B=0 C=23 D=23 'o'
00244 [L641] KSHORT   A=15 B=0 C=1 D=1 1
00245 [L641] TGETV    A=16 B=5 C=13 D=1293 
00246 [L641] TGETS    A=16 B=16 C=54 D=4150 'skill_result_list'
00247 [L641] LEN      A=16 B=0 C=16 D=16 
00248 [L641] KSHORT   A=17 B=0 C=1 D=1 1
00249 [L641] FORI     A=15 B=128 C=23 D=32791 target=273
00250 [L642] MOV      A=19 B=0 C=4 D=4 
00251 [L642] KSTR     A=20 B=0 C=48 D=48 '['
00252 [L642] MOV      A=21 B=0 C=14 D=14 
00253 [L642] TGETV    A=22 B=5 C=13 D=1293 
00254 [L642] TGETS    A=22 B=22 C=54 D=5686 'skill_result_list'
00255 [L642] TGETV    A=22 B=22 C=18 D=5650 
00256 [L642] TGETS    A=22 B=22 C=42 D=5674 'des_order'
00257 [L642] KSTR     A=23 B=0 C=55 D=55 '='
00258 [L642] TGETV    A=24 B=5 C=13 D=1293 
00259 [L642] TGETS    A=24 B=24 C=54 D=6198 'skill_result_list'
00260 [L642] TGETV    A=24 B=24 C=18 D=6162 
00261 [L642] TGETS    A=24 B=24 C=56 D=6200 'field_plus'
00262 [L642] KSTR     A=25 B=0 C=57 D=57 '('
00263 [L642] TGETV    A=26 B=5 C=13 D=1293 
00264 [L642] TGETS    A=26 B=26 C=54 D=6710 'skill_result_list'
00265 [L642] TGETV    A=26 B=26 C=18 D=6674 
00266 [L642] TGETS    A=26 B=26 C=58 D=6714 'field'
00267 [L642] IST      A=0 B=0 C=26 D=26 
00268 [L642] JMP      A=27 B=128 C=1 D=32769 target=270
00269 [L642] KSHORT   A=26 B=0 C=0 D=0 0
00270 [L642] KSTR     A=27 B=0 C=59 D=59 ')]'
00271 [L642] CAT      A=4 B=19 C=27 D=4891 
00272 [L641] FORL     A=15 B=127 C=233 D=32745 target=250
00273 [L645] MOV      A=15 B=0 C=4 D=4 
00274 [L645] KSTR     A=16 B=0 C=12 D=12 '\n'
00275 [L645] CAT      A=4 B=15 C=16 D=3856 
00276 [L621] FORL     A=10 B=127 C=152 D=32664 target=173
00277 [L649] MOV      A=10 B=0 C=4 D=4 
00278 [L649] KSTR     A=11 B=0 C=46 D=46 '--'
00279 [L649] MOV      A=12 B=0 C=9 D=9 
00280 [L649] KSTR     A=13 B=0 C=47 D=47 '--\t'
00281 [L649] CAT      A=4 B=10 C=13 D=2573 
00282 [L651] TGETS    A=10 B=1 C=35 D=291 'fight_result'
00283 [L651] TGETV    A=10 B=10 C=9 D=2569 
00284 [L652] MOV      A=11 B=0 C=4 D=4 
00285 [L652] KSTR     A=12 B=0 C=48 D=48 '['
00286 [L652] TGETS    A=13 B=10 C=43 D=2603 'skill_type'
00287 [L652] KSTR     A=14 B=0 C=50 D=50 ']\t'
00288 [L652] CAT      A=4 B=11 C=14 D=2830 
00289 [L654] KPRI     A=11 B=0 C=0 D=0 
00290 [L655] TGETS    A=12 B=10 C=60 D=2620 'is_src'
00291 [L655] ISNEP    A=12 B=0 C=2 D=2 
00292 [L655] JMP      A=12 B=128 C=10 D=32778 target=303
00293 [L655] TGETS    A=12 B=10 C=52 D=2612 'self_use'
00294 [L655] ISNEP    A=12 B=0 C=2 D=2 
00295 [L655] JMP      A=12 B=128 C=7 D=32775 target=303
00296 [L656] MOV      A=12 B=0 C=4 D=4 
00297 [L656] KSTR     A=13 B=0 C=23 D=23 'o'
00298 [L656] TGETS    A=14 B=10 C=41 D=2601 'src_order'
00299 [L656] KSTR     A=15 B=0 C=53 D=53 ' -> '
00300 [L656] CAT      A=4 B=12 C=15 D=3087 
00301 [L657] KSTR     A=11 B=0 C=23 D=23 'o'
00302 [L657] JMP      A=12 B=128 C=32 D=32800 target=335
00303 [L658] TGETS    A=12 B=10 C=60 D=2620 'is_src'
00304 [L658] ISNEP    A=12 B=0 C=2 D=2 
00305 [L658] JMP      A=12 B=128 C=10 D=32778 target=316
00306 [L658] TGETS    A=12 B=10 C=52 D=2612 'self_use'
00307 [L658] ISNEP    A=12 B=0 C=1 D=1 
00308 [L658] JMP      A=12 B=128 C=7 D=32775 target=316
00309 [L659] MOV      A=12 B=0 C=4 D=4 
00310 [L659] KSTR     A=13 B=0 C=23 D=23 'o'
00311 [L659] TGETS    A=14 B=10 C=41 D=2601 'src_order'
00312 [L659] KSTR     A=15 B=0 C=53 D=53 ' -> '
00313 [L659] CAT      A=4 B=12 C=15 D=3087 
00314 [L660] KSTR     A=11 B=0 C=27 D=27 'e'
00315 [L660] JMP      A=12 B=128 C=19 D=32787 target=335
00316 [L661] TGETS    A=12 B=10 C=60 D=2620 'is_src'
00317 [L661] ISNEP    A=12 B=0 C=1 D=1 
00318 [L661] JMP      A=12 B=128 C=10 D=32778 target=329
00319 [L661] TGETS    A=12 B=10 C=52 D=2612 'self_use'
00320 [L661] ISNEP    A=12 B=0 C=2 D=2 
00321 [L661] JMP      A=12 B=128 C=7 D=32775 target=329
00322 [L662] MOV      A=12 B=0 C=4 D=4 
00323 [L662] KSTR     A=13 B=0 C=27 D=27 'e'
00324 [L662] TGETS    A=14 B=10 C=41 D=2601 'src_order'
00325 [L662] KSTR     A=15 B=0 C=53 D=53 ' -> '
00326 [L662] CAT      A=4 B=12 C=15 D=3087 
00327 [L663] KSTR     A=11 B=0 C=27 D=27 'e'
00328 [L663] JMP      A=12 B=128 C=6 D=32774 target=335
00329 [L665] MOV      A=12 B=0 C=4 D=4 
00330 [L665] KSTR     A=13 B=0 C=27 D=27 'e'
00331 [L665] TGETS    A=14 B=10 C=41 D=2601 'src_order'
00332 [L665] KSTR     A=15 B=0 C=53 D=53 ' -> '
00333 [L665] CAT      A=4 B=12 C=15 D=3087 
00334 [L666] KSTR     A=11 B=0 C=23 D=23 'o'
00335 [L669] KSHORT   A=12 B=0 C=1 D=1 1
00336 [L669] TGETS    A=13 B=10 C=61 D=2621 'damage_count'
00337 [L669] KSHORT   A=14 B=0 C=1 D=1 1
00338 [L669] FORI     A=12 B=128 C=15 D=32783 target=354
00339 [L670] TGETS    A=16 B=10 C=44 D=2604 'damage_list'
00340 [L670] TGETV    A=16 B=16 C=15 D=4111 
00341 [L670] KSHORT   A=17 B=0 C=0 D=0 0
00342 [L670] ISGE     A=17 B=0 C=16 D=16 
00343 [L670] JMP      A=16 B=128 C=9 D=32777 target=353
00344 [L671] MOV      A=16 B=0 C=4 D=4 
00345 [L671] KSTR     A=17 B=0 C=48 D=48 '['
00346 [L671] MOV      A=18 B=0 C=11 D=11 
00347 [L671] MOV      A=19 B=0 C=15 D=15 
00348 [L671] KSTR     A=20 B=0 C=55 D=55 '='
00349 [L671] TGETS    A=21 B=10 C=44 D=2604 'damage_list'
00350 [L671] TGETV    A=21 B=21 C=15 D=5391 
00351 [L671] KSTR     A=22 B=0 C=62 D=62 ']'
00352 [L671] CAT      A=4 B=16 C=22 D=4118 
00353 [L669] FORL     A=12 B=127 C=241 D=32753 target=339
00354 [L674] MOV      A=12 B=0 C=4 D=4 
00355 [L674] KSTR     A=13 B=0 C=12 D=12 '\n'
00356 [L674] CAT      A=4 B=12 C=13 D=3085 
00357 [L616] FORL     A=6 B=127 C=50 D=32562 target=152
00358 [L677] MOV      A=6 B=0 C=4 D=4 
00359 [L677] KSTR     A=7 B=0 C=63 D=63 '=================end======================\n\n\n\n'
00360 [L677] CAT      A=4 B=6 C=7 D=1543 
00361 [L680] UGET     A=6 B=0 C=3 D=3 CCFileUtils
00362 [L680] MOV      A=7 B=0 C=6 D=6 
00363 [L680] TGETS    A=6 B=6 C=64 D=1600 'sharedFileUtils'
00364 [L680] CALL     A=6 B=2 C=2 D=514 
00365 [L680] MOV      A=7 B=0 C=6 D=6 
00366 [L680] TGETS    A=6 B=6 C=65 D=1601 'getWriteablePath'
00367 [L680] CALL     A=6 B=2 C=2 D=514 
00368 [L680] KSTR     A=7 B=0 C=66 D=66 'setting_w/'
00369 [L680] UGET     A=8 B=0 C=4 D=4 string
00370 [L680] TGETS    A=8 B=8 C=67 D=2115 'format'
00371 [L680] KSTR     A=9 B=0 C=68 D=68 '%0.0f'
00372 [L680] GGET     A=10 B=0 C=17 D=17 'd_ms'
00373 [L680] TGETS    A=10 B=10 C=69 D=2629 'd_mainUI'
00374 [L680] TGETS    A=10 B=10 C=70 D=2630 'g_playerInfo'
00375 [L680] TGETS    A=10 B=10 C=71 D=2631 'role_id'
00376 [L680] CALL     A=8 B=2 C=3 D=515 
00377 [L680] KSTR     A=9 B=0 C=72 D=72 '_fight.log'
00378 [L680] CAT      A=6 B=6 C=9 D=1545 
00379 [L681] GGET     A=7 B=0 C=17 D=17 'd_ms'
00380 [L681] TGETS    A=7 B=7 C=73 D=1865 'd_file'
00381 [L681] TGETS    A=7 B=7 C=74 D=1866 'appendFile'
00382 [L681] MOV      A=8 B=0 C=6 D=6 
00383 [L681] MOV      A=9 B=0 C=4 D=4 
00384 [L681] CALL     A=7 B=1 C=3 D=259 
00385 [L685] GGET     A=5 B=0 C=4 D=4 'g_fight_info'
00386 [L685] LEN      A=5 B=0 C=5 D=5 
00387 [L685] KSHORT   A=6 B=0 C=3 D=3 3
00388 [L685] ISGE     A=6 B=0 C=5 D=5 
00389 [L685] JMP      A=5 B=128 C=8 D=32776 target=398
00390 [L686] UGET     A=5 B=0 C=2 D=2 table
00391 [L686] TGETS    A=5 B=5 C=75 D=1355 'remove'
00392 [L686] GGET     A=6 B=0 C=76 D=76 'g_fight_id_list'
00393 [L686] KSHORT   A=7 B=0 C=1 D=1 1
00394 [L686] CALL     A=5 B=2 C=3 D=515 
00395 [L687] GGET     A=6 B=0 C=4 D=4 'g_fight_info'
00396 [L687] KPRI     A=7 B=0 C=0 D=0 
00397 [L687] TSETV    A=7 B=6 C=5 D=1541 
00398 [L690] GGET     A=5 B=0 C=17 D=17 'd_ms'
00399 [L690] TGETS    A=5 B=5 C=77 D=1357 'd_loginUI'
00400 [L690] GGET     A=6 B=0 C=17 D=17 'd_ms'
00401 [L690] TGETS    A=6 B=6 C=77 D=1613 'd_loginUI'
00402 [L690] TGETS    A=6 B=6 C=79 D=1615 'senceID'
00403 [L690] TGETS    A=6 B=6 C=80 D=1616 'fightUI'
00404 [L690] TSETS    A=6 B=5 C=78 D=1358 'g_currentSence'
00405 [L692] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto26 offset=0x3447 source_lines=696-699 params=3
UPVALUES []
00001 [L698] GGET     A=3 B=0 C=0 D=0 'd_ms'
00002 [L698] TGETS    A=3 B=3 C=1 D=769 'd_net'
00003 [L698] TGETS    A=3 B=3 C=2 D=770 'msg_login_rsp_3002'
00004 [L698] MOV      A=4 B=0 C=0 D=0 
00005 [L698] MOV      A=5 B=0 C=1 D=1 
00006 [L698] MOV      A=6 B=0 C=2 D=2 
00007 [L698] CALL     A=3 B=1 C=4 D=260 
00008 [L699] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto27 offset=0x34b6 source_lines=703-707 params=3
UPVALUES ['cclog']
00001 [L704] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L704] KSTR     A=4 B=0 C=0 D=0 'call msg_kick_player_3005'
00003 [L704] CALL     A=3 B=1 C=2 D=258 
00004 [L705] GGET     A=3 B=0 C=1 D=1 'd_ms'
00005 [L705] TGETS    A=3 B=3 C=2 D=770 'd_info'
00006 [L705] TGETS    A=3 B=3 C=3 D=771 'show'
00007 [L705] GGET     A=4 B=0 C=1 D=1 'd_ms'
00008 [L705] TGETS    A=4 B=4 C=4 D=1028 'd_hz'
00009 [L705] TGETS    A=4 B=4 C=5 D=1029 'gethz'
00010 [L705] KSTR     A=5 B=0 C=6 D=6 'kick_player'
00011 [L705] CALL     A=4 B=2 C=2 D=514 
00012 [L705] KSTR     A=5 B=0 C=7 D=7 ', code='
00013 [L705] TGETS    A=6 B=1 C=8 D=264 'reason'
00014 [L705] CAT      A=4 B=4 C=6 D=1030 
00015 [L705] CALL     A=3 B=1 C=2 D=258 
00016 [L706] GGET     A=3 B=0 C=1 D=1 'd_ms'
00017 [L706] TGETS    A=3 B=3 C=9 D=777 'd_net'
00018 [L706] TGETS    A=3 B=3 C=10 D=778 'kick'
00019 [L706] CALL     A=3 B=1 C=1 D=257 
00020 [L707] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto28 offset=0x35a7 source_lines=710-726 params=3
UPVALUES ['cclog', 'string', 'CCDirector']
00001 [L711] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L711] KSTR     A=4 B=0 C=0 D=0 'lua call msg_force_quit_1011, ip=%s, code=%d'
00003 [L711] TGETS    A=5 B=1 C=1 D=257 'client_ip'
00004 [L711] TGETS    A=6 B=1 C=2 D=258 'quit_reason'
00005 [L711] CALL     A=3 B=1 C=4 D=260 
00006 [L713] ISF      A=0 B=0 C=1 D=1 
00007 [L713] JMP      A=3 B=128 C=39 D=32807 target=47
00008 [L713] TGETS    A=3 B=1 C=2 D=258 'quit_reason'
00009 [L713] ISF      A=0 B=0 C=3 D=3 
00010 [L713] JMP      A=4 B=128 C=36 D=32804 target=47
00011 [L713] TGETS    A=3 B=1 C=2 D=258 'quit_reason'
00012 [L713] GGET     A=4 B=0 C=3 D=3 'd_ms'
00013 [L713] TGETS    A=4 B=4 C=4 D=1028 'd_common_def'
00014 [L713] TGETS    A=4 B=4 C=5 D=1029 'disconnect_reason'
00015 [L713] TGETS    A=4 B=4 C=6 D=1030 'repeat_login'
00016 [L713] ISNEV    A=3 B=0 C=4 D=4 
00017 [L713] JMP      A=3 B=128 C=29 D=32797 target=47
00018 [L714] TGETS    A=3 B=1 C=1 D=257 'client_ip'
00019 [L714] IST      A=0 B=0 C=3 D=3 
00020 [L714] JMP      A=4 B=128 C=1 D=32769 target=22
00021 [L714] KSTR     A=3 B=0 C=7 D=7 'unknown'
00022 [L715] UGET     A=4 B=0 C=1 D=1 string
00023 [L715] TGETS    A=4 B=4 C=8 D=1032 'format'
00024 [L715] GGET     A=5 B=0 C=3 D=3 'd_ms'
00025 [L715] TGETS    A=5 B=5 C=9 D=1289 'd_hz'
00026 [L715] TGETS    A=5 B=5 C=10 D=1290 'gethz'
00027 [L715] KSTR     A=6 B=0 C=11 D=11 'player_relogin'
00028 [L715] CALL     A=5 B=2 C=2 D=514 
00029 [L715] MOV      A=6 B=0 C=3 D=3 
00030 [L715] CALL     A=4 B=2 C=3 D=515 
00031 [L717] TDUP     A=5 B=0 C=12 D=12 {'kind': 'table', 'value': {'Zorder': 9999, 'ensureBtnOnly': True}}
00032 [L717] TSETS    A=4 B=5 C=13 D=1293 'string'
00033 [L718] UGET     A=6 B=0 C=2 D=2 CCDirector
00034 [L718] MOV      A=7 B=0 C=6 D=6 
00035 [L718] TGETS    A=6 B=6 C=14 D=1550 'sharedDirector'
00036 [L718] CALL     A=6 B=2 C=2 D=514 
00037 [L718] MOV      A=7 B=0 C=6 D=6 
00038 [L718] TGETS    A=6 B=6 C=15 D=1551 'getRunningScene'
00039 [L718] CALL     A=6 B=2 C=2 D=514 
00040 [L719] GGET     A=7 B=0 C=3 D=3 'd_ms'
00041 [L719] TGETS    A=7 B=7 C=16 D=1808 'd_quitUI'
00042 [L719] TGETS    A=7 B=7 C=17 D=1809 'createYesNoByStyle'
00043 [L719] MOV      A=8 B=0 C=6 D=6 
00044 [L719] MOV      A=9 B=0 C=5 D=5 
00045 [L719] CALL     A=7 B=1 C=3 D=259 
00046 [L719] JMP      A=3 B=128 C=15 D=32783 target=62
00047 [L722] GGET     A=3 B=0 C=3 D=3 'd_ms'
00048 [L722] TGETS    A=3 B=3 C=18 D=786 'd_info'
00049 [L722] TGETS    A=3 B=3 C=19 D=787 'show'
00050 [L722] GGET     A=4 B=0 C=3 D=3 'd_ms'
00051 [L722] TGETS    A=4 B=4 C=9 D=1033 'd_hz'
00052 [L722] TGETS    A=4 B=4 C=10 D=1034 'gethz'
00053 [L722] KSTR     A=5 B=0 C=20 D=20 'kick_player'
00054 [L722] CALL     A=4 B=2 C=2 D=514 
00055 [L722] KSHORT   A=5 B=0 C=5 D=5 5
00056 [L722] KNUM     A=6 B=0 C=0 D=0 0.5
00057 [L722] CALL     A=3 B=1 C=4 D=260 
00058 [L723] GGET     A=3 B=0 C=3 D=3 'd_ms'
00059 [L723] TGETS    A=3 B=3 C=21 D=789 'd_net'
00060 [L723] TGETS    A=3 B=3 C=22 D=790 'kick'
00061 [L723] CALL     A=3 B=1 C=1 D=257 
00062 [L726] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto29 offset=0x3873 source_lines=729-737 params=3
UPVALUES ['cclog']
00001 [L730] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L730] KSTR     A=4 B=0 C=0 D=0 'call msg_query_item_list_1034'
00003 [L730] CALL     A=3 B=1 C=2 D=258 
00004 [L731] MOV      A=3 B=0 C=1 D=1 
00005 [L733] ISEQP    A=1 B=0 C=0 D=0 
00006 [L733] JMP      A=4 B=128 C=8 D=32776 target=15
00007 [L733] TGETS    A=4 B=1 C=1 D=257 'cortege_list'
00008 [L733] ISEQP    A=4 B=0 C=0 D=0 
00009 [L733] JMP      A=4 B=128 C=5 D=32773 target=15
00010 [L734] GGET     A=4 B=0 C=2 D=2 'd_ms'
00011 [L734] TGETS    A=4 B=4 C=3 D=1027 'd_lineupUI'
00012 [L734] TGETS    A=4 B=4 C=4 D=1028 'getDateFormServer'
00013 [L734] MOV      A=5 B=0 C=1 D=1 
00014 [L734] CALL     A=4 B=1 C=2 D=258 
00015 [L736] UGET     A=4 B=0 C=0 D=0 cclog
00016 [L736] KSTR     A=5 B=0 C=5 D=5 'call msg_query_item_list_1034 end'
00017 [L736] CALL     A=4 B=1 C=2 D=258 
00018 [L737] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto30 offset=0x3975 source_lines=740-749 params=3
UPVALUES ['cclog']
00001 [L741] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L741] KSTR     A=4 B=0 C=0 D=0 'call msg_query_item_list_1035'
00003 [L741] CALL     A=3 B=1 C=2 D=258 
00004 [L742] MOV      A=3 B=0 C=1 D=1 
00005 [L744] ISEQP    A=1 B=0 C=0 D=0 
00006 [L744] JMP      A=4 B=128 C=8 D=32776 target=15
00007 [L744] TGETS    A=4 B=1 C=1 D=257 'attach_list'
00008 [L744] ISEQP    A=4 B=0 C=0 D=0 
00009 [L744] JMP      A=4 B=128 C=5 D=32773 target=15
00010 [L745] GGET     A=4 B=0 C=2 D=2 'd_ms'
00011 [L745] TGETS    A=4 B=4 C=3 D=1027 'd_packageUI'
00012 [L745] TGETS    A=4 B=4 C=4 D=1028 'getDateFormServer'
00013 [L745] MOV      A=5 B=0 C=1 D=1 
00014 [L745] CALL     A=4 B=1 C=2 D=258 
00015 [L748] UGET     A=4 B=0 C=0 D=0 cclog
00016 [L748] KSTR     A=5 B=0 C=5 D=5 'call msg_query_item_list_1035 end'
00017 [L748] CALL     A=4 B=1 C=2 D=258 
00018 [L749] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto31 offset=0x3a77 source_lines=751-759 params=3
UPVALUES ['cclog']
00001 [L752] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L752] KSTR     A=4 B=0 C=0 D=0 ' call msg_update_spirit_list_1046 '
00003 [L752] CALL     A=3 B=1 C=2 D=258 
00004 [L753] MOV      A=3 B=0 C=1 D=1 
00005 [L755] ISEQP    A=1 B=0 C=0 D=0 
00006 [L755] JMP      A=4 B=128 C=12 D=32780 target=19
00007 [L755] TGETS    A=4 B=1 C=1 D=257 'spirit_count'
00008 [L755] ISEQN    A=4 B=0 C=0 D=0 0
00009 [L755] JMP      A=4 B=128 C=9 D=32777 target=19
00010 [L756] GGET     A=4 B=0 C=2 D=2 'd_ms'
00011 [L756] TGETS    A=4 B=4 C=3 D=1027 'd_alert'
00012 [L756] TGETS    A=4 B=4 C=4 D=1028 'stop_wait'
00013 [L756] CALL     A=4 B=1 C=1 D=257 
00014 [L757] GGET     A=4 B=0 C=2 D=2 'd_ms'
00015 [L757] TGETS    A=4 B=4 C=5 D=1029 'd_data'
00016 [L757] TGETS    A=4 B=4 C=6 D=1030 'recvSoulsDataFromServer'
00017 [L757] MOV      A=5 B=0 C=1 D=1 
00018 [L757] CALL     A=4 B=1 C=2 D=258 
00019 [L759] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto32 offset=0x3b76 source_lines=763-895 params=3
UPVALUES ['cclog']
00001 [L766] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L766] KSTR     A=4 B=0 C=0 D=0 'call msg_update_tollgate_data_1019'
00003 [L766] CALL     A=3 B=1 C=2 D=258 
00004 [L767] GGET     A=3 B=0 C=1 D=1 'd_ms'
00005 [L767] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00006 [L767] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00007 [L767] TGETS    A=3 B=3 C=4 D=772 'maps'
00008 [L767] TGETS    A=4 B=1 C=5 D=261 'map_id'
00009 [L767] TGETV    A=3 B=3 C=4 D=772 
00010 [L767] ISF      A=0 B=0 C=3 D=3 
00011 [L767] JMP      A=4 B=130 C=66 D=33346 target=590
00012 [L769] TGETS    A=3 B=1 C=6 D=262 'tollgate_type'
00013 [L769] ISNEN    A=3 B=0 C=0 D=0 2
00014 [L769] JMP      A=3 B=128 C=247 D=33015 target=262
00015 [L771] UGET     A=3 B=0 C=0 D=0 cclog
00016 [L771] KSTR     A=4 B=0 C=7 D=7 'elite tollgate'
00017 [L771] CALL     A=3 B=1 C=2 D=258 
00018 [L772] GGET     A=3 B=0 C=1 D=1 'd_ms'
00019 [L772] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00020 [L772] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00021 [L772] TGETS    A=3 B=3 C=4 D=772 'maps'
00022 [L772] TGETS    A=4 B=1 C=5 D=261 'map_id'
00023 [L772] TGETV    A=3 B=3 C=4 D=772 
00024 [L772] TGETS    A=3 B=3 C=8 D=776 'tollgates_elite'
00025 [L772] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00026 [L772] TGETV    A=3 B=3 C=4 D=772 
00027 [L772] ISF      A=0 B=0 C=3 D=3 
00028 [L772] JMP      A=4 B=128 C=25 D=32793 target=54
00029 [L773] GGET     A=3 B=0 C=1 D=1 'd_ms'
00030 [L773] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00031 [L773] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00032 [L773] TGETS    A=3 B=3 C=4 D=772 'maps'
00033 [L773] TGETS    A=4 B=1 C=5 D=261 'map_id'
00034 [L773] TGETV    A=3 B=3 C=4 D=772 
00035 [L773] TGETS    A=3 B=3 C=8 D=776 'tollgates_elite'
00036 [L773] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00037 [L773] TGETV    A=3 B=3 C=4 D=772 
00038 [L773] TGETS    A=3 B=3 C=10 D=778 'pass_star'
00039 [L773] KSHORT   A=4 B=0 C=0 D=0 0
00040 [L773] ISGE     A=4 B=0 C=3 D=3 
00041 [L773] JMP      A=3 B=128 C=6 D=32774 target=48
00042 [L774] GGET     A=3 B=0 C=1 D=1 'd_ms'
00043 [L774] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00044 [L774] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00045 [L774] KPRI     A=4 B=0 C=2 D=2 
00046 [L774] TSETS    A=4 B=3 C=11 D=779 'isFarmStar'
00047 [L774] JMP      A=3 B=128 C=13 D=32781 target=61
00048 [L776] GGET     A=3 B=0 C=1 D=1 'd_ms'
00049 [L776] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00050 [L776] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00051 [L776] KPRI     A=4 B=0 C=1 D=1 
00052 [L776] TSETS    A=4 B=3 C=11 D=779 'isFarmStar'
00053 [L777] JMP      A=3 B=128 C=7 D=32775 target=61
00054 [L779] UGET     A=3 B=0 C=0 D=0 cclog
00055 [L779] KSTR     A=4 B=0 C=12 D=12 'ERROR: unfind tollgates_elite, m_id='
00056 [L779] TGETS    A=5 B=1 C=5 D=261 'map_id'
00057 [L779] KSTR     A=6 B=0 C=13 D=13 ', t_id='
00058 [L779] TGETS    A=7 B=1 C=9 D=265 'tollgate_id'
00059 [L779] CAT      A=4 B=4 C=7 D=1031 
00060 [L779] CALL     A=3 B=1 C=2 D=258 
00061 [L783] TGETS    A=3 B=1 C=10 D=266 'pass_star'
00062 [L783] KSHORT   A=4 B=0 C=1 D=1 1
00063 [L783] ISGT     A=4 B=0 C=3 D=3 
00064 [L783] JMP      A=3 B=128 C=112 D=32880 target=177
00065 [L783] TGETS    A=3 B=1 C=10 D=266 'pass_star'
00066 [L783] KSHORT   A=4 B=0 C=3 D=3 3
00067 [L783] ISGT     A=3 B=0 C=4 D=4 
00068 [L783] JMP      A=3 B=128 C=108 D=32876 target=177
00069 [L785] GGET     A=3 B=0 C=1 D=1 'd_ms'
00070 [L785] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00071 [L785] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00072 [L785] TGETS    A=3 B=3 C=4 D=772 'maps'
00073 [L785] TGETS    A=4 B=1 C=5 D=261 'map_id'
00074 [L785] ADDVN    A=4 B=4 C=1 D=1025 
00075 [L785] TGETV    A=3 B=3 C=4 D=772 
00076 [L785] ISF      A=0 B=0 C=3 D=3 
00077 [L785] JMP      A=4 B=128 C=99 D=32867 target=177
00078 [L786] GGET     A=3 B=0 C=1 D=1 'd_ms'
00079 [L786] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00080 [L786] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00081 [L786] TGETS    A=3 B=3 C=4 D=772 'maps'
00082 [L786] TGETS    A=4 B=1 C=5 D=261 'map_id'
00083 [L786] ADDVN    A=4 B=4 C=1 D=1025 
00084 [L786] TGETV    A=3 B=3 C=4 D=772 
00085 [L786] TGETS    A=3 B=3 C=8 D=776 'tollgates_elite'
00086 [L786] TGETS    A=4 B=1 C=5 D=261 'map_id'
00087 [L786] ADDVN    A=4 B=4 C=1 D=1025 
00088 [L786] MULVN    A=4 B=4 C=2 D=1026 
00089 [L786] ADDVN    A=4 B=4 C=1 D=1025 
00090 [L786] TGETV    A=3 B=3 C=4 D=772 
00091 [L786] ISF      A=0 B=0 C=3 D=3 
00092 [L786] JMP      A=4 B=128 C=84 D=32852 target=177
00093 [L787] GGET     A=3 B=0 C=1 D=1 'd_ms'
00094 [L787] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00095 [L787] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00096 [L787] TGETS    A=3 B=3 C=4 D=772 'maps'
00097 [L787] TGETS    A=4 B=1 C=5 D=261 'map_id'
00098 [L787] ADDVN    A=4 B=4 C=1 D=1025 
00099 [L787] TGETV    A=3 B=3 C=4 D=772 
00100 [L787] TGETS    A=3 B=3 C=8 D=776 'tollgates_elite'
00101 [L787] TGETS    A=4 B=1 C=5 D=261 'map_id'
00102 [L787] ADDVN    A=4 B=4 C=1 D=1025 
00103 [L787] MULVN    A=4 B=4 C=2 D=1026 
00104 [L787] ADDVN    A=4 B=4 C=1 D=1025 
00105 [L787] TGETV    A=3 B=3 C=4 D=772 
00106 [L787] TGETS    A=3 B=3 C=10 D=778 'pass_star'
00107 [L787] ISEQP    A=3 B=0 C=0 D=0 
00108 [L787] JMP      A=3 B=128 C=16 D=32784 target=125
00109 [L788] GGET     A=3 B=0 C=1 D=1 'd_ms'
00110 [L788] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00111 [L788] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00112 [L788] TGETS    A=3 B=3 C=4 D=772 'maps'
00113 [L788] TGETS    A=4 B=1 C=5 D=261 'map_id'
00114 [L788] ADDVN    A=4 B=4 C=1 D=1025 
00115 [L788] TGETV    A=3 B=3 C=4 D=772 
00116 [L788] TGETS    A=3 B=3 C=8 D=776 'tollgates_elite'
00117 [L788] TGETS    A=4 B=1 C=5 D=261 'map_id'
00118 [L788] ADDVN    A=4 B=4 C=1 D=1025 
00119 [L788] MULVN    A=4 B=4 C=2 D=1026 
00120 [L788] ADDVN    A=4 B=4 C=1 D=1025 
00121 [L788] TGETV    A=3 B=3 C=4 D=772 
00122 [L788] TGETS    A=3 B=3 C=10 D=778 'pass_star'
00123 [L788] ISNEN    A=3 B=0 C=3 D=3 0
00124 [L788] JMP      A=3 B=128 C=52 D=32820 target=177
00125 [L790] GGET     A=3 B=0 C=1 D=1 'd_ms'
00126 [L790] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00127 [L790] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00128 [L790] TGETS    A=3 B=3 C=4 D=772 'maps'
00129 [L790] TGETS    A=4 B=1 C=5 D=261 'map_id'
00130 [L790] ADDVN    A=4 B=4 C=1 D=1025 
00131 [L790] TGETV    A=3 B=3 C=4 D=772 
00132 [L790] TGETS    A=3 B=3 C=8 D=776 'tollgates_elite'
00133 [L790] TGETS    A=4 B=1 C=5 D=261 'map_id'
00134 [L790] ADDVN    A=4 B=4 C=1 D=1025 
00135 [L790] MULVN    A=4 B=4 C=2 D=1026 
00136 [L790] ADDVN    A=4 B=4 C=1 D=1025 
00137 [L790] TGETV    A=3 B=3 C=4 D=772 
00138 [L790] KSHORT   A=4 B=0 C=0 D=0 0
00139 [L790] TSETS    A=4 B=3 C=10 D=778 'pass_star'
00140 [L791] GGET     A=3 B=0 C=1 D=1 'd_ms'
00141 [L791] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00142 [L791] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00143 [L791] TGETS    A=3 B=3 C=4 D=772 'maps'
00144 [L791] TGETS    A=4 B=1 C=5 D=261 'map_id'
00145 [L791] ADDVN    A=4 B=4 C=1 D=1025 
00146 [L791] TGETV    A=3 B=3 C=4 D=772 
00147 [L791] TGETS    A=3 B=3 C=8 D=776 'tollgates_elite'
00148 [L791] TGETS    A=4 B=1 C=5 D=261 'map_id'
00149 [L791] ADDVN    A=4 B=4 C=1 D=1025 
00150 [L791] MULVN    A=4 B=4 C=2 D=1026 
00151 [L791] ADDVN    A=4 B=4 C=1 D=1025 
00152 [L791] TGETV    A=3 B=3 C=4 D=772 
00153 [L791] KSHORT   A=4 B=0 C=0 D=0 0
00154 [L791] TSETS    A=4 B=3 C=14 D=782 'day_count'
00155 [L793] GGET     A=3 B=0 C=1 D=1 'd_ms'
00156 [L793] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00157 [L793] TGETS    A=3 B=3 C=15 D=783 'isAllTollgatePassed'
00158 [L793] TGETS    A=4 B=1 C=5 D=261 'map_id'
00159 [L793] KSHORT   A=5 B=0 C=1 D=1 1
00160 [L793] CALL     A=3 B=2 C=3 D=515 
00161 [L793] ISF      A=0 B=0 C=3 D=3 
00162 [L793] JMP      A=4 B=128 C=14 D=32782 target=177
00163 [L794] GGET     A=3 B=0 C=1 D=1 'd_ms'
00164 [L794] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00165 [L794] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00166 [L794] TGETS    A=4 B=1 C=5 D=261 'map_id'
00167 [L794] ADDVN    A=4 B=4 C=1 D=1025 
00168 [L794] TSETS    A=4 B=3 C=16 D=784 'lastUnpassMID_elite'
00169 [L795] GGET     A=3 B=0 C=1 D=1 'd_ms'
00170 [L795] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00171 [L795] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00172 [L795] TGETS    A=4 B=1 C=5 D=261 'map_id'
00173 [L795] ADDVN    A=4 B=4 C=1 D=1025 
00174 [L795] MULVN    A=4 B=4 C=2 D=1026 
00175 [L795] ADDVN    A=4 B=4 C=1 D=1025 
00176 [L795] TSETS    A=4 B=3 C=17 D=785 'lastUnpassTID_elite'
00177 [L801] GGET     A=3 B=0 C=1 D=1 'd_ms'
00178 [L801] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00179 [L801] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00180 [L801] TGETS    A=3 B=3 C=4 D=772 'maps'
00181 [L801] TGETS    A=4 B=1 C=5 D=261 'map_id'
00182 [L801] TGETV    A=3 B=3 C=4 D=772 
00183 [L801] TGETS    A=3 B=3 C=8 D=776 'tollgates_elite'
00184 [L801] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00185 [L801] TGETV    A=3 B=3 C=4 D=772 
00186 [L801] GGET     A=4 B=0 C=1 D=1 'd_ms'
00187 [L801] TGETS    A=4 B=4 C=2 D=1026 'd_mapUI'
00188 [L801] TGETS    A=4 B=4 C=3 D=1027 'g_mapUI'
00189 [L801] TGETS    A=4 B=4 C=4 D=1028 'maps'
00190 [L801] TGETS    A=5 B=1 C=5 D=261 'map_id'
00191 [L801] TGETV    A=4 B=4 C=5 D=1029 
00192 [L801] TGETS    A=4 B=4 C=8 D=1032 'tollgates_elite'
00193 [L801] TGETS    A=5 B=1 C=9 D=265 'tollgate_id'
00194 [L801] TGETV    A=4 B=4 C=5 D=1029 
00195 [L801] TGETS    A=4 B=4 C=10 D=1034 'pass_star'
00196 [L801] TSETS    A=4 B=3 C=18 D=786 'last_pass_star'
00197 [L804] GGET     A=3 B=0 C=1 D=1 'd_ms'
00198 [L804] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00199 [L804] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00200 [L804] TGETS    A=3 B=3 C=4 D=772 'maps'
00201 [L804] TGETS    A=4 B=1 C=5 D=261 'map_id'
00202 [L804] TGETV    A=3 B=3 C=4 D=772 
00203 [L804] TGETS    A=3 B=3 C=8 D=776 'tollgates_elite'
00204 [L804] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00205 [L804] TGETV    A=3 B=3 C=4 D=772 
00206 [L804] TGETS    A=3 B=3 C=10 D=778 'pass_star'
00207 [L804] TGETS    A=4 B=1 C=10 D=266 'pass_star'
00208 [L804] ISGE     A=3 B=0 C=4 D=4 
00209 [L804] JMP      A=3 B=128 C=11 D=32779 target=221
00210 [L805] GGET     A=3 B=0 C=1 D=1 'd_ms'
00211 [L805] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00212 [L805] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00213 [L805] TGETS    A=3 B=3 C=4 D=772 'maps'
00214 [L805] TGETS    A=4 B=1 C=5 D=261 'map_id'
00215 [L805] TGETV    A=3 B=3 C=4 D=772 
00216 [L805] TGETS    A=3 B=3 C=8 D=776 'tollgates_elite'
00217 [L805] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00218 [L805] TGETV    A=3 B=3 C=4 D=772 
00219 [L805] TGETS    A=4 B=1 C=10 D=266 'pass_star'
00220 [L805] TSETS    A=4 B=3 C=10 D=778 'pass_star'
00221 [L808] GGET     A=3 B=0 C=1 D=1 'd_ms'
00222 [L808] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00223 [L808] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00224 [L808] TGETS    A=3 B=3 C=4 D=772 'maps'
00225 [L808] TGETS    A=4 B=1 C=5 D=261 'map_id'
00226 [L808] TGETV    A=3 B=3 C=4 D=772 
00227 [L808] TGETS    A=3 B=3 C=8 D=776 'tollgates_elite'
00228 [L808] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00229 [L808] TGETV    A=3 B=3 C=4 D=772 
00230 [L808] TGETS    A=4 B=1 C=14 D=270 'day_count'
00231 [L808] TSETS    A=4 B=3 C=14 D=782 'day_count'
00232 [L811] GGET     A=3 B=0 C=1 D=1 'd_ms'
00233 [L811] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00234 [L811] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00235 [L811] TGETS    A=3 B=3 C=16 D=784 'lastUnpassMID_elite'
00236 [L811] TGETS    A=4 B=1 C=5 D=261 'map_id'
00237 [L811] ISGE     A=3 B=0 C=4 D=4 
00238 [L811] JMP      A=3 B=128 C=5 D=32773 target=244
00239 [L812] GGET     A=3 B=0 C=1 D=1 'd_ms'
00240 [L812] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00241 [L812] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00242 [L812] TGETS    A=4 B=1 C=5 D=261 'map_id'
00243 [L812] TSETS    A=4 B=3 C=16 D=784 'lastUnpassMID_elite'
00244 [L815] GGET     A=3 B=0 C=1 D=1 'd_ms'
00245 [L815] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00246 [L815] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00247 [L815] TGETS    A=3 B=3 C=17 D=785 'lastUnpassTID_elite'
00248 [L815] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00249 [L815] ISGE     A=3 B=0 C=4 D=4 
00250 [L815] JMP      A=3 B=128 C=5 D=32773 target=256
00251 [L816] GGET     A=3 B=0 C=1 D=1 'd_ms'
00252 [L816] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00253 [L816] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00254 [L816] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00255 [L816] TSETS    A=4 B=3 C=17 D=785 'lastUnpassTID_elite'
00256 [L820] GGET     A=3 B=0 C=1 D=1 'd_ms'
00257 [L820] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00258 [L820] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00259 [L820] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00260 [L820] TSETS    A=4 B=3 C=19 D=787 'last_fight_npc_elite'
00261 [L820] JMP      A=3 B=129 C=76 D=33100 target=594
00262 [L824] GGET     A=3 B=0 C=1 D=1 'd_ms'
00263 [L824] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00264 [L824] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00265 [L824] TGETS    A=3 B=3 C=4 D=772 'maps'
00266 [L824] TGETS    A=4 B=1 C=5 D=261 'map_id'
00267 [L824] TGETV    A=3 B=3 C=4 D=772 
00268 [L824] TGETS    A=3 B=3 C=20 D=788 'tollgates'
00269 [L824] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00270 [L824] TGETV    A=3 B=3 C=4 D=772 
00271 [L824] ISF      A=0 B=0 C=3 D=3 
00272 [L824] JMP      A=4 B=129 C=56 D=33080 target=585
00273 [L826] GGET     A=3 B=0 C=1 D=1 'd_ms'
00274 [L826] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00275 [L826] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00276 [L826] TGETS    A=3 B=3 C=4 D=772 'maps'
00277 [L826] TGETS    A=4 B=1 C=5 D=261 'map_id'
00278 [L826] TGETV    A=3 B=3 C=4 D=772 
00279 [L826] TGETS    A=3 B=3 C=20 D=788 'tollgates'
00280 [L826] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00281 [L826] TGETV    A=3 B=3 C=4 D=772 
00282 [L826] TGETS    A=3 B=3 C=10 D=778 'pass_star'
00283 [L826] KSHORT   A=4 B=0 C=0 D=0 0
00284 [L826] ISGE     A=4 B=0 C=3 D=3 
00285 [L826] JMP      A=3 B=128 C=6 D=32774 target=292
00286 [L827] GGET     A=3 B=0 C=1 D=1 'd_ms'
00287 [L827] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00288 [L827] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00289 [L827] KPRI     A=4 B=0 C=2 D=2 
00290 [L827] TSETS    A=4 B=3 C=11 D=779 'isFarmStar'
00291 [L827] JMP      A=3 B=128 C=5 D=32773 target=297
00292 [L829] GGET     A=3 B=0 C=1 D=1 'd_ms'
00293 [L829] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00294 [L829] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00295 [L829] KPRI     A=4 B=0 C=1 D=1 
00296 [L829] TSETS    A=4 B=3 C=11 D=779 'isFarmStar'
00297 [L832] TGETS    A=3 B=1 C=10 D=266 'pass_star'
00298 [L832] KSHORT   A=4 B=0 C=1 D=1 1
00299 [L832] ISGT     A=4 B=0 C=3 D=3 
00300 [L832] JMP      A=3 B=128 C=189 D=32957 target=490
00301 [L832] TGETS    A=3 B=1 C=10 D=266 'pass_star'
00302 [L832] KSHORT   A=4 B=0 C=3 D=3 3
00303 [L832] ISGT     A=3 B=0 C=4 D=4 
00304 [L832] JMP      A=3 B=128 C=185 D=32953 target=490
00305 [L834] GGET     A=3 B=0 C=1 D=1 'd_ms'
00306 [L834] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00307 [L834] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00308 [L834] TGETS    A=3 B=3 C=4 D=772 'maps'
00309 [L834] TGETS    A=4 B=1 C=5 D=261 'map_id'
00310 [L834] TGETV    A=3 B=3 C=4 D=772 
00311 [L834] ISF      A=0 B=0 C=3 D=3 
00312 [L834] JMP      A=4 B=128 C=69 D=32837 target=382
00313 [L835] GGET     A=3 B=0 C=1 D=1 'd_ms'
00314 [L835] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00315 [L835] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00316 [L835] TGETS    A=3 B=3 C=4 D=772 'maps'
00317 [L835] TGETS    A=4 B=1 C=5 D=261 'map_id'
00318 [L835] TGETV    A=3 B=3 C=4 D=772 
00319 [L835] TGETS    A=3 B=3 C=20 D=788 'tollgates'
00320 [L835] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00321 [L835] ADDVN    A=4 B=4 C=1 D=1025 
00322 [L835] TGETV    A=3 B=3 C=4 D=772 
00323 [L835] ISF      A=0 B=0 C=3 D=3 
00324 [L835] JMP      A=4 B=128 C=57 D=32825 target=382
00325 [L836] GGET     A=3 B=0 C=1 D=1 'd_ms'
00326 [L836] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00327 [L836] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00328 [L836] TGETS    A=3 B=3 C=4 D=772 'maps'
00329 [L836] TGETS    A=4 B=1 C=5 D=261 'map_id'
00330 [L836] TGETV    A=3 B=3 C=4 D=772 
00331 [L836] TGETS    A=3 B=3 C=20 D=788 'tollgates'
00332 [L836] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00333 [L836] ADDVN    A=4 B=4 C=1 D=1025 
00334 [L836] TGETV    A=3 B=3 C=4 D=772 
00335 [L836] TGETS    A=3 B=3 C=10 D=778 'pass_star'
00336 [L836] ISEQP    A=3 B=0 C=0 D=0 
00337 [L836] JMP      A=3 B=128 C=13 D=32781 target=351
00338 [L837] GGET     A=3 B=0 C=1 D=1 'd_ms'
00339 [L837] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00340 [L837] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00341 [L837] TGETS    A=3 B=3 C=4 D=772 'maps'
00342 [L837] TGETS    A=4 B=1 C=5 D=261 'map_id'
00343 [L837] TGETV    A=3 B=3 C=4 D=772 
00344 [L837] TGETS    A=3 B=3 C=20 D=788 'tollgates'
00345 [L837] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00346 [L837] ADDVN    A=4 B=4 C=1 D=1025 
00347 [L837] TGETV    A=3 B=3 C=4 D=772 
00348 [L837] TGETS    A=3 B=3 C=10 D=778 'pass_star'
00349 [L837] ISNEN    A=3 B=0 C=3 D=3 0
00350 [L837] JMP      A=3 B=128 C=31 D=32799 target=382
00351 [L839] GGET     A=3 B=0 C=1 D=1 'd_ms'
00352 [L839] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00353 [L839] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00354 [L839] TGETS    A=3 B=3 C=4 D=772 'maps'
00355 [L839] TGETS    A=4 B=1 C=5 D=261 'map_id'
00356 [L839] TGETV    A=3 B=3 C=4 D=772 
00357 [L839] TGETS    A=3 B=3 C=20 D=788 'tollgates'
00358 [L839] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00359 [L839] ADDVN    A=4 B=4 C=1 D=1025 
00360 [L839] TGETV    A=3 B=3 C=4 D=772 
00361 [L839] KSHORT   A=4 B=0 C=0 D=0 0
00362 [L839] TSETS    A=4 B=3 C=14 D=782 'day_count'
00363 [L840] GGET     A=3 B=0 C=1 D=1 'd_ms'
00364 [L840] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00365 [L840] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00366 [L840] TGETS    A=3 B=3 C=4 D=772 'maps'
00367 [L840] TGETS    A=4 B=1 C=5 D=261 'map_id'
00368 [L840] TGETV    A=3 B=3 C=4 D=772 
00369 [L840] TGETS    A=3 B=3 C=20 D=788 'tollgates'
00370 [L840] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00371 [L840] ADDVN    A=4 B=4 C=1 D=1025 
00372 [L840] TGETV    A=3 B=3 C=4 D=772 
00373 [L840] KSHORT   A=4 B=0 C=0 D=0 0
00374 [L840] TSETS    A=4 B=3 C=10 D=778 'pass_star'
00375 [L841] GGET     A=3 B=0 C=1 D=1 'd_ms'
00376 [L841] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00377 [L841] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00378 [L841] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00379 [L841] ADDVN    A=4 B=4 C=1 D=1025 
00380 [L841] TSETS    A=4 B=3 C=21 D=789 'lastUnpassTID'
00381 [L841] JMP      A=3 B=128 C=108 D=32876 target=490
00382 [L843] TGETS    A=3 B=1 C=9 D=265 'tollgate_id'
00383 [L843] GGET     A=4 B=0 C=1 D=1 'd_ms'
00384 [L843] TGETS    A=4 B=4 C=2 D=1026 'd_mapUI'
00385 [L843] TGETS    A=4 B=4 C=22 D=1046 'getLastTollgate'
00386 [L843] TGETS    A=5 B=1 C=5 D=261 'map_id'
00387 [L843] CALL     A=4 B=2 C=2 D=514 
00388 [L843] ISNEV    A=3 B=0 C=4 D=4 
00389 [L843] JMP      A=3 B=128 C=100 D=32868 target=490
00390 [L846] GGET     A=3 B=0 C=1 D=1 'd_ms'
00391 [L846] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00392 [L846] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00393 [L846] TGETS    A=3 B=3 C=4 D=772 'maps'
00394 [L846] TGETS    A=4 B=1 C=5 D=261 'map_id'
00395 [L846] ADDVN    A=4 B=4 C=1 D=1025 
00396 [L846] TGETV    A=3 B=3 C=4 D=772 
00397 [L846] ISF      A=0 B=0 C=3 D=3 
00398 [L846] JMP      A=4 B=128 C=91 D=32859 target=490
00399 [L847] GGET     A=3 B=0 C=1 D=1 'd_ms'
00400 [L847] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00401 [L847] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00402 [L847] TGETS    A=3 B=3 C=4 D=772 'maps'
00403 [L847] TGETS    A=4 B=1 C=5 D=261 'map_id'
00404 [L847] ADDVN    A=4 B=4 C=1 D=1025 
00405 [L847] TGETV    A=3 B=3 C=4 D=772 
00406 [L847] TGETS    A=3 B=3 C=20 D=788 'tollgates'
00407 [L847] TGETS    A=4 B=1 C=5 D=261 'map_id'
00408 [L847] ADDVN    A=4 B=4 C=1 D=1025 
00409 [L847] MULVN    A=4 B=4 C=2 D=1026 
00410 [L847] ADDVN    A=4 B=4 C=1 D=1025 
00411 [L847] TGETV    A=3 B=3 C=4 D=772 
00412 [L847] ISF      A=0 B=0 C=3 D=3 
00413 [L847] JMP      A=4 B=128 C=76 D=32844 target=490
00414 [L848] GGET     A=3 B=0 C=1 D=1 'd_ms'
00415 [L848] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00416 [L848] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00417 [L848] TGETS    A=3 B=3 C=4 D=772 'maps'
00418 [L848] TGETS    A=4 B=1 C=5 D=261 'map_id'
00419 [L848] ADDVN    A=4 B=4 C=1 D=1025 
00420 [L848] TGETV    A=3 B=3 C=4 D=772 
00421 [L848] TGETS    A=3 B=3 C=20 D=788 'tollgates'
00422 [L848] TGETS    A=4 B=1 C=5 D=261 'map_id'
00423 [L848] ADDVN    A=4 B=4 C=1 D=1025 
00424 [L848] MULVN    A=4 B=4 C=2 D=1026 
00425 [L848] ADDVN    A=4 B=4 C=1 D=1025 
00426 [L848] TGETV    A=3 B=3 C=4 D=772 
00427 [L848] TGETS    A=3 B=3 C=10 D=778 'pass_star'
00428 [L848] ISEQP    A=3 B=0 C=0 D=0 
00429 [L848] JMP      A=3 B=128 C=16 D=32784 target=446
00430 [L849] GGET     A=3 B=0 C=1 D=1 'd_ms'
00431 [L849] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00432 [L849] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00433 [L849] TGETS    A=3 B=3 C=4 D=772 'maps'
00434 [L849] TGETS    A=4 B=1 C=5 D=261 'map_id'
00435 [L849] ADDVN    A=4 B=4 C=1 D=1025 
00436 [L849] TGETV    A=3 B=3 C=4 D=772 
00437 [L849] TGETS    A=3 B=3 C=20 D=788 'tollgates'
00438 [L849] TGETS    A=4 B=1 C=5 D=261 'map_id'
00439 [L849] ADDVN    A=4 B=4 C=1 D=1025 
00440 [L849] MULVN    A=4 B=4 C=2 D=1026 
00441 [L849] ADDVN    A=4 B=4 C=1 D=1025 
00442 [L849] TGETV    A=3 B=3 C=4 D=772 
00443 [L849] TGETS    A=3 B=3 C=10 D=778 'pass_star'
00444 [L849] ISNEN    A=3 B=0 C=3 D=3 0
00445 [L849] JMP      A=3 B=128 C=44 D=32812 target=490
00446 [L851] GGET     A=3 B=0 C=1 D=1 'd_ms'
00447 [L851] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00448 [L851] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00449 [L851] TGETS    A=3 B=3 C=4 D=772 'maps'
00450 [L851] TGETS    A=4 B=1 C=5 D=261 'map_id'
00451 [L851] ADDVN    A=4 B=4 C=1 D=1025 
00452 [L851] TGETV    A=3 B=3 C=4 D=772 
00453 [L851] TGETS    A=3 B=3 C=20 D=788 'tollgates'
00454 [L851] TGETS    A=4 B=1 C=5 D=261 'map_id'
00455 [L851] ADDVN    A=4 B=4 C=1 D=1025 
00456 [L851] MULVN    A=4 B=4 C=2 D=1026 
00457 [L851] ADDVN    A=4 B=4 C=1 D=1025 
00458 [L851] TGETV    A=3 B=3 C=4 D=772 
00459 [L851] KSHORT   A=4 B=0 C=0 D=0 0
00460 [L851] TSETS    A=4 B=3 C=10 D=778 'pass_star'
00461 [L852] GGET     A=3 B=0 C=1 D=1 'd_ms'
00462 [L852] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00463 [L852] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00464 [L852] TGETS    A=3 B=3 C=4 D=772 'maps'
00465 [L852] TGETS    A=4 B=1 C=5 D=261 'map_id'
00466 [L852] ADDVN    A=4 B=4 C=1 D=1025 
00467 [L852] TGETV    A=3 B=3 C=4 D=772 
00468 [L852] TGETS    A=3 B=3 C=20 D=788 'tollgates'
00469 [L852] TGETS    A=4 B=1 C=5 D=261 'map_id'
00470 [L852] ADDVN    A=4 B=4 C=1 D=1025 
00471 [L852] MULVN    A=4 B=4 C=2 D=1026 
00472 [L852] ADDVN    A=4 B=4 C=1 D=1025 
00473 [L852] TGETV    A=3 B=3 C=4 D=772 
00474 [L852] KSHORT   A=4 B=0 C=0 D=0 0
00475 [L852] TSETS    A=4 B=3 C=14 D=782 'day_count'
00476 [L854] GGET     A=3 B=0 C=1 D=1 'd_ms'
00477 [L854] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00478 [L854] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00479 [L854] TGETS    A=4 B=1 C=5 D=261 'map_id'
00480 [L854] ADDVN    A=4 B=4 C=1 D=1025 
00481 [L854] TSETS    A=4 B=3 C=23 D=791 'lastUnpassMID'
00482 [L855] GGET     A=3 B=0 C=1 D=1 'd_ms'
00483 [L855] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00484 [L855] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00485 [L855] TGETS    A=4 B=1 C=5 D=261 'map_id'
00486 [L855] ADDVN    A=4 B=4 C=1 D=1025 
00487 [L855] MULVN    A=4 B=4 C=2 D=1026 
00488 [L855] ADDVN    A=4 B=4 C=1 D=1025 
00489 [L855] TSETS    A=4 B=3 C=21 D=789 'lastUnpassTID'
00490 [L862] GGET     A=3 B=0 C=1 D=1 'd_ms'
00491 [L862] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00492 [L862] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00493 [L862] TGETS    A=3 B=3 C=4 D=772 'maps'
00494 [L862] TGETS    A=4 B=1 C=5 D=261 'map_id'
00495 [L862] TGETV    A=3 B=3 C=4 D=772 
00496 [L862] TGETS    A=3 B=3 C=20 D=788 'tollgates'
00497 [L862] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00498 [L862] TGETV    A=3 B=3 C=4 D=772 
00499 [L862] GGET     A=4 B=0 C=1 D=1 'd_ms'
00500 [L862] TGETS    A=4 B=4 C=2 D=1026 'd_mapUI'
00501 [L862] TGETS    A=4 B=4 C=3 D=1027 'g_mapUI'
00502 [L862] TGETS    A=4 B=4 C=4 D=1028 'maps'
00503 [L862] TGETS    A=5 B=1 C=5 D=261 'map_id'
00504 [L862] TGETV    A=4 B=4 C=5 D=1029 
00505 [L862] TGETS    A=4 B=4 C=20 D=1044 'tollgates'
00506 [L862] TGETS    A=5 B=1 C=9 D=265 'tollgate_id'
00507 [L862] TGETV    A=4 B=4 C=5 D=1029 
00508 [L862] TGETS    A=4 B=4 C=10 D=1034 'pass_star'
00509 [L862] TSETS    A=4 B=3 C=18 D=786 'last_pass_star'
00510 [L865] GGET     A=3 B=0 C=1 D=1 'd_ms'
00511 [L865] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00512 [L865] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00513 [L865] TGETS    A=3 B=3 C=4 D=772 'maps'
00514 [L865] TGETS    A=4 B=1 C=5 D=261 'map_id'
00515 [L865] TGETV    A=3 B=3 C=4 D=772 
00516 [L865] TGETS    A=3 B=3 C=20 D=788 'tollgates'
00517 [L865] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00518 [L865] TGETV    A=3 B=3 C=4 D=772 
00519 [L865] TGETS    A=3 B=3 C=10 D=778 'pass_star'
00520 [L865] TGETS    A=4 B=1 C=10 D=266 'pass_star'
00521 [L865] ISGE     A=3 B=0 C=4 D=4 
00522 [L865] JMP      A=3 B=128 C=11 D=32779 target=534
00523 [L866] GGET     A=3 B=0 C=1 D=1 'd_ms'
00524 [L866] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00525 [L866] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00526 [L866] TGETS    A=3 B=3 C=4 D=772 'maps'
00527 [L866] TGETS    A=4 B=1 C=5 D=261 'map_id'
00528 [L866] TGETV    A=3 B=3 C=4 D=772 
00529 [L866] TGETS    A=3 B=3 C=20 D=788 'tollgates'
00530 [L866] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00531 [L866] TGETV    A=3 B=3 C=4 D=772 
00532 [L866] TGETS    A=4 B=1 C=10 D=266 'pass_star'
00533 [L866] TSETS    A=4 B=3 C=10 D=778 'pass_star'
00534 [L868] GGET     A=3 B=0 C=1 D=1 'd_ms'
00535 [L868] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00536 [L868] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00537 [L868] TGETS    A=3 B=3 C=4 D=772 'maps'
00538 [L868] TGETS    A=4 B=1 C=5 D=261 'map_id'
00539 [L868] TGETV    A=3 B=3 C=4 D=772 
00540 [L868] TGETS    A=3 B=3 C=20 D=788 'tollgates'
00541 [L868] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00542 [L868] TGETV    A=3 B=3 C=4 D=772 
00543 [L868] TGETS    A=4 B=1 C=14 D=270 'day_count'
00544 [L868] TSETS    A=4 B=3 C=14 D=782 'day_count'
00545 [L871] GGET     A=3 B=0 C=1 D=1 'd_ms'
00546 [L871] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00547 [L871] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00548 [L871] TGETS    A=3 B=3 C=23 D=791 'lastUnpassMID'
00549 [L871] TGETS    A=4 B=1 C=5 D=261 'map_id'
00550 [L871] ISGE     A=3 B=0 C=4 D=4 
00551 [L871] JMP      A=3 B=128 C=5 D=32773 target=557
00552 [L872] GGET     A=3 B=0 C=1 D=1 'd_ms'
00553 [L872] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00554 [L872] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00555 [L872] TGETS    A=4 B=1 C=5 D=261 'map_id'
00556 [L872] TSETS    A=4 B=3 C=23 D=791 'lastUnpassMID'
00557 [L875] GGET     A=3 B=0 C=1 D=1 'd_ms'
00558 [L875] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00559 [L875] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00560 [L875] TGETS    A=3 B=3 C=21 D=789 'lastUnpassTID'
00561 [L875] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00562 [L875] ISGE     A=3 B=0 C=4 D=4 
00563 [L875] JMP      A=3 B=128 C=5 D=32773 target=569
00564 [L876] GGET     A=3 B=0 C=1 D=1 'd_ms'
00565 [L876] TGETS    A=3 B=3 C=2 D=770 'd_mapUI'
00566 [L876] TGETS    A=3 B=3 C=3 D=771 'g_mapUI'
00567 [L876] TGETS    A=4 B=1 C=9 D=265 'tollgate_id'
00568 [L876] TSETS    A=4 B=3 C=21 D=789 'lastUnpassTID'
00569 [L879] TNEW     A=3 B=0 C=0 D=0 
00570 [L880] TGETS    A=4 B=1 C=5 D=261 'map_id'
00571 [L880] TSETS    A=4 B=3 C=24 D=792 'mapID'
00572 [L881] TGETS    A=4 B=1 C=25 D=281 'pass_map'
00573 [L881] TSETS    A=4 B=3 C=25 D=793 'pass_map'
00574 [L882] GGET     A=4 B=0 C=1 D=1 'd_ms'
00575 [L882] TGETS    A=4 B=4 C=26 D=1050 'd_subLevelUI'
00576 [L882] TGETS    A=4 B=4 C=27 D=1051 'g_mapStates'
00577 [L882] TGETS    A=5 B=1 C=5 D=261 'map_id'
00578 [L882] TSETV    A=3 B=4 C=5 D=1029 
00579 [L885] GGET     A=4 B=0 C=1 D=1 'd_ms'
00580 [L885] TGETS    A=4 B=4 C=2 D=1026 'd_mapUI'
00581 [L885] TGETS    A=4 B=4 C=3 D=1027 'g_mapUI'
00582 [L885] TGETS    A=5 B=1 C=9 D=265 'tollgate_id'
00583 [L885] TSETS    A=5 B=4 C=28 D=1052 'last_fight_npc'
00584 [L885] JMP      A=3 B=128 C=9 D=32777 target=594
00585 [L887] UGET     A=3 B=0 C=0 D=0 cclog
00586 [L887] KSTR     A=4 B=0 C=29 D=29 'ERROR: 1019 t_id=%d'
00587 [L887] TGETS    A=5 B=1 C=9 D=265 'tollgate_id'
00588 [L887] CALL     A=3 B=1 C=3 D=259 
00589 [L890] JMP      A=3 B=128 C=4 D=32772 target=594
00590 [L892] UGET     A=3 B=0 C=0 D=0 cclog
00591 [L892] KSTR     A=4 B=0 C=30 D=30 'ERROR: 1019 mapid=%d'
00592 [L892] TGETS    A=5 B=1 C=5 D=261 'map_id'
00593 [L892] CALL     A=3 B=1 C=3 D=259 
00594 [L895] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto33 offset=0x4917 source_lines=899-976 params=3
UPVALUES ['cclog']
00001 [L900] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L900] KSTR     A=4 B=0 C=0 D=0 'call msg_update_tollgate_list_1020'
00003 [L900] CALL     A=3 B=1 C=2 D=258 
00004 [L904] GGET     A=3 B=0 C=1 D=1 'd_ms'
00005 [L904] TGETS    A=3 B=3 C=2 D=770 'd_alert'
00006 [L904] TGETS    A=3 B=3 C=3 D=771 'stop_wait'
00007 [L904] CALL     A=3 B=1 C=1 D=257 
00008 [L907] TGETS    A=3 B=1 C=4 D=260 'first_send'
00009 [L907] ISNEP    A=3 B=0 C=2 D=2 
00010 [L907] JMP      A=3 B=128 C=4 D=32772 target=15
00011 [L909] GGET     A=3 B=0 C=1 D=1 'd_ms'
00012 [L909] TGETS    A=3 B=3 C=5 D=773 'd_mapUI'
00013 [L909] TGETS    A=3 B=3 C=6 D=774 'initMapCsv'
00014 [L909] CALL     A=3 B=1 C=1 D=257 
00015 [L913] KSHORT   A=3 B=0 C=1 D=1 1
00016 [L913] TGETS    A=4 B=1 C=7 D=263 'tollgate_count'
00017 [L913] KSHORT   A=5 B=0 C=1 D=1 1
00018 [L913] FORI     A=3 B=128 C=164 D=32932 target=183
00019 [L915] TGETS    A=7 B=1 C=8 D=264 'tollgate_list'
00020 [L915] TGETV    A=7 B=7 C=6 D=1798 
00021 [L915] TGETS    A=7 B=7 C=9 D=1801 'map_id'
00022 [L916] TGETS    A=8 B=1 C=8 D=264 'tollgate_list'
00023 [L916] TGETV    A=8 B=8 C=6 D=2054 
00024 [L916] TGETS    A=8 B=8 C=10 D=2058 'tollgate_id'
00025 [L917] GGET     A=9 B=0 C=1 D=1 'd_ms'
00026 [L917] TGETS    A=9 B=9 C=5 D=2309 'd_mapUI'
00027 [L917] TGETS    A=9 B=9 C=11 D=2315 'g_mapUI'
00028 [L917] TGETS    A=9 B=9 C=12 D=2316 'maps'
00029 [L917] TGETV    A=9 B=9 C=7 D=2311 
00030 [L917] IST      A=0 B=0 C=9 D=9 
00031 [L917] JMP      A=9 B=128 C=5 D=32773 target=37
00032 [L918] UGET     A=9 B=0 C=0 D=0 cclog
00033 [L918] KSTR     A=10 B=0 C=13 D=13 'ERROR: 1020 get invalid mapid=%d'
00034 [L918] MOV      A=11 B=0 C=7 D=7 
00035 [L918] CALL     A=9 B=1 C=3 D=259 
00036 [L918] JMP      A=9 B=128 C=145 D=32913 target=182
00037 [L921] TGETS    A=9 B=1 C=8 D=264 'tollgate_list'
00038 [L921] TGETV    A=9 B=9 C=6 D=2310 
00039 [L921] TGETS    A=9 B=9 C=14 D=2318 'tollgate_type'
00040 [L921] ISNEN    A=9 B=0 C=0 D=0 2
00041 [L921] JMP      A=9 B=128 C=72 D=32840 target=114
00042 [L923] UGET     A=9 B=0 C=0 D=0 cclog
00043 [L923] KSTR     A=10 B=0 C=15 D=15 'elite_tollgate'
00044 [L923] CALL     A=9 B=1 C=2 D=258 
00045 [L925] GGET     A=9 B=0 C=1 D=1 'd_ms'
00046 [L925] TGETS    A=9 B=9 C=5 D=2309 'd_mapUI'
00047 [L925] TGETS    A=9 B=9 C=11 D=2315 'g_mapUI'
00048 [L925] TGETS    A=9 B=9 C=16 D=2320 'lastUnpassMID_elite'
00049 [L925] ISGE     A=9 B=0 C=7 D=7 
00050 [L925] JMP      A=9 B=128 C=4 D=32772 target=55
00051 [L926] GGET     A=9 B=0 C=1 D=1 'd_ms'
00052 [L926] TGETS    A=9 B=9 C=5 D=2309 'd_mapUI'
00053 [L926] TGETS    A=9 B=9 C=11 D=2315 'g_mapUI'
00054 [L926] TSETS    A=7 B=9 C=16 D=2320 'lastUnpassMID_elite'
00055 [L933] GGET     A=9 B=0 C=1 D=1 'd_ms'
00056 [L933] TGETS    A=9 B=9 C=5 D=2309 'd_mapUI'
00057 [L933] TGETS    A=9 B=9 C=11 D=2315 'g_mapUI'
00058 [L933] TGETS    A=9 B=9 C=17 D=2321 'lastUnpassTID_elite'
00059 [L933] ISGE     A=9 B=0 C=8 D=8 
00060 [L933] JMP      A=9 B=128 C=4 D=32772 target=65
00061 [L934] GGET     A=9 B=0 C=1 D=1 'd_ms'
00062 [L934] TGETS    A=9 B=9 C=5 D=2309 'd_mapUI'
00063 [L934] TGETS    A=9 B=9 C=11 D=2315 'g_mapUI'
00064 [L934] TSETS    A=8 B=9 C=17 D=2321 'lastUnpassTID_elite'
00065 [L938] GGET     A=9 B=0 C=1 D=1 'd_ms'
00066 [L938] TGETS    A=9 B=9 C=5 D=2309 'd_mapUI'
00067 [L938] TGETS    A=9 B=9 C=11 D=2315 'g_mapUI'
00068 [L938] TGETS    A=9 B=9 C=12 D=2316 'maps'
00069 [L938] TGETV    A=9 B=9 C=7 D=2311 
00070 [L938] TGETS    A=9 B=9 C=18 D=2322 'tollgates_elite'
00071 [L938] TGETV    A=9 B=9 C=8 D=2312 
00072 [L938] IST      A=0 B=0 C=9 D=9 
00073 [L938] JMP      A=9 B=128 C=6 D=32774 target=80
00074 [L939] UGET     A=9 B=0 C=0 D=0 cclog
00075 [L939] KSTR     A=10 B=0 C=19 D=19 'ERROR:elite 1020 get invalid mapid=%d, tollgate_id=%d'
00076 [L939] MOV      A=11 B=0 C=7 D=7 
00077 [L939] MOV      A=12 B=0 C=8 D=8 
00078 [L939] CALL     A=9 B=1 C=4 D=260 
00079 [L939] JMP      A=9 B=128 C=102 D=32870 target=182
00080 [L942] GGET     A=9 B=0 C=1 D=1 'd_ms'
00081 [L942] TGETS    A=9 B=9 C=5 D=2309 'd_mapUI'
00082 [L942] TGETS    A=9 B=9 C=11 D=2315 'g_mapUI'
00083 [L942] TGETS    A=9 B=9 C=12 D=2316 'maps'
00084 [L942] TGETV    A=9 B=9 C=7 D=2311 
00085 [L942] TGETS    A=9 B=9 C=18 D=2322 'tollgates_elite'
00086 [L942] TGETV    A=9 B=9 C=8 D=2312 
00087 [L942] TGETS    A=10 B=1 C=8 D=264 'tollgate_list'
00088 [L942] TGETV    A=10 B=10 C=6 D=2566 
00089 [L942] TGETS    A=10 B=10 C=20 D=2580 'day_count'
00090 [L942] TSETS    A=10 B=9 C=20 D=2324 'day_count'
00091 [L943] GGET     A=9 B=0 C=1 D=1 'd_ms'
00092 [L943] TGETS    A=9 B=9 C=5 D=2309 'd_mapUI'
00093 [L943] TGETS    A=9 B=9 C=11 D=2315 'g_mapUI'
00094 [L943] TGETS    A=9 B=9 C=12 D=2316 'maps'
00095 [L943] TGETV    A=9 B=9 C=7 D=2311 
00096 [L943] TGETS    A=9 B=9 C=18 D=2322 'tollgates_elite'
00097 [L943] TGETV    A=9 B=9 C=8 D=2312 
00098 [L943] TGETS    A=10 B=1 C=8 D=264 'tollgate_list'
00099 [L943] TGETV    A=10 B=10 C=6 D=2566 
00100 [L943] TGETS    A=10 B=10 C=21 D=2581 'pass_star'
00101 [L943] TSETS    A=10 B=9 C=21 D=2325 'pass_star'
00102 [L944] GGET     A=9 B=0 C=1 D=1 'd_ms'
00103 [L944] TGETS    A=9 B=9 C=5 D=2309 'd_mapUI'
00104 [L944] TGETS    A=9 B=9 C=11 D=2315 'g_mapUI'
00105 [L944] TGETS    A=9 B=9 C=12 D=2316 'maps'
00106 [L944] TGETV    A=9 B=9 C=7 D=2311 
00107 [L944] TGETS    A=9 B=9 C=18 D=2322 'tollgates_elite'
00108 [L944] TGETV    A=9 B=9 C=8 D=2312 
00109 [L944] TGETS    A=10 B=1 C=8 D=264 'tollgate_list'
00110 [L944] TGETV    A=10 B=10 C=6 D=2566 
00111 [L944] TGETS    A=10 B=10 C=22 D=2582 'flush_count'
00112 [L944] TSETS    A=10 B=9 C=22 D=2326 'flush_count'
00113 [L945] JMP      A=9 B=128 C=68 D=32836 target=182
00114 [L949] GGET     A=9 B=0 C=1 D=1 'd_ms'
00115 [L949] TGETS    A=9 B=9 C=5 D=2309 'd_mapUI'
00116 [L949] TGETS    A=9 B=9 C=11 D=2315 'g_mapUI'
00117 [L949] TGETS    A=9 B=9 C=23 D=2327 'lastUnpassMID'
00118 [L949] ISGE     A=9 B=0 C=7 D=7 
00119 [L949] JMP      A=9 B=128 C=4 D=32772 target=124
00120 [L950] GGET     A=9 B=0 C=1 D=1 'd_ms'
00121 [L950] TGETS    A=9 B=9 C=5 D=2309 'd_mapUI'
00122 [L950] TGETS    A=9 B=9 C=11 D=2315 'g_mapUI'
00123 [L950] TSETS    A=7 B=9 C=23 D=2327 'lastUnpassMID'
00124 [L957] GGET     A=9 B=0 C=1 D=1 'd_ms'
00125 [L957] TGETS    A=9 B=9 C=5 D=2309 'd_mapUI'
00126 [L957] TGETS    A=9 B=9 C=11 D=2315 'g_mapUI'
00127 [L957] TGETS    A=9 B=9 C=24 D=2328 'lastUnpassTID'
00128 [L957] ISGE     A=9 B=0 C=8 D=8 
00129 [L957] JMP      A=9 B=128 C=4 D=32772 target=134
00130 [L958] GGET     A=9 B=0 C=1 D=1 'd_ms'
00131 [L958] TGETS    A=9 B=9 C=5 D=2309 'd_mapUI'
00132 [L958] TGETS    A=9 B=9 C=11 D=2315 'g_mapUI'
00133 [L958] TSETS    A=8 B=9 C=24 D=2328 'lastUnpassTID'
00134 [L963] GGET     A=9 B=0 C=1 D=1 'd_ms'
00135 [L963] TGETS    A=9 B=9 C=5 D=2309 'd_mapUI'
00136 [L963] TGETS    A=9 B=9 C=11 D=2315 'g_mapUI'
00137 [L963] TGETS    A=9 B=9 C=12 D=2316 'maps'
00138 [L963] TGETV    A=9 B=9 C=7 D=2311 
00139 [L963] TGETS    A=9 B=9 C=25 D=2329 'tollgates'
00140 [L963] TGETV    A=9 B=9 C=8 D=2312 
00141 [L963] IST      A=0 B=0 C=9 D=9 
00142 [L963] JMP      A=9 B=128 C=6 D=32774 target=149
00143 [L964] UGET     A=9 B=0 C=0 D=0 cclog
00144 [L964] KSTR     A=10 B=0 C=26 D=26 'ERROR: 1020 get invalid mapid=%d, tollgate_id=%d'
00145 [L964] MOV      A=11 B=0 C=7 D=7 
00146 [L964] MOV      A=12 B=0 C=8 D=8 
00147 [L964] CALL     A=9 B=1 C=4 D=260 
00148 [L964] JMP      A=9 B=128 C=33 D=32801 target=182
00149 [L967] GGET     A=9 B=0 C=1 D=1 'd_ms'
00150 [L967] TGETS    A=9 B=9 C=5 D=2309 'd_mapUI'
00151 [L967] TGETS    A=9 B=9 C=11 D=2315 'g_mapUI'
00152 [L967] TGETS    A=9 B=9 C=12 D=2316 'maps'
00153 [L967] TGETV    A=9 B=9 C=7 D=2311 
00154 [L967] TGETS    A=9 B=9 C=25 D=2329 'tollgates'
00155 [L967] TGETV    A=9 B=9 C=8 D=2312 
00156 [L967] TGETS    A=10 B=1 C=8 D=264 'tollgate_list'
00157 [L967] TGETV    A=10 B=10 C=6 D=2566 
00158 [L967] TGETS    A=10 B=10 C=20 D=2580 'day_count'
00159 [L967] TSETS    A=10 B=9 C=20 D=2324 'day_count'
00160 [L968] GGET     A=9 B=0 C=1 D=1 'd_ms'
00161 [L968] TGETS    A=9 B=9 C=5 D=2309 'd_mapUI'
00162 [L968] TGETS    A=9 B=9 C=11 D=2315 'g_mapUI'
00163 [L968] TGETS    A=9 B=9 C=12 D=2316 'maps'
00164 [L968] TGETV    A=9 B=9 C=7 D=2311 
00165 [L968] TGETS    A=9 B=9 C=25 D=2329 'tollgates'
00166 [L968] TGETV    A=9 B=9 C=8 D=2312 
00167 [L968] TGETS    A=10 B=1 C=8 D=264 'tollgate_list'
00168 [L968] TGETV    A=10 B=10 C=6 D=2566 
00169 [L968] TGETS    A=10 B=10 C=21 D=2581 'pass_star'
00170 [L968] TSETS    A=10 B=9 C=21 D=2325 'pass_star'
00171 [L969] GGET     A=9 B=0 C=1 D=1 'd_ms'
00172 [L969] TGETS    A=9 B=9 C=5 D=2309 'd_mapUI'
00173 [L969] TGETS    A=9 B=9 C=11 D=2315 'g_mapUI'
00174 [L969] TGETS    A=9 B=9 C=12 D=2316 'maps'
00175 [L969] TGETV    A=9 B=9 C=7 D=2311 
00176 [L969] TGETS    A=9 B=9 C=25 D=2329 'tollgates'
00177 [L969] TGETV    A=9 B=9 C=8 D=2312 
00178 [L969] TGETS    A=10 B=1 C=8 D=264 'tollgate_list'
00179 [L969] TGETV    A=10 B=10 C=6 D=2566 
00180 [L969] TGETS    A=10 B=10 C=22 D=2582 'flush_count'
00181 [L969] TSETS    A=10 B=9 C=22 D=2326 'flush_count'
00182 [L913] FORL     A=3 B=127 C=92 D=32604 target=19
00183 [L976] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto34 offset=0x4ec0 source_lines=1059-1062 params=0
UPVALUES []
00001 [L1060] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L1060] TGETS    A=0 B=0 C=1 D=1 'd_info'
00003 [L1060] TGETS    A=0 B=0 C=2 D=2 'show'
00004 [L1060] GGET     A=1 B=0 C=0 D=0 'd_ms'
00005 [L1060] TGETS    A=1 B=1 C=3 D=259 'd_hz'
00006 [L1060] TGETS    A=1 B=1 C=4 D=260 'gethz'
00007 [L1060] KSTR     A=2 B=0 C=5 D=5 'leave_game_5_min'
00008 [L1060] CALL     A=1 B=0 C=2 D=2 
00009 [L1060] CALLM    A=0 B=1 C=0 D=256 
00010 [L1061] GGET     A=0 B=0 C=6 D=6 'jumpLoginUI'
00011 [L1061] CALL     A=0 B=1 C=1 D=257 
00012 [L1062] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto35 offset=0x4f43 source_lines=984-1087 params=3
UPVALUES ['cclog', 'CCTextureCache', 'os', 'main_server', 'CCDirector']
00001 [L985] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L985] KSTR     A=4 B=0 C=0 D=0 'lua call event_client_info_20, ----[%d]'
00003 [L985] TGETS    A=5 B=1 C=1 D=257 'type'
00004 [L985] CALL     A=3 B=1 C=3 D=259 
00005 [L986] TGETS    A=3 B=1 C=1 D=257 'type'
00006 [L986] ISNEN    A=3 B=0 C=0 D=0 100
00007 [L986] JMP      A=3 B=128 C=1 D=32769 target=9
00008 [L986] JMP      A=3 B=128 C=232 D=33000 target=241
00009 [L988] TGETS    A=3 B=1 C=1 D=257 'type'
00010 [L988] ISNEN    A=3 B=0 C=1 D=1 101
00011 [L988] JMP      A=3 B=128 C=1 D=32769 target=13
00012 [L988] JMP      A=3 B=128 C=228 D=32996 target=241
00013 [L990] TGETS    A=3 B=1 C=1 D=257 'type'
00014 [L990] ISNEN    A=3 B=0 C=2 D=2 102
00015 [L990] JMP      A=3 B=128 C=1 D=32769 target=17
00016 [L990] JMP      A=3 B=128 C=224 D=32992 target=241
00017 [L992] TGETS    A=3 B=1 C=1 D=257 'type'
00018 [L992] ISNEN    A=3 B=0 C=3 D=3 201
00019 [L992] JMP      A=3 B=128 C=51 D=32819 target=71
00020 [L993] GGET     A=3 B=0 C=2 D=2 'd_ms'
00021 [L993] TGETS    A=3 B=3 C=3 D=771 'd_u'
00022 [L993] TGETS    A=3 B=3 C=4 D=772 'isWP8'
00023 [L993] CALL     A=3 B=2 C=1 D=513 
00024 [L993] ISF      A=0 B=0 C=3 D=3 
00025 [L993] JMP      A=4 B=128 C=5 D=32773 target=31
00026 [L994] GGET     A=3 B=0 C=2 D=2 'd_ms'
00027 [L994] TGETS    A=3 B=3 C=3 D=771 'd_u'
00028 [L994] TGETS    A=3 B=3 C=5 D=773 'removeAllCache'
00029 [L994] CALL     A=3 B=1 C=1 D=257 
00030 [L994] JMP      A=3 B=128 C=7 D=32775 target=38
00031 [L996] UGET     A=3 B=0 C=1 D=1 CCTextureCache
00032 [L996] MOV      A=4 B=0 C=3 D=3 
00033 [L996] TGETS    A=3 B=3 C=6 D=774 'sharedTextureCache'
00034 [L996] CALL     A=3 B=2 C=2 D=514 
00035 [L996] MOV      A=4 B=0 C=3 D=3 
00036 [L996] TGETS    A=3 B=3 C=7 D=775 'removeUnusedTextures'
00037 [L996] CALL     A=3 B=1 C=2 D=258 
00038 [L1000] GGET     A=3 B=0 C=2 D=2 'd_ms'
00039 [L1000] TGETS    A=3 B=3 C=8 D=776 'd_stat'
00040 [L1000] TGETS    A=3 B=3 C=9 D=777 'cleanCrashFlag'
00041 [L1000] CALL     A=3 B=1 C=1 D=257 
00042 [L1001] GGET     A=3 B=0 C=10 D=10 'g_self'
00043 [L1001] UGET     A=4 B=0 C=2 D=2 os
00044 [L1001] TGETS    A=4 B=4 C=12 D=1036 'time'
00045 [L1001] CALL     A=4 B=2 C=1 D=513 
00046 [L1001] TSETS    A=4 B=3 C=11 D=779 'enter_back_time'
00047 [L1002] GGET     A=3 B=0 C=2 D=2 'd_ms'
00048 [L1002] TGETS    A=3 B=3 C=3 D=771 'd_u'
00049 [L1002] TGETS    A=3 B=3 C=13 D=781 'reload_pic'
00050 [L1002] CALL     A=3 B=1 C=1 D=257 
00051 [L1005] GGET     A=3 B=0 C=2 D=2 'd_ms'
00052 [L1005] TGETS    A=3 B=3 C=14 D=782 'd_guideUI'
00053 [L1005] TGETS    A=3 B=3 C=15 D=783 'g_isPlayingMoving'
00054 [L1005] ISF      A=0 B=0 C=3 D=3 
00055 [L1005] JMP      A=4 B=128 C=8 D=32776 target=64
00056 [L1005] UGET     A=3 B=0 C=3 D=3 main_server
00057 [L1005] TGETS    A=3 B=3 C=16 D=784 'isMoivePlaying'
00058 [L1005] CALL     A=3 B=2 C=1 D=513 
00059 [L1005] ISNEN    A=3 B=0 C=4 D=4 1
00060 [L1005] JMP      A=3 B=128 C=3 D=32771 target=64
00061 [L1006] UGET     A=3 B=0 C=3 D=3 main_server
00062 [L1006] TGETS    A=3 B=3 C=17 D=785 'pauseMoive'
00063 [L1006] CALL     A=3 B=1 C=1 D=257 
00064 [L1009] GGET     A=3 B=0 C=10 D=10 'g_self'
00065 [L1009] KPRI     A=4 B=0 C=2 D=2 
00066 [L1009] TSETS    A=4 B=3 C=18 D=786 'hadEnterBack'
00067 [L1010] UGET     A=3 B=0 C=0 D=0 cclog
00068 [L1010] KSTR     A=4 B=0 C=19 D=19 'APP EVENT_DID_ENTER_BACK'
00069 [L1010] CALL     A=3 B=1 C=2 D=258 
00070 [L1010] JMP      A=3 B=128 C=170 D=32938 target=241
00071 [L1013] TGETS    A=3 B=1 C=1 D=257 'type'
00072 [L1013] ISNEN    A=3 B=0 C=5 D=5 202
00073 [L1013] JMP      A=3 B=128 C=116 D=32884 target=190
00074 [L1015] UGET     A=3 B=0 C=0 D=0 cclog
00075 [L1015] KSTR     A=4 B=0 C=20 D=20 'APP EVENT_WILL_ENTER_FORE'
00076 [L1015] CALL     A=3 B=1 C=2 D=258 
00077 [L1016] UGET     A=3 B=0 C=4 D=4 CCDirector
00078 [L1016] MOV      A=4 B=0 C=3 D=3 
00079 [L1016] TGETS    A=3 B=3 C=21 D=789 'sharedDirector'
00080 [L1016] CALL     A=3 B=2 C=2 D=514 
00081 [L1016] MOV      A=4 B=0 C=3 D=3 
00082 [L1016] TGETS    A=3 B=3 C=22 D=790 'resume'
00083 [L1016] CALL     A=3 B=1 C=2 D=258 
00084 [L1017] GGET     A=3 B=0 C=2 D=2 'd_ms'
00085 [L1017] TGETS    A=3 B=3 C=3 D=771 'd_u'
00086 [L1017] TGETS    A=3 B=3 C=23 D=791 'reload_pic_clean'
00087 [L1017] CALL     A=3 B=1 C=1 D=257 
00088 [L1020] GGET     A=3 B=0 C=2 D=2 'd_ms'
00089 [L1020] TGETS    A=3 B=3 C=24 D=792 'd_setting'
00090 [L1020] TGETS    A=3 B=3 C=25 D=793 'g_setting'
00091 [L1020] TGETS    A=3 B=3 C=26 D=794 'openMusic'
00092 [L1020] ISNEN    A=3 B=0 C=4 D=4 1
00093 [L1020] JMP      A=3 B=128 C=1 D=32769 target=95
00094 [L1020] JMP      A=3 B=128 C=4 D=32772 target=99
00095 [L1024] GGET     A=3 B=0 C=2 D=2 'd_ms'
00096 [L1024] TGETS    A=3 B=3 C=27 D=795 'd_music_mgr'
00097 [L1024] TGETS    A=3 B=3 C=28 D=796 'stop_bkg'
00098 [L1024] CALL     A=3 B=1 C=1 D=257 
00099 [L1028] GGET     A=3 B=0 C=2 D=2 'd_ms'
00100 [L1028] TGETS    A=3 B=3 C=29 D=797 'd_loginUI'
00101 [L1028] TGETS    A=3 B=3 C=30 D=798 'checkTPSdkEvent'
00102 [L1028] CALL     A=3 B=1 C=1 D=257 
00103 [L1030] GGET     A=3 B=0 C=10 D=10 'g_self'
00104 [L1030] TGETS    A=3 B=3 C=18 D=786 'hadEnterBack'
00105 [L1030] ISF      A=0 B=0 C=3 D=3 
00106 [L1030] JMP      A=4 B=128 C=8 D=32776 target=115
00107 [L1031] GGET     A=3 B=0 C=2 D=2 'd_ms'
00108 [L1031] TGETS    A=3 B=3 C=31 D=799 'd_mainUI'
00109 [L1031] TGETS    A=3 B=3 C=32 D=800 'unScheduleCountTime'
00110 [L1031] CALL     A=3 B=1 C=1 D=257 
00111 [L1032] GGET     A=3 B=0 C=2 D=2 'd_ms'
00112 [L1032] TGETS    A=3 B=3 C=31 D=799 'd_mainUI'
00113 [L1032] TGETS    A=3 B=3 C=33 D=801 'scheduleCountTime'
00114 [L1032] CALL     A=3 B=1 C=1 D=257 
00115 [L1037] GGET     A=3 B=0 C=2 D=2 'd_ms'
00116 [L1037] TGETS    A=3 B=3 C=14 D=782 'd_guideUI'
00117 [L1037] TGETS    A=3 B=3 C=15 D=783 'g_isPlayingMoving'
00118 [L1037] ISF      A=0 B=0 C=3 D=3 
00119 [L1037] JMP      A=4 B=128 C=12 D=32780 target=132
00120 [L1037] UGET     A=3 B=0 C=3 D=3 main_server
00121 [L1037] TGETS    A=3 B=3 C=16 D=784 'isMoivePlaying'
00122 [L1037] CALL     A=3 B=2 C=1 D=513 
00123 [L1037] ISNEN    A=3 B=0 C=4 D=4 1
00124 [L1037] JMP      A=3 B=128 C=7 D=32775 target=132
00125 [L1038] GGET     A=3 B=0 C=2 D=2 'd_ms'
00126 [L1038] TGETS    A=3 B=3 C=27 D=795 'd_music_mgr'
00127 [L1038] TGETS    A=3 B=3 C=28 D=796 'stop_bkg'
00128 [L1038] CALL     A=3 B=1 C=1 D=257 
00129 [L1039] UGET     A=3 B=0 C=3 D=3 main_server
00130 [L1039] TGETS    A=3 B=3 C=34 D=802 'resumeMoive'
00131 [L1039] CALL     A=3 B=1 C=1 D=257 
00132 [L1043] GGET     A=3 B=0 C=2 D=2 'd_ms'
00133 [L1043] TGETS    A=3 B=3 C=3 D=771 'd_u'
00134 [L1043] TGETS    A=3 B=3 C=35 D=803 'isADR'
00135 [L1043] CALL     A=3 B=2 C=1 D=513 
00136 [L1043] ISF      A=0 B=0 C=3 D=3 
00137 [L1043] JMP      A=4 B=128 C=20 D=32788 target=158
00138 [L1044] GGET     A=3 B=0 C=2 D=2 'd_ms'
00139 [L1044] TGETS    A=3 B=3 C=14 D=782 'd_guideUI'
00140 [L1044] TGETS    A=3 B=3 C=15 D=783 'g_isPlayingMoving'
00141 [L1044] ISF      A=0 B=0 C=3 D=3 
00142 [L1044] JMP      A=4 B=128 C=15 D=32783 target=158
00143 [L1044] UGET     A=3 B=0 C=3 D=3 main_server
00144 [L1044] TGETS    A=3 B=3 C=16 D=784 'isMoivePlaying'
00145 [L1044] CALL     A=3 B=2 C=1 D=513 
00146 [L1044] ISNEN    A=3 B=0 C=6 D=6 0
00147 [L1044] JMP      A=3 B=128 C=10 D=32778 target=158
00148 [L1045] UGET     A=3 B=0 C=3 D=3 main_server
00149 [L1045] TGETS    A=3 B=3 C=36 D=804 'startPlayMoive'
00150 [L1045] KSTR     A=4 B=0 C=37 D=37 'none'
00151 [L1045] CALL     A=3 B=1 C=2 D=258 
00152 [L1047] GGET     A=3 B=0 C=2 D=2 'd_ms'
00153 [L1047] TGETS    A=3 B=3 C=27 D=795 'd_music_mgr'
00154 [L1047] TGETS    A=3 B=3 C=28 D=796 'stop_bkg'
00155 [L1047] CALL     A=3 B=1 C=1 D=257 
00156 [L1048] KPRI     A=3 B=0 C=2 D=2 
00157 [L1048] GSET     A=3 B=0 C=15 D=15 'g_isPlayingMoving'
00158 [L1053] GGET     A=3 B=0 C=10 D=10 'g_self'
00159 [L1053] TGETS    A=3 B=3 C=11 D=779 'enter_back_time'
00160 [L1053] ISF      A=0 B=0 C=3 D=3 
00161 [L1053] JMP      A=4 B=128 C=23 D=32791 target=185
00162 [L1054] UGET     A=3 B=0 C=2 D=2 os
00163 [L1054] TGETS    A=3 B=3 C=12 D=780 'time'
00164 [L1054] CALL     A=3 B=2 C=1 D=513 
00165 [L1054] GGET     A=4 B=0 C=10 D=10 'g_self'
00166 [L1054] TGETS    A=4 B=4 C=11 D=1035 'enter_back_time'
00167 [L1054] SUBVV    A=3 B=3 C=4 D=772 
00168 [L1055] UGET     A=4 B=0 C=0 D=0 cclog
00169 [L1055] KSTR     A=5 B=0 C=38 D=38 'enter background time='
00170 [L1055] MOV      A=6 B=0 C=3 D=3 
00171 [L1055] CAT      A=5 B=5 C=6 D=1286 
00172 [L1055] CALL     A=4 B=1 C=2 D=258 
00173 [L1057] KSHORT   A=4 B=1 C=44 D=300 300
00174 [L1057] ISGE     A=4 B=0 C=3 D=3 
00175 [L1057] JMP      A=4 B=128 C=9 D=32777 target=185
00176 [L1062] FNEW     A=4 B=0 C=39 D=39 {'kind': 'proto', 'id': 34}
00177 [L1063] GGET     A=5 B=0 C=2 D=2 'd_ms'
00178 [L1063] TGETS    A=5 B=5 C=3 D=1283 'd_u'
00179 [L1063] TGETS    A=5 B=5 C=40 D=1320 'delay_node'
00180 [L1063] KSHORT   A=6 B=0 C=0 D=0 0
00181 [L1063] MOV      A=7 B=0 C=4 D=4 
00182 [L1063] CALL     A=5 B=1 C=3 D=259 
00183 [L1064] UCLO     A=0 B=128 C=0 D=32768 target=184
00184 [L1064] RET0     A=0 B=0 C=1 D=1 
00185 [L1068] GGET     A=3 B=0 C=2 D=2 'd_ms'
00186 [L1068] TGETS    A=3 B=3 C=8 D=776 'd_stat'
00187 [L1068] TGETS    A=3 B=3 C=41 D=809 'setCrashFlag'
00188 [L1068] CALL     A=3 B=1 C=1 D=257 
00189 [L1068] JMP      A=3 B=128 C=51 D=32819 target=241
00190 [L1072] TGETS    A=3 B=1 C=1 D=257 'type'
00191 [L1072] ISNEN    A=3 B=0 C=7 D=7 404
00192 [L1072] JMP      A=3 B=128 C=7 D=32775 target=200
00193 [L1073] GGET     A=3 B=0 C=42 D=42 'send_quit_game_1014'
00194 [L1073] CALL     A=3 B=1 C=1 D=257 
00195 [L1074] GGET     A=3 B=0 C=2 D=2 'd_ms'
00196 [L1074] TGETS    A=3 B=3 C=43 D=811 'd_alert'
00197 [L1074] TGETS    A=3 B=3 C=44 D=812 'stop_wait'
00198 [L1074] CALL     A=3 B=1 C=1 D=257 
00199 [L1074] JMP      A=3 B=128 C=41 D=32809 target=241
00200 [L1075] TGETS    A=3 B=1 C=1 D=257 'type'
00201 [L1075] ISNEN    A=3 B=0 C=8 D=8 105
00202 [L1075] JMP      A=3 B=128 C=4 D=32772 target=207
00203 [L1077] UGET     A=3 B=0 C=0 D=0 cclog
00204 [L1077] KSTR     A=4 B=0 C=45 D=45 'ERROR: cmd transfer to updateUI.'
00205 [L1077] CALL     A=3 B=1 C=2 D=258 
00206 [L1077] JMP      A=3 B=128 C=34 D=32802 target=241
00207 [L1078] TGETS    A=3 B=1 C=1 D=257 'type'
00208 [L1078] ISNEN    A=3 B=0 C=9 D=9 501
00209 [L1078] JMP      A=3 B=128 C=8 D=32776 target=218
00210 [L1079] UGET     A=3 B=0 C=0 D=0 cclog
00211 [L1079] KSTR     A=4 B=0 C=46 D=46 'user cancel moive'
00212 [L1079] CALL     A=3 B=1 C=2 D=258 
00213 [L1080] GGET     A=3 B=0 C=2 D=2 'd_ms'
00214 [L1080] TGETS    A=3 B=3 C=14 D=782 'd_guideUI'
00215 [L1080] TGETS    A=3 B=3 C=47 D=815 'moiveFinished'
00216 [L1080] CALL     A=3 B=1 C=1 D=257 
00217 [L1080] JMP      A=3 B=128 C=23 D=32791 target=241
00218 [L1081] TGETS    A=3 B=1 C=1 D=257 'type'
00219 [L1081] ISNEN    A=3 B=0 C=10 D=10 502
00220 [L1081] JMP      A=3 B=128 C=8 D=32776 target=229
00221 [L1082] UGET     A=3 B=0 C=0 D=0 cclog
00222 [L1082] KSTR     A=4 B=0 C=48 D=48 'moive finished'
00223 [L1082] CALL     A=3 B=1 C=2 D=258 
00224 [L1083] GGET     A=3 B=0 C=2 D=2 'd_ms'
00225 [L1083] TGETS    A=3 B=3 C=14 D=782 'd_guideUI'
00226 [L1083] TGETS    A=3 B=3 C=47 D=815 'moiveFinished'
00227 [L1083] CALL     A=3 B=1 C=1 D=257 
00228 [L1083] JMP      A=3 B=128 C=12 D=32780 target=241
00229 [L1085] GGET     A=3 B=0 C=2 D=2 'd_ms'
00230 [L1085] TGETS    A=3 B=3 C=49 D=817 'd_info'
00231 [L1085] TGETS    A=3 B=3 C=50 D=818 'show'
00232 [L1085] GGET     A=4 B=0 C=2 D=2 'd_ms'
00233 [L1085] TGETS    A=4 B=4 C=51 D=1075 'd_hz'
00234 [L1085] TGETS    A=4 B=4 C=52 D=1076 'gethz'
00235 [L1085] KSTR     A=5 B=0 C=53 D=53 'unkown_event_client_info'
00236 [L1085] CALL     A=4 B=2 C=2 D=514 
00237 [L1085] KSTR     A=5 B=0 C=54 D=54 ', code='
00238 [L1085] TGETS    A=6 B=1 C=1 D=257 'type'
00239 [L1085] CAT      A=4 B=4 C=6 D=1030 
00240 [L1085] CALL     A=3 B=1 C=2 D=258 
00241 [L1087] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto36 offset=0x575f source_lines=1092-1128 params=3
UPVALUES ['cclog', 'require']
00001 [L1094] ISF      A=0 B=0 C=0 D=0 
00002 [L1094] JMP      A=3 B=128 C=15 D=32783 target=18
00003 [L1094] TGETS    A=3 B=1 C=0 D=256 'type'
00004 [L1094] ISF      A=0 B=0 C=3 D=3 
00005 [L1094] JMP      A=4 B=128 C=12 D=32780 target=18
00006 [L1094] TGETS    A=3 B=1 C=1 D=257 'filename'
00007 [L1094] ISF      A=0 B=0 C=3 D=3 
00008 [L1094] JMP      A=4 B=128 C=9 D=32777 target=18
00009 [L1095] UGET     A=3 B=0 C=0 D=0 cclog
00010 [L1095] KSTR     A=4 B=0 C=2 D=2 'event_client_update_info_21: msg_id='
00011 [L1095] MOV      A=5 B=0 C=0 D=0 
00012 [L1095] KSTR     A=6 B=0 C=3 D=3 ', type='
00013 [L1095] TGETS    A=7 B=1 C=0 D=256 'type'
00014 [L1095] KSTR     A=8 B=0 C=4 D=4 ', filename='
00015 [L1095] TGETS    A=9 B=1 C=1 D=257 'filename'
00016 [L1095] CAT      A=4 B=4 C=9 D=1033 
00017 [L1095] CALL     A=3 B=1 C=2 D=258 
00018 [L1099] TGETS    A=3 B=1 C=0 D=256 'type'
00019 [L1099] ISNEN    A=3 B=0 C=0 D=0 105
00020 [L1099] JMP      A=3 B=128 C=61 D=32829 target=82
00021 [L1100] UGET     A=3 B=0 C=1 D=1 require
00022 [L1100] KSTR     A=4 B=0 C=5 D=5 'update.update_mgr'
00023 [L1100] CALL     A=3 B=2 C=2 D=514 
00024 [L1101] TGETS    A=4 B=1 C=6 D=262 'status'
00025 [L1101] ISNEN    A=4 B=0 C=1 D=1 2
00026 [L1101] JMP      A=4 B=128 C=31 D=32799 target=58
00027 [L1102] TGETS    A=4 B=3 C=7 D=775 'doDownLoadFile'
00028 [L1102] MOV      A=5 B=0 C=1 D=1 
00029 [L1102] CALL     A=4 B=1 C=2 D=258 
00030 [L1103] TGETS    A=4 B=1 C=1 D=257 'filename'
00031 [L1103] ISF      A=0 B=0 C=4 D=4 
00032 [L1103] JMP      A=5 B=128 C=64 D=32832 target=97
00033 [L1104] TGETS    A=4 B=1 C=1 D=257 'filename'
00034 [L1104] ISNES    A=4 B=0 C=8 D=8 'send_problem'
00035 [L1104] JMP      A=4 B=128 C=5 D=32773 target=41
00036 [L1105] GGET     A=4 B=0 C=9 D=9 'd_ms'
00037 [L1105] TGETS    A=4 B=4 C=10 D=1034 'd_systemSetUI'
00038 [L1105] TGETS    A=4 B=4 C=11 D=1035 'callbackSendProblem'
00039 [L1105] CALL     A=4 B=1 C=1 D=257 
00040 [L1105] JMP      A=4 B=128 C=56 D=32824 target=97
00041 [L1106] TGETS    A=4 B=1 C=1 D=257 'filename'
00042 [L1106] ISNES    A=4 B=0 C=12 D=12 'find_problem'
00043 [L1106] JMP      A=4 B=128 C=5 D=32773 target=49
00044 [L1107] GGET     A=4 B=0 C=9 D=9 'd_ms'
00045 [L1107] TGETS    A=4 B=4 C=10 D=1034 'd_systemSetUI'
00046 [L1107] TGETS    A=4 B=4 C=13 D=1037 'callbackFindProblem'
00047 [L1107] CALL     A=4 B=1 C=1 D=257 
00048 [L1107] JMP      A=4 B=128 C=48 D=32816 target=97
00049 [L1108] TGETS    A=4 B=1 C=1 D=257 'filename'
00050 [L1108] ISNES    A=4 B=0 C=14 D=14 'create_user_reply'
00051 [L1108] JMP      A=4 B=128 C=45 D=32813 target=97
00052 [L1109] GGET     A=4 B=0 C=9 D=9 'd_ms'
00053 [L1109] TGETS    A=4 B=4 C=10 D=1034 'd_systemSetUI'
00054 [L1109] TGETS    A=4 B=4 C=15 D=1039 'callbackCreateUserReply'
00055 [L1109] CALL     A=4 B=1 C=1 D=257 
00056 [L1109] JMP      A=4 B=128 C=40 D=32808 target=97
00057 [L1113] JMP      A=4 B=128 C=39 D=32807 target=97
00058 [L1114] TGETS    A=4 B=1 C=6 D=262 'status'
00059 [L1114] ISNEN    A=4 B=0 C=2 D=2 1
00060 [L1114] JMP      A=4 B=128 C=4 D=32772 target=65
00061 [L1115] TGETS    A=4 B=3 C=16 D=784 'downloadingFile'
00062 [L1115] MOV      A=5 B=0 C=1 D=1 
00063 [L1115] CALL     A=4 B=1 C=2 D=258 
00064 [L1115] JMP      A=4 B=128 C=32 D=32800 target=97
00065 [L1116] TGETS    A=4 B=1 C=6 D=262 'status'
00066 [L1116] ISNEN    A=4 B=0 C=3 D=3 -1
00067 [L1116] JMP      A=4 B=128 C=4 D=32772 target=72
00068 [L1117] TGETS    A=4 B=3 C=17 D=785 'downloadFailed'
00069 [L1117] MOV      A=5 B=0 C=1 D=1 
00070 [L1117] CALL     A=4 B=1 C=2 D=258 
00071 [L1117] JMP      A=4 B=128 C=25 D=32793 target=97
00072 [L1118] TGETS    A=4 B=1 C=6 D=262 'status'
00073 [L1118] ISNEN    A=4 B=0 C=4 D=4 -2
00074 [L1118] JMP      A=4 B=128 C=22 D=32790 target=97
00075 [L1119] UGET     A=4 B=0 C=0 D=0 cclog
00076 [L1119] KSTR     A=5 B=0 C=18 D=18 'time out(30s)!!!'
00077 [L1119] CALL     A=4 B=1 C=2 D=258 
00078 [L1120] TGETS    A=4 B=3 C=17 D=785 'downloadFailed'
00079 [L1120] MOV      A=5 B=0 C=1 D=1 
00080 [L1120] CALL     A=4 B=1 C=2 D=258 
00081 [L1121] JMP      A=3 B=128 C=15 D=32783 target=97
00082 [L1123] TGETS    A=3 B=1 C=0 D=256 'type'
00083 [L1123] IST      A=0 B=0 C=3 D=3 
00084 [L1123] JMP      A=4 B=128 C=1 D=32769 target=86
00085 [L1123] KSTR     A=3 B=0 C=19 D=19 'null'
00086 [L1124] TGETS    A=4 B=1 C=1 D=257 'filename'
00087 [L1124] IST      A=0 B=0 C=4 D=4 
00088 [L1124] JMP      A=5 B=128 C=1 D=32769 target=90
00089 [L1124] KSTR     A=4 B=0 C=19 D=19 'null'
00090 [L1125] UGET     A=5 B=0 C=0 D=0 cclog
00091 [L1125] KSTR     A=6 B=0 C=20 D=20 'ERROR: unhandle update_info_21, type='
00092 [L1125] MOV      A=7 B=0 C=3 D=3 
00093 [L1125] KSTR     A=8 B=0 C=4 D=4 ', filename='
00094 [L1125] MOV      A=9 B=0 C=4 D=4 
00095 [L1125] CAT      A=6 B=6 C=9 D=1545 
00096 [L1125] CALL     A=5 B=1 C=2 D=258 
00097 [L1128] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto37 offset=0x5afb source_lines=1151-1153 params=0
UPVALUES []
00001 [L1152] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L1152] TGETS    A=0 B=0 C=1 D=1 'd_alert'
00003 [L1152] TGETS    A=0 B=0 C=2 D=2 'start_wait'
00004 [L1152] KPRI     A=1 B=0 C=0 D=0 
00005 [L1152] KSHORT   A=2 B=0 C=5 D=5 5
00006 [L1152] CALL     A=0 B=1 C=3 D=259 
00007 [L1153] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto38 offset=0x5b44 source_lines=1163-1169 params=0
UPVALUES ['require']
00001 [L1165] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L1165] TGETS    A=0 B=0 C=1 D=1 'd_net'
00003 [L1165] TGETS    A=0 B=0 C=2 D=2 'resetNetWork'
00004 [L1165] CALL     A=0 B=1 C=1 D=257 
00005 [L1167] UGET     A=0 B=0 C=0 D=0 require
00006 [L1167] KSTR     A=1 B=0 C=3 D=3 'update.ms_jumper'
00007 [L1167] CALL     A=0 B=2 C=2 D=514 
00008 [L1168] TGETS    A=1 B=0 C=4 D=4 'refresh_updateUI'
00009 [L1168] CALL     A=1 B=1 C=1 D=257 
00010 [L1169] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto39 offset=0x5bd6 source_lines=1133-1172 params=1
UPVALUES ['cclog', 'require']
00001 [L1135] IST      A=0 B=0 C=0 D=0 
00002 [L1135] JMP      A=1 B=128 C=1 D=32769 target=4
00003 [L1135] KSHORT   A=0 B=0 C=3 D=3 3
00004 [L1137] GGET     A=1 B=0 C=0 D=0 'g_isJumping'
00005 [L1137] ISF      A=0 B=0 C=1 D=1 
00006 [L1137] JMP      A=2 B=128 C=4 D=32772 target=11
00007 [L1138] UGET     A=1 B=0 C=0 D=0 cclog
00008 [L1138] KSTR     A=2 B=0 C=1 D=1 'is Jumping'
00009 [L1138] CALL     A=1 B=1 C=2 D=258 
00010 [L1139] UCLO     A=0 B=128 C=45 D=32813 target=56
00011 [L1144] KPRI     A=1 B=0 C=2 D=2 
00012 [L1144] GSET     A=1 B=0 C=0 D=0 'g_isJumping'
00013 [L1145] UGET     A=1 B=0 C=0 D=0 cclog
00014 [L1145] KSTR     A=2 B=0 C=2 D=2 'call jumpLoginUI'
00015 [L1145] CALL     A=1 B=1 C=2 D=258 
00016 [L1146] GGET     A=1 B=0 C=3 D=3 'd_ms'
00017 [L1146] TGETS    A=1 B=1 C=4 D=260 'd_stat'
00018 [L1146] TGETS    A=1 B=1 C=5 D=261 'cleanCrashFlag'
00019 [L1146] CALL     A=1 B=1 C=1 D=257 
00020 [L1148] GGET     A=1 B=0 C=3 D=3 'd_ms'
00021 [L1148] TGETS    A=1 B=1 C=6 D=262 'd_loginUI'
00022 [L1148] KPRI     A=2 B=0 C=0 D=0 
00023 [L1148] TSETS    A=2 B=1 C=7 D=263 'g_currentSence'
00024 [L1153] FNEW     A=1 B=0 C=8 D=8 {'kind': 'proto', 'id': 37}
00025 [L1154] GGET     A=2 B=0 C=3 D=3 'd_ms'
00026 [L1154] TGETS    A=2 B=2 C=9 D=521 'd_u'
00027 [L1154] TGETS    A=2 B=2 C=10 D=522 'delay_node'
00028 [L1154] KSHORT   A=3 B=0 C=0 D=0 0
00029 [L1154] MOV      A=4 B=0 C=1 D=1 
00030 [L1154] CALL     A=2 B=1 C=3 D=259 
00031 [L1156] UGET     A=2 B=0 C=0 D=0 cclog
00032 [L1156] KSTR     A=3 B=0 C=11 D=11 'clean globalTimer'
00033 [L1156] CALL     A=2 B=1 C=2 D=258 
00034 [L1157] GGET     A=2 B=0 C=3 D=3 'd_ms'
00035 [L1157] TGETS    A=2 B=2 C=12 D=524 'd_mainUI'
00036 [L1157] TGETS    A=2 B=2 C=13 D=525 'unScheduleCountTime'
00037 [L1157] CALL     A=2 B=1 C=1 D=257 
00038 [L1159] GGET     A=2 B=0 C=3 D=3 'd_ms'
00039 [L1159] TGETS    A=2 B=2 C=14 D=526 'd_net'
00040 [L1159] TGETS    A=2 B=2 C=15 D=527 'set_net_status'
00041 [L1159] KSTR     A=3 B=0 C=16 D=16 'INIT'
00042 [L1159] KPRI     A=4 B=0 C=2 D=2 
00043 [L1159] CALL     A=2 B=1 C=3 D=259 
00044 [L1160] GGET     A=2 B=0 C=3 D=3 'd_ms'
00045 [L1160] TGETS    A=2 B=2 C=14 D=526 'd_net'
00046 [L1160] TGETS    A=2 B=2 C=17 D=529 'cancelTick'
00047 [L1160] CALL     A=2 B=1 C=1 D=257 
00048 [L1169] FNEW     A=2 B=0 C=18 D=18 {'kind': 'proto', 'id': 38}
00049 [L1171] GGET     A=3 B=0 C=3 D=3 'd_ms'
00050 [L1171] TGETS    A=3 B=3 C=9 D=777 'd_u'
00051 [L1171] TGETS    A=3 B=3 C=10 D=778 'delay_node'
00052 [L1171] MOV      A=4 B=0 C=0 D=0 
00053 [L1171] MOV      A=5 B=0 C=2 D=2 
00054 [L1171] CALL     A=3 B=1 C=3 D=259 
00055 [L1172] RET0     A=0 B=0 C=1 D=1 
00056 [L1172] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto40 offset=0x5e03 source_lines=1176-1181 params=3
UPVALUES ['string']
00001 [L1177] UGET     A=3 B=0 C=0 D=0 string
00002 [L1177] TGETS    A=3 B=3 C=0 D=768 'format'
00003 [L1177] KSTR     A=4 B=0 C=1 D=1 'login_code_%d'
00004 [L1177] TGETS    A=5 B=1 C=2 D=258 'reason'
00005 [L1177] CALL     A=3 B=2 C=3 D=515 
00006 [L1178] GGET     A=4 B=0 C=3 D=3 'd_ms'
00007 [L1178] TGETS    A=4 B=4 C=4 D=1028 'd_info'
00008 [L1178] TGETS    A=4 B=4 C=5 D=1029 'show'
00009 [L1178] GGET     A=5 B=0 C=3 D=3 'd_ms'
00010 [L1178] TGETS    A=5 B=5 C=6 D=1286 'd_hz'
00011 [L1178] TGETS    A=5 B=5 C=7 D=1287 'gethz'
00012 [L1178] MOV      A=6 B=0 C=3 D=3 
00013 [L1178] CALL     A=5 B=0 C=2 D=2 
00014 [L1178] CALLM    A=4 B=1 C=0 D=256 
00015 [L1179] GGET     A=4 B=0 C=3 D=3 'd_ms'
00016 [L1179] TGETS    A=4 B=4 C=8 D=1032 'd_alert'
00017 [L1179] TGETS    A=4 B=4 C=9 D=1033 'stop_wait'
00018 [L1179] CALL     A=4 B=1 C=1 D=257 
00019 [L1180] GGET     A=4 B=0 C=3 D=3 'd_ms'
00020 [L1180] TGETS    A=4 B=4 C=10 D=1034 'd_net'
00021 [L1180] TGETS    A=4 B=4 C=11 D=1035 'kick'
00022 [L1180] CALL     A=4 B=1 C=1 D=257 
00023 [L1181] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto41 offset=0x5f02 source_lines=1196-1196 params=0
UPVALUES []
00001 [L1196] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L1196] TGETS    A=0 B=0 C=1 D=1 'd_guildFightUI'
00003 [L1196] TGETS    A=0 B=0 C=2 D=2 'invalid_match_time'
00004 [L1196] CALL     A=0 B=1 C=1 D=257 
00005 [L1196] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto42 offset=0x5f4f source_lines=1197-1197 params=0
UPVALUES []
00001 [L1197] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L1197] TGETS    A=0 B=0 C=1 D=1 'd_guildFightUI'
00003 [L1197] TGETS    A=0 B=0 C=2 D=2 'less_action_point'
00004 [L1197] CALL     A=0 B=1 C=1 D=257 
00005 [L1197] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto43 offset=0x5f9b source_lines=1198-1198 params=0
UPVALUES []
00001 [L1198] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L1198] TGETS    A=0 B=0 C=1 D=1 'd_guildFightUI'
00003 [L1198] TGETS    A=0 B=0 C=2 D=2 'less_life_point'
00004 [L1198] CALL     A=0 B=1 C=1 D=257 
00005 [L1198] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto44 offset=0x5fe7 source_lines=1202-1846 params=3
UPVALUES ['table', 'cclog', 'os', 'opetaionFunc', 'string']
00001 [L1203] UGET     A=3 B=0 C=0 D=0 table
00002 [L1203] TGETS    A=3 B=3 C=0 D=768 'loadstring'
00003 [L1203] TGETS    A=4 B=1 C=1 D=257 'data'
00004 [L1203] CALL     A=3 B=2 C=2 D=514 
00005 [L1205] ISEQP    A=1 B=0 C=0 D=0 
00006 [L1205] JMP      A=4 B=140 C=191 D=36031 target=3270
00007 [L1205] TGETS    A=4 B=1 C=2 D=258 'id'
00008 [L1205] ISEQN    A=4 B=0 C=0 D=0 0
00009 [L1205] JMP      A=4 B=140 C=188 D=36028 target=3270
00010 [L1206] UGET     A=4 B=0 C=1 D=1 cclog
00011 [L1206] KSTR     A=5 B=0 C=3 D=3 'call msg_common_event_2998, ----[%d]'
00012 [L1206] TGETS    A=6 B=1 C=2 D=258 'id'
00013 [L1206] CALL     A=4 B=1 C=3 D=259 
00014 [L1207] GGET     A=4 B=0 C=4 D=4 'd_ms'
00015 [L1207] TGETS    A=4 B=4 C=5 D=1029 'd_alert'
00016 [L1207] TGETS    A=4 B=4 C=6 D=1030 'stop_wait'
00017 [L1207] CALL     A=4 B=1 C=1 D=257 
00018 [L1208] TGETS    A=4 B=1 C=2 D=258 'id'
00019 [L1208] ISNEN    A=4 B=0 C=1 D=1 1
00020 [L1208] JMP      A=4 B=128 C=59 D=32827 target=80
00021 [L1209] TGETS    A=4 B=3 C=7 D=775 'flag'
00022 [L1209] ISNEN    A=4 B=0 C=2 D=2 2
00023 [L1209] JMP      A=4 B=128 C=1 D=32769 target=25
00024 [L1209] JMP      A=4 B=140 C=173 D=36013 target=3270
00025 [L1211] TGETS    A=4 B=3 C=7 D=775 'flag'
00026 [L1211] ISNEN    A=4 B=0 C=1 D=1 1
00027 [L1211] JMP      A=4 B=128 C=6 D=32774 target=34
00028 [L1212] GGET     A=4 B=0 C=4 D=4 'd_ms'
00029 [L1212] TGETS    A=4 B=4 C=8 D=1032 'd_packageUI'
00030 [L1212] TGETS    A=4 B=4 C=9 D=1033 'show'
00031 [L1212] MOV      A=5 B=0 C=1 D=1 
00032 [L1212] CALL     A=4 B=1 C=2 D=258 
00033 [L1212] JMP      A=4 B=140 C=164 D=36004 target=3270
00034 [L1213] TGETS    A=4 B=3 C=7 D=775 'flag'
00035 [L1213] ISNEN    A=4 B=0 C=0 D=0 0
00036 [L1213] JMP      A=4 B=128 C=14 D=32782 target=51
00037 [L1214] GGET     A=4 B=0 C=4 D=4 'd_ms'
00038 [L1214] TGETS    A=4 B=4 C=10 D=1034 'd_mainUI'
00039 [L1214] TGETS    A=4 B=4 C=11 D=1035 'g_isNeedGuide'
00040 [L1214] ISF      A=0 B=0 C=4 D=4 
00041 [L1214] JMP      A=5 B=128 C=1 D=32769 target=43
00042 [L1215] RET0     A=0 B=0 C=1 D=1 
00043 [L1218] UGET     A=4 B=0 C=1 D=1 cclog
00044 [L1218] KSTR     A=5 B=0 C=12 D=12 'Lua:Gundam:::msg_modify_attr_1032>>updateCharacterInfo 1 times!!!'
00045 [L1218] CALL     A=4 B=1 C=2 D=258 
00046 [L1219] GGET     A=4 B=0 C=4 D=4 'd_ms'
00047 [L1219] TGETS    A=4 B=4 C=13 D=1037 'd_lineupUI'
00048 [L1219] TGETS    A=4 B=4 C=14 D=1038 'reShowDetail'
00049 [L1219] CALL     A=4 B=1 C=1 D=257 
00050 [L1219] JMP      A=4 B=140 C=147 D=35987 target=3270
00051 [L1220] TGETS    A=4 B=3 C=7 D=775 'flag'
00052 [L1220] ISNEN    A=4 B=0 C=3 D=3 3
00053 [L1220] JMP      A=4 B=128 C=5 D=32773 target=59
00054 [L1221] GGET     A=4 B=0 C=4 D=4 'd_ms'
00055 [L1221] TGETS    A=4 B=4 C=15 D=1039 'd_charPositionUI'
00056 [L1221] TGETS    A=4 B=4 C=16 D=1040 'updateItemSucceed'
00057 [L1221] CALL     A=4 B=1 C=1 D=257 
00058 [L1221] JMP      A=4 B=140 C=139 D=35979 target=3270
00059 [L1222] TGETS    A=4 B=3 C=7 D=775 'flag'
00060 [L1222] ISNEN    A=4 B=0 C=4 D=4 4
00061 [L1222] JMP      A=4 B=128 C=10 D=32778 target=72
00062 [L1223] GGET     A=4 B=0 C=4 D=4 'd_ms'
00063 [L1223] TGETS    A=4 B=4 C=17 D=1041 'd_formationUI'
00064 [L1223] TGETS    A=4 B=4 C=18 D=1042 'replaceCharSucceed'
00065 [L1223] CALL     A=4 B=1 C=1 D=257 
00066 [L1224] GGET     A=4 B=0 C=4 D=4 'd_ms'
00067 [L1224] TGETS    A=4 B=4 C=15 D=1039 'd_charPositionUI'
00068 [L1224] TGETS    A=4 B=4 C=19 D=1043 'changeCharSucceed'
00069 [L1224] KSHORT   A=5 B=0 C=1 D=1 1
00070 [L1224] CALL     A=4 B=1 C=2 D=258 
00071 [L1224] JMP      A=4 B=140 C=126 D=35966 target=3270
00072 [L1225] TGETS    A=4 B=3 C=7 D=775 'flag'
00073 [L1225] ISNEN    A=4 B=0 C=5 D=5 5
00074 [L1225] JMP      A=4 B=140 C=123 D=35963 target=3270
00075 [L1226] GGET     A=4 B=0 C=4 D=4 'd_ms'
00076 [L1226] TGETS    A=4 B=4 C=15 D=1039 'd_charPositionUI'
00077 [L1226] TGETS    A=4 B=4 C=20 D=1044 'changeCharOrderSucceed'
00078 [L1226] CALL     A=4 B=1 C=1 D=257 
00079 [L1228] JMP      A=4 B=140 C=118 D=35958 target=3270
00080 [L1230] TGETS    A=4 B=1 C=2 D=258 'id'
00081 [L1230] GGET     A=5 B=0 C=4 D=4 'd_ms'
00082 [L1230] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00083 [L1230] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00084 [L1230] TGETS    A=5 B=5 C=23 D=1303 'send_error_code'
00085 [L1230] ISNEV    A=4 B=0 C=5 D=5 
00086 [L1230] JMP      A=4 B=128 C=104 D=32872 target=191
00087 [L1232] TGETS    A=4 B=3 C=24 D=792 'op_string'
00088 [L1232] ISF      A=0 B=0 C=4 D=4 
00089 [L1232] JMP      A=5 B=128 C=6 D=32774 target=96
00090 [L1233] GGET     A=4 B=0 C=4 D=4 'd_ms'
00091 [L1233] TGETS    A=4 B=4 C=25 D=1049 'd_info'
00092 [L1233] TGETS    A=4 B=4 C=9 D=1033 'show'
00093 [L1233] TGETS    A=5 B=3 C=24 D=792 'op_string'
00094 [L1233] CALL     A=4 B=1 C=2 D=258 
00095 [L1233] JMP      A=4 B=140 C=102 D=35942 target=3270
00096 [L1234] TGETS    A=4 B=3 C=26 D=794 'op_code'
00097 [L1234] ISF      A=0 B=0 C=4 D=4 
00098 [L1234] JMP      A=5 B=140 C=99 D=35939 target=3270
00099 [L1237] TGETS    A=4 B=3 C=27 D=795 'update_list'
00100 [L1237] ISF      A=0 B=0 C=4 D=4 
00101 [L1237] JMP      A=5 B=128 C=20 D=32788 target=122
00102 [L1238] KSHORT   A=4 B=0 C=1 D=1 1
00103 [L1238] TGETS    A=5 B=3 C=27 D=795 'update_list'
00104 [L1238] LEN      A=5 B=0 C=5 D=5 
00105 [L1238] KSHORT   A=6 B=0 C=1 D=1 1
00106 [L1238] FORI     A=4 B=128 C=15 D=32783 target=122
00107 [L1239] TGETS    A=8 B=3 C=27 D=795 'update_list'
00108 [L1239] TGETV    A=8 B=8 C=7 D=2055 
00109 [L1240] TGETS    A=9 B=3 C=27 D=795 'update_list'
00110 [L1240] TGETV    A=9 B=9 C=7 D=2311 
00111 [L1240] TGETS    A=9 B=9 C=29 D=2333 'attr_list'
00112 [L1240] LEN      A=9 B=0 C=9 D=9 
00113 [L1240] TSETS    A=9 B=8 C=28 D=2076 'attr_count'
00114 [L1241] GGET     A=9 B=0 C=30 D=30 'msg_modify_attr_1032'
00115 [L1241] KSHORT   A=10 B=4 C=8 D=1032 1032
00116 [L1241] MOV      A=11 B=0 C=8 D=8 
00117 [L1241] UGET     A=12 B=0 C=2 D=2 os
00118 [L1241] TGETS    A=12 B=12 C=31 D=3103 'time'
00119 [L1241] CALL     A=12 B=0 C=1 D=1 
00120 [L1241] CALLM    A=9 B=1 C=2 D=258 
00121 [L1238] FORL     A=4 B=127 C=241 D=32753 target=107
00122 [L1245] TGETS    A=4 B=3 C=26 D=794 'op_code'
00123 [L1245] ISNEN    A=4 B=0 C=3 D=3 3
00124 [L1245] JMP      A=4 B=128 C=23 D=32791 target=148
00125 [L1246] GGET     A=4 B=0 C=4 D=4 'd_ms'
00126 [L1246] TGETS    A=4 B=4 C=32 D=1056 'd_activityUI'
00127 [L1246] TGETS    A=4 B=4 C=33 D=1057 'g_currentActivity'
00128 [L1246] GGET     A=5 B=0 C=4 D=4 'd_ms'
00129 [L1246] TGETS    A=5 B=5 C=32 D=1312 'd_activityUI'
00130 [L1246] TGETS    A=5 B=5 C=34 D=1314 'activityID'
00131 [L1246] TGETS    A=5 B=5 C=35 D=1315 'dujie'
00132 [L1246] ISNEV    A=4 B=0 C=5 D=5 
00133 [L1246] JMP      A=4 B=128 C=26 D=32794 target=160
00134 [L1248] GGET     A=4 B=0 C=4 D=4 'd_ms'
00135 [L1248] TGETS    A=4 B=4 C=36 D=1060 'd_crossDoomUI'
00136 [L1248] TGETS    A=4 B=4 C=37 D=1061 'pressInfoBegin'
00137 [L1248] CALL     A=4 B=1 C=1 D=257 
00138 [L1249] GGET     A=4 B=0 C=4 D=4 'd_ms'
00139 [L1249] TGETS    A=4 B=4 C=25 D=1049 'd_info'
00140 [L1249] TGETS    A=4 B=4 C=9 D=1033 'show'
00141 [L1249] GGET     A=5 B=0 C=4 D=4 'd_ms'
00142 [L1249] TGETS    A=5 B=5 C=38 D=1318 'd_hz'
00143 [L1249] TGETS    A=5 B=5 C=39 D=1319 'gethz'
00144 [L1249] KSTR     A=6 B=0 C=40 D=40 'operation_code_dujie'
00145 [L1249] CALL     A=5 B=0 C=2 D=2 
00146 [L1249] CALLM    A=4 B=1 C=0 D=256 
00147 [L1250] JMP      A=4 B=128 C=12 D=32780 target=160
00148 [L1251] TGETS    A=4 B=3 C=26 D=794 'op_code'
00149 [L1251] ISF      A=0 B=0 C=4 D=4 
00150 [L1251] JMP      A=5 B=128 C=9 D=32777 target=160
00151 [L1251] UGET     A=4 B=0 C=3 D=3 opetaionFunc
00152 [L1251] TGETS    A=5 B=3 C=26 D=794 'op_code'
00153 [L1251] TGETV    A=4 B=4 C=5 D=1029 
00154 [L1251] ISF      A=0 B=0 C=4 D=4 
00155 [L1251] JMP      A=5 B=128 C=4 D=32772 target=160
00156 [L1252] UGET     A=4 B=0 C=3 D=3 opetaionFunc
00157 [L1252] TGETS    A=5 B=3 C=26 D=794 'op_code'
00158 [L1252] TGETV    A=4 B=4 C=5 D=1029 
00159 [L1252] CALL     A=4 B=1 C=1 D=257 
00160 [L1256] TGETS    A=4 B=3 C=41 D=809 'show_tip'
00161 [L1256] ISF      A=0 B=0 C=4 D=4 
00162 [L1256] JMP      A=5 B=128 C=6 D=32774 target=169
00163 [L1257] GGET     A=4 B=0 C=4 D=4 'd_ms'
00164 [L1257] TGETS    A=4 B=4 C=25 D=1049 'd_info'
00165 [L1257] TGETS    A=4 B=4 C=9 D=1033 'show'
00166 [L1257] TGETS    A=5 B=3 C=41 D=809 'show_tip'
00167 [L1257] CALL     A=4 B=1 C=2 D=258 
00168 [L1257] JMP      A=4 B=128 C=11 D=32779 target=180
00169 [L1259] GGET     A=4 B=0 C=4 D=4 'd_ms'
00170 [L1259] TGETS    A=4 B=4 C=25 D=1049 'd_info'
00171 [L1259] TGETS    A=4 B=4 C=9 D=1033 'show'
00172 [L1259] GGET     A=5 B=0 C=4 D=4 'd_ms'
00173 [L1259] TGETS    A=5 B=5 C=38 D=1318 'd_hz'
00174 [L1259] TGETS    A=5 B=5 C=39 D=1319 'gethz'
00175 [L1259] KSTR     A=6 B=0 C=42 D=42 'operation_code_'
00176 [L1259] TGETS    A=7 B=3 C=26 D=794 'op_code'
00177 [L1259] CAT      A=6 B=6 C=7 D=1543 
00178 [L1259] CALL     A=5 B=0 C=2 D=2 
00179 [L1259] CALLM    A=4 B=1 C=0 D=256 
00180 [L1262] GGET     A=4 B=0 C=4 D=4 'd_ms'
00181 [L1262] TGETS    A=4 B=4 C=10 D=1034 'd_mainUI'
00182 [L1262] TGETS    A=4 B=4 C=11 D=1035 'g_isNeedGuide'
00183 [L1262] ISF      A=0 B=0 C=4 D=4 
00184 [L1262] JMP      A=5 B=140 C=13 D=35853 target=3270
00185 [L1263] UGET     A=4 B=0 C=1 D=1 cclog
00186 [L1263] KSTR     A=5 B=0 C=43 D=43 '--------------->get error code in guide, jump to login UI <-------------'
00187 [L1263] CALL     A=4 B=1 C=2 D=258 
00188 [L1264] GGET     A=4 B=0 C=44 D=44 'jumpLoginUI'
00189 [L1264] CALL     A=4 B=1 C=1 D=257 
00190 [L1266] JMP      A=4 B=140 C=7 D=35847 target=3270
00191 [L1268] TGETS    A=4 B=1 C=2 D=258 'id'
00192 [L1268] GGET     A=5 B=0 C=4 D=4 'd_ms'
00193 [L1268] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00194 [L1268] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00195 [L1268] TGETS    A=5 B=5 C=45 D=1325 'get_spirit'
00196 [L1268] ISNEV    A=4 B=0 C=5 D=5 
00197 [L1268] JMP      A=4 B=128 C=6 D=32774 target=204
00198 [L1270] GGET     A=4 B=0 C=4 D=4 'd_ms'
00199 [L1270] TGETS    A=4 B=4 C=46 D=1070 'd_data'
00200 [L1270] TGETS    A=4 B=4 C=47 D=1071 'updateSoulsData'
00201 [L1270] MOV      A=5 B=0 C=3 D=3 
00202 [L1270] CALL     A=4 B=1 C=2 D=258 
00203 [L1270] JMP      A=4 B=139 C=250 D=35834 target=3270
00204 [L1272] TGETS    A=4 B=1 C=2 D=258 'id'
00205 [L1272] GGET     A=5 B=0 C=4 D=4 'd_ms'
00206 [L1272] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00207 [L1272] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00208 [L1272] TGETS    A=5 B=5 C=48 D=1328 'attention'
00209 [L1272] ISNEV    A=4 B=0 C=5 D=5 
00210 [L1272] JMP      A=4 B=128 C=36 D=32804 target=247
00211 [L1273] TGETS    A=4 B=3 C=49 D=817 'count'
00212 [L1273] ISF      A=0 B=0 C=4 D=4 
00213 [L1273] JMP      A=5 B=128 C=27 D=32795 target=241
00214 [L1274] TGETS    A=4 B=3 C=49 D=817 'count'
00215 [L1276] UGET     A=5 B=0 C=4 D=4 string
00216 [L1276] TGETS    A=5 B=5 C=50 D=1330 'format'
00217 [L1276] GGET     A=6 B=0 C=4 D=4 'd_ms'
00218 [L1276] TGETS    A=6 B=6 C=38 D=1574 'd_hz'
00219 [L1276] TGETS    A=6 B=6 C=39 D=1575 'gethz'
00220 [L1276] KSTR     A=7 B=0 C=51 D=51 'maxAttention'
00221 [L1276] CALL     A=6 B=2 C=2 D=514 
00222 [L1276] MOV      A=7 B=0 C=4 D=4 
00223 [L1276] CALL     A=5 B=2 C=3 D=515 
00224 [L1277] ISNEN    A=4 B=0 C=0 D=0 0
00225 [L1277] JMP      A=6 B=128 C=9 D=32777 target=235
00226 [L1278] UGET     A=6 B=0 C=4 D=4 string
00227 [L1278] TGETS    A=6 B=6 C=50 D=1586 'format'
00228 [L1278] GGET     A=7 B=0 C=4 D=4 'd_ms'
00229 [L1278] TGETS    A=7 B=7 C=38 D=1830 'd_hz'
00230 [L1278] TGETS    A=7 B=7 C=39 D=1831 'gethz'
00231 [L1278] KSTR     A=8 B=0 C=52 D=52 'hasInBlack'
00232 [L1278] CALL     A=7 B=0 C=2 D=2 
00233 [L1278] CALLM    A=6 B=2 C=0 D=512 
00234 [L1278] MOV      A=5 B=0 C=6 D=6 
00235 [L1280] GGET     A=6 B=0 C=4 D=4 'd_ms'
00236 [L1280] TGETS    A=6 B=6 C=25 D=1561 'd_info'
00237 [L1280] TGETS    A=6 B=6 C=9 D=1545 'show'
00238 [L1280] MOV      A=7 B=0 C=5 D=5 
00239 [L1280] CALL     A=6 B=1 C=2 D=258 
00240 [L1281] RET0     A=0 B=0 C=1 D=1 
00241 [L1283] GGET     A=4 B=0 C=4 D=4 'd_ms'
00242 [L1283] TGETS    A=4 B=4 C=53 D=1077 'd_followUI'
00243 [L1283] TGETS    A=4 B=4 C=54 D=1078 'followResult'
00244 [L1283] MOV      A=5 B=0 C=3 D=3 
00245 [L1283] CALL     A=4 B=1 C=2 D=258 
00246 [L1283] JMP      A=4 B=139 C=207 D=35791 target=3270
00247 [L1285] TGETS    A=4 B=1 C=2 D=258 'id'
00248 [L1285] GGET     A=5 B=0 C=4 D=4 'd_ms'
00249 [L1285] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00250 [L1285] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00251 [L1285] TGETS    A=5 B=5 C=55 D=1335 'mail_list'
00252 [L1285] ISNEV    A=4 B=0 C=5 D=5 
00253 [L1285] JMP      A=4 B=128 C=6 D=32774 target=260
00254 [L1286] GGET     A=4 B=0 C=4 D=4 'd_ms'
00255 [L1286] TGETS    A=4 B=4 C=56 D=1080 'd_messageUI'
00256 [L1286] TGETS    A=4 B=4 C=57 D=1081 'addSystemMailIdList'
00257 [L1286] MOV      A=5 B=0 C=3 D=3 
00258 [L1286] CALL     A=4 B=1 C=2 D=258 
00259 [L1286] JMP      A=4 B=139 C=194 D=35778 target=3270
00260 [L1288] TGETS    A=4 B=1 C=2 D=258 'id'
00261 [L1288] GGET     A=5 B=0 C=4 D=4 'd_ms'
00262 [L1288] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00263 [L1288] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00264 [L1288] TGETS    A=5 B=5 C=58 D=1338 'mail_content'
00265 [L1288] ISNEV    A=4 B=0 C=5 D=5 
00266 [L1288] JMP      A=4 B=128 C=6 D=32774 target=273
00267 [L1289] GGET     A=4 B=0 C=4 D=4 'd_ms'
00268 [L1289] TGETS    A=4 B=4 C=56 D=1080 'd_messageUI'
00269 [L1289] TGETS    A=4 B=4 C=59 D=1083 'addSystemMailContent'
00270 [L1289] MOV      A=5 B=0 C=3 D=3 
00271 [L1289] CALL     A=4 B=1 C=2 D=258 
00272 [L1289] JMP      A=4 B=139 C=181 D=35765 target=3270
00273 [L1291] TGETS    A=4 B=1 C=2 D=258 'id'
00274 [L1291] GGET     A=5 B=0 C=4 D=4 'd_ms'
00275 [L1291] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00276 [L1291] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00277 [L1291] TGETS    A=5 B=5 C=60 D=1340 'mail_attach'
00278 [L1291] ISNEV    A=4 B=0 C=5 D=5 
00279 [L1291] JMP      A=4 B=128 C=6 D=32774 target=286
00280 [L1292] GGET     A=4 B=0 C=4 D=4 'd_ms'
00281 [L1292] TGETS    A=4 B=4 C=56 D=1080 'd_messageUI'
00282 [L1292] TGETS    A=4 B=4 C=61 D=1085 'getSystemMailAttach'
00283 [L1292] MOV      A=5 B=0 C=3 D=3 
00284 [L1292] CALL     A=4 B=1 C=2 D=258 
00285 [L1292] JMP      A=4 B=139 C=168 D=35752 target=3270
00286 [L1294] TGETS    A=4 B=1 C=2 D=258 'id'
00287 [L1294] GGET     A=5 B=0 C=4 D=4 'd_ms'
00288 [L1294] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00289 [L1294] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00290 [L1294] TGETS    A=5 B=5 C=62 D=1342 'sell_equip'
00291 [L1294] ISNEV    A=4 B=0 C=5 D=5 
00292 [L1294] JMP      A=4 B=128 C=6 D=32774 target=299
00293 [L1295] GGET     A=4 B=0 C=4 D=4 'd_ms'
00294 [L1295] TGETS    A=4 B=4 C=63 D=1087 'd_batchSaleUI'
00295 [L1295] TGETS    A=4 B=4 C=64 D=1088 'getSaleResult'
00296 [L1295] MOV      A=5 B=0 C=1 D=1 
00297 [L1295] CALL     A=4 B=1 C=2 D=258 
00298 [L1295] JMP      A=4 B=139 C=155 D=35739 target=3270
00299 [L1297] TGETS    A=4 B=1 C=2 D=258 'id'
00300 [L1297] GGET     A=5 B=0 C=4 D=4 'd_ms'
00301 [L1297] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00302 [L1297] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00303 [L1297] TGETS    A=5 B=5 C=65 D=1345 'bulletin'
00304 [L1297] ISNEV    A=4 B=0 C=5 D=5 
00305 [L1297] JMP      A=4 B=128 C=28 D=32796 target=334
00306 [L1299] GGET     A=4 B=0 C=4 D=4 'd_ms'
00307 [L1299] TGETS    A=4 B=4 C=10 D=1034 'd_mainUI'
00308 [L1299] TGETS    A=4 B=4 C=11 D=1035 'g_isNeedGuide'
00309 [L1299] IST      A=0 B=0 C=4 D=4 
00310 [L1300] JMP      A=4 B=139 C=143 D=35727 target=3270
00311 [L1300] GGET     A=4 B=0 C=4 D=4 'd_ms'
00312 [L1300] TGETS    A=4 B=4 C=66 D=1090 'd_loginUI'
00313 [L1300] TGETS    A=4 B=4 C=67 D=1091 'g_currentSence'
00314 [L1300] GGET     A=5 B=0 C=4 D=4 'd_ms'
00315 [L1300] TGETS    A=5 B=5 C=66 D=1346 'd_loginUI'
00316 [L1300] TGETS    A=5 B=5 C=68 D=1348 'senceID'
00317 [L1300] TGETS    A=5 B=5 C=69 D=1349 'mainUI'
00318 [L1300] ISNEV    A=4 B=0 C=5 D=5 
00319 [L1300] JMP      A=4 B=139 C=134 D=35718 target=3270
00320 [L1301] GGET     A=4 B=0 C=4 D=4 'd_ms'
00321 [L1301] TGETS    A=4 B=4 C=70 D=1094 'd_noticeUI'
00322 [L1301] TGETS    A=4 B=4 C=71 D=1095 'updateNoticeList'
00323 [L1301] MOV      A=5 B=0 C=3 D=3 
00324 [L1301] CALL     A=4 B=1 C=2 D=258 
00325 [L1302] GGET     A=4 B=0 C=4 D=4 'd_ms'
00326 [L1302] TGETS    A=4 B=4 C=70 D=1094 'd_noticeUI'
00327 [L1302] TGETS    A=4 B=4 C=9 D=1033 'show'
00328 [L1302] GGET     A=5 B=0 C=4 D=4 'd_ms'
00329 [L1302] TGETS    A=5 B=5 C=10 D=1290 'd_mainUI'
00330 [L1302] TGETS    A=5 B=5 C=72 D=1352 'g_mainUI'
00331 [L1302] TGETS    A=5 B=5 C=73 D=1353 'main_layer'
00332 [L1302] CALL     A=4 B=1 C=2 D=258 
00333 [L1303] JMP      A=4 B=139 C=120 D=35704 target=3270
00334 [L1305] TGETS    A=4 B=1 C=2 D=258 'id'
00335 [L1305] GGET     A=5 B=0 C=4 D=4 'd_ms'
00336 [L1305] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00337 [L1305] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00338 [L1305] TGETS    A=5 B=5 C=74 D=1354 'lineup_data'
00339 [L1305] ISNEV    A=4 B=0 C=5 D=5 
00340 [L1305] JMP      A=4 B=128 C=10 D=32778 target=351
00341 [L1306] GGET     A=4 B=0 C=4 D=4 'd_ms'
00342 [L1306] TGETS    A=4 B=4 C=75 D=1099 'd_checkLineupUI'
00343 [L1306] TGETS    A=4 B=4 C=9 D=1033 'show'
00344 [L1306] MOV      A=5 B=0 C=3 D=3 
00345 [L1306] CALL     A=4 B=1 C=2 D=258 
00346 [L1307] GGET     A=4 B=0 C=4 D=4 'd_ms'
00347 [L1307] TGETS    A=4 B=4 C=5 D=1029 'd_alert'
00348 [L1307] TGETS    A=4 B=4 C=6 D=1030 'stop_wait'
00349 [L1307] CALL     A=4 B=1 C=1 D=257 
00350 [L1307] JMP      A=4 B=139 C=103 D=35687 target=3270
00351 [L1309] TGETS    A=4 B=1 C=2 D=258 'id'
00352 [L1309] GGET     A=5 B=0 C=4 D=4 'd_ms'
00353 [L1309] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00354 [L1309] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00355 [L1309] TGETS    A=5 B=5 C=76 D=1356 'gift_attach'
00356 [L1309] ISNEV    A=4 B=0 C=5 D=5 
00357 [L1309] JMP      A=4 B=128 C=6 D=32774 target=364
00358 [L1311] GGET     A=4 B=0 C=4 D=4 'd_ms'
00359 [L1311] TGETS    A=4 B=4 C=77 D=1101 'd_systemSetUI'
00360 [L1311] TGETS    A=4 B=4 C=78 D=1102 'recvExchangGiftBag'
00361 [L1311] MOV      A=5 B=0 C=3 D=3 
00362 [L1311] CALL     A=4 B=1 C=2 D=258 
00363 [L1311] JMP      A=4 B=139 C=90 D=35674 target=3270
00364 [L1313] TGETS    A=4 B=1 C=2 D=258 'id'
00365 [L1313] GGET     A=5 B=0 C=4 D=4 'd_ms'
00366 [L1313] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00367 [L1313] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00368 [L1313] TGETS    A=5 B=5 C=79 D=1359 'modify_name'
00369 [L1313] ISNEV    A=4 B=0 C=5 D=5 
00370 [L1313] JMP      A=4 B=128 C=6 D=32774 target=377
00371 [L1315] GGET     A=4 B=0 C=4 D=4 'd_ms'
00372 [L1315] TGETS    A=4 B=4 C=80 D=1104 'd_commonLayerUI'
00373 [L1315] TGETS    A=4 B=4 C=81 D=1105 'recvModitynameMsg'
00374 [L1315] MOV      A=5 B=0 C=3 D=3 
00375 [L1315] CALL     A=4 B=1 C=2 D=258 
00376 [L1315] JMP      A=4 B=139 C=77 D=35661 target=3270
00377 [L1317] TGETS    A=4 B=1 C=2 D=258 'id'
00378 [L1317] GGET     A=5 B=0 C=4 D=4 'd_ms'
00379 [L1317] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00380 [L1317] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00381 [L1317] TGETS    A=5 B=5 C=82 D=1362 'object_upgrade'
00382 [L1317] ISNEV    A=4 B=0 C=5 D=5 
00383 [L1317] JMP      A=4 B=128 C=49 D=32817 target=433
00384 [L1319] TGETS    A=4 B=3 C=83 D=851 'obj_type'
00385 [L1319] GGET     A=5 B=0 C=4 D=4 'd_ms'
00386 [L1319] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00387 [L1319] TGETS    A=5 B=5 C=84 D=1364 'object_type'
00388 [L1319] TGETS    A=5 B=5 C=85 D=1365 'item'
00389 [L1319] ISNEV    A=4 B=0 C=5 D=5 
00390 [L1319] JMP      A=4 B=128 C=6 D=32774 target=397
00391 [L1320] GGET     A=4 B=0 C=4 D=4 'd_ms'
00392 [L1320] TGETS    A=4 B=4 C=86 D=1110 'd_equipmentUpgradeUI'
00393 [L1320] TGETS    A=4 B=4 C=87 D=1111 'recvEnhanceMsg'
00394 [L1320] MOV      A=5 B=0 C=3 D=3 
00395 [L1320] CALL     A=4 B=1 C=2 D=258 
00396 [L1320] JMP      A=4 B=139 C=57 D=35641 target=3270
00397 [L1323] TGETS    A=4 B=3 C=83 D=851 'obj_type'
00398 [L1323] GGET     A=5 B=0 C=4 D=4 'd_ms'
00399 [L1323] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00400 [L1323] TGETS    A=5 B=5 C=84 D=1364 'object_type'
00401 [L1323] TGETS    A=5 B=5 C=88 D=1368 'skill'
00402 [L1323] ISNEV    A=4 B=0 C=5 D=5 
00403 [L1323] JMP      A=4 B=128 C=6 D=32774 target=410
00404 [L1324] GGET     A=4 B=0 C=4 D=4 'd_ms'
00405 [L1324] TGETS    A=4 B=4 C=89 D=1113 'd_skillUpgradeUI'
00406 [L1324] TGETS    A=4 B=4 C=90 D=1114 'showServerRet'
00407 [L1324] MOV      A=5 B=0 C=3 D=3 
00408 [L1324] CALL     A=4 B=1 C=2 D=258 
00409 [L1324] JMP      A=4 B=139 C=44 D=35628 target=3270
00410 [L1326] TGETS    A=4 B=3 C=83 D=851 'obj_type'
00411 [L1326] GGET     A=5 B=0 C=4 D=4 'd_ms'
00412 [L1326] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00413 [L1326] TGETS    A=5 B=5 C=84 D=1364 'object_type'
00414 [L1326] TGETS    A=5 B=5 C=91 D=1371 'role'
00415 [L1326] ISNEV    A=4 B=0 C=5 D=5 
00416 [L1326] JMP      A=4 B=139 C=37 D=35621 target=3270
00417 [L1327] GGET     A=4 B=0 C=4 D=4 'd_ms'
00418 [L1327] TGETS    A=4 B=4 C=10 D=1034 'd_mainUI'
00419 [L1327] TGETS    A=4 B=4 C=92 D=1116 'g_playerInfo'
00420 [L1327] KPRI     A=5 B=0 C=2 D=2 
00421 [L1327] TSETS    A=5 B=4 C=93 D=1117 'isLevelUp'
00422 [L1328] GGET     A=4 B=0 C=4 D=4 'd_ms'
00423 [L1328] TGETS    A=4 B=4 C=10 D=1034 'd_mainUI'
00424 [L1328] TGETS    A=4 B=4 C=92 D=1116 'g_playerInfo'
00425 [L1328] TSETS    A=3 B=4 C=94 D=1118 'levelUpInfo'
00426 [L1330] GGET     A=4 B=0 C=4 D=4 'd_ms'
00427 [L1330] TGETS    A=4 B=4 C=10 D=1034 'd_mainUI'
00428 [L1330] TDUP     A=5 B=0 C=97 D=97 {'kind': 'table', 'value': {}}
00429 [L1330] TGETS    A=6 B=3 C=96 D=864 'gift_list'
00430 [L1330] TSETS    A=6 B=5 C=98 D=1378 'prize_list'
00431 [L1330] TSETS    A=5 B=4 C=95 D=1119 'levelup_prize'
00432 [L1331] JMP      A=4 B=139 C=21 D=35605 target=3270
00433 [L1333] TGETS    A=4 B=1 C=2 D=258 'id'
00434 [L1333] GGET     A=5 B=0 C=4 D=4 'd_ms'
00435 [L1333] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00436 [L1333] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00437 [L1333] TGETS    A=5 B=5 C=99 D=1379 'update_impart'
00438 [L1333] ISNEV    A=4 B=0 C=5 D=5 
00439 [L1333] JMP      A=4 B=128 C=6 D=32774 target=446
00440 [L1335] GGET     A=4 B=0 C=4 D=4 'd_ms'
00441 [L1335] TGETS    A=4 B=4 C=100 D=1124 'd_inheritUI'
00442 [L1335] TGETS    A=4 B=4 C=101 D=1125 'recvInheritMsg'
00443 [L1335] MOV      A=5 B=0 C=3 D=3 
00444 [L1335] CALL     A=4 B=1 C=2 D=258 
00445 [L1335] JMP      A=4 B=139 C=8 D=35592 target=3270
00446 [L1337] TGETS    A=4 B=1 C=2 D=258 'id'
00447 [L1337] GGET     A=5 B=0 C=4 D=4 'd_ms'
00448 [L1337] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00449 [L1337] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00450 [L1337] TGETS    A=5 B=5 C=102 D=1382 'god_bless'
00451 [L1337] ISNEV    A=4 B=0 C=5 D=5 
00452 [L1337] JMP      A=4 B=128 C=6 D=32774 target=459
00453 [L1339] GGET     A=4 B=0 C=4 D=4 'd_ms'
00454 [L1339] TGETS    A=4 B=4 C=103 D=1127 'd_godBlessUI'
00455 [L1339] TGETS    A=4 B=4 C=104 D=1128 'recvGodBless'
00456 [L1339] MOV      A=5 B=0 C=3 D=3 
00457 [L1339] CALL     A=4 B=1 C=2 D=258 
00458 [L1339] JMP      A=4 B=138 C=251 D=35579 target=3270
00459 [L1341] TGETS    A=4 B=1 C=2 D=258 'id'
00460 [L1341] GGET     A=5 B=0 C=4 D=4 'd_ms'
00461 [L1341] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00462 [L1341] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00463 [L1341] TGETS    A=5 B=5 C=105 D=1385 'tollgate_prize'
00464 [L1341] ISNEV    A=4 B=0 C=5 D=5 
00465 [L1341] JMP      A=4 B=128 C=8 D=32776 target=474
00466 [L1343] TDUP     A=4 B=0 C=107 D=107 {'kind': 'table', 'value': {'prize_src': 'GuanQia'}}
00467 [L1343] TSETS    A=4 B=3 C=106 D=874 'attach_content'
00468 [L1344] GGET     A=4 B=0 C=4 D=4 'd_ms'
00469 [L1344] TGETS    A=4 B=4 C=108 D=1132 'd_prizeUI'
00470 [L1344] TGETS    A=4 B=4 C=109 D=1133 'setPrize'
00471 [L1344] MOV      A=5 B=0 C=3 D=3 
00472 [L1344] CALL     A=4 B=1 C=2 D=258 
00473 [L1344] JMP      A=4 B=138 C=236 D=35564 target=3270
00474 [L1346] TGETS    A=4 B=1 C=2 D=258 'id'
00475 [L1346] GGET     A=5 B=0 C=4 D=4 'd_ms'
00476 [L1346] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00477 [L1346] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00478 [L1346] TGETS    A=5 B=5 C=110 D=1390 'update_label'
00479 [L1346] ISNEV    A=4 B=0 C=5 D=5 
00480 [L1346] JMP      A=4 B=128 C=5 D=32773 target=486
00481 [L1348] GGET     A=4 B=0 C=4 D=4 'd_ms'
00482 [L1348] TGETS    A=4 B=4 C=111 D=1135 'd_runeUI'
00483 [L1348] TGETS    A=4 B=4 C=112 D=1136 'onGetHandbookResult'
00484 [L1348] CALL     A=4 B=1 C=1 D=257 
00485 [L1348] JMP      A=4 B=138 C=224 D=35552 target=3270
00486 [L1349] TGETS    A=4 B=1 C=2 D=258 'id'
00487 [L1349] GGET     A=5 B=0 C=4 D=4 'd_ms'
00488 [L1349] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00489 [L1349] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00490 [L1349] TGETS    A=5 B=5 C=113 D=1393 'rape_info'
00491 [L1349] ISNEV    A=4 B=0 C=5 D=5 
00492 [L1349] JMP      A=4 B=128 C=6 D=32774 target=499
00493 [L1351] GGET     A=4 B=0 C=4 D=4 'd_ms'
00494 [L1351] TGETS    A=4 B=4 C=36 D=1060 'd_crossDoomUI'
00495 [L1351] TGETS    A=4 B=4 C=114 D=1138 'callbackRapeInfo'
00496 [L1351] MOV      A=5 B=0 C=3 D=3 
00497 [L1351] CALL     A=4 B=1 C=2 D=258 
00498 [L1351] JMP      A=4 B=138 C=211 D=35539 target=3270
00499 [L1352] TGETS    A=4 B=1 C=2 D=258 'id'
00500 [L1352] GGET     A=5 B=0 C=4 D=4 'd_ms'
00501 [L1352] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00502 [L1352] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00503 [L1352] TGETS    A=5 B=5 C=115 D=1395 'rape_fight_result'
00504 [L1352] ISNEV    A=4 B=0 C=5 D=5 
00505 [L1352] JMP      A=4 B=128 C=6 D=32774 target=512
00506 [L1354] GGET     A=4 B=0 C=4 D=4 'd_ms'
00507 [L1354] TGETS    A=4 B=4 C=36 D=1060 'd_crossDoomUI'
00508 [L1354] TGETS    A=4 B=4 C=116 D=1140 'callbackRapeFightRet'
00509 [L1354] MOV      A=5 B=0 C=3 D=3 
00510 [L1354] CALL     A=4 B=1 C=2 D=258 
00511 [L1354] JMP      A=4 B=138 C=198 D=35526 target=3270
00512 [L1355] TGETS    A=4 B=1 C=2 D=258 'id'
00513 [L1355] GGET     A=5 B=0 C=4 D=4 'd_ms'
00514 [L1355] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00515 [L1355] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00516 [L1355] TGETS    A=5 B=5 C=117 D=1397 'rape_sweep_result'
00517 [L1355] ISNEV    A=4 B=0 C=5 D=5 
00518 [L1355] JMP      A=4 B=128 C=6 D=32774 target=525
00519 [L1357] GGET     A=4 B=0 C=4 D=4 'd_ms'
00520 [L1357] TGETS    A=4 B=4 C=36 D=1060 'd_crossDoomUI'
00521 [L1357] TGETS    A=4 B=4 C=118 D=1142 'callbackRapeSweepResult'
00522 [L1357] MOV      A=5 B=0 C=3 D=3 
00523 [L1357] CALL     A=4 B=1 C=2 D=258 
00524 [L1357] JMP      A=4 B=138 C=185 D=35513 target=3270
00525 [L1358] TGETS    A=4 B=1 C=2 D=258 'id'
00526 [L1358] GGET     A=5 B=0 C=4 D=4 'd_ms'
00527 [L1358] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00528 [L1358] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00529 [L1358] TGETS    A=5 B=5 C=119 D=1399 'feed_result'
00530 [L1358] ISNEV    A=4 B=0 C=5 D=5 
00531 [L1358] JMP      A=4 B=128 C=6 D=32774 target=538
00532 [L1360] GGET     A=4 B=0 C=4 D=4 'd_ms'
00533 [L1360] TGETS    A=4 B=4 C=120 D=1144 'd_eatBunUI'
00534 [L1360] TGETS    A=4 B=4 C=121 D=1145 'callbackFeedRet'
00535 [L1360] MOV      A=5 B=0 C=3 D=3 
00536 [L1360] CALL     A=4 B=1 C=2 D=258 
00537 [L1360] JMP      A=4 B=138 C=172 D=35500 target=3270
00538 [L1361] TGETS    A=4 B=1 C=2 D=258 'id'
00539 [L1361] GGET     A=5 B=0 C=4 D=4 'd_ms'
00540 [L1361] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00541 [L1361] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00542 [L1361] TGETS    A=5 B=5 C=122 D=1402 'consume_cortege'
00543 [L1361] ISNEV    A=4 B=0 C=5 D=5 
00544 [L1361] JMP      A=4 B=128 C=6 D=32774 target=551
00545 [L1363] GGET     A=4 B=0 C=4 D=4 'd_ms'
00546 [L1363] TGETS    A=4 B=4 C=123 D=1147 'd_cortegeRecycleUI'
00547 [L1363] TGETS    A=4 B=4 C=124 D=1148 'callbackConsumeCortege'
00548 [L1363] MOV      A=5 B=0 C=3 D=3 
00549 [L1363] CALL     A=4 B=1 C=2 D=258 
00550 [L1363] JMP      A=4 B=138 C=159 D=35487 target=3270
00551 [L1364] TGETS    A=4 B=1 C=2 D=258 'id'
00552 [L1364] GGET     A=5 B=0 C=4 D=4 'd_ms'
00553 [L1364] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00554 [L1364] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00555 [L1364] TGETS    A=5 B=5 C=125 D=1405 'broadcast_msg'
00556 [L1364] ISNEV    A=4 B=0 C=5 D=5 
00557 [L1364] JMP      A=4 B=128 C=6 D=32774 target=564
00558 [L1366] GGET     A=4 B=0 C=4 D=4 'd_ms'
00559 [L1366] TGETS    A=4 B=4 C=126 D=1150 'd_hll'
00560 [L1366] TGETS    A=4 B=4 C=127 D=1151 'callbackNewMsg'
00561 [L1366] MOV      A=5 B=0 C=3 D=3 
00562 [L1366] CALL     A=4 B=1 C=2 D=258 
00563 [L1366] JMP      A=4 B=138 C=146 D=35474 target=3270
00564 [L1367] TGETS    A=4 B=1 C=2 D=258 'id'
00565 [L1367] GGET     A=5 B=0 C=4 D=4 'd_ms'
00566 [L1367] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00567 [L1367] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00568 [L1367] TGETS    A=5 B=5 C=128 D=1408 'rush_gold'
00569 [L1367] ISNEV    A=4 B=0 C=5 D=5 
00570 [L1367] JMP      A=4 B=128 C=6 D=32774 target=577
00571 [L1369] GGET     A=4 B=0 C=4 D=4 'd_ms'
00572 [L1369] TGETS    A=4 B=4 C=129 D=1153 'd_goldRushUI'
00573 [L1369] TGETS    A=4 B=4 C=130 D=1154 'onNewOthersMsg'
00574 [L1369] MOV      A=5 B=0 C=3 D=3 
00575 [L1369] CALL     A=4 B=1 C=2 D=258 
00576 [L1369] JMP      A=4 B=138 C=133 D=35461 target=3270
00577 [L1370] TGETS    A=4 B=1 C=2 D=258 'id'
00578 [L1370] GGET     A=5 B=0 C=4 D=4 'd_ms'
00579 [L1370] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00580 [L1370] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00581 [L1370] TGETS    A=5 B=5 C=131 D=1411 'search_gold_news'
00582 [L1370] ISNEV    A=4 B=0 C=5 D=5 
00583 [L1370] JMP      A=4 B=128 C=6 D=32774 target=590
00584 [L1372] GGET     A=4 B=0 C=4 D=4 'd_ms'
00585 [L1372] TGETS    A=4 B=4 C=132 D=1156 'd_fishRushUI'
00586 [L1372] TGETS    A=4 B=4 C=130 D=1154 'onNewOthersMsg'
00587 [L1372] MOV      A=5 B=0 C=3 D=3 
00588 [L1372] CALL     A=4 B=1 C=2 D=258 
00589 [L1372] JMP      A=4 B=138 C=120 D=35448 target=3270
00590 [L1373] TGETS    A=4 B=1 C=2 D=258 'id'
00591 [L1373] GGET     A=5 B=0 C=4 D=4 'd_ms'
00592 [L1373] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00593 [L1373] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00594 [L1373] TGETS    A=5 B=5 C=133 D=1413 'role_rush_gold'
00595 [L1373] ISNEV    A=4 B=0 C=5 D=5 
00596 [L1373] JMP      A=4 B=128 C=6 D=32774 target=603
00597 [L1375] GGET     A=4 B=0 C=4 D=4 'd_ms'
00598 [L1375] TGETS    A=4 B=4 C=129 D=1153 'd_goldRushUI'
00599 [L1375] TGETS    A=4 B=4 C=134 D=1158 'onGetGoldRushResult'
00600 [L1375] MOV      A=5 B=0 C=3 D=3 
00601 [L1375] CALL     A=4 B=1 C=2 D=258 
00602 [L1375] JMP      A=4 B=138 C=107 D=35435 target=3270
00603 [L1376] TGETS    A=4 B=1 C=2 D=258 'id'
00604 [L1376] GGET     A=5 B=0 C=4 D=4 'd_ms'
00605 [L1376] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00606 [L1376] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00607 [L1376] TGETS    A=5 B=5 C=135 D=1415 'search_gold'
00608 [L1376] ISNEV    A=4 B=0 C=5 D=5 
00609 [L1376] JMP      A=4 B=128 C=6 D=32774 target=616
00610 [L1378] GGET     A=4 B=0 C=4 D=4 'd_ms'
00611 [L1378] TGETS    A=4 B=4 C=132 D=1156 'd_fishRushUI'
00612 [L1378] TGETS    A=4 B=4 C=136 D=1160 'onGetFishRushResult'
00613 [L1378] MOV      A=5 B=0 C=3 D=3 
00614 [L1378] CALL     A=4 B=1 C=2 D=258 
00615 [L1378] JMP      A=4 B=138 C=94 D=35422 target=3270
00616 [L1379] TGETS    A=4 B=1 C=2 D=258 'id'
00617 [L1379] GGET     A=5 B=0 C=4 D=4 'd_ms'
00618 [L1379] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00619 [L1379] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00620 [L1379] TGETS    A=5 B=5 C=137 D=1417 'visit_caishen_prize'
00621 [L1379] ISNEV    A=4 B=0 C=5 D=5 
00622 [L1379] JMP      A=4 B=128 C=6 D=32774 target=629
00623 [L1381] GGET     A=4 B=0 C=4 D=4 'd_ms'
00624 [L1381] TGETS    A=4 B=4 C=138 D=1162 'd_springActivityMoneyUI'
00625 [L1381] TGETS    A=4 B=4 C=139 D=1163 'onGetSpringActivityMoneyResult'
00626 [L1381] MOV      A=5 B=0 C=3 D=3 
00627 [L1381] CALL     A=4 B=1 C=2 D=258 
00628 [L1381] JMP      A=4 B=138 C=81 D=35409 target=3270
00629 [L1382] TGETS    A=4 B=1 C=2 D=258 'id'
00630 [L1382] GGET     A=5 B=0 C=4 D=4 'd_ms'
00631 [L1382] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00632 [L1382] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00633 [L1382] TGETS    A=5 B=5 C=140 D=1420 'exchange_caishen_prize'
00634 [L1382] ISNEV    A=4 B=0 C=5 D=5 
00635 [L1382] JMP      A=4 B=128 C=6 D=32774 target=642
00636 [L1384] GGET     A=4 B=0 C=4 D=4 'd_ms'
00637 [L1384] TGETS    A=4 B=4 C=138 D=1162 'd_springActivityMoneyUI'
00638 [L1384] TGETS    A=4 B=4 C=141 D=1165 'onGetSpringActivityExchangeResult'
00639 [L1384] MOV      A=5 B=0 C=3 D=3 
00640 [L1384] CALL     A=4 B=1 C=2 D=258 
00641 [L1384] JMP      A=4 B=138 C=68 D=35396 target=3270
00642 [L1385] TGETS    A=4 B=1 C=2 D=258 'id'
00643 [L1385] GGET     A=5 B=0 C=4 D=4 'd_ms'
00644 [L1385] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00645 [L1385] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00646 [L1385] TGETS    A=5 B=5 C=142 D=1422 'checkin_result'
00647 [L1385] ISNEV    A=4 B=0 C=5 D=5 
00648 [L1385] JMP      A=4 B=128 C=6 D=32774 target=655
00649 [L1387] GGET     A=4 B=0 C=4 D=4 'd_ms'
00650 [L1387] TGETS    A=4 B=4 C=143 D=1167 'd_checkinUI'
00651 [L1387] TGETS    A=4 B=4 C=144 D=1168 'callbackUpdateRet'
00652 [L1387] MOV      A=5 B=0 C=3 D=3 
00653 [L1387] CALL     A=4 B=1 C=2 D=258 
00654 [L1387] JMP      A=4 B=138 C=55 D=35383 target=3270
00655 [L1388] TGETS    A=4 B=1 C=2 D=258 'id'
00656 [L1388] GGET     A=5 B=0 C=4 D=4 'd_ms'
00657 [L1388] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00658 [L1388] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00659 [L1388] TGETS    A=5 B=5 C=145 D=1425 'send_order_id'
00660 [L1388] ISNEV    A=4 B=0 C=5 D=5 
00661 [L1388] JMP      A=4 B=128 C=6 D=32774 target=668
00662 [L1390] GGET     A=4 B=0 C=4 D=4 'd_ms'
00663 [L1390] TGETS    A=4 B=4 C=146 D=1170 'd_recharge'
00664 [L1390] TGETS    A=4 B=4 C=147 D=1171 'callback_send_order_id'
00665 [L1390] MOV      A=5 B=0 C=3 D=3 
00666 [L1390] CALL     A=4 B=1 C=2 D=258 
00667 [L1390] JMP      A=4 B=138 C=42 D=35370 target=3270
00668 [L1391] TGETS    A=4 B=1 C=2 D=258 'id'
00669 [L1391] GGET     A=5 B=0 C=4 D=4 'd_ms'
00670 [L1391] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00671 [L1391] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00672 [L1391] TGETS    A=5 B=5 C=148 D=1428 'send_order_result'
00673 [L1391] ISNEV    A=4 B=0 C=5 D=5 
00674 [L1391] JMP      A=4 B=128 C=6 D=32774 target=681
00675 [L1393] GGET     A=4 B=0 C=4 D=4 'd_ms'
00676 [L1393] TGETS    A=4 B=4 C=146 D=1170 'd_recharge'
00677 [L1393] TGETS    A=4 B=4 C=149 D=1173 'callback_send_order_result'
00678 [L1393] MOV      A=5 B=0 C=3 D=3 
00679 [L1393] CALL     A=4 B=1 C=2 D=258 
00680 [L1393] JMP      A=4 B=138 C=29 D=35357 target=3270
00681 [L1395] TGETS    A=4 B=1 C=2 D=258 'id'
00682 [L1395] GGET     A=5 B=0 C=4 D=4 'd_ms'
00683 [L1395] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00684 [L1395] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00685 [L1395] TGETS    A=5 B=5 C=150 D=1430 'activity_board'
00686 [L1395] ISNEV    A=4 B=0 C=5 D=5 
00687 [L1395] JMP      A=4 B=128 C=6 D=32774 target=694
00688 [L1397] GGET     A=4 B=0 C=4 D=4 'd_ms'
00689 [L1397] TGETS    A=4 B=4 C=56 D=1080 'd_messageUI'
00690 [L1397] TGETS    A=4 B=4 C=151 D=1175 'callback_activity_board'
00691 [L1397] MOV      A=5 B=0 C=3 D=3 
00692 [L1397] CALL     A=4 B=1 C=2 D=258 
00693 [L1397] JMP      A=4 B=138 C=16 D=35344 target=3270
00694 [L1399] TGETS    A=4 B=1 C=2 D=258 'id'
00695 [L1399] GGET     A=5 B=0 C=4 D=4 'd_ms'
00696 [L1399] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00697 [L1399] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00698 [L1399] TGETS    A=5 B=5 C=152 D=1432 'report_player'
00699 [L1399] ISNEV    A=4 B=0 C=5 D=5 
00700 [L1399] JMP      A=4 B=128 C=6 D=32774 target=707
00701 [L1400] GGET     A=4 B=0 C=4 D=4 'd_ms'
00702 [L1400] TGETS    A=4 B=4 C=153 D=1177 'd_chatUI'
00703 [L1400] TGETS    A=4 B=4 C=154 D=1178 'callback_report_player'
00704 [L1400] MOV      A=5 B=0 C=3 D=3 
00705 [L1400] CALL     A=4 B=1 C=2 D=258 
00706 [L1400] JMP      A=4 B=138 C=3 D=35331 target=3270
00707 [L1402] TGETS    A=4 B=1 C=2 D=258 'id'
00708 [L1402] GGET     A=5 B=0 C=4 D=4 'd_ms'
00709 [L1402] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00710 [L1402] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00711 [L1402] TGETS    A=5 B=5 C=155 D=1435 'take_vip_gold'
00712 [L1402] ISNEV    A=4 B=0 C=5 D=5 
00713 [L1402] JMP      A=4 B=128 C=6 D=32774 target=720
00714 [L1403] GGET     A=4 B=0 C=4 D=4 'd_ms'
00715 [L1403] TGETS    A=4 B=4 C=156 D=1180 'd_vipUI'
00716 [L1403] TGETS    A=4 B=4 C=157 D=1181 'callback_take_vip_gold'
00717 [L1403] MOV      A=5 B=0 C=3 D=3 
00718 [L1403] CALL     A=4 B=1 C=2 D=258 
00719 [L1403] JMP      A=4 B=137 C=246 D=35318 target=3270
00720 [L1404] TGETS    A=4 B=1 C=2 D=258 'id'
00721 [L1404] GGET     A=5 B=0 C=4 D=4 'd_ms'
00722 [L1404] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00723 [L1404] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00724 [L1404] TGETS    A=5 B=5 C=158 D=1438 'take_vip_gift'
00725 [L1404] ISNEV    A=4 B=0 C=5 D=5 
00726 [L1404] JMP      A=4 B=128 C=6 D=32774 target=733
00727 [L1405] GGET     A=4 B=0 C=4 D=4 'd_ms'
00728 [L1405] TGETS    A=4 B=4 C=156 D=1180 'd_vipUI'
00729 [L1405] TGETS    A=4 B=4 C=159 D=1183 'callback_take_vip_gift'
00730 [L1405] MOV      A=5 B=0 C=3 D=3 
00731 [L1405] CALL     A=4 B=1 C=2 D=258 
00732 [L1405] JMP      A=4 B=137 C=233 D=35305 target=3270
00733 [L1406] TGETS    A=4 B=1 C=2 D=258 'id'
00734 [L1406] GGET     A=5 B=0 C=4 D=4 'd_ms'
00735 [L1406] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00736 [L1406] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00737 [L1406] TGETS    A=5 B=5 C=160 D=1440 'train_role'
00738 [L1406] ISNEV    A=4 B=0 C=5 D=5 
00739 [L1406] JMP      A=4 B=128 C=52 D=32820 target=792
00740 [L1408] TGETS    A=4 B=3 C=161 D=929 'addition_field'
00741 [L1408] GGET     A=5 B=0 C=4 D=4 'd_ms'
00742 [L1408] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00743 [L1408] TGETS    A=5 B=5 C=162 D=1442 'role_property'
00744 [L1408] TGETS    A=5 B=5 C=163 D=1443 'role_max_hp_plus'
00745 [L1408] ISNEV    A=4 B=0 C=5 D=5 
00746 [L1408] JMP      A=4 B=128 C=6 D=32774 target=753
00747 [L1409] GGET     A=4 B=0 C=4 D=4 'd_ms'
00748 [L1409] TGETS    A=4 B=4 C=164 D=1188 'd_practiceUI'
00749 [L1409] TGETS    A=4 B=4 C=165 D=1189 'g_increasedValue'
00750 [L1409] TGETS    A=5 B=3 C=167 D=935 'addition_value'
00751 [L1409] TSETS    A=5 B=4 C=166 D=1190 'increatedHP'
00752 [L1409] JMP      A=4 B=137 C=213 D=35285 target=3270
00753 [L1411] TGETS    A=4 B=3 C=161 D=929 'addition_field'
00754 [L1411] GGET     A=5 B=0 C=4 D=4 'd_ms'
00755 [L1411] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00756 [L1411] TGETS    A=5 B=5 C=162 D=1442 'role_property'
00757 [L1411] TGETS    A=5 B=5 C=168 D=1448 'role_max_magic_plus'
00758 [L1411] ISNEV    A=4 B=0 C=5 D=5 
00759 [L1411] JMP      A=4 B=128 C=6 D=32774 target=766
00760 [L1412] GGET     A=4 B=0 C=4 D=4 'd_ms'
00761 [L1412] TGETS    A=4 B=4 C=164 D=1188 'd_practiceUI'
00762 [L1412] TGETS    A=4 B=4 C=165 D=1189 'g_increasedValue'
00763 [L1412] TGETS    A=5 B=3 C=167 D=935 'addition_value'
00764 [L1412] TSETS    A=5 B=4 C=169 D=1193 'increatedMana'
00765 [L1412] JMP      A=4 B=137 C=200 D=35272 target=3270
00766 [L1414] TGETS    A=4 B=3 C=161 D=929 'addition_field'
00767 [L1414] GGET     A=5 B=0 C=4 D=4 'd_ms'
00768 [L1414] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00769 [L1414] TGETS    A=5 B=5 C=162 D=1442 'role_property'
00770 [L1414] TGETS    A=5 B=5 C=170 D=1450 'role_wuligongji_plus'
00771 [L1414] ISNEV    A=4 B=0 C=5 D=5 
00772 [L1414] JMP      A=4 B=128 C=6 D=32774 target=779
00773 [L1415] GGET     A=4 B=0 C=4 D=4 'd_ms'
00774 [L1415] TGETS    A=4 B=4 C=164 D=1188 'd_practiceUI'
00775 [L1415] TGETS    A=4 B=4 C=165 D=1189 'g_increasedValue'
00776 [L1415] TGETS    A=5 B=3 C=167 D=935 'addition_value'
00777 [L1415] TSETS    A=5 B=4 C=171 D=1195 'increatedDamage'
00778 [L1415] JMP      A=4 B=137 C=187 D=35259 target=3270
00779 [L1417] TGETS    A=4 B=3 C=161 D=929 'addition_field'
00780 [L1417] GGET     A=5 B=0 C=4 D=4 'd_ms'
00781 [L1417] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00782 [L1417] TGETS    A=5 B=5 C=162 D=1442 'role_property'
00783 [L1417] TGETS    A=5 B=5 C=172 D=1452 'role_wulifangyu_plus'
00784 [L1417] ISNEV    A=4 B=0 C=5 D=5 
00785 [L1417] JMP      A=4 B=137 C=180 D=35252 target=3270
00786 [L1418] GGET     A=4 B=0 C=4 D=4 'd_ms'
00787 [L1418] TGETS    A=4 B=4 C=164 D=1188 'd_practiceUI'
00788 [L1418] TGETS    A=4 B=4 C=165 D=1189 'g_increasedValue'
00789 [L1418] TGETS    A=5 B=3 C=167 D=935 'addition_value'
00790 [L1418] TSETS    A=5 B=4 C=173 D=1197 'increatedDefence'
00791 [L1420] JMP      A=4 B=137 C=174 D=35246 target=3270
00792 [L1422] TGETS    A=4 B=1 C=2 D=258 'id'
00793 [L1422] GGET     A=5 B=0 C=4 D=4 'd_ms'
00794 [L1422] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00795 [L1422] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00796 [L1422] TGETS    A=5 B=5 C=174 D=1454 'train_cortege'
00797 [L1422] ISNEV    A=4 B=0 C=5 D=5 
00798 [L1422] JMP      A=4 B=128 C=39 D=32807 target=838
00799 [L1424] TGETS    A=4 B=3 C=175 D=943 'train_result'
00800 [L1424] GGET     A=5 B=0 C=4 D=4 'd_ms'
00801 [L1424] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00802 [L1424] TGETS    A=5 B=5 C=176 D=1456 'train_cortege_result'
00803 [L1424] TGETS    A=5 B=5 C=177 D=1457 'request'
00804 [L1424] ISNEV    A=4 B=0 C=5 D=5 
00805 [L1424] JMP      A=4 B=128 C=6 D=32774 target=812
00806 [L1425] GGET     A=4 B=0 C=4 D=4 'd_ms'
00807 [L1425] TGETS    A=4 B=4 C=178 D=1202 'd_trainingUI'
00808 [L1425] TGETS    A=4 B=4 C=179 D=1203 'trainingResult'
00809 [L1425] MOV      A=5 B=0 C=3 D=3 
00810 [L1425] CALL     A=4 B=1 C=2 D=258 
00811 [L1425] JMP      A=4 B=137 C=154 D=35226 target=3270
00812 [L1426] TGETS    A=4 B=3 C=175 D=943 'train_result'
00813 [L1426] GGET     A=5 B=0 C=4 D=4 'd_ms'
00814 [L1426] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00815 [L1426] TGETS    A=5 B=5 C=176 D=1456 'train_cortege_result'
00816 [L1426] TGETS    A=5 B=5 C=180 D=1460 'confirm'
00817 [L1426] ISNEV    A=4 B=0 C=5 D=5 
00818 [L1426] JMP      A=4 B=128 C=6 D=32774 target=825
00819 [L1427] GGET     A=4 B=0 C=4 D=4 'd_ms'
00820 [L1427] TGETS    A=4 B=4 C=178 D=1202 'd_trainingUI'
00821 [L1427] TGETS    A=4 B=4 C=181 D=1205 'confirmResult'
00822 [L1427] MOV      A=5 B=0 C=3 D=3 
00823 [L1427] CALL     A=4 B=1 C=2 D=258 
00824 [L1427] JMP      A=4 B=137 C=141 D=35213 target=3270
00825 [L1428] TGETS    A=4 B=3 C=175 D=943 'train_result'
00826 [L1428] GGET     A=5 B=0 C=4 D=4 'd_ms'
00827 [L1428] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00828 [L1428] TGETS    A=5 B=5 C=176 D=1456 'train_cortege_result'
00829 [L1428] TGETS    A=5 B=5 C=182 D=1462 'giveup'
00830 [L1428] ISNEV    A=4 B=0 C=5 D=5 
00831 [L1428] JMP      A=4 B=137 C=134 D=35206 target=3270
00832 [L1429] GGET     A=4 B=0 C=4 D=4 'd_ms'
00833 [L1429] TGETS    A=4 B=4 C=178 D=1202 'd_trainingUI'
00834 [L1429] TGETS    A=4 B=4 C=183 D=1207 'giveupResult'
00835 [L1429] MOV      A=5 B=0 C=3 D=3 
00836 [L1429] CALL     A=4 B=1 C=2 D=258 
00837 [L1430] JMP      A=4 B=137 C=128 D=35200 target=3270
00838 [L1432] TGETS    A=4 B=1 C=2 D=258 'id'
00839 [L1432] GGET     A=5 B=0 C=4 D=4 'd_ms'
00840 [L1432] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00841 [L1432] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00842 [L1432] TGETS    A=5 B=5 C=184 D=1464 'equip_compose'
00843 [L1432] ISNEV    A=4 B=0 C=5 D=5 
00844 [L1432] JMP      A=4 B=128 C=6 D=32774 target=851
00845 [L1434] GGET     A=4 B=0 C=4 D=4 'd_ms'
00846 [L1434] TGETS    A=4 B=4 C=185 D=1209 'd_forgeUI'
00847 [L1434] TGETS    A=4 B=4 C=186 D=1210 'getForgeResult'
00848 [L1434] MOV      A=5 B=0 C=3 D=3 
00849 [L1434] CALL     A=4 B=1 C=2 D=258 
00850 [L1434] JMP      A=4 B=137 C=115 D=35187 target=3270
00851 [L1435] TGETS    A=4 B=1 C=2 D=258 'id'
00852 [L1435] GGET     A=5 B=0 C=4 D=4 'd_ms'
00853 [L1435] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00854 [L1435] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00855 [L1435] TGETS    A=5 B=5 C=187 D=1467 'update_compose'
00856 [L1435] ISNEV    A=4 B=0 C=5 D=5 
00857 [L1435] JMP      A=4 B=128 C=6 D=32774 target=864
00858 [L1437] GGET     A=4 B=0 C=4 D=4 'd_ms'
00859 [L1437] TGETS    A=4 B=4 C=185 D=1209 'd_forgeUI'
00860 [L1437] TGETS    A=4 B=4 C=188 D=1212 'updateForgeList'
00861 [L1437] MOV      A=5 B=0 C=3 D=3 
00862 [L1437] CALL     A=4 B=1 C=2 D=258 
00863 [L1437] JMP      A=4 B=137 C=102 D=35174 target=3270
00864 [L1439] TGETS    A=4 B=1 C=2 D=258 'id'
00865 [L1439] GGET     A=5 B=0 C=4 D=4 'd_ms'
00866 [L1439] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00867 [L1439] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00868 [L1439] TGETS    A=5 B=5 C=189 D=1469 'pick_cortege'
00869 [L1439] ISNEV    A=4 B=0 C=5 D=5 
00870 [L1439] JMP      A=4 B=128 C=6 D=32774 target=877
00871 [L1440] GGET     A=4 B=0 C=4 D=4 'd_ms'
00872 [L1440] TGETS    A=4 B=4 C=190 D=1214 'd_summonUI'
00873 [L1440] TGETS    A=4 B=4 C=191 D=1215 'getSummonResult'
00874 [L1440] MOV      A=5 B=0 C=3 D=3 
00875 [L1440] CALL     A=4 B=1 C=2 D=258 
00876 [L1440] JMP      A=4 B=137 C=89 D=35161 target=3270
00877 [L1441] TGETS    A=4 B=1 C=2 D=258 'id'
00878 [L1441] GGET     A=5 B=0 C=4 D=4 'd_ms'
00879 [L1441] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00880 [L1441] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00881 [L1441] TGETS    A=5 B=5 C=192 D=1472 'buy_item'
00882 [L1441] ISNEV    A=4 B=0 C=5 D=5 
00883 [L1441] JMP      A=4 B=128 C=6 D=32774 target=890
00884 [L1443] GGET     A=4 B=0 C=4 D=4 'd_ms'
00885 [L1443] TGETS    A=4 B=4 C=193 D=1217 'd_shopUI'
00886 [L1443] TGETS    A=4 B=4 C=194 D=1218 'recvBuyShopItem'
00887 [L1443] MOV      A=5 B=0 C=3 D=3 
00888 [L1443] CALL     A=4 B=1 C=2 D=258 
00889 [L1443] JMP      A=4 B=137 C=76 D=35148 target=3270
00890 [L1444] TGETS    A=4 B=1 C=2 D=258 'id'
00891 [L1444] GGET     A=5 B=0 C=4 D=4 'd_ms'
00892 [L1444] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00893 [L1444] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00894 [L1444] TGETS    A=5 B=5 C=195 D=1475 'spirit_compose'
00895 [L1444] ISNEV    A=4 B=0 C=5 D=5 
00896 [L1444] JMP      A=4 B=128 C=6 D=32774 target=903
00897 [L1446] GGET     A=4 B=0 C=4 D=4 'd_ms'
00898 [L1446] TGETS    A=4 B=4 C=196 D=1220 'd_allLineupUI'
00899 [L1446] TGETS    A=4 B=4 C=197 D=1221 'recvSoulComposeMsg'
00900 [L1446] MOV      A=5 B=0 C=3 D=3 
00901 [L1446] CALL     A=4 B=1 C=2 D=258 
00902 [L1446] JMP      A=4 B=137 C=63 D=35135 target=3270
00903 [L1447] TGETS    A=4 B=1 C=2 D=258 'id'
00904 [L1447] GGET     A=5 B=0 C=4 D=4 'd_ms'
00905 [L1447] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00906 [L1447] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00907 [L1447] TGETS    A=5 B=5 C=198 D=1478 'use_item'
00908 [L1447] ISNEV    A=4 B=0 C=5 D=5 
00909 [L1447] JMP      A=4 B=128 C=6 D=32774 target=916
00910 [L1449] GGET     A=4 B=0 C=4 D=4 'd_ms'
00911 [L1449] TGETS    A=4 B=4 C=80 D=1104 'd_commonLayerUI'
00912 [L1449] TGETS    A=4 B=4 C=199 D=1223 'recvUsedItem'
00913 [L1449] MOV      A=5 B=0 C=3 D=3 
00914 [L1449] CALL     A=4 B=1 C=2 D=258 
00915 [L1449] JMP      A=4 B=137 C=50 D=35122 target=3270
00916 [L1459] TGETS    A=4 B=1 C=2 D=258 'id'
00917 [L1459] GGET     A=5 B=0 C=4 D=4 'd_ms'
00918 [L1459] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00919 [L1459] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00920 [L1459] TGETS    A=5 B=5 C=200 D=1480 'lucky_list'
00921 [L1459] ISNEV    A=4 B=0 C=5 D=5 
00922 [L1459] JMP      A=4 B=128 C=6 D=32774 target=929
00923 [L1460] GGET     A=4 B=0 C=4 D=4 'd_ms'
00924 [L1460] TGETS    A=4 B=4 C=201 D=1225 'd_worldBossUI'
00925 [L1460] TGETS    A=4 B=4 C=202 D=1226 'getLuckRankRes'
00926 [L1460] MOV      A=5 B=0 C=3 D=3 
00927 [L1460] CALL     A=4 B=1 C=2 D=258 
00928 [L1460] JMP      A=4 B=137 C=37 D=35109 target=3270
00929 [L1461] TGETS    A=4 B=1 C=2 D=258 'id'
00930 [L1461] GGET     A=5 B=0 C=4 D=4 'd_ms'
00931 [L1461] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00932 [L1461] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00933 [L1461] TGETS    A=5 B=5 C=203 D=1483 'damage_history_list'
00934 [L1461] ISNEV    A=4 B=0 C=5 D=5 
00935 [L1461] JMP      A=4 B=128 C=6 D=32774 target=942
00936 [L1462] GGET     A=4 B=0 C=4 D=4 'd_ms'
00937 [L1462] TGETS    A=4 B=4 C=201 D=1225 'd_worldBossUI'
00938 [L1462] TGETS    A=4 B=4 C=204 D=1228 'getFightNewsRes'
00939 [L1462] MOV      A=5 B=0 C=3 D=3 
00940 [L1462] CALL     A=4 B=1 C=2 D=258 
00941 [L1462] JMP      A=4 B=137 C=24 D=35096 target=3270
00942 [L1463] TGETS    A=4 B=1 C=2 D=258 'id'
00943 [L1463] GGET     A=5 B=0 C=4 D=4 'd_ms'
00944 [L1463] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00945 [L1463] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00946 [L1463] TGETS    A=5 B=5 C=205 D=1485 'damage_expect_list'
00947 [L1463] ISNEV    A=4 B=0 C=5 D=5 
00948 [L1463] JMP      A=4 B=128 C=6 D=32774 target=955
00949 [L1464] GGET     A=4 B=0 C=4 D=4 'd_ms'
00950 [L1464] TGETS    A=4 B=4 C=201 D=1225 'd_worldBossUI'
00951 [L1464] TGETS    A=4 B=4 C=206 D=1230 'getFightInfo'
00952 [L1464] MOV      A=5 B=0 C=3 D=3 
00953 [L1464] CALL     A=4 B=1 C=2 D=258 
00954 [L1464] JMP      A=4 B=137 C=11 D=35083 target=3270
00955 [L1465] TGETS    A=4 B=1 C=2 D=258 'id'
00956 [L1465] GGET     A=5 B=0 C=4 D=4 'd_ms'
00957 [L1465] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00958 [L1465] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00959 [L1465] TGETS    A=5 B=5 C=207 D=1487 'lucky_prize'
00960 [L1465] ISNEV    A=4 B=0 C=5 D=5 
00961 [L1465] JMP      A=4 B=128 C=6 D=32774 target=968
00962 [L1466] GGET     A=4 B=0 C=4 D=4 'd_ms'
00963 [L1466] TGETS    A=4 B=4 C=201 D=1225 'd_worldBossUI'
00964 [L1466] TGETS    A=4 B=4 C=208 D=1232 'getLuckPointPrize'
00965 [L1466] MOV      A=5 B=0 C=3 D=3 
00966 [L1466] CALL     A=4 B=1 C=2 D=258 
00967 [L1466] JMP      A=4 B=136 C=254 D=35070 target=3270
00968 [L1467] TGETS    A=4 B=1 C=2 D=258 'id'
00969 [L1467] GGET     A=5 B=0 C=4 D=4 'd_ms'
00970 [L1467] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00971 [L1467] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00972 [L1467] TGETS    A=5 B=5 C=209 D=1489 'party_end'
00973 [L1467] ISNEV    A=4 B=0 C=5 D=5 
00974 [L1467] JMP      A=4 B=128 C=6 D=32774 target=981
00975 [L1468] GGET     A=4 B=0 C=4 D=4 'd_ms'
00976 [L1468] TGETS    A=4 B=4 C=201 D=1225 'd_worldBossUI'
00977 [L1468] TGETS    A=4 B=4 C=210 D=1234 'activityEnd'
00978 [L1468] MOV      A=5 B=0 C=3 D=3 
00979 [L1468] CALL     A=4 B=1 C=2 D=258 
00980 [L1468] JMP      A=4 B=136 C=241 D=35057 target=3270
00981 [L1469] TGETS    A=4 B=1 C=2 D=258 'id'
00982 [L1469] GGET     A=5 B=0 C=4 D=4 'd_ms'
00983 [L1469] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00984 [L1469] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00985 [L1469] TGETS    A=5 B=5 C=211 D=1491 'party_add_plus'
00986 [L1469] ISNEV    A=4 B=0 C=5 D=5 
00987 [L1469] JMP      A=4 B=128 C=6 D=32774 target=994
00988 [L1470] GGET     A=4 B=0 C=4 D=4 'd_ms'
00989 [L1470] TGETS    A=4 B=4 C=201 D=1225 'd_worldBossUI'
00990 [L1470] TGETS    A=4 B=4 C=212 D=1236 'updateBounsDamage'
00991 [L1470] MOV      A=5 B=0 C=3 D=3 
00992 [L1470] CALL     A=4 B=1 C=2 D=258 
00993 [L1470] JMP      A=4 B=136 C=228 D=35044 target=3270
00994 [L1471] TGETS    A=4 B=1 C=2 D=258 'id'
00995 [L1471] GGET     A=5 B=0 C=4 D=4 'd_ms'
00996 [L1471] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
00997 [L1471] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
00998 [L1471] TGETS    A=5 B=5 C=213 D=1493 'top_fight_prize'
00999 [L1471] ISNEV    A=4 B=0 C=5 D=5 
01000 [L1471] JMP      A=4 B=128 C=6 D=32774 target=1007
01001 [L1473] GGET     A=4 B=0 C=4 D=4 'd_ms'
01002 [L1473] TGETS    A=4 B=4 C=214 D=1238 'd_rankUI'
01003 [L1473] TGETS    A=4 B=4 C=215 D=1239 'recvRewardsResult'
01004 [L1473] MOV      A=5 B=0 C=3 D=3 
01005 [L1473] CALL     A=4 B=1 C=2 D=258 
01006 [L1473] JMP      A=4 B=136 C=215 D=35031 target=3270
01007 [L1474] TGETS    A=4 B=1 C=2 D=258 'id'
01008 [L1474] GGET     A=5 B=0 C=4 D=4 'd_ms'
01009 [L1474] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01010 [L1474] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01011 [L1474] TGETS    A=5 B=5 C=216 D=1496 'top_day_prize'
01012 [L1474] ISNEV    A=4 B=0 C=5 D=5 
01013 [L1474] JMP      A=4 B=128 C=6 D=32774 target=1020
01014 [L1476] GGET     A=4 B=0 C=4 D=4 'd_ms'
01015 [L1476] TGETS    A=4 B=4 C=214 D=1238 'd_rankUI'
01016 [L1476] TGETS    A=4 B=4 C=217 D=1241 'flashRankUI'
01017 [L1476] MOV      A=5 B=0 C=3 D=3 
01018 [L1476] CALL     A=4 B=1 C=2 D=258 
01019 [L1476] JMP      A=4 B=136 C=202 D=35018 target=3270
01020 [L1477] TGETS    A=4 B=1 C=2 D=258 'id'
01021 [L1477] GGET     A=5 B=0 C=4 D=4 'd_ms'
01022 [L1477] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01023 [L1477] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01024 [L1477] TGETS    A=5 B=5 C=218 D=1498 'new_role_guide'
01025 [L1477] ISNEV    A=4 B=0 C=5 D=5 
01026 [L1477] JMP      A=4 B=128 C=6 D=32774 target=1033
01027 [L1479] GGET     A=4 B=0 C=4 D=4 'd_ms'
01028 [L1479] TGETS    A=4 B=4 C=219 D=1243 'd_guideUI'
01029 [L1479] TGETS    A=4 B=4 C=220 D=1244 'guideSucceed'
01030 [L1479] MOV      A=5 B=0 C=3 D=3 
01031 [L1479] CALL     A=4 B=1 C=2 D=258 
01032 [L1479] JMP      A=4 B=136 C=189 D=35005 target=3270
01033 [L1481] TGETS    A=4 B=1 C=2 D=258 'id'
01034 [L1481] GGET     A=5 B=0 C=4 D=4 'd_ms'
01035 [L1481] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01036 [L1481] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01037 [L1481] TGETS    A=5 B=5 C=221 D=1501 'duty_status'
01038 [L1481] ISNEV    A=4 B=0 C=5 D=5 
01039 [L1481] JMP      A=4 B=128 C=6 D=32774 target=1046
01040 [L1482] GGET     A=4 B=0 C=4 D=4 'd_ms'
01041 [L1482] TGETS    A=4 B=4 C=222 D=1246 'd_endlessFightUI'
01042 [L1482] TGETS    A=4 B=4 C=223 D=1247 'getEndlessFightRes'
01043 [L1482] MOV      A=5 B=0 C=3 D=3 
01044 [L1482] CALL     A=4 B=1 C=2 D=258 
01045 [L1482] JMP      A=4 B=136 C=176 D=34992 target=3270
01046 [L1483] TGETS    A=4 B=1 C=2 D=258 'id'
01047 [L1483] GGET     A=5 B=0 C=4 D=4 'd_ms'
01048 [L1483] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01049 [L1483] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01050 [L1483] TGETS    A=5 B=5 C=224 D=1504 'exchange_top_score'
01051 [L1483] ISNEV    A=4 B=0 C=5 D=5 
01052 [L1483] JMP      A=4 B=128 C=6 D=32774 target=1059
01053 [L1484] GGET     A=4 B=0 C=4 D=4 'd_ms'
01054 [L1484] TGETS    A=4 B=4 C=214 D=1238 'd_rankUI'
01055 [L1484] TGETS    A=4 B=4 C=225 D=1249 'recvCreditsChargeMsg'
01056 [L1484] MOV      A=5 B=0 C=3 D=3 
01057 [L1484] CALL     A=4 B=1 C=2 D=258 
01058 [L1484] JMP      A=4 B=136 C=163 D=34979 target=3270
01059 [L1486] TGETS    A=4 B=1 C=2 D=258 'id'
01060 [L1486] GGET     A=5 B=0 C=4 D=4 'd_ms'
01061 [L1486] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01062 [L1486] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01063 [L1486] TGETS    A=5 B=5 C=226 D=1506 'duty_history_list'
01064 [L1486] ISNEV    A=4 B=0 C=5 D=5 
01065 [L1486] JMP      A=4 B=128 C=6 D=32774 target=1072
01066 [L1487] GGET     A=4 B=0 C=4 D=4 'd_ms'
01067 [L1487] TGETS    A=4 B=4 C=222 D=1246 'd_endlessFightUI'
01068 [L1487] TGETS    A=4 B=4 C=227 D=1251 'getRankInfo'
01069 [L1487] MOV      A=5 B=0 C=3 D=3 
01070 [L1487] CALL     A=4 B=1 C=2 D=258 
01071 [L1487] JMP      A=4 B=136 C=150 D=34966 target=3270
01072 [L1489] TGETS    A=4 B=1 C=2 D=258 'id'
01073 [L1489] GGET     A=5 B=0 C=4 D=4 'd_ms'
01074 [L1489] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01075 [L1489] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01076 [L1489] TGETS    A=5 B=5 C=228 D=1508 'visit_result'
01077 [L1489] ISNEV    A=4 B=0 C=5 D=5 
01078 [L1489] JMP      A=4 B=128 C=6 D=32774 target=1085
01079 [L1490] GGET     A=4 B=0 C=4 D=4 'd_ms'
01080 [L1490] TGETS    A=4 B=4 C=229 D=1253 'd_loginGameUI'
01081 [L1490] TGETS    A=4 B=4 C=230 D=1254 'getResFromServer'
01082 [L1490] MOV      A=5 B=0 C=3 D=3 
01083 [L1490] CALL     A=4 B=1 C=2 D=258 
01084 [L1490] JMP      A=4 B=136 C=137 D=34953 target=3270
01085 [L1491] TGETS    A=4 B=1 C=2 D=258 'id'
01086 [L1491] GGET     A=5 B=0 C=4 D=4 'd_ms'
01087 [L1491] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01088 [L1491] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01089 [L1491] TGETS    A=5 B=5 C=231 D=1511 'fight_end'
01090 [L1491] ISNEV    A=4 B=0 C=5 D=5 
01091 [L1491] JMP      A=4 B=128 C=38 D=32806 target=1130
01092 [L1495] TGETS    A=4 B=3 C=232 D=1000 'fight_id'
01093 [L1495] ISF      A=0 B=0 C=4 D=4 
01094 [L1495] JMP      A=5 B=136 C=127 D=34943 target=3270
01095 [L1495] TGETS    A=4 B=3 C=233 D=1001 'fight_type'
01096 [L1495] ISF      A=0 B=0 C=4 D=4 
01097 [L1495] JMP      A=5 B=136 C=124 D=34940 target=3270
01098 [L1495] GGET     A=4 B=0 C=234 D=234 'g_fight_info'
01099 [L1495] TGETS    A=5 B=3 C=232 D=1000 'fight_id'
01100 [L1495] TGETV    A=4 B=4 C=5 D=1029 
01101 [L1495] ISF      A=0 B=0 C=4 D=4 
01102 [L1495] JMP      A=5 B=136 C=119 D=34935 target=3270
01103 [L1496] GGET     A=4 B=0 C=4 D=4 'd_ms'
01104 [L1496] TGETS    A=4 B=4 C=5 D=1029 'd_alert'
01105 [L1496] TGETS    A=4 B=4 C=6 D=1030 'stop_wait'
01106 [L1496] CALL     A=4 B=1 C=1 D=257 
01107 [L1499] GGET     A=4 B=0 C=234 D=234 'g_fight_info'
01108 [L1499] TGETS    A=5 B=3 C=232 D=1000 'fight_id'
01109 [L1499] TGETV    A=4 B=4 C=5 D=1029 
01110 [L1499] TSETS    A=3 B=4 C=235 D=1259 'fight_end_data'
01111 [L1501] GGET     A=4 B=0 C=4 D=4 'd_ms'
01112 [L1501] TGETS    A=4 B=4 C=236 D=1260 'd_fightUI'
01113 [L1501] TGETS    A=4 B=4 C=237 D=1261 'actFight'
01114 [L1501] GGET     A=5 B=0 C=234 D=234 'g_fight_info'
01115 [L1501] TGETS    A=6 B=3 C=232 D=1000 'fight_id'
01116 [L1501] TGETV    A=5 B=5 C=6 D=1286 
01117 [L1501] TGETS    A=6 B=3 C=233 D=1001 'fight_type'
01118 [L1501] CALL     A=4 B=1 C=3 D=259 
01119 [L1502] GGET     A=4 B=0 C=4 D=4 'd_ms'
01120 [L1502] TGETS    A=4 B=4 C=236 D=1260 'd_fightUI'
01121 [L1502] TGETS    A=4 B=4 C=238 D=1262 'g_fightUI'
01122 [L1502] KPRI     A=5 B=0 C=1 D=1 
01123 [L1502] TSETS    A=5 B=4 C=239 D=1263 'is_fight_end'
01124 [L1503] GGET     A=4 B=0 C=4 D=4 'd_ms'
01125 [L1503] TGETS    A=4 B=4 C=236 D=1260 'd_fightUI'
01126 [L1503] TGETS    A=4 B=4 C=238 D=1262 'g_fightUI'
01127 [L1503] KPRI     A=5 B=0 C=1 D=1 
01128 [L1503] TSETS    A=5 B=4 C=240 D=1264 'is_replay'
01129 [L1504] JMP      A=4 B=136 C=92 D=34908 target=3270
01130 [L1506] TGETS    A=4 B=1 C=2 D=258 'id'
01131 [L1506] GGET     A=5 B=0 C=4 D=4 'd_ms'
01132 [L1506] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01133 [L1506] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01134 [L1506] TGETS    A=5 B=5 C=241 D=1521 'experience_notify'
01135 [L1506] ISNEV    A=4 B=0 C=5 D=5 
01136 [L1506] JMP      A=4 B=128 C=36 D=32804 target=1173
01137 [L1508] GGET     A=4 B=0 C=234 D=234 'g_fight_info'
01138 [L1508] TGETS    A=5 B=3 C=232 D=1000 'fight_id'
01139 [L1508] TGETV    A=4 B=4 C=5 D=1029 
01140 [L1508] ISF      A=0 B=0 C=4 D=4 
01141 [L1508] JMP      A=5 B=136 C=80 D=34896 target=3270
01142 [L1510] GGET     A=4 B=0 C=234 D=234 'g_fight_info'
01143 [L1510] TGETS    A=5 B=3 C=232 D=1000 'fight_id'
01144 [L1510] TGETV    A=4 B=4 C=5 D=1029 
01145 [L1510] TGETS    A=4 B=4 C=242 D=1266 'rewards'
01146 [L1510] IST      A=0 B=0 C=4 D=4 
01147 [L1510] JMP      A=4 B=128 C=5 D=32773 target=1153
01148 [L1511] GGET     A=4 B=0 C=234 D=234 'g_fight_info'
01149 [L1511] TGETS    A=5 B=3 C=232 D=1000 'fight_id'
01150 [L1511] TGETV    A=4 B=4 C=5 D=1029 
01151 [L1511] TNEW     A=5 B=0 C=0 D=0 
01152 [L1511] TSETS    A=5 B=4 C=242 D=1266 'rewards'
01153 [L1514] TGETS    A=4 B=3 C=83 D=851 'obj_type'
01154 [L1514] ISNEN    A=4 B=0 C=1 D=1 1
01155 [L1514] JMP      A=4 B=128 C=7 D=32775 target=1163
01156 [L1515] GGET     A=4 B=0 C=234 D=234 'g_fight_info'
01157 [L1515] TGETS    A=5 B=3 C=232 D=1000 'fight_id'
01158 [L1515] TGETV    A=4 B=4 C=5 D=1029 
01159 [L1515] TGETS    A=4 B=4 C=242 D=1266 'rewards'
01160 [L1515] TGETS    A=5 B=3 C=244 D=1012 'exp_plus'
01161 [L1515] TSETS    A=5 B=4 C=243 D=1267 'role_exp'
01162 [L1515] JMP      A=4 B=136 C=59 D=34875 target=3270
01163 [L1516] TGETS    A=4 B=3 C=83 D=851 'obj_type'
01164 [L1516] ISNEN    A=4 B=0 C=4 D=4 4
01165 [L1516] JMP      A=4 B=136 C=56 D=34872 target=3270
01166 [L1517] GGET     A=4 B=0 C=234 D=234 'g_fight_info'
01167 [L1517] TGETS    A=5 B=3 C=232 D=1000 'fight_id'
01168 [L1517] TGETV    A=4 B=4 C=5 D=1029 
01169 [L1517] TGETS    A=4 B=4 C=242 D=1266 'rewards'
01170 [L1517] TGETS    A=5 B=3 C=246 D=1014 'exp_list'
01171 [L1517] TSETS    A=5 B=4 C=245 D=1269 'cor_exp'
01172 [L1519] JMP      A=4 B=136 C=49 D=34865 target=3270
01173 [L1520] TGETS    A=4 B=1 C=2 D=258 'id'
01174 [L1520] GGET     A=5 B=0 C=4 D=4 'd_ms'
01175 [L1520] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01176 [L1520] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01177 [L1520] TGETS    A=5 B=5 C=247 D=1527 'event_status1'
01178 [L1520] ISNEV    A=4 B=0 C=5 D=5 
01179 [L1520] JMP      A=4 B=128 C=6 D=32774 target=1186
01180 [L1522] GGET     A=4 B=0 C=4 D=4 'd_ms'
01181 [L1522] TGETS    A=4 B=4 C=32 D=1056 'd_activityUI'
01182 [L1522] TGETS    A=4 B=4 C=248 D=1272 'getQiwenStatus'
01183 [L1522] MOV      A=5 B=0 C=3 D=3 
01184 [L1522] CALL     A=4 B=1 C=2 D=258 
01185 [L1522] JMP      A=4 B=136 C=36 D=34852 target=3270
01186 [L1523] TGETS    A=4 B=1 C=2 D=258 'id'
01187 [L1523] GGET     A=5 B=0 C=4 D=4 'd_ms'
01188 [L1523] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01189 [L1523] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01190 [L1523] TGETS    A=5 B=5 C=249 D=1529 'event_status2'
01191 [L1523] ISNEV    A=4 B=0 C=5 D=5 
01192 [L1523] JMP      A=4 B=128 C=6 D=32774 target=1199
01193 [L1525] GGET     A=4 B=0 C=4 D=4 'd_ms'
01194 [L1525] TGETS    A=4 B=4 C=32 D=1056 'd_activityUI'
01195 [L1525] TGETS    A=4 B=4 C=250 D=1274 'getYishiStatus'
01196 [L1525] MOV      A=5 B=0 C=3 D=3 
01197 [L1525] CALL     A=4 B=1 C=2 D=258 
01198 [L1525] JMP      A=4 B=136 C=23 D=34839 target=3270
01199 [L1526] TGETS    A=4 B=1 C=2 D=258 'id'
01200 [L1526] GGET     A=5 B=0 C=4 D=4 'd_ms'
01201 [L1526] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01202 [L1526] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01203 [L1526] TGETS    A=5 B=5 C=251 D=1531 'use_item_by_gold'
01204 [L1526] ISNEV    A=4 B=0 C=5 D=5 
01205 [L1526] JMP      A=4 B=128 C=65 D=32833 target=1271
01206 [L1527] TGETS    A=4 B=3 C=252 D=1020 'type_id'
01207 [L1527] ISNEN    A=4 B=0 C=6 D=6 1022
01208 [L1527] JMP      A=4 B=128 C=32 D=32800 target=1241
01209 [L1528] GGET     A=4 B=0 C=4 D=4 'd_ms'
01210 [L1528] TGETS    A=4 B=4 C=10 D=1034 'd_mainUI'
01211 [L1528] TGETS    A=4 B=4 C=92 D=1116 'g_playerInfo'
01212 [L1528] TGETS    A=4 B=4 C=253 D=1277 'increasedStr'
01213 [L1528] IST      A=0 B=0 C=4 D=4 
01214 [L1528] JMP      A=5 B=128 C=1 D=32769 target=1216
01215 [L1528] KSHORT   A=4 B=0 C=10 D=10 10
01216 [L1529] GGET     A=5 B=0 C=4 D=4 'd_ms'
01217 [L1529] TGETS    A=5 B=5 C=25 D=1305 'd_info'
01218 [L1529] TGETS    A=5 B=5 C=9 D=1289 'show'
01219 [L1529] UGET     A=6 B=0 C=4 D=4 string
01220 [L1529] TGETS    A=6 B=6 C=50 D=1586 'format'
01221 [L1529] GGET     A=7 B=0 C=4 D=4 'd_ms'
01222 [L1529] TGETS    A=7 B=7 C=38 D=1830 'd_hz'
01223 [L1529] TGETS    A=7 B=7 C=39 D=1831 'gethz'
01224 [L1529] KSTR     A=8 B=0 C=254 D=254 'congrasStrEne'
01225 [L1529] CALL     A=7 B=2 C=2 D=514 
01226 [L1529] GGET     A=8 B=0 C=4 D=4 'd_ms'
01227 [L1529] TGETS    A=8 B=8 C=38 D=2086 'd_hz'
01228 [L1529] TGETS    A=8 B=8 C=39 D=2087 'gethz'
01229 [L1529] KSTR     A=9 B=0 C=255 D=255 'strength'
01230 [L1529] CALL     A=8 B=2 C=2 D=514 
01231 [L1529] MOV      A=9 B=0 C=4 D=4 
01232 [L1529] CALL     A=6 B=0 C=4 D=4 
01233 [L1529] CALLM    A=5 B=1 C=0 D=256 
01234 [L1530] GGET     A=5 B=0 C=4 D=4 'd_ms'
01235 [L1530] KSTR     A=6 B=1 C=0 D=256 'd_saodangUI'
01236 [L1530] TGETV    A=5 B=5 C=6 D=1286 
01237 [L1530] KSTR     A=6 B=1 C=1 D=257 'reloadData'
01238 [L1530] TGETV    A=5 B=5 C=6 D=1286 
01239 [L1530] CALL     A=5 B=1 C=1 D=257 
01240 [L1530] JMP      A=4 B=135 C=237 D=34797 target=3270
01241 [L1531] TGETS    A=4 B=1 C=252 D=508 'type_id'
01242 [L1531] ISNEN    A=4 B=0 C=7 D=7 1023
01243 [L1531] JMP      A=4 B=135 C=234 D=34794 target=3270
01244 [L1532] GGET     A=4 B=0 C=4 D=4 'd_ms'
01245 [L1532] TGETS    A=4 B=4 C=10 D=1034 'd_mainUI'
01246 [L1532] TGETS    A=4 B=4 C=92 D=1116 'g_playerInfo'
01247 [L1532] KSTR     A=5 B=1 C=2 D=258 'increasedEne'
01248 [L1532] TGETV    A=4 B=4 C=5 D=1029 
01249 [L1532] IST      A=0 B=0 C=4 D=4 
01250 [L1532] JMP      A=5 B=128 C=1 D=32769 target=1252
01251 [L1532] KSHORT   A=4 B=0 C=10 D=10 10
01252 [L1533] GGET     A=5 B=0 C=4 D=4 'd_ms'
01253 [L1533] TGETS    A=5 B=5 C=25 D=1305 'd_info'
01254 [L1533] TGETS    A=5 B=5 C=9 D=1289 'show'
01255 [L1533] UGET     A=6 B=0 C=4 D=4 string
01256 [L1533] TGETS    A=6 B=6 C=50 D=1586 'format'
01257 [L1533] GGET     A=7 B=0 C=4 D=4 'd_ms'
01258 [L1533] TGETS    A=7 B=7 C=38 D=1830 'd_hz'
01259 [L1533] TGETS    A=7 B=7 C=39 D=1831 'gethz'
01260 [L1533] KSTR     A=8 B=0 C=254 D=254 'congrasStrEne'
01261 [L1533] CALL     A=7 B=2 C=2 D=514 
01262 [L1533] GGET     A=8 B=0 C=4 D=4 'd_ms'
01263 [L1533] TGETS    A=8 B=8 C=38 D=2086 'd_hz'
01264 [L1533] TGETS    A=8 B=8 C=39 D=2087 'gethz'
01265 [L1533] KSTR     A=9 B=1 C=3 D=259 'killPoint'
01266 [L1533] CALL     A=8 B=2 C=2 D=514 
01267 [L1533] MOV      A=9 B=0 C=4 D=4 
01268 [L1533] CALL     A=6 B=0 C=4 D=4 
01269 [L1533] CALLM    A=5 B=1 C=0 D=256 
01270 [L1534] JMP      A=4 B=135 C=207 D=34767 target=3270
01271 [L1535] TGETS    A=4 B=1 C=2 D=258 'id'
01272 [L1535] GGET     A=5 B=0 C=4 D=4 'd_ms'
01273 [L1535] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01274 [L1535] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01275 [L1535] KSTR     A=6 B=1 C=4 D=260 'cortege_evolve'
01276 [L1535] TGETV    A=5 B=5 C=6 D=1286 
01277 [L1535] ISNEV    A=4 B=0 C=5 D=5 
01278 [L1535] JMP      A=4 B=128 C=7 D=32775 target=1286
01279 [L1536] GGET     A=4 B=0 C=4 D=4 'd_ms'
01280 [L1536] KSTR     A=5 B=1 C=5 D=261 'd_feishengUI'
01281 [L1536] TGETV    A=4 B=4 C=5 D=1029 
01282 [L1536] KSTR     A=5 B=1 C=6 D=262 'getFeiShengRes'
01283 [L1536] TGETV    A=4 B=4 C=5 D=1029 
01284 [L1536] CALL     A=4 B=1 C=1 D=257 
01285 [L1536] JMP      A=4 B=135 C=192 D=34752 target=3270
01286 [L1537] TGETS    A=4 B=1 C=2 D=258 'id'
01287 [L1537] GGET     A=5 B=0 C=4 D=4 'd_ms'
01288 [L1537] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01289 [L1537] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01290 [L1537] KSTR     A=6 B=1 C=7 D=263 'remove_spirit'
01291 [L1537] TGETV    A=5 B=5 C=6 D=1286 
01292 [L1537] ISNEV    A=4 B=0 C=5 D=5 
01293 [L1537] JMP      A=4 B=128 C=8 D=32776 target=1302
01294 [L1538] KSTR     A=4 B=1 C=8 D=264 'total_count'
01295 [L1538] TGETV    A=4 B=3 C=4 D=772 
01296 [L1539] GGET     A=5 B=0 C=4 D=4 'd_ms'
01297 [L1539] TGETS    A=5 B=5 C=46 D=1326 'd_data'
01298 [L1539] TGETS    A=5 B=5 C=47 D=1327 'updateSoulsData'
01299 [L1539] MOV      A=6 B=0 C=3 D=3 
01300 [L1539] CALL     A=5 B=1 C=2 D=258 
01301 [L1539] JMP      A=4 B=135 C=176 D=34736 target=3270
01302 [L1540] TGETS    A=4 B=1 C=2 D=258 'id'
01303 [L1540] GGET     A=5 B=1 C=9 D=265 'e_t'
01304 [L1540] KSTR     A=6 B=1 C=10 D=266 'spirit_pray'
01305 [L1540] TGETV    A=5 B=5 C=6 D=1286 
01306 [L1540] ISNEV    A=4 B=0 C=5 D=5 
01307 [L1540] JMP      A=4 B=128 C=8 D=32776 target=1316
01308 [L1542] GGET     A=4 B=0 C=4 D=4 'd_ms'
01309 [L1542] KSTR     A=5 B=1 C=11 D=267 'd_qiFuUI'
01310 [L1542] TGETV    A=4 B=4 C=5 D=1029 
01311 [L1542] KSTR     A=5 B=1 C=12 D=268 'getQiFuResult'
01312 [L1542] TGETV    A=4 B=4 C=5 D=1029 
01313 [L1542] MOV      A=5 B=0 C=3 D=3 
01314 [L1542] CALL     A=4 B=1 C=2 D=258 
01315 [L1542] JMP      A=4 B=135 C=162 D=34722 target=3270
01316 [L1543] TGETS    A=4 B=1 C=2 D=258 'id'
01317 [L1543] GGET     A=5 B=1 C=9 D=265 'e_t'
01318 [L1543] KSTR     A=6 B=1 C=13 D=269 'flush_tollgate'
01319 [L1543] TGETV    A=5 B=5 C=6 D=1286 
01320 [L1543] ISNEV    A=4 B=0 C=5 D=5 
01321 [L1543] JMP      A=4 B=128 C=8 D=32776 target=1330
01322 [L1544] GGET     A=4 B=0 C=4 D=4 'd_ms'
01323 [L1544] KSTR     A=5 B=1 C=14 D=270 'd_subLevelUI'
01324 [L1544] TGETV    A=4 B=4 C=5 D=1029 
01325 [L1544] KSTR     A=5 B=1 C=15 D=271 'getRefleshRes'
01326 [L1544] TGETV    A=4 B=4 C=5 D=1029 
01327 [L1544] MOV      A=5 B=0 C=3 D=3 
01328 [L1544] CALL     A=4 B=1 C=2 D=258 
01329 [L1544] JMP      A=4 B=135 C=148 D=34708 target=3270
01330 [L1546] TGETS    A=4 B=1 C=2 D=258 'id'
01331 [L1546] GGET     A=5 B=1 C=9 D=265 'e_t'
01332 [L1546] KSTR     A=6 B=1 C=16 D=272 'task_prize'
01333 [L1546] TGETV    A=5 B=5 C=6 D=1286 
01334 [L1546] ISNEV    A=4 B=0 C=5 D=5 
01335 [L1546] JMP      A=4 B=128 C=8 D=32776 target=1344
01336 [L1547] GGET     A=4 B=0 C=4 D=4 'd_ms'
01337 [L1547] KSTR     A=5 B=1 C=17 D=273 'd_tianShuUI'
01338 [L1547] TGETV    A=4 B=4 C=5 D=1029 
01339 [L1547] KSTR     A=5 B=1 C=18 D=274 'getTaskPrizeRes'
01340 [L1547] TGETV    A=4 B=4 C=5 D=1029 
01341 [L1547] MOV      A=5 B=0 C=3 D=3 
01342 [L1547] CALL     A=4 B=1 C=2 D=258 
01343 [L1547] JMP      A=4 B=135 C=134 D=34694 target=3270
01344 [L1549] TGETS    A=4 B=1 C=2 D=258 'id'
01345 [L1549] GGET     A=5 B=0 C=4 D=4 'd_ms'
01346 [L1549] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01347 [L1549] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01348 [L1549] KSTR     A=6 B=1 C=19 D=275 'first_charge_gift'
01349 [L1549] TGETV    A=5 B=5 C=6 D=1286 
01350 [L1549] ISNEV    A=4 B=0 C=5 D=5 
01351 [L1549] JMP      A=4 B=128 C=22 D=32790 target=1374
01352 [L1550] GGET     A=4 B=0 C=4 D=4 'd_ms'
01353 [L1550] KSTR     A=5 B=1 C=20 D=276 'd_rechargeUI'
01354 [L1550] TGETV    A=4 B=4 C=5 D=1029 
01355 [L1550] KSTR     A=5 B=1 C=21 D=277 'onReceiveGiftResult'
01356 [L1550] TGETV    A=4 B=4 C=5 D=1029 
01357 [L1550] MOV      A=5 B=0 C=3 D=3 
01358 [L1550] CALL     A=4 B=1 C=2 D=258 
01359 [L1551] GGET     A=4 B=0 C=4 D=4 'd_ms'
01360 [L1551] KSTR     A=5 B=1 C=22 D=278 'd_firstChargeUI'
01361 [L1551] TGETV    A=4 B=4 C=5 D=1029 
01362 [L1551] KSTR     A=5 B=1 C=21 D=277 'onReceiveGiftResult'
01363 [L1551] TGETV    A=4 B=4 C=5 D=1029 
01364 [L1551] MOV      A=5 B=0 C=3 D=3 
01365 [L1551] CALL     A=4 B=1 C=2 D=258 
01366 [L1552] GGET     A=4 B=0 C=4 D=4 'd_ms'
01367 [L1552] KSTR     A=5 B=1 C=23 D=279 'd_actNoticeUI'
01368 [L1552] TGETV    A=4 B=4 C=5 D=1029 
01369 [L1552] KSTR     A=5 B=1 C=21 D=277 'onReceiveGiftResult'
01370 [L1552] TGETV    A=4 B=4 C=5 D=1029 
01371 [L1552] MOV      A=5 B=0 C=3 D=3 
01372 [L1552] CALL     A=4 B=1 C=2 D=258 
01373 [L1552] JMP      A=4 B=135 C=104 D=34664 target=3270
01374 [L1553] TGETS    A=4 B=1 C=2 D=258 'id'
01375 [L1553] GGET     A=5 B=1 C=9 D=265 'e_t'
01376 [L1553] KSTR     A=6 B=1 C=24 D=280 'tollgate_sweep_update'
01377 [L1553] TGETV    A=5 B=5 C=6 D=1286 
01378 [L1553] ISNEV    A=4 B=0 C=5 D=5 
01379 [L1553] JMP      A=4 B=128 C=8 D=32776 target=1388
01380 [L1554] GGET     A=4 B=0 C=4 D=4 'd_ms'
01381 [L1554] KSTR     A=5 B=1 C=0 D=256 'd_saodangUI'
01382 [L1554] TGETV    A=4 B=4 C=5 D=1029 
01383 [L1554] KSTR     A=5 B=1 C=25 D=281 'getMassacreResult'
01384 [L1554] TGETV    A=4 B=4 C=5 D=1029 
01385 [L1554] MOV      A=5 B=0 C=3 D=3 
01386 [L1554] CALL     A=4 B=1 C=2 D=258 
01387 [L1554] JMP      A=4 B=135 C=90 D=34650 target=3270
01388 [L1555] TGETS    A=4 B=1 C=2 D=258 'id'
01389 [L1555] GGET     A=5 B=0 C=4 D=4 'd_ms'
01390 [L1555] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01391 [L1555] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01392 [L1555] KSTR     A=6 B=1 C=26 D=282 'convert_output'
01393 [L1555] TGETV    A=5 B=5 C=6 D=1286 
01394 [L1555] ISNEV    A=4 B=0 C=5 D=5 
01395 [L1555] JMP      A=4 B=128 C=8 D=32776 target=1404
01396 [L1556] GGET     A=4 B=0 C=4 D=4 'd_ms'
01397 [L1556] KSTR     A=5 B=1 C=27 D=283 'd_cortCallUI'
01398 [L1556] TGETV    A=4 B=4 C=5 D=1029 
01399 [L1556] KSTR     A=5 B=1 C=28 D=284 'callbackOutput'
01400 [L1556] TGETV    A=4 B=4 C=5 D=1029 
01401 [L1556] MOV      A=5 B=0 C=3 D=3 
01402 [L1556] CALL     A=4 B=1 C=2 D=258 
01403 [L1556] JMP      A=4 B=135 C=74 D=34634 target=3270
01404 [L1557] TGETS    A=4 B=1 C=2 D=258 'id'
01405 [L1557] GGET     A=5 B=0 C=4 D=4 'd_ms'
01406 [L1557] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01407 [L1557] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01408 [L1557] KSTR     A=6 B=1 C=29 D=285 'create_invite_code'
01409 [L1557] TGETV    A=5 B=5 C=6 D=1286 
01410 [L1557] ISNEV    A=4 B=0 C=5 D=5 
01411 [L1557] JMP      A=4 B=128 C=8 D=32776 target=1420
01412 [L1558] GGET     A=4 B=0 C=4 D=4 'd_ms'
01413 [L1558] KSTR     A=5 B=1 C=30 D=286 'd_friendsUI'
01414 [L1558] TGETV    A=4 B=4 C=5 D=1029 
01415 [L1558] KSTR     A=5 B=1 C=31 D=287 'callbackCreateFriendCode'
01416 [L1558] TGETV    A=4 B=4 C=5 D=1029 
01417 [L1558] MOV      A=5 B=0 C=3 D=3 
01418 [L1558] CALL     A=4 B=1 C=2 D=258 
01419 [L1558] JMP      A=4 B=135 C=58 D=34618 target=3270
01420 [L1559] TGETS    A=4 B=1 C=2 D=258 'id'
01421 [L1559] GGET     A=5 B=0 C=4 D=4 'd_ms'
01422 [L1559] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01423 [L1559] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01424 [L1559] KSTR     A=6 B=1 C=32 D=288 'activate_invite_code'
01425 [L1559] TGETV    A=5 B=5 C=6 D=1286 
01426 [L1559] ISNEV    A=4 B=0 C=5 D=5 
01427 [L1559] JMP      A=4 B=128 C=7 D=32775 target=1435
01428 [L1560] GGET     A=4 B=0 C=4 D=4 'd_ms'
01429 [L1560] TGETS    A=4 B=4 C=77 D=1101 'd_systemSetUI'
01430 [L1560] KSTR     A=5 B=1 C=33 D=289 'callbackFriendCode'
01431 [L1560] TGETV    A=4 B=4 C=5 D=1029 
01432 [L1560] MOV      A=5 B=0 C=3 D=3 
01433 [L1560] CALL     A=4 B=1 C=2 D=258 
01434 [L1560] JMP      A=4 B=135 C=43 D=34603 target=3270
01435 [L1561] TGETS    A=4 B=1 C=2 D=258 'id'
01436 [L1561] GGET     A=5 B=1 C=9 D=265 'e_t'
01437 [L1561] KSTR     A=6 B=1 C=34 D=290 'activate_account'
01438 [L1561] TGETV    A=5 B=5 C=6 D=1286 
01439 [L1561] ISNEV    A=4 B=0 C=5 D=5 
01440 [L1561] JMP      A=4 B=128 C=8 D=32776 target=1449
01441 [L1562] GGET     A=4 B=0 C=4 D=4 'd_ms'
01442 [L1562] KSTR     A=5 B=1 C=35 D=291 'd_playerCenterUI'
01443 [L1562] TGETV    A=4 B=4 C=5 D=1029 
01444 [L1562] KSTR     A=5 B=1 C=36 D=292 'getActivateRes'
01445 [L1562] TGETV    A=4 B=4 C=5 D=1029 
01446 [L1562] MOV      A=5 B=0 C=3 D=3 
01447 [L1562] CALL     A=4 B=1 C=2 D=258 
01448 [L1562] JMP      A=4 B=135 C=29 D=34589 target=3270
01449 [L1563] TGETS    A=4 B=1 C=2 D=258 'id'
01450 [L1563] GGET     A=5 B=1 C=9 D=265 'e_t'
01451 [L1563] KSTR     A=6 B=1 C=37 D=293 'register_account'
01452 [L1563] TGETV    A=5 B=5 C=6 D=1286 
01453 [L1563] ISNEV    A=4 B=0 C=5 D=5 
01454 [L1563] JMP      A=4 B=128 C=8 D=32776 target=1463
01455 [L1564] GGET     A=4 B=0 C=4 D=4 'd_ms'
01456 [L1564] KSTR     A=5 B=1 C=35 D=291 'd_playerCenterUI'
01457 [L1564] TGETV    A=4 B=4 C=5 D=1029 
01458 [L1564] KSTR     A=5 B=1 C=38 D=294 'getRegisterRes'
01459 [L1564] TGETV    A=4 B=4 C=5 D=1029 
01460 [L1564] MOV      A=5 B=0 C=3 D=3 
01461 [L1564] CALL     A=4 B=1 C=2 D=258 
01462 [L1564] JMP      A=4 B=135 C=15 D=34575 target=3270
01463 [L1565] TGETS    A=4 B=1 C=2 D=258 'id'
01464 [L1565] GGET     A=5 B=1 C=9 D=265 'e_t'
01465 [L1565] KSTR     A=6 B=1 C=39 D=295 'modify_password'
01466 [L1565] TGETV    A=5 B=5 C=6 D=1286 
01467 [L1565] ISNEV    A=4 B=0 C=5 D=5 
01468 [L1565] JMP      A=4 B=128 C=8 D=32776 target=1477
01469 [L1566] GGET     A=4 B=0 C=4 D=4 'd_ms'
01470 [L1566] KSTR     A=5 B=1 C=35 D=291 'd_playerCenterUI'
01471 [L1566] TGETV    A=4 B=4 C=5 D=1029 
01472 [L1566] KSTR     A=5 B=1 C=40 D=296 'getModifyPWDRes'
01473 [L1566] TGETV    A=4 B=4 C=5 D=1029 
01474 [L1566] MOV      A=5 B=0 C=3 D=3 
01475 [L1566] CALL     A=4 B=1 C=2 D=258 
01476 [L1566] JMP      A=4 B=135 C=1 D=34561 target=3270
01477 [L1567] TGETS    A=4 B=1 C=2 D=258 'id'
01478 [L1567] GGET     A=5 B=1 C=9 D=265 'e_t'
01479 [L1567] KSTR     A=6 B=1 C=41 D=297 'register_real'
01480 [L1567] TGETV    A=5 B=5 C=6 D=1286 
01481 [L1567] ISNEV    A=4 B=0 C=5 D=5 
01482 [L1567] JMP      A=4 B=128 C=8 D=32776 target=1491
01483 [L1568] GGET     A=4 B=0 C=4 D=4 'd_ms'
01484 [L1568] KSTR     A=5 B=1 C=35 D=291 'd_playerCenterUI'
01485 [L1568] TGETV    A=4 B=4 C=5 D=1029 
01486 [L1568] KSTR     A=5 B=1 C=42 D=298 'getRegisterInfoRes'
01487 [L1568] TGETV    A=4 B=4 C=5 D=1029 
01488 [L1568] MOV      A=5 B=0 C=3 D=3 
01489 [L1568] CALL     A=4 B=1 C=2 D=258 
01490 [L1568] JMP      A=4 B=134 C=243 D=34547 target=3270
01491 [L1569] TGETS    A=4 B=1 C=2 D=258 'id'
01492 [L1569] GGET     A=5 B=1 C=9 D=265 'e_t'
01493 [L1569] KSTR     A=6 B=1 C=43 D=299 'train_boss'
01494 [L1569] TGETV    A=5 B=5 C=6 D=1286 
01495 [L1569] ISNEV    A=4 B=0 C=5 D=5 
01496 [L1569] JMP      A=4 B=128 C=8 D=32776 target=1505
01497 [L1570] GGET     A=4 B=0 C=4 D=4 'd_ms'
01498 [L1570] KSTR     A=5 B=1 C=44 D=300 'd_shilianUI'
01499 [L1570] TGETV    A=4 B=4 C=5 D=1029 
01500 [L1570] KSTR     A=5 B=1 C=45 D=301 'processStatus'
01501 [L1570] TGETV    A=4 B=4 C=5 D=1029 
01502 [L1570] MOV      A=5 B=0 C=3 D=3 
01503 [L1570] CALL     A=4 B=1 C=2 D=258 
01504 [L1570] JMP      A=4 B=134 C=229 D=34533 target=3270
01505 [L1572] TGETS    A=4 B=1 C=2 D=258 'id'
01506 [L1572] GGET     A=5 B=0 C=4 D=4 'd_ms'
01507 [L1572] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01508 [L1572] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01509 [L1572] KSTR     A=6 B=1 C=46 D=302 'consume_fairy_roll'
01510 [L1572] TGETV    A=5 B=5 C=6 D=1286 
01511 [L1572] ISNEV    A=4 B=0 C=5 D=5 
01512 [L1572] JMP      A=4 B=128 C=8 D=32776 target=1521
01513 [L1573] GGET     A=4 B=0 C=4 D=4 'd_ms'
01514 [L1573] KSTR     A=5 B=1 C=47 D=303 'd_expbookUI'
01515 [L1573] TGETV    A=4 B=4 C=5 D=1029 
01516 [L1573] KSTR     A=5 B=1 C=48 D=304 'onGetExpResult'
01517 [L1573] TGETV    A=4 B=4 C=5 D=1029 
01518 [L1573] MOV      A=5 B=0 C=3 D=3 
01519 [L1573] CALL     A=4 B=1 C=2 D=258 
01520 [L1573] JMP      A=4 B=134 C=213 D=34517 target=3270
01521 [L1575] TGETS    A=4 B=1 C=2 D=258 'id'
01522 [L1575] GGET     A=5 B=0 C=4 D=4 'd_ms'
01523 [L1575] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01524 [L1575] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01525 [L1575] KSTR     A=6 B=1 C=49 D=305 'take_monthcard_gold'
01526 [L1575] TGETV    A=5 B=5 C=6 D=1286 
01527 [L1575] ISNEV    A=4 B=0 C=5 D=5 
01528 [L1575] JMP      A=4 B=128 C=8 D=32776 target=1537
01529 [L1576] GGET     A=4 B=0 C=4 D=4 'd_ms'
01530 [L1576] KSTR     A=5 B=1 C=50 D=306 'd_monthCardUI'
01531 [L1576] TGETV    A=4 B=4 C=5 D=1029 
01532 [L1576] KSTR     A=5 B=1 C=51 D=307 'callbackGetTodayGold'
01533 [L1576] TGETV    A=4 B=4 C=5 D=1029 
01534 [L1576] MOV      A=5 B=0 C=3 D=3 
01535 [L1576] CALL     A=4 B=1 C=2 D=258 
01536 [L1576] JMP      A=4 B=134 C=197 D=34501 target=3270
01537 [L1577] TGETS    A=4 B=1 C=2 D=258 'id'
01538 [L1577] GGET     A=5 B=0 C=4 D=4 'd_ms'
01539 [L1577] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01540 [L1577] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01541 [L1577] KSTR     A=6 B=1 C=52 D=308 'take_online_prize'
01542 [L1577] TGETV    A=5 B=5 C=6 D=1286 
01543 [L1577] ISNEV    A=4 B=0 C=5 D=5 
01544 [L1577] JMP      A=4 B=128 C=8 D=32776 target=1553
01545 [L1578] GGET     A=4 B=0 C=4 D=4 'd_ms'
01546 [L1578] KSTR     A=5 B=1 C=53 D=309 'd_rotUI'
01547 [L1578] TGETV    A=4 B=4 C=5 D=1029 
01548 [L1578] KSTR     A=5 B=1 C=21 D=277 'onReceiveGiftResult'
01549 [L1578] TGETV    A=4 B=4 C=5 D=1029 
01550 [L1578] MOV      A=5 B=0 C=3 D=3 
01551 [L1578] CALL     A=4 B=1 C=2 D=258 
01552 [L1578] JMP      A=4 B=134 C=181 D=34485 target=3270
01553 [L1579] TGETS    A=4 B=1 C=2 D=258 'id'
01554 [L1579] GGET     A=5 B=0 C=4 D=4 'd_ms'
01555 [L1579] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01556 [L1579] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01557 [L1579] KSTR     A=6 B=1 C=54 D=310 'rape_back_result'
01558 [L1579] TGETV    A=5 B=5 C=6 D=1286 
01559 [L1579] ISNEV    A=4 B=0 C=5 D=5 
01560 [L1579] JMP      A=4 B=128 C=7 D=32775 target=1568
01561 [L1580] GGET     A=4 B=0 C=4 D=4 'd_ms'
01562 [L1580] TGETS    A=4 B=4 C=36 D=1060 'd_crossDoomUI'
01563 [L1580] KSTR     A=5 B=1 C=55 D=311 'callbackShowFightBackRet'
01564 [L1580] TGETV    A=4 B=4 C=5 D=1029 
01565 [L1580] MOV      A=5 B=0 C=3 D=3 
01566 [L1580] CALL     A=4 B=1 C=2 D=258 
01567 [L1580] JMP      A=4 B=134 C=166 D=34470 target=3270
01568 [L1581] TGETS    A=4 B=1 C=2 D=258 'id'
01569 [L1581] GGET     A=5 B=0 C=4 D=4 'd_ms'
01570 [L1581] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01571 [L1581] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01572 [L1581] KSTR     A=6 B=1 C=56 D=312 'rape_back_list'
01573 [L1581] TGETV    A=5 B=5 C=6 D=1286 
01574 [L1581] ISNEV    A=4 B=0 C=5 D=5 
01575 [L1581] JMP      A=4 B=128 C=7 D=32775 target=1583
01576 [L1582] GGET     A=4 B=0 C=4 D=4 'd_ms'
01577 [L1582] TGETS    A=4 B=4 C=56 D=1080 'd_messageUI'
01578 [L1582] KSTR     A=5 B=1 C=57 D=313 'callback_rape_back_list'
01579 [L1582] TGETV    A=4 B=4 C=5 D=1029 
01580 [L1582] MOV      A=5 B=0 C=3 D=3 
01581 [L1582] CALL     A=4 B=1 C=2 D=258 
01582 [L1582] JMP      A=4 B=134 C=151 D=34455 target=3270
01583 [L1583] TGETS    A=4 B=1 C=2 D=258 'id'
01584 [L1583] GGET     A=5 B=0 C=4 D=4 'd_ms'
01585 [L1583] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01586 [L1583] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01587 [L1583] KSTR     A=6 B=1 C=58 D=314 'skip_rape_back'
01588 [L1583] TGETV    A=5 B=5 C=6 D=1286 
01589 [L1583] ISNEV    A=4 B=0 C=5 D=5 
01590 [L1583] JMP      A=4 B=128 C=7 D=32775 target=1598
01591 [L1584] GGET     A=4 B=0 C=4 D=4 'd_ms'
01592 [L1584] TGETS    A=4 B=4 C=56 D=1080 'd_messageUI'
01593 [L1584] KSTR     A=5 B=1 C=59 D=315 'callback_skip_rape_back'
01594 [L1584] TGETV    A=4 B=4 C=5 D=1029 
01595 [L1584] MOV      A=5 B=0 C=3 D=3 
01596 [L1584] CALL     A=4 B=1 C=2 D=258 
01597 [L1584] JMP      A=4 B=134 C=136 D=34440 target=3270
01598 [L1586] TGETS    A=4 B=1 C=2 D=258 'id'
01599 [L1586] GGET     A=5 B=0 C=4 D=4 'd_ms'
01600 [L1586] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01601 [L1586] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01602 [L1586] KSTR     A=6 B=1 C=60 D=316 'upgrade_ext_skill_result'
01603 [L1586] TGETV    A=5 B=5 C=6 D=1286 
01604 [L1586] ISNEV    A=4 B=0 C=5 D=5 
01605 [L1586] JMP      A=4 B=128 C=8 D=32776 target=1614
01606 [L1587] GGET     A=4 B=0 C=4 D=4 'd_ms'
01607 [L1587] KSTR     A=5 B=1 C=61 D=317 'd_jpmkUI'
01608 [L1587] TGETV    A=4 B=4 C=5 D=1029 
01609 [L1587] KSTR     A=5 B=1 C=62 D=318 'callback_update_jp_req'
01610 [L1587] TGETV    A=4 B=4 C=5 D=1029 
01611 [L1587] MOV      A=5 B=0 C=3 D=3 
01612 [L1587] CALL     A=4 B=1 C=2 D=258 
01613 [L1587] JMP      A=4 B=134 C=120 D=34424 target=3270
01614 [L1588] TGETS    A=4 B=1 C=2 D=258 'id'
01615 [L1588] GGET     A=5 B=0 C=4 D=4 'd_ms'
01616 [L1588] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01617 [L1588] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01618 [L1588] KSTR     A=6 B=1 C=63 D=319 'equip_ext_skill_result'
01619 [L1588] TGETV    A=5 B=5 C=6 D=1286 
01620 [L1588] ISNEV    A=4 B=0 C=5 D=5 
01621 [L1588] JMP      A=4 B=128 C=8 D=32776 target=1630
01622 [L1589] GGET     A=4 B=0 C=4 D=4 'd_ms'
01623 [L1589] KSTR     A=5 B=1 C=61 D=317 'd_jpmkUI'
01624 [L1589] TGETV    A=4 B=4 C=5 D=1029 
01625 [L1589] KSTR     A=5 B=1 C=64 D=320 'callback_change_jp_req'
01626 [L1589] TGETV    A=4 B=4 C=5 D=1029 
01627 [L1589] MOV      A=5 B=0 C=3 D=3 
01628 [L1589] CALL     A=4 B=1 C=2 D=258 
01629 [L1589] JMP      A=4 B=134 C=104 D=34408 target=3270
01630 [L1590] TGETS    A=4 B=1 C=2 D=258 'id'
01631 [L1590] GGET     A=5 B=0 C=4 D=4 'd_ms'
01632 [L1590] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01633 [L1590] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01634 [L1590] KSTR     A=6 B=1 C=65 D=321 'change_ext_skill_owner'
01635 [L1590] TGETV    A=5 B=5 C=6 D=1286 
01636 [L1590] ISNEV    A=4 B=0 C=5 D=5 
01637 [L1590] JMP      A=4 B=128 C=7 D=32775 target=1645
01638 [L1591] GGET     A=4 B=0 C=4 D=4 'd_ms'
01639 [L1591] TGETS    A=4 B=4 C=13 D=1037 'd_lineupUI'
01640 [L1591] KSTR     A=5 B=1 C=66 D=322 'updateItemInfoOwnerId'
01641 [L1591] TGETV    A=4 B=4 C=5 D=1029 
01642 [L1591] MOV      A=5 B=0 C=3 D=3 
01643 [L1591] CALL     A=4 B=1 C=2 D=258 
01644 [L1591] JMP      A=4 B=134 C=89 D=34393 target=3270
01645 [L1593] TGETS    A=4 B=1 C=2 D=258 'id'
01646 [L1593] GGET     A=5 B=0 C=4 D=4 'd_ms'
01647 [L1593] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01648 [L1593] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01649 [L1593] KSTR     A=6 B=1 C=67 D=323 'change_genius'
01650 [L1593] TGETV    A=5 B=5 C=6 D=1286 
01651 [L1593] ISNEV    A=4 B=0 C=5 D=5 
01652 [L1593] JMP      A=4 B=128 C=7 D=32775 target=1660
01653 [L1594] GGET     A=4 B=0 C=4 D=4 'd_ms'
01654 [L1594] TGETS    A=4 B=4 C=111 D=1135 'd_runeUI'
01655 [L1594] KSTR     A=5 B=1 C=68 D=324 'callback_change_genius'
01656 [L1594] TGETV    A=4 B=4 C=5 D=1029 
01657 [L1594] MOV      A=5 B=0 C=3 D=3 
01658 [L1594] CALL     A=4 B=1 C=2 D=258 
01659 [L1594] JMP      A=4 B=134 C=74 D=34378 target=3270
01660 [L1595] TGETS    A=4 B=1 C=2 D=258 'id'
01661 [L1595] GGET     A=5 B=0 C=4 D=4 'd_ms'
01662 [L1595] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01663 [L1595] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01664 [L1595] KSTR     A=6 B=1 C=69 D=325 'lantern_activity'
01665 [L1595] TGETV    A=5 B=5 C=6 D=1286 
01666 [L1595] ISNEV    A=4 B=0 C=5 D=5 
01667 [L1595] JMP      A=4 B=128 C=7 D=32775 target=1675
01668 [L1596] GGET     A=4 B=0 C=4 D=4 'd_ms'
01669 [L1596] KSTR     A=5 B=1 C=70 D=326 'd_lanternRiddleUI'
01670 [L1596] TGETV    A=4 B=4 C=5 D=1029 
01671 [L1596] TGETS    A=4 B=4 C=230 D=1254 'getResFromServer'
01672 [L1596] MOV      A=5 B=0 C=3 D=3 
01673 [L1596] CALL     A=4 B=1 C=2 D=258 
01674 [L1596] JMP      A=4 B=134 C=59 D=34363 target=3270
01675 [L1597] TGETS    A=4 B=1 C=2 D=258 'id'
01676 [L1597] GGET     A=5 B=0 C=4 D=4 'd_ms'
01677 [L1597] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01678 [L1597] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01679 [L1597] KSTR     A=6 B=1 C=71 D=327 'land_father'
01680 [L1597] TGETV    A=5 B=5 C=6 D=1286 
01681 [L1597] ISNEV    A=4 B=0 C=5 D=5 
01682 [L1597] JMP      A=4 B=128 C=6 D=32774 target=1689
01683 [L1598] GGET     A=4 B=0 C=4 D=4 'd_ms'
01684 [L1598] TGETS    A=4 B=4 C=103 D=1127 'd_godBlessUI'
01685 [L1598] TGETS    A=4 B=4 C=230 D=1254 'getResFromServer'
01686 [L1598] MOV      A=5 B=0 C=3 D=3 
01687 [L1598] CALL     A=4 B=1 C=2 D=258 
01688 [L1598] JMP      A=4 B=134 C=45 D=34349 target=3270
01689 [L1599] TGETS    A=4 B=1 C=2 D=258 'id'
01690 [L1599] GGET     A=5 B=0 C=4 D=4 'd_ms'
01691 [L1599] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01692 [L1599] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01693 [L1599] KSTR     A=6 B=1 C=72 D=328 'single_match_info'
01694 [L1599] TGETV    A=5 B=5 C=6 D=1286 
01695 [L1599] ISNEV    A=4 B=0 C=5 D=5 
01696 [L1599] JMP      A=4 B=128 C=7 D=32775 target=1704
01697 [L1600] GGET     A=4 B=0 C=4 D=4 'd_ms'
01698 [L1600] KSTR     A=5 B=1 C=73 D=329 'd_crossRankUI'
01699 [L1600] TGETV    A=4 B=4 C=5 D=1029 
01700 [L1600] TGETS    A=4 B=4 C=230 D=1254 'getResFromServer'
01701 [L1600] MOV      A=5 B=0 C=3 D=3 
01702 [L1600] CALL     A=4 B=1 C=2 D=258 
01703 [L1600] JMP      A=4 B=134 C=30 D=34334 target=3270
01704 [L1601] TGETS    A=4 B=1 C=2 D=258 'id'
01705 [L1601] GGET     A=5 B=0 C=4 D=4 'd_ms'
01706 [L1601] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01707 [L1601] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01708 [L1601] KSTR     A=6 B=1 C=74 D=330 'single_lineup_info'
01709 [L1601] TGETV    A=5 B=5 C=6 D=1286 
01710 [L1601] ISNEV    A=4 B=0 C=5 D=5 
01711 [L1601] JMP      A=4 B=128 C=8 D=32776 target=1720
01712 [L1602] GGET     A=4 B=0 C=4 D=4 'd_ms'
01713 [L1602] KSTR     A=5 B=1 C=73 D=329 'd_crossRankUI'
01714 [L1602] TGETV    A=4 B=4 C=5 D=1029 
01715 [L1602] KSTR     A=5 B=1 C=75 D=331 'getLineupResFromServer'
01716 [L1602] TGETV    A=4 B=4 C=5 D=1029 
01717 [L1602] MOV      A=5 B=0 C=3 D=3 
01718 [L1602] CALL     A=4 B=1 C=2 D=258 
01719 [L1602] JMP      A=4 B=134 C=14 D=34318 target=3270
01720 [L1603] TGETS    A=4 B=1 C=2 D=258 'id'
01721 [L1603] GGET     A=5 B=0 C=4 D=4 'd_ms'
01722 [L1603] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01723 [L1603] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01724 [L1603] KSTR     A=6 B=1 C=76 D=332 'single_flush_reponse'
01725 [L1603] TGETV    A=5 B=5 C=6 D=1286 
01726 [L1603] ISNEV    A=4 B=0 C=5 D=5 
01727 [L1603] JMP      A=4 B=128 C=8 D=32776 target=1736
01728 [L1604] GGET     A=4 B=0 C=4 D=4 'd_ms'
01729 [L1604] KSTR     A=5 B=1 C=73 D=329 'd_crossRankUI'
01730 [L1604] TGETV    A=4 B=4 C=5 D=1029 
01731 [L1604] KSTR     A=5 B=1 C=77 D=333 'getFreshResFromServer'
01732 [L1604] TGETV    A=4 B=4 C=5 D=1029 
01733 [L1604] MOV      A=5 B=0 C=3 D=3 
01734 [L1604] CALL     A=4 B=1 C=2 D=258 
01735 [L1604] JMP      A=4 B=133 C=254 D=34302 target=3270
01736 [L1605] TGETS    A=4 B=1 C=2 D=258 'id'
01737 [L1605] GGET     A=5 B=0 C=4 D=4 'd_ms'
01738 [L1605] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01739 [L1605] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01740 [L1605] KSTR     A=6 B=1 C=78 D=334 'single_win_prize_reponse'
01741 [L1605] TGETV    A=5 B=5 C=6 D=1286 
01742 [L1605] ISNEV    A=4 B=0 C=5 D=5 
01743 [L1605] JMP      A=4 B=128 C=8 D=32776 target=1752
01744 [L1606] GGET     A=4 B=0 C=4 D=4 'd_ms'
01745 [L1606] KSTR     A=5 B=1 C=73 D=329 'd_crossRankUI'
01746 [L1606] TGETV    A=4 B=4 C=5 D=1029 
01747 [L1606] KSTR     A=5 B=1 C=79 D=335 'getRewardResFromServer'
01748 [L1606] TGETV    A=4 B=4 C=5 D=1029 
01749 [L1606] MOV      A=5 B=0 C=3 D=3 
01750 [L1606] CALL     A=4 B=1 C=2 D=258 
01751 [L1606] JMP      A=4 B=133 C=238 D=34286 target=3270
01752 [L1607] TGETS    A=4 B=1 C=2 D=258 'id'
01753 [L1607] GGET     A=5 B=0 C=4 D=4 'd_ms'
01754 [L1607] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01755 [L1607] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01756 [L1607] KSTR     A=6 B=1 C=80 D=336 'single_query_prize_response'
01757 [L1607] TGETV    A=5 B=5 C=6 D=1286 
01758 [L1607] ISNEV    A=4 B=0 C=5 D=5 
01759 [L1607] JMP      A=4 B=128 C=8 D=32776 target=1768
01760 [L1608] GGET     A=4 B=0 C=4 D=4 'd_ms'
01761 [L1608] KSTR     A=5 B=1 C=73 D=329 'd_crossRankUI'
01762 [L1608] TGETV    A=4 B=4 C=5 D=1029 
01763 [L1608] KSTR     A=5 B=1 C=81 D=337 'getRewardInfoResFromServer'
01764 [L1608] TGETV    A=4 B=4 C=5 D=1029 
01765 [L1608] MOV      A=5 B=0 C=3 D=3 
01766 [L1608] CALL     A=4 B=1 C=2 D=258 
01767 [L1608] JMP      A=4 B=133 C=222 D=34270 target=3270
01768 [L1609] TGETS    A=4 B=1 C=2 D=258 'id'
01769 [L1609] GGET     A=5 B=0 C=4 D=4 'd_ms'
01770 [L1609] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01771 [L1609] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01772 [L1609] KSTR     A=6 B=1 C=82 D=338 'single_fight_prize'
01773 [L1609] TGETV    A=5 B=5 C=6 D=1286 
01774 [L1609] ISNEV    A=4 B=0 C=5 D=5 
01775 [L1609] JMP      A=4 B=128 C=8 D=32776 target=1784
01776 [L1610] GGET     A=4 B=0 C=4 D=4 'd_ms'
01777 [L1610] KSTR     A=5 B=1 C=73 D=329 'd_crossRankUI'
01778 [L1610] TGETV    A=4 B=4 C=5 D=1029 
01779 [L1610] KSTR     A=5 B=1 C=83 D=339 'getFightPrizeResFromServer'
01780 [L1610] TGETV    A=4 B=4 C=5 D=1029 
01781 [L1610] MOV      A=5 B=0 C=3 D=3 
01782 [L1610] CALL     A=4 B=1 C=2 D=258 
01783 [L1610] JMP      A=4 B=133 C=206 D=34254 target=3270
01784 [L1611] TGETS    A=4 B=1 C=2 D=258 'id'
01785 [L1611] GGET     A=5 B=0 C=4 D=4 'd_ms'
01786 [L1611] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01787 [L1611] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01788 [L1611] KSTR     A=6 B=1 C=84 D=340 'single_rank_prize_response'
01789 [L1611] TGETV    A=5 B=5 C=6 D=1286 
01790 [L1611] ISNEV    A=4 B=0 C=5 D=5 
01791 [L1611] JMP      A=4 B=128 C=8 D=32776 target=1800
01792 [L1612] GGET     A=4 B=0 C=4 D=4 'd_ms'
01793 [L1612] KSTR     A=5 B=1 C=73 D=329 'd_crossRankUI'
01794 [L1612] TGETV    A=4 B=4 C=5 D=1029 
01795 [L1612] KSTR     A=5 B=1 C=85 D=341 'onGetRankPrizeFromServer'
01796 [L1612] TGETV    A=4 B=4 C=5 D=1029 
01797 [L1612] MOV      A=5 B=0 C=3 D=3 
01798 [L1612] CALL     A=4 B=1 C=2 D=258 
01799 [L1612] JMP      A=4 B=133 C=190 D=34238 target=3270
01800 [L1613] TGETS    A=4 B=1 C=2 D=258 'id'
01801 [L1613] GGET     A=5 B=0 C=4 D=4 'd_ms'
01802 [L1613] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01803 [L1613] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01804 [L1613] KSTR     A=6 B=1 C=86 D=342 'query_singlerank_prize_response'
01805 [L1613] TGETV    A=5 B=5 C=6 D=1286 
01806 [L1613] ISNEV    A=4 B=0 C=5 D=5 
01807 [L1613] JMP      A=4 B=128 C=8 D=32776 target=1816
01808 [L1614] GGET     A=4 B=0 C=4 D=4 'd_ms'
01809 [L1614] KSTR     A=5 B=1 C=73 D=329 'd_crossRankUI'
01810 [L1614] TGETV    A=4 B=4 C=5 D=1029 
01811 [L1614] KSTR     A=5 B=1 C=87 D=343 'onGetRankPrizeStatus'
01812 [L1614] TGETV    A=4 B=4 C=5 D=1029 
01813 [L1614] MOV      A=5 B=0 C=3 D=3 
01814 [L1614] CALL     A=4 B=1 C=2 D=258 
01815 [L1614] JMP      A=4 B=133 C=174 D=34222 target=3270
01816 [L1615] TGETS    A=4 B=1 C=2 D=258 'id'
01817 [L1615] GGET     A=5 B=0 C=4 D=4 'd_ms'
01818 [L1615] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
01819 [L1615] TGETS    A=5 B=5 C=22 D=1302 'common_event_type'
01820 [L1615] KSTR     A=6 B=1 C=88 D=344 'fight_extra_logic'
01821 [L1615] TGETV    A=5 B=5 C=6 D=1286 
01822 [L1615] ISNEV    A=4 B=0 C=5 D=5 
01823 [L1615] JMP      A=4 B=128 C=4 D=32772 target=1828
01824 [L1616] GGET     A=4 B=1 C=89 D=345 'callback_fight_extra_logic'
01825 [L1616] MOV      A=5 B=0 C=3 D=3 
01826 [L1616] CALL     A=4 B=1 C=2 D=258 
01827 [L1616] JMP      A=4 B=133 C=162 D=34210 target=3270
01828 [L1617] TGETS    A=4 B=1 C=2 D=258 'id'
01829 [L1617] GGET     A=5 B=1 C=9 D=265 'e_t'
01830 [L1617] KSTR     A=6 B=1 C=90 D=346 'last_pick_data'
01831 [L1617] TGETV    A=5 B=5 C=6 D=1286 
01832 [L1617] ISNEV    A=4 B=0 C=5 D=5 
01833 [L1617] JMP      A=4 B=128 C=7 D=32775 target=1841
01834 [L1618] GGET     A=4 B=0 C=4 D=4 'd_ms'
01835 [L1618] TGETS    A=4 B=4 C=190 D=1214 'd_summonUI'
01836 [L1618] KSTR     A=5 B=1 C=91 D=347 'getLastSummonType'
01837 [L1618] TGETV    A=4 B=4 C=5 D=1029 
01838 [L1618] MOV      A=5 B=0 C=3 D=3 
01839 [L1618] CALL     A=4 B=1 C=2 D=258 
01840 [L1618] JMP      A=4 B=133 C=149 D=34197 target=3270
01841 [L1620] TGETS    A=4 B=1 C=2 D=258 'id'
01842 [L1620] GGET     A=5 B=1 C=9 D=265 'e_t'
01843 [L1620] KSTR     A=6 B=1 C=92 D=348 'update_config'
01844 [L1620] TGETV    A=5 B=5 C=6 D=1286 
01845 [L1620] ISNEV    A=4 B=0 C=5 D=5 
01846 [L1620] JMP      A=4 B=128 C=7 D=32775 target=1854
01847 [L1621] GGET     A=4 B=0 C=4 D=4 'd_ms'
01848 [L1621] TGETS    A=4 B=4 C=46 D=1070 'd_data'
01849 [L1621] KSTR     A=5 B=1 C=93 D=349 'callback_update_config'
01850 [L1621] TGETV    A=4 B=4 C=5 D=1029 
01851 [L1621] MOV      A=5 B=0 C=3 D=3 
01852 [L1621] CALL     A=4 B=1 C=2 D=258 
01853 [L1621] JMP      A=4 B=133 C=136 D=34184 target=3270
01854 [L1622] TGETS    A=4 B=1 C=2 D=258 'id'
01855 [L1622] GGET     A=5 B=1 C=9 D=265 'e_t'
01856 [L1622] KSTR     A=6 B=1 C=94 D=350 'order_prebuy_result'
01857 [L1622] TGETV    A=5 B=5 C=6 D=1286 
01858 [L1622] ISNEV    A=4 B=0 C=5 D=5 
01859 [L1622] JMP      A=4 B=128 C=8 D=32776 target=1868
01860 [L1623] GGET     A=4 B=0 C=4 D=4 'd_ms'
01861 [L1623] KSTR     A=5 B=1 C=50 D=306 'd_monthCardUI'
01862 [L1623] TGETV    A=4 B=4 C=5 D=1029 
01863 [L1623] KSTR     A=5 B=1 C=95 D=351 'callback_prebug_mc'
01864 [L1623] TGETV    A=4 B=4 C=5 D=1029 
01865 [L1623] MOV      A=5 B=0 C=3 D=3 
01866 [L1623] CALL     A=4 B=1 C=2 D=258 
01867 [L1623] JMP      A=4 B=133 C=122 D=34170 target=3270
01868 [L1624] TGETS    A=4 B=1 C=2 D=258 'id'
01869 [L1624] GGET     A=5 B=1 C=9 D=265 'e_t'
01870 [L1624] KSTR     A=6 B=1 C=96 D=352 'update_msg'
01871 [L1624] TGETV    A=5 B=5 C=6 D=1286 
01872 [L1624] ISNEV    A=4 B=0 C=5 D=5 
01873 [L1624] JMP      A=4 B=128 C=10 D=32778 target=1884
01874 [L1625] UGET     A=4 B=0 C=1 D=1 cclog
01875 [L1625] KSTR     A=5 B=1 C=97 D=353 '2998_9 msg, channel_type='
01876 [L1625] KSTR     A=6 B=1 C=98 D=354 'channel_type'
01877 [L1625] TGETV    A=6 B=3 C=6 D=774 
01878 [L1625] IST      A=0 B=0 C=6 D=6 
01879 [L1625] JMP      A=7 B=128 C=1 D=32769 target=1881
01880 [L1625] KSHORT   A=6 B=255 C=255 D=65535 -1
01881 [L1625] CAT      A=5 B=5 C=6 D=1286 
01882 [L1625] CALL     A=4 B=1 C=2 D=258 
01883 [L1625] JMP      A=4 B=133 C=106 D=34154 target=3270
01884 [L1626] TGETS    A=4 B=1 C=2 D=258 'id'
01885 [L1626] GGET     A=5 B=1 C=9 D=265 'e_t'
01886 [L1626] KSTR     A=6 B=1 C=99 D=355 'stone_event'
01887 [L1626] TGETV    A=5 B=5 C=6 D=1286 
01888 [L1626] ISNEV    A=4 B=0 C=5 D=5 
01889 [L1626] JMP      A=4 B=128 C=38 D=32806 target=1928
01890 [L1627] GGET     A=4 B=0 C=4 D=4 'd_ms'
01891 [L1627] TGETS    A=4 B=4 C=21 D=1045 'd_common_def'
01892 [L1627] KSTR     A=5 B=1 C=100 D=356 'stone_event_type'
01893 [L1627] TGETV    A=4 B=4 C=5 D=1029 
01894 [L1628] TGETS    A=5 B=3 C=7 D=775 'flag'
01895 [L1628] KSTR     A=6 B=1 C=101 D=357 'upgrade_stone'
01896 [L1628] TGETV    A=6 B=4 C=6 D=1030 
01897 [L1628] ISNEV    A=5 B=0 C=6 D=6 
01898 [L1628] JMP      A=5 B=128 C=8 D=32776 target=1907
01899 [L1629] GGET     A=5 B=0 C=4 D=4 'd_ms'
01900 [L1629] KSTR     A=6 B=1 C=102 D=358 'd_stoneUpgradeUI'
01901 [L1629] TGETV    A=5 B=5 C=6 D=1286 
01902 [L1629] KSTR     A=6 B=1 C=103 D=359 'onGetUpgradeResult'
01903 [L1629] TGETV    A=5 B=5 C=6 D=1286 
01904 [L1629] MOV      A=6 B=0 C=3 D=3 
01905 [L1629] CALL     A=5 B=1 C=2 D=258 
01906 [L1629] JMP      A=5 B=133 C=83 D=34131 target=3270
01907 [L1630] TGETS    A=5 B=3 C=7 D=775 'flag'
01908 [L1630] KSTR     A=6 B=1 C=104 D=360 'reborn_stone'
01909 [L1630] TGETV    A=6 B=4 C=6 D=1030 
01910 [L1630] ISNEV    A=5 B=0 C=6 D=6 
01911 [L1630] JMP      A=5 B=128 C=8 D=32776 target=1920
01912 [L1631] GGET     A=5 B=0 C=4 D=4 'd_ms'
01913 [L1631] KSTR     A=6 B=1 C=105 D=361 'd_stoneCastUI'
01914 [L1631] TGETV    A=5 B=5 C=6 D=1286 
01915 [L1631] KSTR     A=6 B=1 C=106 D=362 'onGetResult'
01916 [L1631] TGETV    A=5 B=5 C=6 D=1286 
01917 [L1631] MOV      A=6 B=0 C=3 D=3 
01918 [L1631] CALL     A=5 B=1 C=2 D=258 
01919 [L1631] JMP      A=5 B=133 C=70 D=34118 target=3270
01920 [L1633] GGET     A=5 B=0 C=4 D=4 'd_ms'
01921 [L1633] KSTR     A=6 B=1 C=107 D=363 'd_stoneUI'
01922 [L1633] TGETV    A=5 B=5 C=6 D=1286 
01923 [L1633] KSTR     A=6 B=1 C=108 D=364 'onGetResponse'
01924 [L1633] TGETV    A=5 B=5 C=6 D=1286 
01925 [L1633] MOV      A=6 B=0 C=3 D=3 
01926 [L1633] CALL     A=5 B=1 C=2 D=258 
01927 [L1634] JMP      A=4 B=133 C=62 D=34110 target=3270
01928 [L1635] TGETS    A=4 B=1 C=2 D=258 'id'
01929 [L1635] GGET     A=5 B=1 C=9 D=265 'e_t'
01930 [L1635] KSTR     A=6 B=1 C=109 D=365 'union_event'
01931 [L1635] TGETV    A=5 B=5 C=6 D=1286 
01932 [L1635] ISNEV    A=4 B=0 C=5 D=5 
01933 [L1635] JMP      A=4 B=128 C=8 D=32776 target=1942
01934 [L1636] GGET     A=4 B=0 C=4 D=4 'd_ms'
01935 [L1636] KSTR     A=5 B=1 C=110 D=366 'd_xianmengUI'
01936 [L1636] TGETV    A=4 B=4 C=5 D=1029 
01937 [L1636] KSTR     A=5 B=1 C=111 D=367 'getUnionEvent'
01938 [L1636] TGETV    A=4 B=4 C=5 D=1029 
01939 [L1636] MOV      A=5 B=0 C=3 D=3 
01940 [L1636] CALL     A=4 B=1 C=2 D=258 
01941 [L1636] JMP      A=4 B=133 C=48 D=34096 target=3270
01942 [L1637] TGETS    A=4 B=1 C=2 D=258 'id'
01943 [L1637] GGET     A=5 B=1 C=9 D=265 'e_t'
01944 [L1637] KSTR     A=6 B=1 C=112 D=368 'skill_transform'
01945 [L1637] TGETV    A=5 B=5 C=6 D=1286 
01946 [L1637] ISNEV    A=4 B=0 C=5 D=5 
01947 [L1637] JMP      A=4 B=128 C=8 D=32776 target=1956
01948 [L1638] GGET     A=4 B=0 C=4 D=4 'd_ms'
01949 [L1638] KSTR     A=5 B=1 C=113 D=369 'd_qiankunnizhuan'
01950 [L1638] TGETV    A=4 B=4 C=5 D=1029 
01951 [L1638] KSTR     A=5 B=1 C=114 D=370 'transformSuccess'
01952 [L1638] TGETV    A=4 B=4 C=5 D=1029 
01953 [L1638] MOV      A=5 B=0 C=3 D=3 
01954 [L1638] CALL     A=4 B=1 C=2 D=258 
01955 [L1638] JMP      A=4 B=133 C=34 D=34082 target=3270
01956 [L1639] TGETS    A=4 B=1 C=2 D=258 'id'
01957 [L1639] GGET     A=5 B=1 C=9 D=265 'e_t'
01958 [L1639] KSTR     A=6 B=1 C=115 D=371 'item_transform'
01959 [L1639] TGETV    A=5 B=5 C=6 D=1286 
01960 [L1639] ISNEV    A=4 B=0 C=5 D=5 
01961 [L1639] JMP      A=4 B=128 C=8 D=32776 target=1970
01962 [L1640] GGET     A=4 B=0 C=4 D=4 'd_ms'
01963 [L1640] KSTR     A=5 B=1 C=116 D=372 'd_equipTransUI'
01964 [L1640] TGETV    A=4 B=4 C=5 D=1029 
01965 [L1640] KSTR     A=5 B=1 C=114 D=370 'transformSuccess'
01966 [L1640] TGETV    A=4 B=4 C=5 D=1029 
01967 [L1640] MOV      A=5 B=0 C=3 D=3 
01968 [L1640] CALL     A=4 B=1 C=2 D=258 
01969 [L1640] JMP      A=4 B=133 C=20 D=34068 target=3270
01970 [L1641] TGETS    A=4 B=1 C=2 D=258 'id'
01971 [L1641] GGET     A=5 B=1 C=9 D=265 'e_t'
01972 [L1641] KSTR     A=6 B=1 C=117 D=373 'tangwang_card_prize'
01973 [L1641] TGETV    A=5 B=5 C=6 D=1286 
01974 [L1641] ISNEV    A=4 B=0 C=5 D=5 
01975 [L1641] JMP      A=4 B=128 C=8 D=32776 target=1984
01976 [L1642] GGET     A=4 B=0 C=4 D=4 'd_ms'
01977 [L1642] KSTR     A=5 B=1 C=118 D=374 'd_cardUI'
01978 [L1642] TGETV    A=4 B=4 C=5 D=1029 
01979 [L1642] KSTR     A=5 B=1 C=119 D=375 'onGetExchangeResponse'
01980 [L1642] TGETV    A=4 B=4 C=5 D=1029 
01981 [L1642] MOV      A=5 B=0 C=3 D=3 
01982 [L1642] CALL     A=4 B=1 C=2 D=258 
01983 [L1642] JMP      A=4 B=133 C=6 D=34054 target=3270
01984 [L1643] TGETS    A=4 B=1 C=2 D=258 'id'
01985 [L1643] GGET     A=5 B=1 C=9 D=265 'e_t'
01986 [L1643] KSTR     A=6 B=1 C=120 D=376 'spring_charge_status'
01987 [L1643] TGETV    A=5 B=5 C=6 D=1286 
01988 [L1643] ISNEV    A=4 B=0 C=5 D=5 
01989 [L1643] JMP      A=4 B=128 C=8 D=32776 target=1998
01990 [L1644] GGET     A=4 B=0 C=4 D=4 'd_ms'
01991 [L1644] KSTR     A=5 B=1 C=121 D=377 'd_chargePresentUI'
01992 [L1644] TGETV    A=4 B=4 C=5 D=1029 
01993 [L1644] KSTR     A=5 B=1 C=122 D=378 'getResult'
01994 [L1644] TGETV    A=4 B=4 C=5 D=1029 
01995 [L1644] MOV      A=5 B=0 C=3 D=3 
01996 [L1644] CALL     A=4 B=1 C=2 D=258 
01997 [L1644] JMP      A=4 B=132 C=248 D=34040 target=3270
01998 [L1645] TGETS    A=4 B=1 C=2 D=258 'id'
01999 [L1645] GGET     A=5 B=1 C=9 D=265 'e_t'
02000 [L1645] KSTR     A=6 B=1 C=123 D=379 'spring_charge_prize'
02001 [L1645] TGETV    A=5 B=5 C=6 D=1286 
02002 [L1645] ISNEV    A=4 B=0 C=5 D=5 
02003 [L1645] JMP      A=4 B=128 C=8 D=32776 target=2012
02004 [L1646] GGET     A=4 B=0 C=4 D=4 'd_ms'
02005 [L1646] KSTR     A=5 B=1 C=121 D=377 'd_chargePresentUI'
02006 [L1646] TGETV    A=4 B=4 C=5 D=1029 
02007 [L1646] KSTR     A=5 B=1 C=124 D=380 'getPrizeResult'
02008 [L1646] TGETV    A=4 B=4 C=5 D=1029 
02009 [L1646] MOV      A=5 B=0 C=3 D=3 
02010 [L1646] CALL     A=4 B=1 C=2 D=258 
02011 [L1646] JMP      A=4 B=132 C=234 D=34026 target=3270
02012 [L1647] TGETS    A=4 B=1 C=2 D=258 'id'
02013 [L1647] GGET     A=5 B=1 C=9 D=265 'e_t'
02014 [L1647] KSTR     A=6 B=1 C=125 D=381 'online_prize_info'
02015 [L1647] TGETV    A=5 B=5 C=6 D=1286 
02016 [L1647] ISNEV    A=4 B=0 C=5 D=5 
02017 [L1647] JMP      A=4 B=128 C=8 D=32776 target=2026
02018 [L1648] GGET     A=4 B=0 C=4 D=4 'd_ms'
02019 [L1648] KSTR     A=5 B=1 C=53 D=309 'd_rotUI'
02020 [L1648] TGETV    A=4 B=4 C=5 D=1029 
02021 [L1648] KSTR     A=5 B=1 C=126 D=382 'initRewards'
02022 [L1648] TGETV    A=4 B=4 C=5 D=1029 
02023 [L1648] MOV      A=5 B=0 C=3 D=3 
02024 [L1648] CALL     A=4 B=1 C=2 D=258 
02025 [L1648] JMP      A=4 B=132 C=220 D=34012 target=3270
02026 [L1649] TGETS    A=4 B=1 C=2 D=258 'id'
02027 [L1649] GGET     A=5 B=1 C=9 D=265 'e_t'
02028 [L1649] KSTR     A=6 B=1 C=127 D=383 'cheer_event'
02029 [L1649] TGETV    A=5 B=5 C=6 D=1286 
02030 [L1649] ISNEV    A=4 B=0 C=5 D=5 
02031 [L1649] JMP      A=4 B=128 C=8 D=32776 target=2040
02032 [L1650] GGET     A=4 B=0 C=4 D=4 'd_ms'
02033 [L1650] KSTR     A=5 B=1 C=128 D=384 'd_cheerSquadUI'
02034 [L1650] TGETV    A=4 B=4 C=5 D=1029 
02035 [L1650] KSTR     A=5 B=1 C=129 D=385 'onGetCheerResults'
02036 [L1650] TGETV    A=4 B=4 C=5 D=1029 
02037 [L1650] MOV      A=5 B=0 C=3 D=3 
02038 [L1650] CALL     A=4 B=1 C=2 D=258 
02039 [L1650] JMP      A=4 B=132 C=206 D=33998 target=3270
02040 [L1651] TGETS    A=4 B=1 C=2 D=258 'id'
02041 [L1651] GGET     A=5 B=1 C=9 D=265 'e_t'
02042 [L1651] KSTR     A=6 B=1 C=130 D=386 'random_compose_list'
02043 [L1651] TGETV    A=5 B=5 C=6 D=1286 
02044 [L1651] ISNEV    A=4 B=0 C=5 D=5 
02045 [L1651] JMP      A=4 B=128 C=8 D=32776 target=2054
02046 [L1652] GGET     A=4 B=0 C=4 D=4 'd_ms'
02047 [L1652] KSTR     A=5 B=1 C=131 D=387 'd_equipPieceUI'
02048 [L1652] TGETV    A=4 B=4 C=5 D=1029 
02049 [L1652] KSTR     A=5 B=1 C=132 D=388 'initData'
02050 [L1652] TGETV    A=4 B=4 C=5 D=1029 
02051 [L1652] MOV      A=5 B=0 C=3 D=3 
02052 [L1652] CALL     A=4 B=1 C=2 D=258 
02053 [L1652] JMP      A=4 B=132 C=192 D=33984 target=3270
02054 [L1653] TGETS    A=4 B=1 C=2 D=258 'id'
02055 [L1653] GGET     A=5 B=1 C=9 D=265 'e_t'
02056 [L1653] KSTR     A=6 B=1 C=133 D=389 'modify_head'
02057 [L1653] TGETV    A=5 B=5 C=6 D=1286 
02058 [L1653] ISNEV    A=4 B=0 C=5 D=5 
02059 [L1653] JMP      A=4 B=128 C=7 D=32775 target=2067
02060 [L1654] GGET     A=4 B=0 C=4 D=4 'd_ms'
02061 [L1654] TGETS    A=4 B=4 C=111 D=1135 'd_runeUI'
02062 [L1654] KSTR     A=5 B=1 C=134 D=390 'callback_changeHead'
02063 [L1654] TGETV    A=4 B=4 C=5 D=1029 
02064 [L1654] MOV      A=5 B=0 C=3 D=3 
02065 [L1654] CALL     A=4 B=1 C=2 D=258 
02066 [L1654] JMP      A=4 B=132 C=179 D=33971 target=3270
02067 [L1655] TGETS    A=4 B=1 C=2 D=258 'id'
02068 [L1655] GGET     A=5 B=1 C=9 D=265 'e_t'
02069 [L1655] KSTR     A=6 B=1 C=135 D=391 'send_feast_gift'
02070 [L1655] TGETV    A=5 B=5 C=6 D=1286 
02071 [L1655] ISNEV    A=4 B=0 C=5 D=5 
02072 [L1655] JMP      A=4 B=128 C=8 D=32776 target=2081
02073 [L1656] GGET     A=4 B=0 C=4 D=4 'd_ms'
02074 [L1656] KSTR     A=5 B=1 C=136 D=392 'd_guildPartyUI'
02075 [L1656] TGETV    A=4 B=4 C=5 D=1029 
02076 [L1656] KSTR     A=5 B=1 C=137 D=393 'onGetNewGift'
02077 [L1656] TGETV    A=4 B=4 C=5 D=1029 
02078 [L1656] MOV      A=5 B=0 C=3 D=3 
02079 [L1656] CALL     A=4 B=1 C=2 D=258 
02080 [L1656] JMP      A=4 B=132 C=165 D=33957 target=3270
02081 [L1657] TGETS    A=4 B=1 C=2 D=258 'id'
02082 [L1657] GGET     A=5 B=1 C=9 D=265 'e_t'
02083 [L1657] KSTR     A=6 B=1 C=138 D=394 'consume_gold_data'
02084 [L1657] TGETV    A=5 B=5 C=6 D=1286 
02085 [L1657] ISNEV    A=4 B=0 C=5 D=5 
02086 [L1657] JMP      A=4 B=128 C=8 D=32776 target=2095
02087 [L1658] GGET     A=4 B=0 C=4 D=4 'd_ms'
02088 [L1658] KSTR     A=5 B=1 C=139 D=395 'd_promotionUI'
02089 [L1658] TGETV    A=4 B=4 C=5 D=1029 
02090 [L1658] KSTR     A=5 B=1 C=140 D=396 'onGetActivityStatus'
02091 [L1658] TGETV    A=4 B=4 C=5 D=1029 
02092 [L1658] MOV      A=5 B=0 C=3 D=3 
02093 [L1658] CALL     A=4 B=1 C=2 D=258 
02094 [L1658] JMP      A=4 B=132 C=151 D=33943 target=3270
02095 [L1659] TGETS    A=4 B=1 C=2 D=258 'id'
02096 [L1659] GGET     A=5 B=1 C=9 D=265 'e_t'
02097 [L1659] KSTR     A=6 B=1 C=141 D=397 'consume_gold_prize'
02098 [L1659] TGETV    A=5 B=5 C=6 D=1286 
02099 [L1659] ISNEV    A=4 B=0 C=5 D=5 
02100 [L1659] JMP      A=4 B=128 C=8 D=32776 target=2109
02101 [L1660] GGET     A=4 B=0 C=4 D=4 'd_ms'
02102 [L1660] KSTR     A=5 B=1 C=139 D=395 'd_promotionUI'
02103 [L1660] TGETV    A=4 B=4 C=5 D=1029 
02104 [L1660] KSTR     A=5 B=1 C=124 D=380 'getPrizeResult'
02105 [L1660] TGETV    A=4 B=4 C=5 D=1029 
02106 [L1660] MOV      A=5 B=0 C=3 D=3 
02107 [L1660] CALL     A=4 B=1 C=2 D=258 
02108 [L1660] JMP      A=4 B=132 C=137 D=33929 target=3270
02109 [L1661] TGETS    A=4 B=1 C=2 D=258 'id'
02110 [L1661] GGET     A=5 B=1 C=9 D=265 'e_t'
02111 [L1661] KSTR     A=6 B=1 C=142 D=398 'monday_activity'
02112 [L1661] TGETV    A=5 B=5 C=6 D=1286 
02113 [L1661] ISNEV    A=4 B=0 C=5 D=5 
02114 [L1661] JMP      A=4 B=128 C=8 D=32776 target=2123
02115 [L1662] GGET     A=4 B=0 C=4 D=4 'd_ms'
02116 [L1662] KSTR     A=5 B=1 C=143 D=399 'd_mondayUI'
02117 [L1662] TGETV    A=4 B=4 C=5 D=1029 
02118 [L1662] KSTR     A=5 B=1 C=140 D=396 'onGetActivityStatus'
02119 [L1662] TGETV    A=4 B=4 C=5 D=1029 
02120 [L1662] MOV      A=5 B=0 C=3 D=3 
02121 [L1662] CALL     A=4 B=1 C=2 D=258 
02122 [L1662] JMP      A=4 B=132 C=123 D=33915 target=3270
02123 [L1663] TGETS    A=4 B=1 C=2 D=258 'id'
02124 [L1663] GGET     A=5 B=1 C=9 D=265 'e_t'
02125 [L1663] KSTR     A=6 B=1 C=144 D=400 'update_activity_time'
02126 [L1663] TGETV    A=5 B=5 C=6 D=1286 
02127 [L1663] ISNEV    A=4 B=0 C=5 D=5 
02128 [L1663] JMP      A=4 B=128 C=7 D=32775 target=2136
02129 [L1664] GGET     A=4 B=0 C=4 D=4 'd_ms'
02130 [L1664] TGETS    A=4 B=4 C=32 D=1056 'd_activityUI'
02131 [L1664] KSTR     A=5 B=1 C=145 D=401 'updateAllActivityStatus'
02132 [L1664] TGETV    A=4 B=4 C=5 D=1029 
02133 [L1664] MOV      A=5 B=0 C=3 D=3 
02134 [L1664] CALL     A=4 B=1 C=2 D=258 
02135 [L1664] JMP      A=4 B=132 C=110 D=33902 target=3270
02136 [L1665] TGETS    A=4 B=1 C=2 D=258 'id'
02137 [L1665] GGET     A=5 B=1 C=9 D=265 'e_t'
02138 [L1665] KSTR     A=6 B=1 C=146 D=402 'equip_advance'
02139 [L1665] TGETV    A=5 B=5 C=6 D=1286 
02140 [L1665] ISNEV    A=4 B=0 C=5 D=5 
02141 [L1665] JMP      A=4 B=128 C=8 D=32776 target=2150
02142 [L1666] GGET     A=4 B=0 C=4 D=4 'd_ms'
02143 [L1666] KSTR     A=5 B=1 C=147 D=403 'd_equipAdvanceUI'
02144 [L1666] TGETV    A=4 B=4 C=5 D=1029 
02145 [L1666] KSTR     A=5 B=1 C=148 D=404 'onGetAdvanceResult'
02146 [L1666] TGETV    A=4 B=4 C=5 D=1029 
02147 [L1666] MOV      A=5 B=0 C=3 D=3 
02148 [L1666] CALL     A=4 B=1 C=2 D=258 
02149 [L1666] JMP      A=4 B=132 C=96 D=33888 target=3270
02150 [L1667] TGETS    A=4 B=1 C=2 D=258 'id'
02151 [L1667] GGET     A=5 B=1 C=9 D=265 'e_t'
02152 [L1667] KSTR     A=6 B=1 C=149 D=405 'material_transform'
02153 [L1667] TGETV    A=5 B=5 C=6 D=1286 
02154 [L1667] ISNEV    A=4 B=0 C=5 D=5 
02155 [L1667] JMP      A=4 B=128 C=8 D=32776 target=2164
02156 [L1668] GGET     A=4 B=0 C=4 D=4 'd_ms'
02157 [L1668] KSTR     A=5 B=1 C=150 D=406 'd_smithUI'
02158 [L1668] TGETV    A=4 B=4 C=5 D=1029 
02159 [L1668] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
02160 [L1668] TGETV    A=4 B=4 C=5 D=1029 
02161 [L1668] MOV      A=5 B=0 C=3 D=3 
02162 [L1668] CALL     A=4 B=1 C=2 D=258 
02163 [L1668] JMP      A=4 B=132 C=82 D=33874 target=3270
02164 [L1669] TGETS    A=4 B=1 C=2 D=258 'id'
02165 [L1669] GGET     A=5 B=1 C=9 D=265 'e_t'
02166 [L1669] KSTR     A=6 B=1 C=151 D=407 'labourday_data'
02167 [L1669] TGETV    A=5 B=5 C=6 D=1286 
02168 [L1669] ISNEV    A=4 B=0 C=5 D=5 
02169 [L1669] JMP      A=4 B=128 C=8 D=32776 target=2178
02170 [L1670] GGET     A=4 B=0 C=4 D=4 'd_ms'
02171 [L1670] KSTR     A=5 B=1 C=152 D=408 'd_richmanUI'
02172 [L1670] TGETV    A=4 B=4 C=5 D=1029 
02173 [L1670] KSTR     A=5 B=1 C=140 D=396 'onGetActivityStatus'
02174 [L1670] TGETV    A=4 B=4 C=5 D=1029 
02175 [L1670] MOV      A=5 B=0 C=3 D=3 
02176 [L1670] CALL     A=4 B=1 C=2 D=258 
02177 [L1670] JMP      A=4 B=132 C=68 D=33860 target=3270
02178 [L1671] TGETS    A=4 B=1 C=2 D=258 'id'
02179 [L1671] GGET     A=5 B=1 C=9 D=265 'e_t'
02180 [L1671] KSTR     A=6 B=1 C=153 D=409 'labourday_exchange_prize'
02181 [L1671] TGETV    A=5 B=5 C=6 D=1286 
02182 [L1671] ISNEV    A=4 B=0 C=5 D=5 
02183 [L1671] JMP      A=4 B=128 C=8 D=32776 target=2192
02184 [L1672] GGET     A=4 B=0 C=4 D=4 'd_ms'
02185 [L1672] KSTR     A=5 B=1 C=152 D=408 'd_richmanUI'
02186 [L1672] TGETV    A=4 B=4 C=5 D=1029 
02187 [L1672] KSTR     A=5 B=1 C=154 D=410 'onGetBuyResult'
02188 [L1672] TGETV    A=4 B=4 C=5 D=1029 
02189 [L1672] MOV      A=5 B=0 C=3 D=3 
02190 [L1672] CALL     A=4 B=1 C=2 D=258 
02191 [L1672] JMP      A=4 B=132 C=54 D=33846 target=3270
02192 [L1673] TGETS    A=4 B=1 C=2 D=258 'id'
02193 [L1673] GGET     A=5 B=1 C=9 D=265 'e_t'
02194 [L1673] KSTR     A=6 B=1 C=155 D=411 'labourday_roll_prize'
02195 [L1673] TGETV    A=5 B=5 C=6 D=1286 
02196 [L1673] ISNEV    A=4 B=0 C=5 D=5 
02197 [L1673] JMP      A=4 B=128 C=8 D=32776 target=2206
02198 [L1674] GGET     A=4 B=0 C=4 D=4 'd_ms'
02199 [L1674] KSTR     A=5 B=1 C=152 D=408 'd_richmanUI'
02200 [L1674] TGETV    A=4 B=4 C=5 D=1029 
02201 [L1674] KSTR     A=5 B=1 C=156 D=412 'onGetRollResult'
02202 [L1674] TGETV    A=4 B=4 C=5 D=1029 
02203 [L1674] MOV      A=5 B=0 C=3 D=3 
02204 [L1674] CALL     A=4 B=1 C=2 D=258 
02205 [L1674] JMP      A=4 B=132 C=40 D=33832 target=3270
02206 [L1675] TGETS    A=4 B=1 C=2 D=258 'id'
02207 [L1675] GGET     A=5 B=1 C=9 D=265 'e_t'
02208 [L1675] KSTR     A=6 B=1 C=157 D=413 'cortege_devolve'
02209 [L1675] TGETV    A=5 B=5 C=6 D=1286 
02210 [L1675] ISNEV    A=4 B=0 C=5 D=5 
02211 [L1675] JMP      A=4 B=128 C=8 D=32776 target=2220
02212 [L1676] GGET     A=4 B=0 C=4 D=4 'd_ms'
02213 [L1676] KSTR     A=5 B=1 C=158 D=414 'd_soulRecycleUI'
02214 [L1676] TGETV    A=4 B=4 C=5 D=1029 
02215 [L1676] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
02216 [L1676] TGETV    A=4 B=4 C=5 D=1029 
02217 [L1676] MOV      A=5 B=0 C=3 D=3 
02218 [L1676] CALL     A=4 B=1 C=2 D=258 
02219 [L1676] JMP      A=4 B=132 C=26 D=33818 target=3270
02220 [L1677] TGETS    A=4 B=1 C=2 D=258 'id'
02221 [L1677] GGET     A=5 B=1 C=9 D=265 'e_t'
02222 [L1677] KSTR     A=6 B=1 C=159 D=415 'common_activity'
02223 [L1677] TGETV    A=5 B=5 C=6 D=1286 
02224 [L1677] ISNEV    A=4 B=0 C=5 D=5 
02225 [L1677] JMP      A=4 B=128 C=8 D=32776 target=2234
02226 [L1678] GGET     A=4 B=0 C=4 D=4 'd_ms'
02227 [L1678] KSTR     A=5 B=1 C=23 D=279 'd_actNoticeUI'
02228 [L1678] TGETV    A=4 B=4 C=5 D=1029 
02229 [L1678] KSTR     A=5 B=1 C=160 D=416 'callbackGetActNoticeData'
02230 [L1678] TGETV    A=4 B=4 C=5 D=1029 
02231 [L1678] MOV      A=5 B=0 C=3 D=3 
02232 [L1678] CALL     A=4 B=1 C=2 D=258 
02233 [L1678] JMP      A=4 B=132 C=12 D=33804 target=3270
02234 [L1679] TGETS    A=4 B=1 C=2 D=258 'id'
02235 [L1679] GGET     A=5 B=1 C=9 D=265 'e_t'
02236 [L1679] KSTR     A=6 B=1 C=161 D=417 'local_union_fight'
02237 [L1679] TGETV    A=5 B=5 C=6 D=1286 
02238 [L1679] ISNEV    A=4 B=0 C=5 D=5 
02239 [L1679] JMP      A=4 B=128 C=8 D=32776 target=2248
02240 [L1680] GGET     A=4 B=0 C=4 D=4 'd_ms'
02241 [L1680] KSTR     A=5 B=1 C=162 D=418 'd_guildFightUI'
02242 [L1680] TGETV    A=4 B=4 C=5 D=1029 
02243 [L1680] KSTR     A=5 B=1 C=163 D=419 'getUnionFightInfo'
02244 [L1680] TGETV    A=4 B=4 C=5 D=1029 
02245 [L1680] MOV      A=5 B=0 C=3 D=3 
02246 [L1680] CALL     A=4 B=1 C=2 D=258 
02247 [L1680] JMP      A=4 B=131 C=254 D=33790 target=3270
02248 [L1681] TGETS    A=4 B=1 C=2 D=258 'id'
02249 [L1681] GGET     A=5 B=1 C=9 D=265 'e_t'
02250 [L1681] KSTR     A=6 B=1 C=164 D=420 'dragon_boat_activity'
02251 [L1681] TGETV    A=5 B=5 C=6 D=1286 
02252 [L1681] ISNEV    A=4 B=0 C=5 D=5 
02253 [L1681] JMP      A=4 B=128 C=8 D=32776 target=2262
02254 [L1682] GGET     A=4 B=0 C=4 D=4 'd_ms'
02255 [L1682] KSTR     A=5 B=1 C=165 D=421 'd_ricePuddingUI'
02256 [L1682] TGETV    A=4 B=4 C=5 D=1029 
02257 [L1682] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
02258 [L1682] TGETV    A=4 B=4 C=5 D=1029 
02259 [L1682] MOV      A=5 B=0 C=3 D=3 
02260 [L1682] CALL     A=4 B=1 C=2 D=258 
02261 [L1682] JMP      A=4 B=131 C=240 D=33776 target=3270
02262 [L1683] TGETS    A=4 B=1 C=2 D=258 'id'
02263 [L1683] GGET     A=5 B=1 C=9 D=265 'e_t'
02264 [L1683] KSTR     A=6 B=1 C=166 D=422 'midautumn_activity'
02265 [L1683] TGETV    A=5 B=5 C=6 D=1286 
02266 [L1683] ISNEV    A=4 B=0 C=5 D=5 
02267 [L1683] JMP      A=4 B=128 C=8 D=32776 target=2276
02268 [L1684] GGET     A=4 B=0 C=4 D=4 'd_ms'
02269 [L1684] KSTR     A=5 B=1 C=167 D=423 'd_moonCakeUI'
02270 [L1684] TGETV    A=4 B=4 C=5 D=1029 
02271 [L1684] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
02272 [L1684] TGETV    A=4 B=4 C=5 D=1029 
02273 [L1684] MOV      A=5 B=0 C=3 D=3 
02274 [L1684] CALL     A=4 B=1 C=2 D=258 
02275 [L1684] JMP      A=4 B=131 C=226 D=33762 target=3270
02276 [L1685] TGETS    A=4 B=1 C=2 D=258 'id'
02277 [L1685] GGET     A=5 B=1 C=9 D=265 'e_t'
02278 [L1685] KSTR     A=6 B=1 C=168 D=424 'broad_monthcake_news'
02279 [L1685] TGETV    A=5 B=5 C=6 D=1286 
02280 [L1685] ISNEV    A=4 B=0 C=5 D=5 
02281 [L1685] JMP      A=4 B=128 C=8 D=32776 target=2290
02282 [L1686] GGET     A=4 B=0 C=4 D=4 'd_ms'
02283 [L1686] KSTR     A=5 B=1 C=167 D=423 'd_moonCakeUI'
02284 [L1686] TGETV    A=4 B=4 C=5 D=1029 
02285 [L1686] KSTR     A=5 B=1 C=169 D=425 'onGetResultLuckyList'
02286 [L1686] TGETV    A=4 B=4 C=5 D=1029 
02287 [L1686] MOV      A=5 B=0 C=3 D=3 
02288 [L1686] CALL     A=4 B=1 C=2 D=258 
02289 [L1686] JMP      A=4 B=131 C=212 D=33748 target=3270
02290 [L1687] TGETS    A=4 B=1 C=2 D=258 'id'
02291 [L1687] GGET     A=5 B=1 C=9 D=265 'e_t'
02292 [L1687] KSTR     A=6 B=1 C=170 D=426 'query_champion_list'
02293 [L1687] TGETV    A=5 B=5 C=6 D=1286 
02294 [L1687] ISNEV    A=4 B=0 C=5 D=5 
02295 [L1687] JMP      A=4 B=128 C=8 D=32776 target=2304
02296 [L1688] GGET     A=4 B=0 C=4 D=4 'd_ms'
02297 [L1688] KSTR     A=5 B=1 C=171 D=427 'd_monumentUI'
02298 [L1688] TGETV    A=4 B=4 C=5 D=1029 
02299 [L1688] KSTR     A=5 B=1 C=172 D=428 'onGetMonumentData'
02300 [L1688] TGETV    A=4 B=4 C=5 D=1029 
02301 [L1688] MOV      A=5 B=0 C=3 D=3 
02302 [L1688] CALL     A=4 B=1 C=2 D=258 
02303 [L1688] JMP      A=4 B=131 C=198 D=33734 target=3270
02304 [L1689] TGETS    A=4 B=1 C=2 D=258 'id'
02305 [L1689] GGET     A=5 B=1 C=9 D=265 'e_t'
02306 [L1689] KSTR     A=6 B=1 C=173 D=429 'meet_mystery'
02307 [L1689] TGETV    A=5 B=5 C=6 D=1286 
02308 [L1689] ISNEV    A=4 B=0 C=5 D=5 
02309 [L1689] JMP      A=4 B=128 C=8 D=32776 target=2318
02310 [L1690] GGET     A=4 B=0 C=4 D=4 'd_ms'
02311 [L1690] KSTR     A=5 B=1 C=174 D=430 'd_mysteryUI'
02312 [L1690] TGETV    A=4 B=4 C=5 D=1029 
02313 [L1690] KSTR     A=5 B=1 C=140 D=396 'onGetActivityStatus'
02314 [L1690] TGETV    A=4 B=4 C=5 D=1029 
02315 [L1690] MOV      A=5 B=0 C=3 D=3 
02316 [L1690] CALL     A=4 B=1 C=2 D=258 
02317 [L1690] JMP      A=4 B=131 C=184 D=33720 target=3270
02318 [L1691] TGETS    A=4 B=1 C=2 D=258 'id'
02319 [L1691] GGET     A=5 B=1 C=9 D=265 'e_t'
02320 [L1691] KSTR     A=6 B=1 C=175 D=431 'mystery_consume'
02321 [L1691] TGETV    A=5 B=5 C=6 D=1286 
02322 [L1691] ISNEV    A=4 B=0 C=5 D=5 
02323 [L1691] JMP      A=4 B=128 C=8 D=32776 target=2332
02324 [L1692] GGET     A=4 B=0 C=4 D=4 'd_ms'
02325 [L1692] KSTR     A=5 B=1 C=174 D=430 'd_mysteryUI'
02326 [L1692] TGETV    A=4 B=4 C=5 D=1029 
02327 [L1692] KSTR     A=5 B=1 C=154 D=410 'onGetBuyResult'
02328 [L1692] TGETV    A=4 B=4 C=5 D=1029 
02329 [L1692] MOV      A=5 B=0 C=3 D=3 
02330 [L1692] CALL     A=4 B=1 C=2 D=258 
02331 [L1692] JMP      A=4 B=131 C=170 D=33706 target=3270
02332 [L1693] TGETS    A=4 B=1 C=2 D=258 'id'
02333 [L1693] GGET     A=5 B=1 C=9 D=265 'e_t'
02334 [L1693] KSTR     A=6 B=1 C=176 D=432 'mystery_flush_use_map'
02335 [L1693] TGETV    A=5 B=5 C=6 D=1286 
02336 [L1693] ISNEV    A=4 B=0 C=5 D=5 
02337 [L1693] JMP      A=4 B=128 C=8 D=32776 target=2346
02338 [L1694] GGET     A=4 B=0 C=4 D=4 'd_ms'
02339 [L1694] KSTR     A=5 B=1 C=174 D=430 'd_mysteryUI'
02340 [L1694] TGETV    A=4 B=4 C=5 D=1029 
02341 [L1694] KSTR     A=5 B=1 C=177 D=433 'onGetRefreshResult'
02342 [L1694] TGETV    A=4 B=4 C=5 D=1029 
02343 [L1694] MOV      A=5 B=0 C=3 D=3 
02344 [L1694] CALL     A=4 B=1 C=2 D=258 
02345 [L1694] JMP      A=4 B=131 C=156 D=33692 target=3270
02346 [L1695] TGETS    A=4 B=1 C=2 D=258 'id'
02347 [L1695] GGET     A=5 B=1 C=9 D=265 'e_t'
02348 [L1695] KSTR     A=6 B=1 C=178 D=434 'group_buy_activity'
02349 [L1695] TGETV    A=5 B=5 C=6 D=1286 
02350 [L1695] ISNEV    A=4 B=0 C=5 D=5 
02351 [L1695] JMP      A=4 B=128 C=8 D=32776 target=2360
02352 [L1696] GGET     A=4 B=0 C=4 D=4 'd_ms'
02353 [L1696] KSTR     A=5 B=1 C=23 D=279 'd_actNoticeUI'
02354 [L1696] TGETV    A=4 B=4 C=5 D=1029 
02355 [L1696] KSTR     A=5 B=1 C=179 D=435 'onGetGrouponResult'
02356 [L1696] TGETV    A=4 B=4 C=5 D=1029 
02357 [L1696] MOV      A=5 B=0 C=3 D=3 
02358 [L1696] CALL     A=4 B=1 C=2 D=258 
02359 [L1696] JMP      A=4 B=131 C=142 D=33678 target=3270
02360 [L1697] TGETS    A=4 B=1 C=2 D=258 'id'
02361 [L1697] GGET     A=5 B=1 C=9 D=265 'e_t'
02362 [L1697] KSTR     A=6 B=1 C=180 D=436 'panic_buy_activity'
02363 [L1697] TGETV    A=5 B=5 C=6 D=1286 
02364 [L1697] ISNEV    A=4 B=0 C=5 D=5 
02365 [L1697] JMP      A=4 B=128 C=8 D=32776 target=2374
02366 [L1698] GGET     A=4 B=0 C=4 D=4 'd_ms'
02367 [L1698] KSTR     A=5 B=1 C=181 D=437 'd_salesUI'
02368 [L1698] TGETV    A=4 B=4 C=5 D=1029 
02369 [L1698] KSTR     A=5 B=1 C=154 D=410 'onGetBuyResult'
02370 [L1698] TGETV    A=4 B=4 C=5 D=1029 
02371 [L1698] MOV      A=5 B=0 C=3 D=3 
02372 [L1698] CALL     A=4 B=1 C=2 D=258 
02373 [L1698] JMP      A=4 B=131 C=128 D=33664 target=3270
02374 [L1699] TGETS    A=4 B=1 C=2 D=258 'id'
02375 [L1699] GGET     A=5 B=1 C=9 D=265 'e_t'
02376 [L1699] KSTR     A=6 B=1 C=182 D=438 'query_panic_buy'
02377 [L1699] TGETV    A=5 B=5 C=6 D=1286 
02378 [L1699] ISNEV    A=4 B=0 C=5 D=5 
02379 [L1699] JMP      A=4 B=128 C=8 D=32776 target=2388
02380 [L1700] GGET     A=4 B=0 C=4 D=4 'd_ms'
02381 [L1700] KSTR     A=5 B=1 C=181 D=437 'd_salesUI'
02382 [L1700] TGETV    A=4 B=4 C=5 D=1029 
02383 [L1700] KSTR     A=5 B=1 C=183 D=439 'getActivityData'
02384 [L1700] TGETV    A=4 B=4 C=5 D=1029 
02385 [L1700] MOV      A=5 B=0 C=3 D=3 
02386 [L1700] CALL     A=4 B=1 C=2 D=258 
02387 [L1700] JMP      A=4 B=131 C=114 D=33650 target=3270
02388 [L1701] TGETS    A=4 B=1 C=2 D=258 'id'
02389 [L1701] GGET     A=5 B=1 C=9 D=265 'e_t'
02390 [L1701] KSTR     A=6 B=1 C=184 D=440 'praise_player'
02391 [L1701] TGETV    A=5 B=5 C=6 D=1286 
02392 [L1701] ISNEV    A=4 B=0 C=5 D=5 
02393 [L1701] JMP      A=4 B=128 C=7 D=32775 target=2401
02394 [L1702] GGET     A=4 B=0 C=4 D=4 'd_ms'
02395 [L1702] TGETS    A=4 B=4 C=201 D=1225 'd_worldBossUI'
02396 [L1702] KSTR     A=5 B=1 C=185 D=441 'getPraiseResult'
02397 [L1702] TGETV    A=4 B=4 C=5 D=1029 
02398 [L1702] MOV      A=5 B=0 C=3 D=3 
02399 [L1702] CALL     A=4 B=1 C=2 D=258 
02400 [L1702] JMP      A=4 B=131 C=101 D=33637 target=3270
02401 [L1703] TGETS    A=4 B=1 C=2 D=258 'id'
02402 [L1703] GGET     A=5 B=1 C=9 D=265 'e_t'
02403 [L1703] KSTR     A=6 B=1 C=186 D=442 'friend_buff'
02404 [L1703] TGETV    A=5 B=5 C=6 D=1286 
02405 [L1703] ISNEV    A=4 B=0 C=5 D=5 
02406 [L1703] JMP      A=4 B=128 C=8 D=32776 target=2415
02407 [L1704] GGET     A=4 B=0 C=4 D=4 'd_ms'
02408 [L1704] KSTR     A=5 B=1 C=187 D=443 'd_levelUpBuffUI'
02409 [L1704] TGETV    A=4 B=4 C=5 D=1029 
02410 [L1704] KSTR     A=5 B=1 C=188 D=444 'callback_getBuffData'
02411 [L1704] TGETV    A=4 B=4 C=5 D=1029 
02412 [L1704] MOV      A=5 B=0 C=3 D=3 
02413 [L1704] CALL     A=4 B=1 C=2 D=258 
02414 [L1704] JMP      A=4 B=131 C=87 D=33623 target=3270
02415 [L1705] TGETS    A=4 B=1 C=2 D=258 'id'
02416 [L1705] GGET     A=5 B=1 C=9 D=265 'e_t'
02417 [L1705] KSTR     A=6 B=1 C=189 D=445 'random_monday_prize'
02418 [L1705] TGETV    A=5 B=5 C=6 D=1286 
02419 [L1705] ISNEV    A=4 B=0 C=5 D=5 
02420 [L1705] JMP      A=4 B=128 C=8 D=32776 target=2429
02421 [L1706] GGET     A=4 B=0 C=4 D=4 'd_ms'
02422 [L1706] KSTR     A=5 B=1 C=143 D=399 'd_mondayUI'
02423 [L1706] TGETV    A=4 B=4 C=5 D=1029 
02424 [L1706] KSTR     A=5 B=1 C=190 D=446 'onGetExchangeResult'
02425 [L1706] TGETV    A=4 B=4 C=5 D=1029 
02426 [L1706] MOV      A=5 B=0 C=3 D=3 
02427 [L1706] CALL     A=4 B=1 C=2 D=258 
02428 [L1706] JMP      A=4 B=131 C=73 D=33609 target=3270
02429 [L1707] TGETS    A=4 B=1 C=2 D=258 'id'
02430 [L1707] GGET     A=5 B=1 C=9 D=265 'e_t'
02431 [L1707] KSTR     A=6 B=1 C=191 D=447 'prey_event'
02432 [L1707] TGETV    A=5 B=5 C=6 D=1286 
02433 [L1707] ISNEV    A=4 B=0 C=5 D=5 
02434 [L1707] JMP      A=4 B=128 C=8 D=32776 target=2443
02435 [L1708] GGET     A=4 B=0 C=4 D=4 'd_ms'
02436 [L1708] KSTR     A=5 B=1 C=192 D=448 'd_landUI'
02437 [L1708] TGETV    A=4 B=4 C=5 D=1029 
02438 [L1708] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
02439 [L1708] TGETV    A=4 B=4 C=5 D=1029 
02440 [L1708] MOV      A=5 B=0 C=3 D=3 
02441 [L1708] CALL     A=4 B=1 C=2 D=258 
02442 [L1708] JMP      A=4 B=131 C=59 D=33595 target=3270
02443 [L1709] TGETS    A=4 B=1 C=2 D=258 'id'
02444 [L1709] GGET     A=5 B=1 C=9 D=265 'e_t'
02445 [L1709] KSTR     A=6 B=1 C=193 D=449 'team_event'
02446 [L1709] TGETV    A=5 B=5 C=6 D=1286 
02447 [L1709] ISNEV    A=4 B=0 C=5 D=5 
02448 [L1709] JMP      A=4 B=128 C=8 D=32776 target=2457
02449 [L1710] GGET     A=4 B=0 C=4 D=4 'd_ms'
02450 [L1710] KSTR     A=5 B=1 C=194 D=450 'd_teamUI'
02451 [L1710] TGETV    A=4 B=4 C=5 D=1029 
02452 [L1710] KSTR     A=5 B=1 C=195 D=451 'onGetTeamEvents'
02453 [L1710] TGETV    A=4 B=4 C=5 D=1029 
02454 [L1710] MOV      A=5 B=0 C=3 D=3 
02455 [L1710] CALL     A=4 B=1 C=2 D=258 
02456 [L1710] JMP      A=4 B=131 C=45 D=33581 target=3270
02457 [L1711] TGETS    A=4 B=1 C=2 D=258 'id'
02458 [L1711] GGET     A=5 B=1 C=9 D=265 'e_t'
02459 [L1711] KSTR     A=6 B=1 C=196 D=452 'valentine_activity'
02460 [L1711] TGETV    A=5 B=5 C=6 D=1286 
02461 [L1711] ISNEV    A=4 B=0 C=5 D=5 
02462 [L1711] JMP      A=4 B=128 C=7 D=32775 target=2470
02463 [L1712] GGET     A=4 B=0 C=4 D=4 'd_ms'
02464 [L1712] KSTR     A=5 B=1 C=197 D=453 'd_guessUI'
02465 [L1712] TGETV    A=4 B=4 C=5 D=1029 
02466 [L1712] TGETS    A=4 B=4 C=230 D=1254 'getResFromServer'
02467 [L1712] MOV      A=5 B=0 C=3 D=3 
02468 [L1712] CALL     A=4 B=1 C=2 D=258 
02469 [L1712] JMP      A=4 B=131 C=32 D=33568 target=3270
02470 [L1713] TGETS    A=4 B=1 C=2 D=258 'id'
02471 [L1713] GGET     A=5 B=1 C=9 D=265 'e_t'
02472 [L1713] KSTR     A=6 B=1 C=198 D=454 'query_fight_record'
02473 [L1713] TGETV    A=5 B=5 C=6 D=1286 
02474 [L1713] ISNEV    A=4 B=0 C=5 D=5 
02475 [L1713] JMP      A=4 B=128 C=8 D=32776 target=2484
02476 [L1714] GGET     A=4 B=0 C=4 D=4 'd_ms'
02477 [L1714] KSTR     A=5 B=1 C=162 D=418 'd_guildFightUI'
02478 [L1714] TGETV    A=4 B=4 C=5 D=1029 
02479 [L1714] KSTR     A=5 B=1 C=199 D=455 'callback_fight_record'
02480 [L1714] TGETV    A=4 B=4 C=5 D=1029 
02481 [L1714] MOV      A=5 B=0 C=3 D=3 
02482 [L1714] CALL     A=4 B=1 C=2 D=258 
02483 [L1714] JMP      A=4 B=131 C=18 D=33554 target=3270
02484 [L1715] TGETS    A=4 B=1 C=2 D=258 'id'
02485 [L1715] GGET     A=5 B=1 C=9 D=265 'e_t'
02486 [L1715] KSTR     A=6 B=1 C=200 D=456 'sell_items'
02487 [L1715] TGETV    A=5 B=5 C=6 D=1286 
02488 [L1715] ISNEV    A=4 B=0 C=5 D=5 
02489 [L1715] JMP      A=4 B=128 C=7 D=32775 target=2497
02490 [L1716] GGET     A=4 B=0 C=4 D=4 'd_ms'
02491 [L1716] TGETS    A=4 B=4 C=8 D=1032 'd_packageUI'
02492 [L1716] KSTR     A=5 B=1 C=201 D=457 'onGetSaleResult'
02493 [L1716] TGETV    A=4 B=4 C=5 D=1029 
02494 [L1716] MOV      A=5 B=0 C=3 D=3 
02495 [L1716] CALL     A=4 B=1 C=2 D=258 
02496 [L1716] JMP      A=4 B=131 C=5 D=33541 target=3270
02497 [L1717] TGETS    A=4 B=1 C=2 D=258 'id'
02498 [L1717] GGET     A=5 B=1 C=9 D=265 'e_t'
02499 [L1717] KSTR     A=6 B=1 C=202 D=458 'hunt_soul'
02500 [L1717] TGETV    A=5 B=5 C=6 D=1286 
02501 [L1717] ISNEV    A=4 B=0 C=5 D=5 
02502 [L1717] JMP      A=4 B=128 C=8 D=32776 target=2511
02503 [L1718] GGET     A=4 B=0 C=4 D=4 'd_ms'
02504 [L1718] KSTR     A=5 B=1 C=203 D=459 'd_soulHuntUI'
02505 [L1718] TGETV    A=4 B=4 C=5 D=1029 
02506 [L1718] KSTR     A=5 B=1 C=108 D=364 'onGetResponse'
02507 [L1718] TGETV    A=4 B=4 C=5 D=1029 
02508 [L1718] MOV      A=5 B=0 C=3 D=3 
02509 [L1718] CALL     A=4 B=1 C=2 D=258 
02510 [L1718] JMP      A=4 B=130 C=247 D=33527 target=3270
02511 [L1719] TGETS    A=4 B=1 C=2 D=258 'id'
02512 [L1719] GGET     A=5 B=1 C=9 D=265 'e_t'
02513 [L1719] KSTR     A=6 B=1 C=204 D=460 'upgrade_buffer'
02514 [L1719] TGETV    A=5 B=5 C=6 D=1286 
02515 [L1719] ISNEV    A=4 B=0 C=5 D=5 
02516 [L1719] JMP      A=4 B=128 C=7 D=32775 target=2524
02517 [L1720] GGET     A=4 B=0 C=4 D=4 'd_ms'
02518 [L1720] TGETS    A=4 B=4 C=89 D=1113 'd_skillUpgradeUI'
02519 [L1720] KSTR     A=5 B=1 C=205 D=461 'showServerAdvanceRet'
02520 [L1720] TGETV    A=4 B=4 C=5 D=1029 
02521 [L1720] MOV      A=5 B=0 C=3 D=3 
02522 [L1720] CALL     A=4 B=1 C=2 D=258 
02523 [L1720] JMP      A=4 B=130 C=234 D=33514 target=3270
02524 [L1721] TGETS    A=4 B=1 C=2 D=258 'id'
02525 [L1721] GGET     A=5 B=1 C=9 D=265 'e_t'
02526 [L1721] KSTR     A=6 B=1 C=206 D=462 'query_fight_end'
02527 [L1721] TGETV    A=5 B=5 C=6 D=1286 
02528 [L1721] ISNEV    A=4 B=0 C=5 D=5 
02529 [L1721] JMP      A=4 B=128 C=44 D=32812 target=2574
02530 [L1722] TGETS    A=4 B=3 C=233 D=1001 'fight_type'
02531 [L1722] ISF      A=0 B=0 C=4 D=4 
02532 [L1722] JMP      A=5 B=128 C=15 D=32783 target=2548
02533 [L1722] TGETS    A=4 B=3 C=233 D=1001 'fight_type'
02534 [L1722] GGET     A=5 B=0 C=4 D=4 'd_ms'
02535 [L1722] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
02536 [L1722] TGETS    A=5 B=5 C=233 D=1513 'fight_type'
02537 [L1722] KSTR     A=6 B=1 C=207 D=463 'fight_world_fight_record'
02538 [L1722] TGETV    A=5 B=5 C=6 D=1286 
02539 [L1722] ISNEV    A=4 B=0 C=5 D=5 
02540 [L1722] JMP      A=4 B=128 C=7 D=32775 target=2548
02541 [L1723] GGET     A=4 B=0 C=4 D=4 'd_ms'
02542 [L1723] KSTR     A=5 B=1 C=73 D=329 'd_crossRankUI'
02543 [L1723] TGETV    A=4 B=4 C=5 D=1029 
02544 [L1723] KSTR     A=5 B=1 C=208 D=464 'showFightRecordUI'
02545 [L1723] TGETV    A=4 B=4 C=5 D=1029 
02546 [L1723] CALL     A=4 B=1 C=1 D=257 
02547 [L1723] JMP      A=4 B=130 C=210 D=33490 target=3270
02548 [L1724] TGETS    A=4 B=3 C=233 D=1001 'fight_type'
02549 [L1724] ISF      A=0 B=0 C=4 D=4 
02550 [L1724] JMP      A=5 B=128 C=15 D=32783 target=2566
02551 [L1724] TGETS    A=4 B=3 C=233 D=1001 'fight_type'
02552 [L1724] GGET     A=5 B=0 C=4 D=4 'd_ms'
02553 [L1724] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
02554 [L1724] TGETS    A=5 B=5 C=233 D=1513 'fight_type'
02555 [L1724] KSTR     A=6 B=1 C=209 D=465 'free_world_fight_record'
02556 [L1724] TGETV    A=5 B=5 C=6 D=1286 
02557 [L1724] ISNEV    A=4 B=0 C=5 D=5 
02558 [L1724] JMP      A=4 B=128 C=7 D=32775 target=2566
02559 [L1725] GGET     A=4 B=0 C=4 D=4 'd_ms'
02560 [L1725] KSTR     A=5 B=1 C=210 D=466 'd_arenaUI'
02561 [L1725] TGETV    A=4 B=4 C=5 D=1029 
02562 [L1725] KSTR     A=5 B=1 C=211 D=467 'playRecord'
02563 [L1725] TGETV    A=4 B=4 C=5 D=1029 
02564 [L1725] CALL     A=4 B=1 C=1 D=257 
02565 [L1725] JMP      A=4 B=130 C=192 D=33472 target=3270
02566 [L1727] GGET     A=4 B=0 C=4 D=4 'd_ms'
02567 [L1727] KSTR     A=5 B=1 C=162 D=418 'd_guildFightUI'
02568 [L1727] TGETV    A=4 B=4 C=5 D=1029 
02569 [L1727] KSTR     A=5 B=1 C=212 D=468 'callback_fight_record_end'
02570 [L1727] TGETV    A=4 B=4 C=5 D=1029 
02571 [L1727] MOV      A=5 B=0 C=3 D=3 
02572 [L1727] CALL     A=4 B=1 C=2 D=258 
02573 [L1728] JMP      A=4 B=130 C=184 D=33464 target=3270
02574 [L1729] TGETS    A=4 B=1 C=2 D=258 'id'
02575 [L1729] GGET     A=5 B=1 C=9 D=265 'e_t'
02576 [L1729] KSTR     A=6 B=1 C=213 D=469 'query_collect_info'
02577 [L1729] TGETV    A=5 B=5 C=6 D=1286 
02578 [L1729] ISNEV    A=4 B=0 C=5 D=5 
02579 [L1729] JMP      A=4 B=128 C=8 D=32776 target=2588
02580 [L1730] GGET     A=4 B=0 C=4 D=4 'd_ms'
02581 [L1730] KSTR     A=5 B=1 C=214 D=470 'd_cortCollectUI'
02582 [L1730] TGETV    A=4 B=4 C=5 D=1029 
02583 [L1730] KSTR     A=5 B=1 C=215 D=471 'getCollectInfo'
02584 [L1730] TGETV    A=4 B=4 C=5 D=1029 
02585 [L1730] MOV      A=5 B=0 C=3 D=3 
02586 [L1730] CALL     A=4 B=1 C=2 D=258 
02587 [L1730] JMP      A=4 B=130 C=170 D=33450 target=3270
02588 [L1731] TGETS    A=4 B=1 C=2 D=258 'id'
02589 [L1731] GGET     A=5 B=1 C=9 D=265 'e_t'
02590 [L1731] KSTR     A=6 B=1 C=216 D=472 'activate_cortege'
02591 [L1731] TGETV    A=5 B=5 C=6 D=1286 
02592 [L1731] ISNEV    A=4 B=0 C=5 D=5 
02593 [L1731] JMP      A=4 B=128 C=8 D=32776 target=2602
02594 [L1732] GGET     A=4 B=0 C=4 D=4 'd_ms'
02595 [L1732] KSTR     A=5 B=1 C=214 D=470 'd_cortCollectUI'
02596 [L1732] TGETV    A=4 B=4 C=5 D=1029 
02597 [L1732] KSTR     A=5 B=1 C=217 D=473 'getActiveResult'
02598 [L1732] TGETV    A=4 B=4 C=5 D=1029 
02599 [L1732] MOV      A=5 B=0 C=3 D=3 
02600 [L1732] CALL     A=4 B=1 C=2 D=258 
02601 [L1732] JMP      A=4 B=130 C=156 D=33436 target=3270
02602 [L1733] TGETS    A=4 B=1 C=2 D=258 'id'
02603 [L1733] GGET     A=5 B=1 C=9 D=265 'e_t'
02604 [L1733] KSTR     A=6 B=1 C=218 D=474 'query_role_info'
02605 [L1733] TGETV    A=5 B=5 C=6 D=1286 
02606 [L1733] ISNEV    A=4 B=0 C=5 D=5 
02607 [L1733] JMP      A=4 B=128 C=7 D=32775 target=2615
02608 [L1734] GGET     A=4 B=0 C=4 D=4 'd_ms'
02609 [L1734] TGETS    A=4 B=4 C=10 D=1034 'd_mainUI'
02610 [L1734] KSTR     A=5 B=1 C=219 D=475 'onGetRoleProperty'
02611 [L1734] TGETV    A=4 B=4 C=5 D=1029 
02612 [L1734] MOV      A=5 B=0 C=3 D=3 
02613 [L1734] CALL     A=4 B=1 C=2 D=258 
02614 [L1734] JMP      A=4 B=130 C=143 D=33423 target=3270
02615 [L1735] TGETS    A=4 B=1 C=2 D=258 'id'
02616 [L1735] GGET     A=5 B=1 C=9 D=265 'e_t'
02617 [L1735] KSTR     A=6 B=1 C=220 D=476 'weekend_event'
02618 [L1735] TGETV    A=5 B=5 C=6 D=1286 
02619 [L1735] ISNEV    A=4 B=0 C=5 D=5 
02620 [L1735] JMP      A=4 B=128 C=8 D=32776 target=2629
02621 [L1736] GGET     A=4 B=0 C=4 D=4 'd_ms'
02622 [L1736] KSTR     A=5 B=1 C=221 D=477 'd_miniGameUI'
02623 [L1736] TGETV    A=4 B=4 C=5 D=1029 
02624 [L1736] KSTR     A=5 B=1 C=222 D=478 'onGetActResult'
02625 [L1736] TGETV    A=4 B=4 C=5 D=1029 
02626 [L1736] MOV      A=5 B=0 C=3 D=3 
02627 [L1736] CALL     A=4 B=1 C=2 D=258 
02628 [L1736] JMP      A=4 B=130 C=129 D=33409 target=3270
02629 [L1737] TGETS    A=4 B=1 C=2 D=258 'id'
02630 [L1737] GGET     A=5 B=1 C=9 D=265 'e_t'
02631 [L1737] KSTR     A=6 B=1 C=223 D=479 'nine_sky_event'
02632 [L1737] TGETV    A=5 B=5 C=6 D=1286 
02633 [L1737] ISNEV    A=4 B=0 C=5 D=5 
02634 [L1737] JMP      A=4 B=128 C=8 D=32776 target=2643
02635 [L1738] GGET     A=4 B=0 C=4 D=4 'd_ms'
02636 [L1738] KSTR     A=5 B=1 C=224 D=480 'd_towerUI'
02637 [L1738] TGETV    A=4 B=4 C=5 D=1029 
02638 [L1738] KSTR     A=5 B=1 C=222 D=478 'onGetActResult'
02639 [L1738] TGETV    A=4 B=4 C=5 D=1029 
02640 [L1738] MOV      A=5 B=0 C=3 D=3 
02641 [L1738] CALL     A=4 B=1 C=2 D=258 
02642 [L1738] JMP      A=4 B=130 C=115 D=33395 target=3270
02643 [L1739] TGETS    A=4 B=1 C=2 D=258 'id'
02644 [L1739] GGET     A=5 B=1 C=9 D=265 'e_t'
02645 [L1739] KSTR     A=6 B=1 C=225 D=481 'spirit_gossip_event'
02646 [L1739] TGETV    A=5 B=5 C=6 D=1286 
02647 [L1739] ISNEV    A=4 B=0 C=5 D=5 
02648 [L1739] JMP      A=4 B=128 C=8 D=32776 target=2657
02649 [L1740] GGET     A=4 B=0 C=4 D=4 'd_ms'
02650 [L1740] KSTR     A=5 B=1 C=226 D=482 'd_lingUI'
02651 [L1740] TGETV    A=4 B=4 C=5 D=1029 
02652 [L1740] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
02653 [L1740] TGETV    A=4 B=4 C=5 D=1029 
02654 [L1740] MOV      A=5 B=0 C=3 D=3 
02655 [L1740] CALL     A=4 B=1 C=2 D=258 
02656 [L1740] JMP      A=4 B=130 C=101 D=33381 target=3270
02657 [L1741] TGETS    A=4 B=1 C=2 D=258 'id'
02658 [L1741] GGET     A=5 B=1 C=9 D=265 'e_t'
02659 [L1741] KSTR     A=6 B=1 C=227 D=483 'longevity_hill_event'
02660 [L1741] TGETV    A=5 B=5 C=6 D=1286 
02661 [L1741] ISNEV    A=4 B=0 C=5 D=5 
02662 [L1741] JMP      A=4 B=128 C=8 D=32776 target=2671
02663 [L1742] GGET     A=4 B=0 C=4 D=4 'd_ms'
02664 [L1742] KSTR     A=5 B=1 C=228 D=484 'd_kickUI'
02665 [L1742] TGETV    A=4 B=4 C=5 D=1029 
02666 [L1742] KSTR     A=5 B=1 C=108 D=364 'onGetResponse'
02667 [L1742] TGETV    A=4 B=4 C=5 D=1029 
02668 [L1742] MOV      A=5 B=0 C=3 D=3 
02669 [L1742] CALL     A=4 B=1 C=2 D=258 
02670 [L1742] JMP      A=4 B=130 C=87 D=33367 target=3270
02671 [L1743] TGETS    A=4 B=1 C=2 D=258 'id'
02672 [L1743] GGET     A=5 B=1 C=9 D=265 'e_t'
02673 [L1743] KSTR     A=6 B=1 C=229 D=485 'pile_snowman'
02674 [L1743] TGETV    A=5 B=5 C=6 D=1286 
02675 [L1743] ISNEV    A=4 B=0 C=5 D=5 
02676 [L1743] JMP      A=4 B=128 C=8 D=32776 target=2685
02677 [L1744] GGET     A=4 B=0 C=4 D=4 'd_ms'
02678 [L1744] KSTR     A=5 B=1 C=230 D=486 'd_snowmanUI'
02679 [L1744] TGETV    A=4 B=4 C=5 D=1029 
02680 [L1744] KSTR     A=5 B=1 C=108 D=364 'onGetResponse'
02681 [L1744] TGETV    A=4 B=4 C=5 D=1029 
02682 [L1744] MOV      A=5 B=0 C=3 D=3 
02683 [L1744] CALL     A=4 B=1 C=2 D=258 
02684 [L1744] JMP      A=4 B=130 C=73 D=33353 target=3270
02685 [L1745] TGETS    A=4 B=1 C=2 D=258 'id'
02686 [L1745] GGET     A=5 B=1 C=9 D=265 'e_t'
02687 [L1745] KSTR     A=6 B=1 C=231 D=487 'broad_pile_snowman'
02688 [L1745] TGETV    A=5 B=5 C=6 D=1286 
02689 [L1745] ISNEV    A=4 B=0 C=5 D=5 
02690 [L1745] JMP      A=4 B=128 C=8 D=32776 target=2699
02691 [L1746] GGET     A=4 B=0 C=4 D=4 'd_ms'
02692 [L1746] KSTR     A=5 B=1 C=230 D=486 'd_snowmanUI'
02693 [L1746] TGETV    A=4 B=4 C=5 D=1029 
02694 [L1746] KSTR     A=5 B=1 C=232 D=488 'onGetBroadcast'
02695 [L1746] TGETV    A=4 B=4 C=5 D=1029 
02696 [L1746] MOV      A=5 B=0 C=3 D=3 
02697 [L1746] CALL     A=4 B=1 C=2 D=258 
02698 [L1746] JMP      A=4 B=130 C=59 D=33339 target=3270
02699 [L1747] TGETS    A=4 B=1 C=2 D=258 'id'
02700 [L1747] GGET     A=5 B=1 C=9 D=265 'e_t'
02701 [L1747] KSTR     A=6 B=1 C=233 D=489 'analysis_dream'
02702 [L1747] TGETV    A=5 B=5 C=6 D=1286 
02703 [L1747] ISNEV    A=4 B=0 C=5 D=5 
02704 [L1747] JMP      A=4 B=128 C=8 D=32776 target=2713
02705 [L1748] GGET     A=4 B=0 C=4 D=4 'd_ms'
02706 [L1748] KSTR     A=5 B=1 C=234 D=490 'd_dreamUI'
02707 [L1748] TGETV    A=4 B=4 C=5 D=1029 
02708 [L1748] KSTR     A=5 B=1 C=108 D=364 'onGetResponse'
02709 [L1748] TGETV    A=4 B=4 C=5 D=1029 
02710 [L1748] MOV      A=5 B=0 C=3 D=3 
02711 [L1748] CALL     A=4 B=1 C=2 D=258 
02712 [L1748] JMP      A=4 B=130 C=45 D=33325 target=3270
02713 [L1749] TGETS    A=4 B=1 C=2 D=258 'id'
02714 [L1749] GGET     A=5 B=1 C=9 D=265 'e_t'
02715 [L1749] KSTR     A=6 B=1 C=235 D=491 'monster_nian_event'
02716 [L1749] TGETV    A=5 B=5 C=6 D=1286 
02717 [L1749] ISNEV    A=4 B=0 C=5 D=5 
02718 [L1749] JMP      A=4 B=128 C=8 D=32776 target=2727
02719 [L1750] GGET     A=4 B=0 C=4 D=4 'd_ms'
02720 [L1750] KSTR     A=5 B=1 C=236 D=492 'd_omenUI'
02721 [L1750] TGETV    A=4 B=4 C=5 D=1029 
02722 [L1750] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
02723 [L1750] TGETV    A=4 B=4 C=5 D=1029 
02724 [L1750] MOV      A=5 B=0 C=3 D=3 
02725 [L1750] CALL     A=4 B=1 C=2 D=258 
02726 [L1750] JMP      A=4 B=130 C=31 D=33311 target=3270
02727 [L1751] TGETS    A=4 B=1 C=2 D=258 'id'
02728 [L1751] GGET     A=5 B=1 C=9 D=265 'e_t'
02729 [L1751] KSTR     A=6 B=1 C=237 D=493 'remove_friend_serial'
02730 [L1751] TGETV    A=5 B=5 C=6 D=1286 
02731 [L1751] ISNEV    A=4 B=0 C=5 D=5 
02732 [L1751] JMP      A=4 B=128 C=7 D=32775 target=2740
02733 [L1752] GGET     A=4 B=0 C=4 D=4 'd_ms'
02734 [L1752] TGETS    A=4 B=4 C=53 D=1077 'd_followUI'
02735 [L1752] KSTR     A=5 B=1 C=238 D=494 'onGetRemoveRelationA_B'
02736 [L1752] TGETV    A=4 B=4 C=5 D=1029 
02737 [L1752] MOV      A=5 B=0 C=3 D=3 
02738 [L1752] CALL     A=4 B=1 C=2 D=258 
02739 [L1752] JMP      A=4 B=130 C=18 D=33298 target=3270
02740 [L1753] TGETS    A=4 B=1 C=2 D=258 'id'
02741 [L1753] GGET     A=5 B=1 C=9 D=265 'e_t'
02742 [L1753] KSTR     A=6 B=1 C=239 D=495 'reborn_event'
02743 [L1753] TGETV    A=5 B=5 C=6 D=1286 
02744 [L1753] ISNEV    A=4 B=0 C=5 D=5 
02745 [L1753] JMP      A=4 B=128 C=8 D=32776 target=2754
02746 [L1754] GGET     A=4 B=0 C=4 D=4 'd_ms'
02747 [L1754] KSTR     A=5 B=1 C=240 D=496 'd_ascensionUI'
02748 [L1754] TGETV    A=4 B=4 C=5 D=1029 
02749 [L1754] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
02750 [L1754] TGETV    A=4 B=4 C=5 D=1029 
02751 [L1754] MOV      A=5 B=0 C=3 D=3 
02752 [L1754] CALL     A=4 B=1 C=2 D=258 
02753 [L1754] JMP      A=4 B=130 C=4 D=33284 target=3270
02754 [L1755] TGETS    A=4 B=1 C=2 D=258 'id'
02755 [L1755] GGET     A=5 B=1 C=9 D=265 'e_t'
02756 [L1755] KSTR     A=6 B=1 C=241 D=497 'specter_event'
02757 [L1755] TGETV    A=5 B=5 C=6 D=1286 
02758 [L1755] ISNEV    A=4 B=0 C=5 D=5 
02759 [L1755] JMP      A=4 B=128 C=8 D=32776 target=2768
02760 [L1756] GGET     A=4 B=0 C=4 D=4 'd_ms'
02761 [L1756] KSTR     A=5 B=1 C=242 D=498 'd_abyssUI'
02762 [L1756] TGETV    A=4 B=4 C=5 D=1029 
02763 [L1756] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
02764 [L1756] TGETV    A=4 B=4 C=5 D=1029 
02765 [L1756] MOV      A=5 B=0 C=3 D=3 
02766 [L1756] CALL     A=4 B=1 C=2 D=258 
02767 [L1756] JMP      A=4 B=129 C=246 D=33270 target=3270
02768 [L1757] TGETS    A=4 B=1 C=2 D=258 'id'
02769 [L1757] GGET     A=5 B=1 C=9 D=265 'e_t'
02770 [L1757] KSTR     A=6 B=1 C=243 D=499 'wishing_pavilion'
02771 [L1757] TGETV    A=5 B=5 C=6 D=1286 
02772 [L1757] ISNEV    A=4 B=0 C=5 D=5 
02773 [L1757] JMP      A=4 B=128 C=8 D=32776 target=2782
02774 [L1758] GGET     A=4 B=0 C=4 D=4 'd_ms'
02775 [L1758] KSTR     A=5 B=1 C=244 D=500 'd_newPromotionUI'
02776 [L1758] TGETV    A=4 B=4 C=5 D=1029 
02777 [L1758] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
02778 [L1758] TGETV    A=4 B=4 C=5 D=1029 
02779 [L1758] MOV      A=5 B=0 C=3 D=3 
02780 [L1758] CALL     A=4 B=1 C=2 D=258 
02781 [L1758] JMP      A=4 B=129 C=232 D=33256 target=3270
02782 [L1759] TGETS    A=4 B=1 C=2 D=258 'id'
02783 [L1759] GGET     A=5 B=1 C=9 D=265 'e_t'
02784 [L1759] KSTR     A=6 B=1 C=245 D=501 'animal_grow_event'
02785 [L1759] TGETV    A=5 B=5 C=6 D=1286 
02786 [L1759] ISNEV    A=4 B=0 C=5 D=5 
02787 [L1759] JMP      A=4 B=128 C=8 D=32776 target=2796
02788 [L1760] GGET     A=4 B=0 C=4 D=4 'd_ms'
02789 [L1760] KSTR     A=5 B=1 C=246 D=502 'd_petUI'
02790 [L1760] TGETV    A=4 B=4 C=5 D=1029 
02791 [L1760] KSTR     A=5 B=1 C=108 D=364 'onGetResponse'
02792 [L1760] TGETV    A=4 B=4 C=5 D=1029 
02793 [L1760] MOV      A=5 B=0 C=3 D=3 
02794 [L1760] CALL     A=4 B=1 C=2 D=258 
02795 [L1760] JMP      A=4 B=129 C=218 D=33242 target=3270
02796 [L1761] TGETS    A=4 B=1 C=2 D=258 'id'
02797 [L1761] GGET     A=5 B=1 C=9 D=265 'e_t'
02798 [L1761] KSTR     A=6 B=1 C=247 D=503 'title_event'
02799 [L1761] TGETV    A=5 B=5 C=6 D=1286 
02800 [L1761] ISNEV    A=4 B=0 C=5 D=5 
02801 [L1761] JMP      A=4 B=128 C=8 D=32776 target=2810
02802 [L1762] GGET     A=4 B=0 C=4 D=4 'd_ms'
02803 [L1762] KSTR     A=5 B=1 C=248 D=504 'd_honorUI'
02804 [L1762] TGETV    A=4 B=4 C=5 D=1029 
02805 [L1762] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
02806 [L1762] TGETV    A=4 B=4 C=5 D=1029 
02807 [L1762] MOV      A=5 B=0 C=3 D=3 
02808 [L1762] CALL     A=4 B=1 C=2 D=258 
02809 [L1762] JMP      A=4 B=129 C=204 D=33228 target=3270
02810 [L1763] TGETS    A=4 B=1 C=2 D=258 'id'
02811 [L1763] GGET     A=5 B=1 C=9 D=265 'e_t'
02812 [L1763] KSTR     A=6 B=1 C=249 D=505 'furnace_activity'
02813 [L1763] TGETV    A=5 B=5 C=6 D=1286 
02814 [L1763] ISNEV    A=4 B=0 C=5 D=5 
02815 [L1763] JMP      A=4 B=128 C=8 D=32776 target=2824
02816 [L1764] GGET     A=4 B=0 C=4 D=4 'd_ms'
02817 [L1764] KSTR     A=5 B=1 C=250 D=506 'd_alchemyUI'
02818 [L1764] TGETV    A=4 B=4 C=5 D=1029 
02819 [L1764] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
02820 [L1764] TGETV    A=4 B=4 C=5 D=1029 
02821 [L1764] MOV      A=5 B=0 C=3 D=3 
02822 [L1764] CALL     A=4 B=1 C=2 D=258 
02823 [L1764] JMP      A=4 B=129 C=190 D=33214 target=3270
02824 [L1765] TGETS    A=4 B=1 C=2 D=258 'id'
02825 [L1765] GGET     A=5 B=1 C=9 D=265 'e_t'
02826 [L1765] KSTR     A=6 B=1 C=251 D=507 'orient_train_cortege'
02827 [L1765] TGETV    A=5 B=5 C=6 D=1286 
02828 [L1765] ISNEV    A=4 B=0 C=5 D=5 
02829 [L1765] JMP      A=4 B=128 C=7 D=32775 target=2837
02830 [L1766] GGET     A=4 B=0 C=4 D=4 'd_ms'
02831 [L1766] TGETS    A=4 B=4 C=178 D=1202 'd_trainingUI'
02832 [L1766] KSTR     A=5 B=1 C=252 D=508 'onGetDirectResult'
02833 [L1766] TGETV    A=4 B=4 C=5 D=1029 
02834 [L1766] MOV      A=5 B=0 C=3 D=3 
02835 [L1766] CALL     A=4 B=1 C=2 D=258 
02836 [L1766] JMP      A=4 B=129 C=177 D=33201 target=3270
02837 [L1767] TGETS    A=4 B=1 C=2 D=258 'id'
02838 [L1767] GGET     A=5 B=1 C=9 D=265 'e_t'
02839 [L1767] KSTR     A=6 B=1 C=253 D=509 'summer_activity'
02840 [L1767] TGETV    A=5 B=5 C=6 D=1286 
02841 [L1767] ISNEV    A=4 B=0 C=5 D=5 
02842 [L1767] JMP      A=4 B=128 C=8 D=32776 target=2851
02843 [L1768] GGET     A=4 B=0 C=4 D=4 'd_ms'
02844 [L1768] KSTR     A=5 B=1 C=254 D=510 'd_summerUI'
02845 [L1768] TGETV    A=4 B=4 C=5 D=1029 
02846 [L1768] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
02847 [L1768] TGETV    A=4 B=4 C=5 D=1029 
02848 [L1768] MOV      A=5 B=0 C=3 D=3 
02849 [L1768] CALL     A=4 B=1 C=2 D=258 
02850 [L1768] JMP      A=4 B=129 C=163 D=33187 target=3270
02851 [L1769] TGETS    A=4 B=1 C=2 D=258 'id'
02852 [L1769] GGET     A=5 B=1 C=9 D=265 'e_t'
02853 [L1769] KSTR     A=6 B=1 C=255 D=511 'awaken_skill'
02854 [L1769] TGETV    A=5 B=5 C=6 D=1286 
02855 [L1769] ISNEV    A=4 B=0 C=5 D=5 
02856 [L1769] JMP      A=4 B=128 C=8 D=32776 target=2865
02857 [L1770] GGET     A=4 B=0 C=4 D=4 'd_ms'
02858 [L1770] KSTR     A=5 B=2 C=0 D=512 'd_wakeUI'
02859 [L1770] TGETV    A=4 B=4 C=5 D=1029 
02860 [L1770] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
02861 [L1770] TGETV    A=4 B=4 C=5 D=1029 
02862 [L1770] MOV      A=5 B=0 C=3 D=3 
02863 [L1770] CALL     A=4 B=1 C=2 D=258 
02864 [L1770] JMP      A=4 B=129 C=149 D=33173 target=3270
02865 [L1771] TGETS    A=4 B=1 C=2 D=258 'id'
02866 [L1771] GGET     A=5 B=1 C=9 D=265 'e_t'
02867 [L1771] KSTR     A=6 B=2 C=1 D=513 'yuanshi_activity'
02868 [L1771] TGETV    A=5 B=5 C=6 D=1286 
02869 [L1771] ISNEV    A=4 B=0 C=5 D=5 
02870 [L1771] JMP      A=4 B=128 C=8 D=32776 target=2879
02871 [L1772] GGET     A=4 B=0 C=4 D=4 'd_ms'
02872 [L1772] KSTR     A=5 B=2 C=2 D=514 'd_twoYearsCelebrateUI'
02873 [L1772] TGETV    A=4 B=4 C=5 D=1029 
02874 [L1772] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
02875 [L1772] TGETV    A=4 B=4 C=5 D=1029 
02876 [L1772] MOV      A=5 B=0 C=3 D=3 
02877 [L1772] CALL     A=4 B=1 C=2 D=258 
02878 [L1772] JMP      A=4 B=129 C=135 D=33159 target=3270
02879 [L1773] TGETS    A=4 B=1 C=2 D=258 'id'
02880 [L1773] GGET     A=5 B=1 C=9 D=265 'e_t'
02881 [L1773] KSTR     A=6 B=2 C=3 D=515 'vip_shop_event'
02882 [L1773] TGETV    A=5 B=5 C=6 D=1286 
02883 [L1773] ISNEV    A=4 B=0 C=5 D=5 
02884 [L1773] JMP      A=4 B=128 C=8 D=32776 target=2893
02885 [L1774] GGET     A=4 B=0 C=4 D=4 'd_ms'
02886 [L1774] KSTR     A=5 B=2 C=4 D=516 'd_xianlingShopUI'
02887 [L1774] TGETV    A=4 B=4 C=5 D=1029 
02888 [L1774] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
02889 [L1774] TGETV    A=4 B=4 C=5 D=1029 
02890 [L1774] MOV      A=5 B=0 C=3 D=3 
02891 [L1774] CALL     A=4 B=1 C=2 D=258 
02892 [L1774] JMP      A=4 B=129 C=121 D=33145 target=3270
02893 [L1775] TGETS    A=4 B=1 C=2 D=258 'id'
02894 [L1775] GGET     A=5 B=1 C=9 D=265 'e_t'
02895 [L1775] KSTR     A=6 B=2 C=5 D=517 'imperial_examination'
02896 [L1775] TGETV    A=5 B=5 C=6 D=1286 
02897 [L1775] ISNEV    A=4 B=0 C=5 D=5 
02898 [L1775] JMP      A=4 B=128 C=8 D=32776 target=2907
02899 [L1776] GGET     A=4 B=0 C=4 D=4 'd_ms'
02900 [L1776] KSTR     A=5 B=2 C=6 D=518 'd_answerUI'
02901 [L1776] TGETV    A=4 B=4 C=5 D=1029 
02902 [L1776] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
02903 [L1776] TGETV    A=4 B=4 C=5 D=1029 
02904 [L1776] MOV      A=5 B=0 C=3 D=3 
02905 [L1776] CALL     A=4 B=1 C=2 D=258 
02906 [L1776] JMP      A=4 B=129 C=107 D=33131 target=3270
02907 [L1777] TGETS    A=4 B=1 C=2 D=258 'id'
02908 [L1777] GGET     A=5 B=1 C=9 D=265 'e_t'
02909 [L1777] KSTR     A=6 B=2 C=7 D=519 'restore_awaken_skill'
02910 [L1777] TGETV    A=5 B=5 C=6 D=1286 
02911 [L1777] ISNEV    A=4 B=0 C=5 D=5 
02912 [L1777] JMP      A=4 B=128 C=8 D=32776 target=2921
02913 [L1778] GGET     A=4 B=0 C=4 D=4 'd_ms'
02914 [L1778] KSTR     A=5 B=2 C=0 D=512 'd_wakeUI'
02915 [L1778] TGETV    A=4 B=4 C=5 D=1029 
02916 [L1778] KSTR     A=5 B=2 C=8 D=520 'reStoreAwakenSkillResult'
02917 [L1778] TGETV    A=4 B=4 C=5 D=1029 
02918 [L1778] MOV      A=5 B=0 C=3 D=3 
02919 [L1778] CALL     A=4 B=1 C=2 D=258 
02920 [L1778] JMP      A=4 B=129 C=93 D=33117 target=3270
02921 [L1779] TGETS    A=4 B=1 C=2 D=258 'id'
02922 [L1779] GGET     A=5 B=1 C=9 D=265 'e_t'
02923 [L1779] KSTR     A=6 B=2 C=9 D=521 'equip_ext_star'
02924 [L1779] TGETV    A=5 B=5 C=6 D=1286 
02925 [L1779] ISNEV    A=4 B=0 C=5 D=5 
02926 [L1779] JMP      A=4 B=128 C=8 D=32776 target=2935
02927 [L1780] GGET     A=4 B=0 C=4 D=4 'd_ms'
02928 [L1780] KSTR     A=5 B=2 C=0 D=512 'd_wakeUI'
02929 [L1780] TGETV    A=4 B=4 C=5 D=1029 
02930 [L1780] KSTR     A=5 B=2 C=10 D=522 'onEquipResult'
02931 [L1780] TGETV    A=4 B=4 C=5 D=1029 
02932 [L1780] MOV      A=5 B=0 C=3 D=3 
02933 [L1780] CALL     A=4 B=1 C=2 D=258 
02934 [L1780] JMP      A=4 B=129 C=79 D=33103 target=3270
02935 [L1781] TGETS    A=4 B=1 C=2 D=258 'id'
02936 [L1781] GGET     A=5 B=1 C=9 D=265 'e_t'
02937 [L1781] KSTR     A=6 B=2 C=11 D=523 'unload_ext_star'
02938 [L1781] TGETV    A=5 B=5 C=6 D=1286 
02939 [L1781] ISNEV    A=4 B=0 C=5 D=5 
02940 [L1781] JMP      A=4 B=128 C=8 D=32776 target=2949
02941 [L1782] GGET     A=4 B=0 C=4 D=4 'd_ms'
02942 [L1782] KSTR     A=5 B=2 C=0 D=512 'd_wakeUI'
02943 [L1782] TGETV    A=4 B=4 C=5 D=1029 
02944 [L1782] KSTR     A=5 B=2 C=12 D=524 'onUnloadResult'
02945 [L1782] TGETV    A=4 B=4 C=5 D=1029 
02946 [L1782] MOV      A=5 B=0 C=3 D=3 
02947 [L1782] CALL     A=4 B=1 C=2 D=258 
02948 [L1782] JMP      A=4 B=129 C=65 D=33089 target=3270
02949 [L1783] TGETS    A=4 B=1 C=2 D=258 'id'
02950 [L1783] GGET     A=5 B=1 C=9 D=265 'e_t'
02951 [L1783] KSTR     A=6 B=2 C=13 D=525 'upgrade_ext_star'
02952 [L1783] TGETV    A=5 B=5 C=6 D=1286 
02953 [L1783] ISNEV    A=4 B=0 C=5 D=5 
02954 [L1783] JMP      A=4 B=128 C=8 D=32776 target=2963
02955 [L1784] GGET     A=4 B=0 C=4 D=4 'd_ms'
02956 [L1784] KSTR     A=5 B=2 C=0 D=512 'd_wakeUI'
02957 [L1784] TGETV    A=4 B=4 C=5 D=1029 
02958 [L1784] KSTR     A=5 B=2 C=14 D=526 'onUpgradeResult'
02959 [L1784] TGETV    A=4 B=4 C=5 D=1029 
02960 [L1784] MOV      A=5 B=0 C=3 D=3 
02961 [L1784] CALL     A=4 B=1 C=2 D=258 
02962 [L1784] JMP      A=4 B=129 C=51 D=33075 target=3270
02963 [L1785] TGETS    A=4 B=1 C=2 D=258 'id'
02964 [L1785] GGET     A=5 B=1 C=9 D=265 'e_t'
02965 [L1785] KSTR     A=6 B=2 C=15 D=527 'decompose_ext_star'
02966 [L1785] TGETV    A=5 B=5 C=6 D=1286 
02967 [L1785] ISNEV    A=4 B=0 C=5 D=5 
02968 [L1785] JMP      A=4 B=128 C=8 D=32776 target=2977
02969 [L1786] GGET     A=4 B=0 C=4 D=4 'd_ms'
02970 [L1786] KSTR     A=5 B=2 C=0 D=512 'd_wakeUI'
02971 [L1786] TGETV    A=4 B=4 C=5 D=1029 
02972 [L1786] KSTR     A=5 B=2 C=16 D=528 'onResolveResult'
02973 [L1786] TGETV    A=4 B=4 C=5 D=1029 
02974 [L1786] MOV      A=5 B=0 C=3 D=3 
02975 [L1786] CALL     A=4 B=1 C=2 D=258 
02976 [L1786] JMP      A=4 B=129 C=37 D=33061 target=3270
02977 [L1787] TGETS    A=4 B=1 C=2 D=258 'id'
02978 [L1787] GGET     A=5 B=1 C=9 D=265 'e_t'
02979 [L1787] KSTR     A=6 B=2 C=17 D=529 'divination_event'
02980 [L1787] TGETV    A=5 B=5 C=6 D=1286 
02981 [L1787] ISNEV    A=4 B=0 C=5 D=5 
02982 [L1787] JMP      A=4 B=128 C=8 D=32776 target=2991
02983 [L1788] GGET     A=4 B=0 C=4 D=4 'd_ms'
02984 [L1788] KSTR     A=5 B=2 C=0 D=512 'd_wakeUI'
02985 [L1788] TGETV    A=4 B=4 C=5 D=1029 
02986 [L1788] KSTR     A=5 B=2 C=18 D=530 'onDivineResult'
02987 [L1788] TGETV    A=4 B=4 C=5 D=1029 
02988 [L1788] MOV      A=5 B=0 C=3 D=3 
02989 [L1788] CALL     A=4 B=1 C=2 D=258 
02990 [L1788] JMP      A=4 B=129 C=23 D=33047 target=3270
02991 [L1789] TGETS    A=4 B=1 C=2 D=258 'id'
02992 [L1789] GGET     A=5 B=1 C=9 D=265 'e_t'
02993 [L1789] KSTR     A=6 B=2 C=19 D=531 'replace_equiped_star'
02994 [L1789] TGETV    A=5 B=5 C=6 D=1286 
02995 [L1789] ISNEV    A=4 B=0 C=5 D=5 
02996 [L1789] JMP      A=4 B=128 C=8 D=32776 target=3005
02997 [L1790] GGET     A=4 B=0 C=4 D=4 'd_ms'
02998 [L1790] KSTR     A=5 B=2 C=0 D=512 'd_wakeUI'
02999 [L1790] TGETV    A=4 B=4 C=5 D=1029 
03000 [L1790] KSTR     A=5 B=2 C=20 D=532 'onReplaceResult'
03001 [L1790] TGETV    A=4 B=4 C=5 D=1029 
03002 [L1790] MOV      A=5 B=0 C=3 D=3 
03003 [L1790] CALL     A=4 B=1 C=2 D=258 
03004 [L1790] JMP      A=4 B=129 C=9 D=33033 target=3270
03005 [L1791] TGETS    A=4 B=1 C=2 D=258 'id'
03006 [L1791] GGET     A=5 B=1 C=9 D=265 'e_t'
03007 [L1791] KSTR     A=6 B=2 C=21 D=533 'lock_item_info'
03008 [L1791] TGETV    A=5 B=5 C=6 D=1286 
03009 [L1791] ISNEV    A=4 B=0 C=5 D=5 
03010 [L1791] JMP      A=4 B=128 C=8 D=32776 target=3019
03011 [L1792] GGET     A=4 B=0 C=4 D=4 'd_ms'
03012 [L1792] TGETS    A=4 B=4 C=8 D=1032 'd_packageUI'
03013 [L1792] KSTR     A=5 B=2 C=22 D=534 'addStarLockInfo'
03014 [L1792] TGETV    A=4 B=4 C=5 D=1029 
03015 [L1792] KNIL     A=5 B=0 C=6 D=6 
03016 [L1792] KPRI     A=7 B=0 C=2 D=2 
03017 [L1792] CALL     A=4 B=1 C=4 D=260 
03018 [L1792] JMP      A=4 B=128 C=251 D=33019 target=3270
03019 [L1793] TGETS    A=4 B=1 C=2 D=258 'id'
03020 [L1793] GGET     A=5 B=1 C=9 D=265 'e_t'
03021 [L1793] KSTR     A=6 B=2 C=23 D=535 'cross_camp_info'
03022 [L1793] TGETV    A=5 B=5 C=6 D=1286 
03023 [L1793] ISNEV    A=4 B=0 C=5 D=5 
03024 [L1793] JMP      A=4 B=128 C=42 D=32810 target=3067
03025 [L1794] TGETS    A=4 B=3 C=7 D=775 'flag'
03026 [L1794] GGET     A=5 B=0 C=4 D=4 'd_ms'
03027 [L1794] TGETS    A=5 B=5 C=21 D=1301 'd_common_def'
03028 [L1794] KSTR     A=6 B=2 C=24 D=536 'cross_camp_op_type'
03029 [L1794] TGETV    A=5 B=5 C=6 D=1286 
03030 [L1794] KSTR     A=6 B=2 C=25 D=537 'camp_fight'
03031 [L1794] TGETV    A=5 B=5 C=6 D=1286 
03032 [L1794] ISNEV    A=4 B=0 C=5 D=5 
03033 [L1794] JMP      A=4 B=128 C=25 D=32793 target=3059
03034 [L1795] KSTR     A=4 B=2 C=26 D=538 'result'
03035 [L1795] TGETV    A=4 B=3 C=4 D=772 
03036 [L1795] ISNEN    A=4 B=0 C=1 D=1 1
03037 [L1795] JMP      A=4 B=128 C=11 D=32779 target=3049
03038 [L1796] GGET     A=4 B=0 C=4 D=4 'd_ms'
03039 [L1796] TGETS    A=4 B=4 C=236 D=1260 'd_fightUI'
03040 [L1796] TGETS    A=4 B=4 C=238 D=1262 'g_fightUI'
03041 [L1796] KSTR     A=5 B=2 C=27 D=539 'final_grab_info'
03042 [L1796] KSTR     A=6 B=2 C=28 D=540 'grab_info'
03043 [L1796] TGETV    A=6 B=3 C=6 D=774 
03044 [L1796] IST      A=0 B=0 C=6 D=6 
03045 [L1796] JMP      A=7 B=128 C=1 D=32769 target=3047
03046 [L1796] TNEW     A=6 B=0 C=0 D=0 
03047 [L1796] TSETV    A=6 B=4 C=5 D=1029 
03048 [L1796] JMP      A=4 B=128 C=221 D=32989 target=3270
03049 [L1798] GGET     A=4 B=0 C=4 D=4 'd_ms'
03050 [L1798] TGETS    A=4 B=4 C=25 D=1049 'd_info'
03051 [L1798] TGETS    A=4 B=4 C=9 D=1033 'show'
03052 [L1798] GGET     A=5 B=0 C=4 D=4 'd_ms'
03053 [L1798] TGETS    A=5 B=5 C=38 D=1318 'd_hz'
03054 [L1798] TGETS    A=5 B=5 C=39 D=1319 'gethz'
03055 [L1798] KSTR     A=6 B=2 C=29 D=541 'operation_failed'
03056 [L1798] CALL     A=5 B=0 C=2 D=2 
03057 [L1798] CALLM    A=4 B=1 C=0 D=256 
03058 [L1799] JMP      A=4 B=128 C=211 D=32979 target=3270
03059 [L1801] GGET     A=4 B=0 C=4 D=4 'd_ms'
03060 [L1801] KSTR     A=5 B=2 C=30 D=542 'd_crossServerUI'
03061 [L1801] TGETV    A=4 B=4 C=5 D=1029 
03062 [L1801] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
03063 [L1801] TGETV    A=4 B=4 C=5 D=1029 
03064 [L1801] MOV      A=5 B=0 C=3 D=3 
03065 [L1801] CALL     A=4 B=1 C=2 D=258 
03066 [L1802] JMP      A=4 B=128 C=203 D=32971 target=3270
03067 [L1803] TGETS    A=4 B=1 C=2 D=258 'id'
03068 [L1803] GGET     A=5 B=1 C=9 D=265 'e_t'
03069 [L1803] KSTR     A=6 B=2 C=31 D=543 'sky_pavilion_event'
03070 [L1803] TGETV    A=5 B=5 C=6 D=1286 
03071 [L1803] ISNEV    A=4 B=0 C=5 D=5 
03072 [L1803] JMP      A=4 B=128 C=8 D=32776 target=3081
03073 [L1804] GGET     A=4 B=0 C=4 D=4 'd_ms'
03074 [L1804] KSTR     A=5 B=2 C=32 D=544 'd_destinyUI'
03075 [L1804] TGETV    A=4 B=4 C=5 D=1029 
03076 [L1804] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
03077 [L1804] TGETV    A=4 B=4 C=5 D=1029 
03078 [L1804] MOV      A=5 B=0 C=3 D=3 
03079 [L1804] CALL     A=4 B=1 C=2 D=258 
03080 [L1804] JMP      A=4 B=128 C=189 D=32957 target=3270
03081 [L1805] TGETS    A=4 B=1 C=2 D=258 'id'
03082 [L1805] GGET     A=5 B=1 C=9 D=265 'e_t'
03083 [L1805] KSTR     A=6 B=2 C=33 D=545 'hero_back_event'
03084 [L1805] TGETV    A=5 B=5 C=6 D=1286 
03085 [L1805] ISNEV    A=4 B=0 C=5 D=5 
03086 [L1805] JMP      A=4 B=128 C=8 D=32776 target=3095
03087 [L1806] GGET     A=4 B=0 C=4 D=4 'd_ms'
03088 [L1806] KSTR     A=5 B=2 C=34 D=546 'd_returnUI'
03089 [L1806] TGETV    A=4 B=4 C=5 D=1029 
03090 [L1806] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
03091 [L1806] TGETV    A=4 B=4 C=5 D=1029 
03092 [L1806] MOV      A=5 B=0 C=3 D=3 
03093 [L1806] CALL     A=4 B=1 C=2 D=258 
03094 [L1806] JMP      A=4 B=128 C=175 D=32943 target=3270
03095 [L1807] TGETS    A=4 B=1 C=2 D=258 'id'
03096 [L1807] GGET     A=5 B=1 C=9 D=265 'e_t'
03097 [L1807] KSTR     A=6 B=2 C=35 D=547 'save_monkey_event'
03098 [L1807] TGETV    A=5 B=5 C=6 D=1286 
03099 [L1807] ISNEV    A=4 B=0 C=5 D=5 
03100 [L1807] JMP      A=4 B=128 C=8 D=32776 target=3109
03101 [L1808] GGET     A=4 B=0 C=4 D=4 'd_ms'
03102 [L1808] KSTR     A=5 B=2 C=36 D=548 'd_saveMonkeyUI'
03103 [L1808] TGETV    A=4 B=4 C=5 D=1029 
03104 [L1808] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
03105 [L1808] TGETV    A=4 B=4 C=5 D=1029 
03106 [L1808] MOV      A=5 B=0 C=3 D=3 
03107 [L1808] CALL     A=4 B=1 C=2 D=258 
03108 [L1808] JMP      A=4 B=128 C=161 D=32929 target=3270
03109 [L1809] TGETS    A=4 B=1 C=2 D=258 'id'
03110 [L1809] GGET     A=5 B=1 C=9 D=265 'e_t'
03111 [L1809] KSTR     A=6 B=2 C=37 D=549 'daily_active_event'
03112 [L1809] TGETV    A=5 B=5 C=6 D=1286 
03113 [L1809] ISNEV    A=4 B=0 C=5 D=5 
03114 [L1809] JMP      A=4 B=128 C=7 D=32775 target=3122
03115 [L1810] GGET     A=4 B=0 C=4 D=4 'd_ms'
03116 [L1810] TGETS    A=4 B=4 C=143 D=1167 'd_checkinUI'
03117 [L1810] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
03118 [L1810] TGETV    A=4 B=4 C=5 D=1029 
03119 [L1810] MOV      A=5 B=0 C=3 D=3 
03120 [L1810] CALL     A=4 B=1 C=2 D=258 
03121 [L1810] JMP      A=4 B=128 C=148 D=32916 target=3270
03122 [L1811] TGETS    A=4 B=1 C=2 D=258 'id'
03123 [L1811] GGET     A=5 B=1 C=9 D=265 'e_t'
03124 [L1811] KSTR     A=6 B=2 C=38 D=550 'free_fight_event'
03125 [L1811] TGETV    A=5 B=5 C=6 D=1286 
03126 [L1811] ISNEV    A=4 B=0 C=5 D=5 
03127 [L1811] JMP      A=4 B=128 C=8 D=32776 target=3136
03128 [L1812] GGET     A=4 B=0 C=4 D=4 'd_ms'
03129 [L1812] KSTR     A=5 B=1 C=210 D=466 'd_arenaUI'
03130 [L1812] TGETV    A=4 B=4 C=5 D=1029 
03131 [L1812] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
03132 [L1812] TGETV    A=4 B=4 C=5 D=1029 
03133 [L1812] MOV      A=5 B=0 C=3 D=3 
03134 [L1812] CALL     A=4 B=1 C=2 D=258 
03135 [L1812] JMP      A=4 B=128 C=134 D=32902 target=3270
03136 [L1813] TGETS    A=4 B=1 C=2 D=258 'id'
03137 [L1813] GGET     A=5 B=1 C=9 D=265 'e_t'
03138 [L1813] KSTR     A=6 B=2 C=39 D=551 'rulai_table_activity'
03139 [L1813] TGETV    A=5 B=5 C=6 D=1286 
03140 [L1813] ISNEV    A=4 B=0 C=5 D=5 
03141 [L1813] JMP      A=4 B=128 C=8 D=32776 target=3150
03142 [L1814] GGET     A=4 B=0 C=4 D=4 'd_ms'
03143 [L1814] KSTR     A=5 B=2 C=40 D=552 'd_turntableUI'
03144 [L1814] TGETV    A=4 B=4 C=5 D=1029 
03145 [L1814] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
03146 [L1814] TGETV    A=4 B=4 C=5 D=1029 
03147 [L1814] MOV      A=5 B=0 C=3 D=3 
03148 [L1814] CALL     A=4 B=1 C=2 D=258 
03149 [L1814] JMP      A=4 B=128 C=120 D=32888 target=3270
03150 [L1815] TGETS    A=4 B=1 C=2 D=258 'id'
03151 [L1815] GGET     A=5 B=1 C=9 D=265 'e_t'
03152 [L1815] KSTR     A=6 B=2 C=41 D=553 'equip_rising_star_refund'
03153 [L1815] TGETV    A=5 B=5 C=6 D=1286 
03154 [L1815] ISNEV    A=4 B=0 C=5 D=5 
03155 [L1815] JMP      A=4 B=128 C=17 D=32785 target=3173
03156 [L1816] KSTR     A=4 B=2 C=42 D=554 'attach_list'
03157 [L1816] TGETV    A=4 B=3 C=4 D=772 
03158 [L1816] LEN      A=4 B=0 C=4 D=4 
03159 [L1816] KSHORT   A=5 B=0 C=0 D=0 0
03160 [L1816] ISGE     A=5 B=0 C=4 D=4 
03161 [L1816] JMP      A=4 B=128 C=6 D=32774 target=3168
03162 [L1817] GGET     A=4 B=0 C=4 D=4 'd_ms'
03163 [L1817] TGETS    A=4 B=4 C=89 D=1113 'd_skillUpgradeUI'
03164 [L1817] KSTR     A=5 B=2 C=43 D=555 'showReturnItem'
03165 [L1817] TGETV    A=4 B=4 C=5 D=1029 
03166 [L1817] MOV      A=5 B=0 C=3 D=3 
03167 [L1817] CALL     A=4 B=1 C=2 D=258 
03168 [L1819] GGET     A=4 B=0 C=4 D=4 'd_ms'
03169 [L1819] TGETS    A=4 B=4 C=15 D=1039 'd_charPositionUI'
03170 [L1819] TGETS    A=4 B=4 C=20 D=1044 'changeCharOrderSucceed'
03171 [L1819] CALL     A=4 B=1 C=1 D=257 
03172 [L1819] JMP      A=4 B=128 C=97 D=32865 target=3270
03173 [L1820] TGETS    A=4 B=1 C=2 D=258 'id'
03174 [L1820] GGET     A=5 B=1 C=9 D=265 'e_t'
03175 [L1820] KSTR     A=6 B=2 C=44 D=556 'daily_pay_info'
03176 [L1820] TGETV    A=5 B=5 C=6 D=1286 
03177 [L1820] ISNEV    A=4 B=0 C=5 D=5 
03178 [L1820] JMP      A=4 B=128 C=58 D=32826 target=3237
03179 [L1821] TGETS    A=4 B=3 C=2 D=770 'id'
03180 [L1821] ISNEN    A=4 B=0 C=1 D=1 1
03181 [L1821] JMP      A=4 B=128 C=19 D=32787 target=3201
03182 [L1822] GGET     A=4 B=0 C=4 D=4 'd_ms'
03183 [L1822] KSTR     A=5 B=1 C=23 D=279 'd_actNoticeUI'
03184 [L1822] TGETV    A=4 B=4 C=5 D=1029 
03185 [L1822] KSTR     A=5 B=2 C=45 D=557 'setMeiridata'
03186 [L1822] TGETV    A=4 B=4 C=5 D=1029 
03187 [L1822] MOV      A=5 B=0 C=3 D=3 
03188 [L1822] CALL     A=4 B=1 C=2 D=258 
03189 [L1823] TGETS    A=4 B=3 C=1 D=769 'data'
03190 [L1823] KSTR     A=5 B=2 C=46 D=558 'isopen'
03191 [L1823] TGETV    A=4 B=4 C=5 D=1029 
03192 [L1823] ISF      A=0 B=0 C=4 D=4 
03193 [L1823] JMP      A=5 B=128 C=76 D=32844 target=3270
03194 [L1824] GGET     A=4 B=0 C=4 D=4 'd_ms'
03195 [L1824] KSTR     A=5 B=1 C=23 D=279 'd_actNoticeUI'
03196 [L1824] TGETV    A=4 B=4 C=5 D=1029 
03197 [L1824] KSTR     A=5 B=2 C=47 D=559 'showIcon'
03198 [L1824] TGETV    A=4 B=4 C=5 D=1029 
03199 [L1824] CALL     A=4 B=1 C=1 D=257 
03200 [L1825] JMP      A=4 B=128 C=69 D=32837 target=3270
03201 [L1826] TGETS    A=4 B=3 C=2 D=770 'id'
03202 [L1826] ISNEN    A=4 B=0 C=2 D=2 2
03203 [L1826] JMP      A=4 B=128 C=15 D=32783 target=3219
03204 [L1827] TNEW     A=4 B=0 C=0 D=0 
03205 [L1828] KSTR     A=5 B=2 C=42 D=554 'attach_list'
03206 [L1828] TGETS    A=6 B=3 C=1 D=769 'data'
03207 [L1828] TSETV    A=6 B=4 C=5 D=1029 
03208 [L1829] KSTR     A=5 B=2 C=26 D=538 'result'
03209 [L1829] KSHORT   A=6 B=0 C=1 D=1 1
03210 [L1829] TSETV    A=6 B=4 C=5 D=1029 
03211 [L1830] GGET     A=5 B=0 C=4 D=4 'd_ms'
03212 [L1830] KSTR     A=6 B=1 C=23 D=279 'd_actNoticeUI'
03213 [L1830] TGETV    A=5 B=5 C=6 D=1286 
03214 [L1830] KSTR     A=6 B=2 C=48 D=560 'showgetItem'
03215 [L1830] TGETV    A=5 B=5 C=6 D=1286 
03216 [L1830] MOV      A=6 B=0 C=4 D=4 
03217 [L1830] CALL     A=5 B=1 C=2 D=258 
03218 [L1830] JMP      A=4 B=128 C=51 D=32819 target=3270
03219 [L1831] TGETS    A=4 B=3 C=2 D=770 'id'
03220 [L1831] ISNEN    A=4 B=0 C=3 D=3 3
03221 [L1831] JMP      A=4 B=128 C=48 D=32816 target=3270
03222 [L1832] TNEW     A=4 B=0 C=0 D=0 
03223 [L1833] KSTR     A=5 B=2 C=42 D=554 'attach_list'
03224 [L1833] TGETS    A=6 B=3 C=1 D=769 'data'
03225 [L1833] TSETV    A=6 B=4 C=5 D=1029 
03226 [L1834] KSTR     A=5 B=2 C=26 D=538 'result'
03227 [L1834] KSHORT   A=6 B=0 C=1 D=1 1
03228 [L1834] TSETV    A=6 B=4 C=5 D=1029 
03229 [L1835] GGET     A=5 B=0 C=4 D=4 'd_ms'
03230 [L1835] KSTR     A=6 B=1 C=23 D=279 'd_actNoticeUI'
03231 [L1835] TGETV    A=5 B=5 C=6 D=1286 
03232 [L1835] KSTR     A=6 B=2 C=48 D=560 'showgetItem'
03233 [L1835] TGETV    A=5 B=5 C=6 D=1286 
03234 [L1835] MOV      A=6 B=0 C=4 D=4 
03235 [L1835] CALL     A=5 B=1 C=2 D=258 
03236 [L1836] JMP      A=4 B=128 C=33 D=32801 target=3270
03237 [L1837] TGETS    A=4 B=1 C=2 D=258 'id'
03238 [L1837] GGET     A=5 B=1 C=9 D=265 'e_t'
03239 [L1837] KSTR     A=6 B=2 C=49 D=561 'ios_pay_limit_info'
03240 [L1837] TGETV    A=5 B=5 C=6 D=1286 
03241 [L1837] ISNEV    A=4 B=0 C=5 D=5 
03242 [L1837] JMP      A=4 B=128 C=8 D=32776 target=3251
03243 [L1838] GGET     A=4 B=0 C=4 D=4 'd_ms'
03244 [L1838] KSTR     A=5 B=1 C=20 D=276 'd_rechargeUI'
03245 [L1838] TGETV    A=4 B=4 C=5 D=1029 
03246 [L1838] KSTR     A=5 B=2 C=50 D=562 'setIosLimitTime'
03247 [L1838] TGETV    A=4 B=4 C=5 D=1029 
03248 [L1838] MOV      A=5 B=0 C=3 D=3 
03249 [L1838] CALL     A=4 B=1 C=2 D=258 
03250 [L1838] JMP      A=4 B=128 C=19 D=32787 target=3270
03251 [L1839] TGETS    A=4 B=1 C=2 D=258 'id'
03252 [L1839] GGET     A=5 B=1 C=9 D=265 'e_t'
03253 [L1839] KSTR     A=6 B=2 C=51 D=563 'babel_tower_info'
03254 [L1839] TGETV    A=5 B=5 C=6 D=1286 
03255 [L1839] ISNEV    A=4 B=0 C=5 D=5 
03256 [L1839] JMP      A=4 B=128 C=8 D=32776 target=3265
03257 [L1840] GGET     A=4 B=0 C=4 D=4 'd_ms'
03258 [L1840] KSTR     A=5 B=2 C=52 D=564 'd_tongtiantaUI'
03259 [L1840] TGETV    A=4 B=4 C=5 D=1029 
03260 [L1840] KSTR     A=5 B=1 C=106 D=362 'onGetResult'
03261 [L1840] TGETV    A=4 B=4 C=5 D=1029 
03262 [L1840] MOV      A=5 B=0 C=3 D=3 
03263 [L1840] CALL     A=4 B=1 C=2 D=258 
03264 [L1840] JMP      A=4 B=128 C=5 D=32773 target=3270
03265 [L1843] UGET     A=4 B=0 C=1 D=1 cclog
03266 [L1843] KSTR     A=5 B=2 C=53 D=565 'ERROR: unhand 2998 msg, id = '
03267 [L1843] TGETS    A=6 B=1 C=2 D=258 'id'
03268 [L1843] CAT      A=5 B=5 C=6 D=1286 
03269 [L1843] CALL     A=4 B=1 C=2 D=258 
03270 [L1846] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto45 offset=0xcf73 source_lines=1862-1871 params=3
UPVALUES []
00001 [L1863] MOV      A=3 B=0 C=1 D=1 
00002 [L1864] TGETS    A=4 B=1 C=0 D=256 'show_count'
00003 [L1864] ISEQN    A=4 B=0 C=0 D=0 0
00004 [L1864] JMP      A=4 B=128 C=9 D=32777 target=14
00005 [L1865] GGET     A=4 B=0 C=1 D=1 'd_ms'
00006 [L1865] TGETS    A=4 B=4 C=2 D=1026 'd_alert'
00007 [L1865] TGETS    A=4 B=4 C=3 D=1027 'stop_wait'
00008 [L1865] CALL     A=4 B=1 C=1 D=257 
00009 [L1866] GGET     A=4 B=0 C=1 D=1 'd_ms'
00010 [L1866] TGETS    A=4 B=4 C=4 D=1028 'd_rankUI'
00011 [L1866] TGETS    A=4 B=4 C=5 D=1029 'getDateFormServer'
00012 [L1866] MOV      A=5 B=0 C=1 D=1 
00013 [L1866] CALL     A=4 B=1 C=2 D=258 
00014 [L1871] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto46 offset=0xd028 source_lines=1873-2109 params=3
UPVALUES ['cclog', 'tostring', 'math', 'string', 'pairs']
00001 [L1875] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L1875] KSTR     A=4 B=0 C=0 D=0 'call msg_modify_attr_1032'
00003 [L1875] CALL     A=3 B=1 C=2 D=258 
00004 [L1877] TGETS    A=3 B=1 C=1 D=257 'unit_type'
00005 [L1877] GGET     A=4 B=0 C=2 D=2 'o_t'
00006 [L1877] TGETS    A=4 B=4 C=3 D=1027 'cortege'
00007 [L1877] ISNEV    A=3 B=0 C=4 D=4 
00008 [L1877] JMP      A=3 B=128 C=6 D=32774 target=15
00009 [L1878] GGET     A=3 B=0 C=4 D=4 'd_ms'
00010 [L1878] TGETS    A=3 B=3 C=5 D=773 'd_lineupUI'
00011 [L1878] TGETS    A=3 B=3 C=6 D=774 'updateCharacterInfo'
00012 [L1878] MOV      A=4 B=0 C=1 D=1 
00013 [L1878] CALL     A=3 B=1 C=2 D=258 
00014 [L1878] JMP      A=3 B=132 C=27 D=33819 target=1066
00015 [L1879] TGETS    A=3 B=1 C=1 D=257 'unit_type'
00016 [L1879] GGET     A=4 B=0 C=2 D=2 'o_t'
00017 [L1879] TGETS    A=4 B=4 C=7 D=1031 'item'
00018 [L1879] ISNEV    A=3 B=0 C=4 D=4 
00019 [L1879] JMP      A=3 B=128 C=6 D=32774 target=26
00020 [L1881] GGET     A=3 B=0 C=4 D=4 'd_ms'
00021 [L1881] TGETS    A=3 B=3 C=5 D=773 'd_lineupUI'
00022 [L1881] TGETS    A=3 B=3 C=8 D=776 'updateItemInfo'
00023 [L1881] MOV      A=4 B=0 C=1 D=1 
00024 [L1881] CALL     A=3 B=1 C=2 D=258 
00025 [L1881] JMP      A=3 B=132 C=16 D=33808 target=1066
00026 [L1882] TGETS    A=3 B=1 C=1 D=257 'unit_type'
00027 [L1882] GGET     A=4 B=0 C=2 D=2 'o_t'
00028 [L1882] TGETS    A=4 B=4 C=9 D=1033 'skill'
00029 [L1882] ISNEV    A=3 B=0 C=4 D=4 
00030 [L1882] JMP      A=3 B=128 C=6 D=32774 target=37
00031 [L1883] GGET     A=3 B=0 C=4 D=4 'd_ms'
00032 [L1883] TGETS    A=3 B=3 C=5 D=773 'd_lineupUI'
00033 [L1883] TGETS    A=3 B=3 C=10 D=778 'updateSkillInfo'
00034 [L1883] MOV      A=4 B=0 C=1 D=1 
00035 [L1883] CALL     A=3 B=1 C=2 D=258 
00036 [L1883] JMP      A=3 B=132 C=5 D=33797 target=1066
00037 [L1885] TGETS    A=3 B=1 C=1 D=257 'unit_type'
00038 [L1885] GGET     A=4 B=0 C=2 D=2 'o_t'
00039 [L1885] TGETS    A=4 B=4 C=11 D=1035 'role'
00040 [L1885] ISNEV    A=3 B=0 C=4 D=4 
00041 [L1885] JMP      A=3 B=131 C=251 D=33787 target=1061
00042 [L1886] KSHORT   A=3 B=0 C=1 D=1 1
00043 [L1886] TGETS    A=4 B=1 C=12 D=268 'attr_list'
00044 [L1886] LEN      A=4 B=0 C=4 D=4 
00045 [L1886] KSHORT   A=5 B=0 C=1 D=1 1
00046 [L1886] FORI     A=3 B=131 C=245 D=33781 target=1060
00047 [L1887] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00048 [L1887] TGETV    A=7 B=7 C=6 D=1798 
00049 [L1887] TGETS    A=7 B=7 C=13 D=1805 'type'
00050 [L1887] GGET     A=8 B=0 C=14 D=14 'r_p'
00051 [L1887] TGETS    A=8 B=8 C=15 D=2063 'top_fight_count'
00052 [L1887] ISNEV    A=7 B=0 C=8 D=8 
00053 [L1887] JMP      A=7 B=128 C=54 D=32822 target=108
00054 [L1888] GGET     A=7 B=0 C=4 D=4 'd_ms'
00055 [L1888] TGETS    A=7 B=7 C=16 D=1808 'd_rankUI'
00056 [L1888] TGETS    A=7 B=7 C=17 D=1809 'g_rankInfo'
00057 [L1888] ISEQP    A=7 B=0 C=0 D=0 
00058 [L1888] JMP      A=7 B=128 C=7 D=32775 target=66
00059 [L1889] GGET     A=7 B=0 C=4 D=4 'd_ms'
00060 [L1889] TGETS    A=7 B=7 C=16 D=1808 'd_rankUI'
00061 [L1889] TGETS    A=7 B=7 C=17 D=1809 'g_rankInfo'
00062 [L1889] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00063 [L1889] TGETV    A=8 B=8 C=6 D=2054 
00064 [L1889] TGETS    A=8 B=8 C=19 D=2067 'value'
00065 [L1889] TSETS    A=8 B=7 C=18 D=1810 'fight_count'
00066 [L1892] GGET     A=7 B=0 C=4 D=4 'd_ms'
00067 [L1892] TGETS    A=7 B=7 C=20 D=1812 'd_loginUI'
00068 [L1892] TGETS    A=7 B=7 C=21 D=1813 'g_currentSence'
00069 [L1892] GGET     A=8 B=0 C=4 D=4 'd_ms'
00070 [L1892] TGETS    A=8 B=8 C=20 D=2068 'd_loginUI'
00071 [L1892] TGETS    A=8 B=8 C=22 D=2070 'senceID'
00072 [L1892] TGETS    A=8 B=8 C=23 D=2071 'adventure'
00073 [L1892] ISNEV    A=7 B=0 C=8 D=8 
00074 [L1892] JMP      A=7 B=131 C=216 D=33752 target=1059
00075 [L1893] GGET     A=7 B=0 C=4 D=4 'd_ms'
00076 [L1893] TGETS    A=7 B=7 C=24 D=1816 'd_activityUI'
00077 [L1893] TGETS    A=7 B=7 C=25 D=1817 'g_currentActivity'
00078 [L1893] GGET     A=8 B=0 C=4 D=4 'd_ms'
00079 [L1893] TGETS    A=8 B=8 C=24 D=2072 'd_activityUI'
00080 [L1893] TGETS    A=8 B=8 C=26 D=2074 'activityID'
00081 [L1893] TGETS    A=8 B=8 C=27 D=2075 'fengshenbang'
00082 [L1893] ISNEV    A=7 B=0 C=8 D=8 
00083 [L1893] JMP      A=7 B=131 C=207 D=33743 target=1059
00084 [L1894] GGET     A=7 B=0 C=4 D=4 'd_ms'
00085 [L1894] TGETS    A=7 B=7 C=16 D=1808 'd_rankUI'
00086 [L1894] TGETS    A=7 B=7 C=17 D=1809 'g_rankInfo'
00087 [L1894] TGETS    A=7 B=7 C=18 D=1810 'fight_count'
00088 [L1895] GGET     A=8 B=0 C=4 D=4 'd_ms'
00089 [L1895] TGETS    A=8 B=8 C=28 D=2076 'd_hz'
00090 [L1895] TGETS    A=8 B=8 C=29 D=2077 'gethz'
00091 [L1895] KSTR     A=9 B=0 C=30 D=30 'fengshenbang_rank_challenge_count'
00092 [L1895] CALL     A=8 B=2 C=2 D=514 
00093 [L1895] KSTR     A=9 B=0 C=31 D=31 ' : '
00094 [L1895] UGET     A=10 B=0 C=1 D=1 tostring
00095 [L1895] MOV      A=11 B=0 C=7 D=7 
00096 [L1895] CALL     A=10 B=2 C=2 D=514 
00097 [L1895] CAT      A=8 B=8 C=10 D=2058 
00098 [L1896] GGET     A=9 B=0 C=4 D=4 'd_ms'
00099 [L1896] TGETS    A=9 B=9 C=16 D=2320 'd_rankUI'
00100 [L1896] TGETS    A=9 B=9 C=32 D=2336 'g_rankUI'
00101 [L1896] TGETS    A=9 B=9 C=33 D=2337 'show_labels'
00102 [L1896] TGETS    A=9 B=9 C=34 D=2338 'challenge_count_label'
00103 [L1896] MOV      A=10 B=0 C=9 D=9 
00104 [L1896] TGETS    A=9 B=9 C=35 D=2339 'setString'
00105 [L1896] MOV      A=11 B=0 C=8 D=8 
00106 [L1896] CALL     A=9 B=1 C=3 D=259 
00107 [L1897] JMP      A=7 B=131 C=183 D=33719 target=1059
00108 [L1899] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00109 [L1899] TGETV    A=7 B=7 C=6 D=1798 
00110 [L1899] TGETS    A=7 B=7 C=13 D=1805 'type'
00111 [L1899] GGET     A=8 B=0 C=14 D=14 'r_p'
00112 [L1899] TGETS    A=8 B=8 C=36 D=2084 'silver_coin'
00113 [L1899] ISNEV    A=7 B=0 C=8 D=8 
00114 [L1899] JMP      A=7 B=128 C=106 D=32874 target=221
00115 [L1900] UGET     A=7 B=0 C=2 D=2 math
00116 [L1900] TGETS    A=7 B=7 C=37 D=1829 'floor'
00117 [L1900] GGET     A=8 B=0 C=4 D=4 'd_ms'
00118 [L1900] TGETS    A=8 B=8 C=38 D=2086 'd_mainUI'
00119 [L1900] TGETS    A=8 B=8 C=39 D=2087 'g_playerInfo'
00120 [L1900] TGETS    A=8 B=8 C=36 D=2084 'silver_coin'
00121 [L1900] CALL     A=7 B=2 C=2 D=514 
00122 [L1901] GGET     A=8 B=0 C=4 D=4 'd_ms'
00123 [L1901] TGETS    A=8 B=8 C=38 D=2086 'd_mainUI'
00124 [L1901] TGETS    A=8 B=8 C=39 D=2087 'g_playerInfo'
00125 [L1901] UGET     A=9 B=0 C=2 D=2 math
00126 [L1901] TGETS    A=9 B=9 C=37 D=2341 'floor'
00127 [L1901] TGETS    A=10 B=1 C=12 D=268 'attr_list'
00128 [L1901] TGETV    A=10 B=10 C=6 D=2566 
00129 [L1901] TGETS    A=10 B=10 C=19 D=2579 'value'
00130 [L1901] CALL     A=9 B=2 C=2 D=514 
00131 [L1901] SUBVV    A=9 B=9 C=7 D=2311 
00132 [L1901] TSETS    A=9 B=8 C=40 D=2088 'increasedMoney'
00133 [L1902] GGET     A=8 B=0 C=4 D=4 'd_ms'
00134 [L1902] TGETS    A=8 B=8 C=38 D=2086 'd_mainUI'
00135 [L1902] TGETS    A=8 B=8 C=39 D=2087 'g_playerInfo'
00136 [L1902] UGET     A=9 B=0 C=2 D=2 math
00137 [L1902] TGETS    A=9 B=9 C=37 D=2341 'floor'
00138 [L1902] TGETS    A=10 B=1 C=12 D=268 'attr_list'
00139 [L1902] TGETV    A=10 B=10 C=6 D=2566 
00140 [L1902] TGETS    A=10 B=10 C=19 D=2579 'value'
00141 [L1902] CALL     A=9 B=2 C=2 D=514 
00142 [L1902] TSETS    A=9 B=8 C=36 D=2084 'silver_coin'
00143 [L1904] GGET     A=8 B=0 C=4 D=4 'd_ms'
00144 [L1904] TGETS    A=8 B=8 C=38 D=2086 'd_mainUI'
00145 [L1904] TGETS    A=8 B=8 C=39 D=2087 'g_playerInfo'
00146 [L1904] TGETS    A=8 B=8 C=36 D=2084 'silver_coin'
00147 [L1904] KSHORT   A=9 B=0 C=0 D=0 0
00148 [L1904] ISGE     A=8 B=0 C=9 D=9 
00149 [L1904] JMP      A=8 B=128 C=5 D=32773 target=155
00150 [L1905] GGET     A=8 B=0 C=4 D=4 'd_ms'
00151 [L1905] TGETS    A=8 B=8 C=38 D=2086 'd_mainUI'
00152 [L1905] TGETS    A=8 B=8 C=39 D=2087 'g_playerInfo'
00153 [L1905] KNUM     A=9 B=0 C=0 D=0 2000000000
00154 [L1905] TSETS    A=9 B=8 C=36 D=2084 'silver_coin'
00155 [L1908] GGET     A=8 B=0 C=4 D=4 'd_ms'
00156 [L1908] TGETS    A=8 B=8 C=20 D=2068 'd_loginUI'
00157 [L1908] TGETS    A=8 B=8 C=21 D=2069 'g_currentSence'
00158 [L1908] GGET     A=9 B=0 C=4 D=4 'd_ms'
00159 [L1908] TGETS    A=9 B=9 C=20 D=2324 'd_loginUI'
00160 [L1908] TGETS    A=9 B=9 C=22 D=2326 'senceID'
00161 [L1908] TGETS    A=9 B=9 C=41 D=2345 'mainUI'
00162 [L1908] ISNEV    A=8 B=0 C=9 D=9 
00163 [L1908] JMP      A=8 B=128 C=17 D=32785 target=181
00164 [L1909] GGET     A=8 B=0 C=4 D=4 'd_ms'
00165 [L1909] TGETS    A=8 B=8 C=38 D=2086 'd_mainUI'
00166 [L1909] TGETS    A=8 B=8 C=42 D=2090 'g_mainUI'
00167 [L1909] TGETS    A=8 B=8 C=43 D=2091 'playerInfoTab'
00168 [L1909] TGETS    A=8 B=8 C=44 D=2092 'money_label'
00169 [L1909] MOV      A=9 B=0 C=8 D=8 
00170 [L1909] TGETS    A=8 B=8 C=35 D=2083 'setString'
00171 [L1909] UGET     A=10 B=0 C=3 D=3 string
00172 [L1909] TGETS    A=10 B=10 C=45 D=2605 'format'
00173 [L1909] KSTR     A=11 B=0 C=46 D=46 '%d'
00174 [L1909] GGET     A=12 B=0 C=4 D=4 'd_ms'
00175 [L1909] TGETS    A=12 B=12 C=38 D=3110 'd_mainUI'
00176 [L1909] TGETS    A=12 B=12 C=39 D=3111 'g_playerInfo'
00177 [L1909] TGETS    A=12 B=12 C=36 D=3108 'silver_coin'
00178 [L1909] CALL     A=10 B=0 C=3 D=3 
00179 [L1909] CALLM    A=8 B=1 C=1 D=257 
00180 [L1909] JMP      A=8 B=131 C=110 D=33646 target=1059
00181 [L1910] GGET     A=8 B=0 C=4 D=4 'd_ms'
00182 [L1910] TGETS    A=8 B=8 C=20 D=2068 'd_loginUI'
00183 [L1910] TGETS    A=8 B=8 C=21 D=2069 'g_currentSence'
00184 [L1910] GGET     A=9 B=0 C=4 D=4 'd_ms'
00185 [L1910] TGETS    A=9 B=9 C=20 D=2324 'd_loginUI'
00186 [L1910] TGETS    A=9 B=9 C=22 D=2326 'senceID'
00187 [L1910] TGETS    A=9 B=9 C=47 D=2351 'mapUI'
00188 [L1910] ISNEV    A=8 B=0 C=9 D=9 
00189 [L1910] JMP      A=8 B=128 C=17 D=32785 target=207
00190 [L1911] GGET     A=8 B=0 C=4 D=4 'd_ms'
00191 [L1911] TGETS    A=8 B=8 C=48 D=2096 'd_mapUI'
00192 [L1911] TGETS    A=8 B=8 C=49 D=2097 'g_mapUI'
00193 [L1911] TGETS    A=8 B=8 C=43 D=2091 'playerInfoTab'
00194 [L1911] TGETS    A=8 B=8 C=44 D=2092 'money_label'
00195 [L1911] MOV      A=9 B=0 C=8 D=8 
00196 [L1911] TGETS    A=8 B=8 C=35 D=2083 'setString'
00197 [L1911] UGET     A=10 B=0 C=3 D=3 string
00198 [L1911] TGETS    A=10 B=10 C=45 D=2605 'format'
00199 [L1911] KSTR     A=11 B=0 C=46 D=46 '%d'
00200 [L1911] GGET     A=12 B=0 C=4 D=4 'd_ms'
00201 [L1911] TGETS    A=12 B=12 C=38 D=3110 'd_mainUI'
00202 [L1911] TGETS    A=12 B=12 C=39 D=3111 'g_playerInfo'
00203 [L1911] TGETS    A=12 B=12 C=36 D=3108 'silver_coin'
00204 [L1911] CALL     A=10 B=0 C=3 D=3 
00205 [L1911] CALLM    A=8 B=1 C=1 D=257 
00206 [L1911] JMP      A=8 B=131 C=84 D=33620 target=1059
00207 [L1912] GGET     A=8 B=0 C=4 D=4 'd_ms'
00208 [L1912] TGETS    A=8 B=8 C=20 D=2068 'd_loginUI'
00209 [L1912] TGETS    A=8 B=8 C=21 D=2069 'g_currentSence'
00210 [L1912] GGET     A=9 B=0 C=4 D=4 'd_ms'
00211 [L1912] TGETS    A=9 B=9 C=20 D=2324 'd_loginUI'
00212 [L1912] TGETS    A=9 B=9 C=22 D=2326 'senceID'
00213 [L1912] TGETS    A=9 B=9 C=23 D=2327 'adventure'
00214 [L1912] ISNEV    A=8 B=0 C=9 D=9 
00215 [L1912] JMP      A=8 B=131 C=75 D=33611 target=1059
00216 [L1913] GGET     A=8 B=0 C=4 D=4 'd_ms'
00217 [L1913] TGETS    A=8 B=8 C=24 D=2072 'd_activityUI'
00218 [L1913] TGETS    A=8 B=8 C=50 D=2098 'updateMoney'
00219 [L1913] CALL     A=8 B=1 C=1 D=257 
00220 [L1914] JMP      A=7 B=131 C=70 D=33606 target=1059
00221 [L1916] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00222 [L1916] TGETV    A=7 B=7 C=6 D=1798 
00223 [L1916] TGETS    A=7 B=7 C=13 D=1805 'type'
00224 [L1916] GGET     A=8 B=0 C=14 D=14 'r_p'
00225 [L1916] TGETS    A=8 B=8 C=51 D=2099 'role_max_hp_plus'
00226 [L1916] ISNEV    A=7 B=0 C=8 D=8 
00227 [L1916] JMP      A=7 B=128 C=8 D=32776 target=236
00228 [L1917] GGET     A=7 B=0 C=4 D=4 'd_ms'
00229 [L1917] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00230 [L1917] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00231 [L1917] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00232 [L1917] TGETV    A=8 B=8 C=6 D=2054 
00233 [L1917] TGETS    A=8 B=8 C=19 D=2067 'value'
00234 [L1917] TSETS    A=8 B=7 C=52 D=1844 'max_hp_plus'
00235 [L1917] JMP      A=7 B=131 C=55 D=33591 target=1059
00236 [L1919] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00237 [L1919] TGETV    A=7 B=7 C=6 D=1798 
00238 [L1919] TGETS    A=7 B=7 C=13 D=1805 'type'
00239 [L1919] GGET     A=8 B=0 C=14 D=14 'r_p'
00240 [L1919] TGETS    A=8 B=8 C=53 D=2101 'role_max_magic_plus'
00241 [L1919] ISNEV    A=7 B=0 C=8 D=8 
00242 [L1919] JMP      A=7 B=128 C=8 D=32776 target=251
00243 [L1920] GGET     A=7 B=0 C=4 D=4 'd_ms'
00244 [L1920] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00245 [L1920] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00246 [L1920] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00247 [L1920] TGETV    A=8 B=8 C=6 D=2054 
00248 [L1920] TGETS    A=8 B=8 C=19 D=2067 'value'
00249 [L1920] TSETS    A=8 B=7 C=54 D=1846 'max_magic_plus'
00250 [L1920] JMP      A=7 B=131 C=40 D=33576 target=1059
00251 [L1922] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00252 [L1922] TGETV    A=7 B=7 C=6 D=1798 
00253 [L1922] TGETS    A=7 B=7 C=13 D=1805 'type'
00254 [L1922] GGET     A=8 B=0 C=14 D=14 'r_p'
00255 [L1922] TGETS    A=8 B=8 C=55 D=2103 'role_wuligongji_plus'
00256 [L1922] ISNEV    A=7 B=0 C=8 D=8 
00257 [L1922] JMP      A=7 B=128 C=8 D=32776 target=266
00258 [L1923] GGET     A=7 B=0 C=4 D=4 'd_ms'
00259 [L1923] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00260 [L1923] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00261 [L1923] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00262 [L1923] TGETV    A=8 B=8 C=6 D=2054 
00263 [L1923] TGETS    A=8 B=8 C=19 D=2067 'value'
00264 [L1923] TSETS    A=8 B=7 C=56 D=1848 'gongji_plus'
00265 [L1923] JMP      A=7 B=131 C=25 D=33561 target=1059
00266 [L1925] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00267 [L1925] TGETV    A=7 B=7 C=6 D=1798 
00268 [L1925] TGETS    A=7 B=7 C=13 D=1805 'type'
00269 [L1925] GGET     A=8 B=0 C=14 D=14 'r_p'
00270 [L1925] TGETS    A=8 B=8 C=57 D=2105 'role_wulifangyu_plus'
00271 [L1925] ISNEV    A=7 B=0 C=8 D=8 
00272 [L1925] JMP      A=7 B=128 C=8 D=32776 target=281
00273 [L1926] GGET     A=7 B=0 C=4 D=4 'd_ms'
00274 [L1926] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00275 [L1926] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00276 [L1926] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00277 [L1926] TGETV    A=8 B=8 C=6 D=2054 
00278 [L1926] TGETS    A=8 B=8 C=19 D=2067 'value'
00279 [L1926] TSETS    A=8 B=7 C=58 D=1850 'fangyu_plus'
00280 [L1926] JMP      A=7 B=131 C=10 D=33546 target=1059
00281 [L1928] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00282 [L1928] TGETV    A=7 B=7 C=6 D=1798 
00283 [L1928] TGETS    A=7 B=7 C=13 D=1805 'type'
00284 [L1928] GGET     A=8 B=0 C=14 D=14 'r_p'
00285 [L1928] TGETS    A=8 B=8 C=59 D=2107 'addition_rule_index'
00286 [L1928] ISNEV    A=7 B=0 C=8 D=8 
00287 [L1928] JMP      A=7 B=128 C=8 D=32776 target=296
00288 [L1929] GGET     A=7 B=0 C=4 D=4 'd_ms'
00289 [L1929] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00290 [L1929] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00291 [L1929] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00292 [L1929] TGETV    A=8 B=8 C=6 D=2054 
00293 [L1929] TGETS    A=8 B=8 C=19 D=2067 'value'
00294 [L1929] TSETS    A=8 B=7 C=60 D=1852 'rule_index'
00295 [L1929] JMP      A=7 B=130 C=251 D=33531 target=1059
00296 [L1937] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00297 [L1937] TGETV    A=7 B=7 C=6 D=1798 
00298 [L1937] TGETS    A=7 B=7 C=13 D=1805 'type'
00299 [L1937] GGET     A=8 B=0 C=14 D=14 'r_p'
00300 [L1937] TGETS    A=8 B=8 C=61 D=2109 'level'
00301 [L1937] ISNEV    A=7 B=0 C=8 D=8 
00302 [L1937] JMP      A=7 B=128 C=55 D=32823 target=358
00303 [L1938] GGET     A=7 B=0 C=4 D=4 'd_ms'
00304 [L1938] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00305 [L1938] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00306 [L1938] TGETS    A=7 B=7 C=61 D=1853 'level'
00307 [L1940] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00308 [L1940] TGETV    A=8 B=8 C=6 D=2054 
00309 [L1940] TGETS    A=8 B=8 C=19 D=2067 'value'
00310 [L1940] ISNEN    A=8 B=0 C=1 D=1 5
00311 [L1940] JMP      A=8 B=128 C=4 D=32772 target=316
00312 [L1941] GGET     A=8 B=0 C=4 D=4 'd_ms'
00313 [L1941] TGETS    A=8 B=8 C=62 D=2110 'd_playerInfoUI'
00314 [L1941] KPRI     A=9 B=0 C=2 D=2 
00315 [L1941] TSETS    A=9 B=8 C=63 D=2111 'g_isNeedHintPractice'
00316 [L1944] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00317 [L1944] TGETV    A=8 B=8 C=6 D=2054 
00318 [L1944] TGETS    A=8 B=8 C=19 D=2067 'value'
00319 [L1944] KSHORT   A=9 B=0 C=5 D=5 5
00320 [L1944] ISGT     A=9 B=0 C=8 D=8 
00321 [L1944] JMP      A=8 B=128 C=28 D=32796 target=350
00322 [L1946] GGET     A=8 B=0 C=4 D=4 'd_ms'
00323 [L1946] TGETS    A=8 B=8 C=38 D=2086 'd_mainUI'
00324 [L1946] KPRI     A=9 B=0 C=1 D=1 
00325 [L1946] TSETS    A=9 B=8 C=64 D=2112 'g_isNeedHint'
00326 [L1947] GGET     A=8 B=0 C=4 D=4 'd_ms'
00327 [L1947] TGETS    A=8 B=8 C=62 D=2110 'd_playerInfoUI'
00328 [L1947] KPRI     A=9 B=0 C=2 D=2 
00329 [L1947] TSETS    A=9 B=8 C=65 D=2113 'g_playHintAnimate'
00330 [L1949] GGET     A=8 B=0 C=4 D=4 'd_ms'
00331 [L1949] TGETS    A=8 B=8 C=38 D=2086 'd_mainUI'
00332 [L1949] TGETS    A=8 B=8 C=39 D=2087 'g_playerInfo'
00333 [L1949] TGETS    A=9 B=1 C=12 D=268 'attr_list'
00334 [L1949] TGETV    A=9 B=9 C=6 D=2310 
00335 [L1949] TGETS    A=9 B=9 C=19 D=2323 'value'
00336 [L1949] SUBVV    A=9 B=9 C=7 D=2311 
00337 [L1949] TSETS    A=9 B=8 C=66 D=2114 'increasedLevel'
00338 [L1950] GGET     A=8 B=0 C=4 D=4 'd_ms'
00339 [L1950] TGETS    A=8 B=8 C=38 D=2086 'd_mainUI'
00340 [L1950] TGETS    A=8 B=8 C=39 D=2087 'g_playerInfo'
00341 [L1950] TGETS    A=8 B=8 C=66 D=2114 'increasedLevel'
00342 [L1950] KSHORT   A=9 B=0 C=0 D=0 0
00343 [L1950] ISGE     A=9 B=0 C=8 D=8 
00344 [L1950] JMP      A=8 B=128 C=5 D=32773 target=350
00345 [L1951] GGET     A=8 B=0 C=4 D=4 'd_ms'
00346 [L1951] TGETS    A=8 B=8 C=38 D=2086 'd_mainUI'
00347 [L1951] TGETS    A=8 B=8 C=39 D=2087 'g_playerInfo'
00348 [L1951] KPRI     A=9 B=0 C=2 D=2 
00349 [L1951] TSETS    A=9 B=8 C=67 D=2115 'isHintPractice'
00350 [L1954] GGET     A=8 B=0 C=4 D=4 'd_ms'
00351 [L1954] TGETS    A=8 B=8 C=38 D=2086 'd_mainUI'
00352 [L1954] TGETS    A=8 B=8 C=39 D=2087 'g_playerInfo'
00353 [L1954] TGETS    A=9 B=1 C=12 D=268 'attr_list'
00354 [L1954] TGETV    A=9 B=9 C=6 D=2310 
00355 [L1954] TGETS    A=9 B=9 C=19 D=2323 'value'
00356 [L1954] TSETS    A=9 B=8 C=61 D=2109 'level'
00357 [L1954] JMP      A=7 B=130 C=189 D=33469 target=1059
00358 [L1956] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00359 [L1956] TGETV    A=7 B=7 C=6 D=1798 
00360 [L1956] TGETS    A=7 B=7 C=13 D=1805 'type'
00361 [L1956] GGET     A=8 B=0 C=14 D=14 'r_p'
00362 [L1956] TGETS    A=8 B=8 C=68 D=2116 'strength'
00363 [L1956] ISNEV    A=7 B=0 C=8 D=8 
00364 [L1956] JMP      A=7 B=128 C=30 D=32798 target=395
00365 [L1957] GGET     A=7 B=0 C=4 D=4 'd_ms'
00366 [L1957] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00367 [L1957] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00368 [L1957] TGETS    A=7 B=7 C=68 D=1860 'strength'
00369 [L1957] ISF      A=0 B=0 C=7 D=7 
00370 [L1957] JMP      A=8 B=130 C=176 D=33456 target=1059
00371 [L1958] GGET     A=7 B=0 C=4 D=4 'd_ms'
00372 [L1958] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00373 [L1958] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00374 [L1958] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00375 [L1958] TGETV    A=8 B=8 C=6 D=2054 
00376 [L1958] TGETS    A=8 B=8 C=19 D=2067 'value'
00377 [L1958] GGET     A=9 B=0 C=4 D=4 'd_ms'
00378 [L1958] TGETS    A=9 B=9 C=38 D=2342 'd_mainUI'
00379 [L1958] TGETS    A=9 B=9 C=39 D=2343 'g_playerInfo'
00380 [L1958] TGETS    A=9 B=9 C=68 D=2372 'strength'
00381 [L1958] SUBVV    A=8 B=8 C=9 D=2057 
00382 [L1958] TSETS    A=8 B=7 C=69 D=1861 'increasedStr'
00383 [L1959] GGET     A=7 B=0 C=4 D=4 'd_ms'
00384 [L1959] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00385 [L1959] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00386 [L1959] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00387 [L1959] TGETV    A=8 B=8 C=6 D=2054 
00388 [L1959] TGETS    A=8 B=8 C=19 D=2067 'value'
00389 [L1959] TSETS    A=8 B=7 C=68 D=1860 'strength'
00390 [L1960] GGET     A=7 B=0 C=4 D=4 'd_ms'
00391 [L1960] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00392 [L1960] TGETS    A=7 B=7 C=70 D=1862 'updateStrength'
00393 [L1960] CALL     A=7 B=1 C=1 D=257 
00394 [L1961] JMP      A=7 B=130 C=152 D=33432 target=1059
00395 [L1963] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00396 [L1963] TGETV    A=7 B=7 C=6 D=1798 
00397 [L1963] TGETS    A=7 B=7 C=13 D=1805 'type'
00398 [L1963] GGET     A=8 B=0 C=14 D=14 'r_p'
00399 [L1963] TGETS    A=8 B=8 C=71 D=2119 'energy'
00400 [L1963] ISNEV    A=7 B=0 C=8 D=8 
00401 [L1963] JMP      A=7 B=128 C=30 D=32798 target=432
00402 [L1964] GGET     A=7 B=0 C=4 D=4 'd_ms'
00403 [L1964] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00404 [L1964] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00405 [L1964] TGETS    A=7 B=7 C=71 D=1863 'energy'
00406 [L1964] ISF      A=0 B=0 C=7 D=7 
00407 [L1964] JMP      A=8 B=130 C=139 D=33419 target=1059
00408 [L1965] GGET     A=7 B=0 C=4 D=4 'd_ms'
00409 [L1965] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00410 [L1965] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00411 [L1965] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00412 [L1965] TGETV    A=8 B=8 C=6 D=2054 
00413 [L1965] TGETS    A=8 B=8 C=19 D=2067 'value'
00414 [L1965] GGET     A=9 B=0 C=4 D=4 'd_ms'
00415 [L1965] TGETS    A=9 B=9 C=38 D=2342 'd_mainUI'
00416 [L1965] TGETS    A=9 B=9 C=39 D=2343 'g_playerInfo'
00417 [L1965] TGETS    A=9 B=9 C=71 D=2375 'energy'
00418 [L1965] SUBVV    A=8 B=8 C=9 D=2057 
00419 [L1965] TSETS    A=8 B=7 C=72 D=1864 'increasedEne'
00420 [L1966] GGET     A=7 B=0 C=4 D=4 'd_ms'
00421 [L1966] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00422 [L1966] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00423 [L1966] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00424 [L1966] TGETV    A=8 B=8 C=6 D=2054 
00425 [L1966] TGETS    A=8 B=8 C=19 D=2067 'value'
00426 [L1966] TSETS    A=8 B=7 C=71 D=1863 'energy'
00427 [L1967] GGET     A=7 B=0 C=4 D=4 'd_ms'
00428 [L1967] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00429 [L1967] TGETS    A=7 B=7 C=73 D=1865 'updateEnergy'
00430 [L1967] CALL     A=7 B=1 C=1 D=257 
00431 [L1968] JMP      A=7 B=130 C=115 D=33395 target=1059
00432 [L1970] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00433 [L1970] TGETV    A=7 B=7 C=6 D=1798 
00434 [L1970] TGETS    A=7 B=7 C=13 D=1805 'type'
00435 [L1970] GGET     A=8 B=0 C=14 D=14 'r_p'
00436 [L1970] TGETS    A=8 B=8 C=74 D=2122 'gold_coin'
00437 [L1970] ISNEV    A=7 B=0 C=8 D=8 
00438 [L1970] JMP      A=7 B=128 C=84 D=32852 target=523
00439 [L1971] GGET     A=7 B=0 C=4 D=4 'd_ms'
00440 [L1971] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00441 [L1971] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00442 [L1971] TGETS    A=7 B=7 C=74 D=1866 'gold_coin'
00443 [L1971] IST      A=0 B=0 C=7 D=7 
00444 [L1971] JMP      A=8 B=128 C=1 D=32769 target=446
00445 [L1971] KSHORT   A=7 B=0 C=0 D=0 0
00446 [L1972] GGET     A=8 B=0 C=4 D=4 'd_ms'
00447 [L1972] TGETS    A=8 B=8 C=38 D=2086 'd_mainUI'
00448 [L1972] TGETS    A=8 B=8 C=39 D=2087 'g_playerInfo'
00449 [L1972] TGETS    A=9 B=1 C=12 D=268 'attr_list'
00450 [L1972] TGETV    A=9 B=9 C=6 D=2310 
00451 [L1972] TGETS    A=9 B=9 C=19 D=2323 'value'
00452 [L1972] SUBVV    A=9 B=9 C=7 D=2311 
00453 [L1972] TSETS    A=9 B=8 C=75 D=2123 'increasedGold'
00454 [L1973] GGET     A=8 B=0 C=4 D=4 'd_ms'
00455 [L1973] TGETS    A=8 B=8 C=38 D=2086 'd_mainUI'
00456 [L1973] TGETS    A=8 B=8 C=39 D=2087 'g_playerInfo'
00457 [L1973] TGETS    A=9 B=1 C=12 D=268 'attr_list'
00458 [L1973] TGETV    A=9 B=9 C=6 D=2310 
00459 [L1973] TGETS    A=9 B=9 C=19 D=2323 'value'
00460 [L1973] TSETS    A=9 B=8 C=74 D=2122 'gold_coin'
00461 [L1974] GGET     A=8 B=0 C=4 D=4 'd_ms'
00462 [L1974] TGETS    A=8 B=8 C=20 D=2068 'd_loginUI'
00463 [L1974] TGETS    A=8 B=8 C=21 D=2069 'g_currentSence'
00464 [L1974] GGET     A=9 B=0 C=4 D=4 'd_ms'
00465 [L1974] TGETS    A=9 B=9 C=20 D=2324 'd_loginUI'
00466 [L1974] TGETS    A=9 B=9 C=22 D=2326 'senceID'
00467 [L1974] TGETS    A=9 B=9 C=41 D=2345 'mainUI'
00468 [L1974] ISNEV    A=8 B=0 C=9 D=9 
00469 [L1974] JMP      A=8 B=128 C=15 D=32783 target=485
00470 [L1975] GGET     A=8 B=0 C=4 D=4 'd_ms'
00471 [L1975] TGETS    A=8 B=8 C=38 D=2086 'd_mainUI'
00472 [L1975] TGETS    A=8 B=8 C=42 D=2090 'g_mainUI'
00473 [L1975] TGETS    A=8 B=8 C=43 D=2091 'playerInfoTab'
00474 [L1975] TGETS    A=8 B=8 C=76 D=2124 'gold_label'
00475 [L1975] MOV      A=9 B=0 C=8 D=8 
00476 [L1975] TGETS    A=8 B=8 C=35 D=2083 'setString'
00477 [L1975] UGET     A=10 B=0 C=1 D=1 tostring
00478 [L1975] GGET     A=11 B=0 C=4 D=4 'd_ms'
00479 [L1975] TGETS    A=11 B=11 C=38 D=2854 'd_mainUI'
00480 [L1975] TGETS    A=11 B=11 C=39 D=2855 'g_playerInfo'
00481 [L1975] TGETS    A=11 B=11 C=74 D=2890 'gold_coin'
00482 [L1975] CALL     A=10 B=0 C=2 D=2 
00483 [L1975] CALLM    A=8 B=1 C=1 D=257 
00484 [L1975] JMP      A=8 B=130 C=62 D=33342 target=1059
00485 [L1976] GGET     A=8 B=0 C=4 D=4 'd_ms'
00486 [L1976] TGETS    A=8 B=8 C=20 D=2068 'd_loginUI'
00487 [L1976] TGETS    A=8 B=8 C=21 D=2069 'g_currentSence'
00488 [L1976] GGET     A=9 B=0 C=4 D=4 'd_ms'
00489 [L1976] TGETS    A=9 B=9 C=20 D=2324 'd_loginUI'
00490 [L1976] TGETS    A=9 B=9 C=22 D=2326 'senceID'
00491 [L1976] TGETS    A=9 B=9 C=47 D=2351 'mapUI'
00492 [L1976] ISNEV    A=8 B=0 C=9 D=9 
00493 [L1976] JMP      A=8 B=128 C=15 D=32783 target=509
00494 [L1977] GGET     A=8 B=0 C=4 D=4 'd_ms'
00495 [L1977] TGETS    A=8 B=8 C=48 D=2096 'd_mapUI'
00496 [L1977] TGETS    A=8 B=8 C=49 D=2097 'g_mapUI'
00497 [L1977] TGETS    A=8 B=8 C=43 D=2091 'playerInfoTab'
00498 [L1977] TGETS    A=8 B=8 C=76 D=2124 'gold_label'
00499 [L1977] MOV      A=9 B=0 C=8 D=8 
00500 [L1977] TGETS    A=8 B=8 C=35 D=2083 'setString'
00501 [L1977] UGET     A=10 B=0 C=1 D=1 tostring
00502 [L1977] GGET     A=11 B=0 C=4 D=4 'd_ms'
00503 [L1977] TGETS    A=11 B=11 C=38 D=2854 'd_mainUI'
00504 [L1977] TGETS    A=11 B=11 C=39 D=2855 'g_playerInfo'
00505 [L1977] TGETS    A=11 B=11 C=74 D=2890 'gold_coin'
00506 [L1977] CALL     A=10 B=0 C=2 D=2 
00507 [L1977] CALLM    A=8 B=1 C=1 D=257 
00508 [L1977] JMP      A=8 B=130 C=38 D=33318 target=1059
00509 [L1978] GGET     A=8 B=0 C=4 D=4 'd_ms'
00510 [L1978] TGETS    A=8 B=8 C=20 D=2068 'd_loginUI'
00511 [L1978] TGETS    A=8 B=8 C=21 D=2069 'g_currentSence'
00512 [L1978] GGET     A=9 B=0 C=4 D=4 'd_ms'
00513 [L1978] TGETS    A=9 B=9 C=20 D=2324 'd_loginUI'
00514 [L1978] TGETS    A=9 B=9 C=22 D=2326 'senceID'
00515 [L1978] TGETS    A=9 B=9 C=23 D=2327 'adventure'
00516 [L1978] ISNEV    A=8 B=0 C=9 D=9 
00517 [L1978] JMP      A=8 B=130 C=29 D=33309 target=1059
00518 [L1979] GGET     A=8 B=0 C=4 D=4 'd_ms'
00519 [L1979] TGETS    A=8 B=8 C=24 D=2072 'd_activityUI'
00520 [L1979] TGETS    A=8 B=8 C=77 D=2125 'updateGold'
00521 [L1979] CALL     A=8 B=1 C=1 D=257 
00522 [L1980] JMP      A=7 B=130 C=24 D=33304 target=1059
00523 [L1982] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00524 [L1982] TGETV    A=7 B=7 C=6 D=1798 
00525 [L1982] TGETS    A=7 B=7 C=13 D=1805 'type'
00526 [L1982] GGET     A=8 B=0 C=14 D=14 'r_p'
00527 [L1982] TGETS    A=8 B=8 C=78 D=2126 'cortege_count'
00528 [L1982] ISNEV    A=7 B=0 C=8 D=8 
00529 [L1982] JMP      A=7 B=128 C=20 D=32788 target=550
00530 [L1983] GGET     A=7 B=0 C=4 D=4 'd_ms'
00531 [L1983] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00532 [L1983] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00533 [L1983] TGETS    A=7 B=7 C=78 D=1870 'cortege_count'
00534 [L1984] GGET     A=8 B=0 C=4 D=4 'd_ms'
00535 [L1984] TGETS    A=8 B=8 C=38 D=2086 'd_mainUI'
00536 [L1984] TGETS    A=8 B=8 C=39 D=2087 'g_playerInfo'
00537 [L1984] TGETS    A=9 B=1 C=12 D=268 'attr_list'
00538 [L1984] TGETV    A=9 B=9 C=6 D=2310 
00539 [L1984] TGETS    A=9 B=9 C=19 D=2323 'value'
00540 [L1984] SUBVV    A=9 B=9 C=7 D=2311 
00541 [L1984] TSETS    A=9 B=8 C=79 D=2127 'increasedCortegeCount'
00542 [L1985] GGET     A=8 B=0 C=4 D=4 'd_ms'
00543 [L1985] TGETS    A=8 B=8 C=38 D=2086 'd_mainUI'
00544 [L1985] TGETS    A=8 B=8 C=39 D=2087 'g_playerInfo'
00545 [L1985] TGETS    A=9 B=1 C=12 D=268 'attr_list'
00546 [L1985] TGETV    A=9 B=9 C=6 D=2310 
00547 [L1985] TGETS    A=9 B=9 C=19 D=2323 'value'
00548 [L1985] TSETS    A=9 B=8 C=78 D=2126 'cortege_count'
00549 [L1985] JMP      A=7 B=129 C=253 D=33277 target=1059
00550 [L1987] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00551 [L1987] TGETV    A=7 B=7 C=6 D=1798 
00552 [L1987] TGETS    A=7 B=7 C=13 D=1805 'type'
00553 [L1987] GGET     A=8 B=0 C=14 D=14 'r_p'
00554 [L1987] TGETS    A=8 B=8 C=80 D=2128 'first_charge'
00555 [L1987] ISNEV    A=7 B=0 C=8 D=8 
00556 [L1987] JMP      A=7 B=128 C=16 D=32784 target=573
00557 [L1988] GGET     A=7 B=0 C=4 D=4 'd_ms'
00558 [L1988] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00559 [L1988] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00560 [L1988] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00561 [L1988] TGETV    A=8 B=8 C=6 D=2054 
00562 [L1988] TGETS    A=8 B=8 C=19 D=2067 'value'
00563 [L1988] TSETS    A=8 B=7 C=80 D=1872 'first_charge'
00564 [L1989] GGET     A=7 B=0 C=4 D=4 'd_ms'
00565 [L1989] TGETS    A=7 B=7 C=81 D=1873 'd_u'
00566 [L1989] TGETS    A=7 B=7 C=82 D=1874 'delay_node'
00567 [L1989] KNUM     A=8 B=0 C=2 D=2 0.1
00568 [L1989] GGET     A=9 B=0 C=4 D=4 'd_ms'
00569 [L1989] TGETS    A=9 B=9 C=83 D=2387 'd_bonusUI'
00570 [L1989] TGETS    A=9 B=9 C=84 D=2388 'checkFirstRecharge'
00571 [L1989] CALL     A=7 B=1 C=3 D=259 
00572 [L1989] JMP      A=7 B=129 C=230 D=33254 target=1059
00573 [L1991] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00574 [L1991] TGETV    A=7 B=7 C=6 D=1798 
00575 [L1991] TGETS    A=7 B=7 C=13 D=1805 'type'
00576 [L1991] GGET     A=8 B=0 C=14 D=14 'r_p'
00577 [L1991] TGETS    A=8 B=8 C=85 D=2133 'gongji_plus_rate'
00578 [L1991] ISNEV    A=7 B=0 C=8 D=8 
00579 [L1991] JMP      A=7 B=128 C=7 D=32775 target=587
00580 [L1992] GGET     A=7 B=0 C=4 D=4 'd_ms'
00581 [L1992] TGETS    A=7 B=7 C=86 D=1878 'd_worldBossUI'
00582 [L1992] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00583 [L1992] TGETV    A=8 B=8 C=6 D=2054 
00584 [L1992] TGETS    A=8 B=8 C=19 D=2067 'value'
00585 [L1992] TSETS    A=8 B=7 C=87 D=1879 'g_damageBouns'
00586 [L1992] JMP      A=7 B=129 C=216 D=33240 target=1059
00587 [L1996] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00588 [L1996] TGETV    A=7 B=7 C=6 D=1798 
00589 [L1996] TGETS    A=7 B=7 C=13 D=1805 'type'
00590 [L1996] GGET     A=8 B=0 C=14 D=14 'r_p'
00591 [L1996] TGETS    A=8 B=8 C=88 D=2136 'top_first_promote_time'
00592 [L1996] ISNEV    A=7 B=0 C=8 D=8 
00593 [L1996] JMP      A=7 B=128 C=12 D=32780 target=606
00594 [L1998] GGET     A=7 B=0 C=4 D=4 'd_ms'
00595 [L1998] TGETS    A=7 B=7 C=16 D=1808 'd_rankUI'
00596 [L1998] TGETS    A=7 B=7 C=17 D=1809 'g_rankInfo'
00597 [L1998] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00598 [L1998] TGETV    A=8 B=8 C=6 D=2054 
00599 [L1998] TGETS    A=8 B=8 C=19 D=2067 'value'
00600 [L1998] TSETS    A=8 B=7 C=89 D=1881 'promote_time'
00601 [L1999] GGET     A=7 B=0 C=4 D=4 'd_ms'
00602 [L1999] TGETS    A=7 B=7 C=16 D=1808 'd_rankUI'
00603 [L1999] TGETS    A=7 B=7 C=90 D=1882 'updateSelfScore'
00604 [L1999] CALL     A=7 B=1 C=1 D=257 
00605 [L1999] JMP      A=7 B=129 C=197 D=33221 target=1059
00606 [L2000] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00607 [L2000] TGETV    A=7 B=7 C=6 D=1798 
00608 [L2000] TGETS    A=7 B=7 C=13 D=1805 'type'
00609 [L2000] GGET     A=8 B=0 C=14 D=14 'r_p'
00610 [L2000] TGETS    A=8 B=8 C=91 D=2139 'top_first_promote_prize'
00611 [L2000] ISNEV    A=7 B=0 C=8 D=8 
00612 [L2000] JMP      A=7 B=128 C=12 D=32780 target=625
00613 [L2001] GGET     A=7 B=0 C=4 D=4 'd_ms'
00614 [L2001] TGETS    A=7 B=7 C=16 D=1808 'd_rankUI'
00615 [L2001] TGETS    A=7 B=7 C=17 D=1809 'g_rankInfo'
00616 [L2001] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00617 [L2001] TGETV    A=8 B=8 C=6 D=2054 
00618 [L2001] TGETS    A=8 B=8 C=19 D=2067 'value'
00619 [L2001] TSETS    A=8 B=7 C=92 D=1884 'promote_prize'
00620 [L2002] GGET     A=7 B=0 C=4 D=4 'd_ms'
00621 [L2002] TGETS    A=7 B=7 C=16 D=1808 'd_rankUI'
00622 [L2002] TGETS    A=7 B=7 C=90 D=1882 'updateSelfScore'
00623 [L2002] CALL     A=7 B=1 C=1 D=257 
00624 [L2002] JMP      A=7 B=129 C=178 D=33202 target=1059
00625 [L2004] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00626 [L2004] TGETV    A=7 B=7 C=6 D=1798 
00627 [L2004] TGETS    A=7 B=7 C=13 D=1805 'type'
00628 [L2004] GGET     A=8 B=0 C=14 D=14 'r_p'
00629 [L2004] TGETS    A=8 B=8 C=93 D=2141 'top_day_prize_time'
00630 [L2004] ISNEV    A=7 B=0 C=8 D=8 
00631 [L2004] JMP      A=7 B=128 C=8 D=32776 target=640
00632 [L2006] GGET     A=7 B=0 C=4 D=4 'd_ms'
00633 [L2006] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00634 [L2006] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00635 [L2006] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00636 [L2006] TGETV    A=8 B=8 C=6 D=2054 
00637 [L2006] TGETS    A=8 B=8 C=19 D=2067 'value'
00638 [L2006] TSETS    A=8 B=7 C=93 D=1885 'top_day_prize_time'
00639 [L2006] JMP      A=7 B=129 C=163 D=33187 target=1059
00640 [L2008] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00641 [L2008] TGETV    A=7 B=7 C=6 D=1798 
00642 [L2008] TGETS    A=7 B=7 C=13 D=1805 'type'
00643 [L2008] GGET     A=8 B=0 C=14 D=14 'r_p'
00644 [L2008] TGETS    A=8 B=8 C=94 D=2142 'top_score'
00645 [L2008] ISNEV    A=7 B=0 C=8 D=8 
00646 [L2008] JMP      A=7 B=128 C=17 D=32785 target=664
00647 [L2010] GGET     A=7 B=0 C=4 D=4 'd_ms'
00648 [L2010] TGETS    A=7 B=7 C=16 D=1808 'd_rankUI'
00649 [L2010] TGETS    A=7 B=7 C=17 D=1809 'g_rankInfo'
00650 [L2010] ISEQP    A=7 B=0 C=0 D=0 
00651 [L2010] JMP      A=7 B=129 C=151 D=33175 target=1059
00652 [L2011] GGET     A=7 B=0 C=4 D=4 'd_ms'
00653 [L2011] TGETS    A=7 B=7 C=16 D=1808 'd_rankUI'
00654 [L2011] TGETS    A=7 B=7 C=17 D=1809 'g_rankInfo'
00655 [L2011] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00656 [L2011] TGETV    A=8 B=8 C=6 D=2054 
00657 [L2011] TGETS    A=8 B=8 C=19 D=2067 'value'
00658 [L2011] TSETS    A=8 B=7 C=95 D=1887 'self_score'
00659 [L2012] GGET     A=7 B=0 C=4 D=4 'd_ms'
00660 [L2012] TGETS    A=7 B=7 C=16 D=1808 'd_rankUI'
00661 [L2012] TGETS    A=7 B=7 C=90 D=1882 'updateSelfScore'
00662 [L2012] CALL     A=7 B=1 C=1 D=257 
00663 [L2013] JMP      A=7 B=129 C=139 D=33163 target=1059
00664 [L2014] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00665 [L2014] TGETV    A=7 B=7 C=6 D=1798 
00666 [L2014] TGETS    A=7 B=7 C=13 D=1805 'type'
00667 [L2014] GGET     A=8 B=0 C=14 D=14 'r_p'
00668 [L2014] TGETS    A=8 B=8 C=96 D=2144 'buy_strength_item_count'
00669 [L2014] ISNEV    A=7 B=0 C=8 D=8 
00670 [L2014] JMP      A=7 B=128 C=8 D=32776 target=679
00671 [L2015] GGET     A=7 B=0 C=4 D=4 'd_ms'
00672 [L2015] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00673 [L2015] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00674 [L2015] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00675 [L2015] TGETV    A=8 B=8 C=6 D=2054 
00676 [L2015] TGETS    A=8 B=8 C=19 D=2067 'value'
00677 [L2015] TSETS    A=8 B=7 C=97 D=1889 'strength_item_count'
00678 [L2015] JMP      A=7 B=129 C=124 D=33148 target=1059
00679 [L2016] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00680 [L2016] TGETV    A=7 B=7 C=6 D=1798 
00681 [L2016] TGETS    A=7 B=7 C=13 D=1805 'type'
00682 [L2016] GGET     A=8 B=0 C=14 D=14 'r_p'
00683 [L2016] TGETS    A=8 B=8 C=98 D=2146 'buy_energy_item_count'
00684 [L2016] ISNEV    A=7 B=0 C=8 D=8 
00685 [L2016] JMP      A=7 B=128 C=8 D=32776 target=694
00686 [L2017] GGET     A=7 B=0 C=4 D=4 'd_ms'
00687 [L2017] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00688 [L2017] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00689 [L2017] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00690 [L2017] TGETV    A=8 B=8 C=6 D=2054 
00691 [L2017] TGETS    A=8 B=8 C=19 D=2067 'value'
00692 [L2017] TSETS    A=8 B=7 C=99 D=1891 'energy_item_count'
00693 [L2017] JMP      A=7 B=129 C=109 D=33133 target=1059
00694 [L2018] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00695 [L2018] TGETV    A=7 B=7 C=6 D=1798 
00696 [L2018] TGETS    A=7 B=7 C=13 D=1805 'type'
00697 [L2018] GGET     A=8 B=0 C=14 D=14 'r_p'
00698 [L2018] TGETS    A=8 B=8 C=100 D=2148 'buy_strength_count_limit'
00699 [L2018] ISNEV    A=7 B=0 C=8 D=8 
00700 [L2018] JMP      A=7 B=128 C=8 D=32776 target=709
00701 [L2019] GGET     A=7 B=0 C=4 D=4 'd_ms'
00702 [L2019] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00703 [L2019] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00704 [L2019] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00705 [L2019] TGETV    A=8 B=8 C=6 D=2054 
00706 [L2019] TGETS    A=8 B=8 C=19 D=2067 'value'
00707 [L2019] TSETS    A=8 B=7 C=101 D=1893 'strength_item_limit'
00708 [L2019] JMP      A=7 B=129 C=94 D=33118 target=1059
00709 [L2020] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00710 [L2020] TGETV    A=7 B=7 C=6 D=1798 
00711 [L2020] TGETS    A=7 B=7 C=13 D=1805 'type'
00712 [L2020] GGET     A=8 B=0 C=14 D=14 'r_p'
00713 [L2020] TGETS    A=8 B=8 C=102 D=2150 'buy_energy_count_limit'
00714 [L2020] ISNEV    A=7 B=0 C=8 D=8 
00715 [L2020] JMP      A=7 B=128 C=8 D=32776 target=724
00716 [L2021] GGET     A=7 B=0 C=4 D=4 'd_ms'
00717 [L2021] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00718 [L2021] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00719 [L2021] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00720 [L2021] TGETV    A=8 B=8 C=6 D=2054 
00721 [L2021] TGETS    A=8 B=8 C=19 D=2067 'value'
00722 [L2021] TSETS    A=8 B=7 C=103 D=1895 'energy_item_limit'
00723 [L2021] JMP      A=7 B=129 C=79 D=33103 target=1059
00724 [L2023] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00725 [L2023] TGETV    A=7 B=7 C=6 D=1798 
00726 [L2023] TGETS    A=7 B=7 C=13 D=1805 'type'
00727 [L2023] GGET     A=8 B=0 C=14 D=14 'r_p'
00728 [L2023] TGETS    A=8 B=8 C=104 D=2152 'buy_strength_item_time'
00729 [L2023] ISNEV    A=7 B=0 C=8 D=8 
00730 [L2023] JMP      A=7 B=128 C=8 D=32776 target=739
00731 [L2024] GGET     A=7 B=0 C=4 D=4 'd_ms'
00732 [L2024] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00733 [L2024] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00734 [L2024] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00735 [L2024] TGETV    A=8 B=8 C=6 D=2054 
00736 [L2024] TGETS    A=8 B=8 C=19 D=2067 'value'
00737 [L2024] TSETS    A=8 B=7 C=105 D=1897 'strength_item_time'
00738 [L2024] JMP      A=7 B=129 C=64 D=33088 target=1059
00739 [L2025] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00740 [L2025] TGETV    A=7 B=7 C=6 D=1798 
00741 [L2025] TGETS    A=7 B=7 C=13 D=1805 'type'
00742 [L2025] GGET     A=8 B=0 C=14 D=14 'r_p'
00743 [L2025] TGETS    A=8 B=8 C=106 D=2154 'buy_energy_item_time'
00744 [L2025] ISNEV    A=7 B=0 C=8 D=8 
00745 [L2025] JMP      A=7 B=128 C=8 D=32776 target=754
00746 [L2026] GGET     A=7 B=0 C=4 D=4 'd_ms'
00747 [L2026] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00748 [L2026] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00749 [L2026] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00750 [L2026] TGETV    A=8 B=8 C=6 D=2054 
00751 [L2026] TGETS    A=8 B=8 C=19 D=2067 'value'
00752 [L2026] TSETS    A=8 B=7 C=107 D=1899 'energy_item_time'
00753 [L2026] JMP      A=7 B=129 C=49 D=33073 target=1059
00754 [L2027] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00755 [L2027] TGETV    A=7 B=7 C=6 D=1798 
00756 [L2027] TGETS    A=7 B=7 C=13 D=1805 'type'
00757 [L2027] GGET     A=8 B=0 C=14 D=14 'r_p'
00758 [L2027] TGETS    A=8 B=8 C=108 D=2156 'party_fight_count'
00759 [L2027] ISNEV    A=7 B=0 C=8 D=8 
00760 [L2027] JMP      A=7 B=128 C=7 D=32775 target=768
00761 [L2028] GGET     A=7 B=0 C=4 D=4 'd_ms'
00762 [L2028] TGETS    A=7 B=7 C=86 D=1878 'd_worldBossUI'
00763 [L2028] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00764 [L2028] TGETV    A=8 B=8 C=6 D=2054 
00765 [L2028] TGETS    A=8 B=8 C=19 D=2067 'value'
00766 [L2028] TSETS    A=8 B=7 C=109 D=1901 'g_normalFightCount'
00767 [L2028] JMP      A=7 B=129 C=35 D=33059 target=1059
00768 [L2030] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00769 [L2030] TGETV    A=7 B=7 C=6 D=1798 
00770 [L2030] TGETS    A=7 B=7 C=13 D=1805 'type'
00771 [L2030] GGET     A=8 B=0 C=14 D=14 'r_p'
00772 [L2030] TGETS    A=8 B=8 C=110 D=2158 'party_fight_count_plus'
00773 [L2030] ISNEV    A=7 B=0 C=8 D=8 
00774 [L2030] JMP      A=7 B=128 C=7 D=32775 target=782
00775 [L2031] GGET     A=7 B=0 C=4 D=4 'd_ms'
00776 [L2031] TGETS    A=7 B=7 C=86 D=1878 'd_worldBossUI'
00777 [L2031] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00778 [L2031] TGETV    A=8 B=8 C=6 D=2054 
00779 [L2031] TGETS    A=8 B=8 C=19 D=2067 'value'
00780 [L2031] TSETS    A=8 B=7 C=111 D=1903 'g_payFightCount'
00781 [L2031] JMP      A=7 B=129 C=21 D=33045 target=1059
00782 [L2033] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00783 [L2033] TGETV    A=7 B=7 C=6 D=1798 
00784 [L2033] TGETS    A=7 B=7 C=13 D=1805 'type'
00785 [L2033] GGET     A=8 B=0 C=14 D=14 'r_p'
00786 [L2033] TGETS    A=8 B=8 C=112 D=2160 'rape_flush_count_limit'
00787 [L2033] ISNEV    A=7 B=0 C=8 D=8 
00788 [L2033] JMP      A=7 B=128 C=8 D=32776 target=797
00789 [L2034] GGET     A=7 B=0 C=4 D=4 'd_ms'
00790 [L2034] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00791 [L2034] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00792 [L2034] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00793 [L2034] TGETV    A=8 B=8 C=6 D=2054 
00794 [L2034] TGETS    A=8 B=8 C=19 D=2067 'value'
00795 [L2034] TSETS    A=8 B=7 C=113 D=1905 'rape_flush_limit'
00796 [L2034] JMP      A=7 B=129 C=6 D=33030 target=1059
00797 [L2036] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00798 [L2036] TGETV    A=7 B=7 C=6 D=1798 
00799 [L2036] TGETS    A=7 B=7 C=13 D=1805 'type'
00800 [L2036] GGET     A=8 B=0 C=14 D=14 'r_p'
00801 [L2036] TGETS    A=8 B=8 C=114 D=2162 'top_fight_count_limit'
00802 [L2036] ISNEV    A=7 B=0 C=8 D=8 
00803 [L2036] JMP      A=7 B=128 C=8 D=32776 target=812
00804 [L2037] GGET     A=7 B=0 C=4 D=4 'd_ms'
00805 [L2037] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00806 [L2037] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00807 [L2037] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00808 [L2037] TGETV    A=8 B=8 C=6 D=2054 
00809 [L2037] TGETS    A=8 B=8 C=19 D=2067 'value'
00810 [L2037] TSETS    A=8 B=7 C=115 D=1907 'top_fight_limit'
00811 [L2037] JMP      A=7 B=128 C=247 D=33015 target=1059
00812 [L2039] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00813 [L2039] TGETV    A=7 B=7 C=6 D=1798 
00814 [L2039] TGETS    A=7 B=7 C=13 D=1805 'type'
00815 [L2039] GGET     A=8 B=0 C=14 D=14 'r_p'
00816 [L2039] TGETS    A=8 B=8 C=116 D=2164 'name'
00817 [L2039] ISNEV    A=7 B=0 C=8 D=8 
00818 [L2039] JMP      A=7 B=128 C=8 D=32776 target=827
00819 [L2040] GGET     A=7 B=0 C=4 D=4 'd_ms'
00820 [L2040] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00821 [L2040] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00822 [L2040] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00823 [L2040] TGETV    A=8 B=8 C=6 D=2054 
00824 [L2040] TGETS    A=8 B=8 C=19 D=2067 'value'
00825 [L2040] TSETS    A=8 B=7 C=117 D=1909 'role_name'
00826 [L2040] JMP      A=7 B=128 C=232 D=33000 target=1059
00827 [L2042] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00828 [L2042] TGETV    A=7 B=7 C=6 D=1798 
00829 [L2042] TGETS    A=7 B=7 C=13 D=1805 'type'
00830 [L2042] GGET     A=8 B=0 C=14 D=14 'r_p'
00831 [L2042] TGETS    A=8 B=8 C=118 D=2166 'task_progress'
00832 [L2042] ISNEV    A=7 B=0 C=8 D=8 
00833 [L2042] JMP      A=7 B=128 C=12 D=32780 target=846
00834 [L2043] GGET     A=7 B=0 C=4 D=4 'd_ms'
00835 [L2043] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00836 [L2043] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00837 [L2043] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00838 [L2043] TGETV    A=8 B=8 C=6 D=2054 
00839 [L2043] TGETS    A=8 B=8 C=19 D=2067 'value'
00840 [L2043] TSETS    A=8 B=7 C=118 D=1910 'task_progress'
00841 [L2044] GGET     A=7 B=0 C=4 D=4 'd_ms'
00842 [L2044] TGETS    A=7 B=7 C=119 D=1911 'd_tianShuUI'
00843 [L2044] TGETS    A=7 B=7 C=120 D=1912 'showHint'
00844 [L2044] CALL     A=7 B=1 C=1 D=257 
00845 [L2044] JMP      A=7 B=128 C=213 D=32981 target=1059
00846 [L2045] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00847 [L2045] TGETV    A=7 B=7 C=6 D=1798 
00848 [L2045] TGETS    A=7 B=7 C=13 D=1805 'type'
00849 [L2045] GGET     A=8 B=0 C=14 D=14 'r_p'
00850 [L2045] TGETS    A=8 B=8 C=121 D=2169 'take_charge_gift_time'
00851 [L2045] ISNEV    A=7 B=0 C=8 D=8 
00852 [L2045] JMP      A=7 B=128 C=8 D=32776 target=861
00853 [L2046] GGET     A=7 B=0 C=4 D=4 'd_ms'
00854 [L2046] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00855 [L2046] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00856 [L2046] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00857 [L2046] TGETV    A=8 B=8 C=6 D=2054 
00858 [L2046] TGETS    A=8 B=8 C=19 D=2067 'value'
00859 [L2046] TSETS    A=8 B=7 C=121 D=1913 'take_charge_gift_time'
00860 [L2046] JMP      A=7 B=128 C=198 D=32966 target=1059
00861 [L2047] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00862 [L2047] TGETV    A=7 B=7 C=6 D=1798 
00863 [L2047] TGETS    A=7 B=7 C=13 D=1805 'type'
00864 [L2047] GGET     A=8 B=0 C=14 D=14 'r_p'
00865 [L2047] TGETS    A=8 B=8 C=122 D=2170 'take_vip_gold_time'
00866 [L2047] ISNEV    A=7 B=0 C=8 D=8 
00867 [L2047] JMP      A=7 B=128 C=16 D=32784 target=884
00868 [L2048] GGET     A=7 B=0 C=4 D=4 'd_ms'
00869 [L2048] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00870 [L2048] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00871 [L2048] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00872 [L2048] TGETV    A=8 B=8 C=6 D=2054 
00873 [L2048] TGETS    A=8 B=8 C=19 D=2067 'value'
00874 [L2048] TSETS    A=8 B=7 C=122 D=1914 'take_vip_gold_time'
00875 [L2049] GGET     A=7 B=0 C=4 D=4 'd_ms'
00876 [L2049] TGETS    A=7 B=7 C=81 D=1873 'd_u'
00877 [L2049] TGETS    A=7 B=7 C=82 D=1874 'delay_node'
00878 [L2049] KNUM     A=8 B=0 C=2 D=2 0.1
00879 [L2049] GGET     A=9 B=0 C=4 D=4 'd_ms'
00880 [L2049] TGETS    A=9 B=9 C=38 D=2342 'd_mainUI'
00881 [L2049] TGETS    A=9 B=9 C=123 D=2427 'checkVIPAnim'
00882 [L2049] CALL     A=7 B=1 C=3 D=259 
00883 [L2049] JMP      A=7 B=128 C=175 D=32943 target=1059
00884 [L2050] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00885 [L2050] TGETV    A=7 B=7 C=6 D=1798 
00886 [L2050] TGETS    A=7 B=7 C=13 D=1805 'type'
00887 [L2050] GGET     A=8 B=0 C=14 D=14 'r_p'
00888 [L2050] TGETS    A=8 B=8 C=124 D=2172 'vip_level'
00889 [L2050] ISNEV    A=7 B=0 C=8 D=8 
00890 [L2050] JMP      A=7 B=128 C=16 D=32784 target=907
00891 [L2051] GGET     A=7 B=0 C=4 D=4 'd_ms'
00892 [L2051] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00893 [L2051] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00894 [L2051] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00895 [L2051] TGETV    A=8 B=8 C=6 D=2054 
00896 [L2051] TGETS    A=8 B=8 C=19 D=2067 'value'
00897 [L2051] TSETS    A=8 B=7 C=124 D=1916 'vip_level'
00898 [L2052] GGET     A=7 B=0 C=4 D=4 'd_ms'
00899 [L2052] TGETS    A=7 B=7 C=81 D=1873 'd_u'
00900 [L2052] TGETS    A=7 B=7 C=82 D=1874 'delay_node'
00901 [L2052] KNUM     A=8 B=0 C=2 D=2 0.1
00902 [L2052] GGET     A=9 B=0 C=4 D=4 'd_ms'
00903 [L2052] TGETS    A=9 B=9 C=38 D=2342 'd_mainUI'
00904 [L2052] TGETS    A=9 B=9 C=123 D=2427 'checkVIPAnim'
00905 [L2052] CALL     A=7 B=1 C=3 D=259 
00906 [L2052] JMP      A=7 B=128 C=152 D=32920 target=1059
00907 [L2053] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00908 [L2053] TGETV    A=7 B=7 C=6 D=1798 
00909 [L2053] TGETS    A=7 B=7 C=13 D=1805 'type'
00910 [L2053] GGET     A=8 B=0 C=14 D=14 'r_p'
00911 [L2053] TGETS    A=8 B=8 C=125 D=2173 'vip_gift'
00912 [L2053] ISNEV    A=7 B=0 C=8 D=8 
00913 [L2053] JMP      A=7 B=128 C=16 D=32784 target=930
00914 [L2054] GGET     A=7 B=0 C=4 D=4 'd_ms'
00915 [L2054] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00916 [L2054] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00917 [L2054] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00918 [L2054] TGETV    A=8 B=8 C=6 D=2054 
00919 [L2054] TGETS    A=8 B=8 C=19 D=2067 'value'
00920 [L2054] TSETS    A=8 B=7 C=125 D=1917 'vip_gift'
00921 [L2055] GGET     A=7 B=0 C=4 D=4 'd_ms'
00922 [L2055] TGETS    A=7 B=7 C=81 D=1873 'd_u'
00923 [L2055] TGETS    A=7 B=7 C=82 D=1874 'delay_node'
00924 [L2055] KNUM     A=8 B=0 C=2 D=2 0.1
00925 [L2055] GGET     A=9 B=0 C=4 D=4 'd_ms'
00926 [L2055] TGETS    A=9 B=9 C=38 D=2342 'd_mainUI'
00927 [L2055] TGETS    A=9 B=9 C=123 D=2427 'checkVIPAnim'
00928 [L2055] CALL     A=7 B=1 C=3 D=259 
00929 [L2055] JMP      A=7 B=128 C=129 D=32897 target=1059
00930 [L2056] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00931 [L2056] TGETV    A=7 B=7 C=6 D=1798 
00932 [L2056] TGETS    A=7 B=7 C=13 D=1805 'type'
00933 [L2056] GGET     A=8 B=0 C=14 D=14 'r_p'
00934 [L2056] TGETS    A=8 B=8 C=126 D=2174 'month_card_time'
00935 [L2056] ISNEV    A=7 B=0 C=8 D=8 
00936 [L2056] JMP      A=7 B=128 C=21 D=32789 target=958
00937 [L2057] GGET     A=7 B=0 C=4 D=4 'd_ms'
00938 [L2057] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00939 [L2057] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00940 [L2057] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00941 [L2057] TGETV    A=8 B=8 C=6 D=2054 
00942 [L2057] TGETS    A=8 B=8 C=19 D=2067 'value'
00943 [L2057] TSETS    A=8 B=7 C=126 D=1918 'month_card_time'
00944 [L2058] GGET     A=7 B=0 C=4 D=4 'd_ms'
00945 [L2058] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00946 [L2058] TGETS    A=7 B=7 C=127 D=1919 'freshMcardTink'
00947 [L2058] CALL     A=7 B=1 C=1 D=257 
00948 [L2059] GGET     A=7 B=0 C=4 D=4 'd_ms'
00949 [L2059] TGETS    A=7 B=7 C=128 D=1920 'd_shopUI'
00950 [L2059] TGETS    A=7 B=7 C=129 D=1921 'g_self'
00951 [L2059] KPRI     A=8 B=0 C=0 D=0 
00952 [L2059] TSETS    A=8 B=7 C=130 D=1922 'call_back'
00953 [L2060] GGET     A=7 B=0 C=4 D=4 'd_ms'
00954 [L2060] TGETS    A=7 B=7 C=128 D=1920 'd_shopUI'
00955 [L2060] TGETS    A=7 B=7 C=131 D=1923 'getGoodsList'
00956 [L2060] CALL     A=7 B=1 C=1 D=257 
00957 [L2060] JMP      A=7 B=128 C=101 D=32869 target=1059
00958 [L2061] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00959 [L2061] TGETV    A=7 B=7 C=6 D=1798 
00960 [L2061] TGETS    A=7 B=7 C=13 D=1805 'type'
00961 [L2061] GGET     A=8 B=0 C=14 D=14 'r_p'
00962 [L2061] TGETS    A=8 B=8 C=132 D=2180 'role_combat_power'
00963 [L2061] ISNEV    A=7 B=0 C=8 D=8 
00964 [L2061] JMP      A=7 B=128 C=15 D=32783 target=980
00965 [L2062] GGET     A=7 B=0 C=4 D=4 'd_ms'
00966 [L2062] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00967 [L2062] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00968 [L2062] UGET     A=8 B=0 C=2 D=2 math
00969 [L2062] TGETS    A=8 B=8 C=37 D=2085 'floor'
00970 [L2062] TGETS    A=9 B=1 C=12 D=268 'attr_list'
00971 [L2062] TGETV    A=9 B=9 C=6 D=2310 
00972 [L2062] TGETS    A=9 B=9 C=19 D=2323 'value'
00973 [L2062] CALL     A=8 B=2 C=2 D=514 
00974 [L2062] TSETS    A=8 B=7 C=132 D=1924 'role_combat_power'
00975 [L2063] GGET     A=7 B=0 C=4 D=4 'd_ms'
00976 [L2063] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00977 [L2063] TGETS    A=7 B=7 C=133 D=1925 'showCombat'
00978 [L2063] CALL     A=7 B=1 C=1 D=257 
00979 [L2063] JMP      A=7 B=128 C=79 D=32847 target=1059
00980 [L2064] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00981 [L2064] TGETV    A=7 B=7 C=6 D=1798 
00982 [L2064] TGETS    A=7 B=7 C=13 D=1805 'type'
00983 [L2064] GGET     A=8 B=0 C=14 D=14 'r_p'
00984 [L2064] TGETS    A=8 B=8 C=134 D=2182 'monthcard_unact_count'
00985 [L2064] ISNEV    A=7 B=0 C=8 D=8 
00986 [L2064] JMP      A=7 B=128 C=1 D=32769 target=988
00987 [L2064] JMP      A=7 B=128 C=71 D=32839 target=1059
00988 [L2067] TGETS    A=7 B=1 C=12 D=268 'attr_list'
00989 [L2067] TGETV    A=7 B=7 C=6 D=1798 
00990 [L2067] TGETS    A=7 B=7 C=13 D=1805 'type'
00991 [L2067] GGET     A=8 B=0 C=14 D=14 'r_p'
00992 [L2067] TGETS    A=8 B=8 C=135 D=2183 'first_charge_gift'
00993 [L2067] ISNEV    A=7 B=0 C=8 D=8 
00994 [L2067] JMP      A=7 B=128 C=16 D=32784 target=1011
00995 [L2068] GGET     A=7 B=0 C=4 D=4 'd_ms'
00996 [L2068] TGETS    A=7 B=7 C=38 D=1830 'd_mainUI'
00997 [L2068] TGETS    A=7 B=7 C=39 D=1831 'g_playerInfo'
00998 [L2068] TGETS    A=8 B=1 C=12 D=268 'attr_list'
00999 [L2068] TGETV    A=8 B=8 C=6 D=2054 
01000 [L2068] TGETS    A=8 B=8 C=19 D=2067 'value'
01001 [L2068] TSETS    A=8 B=7 C=135 D=1927 'first_charge_gift'
01002 [L2069] GGET     A=7 B=0 C=4 D=4 'd_ms'
01003 [L2069] TGETS    A=7 B=7 C=81 D=1873 'd_u'
01004 [L2069] TGETS    A=7 B=7 C=82 D=1874 'delay_node'
01005 [L2069] KNUM     A=8 B=0 C=2 D=2 0.1
01006 [L2069] GGET     A=9 B=0 C=4 D=4 'd_ms'
01007 [L2069] TGETS    A=9 B=9 C=83 D=2387 'd_bonusUI'
01008 [L2069] TGETS    A=9 B=9 C=84 D=2388 'checkFirstRecharge'
01009 [L2069] CALL     A=7 B=1 C=3 D=259 
01010 [L2069] JMP      A=7 B=128 C=48 D=32816 target=1059
01011 [L2072] KPRI     A=7 B=0 C=1 D=1 
01012 [L2073] UGET     A=8 B=0 C=4 D=4 pairs
01013 [L2073] GGET     A=9 B=0 C=14 D=14 'r_p'
01014 [L2073] CALL     A=8 B=4 C=2 D=1026 
01015 [L2073] ISNEXT   A=11 B=128 C=32 D=32800 target=1048
01016 [L2074] TGETS    A=13 B=1 C=12 D=268 'attr_list'
01017 [L2074] TGETV    A=13 B=13 C=6 D=3334 
01018 [L2074] TGETS    A=13 B=13 C=13 D=3341 'type'
01019 [L2074] ISNEV    A=12 B=0 C=13 D=13 
01020 [L2074] JMP      A=13 B=128 C=27 D=32795 target=1048
01021 [L2075] KPRI     A=7 B=0 C=2 D=2 
01022 [L2076] UGET     A=13 B=0 C=0 D=0 cclog
01023 [L2076] KSTR     A=14 B=0 C=136 D=136 'update 1032, property_name='
01024 [L2076] MOV      A=15 B=0 C=11 D=11 
01025 [L2076] CAT      A=14 B=14 C=15 D=3599 
01026 [L2076] CALL     A=13 B=1 C=2 D=258 
01027 [L2077] GGET     A=13 B=0 C=4 D=4 'd_ms'
01028 [L2077] TGETS    A=13 B=13 C=38 D=3366 'd_mainUI'
01029 [L2077] TGETS    A=13 B=13 C=39 D=3367 'g_playerInfo'
01030 [L2077] TGETV    A=13 B=13 C=11 D=3339 
01031 [L2077] ISF      A=0 B=0 C=13 D=13 
01032 [L2077] JMP      A=14 B=128 C=8 D=32776 target=1041
01033 [L2078] GGET     A=13 B=0 C=4 D=4 'd_ms'
01034 [L2078] TGETS    A=13 B=13 C=38 D=3366 'd_mainUI'
01035 [L2078] TGETS    A=13 B=13 C=39 D=3367 'g_playerInfo'
01036 [L2078] TGETS    A=14 B=1 C=12 D=268 'attr_list'
01037 [L2078] TGETV    A=14 B=14 C=6 D=3590 
01038 [L2078] TGETS    A=14 B=14 C=19 D=3603 'value'
01039 [L2078] TSETV    A=14 B=13 C=11 D=3339 
01040 [L2078] JMP      A=13 B=128 C=9 D=32777 target=1050
01041 [L2081] UGET     A=13 B=0 C=0 D=0 cclog
01042 [L2081] KSTR     A=14 B=0 C=137 D=137 'ERROR: 1032 can not find role_property=['
01043 [L2081] MOV      A=15 B=0 C=11 D=11 
01044 [L2081] KSTR     A=16 B=0 C=138 D=138 '] in g_playerInfo.'
01045 [L2081] CAT      A=14 B=14 C=16 D=3600 
01046 [L2081] CALL     A=13 B=1 C=2 D=258 
01047 [L2083] JMP      A=8 B=128 C=2 D=32770 target=1050
01048 [L2073] ITERN    A=11 B=3 C=3 D=771 
01049 [L2073] ITERL    A=11 B=127 C=222 D=32734 target=1016
01050 [L2087] ISNEP    A=7 B=0 C=1 D=1 
01051 [L2087] JMP      A=8 B=128 C=7 D=32775 target=1059
01052 [L2089] UGET     A=8 B=0 C=0 D=0 cclog
01053 [L2089] KSTR     A=9 B=0 C=139 D=139 'ERROR: 1032 unhandle role_property='
01054 [L2089] TGETS    A=10 B=1 C=12 D=268 'attr_list'
01055 [L2089] TGETV    A=10 B=10 C=6 D=2566 
01056 [L2089] TGETS    A=10 B=10 C=13 D=2573 'type'
01057 [L2089] CAT      A=9 B=9 C=10 D=2314 
01058 [L2089] CALL     A=8 B=1 C=2 D=258 
01059 [L1886] FORL     A=3 B=124 C=11 D=31755 target=47
01060 [L2093] JMP      A=3 B=128 C=5 D=32773 target=1066
01061 [L2096] UGET     A=3 B=0 C=0 D=0 cclog
01062 [L2096] KSTR     A=4 B=0 C=140 D=140 'ERROR: unhandle 1032 object_type='
01063 [L2096] TGETS    A=5 B=1 C=1 D=257 'unit_type'
01064 [L2096] CAT      A=4 B=4 C=5 D=1029 
01065 [L2096] CALL     A=3 B=1 C=2 D=258 
01066 [L2109] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto47 offset=0xedd8 source_lines=2111-2127 params=3
UPVALUES []
00001 [L2112] ISEQP    A=1 B=0 C=0 D=0 
00002 [L2112] JMP      A=3 B=128 C=64 D=32832 target=67
00003 [L2113] TGETS    A=3 B=1 C=0 D=256 'channel'
00004 [L2113] GGET     A=4 B=0 C=1 D=1 'd_ms'
00005 [L2113] TGETS    A=4 B=4 C=2 D=1026 'd_common_def'
00006 [L2113] TGETS    A=4 B=4 C=3 D=1027 'channel_type'
00007 [L2113] TGETS    A=4 B=4 C=4 D=1028 'channel_world'
00008 [L2113] ISNEV    A=3 B=0 C=4 D=4 
00009 [L2113] JMP      A=3 B=128 C=6 D=32774 target=16
00010 [L2114] GGET     A=3 B=0 C=1 D=1 'd_ms'
00011 [L2114] TGETS    A=3 B=3 C=5 D=773 'd_newChatUI'
00012 [L2114] TGETS    A=3 B=3 C=6 D=774 'updateMessage'
00013 [L2114] MOV      A=4 B=0 C=1 D=1 
00014 [L2114] CALL     A=3 B=1 C=2 D=258 
00015 [L2114] JMP      A=3 B=128 C=51 D=32819 target=67
00016 [L2115] TGETS    A=3 B=1 C=0 D=256 'channel'
00017 [L2115] GGET     A=4 B=0 C=1 D=1 'd_ms'
00018 [L2115] TGETS    A=4 B=4 C=2 D=1026 'd_common_def'
00019 [L2115] TGETS    A=4 B=4 C=3 D=1027 'channel_type'
00020 [L2115] TGETS    A=4 B=4 C=7 D=1031 'channel_union'
00021 [L2115] ISNEV    A=3 B=0 C=4 D=4 
00022 [L2115] JMP      A=3 B=128 C=6 D=32774 target=29
00023 [L2116] GGET     A=3 B=0 C=1 D=1 'd_ms'
00024 [L2116] TGETS    A=3 B=3 C=5 D=773 'd_newChatUI'
00025 [L2116] TGETS    A=3 B=3 C=6 D=774 'updateMessage'
00026 [L2116] MOV      A=4 B=0 C=1 D=1 
00027 [L2116] CALL     A=3 B=1 C=2 D=258 
00028 [L2116] JMP      A=3 B=128 C=38 D=32806 target=67
00029 [L2117] TGETS    A=3 B=1 C=0 D=256 'channel'
00030 [L2117] GGET     A=4 B=0 C=1 D=1 'd_ms'
00031 [L2117] TGETS    A=4 B=4 C=2 D=1026 'd_common_def'
00032 [L2117] TGETS    A=4 B=4 C=3 D=1027 'channel_type'
00033 [L2117] TGETS    A=4 B=4 C=8 D=1032 'channel_private'
00034 [L2117] ISNEV    A=3 B=0 C=4 D=4 
00035 [L2117] JMP      A=3 B=128 C=6 D=32774 target=42
00036 [L2118] GGET     A=3 B=0 C=1 D=1 'd_ms'
00037 [L2118] TGETS    A=3 B=3 C=9 D=777 'd_messageUI'
00038 [L2118] TGETS    A=3 B=3 C=10 D=778 'updatePrivateMessage'
00039 [L2118] MOV      A=4 B=0 C=1 D=1 
00040 [L2118] CALL     A=3 B=1 C=2 D=258 
00041 [L2118] JMP      A=3 B=128 C=25 D=32793 target=67
00042 [L2119] TGETS    A=3 B=1 C=0 D=256 'channel'
00043 [L2119] GGET     A=4 B=0 C=1 D=1 'd_ms'
00044 [L2119] TGETS    A=4 B=4 C=2 D=1026 'd_common_def'
00045 [L2119] TGETS    A=4 B=4 C=3 D=1027 'channel_type'
00046 [L2119] TGETS    A=4 B=4 C=11 D=1035 'channel_fight'
00047 [L2119] ISNEV    A=3 B=0 C=4 D=4 
00048 [L2119] JMP      A=3 B=128 C=6 D=32774 target=55
00049 [L2120] GGET     A=3 B=0 C=1 D=1 'd_ms'
00050 [L2120] TGETS    A=3 B=3 C=9 D=777 'd_messageUI'
00051 [L2120] TGETS    A=3 B=3 C=12 D=780 'updateFightMessage'
00052 [L2120] MOV      A=4 B=0 C=1 D=1 
00053 [L2120] CALL     A=3 B=1 C=2 D=258 
00054 [L2120] JMP      A=3 B=128 C=12 D=32780 target=67
00055 [L2121] TGETS    A=3 B=1 C=0 D=256 'channel'
00056 [L2121] GGET     A=4 B=0 C=1 D=1 'd_ms'
00057 [L2121] TGETS    A=4 B=4 C=2 D=1026 'd_common_def'
00058 [L2121] TGETS    A=4 B=4 C=3 D=1027 'channel_type'
00059 [L2121] TGETS    A=4 B=4 C=13 D=1037 'channel_system'
00060 [L2121] ISNEV    A=3 B=0 C=4 D=4 
00061 [L2121] JMP      A=3 B=128 C=5 D=32773 target=67
00062 [L2123] GGET     A=3 B=0 C=1 D=1 'd_ms'
00063 [L2123] TGETS    A=3 B=3 C=9 D=777 'd_messageUI'
00064 [L2123] TGETS    A=3 B=3 C=14 D=782 'updateSystemMessage'
00065 [L2123] MOV      A=4 B=0 C=1 D=1 
00066 [L2123] CALL     A=3 B=1 C=2 D=258 
00067 [L2127] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto48 offset=0xf022 source_lines=2129-2134 params=3
UPVALUES []
00001 [L2130] ISEQP    A=1 B=0 C=0 D=0 
00002 [L2130] JMP      A=3 B=128 C=9 D=32777 target=12
00003 [L2131] GGET     A=3 B=0 C=0 D=0 'd_ms'
00004 [L2131] TGETS    A=3 B=3 C=1 D=769 'd_alert'
00005 [L2131] TGETS    A=3 B=3 C=2 D=770 'stop_wait'
00006 [L2131] CALL     A=3 B=1 C=1 D=257 
00007 [L2132] GGET     A=3 B=0 C=0 D=0 'd_ms'
00008 [L2132] TGETS    A=3 B=3 C=3 D=771 'd_followUI'
00009 [L2132] TGETS    A=3 B=3 C=4 D=772 'getSearchResult'
00010 [L2132] MOV      A=4 B=0 C=1 D=1 
00011 [L2132] CALL     A=3 B=1 C=2 D=258 
00012 [L2134] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto49 offset=0xf0b8 source_lines=2136-2140 params=3
UPVALUES []
00001 [L2137] ISEQP    A=1 B=0 C=0 D=0 
00002 [L2137] JMP      A=3 B=128 C=5 D=32773 target=8
00003 [L2138] GGET     A=3 B=0 C=0 D=0 'd_ms'
00004 [L2138] TGETS    A=3 B=3 C=1 D=769 'd_followUI'
00005 [L2138] TGETS    A=3 B=3 C=2 D=770 'updateFollowList'
00006 [L2138] MOV      A=4 B=0 C=1 D=1 
00007 [L2138] CALL     A=3 B=1 C=2 D=258 
00008 [L2140] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto50 offset=0xf12a source_lines=2142-2155 params=3
UPVALUES ['table']
00001 [L2143] ISF      A=0 B=0 C=1 D=1 
00002 [L2143] JMP      A=3 B=128 C=47 D=32815 target=50
00003 [L2143] TGETS    A=3 B=1 C=0 D=256 'data'
00004 [L2143] ISF      A=0 B=0 C=3 D=3 
00005 [L2143] JMP      A=4 B=128 C=44 D=32812 target=50
00006 [L2144] UGET     A=3 B=0 C=0 D=0 table
00007 [L2144] TGETS    A=3 B=3 C=1 D=769 'loadstring'
00008 [L2144] TGETS    A=4 B=1 C=0 D=256 'data'
00009 [L2144] CALL     A=3 B=2 C=2 D=514 
00010 [L2145] ISF      A=0 B=0 C=3 D=3 
00011 [L2145] JMP      A=4 B=128 C=38 D=32806 target=50
00012 [L2146] TGETS    A=4 B=3 C=2 D=770 'obj_type'
00013 [L2146] GGET     A=5 B=0 C=3 D=3 'd_ms'
00014 [L2146] TGETS    A=5 B=5 C=4 D=1284 'd_common_def'
00015 [L2146] TGETS    A=5 B=5 C=5 D=1285 'object_type'
00016 [L2146] TGETS    A=5 B=5 C=6 D=1286 'item'
00017 [L2146] ISNEV    A=4 B=0 C=5 D=5 
00018 [L2146] JMP      A=4 B=128 C=6 D=32774 target=25
00019 [L2147] GGET     A=4 B=0 C=3 D=3 'd_ms'
00020 [L2147] TGETS    A=4 B=4 C=7 D=1031 'd_packageUI'
00021 [L2147] TGETS    A=4 B=4 C=8 D=1032 'removeItemsFromPackage'
00022 [L2147] MOV      A=5 B=0 C=3 D=3 
00023 [L2147] CALL     A=4 B=1 C=2 D=258 
00024 [L2147] JMP      A=4 B=128 C=25 D=32793 target=50
00025 [L2148] TGETS    A=4 B=3 C=2 D=770 'obj_type'
00026 [L2148] GGET     A=5 B=0 C=3 D=3 'd_ms'
00027 [L2148] TGETS    A=5 B=5 C=4 D=1284 'd_common_def'
00028 [L2148] TGETS    A=5 B=5 C=5 D=1285 'object_type'
00029 [L2148] TGETS    A=5 B=5 C=9 D=1289 'skill'
00030 [L2148] ISNEV    A=4 B=0 C=5 D=5 
00031 [L2148] JMP      A=4 B=128 C=6 D=32774 target=38
00032 [L2149] GGET     A=4 B=0 C=3 D=3 'd_ms'
00033 [L2149] TGETS    A=4 B=4 C=7 D=1031 'd_packageUI'
00034 [L2149] TGETS    A=4 B=4 C=8 D=1032 'removeItemsFromPackage'
00035 [L2149] MOV      A=5 B=0 C=3 D=3 
00036 [L2149] CALL     A=4 B=1 C=2 D=258 
00037 [L2149] JMP      A=4 B=128 C=12 D=32780 target=50
00038 [L2150] TGETS    A=4 B=3 C=2 D=770 'obj_type'
00039 [L2150] GGET     A=5 B=0 C=3 D=3 'd_ms'
00040 [L2150] TGETS    A=5 B=5 C=4 D=1284 'd_common_def'
00041 [L2150] TGETS    A=5 B=5 C=5 D=1285 'object_type'
00042 [L2150] TGETS    A=5 B=5 C=10 D=1290 'cortege'
00043 [L2150] ISNEV    A=4 B=0 C=5 D=5 
00044 [L2150] JMP      A=4 B=128 C=5 D=32773 target=50
00045 [L2151] GGET     A=4 B=0 C=3 D=3 'd_ms'
00046 [L2151] TGETS    A=4 B=4 C=11 D=1035 'd_lineupUI'
00047 [L2151] TGETS    A=4 B=4 C=12 D=1036 'callbackRemoveCortege'
00048 [L2151] MOV      A=5 B=0 C=3 D=3 
00049 [L2151] CALL     A=4 B=1 C=2 D=258 
00050 [L2155] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto51 offset=0xf2f0 source_lines=2157-2164 params=0
UPVALUES ['cclog']
00001 [L2159] TNEW     A=0 B=0 C=0 D=0 
00002 [L2160] KSHORT   A=1 B=0 C=0 D=0 0
00003 [L2160] TSETS    A=1 B=0 C=0 D=0 'flag'
00004 [L2162] UGET     A=1 B=0 C=0 D=0 cclog
00005 [L2162] KSTR     A=2 B=0 C=1 D=1 'try send_quit_game 1014 to bs'
00006 [L2162] CALL     A=1 B=1 C=2 D=258 
00007 [L2163] GGET     A=1 B=0 C=2 D=2 'd_ms'
00008 [L2163] TGETS    A=1 B=1 C=3 D=259 'd_u'
00009 [L2163] TGETS    A=1 B=1 C=4 D=260 'main_server_send_msg_server'
00010 [L2163] GGET     A=2 B=0 C=2 D=2 'd_ms'
00011 [L2163] TGETS    A=2 B=2 C=5 D=517 'd_msg_def'
00012 [L2163] TGETS    A=2 B=2 C=6 D=518 'gscl_msg_id'
00013 [L2163] TGETS    A=2 B=2 C=7 D=519 'msg_quit_game'
00014 [L2163] MOV      A=3 B=0 C=0 D=0 
00015 [L2163] GGET     A=4 B=0 C=2 D=2 'd_ms'
00016 [L2163] TGETS    A=4 B=4 C=8 D=1032 'd_net'
00017 [L2163] TGETS    A=4 B=4 C=9 D=1033 'g_bs'
00018 [L2163] TGETS    A=4 B=4 C=10 D=1034 'socket'
00019 [L2163] CALL     A=1 B=1 C=4 D=260 
00020 [L2164] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto52 offset=0xf3f1 source_lines=2166-2168 params=3
UPVALUES []
00001 [L2167] GGET     A=3 B=0 C=0 D=0 'd_ms'
00002 [L2167] TGETS    A=3 B=3 C=1 D=769 'd_summonUI'
00003 [L2167] TGETS    A=3 B=3 C=2 D=770 'updateSummonNews'
00004 [L2167] MOV      A=4 B=0 C=1 D=1 
00005 [L2167] CALL     A=3 B=1 C=2 D=258 
00006 [L2168] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto53 offset=0xf459 source_lines=2171-2182 params=3
UPVALUES []
00001 [L2172] TGETS    A=3 B=1 C=0 D=256 'map_count'
00002 [L2173] KSHORT   A=4 B=0 C=1 D=1 1
00003 [L2173] MOV      A=5 B=0 C=3 D=3 
00004 [L2173] KSHORT   A=6 B=0 C=1 D=1 1
00005 [L2173] FORI     A=4 B=128 C=16 D=32784 target=22
00006 [L2174] TGETS    A=8 B=1 C=1 D=257 'map_list'
00007 [L2174] TGETV    A=8 B=8 C=7 D=2055 
00008 [L2175] TGETS    A=9 B=8 C=2 D=2050 'tollgate_type'
00009 [L2175] ISNEN    A=9 B=0 C=0 D=0 1
00010 [L2175] JMP      A=9 B=128 C=10 D=32778 target=21
00011 [L2176] TNEW     A=9 B=0 C=0 D=0 
00012 [L2177] TGETS    A=10 B=8 C=3 D=2051 'map_id'
00013 [L2177] TSETS    A=10 B=9 C=3 D=2307 'map_id'
00014 [L2178] TGETS    A=10 B=8 C=4 D=2052 'pass_map'
00015 [L2178] TSETS    A=10 B=9 C=4 D=2308 'pass_map'
00016 [L2179] GGET     A=10 B=0 C=5 D=5 'd_ms'
00017 [L2179] TGETS    A=10 B=10 C=6 D=2566 'd_subLevelUI'
00018 [L2179] TGETS    A=10 B=10 C=7 D=2567 'g_mapStates'
00019 [L2179] TGETS    A=11 B=8 C=3 D=2051 'map_id'
00020 [L2179] TSETV    A=9 B=10 C=11 D=2571 
00021 [L2173] FORL     A=4 B=127 C=240 D=32752 target=6
00022 [L2182] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto54 offset=0xf563 source_lines=2190-2291 params=0
UPVALUES ['msg_table', 'cclog']
00001 [L2192] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L2192] TGETS    A=0 B=0 C=1 D=1 'd_tp_config'
00003 [L2192] TGETS    A=0 B=0 C=2 D=2 'getThirdPartyFlag'
00004 [L2192] CALL     A=0 B=2 C=1 D=513 
00005 [L2193] GGET     A=1 B=0 C=0 D=0 'd_ms'
00006 [L2193] TGETS    A=1 B=1 C=1 D=257 'd_tp_config'
00007 [L2193] TGETS    A=1 B=1 C=3 D=259 'ThirdPlatformDef'
00008 [L2194] TGETS    A=2 B=1 C=4 D=260 'oppo'
00009 [L2194] ISNEV    A=0 B=0 C=2 D=2 
00010 [L2194] JMP      A=2 B=128 C=6 D=32774 target=17
00011 [L2195] GGET     A=2 B=0 C=0 D=0 'd_ms'
00012 [L2195] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00013 [L2195] TGETS    A=2 B=2 C=6 D=518 'requestLoginOPPO'
00014 [L2195] UGET     A=3 B=0 C=0 D=0 msg_table
00015 [L2195] CALL     A=2 B=1 C=2 D=258 
00016 [L2195] JMP      A=2 B=129 C=169 D=33193 target=442
00017 [L2196] TGETS    A=2 B=1 C=7 D=263 'oppo_new_a'
00018 [L2196] ISNEV    A=0 B=0 C=2 D=2 
00019 [L2196] JMP      A=2 B=128 C=6 D=32774 target=26
00020 [L2197] GGET     A=2 B=0 C=0 D=0 'd_ms'
00021 [L2197] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00022 [L2197] TGETS    A=2 B=2 C=8 D=520 'requestLoginOPPONEWA'
00023 [L2197] UGET     A=3 B=0 C=0 D=0 msg_table
00024 [L2197] CALL     A=2 B=1 C=2 D=258 
00025 [L2197] JMP      A=2 B=129 C=160 D=33184 target=442
00026 [L2198] TGETS    A=2 B=1 C=9 D=265 'oppo_new2_a'
00027 [L2198] ISNEV    A=0 B=0 C=2 D=2 
00028 [L2198] JMP      A=2 B=128 C=6 D=32774 target=35
00029 [L2199] GGET     A=2 B=0 C=0 D=0 'd_ms'
00030 [L2199] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00031 [L2199] TGETS    A=2 B=2 C=10 D=522 'requestLoginOPPONEW2A'
00032 [L2199] UGET     A=3 B=0 C=0 D=0 msg_table
00033 [L2199] CALL     A=2 B=1 C=2 D=258 
00034 [L2199] JMP      A=2 B=129 C=151 D=33175 target=442
00035 [L2200] TGETS    A=2 B=1 C=11 D=267 'pp_i'
00036 [L2200] ISNEV    A=0 B=0 C=2 D=2 
00037 [L2200] JMP      A=2 B=128 C=6 D=32774 target=44
00038 [L2201] GGET     A=2 B=0 C=0 D=0 'd_ms'
00039 [L2201] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00040 [L2201] TGETS    A=2 B=2 C=12 D=524 'requestLoginPP'
00041 [L2201] UGET     A=3 B=0 C=0 D=0 msg_table
00042 [L2201] CALL     A=2 B=1 C=2 D=258 
00043 [L2201] JMP      A=2 B=129 C=142 D=33166 target=442
00044 [L2202] TGETS    A=2 B=1 C=13 D=269 'tb_i'
00045 [L2202] ISNEV    A=0 B=0 C=2 D=2 
00046 [L2202] JMP      A=2 B=128 C=6 D=32774 target=53
00047 [L2203] GGET     A=2 B=0 C=0 D=0 'd_ms'
00048 [L2203] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00049 [L2203] TGETS    A=2 B=2 C=14 D=526 'requestLoginTB'
00050 [L2203] UGET     A=3 B=0 C=0 D=0 msg_table
00051 [L2203] CALL     A=2 B=1 C=2 D=258 
00052 [L2203] JMP      A=2 B=129 C=133 D=33157 target=442
00053 [L2204] TGETS    A=2 B=1 C=15 D=271 'vivo_a'
00054 [L2204] ISNEV    A=0 B=0 C=2 D=2 
00055 [L2204] JMP      A=2 B=128 C=6 D=32774 target=62
00056 [L2205] GGET     A=2 B=0 C=0 D=0 'd_ms'
00057 [L2205] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00058 [L2205] TGETS    A=2 B=2 C=16 D=528 'requestLoginVIVO'
00059 [L2205] UGET     A=3 B=0 C=0 D=0 msg_table
00060 [L2205] CALL     A=2 B=1 C=2 D=258 
00061 [L2205] JMP      A=2 B=129 C=124 D=33148 target=442
00062 [L2206] TGETS    A=2 B=1 C=17 D=273 'ios'
00063 [L2206] ISEQV    A=0 B=0 C=2 D=2 
00064 [L2206] JMP      A=2 B=128 C=3 D=32771 target=68
00065 [L2206] TGETS    A=2 B=1 C=18 D=274 'ios_tw'
00066 [L2206] ISNEV    A=0 B=0 C=2 D=2 
00067 [L2206] JMP      A=2 B=128 C=6 D=32774 target=74
00068 [L2207] GGET     A=2 B=0 C=0 D=0 'd_ms'
00069 [L2207] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00070 [L2207] TGETS    A=2 B=2 C=19 D=531 'requestLoginIOS'
00071 [L2207] UGET     A=3 B=0 C=0 D=0 msg_table
00072 [L2207] CALL     A=2 B=1 C=2 D=258 
00073 [L2207] JMP      A=2 B=129 C=112 D=33136 target=442
00074 [L2208] TGETS    A=2 B=1 C=20 D=276 'uc_i'
00075 [L2208] ISNEV    A=0 B=0 C=2 D=2 
00076 [L2208] JMP      A=2 B=128 C=6 D=32774 target=83
00077 [L2209] GGET     A=2 B=0 C=0 D=0 'd_ms'
00078 [L2209] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00079 [L2209] TGETS    A=2 B=2 C=21 D=533 'requestLoginUCI'
00080 [L2209] UGET     A=3 B=0 C=0 D=0 msg_table
00081 [L2209] CALL     A=2 B=1 C=2 D=258 
00082 [L2209] JMP      A=2 B=129 C=103 D=33127 target=442
00083 [L2210] TGETS    A=2 B=1 C=22 D=278 'p91_i'
00084 [L2210] ISNEV    A=0 B=0 C=2 D=2 
00085 [L2210] JMP      A=2 B=128 C=6 D=32774 target=92
00086 [L2211] GGET     A=2 B=0 C=0 D=0 'd_ms'
00087 [L2211] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00088 [L2211] TGETS    A=2 B=2 C=23 D=535 'requestLoginP91I'
00089 [L2211] UGET     A=3 B=0 C=0 D=0 msg_table
00090 [L2211] CALL     A=2 B=1 C=2 D=258 
00091 [L2211] JMP      A=2 B=129 C=94 D=33118 target=442
00092 [L2212] TGETS    A=2 B=1 C=24 D=280 'p91n_i'
00093 [L2212] ISNEV    A=0 B=0 C=2 D=2 
00094 [L2212] JMP      A=2 B=128 C=6 D=32774 target=101
00095 [L2213] GGET     A=2 B=0 C=0 D=0 'd_ms'
00096 [L2213] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00097 [L2213] TGETS    A=2 B=2 C=25 D=537 'requestLoginP91NI'
00098 [L2213] UGET     A=3 B=0 C=0 D=0 msg_table
00099 [L2213] CALL     A=2 B=1 C=2 D=258 
00100 [L2213] JMP      A=2 B=129 C=85 D=33109 target=442
00101 [L2214] TGETS    A=2 B=1 C=26 D=282 'p91_a'
00102 [L2214] ISEQV    A=0 B=0 C=2 D=2 
00103 [L2214] JMP      A=2 B=128 C=3 D=32771 target=107
00104 [L2214] TGETS    A=2 B=1 C=27 D=283 'p91n_a'
00105 [L2214] ISNEV    A=0 B=0 C=2 D=2 
00106 [L2214] JMP      A=2 B=128 C=6 D=32774 target=113
00107 [L2215] GGET     A=2 B=0 C=0 D=0 'd_ms'
00108 [L2215] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00109 [L2215] TGETS    A=2 B=2 C=28 D=540 'requestLoginP91a'
00110 [L2215] UGET     A=3 B=0 C=0 D=0 msg_table
00111 [L2215] CALL     A=2 B=1 C=2 D=258 
00112 [L2215] JMP      A=2 B=129 C=73 D=33097 target=442
00113 [L2216] TGETS    A=2 B=1 C=29 D=285 'dj_i'
00114 [L2216] ISNEV    A=0 B=0 C=2 D=2 
00115 [L2216] JMP      A=2 B=128 C=6 D=32774 target=122
00116 [L2217] GGET     A=2 B=0 C=0 D=0 'd_ms'
00117 [L2217] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00118 [L2217] TGETS    A=2 B=2 C=30 D=542 'requestLoginDJIOS'
00119 [L2217] UGET     A=3 B=0 C=0 D=0 msg_table
00120 [L2217] CALL     A=2 B=1 C=2 D=258 
00121 [L2217] JMP      A=2 B=129 C=64 D=33088 target=442
00122 [L2218] TGETS    A=2 B=1 C=31 D=287 'uc_a'
00123 [L2218] ISNEV    A=0 B=0 C=2 D=2 
00124 [L2218] JMP      A=2 B=128 C=6 D=32774 target=131
00125 [L2219] GGET     A=2 B=0 C=0 D=0 'd_ms'
00126 [L2219] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00127 [L2219] TGETS    A=2 B=2 C=32 D=544 'requestLoginUCA'
00128 [L2219] UGET     A=3 B=0 C=0 D=0 msg_table
00129 [L2219] CALL     A=2 B=1 C=2 D=258 
00130 [L2219] JMP      A=2 B=129 C=55 D=33079 target=442
00131 [L2220] TGETS    A=2 B=1 C=33 D=289 'p360_a'
00132 [L2220] ISNEV    A=0 B=0 C=2 D=2 
00133 [L2220] JMP      A=2 B=128 C=6 D=32774 target=140
00134 [L2221] GGET     A=2 B=0 C=0 D=0 'd_ms'
00135 [L2221] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00136 [L2221] TGETS    A=2 B=2 C=34 D=546 'requestLoginP360a'
00137 [L2221] UGET     A=3 B=0 C=0 D=0 msg_table
00138 [L2221] CALL     A=2 B=1 C=2 D=258 
00139 [L2221] JMP      A=2 B=129 C=46 D=33070 target=442
00140 [L2222] TGETS    A=2 B=1 C=35 D=291 'p360_na'
00141 [L2222] ISNEV    A=0 B=0 C=2 D=2 
00142 [L2222] JMP      A=2 B=128 C=6 D=32774 target=149
00143 [L2223] GGET     A=2 B=0 C=0 D=0 'd_ms'
00144 [L2223] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00145 [L2223] TGETS    A=2 B=2 C=36 D=548 'requestLoginP360_na'
00146 [L2223] UGET     A=3 B=0 C=0 D=0 msg_table
00147 [L2223] CALL     A=2 B=1 C=2 D=258 
00148 [L2223] JMP      A=2 B=129 C=37 D=33061 target=442
00149 [L2224] TGETS    A=2 B=1 C=37 D=293 'bd_a'
00150 [L2224] ISNEV    A=0 B=0 C=2 D=2 
00151 [L2224] JMP      A=2 B=128 C=6 D=32774 target=158
00152 [L2225] GGET     A=2 B=0 C=0 D=0 'd_ms'
00153 [L2225] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00154 [L2225] TGETS    A=2 B=2 C=38 D=550 'requestLoginBD'
00155 [L2225] UGET     A=3 B=0 C=0 D=0 msg_table
00156 [L2225] CALL     A=2 B=1 C=2 D=258 
00157 [L2225] JMP      A=2 B=129 C=28 D=33052 target=442
00158 [L2226] TGETS    A=2 B=1 C=39 D=295 'ky_i'
00159 [L2226] ISNEV    A=0 B=0 C=2 D=2 
00160 [L2226] JMP      A=2 B=128 C=6 D=32774 target=167
00161 [L2227] GGET     A=2 B=0 C=0 D=0 'd_ms'
00162 [L2227] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00163 [L2227] TGETS    A=2 B=2 C=40 D=552 'requestLoginKYI'
00164 [L2227] UGET     A=3 B=0 C=0 D=0 msg_table
00165 [L2227] CALL     A=2 B=1 C=2 D=258 
00166 [L2227] JMP      A=2 B=129 C=19 D=33043 target=442
00167 [L2228] TGETS    A=2 B=1 C=41 D=297 'lnv_a'
00168 [L2228] ISNEV    A=0 B=0 C=2 D=2 
00169 [L2228] JMP      A=2 B=128 C=6 D=32774 target=176
00170 [L2229] GGET     A=2 B=0 C=0 D=0 'd_ms'
00171 [L2229] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00172 [L2229] TGETS    A=2 B=2 C=42 D=554 'requestLoginLenovo'
00173 [L2229] UGET     A=3 B=0 C=0 D=0 msg_table
00174 [L2229] CALL     A=2 B=1 C=2 D=258 
00175 [L2229] JMP      A=2 B=129 C=10 D=33034 target=442
00176 [L2230] TGETS    A=2 B=1 C=43 D=299 'lnv_new_a'
00177 [L2230] ISNEV    A=0 B=0 C=2 D=2 
00178 [L2230] JMP      A=2 B=128 C=6 D=32774 target=185
00179 [L2231] GGET     A=2 B=0 C=0 D=0 'd_ms'
00180 [L2231] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00181 [L2231] TGETS    A=2 B=2 C=44 D=556 'requestLoginLenovo_new_a'
00182 [L2231] UGET     A=3 B=0 C=0 D=0 msg_table
00183 [L2231] CALL     A=2 B=1 C=2 D=258 
00184 [L2231] JMP      A=2 B=129 C=1 D=33025 target=442
00185 [L2232] TGETS    A=2 B=1 C=45 D=301 'xm_a'
00186 [L2232] ISNEV    A=0 B=0 C=2 D=2 
00187 [L2232] JMP      A=2 B=128 C=6 D=32774 target=194
00188 [L2233] GGET     A=2 B=0 C=0 D=0 'd_ms'
00189 [L2233] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00190 [L2233] TGETS    A=2 B=2 C=46 D=558 'requestLoginXMA'
00191 [L2233] UGET     A=3 B=0 C=0 D=0 msg_table
00192 [L2233] CALL     A=2 B=1 C=2 D=258 
00193 [L2233] JMP      A=2 B=128 C=248 D=33016 target=442
00194 [L2234] TGETS    A=2 B=1 C=47 D=303 'dj_a'
00195 [L2234] ISNEV    A=0 B=0 C=2 D=2 
00196 [L2234] JMP      A=2 B=128 C=6 D=32774 target=203
00197 [L2235] GGET     A=2 B=0 C=0 D=0 'd_ms'
00198 [L2235] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00199 [L2235] TGETS    A=2 B=2 C=48 D=560 'requestLoginDJA'
00200 [L2235] UGET     A=3 B=0 C=0 D=0 msg_table
00201 [L2235] CALL     A=2 B=1 C=2 D=258 
00202 [L2235] JMP      A=2 B=128 C=239 D=33007 target=442
00203 [L2236] TGETS    A=2 B=1 C=49 D=305 'wdj_a'
00204 [L2236] ISNEV    A=0 B=0 C=2 D=2 
00205 [L2236] JMP      A=2 B=128 C=6 D=32774 target=212
00206 [L2237] GGET     A=2 B=0 C=0 D=0 'd_ms'
00207 [L2237] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00208 [L2237] TGETS    A=2 B=2 C=50 D=562 'requestLoginWDJA'
00209 [L2237] UGET     A=3 B=0 C=0 D=0 msg_table
00210 [L2237] CALL     A=2 B=1 C=2 D=258 
00211 [L2237] JMP      A=2 B=128 C=230 D=32998 target=442
00212 [L2238] TGETS    A=2 B=1 C=51 D=307 'gfan_a'
00213 [L2238] ISNEV    A=0 B=0 C=2 D=2 
00214 [L2238] JMP      A=2 B=128 C=6 D=32774 target=221
00215 [L2239] GGET     A=2 B=0 C=0 D=0 'd_ms'
00216 [L2239] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00217 [L2239] TGETS    A=2 B=2 C=52 D=564 'requestLoginGFANA'
00218 [L2239] UGET     A=3 B=0 C=0 D=0 msg_table
00219 [L2239] CALL     A=2 B=1 C=2 D=258 
00220 [L2239] JMP      A=2 B=128 C=221 D=32989 target=442
00221 [L2240] TGETS    A=2 B=1 C=53 D=309 'az_a'
00222 [L2240] ISNEV    A=0 B=0 C=2 D=2 
00223 [L2240] JMP      A=2 B=128 C=6 D=32774 target=230
00224 [L2241] GGET     A=2 B=0 C=0 D=0 'd_ms'
00225 [L2241] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00226 [L2241] TGETS    A=2 B=2 C=54 D=566 'requestLoginAnZhi'
00227 [L2241] UGET     A=3 B=0 C=0 D=0 msg_table
00228 [L2241] CALL     A=2 B=1 C=2 D=258 
00229 [L2241] JMP      A=2 B=128 C=212 D=32980 target=442
00230 [L2242] TGETS    A=2 B=1 C=55 D=311 'hw_a'
00231 [L2242] ISNEV    A=0 B=0 C=2 D=2 
00232 [L2242] JMP      A=2 B=128 C=6 D=32774 target=239
00233 [L2243] GGET     A=2 B=0 C=0 D=0 'd_ms'
00234 [L2243] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00235 [L2243] TGETS    A=2 B=2 C=56 D=568 'requestLoginHW'
00236 [L2243] UGET     A=3 B=0 C=0 D=0 msg_table
00237 [L2243] CALL     A=2 B=1 C=2 D=258 
00238 [L2243] JMP      A=2 B=128 C=203 D=32971 target=442
00239 [L2244] TGETS    A=2 B=1 C=57 D=313 'itools_i'
00240 [L2244] ISNEV    A=0 B=0 C=2 D=2 
00241 [L2244] JMP      A=2 B=128 C=6 D=32774 target=248
00242 [L2245] GGET     A=2 B=0 C=0 D=0 'd_ms'
00243 [L2245] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00244 [L2245] TGETS    A=2 B=2 C=58 D=570 'requestLoginITOOLSI'
00245 [L2245] UGET     A=3 B=0 C=0 D=0 msg_table
00246 [L2245] CALL     A=2 B=1 C=2 D=258 
00247 [L2245] JMP      A=2 B=128 C=194 D=32962 target=442
00248 [L2246] TGETS    A=2 B=1 C=59 D=315 'yyh_a'
00249 [L2246] ISNEV    A=0 B=0 C=2 D=2 
00250 [L2246] JMP      A=2 B=128 C=6 D=32774 target=257
00251 [L2247] GGET     A=2 B=0 C=0 D=0 'd_ms'
00252 [L2247] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00253 [L2247] TGETS    A=2 B=2 C=60 D=572 'requestLogin_YYF'
00254 [L2247] UGET     A=3 B=0 C=0 D=0 msg_table
00255 [L2247] CALL     A=2 B=1 C=2 D=258 
00256 [L2247] JMP      A=2 B=128 C=185 D=32953 target=442
00257 [L2248] TGETS    A=2 B=1 C=61 D=317 'mzw_a'
00258 [L2248] ISNEV    A=0 B=0 C=2 D=2 
00259 [L2248] JMP      A=2 B=128 C=6 D=32774 target=266
00260 [L2249] GGET     A=2 B=0 C=0 D=0 'd_ms'
00261 [L2249] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00262 [L2249] TGETS    A=2 B=2 C=62 D=574 'requestLoginMZWA'
00263 [L2249] UGET     A=3 B=0 C=0 D=0 msg_table
00264 [L2249] CALL     A=2 B=1 C=2 D=258 
00265 [L2249] JMP      A=2 B=128 C=176 D=32944 target=442
00266 [L2250] TGETS    A=2 B=1 C=63 D=319 'yj_a'
00267 [L2250] ISNEV    A=0 B=0 C=2 D=2 
00268 [L2250] JMP      A=2 B=128 C=6 D=32774 target=275
00269 [L2251] GGET     A=2 B=0 C=0 D=0 'd_ms'
00270 [L2251] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00271 [L2251] TGETS    A=2 B=2 C=64 D=576 'requestLoginYJA'
00272 [L2251] UGET     A=3 B=0 C=0 D=0 msg_table
00273 [L2251] CALL     A=2 B=1 C=2 D=258 
00274 [L2251] JMP      A=2 B=128 C=167 D=32935 target=442
00275 [L2252] TGETS    A=2 B=1 C=65 D=321 'yx_a'
00276 [L2252] ISNEV    A=0 B=0 C=2 D=2 
00277 [L2252] JMP      A=2 B=128 C=6 D=32774 target=284
00278 [L2253] GGET     A=2 B=0 C=0 D=0 'd_ms'
00279 [L2253] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00280 [L2253] TGETS    A=2 B=2 C=66 D=578 'requestLoginYXA'
00281 [L2253] UGET     A=3 B=0 C=0 D=0 msg_table
00282 [L2253] CALL     A=2 B=1 C=2 D=258 
00283 [L2253] JMP      A=2 B=128 C=158 D=32926 target=442
00284 [L2254] TGETS    A=2 B=1 C=67 D=323 'amigo_a'
00285 [L2254] ISNEV    A=0 B=0 C=2 D=2 
00286 [L2254] JMP      A=2 B=128 C=6 D=32774 target=293
00287 [L2255] GGET     A=2 B=0 C=0 D=0 'd_ms'
00288 [L2255] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00289 [L2255] TGETS    A=2 B=2 C=68 D=580 'requestLoginAmigoA'
00290 [L2255] UGET     A=3 B=0 C=0 D=0 msg_table
00291 [L2255] CALL     A=2 B=1 C=2 D=258 
00292 [L2255] JMP      A=2 B=128 C=149 D=32917 target=442
00293 [L2256] TGETS    A=2 B=1 C=69 D=325 'yy_a'
00294 [L2256] ISNEV    A=0 B=0 C=2 D=2 
00295 [L2256] JMP      A=2 B=128 C=6 D=32774 target=302
00296 [L2257] GGET     A=2 B=0 C=0 D=0 'd_ms'
00297 [L2257] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00298 [L2257] TGETS    A=2 B=2 C=70 D=582 'requestLoginYYA'
00299 [L2257] UGET     A=3 B=0 C=0 D=0 msg_table
00300 [L2257] CALL     A=2 B=1 C=2 D=258 
00301 [L2257] JMP      A=2 B=128 C=140 D=32908 target=442
00302 [L2258] TGETS    A=2 B=1 C=71 D=327 'tw_i'
00303 [L2258] ISNEV    A=0 B=0 C=2 D=2 
00304 [L2258] JMP      A=2 B=128 C=6 D=32774 target=311
00305 [L2259] GGET     A=2 B=0 C=0 D=0 'd_ms'
00306 [L2259] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00307 [L2259] TGETS    A=2 B=2 C=72 D=584 'requestLoginTWI'
00308 [L2259] UGET     A=3 B=0 C=0 D=0 msg_table
00309 [L2259] CALL     A=2 B=1 C=2 D=258 
00310 [L2259] JMP      A=2 B=128 C=131 D=32899 target=442
00311 [L2260] TGETS    A=2 B=1 C=73 D=329 'tw_a'
00312 [L2260] ISNEV    A=0 B=0 C=2 D=2 
00313 [L2260] JMP      A=2 B=128 C=6 D=32774 target=320
00314 [L2261] GGET     A=2 B=0 C=0 D=0 'd_ms'
00315 [L2261] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00316 [L2261] TGETS    A=2 B=2 C=74 D=586 'requestLoginTWA'
00317 [L2261] UGET     A=3 B=0 C=0 D=0 msg_table
00318 [L2261] CALL     A=2 B=1 C=2 D=258 
00319 [L2261] JMP      A=2 B=128 C=122 D=32890 target=442
00320 [L2262] TGETS    A=2 B=1 C=75 D=331 'p37wan_a'
00321 [L2262] ISNEV    A=0 B=0 C=2 D=2 
00322 [L2262] JMP      A=2 B=128 C=6 D=32774 target=329
00323 [L2263] GGET     A=2 B=0 C=0 D=0 'd_ms'
00324 [L2263] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00325 [L2263] TGETS    A=2 B=2 C=76 D=588 'requestLoginP37WANA'
00326 [L2263] UGET     A=3 B=0 C=0 D=0 msg_table
00327 [L2263] CALL     A=2 B=1 C=2 D=258 
00328 [L2263] JMP      A=2 B=128 C=113 D=32881 target=442
00329 [L2264] TGETS    A=2 B=1 C=77 D=333 'meizu_a'
00330 [L2264] ISNEV    A=0 B=0 C=2 D=2 
00331 [L2264] JMP      A=2 B=128 C=6 D=32774 target=338
00332 [L2265] GGET     A=2 B=0 C=0 D=0 'd_ms'
00333 [L2265] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00334 [L2265] TGETS    A=2 B=2 C=78 D=590 'requestLoginMeizuA'
00335 [L2265] UGET     A=3 B=0 C=0 D=0 msg_table
00336 [L2265] CALL     A=2 B=1 C=2 D=258 
00337 [L2265] JMP      A=2 B=128 C=104 D=32872 target=442
00338 [L2266] TGETS    A=2 B=1 C=79 D=335 'xunlei_a'
00339 [L2266] ISNEV    A=0 B=0 C=2 D=2 
00340 [L2266] JMP      A=2 B=128 C=6 D=32774 target=347
00341 [L2267] GGET     A=2 B=0 C=0 D=0 'd_ms'
00342 [L2267] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00343 [L2267] TGETS    A=2 B=2 C=80 D=592 'requestLoginXunlei_a'
00344 [L2267] UGET     A=3 B=0 C=0 D=0 msg_table
00345 [L2267] CALL     A=2 B=1 C=2 D=258 
00346 [L2267] JMP      A=2 B=128 C=95 D=32863 target=442
00347 [L2268] TGETS    A=2 B=1 C=81 D=337 'kp_a'
00348 [L2268] ISNEV    A=0 B=0 C=2 D=2 
00349 [L2268] JMP      A=2 B=128 C=6 D=32774 target=356
00350 [L2269] GGET     A=2 B=0 C=0 D=0 'd_ms'
00351 [L2269] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00352 [L2269] TGETS    A=2 B=2 C=82 D=594 'requestLoginKPA'
00353 [L2269] UGET     A=3 B=0 C=0 D=0 msg_table
00354 [L2269] CALL     A=2 B=1 C=2 D=258 
00355 [L2269] JMP      A=2 B=128 C=86 D=32854 target=442
00356 [L2270] TGETS    A=2 B=1 C=83 D=339 'yyb_qq_a'
00357 [L2270] ISNEV    A=0 B=0 C=2 D=2 
00358 [L2270] JMP      A=2 B=128 C=6 D=32774 target=365
00359 [L2271] GGET     A=2 B=0 C=0 D=0 'd_ms'
00360 [L2271] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00361 [L2271] TGETS    A=2 B=2 C=84 D=596 'requestLoginQQ'
00362 [L2271] UGET     A=3 B=0 C=0 D=0 msg_table
00363 [L2271] CALL     A=2 B=1 C=2 D=258 
00364 [L2271] JMP      A=2 B=128 C=77 D=32845 target=442
00365 [L2272] TGETS    A=2 B=1 C=85 D=341 'yyb_wx_a'
00366 [L2272] ISNEV    A=0 B=0 C=2 D=2 
00367 [L2272] JMP      A=2 B=128 C=6 D=32774 target=374
00368 [L2273] GGET     A=2 B=0 C=0 D=0 'd_ms'
00369 [L2273] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00370 [L2273] TGETS    A=2 B=2 C=86 D=598 'requestLoginWX'
00371 [L2273] UGET     A=3 B=0 C=0 D=0 msg_table
00372 [L2273] CALL     A=2 B=1 C=2 D=258 
00373 [L2273] JMP      A=2 B=128 C=68 D=32836 target=442
00374 [L2274] TGETS    A=2 B=1 C=87 D=343 'lengjing'
00375 [L2274] ISNEV    A=0 B=0 C=2 D=2 
00376 [L2274] JMP      A=2 B=128 C=6 D=32774 target=383
00377 [L2275] GGET     A=2 B=0 C=0 D=0 'd_ms'
00378 [L2275] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00379 [L2275] TGETS    A=2 B=2 C=88 D=600 'requestLoginLengJing'
00380 [L2275] UGET     A=3 B=0 C=0 D=0 msg_table
00381 [L2275] CALL     A=2 B=1 C=2 D=258 
00382 [L2275] JMP      A=2 B=128 C=59 D=32827 target=442
00383 [L2276] TGETS    A=2 B=1 C=89 D=345 'p91bn_a'
00384 [L2276] ISNEV    A=0 B=0 C=2 D=2 
00385 [L2276] JMP      A=2 B=128 C=6 D=32774 target=392
00386 [L2277] GGET     A=2 B=0 C=0 D=0 'd_ms'
00387 [L2277] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00388 [L2277] TGETS    A=2 B=2 C=90 D=602 'requestLoginP91bn_a'
00389 [L2277] UGET     A=3 B=0 C=0 D=0 msg_table
00390 [L2277] CALL     A=2 B=1 C=2 D=258 
00391 [L2277] JMP      A=2 B=128 C=50 D=32818 target=442
00392 [L2278] TGETS    A=2 B=1 C=91 D=347 'bdn_a'
00393 [L2278] ISNEV    A=0 B=0 C=2 D=2 
00394 [L2278] JMP      A=2 B=128 C=6 D=32774 target=401
00395 [L2279] GGET     A=2 B=0 C=0 D=0 'd_ms'
00396 [L2279] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00397 [L2279] TGETS    A=2 B=2 C=92 D=604 'requestLoginbdn'
00398 [L2279] UGET     A=3 B=0 C=0 D=0 msg_table
00399 [L2279] CALL     A=2 B=1 C=2 D=258 
00400 [L2279] JMP      A=2 B=128 C=41 D=32809 target=442
00401 [L2280] TGETS    A=2 B=1 C=93 D=349 'openxlive_wp'
00402 [L2280] ISNEV    A=0 B=0 C=2 D=2 
00403 [L2280] JMP      A=2 B=128 C=6 D=32774 target=410
00404 [L2281] GGET     A=2 B=0 C=0 D=0 'd_ms'
00405 [L2281] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00406 [L2281] TGETS    A=2 B=2 C=94 D=606 'requestLoginOpenxlive_wp'
00407 [L2281] UGET     A=3 B=0 C=0 D=0 msg_table
00408 [L2281] CALL     A=2 B=1 C=2 D=258 
00409 [L2281] JMP      A=2 B=128 C=32 D=32800 target=442
00410 [L2282] TGETS    A=2 B=1 C=95 D=351 'sy_wp_a'
00411 [L2282] ISNEV    A=0 B=0 C=2 D=2 
00412 [L2282] JMP      A=2 B=128 C=6 D=32774 target=419
00413 [L2283] GGET     A=2 B=0 C=0 D=0 'd_ms'
00414 [L2283] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00415 [L2283] TGETS    A=2 B=2 C=96 D=608 'requestLogin_sy_wp_a'
00416 [L2283] UGET     A=3 B=0 C=0 D=0 msg_table
00417 [L2283] CALL     A=2 B=1 C=2 D=258 
00418 [L2283] JMP      A=2 B=128 C=23 D=32791 target=442
00419 [L2284] TGETS    A=2 B=1 C=97 D=353 'qmdy'
00420 [L2284] ISNEV    A=0 B=0 C=2 D=2 
00421 [L2284] JMP      A=2 B=128 C=6 D=32774 target=428
00422 [L2285] GGET     A=2 B=0 C=0 D=0 'd_ms'
00423 [L2285] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00424 [L2285] TGETS    A=2 B=2 C=98 D=610 'requestLogin_qmdy'
00425 [L2285] UGET     A=3 B=0 C=0 D=0 msg_table
00426 [L2285] CALL     A=2 B=1 C=2 D=258 
00427 [L2285] JMP      A=2 B=128 C=14 D=32782 target=442
00428 [L2286] TGETS    A=2 B=1 C=99 D=355 'wdj_a2'
00429 [L2286] ISNEV    A=0 B=0 C=2 D=2 
00430 [L2286] JMP      A=2 B=128 C=6 D=32774 target=437
00431 [L2287] GGET     A=2 B=0 C=0 D=0 'd_ms'
00432 [L2287] TGETS    A=2 B=2 C=5 D=517 'd_loginUI'
00433 [L2287] TGETS    A=2 B=2 C=100 D=612 'requestLoginWDJA2'
00434 [L2287] UGET     A=3 B=0 C=0 D=0 msg_table
00435 [L2287] CALL     A=2 B=1 C=2 D=258 
00436 [L2287] JMP      A=2 B=128 C=5 D=32773 target=442
00437 [L2289] UGET     A=2 B=0 C=1 D=1 cclog
00438 [L2289] KSTR     A=3 B=0 C=101 D=101 'ERROR: unhandle tp login or pay event, type='
00439 [L2289] MOV      A=4 B=0 C=0 D=0 
00440 [L2289] CAT      A=3 B=3 C=4 D=772 
00441 [L2289] CALL     A=2 B=1 C=2 D=258 
00442 [L2291] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto55 offset=0x10342 source_lines=2184-2299 params=3
UPVALUES ['cclog', 'CCDirector']
00001 [L2185] UGET     A=3 B=0 C=0 D=0 cclog
00002 [L2185] KSTR     A=4 B=0 C=0 D=0 'call event_msg_third_party_platform_22'
00003 [L2185] CALL     A=3 B=1 C=2 D=258 
00004 [L2186] UGET     A=3 B=0 C=1 D=1 CCDirector
00005 [L2186] MOV      A=4 B=0 C=3 D=3 
00006 [L2186] TGETS    A=3 B=3 C=1 D=769 'sharedDirector'
00007 [L2186] CALL     A=3 B=2 C=2 D=514 
00008 [L2186] MOV      A=4 B=0 C=3 D=3 
00009 [L2186] TGETS    A=3 B=3 C=2 D=770 'isPaused'
00010 [L2186] CALL     A=3 B=2 C=2 D=514 
00011 [L2186] ISF      A=0 B=0 C=3 D=3 
00012 [L2186] JMP      A=4 B=128 C=7 D=32775 target=20
00013 [L2187] UGET     A=3 B=0 C=1 D=1 CCDirector
00014 [L2187] MOV      A=4 B=0 C=3 D=3 
00015 [L2187] TGETS    A=3 B=3 C=1 D=769 'sharedDirector'
00016 [L2187] CALL     A=3 B=2 C=2 D=514 
00017 [L2187] MOV      A=4 B=0 C=3 D=3 
00018 [L2187] TGETS    A=3 B=3 C=3 D=771 'resume'
00019 [L2187] CALL     A=3 B=1 C=2 D=258 
00020 [L2291] FNEW     A=3 B=0 C=4 D=4 {'kind': 'proto', 'id': 54}
00021 [L2293] GGET     A=4 B=0 C=5 D=5 'd_ms'
00022 [L2293] TGETS    A=4 B=4 C=6 D=1030 'd_u'
00023 [L2293] TGETS    A=4 B=4 C=7 D=1031 'isIOS'
00024 [L2293] CALL     A=4 B=2 C=1 D=513 
00025 [L2293] IST      A=0 B=0 C=4 D=4 
00026 [L2293] JMP      A=5 B=128 C=6 D=32774 target=33
00027 [L2293] GGET     A=4 B=0 C=5 D=5 'd_ms'
00028 [L2293] TGETS    A=4 B=4 C=6 D=1030 'd_u'
00029 [L2293] TGETS    A=4 B=4 C=8 D=1032 'isWP8'
00030 [L2293] CALL     A=4 B=2 C=1 D=513 
00031 [L2293] ISF      A=0 B=0 C=4 D=4 
00032 [L2293] JMP      A=5 B=128 C=3 D=32771 target=36
00033 [L2295] MOV      A=4 B=0 C=3 D=3 
00034 [L2295] CALL     A=4 B=1 C=1 D=257 
00035 [L2295] JMP      A=4 B=128 C=6 D=32774 target=42
00036 [L2297] GGET     A=4 B=0 C=5 D=5 'd_ms'
00037 [L2297] TGETS    A=4 B=4 C=6 D=1030 'd_u'
00038 [L2297] TGETS    A=4 B=4 C=9 D=1033 'delay_node'
00039 [L2297] KSHORT   A=5 B=0 C=0 D=0 0
00040 [L2297] MOV      A=6 B=0 C=3 D=3 
00041 [L2297] CALL     A=4 B=1 C=3 D=259 
00042 [L2299] UCLO     A=0 B=128 C=0 D=32768 target=43
00043 [L2299] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto56 offset=0x104ce source_lines=2301-2304 params=3
UPVALUES []
00001 [L2302] GGET     A=3 B=0 C=0 D=0 'd_ms'
00002 [L2302] TGETS    A=3 B=3 C=1 D=769 'd_alert'
00003 [L2302] TGETS    A=3 B=3 C=2 D=770 'stop_wait'
00004 [L2302] CALL     A=3 B=1 C=1 D=257 
00005 [L2303] GGET     A=3 B=0 C=0 D=0 'd_ms'
00006 [L2303] TGETS    A=3 B=3 C=3 D=771 'd_saodangUI'
00007 [L2303] TGETS    A=3 B=3 C=4 D=772 'getRefreshRes'
00008 [L2303] CALL     A=3 B=1 C=1 D=257 
00009 [L2304] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto57 offset=0x10555 source_lines=2307-2310 params=3
UPVALUES []
00001 [L2308] GGET     A=3 B=0 C=0 D=0 'd_ms'
00002 [L2308] TGETS    A=3 B=3 C=1 D=769 'd_alert'
00003 [L2308] TGETS    A=3 B=3 C=2 D=770 'stop_wait'
00004 [L2308] CALL     A=3 B=1 C=1 D=257 
00005 [L2309] GGET     A=3 B=0 C=0 D=0 'd_ms'
00006 [L2309] TGETS    A=3 B=3 C=3 D=771 'd_messageUI'
00007 [L2309] TGETS    A=3 B=3 C=4 D=772 'callback_activity_msg_update'
00008 [L2309] MOV      A=4 B=0 C=1 D=1 
00009 [L2309] MOV      A=5 B=0 C=2 D=2 
00010 [L2309] CALL     A=3 B=1 C=3 D=259 
00011 [L2310] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto58 offset=0x105f4 source_lines=2312-2314 params=3
UPVALUES []
00001 [L2313] GGET     A=3 B=0 C=0 D=0 'd_ms'
00002 [L2313] TGETS    A=3 B=3 C=1 D=769 'd_achieveUI'
00003 [L2313] TGETS    A=3 B=3 C=2 D=770 'onGetAchieves'
00004 [L2313] MOV      A=4 B=0 C=1 D=1 
00005 [L2313] CALL     A=3 B=1 C=2 D=258 
00006 [L2314] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto59 offset=0x10659 source_lines=2316-2318 params=3
UPVALUES []
00001 [L2317] GGET     A=3 B=0 C=0 D=0 'd_ms'
00002 [L2317] TGETS    A=3 B=3 C=1 D=769 'd_honorUI'
00003 [L2317] TGETS    A=3 B=3 C=2 D=770 'onGetTitles'
00004 [L2317] MOV      A=4 B=0 C=1 D=1 
00005 [L2317] CALL     A=3 B=1 C=2 D=258 
00006 [L2318] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto60 offset=0x106bb source_lines=2320-2323 params=3
UPVALUES ['table']
00001 [L2321] UGET     A=3 B=0 C=0 D=0 table
00002 [L2321] TGETS    A=3 B=3 C=0 D=768 'loadstring'
00003 [L2321] TGETS    A=4 B=1 C=1 D=257 'data'
00004 [L2321] CALL     A=3 B=2 C=2 D=514 
00005 [L2322] GGET     A=4 B=0 C=2 D=2 'd_ms'
00006 [L2322] TGETS    A=4 B=4 C=3 D=1027 'd_homeUI'
00007 [L2322] TGETS    A=4 B=4 C=4 D=1028 'onGetResult'
00008 [L2322] TGETS    A=5 B=1 C=5 D=261 'id'
00009 [L2322] MOV      A=6 B=0 C=3 D=3 
00010 [L2322] CALL     A=4 B=1 C=3 D=259 
00011 [L2323] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto61 offset=0x1075d source_lines=2325-2328 params=3
UPVALUES ['table']
00001 [L2326] UGET     A=3 B=0 C=0 D=0 table
00002 [L2326] TGETS    A=3 B=3 C=0 D=768 'loadstring'
00003 [L2326] TGETS    A=4 B=1 C=1 D=257 'data'
00004 [L2326] CALL     A=3 B=2 C=2 D=514 
00005 [L2327] GGET     A=4 B=0 C=2 D=2 'd_ms'
00006 [L2327] TGETS    A=4 B=4 C=3 D=1027 'd_undergoOrdealUI'
00007 [L2327] TGETS    A=4 B=4 C=4 D=1028 'onGetResult'
00008 [L2327] TGETS    A=5 B=1 C=5 D=261 'id'
00009 [L2327] MOV      A=6 B=0 C=3 D=3 
00010 [L2327] CALL     A=4 B=1 C=3 D=259 
00011 [L2328] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto62 offset=0x10808 source_lines=2331-2351 params=3
UPVALUES []
00001 [L2332] TGETS    A=3 B=1 C=0 D=256 'tip_type'
00002 [L2332] GGET     A=4 B=0 C=1 D=1 't_t'
00003 [L2332] TGETS    A=4 B=4 C=2 D=1026 'tip'
00004 [L2332] ISNEV    A=3 B=0 C=4 D=4 
00005 [L2332] JMP      A=3 B=128 C=6 D=32774 target=12
00006 [L2333] GGET     A=3 B=0 C=3 D=3 'd_ms'
00007 [L2333] TGETS    A=3 B=3 C=4 D=772 'd_xianmengUI'
00008 [L2333] TGETS    A=3 B=3 C=5 D=773 'getXianMengTip'
00009 [L2333] MOV      A=4 B=0 C=1 D=1 
00010 [L2333] CALL     A=3 B=1 C=2 D=258 
00011 [L2333] JMP      A=3 B=128 C=86 D=32854 target=98
00012 [L2334] TGETS    A=3 B=1 C=0 D=256 'tip_type'
00013 [L2334] GGET     A=4 B=0 C=1 D=1 't_t'
00014 [L2334] TGETS    A=4 B=4 C=6 D=1030 'update_prey'
00015 [L2334] ISNEV    A=3 B=0 C=4 D=4 
00016 [L2334] JMP      A=3 B=128 C=6 D=32774 target=23
00017 [L2335] GGET     A=3 B=0 C=3 D=3 'd_ms'
00018 [L2335] TGETS    A=3 B=3 C=7 D=775 'd_landUI'
00019 [L2335] TGETS    A=3 B=3 C=8 D=776 'updateStatus'
00020 [L2335] MOV      A=4 B=0 C=1 D=1 
00021 [L2335] CALL     A=3 B=1 C=2 D=258 
00022 [L2335] JMP      A=3 B=128 C=75 D=32843 target=98
00023 [L2336] TGETS    A=3 B=1 C=0 D=256 'tip_type'
00024 [L2336] GGET     A=4 B=0 C=1 D=1 't_t'
00025 [L2336] TGETS    A=4 B=4 C=9 D=1033 'update_vip_shop'
00026 [L2336] ISNEV    A=3 B=0 C=4 D=4 
00027 [L2336] JMP      A=3 B=128 C=6 D=32774 target=34
00028 [L2337] GGET     A=3 B=0 C=3 D=3 'd_ms'
00029 [L2337] TGETS    A=3 B=3 C=10 D=778 'd_xianlingShopUI'
00030 [L2337] TGETS    A=3 B=3 C=8 D=776 'updateStatus'
00031 [L2337] MOV      A=4 B=0 C=1 D=1 
00032 [L2337] CALL     A=3 B=1 C=2 D=258 
00033 [L2337] JMP      A=3 B=128 C=64 D=32832 target=98
00034 [L2338] TGETS    A=3 B=1 C=0 D=256 'tip_type'
00035 [L2338] GGET     A=4 B=0 C=1 D=1 't_t'
00036 [L2338] TGETS    A=4 B=4 C=11 D=1035 'update_weekend_team'
00037 [L2338] ISNEV    A=3 B=0 C=4 D=4 
00038 [L2338] JMP      A=3 B=128 C=6 D=32774 target=45
00039 [L2339] GGET     A=3 B=0 C=3 D=3 'd_ms'
00040 [L2339] TGETS    A=3 B=3 C=12 D=780 'd_miniGameUI'
00041 [L2339] TGETS    A=3 B=3 C=13 D=781 'updateTeam'
00042 [L2339] MOV      A=4 B=0 C=1 D=1 
00043 [L2339] CALL     A=3 B=1 C=2 D=258 
00044 [L2339] JMP      A=3 B=128 C=53 D=32821 target=98
00045 [L2340] TGETS    A=3 B=1 C=0 D=256 'tip_type'
00046 [L2340] GGET     A=4 B=0 C=1 D=1 't_t'
00047 [L2340] TGETS    A=4 B=4 C=14 D=1038 'update_game_data'
00048 [L2340] ISNEV    A=3 B=0 C=4 D=4 
00049 [L2340] JMP      A=3 B=128 C=6 D=32774 target=56
00050 [L2341] GGET     A=3 B=0 C=3 D=3 'd_ms'
00051 [L2341] TGETS    A=3 B=3 C=12 D=780 'd_miniGameUI'
00052 [L2341] TGETS    A=3 B=3 C=15 D=783 'onGetActEvents'
00053 [L2341] MOV      A=4 B=0 C=1 D=1 
00054 [L2341] CALL     A=3 B=1 C=2 D=258 
00055 [L2341] JMP      A=3 B=128 C=42 D=32810 target=98
00056 [L2342] TGETS    A=3 B=1 C=0 D=256 'tip_type'
00057 [L2342] GGET     A=4 B=0 C=1 D=1 't_t'
00058 [L2342] TGETS    A=4 B=4 C=16 D=1040 'send_weekend_talk'
00059 [L2342] ISNEV    A=3 B=0 C=4 D=4 
00060 [L2342] JMP      A=3 B=128 C=6 D=32774 target=67
00061 [L2343] GGET     A=3 B=0 C=3 D=3 'd_ms'
00062 [L2343] TGETS    A=3 B=3 C=17 D=785 'd_newChatUI'
00063 [L2343] TGETS    A=3 B=3 C=18 D=786 'updateTeamMessage'
00064 [L2343] MOV      A=4 B=0 C=1 D=1 
00065 [L2343] CALL     A=3 B=1 C=2 D=258 
00066 [L2343] JMP      A=3 B=128 C=31 D=32799 target=98
00067 [L2344] TGETS    A=3 B=1 C=0 D=256 'tip_type'
00068 [L2344] GGET     A=4 B=0 C=1 D=1 't_t'
00069 [L2344] TGETS    A=4 B=4 C=19 D=1043 'update_activity'
00070 [L2344] ISNEV    A=3 B=0 C=4 D=4 
00071 [L2344] JMP      A=3 B=128 C=5 D=32773 target=77
00072 [L2345] GGET     A=3 B=0 C=3 D=3 'd_ms'
00073 [L2345] TGETS    A=3 B=3 C=20 D=788 'd_actNoticeUI'
00074 [L2345] TGETS    A=3 B=3 C=21 D=789 'showIcon'
00075 [L2345] CALL     A=3 B=1 C=1 D=257 
00076 [L2345] JMP      A=3 B=128 C=21 D=32789 target=98
00077 [L2346] TGETS    A=3 B=1 C=0 D=256 'tip_type'
00078 [L2346] GGET     A=4 B=0 C=1 D=1 't_t'
00079 [L2346] TGETS    A=4 B=4 C=22 D=1046 'specter_tips'
00080 [L2346] ISNEV    A=3 B=0 C=4 D=4 
00081 [L2346] JMP      A=3 B=128 C=6 D=32774 target=88
00082 [L2347] GGET     A=3 B=0 C=3 D=3 'd_ms'
00083 [L2347] TGETS    A=3 B=3 C=23 D=791 'd_abyssUI'
00084 [L2347] TGETS    A=3 B=3 C=24 D=792 'updateRightMsg'
00085 [L2347] MOV      A=4 B=0 C=1 D=1 
00086 [L2347] CALL     A=3 B=1 C=2 D=258 
00087 [L2347] JMP      A=3 B=128 C=10 D=32778 target=98
00088 [L2348] TGETS    A=3 B=1 C=0 D=256 'tip_type'
00089 [L2348] GGET     A=4 B=0 C=1 D=1 't_t'
00090 [L2348] TGETS    A=4 B=4 C=25 D=1049 'monster_event'
00091 [L2348] ISNEV    A=3 B=0 C=4 D=4 
00092 [L2348] JMP      A=3 B=128 C=5 D=32773 target=98
00093 [L2349] GGET     A=3 B=0 C=3 D=3 'd_ms'
00094 [L2349] TGETS    A=3 B=3 C=26 D=794 'd_omenUI'
00095 [L2349] TGETS    A=3 B=3 C=27 D=795 'onGetSync'
00096 [L2349] MOV      A=4 B=0 C=1 D=1 
00097 [L2349] CALL     A=3 B=1 C=2 D=258 
00098 [L2351] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto63 offset=0x10b7a source_lines=2353-2423 params=3
UPVALUES ['cclog', 'table']
00001 [L2354] ISEQP    A=1 B=0 C=0 D=0 
00002 [L2354] JMP      A=3 B=129 C=60 D=33084 target=319
00003 [L2354] TGETS    A=3 B=1 C=0 D=256 'id'
00004 [L2354] ISEQN    A=3 B=0 C=0 D=0 0
00005 [L2354] JMP      A=3 B=129 C=57 D=33081 target=319
00006 [L2355] UGET     A=3 B=0 C=0 D=0 cclog
00007 [L2355] KSTR     A=4 B=0 C=1 D=1 'call msg_union_event_1301, ----[%d]'
00008 [L2355] TGETS    A=5 B=1 C=0 D=256 'id'
00009 [L2355] CALL     A=3 B=1 C=3 D=259 
00010 [L2356] GGET     A=3 B=0 C=2 D=2 'd_ms'
00011 [L2356] TGETS    A=3 B=3 C=3 D=771 'd_alert'
00012 [L2356] TGETS    A=3 B=3 C=4 D=772 'stop_wait'
00013 [L2356] CALL     A=3 B=1 C=1 D=257 
00014 [L2357] UGET     A=3 B=0 C=1 D=1 table
00015 [L2357] TGETS    A=3 B=3 C=5 D=773 'loadstring'
00016 [L2357] TGETS    A=4 B=1 C=6 D=262 'data'
00017 [L2357] CALL     A=3 B=2 C=2 D=514 
00018 [L2358] TGETS    A=4 B=1 C=0 D=256 'id'
00019 [L2358] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00020 [L2358] TGETS    A=5 B=5 C=8 D=1288 'query_plant_info'
00021 [L2358] ISNEV    A=4 B=0 C=5 D=5 
00022 [L2358] JMP      A=4 B=128 C=6 D=32774 target=29
00023 [L2359] GGET     A=4 B=0 C=2 D=2 'd_ms'
00024 [L2359] TGETS    A=4 B=4 C=9 D=1033 'd_worldTreeUI'
00025 [L2359] TGETS    A=4 B=4 C=10 D=1034 'onGetTreeStatus'
00026 [L2359] MOV      A=5 B=0 C=3 D=3 
00027 [L2359] CALL     A=4 B=1 C=2 D=258 
00028 [L2359] JMP      A=4 B=129 C=34 D=33058 target=319
00029 [L2360] TGETS    A=4 B=1 C=0 D=256 'id'
00030 [L2360] ISNEN    A=4 B=0 C=1 D=1 37
00031 [L2360] JMP      A=4 B=128 C=6 D=32774 target=38
00032 [L2361] GGET     A=4 B=0 C=2 D=2 'd_ms'
00033 [L2361] TGETS    A=4 B=4 C=9 D=1033 'd_worldTreeUI'
00034 [L2361] TGETS    A=4 B=4 C=11 D=1035 'onGetBuySeedResult'
00035 [L2361] MOV      A=5 B=0 C=3 D=3 
00036 [L2361] CALL     A=4 B=1 C=2 D=258 
00037 [L2361] JMP      A=4 B=129 C=25 D=33049 target=319
00038 [L2362] TGETS    A=4 B=1 C=0 D=256 'id'
00039 [L2362] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00040 [L2362] TGETS    A=5 B=5 C=12 D=1292 'tree_plant'
00041 [L2362] ISNEV    A=4 B=0 C=5 D=5 
00042 [L2362] JMP      A=4 B=128 C=6 D=32774 target=49
00043 [L2363] GGET     A=4 B=0 C=2 D=2 'd_ms'
00044 [L2363] TGETS    A=4 B=4 C=9 D=1033 'd_worldTreeUI'
00045 [L2363] TGETS    A=4 B=4 C=13 D=1037 'onGetPlantTreeResult'
00046 [L2363] MOV      A=5 B=0 C=3 D=3 
00047 [L2363] CALL     A=4 B=1 C=2 D=258 
00048 [L2363] JMP      A=4 B=129 C=14 D=33038 target=319
00049 [L2364] TGETS    A=4 B=1 C=0 D=256 'id'
00050 [L2364] ISNEN    A=4 B=0 C=2 D=2 32
00051 [L2364] JMP      A=4 B=128 C=6 D=32774 target=58
00052 [L2365] GGET     A=4 B=0 C=2 D=2 'd_ms'
00053 [L2365] TGETS    A=4 B=4 C=14 D=1038 'd_secretAreaUI'
00054 [L2365] TGETS    A=4 B=4 C=15 D=1039 'callback_pressDismissTeam'
00055 [L2365] MOV      A=5 B=0 C=3 D=3 
00056 [L2365] CALL     A=4 B=1 C=2 D=258 
00057 [L2365] JMP      A=4 B=129 C=5 D=33029 target=319
00058 [L2366] TGETS    A=4 B=1 C=0 D=256 'id'
00059 [L2366] ISNEN    A=4 B=0 C=3 D=3 35
00060 [L2366] JMP      A=4 B=128 C=6 D=32774 target=67
00061 [L2367] GGET     A=4 B=0 C=2 D=2 'd_ms'
00062 [L2367] TGETS    A=4 B=4 C=9 D=1033 'd_worldTreeUI'
00063 [L2367] TGETS    A=4 B=4 C=16 D=1040 'onGetFeedMission'
00064 [L2367] MOV      A=5 B=0 C=3 D=3 
00065 [L2367] CALL     A=4 B=1 C=2 D=258 
00066 [L2367] JMP      A=4 B=128 C=252 D=33020 target=319
00067 [L2368] TGETS    A=4 B=1 C=0 D=256 'id'
00068 [L2368] ISNEN    A=4 B=0 C=4 D=4 44
00069 [L2368] JMP      A=4 B=128 C=6 D=32774 target=76
00070 [L2369] GGET     A=4 B=0 C=2 D=2 'd_ms'
00071 [L2369] TGETS    A=4 B=4 C=14 D=1038 'd_secretAreaUI'
00072 [L2369] TGETS    A=4 B=4 C=17 D=1041 'callback_getSecretAreaStatus'
00073 [L2369] MOV      A=5 B=0 C=3 D=3 
00074 [L2369] CALL     A=4 B=1 C=2 D=258 
00075 [L2369] JMP      A=4 B=128 C=243 D=33011 target=319
00076 [L2370] TGETS    A=4 B=1 C=0 D=256 'id'
00077 [L2370] ISNEN    A=4 B=0 C=5 D=5 28
00078 [L2370] JMP      A=4 B=128 C=6 D=32774 target=85
00079 [L2371] GGET     A=4 B=0 C=2 D=2 'd_ms'
00080 [L2371] TGETS    A=4 B=4 C=14 D=1038 'd_secretAreaUI'
00081 [L2371] TGETS    A=4 B=4 C=18 D=1042 'callback_accept_team_apply'
00082 [L2371] MOV      A=5 B=0 C=3 D=3 
00083 [L2371] CALL     A=4 B=1 C=2 D=258 
00084 [L2371] JMP      A=4 B=128 C=234 D=33002 target=319
00085 [L2372] TGETS    A=4 B=1 C=0 D=256 'id'
00086 [L2372] ISNEN    A=4 B=0 C=6 D=6 41
00087 [L2372] JMP      A=4 B=128 C=6 D=32774 target=94
00088 [L2373] GGET     A=4 B=0 C=2 D=2 'd_ms'
00089 [L2373] TGETS    A=4 B=4 C=14 D=1038 'd_secretAreaUI'
00090 [L2373] TGETS    A=4 B=4 C=19 D=1043 'callback_fam_train_boss'
00091 [L2373] MOV      A=5 B=0 C=3 D=3 
00092 [L2373] CALL     A=4 B=1 C=2 D=258 
00093 [L2373] JMP      A=4 B=128 C=225 D=32993 target=319
00094 [L2374] TGETS    A=4 B=1 C=0 D=256 'id'
00095 [L2374] ISNEN    A=4 B=0 C=7 D=7 42
00096 [L2374] JMP      A=4 B=128 C=6 D=32774 target=103
00097 [L2375] GGET     A=4 B=0 C=2 D=2 'd_ms'
00098 [L2375] TGETS    A=4 B=4 C=14 D=1038 'd_secretAreaUI'
00099 [L2375] TGETS    A=4 B=4 C=20 D=1044 'callback_query_fam_fight'
00100 [L2375] MOV      A=5 B=0 C=3 D=3 
00101 [L2375] CALL     A=4 B=1 C=2 D=258 
00102 [L2375] JMP      A=4 B=128 C=216 D=32984 target=319
00103 [L2376] TGETS    A=4 B=1 C=0 D=256 'id'
00104 [L2376] ISNEN    A=4 B=0 C=8 D=8 43
00105 [L2376] JMP      A=4 B=128 C=6 D=32774 target=112
00106 [L2377] GGET     A=4 B=0 C=2 D=2 'd_ms'
00107 [L2377] TGETS    A=4 B=4 C=14 D=1038 'd_secretAreaUI'
00108 [L2377] TGETS    A=4 B=4 C=21 D=1045 'callback_fam_search_gold'
00109 [L2377] MOV      A=5 B=0 C=3 D=3 
00110 [L2377] CALL     A=4 B=1 C=2 D=258 
00111 [L2377] JMP      A=4 B=128 C=207 D=32975 target=319
00112 [L2378] TGETS    A=4 B=1 C=0 D=256 'id'
00113 [L2378] ISNEN    A=4 B=0 C=9 D=9 50
00114 [L2378] JMP      A=4 B=128 C=6 D=32774 target=121
00115 [L2379] GGET     A=4 B=0 C=2 D=2 'd_ms'
00116 [L2379] TGETS    A=4 B=4 C=14 D=1038 'd_secretAreaUI'
00117 [L2379] TGETS    A=4 B=4 C=22 D=1046 'callback_get_apply_list'
00118 [L2379] MOV      A=5 B=0 C=3 D=3 
00119 [L2379] CALL     A=4 B=1 C=2 D=258 
00120 [L2379] JMP      A=4 B=128 C=198 D=32966 target=319
00121 [L2380] TGETS    A=4 B=1 C=0 D=256 'id'
00122 [L2380] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00123 [L2380] TGETS    A=5 B=5 C=23 D=1303 'back_to_ownteam'
00124 [L2380] ISNEV    A=4 B=0 C=5 D=5 
00125 [L2380] JMP      A=4 B=128 C=6 D=32774 target=132
00126 [L2381] GGET     A=4 B=0 C=2 D=2 'd_ms'
00127 [L2381] TGETS    A=4 B=4 C=14 D=1038 'd_secretAreaUI'
00128 [L2381] TGETS    A=4 B=4 C=17 D=1041 'callback_getSecretAreaStatus'
00129 [L2381] MOV      A=5 B=0 C=3 D=3 
00130 [L2381] CALL     A=4 B=1 C=2 D=258 
00131 [L2381] JMP      A=4 B=128 C=187 D=32955 target=319
00132 [L2382] TGETS    A=4 B=1 C=0 D=256 'id'
00133 [L2382] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00134 [L2382] TGETS    A=5 B=5 C=24 D=1304 'query_fam_teamlist'
00135 [L2382] ISNEV    A=4 B=0 C=5 D=5 
00136 [L2382] JMP      A=4 B=128 C=6 D=32774 target=143
00137 [L2383] GGET     A=4 B=0 C=2 D=2 'd_ms'
00138 [L2383] TGETS    A=4 B=4 C=14 D=1038 'd_secretAreaUI'
00139 [L2383] TGETS    A=4 B=4 C=25 D=1049 'onGetTeamsList'
00140 [L2383] MOV      A=5 B=0 C=3 D=3 
00141 [L2383] CALL     A=4 B=1 C=2 D=258 
00142 [L2383] JMP      A=4 B=128 C=176 D=32944 target=319
00143 [L2384] TGETS    A=4 B=1 C=0 D=256 'id'
00144 [L2384] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00145 [L2384] TGETS    A=5 B=5 C=26 D=1306 'query_fam_teaminfo'
00146 [L2384] ISNEV    A=4 B=0 C=5 D=5 
00147 [L2384] JMP      A=4 B=128 C=6 D=32774 target=154
00148 [L2385] GGET     A=4 B=0 C=2 D=2 'd_ms'
00149 [L2385] TGETS    A=4 B=4 C=14 D=1038 'd_secretAreaUI'
00150 [L2385] TGETS    A=4 B=4 C=27 D=1051 'onGetTeamDetail'
00151 [L2385] MOV      A=5 B=0 C=3 D=3 
00152 [L2385] CALL     A=4 B=1 C=2 D=258 
00153 [L2385] JMP      A=4 B=128 C=165 D=32933 target=319
00154 [L2386] TGETS    A=4 B=1 C=0 D=256 'id'
00155 [L2386] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00156 [L2386] TGETS    A=5 B=5 C=26 D=1306 'query_fam_teaminfo'
00157 [L2386] ISNEV    A=4 B=0 C=5 D=5 
00158 [L2386] JMP      A=4 B=128 C=1 D=32769 target=160
00159 [L2386] JMP      A=4 B=128 C=159 D=32927 target=319
00160 [L2390] TGETS    A=4 B=1 C=0 D=256 'id'
00161 [L2390] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00162 [L2390] TGETS    A=5 B=5 C=28 D=1308 'query_union_train_info'
00163 [L2390] ISEQV    A=4 B=0 C=5 D=5 
00164 [L2390] JMP      A=4 B=128 C=45 D=32813 target=210
00165 [L2391] TGETS    A=4 B=1 C=0 D=256 'id'
00166 [L2391] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00167 [L2391] TGETS    A=5 B=5 C=29 D=1309 'open_union_train_boss'
00168 [L2391] ISEQV    A=4 B=0 C=5 D=5 
00169 [L2391] JMP      A=4 B=128 C=40 D=32808 target=210
00170 [L2392] TGETS    A=4 B=1 C=0 D=256 'id'
00171 [L2392] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00172 [L2392] TGETS    A=5 B=5 C=30 D=1310 'union_train_boss_fight'
00173 [L2392] ISEQV    A=4 B=0 C=5 D=5 
00174 [L2392] JMP      A=4 B=128 C=35 D=32803 target=210
00175 [L2393] TGETS    A=4 B=1 C=0 D=256 'id'
00176 [L2393] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00177 [L2393] TGETS    A=5 B=5 C=31 D=1311 'inside_union_pet'
00178 [L2393] ISEQV    A=4 B=0 C=5 D=5 
00179 [L2393] JMP      A=4 B=128 C=30 D=32798 target=210
00180 [L2394] TGETS    A=4 B=1 C=0 D=256 'id'
00181 [L2394] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00182 [L2394] TGETS    A=5 B=5 C=32 D=1312 'union_lucky_catch'
00183 [L2394] ISEQV    A=4 B=0 C=5 D=5 
00184 [L2394] JMP      A=4 B=128 C=25 D=32793 target=210
00185 [L2395] TGETS    A=4 B=1 C=0 D=256 'id'
00186 [L2395] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00187 [L2395] TGETS    A=5 B=5 C=33 D=1313 'update_union_catch'
00188 [L2395] ISEQV    A=4 B=0 C=5 D=5 
00189 [L2395] JMP      A=4 B=128 C=20 D=32788 target=210
00190 [L2396] TGETS    A=4 B=1 C=0 D=256 'id'
00191 [L2396] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00192 [L2396] TGETS    A=5 B=5 C=34 D=1314 'change_appoint_role'
00193 [L2396] ISEQV    A=4 B=0 C=5 D=5 
00194 [L2396] JMP      A=4 B=128 C=15 D=32783 target=210
00195 [L2397] TGETS    A=4 B=1 C=0 D=256 'id'
00196 [L2397] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00197 [L2397] TGETS    A=5 B=5 C=35 D=1315 'support_train_boss_fight'
00198 [L2397] ISEQV    A=4 B=0 C=5 D=5 
00199 [L2397] JMP      A=4 B=128 C=10 D=32778 target=210
00200 [L2398] TGETS    A=4 B=1 C=0 D=256 'id'
00201 [L2398] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00202 [L2398] TGETS    A=5 B=5 C=36 D=1316 'get_union_train_prize'
00203 [L2398] ISEQV    A=4 B=0 C=5 D=5 
00204 [L2398] JMP      A=4 B=128 C=5 D=32773 target=210
00205 [L2399] TGETS    A=4 B=1 C=0 D=256 'id'
00206 [L2399] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00207 [L2399] TGETS    A=5 B=5 C=37 D=1317 'query_train_fight_record'
00208 [L2399] ISNEV    A=4 B=0 C=5 D=5 
00209 [L2399] JMP      A=4 B=128 C=7 D=32775 target=217
00210 [L2401] GGET     A=4 B=0 C=2 D=2 'd_ms'
00211 [L2401] TGETS    A=4 B=4 C=38 D=1062 'd_petHomeUI'
00212 [L2401] TGETS    A=4 B=4 C=39 D=1063 'MsgHandle'
00213 [L2401] MOV      A=5 B=0 C=1 D=1 
00214 [L2401] MOV      A=6 B=0 C=3 D=3 
00215 [L2401] CALL     A=4 B=1 C=3 D=259 
00216 [L2401] JMP      A=4 B=128 C=102 D=32870 target=319
00217 [L2403] TGETS    A=4 B=1 C=0 D=256 'id'
00218 [L2403] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00219 [L2403] TGETS    A=5 B=5 C=40 D=1320 'union_task_info'
00220 [L2403] ISNEV    A=4 B=0 C=5 D=5 
00221 [L2403] JMP      A=4 B=128 C=7 D=32775 target=229
00222 [L2404] GGET     A=4 B=0 C=2 D=2 'd_ms'
00223 [L2404] TGETS    A=4 B=4 C=41 D=1065 'd_pethuntUI'
00224 [L2404] TGETS    A=4 B=4 C=42 D=1066 'onGetResult'
00225 [L2404] TGETS    A=5 B=1 C=0 D=256 'id'
00226 [L2404] MOV      A=6 B=0 C=3 D=3 
00227 [L2404] CALL     A=4 B=1 C=3 D=259 
00228 [L2404] JMP      A=4 B=128 C=90 D=32858 target=319
00229 [L2405] TGETS    A=4 B=1 C=0 D=256 'id'
00230 [L2405] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00231 [L2405] TGETS    A=5 B=5 C=43 D=1323 'union_wander_operate'
00232 [L2405] ISNEV    A=4 B=0 C=5 D=5 
00233 [L2405] JMP      A=4 B=128 C=7 D=32775 target=241
00234 [L2406] GGET     A=4 B=0 C=2 D=2 'd_ms'
00235 [L2406] TGETS    A=4 B=4 C=41 D=1065 'd_pethuntUI'
00236 [L2406] TGETS    A=4 B=4 C=42 D=1066 'onGetResult'
00237 [L2406] TGETS    A=5 B=1 C=0 D=256 'id'
00238 [L2406] MOV      A=6 B=0 C=3 D=3 
00239 [L2406] CALL     A=4 B=1 C=3 D=259 
00240 [L2406] JMP      A=4 B=128 C=78 D=32846 target=319
00241 [L2407] TGETS    A=4 B=1 C=0 D=256 'id'
00242 [L2407] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00243 [L2407] TGETS    A=5 B=5 C=44 D=1324 'union_catch_operate'
00244 [L2407] ISNEV    A=4 B=0 C=5 D=5 
00245 [L2407] JMP      A=4 B=128 C=7 D=32775 target=253
00246 [L2408] GGET     A=4 B=0 C=2 D=2 'd_ms'
00247 [L2408] TGETS    A=4 B=4 C=41 D=1065 'd_pethuntUI'
00248 [L2408] TGETS    A=4 B=4 C=42 D=1066 'onGetResult'
00249 [L2408] TGETS    A=5 B=1 C=0 D=256 'id'
00250 [L2408] MOV      A=6 B=0 C=3 D=3 
00251 [L2408] CALL     A=4 B=1 C=3 D=259 
00252 [L2408] JMP      A=4 B=128 C=66 D=32834 target=319
00253 [L2409] TGETS    A=4 B=1 C=0 D=256 'id'
00254 [L2409] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00255 [L2409] TGETS    A=5 B=5 C=45 D=1325 'union_pet_shop'
00256 [L2409] ISNEV    A=4 B=0 C=5 D=5 
00257 [L2409] JMP      A=4 B=128 C=7 D=32775 target=265
00258 [L2410] GGET     A=4 B=0 C=2 D=2 'd_ms'
00259 [L2410] TGETS    A=4 B=4 C=41 D=1065 'd_pethuntUI'
00260 [L2410] TGETS    A=4 B=4 C=42 D=1066 'onGetResult'
00261 [L2410] TGETS    A=5 B=1 C=0 D=256 'id'
00262 [L2410] MOV      A=6 B=0 C=3 D=3 
00263 [L2410] CALL     A=4 B=1 C=3 D=259 
00264 [L2410] JMP      A=4 B=128 C=54 D=32822 target=319
00265 [L2411] TGETS    A=4 B=1 C=0 D=256 'id'
00266 [L2411] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00267 [L2411] TGETS    A=5 B=5 C=46 D=1326 'union_task_operate'
00268 [L2411] ISNEV    A=4 B=0 C=5 D=5 
00269 [L2411] JMP      A=4 B=128 C=7 D=32775 target=277
00270 [L2412] GGET     A=4 B=0 C=2 D=2 'd_ms'
00271 [L2412] TGETS    A=4 B=4 C=41 D=1065 'd_pethuntUI'
00272 [L2412] TGETS    A=4 B=4 C=42 D=1066 'onGetResult'
00273 [L2412] TGETS    A=5 B=1 C=0 D=256 'id'
00274 [L2412] MOV      A=6 B=0 C=3 D=3 
00275 [L2412] CALL     A=4 B=1 C=3 D=259 
00276 [L2412] JMP      A=4 B=128 C=42 D=32810 target=319
00277 [L2413] TGETS    A=4 B=1 C=0 D=256 'id'
00278 [L2413] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00279 [L2413] TGETS    A=5 B=5 C=47 D=1327 'union_pet_rank'
00280 [L2413] ISNEV    A=4 B=0 C=5 D=5 
00281 [L2413] JMP      A=4 B=128 C=7 D=32775 target=289
00282 [L2414] GGET     A=4 B=0 C=2 D=2 'd_ms'
00283 [L2414] TGETS    A=4 B=4 C=41 D=1065 'd_pethuntUI'
00284 [L2414] TGETS    A=4 B=4 C=42 D=1066 'onGetResult'
00285 [L2414] TGETS    A=5 B=1 C=0 D=256 'id'
00286 [L2414] MOV      A=6 B=0 C=3 D=3 
00287 [L2414] CALL     A=4 B=1 C=3 D=259 
00288 [L2414] JMP      A=4 B=128 C=30 D=32798 target=319
00289 [L2415] TGETS    A=4 B=1 C=0 D=256 'id'
00290 [L2415] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00291 [L2415] TGETS    A=5 B=5 C=48 D=1328 'union_task_boss_fight'
00292 [L2415] ISNEV    A=4 B=0 C=5 D=5 
00293 [L2415] JMP      A=4 B=128 C=7 D=32775 target=301
00294 [L2416] GGET     A=4 B=0 C=2 D=2 'd_ms'
00295 [L2416] TGETS    A=4 B=4 C=41 D=1065 'd_pethuntUI'
00296 [L2416] TGETS    A=4 B=4 C=42 D=1066 'onGetResult'
00297 [L2416] TGETS    A=5 B=1 C=0 D=256 'id'
00298 [L2416] MOV      A=6 B=0 C=3 D=3 
00299 [L2416] CALL     A=4 B=1 C=3 D=259 
00300 [L2416] JMP      A=4 B=128 C=18 D=32786 target=319
00301 [L2417] TGETS    A=4 B=1 C=0 D=256 'id'
00302 [L2417] GGET     A=5 B=0 C=7 D=7 'u_e_t'
00303 [L2417] TGETS    A=5 B=5 C=49 D=1329 'update_union_wander'
00304 [L2417] ISNEV    A=4 B=0 C=5 D=5 
00305 [L2417] JMP      A=4 B=128 C=7 D=32775 target=313
00306 [L2418] GGET     A=4 B=0 C=2 D=2 'd_ms'
00307 [L2418] TGETS    A=4 B=4 C=41 D=1065 'd_pethuntUI'
00308 [L2418] TGETS    A=4 B=4 C=42 D=1066 'onGetResult'
00309 [L2418] TGETS    A=5 B=1 C=0 D=256 'id'
00310 [L2418] MOV      A=6 B=0 C=3 D=3 
00311 [L2418] CALL     A=4 B=1 C=3 D=259 
00312 [L2418] JMP      A=4 B=128 C=6 D=32774 target=319
00313 [L2420] GGET     A=4 B=0 C=2 D=2 'd_ms'
00314 [L2420] TGETS    A=4 B=4 C=50 D=1074 'd_xianmengUI'
00315 [L2420] TGETS    A=4 B=4 C=51 D=1075 'getServerResponse'
00316 [L2420] TGETS    A=5 B=1 C=0 D=256 'id'
00317 [L2420] MOV      A=6 B=0 C=3 D=3 
00318 [L2420] CALL     A=4 B=1 C=3 D=259 
00319 [L2423] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto64 offset=0x115a1 source_lines=2425-2428 params=3
UPVALUES []
00001 [L2426] GGET     A=3 B=0 C=0 D=0 'd_ms'
00002 [L2426] TGETS    A=3 B=3 C=1 D=769 'd_alert'
00003 [L2426] TGETS    A=3 B=3 C=2 D=770 'stop_wait'
00004 [L2426] CALL     A=3 B=1 C=1 D=257 
00005 [L2427] GGET     A=3 B=0 C=0 D=0 'd_ms'
00006 [L2427] TGETS    A=3 B=3 C=3 D=771 'd_crossRankUI'
00007 [L2427] TGETS    A=3 B=3 C=4 D=772 'getRankInfoFromServer'
00008 [L2427] MOV      A=4 B=0 C=1 D=1 
00009 [L2427] CALL     A=3 B=1 C=2 D=258 
00010 [L2428] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto65 offset=0x11637 source_lines=2431-2488 params=0
UPVALUES []
00001 [L2433] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00002 [L2433] GGET     A=1 B=0 C=1 D=1 'd_ms'
00003 [L2433] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00004 [L2433] TGETS    A=1 B=1 C=3 D=259 'common_id'
00005 [L2433] TGETS    A=1 B=1 C=4 D=260 'event_client_info'
00006 [L2433] GGET     A=2 B=0 C=5 D=5 'event_client_info_20'
00007 [L2433] CALL     A=0 B=1 C=3 D=259 
00008 [L2434] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00009 [L2434] GGET     A=1 B=0 C=1 D=1 'd_ms'
00010 [L2434] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00011 [L2434] TGETS    A=1 B=1 C=3 D=259 'common_id'
00012 [L2434] TGETS    A=1 B=1 C=6 D=262 'event_client_update_info'
00013 [L2434] GGET     A=2 B=0 C=7 D=7 'event_client_update_info_21'
00014 [L2434] CALL     A=0 B=1 C=3 D=259 
00015 [L2435] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00016 [L2435] GGET     A=1 B=0 C=1 D=1 'd_ms'
00017 [L2435] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00018 [L2435] TGETS    A=1 B=1 C=3 D=259 'common_id'
00019 [L2435] TGETS    A=1 B=1 C=8 D=264 'event_third_party_platform'
00020 [L2435] GGET     A=2 B=0 C=9 D=9 'event_msg_third_party_platform_22'
00021 [L2435] CALL     A=0 B=1 C=3 D=259 
00022 [L2437] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00023 [L2437] GGET     A=1 B=0 C=1 D=1 'd_ms'
00024 [L2437] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00025 [L2437] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00026 [L2437] TGETS    A=1 B=1 C=11 D=267 'msg_inside_game'
00027 [L2437] GGET     A=2 B=0 C=12 D=12 'inside_game_1017'
00028 [L2437] CALL     A=0 B=1 C=3 D=259 
00029 [L2438] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00030 [L2438] GGET     A=1 B=0 C=1 D=1 'd_ms'
00031 [L2438] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00032 [L2438] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00033 [L2438] TGETS    A=1 B=1 C=13 D=269 'msg_fight_result'
00034 [L2438] GGET     A=2 B=0 C=14 D=14 'fight_result_1027'
00035 [L2438] CALL     A=0 B=1 C=3 D=259 
00036 [L2439] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00037 [L2439] GGET     A=1 B=0 C=1 D=1 'd_ms'
00038 [L2439] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00039 [L2439] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00040 [L2439] TGETS    A=1 B=1 C=15 D=271 'msg_fight_lineup'
00041 [L2439] GGET     A=2 B=0 C=16 D=16 'fight_lineup_1028'
00042 [L2439] CALL     A=0 B=1 C=3 D=259 
00043 [L2440] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00044 [L2440] GGET     A=1 B=0 C=1 D=1 'd_ms'
00045 [L2440] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00046 [L2440] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00047 [L2440] TGETS    A=1 B=1 C=17 D=273 'msg_special_fight_result'
00048 [L2440] GGET     A=2 B=0 C=18 D=18 'special_fight_result_1140'
00049 [L2440] CALL     A=0 B=1 C=3 D=259 
00050 [L2441] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00051 [L2441] GGET     A=1 B=0 C=1 D=1 'd_ms'
00052 [L2441] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00053 [L2441] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00054 [L2441] TGETS    A=1 B=1 C=19 D=275 'msg_special_fight_lineup'
00055 [L2441] GGET     A=2 B=0 C=20 D=20 'special_fight_lineup_1141'
00056 [L2441] CALL     A=0 B=1 C=3 D=259 
00057 [L2443] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00058 [L2443] GGET     A=1 B=0 C=1 D=1 'd_ms'
00059 [L2443] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00060 [L2443] TGETS    A=1 B=1 C=21 D=277 'lscl_msg_id'
00061 [L2443] TGETS    A=1 B=1 C=22 D=278 'msg_login_rsp'
00062 [L2443] GGET     A=2 B=0 C=23 D=23 'msg_login_rsp_3002'
00063 [L2443] CALL     A=0 B=1 C=3 D=259 
00064 [L2446] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00065 [L2446] GGET     A=1 B=0 C=1 D=1 'd_ms'
00066 [L2446] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00067 [L2446] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00068 [L2446] TGETS    A=1 B=1 C=24 D=280 'msg_force_quit'
00069 [L2446] GGET     A=2 B=0 C=25 D=25 'msg_force_quit_1011'
00070 [L2446] CALL     A=0 B=1 C=3 D=259 
00071 [L2448] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00072 [L2448] GGET     A=1 B=0 C=1 D=1 'd_ms'
00073 [L2448] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00074 [L2448] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00075 [L2448] TGETS    A=1 B=1 C=26 D=282 'msg_update_cortege_list'
00076 [L2448] GGET     A=2 B=0 C=27 D=27 'msg_update_cortege_list_1034'
00077 [L2448] CALL     A=0 B=1 C=3 D=259 
00078 [L2449] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00079 [L2449] GGET     A=1 B=0 C=1 D=1 'd_ms'
00080 [L2449] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00081 [L2449] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00082 [L2449] TGETS    A=1 B=1 C=28 D=284 'msg_update_attach_list'
00083 [L2449] GGET     A=2 B=0 C=29 D=29 'msg_update_attach_list_1035'
00084 [L2449] CALL     A=0 B=1 C=3 D=259 
00085 [L2451] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00086 [L2451] GGET     A=1 B=0 C=1 D=1 'd_ms'
00087 [L2451] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00088 [L2451] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00089 [L2451] TGETS    A=1 B=1 C=30 D=286 'msg_update_spirit_list'
00090 [L2451] GGET     A=2 B=0 C=31 D=31 'msg_update_spirit_list_1046'
00091 [L2451] CALL     A=0 B=1 C=3 D=259 
00092 [L2453] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00093 [L2453] GGET     A=1 B=0 C=1 D=1 'd_ms'
00094 [L2453] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00095 [L2453] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00096 [L2453] TGETS    A=1 B=1 C=32 D=288 'msg_common_event'
00097 [L2453] GGET     A=2 B=0 C=33 D=33 'msg_common_event_2998'
00098 [L2453] CALL     A=0 B=1 C=3 D=259 
00099 [L2455] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00100 [L2455] GGET     A=1 B=0 C=1 D=1 'd_ms'
00101 [L2455] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00102 [L2455] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00103 [L2455] TGETS    A=1 B=1 C=34 D=290 'msg_update_tollgate_data'
00104 [L2455] GGET     A=2 B=0 C=35 D=35 'msg_update_tollgate_data_1019'
00105 [L2455] CALL     A=0 B=1 C=3 D=259 
00106 [L2456] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00107 [L2456] GGET     A=1 B=0 C=1 D=1 'd_ms'
00108 [L2456] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00109 [L2456] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00110 [L2456] TGETS    A=1 B=1 C=36 D=292 'msg_update_tollgate_list'
00111 [L2456] GGET     A=2 B=0 C=37 D=37 'msg_update_tollgate_list_1020'
00112 [L2456] CALL     A=0 B=1 C=3 D=259 
00113 [L2457] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00114 [L2457] GGET     A=1 B=0 C=1 D=1 'd_ms'
00115 [L2457] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00116 [L2457] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00117 [L2457] TGETS    A=1 B=1 C=38 D=294 'msg_update_top_list'
00118 [L2457] GGET     A=2 B=0 C=39 D=39 'msg_update_top_list_1022'
00119 [L2457] CALL     A=0 B=1 C=3 D=259 
00120 [L2458] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00121 [L2458] GGET     A=1 B=0 C=1 D=1 'd_ms'
00122 [L2458] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00123 [L2458] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00124 [L2458] TGETS    A=1 B=1 C=40 D=296 'msg_modify_attr'
00125 [L2458] GGET     A=2 B=0 C=41 D=41 'msg_modify_attr_1032'
00126 [L2458] CALL     A=0 B=1 C=3 D=259 
00127 [L2459] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00128 [L2459] GGET     A=1 B=0 C=1 D=1 'd_ms'
00129 [L2459] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00130 [L2459] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00131 [L2459] TGETS    A=1 B=1 C=42 D=298 'msg_chat_info_to_client'
00132 [L2459] GGET     A=2 B=0 C=43 D=43 'msg_chat_info_to_client_1098'
00133 [L2459] CALL     A=0 B=1 C=3 D=259 
00134 [L2460] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00135 [L2460] GGET     A=1 B=0 C=1 D=1 'd_ms'
00136 [L2460] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00137 [L2460] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00138 [L2460] TGETS    A=1 B=1 C=44 D=300 'msg_search_player_result'
00139 [L2460] GGET     A=2 B=0 C=45 D=45 'msg_search_player_result_1092'
00140 [L2460] CALL     A=0 B=1 C=3 D=259 
00141 [L2461] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00142 [L2461] GGET     A=1 B=0 C=1 D=1 'd_ms'
00143 [L2461] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00144 [L2461] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00145 [L2461] TGETS    A=1 B=1 C=46 D=302 'msg_update_attention_list'
00146 [L2461] GGET     A=2 B=0 C=47 D=47 'msg_update_attention_list_1095'
00147 [L2461] CALL     A=0 B=1 C=3 D=259 
00148 [L2462] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00149 [L2462] GGET     A=1 B=0 C=1 D=1 'd_ms'
00150 [L2462] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00151 [L2462] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00152 [L2462] TGETS    A=1 B=1 C=48 D=304 'msg_remove_object'
00153 [L2462] GGET     A=2 B=0 C=49 D=49 'msg_remove_object_1038'
00154 [L2462] CALL     A=0 B=1 C=3 D=259 
00155 [L2464] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00156 [L2464] GGET     A=1 B=0 C=1 D=1 'd_ms'
00157 [L2464] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00158 [L2464] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00159 [L2464] TGETS    A=1 B=1 C=50 D=306 'msg_kick_player'
00160 [L2464] GGET     A=2 B=0 C=51 D=51 'msg_kick_player_2997'
00161 [L2464] CALL     A=0 B=1 C=3 D=259 
00162 [L2466] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00163 [L2466] GGET     A=1 B=0 C=1 D=1 'd_ms'
00164 [L2466] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00165 [L2466] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00166 [L2466] TGETS    A=1 B=1 C=22 D=278 'msg_login_rsp'
00167 [L2466] GGET     A=2 B=0 C=52 D=52 'msg_login_rsp_1002'
00168 [L2466] CALL     A=0 B=1 C=3 D=259 
00169 [L2467] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00170 [L2467] GGET     A=1 B=0 C=1 D=1 'd_ms'
00171 [L2467] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00172 [L2467] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00173 [L2467] TGETS    A=1 B=1 C=53 D=309 'msg_keep_alive'
00174 [L2467] GGET     A=2 B=0 C=54 D=54 'msg_keep_alive_2999'
00175 [L2467] CALL     A=0 B=1 C=3 D=259 
00176 [L2469] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00177 [L2469] GGET     A=1 B=0 C=1 D=1 'd_ms'
00178 [L2469] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00179 [L2469] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00180 [L2469] TGETS    A=1 B=1 C=55 D=311 'msg_update_lottery_list'
00181 [L2469] GGET     A=2 B=0 C=56 D=56 'msg_update_lottery_list_1047'
00182 [L2469] CALL     A=0 B=1 C=3 D=259 
00183 [L2471] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00184 [L2471] GGET     A=1 B=0 C=1 D=1 'd_ms'
00185 [L2471] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00186 [L2471] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00187 [L2471] TGETS    A=1 B=1 C=57 D=313 'msg_update_label_list'
00188 [L2471] GGET     A=2 B=0 C=58 D=58 'msg_update_label_list_1044'
00189 [L2471] CALL     A=0 B=1 C=3 D=259 
00190 [L2472] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00191 [L2472] GGET     A=1 B=0 C=1 D=1 'd_ms'
00192 [L2472] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00193 [L2472] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00194 [L2472] TGETS    A=1 B=1 C=59 D=315 'msg_update_label_status'
00195 [L2472] GGET     A=2 B=0 C=60 D=60 'msg_update_label_status_1045'
00196 [L2472] CALL     A=0 B=1 C=3 D=259 
00197 [L2473] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00198 [L2473] GGET     A=1 B=0 C=1 D=1 'd_ms'
00199 [L2473] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00200 [L2473] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00201 [L2473] TGETS    A=1 B=1 C=61 D=317 'msg_update_map_list'
00202 [L2473] GGET     A=2 B=0 C=62 D=62 'msg_update_map_list_1023'
00203 [L2473] CALL     A=0 B=1 C=3 D=259 
00204 [L2474] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00205 [L2474] GGET     A=1 B=0 C=1 D=1 'd_ms'
00206 [L2474] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00207 [L2474] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00208 [L2474] TGETS    A=1 B=1 C=63 D=319 'msg_update_sweep_rsp'
00209 [L2474] GGET     A=2 B=0 C=64 D=64 'msg_update_sweep_rsp_1062'
00210 [L2474] CALL     A=0 B=1 C=3 D=259 
00211 [L2476] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00212 [L2476] GGET     A=1 B=0 C=1 D=1 'd_ms'
00213 [L2476] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00214 [L2476] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00215 [L2476] TGETS    A=1 B=1 C=65 D=321 'msg_update_activity_info'
00216 [L2476] GGET     A=2 B=0 C=66 D=66 'msg_update_activity_info_1221'
00217 [L2476] CALL     A=0 B=1 C=3 D=259 
00218 [L2478] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00219 [L2478] GGET     A=1 B=0 C=1 D=1 'd_ms'
00220 [L2478] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00221 [L2478] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00222 [L2478] TGETS    A=1 B=1 C=67 D=323 'msg_process_done'
00223 [L2478] GGET     A=2 B=0 C=68 D=68 'msg_process_done_1106'
00224 [L2478] CALL     A=0 B=1 C=3 D=259 
00225 [L2479] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00226 [L2479] GGET     A=1 B=0 C=1 D=1 'd_ms'
00227 [L2479] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00228 [L2479] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00229 [L2479] TGETS    A=1 B=1 C=69 D=325 'msg_reconnect_notify'
00230 [L2479] GGET     A=2 B=0 C=70 D=70 'msg_reconnect_notify_2996'
00231 [L2479] CALL     A=0 B=1 C=3 D=259 
00232 [L2480] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00233 [L2480] GGET     A=1 B=0 C=1 D=1 'd_ms'
00234 [L2480] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00235 [L2480] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00236 [L2480] TGETS    A=1 B=1 C=71 D=327 'msg_modify_achievements'
00237 [L2480] GGET     A=2 B=0 C=72 D=72 'msg_modify_achievements_1066'
00238 [L2480] CALL     A=0 B=1 C=3 D=259 
00239 [L2481] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00240 [L2481] GGET     A=1 B=0 C=1 D=1 'd_ms'
00241 [L2481] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00242 [L2481] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00243 [L2481] TGETS    A=1 B=1 C=73 D=329 'msg_modify_title'
00244 [L2481] GGET     A=2 B=0 C=74 D=74 'msg_modify_title_1077'
00245 [L2481] CALL     A=0 B=1 C=3 D=259 
00246 [L2482] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00247 [L2482] GGET     A=1 B=0 C=1 D=1 'd_ms'
00248 [L2482] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00249 [L2482] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00250 [L2482] TGETS    A=1 B=1 C=75 D=331 'msg_send_tip_info'
00251 [L2482] GGET     A=2 B=0 C=76 D=76 'msg_send_tip_info_2995'
00252 [L2482] CALL     A=0 B=1 C=3 D=259 
00253 [L2483] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00254 [L2483] GGET     A=1 B=0 C=1 D=1 'd_ms'
00255 [L2483] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00256 [L2483] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00257 [L2483] TGETS    A=1 B=1 C=77 D=333 'msg_hole_event'
00258 [L2483] GGET     A=2 B=0 C=78 D=78 'msg_hole_event_1348'
00259 [L2483] CALL     A=0 B=1 C=3 D=259 
00260 [L2484] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00261 [L2484] GGET     A=1 B=0 C=1 D=1 'd_ms'
00262 [L2484] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00263 [L2484] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00264 [L2484] TGETS    A=1 B=1 C=79 D=335 'msg_undergo_ordeal_event'
00265 [L2484] GGET     A=2 B=0 C=80 D=80 'msg_undergo_ordeal_event_1349'
00266 [L2484] CALL     A=0 B=1 C=3 D=259 
00267 [L2485] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00268 [L2485] GGET     A=1 B=0 C=1 D=1 'd_ms'
00269 [L2485] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00270 [L2485] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00271 [L2485] TGETS    A=1 B=1 C=81 D=337 'msg_union_event'
00272 [L2485] GGET     A=2 B=0 C=82 D=82 'msg_union_event_1301'
00273 [L2485] CALL     A=0 B=1 C=3 D=259 
00274 [L2486] GGET     A=0 B=0 C=0 D=0 'regist_msg_function'
00275 [L2486] GGET     A=1 B=0 C=1 D=1 'd_ms'
00276 [L2486] TGETS    A=1 B=1 C=2 D=258 'd_msg_def'
00277 [L2486] TGETS    A=1 B=1 C=10 D=266 'gscl_msg_id'
00278 [L2486] TGETS    A=1 B=1 C=83 D=339 'msg_single_toplist_response'
00279 [L2486] GGET     A=2 B=0 C=84 D=84 'msg_get_single_toplist_1237'
00280 [L2486] CALL     A=0 B=1 C=3 D=259 
00281 [L2488] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto66 offset=0x1231e source_lines=0-2492 params=0
UPVALUES []
00001 [L7] GGET     A=0 B=0 C=0 D=0 'require'
00002 [L8] GGET     A=1 B=0 C=1 D=1 'bits'
00003 [L9] GGET     A=2 B=0 C=2 D=2 'sqlite'
00004 [L10] GGET     A=3 B=0 C=3 D=3 'type'
00005 [L11] GGET     A=4 B=0 C=4 D=4 'print'
00006 [L12] GGET     A=5 B=0 C=5 D=5 'tostring'
00007 [L13] GGET     A=6 B=0 C=6 D=6 'pairs'
00008 [L14] GGET     A=7 B=0 C=7 D=7 'debug'
00009 [L15] GGET     A=8 B=0 C=8 D=8 'math'
00010 [L16] GGET     A=9 B=0 C=9 D=9 'string'
00011 [L17] GGET     A=10 B=0 C=10 D=10 'table'
00012 [L18] GGET     A=11 B=0 C=11 D=11 'CCLuaLog'
00013 [L19] GGET     A=12 B=0 C=12 D=12 'os'
00014 [L20] GGET     A=13 B=0 C=13 D=13 'CCString'
00015 [L21] GGET     A=14 B=0 C=14 D=14 'CCFileUtils'
00016 [L22] GGET     A=15 B=0 C=15 D=15 'CCDirector'
00017 [L23] GGET     A=16 B=0 C=16 D=16 '_G'
00018 [L24] GGET     A=17 B=0 C=17 D=17 'package'
00019 [L26] GGET     A=18 B=0 C=18 D=18 'xpcall'
00020 [L27] GGET     A=19 B=0 C=19 D=19 'CCArray'
00021 [L28] GGET     A=20 B=0 C=20 D=20 'CCDelayTime'
00022 [L29] GGET     A=21 B=0 C=21 D=21 'CCCallFuncN'
00023 [L30] GGET     A=22 B=0 C=22 D=22 'CCSequence'
00024 [L31] GGET     A=23 B=0 C=23 D=23 'CCTextureCache'
00025 [L34] GGET     A=24 B=0 C=24 D=24 'main_server'
00026 [L36] GGET     A=25 B=0 C=25 D=25 'module'
00027 [L36] KSTR     A=26 B=0 C=26 D=26 'event_mgr'
00028 [L36] CALL     A=25 B=1 C=2 D=258 
00029 [L38] MOV      A=25 B=0 C=0 D=0 
00030 [L38] KSTR     A=26 B=0 C=27 D=27 'ms'
00031 [L38] CALL     A=25 B=2 C=2 D=514 
00032 [L38] GSET     A=25 B=0 C=28 D=28 'd_ms'
00033 [L39] GGET     A=25 B=0 C=28 D=28 'd_ms'
00034 [L39] IST      A=0 B=0 C=25 D=25 
00035 [L39] JMP      A=25 B=128 C=3 D=32771 target=39
00036 [L40] MOV      A=25 B=0 C=11 D=11 
00037 [L40] KSTR     A=26 B=0 C=29 D=29 'mg_client load d_ms fail.'
00038 [L40] CALL     A=25 B=1 C=2 D=258 
00039 [L45] FNEW     A=25 B=0 C=30 D=30 {'kind': 'proto', 'id': 0}
00040 [L48] GGET     A=26 B=0 C=28 D=28 'd_ms'
00041 [L48] TGETS    A=26 B=26 C=31 D=6687 'd_common_def'
00042 [L48] TGETS    A=26 B=26 C=32 D=6688 'object_type'
00043 [L48] GSET     A=26 B=0 C=33 D=33 'o_t'
00044 [L49] GGET     A=26 B=0 C=28 D=28 'd_ms'
00045 [L49] TGETS    A=26 B=26 C=31 D=6687 'd_common_def'
00046 [L49] TGETS    A=26 B=26 C=34 D=6690 'role_property'
00047 [L49] GSET     A=26 B=0 C=35 D=35 'r_p'
00048 [L50] GGET     A=26 B=0 C=28 D=28 'd_ms'
00049 [L50] TGETS    A=26 B=26 C=31 D=6687 'd_common_def'
00050 [L50] TGETS    A=26 B=26 C=36 D=6692 'cortege_property'
00051 [L50] GSET     A=26 B=0 C=37 D=37 'c_p'
00052 [L51] GGET     A=26 B=0 C=28 D=28 'd_ms'
00053 [L51] TGETS    A=26 B=26 C=31 D=6687 'd_common_def'
00054 [L51] TGETS    A=26 B=26 C=38 D=6694 'common_event_type'
00055 [L51] GSET     A=26 B=0 C=39 D=39 'e_t'
00056 [L52] GGET     A=26 B=0 C=28 D=28 'd_ms'
00057 [L52] TGETS    A=26 B=26 C=31 D=6687 'd_common_def'
00058 [L52] TGETS    A=26 B=26 C=40 D=6696 'union_event_type'
00059 [L52] GSET     A=26 B=0 C=41 D=41 'u_e_t'
00060 [L53] GGET     A=26 B=0 C=28 D=28 'd_ms'
00061 [L53] TGETS    A=26 B=26 C=31 D=6687 'd_common_def'
00062 [L53] TGETS    A=26 B=26 C=42 D=6698 'tip_type'
00063 [L53] GSET     A=26 B=0 C=43 D=43 't_t'
00064 [L56] TNEW     A=26 B=0 C=0 D=0 
00065 [L56] GSET     A=26 B=0 C=44 D=44 'g_msg_fun'
00066 [L58] TNEW     A=26 B=0 C=0 D=0 
00067 [L58] GSET     A=26 B=0 C=45 D=45 'g_fight_info'
00068 [L59] TNEW     A=26 B=0 C=0 D=0 
00069 [L59] GSET     A=26 B=0 C=46 D=46 'g_fight_id_list'
00070 [L62] TNEW     A=26 B=0 C=0 D=0 
00071 [L62] GSET     A=26 B=0 C=47 D=47 'g_self'
00072 [L63] GGET     A=26 B=0 C=47 D=47 'g_self'
00073 [L63] KSHORT   A=27 B=255 C=255 D=65535 -1
00074 [L63] TSETS    A=27 B=26 C=48 D=6704 'specialFightType'
00075 [L65] TNEW     A=26 B=0 C=0 D=0 
00076 [L65] GSET     A=26 B=0 C=49 D=49 'g_net_package_list'
00077 [L66] KPRI     A=26 B=0 C=0 D=0 
00078 [L66] GSET     A=26 B=0 C=50 D=50 'g_next_msg_type'
00079 [L77] FNEW     A=26 B=0 C=51 D=51 {'kind': 'proto', 'id': 1}
00080 [L69] GSET     A=26 B=0 C=52 D=52 'getLastFightInfo'
00081 [L86] FNEW     A=26 B=0 C=53 D=53 {'kind': 'proto', 'id': 2}
00082 [L81] GSET     A=26 B=0 C=54 D=54 'setSpecialFightType'
00083 [L102] FNEW     A=26 B=0 C=55 D=55 {'kind': 'proto', 'id': 3}
00084 [L90] GSET     A=26 B=0 C=56 D=56 'getLastFightType'
00085 [L112] FNEW     A=26 B=0 C=57 D=57 {'kind': 'proto', 'id': 4}
00086 [L106] GSET     A=26 B=0 C=58 D=58 'getLastOurName'
00087 [L122] FNEW     A=26 B=0 C=59 D=59 {'kind': 'proto', 'id': 5}
00088 [L116] GSET     A=26 B=0 C=60 D=60 'getLastEnemyName'
00089 [L127] TNEW     A=26 B=0 C=0 D=0 
00090 [L127] GSET     A=26 B=0 C=61 D=61 'g_all_fight_events'
00091 [L142] FNEW     A=26 B=0 C=62 D=62 {'kind': 'proto', 'id': 6}
00092 [L129] GSET     A=26 B=0 C=63 D=63 'callback_fight_extra_logic'
00093 [L154] FNEW     A=26 B=0 C=64 D=64 {'kind': 'proto', 'id': 7}
00094 [L147] GSET     A=26 B=0 C=65 D=65 'get_fight_events'
00095 [L160] FNEW     A=26 B=0 C=66 D=66 {'kind': 'proto', 'id': 8}
00096 [L158] GSET     A=26 B=0 C=67 D=67 'clean_all_fight_events'
00097 [L214] FNEW     A=26 B=0 C=68 D=68 {'kind': 'proto', 'id': 9}
00098 [L164] GSET     A=26 B=0 C=69 D=69 'dispatch_event'
00099 [L242] FNEW     A=26 B=0 C=70 D=70 {'kind': 'proto', 'id': 11}
00100 [L219] GSET     A=26 B=0 C=71 D=71 'handleSavedPackages'
00101 [L255] FNEW     A=26 B=0 C=72 D=72 {'kind': 'proto', 'id': 12}
00102 [L246] GSET     A=26 B=0 C=73 D=73 'getNextPackageType'
00103 [L277] FNEW     A=26 B=0 C=74 D=74 {'kind': 'proto', 'id': 13}
00104 [L259] GSET     A=26 B=0 C=75 D=75 'msg_process_done_1106'
00105 [L285] FNEW     A=26 B=0 C=76 D=76 {'kind': 'proto', 'id': 14}
00106 [L280] GSET     A=26 B=0 C=77 D=77 'regist_msg_function'
00107 [L298] FNEW     A=26 B=0 C=78 D=78 {'kind': 'proto', 'id': 15}
00108 [L288] GSET     A=26 B=0 C=79 D=79 'msg_login_rsp_1002'
00109 [L312] FNEW     A=26 B=0 C=80 D=80 {'kind': 'proto', 'id': 16}
00110 [L300] GSET     A=26 B=0 C=81 D=81 'inside_game_1017'
00111 [L322] FNEW     A=26 B=0 C=82 D=82 {'kind': 'proto', 'id': 17}
00112 [L316] GSET     A=26 B=0 C=83 D=83 'msg_reconnect_notify_2996'
00113 [L330] FNEW     A=26 B=0 C=84 D=84 {'kind': 'proto', 'id': 18}
00114 [L325] GSET     A=26 B=0 C=85 D=85 'msg_keep_alive_2999'
00115 [L349] FNEW     A=26 B=0 C=86 D=86 {'kind': 'proto', 'id': 19}
00116 [L333] GSET     A=26 B=0 C=87 D=87 'update_item_list_1056'
00117 [L366] FNEW     A=26 B=0 C=88 D=88 {'kind': 'proto', 'id': 20}
00118 [L353] GSET     A=26 B=0 C=89 D=89 'msg_update_label_list_1044'
00119 [L379] FNEW     A=26 B=0 C=90 D=90 {'kind': 'proto', 'id': 21}
00120 [L370] GSET     A=26 B=0 C=91 D=91 'msg_update_label_status_1045'
00121 [L398] FNEW     A=26 B=0 C=92 D=92 {'kind': 'proto', 'id': 22}
00122 [L383] GSET     A=26 B=0 C=93 D=93 'fight_lineup_1028'
00123 [L415] FNEW     A=26 B=0 C=94 D=94 {'kind': 'proto', 'id': 23}
00124 [L400] GSET     A=26 B=0 C=95 D=95 'special_fight_lineup_1141'
00125 [L558] FNEW     A=26 B=0 C=96 D=96 {'kind': 'proto', 'id': 24}
00126 [L417] GSET     A=26 B=0 C=97 D=97 'fight_result_1027'
00127 [L692] FNEW     A=26 B=0 C=98 D=98 {'kind': 'proto', 'id': 25}
00128 [L561] GSET     A=26 B=0 C=99 D=99 'special_fight_result_1140'
00129 [L699] FNEW     A=26 B=0 C=100 D=100 {'kind': 'proto', 'id': 26}
00130 [L696] GSET     A=26 B=0 C=101 D=101 'msg_login_rsp_3002'
00131 [L707] FNEW     A=26 B=0 C=102 D=102 {'kind': 'proto', 'id': 27}
00132 [L703] GSET     A=26 B=0 C=103 D=103 'msg_kick_player_3005'
00133 [L726] FNEW     A=26 B=0 C=104 D=104 {'kind': 'proto', 'id': 28}
00134 [L710] GSET     A=26 B=0 C=105 D=105 'msg_force_quit_1011'
00135 [L737] FNEW     A=26 B=0 C=106 D=106 {'kind': 'proto', 'id': 29}
00136 [L729] GSET     A=26 B=0 C=107 D=107 'msg_update_cortege_list_1034'
00137 [L749] FNEW     A=26 B=0 C=108 D=108 {'kind': 'proto', 'id': 30}
00138 [L740] GSET     A=26 B=0 C=109 D=109 'msg_update_attach_list_1035'
00139 [L759] FNEW     A=26 B=0 C=110 D=110 {'kind': 'proto', 'id': 31}
00140 [L751] GSET     A=26 B=0 C=111 D=111 'msg_update_spirit_list_1046'
00141 [L895] FNEW     A=26 B=0 C=112 D=112 {'kind': 'proto', 'id': 32}
00142 [L763] GSET     A=26 B=0 C=113 D=113 'msg_update_tollgate_data_1019'
00143 [L976] FNEW     A=26 B=0 C=114 D=114 {'kind': 'proto', 'id': 33}
00144 [L899] GSET     A=26 B=0 C=115 D=115 'msg_update_tollgate_list_1020'
00145 [L1087] FNEW     A=26 B=0 C=116 D=116 {'kind': 'proto', 'id': 35}
00146 [L984] GSET     A=26 B=0 C=117 D=117 'event_client_info_20'
00147 [L1128] FNEW     A=26 B=0 C=118 D=118 {'kind': 'proto', 'id': 36}
00148 [L1092] GSET     A=26 B=0 C=119 D=119 'event_client_update_info_21'
00149 [L1132] KPRI     A=26 B=0 C=1 D=1 
00150 [L1132] GSET     A=26 B=0 C=120 D=120 'g_isJumping'
00151 [L1172] FNEW     A=26 B=0 C=121 D=121 {'kind': 'proto', 'id': 39}
00152 [L1133] GSET     A=26 B=0 C=122 D=122 'jumpLoginUI'
00153 [L1181] FNEW     A=26 B=0 C=123 D=123 {'kind': 'proto', 'id': 40}
00154 [L1176] GSET     A=26 B=0 C=124 D=124 'msg_kick_player_2997'
00155 [L1194] GGET     A=26 B=0 C=28 D=28 'd_ms'
00156 [L1194] TGETS    A=26 B=26 C=31 D=6687 'd_common_def'
00157 [L1194] TGETS    A=26 B=26 C=125 D=6781 'operation_code'
00158 [L1195] TNEW     A=27 B=16 C=0 D=4096 
00159 [L1196] TGETS    A=28 B=26 C=126 D=6782 'invalid_match_time'
00160 [L1196] FNEW     A=29 B=0 C=127 D=127 {'kind': 'proto', 'id': 41}
00161 [L1196] TSETV    A=29 B=27 C=28 D=6940 
00162 [L1197] TGETS    A=28 B=26 C=128 D=6784 'less_action_point'
00163 [L1197] FNEW     A=29 B=0 C=129 D=129 {'kind': 'proto', 'id': 42}
00164 [L1197] TSETV    A=29 B=27 C=28 D=6940 
00165 [L1198] TGETS    A=28 B=26 C=130 D=6786 'less_life_point'
00166 [L1198] FNEW     A=29 B=0 C=131 D=131 {'kind': 'proto', 'id': 43}
00167 [L1198] TSETV    A=29 B=27 C=28 D=6940 
00168 [L1846] FNEW     A=28 B=0 C=132 D=132 {'kind': 'proto', 'id': 44}
00169 [L1202] GSET     A=28 B=0 C=133 D=133 'msg_common_event_2998'
00170 [L1871] FNEW     A=28 B=0 C=134 D=134 {'kind': 'proto', 'id': 45}
00171 [L1862] GSET     A=28 B=0 C=135 D=135 'msg_update_top_list_1022'
00172 [L2109] FNEW     A=28 B=0 C=136 D=136 {'kind': 'proto', 'id': 46}
00173 [L1873] GSET     A=28 B=0 C=137 D=137 'msg_modify_attr_1032'
00174 [L2127] FNEW     A=28 B=0 C=138 D=138 {'kind': 'proto', 'id': 47}
00175 [L2111] GSET     A=28 B=0 C=139 D=139 'msg_chat_info_to_client_1098'
00176 [L2134] FNEW     A=28 B=0 C=140 D=140 {'kind': 'proto', 'id': 48}
00177 [L2129] GSET     A=28 B=0 C=141 D=141 'msg_search_player_result_1092'
00178 [L2140] FNEW     A=28 B=0 C=142 D=142 {'kind': 'proto', 'id': 49}
00179 [L2136] GSET     A=28 B=0 C=143 D=143 'msg_update_attention_list_1095'
00180 [L2155] FNEW     A=28 B=0 C=144 D=144 {'kind': 'proto', 'id': 50}
00181 [L2142] GSET     A=28 B=0 C=145 D=145 'msg_remove_object_1038'
00182 [L2164] FNEW     A=28 B=0 C=146 D=146 {'kind': 'proto', 'id': 51}
00183 [L2157] GSET     A=28 B=0 C=147 D=147 'send_quit_game_1014'
00184 [L2168] FNEW     A=28 B=0 C=148 D=148 {'kind': 'proto', 'id': 52}
00185 [L2166] GSET     A=28 B=0 C=149 D=149 'msg_update_lottery_list_1047'
00186 [L2182] FNEW     A=28 B=0 C=150 D=150 {'kind': 'proto', 'id': 53}
00187 [L2171] GSET     A=28 B=0 C=151 D=151 'msg_update_map_list_1023'
00188 [L2299] FNEW     A=28 B=0 C=152 D=152 {'kind': 'proto', 'id': 55}
00189 [L2184] GSET     A=28 B=0 C=153 D=153 'event_msg_third_party_platform_22'
00190 [L2304] FNEW     A=28 B=0 C=154 D=154 {'kind': 'proto', 'id': 56}
00191 [L2301] GSET     A=28 B=0 C=155 D=155 'msg_update_sweep_rsp_1062'
00192 [L2310] FNEW     A=28 B=0 C=156 D=156 {'kind': 'proto', 'id': 57}
00193 [L2307] GSET     A=28 B=0 C=157 D=157 'msg_update_activity_info_1221'
00194 [L2314] FNEW     A=28 B=0 C=158 D=158 {'kind': 'proto', 'id': 58}
00195 [L2312] GSET     A=28 B=0 C=159 D=159 'msg_modify_achievements_1066'
00196 [L2318] FNEW     A=28 B=0 C=160 D=160 {'kind': 'proto', 'id': 59}
00197 [L2316] GSET     A=28 B=0 C=161 D=161 'msg_modify_title_1077'
00198 [L2323] FNEW     A=28 B=0 C=162 D=162 {'kind': 'proto', 'id': 60}
00199 [L2320] GSET     A=28 B=0 C=163 D=163 'msg_hole_event_1348'
00200 [L2328] FNEW     A=28 B=0 C=164 D=164 {'kind': 'proto', 'id': 61}
00201 [L2325] GSET     A=28 B=0 C=165 D=165 'msg_undergo_ordeal_event_1349'
00202 [L2351] FNEW     A=28 B=0 C=166 D=166 {'kind': 'proto', 'id': 62}
00203 [L2331] GSET     A=28 B=0 C=167 D=167 'msg_send_tip_info_2995'
00204 [L2423] FNEW     A=28 B=0 C=168 D=168 {'kind': 'proto', 'id': 63}
00205 [L2353] GSET     A=28 B=0 C=169 D=169 'msg_union_event_1301'
00206 [L2428] FNEW     A=28 B=0 C=170 D=170 {'kind': 'proto', 'id': 64}
00207 [L2425] GSET     A=28 B=0 C=171 D=171 'msg_get_single_toplist_1237'
00208 [L2488] FNEW     A=28 B=0 C=172 D=172 {'kind': 'proto', 'id': 65}
00209 [L2431] GSET     A=28 B=0 C=173 D=173 'init'
00210 [L2488] UCLO     A=0 B=128 C=0 D=32768 target=211
00211 [L2488] RET0     A=0 B=0 C=1 D=1 
