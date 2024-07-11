import streamlit as st

# Define the questions and their corresponding point values
questions = [
    {"question": "How often do you exercise?", "options": {"Daily": 5, "Weekly": 3, "Monthly": 1, "Never": 0}},
    {"question": "How many servings of vegetables do you eat per day?", "options": {"0": 0, "1-2": 2, "3-4": 4, "5 or more": 5}},
    {"question": "How many hours of sleep do you get per night?", "options": {"Less than 5": 1, "5-6": 3, "7-8": 5, "More than 8": 4}},
    {"question": "How often do you feel stressed?", "options": {"Always": 0, "Often": 1, "Sometimes": 3, "Rarely": 5}}
]

def main():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.score = 0

    if st.session_state.current_question < len(questions):
        question = questions[st.session_state.current_question]
        st.header(f"Question {st.session_state.current_question + 1}")
        st.write(question["question"])
        
        for option, points in question["options"].items():
            if st.button(option):
                st.session_state.score += points
                st.session_state.current_question += 1
                st.experimental_rerun()
    else:
        st.header("Your Total Score")
        st.write(f"Your total score is: {st.session_state.score}")
        if st.button("Restart"):
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.experimental_rerun()

if __name__ == "__main__":
    main()
