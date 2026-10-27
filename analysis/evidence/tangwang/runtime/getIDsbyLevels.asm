LuaJIT dump version=1; source='@D:\\mg_update_\\lua_cache\\lua1\\0aaf9138ef79f4065afb567aa3dec130.data'; root=proto1

FUNCTION proto0 offset=0x4a source_lines=480-487 params=2
UPVALUES ['pairs']
00001 [L481] UGET     A=2 B=0 C=0 D=0 pairs
00002 [L481] MOV      A=3 B=0 C=0 D=0 
00003 [L481] CALL     A=2 B=4 C=2 D=1026 
00004 [L481] ISNEXT   A=5 B=128 C=5 D=32773 target=10
00005 [L482] TGETS    A=7 B=6 C=0 D=1536 'id'
00006 [L482] ISNEV    A=1 B=0 C=7 D=7 
00007 [L482] JMP      A=7 B=128 C=2 D=32770 target=10
00008 [L483] KPRI     A=7 B=0 C=2 D=2 
00009 [L483] RET1     A=7 B=0 C=2 D=2 
00010 [L481] ITERN    A=5 B=3 C=3 D=771 
00011 [L481] ITERL    A=5 B=127 C=249 D=32761 target=5
00012 [L486] KPRI     A=2 B=0 C=1 D=1 
00013 [L486] RET1     A=2 B=0 C=2 D=2 

FUNCTION proto1 offset=0xc3 source_lines=479-510 params=1
UPVALUES ['pairs', 'table']
00001 [L487] FNEW     A=1 B=0 C=0 D=0 {'kind': 'proto', 'id': 0}
00002 [L488] TNEW     A=2 B=0 C=0 D=0 
00003 [L489] KSHORT   A=3 B=0 C=1 D=1 1
00004 [L489] LEN      A=4 B=0 C=0 D=0 
00005 [L489] KSHORT   A=5 B=0 C=1 D=1 1
00006 [L489] FORI     A=3 B=128 C=38 D=32806 target=45
00007 [L490] GGET     A=7 B=0 C=1 D=1 'g_cardUI'
00008 [L490] TGETS    A=7 B=7 C=2 D=1794 'countList'
00009 [L490] TGETV    A=8 B=0 C=6 D=6 
00010 [L490] TGETV    A=7 B=7 C=8 D=1800 
00011 [L491] ISF      A=0 B=0 C=7 D=7 
00012 [L491] JMP      A=8 B=128 C=2 D=32770 target=15
00013 [L492] TGETS    A=7 B=7 C=3 D=1795 'ids'
00014 [L492] JMP      A=8 B=128 C=1 D=32769 target=16
00015 [L494] TNEW     A=7 B=0 C=0 D=0 
00016 [L496] KPRI     A=8 B=0 C=1 D=1 
00017 [L497] KSHORT   A=9 B=0 C=1 D=1 1
00018 [L497] LEN      A=10 B=0 C=7 D=7 
00019 [L497] KSHORT   A=11 B=0 C=1 D=1 1
00020 [L497] FORI     A=9 B=128 C=16 D=32784 target=37
00021 [L498] TGETV    A=13 B=7 C=12 D=1804 
00022 [L499] MOV      A=14 B=0 C=1 D=1 
00023 [L499] MOV      A=15 B=0 C=2 D=2 
00024 [L499] MOV      A=16 B=0 C=13 D=13 
00025 [L499] CALL     A=14 B=2 C=3 D=515 
00026 [L499] IST      A=0 B=0 C=14 D=14 
00027 [L499] JMP      A=14 B=128 C=8 D=32776 target=36
00028 [L500] UGET     A=14 B=0 C=1 D=1 table
00029 [L500] TGETS    A=14 B=14 C=4 D=3588 'insert'
00030 [L500] MOV      A=15 B=0 C=2 D=2 
00031 [L500] TDUP     A=16 B=0 C=5 D=5 {'kind': 'table', 'value': {}}
00032 [L500] TSETS    A=13 B=16 C=6 D=4102 'id'
00033 [L500] CALL     A=14 B=1 C=3 D=259 
00034 [L501] KPRI     A=8 B=0 C=2 D=2 
00035 [L502] JMP      A=9 B=128 C=1 D=32769 target=37
00036 [L497] FORL     A=9 B=127 C=240 D=32752 target=21
00037 [L505] IST      A=0 B=0 C=8 D=8 
00038 [L505] JMP      A=9 B=128 C=5 D=32773 target=44
00039 [L506] UGET     A=9 B=0 C=1 D=1 table
00040 [L506] TGETS    A=9 B=9 C=4 D=2308 'insert'
00041 [L506] MOV      A=10 B=0 C=2 D=2 
00042 [L506] TDUP     A=11 B=0 C=7 D=7 {'kind': 'table', 'value': {'id': 0}}
00043 [L506] CALL     A=9 B=1 C=3 D=259 
00044 [L489] FORL     A=3 B=127 C=218 D=32730 target=7
00045 [L509] UCLO     A=0 B=128 C=0 D=32768 target=46
00046 [L509] RET1     A=2 B=0 C=2 D=2 
