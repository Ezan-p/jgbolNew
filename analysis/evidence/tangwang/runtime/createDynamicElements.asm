LuaJIT dump version=1; source='@D:\\mg_update_\\lua_cache\\lua1\\0aaf9138ef79f4065afb567aa3dec130.data'; root=proto2

FUNCTION proto0 offset=0x4a source_lines=230-232 params=0
UPVALUES ['introduce']
00001 [L231] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L231] TGETS    A=0 B=0 C=1 D=1 'd_u'
00003 [L231] TGETS    A=0 B=0 C=2 D=2 'remove'
00004 [L231] UGET     A=1 B=0 C=0 D=0 introduce
00005 [L231] CALL     A=0 B=1 C=2 D=258 
00006 [L232] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto1 offset=0x92 source_lines=195-240 params=0
UPVALUES ['buttons', 'left_scroll', 'CCArray', 'CCMoveBy', 'CCEaseOut', 'CCDelayTime', 'CCSequence', 'right_scroll', 'paper_bkg', 'CCScaleBy', 'CCCallFuncN', 'introduce']
00001 [L197] UGET     A=0 B=0 C=0 D=0 buttons
00002 [L197] TGETB    A=0 B=0 C=1 D=1 
00003 [L197] ISF      A=0 B=0 C=0 D=0 
00004 [L197] JMP      A=1 B=128 C=6 D=32774 target=11
00005 [L198] GGET     A=0 B=0 C=0 D=0 'd_ms'
00006 [L198] TGETS    A=0 B=0 C=1 D=1 'd_u'
00007 [L198] TGETS    A=0 B=0 C=2 D=2 'remove'
00008 [L198] UGET     A=1 B=0 C=0 D=0 buttons
00009 [L198] TGETB    A=1 B=1 C=1 D=257 
00010 [L198] CALL     A=0 B=1 C=2 D=258 
00011 [L201] KNUM     A=0 B=0 C=0 D=0 0.5
00012 [L202] KNUM     A=1 B=0 C=1 D=1 0.25
00013 [L204] UGET     A=2 B=0 C=1 D=1 left_scroll
00014 [L204] ISF      A=0 B=0 C=2 D=2 
00015 [L204] JMP      A=3 B=128 C=54 D=32822 target=70
00016 [L205] UGET     A=2 B=0 C=2 D=2 CCArray
00017 [L205] MOV      A=3 B=0 C=2 D=2 
00018 [L205] TGETS    A=2 B=2 C=3 D=515 'create'
00019 [L205] CALL     A=2 B=2 C=2 D=514 
00020 [L206] UGET     A=3 B=0 C=3 D=3 CCMoveBy
00021 [L206] MOV      A=4 B=0 C=3 D=3 
00022 [L206] TGETS    A=3 B=3 C=3 D=771 'create'
00023 [L206] MOV      A=5 B=0 C=0 D=0 
00024 [L206] GGET     A=6 B=0 C=0 D=0 'd_ms'
00025 [L206] TGETS    A=6 B=6 C=1 D=1537 'd_u'
00026 [L206] TGETS    A=6 B=6 C=4 D=1540 'makePoint'
00027 [L206] GGET     A=7 B=0 C=5 D=5 'g_self'
00028 [L206] TGETS    A=7 B=7 C=6 D=1798 'left_x'
00029 [L206] SUBNV    A=7 B=7 C=2 D=1794 
00030 [L206] KSHORT   A=8 B=0 C=0 D=0 0
00031 [L206] CALL     A=6 B=0 C=3 D=3 
00032 [L206] CALLM    A=3 B=2 C=2 D=514 
00033 [L207] MOV      A=5 B=0 C=2 D=2 
00034 [L207] TGETS    A=4 B=2 C=7 D=519 'addObject'
00035 [L207] UGET     A=6 B=0 C=4 D=4 CCEaseOut
00036 [L207] MOV      A=7 B=0 C=6 D=6 
00037 [L207] TGETS    A=6 B=6 C=3 D=1539 'create'
00038 [L207] MOV      A=8 B=0 C=3 D=3 
00039 [L207] KSHORT   A=9 B=0 C=3 D=3 3
00040 [L207] CALL     A=6 B=0 C=4 D=4 
00041 [L207] CALLM    A=4 B=1 C=1 D=257 
00042 [L208] MOV      A=5 B=0 C=2 D=2 
00043 [L208] TGETS    A=4 B=2 C=7 D=519 'addObject'
00044 [L208] UGET     A=6 B=0 C=5 D=5 CCDelayTime
00045 [L208] MOV      A=7 B=0 C=6 D=6 
00046 [L208] TGETS    A=6 B=6 C=3 D=1539 'create'
00047 [L208] MOV      A=8 B=0 C=1 D=1 
00048 [L208] CALL     A=6 B=0 C=3 D=3 
00049 [L208] CALLM    A=4 B=1 C=1 D=257 
00050 [L209] MOV      A=5 B=0 C=2 D=2 
00051 [L209] TGETS    A=4 B=2 C=7 D=519 'addObject'
00052 [L209] UGET     A=6 B=0 C=4 D=4 CCEaseOut
00053 [L209] MOV      A=7 B=0 C=6 D=6 
00054 [L209] TGETS    A=6 B=6 C=3 D=1539 'create'
00055 [L209] MOV      A=9 B=0 C=3 D=3 
00056 [L209] TGETS    A=8 B=3 C=8 D=776 'reverse'
00057 [L209] CALL     A=8 B=2 C=2 D=514 
00058 [L209] KSHORT   A=9 B=0 C=3 D=3 3
00059 [L209] CALL     A=6 B=0 C=4 D=4 
00060 [L209] CALLM    A=4 B=1 C=1 D=257 
00061 [L210] UGET     A=4 B=0 C=1 D=1 left_scroll
00062 [L210] MOV      A=5 B=0 C=4 D=4 
00063 [L210] TGETS    A=4 B=4 C=9 D=1033 'runAction'
00064 [L210] UGET     A=6 B=0 C=6 D=6 CCSequence
00065 [L210] MOV      A=7 B=0 C=6 D=6 
00066 [L210] TGETS    A=6 B=6 C=3 D=1539 'create'
00067 [L210] MOV      A=8 B=0 C=2 D=2 
00068 [L210] CALL     A=6 B=0 C=3 D=3 
00069 [L210] CALLM    A=4 B=1 C=1 D=257 
00070 [L212] UGET     A=2 B=0 C=7 D=7 right_scroll
00071 [L212] ISF      A=0 B=0 C=2 D=2 
00072 [L212] JMP      A=3 B=128 C=54 D=32822 target=127
00073 [L213] UGET     A=2 B=0 C=2 D=2 CCArray
00074 [L213] MOV      A=3 B=0 C=2 D=2 
00075 [L213] TGETS    A=2 B=2 C=3 D=515 'create'
00076 [L213] CALL     A=2 B=2 C=2 D=514 
00077 [L214] UGET     A=3 B=0 C=3 D=3 CCMoveBy
00078 [L214] MOV      A=4 B=0 C=3 D=3 
00079 [L214] TGETS    A=3 B=3 C=3 D=771 'create'
00080 [L214] MOV      A=5 B=0 C=0 D=0 
00081 [L214] GGET     A=6 B=0 C=0 D=0 'd_ms'
00082 [L214] TGETS    A=6 B=6 C=1 D=1537 'd_u'
00083 [L214] TGETS    A=6 B=6 C=4 D=1540 'makePoint'
00084 [L214] GGET     A=7 B=0 C=5 D=5 'g_self'
00085 [L214] TGETS    A=7 B=7 C=6 D=1798 'left_x'
00086 [L214] SUBVN    A=7 B=7 C=2 D=1794 
00087 [L214] KSHORT   A=8 B=0 C=0 D=0 0
00088 [L214] CALL     A=6 B=0 C=3 D=3 
00089 [L214] CALLM    A=3 B=2 C=2 D=514 
00090 [L215] MOV      A=5 B=0 C=2 D=2 
00091 [L215] TGETS    A=4 B=2 C=7 D=519 'addObject'
00092 [L215] UGET     A=6 B=0 C=4 D=4 CCEaseOut
00093 [L215] MOV      A=7 B=0 C=6 D=6 
00094 [L215] TGETS    A=6 B=6 C=3 D=1539 'create'
00095 [L215] MOV      A=8 B=0 C=3 D=3 
00096 [L215] KSHORT   A=9 B=0 C=3 D=3 3
00097 [L215] CALL     A=6 B=0 C=4 D=4 
00098 [L215] CALLM    A=4 B=1 C=1 D=257 
00099 [L216] MOV      A=5 B=0 C=2 D=2 
00100 [L216] TGETS    A=4 B=2 C=7 D=519 'addObject'
00101 [L216] UGET     A=6 B=0 C=5 D=5 CCDelayTime
00102 [L216] MOV      A=7 B=0 C=6 D=6 
00103 [L216] TGETS    A=6 B=6 C=3 D=1539 'create'
00104 [L216] MOV      A=8 B=0 C=1 D=1 
00105 [L216] CALL     A=6 B=0 C=3 D=3 
00106 [L216] CALLM    A=4 B=1 C=1 D=257 
00107 [L217] MOV      A=5 B=0 C=2 D=2 
00108 [L217] TGETS    A=4 B=2 C=7 D=519 'addObject'
00109 [L217] UGET     A=6 B=0 C=4 D=4 CCEaseOut
00110 [L217] MOV      A=7 B=0 C=6 D=6 
00111 [L217] TGETS    A=6 B=6 C=3 D=1539 'create'
00112 [L217] MOV      A=9 B=0 C=3 D=3 
00113 [L217] TGETS    A=8 B=3 C=8 D=776 'reverse'
00114 [L217] CALL     A=8 B=2 C=2 D=514 
00115 [L217] KSHORT   A=9 B=0 C=3 D=3 3
00116 [L217] CALL     A=6 B=0 C=4 D=4 
00117 [L217] CALLM    A=4 B=1 C=1 D=257 
00118 [L218] UGET     A=4 B=0 C=7 D=7 right_scroll
00119 [L218] MOV      A=5 B=0 C=4 D=4 
00120 [L218] TGETS    A=4 B=4 C=9 D=1033 'runAction'
00121 [L218] UGET     A=6 B=0 C=6 D=6 CCSequence
00122 [L218] MOV      A=7 B=0 C=6 D=6 
00123 [L218] TGETS    A=6 B=6 C=3 D=1539 'create'
00124 [L218] MOV      A=8 B=0 C=2 D=2 
00125 [L218] CALL     A=6 B=0 C=3 D=3 
00126 [L218] CALLM    A=4 B=1 C=1 D=257 
00127 [L220] UGET     A=2 B=0 C=8 D=8 paper_bkg
00128 [L220] ISF      A=0 B=0 C=2 D=2 
00129 [L220] JMP      A=3 B=128 C=64 D=32832 target=194
00130 [L221] UGET     A=2 B=0 C=2 D=2 CCArray
00131 [L221] MOV      A=3 B=0 C=2 D=2 
00132 [L221] TGETS    A=2 B=2 C=3 D=515 'create'
00133 [L221] CALL     A=2 B=2 C=2 D=514 
00134 [L222] UGET     A=3 B=0 C=9 D=9 CCScaleBy
00135 [L222] MOV      A=4 B=0 C=3 D=3 
00136 [L222] TGETS    A=3 B=3 C=3 D=771 'create'
00137 [L222] MOV      A=5 B=0 C=0 D=0 
00138 [L222] KNUM     A=6 B=0 C=3 D=3 0.02
00139 [L222] KSHORT   A=7 B=0 C=1 D=1 1
00140 [L222] CALL     A=3 B=2 C=5 D=517 
00141 [L223] MOV      A=5 B=0 C=2 D=2 
00142 [L223] TGETS    A=4 B=2 C=7 D=519 'addObject'
00143 [L223] UGET     A=6 B=0 C=4 D=4 CCEaseOut
00144 [L223] MOV      A=7 B=0 C=6 D=6 
00145 [L223] TGETS    A=6 B=6 C=3 D=1539 'create'
00146 [L223] MOV      A=8 B=0 C=3 D=3 
00147 [L223] KSHORT   A=9 B=0 C=3 D=3 3
00148 [L223] CALL     A=6 B=0 C=4 D=4 
00149 [L223] CALLM    A=4 B=1 C=1 D=257 
00150 [L224] MOV      A=5 B=0 C=2 D=2 
00151 [L224] TGETS    A=4 B=2 C=7 D=519 'addObject'
00152 [L224] UGET     A=6 B=0 C=5 D=5 CCDelayTime
00153 [L224] MOV      A=7 B=0 C=6 D=6 
00154 [L224] TGETS    A=6 B=6 C=3 D=1539 'create'
00155 [L224] MOV      A=8 B=0 C=1 D=1 
00156 [L224] CALL     A=6 B=0 C=3 D=3 
00157 [L224] CALLM    A=4 B=1 C=1 D=257 
00158 [L225] MOV      A=5 B=0 C=2 D=2 
00159 [L225] TGETS    A=4 B=2 C=7 D=519 'addObject'
00160 [L225] UGET     A=6 B=0 C=4 D=4 CCEaseOut
00161 [L225] MOV      A=7 B=0 C=6 D=6 
00162 [L225] TGETS    A=6 B=6 C=3 D=1539 'create'
00163 [L225] MOV      A=9 B=0 C=3 D=3 
00164 [L225] TGETS    A=8 B=3 C=8 D=776 'reverse'
00165 [L225] CALL     A=8 B=2 C=2 D=514 
00166 [L225] KSHORT   A=9 B=0 C=3 D=3 3
00167 [L225] CALL     A=6 B=0 C=4 D=4 
00168 [L225] CALLM    A=4 B=1 C=1 D=257 
00169 [L226] MOV      A=5 B=0 C=2 D=2 
00170 [L226] TGETS    A=4 B=2 C=7 D=519 'addObject'
00171 [L226] UGET     A=6 B=0 C=5 D=5 CCDelayTime
00172 [L226] MOV      A=7 B=0 C=6 D=6 
00173 [L226] TGETS    A=6 B=6 C=3 D=1539 'create'
00174 [L226] MULVN    A=8 B=1 C=4 D=260 
00175 [L226] CALL     A=6 B=0 C=3 D=3 
00176 [L226] CALLM    A=4 B=1 C=1 D=257 
00177 [L227] MOV      A=5 B=0 C=2 D=2 
00178 [L227] TGETS    A=4 B=2 C=7 D=519 'addObject'
00179 [L227] UGET     A=6 B=0 C=10 D=10 CCCallFuncN
00180 [L227] MOV      A=7 B=0 C=6 D=6 
00181 [L227] TGETS    A=6 B=6 C=3 D=1539 'create'
00182 [L227] GGET     A=8 B=0 C=10 D=10 'createExchangeLayer'
00183 [L227] CALL     A=6 B=0 C=3 D=3 
00184 [L227] CALLM    A=4 B=1 C=1 D=257 
00185 [L228] UGET     A=4 B=0 C=8 D=8 paper_bkg
00186 [L228] MOV      A=5 B=0 C=4 D=4 
00187 [L228] TGETS    A=4 B=4 C=9 D=1033 'runAction'
00188 [L228] UGET     A=6 B=0 C=6 D=6 CCSequence
00189 [L228] MOV      A=7 B=0 C=6 D=6 
00190 [L228] TGETS    A=6 B=6 C=3 D=1539 'create'
00191 [L228] MOV      A=8 B=0 C=2 D=2 
00192 [L228] CALL     A=6 B=0 C=3 D=3 
00193 [L228] CALLM    A=4 B=1 C=1 D=257 
00194 [L232] FNEW     A=2 B=0 C=11 D=11 {'kind': 'proto', 'id': 0}
00195 [L233] UGET     A=3 B=0 C=11 D=11 introduce
00196 [L233] ISF      A=0 B=0 C=3 D=3 
00197 [L233] JMP      A=4 B=128 C=37 D=32805 target=235
00198 [L234] UGET     A=3 B=0 C=2 D=2 CCArray
00199 [L234] MOV      A=4 B=0 C=3 D=3 
00200 [L234] TGETS    A=3 B=3 C=3 D=771 'create'
00201 [L234] CALL     A=3 B=2 C=2 D=514 
00202 [L235] UGET     A=4 B=0 C=9 D=9 CCScaleBy
00203 [L235] MOV      A=5 B=0 C=4 D=4 
00204 [L235] TGETS    A=4 B=4 C=3 D=1027 'create'
00205 [L235] MOV      A=6 B=0 C=0 D=0 
00206 [L235] KNUM     A=7 B=0 C=3 D=3 0.02
00207 [L235] KSHORT   A=8 B=0 C=1 D=1 1
00208 [L235] CALL     A=4 B=2 C=5 D=517 
00209 [L236] MOV      A=6 B=0 C=3 D=3 
00210 [L236] TGETS    A=5 B=3 C=7 D=775 'addObject'
00211 [L236] UGET     A=7 B=0 C=4 D=4 CCEaseOut
00212 [L236] MOV      A=8 B=0 C=7 D=7 
00213 [L236] TGETS    A=7 B=7 C=3 D=1795 'create'
00214 [L236] MOV      A=9 B=0 C=4 D=4 
00215 [L236] KSHORT   A=10 B=0 C=3 D=3 3
00216 [L236] CALL     A=7 B=0 C=4 D=4 
00217 [L236] CALLM    A=5 B=1 C=1 D=257 
00218 [L237] MOV      A=6 B=0 C=3 D=3 
00219 [L237] TGETS    A=5 B=3 C=7 D=775 'addObject'
00220 [L237] UGET     A=7 B=0 C=10 D=10 CCCallFuncN
00221 [L237] MOV      A=8 B=0 C=7 D=7 
00222 [L237] TGETS    A=7 B=7 C=3 D=1795 'create'
00223 [L237] MOV      A=9 B=0 C=2 D=2 
00224 [L237] CALL     A=7 B=0 C=3 D=3 
00225 [L237] CALLM    A=5 B=1 C=1 D=257 
00226 [L238] UGET     A=5 B=0 C=11 D=11 introduce
00227 [L238] MOV      A=6 B=0 C=5 D=5 
00228 [L238] TGETS    A=5 B=5 C=9 D=1289 'runAction'
00229 [L238] UGET     A=7 B=0 C=6 D=6 CCSequence
00230 [L238] MOV      A=8 B=0 C=7 D=7 
00231 [L238] TGETS    A=7 B=7 C=3 D=1795 'create'
00232 [L238] MOV      A=9 B=0 C=3 D=3 
00233 [L238] CALL     A=7 B=0 C=3 D=3 
00234 [L238] CALLM    A=5 B=1 C=1 D=257 
00235 [L240] RET0     A=0 B=0 C=1 D=1 

FUNCTION proto2 offset=0x6d8 source_lines=180-249 params=0
UPVALUES ['CCArray', 'CCMoveBy', 'CCEaseOut', 'CCDelayTime', 'CCSequence', 'CCScaleBy', 'CCCallFuncN']
00001 [L182] GGET     A=0 B=0 C=0 D=0 'd_ms'
00002 [L182] TGETS    A=0 B=0 C=1 D=1 'd_u'
00003 [L182] TGETS    A=0 B=0 C=2 D=2 'createByStyles'
00004 [L182] TDUP     A=1 B=0 C=3 D=3 {'kind': 'table', 'value': {'pic': 'v2/CardUI/scroll_left.png', 'scaleY': 0.865}}
00005 [L182] GGET     A=2 B=0 C=4 D=4 'g_self'
00006 [L182] TGETS    A=2 B=2 C=5 D=517 'left_x'
00007 [L182] TSETS    A=2 B=1 C=6 D=262 'x'
00008 [L182] GGET     A=2 B=0 C=4 D=4 'g_self'
00009 [L182] TGETS    A=2 B=2 C=7 D=519 'center_y'
00010 [L182] TSETS    A=2 B=1 C=8 D=264 'y'
00011 [L182] CALL     A=0 B=2 C=2 D=514 
00012 [L183] GGET     A=1 B=0 C=9 D=9 'g_cardUI'
00013 [L183] TGETS    A=1 B=1 C=10 D=266 'main_layer'
00014 [L183] MOV      A=2 B=0 C=1 D=1 
00015 [L183] TGETS    A=1 B=1 C=11 D=267 'addChild'
00016 [L183] MOV      A=3 B=0 C=0 D=0 
00017 [L183] KSHORT   A=4 B=0 C=10 D=10 10
00018 [L183] CALL     A=1 B=1 C=4 D=260 
00019 [L185] GGET     A=1 B=0 C=0 D=0 'd_ms'
00020 [L185] TGETS    A=1 B=1 C=1 D=257 'd_u'
00021 [L185] TGETS    A=1 B=1 C=2 D=258 'createByStyles'
00022 [L185] TDUP     A=2 B=0 C=12 D=12 {'kind': 'table', 'value': {'scaleY': 0.865, 'pic': 'v2/CardUI/scroll_left.png', 'FlipX': True}}
00023 [L185] GGET     A=3 B=0 C=4 D=4 'g_self'
00024 [L185] TGETS    A=3 B=3 C=5 D=773 'left_x'
00025 [L185] SUBNV    A=3 B=3 C=0 D=768 
00026 [L185] TSETS    A=3 B=2 C=6 D=518 'x'
00027 [L185] GGET     A=3 B=0 C=4 D=4 'g_self'
00028 [L185] TGETS    A=3 B=3 C=7 D=775 'center_y'
00029 [L185] TSETS    A=3 B=2 C=8 D=520 'y'
00030 [L185] CALL     A=1 B=2 C=2 D=514 
00031 [L186] GGET     A=2 B=0 C=9 D=9 'g_cardUI'
00032 [L186] TGETS    A=2 B=2 C=10 D=522 'main_layer'
00033 [L186] MOV      A=3 B=0 C=2 D=2 
00034 [L186] TGETS    A=2 B=2 C=11 D=523 'addChild'
00035 [L186] MOV      A=4 B=0 C=1 D=1 
00036 [L186] KSHORT   A=5 B=0 C=10 D=10 10
00037 [L186] CALL     A=2 B=1 C=4 D=260 
00038 [L188] GGET     A=2 B=0 C=0 D=0 'd_ms'
00039 [L188] TGETS    A=2 B=2 C=1 D=513 'd_u'
00040 [L188] TGETS    A=2 B=2 C=2 D=514 'createByStyles'
00041 [L188] TDUP     A=3 B=0 C=13 D=13 {'kind': 'table', 'value': {'x': 0.5, 'pic': 'v2/CardUI/scroll_bkg1.png', 'scaleY': 0.768}}
00042 [L188] GGET     A=4 B=0 C=4 D=4 'g_self'
00043 [L188] TGETS    A=4 B=4 C=7 D=1031 'center_y'
00044 [L188] TSETS    A=4 B=3 C=8 D=776 'y'
00045 [L188] CALL     A=2 B=2 C=2 D=514 
00046 [L189] GGET     A=3 B=0 C=9 D=9 'g_cardUI'
00047 [L189] TGETS    A=3 B=3 C=10 D=778 'main_layer'
00048 [L189] MOV      A=4 B=0 C=3 D=3 
00049 [L189] TGETS    A=3 B=3 C=11 D=779 'addChild'
00050 [L189] MOV      A=5 B=0 C=2 D=2 
00051 [L189] KSHORT   A=6 B=0 C=1 D=1 1
00052 [L189] CALL     A=3 B=1 C=4 D=260 
00053 [L191] GGET     A=3 B=0 C=0 D=0 'd_ms'
00054 [L191] TGETS    A=3 B=3 C=1 D=769 'd_u'
00055 [L191] TGETS    A=3 B=3 C=2 D=770 'createByStyles'
00056 [L191] TDUP     A=4 B=0 C=14 D=14 {'kind': 'table', 'value': {'x': 0.5, 'pic': 'v2/CardUI/scroll_bkg2.png', 'scaleY': 0.768}}
00057 [L191] GGET     A=5 B=0 C=4 D=4 'g_self'
00058 [L191] TGETS    A=5 B=5 C=7 D=1287 'center_y'
00059 [L191] TSETS    A=5 B=4 C=8 D=1032 'y'
00060 [L191] CALL     A=3 B=2 C=2 D=514 
00061 [L192] GGET     A=4 B=0 C=9 D=9 'g_cardUI'
00062 [L192] TGETS    A=4 B=4 C=10 D=1034 'main_layer'
00063 [L192] MOV      A=5 B=0 C=4 D=4 
00064 [L192] TGETS    A=4 B=4 C=11 D=1035 'addChild'
00065 [L192] MOV      A=6 B=0 C=3 D=3 
00066 [L192] KSHORT   A=7 B=0 C=2 D=2 2
00067 [L192] CALL     A=4 B=1 C=4 D=260 
00068 [L194] TNEW     A=4 B=0 C=0 D=0 
00069 [L240] FNEW     A=5 B=0 C=15 D=15 {'kind': 'proto', 'id': 1}
00070 [L242] TDUP     A=6 B=0 C=16 D=16 {'kind': 'table', 'value': {'x': 0, 'y': 0}}
00071 [L245] TDUP     A=7 B=0 C=17 D=17 {'kind': 'table', 'value': {'spic': 'v2/CardUI/exchange2.png', 'x': 0.5, 'npic': 'v2/CardUI/exchange1.png', 'y': 0.118}}
00072 [L246] TSETS    A=5 B=7 C=18 D=1810 'call_back'
00073 [L246] TSETB    A=7 B=6 C=1 D=1537 
00074 [L248] GGET     A=7 B=0 C=9 D=9 'g_cardUI'
00075 [L248] TGETS    A=7 B=7 C=10 D=1802 'main_layer'
00076 [L248] MOV      A=8 B=0 C=7 D=7 
00077 [L248] TGETS    A=7 B=7 C=11 D=1803 'addChild'
00078 [L248] GGET     A=9 B=0 C=0 D=0 'd_ms'
00079 [L248] TGETS    A=9 B=9 C=1 D=2305 'd_u'
00080 [L248] TGETS    A=9 B=9 C=19 D=2323 'createMenu'
00081 [L248] MOV      A=10 B=0 C=6 D=6 
00082 [L248] MOV      A=11 B=0 C=4 D=4 
00083 [L248] CALL     A=9 B=2 C=3 D=515 
00084 [L248] KSHORT   A=10 B=0 C=3 D=3 3
00085 [L248] CALL     A=7 B=1 C=4 D=260 
00086 [L249] UCLO     A=0 B=128 C=0 D=32768 target=87
00087 [L249] RET0     A=0 B=0 C=1 D=1 
