import streamlit as st
import copy
from src.strategies import naked_single, hidden_single, create_candidates, next_sudoku, difficulty_eval, count_empty
from src.display import display_sudoku

#st.title("Sudoku analyser")
st.set_page_config(page_title="Sudoku", layout="wide")
st.header("Sudoku analyser",divider=True)
st.markdown("Evaluate your sudoku and make it easier")

if 'sudoku' not in st.session_state:
    st.session_state.sudoku = [[0,8,0,6,1,0,0,0,4],[5,0,0,0,0,3,1,8,0],[0,0,0,0,0,0,9,0,0],[3,0,0,0,0,0,0,0,0],[0,0,6,0,0,0,0,2,5],[9,0,0,0,6,0,0,4,0],[0,5,1,3,0,9,7,0,0],[0,0,0,8,0,0,0,0,0],[4,0,0,0,0,0,0,0,0]]
    st.session_state.sudoku_original = copy.deepcopy(st.session_state.sudoku)
    sol, strat = next_sudoku(copy.deepcopy(st.session_state.sudoku))
    st.session_state.solved_sudoku = sol
    st.session_state.strategies_total = strat
    st.session_state.show_result = False
    st.session_state.show_candidates = False

col1, col2, col3 = st.columns([3, 1, 3])

with col1:
    user_input = st.text_input("Sudoku (empty places with 0):", "".join([str(n) for row in st.session_state.sudoku for n in row]))
    
    b1, b2, b3, b4 = st.columns(4)

    if b1.button("Enter",use_container_width=True):
        if len(user_input) == 81:
            st.session_state.sudoku = [[int(user_input[r * 9 + c]) for c in range(9)] for r in range(9)]
            st.session_state.show_result = False
            st.rerun()

    btn_text = "Candidatos ON" if st.session_state.show_candidates else "Candidatos OFF"
    if b2.button(btn_text,use_container_width=True):
        st.session_state.show_candidates = not st.session_state.show_candidates
        st.rerun()

    if b3.button("Reset",use_container_width=True):
        st.session_state.sudoku = copy.deepcopy(st.session_state.sudoku_original)
        st.session_state.show_result = False
        st.rerun()

    if b4.button("Compute",use_container_width=True):
        st.session_state.sudoku = copy.deepcopy(st.session_state.solved_sudoku)
        st.session_state.show_result = True
        st.rerun()

    to_choose_level = st.select_slider("Select level", options=["Easy", "Medium", "Hard"])

    diff_string, diff_int = difficulty_eval(count_empty(st.session_state.sudoku_original), *st.session_state.strategies_total)
    st.markdown(diff_string)
    st.progress(diff_int/1)

with col3:
    candidates = create_candidates(st.session_state.sudoku) if st.session_state.show_candidates else None
    fig = display_sudoku(st.session_state.sudoku, candidates=candidates)
    st.pyplot(fig)
