"""Compatibility routes for native fortune and Tangwang card requests."""
from . import activity_caishen as caishen, activity_tangwang as tangwang
from .activity_tangwang import COMBINATIONS, card


def state(role,now,r):
    return caishen.state(role,now,r)


def status(role,now,r):
    out=tangwang.status(role,now,r)
    out['visit_caishen']=caishen.payload(state(role,now,r),r)
    return out


def settle(role,mid,req,now,r):
    if mid in (1210,1211):return caishen.settle(role,mid,req,now,r)
    return tangwang.settle(role,req,now,r)
