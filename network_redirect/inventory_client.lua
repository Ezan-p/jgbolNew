-- The original item_name.csv puts 1307 at order 100, far from 1304-1306
-- (305-307). Keep scripture bags together without changing item metadata.
do
 local ms=package.loaded.ms
 local bag=ms and ms.d_packageUI
 if not bag or not bag.sortProps then return 'pending' end
 if not bag._localInventoryRestore then
  local original=bag.sortProps
  local function order(item)
   local tid=item.type_id
   if tid and tid>=1304 and tid<=1307 then
    -- Fractional positions avoid interleaving native integer-order scrolls.
    return 305+(tid-1303)/10
   end
   return item.csvInfo.sortOrder or 0
  end
  bag.sortProps=function(a,b)
   return order(a)<order(b)
  end
  bag._localInventoryRestore=function()
   bag.sortProps=original;bag._localInventoryRestore=nil
  end
 end
end
