# Uncomment this line to import some functions that can help
# you debug your algorithm
# from plotting import draw_line, draw_hull, circle_point

def compute_hull_dvcq(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    pts = sorted(set(points))
    return DVCQ(pts)

def compute_hull_other(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    import math
    pts = list(set(points))
    if len(pts) <= 2:
        return pts
    pivot = min(pts, key=lambda p: (p[1], p[0]))
    def polar_angle(p):
        return math.atan2(p[1] - pivot[1], p[0] - pivot[0])
    def distance(p):
        return (p[0] - pivot[0])**2 + (p[1] - pivot[1])**2
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    sorted_pts = sorted([p for p in pts if p != pivot], key=lambda p: (polar_angle(p), distance(p)))
    filtered = [pivot]
    i = 0
    while i < len(sorted_pts):
        j = i
        while j < len(sorted_pts)-1 and math.isclose(polar_angle(sorted_pts[j]), polar_angle(sorted_pts[j+1])):
            j += 1
        filtered.append(sorted_pts[j])
        i = j + 1
    if len(filtered) < 3:
        return filtered
    stack = [filtered[0], filtered[1], filtered[2]]
    for pt in filtered[3:]:
        while len(stack) > 1 and cross(stack[-2], stack[-1], pt) <= 0:
            stack.pop()
        stack.append(pt)
    return stack

def DVCQ(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    if len(points) <= 3:
        return _base_case(points)

    mid = len(points) // 2
    left_hull = DVCQ(points[:mid])
    right_hull = DVCQ(points[mid:])

    return _merge_hulls(left_hull, right_hull)

def _base_case(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the convex hull of 3 or fewer points in clockwise order."""
    if len(points) <= 2:
        return points

    a, b, c = points
    turn = _orientation(a, b, c)

    if turn == 0:  # collinear
        return [a, c]
    elif turn == 1:  # already clockwise
        return [a, b, c]
    else:  # counterclockwise -> swap last two
        return [a, c, b]

def _orientation(p: tuple[float, float], q: tuple[float, float], r: tuple[float, float]) -> int:
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0      # collinear
    elif val > 0:
        return 1      # clockwise
    else:
        return 2      # counterclockwise
    
def _merge_hulls(left_hull: list[tuple[float, float]], right_hull: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Merge two convex hulls into a single convex hull."""
    n, m = len(left_hull), len(right_hull)
    li = max(range(n), key=lambda i: (left_hull[i][0], left_hull[i][1]))
    ri = min(range(m), key=lambda i: (right_hull[i][0], right_hull[i][1]))

    # Upper tangent
    upper_l, upper_r = li, ri
    while True:
        changed = False
        while _orientation(left_hull[upper_l], right_hull[upper_r], left_hull[(upper_l + 1) % n]) == 1:
            upper_l = (upper_l + 1) % n
            changed = True
        while _orientation(left_hull[upper_l], right_hull[upper_r], right_hull[(upper_r - 1) % m]) == 1:
            upper_r = (upper_r - 1) % m
            changed = True
        if not changed:
            break

    # Lower tangent
    lower_l, lower_r = li, ri
    while True:
        changed = False
        while _orientation(right_hull[lower_r], left_hull[lower_l], left_hull[(lower_l - 1) % n]) == 1:
            lower_l = (lower_l - 1) % n
            changed = True
        while _orientation(right_hull[lower_r], left_hull[lower_l], right_hull[(lower_r + 1) % m]) == 1:
            lower_r = (lower_r + 1) % m
            changed = True
        if not changed:
            break

    # Stitch CW (+1): upper_l to lower_l on left, lower_r to upper_r on right
    hull_result = []
    i = upper_l
    while True:
        hull_result.append(left_hull[i])
        if i == lower_l:
            break
        i = (i + 1) % n

    i = lower_r
    while True:
        hull_result.append(right_hull[i])
        if i == upper_r:
            break
        i = (i + 1) % m

    return hull_result