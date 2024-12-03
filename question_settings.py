import streamlit as st
import requests
import random
import json
import pandas as pd

def fetch_questions(amount=5, category=None, difficulty=None, q_type=None):
    url = "https://opentdb.com/api.php"
    params = {
        "amount": amount,
        "category": category,
        "difficulty": difficulty,
        "type": q_type,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["response_code"] == 0:
            return data["results"]
        else:
            st.error("No questions available for the selected options.")
    else:
        st.error("Failed to fetch data from the API.")
    return []

def question_settings():
    st.sidebar.title("Question Settings")
    st.sidebar.divider()
    
    # Set number of questions
    amount = st.sidebar.slider("Number of Questions", 5, 20, key="slider_questions")

    with open("categories.json", "r") as f:
        data = json.load(f)

    categories = [item["name"] for item in data["categories"]]
    category = st.sidebar.selectbox("Category", categories, key="select_category")

    # Difficulty selection
    diff_mapping = {"Easy": "easy", "Medium": "medium", "Hard": "hard"}
    selected_difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="select_difficulty")
    difficulty = diff_mapping[selected_difficulty]

    # Question type selection
    type_mapping = {"Multiple Choice": "multiple", "True/False": "boolean"}
    selected_type = st.sidebar.selectbox("Question Type", ["Multiple Choice", "True/False"], key="select_type")
    q_type = type_mapping[selected_type]

    st.sidebar.divider()

    if st.sidebar.button("Start!", key="start_button"):
        # Get category id from categories.json
        category_id = next((item["id"] for item in data["categories"] if item["name"] == category), None)
        questions = fetch_questions(amount, category_id, difficulty, q_type)

        if questions:
            st.session_state["questions"] = questions
            st.session_state["answers"] = [None] * len(questions)  # Initialize answers in session state

    if "questions" in st.session_state:
        questions = st.session_state["questions"]
        st.subheader("Answer the Questions")

        with st.form(key="form_questions"):
            answers = []

            for idx, question in enumerate(questions):
                st.write(f"**Question {idx + 1}:** {question['question']}")
                options = question["incorrect_answers"] + [question["correct_answer"]]
                # random.shuffle(options)

                # Pre-select the answer if it exists in session state
                selected_answer = st.radio(
                    f"Choose an answer for Question {idx + 1}",
                    options,
                    key=f"question_{idx + 1}",
                    index=None
                )
                answers.append(selected_answer)

            submitted = st.form_submit_button("Submit Answers")
            if submitted:
                st.session_state["answers"] = answers  # Store the selected answers in session state
                score = 0
                results = []

                for idx, question in enumerate(questions):
                    user_answer = st.session_state["answers"][idx]
                    correct_answer = question["correct_answer"]
                    results.append({
                        "Question": question["question"],
                        "Your Answer": user_answer,
                        "Correct Answer": correct_answer,
                        "Correct?": "Yes" if user_answer == correct_answer else "No"
                    })
                    if user_answer == correct_answer:
                        score += 1

                st.write(f"**Your Score:** {score}/{len(questions)}")

                # Display the results in a table format
                results_df = pd.DataFrame(results)
                st.table(results_df)

