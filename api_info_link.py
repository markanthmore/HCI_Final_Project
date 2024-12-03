import streamlit as st
import requests
import pandas as pd  

@st.cache_data  # SAVA DATA ON API CALL
def fetch_category_data():
    url_categories = "https://opentdb.com/api_category.php"
    url_numQuestions = "https://opentdb.com/api_count.php"
    
    # CATEGORY COLLECTION
    category_response = requests.get(url_categories)
    category_response.raise_for_status()
    categories_data = category_response.json().get("trivia_categories", [])

    category_counts = []
    
    #COLLECT QUESTIONS FOR CATEGORIES
    for category in categories_data:
        #MAKE SURE CATEGORY IS A DICTIONARY
        if isinstance(category, dict) and "id" in category and "name" in category:
            category_id = int(category["id"]) 

            #CLEAN TO SHOW CAT NAME ONLY
            category_name = category["name"].split(":")[-1].strip()

            #FETCH QUESTION COUNT FOR CAT
            question_count_url = f"{url_numQuestions}?category={category_id}"
            question_count_response = requests.get(question_count_url)
            question_count_response.raise_for_status()
            question_count_data = question_count_response.json()

            #EXTRACT TOTAL QUESTION COUNTS
            total_questions = question_count_data.get("category_question_count", {}).get("total_question_count", 0)

            #ADD TO CATEGORY COUNTS
            category_counts.append({"Category Name": category_name, "Total Number of Questions": total_questions})
    
    return category_counts

def api_info_link():
    st.sidebar.title("API Info")
    barchartShown = st.sidebar.checkbox("API Question Count")

    try:
        #FETCH CATEGORY DATA
        category_counts = fetch_category_data()

        #DATAFRAME CREATION
        df = pd.DataFrame(category_counts)

        #DISPLAY BAR CHART

        if barchartShown: 

            st.write("Total Questions per Category")
            st.bar_chart(data=df, x="Category Name", y="Total Number of Questions", use_container_width=True)

    except requests.exceptions.RequestException as e:
        st.write(f"Error fetching data: {e}")

