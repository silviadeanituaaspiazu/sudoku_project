from src.config import pd, np, plt

def display_sudoku(grid, candidates=None):
    """
    Si pasas 'candidates', muestra los números pequeños.
    Si no pasas nada, muestra el Sudoku limpio.
    """
    grid = np.array(grid)
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Dibujar cuadrícula
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    for i in range(10):
        lw = 2 if i % 3 == 0 else 0.5
        ax.axhline(i, color='black', lw=lw)
        ax.axvline(i, color='black', lw=lw)
    
    # Dibujar números
    for i in range(9):
        for j in range(9):
            row, col = 8 - i, j
            val = grid[row][col]
            
            if val != 0:
                # Número resuelto
                ax.text(j + 0.5, i + 0.5, str(val), 
                        va='center', ha='center', fontsize=20, fontweight='bold')
            elif candidates is not None:
                # Dibujar candidatos en pequeño
                cands = candidates[row][col]
                for cand in cands:
                    # Cálculo de posición (1-9 a cuadrícula 3x3)
                    c_row = 2 - (cand - 1) // 3
                    c_col = (cand - 1) % 3
                    pos_x = j + 0.15 + (c_col * 0.3)
                    pos_y = i + 0.15 + (c_row * 0.3)
                    ax.text(pos_x, pos_y, str(cand), 
                            va='center', ha='center', fontsize=8, color='gray')
    
    ax.axis('off')
    plt.show()