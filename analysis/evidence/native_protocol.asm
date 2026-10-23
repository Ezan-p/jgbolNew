
jgbol3.87/lib/armeabi/libxiyoujilua.so:	file format elf32-littlearm

Disassembly of section .text:

00105b0c <CurlSocket::decodePackage()>:
  105b0c: b5f0         	push	{r4, r5, r6, r7, lr}
  105b0e: 465f         	mov	r7, r11
  105b10: 4656         	mov	r6, r10
  105b12: 464d         	mov	r5, r9
  105b14: 4644         	mov	r4, r8
  105b16: b4f0         	push	{r4, r5, r6, r7}
  105b18: 23cc         	movs	r3, #0xcc
  105b1a: 005b         	lsls	r3, r3, #0x1
  105b1c: 5cc3         	ldrb	r3, [r0, r3]
  105b1e: 1c05         	adds	r5, r0, #0x0
  105b20: 20cc         	movs	r0, #0xcc
  105b22: 0040         	lsls	r0, r0, #0x1
  105b24: 182c         	adds	r4, r5, r0
  105b26: 7861         	ldrb	r1, [r4, #0x1]
  105b28: 4ad0         	ldr	r2, [pc, #0x340]        @ 0x105e6c <CurlSocket::decodePackage()+0x360>
  105b2a: b093         	sub	sp, #0x4c
  105b2c: 0209         	lsls	r1, r1, #0x8
  105b2e: 4319         	orrs	r1, r3
  105b30: 1c0b         	adds	r3, r1, #0x0
  105b32: 3b14         	subs	r3, #0x14
  105b34: 041b         	lsls	r3, r3, #0x10
  105b36: 0c1b         	lsrs	r3, r3, #0x10
  105b38: 4293         	cmp	r3, r2
  105b3a: d900         	bls	0x105b3e <CurlSocket::decodePackage()+0x32> @ imm = #0x0
  105b3c: e105         	b	0x105d4a <CurlSocket::decodePackage()+0x23e> @ imm = #0x20a
  105b3e: 78e2         	ldrb	r2, [r4, #0x3]
  105b40: 78a3         	ldrb	r3, [r4, #0x2]
  105b42: 0212         	lsls	r2, r2, #0x8
  105b44: 431a         	orrs	r2, r3
  105b46: 7923         	ldrb	r3, [r4, #0x4]
  105b48: 041b         	lsls	r3, r3, #0x10
  105b4a: 431a         	orrs	r2, r3
  105b4c: 7963         	ldrb	r3, [r4, #0x5]
  105b4e: 061b         	lsls	r3, r3, #0x18
  105b50: 431a         	orrs	r2, r3
  105b52: 4bc7         	ldr	r3, [pc, #0x31c]        @ 0x105e70 <CurlSocket::decodePackage()+0x364>
  105b54: 58eb         	ldr	r3, [r5, r3]
  105b56: 429a         	cmp	r2, r3
  105b58: d100         	bne	0x105b5c <CurlSocket::decodePackage()+0x50> @ imm = #0x0
  105b5a: e0b8         	b	0x105cce <CurlSocket::decodePackage()+0x1c2> @ imm = #0x170
  105b5c: d300         	blo	0x105b60 <CurlSocket::decodePackage()+0x54> @ imm = #0x0
  105b5e: e0de         	b	0x105d1e <CurlSocket::decodePackage()+0x212> @ imm = #0x1bc
  105b60: 48c4         	ldr	r0, [pc, #0x310]        @ 0x105e74 <CurlSocket::decodePackage()+0x368>
  105b62: 2301         	movs	r3, #0x1
  105b64: 4698         	mov	r8, r3
  105b66: 4682         	mov	r10, r0
  105b68: 44fa         	add	r10, pc
  105b6a: 4650         	mov	r0, r10
  105b6c: 6803         	ldr	r3, [r0]
  105b6e: 48c2         	ldr	r0, [pc, #0x308]        @ 0x105e78 <CurlSocket::decodePackage()+0x36c>
  105b70: 469a         	mov	r10, r3
  105b72: 4bc2         	ldr	r3, [pc, #0x308]        @ 0x105e7c <CurlSocket::decodePackage()+0x370>
  105b74: 4681         	mov	r9, r0
  105b76: 18ee         	adds	r6, r5, r3
  105b78: 4bc1         	ldr	r3, [pc, #0x304]        @ 0x105e80 <CurlSocket::decodePackage()+0x374>
  105b7a: 469b         	mov	r11, r3
  105b7c: e05f         	b	0x105c3e <CurlSocket::decodePackage()+0x132> @ imm = #0xbe
  105b7e: 1c21         	adds	r1, r4, #0x0
  105b80: ab06         	add	r3, sp, #0x18
  105b82: a811         	add	r0, sp, #0x44
  105b84: f28d e888    	blx	0x392c98 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x256c4> @ imm = #0x28d110
  105b88: 6871         	ldr	r1, [r6, #0x4]
  105b8a: 68b3         	ldr	r3, [r6, #0x8]
  105b8c: 4299         	cmp	r1, r3
  105b8e: d100         	bne	0x105b92 <CurlSocket::decodePackage()+0x86> @ imm = #0x0
  105b90: e098         	b	0x105cc4 <CurlSocket::decodePackage()+0x1b8> @ imm = #0x130
  105b92: 2300         	movs	r3, #0x0
  105b94: 2900         	cmp	r1, #0x0
  105b96: d004         	beq	0x105ba2 <CurlSocket::decodePackage()+0x96> @ imm = #0x8
  105b98: 1c08         	adds	r0, r1, #0x0
  105b9a: a911         	add	r1, sp, #0x44
  105b9c: f28c edc2    	blx	0x392724 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x25150> @ imm = #0x28cb84
  105ba0: 6873         	ldr	r3, [r6, #0x4]
  105ba2: 3304         	adds	r3, #0x4
  105ba4: 6073         	str	r3, [r6, #0x4]
  105ba6: 9811         	ldr	r0, [sp, #0x44]
  105ba8: 1c07         	adds	r7, r0, #0x0
  105baa: 3f0c         	subs	r7, #0xc
  105bac: 4557         	cmp	r7, r10
  105bae: d000         	beq	0x105bb2 <CurlSocket::decodePackage()+0xa6> @ imm = #0x0
  105bb0: e128         	b	0x105e04 <CurlSocket::decodePackage()+0x2f8> @ imm = #0x250
  105bb2: 78e1         	ldrb	r1, [r4, #0x3]
  105bb4: 78a3         	ldrb	r3, [r4, #0x2]
  105bb6: 4fae         	ldr	r7, [pc, #0x2b8]        @ 0x105e70 <CurlSocket::decodePackage()+0x364>
  105bb8: 0209         	lsls	r1, r1, #0x8
  105bba: 4319         	orrs	r1, r3
  105bbc: 7923         	ldrb	r3, [r4, #0x4]
  105bbe: 59ea         	ldr	r2, [r5, r7]
  105bc0: 1c20         	adds	r0, r4, #0x0
  105bc2: 041b         	lsls	r3, r3, #0x10
  105bc4: 4319         	orrs	r1, r3
  105bc6: 7963         	ldrb	r3, [r4, #0x5]
  105bc8: 061b         	lsls	r3, r3, #0x18
  105bca: 4319         	orrs	r1, r3
  105bcc: 1a52         	subs	r2, r2, r1
  105bce: 3199         	adds	r1, #0x99
  105bd0: 31ff         	adds	r1, #0xff
  105bd2: 51ea         	str	r2, [r5, r7]
  105bd4: 1869         	adds	r1, r5, r1
  105bd6: f7e8 efae    	blx	0xeeb34 <.plt+0x17c>    @ imm = #-0x170a4
  105bda: 78e3         	ldrb	r3, [r4, #0x3]
  105bdc: 78a1         	ldrb	r1, [r4, #0x2]
  105bde: 4648         	mov	r0, r9
  105be0: 021b         	lsls	r3, r3, #0x8
  105be2: 430b         	orrs	r3, r1
  105be4: 7921         	ldrb	r1, [r4, #0x4]
  105be6: 4478         	add	r0, pc
  105be8: 59ea         	ldr	r2, [r5, r7]
  105bea: 0409         	lsls	r1, r1, #0x10
  105bec: 430b         	orrs	r3, r1
  105bee: 7961         	ldrb	r1, [r4, #0x5]
  105bf0: 0609         	lsls	r1, r1, #0x18
  105bf2: 430b         	orrs	r3, r1
  105bf4: 4641         	mov	r1, r8
  105bf6: f08b fdbf    	bl	0x191778 <cocos2d::CCLog(char const*, ...)> @ imm = #0x8bb7e
  105bfa: 2301         	movs	r3, #0x1
  105bfc: 4498         	add	r8, r3
  105bfe: 4ba1         	ldr	r3, [pc, #0x284]        @ 0x105e84 <CurlSocket::decodePackage()+0x378>
  105c00: 4598         	cmp	r8, r3
  105c02: d100         	bne	0x105c06 <CurlSocket::decodePackage()+0xfa> @ imm = #0x0
  105c04: e0ae         	b	0x105d64 <CurlSocket::decodePackage()+0x258> @ imm = #0x15c
  105c06: 23cc         	movs	r3, #0xcc
  105c08: 005b         	lsls	r3, r3, #0x1
  105c0a: 7861         	ldrb	r1, [r4, #0x1]
  105c0c: 5ceb         	ldrb	r3, [r5, r3]
  105c0e: 4a97         	ldr	r2, [pc, #0x25c]        @ 0x105e6c <CurlSocket::decodePackage()+0x360>
  105c10: 0209         	lsls	r1, r1, #0x8
  105c12: 4319         	orrs	r1, r3
  105c14: 1c0b         	adds	r3, r1, #0x0
  105c16: 3b14         	subs	r3, #0x14
  105c18: 041b         	lsls	r3, r3, #0x10
  105c1a: 0c1b         	lsrs	r3, r3, #0x10
  105c1c: 4293         	cmp	r3, r2
  105c1e: d900         	bls	0x105c22 <CurlSocket::decodePackage()+0x116> @ imm = #0x0
  105c20: e093         	b	0x105d4a <CurlSocket::decodePackage()+0x23e> @ imm = #0x126
  105c22: 78e2         	ldrb	r2, [r4, #0x3]
  105c24: 78a3         	ldrb	r3, [r4, #0x2]
  105c26: 0212         	lsls	r2, r2, #0x8
  105c28: 431a         	orrs	r2, r3
  105c2a: 7923         	ldrb	r3, [r4, #0x4]
  105c2c: 041b         	lsls	r3, r3, #0x10
  105c2e: 431a         	orrs	r2, r3
  105c30: 7963         	ldrb	r3, [r4, #0x5]
  105c32: 061b         	lsls	r3, r3, #0x18
  105c34: 431a         	orrs	r2, r3
  105c36: 59eb         	ldr	r3, [r5, r7]
  105c38: 429a         	cmp	r2, r3
  105c3a: d050         	beq	0x105cde <CurlSocket::decodePackage()+0x1d2> @ imm = #0xa0
  105c3c: d26f         	bhs	0x105d1e <CurlSocket::decodePackage()+0x212> @ imm = #0xde
  105c3e: 4559         	cmp	r1, r11
  105c40: d19d         	bne	0x105b7e <CurlSocket::decodePackage()+0x72> @ imm = #-0xc6
  105c42: 7ae3         	ldrb	r3, [r4, #0xb]
  105c44: 7aa1         	ldrb	r1, [r4, #0xa]
  105c46: 021b         	lsls	r3, r3, #0x8
  105c48: 430b         	orrs	r3, r1
  105c4a: 7b21         	ldrb	r1, [r4, #0xc]
  105c4c: 0409         	lsls	r1, r1, #0x10
  105c4e: 430b         	orrs	r3, r1
  105c50: 7b61         	ldrb	r1, [r4, #0xd]
  105c52: 0609         	lsls	r1, r1, #0x18
  105c54: 430b         	orrs	r3, r1
  105c56: 2b00         	cmp	r3, #0x0
  105c58: dd68         	ble	0x105d2c <CurlSocket::decodePackage()+0x220> @ imm = #0xd0
  105c5a: 20d3         	movs	r0, #0xd3
  105c5c: 0040         	lsls	r0, r0, #0x1
  105c5e: 1829         	adds	r1, r5, r0
  105c60: 1c1a         	adds	r2, r3, #0x0
  105c62: a810         	add	r0, sp, #0x40
  105c64: ab05         	add	r3, sp, #0x14
  105c66: af0f         	add	r7, sp, #0x3c
  105c68: f28d e816    	blx	0x392c98 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x256c4> @ imm = #0x28d02c
  105c6c: 1c38         	adds	r0, r7, #0x0
  105c6e: aa10         	add	r2, sp, #0x40
  105c70: 1c29         	adds	r1, r5, #0x0
  105c72: f7ff fda9    	bl	0x1057c8 <CurlSocket::unzipPack(std::string const&)> @ imm = #-0x4ae
  105c76: 9810         	ldr	r0, [sp, #0x40]
  105c78: 1c02         	adds	r2, r0, #0x0
  105c7a: 3a0c         	subs	r2, #0xc
  105c7c: 9201         	str	r2, [sp, #0x4]
  105c7e: 4552         	cmp	r2, r10
  105c80: d000         	beq	0x105c84 <CurlSocket::decodePackage()+0x178> @ imm = #0x0
  105c82: e0cc         	b	0x105e1e <CurlSocket::decodePackage()+0x312> @ imm = #0x198
  105c84: 6871         	ldr	r1, [r6, #0x4]
  105c86: 68b3         	ldr	r3, [r6, #0x8]
  105c88: 4299         	cmp	r1, r3
  105c8a: d059         	beq	0x105d40 <CurlSocket::decodePackage()+0x234> @ imm = #0xb2
  105c8c: 2300         	movs	r3, #0x0
  105c8e: 2900         	cmp	r1, #0x0
  105c90: d004         	beq	0x105c9c <CurlSocket::decodePackage()+0x190> @ imm = #0x8
  105c92: 1c08         	adds	r0, r1, #0x0
  105c94: 1c39         	adds	r1, r7, #0x0
  105c96: f28c ed46    	blx	0x392724 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x25150> @ imm = #0x28ca8c
  105c9a: 6873         	ldr	r3, [r6, #0x4]
  105c9c: 3304         	adds	r3, #0x4
  105c9e: 6073         	str	r3, [r6, #0x4]
  105ca0: 6838         	ldr	r0, [r7]
  105ca2: 1c07         	adds	r7, r0, #0x0
  105ca4: 3f0c         	subs	r7, #0xc
  105ca6: 4557         	cmp	r7, r10
  105ca8: d083         	beq	0x105bb2 <CurlSocket::decodePackage()+0xa6> @ imm = #-0xfa
  105caa: 2101         	movs	r1, #0x1
  105cac: 3804         	subs	r0, #0x4
  105cae: 4249         	rsbs	r1, r1, #0
  105cb0: f2af eba0    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x2af740
  105cb4: 2800         	cmp	r0, #0x0
  105cb6: dd00         	ble	0x105cba <CurlSocket::decodePackage()+0x1ae> @ imm = #0x0
  105cb8: e77b         	b	0x105bb2 <CurlSocket::decodePackage()+0xa6> @ imm = #-0x10a
  105cba: 1c38         	adds	r0, r7, #0x0
  105cbc: a90b         	add	r1, sp, #0x2c
  105cbe: f28b ec62    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x28b8c4
  105cc2: e776         	b	0x105bb2 <CurlSocket::decodePackage()+0xa6> @ imm = #-0x114
  105cc4: 1c30         	adds	r0, r6, #0x0
  105cc6: aa11         	add	r2, sp, #0x44
  105cc8: f7fd fda6    	bl	0x103818 <std::vector<std::string, std::allocator<std::string>>::_M_insert_aux(__gnu_cxx::__normal_iterator<std::string*, std::vector<std::string, std::allocator<std::string>>>, std::string const&)> @ imm = #-0x24b4
  105ccc: e76b         	b	0x105ba6 <CurlSocket::decodePackage()+0x9a> @ imm = #-0x12a
  105cce: 4b6e         	ldr	r3, [pc, #0x1b8]        @ 0x105e88 <CurlSocket::decodePackage()+0x37c>
  105cd0: 469a         	mov	r10, r3
  105cd2: 44fa         	add	r10, pc
  105cd4: 4653         	mov	r3, r10
  105cd6: 6818         	ldr	r0, [r3]
  105cd8: 4682         	mov	r10, r0
  105cda: 4868         	ldr	r0, [pc, #0x1a0]        @ 0x105e7c <CurlSocket::decodePackage()+0x370>
  105cdc: 182e         	adds	r6, r5, r0
  105cde: 4b68         	ldr	r3, [pc, #0x1a0]        @ 0x105e80 <CurlSocket::decodePackage()+0x374>
  105ce0: 4299         	cmp	r1, r3
  105ce2: d04a         	beq	0x105d7a <CurlSocket::decodePackage()+0x26e> @ imm = #0x94
  105ce4: 1c21         	adds	r1, r4, #0x0
  105ce6: ab04         	add	r3, sp, #0x10
  105ce8: a80e         	add	r0, sp, #0x38
  105cea: f28c efd6    	blx	0x392c98 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x256c4> @ imm = #0x28cfac
  105cee: 6871         	ldr	r1, [r6, #0x4]
  105cf0: 68b3         	ldr	r3, [r6, #0x8]
  105cf2: 4299         	cmp	r1, r3
  105cf4: d100         	bne	0x105cf8 <CurlSocket::decodePackage()+0x1ec> @ imm = #0x0
  105cf6: e07b         	b	0x105df0 <CurlSocket::decodePackage()+0x2e4> @ imm = #0xf6
  105cf8: 2300         	movs	r3, #0x0
  105cfa: 2900         	cmp	r1, #0x0
  105cfc: d004         	beq	0x105d08 <CurlSocket::decodePackage()+0x1fc> @ imm = #0x8
  105cfe: 1c08         	adds	r0, r1, #0x0
  105d00: a90e         	add	r1, sp, #0x38
  105d02: f28c ed10    	blx	0x392724 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x25150> @ imm = #0x28ca20
  105d06: 6873         	ldr	r3, [r6, #0x4]
  105d08: 3304         	adds	r3, #0x4
  105d0a: 6073         	str	r3, [r6, #0x4]
  105d0c: 980e         	ldr	r0, [sp, #0x38]
  105d0e: 1c04         	adds	r4, r0, #0x0
  105d10: 3c0c         	subs	r4, #0xc
  105d12: 4554         	cmp	r4, r10
  105d14: d000         	beq	0x105d18 <CurlSocket::decodePackage()+0x20c> @ imm = #0x0
  105d16: e08f         	b	0x105e38 <CurlSocket::decodePackage()+0x32c> @ imm = #0x11e
  105d18: 1c28         	adds	r0, r5, #0x0
  105d1a: f7ff fd45    	bl	0x1057a8 <CurlSocket::cleanRecvBuff()> @ imm = #-0x576
  105d1e: b013         	add	sp, #0x4c
  105d20: bc3c         	pop	{r2, r3, r4, r5}
  105d22: 4690         	mov	r8, r2
  105d24: 4699         	mov	r9, r3
  105d26: 46a2         	mov	r10, r4
  105d28: 46ab         	mov	r11, r5
  105d2a: bdf0         	pop	{r4, r5, r6, r7, pc}
  105d2c: 1c13         	adds	r3, r2, #0x0
  105d2e: 3b0a         	subs	r3, #0xa
  105d30: 0a1a         	lsrs	r2, r3, #0x8
  105d32: 72e2         	strb	r2, [r4, #0xb]
  105d34: 0c1a         	lsrs	r2, r3, #0x10
  105d36: 7322         	strb	r2, [r4, #0xc]
  105d38: 0e1a         	lsrs	r2, r3, #0x18
  105d3a: 72a3         	strb	r3, [r4, #0xa]
  105d3c: 7362         	strb	r2, [r4, #0xd]
  105d3e: e78c         	b	0x105c5a <CurlSocket::decodePackage()+0x14e> @ imm = #-0xe8
  105d40: 1c30         	adds	r0, r6, #0x0
  105d42: 1c3a         	adds	r2, r7, #0x0
  105d44: f7fd fd68    	bl	0x103818 <std::vector<std::string, std::allocator<std::string>>::_M_insert_aux(__gnu_cxx::__normal_iterator<std::string*, std::vector<std::string, std::allocator<std::string>>>, std::string const&)> @ imm = #-0x2530
  105d48: e7aa         	b	0x105ca0 <CurlSocket::decodePackage()+0x194> @ imm = #-0xac
  105d4a: 4850         	ldr	r0, [pc, #0x140]        @ 0x105e8c <CurlSocket::decodePackage()+0x380>
  105d4c: 4478         	add	r0, pc
  105d4e: f08b fd13    	bl	0x191778 <cocos2d::CCLog(char const*, ...)> @ imm = #0x8ba26
  105d52: 236a         	movs	r3, #0x6a
  105d54: 1c28         	adds	r0, r5, #0x0
  105d56: 60ab         	str	r3, [r5, #0x8]
  105d58: f7ff fa78    	bl	0x10524c <CurlSocket::disable()> @ imm = #-0xb10
  105d5c: 1c28         	adds	r0, r5, #0x0
  105d5e: f7ff fd23    	bl	0x1057a8 <CurlSocket::cleanRecvBuff()> @ imm = #-0x5ba
  105d62: e7dc         	b	0x105d1e <CurlSocket::decodePackage()+0x212> @ imm = #-0x48
  105d64: 484a         	ldr	r0, [pc, #0x128]        @ 0x105e90 <CurlSocket::decodePackage()+0x384>
  105d66: 4478         	add	r0, pc
  105d68: f08b fd06    	bl	0x191778 <cocos2d::CCLog(char const*, ...)> @ imm = #0x8ba0c
  105d6c: 1c28         	adds	r0, r5, #0x0
  105d6e: f7ff fa6d    	bl	0x10524c <CurlSocket::disable()> @ imm = #-0xb26
  105d72: 1c28         	adds	r0, r5, #0x0
  105d74: f7ff fd18    	bl	0x1057a8 <CurlSocket::cleanRecvBuff()> @ imm = #-0x5d0
  105d78: e7d1         	b	0x105d1e <CurlSocket::decodePackage()+0x212> @ imm = #-0x5e
  105d7a: 22d3         	movs	r2, #0xd3
  105d7c: 0052         	lsls	r2, r2, #0x1
  105d7e: 18a9         	adds	r1, r5, r2
  105d80: 7ae2         	ldrb	r2, [r4, #0xb]
  105d82: 7aa3         	ldrb	r3, [r4, #0xa]
  105d84: a80d         	add	r0, sp, #0x34
  105d86: 0212         	lsls	r2, r2, #0x8
  105d88: 431a         	orrs	r2, r3
  105d8a: 7b23         	ldrb	r3, [r4, #0xc]
  105d8c: af0f         	add	r7, sp, #0x3c
  105d8e: 041b         	lsls	r3, r3, #0x10
  105d90: 431a         	orrs	r2, r3
  105d92: 7b63         	ldrb	r3, [r4, #0xd]
  105d94: 061b         	lsls	r3, r3, #0x18
  105d96: 431a         	orrs	r2, r3
  105d98: ab03         	add	r3, sp, #0xc
  105d9a: f28c ef7e    	blx	0x392c98 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x256c4> @ imm = #0x28cefc
  105d9e: 1c38         	adds	r0, r7, #0x0
  105da0: 1c29         	adds	r1, r5, #0x0
  105da2: aa0d         	add	r2, sp, #0x34
  105da4: f7ff fd10    	bl	0x1057c8 <CurlSocket::unzipPack(std::string const&)> @ imm = #-0x5e0
  105da8: 980d         	ldr	r0, [sp, #0x34]
  105daa: 1c04         	adds	r4, r0, #0x0
  105dac: 3c0c         	subs	r4, #0xc
  105dae: 4554         	cmp	r4, r10
  105db0: d14f         	bne	0x105e52 <CurlSocket::decodePackage()+0x346> @ imm = #0x9e
  105db2: 6871         	ldr	r1, [r6, #0x4]
  105db4: 68b3         	ldr	r3, [r6, #0x8]
  105db6: 4299         	cmp	r1, r3
  105db8: d01f         	beq	0x105dfa <CurlSocket::decodePackage()+0x2ee> @ imm = #0x3e
  105dba: 2300         	movs	r3, #0x0
  105dbc: 2900         	cmp	r1, #0x0
  105dbe: d004         	beq	0x105dca <CurlSocket::decodePackage()+0x2be> @ imm = #0x8
  105dc0: 1c08         	adds	r0, r1, #0x0
  105dc2: 1c39         	adds	r1, r7, #0x0
  105dc4: f28c ecae    	blx	0x392724 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x25150> @ imm = #0x28c95c
  105dc8: 6873         	ldr	r3, [r6, #0x4]
  105dca: 3304         	adds	r3, #0x4
  105dcc: 6073         	str	r3, [r6, #0x4]
  105dce: 980f         	ldr	r0, [sp, #0x3c]
  105dd0: 1c04         	adds	r4, r0, #0x0
  105dd2: 3c0c         	subs	r4, #0xc
  105dd4: 4554         	cmp	r4, r10
  105dd6: d09f         	beq	0x105d18 <CurlSocket::decodePackage()+0x20c> @ imm = #-0xc2
  105dd8: 2101         	movs	r1, #0x1
  105dda: 3804         	subs	r0, #0x4
  105ddc: 4249         	rsbs	r1, r1, #0
  105dde: f2af eb0a    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x2af614
  105de2: 2800         	cmp	r0, #0x0
  105de4: dc98         	bgt	0x105d18 <CurlSocket::decodePackage()+0x20c> @ imm = #-0xd0
  105de6: 1c20         	adds	r0, r4, #0x0
  105de8: a908         	add	r1, sp, #0x20
  105dea: f28b ebcc    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x28b798
  105dee: e793         	b	0x105d18 <CurlSocket::decodePackage()+0x20c> @ imm = #-0xda
  105df0: 1c30         	adds	r0, r6, #0x0
  105df2: aa0e         	add	r2, sp, #0x38
  105df4: f7fd fd10    	bl	0x103818 <std::vector<std::string, std::allocator<std::string>>::_M_insert_aux(__gnu_cxx::__normal_iterator<std::string*, std::vector<std::string, std::allocator<std::string>>>, std::string const&)> @ imm = #-0x25e0
  105df8: e788         	b	0x105d0c <CurlSocket::decodePackage()+0x200> @ imm = #-0xf0
  105dfa: 1c30         	adds	r0, r6, #0x0
  105dfc: 1c3a         	adds	r2, r7, #0x0
  105dfe: f7fd fd0b    	bl	0x103818 <std::vector<std::string, std::allocator<std::string>>::_M_insert_aux(__gnu_cxx::__normal_iterator<std::string*, std::vector<std::string, std::allocator<std::string>>>, std::string const&)> @ imm = #-0x25ea
  105e02: e7e4         	b	0x105dce <CurlSocket::decodePackage()+0x2c2> @ imm = #-0x38
  105e04: 2101         	movs	r1, #0x1
  105e06: 3804         	subs	r0, #0x4
  105e08: 4249         	rsbs	r1, r1, #0
  105e0a: f2af eaf4    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x2af5e8
  105e0e: 2800         	cmp	r0, #0x0
  105e10: dd00         	ble	0x105e14 <CurlSocket::decodePackage()+0x308> @ imm = #0x0
  105e12: e6ce         	b	0x105bb2 <CurlSocket::decodePackage()+0xa6> @ imm = #-0x264
  105e14: 1c38         	adds	r0, r7, #0x0
  105e16: a90c         	add	r1, sp, #0x30
  105e18: f28b ebb4    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x28b768
  105e1c: e6c9         	b	0x105bb2 <CurlSocket::decodePackage()+0xa6> @ imm = #-0x26e
  105e1e: 2101         	movs	r1, #0x1
  105e20: 3804         	subs	r0, #0x4
  105e22: 4249         	rsbs	r1, r1, #0
  105e24: f2af eae6    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x2af5cc
  105e28: 2800         	cmp	r0, #0x0
  105e2a: dd00         	ble	0x105e2e <CurlSocket::decodePackage()+0x322> @ imm = #0x0
  105e2c: e72a         	b	0x105c84 <CurlSocket::decodePackage()+0x178> @ imm = #-0x1ac
  105e2e: 9801         	ldr	r0, [sp, #0x4]
  105e30: a90a         	add	r1, sp, #0x28
  105e32: f28b eba8    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x28b750
  105e36: e725         	b	0x105c84 <CurlSocket::decodePackage()+0x178> @ imm = #-0x1b6
  105e38: 2101         	movs	r1, #0x1
  105e3a: 3804         	subs	r0, #0x4
  105e3c: 4249         	rsbs	r1, r1, #0
  105e3e: f2af eada    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x2af5b4
  105e42: 2800         	cmp	r0, #0x0
  105e44: dd00         	ble	0x105e48 <CurlSocket::decodePackage()+0x33c> @ imm = #0x0
  105e46: e767         	b	0x105d18 <CurlSocket::decodePackage()+0x20c> @ imm = #-0x132
  105e48: 1c20         	adds	r0, r4, #0x0
  105e4a: a909         	add	r1, sp, #0x24
  105e4c: f28b eb9a    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x28b734
  105e50: e762         	b	0x105d18 <CurlSocket::decodePackage()+0x20c> @ imm = #-0x13c
  105e52: 2101         	movs	r1, #0x1
  105e54: 3804         	subs	r0, #0x4
  105e56: 4249         	rsbs	r1, r1, #0
  105e58: f2af eacc    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x2af598
  105e5c: 2800         	cmp	r0, #0x0
  105e5e: dca8         	bgt	0x105db2 <CurlSocket::decodePackage()+0x2a6> @ imm = #-0xb0
  105e60: 1c20         	adds	r0, r4, #0x0
  105e62: a907         	add	r1, sp, #0x1c
  105e64: f28b eb8e    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x28b71c
  105e68: e7a3         	b	0x105db2 <CurlSocket::decodePackage()+0x2a6> @ imm = #-0xba
  105e6a: 46c0         	mov	r8, r8
  105e6c: 4e0b         	ldr	r6, [pc, #0x2c]         @ 0x105e9c <CurlSocket::readMsg()+0x8>
  105e6e: 0000         	movs	r0, r0
  105e70: 8198         	strh	r0, [r3, #0xc]
  105e72: 0000         	movs	r0, r0
  105e74: 6a0c         	ldr	r4, [r1, #0x20]
  105e76: 0038         	movs	r0, r7
  105e78: 4476         	add	r6, lr
  105e7a: 002b         	movs	r3, r5
  105e7c: 81bc         	strh	r4, [r7, #0xc]
  105e7e: 0000         	movs	r0, r0
  105e80: 0bb8         	lsrs	r0, r7, #0xe
  105e82: 0000         	movs	r0, r0
  105e84: 0101         	lsls	r1, r0, #0x4
  105e86: 0000         	movs	r0, r0
  105e88: 68a2         	ldr	r2, [r4, #0x8]
  105e8a: 0038         	movs	r0, r7
  105e8c: 42f4         	cmn	r4, r6
  105e8e: 002b         	movs	r3, r5
  105e90: 42b6         	cmp	r6, r6
  105e92: 002b         	movs	r3, r5


jgbol3.87/lib/armeabi/libxiyoujilua.so:	file format elf32-littlearm

Disassembly of section .text:

00101ddc <LuaInterface::SizeOf(FieldValue*)>:
  101ddc: b510         	push	{r4, lr}
  101dde: 7c0b         	ldrb	r3, [r1, #0x10]
  101de0: 1c0c         	adds	r4, r1, #0x0
  101de2: 2200         	movs	r2, #0x0
  101de4: 2b00         	cmp	r3, #0x0
  101de6: d105         	bne	0x101df4 <LuaInterface::SizeOf(FieldValue*)+0x18> @ imm = #0xa
  101de8: 780b         	ldrb	r3, [r1]
  101dea: 2b6c         	cmp	r3, #0x6c
  101dec: d001         	beq	0x101df2 <LuaInterface::SizeOf(FieldValue*)+0x16> @ imm = #0x2
  101dee: 2b42         	cmp	r3, #0x42
  101df0: d102         	bne	0x101df8 <LuaInterface::SizeOf(FieldValue*)+0x1c> @ imm = #0x4
  101df2: 68a2         	ldr	r2, [r4, #0x8]
  101df4: 1c10         	adds	r0, r2, #0x0
  101df6: bd10         	pop	{r4, pc}
  101df8: 2b62         	cmp	r3, #0x62
  101dfa: d0fa         	beq	0x101df2 <LuaInterface::SizeOf(FieldValue*)+0x16> @ imm = #-0xc
  101dfc: 2b53         	cmp	r3, #0x53
  101dfe: d0f8         	beq	0x101df2 <LuaInterface::SizeOf(FieldValue*)+0x16> @ imm = #-0x10
  101e00: 2b4e         	cmp	r3, #0x4e
  101e02: d0f6         	beq	0x101df2 <LuaInterface::SizeOf(FieldValue*)+0x16> @ imm = #-0x14
  101e04: 2b57         	cmp	r3, #0x57
  101e06: d01e         	beq	0x101e46 <LuaInterface::SizeOf(FieldValue*)+0x6a> @ imm = #0x3c
  101e08: 2b77         	cmp	r3, #0x77
  101e0a: d01c         	beq	0x101e46 <LuaInterface::SizeOf(FieldValue*)+0x6a> @ imm = #0x38
  101e0c: 2b49         	cmp	r3, #0x49
  101e0e: d01d         	beq	0x101e4c <LuaInterface::SizeOf(FieldValue*)+0x70> @ imm = #0x3a
  101e10: 2b69         	cmp	r3, #0x69
  101e12: d01b         	beq	0x101e4c <LuaInterface::SizeOf(FieldValue*)+0x70> @ imm = #0x36
  101e14: 2b66         	cmp	r3, #0x66
  101e16: d019         	beq	0x101e4c <LuaInterface::SizeOf(FieldValue*)+0x70> @ imm = #0x32
  101e18: 2b64         	cmp	r3, #0x64
  101e1a: d020         	beq	0x101e5e <LuaInterface::SizeOf(FieldValue*)+0x82> @ imm = #0x40
  101e1c: 2200         	movs	r2, #0x0
  101e1e: 2b73         	cmp	r3, #0x73
  101e20: d0e8         	beq	0x101df4 <LuaInterface::SizeOf(FieldValue*)+0x18> @ imm = #-0x30
  101e22: 6861         	ldr	r1, [r4, #0x4]
  101e24: 2900         	cmp	r1, #0x0
  101e26: d0e5         	beq	0x101df4 <LuaInterface::SizeOf(FieldValue*)+0x18> @ imm = #-0x36
  101e28: 4b0e         	ldr	r3, [pc, #0x38]         @ 0x101e64 <LuaInterface::SizeOf(FieldValue*)+0x88>
  101e2a: 1e4a         	subs	r2, r1, #0x1
  101e2c: 429a         	cmp	r2, r3
  101e2e: d810         	bhi	0x101e52 <LuaInterface::SizeOf(FieldValue*)+0x76> @ imm = #0x20
  101e30: 6943         	ldr	r3, [r0, #0x14]
  101e32: 008a         	lsls	r2, r1, #0x2
  101e34: 58d3         	ldr	r3, [r2, r3]
  101e36: 2b00         	cmp	r3, #0x0
  101e38: d00b         	beq	0x101e52 <LuaInterface::SizeOf(FieldValue*)+0x76> @ imm = #0x16
  101e3a: 1c19         	adds	r1, r3, #0x0
  101e3c: f000 f816    	bl	0x101e6c <LuaInterface::SizeOf(std::vector<std::pair<std::string, FieldValue*>*, std::allocator<std::pair<std::string, FieldValue*>*>>&)> @ imm = #0x2c
  101e40: 68a2         	ldr	r2, [r4, #0x8]
  101e42: 4342         	muls	r2, r0, r2
  101e44: e7d6         	b	0x101df4 <LuaInterface::SizeOf(FieldValue*)+0x18> @ imm = #-0x54
  101e46: 68a2         	ldr	r2, [r4, #0x8]
  101e48: 0052         	lsls	r2, r2, #0x1
  101e4a: e7d3         	b	0x101df4 <LuaInterface::SizeOf(FieldValue*)+0x18> @ imm = #-0x5a
  101e4c: 68a2         	ldr	r2, [r4, #0x8]
  101e4e: 0092         	lsls	r2, r2, #0x2
  101e50: e7d0         	b	0x101df4 <LuaInterface::SizeOf(FieldValue*)+0x18> @ imm = #-0x60
  101e52: 4805         	ldr	r0, [pc, #0x14]         @ 0x101e68 <LuaInterface::SizeOf(FieldValue*)+0x8c>
  101e54: 4478         	add	r0, pc
  101e56: f08f fc8f    	bl	0x191778 <cocos2d::CCLog(char const*, ...)> @ imm = #0x8f91e
  101e5a: 2200         	movs	r2, #0x0
  101e5c: e7ca         	b	0x101df4 <LuaInterface::SizeOf(FieldValue*)+0x18> @ imm = #-0x6c
  101e5e: 68a2         	ldr	r2, [r4, #0x8]
  101e60: 00d2         	lsls	r2, r2, #0x3
  101e62: e7c7         	b	0x101df4 <LuaInterface::SizeOf(FieldValue*)+0x18> @ imm = #-0x72
  101e64: 270f         	movs	r7, #0xf
  101e66: 0000         	movs	r0, r0
  101e68: 72d8         	strb	r0, [r3, #0xb]
  101e6a: 002b         	movs	r3, r5


jgbol3.87/lib/armeabi/libxiyoujilua.so:	file format elf32-littlearm

Disassembly of section .text:

00101ea4 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)>:
  101ea4: b5f0         	push	{r4, r5, r6, r7, lr}
  101ea6: 465f         	mov	r7, r11
  101ea8: 4656         	mov	r6, r10
  101eaa: 464d         	mov	r5, r9
  101eac: 4644         	mov	r4, r8
  101eae: b4f0         	push	{r4, r5, r6, r7}
  101eb0: b085         	sub	sp, #0x14
  101eb2: 9101         	str	r1, [sp, #0x4]
  101eb4: 4970         	ldr	r1, [pc, #0x1c0]        @ 0x102078 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x1d4>
  101eb6: 1c1e         	adds	r6, r3, #0x0
  101eb8: 230a         	movs	r3, #0xa
  101eba: 468a         	mov	r10, r1
  101ebc: 44fa         	add	r10, pc
  101ebe: 6033         	str	r3, [r6]
  101ec0: 4653         	mov	r3, r10
  101ec2: 4693         	mov	r11, r2
  101ec4: 681a         	ldr	r2, [r3]
  101ec6: 9901         	ldr	r1, [sp, #0x4]
  101ec8: 4680         	mov	r8, r0
  101eca: 6813         	ldr	r3, [r2]
  101ecc: 4692         	mov	r10, r2
  101ece: 008a         	lsls	r2, r1, #0x2
  101ed0: 695b         	ldr	r3, [r3, #0x14]
  101ed2: 2000         	movs	r0, #0x0
  101ed4: 58d5         	ldr	r5, [r2, r3]
  101ed6: 2d00         	cmp	r5, #0x0
  101ed8: d05b         	beq	0x101f92 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0xee> @ imm = #0xb6
  101eda: 682b         	ldr	r3, [r5]
  101edc: 686a         	ldr	r2, [r5, #0x4]
  101ede: 1ad2         	subs	r2, r2, r3
  101ee0: 1092         	asrs	r2, r2, #0x2
  101ee2: d100         	bne	0x101ee6 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x42> @ imm = #0x0
  101ee4: e0c6         	b	0x102074 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x1d0> @ imm = #0x18c
  101ee6: 2400         	movs	r4, #0x0
  101ee8: e00a         	b	0x101f00 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x5c> @ imm = #0x14
  101eea: 6832         	ldr	r2, [r6]
  101eec: 68db         	ldr	r3, [r3, #0xc]
  101eee: 18d3         	adds	r3, r2, r3
  101ef0: 6033         	str	r3, [r6]
  101ef2: 682b         	ldr	r3, [r5]
  101ef4: 686a         	ldr	r2, [r5, #0x4]
  101ef6: 3401         	adds	r4, #0x1
  101ef8: 1ad2         	subs	r2, r2, r3
  101efa: 1092         	asrs	r2, r2, #0x2
  101efc: 4294         	cmp	r4, r2
  101efe: d245         	bhs	0x101f8c <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0xe8> @ imm = #0x8a
  101f00: 00a7         	lsls	r7, r4, #0x2
  101f02: 59da         	ldr	r2, [r3, r7]
  101f04: 6853         	ldr	r3, [r2, #0x4]
  101f06: 7819         	ldrb	r1, [r3]
  101f08: 2973         	cmp	r1, #0x73
  101f0a: d049         	beq	0x101fa0 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0xfc> @ imm = #0x92
  101f0c: 7c19         	ldrb	r1, [r3, #0x10]
  101f0e: 2900         	cmp	r1, #0x0
  101f10: d0eb         	beq	0x101eea <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x46> @ imm = #-0x2a
  101f12: 4659         	mov	r1, r11
  101f14: 6812         	ldr	r2, [r2]
  101f16: 4640         	mov	r0, r8
  101f18: f0d1 edf6    	blx	0x1d3b08 <lua_getfield> @ imm = #0xd1bec
  101f1c: 4640         	mov	r0, r8
  101f1e: f0d0 eb1a    	blx	0x1d2554 <lua_gettop>   @ imm = #0xd0634
  101f22: 4681         	mov	r9, r0
  101f24: 4649         	mov	r1, r9
  101f26: 4640         	mov	r0, r8
  101f28: f0d0 ec66    	blx	0x1d27f8 <lua_type>     @ imm = #0xd08cc
  101f2c: 2800         	cmp	r0, #0x0
  101f2e: d100         	bne	0x101f32 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x8e> @ imm = #0x0
  101f30: e081         	b	0x102036 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x192> @ imm = #0x102
  101f32: 4649         	mov	r1, r9
  101f34: 4640         	mov	r0, r8
  101f36: f0d1 e97c    	blx	0x1d3230 <lua_objlen>   @ imm = #0xd12f8
  101f3a: 682b         	ldr	r3, [r5]
  101f3c: 4681         	mov	r9, r0
  101f3e: 59db         	ldr	r3, [r3, r7]
  101f40: 685b         	ldr	r3, [r3, #0x4]
  101f42: 689a         	ldr	r2, [r3, #0x8]
  101f44: 4290         	cmp	r0, r2
  101f46: d900         	bls	0x101f4a <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0xa6> @ imm = #0x0
  101f48: e080         	b	0x10204c <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x1a8> @ imm = #0x100
  101f4a: 2102         	movs	r1, #0x2
  101f4c: 4640         	mov	r0, r8
  101f4e: 4249         	rsbs	r1, r1, #0
  101f50: f0d0 eb0a    	blx	0x1d2568 <lua_settop>   @ imm = #0xd0614
  101f54: 682b         	ldr	r3, [r5]
  101f56: 59db         	ldr	r3, [r3, r7]
  101f58: 685a         	ldr	r2, [r3, #0x4]
  101f5a: 7813         	ldrb	r3, [r2]
  101f5c: 6852         	ldr	r2, [r2, #0x4]
  101f5e: 2b6c         	cmp	r3, #0x6c
  101f60: d00a         	beq	0x101f78 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0xd4> @ imm = #0x14
  101f62: 2b42         	cmp	r3, #0x42
  101f64: d008         	beq	0x101f78 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0xd4> @ imm = #0x10
  101f66: 2b62         	cmp	r3, #0x62
  101f68: d006         	beq	0x101f78 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0xd4> @ imm = #0xc
  101f6a: 2b57         	cmp	r3, #0x57
  101f6c: d001         	beq	0x101f72 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0xce> @ imm = #0x2
  101f6e: 2b77         	cmp	r3, #0x77
  101f70: d137         	bne	0x101fe2 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x13e> @ imm = #0x6e
  101f72: 464b         	mov	r3, r9
  101f74: 005b         	lsls	r3, r3, #0x1
  101f76: 4699         	mov	r9, r3
  101f78: 6833         	ldr	r3, [r6]
  101f7a: 3401         	adds	r4, #0x1
  101f7c: 444b         	add	r3, r9
  101f7e: 6033         	str	r3, [r6]
  101f80: 682b         	ldr	r3, [r5]
  101f82: 686a         	ldr	r2, [r5, #0x4]
  101f84: 1ad2         	subs	r2, r2, r3
  101f86: 1092         	asrs	r2, r2, #0x2
  101f88: 4294         	cmp	r4, r2
  101f8a: d3b9         	blo	0x101f00 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x5c> @ imm = #-0x8e
  101f8c: 6830         	ldr	r0, [r6]
  101f8e: f2a5 ea74    	blx	0x3a7478 <operator new[](unsigned int)> @ imm = #0x2a54e8
  101f92: b005         	add	sp, #0x14
  101f94: bc3c         	pop	{r2, r3, r4, r5}
  101f96: 4690         	mov	r8, r2
  101f98: 4699         	mov	r9, r3
  101f9a: 46a2         	mov	r10, r4
  101f9c: 46ab         	mov	r11, r5
  101f9e: bdf0         	pop	{r4, r5, r6, r7, pc}
  101fa0: 2200         	movs	r2, #0x0
  101fa2: 9203         	str	r2, [sp, #0xc]
  101fa4: 682b         	ldr	r3, [r5]
  101fa6: 4640         	mov	r0, r8
  101fa8: 4659         	mov	r1, r11
  101faa: 59db         	ldr	r3, [r3, r7]
  101fac: 681a         	ldr	r2, [r3]
  101fae: f0d1 edac    	blx	0x1d3b08 <lua_getfield> @ imm = #0xd1b58
  101fb2: 2101         	movs	r1, #0x1
  101fb4: 4640         	mov	r0, r8
  101fb6: 4249         	rsbs	r1, r1, #0
  101fb8: f0d0 ec1e    	blx	0x1d27f8 <lua_type>     @ imm = #0xd083c
  101fbc: 2800         	cmp	r0, #0x0
  101fbe: d050         	beq	0x102062 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x1be> @ imm = #0xa0
  101fc0: 2101         	movs	r1, #0x1
  101fc2: aa03         	add	r2, sp, #0xc
  101fc4: 4640         	mov	r0, r8
  101fc6: 4249         	rsbs	r1, r1, #0
  101fc8: f0d0 efe2    	blx	0x1d2f90 <lua_tolstring> @ imm = #0xd0fc4
  101fcc: 9b03         	ldr	r3, [sp, #0xc]
  101fce: 6832         	ldr	r2, [r6]
  101fd0: 2102         	movs	r1, #0x2
  101fd2: 3301         	adds	r3, #0x1
  101fd4: 18d3         	adds	r3, r2, r3
  101fd6: 6033         	str	r3, [r6]
  101fd8: 4640         	mov	r0, r8
  101fda: 4249         	rsbs	r1, r1, #0
  101fdc: f0d0 eac4    	blx	0x1d2568 <lua_settop>   @ imm = #0xd0588
  101fe0: e787         	b	0x101ef2 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x4e> @ imm = #-0xf2
  101fe2: 2b49         	cmp	r3, #0x49
  101fe4: d01c         	beq	0x102020 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x17c> @ imm = #0x38
  101fe6: 2b69         	cmp	r3, #0x69
  101fe8: d01a         	beq	0x102020 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x17c> @ imm = #0x34
  101fea: 2b66         	cmp	r3, #0x66
  101fec: d01c         	beq	0x102028 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x184> @ imm = #0x38
  101fee: 2b64         	cmp	r3, #0x64
  101ff0: d033         	beq	0x10205a <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x1b6> @ imm = #0x66
  101ff2: 2b53         	cmp	r3, #0x53
  101ff4: d01c         	beq	0x102030 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x18c> @ imm = #0x38
  101ff6: 2b73         	cmp	r3, #0x73
  101ff8: d01a         	beq	0x102030 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x18c> @ imm = #0x34
  101ffa: 2a00         	cmp	r2, #0x0
  101ffc: d034         	beq	0x102068 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x1c4> @ imm = #0x68
  101ffe: 4b1f         	ldr	r3, [pc, #0x7c]         @ 0x10207c <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x1d8>
  102000: 4651         	mov	r1, r10
  102002: 6808         	ldr	r0, [r1]
  102004: 1e51         	subs	r1, r2, #0x1
  102006: 4299         	cmp	r1, r3
  102008: d831         	bhi	0x10206e <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x1ca> @ imm = #0x62
  10200a: 6943         	ldr	r3, [r0, #0x14]
  10200c: 0092         	lsls	r2, r2, #0x2
  10200e: 58d1         	ldr	r1, [r2, r3]
  102010: 2900         	cmp	r1, #0x0
  102012: d00d         	beq	0x102030 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x18c> @ imm = #0x1a
  102014: f7ff ff2a    	bl	0x101e6c <LuaInterface::SizeOf(std::vector<std::pair<std::string, FieldValue*>*, std::allocator<std::pair<std::string, FieldValue*>*>>&)> @ imm = #-0x1ac
  102018: 464a         	mov	r2, r9
  10201a: 4342         	muls	r2, r0, r2
  10201c: 4691         	mov	r9, r2
  10201e: e7ab         	b	0x101f78 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0xd4> @ imm = #-0xaa
  102020: 4649         	mov	r1, r9
  102022: 0089         	lsls	r1, r1, #0x2
  102024: 4689         	mov	r9, r1
  102026: e7a7         	b	0x101f78 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0xd4> @ imm = #-0xb2
  102028: 464a         	mov	r2, r9
  10202a: 0092         	lsls	r2, r2, #0x2
  10202c: 4691         	mov	r9, r2
  10202e: e7a3         	b	0x101f78 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0xd4> @ imm = #-0xba
  102030: 2300         	movs	r3, #0x0
  102032: 4699         	mov	r9, r3
  102034: e7a0         	b	0x101f78 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0xd4> @ imm = #-0xc0
  102036: 4912         	ldr	r1, [pc, #0x48]         @ 0x102080 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x1dc>
  102038: 4479         	add	r1, pc
  10203a: 682b         	ldr	r3, [r5]
  10203c: 4640         	mov	r0, r8
  10203e: 59db         	ldr	r3, [r3, r7]
  102040: 681a         	ldr	r2, [r3]
  102042: 9b01         	ldr	r3, [sp, #0x4]
  102044: f0c9 ec90    	blx	0x1cb968 <luaL_error>   @ imm = #0xc9920
  102048: 2000         	movs	r0, #0x0
  10204a: e7a2         	b	0x101f92 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0xee> @ imm = #-0xbc
  10204c: 490d         	ldr	r1, [pc, #0x34]         @ 0x102084 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x1e0>
  10204e: 4640         	mov	r0, r8
  102050: 4479         	add	r1, pc
  102052: f0c9 ec8a    	blx	0x1cb968 <luaL_error>   @ imm = #0xc9914
  102056: 2000         	movs	r0, #0x0
  102058: e79b         	b	0x101f92 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0xee> @ imm = #-0xca
  10205a: 464b         	mov	r3, r9
  10205c: 00db         	lsls	r3, r3, #0x3
  10205e: 4699         	mov	r9, r3
  102060: e78a         	b	0x101f78 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0xd4> @ imm = #-0xec
  102062: 4909         	ldr	r1, [pc, #0x24]         @ 0x102088 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x1e4>
  102064: 4479         	add	r1, pc
  102066: e7e8         	b	0x10203a <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0x196> @ imm = #-0x30
  102068: 2100         	movs	r1, #0x0
  10206a: 4689         	mov	r9, r1
  10206c: e784         	b	0x101f78 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0xd4> @ imm = #-0xf8
  10206e: 2200         	movs	r2, #0x0
  102070: 4691         	mov	r9, r2
  102072: e781         	b	0x101f78 <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0xd4> @ imm = #-0xfe
  102074: 200a         	movs	r0, #0xa
  102076: e78a         	b	0x101f8e <LuaInterface::get_msg_buffer(lua_State*, int, int, unsigned int&)+0xea> @ imm = #-0xec
  102078: a99c         	add	r1, sp, #0x270
  10207a: 0038         	movs	r0, r7
  10207c: 270f         	movs	r7, #0xf
  10207e: 0000         	movs	r0, r0
  102080: 7168         	strb	r0, [r5, #0x5]
  102082: 002b         	movs	r3, r5
  102084: 7184         	strb	r4, [r0, #0x6]
  102086: 002b         	movs	r3, r5
  102088: 7108         	strb	r0, [r1, #0x4]
  10208a: 002b         	movs	r3, r5


jgbol3.87/lib/armeabi/libxiyoujilua.so:	file format elf32-littlearm

Disassembly of section .text:

00101e6c <LuaInterface::SizeOf(std::vector<std::pair<std::string, FieldValue*>*, std::allocator<std::pair<std::string, FieldValue*>*>>&)>:
  101e6c: b5f8         	push	{r3, r4, r5, r6, r7, lr}
  101e6e: 680b         	ldr	r3, [r1]
  101e70: 684a         	ldr	r2, [r1, #0x4]
  101e72: 1c07         	adds	r7, r0, #0x0
  101e74: 1c0d         	adds	r5, r1, #0x0
  101e76: 1ad2         	subs	r2, r2, r3
  101e78: 1092         	asrs	r2, r2, #0x2
  101e7a: 2600         	movs	r6, #0x0
  101e7c: 2a00         	cmp	r2, #0x0
  101e7e: d00e         	beq	0x101e9e <LuaInterface::SizeOf(std::vector<std::pair<std::string, FieldValue*>*, std::allocator<std::pair<std::string, FieldValue*>*>>&)+0x32> @ imm = #0x1c
  101e80: 2400         	movs	r4, #0x0
  101e82: 00a2         	lsls	r2, r4, #0x2
  101e84: 58d3         	ldr	r3, [r2, r3]
  101e86: 1c38         	adds	r0, r7, #0x0
  101e88: 3401         	adds	r4, #0x1
  101e8a: 6859         	ldr	r1, [r3, #0x4]
  101e8c: f7ff ffa6    	bl	0x101ddc <LuaInterface::SizeOf(FieldValue*)> @ imm = #-0xb4
  101e90: 682b         	ldr	r3, [r5]
  101e92: 686a         	ldr	r2, [r5, #0x4]
  101e94: 1836         	adds	r6, r6, r0
  101e96: 1ad2         	subs	r2, r2, r3
  101e98: 1092         	asrs	r2, r2, #0x2
  101e9a: 4294         	cmp	r4, r2
  101e9c: d3f1         	blo	0x101e82 <LuaInterface::SizeOf(std::vector<std::pair<std::string, FieldValue*>*, std::allocator<std::pair<std::string, FieldValue*>*>>&)+0x16> @ imm = #-0x1e
  101e9e: 1c30         	adds	r0, r6, #0x0
  101ea0: bdf8         	pop	{r3, r4, r5, r6, r7, pc}


jgbol3.87/lib/armeabi/libxiyoujilua.so:	file format elf32-littlearm

Disassembly of section .text:

00105a34 <CurlSocket::send2Server(CNetwork_Msg const*)>:
  105a34: b570         	push	{r4, r5, r6, lr}
  105a36: 78ca         	ldrb	r2, [r1, #0x3]
  105a38: 788b         	ldrb	r3, [r1, #0x2]
  105a3a: 1c05         	adds	r5, r0, #0x0
  105a3c: 0212         	lsls	r2, r2, #0x8
  105a3e: 431a         	orrs	r2, r3
  105a40: 790b         	ldrb	r3, [r1, #0x4]
  105a42: b084         	sub	sp, #0x10
  105a44: 041b         	lsls	r3, r3, #0x10
  105a46: 431a         	orrs	r2, r3
  105a48: 794b         	ldrb	r3, [r1, #0x5]
  105a4a: 061b         	lsls	r3, r3, #0x18
  105a4c: 431a         	orrs	r2, r3
  105a4e: 4b29         	ldr	r3, [pc, #0xa4]         @ 0x105af4 <CurlSocket::send2Server(CNetwork_Msg const*)+0xc0>
  105a50: 1c10         	adds	r0, r2, #0x0
  105a52: 380b         	subs	r0, #0xb
  105a54: 4298         	cmp	r0, r3
  105a56: d831         	bhi	0x105abc <CurlSocket::send2Server(CNetwork_Msg const*)+0x88> @ imm = #0x62
  105a58: 4b27         	ldr	r3, [pc, #0x9c]         @ 0x105af8 <CurlSocket::send2Server(CNetwork_Msg const*)+0xc4>
  105a5a: 18ec         	adds	r4, r5, r3
  105a5c: 6860         	ldr	r0, [r4, #0x4]
  105a5e: 58eb         	ldr	r3, [r5, r3]
  105a60: 1ac3         	subs	r3, r0, r3
  105a62: 2b7f         	cmp	r3, #0x7f
  105a64: d832         	bhi	0x105acc <CurlSocket::send2Server(CNetwork_Msg const*)+0x98> @ imm = #0x64
  105a66: ab01         	add	r3, sp, #0x4
  105a68: a803         	add	r0, sp, #0xc
  105a6a: f28d e916    	blx	0x392c98 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x256c4> @ imm = #0x28d22c
  105a6e: 6861         	ldr	r1, [r4, #0x4]
  105a70: 68a3         	ldr	r3, [r4, #0x8]
  105a72: 4299         	cmp	r1, r3
  105a74: d01d         	beq	0x105ab2 <CurlSocket::send2Server(CNetwork_Msg const*)+0x7e> @ imm = #0x3a
  105a76: 2300         	movs	r3, #0x0
  105a78: 2900         	cmp	r1, #0x0
  105a7a: d004         	beq	0x105a86 <CurlSocket::send2Server(CNetwork_Msg const*)+0x52> @ imm = #0x8
  105a7c: 1c08         	adds	r0, r1, #0x0
  105a7e: a903         	add	r1, sp, #0xc
  105a80: f28c ee50    	blx	0x392724 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x25150> @ imm = #0x28cca0
  105a84: 6863         	ldr	r3, [r4, #0x4]
  105a86: 3304         	adds	r3, #0x4
  105a88: 6063         	str	r3, [r4, #0x4]
  105a8a: 4b1c         	ldr	r3, [pc, #0x70]         @ 0x105afc <CurlSocket::send2Server(CNetwork_Msg const*)+0xc8>
  105a8c: 9803         	ldr	r0, [sp, #0xc]
  105a8e: 447b         	add	r3, pc
  105a90: 681b         	ldr	r3, [r3]
  105a92: 1c06         	adds	r6, r0, #0x0
  105a94: 3e0c         	subs	r6, #0xc
  105a96: 429e         	cmp	r6, r3
  105a98: d11f         	bne	0x105ada <CurlSocket::send2Server(CNetwork_Msg const*)+0xa6> @ imm = #0x3e
  105a9a: 4b17         	ldr	r3, [pc, #0x5c]         @ 0x105af8 <CurlSocket::send2Server(CNetwork_Msg const*)+0xc4>
  105a9c: 6861         	ldr	r1, [r4, #0x4]
  105a9e: 4818         	ldr	r0, [pc, #0x60]         @ 0x105b00 <CurlSocket::send2Server(CNetwork_Msg const*)+0xcc>
  105aa0: 58eb         	ldr	r3, [r5, r3]
  105aa2: 4478         	add	r0, pc
  105aa4: 1ac9         	subs	r1, r1, r3
  105aa6: 1089         	asrs	r1, r1, #0x2
  105aa8: f08b fe66    	bl	0x191778 <cocos2d::CCLog(char const*, ...)> @ imm = #0x8bccc
  105aac: 2000         	movs	r0, #0x0
  105aae: b004         	add	sp, #0x10
  105ab0: bd70         	pop	{r4, r5, r6, pc}
  105ab2: 1c20         	adds	r0, r4, #0x0
  105ab4: aa03         	add	r2, sp, #0xc
  105ab6: f7fd feaf    	bl	0x103818 <std::vector<std::string, std::allocator<std::string>>::_M_insert_aux(__gnu_cxx::__normal_iterator<std::string*, std::vector<std::string, std::allocator<std::string>>>, std::string const&)> @ imm = #-0x22a2
  105aba: e7e6         	b	0x105a8a <CurlSocket::send2Server(CNetwork_Msg const*)+0x56> @ imm = #-0x34
  105abc: 4811         	ldr	r0, [pc, #0x44]         @ 0x105b04 <CurlSocket::send2Server(CNetwork_Msg const*)+0xd0>
  105abe: 1c11         	adds	r1, r2, #0x0
  105ac0: 4478         	add	r0, pc
  105ac2: f08b fe59    	bl	0x191778 <cocos2d::CCLog(char const*, ...)> @ imm = #0x8bcb2
  105ac6: 2001         	movs	r0, #0x1
  105ac8: 4240         	rsbs	r0, r0, #0
  105aca: e7f0         	b	0x105aae <CurlSocket::send2Server(CNetwork_Msg const*)+0x7a> @ imm = #-0x20
  105acc: 480e         	ldr	r0, [pc, #0x38]         @ 0x105b08 <CurlSocket::send2Server(CNetwork_Msg const*)+0xd4>
  105ace: 4478         	add	r0, pc
  105ad0: f08b fe52    	bl	0x191778 <cocos2d::CCLog(char const*, ...)> @ imm = #0x8bca4
  105ad4: 2002         	movs	r0, #0x2
  105ad6: 4240         	rsbs	r0, r0, #0
  105ad8: e7e9         	b	0x105aae <CurlSocket::send2Server(CNetwork_Msg const*)+0x7a> @ imm = #-0x2e
  105ada: 2101         	movs	r1, #0x1
  105adc: 3804         	subs	r0, #0x4
  105ade: 4249         	rsbs	r1, r1, #0
  105ae0: f2af ec88    	blx	0x3b53f4 <__gnu_uldivmod_helper+0x3c> @ imm = #0x2af910
  105ae4: 2800         	cmp	r0, #0x0
  105ae6: dcd8         	bgt	0x105a9a <CurlSocket::send2Server(CNetwork_Msg const*)+0x66> @ imm = #-0x50
  105ae8: 1c30         	adds	r0, r6, #0x0
  105aea: a902         	add	r1, sp, #0x8
  105aec: f28b ed4a    	blx	0x391584 <void std::__convert_to_v<long double>(char const*, long double&, std::_Ios_Iostate&, int* const&)+0x23fb0> @ imm = #0x28ba94
  105af0: e7d3         	b	0x105a9a <CurlSocket::send2Server(CNetwork_Msg const*)+0x66> @ imm = #-0x5a
  105af2: 46c0         	mov	r8, r8
  105af4: 7ff5         	ldrb	r5, [r6, #0x1f]
  105af6: 0000         	movs	r0, r0
  105af8: 81b0         	strh	r0, [r6, #0xc]
  105afa: 0000         	movs	r0, r0
  105afc: 6ae6         	ldr	r6, [r4, #0x2c]
  105afe: 0038         	movs	r0, r7
  105b00: 4562         	cmp	r2, r12
  105b02: 002b         	movs	r3, r5
  105b04: 4504         	cmp	r4, r0
  105b06: 002b         	movs	r3, r5
  105b08: 4512         	cmp	r2, r2
  105b0a: 002b         	movs	r3, r5


jgbol3.87/lib/armeabi/libxiyoujilua.so:	file format elf32-littlearm

Disassembly of section .text:

00101c98 <FieldValue::FieldValue(char const*)>:
  101c98: b5f0         	push	{r4, r5, r6, r7, lr}
  101c9a: 465f         	mov	r7, r11
  101c9c: 4656         	mov	r6, r10
  101c9e: 464d         	mov	r5, r9
  101ca0: 4644         	mov	r4, r8
  101ca2: b4f0         	push	{r4, r5, r6, r7}
  101ca4: 4f4c         	ldr	r7, [pc, #0x130]        @ 0x101dd8 <FieldValue::FieldValue(char const*)+0x140>
  101ca6: b095         	sub	sp, #0x54
  101ca8: 2201         	movs	r2, #0x1
  101caa: 447f         	add	r7, pc
  101cac: 683f         	ldr	r7, [r7]
  101cae: 6082         	str	r2, [r0, #0x8]
  101cb0: 4681         	mov	r9, r0
  101cb2: 683b         	ldr	r3, [r7]
  101cb4: 1c0e         	adds	r6, r1, #0x0
  101cb6: 2500         	movs	r5, #0x0
  101cb8: 9313         	str	r3, [sp, #0x4c]
  101cba: 2300         	movs	r3, #0x0
  101cbc: 7003         	strb	r3, [r0]
  101cbe: 6043         	str	r3, [r0, #0x4]
  101cc0: 7403         	strb	r3, [r0, #0x10]
  101cc2: 1c08         	adds	r0, r1, #0x0
  101cc4: f7ed e87a    	blx	0xeedbc <.plt+0x404>    @ imm = #-0x12f0c
  101cc8: 2200         	movs	r2, #0x0
  101cca: 1c3b         	adds	r3, r7, #0x0
  101ccc: 2400         	movs	r4, #0x0
  101cce: 2100         	movs	r1, #0x0
  101cd0: 9200         	str	r2, [sp]
  101cd2: 4692         	mov	r10, r2
  101cd4: 4693         	mov	r11, r2
  101cd6: 1c07         	adds	r7, r0, #0x0
  101cd8: 4698         	mov	r8, r3
  101cda: e006         	b	0x101cea <FieldValue::FieldValue(char const*)+0x52> @ imm = #0xc
  101cdc: 2b24         	cmp	r3, #0x24
  101cde: d108         	bne	0x101cf2 <FieldValue::FieldValue(char const*)+0x5a> @ imm = #0x10
  101ce0: 2101         	movs	r1, #0x1
  101ce2: 468b         	mov	r11, r1
  101ce4: 3401         	adds	r4, #0x1
  101ce6: 42af         	cmp	r7, r5
  101ce8: d336         	blo	0x101d58 <FieldValue::FieldValue(char const*)+0xc0> @ imm = #0x6c
  101cea: 5d33         	ldrb	r3, [r6, r4]
  101cec: 3501         	adds	r5, #0x1
  101cee: 2c00         	cmp	r4, #0x0
  101cf0: d0f4         	beq	0x101cdc <FieldValue::FieldValue(char const*)+0x44> @ imm = #-0x18
  101cf2: 4652         	mov	r2, r10
  101cf4: 2a00         	cmp	r2, #0x0
  101cf6: d10e         	bne	0x101d16 <FieldValue::FieldValue(char const*)+0x7e> @ imm = #0x1c
  101cf8: 9a00         	ldr	r2, [sp]
  101cfa: 2a00         	cmp	r2, #0x0
  101cfc: d10b         	bne	0x101d16 <FieldValue::FieldValue(char const*)+0x7e> @ imm = #0x16
  101cfe: 2b5b         	cmp	r3, #0x5b
  101d00: d001         	beq	0x101d06 <FieldValue::FieldValue(char const*)+0x6e> @ imm = #0x2
  101d02: 2b00         	cmp	r3, #0x0
  101d04: d135         	bne	0x101d72 <FieldValue::FieldValue(char const*)+0xda> @ imm = #0x6a
  101d06: 465b         	mov	r3, r11
  101d08: 2b00         	cmp	r3, #0x0
  101d0a: d152         	bne	0x101db2 <FieldValue::FieldValue(char const*)+0x11a> @ imm = #0xa4
  101d0c: 5c73         	ldrb	r3, [r6, r1]
  101d0e: 4649         	mov	r1, r9
  101d10: 700b         	strb	r3, [r1]
  101d12: 5d33         	ldrb	r3, [r6, r4]
  101d14: 1c29         	adds	r1, r5, #0x0
  101d16: 2b5b         	cmp	r3, #0x5b
  101d18: d045         	beq	0x101da6 <FieldValue::FieldValue(char const*)+0x10e> @ imm = #0x8a
  101d1a: 2b7b         	cmp	r3, #0x7b
  101d1c: d046         	beq	0x101dac <FieldValue::FieldValue(char const*)+0x114> @ imm = #0x8c
  101d1e: 2b5d         	cmp	r3, #0x5d
  101d20: d02b         	beq	0x101d7a <FieldValue::FieldValue(char const*)+0xe2> @ imm = #0x56
  101d22: 2b7d         	cmp	r3, #0x7d
  101d24: d1de         	bne	0x101ce4 <FieldValue::FieldValue(char const*)+0x4c> @ imm = #-0x44
  101d26: 9a00         	ldr	r2, [sp]
  101d28: 2a00         	cmp	r2, #0x0
  101d2a: d0db         	beq	0x101ce4 <FieldValue::FieldValue(char const*)+0x4c> @ imm = #-0x4a
  101d2c: 1a63         	subs	r3, r4, r1
  101d2e: 1c1a         	adds	r2, r3, #0x0
  101d30: 1871         	adds	r1, r6, r1
  101d32: a80b         	add	r0, sp, #0x2c
  101d34: 9301         	str	r3, [sp, #0x4]
  101d36: f7ed ea8e    	blx	0xef254 <.plt+0x89c>    @ imm = #-0x12ae4
  101d3a: 9a01         	ldr	r2, [sp, #0x4]
  101d3c: a90b         	add	r1, sp, #0x2c
  101d3e: 2300         	movs	r3, #0x0
  101d40: 548b         	strb	r3, [r1, r2]
  101d42: 1c08         	adds	r0, r1, #0x0
  101d44: f7ed ecc6    	blx	0xef6d4 <.plt+0xd1c>    @ imm = #-0x12674
  101d48: 4649         	mov	r1, r9
  101d4a: 2201         	movs	r2, #0x1
  101d4c: 6088         	str	r0, [r1, #0x8]
  101d4e: 740a         	strb	r2, [r1, #0x10]
  101d50: 3401         	adds	r4, #0x1
  101d52: 1c29         	adds	r1, r5, #0x0
  101d54: 42af         	cmp	r7, r5
  101d56: d2c8         	bhs	0x101cea <FieldValue::FieldValue(char const*)+0x52> @ imm = #-0x70
  101d58: 4647         	mov	r7, r8
  101d5a: 9a13         	ldr	r2, [sp, #0x4c]
  101d5c: 683b         	ldr	r3, [r7]
  101d5e: 4648         	mov	r0, r9
  101d60: 429a         	cmp	r2, r3
  101d62: d136         	bne	0x101dd2 <FieldValue::FieldValue(char const*)+0x13a> @ imm = #0x6c
  101d64: b015         	add	sp, #0x54
  101d66: bc3c         	pop	{r2, r3, r4, r5}
  101d68: 4690         	mov	r8, r2
  101d6a: 4699         	mov	r9, r3
  101d6c: 46a2         	mov	r10, r4
  101d6e: 46ab         	mov	r11, r5
  101d70: bdf0         	pop	{r4, r5, r6, r7, pc}
  101d72: 2b7b         	cmp	r3, #0x7b
  101d74: d0c7         	beq	0x101d06 <FieldValue::FieldValue(char const*)+0x6e> @ imm = #-0x72
  101d76: 2b5d         	cmp	r3, #0x5d
  101d78: d1d3         	bne	0x101d22 <FieldValue::FieldValue(char const*)+0x8a> @ imm = #-0x5a
  101d7a: 4652         	mov	r2, r10
  101d7c: 2a00         	cmp	r2, #0x0
  101d7e: d0b1         	beq	0x101ce4 <FieldValue::FieldValue(char const*)+0x4c> @ imm = #-0x9e
  101d80: 1a63         	subs	r3, r4, r1
  101d82: 1c1a         	adds	r2, r3, #0x0
  101d84: 1871         	adds	r1, r6, r1
  101d86: a80b         	add	r0, sp, #0x2c
  101d88: 9301         	str	r3, [sp, #0x4]
  101d8a: f7ed ea64    	blx	0xef254 <.plt+0x89c>    @ imm = #-0x12b38
  101d8e: 9a01         	ldr	r2, [sp, #0x4]
  101d90: a90b         	add	r1, sp, #0x2c
  101d92: 2300         	movs	r3, #0x0
  101d94: 548b         	strb	r3, [r1, r2]
  101d96: 1c08         	adds	r0, r1, #0x0
  101d98: f7ed ec9c    	blx	0xef6d4 <.plt+0xd1c>    @ imm = #-0x126c8
  101d9c: 4649         	mov	r1, r9
  101d9e: 6088         	str	r0, [r1, #0x8]
  101da0: 5d33         	ldrb	r3, [r6, r4]
  101da2: 1c29         	adds	r1, r5, #0x0
  101da4: e7bd         	b	0x101d22 <FieldValue::FieldValue(char const*)+0x8a> @ imm = #-0x86
  101da6: 2301         	movs	r3, #0x1
  101da8: 469a         	mov	r10, r3
  101daa: e79b         	b	0x101ce4 <FieldValue::FieldValue(char const*)+0x4c> @ imm = #-0xca
  101dac: 2201         	movs	r2, #0x1
  101dae: 9200         	str	r2, [sp]
  101db0: e798         	b	0x101ce4 <FieldValue::FieldValue(char const*)+0x4c> @ imm = #-0xd0
  101db2: 1a62         	subs	r2, r4, r1
  101db4: a803         	add	r0, sp, #0xc
  101db6: 1871         	adds	r1, r6, r1
  101db8: 9201         	str	r2, [sp, #0x4]
  101dba: f7ed ea4c    	blx	0xef254 <.plt+0x89c>    @ imm = #-0x12b68
  101dbe: 9901         	ldr	r1, [sp, #0x4]
  101dc0: ab03         	add	r3, sp, #0xc
  101dc2: 2200         	movs	r2, #0x0
  101dc4: 545a         	strb	r2, [r3, r1]
  101dc6: 1c18         	adds	r0, r3, #0x0
  101dc8: f7ed ec84    	blx	0xef6d4 <.plt+0xd1c>    @ imm = #-0x126f8
  101dcc: 464b         	mov	r3, r9
  101dce: 6058         	str	r0, [r3, #0x4]
  101dd0: e79f         	b	0x101d12 <FieldValue::FieldValue(char const*)+0x7a> @ imm = #-0xc2
  101dd2: f7ed e962    	blx	0xef098 <.plt+0x6e0>    @ imm = #-0x12d3c
  101dd6: 46c0         	mov	r8, r8
  101dd8: a2c2         	adr	r2, #776 <LuaInterface::SizeOf(std::vector<std::pair<std::string, FieldValue*>*, std::allocator<std::pair<std::string, FieldValue*>*>>&)+0x32>
  101dda: 0038         	movs	r0, r7
