import streamlit as st
import pandas as pd
from Question import questions
from datetime import datetime

# Custom CSS for styling
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-color: #FFFFFF;
}}
[data-testid="stSidebar"] {{
    background-color: #43A047;
}}
.stButton>button {{
    background-color: #1E88E5;
    color: white;
    border-radius: 5px;
}}
.stButton>button:hover {{
    background-color: #FFB300;
    color: black;
}}
.stProgress>div>div {{
    background-color: #1E88E5;
}}
h1, h2, h3, h4 {{
    color: #1E88E5;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# File to store the results
RESULTS_FILE = "results.csv"

# Function to save results
def save_results(score, risk_level, answers):
    # Load existing data
    try:
        results_df = pd.read_csv(RESULTS_FILE)
    except FileNotFoundError:
        results_df = pd.DataFrame(columns=["Date", "Score", "Risk Level", "Answers"])

    # Append new data
    new_result = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M:%S"), score, risk_level, str(answers)]], columns=["Date", "Score", "Risk Level", "Answers"])
    results_df = pd.concat([results_df, new_result], ignore_index=True)

    # Save to CSV
    results_df.to_csv(RESULTS_FILE, index=False)

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

# Main function to run the Streamlit app
def main():
    # Initialize session state variables
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answers = []
        st.session_state.started = False

    # Starting page
    if not st.session_state.started:
        st.title("Diabetic Retinopathy Test")
        if st.button("Begin"):
            st.session_state.started = True
            st.experimental_rerun()
    else:
        if st.session_state.current_question < len(questions):
            question = questions[st.session_state.current_question]

            col1, col2 = st.columns([2, 1])  # Create two columns with a 2:1 ratio

            with col1:
                st.header(question['category'])
                st.write(question["question"])

                # Arrange options horizontally and evenly
                num_options = len(question["options"])
                option_cols = st.columns(num_options)
                for col, (option, points) in zip(option_cols, question["options"].items()):
                    if col.button(option):
                        st.session_state.score += points
                        st.session_state.answers.append((question["question"], option, points))
                        st.session_state.current_question += 1
                        st.experimental_rerun()

                # Return button beneath the options
                if st.session_state.current_question > 0:
                    if st.button("Return"):
                        last_answer = st.session_state.answers.pop()
                        st.session_state.score -= last_answer[2]  # Subtract points
                        st.session_state.current_question -= 1
                        st.experimental_rerun()

            with col2:
                st.image(question["image"], use_column_width=True)

            # Dynamic progress bar at the bottom
            progress = (st.session_state.current_question + 1) / len(questions)
            st.progress(progress)

        else:
            # End screen showing score
            st.header("Your Total Score")
            st.write(f"Your total score is: {st.session_state.score}")
            risk_level = calculate_risk_level(st.session_state.score)
            st.write(f"Risk Level: {risk_level}")

            # Save results to file
            save_results(st.session_state.score, risk_level, st.session_state.answers)

            # Provide download link for results
            results_df = pd.read_csv(RESULTS_FILE)
            st.download_button(
                label="Download Results",
                data=results_df.to_csv(index=False).encode('utf-8'),
                file_name=RESULTS_FILE,
                mime='text/csv'
            )

            # Restarts questionnaire
            if st.button("Restart"):
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.answers = []
                st.session_state.started = False
                st.experimental_rerun()

if __name__ == "__main__":
    main()
