
/Users/ezan/Desktop/vibeCoidng/JGBOLNew/jgbol3.87/lib/armeabi/libxiyoujilua.so:	file format elf32-littlearm

Disassembly of section .text:

000ff8f8 <ArkCommon::hash::jenkins::hash(unsigned char*, unsigned int, unsigned int)>:
   ff8f8: b570         	push	{r4, r5, r6, lr}
   ff8fa: 4d4f         	ldr	r5, [pc, #0x13c]        @ 0xffa38 <ArkCommon::hash::jenkins::hash(unsigned char*, unsigned int, unsigned int)+0x140>
   ff8fc: 1c03         	adds	r3, r0, #0x0
   ff8fe: 1c08         	adds	r0, r1, #0x0
   ff900: 1c2c         	adds	r4, r5, #0x0
   ff902: 290b         	cmp	r1, #0xb
   ff904: d948         	bls	0xff998 <ArkCommon::hash::jenkins::hash(unsigned char*, unsigned int, unsigned int)+0xa0> @ imm = #0x90
   ff906: 791e         	ldrb	r6, [r3, #0x4]
   ff908: 380c         	subs	r0, #0xc
   ff90a: 1975         	adds	r5, r6, r5
   ff90c: 795e         	ldrb	r6, [r3, #0x5]
   ff90e: 0236         	lsls	r6, r6, #0x8
   ff910: 19ad         	adds	r5, r5, r6
   ff912: 799e         	ldrb	r6, [r3, #0x6]
   ff914: 0436         	lsls	r6, r6, #0x10
   ff916: 19ad         	adds	r5, r5, r6
   ff918: 79de         	ldrb	r6, [r3, #0x7]
   ff91a: 0636         	lsls	r6, r6, #0x18
   ff91c: 19ad         	adds	r5, r5, r6
   ff91e: 7a1e         	ldrb	r6, [r3, #0x8]
   ff920: 18b2         	adds	r2, r6, r2
   ff922: 7a5e         	ldrb	r6, [r3, #0x9]
   ff924: 0236         	lsls	r6, r6, #0x8
   ff926: 1992         	adds	r2, r2, r6
   ff928: 7a9e         	ldrb	r6, [r3, #0xa]
   ff92a: 0436         	lsls	r6, r6, #0x10
   ff92c: 1992         	adds	r2, r2, r6
   ff92e: 7ade         	ldrb	r6, [r3, #0xb]
   ff930: 0636         	lsls	r6, r6, #0x18
   ff932: 1992         	adds	r2, r2, r6
   ff934: 781e         	ldrb	r6, [r3]
   ff936: 1934         	adds	r4, r6, r4
   ff938: 785e         	ldrb	r6, [r3, #0x1]
   ff93a: 0236         	lsls	r6, r6, #0x8
   ff93c: 19a4         	adds	r4, r4, r6
   ff93e: 789e         	ldrb	r6, [r3, #0x2]
   ff940: 0436         	lsls	r6, r6, #0x10
   ff942: 19a4         	adds	r4, r4, r6
   ff944: 78de         	ldrb	r6, [r3, #0x3]
   ff946: 330c         	adds	r3, #0xc
   ff948: 0636         	lsls	r6, r6, #0x18
   ff94a: 19a4         	adds	r4, r4, r6
   ff94c: 1aa4         	subs	r4, r4, r2
   ff94e: 0b56         	lsrs	r6, r2, #0xd
   ff950: 1b64         	subs	r4, r4, r5
   ff952: 4074         	eors	r4, r6
   ff954: 1aad         	subs	r5, r5, r2
   ff956: 0226         	lsls	r6, r4, #0x8
   ff958: 1b2d         	subs	r5, r5, r4
   ff95a: 4075         	eors	r5, r6
   ff95c: 1b12         	subs	r2, r2, r4
   ff95e: 0b6e         	lsrs	r6, r5, #0xd
   ff960: 1b52         	subs	r2, r2, r5
   ff962: 4072         	eors	r2, r6
   ff964: 1b64         	subs	r4, r4, r5
   ff966: 0b16         	lsrs	r6, r2, #0xc
   ff968: 1aa4         	subs	r4, r4, r2
   ff96a: 4074         	eors	r4, r6
   ff96c: 1aad         	subs	r5, r5, r2
   ff96e: 0426         	lsls	r6, r4, #0x10
   ff970: 1b2d         	subs	r5, r5, r4
   ff972: 4075         	eors	r5, r6
   ff974: 1b12         	subs	r2, r2, r4
   ff976: 096e         	lsrs	r6, r5, #0x5
   ff978: 1b52         	subs	r2, r2, r5
   ff97a: 4072         	eors	r2, r6
   ff97c: 1b64         	subs	r4, r4, r5
   ff97e: 08d6         	lsrs	r6, r2, #0x3
   ff980: 1aa4         	subs	r4, r4, r2
   ff982: 4074         	eors	r4, r6
   ff984: 1aad         	subs	r5, r5, r2
   ff986: 02a6         	lsls	r6, r4, #0xa
   ff988: 1b2d         	subs	r5, r5, r4
   ff98a: 4075         	eors	r5, r6
   ff98c: 1b12         	subs	r2, r2, r4
   ff98e: 1b52         	subs	r2, r2, r5
   ff990: 0bee         	lsrs	r6, r5, #0xf
   ff992: 4072         	eors	r2, r6
   ff994: 280b         	cmp	r0, #0xb
   ff996: d8b6         	bhi	0xff906 <ArkCommon::hash::jenkins::hash(unsigned char*, unsigned int, unsigned int)+0xe> @ imm = #-0x94
   ff998: 3801         	subs	r0, #0x1
   ff99a: 1852         	adds	r2, r2, r1
   ff99c: 280a         	cmp	r0, #0xa
   ff99e: d826         	bhi	0xff9ee <ArkCommon::hash::jenkins::hash(unsigned char*, unsigned int, unsigned int)+0xf6> @ imm = #0x4c
   ff9a0: f2b4 f998    	bl	0x3b3cd4 <__gnu_thumb1_case_uqi> @ imm = #0x2b4330
   ff9a4: 2023         	movs	r0, #0x23
   ff9a6: 1a1d         	subs	r5, r3, r0
   ff9a8: 1518         	asrs	r0, r3, #0x14
   ff9aa: 0f12         	lsrs	r2, r2, #0x1c
   ff9ac: 090c         	lsrs	r4, r1, #0x4
   ff9ae: 0006         	movs	r6, r0
   ff9b0: 7a99         	ldrb	r1, [r3, #0xa]
   ff9b2: 0609         	lsls	r1, r1, #0x18
   ff9b4: 1852         	adds	r2, r2, r1
   ff9b6: 7a59         	ldrb	r1, [r3, #0x9]
   ff9b8: 0409         	lsls	r1, r1, #0x10
   ff9ba: 1852         	adds	r2, r2, r1
   ff9bc: 7a19         	ldrb	r1, [r3, #0x8]
   ff9be: 0209         	lsls	r1, r1, #0x8
   ff9c0: 1852         	adds	r2, r2, r1
   ff9c2: 79d9         	ldrb	r1, [r3, #0x7]
   ff9c4: 0609         	lsls	r1, r1, #0x18
   ff9c6: 186d         	adds	r5, r5, r1
   ff9c8: 7999         	ldrb	r1, [r3, #0x6]
   ff9ca: 0409         	lsls	r1, r1, #0x10
   ff9cc: 186d         	adds	r5, r5, r1
   ff9ce: 7959         	ldrb	r1, [r3, #0x5]
   ff9d0: 0209         	lsls	r1, r1, #0x8
   ff9d2: 186d         	adds	r5, r5, r1
   ff9d4: 7919         	ldrb	r1, [r3, #0x4]
   ff9d6: 186d         	adds	r5, r5, r1
   ff9d8: 78d9         	ldrb	r1, [r3, #0x3]
   ff9da: 0609         	lsls	r1, r1, #0x18
   ff9dc: 1864         	adds	r4, r4, r1
   ff9de: 7899         	ldrb	r1, [r3, #0x2]
   ff9e0: 0409         	lsls	r1, r1, #0x10
   ff9e2: 1864         	adds	r4, r4, r1
   ff9e4: 7859         	ldrb	r1, [r3, #0x1]
   ff9e6: 0209         	lsls	r1, r1, #0x8
   ff9e8: 1864         	adds	r4, r4, r1
   ff9ea: 781b         	ldrb	r3, [r3]
   ff9ec: 18e4         	adds	r4, r4, r3
   ff9ee: 1b64         	subs	r4, r4, r5
   ff9f0: 0b53         	lsrs	r3, r2, #0xd
   ff9f2: 1aa4         	subs	r4, r4, r2
   ff9f4: 405c         	eors	r4, r3
   ff9f6: 1aad         	subs	r5, r5, r2
   ff9f8: 0221         	lsls	r1, r4, #0x8
   ff9fa: 1b2d         	subs	r5, r5, r4
   ff9fc: 404d         	eors	r5, r1
   ff9fe: 1b12         	subs	r2, r2, r4
   ffa00: 0b6b         	lsrs	r3, r5, #0xd
   ffa02: 1b52         	subs	r2, r2, r5
   ffa04: 405a         	eors	r2, r3
   ffa06: 1b64         	subs	r4, r4, r5
   ffa08: 1aa4         	subs	r4, r4, r2
   ffa0a: 0b10         	lsrs	r0, r2, #0xc
   ffa0c: 4060         	eors	r0, r4
   ffa0e: 1aad         	subs	r5, r5, r2
   ffa10: 1a2d         	subs	r5, r5, r0
   ffa12: 0401         	lsls	r1, r0, #0x10
   ffa14: 4069         	eors	r1, r5
   ffa16: 1a12         	subs	r2, r2, r0
   ffa18: 1a52         	subs	r2, r2, r1
   ffa1a: 094b         	lsrs	r3, r1, #0x5
   ffa1c: 4053         	eors	r3, r2
   ffa1e: 1a40         	subs	r0, r0, r1
   ffa20: 08da         	lsrs	r2, r3, #0x3
   ffa22: 1ac0         	subs	r0, r0, r3
   ffa24: 4050         	eors	r0, r2
   ffa26: 1ac9         	subs	r1, r1, r3
   ffa28: 0282         	lsls	r2, r0, #0xa
   ffa2a: 1a09         	subs	r1, r1, r0
   ffa2c: 4051         	eors	r1, r2
   ffa2e: 1a18         	subs	r0, r3, r0
   ffa30: 1a40         	subs	r0, r0, r1
   ffa32: 0bc9         	lsrs	r1, r1, #0xf
   ffa34: 4048         	eors	r0, r1
   ffa36: bd70         	pop	{r4, r5, r6, pc}
   ffa38: 79b9         	ldrb	r1, [r7, #0x6]
   ffa3a: 9e37         	ldr	r6, [sp, #0xdc]

000ffa3c <Kernal_Helper_StringAdjust(char*)>:
   ffa3c: b530         	push	{r4, r5, lr}
   ffa3e: 7803         	ldrb	r3, [r0]
   ffa40: 2b00         	cmp	r3, #0x0
   ffa42: d01a         	beq	0xffa7a <Kernal_Helper_StringAdjust(char*)+0x3e> @ imm = #0x34
   ffa44: 1c42         	adds	r2, r0, #0x1
   ffa46: 1c04         	adds	r4, r0, #0x0
   ffa48: 252f         	movs	r5, #0x2f
   ffa4a: e007         	b	0xffa5c <Kernal_Helper_StringAdjust(char*)+0x20> @ imm = #0xe
   ffa4c: 3320         	adds	r3, #0x20
   ffa4e: 7023         	strb	r3, [r4]
   ffa50: 1c14         	adds	r4, r2, #0x0
   ffa52: 3201         	adds	r2, #0x1
   ffa54: 1e53         	subs	r3, r2, #0x1
   ffa56: 781b         	ldrb	r3, [r3]
   ffa58: 2b00         	cmp	r3, #0x0
   ffa5a: d00e         	beq	0xffa7a <Kernal_Helper_StringAdjust(char*)+0x3e> @ imm = #0x1c
   ffa5c: 1c19         	adds	r1, r3, #0x0
   ffa5e: 3941         	subs	r1, #0x41
   ffa60: 0609         	lsls	r1, r1, #0x18
   ffa62: 0e09         	lsrs	r1, r1, #0x18
   ffa64: 2919         	cmp	r1, #0x19
   ffa66: d9f1         	bls	0xffa4c <Kernal_Helper_StringAdjust(char*)+0x10> @ imm = #-0x1e
   ffa68: 2b5c         	cmp	r3, #0x5c
   ffa6a: d1f1         	bne	0xffa50 <Kernal_Helper_StringAdjust(char*)+0x14> @ imm = #-0x1e
   ffa6c: 7025         	strb	r5, [r4]
   ffa6e: 1c14         	adds	r4, r2, #0x0
   ffa70: 3201         	adds	r2, #0x1
   ffa72: 1e53         	subs	r3, r2, #0x1
   ffa74: 781b         	ldrb	r3, [r3]
   ffa76: 2b00         	cmp	r3, #0x0
   ffa78: d1f0         	bne	0xffa5c <Kernal_Helper_StringAdjust(char*)+0x20> @ imm = #-0x20
   ffa7a: bd30         	pop	{r4, r5, pc}

000ffa7c <Kernal_Helper_StringCopy(char*, char const*, unsigned int)>:
   ffa7c: b5f8         	push	{r3, r4, r5, r6, r7, lr}
   ffa7e: 1c07         	adds	r7, r0, #0x0
   ffa80: 1c08         	adds	r0, r1, #0x0
   ffa82: 1c0e         	adds	r6, r1, #0x0
   ffa84: 1c15         	adds	r5, r2, #0x0
   ffa86: f7ef e99a    	blx	0xeedbc <.plt+0x404>    @ imm = #-0x10ccc
   ffa8a: 1c44         	adds	r4, r0, #0x1
   ffa8c: 42ac         	cmp	r4, r5
   ffa8e: d900         	bls	0xffa92 <Kernal_Helper_StringCopy(char*, char const*, unsigned int)+0x16> @ imm = #0x0
   ffa90: 1c2c         	adds	r4, r5, #0x0
   ffa92: 1c38         	adds	r0, r7, #0x0
   ffa94: 1c31         	adds	r1, r6, #0x0
   ffa96: 197d         	adds	r5, r7, r5
   ffa98: 1c22         	adds	r2, r4, #0x0
   ffa9a: f7ef e84c    	blx	0xeeb34 <.plt+0x17c>    @ imm = #-0x10f68
   ffa9e: 3d01         	subs	r5, #0x1
   ffaa0: 2300         	movs	r3, #0x0
   ffaa2: 702b         	strb	r3, [r5]
   ffaa4: 1c20         	adds	r0, r4, #0x0
   ffaa6: bdf8         	pop	{r3, r4, r5, r6, r7, pc}

000ffaa8 <Kernal_Helper_String2Id(char const*)>:
   ffaa8: b570         	push	{r4, r5, r6, lr}
   ffaaa: 4c10         	ldr	r4, [pc, #0x40]         @ 0xffaec <Kernal_Helper_String2Id(char const*)+0x44>
   ffaac: b0c2         	sub	sp, #0x108
   ffaae: 1c05         	adds	r5, r0, #0x0
   ffab0: 447c         	add	r4, pc
   ffab2: 6824         	ldr	r4, [r4]
   ffab4: 6823         	ldr	r3, [r4]
   ffab6: 9341         	str	r3, [sp, #0x104]
   ffab8: f7ef e980    	blx	0xeedbc <.plt+0x404>    @ imm = #-0x10d00
   ffabc: 2280         	movs	r2, #0x80
   ffabe: 1c29         	adds	r1, r5, #0x0
   ffac0: 0052         	lsls	r2, r2, #0x1
   ffac2: 1c06         	adds	r6, r0, #0x0
   ffac4: a801         	add	r0, sp, #0x4
   ffac6: f7ff ffd9    	bl	0xffa7c <Kernal_Helper_StringCopy(char*, char const*, unsigned int)> @ imm = #-0x4e
   ffaca: a801         	add	r0, sp, #0x4
   ffacc: f7ff ffb6    	bl	0xffa3c <Kernal_Helper_StringAdjust(char*)> @ imm = #-0x94
   ffad0: 2200         	movs	r2, #0x0
   ffad2: a801         	add	r0, sp, #0x4
   ffad4: 1c31         	adds	r1, r6, #0x0
   ffad6: f7ff ff0f    	bl	0xff8f8 <ArkCommon::hash::jenkins::hash(unsigned char*, unsigned int, unsigned int)> @ imm = #-0x1e2
   ffada: 9a41         	ldr	r2, [sp, #0x104]
   ffadc: 6823         	ldr	r3, [r4]
   ffade: 429a         	cmp	r2, r3
   ffae0: d101         	bne	0xffae6 <Kernal_Helper_String2Id(char const*)+0x3e> @ imm = #0x2
   ffae2: b042         	add	sp, #0x108
   ffae4: bd70         	pop	{r4, r5, r6, pc}
   ffae6: f7ef ead8    	blx	0xef098 <.plt+0x6e0>    @ imm = #-0x10a50
   ffaea: 46c0         	mov	r8, r8
   ffaec: c4bc         	stm	r4!, {r2, r3, r4, r5, r7}
   ffaee: 0038         	movs	r0, r7

000ffaf0 <calculateHashAccount(std::string const&)>:
   ffaf0: b5f0         	push	{r4, r5, r6, r7, lr}
   ffaf2: 4647         	mov	r7, r8
   ffaf4: b480         	push	{r7}
   ffaf6: 4a1e         	ldr	r2, [pc, #0x78]         @ 0xffb70 <calculateHashAccount(std::string const&)+0x80>
   ffaf8: 1c06         	adds	r6, r0, #0x0
   ffafa: b082         	sub	sp, #0x8
   ffafc: 4690         	mov	r8, r2
   ffafe: 44f8         	add	r8, pc
   ffb00: 4642         	mov	r2, r8
   ffb02: 6813         	ldr	r3, [r2]
   ffb04: 1c18         	adds	r0, r3, #0x0
   ffb06: 4698         	mov	r8, r3
   ffb08: 6833         	ldr	r3, [r6]
   ffb0a: 300c         	adds	r0, #0xc
   ffb0c: 9001         	str	r0, [sp, #0x4]
   ffb0e: 1c1a         	adds	r2, r3, #0x0
   ffb10: 3a0c         	subs	r2, #0xc
   ffb12: 6817         	ldr	r7, [r2]
   ffb14: 2f00         	cmp	r7, #0x0
   ffb16: dd11         	ble	0xffb3c <calculateHashAccount(std::string const&)+0x4c> @ imm = #0x22
   ffb18: 4d16         	ldr	r5, [pc, #0x58]         @ 0xffb74 <calculateHashAccount(std::string const&)+0x84>
   ffb1a: 2400         	movs	r4, #0x0
   ffb1c: 447d         	add	r5, pc
   ffb1e: 682d         	ldr	r5, [r5]
   ffb20: e000         	b	0xffb24 <calculateHashAccount(std::string const&)+0x34> @ imm = #0x0
   ffb22: 6833         	ldr	r3, [r6]
   ffb24: 5d1b         	ldrb	r3, [r3, r4]
   ffb26: 682a         	ldr	r2, [r5]
   ffb28: a801         	add	r0, sp, #0x4
   ffb2a: 3301         	adds	r3, #0x1
   ffb2c: 005b         	lsls	r3, r3, #0x1
   ffb2e: 5cd1         	ldrb	r1, [r2, r3]
   ffb30: 3401         	adds	r4, #0x1
   ffb32: f292 eb6a    	blx	0x392208 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x24c34> @ imm = #0x2926d4
   ffb36: 42a7         	cmp	r7, r4
   ffb38: d1f3         	bne	0xffb22 <calculateHashAccount(std::string const&)+0x32> @ imm = #-0x1a
   ffb3a: 9801         	ldr	r0, [sp, #0x4]
   ffb3c: f7ff ffb4    	bl	0xffaa8 <Kernal_Helper_String2Id(char const*)> @ imm = #-0x98
   ffb40: 1c05         	adds	r5, r0, #0x0
   ffb42: 9801         	ldr	r0, [sp, #0x4]
   ffb44: 1c04         	adds	r4, r0, #0x0
   ffb46: 3c0c         	subs	r4, #0xc
   ffb48: 4544         	cmp	r4, r8
   ffb4a: d104         	bne	0xffb56 <calculateHashAccount(std::string const&)+0x66> @ imm = #0x8
   ffb4c: b002         	add	sp, #0x8
   ffb4e: 1c28         	adds	r0, r5, #0x0
   ffb50: bc04         	pop	{r2}
   ffb52: 4690         	mov	r8, r2
   ffb54: bdf0         	pop	{r4, r5, r6, r7, pc}
   ffb56: 2101         	movs	r1, #0x1
   ffb58: 3804         	subs	r0, #0x4
   ffb5a: 4249         	rsbs	r1, r1, #0
   ffb5c: f2b5 ec4a    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x2b5894
   ffb60: 2800         	cmp	r0, #0x0
   ffb62: dcf3         	bgt	0xffb4c <calculateHashAccount(std::string const&)+0x5c> @ imm = #-0x1a
   ffb64: 1c20         	adds	r0, r4, #0x0
   ffb66: 4669         	mov	r1, sp
   ffb68: f291 ed0c    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x291a18
   ffb6c: e7ee         	b	0xffb4c <calculateHashAccount(std::string const&)+0x5c> @ imm = #-0x24
   ffb6e: 46c0         	mov	r8, r8
   ffb70: ca76         	ldm	r2, {r1, r2, r4, r5, r6}
   ffb72: 0038         	movs	r0, r7
   ffb74: c60c         	stm	r6!, {r2, r3}
   ffb76: 0038         	movs	r0, r7


/Users/ezan/Desktop/vibeCoidng/JGBOLNew/jgbol3.87/lib/armeabi/libxiyoujilua.so:	file format elf32-littlearm

Disassembly of section .text:

00100d38 <LuaInterface::getHashAccount(lua_State*)>:
  100d38: b530         	push	{r4, r5, lr}
  100d3a: b085         	sub	sp, #0x14
  100d3c: 2101         	movs	r1, #0x1
  100d3e: 2200         	movs	r2, #0x0
  100d40: 1c04         	adds	r4, r0, #0x0
  100d42: f0d2 e926    	blx	0x1d2f90 <lua_tolstring> @ imm = #0xd224c
  100d46: aa01         	add	r2, sp, #0x4
  100d48: 1c01         	adds	r1, r0, #0x0
  100d4a: a803         	add	r0, sp, #0xc
  100d4c: f291 ef84    	blx	0x392c58 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x25684> @ imm = #0x291f08
  100d50: a803         	add	r0, sp, #0xc
  100d52: f7fe fecd    	bl	0xffaf0 <calculateHashAccount(std::string const&)> @ imm = #-0x1266
  100d56: 1c05         	adds	r5, r0, #0x0
  100d58: 4812         	ldr	r0, [pc, #0x48]         @ 0x100da4 <LuaInterface::getHashAccount(lua_State*)+0x6c>
  100d5a: 9a03         	ldr	r2, [sp, #0xc]
  100d5c: 1c29         	adds	r1, r5, #0x0
  100d5e: 4478         	add	r0, pc
  100d60: f090 fd0a    	bl	0x191778 <cocos2d::CCLog(char const*, ...)> @ imm = #0x90a14
  100d64: 1c28         	adds	r0, r5, #0x0
  100d66: f2b3 ea20    	blx	0x3b41a8 <__floatunsidf> @ imm = #0x2b3440
  100d6a: 1c02         	adds	r2, r0, #0x0
  100d6c: 1c0b         	adds	r3, r1, #0x0
  100d6e: 1c20         	adds	r0, r4, #0x0
  100d70: f0d2 eb1a    	blx	0x1d33a8 <lua_pushnumber> @ imm = #0xd2634
  100d74: 4b0c         	ldr	r3, [pc, #0x30]         @ 0x100da8 <LuaInterface::getHashAccount(lua_State*)+0x70>
  100d76: 9803         	ldr	r0, [sp, #0xc]
  100d78: 447b         	add	r3, pc
  100d7a: 681b         	ldr	r3, [r3]
  100d7c: 1c04         	adds	r4, r0, #0x0
  100d7e: 3c0c         	subs	r4, #0xc
  100d80: 429c         	cmp	r4, r3
  100d82: d102         	bne	0x100d8a <LuaInterface::getHashAccount(lua_State*)+0x52> @ imm = #0x4
  100d84: b005         	add	sp, #0x14
  100d86: 2001         	movs	r0, #0x1
  100d88: bd30         	pop	{r4, r5, pc}
  100d8a: 2101         	movs	r1, #0x1
  100d8c: 3804         	subs	r0, #0x4
  100d8e: 4249         	rsbs	r1, r1, #0
  100d90: f2b4 eb30    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x2b4660
  100d94: 2800         	cmp	r0, #0x0
  100d96: dcf5         	bgt	0x100d84 <LuaInterface::getHashAccount(lua_State*)+0x4c> @ imm = #-0x16
  100d98: 1c20         	adds	r0, r4, #0x0
  100d9a: a902         	add	r1, sp, #0x8
  100d9c: f290 ebf2    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x2907e4
  100da0: e7f0         	b	0x100d84 <LuaInterface::getHashAccount(lua_State*)+0x4c> @ imm = #-0x20
  100da2: 46c0         	mov	r8, r8
  100da4: 80be         	strh	r6, [r7, #0x4]
  100da6: 002b         	movs	r3, r5
  100da8: b7fc         	<unknown>
  100daa: 0038         	movs	r0, r7
