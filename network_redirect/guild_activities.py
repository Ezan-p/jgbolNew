"""Guild activity routing; each subsystem owns its persistent settlement."""
from . import guild as u, guild_feast
FEAST = guild_feast.FEAST
feast = guild_feast.feast
feast_data = guild_feast.data


def query(role,s,g,d,now,r):
    q=d['query_type']
    if q==14:return [u.reply(18,dict(query_type=q,feast_data=feast_data(role,s,g,now,r)))]
    if q==15:return [u.reply(18,guild_feast.ranking(role,s,now,r))]
    from . import guild_match
    return guild_match.query(role,s,g,d,now,r)


def settle(role,s,g,op,d,now,r):
    if op in (78,79,80,81,82,83,84,85,86,87,88,89,91,92,94,95):
        u.require(role['level']>=r['pet_role_level'] and g['level']>=r['pet_union_level'], '灵宠仙地需人物50级、仙盟5级')
    if op==69:
        from . import guild_escort
        return guild_escort.settle(role,s,g,d,now,r)
    if op in (83,84,85,86,87,91,92):
        from . import guild_hunt
        return guild_hunt.settle(role,s,g,op,d,now,r)
    if op in (26,27,28,29,30,31,32,33,41,42,43,44,50,73,74,75,78,79,80,81,82,88,89,94,95):
        from . import guild_instances
        return guild_instances.settle(role,s,g,op,d,now,r)
    if op in (45,46,47,48,58,62,63,72,76):
        from . import guild_match
        return guild_match.settle(role,s,g,op,d,now,r)
    if op in (65,66,67,68):
        return guild_feast.settle(role,s,g,op,d,now,r)
    u.require(False,'该仙盟操作尚未完成接入')
