import streamlit as st
from src.strategies import naked_single, hidden_single, create_candidates, next_sudoku
from src.display import display_sudoku

st.set_page_config(page_title="Sudoku", layout="wide")
st.title("🧩 Sudoku")

st.set_page_config(layout="wide")

if 'sudoku' not in st.session_state:
    st.session_state.sudoku = [[0,8,0,6,1,0,0,0,4],[5,0,0,0,0,3,1,8,0],[0,0,0,0,0,0,9,0,0],[3,0,0,0,0,0,0,0,0],[0,0,6,0,0,0,0,2,5],[9,0,0,0,6,0,0,4,0],[0,5,1,3,0,9,7,0,0],[0,0,0,8,0,0,0,0,0],[4,0,0,0,0,0,0,0,0]]
    st.session_state.candidates = create_candidates(st.session_state.sudoku)

col1, col2 = st.columns([1, 2])

with col1:
    user_input = st.text_input("Sudoku (81 números):", "".join([str(n) for row in st.session_state.sudoku for n in row]))
    
    if st.button("Enter Sudoku"):
        st.session_state.sudoku = [[int(user_input[r * 9 + c]) for c in range(9)] for r in range(9)]
        st.session_state.candidates = create_candidates(st.session_state.sudoku)
        st.rerun()

    if st.button("Compute Sudoku"):
        resultado = next_sudoku(st.session_state.sudoku)
        if resultado is not None:
            st.session_state.sudoku, st.session_state.candidates = resultado
            st.rerun()
        else:
            st.warning("No hay más movimientos posibles o el Sudoku está completo.")

with col2:
    fig = display_sudoku(st.session_state.sudoku, st.session_state.candidates)
    st.pyplot(fig)