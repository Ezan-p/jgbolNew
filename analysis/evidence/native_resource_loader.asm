
jgbol3.87/lib/armeabi/libxiyoujilua.so:	file format elf32-littlearm

Disassembly of section .text:

00192744 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)>:
  192744: b5f0         	push	{r4, r5, r6, r7, lr}
  192746: 4657         	mov	r7, r10
  192748: 464e         	mov	r6, r9
  19274a: 4645         	mov	r5, r8
  19274c: b4e0         	push	{r5, r6, r7}
  19274e: 4cae         	ldr	r4, [pc, #0x2b8]        @ 0x192a08 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x2c4>
  192750: b08e         	sub	sp, #0x38
  192752: 1c17         	adds	r7, r2, #0x0
  192754: 4680         	mov	r8, r0
  192756: 466a         	mov	r2, sp
  192758: a80b         	add	r0, sp, #0x2c
  19275a: 447c         	add	r4, pc
  19275c: 1c0d         	adds	r5, r1, #0x0
  19275e: 1c1e         	adds	r6, r3, #0x0
  192760: f200 ea7a    	blx	0x392c58 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x25684> @ imm = #0x2004f4
  192764: 2f00         	cmp	r7, #0x0
  192766: d100         	bne	0x19276a <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x26> @ imm = #0x0
  192768: e107         	b	0x19297a <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x236> @ imm = #0x20e
  19276a: 2d00         	cmp	r5, #0x0
  19276c: d100         	bne	0x192770 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x2c> @ imm = #0x0
  19276e: e104         	b	0x19297a <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x236> @ imm = #0x208
  192770: 782b         	ldrb	r3, [r5]
  192772: 2b2f         	cmp	r3, #0x2f
  192774: d100         	bne	0x192778 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x34> @ imm = #0x0
  192776: e086         	b	0x192886 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x142> @ imm = #0x10c
  192778: 2308         	movs	r3, #0x8
  19277a: 4699         	mov	r9, r3
  19277c: 44c1         	add	r9, r8
  19277e: 4648         	mov	r0, r9
  192780: a90b         	add	r1, sp, #0x2c
  192782: f770 fdc9    	bl	0x103318 <std::_Rb_tree<std::string, std::pair<std::string const, std::string>, std::_Select1st<std::pair<std::string const, std::string>>, std::less<std::string>, std::allocator<std::pair<std::string const, std::string>>>::find(std::string const&)> @ imm = #-0x8f46e
  192786: 4643         	mov	r3, r8
  192788: 330c         	adds	r3, #0xc
  19278a: 4283         	cmp	r3, r0
  19278c: d100         	bne	0x192790 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x4c> @ imm = #0x0
  19278e: e0f8         	b	0x192982 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x23e> @ imm = #0x1f0
  192790: a80c         	add	r0, sp, #0x30
  192792: 4641         	mov	r1, r8
  192794: f7ff fbe4    	bl	0x191f60 <cocos2d::CCFileUtils::getWriteablePath()> @ imm = #-0x838
  192798: 499c         	ldr	r1, [pc, #0x270]        @ 0x192a0c <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x2c8>
  19279a: 220a         	movs	r2, #0xa
  19279c: a80c         	add	r0, sp, #0x30
  19279e: 4479         	add	r1, pc
  1927a0: f1ff edfc    	blx	0x39239c <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x24dc8> @ imm = #0x1ffbf8
  1927a4: a90b         	add	r1, sp, #0x2c
  1927a6: 4648         	mov	r0, r9
  1927a8: f771 fbbe    	bl	0x103f28 <std::map<std::string, std::string, std::less<std::string>, std::allocator<std::pair<std::string const, std::string>>>::operator[](std::string const&)> @ imm = #-0x8e884
  1927ac: 1c01         	adds	r1, r0, #0x0
  1927ae: a80c         	add	r0, sp, #0x30
  1927b0: f1ff ef18    	blx	0x3925e4 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x25010> @ imm = #0x1ffe30
  1927b4: 1c39         	adds	r1, r7, #0x0
  1927b6: 980c         	ldr	r0, [sp, #0x30]
  1927b8: f75c ec62    	blx	0xef080 <.plt+0x6c8>    @ imm = #-0xa373c
  1927bc: 1e07         	subs	r7, r0, #0x0
  1927be: d024         	beq	0x19280a <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0xc6> @ imm = #0x48
  1927c0: 2100         	movs	r1, #0x0
  1927c2: 2202         	movs	r2, #0x2
  1927c4: 1c38         	adds	r0, r7, #0x0
  1927c6: f75c ee7e    	blx	0xef4c4 <.plt+0xb0c>    @ imm = #-0xa3304
  1927ca: 1c38         	adds	r0, r7, #0x0
  1927cc: f75c ef76    	blx	0xef6bc <.plt+0xd04>    @ imm = #-0xa3114
  1927d0: 2100         	movs	r1, #0x0
  1927d2: 4682         	mov	r10, r0
  1927d4: 2200         	movs	r2, #0x0
  1927d6: 1c38         	adds	r0, r7, #0x0
  1927d8: f75c ee74    	blx	0xef4c4 <.plt+0xb0c>    @ imm = #-0xa3318
  1927dc: 4650         	mov	r0, r10
  1927de: f214 ee4c    	blx	0x3a7478 <operator new[](unsigned int)> @ imm = #0x214c98
  1927e2: 4652         	mov	r2, r10
  1927e4: 2101         	movs	r1, #0x1
  1927e6: 1c3b         	adds	r3, r7, #0x0
  1927e8: 1c05         	adds	r5, r0, #0x0
  1927ea: f75c ec38    	blx	0xef05c <.plt+0x6a4>    @ imm = #-0xa3790
  1927ee: 4682         	mov	r10, r0
  1927f0: 1c38         	adds	r0, r7, #0x0
  1927f2: f75c ec22    	blx	0xef038 <.plt+0x680>    @ imm = #-0xa37bc
  1927f6: 2e00         	cmp	r6, #0x0
  1927f8: d001         	beq	0x1927fe <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0xba> @ imm = #0x2
  1927fa: 4653         	mov	r3, r10
  1927fc: 6033         	str	r3, [r6]
  1927fe: 2d00         	cmp	r5, #0x0
  192800: d003         	beq	0x19280a <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0xc6> @ imm = #0x6
  192802: 6833         	ldr	r3, [r6]
  192804: 2b00         	cmp	r3, #0x0
  192806: d000         	beq	0x19280a <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0xc6> @ imm = #0x0
  192808: e0a2         	b	0x192950 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x20c> @ imm = #0x144
  19280a: 4b81         	ldr	r3, [pc, #0x204]        @ 0x192a10 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x2cc>
  19280c: 980c         	ldr	r0, [sp, #0x30]
  19280e: 58e4         	ldr	r4, [r4, r3]
  192810: 1c05         	adds	r5, r0, #0x0
  192812: 3d0c         	subs	r5, #0xc
  192814: 42a5         	cmp	r5, r4
  192816: d000         	beq	0x19281a <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0xd6> @ imm = #0x0
  192818: e0dd         	b	0x1929d6 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x292> @ imm = #0x1ba
  19281a: 497e         	ldr	r1, [pc, #0x1f8]        @ 0x192a14 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x2d0>
  19281c: aa01         	add	r2, sp, #0x4
  19281e: a80c         	add	r0, sp, #0x30
  192820: 4479         	add	r1, pc
  192822: f200 ea1a    	blx	0x392c58 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x25684> @ imm = #0x200434
  192826: a90b         	add	r1, sp, #0x2c
  192828: 4648         	mov	r0, r9
  19282a: f771 fb7d    	bl	0x103f28 <std::map<std::string, std::string, std::less<std::string>, std::allocator<std::pair<std::string const, std::string>>>::operator[](std::string const&)> @ imm = #-0x8e906
  19282e: 1c01         	adds	r1, r0, #0x0
  192830: a80c         	add	r0, sp, #0x30
  192832: f1ff eed8    	blx	0x3925e4 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x25010> @ imm = #0x1ffdb0
  192836: a80b         	add	r0, sp, #0x2c
  192838: a90c         	add	r1, sp, #0x30
  19283a: f1ff efa8    	blx	0x39278c <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x251b8> @ imm = #0x1fff50
  19283e: 980c         	ldr	r0, [sp, #0x30]
  192840: 1c05         	adds	r5, r0, #0x0
  192842: 3d0c         	subs	r5, #0xc
  192844: 42a5         	cmp	r5, r4
  192846: d000         	beq	0x19284a <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x106> @ imm = #0x0
  192848: e0ab         	b	0x1929a2 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x25e> @ imm = #0x156
  19284a: a90b         	add	r1, sp, #0x2c
  19284c: a80d         	add	r0, sp, #0x34
  19284e: f1ff ef6a    	blx	0x392724 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x25150> @ imm = #0x1ffed4
  192852: 1c31         	adds	r1, r6, #0x0
  192854: a80d         	add	r0, sp, #0x34
  192856: f7ff faf9    	bl	0x191e4c <cocos2d::readFileFromAssets(std::string const&, unsigned long*)> @ imm = #-0xa0e
  19285a: 1c05         	adds	r5, r0, #0x0
  19285c: 980d         	ldr	r0, [sp, #0x34]
  19285e: 1c06         	adds	r6, r0, #0x0
  192860: 3e0c         	subs	r6, #0xc
  192862: 42a6         	cmp	r6, r4
  192864: d000         	beq	0x192868 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x124> @ imm = #0x0
  192866: e0a9         	b	0x1929bc <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x278> @ imm = #0x152
  192868: 2d00         	cmp	r5, #0x0
  19286a: d036         	beq	0x1928da <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x196> @ imm = #0x6c
  19286c: 980b         	ldr	r0, [sp, #0x2c]
  19286e: 1c06         	adds	r6, r0, #0x0
  192870: 3e0c         	subs	r6, #0xc
  192872: 42a6         	cmp	r6, r4
  192874: d000         	beq	0x192878 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x134> @ imm = #0x0
  192876: e087         	b	0x192988 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x244> @ imm = #0x10e
  192878: b00e         	add	sp, #0x38
  19287a: 1c28         	adds	r0, r5, #0x0
  19287c: bc1c         	pop	{r2, r3, r4}
  19287e: 4690         	mov	r8, r2
  192880: 4699         	mov	r9, r3
  192882: 46a2         	mov	r10, r4
  192884: bdf0         	pop	{r4, r5, r6, r7, pc}
  192886: 1c39         	adds	r1, r7, #0x0
  192888: 1c28         	adds	r0, r5, #0x0
  19288a: f75c ebfa    	blx	0xef080 <.plt+0x6c8>    @ imm = #-0xa380c
  19288e: 1e07         	subs	r7, r0, #0x0
  192890: d021         	beq	0x1928d6 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x192> @ imm = #0x42
  192892: 2100         	movs	r1, #0x0
  192894: 2202         	movs	r2, #0x2
  192896: 1c38         	adds	r0, r7, #0x0
  192898: f75c ee14    	blx	0xef4c4 <.plt+0xb0c>    @ imm = #-0xa33d8
  19289c: 1c38         	adds	r0, r7, #0x0
  19289e: f75c ef0e    	blx	0xef6bc <.plt+0xd04>    @ imm = #-0xa31e4
  1928a2: 2100         	movs	r1, #0x0
  1928a4: 4681         	mov	r9, r0
  1928a6: 2200         	movs	r2, #0x0
  1928a8: 1c38         	adds	r0, r7, #0x0
  1928aa: f75c ee0c    	blx	0xef4c4 <.plt+0xb0c>    @ imm = #-0xa33e8
  1928ae: 4648         	mov	r0, r9
  1928b0: f214 ede2    	blx	0x3a7478 <operator new[](unsigned int)> @ imm = #0x214bc4
  1928b4: 464a         	mov	r2, r9
  1928b6: 2101         	movs	r1, #0x1
  1928b8: 1c3b         	adds	r3, r7, #0x0
  1928ba: 1c05         	adds	r5, r0, #0x0
  1928bc: f75c ebce    	blx	0xef05c <.plt+0x6a4>    @ imm = #-0xa3864
  1928c0: 4681         	mov	r9, r0
  1928c2: 1c38         	adds	r0, r7, #0x0
  1928c4: f75c ebb8    	blx	0xef038 <.plt+0x680>    @ imm = #-0xa3890
  1928c8: 2e00         	cmp	r6, #0x0
  1928ca: d001         	beq	0x1928d0 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x18c> @ imm = #0x2
  1928cc: 464b         	mov	r3, r9
  1928ce: 6033         	str	r3, [r6]
  1928d0: 4b4f         	ldr	r3, [pc, #0x13c]        @ 0x192a10 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x2cc>
  1928d2: 58e4         	ldr	r4, [r4, r3]
  1928d4: e7c8         	b	0x192868 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x124> @ imm = #-0x70
  1928d6: 4b4e         	ldr	r3, [pc, #0x138]        @ 0x192a10 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x2cc>
  1928d8: 58e4         	ldr	r4, [r4, r3]
  1928da: 4640         	mov	r0, r8
  1928dc: f7ff faa4    	bl	0x191e28 <cocos2d::CCFileUtils::isPopupNotify()> @ imm = #-0xab8
  1928e0: 2500         	movs	r5, #0x0
  1928e2: 2800         	cmp	r0, #0x0
  1928e4: d0c2         	beq	0x19286c <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x128> @ imm = #-0x7c
  1928e6: 494c         	ldr	r1, [pc, #0x130]        @ 0x192a18 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x2d4>
  1928e8: aa02         	add	r2, sp, #0x8
  1928ea: a80c         	add	r0, sp, #0x30
  1928ec: 4479         	add	r1, pc
  1928ee: f200 e9b4    	blx	0x392c58 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x25684> @ imm = #0x200368
  1928f2: 494a         	ldr	r1, [pc, #0x128]        @ 0x192a1c <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x2d8>
  1928f4: aa03         	add	r2, sp, #0xc
  1928f6: a80d         	add	r0, sp, #0x34
  1928f8: 4479         	add	r1, pc
  1928fa: f200 e9ae    	blx	0x392c58 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x25684> @ imm = #0x20035c
  1928fe: 9d0b         	ldr	r5, [sp, #0x2c]
  192900: 1c28         	adds	r0, r5, #0x0
  192902: f75c ea5c    	blx	0xeedbc <.plt+0x404>    @ imm = #-0xa3b48
  192906: 1c29         	adds	r1, r5, #0x0
  192908: 1c02         	adds	r2, r0, #0x0
  19290a: a80d         	add	r0, sp, #0x34
  19290c: f1ff ed46    	blx	0x39239c <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x24dc8> @ imm = #0x1ffa8c
  192910: 4943         	ldr	r1, [pc, #0x10c]        @ 0x192a20 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x2dc>
  192912: 2209         	movs	r2, #0x9
  192914: 4479         	add	r1, pc
  192916: f1ff ed42    	blx	0x39239c <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x24dc8> @ imm = #0x1ffa84
  19291a: 980d         	ldr	r0, [sp, #0x34]
  19291c: f7fe ff2c    	bl	0x191778 <cocos2d::CCLog(char const*, ...)> @ imm = #-0x11a8
  192920: 980d         	ldr	r0, [sp, #0x34]
  192922: 1c05         	adds	r5, r0, #0x0
  192924: 3d0c         	subs	r5, #0xc
  192926: 42a5         	cmp	r5, r4
  192928: d162         	bne	0x1929f0 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x2ac> @ imm = #0xc4
  19292a: 980c         	ldr	r0, [sp, #0x30]
  19292c: 2500         	movs	r5, #0x0
  19292e: 1c06         	adds	r6, r0, #0x0
  192930: 3e0c         	subs	r6, #0xc
  192932: 42a6         	cmp	r6, r4
  192934: d09a         	beq	0x19286c <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x128> @ imm = #-0xcc
  192936: 2101         	movs	r1, #0x1
  192938: 3804         	subs	r0, #0x4
  19293a: 4249         	rsbs	r1, r1, #0
  19293c: f222 ed5a    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x222ab4
  192940: 42a8         	cmp	r0, r5
  192942: dd00         	ble	0x192946 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x202> @ imm = #0x0
  192944: e792         	b	0x19286c <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x128> @ imm = #-0xdc
  192946: 1c30         	adds	r0, r6, #0x0
  192948: a909         	add	r1, sp, #0x24
  19294a: f1fe ee1c    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1fec38
  19294e: e78d         	b	0x19286c <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x128> @ imm = #-0xe6
  192950: 4b2f         	ldr	r3, [pc, #0xbc]         @ 0x192a10 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x2cc>
  192952: 980c         	ldr	r0, [sp, #0x30]
  192954: 58e4         	ldr	r4, [r4, r3]
  192956: 1c06         	adds	r6, r0, #0x0
  192958: 3e0c         	subs	r6, #0xc
  19295a: 42a6         	cmp	r6, r4
  19295c: d100         	bne	0x192960 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x21c> @ imm = #0x0
  19295e: e785         	b	0x19286c <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x128> @ imm = #-0xf6
  192960: 2101         	movs	r1, #0x1
  192962: 3804         	subs	r0, #0x4
  192964: 4249         	rsbs	r1, r1, #0
  192966: f222 ed46    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x222a8c
  19296a: 2800         	cmp	r0, #0x0
  19296c: dd00         	ble	0x192970 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x22c> @ imm = #0x0
  19296e: e77d         	b	0x19286c <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x128> @ imm = #-0x106
  192970: 1c30         	adds	r0, r6, #0x0
  192972: a904         	add	r1, sp, #0x10
  192974: f1fe ee06    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1fec0c
  192978: e778         	b	0x19286c <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x128> @ imm = #-0x110
  19297a: 4b25         	ldr	r3, [pc, #0x94]         @ 0x192a10 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x2cc>
  19297c: 2500         	movs	r5, #0x0
  19297e: 58e4         	ldr	r4, [r4, r3]
  192980: e774         	b	0x19286c <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x128> @ imm = #-0x118
  192982: 4b23         	ldr	r3, [pc, #0x8c]         @ 0x192a10 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x2cc>
  192984: 58e4         	ldr	r4, [r4, r3]
  192986: e760         	b	0x19284a <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x106> @ imm = #-0x140
  192988: 2101         	movs	r1, #0x1
  19298a: 3804         	subs	r0, #0x4
  19298c: 4249         	rsbs	r1, r1, #0
  19298e: f222 ed32    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x222a64
  192992: 2800         	cmp	r0, #0x0
  192994: dd00         	ble	0x192998 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x254> @ imm = #0x0
  192996: e76f         	b	0x192878 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x134> @ imm = #-0x122
  192998: 1c30         	adds	r0, r6, #0x0
  19299a: a90a         	add	r1, sp, #0x28
  19299c: f1fe edf2    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1febe4
  1929a0: e76a         	b	0x192878 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x134> @ imm = #-0x12c
  1929a2: 2101         	movs	r1, #0x1
  1929a4: 3804         	subs	r0, #0x4
  1929a6: 4249         	rsbs	r1, r1, #0
  1929a8: f222 ed24    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x222a48
  1929ac: 2800         	cmp	r0, #0x0
  1929ae: dd00         	ble	0x1929b2 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x26e> @ imm = #0x0
  1929b0: e74b         	b	0x19284a <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x106> @ imm = #-0x16a
  1929b2: 1c28         	adds	r0, r5, #0x0
  1929b4: a906         	add	r1, sp, #0x18
  1929b6: f1fe ede6    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1febcc
  1929ba: e746         	b	0x19284a <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x106> @ imm = #-0x174
  1929bc: 2101         	movs	r1, #0x1
  1929be: 3804         	subs	r0, #0x4
  1929c0: 4249         	rsbs	r1, r1, #0
  1929c2: f222 ed18    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x222a30
  1929c6: 2800         	cmp	r0, #0x0
  1929c8: dd00         	ble	0x1929cc <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x288> @ imm = #0x0
  1929ca: e74d         	b	0x192868 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x124> @ imm = #-0x166
  1929cc: 1c30         	adds	r0, r6, #0x0
  1929ce: a907         	add	r1, sp, #0x1c
  1929d0: f1fe edd8    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1febb0
  1929d4: e748         	b	0x192868 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x124> @ imm = #-0x170
  1929d6: 2101         	movs	r1, #0x1
  1929d8: 3804         	subs	r0, #0x4
  1929da: 4249         	rsbs	r1, r1, #0
  1929dc: f222 ed0a    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x222a14
  1929e0: 2800         	cmp	r0, #0x0
  1929e2: dd00         	ble	0x1929e6 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x2a2> @ imm = #0x0
  1929e4: e719         	b	0x19281a <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0xd6> @ imm = #-0x1ce
  1929e6: 1c28         	adds	r0, r5, #0x0
  1929e8: a905         	add	r1, sp, #0x14
  1929ea: f1fe edcc    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1feb98
  1929ee: e714         	b	0x19281a <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0xd6> @ imm = #-0x1d8
  1929f0: 2101         	movs	r1, #0x1
  1929f2: 3804         	subs	r0, #0x4
  1929f4: 4249         	rsbs	r1, r1, #0
  1929f6: f222 ecfe    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x2229fc
  1929fa: 2800         	cmp	r0, #0x0
  1929fc: dc95         	bgt	0x19292a <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x1e6> @ imm = #-0xd6
  1929fe: 1c28         	adds	r0, r5, #0x0
  192a00: a908         	add	r1, sp, #0x20
  192a02: f1fe edc0    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1feb80
  192a06: e790         	b	0x19292a <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x1e6> @ imm = #-0xe0
  192a08: 9156         	str	r1, [sp, #0x158]
  192a0a: 002f         	movs	r7, r5
  192a0c: 1cbe         	adds	r6, r7, #0x2
  192a0e: 0024         	movs	r4, r4
  192a10: 0cc4         	lsrs	r4, r0, #0x13
  192a12: 0000         	movs	r0, r0
  192a14: 5f90         	ldrsh	r0, [r2, r6]
  192a16: 0022         	movs	r2, r4
  192a18: ae6c         	add	r6, sp, #0x1b0
  192a1a: 0023         	movs	r3, r4
  192a1c: 1b70         	subs	r0, r6, r5
  192a1e: 0024         	movs	r4, r4
  192a20: 1b74         	subs	r4, r6, r5
  192a22: 0024         	movs	r4, r4
