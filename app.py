import random

import streamlit as st

DIFFICULTY_RANGES = {
    "Easy (1-10)": 10,
    "Standard (1-25)": 25,
    "Hard (1-50)": 50,
}


def reset_game() -> None:
    maximum = DIFFICULTY_RANGES[st.session_state.difficulty]
    st.session_state.current_number = random.randint(1, maximum)
    st.session_state.score = 0
    st.session_state.result_message = "Choose Higher or Lower, then make your guess."
    st.session_state.result_type = "info"


if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Easy (1-10)"
    st.session_state.current_number = random.randint(1, 10)
    st.session_state.score = 0
    st.session_state.result_message = "Choose Higher or Lower, then make your guess."
    st.session_state.result_type = "info"

st.title("Higher or Lower")
st.write(
    "Guess whether the next number will be higher or lower than the number on screen. "
    "Build a streak by getting consecutive guesses right."
)

difficulty = st.selectbox(
    "Choose a number range",
    options=list(DIFFICULTY_RANGES),
    key="difficulty",
    on_change=reset_game,
)

st.metric("Current number", st.session_state.current_number)
st.caption(f"Numbers are drawn from 1 to {DIFFICULTY_RANGES[difficulty]}.")

guess = st.radio(
    "Will the next number be higher or lower?",
    options=("Higher", "Lower"),
    horizontal=True,
)

if st.button("Make guess", type="primary"):
    current_number = st.session_state.current_number
    next_number = random.randint(1, DIFFICULTY_RANGES[difficulty])

    if next_number == current_number:
        st.session_state.result_message = (
            f"The next number was {next_number}. It was a tie, so your streak stays the same."
        )
        st.session_state.result_type = "info"
    else:
        correct = (guess == "Higher" and next_number > current_number) or (
            guess == "Lower" and next_number < current_number
        )
        if correct:
            st.session_state.score += 1
            st.session_state.result_message = (
                f"Correct! The next number was {next_number}. Your streak is "
                f"{st.session_state.score}."
            )
            st.session_state.result_type = "success"
        else:
            st.session_state.result_message = (
                f"Not quite. The next number was {next_number}; your streak resets to 0."
            )
            st.session_state.score = 0
            st.session_state.result_type = "error"

    st.session_state.current_number = next_number

st.metric("Correct guesses in a row", st.session_state.score)
getattr(st, st.session_state.result_type)(st.session_state.result_message)

if st.button("Restart game"):
    reset_game()
    st.rerun()