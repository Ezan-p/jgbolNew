
jgbol3.87/lib/armeabi/libxiyoujilua.so:	file format elf32-littlearm

Disassembly of section .text:

0019207c <cocos2d::my_Base64Decode(std::string const&)>:
  19207c: b5f0         	push	{r4, r5, r6, r7, lr}
  19207e: 465f         	mov	r7, r11
  192080: 4656         	mov	r6, r10
  192082: 464d         	mov	r5, r9
  192084: 4644         	mov	r4, r8
  192086: b4f0         	push	{r4, r5, r6, r7}
  192088: 680b         	ldr	r3, [r1]
  19208a: 4682         	mov	r10, r0
  19208c: 4c92         	ldr	r4, [pc, #0x248]        @ 0x1922d8 <cocos2d::my_Base64Decode(std::string const&)+0x25c>
  19208e: 4893         	ldr	r0, [pc, #0x24c]        @ 0x1922dc <cocos2d::my_Base64Decode(std::string const&)+0x260>
  192090: 3b0c         	subs	r3, #0xc
  192092: b091         	sub	sp, #0x44
  192094: 447c         	add	r4, pc
  192096: 4478         	add	r0, pc
  192098: 1c0e         	adds	r6, r1, #0x0
  19209a: 6819         	ldr	r1, [r3]
  19209c: f7ff fb6c    	bl	0x191778 <cocos2d::CCLog(char const*, ...)> @ imm = #-0x928
  1920a0: 1c22         	adds	r2, r4, #0x0
  1920a2: 1d21         	adds	r1, r4, #0x4
  1920a4: 3208         	adds	r2, #0x8
  1920a6: a80a         	add	r0, sp, #0x28
  1920a8: f770 fe4e    	bl	0x102d48 <LuaInterface::recvMsg(lua_State*)+0xdc> @ imm = #-0x8f364
  1920ac: 1c22         	adds	r2, r4, #0x0
  1920ae: 320c         	adds	r2, #0xc
  1920b0: a80b         	add	r0, sp, #0x2c
  1920b2: a90a         	add	r1, sp, #0x28
  1920b4: f770 fe48    	bl	0x102d48 <LuaInterface::recvMsg(lua_State*)+0xdc> @ imm = #-0x8f370
  1920b8: 1c22         	adds	r2, r4, #0x0
  1920ba: 3210         	adds	r2, #0x10
  1920bc: a80c         	add	r0, sp, #0x30
  1920be: a90b         	add	r1, sp, #0x2c
  1920c0: f770 fe42    	bl	0x102d48 <LuaInterface::recvMsg(lua_State*)+0xdc> @ imm = #-0x8f37c
  1920c4: 1c22         	adds	r2, r4, #0x0
  1920c6: 3214         	adds	r2, #0x14
  1920c8: a80d         	add	r0, sp, #0x34
  1920ca: a90c         	add	r1, sp, #0x30
  1920cc: f770 fe3c    	bl	0x102d48 <LuaInterface::recvMsg(lua_State*)+0xdc> @ imm = #-0x8f388
  1920d0: 1c22         	adds	r2, r4, #0x0
  1920d2: 3218         	adds	r2, #0x18
  1920d4: a80e         	add	r0, sp, #0x38
  1920d6: a90d         	add	r1, sp, #0x34
  1920d8: f770 fe36    	bl	0x102d48 <LuaInterface::recvMsg(lua_State*)+0xdc> @ imm = #-0x8f394
  1920dc: 1c22         	adds	r2, r4, #0x0
  1920de: 321c         	adds	r2, #0x1c
  1920e0: a80f         	add	r0, sp, #0x3c
  1920e2: a90e         	add	r1, sp, #0x38
  1920e4: f770 fe30    	bl	0x102d48 <LuaInterface::recvMsg(lua_State*)+0xdc> @ imm = #-0x8f3a0
  1920e8: 1c22         	adds	r2, r4, #0x0
  1920ea: 3220         	adds	r2, #0x20
  1920ec: a809         	add	r0, sp, #0x24
  1920ee: a90f         	add	r1, sp, #0x3c
  1920f0: f770 fe2a    	bl	0x102d48 <LuaInterface::recvMsg(lua_State*)+0xdc> @ imm = #-0x8f3ac
  1920f4: 497a         	ldr	r1, [pc, #0x1e8]        @ 0x1922e0 <cocos2d::my_Base64Decode(std::string const&)+0x264>
  1920f6: 980f         	ldr	r0, [sp, #0x3c]
  1920f8: 4479         	add	r1, pc
  1920fa: 680a         	ldr	r2, [r1]
  1920fc: 1c04         	adds	r4, r0, #0x0
  1920fe: 3c0c         	subs	r4, #0xc
  192100: 9201         	str	r2, [sp, #0x4]
  192102: 4294         	cmp	r4, r2
  192104: d000         	beq	0x192108 <cocos2d::my_Base64Decode(std::string const&)+0x8c> @ imm = #0x0
  192106: e08d         	b	0x192224 <cocos2d::my_Base64Decode(std::string const&)+0x1a8> @ imm = #0x11a
  192108: 980e         	ldr	r0, [sp, #0x38]
  19210a: 9b01         	ldr	r3, [sp, #0x4]
  19210c: 1c04         	adds	r4, r0, #0x0
  19210e: 3c0c         	subs	r4, #0xc
  192110: 429c         	cmp	r4, r3
  192112: d000         	beq	0x192116 <cocos2d::my_Base64Decode(std::string const&)+0x9a> @ imm = #0x0
  192114: e0d3         	b	0x1922be <cocos2d::my_Base64Decode(std::string const&)+0x242> @ imm = #0x1a6
  192116: 980d         	ldr	r0, [sp, #0x34]
  192118: 9901         	ldr	r1, [sp, #0x4]
  19211a: 1c04         	adds	r4, r0, #0x0
  19211c: 3c0c         	subs	r4, #0xc
  19211e: 428c         	cmp	r4, r1
  192120: d000         	beq	0x192124 <cocos2d::my_Base64Decode(std::string const&)+0xa8> @ imm = #0x0
  192122: e0bf         	b	0x1922a4 <cocos2d::my_Base64Decode(std::string const&)+0x228> @ imm = #0x17e
  192124: 980c         	ldr	r0, [sp, #0x30]
  192126: 9a01         	ldr	r2, [sp, #0x4]
  192128: 1c04         	adds	r4, r0, #0x0
  19212a: 3c0c         	subs	r4, #0xc
  19212c: 4294         	cmp	r4, r2
  19212e: d000         	beq	0x192132 <cocos2d::my_Base64Decode(std::string const&)+0xb6> @ imm = #0x0
  192130: e0ab         	b	0x19228a <cocos2d::my_Base64Decode(std::string const&)+0x20e> @ imm = #0x156
  192132: 980b         	ldr	r0, [sp, #0x2c]
  192134: 9b01         	ldr	r3, [sp, #0x4]
  192136: 1c04         	adds	r4, r0, #0x0
  192138: 3c0c         	subs	r4, #0xc
  19213a: 429c         	cmp	r4, r3
  19213c: d000         	beq	0x192140 <cocos2d::my_Base64Decode(std::string const&)+0xc4> @ imm = #0x0
  19213e: e097         	b	0x192270 <cocos2d::my_Base64Decode(std::string const&)+0x1f4> @ imm = #0x12e
  192140: 980a         	ldr	r0, [sp, #0x28]
  192142: 9901         	ldr	r1, [sp, #0x4]
  192144: 1c04         	adds	r4, r0, #0x0
  192146: 3c0c         	subs	r4, #0xc
  192148: 428c         	cmp	r4, r1
  19214a: d000         	beq	0x19214e <cocos2d::my_Base64Decode(std::string const&)+0xd2> @ imm = #0x0
  19214c: e083         	b	0x192256 <cocos2d::my_Base64Decode(std::string const&)+0x1da> @ imm = #0x106
  19214e: 6833         	ldr	r3, [r6]
  192150: 4651         	mov	r1, r10
  192152: 3b0c         	subs	r3, #0xc
  192154: 681a         	ldr	r2, [r3]
  192156: 9b01         	ldr	r3, [sp, #0x4]
  192158: 4690         	mov	r8, r2
  19215a: 330c         	adds	r3, #0xc
  19215c: 600b         	str	r3, [r1]
  19215e: 2a00         	cmp	r2, #0x0
  192160: d052         	beq	0x192208 <cocos2d::my_Base64Decode(std::string const&)+0x18c> @ imm = #0xa4
  192162: 2303         	movs	r3, #0x3
  192164: 2502         	movs	r5, #0x2
  192166: 2400         	movs	r4, #0x0
  192168: 469b         	mov	r11, r3
  19216a: 6833         	ldr	r3, [r6]
  19216c: 2200         	movs	r2, #0x0
  19216e: a809         	add	r0, sp, #0x24
  192170: 5d19         	ldrb	r1, [r3, r4]
  192172: f1fe ee0a    	blx	0x390d88 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x237b4> @ imm = #0x1fec14
  192176: 6833         	ldr	r3, [r6]
  192178: 1c07         	adds	r7, r0, #0x0
  19217a: 2200         	movs	r2, #0x0
  19217c: 191b         	adds	r3, r3, r4
  19217e: 7859         	ldrb	r1, [r3, #0x1]
  192180: a809         	add	r0, sp, #0x24
  192182: f1fe ee02    	blx	0x390d88 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x237b4> @ imm = #0x1fec04
  192186: 0600         	lsls	r0, r0, #0x18
  192188: 0e00         	lsrs	r0, r0, #0x18
  19218a: 1102         	asrs	r2, r0, #0x4
  19218c: 4659         	mov	r1, r11
  19218e: 400a         	ands	r2, r1
  192190: 063f         	lsls	r7, r7, #0x18
  192192: 0dbb         	lsrs	r3, r7, #0x16
  192194: 1c17         	adds	r7, r2, #0x0
  192196: 431f         	orrs	r7, r3
  192198: 063f         	lsls	r7, r7, #0x18
  19219a: 0e3f         	lsrs	r7, r7, #0x18
  19219c: 4681         	mov	r9, r0
  19219e: 2101         	movs	r1, #0x1
  1921a0: 4650         	mov	r0, r10
  1921a2: 1c3a         	adds	r2, r7, #0x0
  1921a4: f200 e86c    	blx	0x392280 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x24cac> @ imm = #0x2000d8
  1921a8: 45a8         	cmp	r8, r5
  1921aa: d915         	bls	0x1921d8 <cocos2d::my_Base64Decode(std::string const&)+0x15c> @ imm = #0x2a
  1921ac: 6833         	ldr	r3, [r6]
  1921ae: 5d59         	ldrb	r1, [r3, r5]
  1921b0: 295f         	cmp	r1, #0x5f
  1921b2: d029         	beq	0x192208 <cocos2d::my_Base64Decode(std::string const&)+0x18c> @ imm = #0x52
  1921b4: 2200         	movs	r2, #0x0
  1921b6: a809         	add	r0, sp, #0x24
  1921b8: f1fe ede6    	blx	0x390d88 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x237b4> @ imm = #0x1febcc
  1921bc: 0607         	lsls	r7, r0, #0x18
  1921be: 0e3f         	lsrs	r7, r7, #0x18
  1921c0: 230f         	movs	r3, #0xf
  1921c2: 4649         	mov	r1, r9
  1921c4: 10ba         	asrs	r2, r7, #0x2
  1921c6: 401a         	ands	r2, r3
  1921c8: 010b         	lsls	r3, r1, #0x4
  1921ca: 431a         	orrs	r2, r3
  1921cc: 0612         	lsls	r2, r2, #0x18
  1921ce: 0e12         	lsrs	r2, r2, #0x18
  1921d0: 4650         	mov	r0, r10
  1921d2: 2101         	movs	r1, #0x1
  1921d4: f200 e854    	blx	0x392280 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x24cac> @ imm = #0x2000a8
  1921d8: 1ce3         	adds	r3, r4, #0x3
  1921da: 4543         	cmp	r3, r8
  1921dc: d210         	bhs	0x192200 <cocos2d::my_Base64Decode(std::string const&)+0x184> @ imm = #0x20
  1921de: 6832         	ldr	r2, [r6]
  1921e0: 5cd1         	ldrb	r1, [r2, r3]
  1921e2: 295f         	cmp	r1, #0x5f
  1921e4: d010         	beq	0x192208 <cocos2d::my_Base64Decode(std::string const&)+0x18c> @ imm = #0x20
  1921e6: 2200         	movs	r2, #0x0
  1921e8: a809         	add	r0, sp, #0x24
  1921ea: f1fe edce    	blx	0x390d88 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x237b4> @ imm = #0x1feb9c
  1921ee: 01bf         	lsls	r7, r7, #0x6
  1921f0: 1c02         	adds	r2, r0, #0x0
  1921f2: 433a         	orrs	r2, r7
  1921f4: 0612         	lsls	r2, r2, #0x18
  1921f6: 0e12         	lsrs	r2, r2, #0x18
  1921f8: 4650         	mov	r0, r10
  1921fa: 2101         	movs	r1, #0x1
  1921fc: f200 e840    	blx	0x392280 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x24cac> @ imm = #0x200080
  192200: 3404         	adds	r4, #0x4
  192202: 3504         	adds	r5, #0x4
  192204: 4544         	cmp	r4, r8
  192206: d3b0         	blo	0x19216a <cocos2d::my_Base64Decode(std::string const&)+0xee> @ imm = #-0xa0
  192208: 9809         	ldr	r0, [sp, #0x24]
  19220a: 9a01         	ldr	r2, [sp, #0x4]
  19220c: 1c04         	adds	r4, r0, #0x0
  19220e: 3c0c         	subs	r4, #0xc
  192210: 4294         	cmp	r4, r2
  192212: d114         	bne	0x19223e <cocos2d::my_Base64Decode(std::string const&)+0x1c2> @ imm = #0x28
  192214: b011         	add	sp, #0x44
  192216: 4650         	mov	r0, r10
  192218: bc3c         	pop	{r2, r3, r4, r5}
  19221a: 4690         	mov	r8, r2
  19221c: 4699         	mov	r9, r3
  19221e: 46a2         	mov	r10, r4
  192220: 46ab         	mov	r11, r5
  192222: bdf0         	pop	{r4, r5, r6, r7, pc}
  192224: 2101         	movs	r1, #0x1
  192226: 3804         	subs	r0, #0x4
  192228: 4249         	rsbs	r1, r1, #0
  19222a: f223 e8e4    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x2231c8
  19222e: 2800         	cmp	r0, #0x0
  192230: dd00         	ble	0x192234 <cocos2d::my_Base64Decode(std::string const&)+0x1b8> @ imm = #0x0
  192232: e769         	b	0x192108 <cocos2d::my_Base64Decode(std::string const&)+0x8c> @ imm = #-0x12e
  192234: 1c20         	adds	r0, r4, #0x0
  192236: a902         	add	r1, sp, #0x8
  192238: f1ff e9a4    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1ff348
  19223c: e764         	b	0x192108 <cocos2d::my_Base64Decode(std::string const&)+0x8c> @ imm = #-0x138
  19223e: 2101         	movs	r1, #0x1
  192240: 3804         	subs	r0, #0x4
  192242: 4249         	rsbs	r1, r1, #0
  192244: f223 e8d6    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x2231ac
  192248: 2800         	cmp	r0, #0x0
  19224a: dce3         	bgt	0x192214 <cocos2d::my_Base64Decode(std::string const&)+0x198> @ imm = #-0x3a
  19224c: 1c20         	adds	r0, r4, #0x0
  19224e: a908         	add	r1, sp, #0x20
  192250: f1ff e998    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1ff330
  192254: e7de         	b	0x192214 <cocos2d::my_Base64Decode(std::string const&)+0x198> @ imm = #-0x44
  192256: 2101         	movs	r1, #0x1
  192258: 3804         	subs	r0, #0x4
  19225a: 4249         	rsbs	r1, r1, #0
  19225c: f223 e8ca    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x223194
  192260: 2800         	cmp	r0, #0x0
  192262: dd00         	ble	0x192266 <cocos2d::my_Base64Decode(std::string const&)+0x1ea> @ imm = #0x0
  192264: e773         	b	0x19214e <cocos2d::my_Base64Decode(std::string const&)+0xd2> @ imm = #-0x11a
  192266: 1c20         	adds	r0, r4, #0x0
  192268: a907         	add	r1, sp, #0x1c
  19226a: f1ff e98c    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1ff318
  19226e: e76e         	b	0x19214e <cocos2d::my_Base64Decode(std::string const&)+0xd2> @ imm = #-0x124
  192270: 2101         	movs	r1, #0x1
  192272: 3804         	subs	r0, #0x4
  192274: 4249         	rsbs	r1, r1, #0
  192276: f223 e8be    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x22317c
  19227a: 2800         	cmp	r0, #0x0
  19227c: dd00         	ble	0x192280 <cocos2d::my_Base64Decode(std::string const&)+0x204> @ imm = #0x0
  19227e: e75f         	b	0x192140 <cocos2d::my_Base64Decode(std::string const&)+0xc4> @ imm = #-0x142
  192280: 1c20         	adds	r0, r4, #0x0
  192282: a906         	add	r1, sp, #0x18
  192284: f1ff e97e    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1ff2fc
  192288: e75a         	b	0x192140 <cocos2d::my_Base64Decode(std::string const&)+0xc4> @ imm = #-0x14c
  19228a: 2101         	movs	r1, #0x1
  19228c: 3804         	subs	r0, #0x4
  19228e: 4249         	rsbs	r1, r1, #0
  192290: f223 e8b0    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x223160
  192294: 2800         	cmp	r0, #0x0
  192296: dd00         	ble	0x19229a <cocos2d::my_Base64Decode(std::string const&)+0x21e> @ imm = #0x0
  192298: e74b         	b	0x192132 <cocos2d::my_Base64Decode(std::string const&)+0xb6> @ imm = #-0x16a
  19229a: 1c20         	adds	r0, r4, #0x0
  19229c: a905         	add	r1, sp, #0x14
  19229e: f1ff e972    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1ff2e4
  1922a2: e746         	b	0x192132 <cocos2d::my_Base64Decode(std::string const&)+0xb6> @ imm = #-0x174
  1922a4: 2101         	movs	r1, #0x1
  1922a6: 3804         	subs	r0, #0x4
  1922a8: 4249         	rsbs	r1, r1, #0
  1922aa: f223 e8a4    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x223148
  1922ae: 2800         	cmp	r0, #0x0
  1922b0: dd00         	ble	0x1922b4 <cocos2d::my_Base64Decode(std::string const&)+0x238> @ imm = #0x0
  1922b2: e737         	b	0x192124 <cocos2d::my_Base64Decode(std::string const&)+0xa8> @ imm = #-0x192
  1922b4: 1c20         	adds	r0, r4, #0x0
  1922b6: a904         	add	r1, sp, #0x10
  1922b8: f1ff e964    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1ff2c8
  1922bc: e732         	b	0x192124 <cocos2d::my_Base64Decode(std::string const&)+0xa8> @ imm = #-0x19c
  1922be: 2101         	movs	r1, #0x1
  1922c0: 3804         	subs	r0, #0x4
  1922c2: 4249         	rsbs	r1, r1, #0
  1922c4: f223 e896    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x22312c
  1922c8: 2800         	cmp	r0, #0x0
  1922ca: dd00         	ble	0x1922ce <cocos2d::my_Base64Decode(std::string const&)+0x252> @ imm = #0x0
  1922cc: e723         	b	0x192116 <cocos2d::my_Base64Decode(std::string const&)+0x9a> @ imm = #-0x1ba
  1922ce: 1c20         	adds	r0, r4, #0x0
  1922d0: a903         	add	r1, sp, #0xc
  1922d2: f1ff e958    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1ff2b0
  1922d6: e71e         	b	0x192116 <cocos2d::my_Base64Decode(std::string const&)+0x9a> @ imm = #-0x1c4
  1922d8: 4370         	muls	r0, r6, r0
  1922da: 0030         	movs	r0, r6
  1922dc: 2382         	movs	r3, #0x82
  1922de: 0024         	movs	r4, r4
  1922e0: a47c         	adr	r4, #496 <cocos2d::CCFileUtils::cleanReleaseW()+0x38>
  1922e2: 002f         	movs	r7, r5
