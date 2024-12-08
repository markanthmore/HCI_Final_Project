import streamlit as st
import requests
import random
import json
import pandas as pd
import time
from PIL import Image
from geopy.geocoders import Nominatim
from game_settings import game_settings

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
    
    amount = st.sidebar.slider("Number of Questions", 5, 20, key="slider_questions")

    with open("categories.json", "r") as f:
        data = json.load(f)

    categories = [item["name"] for item in data["categories"]]
    category = st.sidebar.selectbox("Category", categories, key="select_category")

    diff_mapping = {"Easy": "easy", "Medium": "medium", "Hard": "hard"}
    selected_difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="select_difficulty")
    difficulty = diff_mapping[selected_difficulty]

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
            st.session_state["answers"] = [None] * len(questions)

        
    
    if "questions" in st.session_state:
        questions = st.session_state["questions"]
        st.title(f"**{st.session_state.get('player_name')} Start!**")

        if 'player_avatar' in st.session_state:
                    st.image(st.session_state.player_avatar)

        with st.form(key="form_questions"):
            answers = []

            for idx, question in enumerate(questions):
                st.write(f"**Question {idx + 1}:** {question['question']}")
                options = question["incorrect_answers"] + [question["correct_answer"]]

                
                selected_answer = st.radio(
                    f"Choose an answer for Question {idx + 1}",
                    options,
                    key=f"question_{idx + 1}",
                    index=None
                )
                answers.append(selected_answer)

            submitted = st.form_submit_button("Submit Answers")
            if submitted:
                timer = st.empty()
                with timer:
                    st.success("Answers Submitted")
                time.sleep(1)
                timer.empty()

                st.session_state["answers"] = answers
                score = 0
                results = []
                accumulated_scores = []

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
                    else: 
                        score -= 1
                        
                    accumulated_scores.append(score)   

                st.subheader(f"**{st.session_state.get('player_name')}'s Score:** {score}/{len(questions)}")
                st.divider()

                
                #DISPLAY ANSWERS IN TABLE
                st.write("**Answer Summary**")
                results_df = pd.DataFrame(results)
                st.table(results_df)
                
                #CREATE DATAFRAME FOR LINE CHART
                chart_data = pd.DataFrame({
                    "Question Number": range(1, len(accumulated_scores) + 1),
                    "Cumulative Score": accumulated_scores
                })

                st.divider()
                
                #LINE CHART DISPLAY
                st.write("**Point Progress**")
                st.line_chart(chart_data.set_index("Question Number"))

                st.divider()

                st.write("**Current Location**")
                
                geolocator = Nominatim(user_agent="geoapi")
                location = geolocator.geocode("Miami")

                latitude, longitude = location.latitude, location.longitude

                location_data = pd.DataFrame({'lat': [latitude], 'lon': [longitude]})

                st.map(location_data)
