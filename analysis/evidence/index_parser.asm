
jgbol3.87/lib/armeabi/libxiyoujilua.so:	file format elf32-littlearm

Disassembly of section .text:

00192b90 <cocos2d::CCFileUtils::parse_index_file(std::string const&)>:
  192b90: b5f0         	push	{r4, r5, r6, r7, lr}
  192b92: 4d96         	ldr	r5, [pc, #0x258]        @ 0x192dec <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x25c>
  192b94: 1c0c         	adds	r4, r1, #0x0
  192b96: 4996         	ldr	r1, [pc, #0x258]        @ 0x192df0 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x260>
  192b98: 447d         	add	r5, pc
  192b9a: 682d         	ldr	r5, [r5]
  192b9c: b08f         	sub	sp, #0x3c
  192b9e: 1c07         	adds	r7, r0, #0x0
  192ba0: 1c2b         	adds	r3, r5, #0x0
  192ba2: 330c         	adds	r3, #0xc
  192ba4: 9307         	str	r3, [sp, #0x1c]
  192ba6: 4479         	add	r1, pc
  192ba8: 1c20         	adds	r0, r4, #0x0
  192baa: 2200         	movs	r2, #0x0
  192bac: 2301         	movs	r3, #0x1
  192bae: f1fe e87c    	blx	0x390ca8 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x236d4> @ imm = #0x1fe0f8
  192bb2: 1c06         	adds	r6, r0, #0x0
  192bb4: 281f         	cmp	r0, #0x1f
  192bb6: d900         	bls	0x192bba <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x2a> @ imm = #0x0
  192bb8: e09e         	b	0x192cf8 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x168> @ imm = #0x13c
  192bba: 1c33         	adds	r3, r6, #0x0
  192bbc: a808         	add	r0, sp, #0x20
  192bbe: 1c21         	adds	r1, r4, #0x0
  192bc0: 2200         	movs	r2, #0x0
  192bc2: f1ff ef6a    	blx	0x392a98 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x254c4> @ imm = #0x1ffed4
  192bc6: 9b08         	ldr	r3, [sp, #0x20]
  192bc8: 3b0c         	subs	r3, #0xc
  192bca: 681b         	ldr	r3, [r3]
  192bcc: 2b0b         	cmp	r3, #0xb
  192bce: d900         	bls	0x192bd2 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x42> @ imm = #0x0
  192bd0: e09b         	b	0x192d0a <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x17a> @ imm = #0x136
  192bd2: 6823         	ldr	r3, [r4]
  192bd4: 1c72         	adds	r2, r6, #0x1
  192bd6: 3b0c         	subs	r3, #0xc
  192bd8: 681b         	ldr	r3, [r3]
  192bda: 429a         	cmp	r2, r3
  192bdc: d900         	bls	0x192be0 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x50> @ imm = #0x0
  192bde: e0da         	b	0x192d96 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x206> @ imm = #0x1b4
  192be0: 2301         	movs	r3, #0x1
  192be2: 1c21         	adds	r1, r4, #0x0
  192be4: 425b         	rsbs	r3, r3, #0
  192be6: a809         	add	r0, sp, #0x24
  192be8: f1ff ef56    	blx	0x392a98 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x254c4> @ imm = #0x1ffeac
  192bec: a807         	add	r0, sp, #0x1c
  192bee: a909         	add	r1, sp, #0x24
  192bf0: f1ff edcc    	blx	0x39278c <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x251b8> @ imm = #0x1ffb98
  192bf4: 9809         	ldr	r0, [sp, #0x24]
  192bf6: 1c04         	adds	r4, r0, #0x0
  192bf8: 3c0c         	subs	r4, #0xc
  192bfa: 42ac         	cmp	r4, r5
  192bfc: d000         	beq	0x192c00 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x70> @ imm = #0x0
  192bfe: e0bd         	b	0x192d7c <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x1ec> @ imm = #0x17a
  192c00: 9808         	ldr	r0, [sp, #0x20]
  192c02: 1c04         	adds	r4, r0, #0x0
  192c04: 3c0c         	subs	r4, #0xc
  192c06: 42ac         	cmp	r4, r5
  192c08: d000         	beq	0x192c0c <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x7c> @ imm = #0x0
  192c0a: e0aa         	b	0x192d62 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x1d2> @ imm = #0x154
  192c0c: a907         	add	r1, sp, #0x1c
  192c0e: 2200         	movs	r2, #0x0
  192c10: 2340         	movs	r3, #0x40
  192c12: a80a         	add	r0, sp, #0x28
  192c14: f1ff ef40    	blx	0x392a98 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x254c4> @ imm = #0x1ffe80
  192c18: 4976         	ldr	r1, [pc, #0x1d8]        @ 0x192df4 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x264>
  192c1a: a80a         	add	r0, sp, #0x28
  192c1c: 2200         	movs	r2, #0x0
  192c1e: 4479         	add	r1, pc
  192c20: 2304         	movs	r3, #0x4
  192c22: f1fe e842    	blx	0x390ca8 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x236d4> @ imm = #0x1fe084
  192c26: 1c04         	adds	r4, r0, #0x0
  192c28: 980a         	ldr	r0, [sp, #0x28]
  192c2a: 1c06         	adds	r6, r0, #0x0
  192c2c: 3e0c         	subs	r6, #0xc
  192c2e: 42ae         	cmp	r6, r5
  192c30: d000         	beq	0x192c34 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0xa4> @ imm = #0x0
  192c32: e089         	b	0x192d48 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x1b8> @ imm = #0x112
  192c34: 1c63         	adds	r3, r4, #0x1
  192c36: d100         	bne	0x192c3a <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0xaa> @ imm = #0x0
  192c38: e06c         	b	0x192d14 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x184> @ imm = #0xd8
  192c3a: a907         	add	r1, sp, #0x1c
  192c3c: 2200         	movs	r2, #0x0
  192c3e: 2380         	movs	r3, #0x80
  192c40: a80c         	add	r0, sp, #0x30
  192c42: f1ff ef2a    	blx	0x392a98 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x254c4> @ imm = #0x1ffe54
  192c46: 486c         	ldr	r0, [pc, #0x1b0]        @ 0x192df8 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x268>
  192c48: 990c         	ldr	r1, [sp, #0x30]
  192c4a: 4478         	add	r0, pc
  192c4c: f7fe fd94    	bl	0x191778 <cocos2d::CCLog(char const*, ...)> @ imm = #-0x14d8
  192c50: 980c         	ldr	r0, [sp, #0x30]
  192c52: 1c04         	adds	r4, r0, #0x0
  192c54: 3c0c         	subs	r4, #0xc
  192c56: 42ac         	cmp	r4, r5
  192c58: d000         	beq	0x192c5c <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0xcc> @ imm = #0x0
  192c5a: e0b9         	b	0x192dd0 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x240> @ imm = #0x172
  192c5c: 1c2b         	adds	r3, r5, #0x0
  192c5e: 330c         	adds	r3, #0xc
  192c60: 930d         	str	r3, [sp, #0x34]
  192c62: 9b07         	ldr	r3, [sp, #0x1c]
  192c64: 1c1a         	adds	r2, r3, #0x0
  192c66: 3a0c         	subs	r2, #0xc
  192c68: 6816         	ldr	r6, [r2]
  192c6a: 2e00         	cmp	r6, #0x0
  192c6c: dd2a         	ble	0x192cc4 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x134> @ imm = #0x54
  192c6e: 2400         	movs	r4, #0x0
  192c70: e011         	b	0x192c96 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x106> @ imm = #0x22
  192c72: 3b0c         	subs	r3, #0xc
  192c74: 689b         	ldr	r3, [r3, #0x8]
  192c76: 2b00         	cmp	r3, #0x0
  192c78: db04         	blt	0x192c84 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0xf4> @ imm = #0x8
  192c7a: a807         	add	r0, sp, #0x1c
  192c7c: f1ff e902    	blx	0x391e84 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x248b0> @ imm = #0x1ff204
  192c80: 9b07         	ldr	r3, [sp, #0x1c]
  192c82: 5d19         	ldrb	r1, [r3, r4]
  192c84: a80d         	add	r0, sp, #0x34
  192c86: 3401         	adds	r4, #0x1
  192c88: f1ff eabe    	blx	0x392208 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x24c34> @ imm = #0x1ff57c
  192c8c: 42a6         	cmp	r6, r4
  192c8e: d019         	beq	0x192cc4 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x134> @ imm = #0x32
  192c90: 9b07         	ldr	r3, [sp, #0x1c]
  192c92: 1c1a         	adds	r2, r3, #0x0
  192c94: 3a0c         	subs	r2, #0xc
  192c96: 6892         	ldr	r2, [r2, #0x8]
  192c98: 2a00         	cmp	r2, #0x0
  192c9a: db03         	blt	0x192ca4 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x114> @ imm = #0x6
  192c9c: a807         	add	r0, sp, #0x1c
  192c9e: f1ff e8f2    	blx	0x391e84 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x248b0> @ imm = #0x1ff1e4
  192ca2: 9b07         	ldr	r3, [sp, #0x1c]
  192ca4: 5d19         	ldrb	r1, [r3, r4]
  192ca6: 290a         	cmp	r1, #0xa
  192ca8: d1e3         	bne	0x192c72 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0xe2> @ imm = #-0x3a
  192caa: 9b0d         	ldr	r3, [sp, #0x34]
  192cac: 3b0c         	subs	r3, #0xc
  192cae: 681a         	ldr	r2, [r3]
  192cb0: 2a0b         	cmp	r2, #0xb
  192cb2: d819         	bhi	0x192ce8 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x158> @ imm = #0x32
  192cb4: a80d         	add	r0, sp, #0x34
  192cb6: 2100         	movs	r1, #0x0
  192cb8: 2300         	movs	r3, #0x0
  192cba: 3401         	adds	r4, #0x1
  192cbc: f1fe eca8    	blx	0x391610 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x2403c> @ imm = #0x1fe950
  192cc0: 42a6         	cmp	r6, r4
  192cc2: d1e5         	bne	0x192c90 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x100> @ imm = #-0x36
  192cc4: 484d         	ldr	r0, [pc, #0x134]        @ 0x192dfc <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x26c>
  192cc6: 69f9         	ldr	r1, [r7, #0x1c]
  192cc8: 4478         	add	r0, pc
  192cca: f7fe fd55    	bl	0x191778 <cocos2d::CCLog(char const*, ...)> @ imm = #-0x1556
  192cce: 980d         	ldr	r0, [sp, #0x34]
  192cd0: 1c04         	adds	r4, r0, #0x0
  192cd2: 3c0c         	subs	r4, #0xc
  192cd4: 42ac         	cmp	r4, r5
  192cd6: d000         	beq	0x192cda <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x14a> @ imm = #0x0
  192cd8: e06d         	b	0x192db6 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x226> @ imm = #0xda
  192cda: 9807         	ldr	r0, [sp, #0x1c]
  192cdc: 1c04         	adds	r4, r0, #0x0
  192cde: 3c0c         	subs	r4, #0xc
  192ce0: 42ac         	cmp	r4, r5
  192ce2: d15c         	bne	0x192d9e <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x20e> @ imm = #0xb8
  192ce4: b00f         	add	sp, #0x3c
  192ce6: bdf0         	pop	{r4, r5, r6, r7, pc}
  192ce8: 1c38         	adds	r0, r7, #0x0
  192cea: a90d         	add	r1, sp, #0x34
  192cec: f7ff fe9a    	bl	0x192a24 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x2e0> @ imm = #-0x2cc
  192cf0: 9b0d         	ldr	r3, [sp, #0x34]
  192cf2: 3b0c         	subs	r3, #0xc
  192cf4: 681a         	ldr	r2, [r3]
  192cf6: e7dd         	b	0x192cb4 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x124> @ imm = #-0x46
  192cf8: 4841         	ldr	r0, [pc, #0x104]        @ 0x192e00 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x270>
  192cfa: 4478         	add	r0, pc
  192cfc: f7fe fd3c    	bl	0x191778 <cocos2d::CCLog(char const*, ...)> @ imm = #-0x1588
  192d00: a807         	add	r0, sp, #0x1c
  192d02: 1c21         	adds	r1, r4, #0x0
  192d04: f1ff ed42    	blx	0x39278c <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x251b8> @ imm = #0x1ffa84
  192d08: e780         	b	0x192c0c <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x7c> @ imm = #-0x100
  192d0a: 1c38         	adds	r0, r7, #0x0
  192d0c: a908         	add	r1, sp, #0x20
  192d0e: f7ff fe89    	bl	0x192a24 <cocos2d::CCFileUtils::getFileData(char const*, char const*, unsigned long*)+0x2e0> @ imm = #-0x2ee
  192d12: e75e         	b	0x192bd2 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x42> @ imm = #-0x144
  192d14: a80b         	add	r0, sp, #0x2c
  192d16: a907         	add	r1, sp, #0x1c
  192d18: f7ff f9b0    	bl	0x19207c <cocos2d::my_Base64Decode(std::string const&)> @ imm = #-0xca0
  192d1c: a807         	add	r0, sp, #0x1c
  192d1e: a90b         	add	r1, sp, #0x2c
  192d20: f1ff ed34    	blx	0x39278c <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x251b8> @ imm = #0x1ffa68
  192d24: 980b         	ldr	r0, [sp, #0x2c]
  192d26: 1c06         	adds	r6, r0, #0x0
  192d28: 3e0c         	subs	r6, #0xc
  192d2a: 42ae         	cmp	r6, r5
  192d2c: d100         	bne	0x192d30 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x1a0> @ imm = #0x0
  192d2e: e784         	b	0x192c3a <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0xaa> @ imm = #-0xf8
  192d30: 3804         	subs	r0, #0x4
  192d32: 1c21         	adds	r1, r4, #0x0
  192d34: f222 eb5e    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x2226bc
  192d38: 2800         	cmp	r0, #0x0
  192d3a: dd00         	ble	0x192d3e <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x1ae> @ imm = #0x0
  192d3c: e77d         	b	0x192c3a <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0xaa> @ imm = #-0x106
  192d3e: 1c30         	adds	r0, r6, #0x0
  192d40: a903         	add	r1, sp, #0xc
  192d42: f1fe ec20    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1fe840
  192d46: e778         	b	0x192c3a <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0xaa> @ imm = #-0x110
  192d48: 2101         	movs	r1, #0x1
  192d4a: 3804         	subs	r0, #0x4
  192d4c: 4249         	rsbs	r1, r1, #0
  192d4e: f222 eb52    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x2226a4
  192d52: 2800         	cmp	r0, #0x0
  192d54: dd00         	ble	0x192d58 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x1c8> @ imm = #0x0
  192d56: e76d         	b	0x192c34 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0xa4> @ imm = #-0x126
  192d58: 1c30         	adds	r0, r6, #0x0
  192d5a: a902         	add	r1, sp, #0x8
  192d5c: f1fe ec12    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1fe824
  192d60: e768         	b	0x192c34 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0xa4> @ imm = #-0x130
  192d62: 2101         	movs	r1, #0x1
  192d64: 3804         	subs	r0, #0x4
  192d66: 4249         	rsbs	r1, r1, #0
  192d68: f222 eb44    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x222688
  192d6c: 2800         	cmp	r0, #0x0
  192d6e: dd00         	ble	0x192d72 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x1e2> @ imm = #0x0
  192d70: e74c         	b	0x192c0c <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x7c> @ imm = #-0x168
  192d72: 1c20         	adds	r0, r4, #0x0
  192d74: a901         	add	r1, sp, #0x4
  192d76: f1fe ec06    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1fe80c
  192d7a: e747         	b	0x192c0c <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x7c> @ imm = #-0x172
  192d7c: 2101         	movs	r1, #0x1
  192d7e: 3804         	subs	r0, #0x4
  192d80: 4249         	rsbs	r1, r1, #0
  192d82: f222 eb38    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x222670
  192d86: 2800         	cmp	r0, #0x0
  192d88: dd00         	ble	0x192d8c <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x1fc> @ imm = #0x0
  192d8a: e739         	b	0x192c00 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x70> @ imm = #-0x18e
  192d8c: 1c20         	adds	r0, r4, #0x0
  192d8e: 4669         	mov	r1, sp
  192d90: f1fe ebf8    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1fe7f0
  192d94: e734         	b	0x192c00 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x70> @ imm = #-0x198
  192d96: 481b         	ldr	r0, [pc, #0x6c]         @ 0x192e04 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x274>
  192d98: 4478         	add	r0, pc
  192d9a: f1d5 eb16    	blx	0x3683c8 <ERR_load_SSL_strings+0x340> @ imm = #0x1d562c
  192d9e: 2101         	movs	r1, #0x1
  192da0: 3804         	subs	r0, #0x4
  192da2: 4249         	rsbs	r1, r1, #0
  192da4: f222 eb26    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x22264c
  192da8: 2800         	cmp	r0, #0x0
  192daa: dc9b         	bgt	0x192ce4 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x154> @ imm = #-0xca
  192dac: 1c20         	adds	r0, r4, #0x0
  192dae: a906         	add	r1, sp, #0x18
  192db0: f1fe ebe8    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1fe7d0
  192db4: e796         	b	0x192ce4 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x154> @ imm = #-0xd4
  192db6: 2101         	movs	r1, #0x1
  192db8: 3804         	subs	r0, #0x4
  192dba: 4249         	rsbs	r1, r1, #0
  192dbc: f222 eb1a    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x222634
  192dc0: 2800         	cmp	r0, #0x0
  192dc2: dd00         	ble	0x192dc6 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x236> @ imm = #0x0
  192dc4: e789         	b	0x192cda <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x14a> @ imm = #-0xee
  192dc6: 1c20         	adds	r0, r4, #0x0
  192dc8: a905         	add	r1, sp, #0x14
  192dca: f1fe ebdc    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1fe7b8
  192dce: e784         	b	0x192cda <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x14a> @ imm = #-0xf8
  192dd0: 2101         	movs	r1, #0x1
  192dd2: 3804         	subs	r0, #0x4
  192dd4: 4249         	rsbs	r1, r1, #0
  192dd6: f222 eb0e    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x22261c
  192dda: 2800         	cmp	r0, #0x0
  192ddc: dd00         	ble	0x192de0 <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0x250> @ imm = #0x0
  192dde: e73d         	b	0x192c5c <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0xcc> @ imm = #-0x186
  192de0: 1c20         	adds	r0, r4, #0x0
  192de2: a904         	add	r1, sp, #0x10
  192de4: f1fe ebce    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x1fe79c
  192de8: e738         	b	0x192c5c <cocos2d::CCFileUtils::parse_index_file(std::string const&)+0xcc> @ imm = #-0x190
  192dea: 46c0         	mov	r8, r8
  192dec: 99dc         	ldr	r1, [sp, #0x370]
  192dee: 002f         	movs	r7, r5
  192df0: de62         	udf	#0x62
  192df2: 0027         	movs	r7, r4
  192df4: 17f2         	asrs	r2, r6, #0x1f
  192df6: 0024         	movs	r4, r4
  192df8: 186e         	adds	r6, r5, r1
  192dfa: 0024         	movs	r4, r4
  192dfc: 17fc         	asrs	r4, r7, #0x1f
  192dfe: 0024         	movs	r4, r4
  192e00: 179a         	asrs	r2, r3, #0x1e
  192e02: 0024         	movs	r4, r4
  192e04: f23c 0023    	<unknown>
