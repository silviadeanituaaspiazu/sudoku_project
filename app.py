import streamlit as st
import copy
from src.strategies import next_sudoku, difficulty_eval, count_empty, create_candidates, apply_level
from src.display import display_sudoku

st.set_page_config(page_title="Sudoku", layout="wide")
st.header("Sudoku Difficulty Architect", divider=True)
st.markdown("Evaluate your sudoku and make it easier")

def update_difficulty(grid):
    resolved_state, stats, _ = next_sudoku(copy.deepcopy(grid))
    diff_string, diff_int = difficulty_eval(count_empty(resolved_state), *stats)
    st.session_state.diff_string = diff_string
    st.session_state.diff_int = diff_int
    st.session_state.solved_sudoku = resolved_state

if 'sudoku' not in st.session_state:
    st.session_state.sudoku = [
        [0,8,0,6,1,0,0,0,4], [5,0,0,0,0,3,1,8,0], [0,0,0,0,0,0,9,0,0],
        [3,0,0,0,0,0,0,0,0], [0,0,6,0,0,0,0,2,5], [9,0,0,0,6,0,0,4,0],
        [0,5,1,3,0,9,7,0,0], [0,0,0,8,0,0,0,0,0], [4,0,0,0,0,0,0,0,0]
    ]
    st.session_state.sudoku_original = copy.deepcopy(st.session_state.sudoku)
    st.session_state.show_candidates = False
    
    st.session_state.simplified_cache = {} 
    
    update_difficulty(st.session_state.sudoku)

col1, col2, col3 = st.columns([3, 1, 3])

with col1:
    user_input = st.text_input("Sudoku (81 digits):", "".join([str(n) for row in st.session_state.sudoku for n in row]))
    
    mapping = {
        "Very Easy": 1, "Easy": 2, "Moderate": 4, 
        "Intermediate": 6, "Challenging": 7, 
        "Hard": 8, "Expert": 9, "Master": 10
    }
    
    score = mapping.get(st.session_state.diff_string, 5)
    
    st.markdown(f"Original sudoku level: **{st.session_state.diff_string} ({score}/10)**")

    b1, b2, b3, b4 = st.columns(4)
    
    if b1.button("Enter", use_container_width=True):
        if len(user_input) == 81:
            new_board = [[int(user_input[r * 9 + c]) for c in range(9)] for r in range(9)]
            st.session_state.sudoku = copy.deepcopy(new_board)
            st.session_state.sudoku_original = copy.deepcopy(new_board)
            
            st.session_state.simplified_cache = {} 
            
            update_difficulty(st.session_state.sudoku)
            st.rerun()

    if b2.button("Reset", use_container_width=True):
        st.session_state.sudoku = copy.deepcopy(st.session_state.sudoku_original)
        st.rerun()

    if b3.button("Compute", use_container_width=True):
        st.session_state.sudoku = copy.deepcopy(st.session_state.solved_sudoku)
        st.rerun()
    
    with b4:
        st.toggle("Candidates", key="show_candidates")
    st.divider()
    
    ALLOWED_MAP = {
        "Easy": [0, 1], 
        "Intermediate": [0, 1, 2, 3], 
        "Hard": [0, 1, 2, 3, 4, 5], 
        "Expert": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
    
    level = st.select_slider("Simplify to level:", options=list(ALLOWED_MAP.keys()))
    
    if st.button("Apply Simplification", use_container_width=True):
        if level not in st.session_state.simplified_cache:
            new_sudoku, hints_added = apply_level(
                st.session_state.sudoku_original, 
                ALLOWED_MAP[level]
            )
            st.session_state.simplified_cache[level] = (new_sudoku, hints_added)
        
        cached_sudoku, hints_added = copy.deepcopy(st.session_state.simplified_cache[level])
        st.session_state.sudoku = cached_sudoku
        
        if hints_added > 0:
            st.toast(f"{hints_added} key hints added.", icon="✅")
        else:
            st.toast("The original sudoku already matches this level.", icon="ℹ️")
            
        st.rerun()

with col3:
    smart_candidates = create_candidates(st.session_state.sudoku) if st.session_state.show_candidates else None
    fig = display_sudoku(st.session_state.sudoku, original_grid=st.session_state.sudoku_original, candidates=smart_candidates)
    st.pyplot(fig)