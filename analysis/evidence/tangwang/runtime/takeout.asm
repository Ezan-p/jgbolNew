LuaJIT dump version=1; source='@D:\\mg_update_\\lua_cache\\lua1\\0aaf9138ef79f4065afb567aa3dec130.data'; root=proto0

FUNCTION proto0 offset=0x4b source_lines=454-468 params=1
UPVALUES ['table', 'cclog']
00001 [L455] GGET     A=1 B=0 C=0 D=0 'g_cardUI'
00002 [L455] TGETS    A=1 B=1 C=1 D=257 'UnusedCards'
00003 [L455] TGETV    A=1 B=1 C=0 D=256 
00004 [L455] ISF      A=0 B=0 C=1 D=1 
00005 [L455] JMP      A=2 B=128 C=25 D=32793 target=31
00006 [L456] GGET     A=1 B=0 C=0 D=0 'g_cardUI'
00007 [L456] TGETS    A=1 B=1 C=1 D=257 'UnusedCards'
00008 [L457] TGETV    A=2 B=1 C=0 D=256 
00009 [L457] TGETV    A=3 B=1 C=0 D=256 
00010 [L457] TGETS    A=3 B=3 C=2 D=770 'count'
00011 [L457] SUBVN    A=3 B=3 C=0 D=768 
00012 [L457] TSETS    A=3 B=2 C=2 D=514 'count'
00013 [L458] TGETV    A=2 B=1 C=0 D=256 
00014 [L458] TGETS    A=2 B=2 C=2 D=514 'count'
00015 [L458] ISNEN    A=2 B=0 C=1 D=1 0
00016 [L458] JMP      A=2 B=128 C=6 D=32774 target=23
00017 [L459] UGET     A=2 B=0 C=0 D=0 table
00018 [L459] TGETS    A=2 B=2 C=3 D=515 'remove'
00019 [L459] MOV      A=3 B=0 C=1 D=1 
00020 [L459] MOV      A=4 B=0 C=0 D=0 
00021 [L459] CALL     A=2 B=1 C=3 D=259 
00022 [L459] JMP      A=2 B=128 C=8 D=32776 target=31
00023 [L460] TGETV    A=2 B=1 C=0 D=256 
00024 [L460] TGETS    A=2 B=2 C=2 D=514 'count'
00025 [L460] KSHORT   A=3 B=0 C=0 D=0 0
00026 [L460] ISGE     A=2 B=0 C=3 D=3 
00027 [L460] JMP      A=2 B=128 C=3 D=32771 target=31
00028 [L461] UGET     A=2 B=0 C=1 D=1 cclog
00029 [L461] KSTR     A=3 B=0 C=4 D=4 'ERROR: negtive count in g_cardUI.UnusedCards'
00030 [L461] CALL     A=2 B=1 C=2 D=258 
00031 [L465] GGET     A=1 B=0 C=0 D=0 'g_cardUI'
00032 [L465] TGETS    A=1 B=1 C=5 D=261 'cardsContainer'
00033 [L465] MOV      A=2 B=0 C=1 D=1 
00034 [L465] TGETS    A=1 B=1 C=6 D=262 'getPositionX'
00035 [L465] CALL     A=1 B=2 C=2 D=514 
00036 [L466] GGET     A=2 B=0 C=7 D=7 'createCardsScrollLayer'
00037 [L466] CALL     A=2 B=1 C=1 D=257 
00038 [L467] GGET     A=2 B=0 C=0 D=0 'g_cardUI'
00039 [L467] TGETS    A=2 B=2 C=5 D=517 'cardsContainer'
00040 [L467] MOV      A=3 B=0 C=2 D=2 
00041 [L467] TGETS    A=2 B=2 C=8 D=520 'setPositionX'
00042 [L467] MOV      A=4 B=0 C=1 D=1 
00043 [L467] CALL     A=2 B=1 C=3 D=259 
00044 [L468] RET0     A=0 B=0 C=1 D=1 
