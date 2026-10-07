import math
import sys

def pack_uvs(unique_items, tex_w, tex_h, padding=1):
    # Sort descending by height, then width
    items = sorted(unique_items, key=lambda item: (item[2], item[1]), reverse=True)

    shelves = []
    current_y = 0
    uv_map = {}

    for gid, pw, ph in items:
        placed = False
        for s in shelves:
            if s['rem_w'] >= pw and s['h'] >= ph:
                uv_map[gid] = [s['x'], s['y']]
                s['x'] += pw + padding
                s['rem_w'] -= (pw + padding)
                placed = True
                break
        if not placed:
            if current_y + ph <= tex_h and pw <= tex_w:
                shelves.append({'y': current_y, 'h': ph, 'x': pw + padding, 'rem_w': tex_w - (pw + padding)})
                uv_map[gid] = [0, current_y]
                current_y += ph + padding
                placed = True
            else:
                return False, gid, current_y, pw, ph

    return True, uv_map, current_y, 0, 0

print("Packer logic defined.")
