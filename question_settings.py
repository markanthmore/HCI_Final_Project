import streamlit as st
import requests
import random
import json
from game_settings import game_settings



#TRIVIA QUESTION FETCH FUNCTION
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


#QUESTION SETTINGS FUNCTION
def question_settings():
    if "round_count" not in st.session_state:
        st.error("Round count is not set. Please go back to Game Settings.")
        if st.button("Back to Game Settings"):
            st.session_state.step = "game_settings"
        return

    round_count = st.session_state.round_count

    for i in range(1, round_count + 1):
        st.sidebar.title(f"Round {i}")
        st.sidebar.divider()
        st.sidebar.header("Adjust Question Settings")

        # Number of questions
        amount = st.sidebar.slider("Number of Questions", 1, 20, key=f"slider_round_{i}")

        # Load categories from JSON
        with open("categories.json", "r") as f:
            data = json.load(f)

        categories = [item["name"] for item in data["categories"]]
        category = st.sidebar.selectbox("Category", categories, key=f"select_cat_round_{i}")

        # Difficulty
        diff_mapping = {"Easy": "easy", "Medium": "medium", "Hard": "hard"}
        selected_difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key=f"diff_round_{i}")
        difficulty = diff_mapping[selected_difficulty]

        # Question Type
        type_mapping = {"Multiple Choice": "multiple", "True/False": "boolean"}
        selected_type = st.sidebar.selectbox("Question Type", ["Multiple Choice", "True/False"],
                                             key=f"type_round_{i}")
        q_type = type_mapping[selected_type]

        st.sidebar.divider()

        if st.sidebar.button("Fetch Questions", key=f"fetch_round_{i}"):
            category_id = next((item["id"] for item in data["categories"] if item["name"] == category), None)
            questions = fetch_questions(amount, category_id, difficulty, q_type)

            if questions:
                st.session_state[f"questions_round_{i}"] = questions
                st.session_state[f"answers_round_{i}"] = [None] * len(questions)

    # Display questions for the current round
    for i in range(1, round_count + 1):
        if f"questions_round_{i}" in st.session_state:
            questions = st.session_state[f"questions_round_{i}"]

            st.subheader(f"Round {i}: Answer the Questions")
            with st.form(key=f"form_round_{i}"):
                for idx, question in enumerate(questions):
                    st.write(f"**Question {idx + 1}:** {question['question']}")
                    options = question["incorrect_answers"] + [question["correct_answer"]]
                    random.shuffle(options)

                    # Only pre-select if there is already an answer stored
                    default_index = (
                        options.index(st.session_state[f"answers_round_{i}"][idx])
                        if st.session_state[f"answers_round_{i}"][idx] in options
                        else None
                    )

                    st.session_state[f"answers_round_{i}"][idx] = st.radio(
                        f"Choose an answer for Question {idx + 1}",
                        options,
                        key=f"round_{i}_question_{idx + 1}",
                        index=default_index,
                    )
                submitted = st.form_submit_button("Submit Answers")
                if submitted:
                    # Calculate scores and display results
                    score = 0
                    for idx, question in enumerate(questions):
                        user_answer = st.session_state[f"answers_round_{i}"][idx]
                        correct_answer = question["correct_answer"]
                        st.write(f"**Question {idx + 1}:** {question['question']}")
                        st.write(f"**Your Answer:** {user_answer} | **Correct Answer:** {correct_answer}")
                        if user_answer == correct_answer:
                            score += 1
                    st.write(f"**Round {i} Score:** {score}/{len(questions)}")


                # Show all answers at the end
                # st.write("Your current answers:", st.session_state[f"answers_round_{i}"])
