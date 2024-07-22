import streamlit as st

page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
    background: linear-gradient(#B7B6C1, #EDDFEF);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Define the questions, categories, and their corresponding point values
questions = [
    {"category": "Vision", "question": "Have you noticed any sudden changes in your vision, such as blurred or distorted vision?", "options": {"Yes": 3, "No": 0, "Not sure": 0}, "type": "button"},
    {"category": "Vision", "question": "Do you experience difficulty in seeing at night or in low-light conditions?", "options": {"Yes": 2, "No": 0, "Not sure": 0}, "type": "button"},
    {"category": "Vision", "question": "Are there any dark spots or floaters in your vision that appear to drift across your field of view?", "options": {"Yes": 2, "No": 0, "Not sure": 0}, "type": "button"},
    {"category": "Eye Symptoms", "question": "Do you experience frequent eye pain or discomfort?", "options": {"Yes": 2, "No": 0, "Not sure": 0}, "type": "button"},
    {"category": "Eye Symptoms", "question": "Have you noticed any redness or inflammation in your eyes?", "options": {"Yes": 2, "No": 0, "Not sure": 0}, "type": "button"},
    {"category": "Eye Symptoms", "question": "Are your eyes more sensitive to light than usual?", "options": {"Yes": 1, "No": 0, "Not sure": 0}, "type": "button"},
    {"category": "Medical History", "question": "How well have you been managing your blood sugar levels?", "options": {"Poorly": 3, "Moderately": 2, "Well": 0, "Not sure": 0}, "type": "button"},
    {"category": "Medical History", "question": "Do you have high blood pressure or cholesterol levels?", "options": {"Yes": 2, "No": 0, "Not sure": 0}, "type": "button"},
    {"category": "Medical History", "question": "Have you had diabetes for a long period (more than 5-10 years)?", "options": {"Yes": 3, "No": 0, "Not sure": 0}, "type": "button"},
    {"category": "Routine Eye Exams", "question": "When was your last comprehensive eye exam by an eye specialist?", "options": {"More than a year ago": 3, "Within the last year": 1, "Within the last six months": 0, "Not sure": 0}, "type": "button"},
    {"category": "Routine Eye Exams", "question": "Have you ever been diagnosed with any eye conditions related to diabetes?", "options": {"Yes": 3, "No": 0, "Not sure": 0}, "type": "button"},
    {"category": "General Health", "question": "Are you taking any medications for diabetes, and are you consistent with them?", "options": {"No": 3, "Sometimes": 2, "Yes": 0, "Not sure": 0}, "type": "button"},
    {"category": "General Health", "question": "Have you experienced any sudden weight changes recently?", "options": {"Yes": 2, "No": 0, "Not sure": 0}, "type": "button"},
    {"category": "General Health", "question": "Do you have any other chronic conditions that could affect your vision?", "options": {"Yes": 2, "No": 0, "Not sure": 0}, "type": "button"},
    {"category": "Additional Questions", "question": "Do you smoke or use tobacco products?", "options": {"Yes": 3, "No": 0, "Not sure": 0}, "type":"button"},
    {"category": "Additional Questions", "question": "Do you engage in regular physical activity (at least 30 minutes, 3 times a week)?", "options": {"No": 2, "Yes": 0, "Not sure": 0}, "type": "button"},
    {"category": "Additional Questions", "question": "Do you follow a balanced diet that includes vegetables, fruits, and whole grains?", "options": {"No": 2, "Yes": 0, "Not sure": 0}, "type": "button"},
    {"category": "Additional Questions", "question": "What is your BMI", "options": {"Below 18.5": 0, "18.5-24.9": 0, "25.0-29.9": 0, "Above 30.0": 0}, "type":"button"},
    {"category": "Additional Questions", "question": "Do you drink at least 8 glasses of water daily?", "options": {"No": 1, "Yes": 0, "Not sure": 0}, "type":"button"},
]

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
