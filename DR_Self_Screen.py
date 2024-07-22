import streamlit as st
from Question import questions

page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
    background: linear-gradient(#B7B6C1, #EDDFEF);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Define the questions, categories, and their corresponding point values


# Calculates risk based on user input
def calculate_risk_level(score):
    if score <= 5:
        st.balloons()
        return "Low Risk of Diabetic retinopathy"
    elif score <= 10:
        return "Moderate Risk of Diabetic retinopathy"
    elif score <= 20:
        return "High Risk of Diabetic retinopathy"
    else:
        return "Very High Risk of Diabetic retinopathy"
    
# Calculates risk based on user input
def main():
    # Initialize session state variables
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.score = 0

    if st.session_state.current_question < len(questions):
        question = questions[st.session_state.current_question]

        col1, col2 = st.columns([2, 1],vertical_alignment="center")  # Create two columns with a 2:1 ratio
        
        with col1:
            st.header(question['category'])
            st.write(question["question"])

            # Arrange options horizontally and evenly
            num_options = len(question["options"])
            option_cols = st.columns(num_options)
            for col, (option, points) in zip(option_cols, question["options"].items()):
                if col.button(option):
                    st.session_state.score += points
                    st.session_state.current_question += 1
                    st.experimental_rerun()

            # Return button beneath the options
            if st.session_state.current_question > 0:
                if st.button("Return"):
                    st.session_state.current_question -= 1
                    st.experimental_rerun()
        
        with col2:
            st.image("https://images.unsplash.com/photo-1548407260-da850faa41e3?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1487&q=80")  # Placeholder image

        # Dynamic progress bar at the bottom
        progress = (st.session_state.current_question + 1) / len(questions)
        st.progress(progress)

    else:
        # End screen showing score
        st.header("Your Total Score")
        st.write(f"Your total score is: {st.session_state.score}")
        risk_level = calculate_risk_level(st.session_state.score)
        st.write(f"Risk Level: {risk_level}")
        
        # Restarts questionnaire
        if st.button("Restart"):
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.experimental_rerun()




if __name__ == "__main__":
    main()
