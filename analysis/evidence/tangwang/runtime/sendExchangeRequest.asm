LuaJIT dump version=1; source='@D:\\mg_update_\\lua_cache\\lua1\\0aaf9138ef79f4065afb567aa3dec130.data'; root=proto0

FUNCTION proto0 offset=0x4b source_lines=513-528 params=0
UPVALUES ['table', 'cclog']
00001 [L514] TNEW     A=0 B=0 C=0 D=0 
00002 [L515] KSHORT   A=1 B=0 C=1 D=1 1
00003 [L515] GGET     A=2 B=0 C=0 D=0 'g_self'
00004 [L515] TGETS    A=2 B=2 C=1 D=513 'LetterCount'
00005 [L515] KSHORT   A=3 B=0 C=1 D=1 1
00006 [L515] FORI     A=1 B=128 C=20 D=32788 target=27
00007 [L516] GGET     A=5 B=0 C=2 D=2 'g_cardUI'
00008 [L516] TGETS    A=5 B=5 C=3 D=1283 'UsedCards'
00009 [L516] TGETV    A=5 B=5 C=4 D=1284 
00010 [L516] ISF      A=0 B=0 C=5 D=5 
00011 [L516] JMP      A=6 B=128 C=9 D=32777 target=21
00012 [L517] UGET     A=5 B=0 C=0 D=0 table
00013 [L517] TGETS    A=5 B=5 C=4 D=1284 'insert'
00014 [L517] MOV      A=6 B=0 C=0 D=0 
00015 [L517] GGET     A=7 B=0 C=2 D=2 'g_cardUI'
00016 [L517] TGETS    A=7 B=7 C=3 D=1795 'UsedCards'
00017 [L517] TGETV    A=7 B=7 C=4 D=1796 
00018 [L517] TGETS    A=7 B=7 C=5 D=1797 'level'
00019 [L517] CALL     A=5 B=1 C=3 D=259 
00020 [L517] JMP      A=5 B=128 C=5 D=32773 target=26
00021 [L519] UGET     A=5 B=0 C=0 D=0 table
00022 [L519] TGETS    A=5 B=5 C=4 D=1284 'insert'
00023 [L519] MOV      A=6 B=0 C=0 D=0 
00024 [L519] KSHORT   A=7 B=0 C=0 D=0 0
00025 [L519] CALL     A=5 B=1 C=3 D=259 
00026 [L515] FORL     A=1 B=127 C=236 D=32748 target=7
00027 [L522] GGET     A=1 B=0 C=6 D=6 'getIDsbyLevels'
00028 [L522] MOV      A=2 B=0 C=0 D=0 
00029 [L522] CALL     A=1 B=2 C=2 D=514 
00030 [L522] MOV      A=0 B=0 C=1 D=1 
00031 [L523] TNEW     A=1 B=0 C=0 D=0 
00032 [L524] GGET     A=2 B=0 C=0 D=0 'g_self'
00033 [L524] TGETS    A=2 B=2 C=1 D=513 'LetterCount'
00034 [L524] TSETS    A=2 B=1 C=7 D=263 'count'
00035 [L525] TSETS    A=0 B=1 C=8 D=264 'card_list'
00036 [L526] UGET     A=2 B=0 C=1 D=1 cclog
00037 [L526] KSTR     A=3 B=0 C=9 D=9 'send msg msg_exchange_tangwang_prize '
00038 [L526] CALL     A=2 B=1 C=2 D=258 
00039 [L527] GGET     A=2 B=0 C=10 D=10 'd_ms'
00040 [L527] TGETS    A=2 B=2 C=11 D=523 'd_u'
00041 [L527] TGETS    A=2 B=2 C=12 D=524 'main_server_send_msg'
00042 [L527] GGET     A=3 B=0 C=10 D=10 'd_ms'
00043 [L527] TGETS    A=3 B=3 C=13 D=781 'd_msg_def'
00044 [L527] TGETS    A=3 B=3 C=14 D=782 'gscl_msg_id'
00045 [L527] TGETS    A=3 B=3 C=15 D=783 'msg_exchange_tangwang_prize'
00046 [L527] MOV      A=4 B=0 C=1 D=1 
00047 [L527] CALL     A=2 B=1 C=3 D=259 
00048 [L528] RET0     A=0 B=0 C=1 D=1 
