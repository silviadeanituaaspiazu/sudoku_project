import copy
import random
from itertools import combinations
from collections import defaultdict
from src.direct_solution import solver_sudoku

def update_neighbors(candidates, i, j, val):
    for k in range(9):
        candidates[i][k].discard(val)
        candidates[k][j].discard(val)
    bi, bj = (i // 3) * 3, (j // 3) * 3
    for r in range(bi, bi + 3):
        for c in range(bj, bj + 3):
            candidates[r][c].discard(val)

def create_candidates(sudoku):
    candidates = [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] != 0:
                update_neighbors(candidates, i, j, sudoku[i][j])
                candidates[i][j] = set()
    return candidates

def naked_single(sudoku, cm):
    count, mod = 0, False
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0 and len(cm[i][j]) == 1:
                val = list(cm[i][j])[0]
                sudoku[i][j] = val
                update_neighbors(cm, i, j, val)
                cm[i][j] = set()
                mod, count = True, count + 1
    return mod, count

def hidden_single(sudoku, cm):
    count, mod = 0, False
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                for c in cm[i][j]:
                    r_c, col_c, sq_c = 0, 0, 0
                    for k in range(9):
                        if c in cm[i][k]: r_c += 1
                        if c in cm[k][j]: col_c += 1
                    bi, bj = (i // 3) * 3, (j // 3) * 3
                    for ii in range(bi, bi + 3):
                        for jj in range(bj, bj + 3):
                            if c in cm[ii][jj]: sq_c += 1
                    if r_c == 1 or col_c == 1 or sq_c == 1:
                        sudoku[i][j] = c
                        update_neighbors(cm, i, j, c)
                        cm[i][j] = set()
                        mod, count = True, count + 1
                        break
    return mod, count

def get_unit_coords(ut, idx):
    if ut == "row": return [(idx, c) for c in range(9)]
    if ut == "column": return [(r, idx) for r in range(9)]
    sr, sc = (idx // 3) * 3, (idx % 3) * 3
    return [(sr + r, sc + c) for r in range(3) for c in range(3)]

def find_naked_subset(cm, n=2):
    count = 0
    for ut in ["row", "column", "box"]:
        for i in range(9):
            coords = get_unit_coords(ut, i)
            cc = [(r, c) for r, c in coords if isinstance(cm[r][c], set) and 1 < len(cm[r][c]) <= n]
            if len(cc) >= n:
                for subset in combinations(cc, n):
                    combined = set().union(*(cm[r][c] for r, c in subset))
                    if len(combined) == n:
                        mod = False
                        for r, c in coords:
                            if (r, c) not in subset and (cm[r][c] & combined):
                                cm[r][c] -= combined
                                count, mod = count + len(cm[r][c] & combined), True
                        if mod: return True, 1
    return False, count

def pointing_pairs(cm):
    ec, mod = 0, False
    for br in range(3):
        for bc in range(3):
            bc_c = [(br*3 + i, bc*3 + j) for i in range(3) for j in range(3)]
            for num in range(1, 10):
                cells = [(r, c) for r, c in bc_c if isinstance(cm[r][c], set) and num in cm[r][c]]
                if 1 < len(cells) <= 3:
                    rs, cs = {r for r, c in cells}, {c for r, c in cells}
                    if len(rs) == 1:
                        r = list(rs)[0]
                        for c in range(9):
                            if (r, c) not in bc_c and isinstance(cm[r][c], set) and num in cm[r][c]:
                                cm[r][c].remove(num); ec, mod = ec + 1, True
                    elif len(cs) == 1:
                        c = list(cs)[0]
                        for r in range(9):
                            if (r, c) not in bc_c and isinstance(cm[r][c], set) and num in cm[r][c]:
                                cm[r][c].remove(num); ec, mod = ec + 1, True
    return mod, ec

def box_line_reduction(cm):
    ec, mod = 0, False
    for r in range(9):
        for num in range(1, 10):
            cols = [c for c in range(9) if isinstance(cm[r][c], set) and num in cm[r][c]]
            if 1 < len(cols) <= 3:
                bc = {c // 3 for c in cols}
                if len(bc) == 1:
                    bc_i, br_i = bc.pop(), r // 3
                    for i in range(3):
                        for j in range(3):
                            br, bc_idx = br_i * 3 + i, bc_i * 3 + j
                            if br != r and num in cm[br][bc_idx]:
                                cm[br][bc_idx].remove(num); ec, mod = ec + 1, True
    return mod, ec

def hidden_pairs(cm):
    def proc(coords):
        cmap = defaultdict(list)
        for r, c in coords:
            if isinstance(cm[r][c], set):
                for v in cm[r][c]: cmap[v].append((r, c))
        pairs = [v for v, cs in cmap.items() if len(cs) == 2]
        for i in range(len(pairs)):
            for j in range(i + 1, len(pairs)):
                if cmap[pairs[i]] == cmap[pairs[j]]:
                    (r1, c1), (r2, c2) = cmap[pairs[i]]
                    mod = False
                    for r, c in [(r1, c1), (r2, c2)]:
                        for v in list(cm[r][c]):
                            if v != pairs[i] and v != pairs[j]: cm[r][c].remove(v); mod = True
                    if mod: return True, 1
        return False, 0
    for i in range(9):
        if proc(get_unit_coords("row", i))[0] or proc(get_unit_coords("column", i))[0] or proc(get_unit_coords("box", i))[0]: return True, 2
    return False, 0

def x_wing(cm):
    ec, mod = 0, False
    for num in range(1, 10):
        rows = []
        for r in range(9):
            cols = [c for c in range(9) if isinstance(cm[r][c], set) and num in cm[r][c]]
            if len(cols) == 2:
                rows.append((r, cols))
        
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                r1, cols1 = rows[i]
                r2, cols2 = rows[j]
                
                if cols1 == cols2:
                    col1, col2 = cols1
                    for col in [col1, col2]:
                        for r in range(9):
                            if r != r1 and r != r2 and isinstance(cm[r][col], set) and num in cm[r][col]:
                                cm[r][col].remove(num)
                                ec, mod = ec + 1, True
    return mod, ec

def swordfish(cm):
    for num in range(1, 10):
        rl = [(r, set(c for c in range(9) if isinstance(cm[r][c], set) and num in cm[r][c])) for r in range(9)]
        rl = [x for x in rl if 2 <= len(x[1]) <= 3]
        for sub in combinations(rl, 3):
            comb = sub[0][1] | sub[1][1] | sub[2][1]
            if len(comb) == 3:
                mod = False
                for col in comb:
                    for r in range(9):
                        if r not in [s[0] for s in sub] and num in cm[r][col]:
                            cm[r][col].remove(num); mod = True
                if mod: return True, 1
    return False, 0

def y_wing(cm):
    def sees(r1, c1, r2, c2):
        return r1 == r2 or c1 == c2 or (r1 // 3 == r2 // 3 and c1 // 3 == c2 // 3)

    bival = [(r, c, cm[r][c]) for r in range(9) for c in range(9) if isinstance(cm[r][c], set) and len(cm[r][c]) == 2]

    for r, c, pivot in bival:
        p_list = list(pivot)
        x, y = p_list[0], p_list[1]

        for r1, c1, a1 in bival:
            if (r, c) == (r1, c1) or not sees(r, c, r1, c1): continue
            if x in a1 and y not in a1:
                z = list(a1 - {x})[0]

                for r2, c2, a2 in bival:
                    if (r, c) == (r2, c2) or (r1, c1) == (r2, c2) or not sees(r, c, r2, c2): continue
                    
                    if y in a2 and x not in a2 and z in a2:
                        eliminations = 0
                        for tr in range(9):
                            for tc in range(9):
                                if (tr, tc) in [(r, c), (r1, c1), (r2, c2)]: continue
                                
                                if sees(tr, tc, r1, c1) and sees(tr, tc, r2, c2):
                                    if isinstance(cm[tr][tc], set) and z in cm[tr][tc]:
                                        cm[tr][tc].remove(z)
                                        eliminations += 1
                        
                        if eliminations > 0:
                            return True, 1
                            
    return False, 0

def forcing_chain(cm):
    def propagate(temp_cm, start_r, start_c, val):
        eliminated = set()
        stack = [(start_r, start_c, val)]
        
        while stack:
            r, c, v = stack.pop()
            peers = [(r, i) for i in range(9)] + \
                    [(i, c) for i in range(9)] + \
                    [(r // 3 * 3 + i, c // 3 * 3 + j) for i in range(3) for j in range(3)]
            
            for pr, pc in peers:
                if (pr, pc) != (r, c) and isinstance(temp_cm[pr][pc], set) and v in temp_cm[pr][pc]:
                    temp_cm[pr][pc].remove(v)
                    eliminated.add((pr, pc, v))
                    if len(temp_cm[pr][pc]) == 0:
                        return eliminated, False
                    if len(temp_cm[pr][pc]) == 1:
                        stack.append((pr, pc, list(temp_cm[pr][pc])[0]))
        return eliminated, True

    bival = [(r, c, cm[r][c]) for r in range(9) for c in range(9) if isinstance(cm[r][c], set) and len(cm[r][c]) == 2]
    
    for r, c, cands in bival:
        v1, v2 = list(cands)
        
        cm1 = copy.deepcopy(cm)
        elim1, valid1 = propagate(cm1, r, c, v1)
        
        cm2 = copy.deepcopy(cm)
        elim2, valid2 = propagate(cm2, r, c, v2)
        
        if not valid1:
            cm[r][c].remove(v1)
            return True, 1
        if not valid2:
            cm[r][c].remove(v2)
            return True, 1
            
        common = elim1 & elim2
        if common:
            eliminations = 0
            for er, ec, ev in common:
                if isinstance(cm[er][ec], set) and ev in cm[er][ec]:
                    cm[er][ec].remove(ev)
                    eliminations += 1
            if eliminations > 0:
                return True, 1
                
    return False, 0

def bug_plus_one(cm):
    c3_cells = []
    
    for r in range(9):
        for c in range(9):
            if isinstance(cm[r][c], set) and len(cm[r][c]) > 0:
                l = len(cm[r][c])
                if l > 3 or l == 1:
                    return False, 0 
                elif l == 3:
                    c3_cells.append((r, c))
    
    if len(c3_cells) != 1:
        return False, 0
        
    r, c = c3_cells[0]
    
    for cand in list(cm[r][c]):
        count_row = sum(1 for i in range(9) if isinstance(cm[r][i], set) and cand in cm[r][i])
        count_col = sum(1 for i in range(9) if isinstance(cm[i][c], set) and cand in cm[i][c])
        br, bc = 3 * (r // 3), 3 * (c // 3)
        count_box = sum(1 for i in range(3) for j in range(3) if isinstance(cm[br+i][bc+j], set) and cand in cm[br+i][bc+j])
        if count_row == 3 or count_col == 3 or count_box == 3:
            cm[r][c] = {cand}
            return True, 1
                  
    return False, 0


def next_sudoku(sudoku):
    sc, cm = copy.deepcopy(sudoku), create_candidates(sudoku)
    stats = {
        "ns": 0, "hs": 0, "sub": 0,  # 0, 1, 2: Básicas
        "pp": 0, "bl": 0,            # 3, 4: Intermedias
        "hp": 0, "xw": 0, "yw": 0,   # 5, 6, 7: Avanzadas
        "sw": 0, "bug": 0, "fc": 0   # 8, 9, 10: Muy Avanzadas / Fuerza Bruta
    }
    
    for _ in range(200):
            m1, c1 = naked_single(sc, cm)
            stats["ns"] += c1
            m2, c2 = hidden_single(sc, cm)
            stats["hs"] += c2
            if m1 or m2: continue
            
            m4, c4 = pointing_pairs(cm)
            stats["pp"] += c4
            if m4: continue
            
            m5, c5 = box_line_reduction(cm)
            stats["bl"] += c5
            if m5: continue
            
            m3, c3 = find_naked_subset(cm, n=2)
            stats["sub"] += c3
            if m3: continue
            
            m3_3, c3_3 = find_naked_subset(cm, n=3)
            stats["sub"] += c3_3
            if m3_3: continue
            
            m3_4, c3_4 = find_naked_subset(cm, n=4)
            stats["sub"] += c3_4
            if m3_4: continue
            
            m6, c6 = hidden_pairs(cm)
            stats["hp"] += c6
            if m6: continue
            
            m7, c7 = x_wing(cm)
            stats["xw"] += c7
            if m7: continue
            
            m9, c9 = y_wing(cm)
            stats["yw"] += c9
            if m9: continue
            
            m8, c8 = swordfish(cm)
            stats["sw"] += c8
            if m8: continue
            
            m11, c11 = bug_plus_one(cm)
            stats["bug"] += c11
            if m11: continue
            
            m10, c10 = forcing_chain(cm)
            stats["fc"] += c10
            if m10: continue
            
            break
        
    return sc, stats, cm

def difficulty_eval(*stats):
    if any(stats[i] > 0 for i in [9, 10]):
            level_name, level_val = "Expert", 10
    elif any(stats[i] > 0 for i in [5, 6, 7, 8]):
            level_name, level_val = "Hard", 7
    elif any(stats[i] > 0 for i in [3, 4]):
            level_name, level_val = "Intermediate", 4
    else:
            level_name, level_val = "Easy", 1
            
    return level_name, level_val

def count_empty(sudoku): return sum(r.count(0) for r in sudoku)

def simulate_until_stuck(sudoku, allowed_indices):
    temp_sudoku = copy.deepcopy(sudoku)
    while True:
        sc_temp, stats, cm = next_sudoku(temp_sudoku)
        
        forbidden_used = any(stats[i] > 0 for i in range(11) if i not in allowed_indices)
        
        if forbidden_used:
            return temp_sudoku, False 
            
        if count_empty(sc_temp) == 0: 
            return sc_temp, True 
            
        if sum(stats) == 0:
            return temp_sudoku, False 
            
        temp_sudoku = sc_temp

def apply_level(grid, allowed_indices):
    solved_state, _, _ = next_sudoku(copy.deepcopy(grid))
    current_grid = copy.deepcopy(grid)
    hints_added = 0
    
    if allowed_indices == [0, 1, 2]:
        for _ in range(3):
            empty_cells = [(r, c) for r in range(9) for c in range(9) if current_grid[r][c] == 0]
            if empty_cells:
                r, c = random.choice(empty_cells)
                current_grid[r][c] = solved_state[r][c]
                hints_added += 1

    while True:
        temp_resolved, temp_stats, temp_cm = next_sudoku(copy.deepcopy(current_grid))
        
        used_indices = {i for i, count in enumerate(temp_stats.values()) if count > 0}
        forbidden = [i for i in used_indices if i not in allowed_indices]
        
        if count_empty(temp_resolved) == 0 and not forbidden:
            break
            
        cells_in_forbidden = []
        if forbidden:
            for r in range(9):
                for c in range(9):
                    if current_grid[r][c] == 0 and isinstance(temp_cm[r][c], set):
                        if any(idx in forbidden for idx in range(11)): 
                            cells_in_forbidden.append((r, c))
        
        if cells_in_forbidden:
            r, c = random.choice(cells_in_forbidden)
        else:
            empty_cells = [(r, c) for r in range(9) for c in range(9) if current_grid[r][c] == 0]
            if not empty_cells: break
            r, c = random.choice(empty_cells)
            
        current_grid[r][c] = solved_state[r][c]
        hints_added += 1
        
    return current_grid, hints_added