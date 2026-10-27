LuaJIT dump version=1; source='@D:\\mg_update_\\lua_cache\\lua1\\0aaf9138ef79f4065afb567aa3dec130.data'; root=proto1

FUNCTION proto0 offset=0x4b source_lines=136-145 params=1
UPVALUES ['CCDirector']
00001 [L137] TGETS    A=1 B=0 C=0 D=0 'name'
00002 [L137] ISNES    A=1 B=0 C=1 D=1 'exit'
00003 [L137] JMP      A=1 B=128 C=26 D=32794 target=30
00004 [L138] TNEW     A=1 B=0 C=0 D=0 
00005 [L138] GSET     A=1 B=0 C=2 D=2 'g_cardUI'
00006 [L139] GGET     A=1 B=0 C=3 D=3 'g_self'
00007 [L139] TGETS    A=1 B=1 C=4 D=260 'CountDownHandler'
00008 [L139] ISEQP    A=1 B=0 C=0 D=0 
00009 [L139] JMP      A=1 B=128 C=20 D=32788 target=30
00010 [L139] GGET     A=1 B=0 C=3 D=3 'g_self'
00011 [L139] TGETS    A=1 B=1 C=4 D=260 'CountDownHandler'
00012 [L139] ISEQN    A=1 B=0 C=0 D=0 0
00013 [L139] JMP      A=1 B=128 C=16 D=32784 target=30
00014 [L140] UGET     A=1 B=0 C=0 D=0 CCDirector
00015 [L140] MOV      A=2 B=0 C=1 D=1 
00016 [L140] TGETS    A=1 B=1 C=5 D=261 'sharedDirector'
00017 [L140] CALL     A=1 B=2 C=2 D=514 
00018 [L140] MOV      A=2 B=0 C=1 D=1 
00019 [L140] TGETS    A=1 B=1 C=6 D=262 'getScheduler'
00020 [L140] CALL     A=1 B=2 C=2 D=514 
00021 [L140] MOV      A=2 B=0 C=1 D=1 
00022 [L140] TGETS    A=1 B=1 C=7 D=263 'unscheduleScriptEntry'
00023 [L140] GGET     A=3 B=0 C=3 D=3 'g_self'
00024 [L140] TGETS    A=3 B=3 C=4 D=772 'CountDownHandler'
00025 [L140] CALL     A=1 B=1 C=3 D=259 
00026 [L141] GGET     A=1 B=0 C=3 D=3 'g_self'
00027 [L141] KPRI     A=2 B=0 C=0 D=0 
00028 [L141] TSETS    A=2 B=1 C=4 D=260 'CountDownHandler'
00029 [L142] RET0     A=0 B=0 C=1 D=1 
00030 [L145] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto1 offset=0x166 source_lines=133-151 params=0
UPVALUES ['CCLayer', 'CCDirector']
00001 [L134] GGET     A=0 B=0 C=0 D=0 'g_cardUI'
00002 [L134] UGET     A=1 B=0 C=0 D=0 CCLayer
00003 [L134] MOV      A=2 B=0 C=1 D=1 
00004 [L134] TGETS    A=1 B=1 C=2 D=258 'create'
00005 [L134] CALL     A=1 B=2 C=2 D=514 
00006 [L134] TSETS    A=1 B=0 C=1 D=1 'main_layer'
00007 [L145] FNEW     A=0 B=0 C=3 D=3 {'kind': 'proto', 'id': 0}
00008 [L146] GGET     A=1 B=0 C=0 D=0 'g_cardUI'
00009 [L146] TGETS    A=1 B=1 C=1 D=257 'main_layer'
00010 [L146] MOV      A=2 B=0 C=1 D=1 
00011 [L146] TGETS    A=1 B=1 C=4 D=260 'registerScriptHandler'
00012 [L146] MOV      A=3 B=0 C=0 D=0 
00013 [L146] CALL     A=1 B=1 C=3 D=259 
00014 [L148] GGET     A=1 B=0 C=5 D=5 'createStaticElements'
00015 [L148] CALL     A=1 B=1 C=1 D=257 
00016 [L150] GGET     A=1 B=0 C=6 D=6 'createExchangeLayer'
00017 [L150] CALL     A=1 B=1 C=1 D=257 
00018 [L151] RET0     A=0 B=0 C=1 D=1 
