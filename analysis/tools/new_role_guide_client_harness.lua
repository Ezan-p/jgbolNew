local ms=assert(package.loaded.ms)
local guide=ms.d_guideUI
local saved={}
local function replace(t,k,v)
 saved[#saved+1]={t=t,k=k,v=t[k]};t[k]=v
end
local checks={}
local function check(name,fn)
 local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]=name..':'..tostring(ok)..':'..(err or '')
end
local ok,err=xpcall(function()
 replace(ms.d_mainUI,'g_playerInfo',{level=1,guide_progress=0})
 replace(ms.d_mainUI,'g_isNeedGuide',false)
 replace(ms.d_mainUI,'g_isNeedHint',false)
 replace(guide,'g_currentGuide',guide.g_currentGuide)
 replace(guide,'bit',guide.bit)
 local bits
 replace(ms.d_activityUI,'getActivityGuideState',function(v) bits=v end)
 local names={'playMoive','beforeSummon','guideJourney','guideSummon','guideSummon','guideChgChar',
              'guideJourney3','guideJourney4','guideChgItem','guideJourney5','guideViewQuest','guideJourney6','guideViewQuest2'}
 for stage=1,13 do
  check('resume_'..stage,function()
   ms.d_mainUI.g_playerInfo.guide_progress=2^stage-2
   guide.getGuideState()
   assert(ms.d_mainUI.g_isNeedGuide)
   assert(guide.g_currentGuide==guide.guideState[names[stage]],names[stage])
   assert(bits[stage]==0 and (stage==1 or bits[stage-1]==1))
  end)
 end
 check('completed',function()
  ms.d_mainUI.g_playerInfo.guide_progress=16382
  guide.getGuideState();assert(not ms.d_mainUI.g_isNeedGuide)
 end)
 local called
 replace(guide,'guideFightEndFunc',function() called='fight_end' end)
 check('first_fight_skips_second_fight',function()
  guide.g_currentGuide=guide.guideState.guideFightEnd
  guide.show()
  assert(called=='fight_end')
  assert(guide.g_currentGuide==guide.guideState.guideSummon)
 end)
 replace(guide,'g_dialogIndex',1)
 replace(guide,'showDialog',function() called='dialog' end)
 replace(guide,'packSummonData',function() return {} end)
 replace(ms.d_summonUI,'getSummonResult',function(data) called=data.cortege_type end)
 replace(ms.d_charPositionUI,'changeCharSucceed',function() called='cortege' end)
 replace(ms.d_charPositionUI,'updateItemSucceed',function() called='equip' end)
 replace(ms.d_lineupUI,'g_lineupUI',{packageLayer=nil})
 replace(guide,'endOfForceGuideFunc',function() called='end' end)
 for _,case in ipairs({{2,'dialog'},{5,4053},{6,'cortege'},{9,'equip'},{13,'end'}}) do
  check('callback_'..case[1],function()
   called=nil;guide.guideSucceed({stage=case[1],cortege_type=4053,left_time=0})
   assert(called==case[2])
  end)
 end
end,debug.traceback)
for i=#saved,1,-1 do local s=saved[i];s.t[s.k]=s.v end
if not ok then checks[#checks+1]='harness:false:'..err end
return table.concat(checks,'\n')
