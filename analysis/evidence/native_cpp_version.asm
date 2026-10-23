
jgbol3.87/lib/armeabi/libxiyoujilua.so:	file format elf32-littlearm

Disassembly of section .text:

000ffed8 <LuaInterface::getCppVersion(lua_State*)>:
   ffed8: b510         	push	{r4, lr}
   ffeda: 1c04         	adds	r4, r0, #0x0
   ffedc: 4808         	ldr	r0, [pc, #0x20]         @ 0xfff00 <LuaInterface::getCppVersion(lua_State*)+0x28>
   ffede: 216f         	movs	r1, #0x6f
   ffee0: 4478         	add	r0, pc
   ffee2: f091 fc49    	bl	0x191778 <cocos2d::CCLog(char const*, ...)> @ imm = #0x91892
   ffee6: 4b05         	ldr	r3, [pc, #0x14]         @ 0xffefc <LuaInterface::getCppVersion(lua_State*)+0x24>
   ffee8: 4a03         	ldr	r2, [pc, #0xc]          @ 0xffef8 <LuaInterface::getCppVersion(lua_State*)+0x20>
   ffeea: 1c20         	adds	r0, r4, #0x0
   ffeec: f0d3 ea5c    	blx	0x1d33a8 <lua_pushnumber> @ imm = #0xd34b8
   ffef0: 2001         	movs	r0, #0x1
   ffef2: bd10         	pop	{r4, pc}
   ffef4: 46c0         	mov	r8, r8
   ffef6: 46c0         	mov	r8, r8
   ffef8: 0000         	movs	r0, r0
   ffefa: 0000         	movs	r0, r0
   ffefc: c000         	<unknown>
   ffefe: 405b         	eors	r3, r3
   fff00: 8b64         	ldrh	r4, [r4, #0x1a]
   fff02: 002b         	movs	r3, r5
