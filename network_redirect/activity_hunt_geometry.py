"""Server-owned ray tracing. [B] collision contour fitted to original ground.png.

Coordinates are native pixels relative to (screen_width/2, ground_bottom).
The cannon is (0,-20) [A]. The narrow right edge is an absorbing trap [B].
"""
import math
import secrets

# Counterclockwise; the original left arc is approximated by 18 ten-degree edges.
POLYGON = [(-360.0, 5.0), (390.0, 5.0), (634.0, 235.0),
           (634.0, 325.0), (390.0, 555.0), (-360.0, 555.0)] + [
    (-360 + 275 * math.cos(math.radians(t)), 280 + 275 * math.sin(math.radians(t)))
    for t in range(100, 271, 10)]
POLYGON = POLYGON[:-1]  # last arc endpoint is the first vertex


def cross(a, b):
    return a[0]*b[1] - a[1]*b[0]


def inside(x, y, margin=0):
    for a, b in zip(POLYGON, POLYGON[1:]+POLYGON[:1]):
        edge = (b[0]-a[0], b[1]-a[1])
        if cross(edge, (x-a[0], y-a[1])) < margin*math.hypot(*edge)-1e-3:
            return False
    return True


def board(rows):
    points = []
    for kind, row in rows.items():
        # rand_weight has no shipped denominator: interpreted as percent [B].
        count = row['base_count'] + (row['rand_count'] if secrets.randbelow(100) < row['rand_weight'] else 0)
        for _ in range(count):
            for attempt in range(5000):
                x, y = secrets.randbelow(1200)-600, secrets.randbelow(470)+45
                if inside(x,y,35) and all(math.hypot(x-p['x'],y-p['y']) >= 65 for p in points):
                    points.append(dict(x=x,y=y,soul_type=kind));break
            else:
                raise ValueError('捕魂地图生成失败')
    return points


def trace(points, angle, bounces, radius):
    """Return native move_path; each soul appears only once across all segments."""
    dx, dy = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    # Enter from the cannon through the lower edge without reflecting there.
    p = (dx*25/dy,5.0)
    path = [dict(x=0,y=-20,soul_list=[])]
    caught = set()
    trapped = False
    for _ in range(bounces+1):
        intersections=[]
        for i,(a,b) in enumerate(zip(POLYGON,POLYGON[1:]+POLYGON[:1])):
            e=(b[0]-a[0],b[1]-a[1]);den=cross((dx,dy),e)
            if abs(den)<1e-9:continue
            ap=(a[0]-p[0],a[1]-p[1]);t=cross(ap,e)/den;u=cross(ap,(dx,dy))/den
            if t>1e-6 and -1e-8<=u<=1+1e-8:intersections.append((t,i,e))
        if not intersections:raise ValueError('捕魂轨迹无有效边界')
        distance,edge_id,edge=min(intersections)
        q=(p[0]+dx*distance,p[1]+dy*distance)
        hits=[]
        for i,soul in enumerate(points):
            if i in caught:continue
            v=(soul['x']-p[0],soul['y']-p[1]);t=v[0]*dx+v[1]*dy
            if 0<=t<=distance and abs(cross(v,(dx,dy)))<=radius:
                hits.append((t,i,soul))
        hits.sort(key=lambda h:(h[0],h[1]));caught.update(i for _,i,_ in hits)
        path.append(dict(x=round(q[0],6),y=round(q[1],6),soul_list=[dict(s) for _,_,s in hits]))
        if edge_id==2:
            trapped=True;break
        norm=math.hypot(*edge);nx,ny=-edge[1]/norm,edge[0]/norm
        dot=dx*nx+dy*ny;dx-=2*dot*nx;dy-=2*dot*ny
        p=q
    return dict(move_path=path,trap_hit=trapped),caught
