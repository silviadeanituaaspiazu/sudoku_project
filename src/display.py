from src.config import np, plt
# OLD ONE
# def display_sudoku(grid, candidates=None):
#     grid = np.array(grid)
#     fig, ax = plt.subplots(figsize=(6, 6))
    
#     ax.set_xlim(0, 9)
#     ax.set_ylim(0, 9)

#     for i in range(10):
#         lw = 2 if i % 3 == 0 else 0.5
#         ax.axhline(i, color='black', lw=lw)
#         ax.axvline(i, color='black', lw=lw)
    
#     for i in range(9):
#         for j in range(9):
#             row, col = 8 - i, j
#             val = grid[row][col]
            
#             if val != 0:
#                 ax.text(j + 0.5, i + 0.5, str(val), 
#                         va='center', ha='center', fontsize=20, fontweight='bold')
#             elif candidates is not None:
#                 cands = candidates[row][col]
#                 for cand in cands:
#                     c_row = 2 - (cand - 1) // 3
#                     c_col = (cand - 1) % 3
#                     pos_x = j + 0.15 + (c_col * 0.3)
#                     pos_y = i + 0.15 + (c_row * 0.3)
#                     ax.text(pos_x, pos_y, str(cand), 
#                             va='center', ha='center', fontsize=8, color='gray')
    
#     ax.axis('off')
#     return fig



def display_sudoku(grid, original_grid=None, candidates=None):
    grid = np.array(grid)
    
    # CORRECCIÓN: Si no hay original_grid, usamos el grid actual
    if original_grid is None:
        orig = grid
    else:
        orig = np.array(original_grid)
        
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 9); ax.set_ylim(0, 9)
    
    for i in range(10):
        lw = 2 if i % 3 == 0 else 0.5
        ax.axhline(i, color='black', lw=lw)
        ax.axvline(i, color='black', lw=lw)
        
    for i in range(9):
        for j in range(9):
            row, col = 8 - i, j
            val, o_val = grid[row][col], orig[row][col]
            
            if val != 0:
                color = 'blue' if o_val == 0 else 'black'
                ax.text(j + 0.5, i + 0.5, str(val), va='center', ha='center', 
                        fontsize=20, fontweight='bold', color=color)
            elif candidates is not None:
                for cand in candidates[row][col]:
                    ax.text(j + 0.15 + ((cand-1)%3)*0.3, i + 0.15 + (2-(cand-1)//3)*0.3, 
                            str(cand), va='center', ha='center', fontsize=8, color='gray')
                    
    ax.axis('off')
    return fig