LuaJIT dump version=1; source='@D:\\mg_update_\\lua_cache\\lua1\\0aaf9138ef79f4065afb567aa3dec130.data'; root=proto0

FUNCTION proto0 offset=0x4b source_lines=251-272 params=3
UPVALUES ['CCTOUCHBEGAN', 'CCTOUCHMOVED']
00001 [L252] GGET     A=3 B=0 C=0 D=0 'removeTmpSprite'
00002 [L252] CALL     A=3 B=1 C=1 D=257 
00003 [L253] KSHORT   A=3 B=0 C=1 D=1 1
00004 [L253] GSET     A=3 B=0 C=1 D=1 'g_flag'
00005 [L254] UGET     A=3 B=0 C=0 D=0 CCTOUCHBEGAN
00006 [L254] ISNEV    A=0 B=0 C=3 D=3 
00007 [L254] JMP      A=3 B=128 C=18 D=32786 target=26
00008 [L255] GGET     A=3 B=0 C=2 D=2 'onTouchBegan'
00009 [L255] MOV      A=4 B=0 C=1 D=1 
00010 [L255] MOV      A=5 B=0 C=2 D=2 
00011 [L255] CALL     A=3 B=2 C=3 D=515 
00012 [L256] ISF      A=0 B=0 C=3 D=3 
00013 [L256] JMP      A=4 B=128 C=10 D=32778 target=24
00014 [L257] GGET     A=4 B=0 C=3 D=3 'g_self'
00015 [L257] GGET     A=5 B=0 C=3 D=3 'g_self'
00016 [L257] TGETS    A=5 B=5 C=5 D=1285 'TouchStatus'
00017 [L257] TGETS    A=5 B=5 C=6 D=1286 'Begin'
00018 [L257] TSETS    A=5 B=4 C=4 D=1028 'touch'
00019 [L258] GGET     A=4 B=0 C=7 D=7 'g_cardUI'
00020 [L258] GGET     A=5 B=0 C=7 D=7 'g_cardUI'
00021 [L258] TGETS    A=5 B=5 C=8 D=1288 'TouchCount'
00022 [L258] ADDVN    A=5 B=5 C=0 D=1280 
00023 [L258] TSETS    A=5 B=4 C=8 D=1032 'TouchCount'
00024 [L260] RET1     A=3 B=0 C=2 D=2 
00025 [L260] JMP      A=3 B=128 C=29 D=32797 target=55
00026 [L261] UGET     A=3 B=0 C=1 D=1 CCTOUCHMOVED
00027 [L261] ISNEV    A=0 B=0 C=3 D=3 
00028 [L261] JMP      A=3 B=128 C=10 D=32778 target=39
00029 [L262] GGET     A=3 B=0 C=3 D=3 'g_self'
00030 [L262] GGET     A=4 B=0 C=3 D=3 'g_self'
00031 [L262] TGETS    A=4 B=4 C=5 D=1029 'TouchStatus'
00032 [L262] TGETS    A=4 B=4 C=9 D=1033 'Moved'
00033 [L262] TSETS    A=4 B=3 C=4 D=772 'touch'
00034 [L263] GGET     A=3 B=0 C=10 D=10 'onTouchMoved'
00035 [L263] MOV      A=4 B=0 C=1 D=1 
00036 [L263] MOV      A=5 B=0 C=2 D=2 
00037 [L263] CALL     A=3 B=1 C=3 D=259 
00038 [L263] JMP      A=3 B=128 C=16 D=32784 target=55
00039 [L265] GGET     A=3 B=0 C=3 D=3 'g_self'
00040 [L265] KPRI     A=4 B=0 C=0 D=0 
00041 [L265] TSETS    A=4 B=3 C=4 D=772 'touch'
00042 [L266] GGET     A=3 B=0 C=11 D=11 'onTouchEnded'
00043 [L266] MOV      A=4 B=0 C=1 D=1 
00044 [L266] MOV      A=5 B=0 C=2 D=2 
00045 [L266] CALL     A=3 B=1 C=3 D=259 
00046 [L267] GGET     A=3 B=0 C=7 D=7 'g_cardUI'
00047 [L267] KPRI     A=4 B=0 C=0 D=0 
00048 [L267] TSETS    A=4 B=3 C=12 D=780 'Chosen'
00049 [L269] GGET     A=3 B=0 C=7 D=7 'g_cardUI'
00050 [L269] KPRI     A=4 B=0 C=0 D=0 
00051 [L269] TSETS    A=4 B=3 C=13 D=781 'begin_pos'
00052 [L270] GGET     A=3 B=0 C=7 D=7 'g_cardUI'
00053 [L270] KPRI     A=4 B=0 C=0 D=0 
00054 [L270] TSETS    A=4 B=3 C=14 D=782 'move_pos'
00055 [L272] RET0     A=0 B=0 C=1 D=1 
