LuaJIT dump version=1; source='@D:\\mg_update_\\lua_cache\\lua1\\0aaf9138ef79f4065afb567aa3dec130.data'; root=proto0

FUNCTION proto0 offset=0x4b source_lines=356-368 params=2
UPVALUES ['CCPointMake', 'math', 'ccpDistance']
00001 [L358] GGET     A=2 B=0 C=0 D=0 'g_cardUI'
00002 [L358] TGETS    A=2 B=2 C=1 D=513 'Chosen'
00003 [L358] ISF      A=0 B=0 C=2 D=2 
00004 [L358] JMP      A=3 B=128 C=38 D=32806 target=43
00005 [L358] GGET     A=2 B=0 C=0 D=0 'g_cardUI'
00006 [L358] TGETS    A=2 B=2 C=1 D=513 'Chosen'
00007 [L358] TGETS    A=2 B=2 C=2 D=514 'sprite'
00008 [L358] ISF      A=0 B=0 C=2 D=2 
00009 [L358] JMP      A=3 B=128 C=33 D=32801 target=43
00010 [L359] GGET     A=2 B=0 C=0 D=0 'g_cardUI'
00011 [L359] TGETS    A=2 B=2 C=3 D=515 'main_layer'
00012 [L359] MOV      A=3 B=0 C=2 D=2 
00013 [L359] TGETS    A=2 B=2 C=4 D=516 'convertToNodeSpace'
00014 [L359] UGET     A=4 B=0 C=0 D=0 CCPointMake
00015 [L359] MOV      A=5 B=0 C=0 D=0 
00016 [L359] MOV      A=6 B=0 C=1 D=1 
00017 [L359] CALL     A=4 B=0 C=3 D=3 
00018 [L359] CALLM    A=2 B=2 C=1 D=513 
00019 [L360] UGET     A=3 B=0 C=1 D=1 math
00020 [L360] TGETS    A=3 B=3 C=5 D=773 'abs'
00021 [L360] UGET     A=4 B=0 C=2 D=2 ccpDistance
00022 [L360] GGET     A=5 B=0 C=0 D=0 'g_cardUI'
00023 [L360] TGETS    A=5 B=5 C=1 D=1281 'Chosen'
00024 [L360] TGETS    A=5 B=5 C=6 D=1286 'startPoint'
00025 [L360] MOV      A=6 B=0 C=2 D=2 
00026 [L360] CALL     A=4 B=0 C=3 D=3 
00027 [L360] CALLM    A=3 B=2 C=0 D=512 
00028 [L361] KSHORT   A=4 B=0 C=20 D=20 20
00029 [L361] ISGE     A=4 B=0 C=3 D=3 
00030 [L361] JMP      A=4 B=128 C=4 D=32772 target=35
00031 [L362] GGET     A=4 B=0 C=0 D=0 'g_cardUI'
00032 [L362] TGETS    A=4 B=4 C=1 D=1025 'Chosen'
00033 [L362] KPRI     A=5 B=0 C=2 D=2 
00034 [L362] TSETS    A=5 B=4 C=7 D=1031 'isMoved'
00035 [L364] GGET     A=4 B=0 C=0 D=0 'g_cardUI'
00036 [L364] TGETS    A=4 B=4 C=1 D=1025 'Chosen'
00037 [L364] TGETS    A=4 B=4 C=2 D=1026 'sprite'
00038 [L364] MOV      A=5 B=0 C=4 D=4 
00039 [L364] TGETS    A=4 B=4 C=8 D=1032 'setPosition'
00040 [L364] MOV      A=6 B=0 C=2 D=2 
00041 [L364] CALL     A=4 B=1 C=3 D=259 
00042 [L364] JMP      A=2 B=128 C=11 D=32779 target=54
00043 [L366] GGET     A=2 B=0 C=0 D=0 'g_cardUI'
00044 [L366] GGET     A=3 B=0 C=0 D=0 'g_cardUI'
00045 [L366] TGETS    A=3 B=3 C=3 D=771 'main_layer'
00046 [L366] MOV      A=4 B=0 C=3 D=3 
00047 [L366] TGETS    A=3 B=3 C=4 D=772 'convertToNodeSpace'
00048 [L366] UGET     A=5 B=0 C=0 D=0 CCPointMake
00049 [L366] MOV      A=6 B=0 C=0 D=0 
00050 [L366] MOV      A=7 B=0 C=1 D=1 
00051 [L366] CALL     A=5 B=0 C=3 D=3 
00052 [L366] CALLM    A=3 B=2 C=1 D=513 
00053 [L366] TSETS    A=3 B=2 C=9 D=521 'move_pos'
00054 [L368] RET0     A=0 B=0 C=1 D=1 
