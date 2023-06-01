
import streamlit as st
import numpy as np
from urllib.request import urlopen
import json
import random
import pandas as pd
import html
st.title("Trivia Show")

if 'question' not in st.session_state:
    st.session_state.question = 0
if 'correct' not in st.session_state:
    st.session_state.correct = 0
if 'result_df' not in st.session_state:
    st.session_state.result_df = []
st.session_state.disabled = False


@st.cache_data
def decode_categories():
    cat_query = "https://opentdb.com/api_category.php"
    res = json.load(urlopen(cat_query))
    return res


@st.cache_data
def run_query(category_index, difficulty, n):
    query = f"https://opentdb.com/api.php?amount={n}"
    query += f"&category={category_index}&difficulty={difficulty}&type=multiple"
    response = json.load(urlopen(query))
    return response


def main():
    cats = decode_categories()
    catlog = {x["name"]: int(x["id"]) for x in cats["trivia_categories"]}
    category = st.sidebar.selectbox("Select Category", catlog.keys())
    difficulty = st.sidebar.selectbox(
        "Select Difficulty", ['Easy', 'Medium', 'Hard'])
    number_of_questions = st.sidebar.selectbox(
        "Questions", [10, 5, 15, 20, 25])
    category_index = catlog[category]
    response = run_query(category_index=category_index,
                         difficulty=difficulty.lower(), n=int(number_of_questions))
    total = len(response["results"])
    questions = response["results"]
    df = pd.DataFrame.from_records(questions)
    

    _, next_q = st.columns([10, 2])
    next = next_q.button("Next")
    if next:
        if st.session_state.question < total-1:
            st.session_state.question += 1
        else:
            try:
                st.subheader("Review")
                st.dataframe(pd.concat(st.session_state.result_df))
            except: 
                st.error("No answers selected")
            
    st.info(f" You got {st.session_state.correct}/{total} correct")
    if st.session_state.question >= 0 and st.session_state.question <= number_of_questions:
        question, user_ans, correct_ans = render_qc_ans(df, st.session_state.question)
        result = user_ans == correct_ans
        if user_ans == "Pick one of the following answers: ":
            st.warning("Not yet answered")
        else:
            if result:
                st.success(":white_check_mark: Correct")
                st.session_state.correct += 1

            else:
                st.error(":question: Incorrect")
                st.success(f"Correct answer is : {correct_ans}")

            df_res = pd.DataFrame.from_dict({'question': [question], 'result': [result], 'user answer': [user_ans], 'correct_answer': [correct_ans]})
            st.session_state.result_df.append(df_res)
    else:
        st.session_state.question = 0
        st.session_state.correct = 0
        st.session_state.result_df = []
        st.experimental_rerun()

def render_qc_ans(df, i):
    random.seed(i)
    question = df["question"].iloc[i]
    answer = html.unescape(df['correct_answer'].iloc[i])
    other_choices = df['incorrect_answers'].iloc[i]

    choices = other_choices + [answer]
    choices = random.sample(choices, len(choices))
    choices = [html.unescape(choice) for choice in choices]
    st.write(f"Q{i+1}: {question}", unsafe_allow_html=True)
    user_ans = st.radio("label", ["Pick one of the following answers: "] +
                        choices, label_visibility='collapsed')
    return question, user_ans, answer


if __name__ == '__main__':
    main()
