import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from Question import questions  # Ensure this import is correct in your environment
from datetime import datetime
import base64
from io import BytesIO
from fpdf import FPDF  # Ensure you have fpdf installed
import firebase_admin
from firebase_admin import credentials, firestore

# Load environment variables from the .env file
load_dotenv()

# Get the Firebase key path from the environment variable
firebase_key_path = os.getenv('FIREBASE_KEY_PATH')

# Check if the environment variable is loaded correctly
if firebase_key_path is None:
    raise ValueError("FIREBASE_KEY_PATH environment variable not set")

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_key_path)  # Use the environment variable
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Custom CSS for styling
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #FFFFFF;
}
[data-testid="stSidebar"] {
    background-color: #43A047;
}
.stButton>button {
    background-color: #1E88E5;
    color: white;
    border-radius: 5px;
}
.stButton>button:hover {
    background-color: #FFB300;
    color: black;
}
.stProgress>div>div {
    background-color: #1E88E5;
}
h1, h2, h3, h4 {
    color: #1E88E5;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Function to save results to Firestore
def save_results(score, risk_level, answers):
    # Convert answers to a list of dictionaries
    answers_dict = [{"question": question, "answer": answer, "points": points} for question, answer, points in answers]

    # Create a document reference
    doc_ref = db.collection("diabetes_results").document()
    # Prepare data
    data = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "score": score,
        "risk_level": risk_level,
        "answers": answers_dict
    }
    # Set the data in Firestore
    doc_ref.set(data)

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

# Function to create PDF
def create_pdf(score, risk_level, answers):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Diabetic Retinopathy Test Results", ln=True, align='C')
    pdf.ln(10)
    
    pdf.cell(200, 10, txt=f"Total Score: {score}", ln=True)
    pdf.cell(200, 10, txt=f"Risk Level: {risk_level}", ln=True)
    pdf.ln(10)
    
    pdf.cell(200, 10, txt="Answers:", ln=True)
    pdf.ln(10)
    
    for question, answer, points in answers:
        pdf.cell(200, 10, txt=f"Q: {question}", ln=True)
        pdf.cell(200, 10, txt=f"A: {answer}", ln=True)
        pdf.ln(5)
    
    return pdf

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

            # Save results to Firestore
            save_results(st.session_state.score, risk_level, st.session_state.answers)

            # Toggle for displaying answers table
            show_answers = st.checkbox("Show Answers Table")

            if show_answers:
                answers_df = pd.DataFrame(st.session_state.answers, columns=["Question", "Answer", "Points"])
                st.table(answers_df[["Question", "Answer"]])

            # Toggle for changing download button to create PDF
            create_pdf_button = st.button("Create PDF")

            if create_pdf_button:
                pdf = create_pdf(st.session_state.score, risk_level, st.session_state.answers)
                pdf_buffer = BytesIO()
                pdf.output(pdf_buffer)
                pdf_buffer.seek(0)
                b64 = base64.b64encode(pdf_buffer.read()).decode('latin1')
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="results.pdf">Download PDF</a>'
                st.markdown(href, unsafe_allow_html=True)
            else:
                # Provide download link for results in CSV format
                results_df = pd.DataFrame([{
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Score": st.session_state.score,
                    "Risk Level": risk_level,
                    "Answers": st.session_state.answers
                }])
                st.download_button(
                    label="Download Results",
                    data=results_df.to_csv(index=False).encode('utf-8'),
                    file_name="results.csv",
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
