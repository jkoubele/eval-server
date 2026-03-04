import streamlit as st
import pandas as pd
from enum import StrEnum
from time import time

class Challenges(StrEnum):
    CHALLENGE_1 = "Population of naked mole rats"
    CHALLENGE_2 = "Coffin break"

import pandas as pd

st.title('Programming challenges')

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

challenge = st.selectbox(
    'Select a challenge',
     [x.value for x in Challenges])

st.header("Task description")
if challenge == Challenges.CHALLENGE_1:
    st.write("You wanna se the mole naked?")
    
    with open("challenge_1.zip", "rb") as file:
        st.download_button(
            label="Download challenge starter pack",
            data=file,
            file_name="challenge_1.zip")
    
elif challenge == Challenges.CHALLENGE_2:
    st.write("Coffee!")
    
st.header("Submit a solution")


name = st.text_input("Your name:")
uploaded_file = st.file_uploader('Upload a solution')


if uploaded_file is not None:
    if not name:
        st.badge("Please provide your name", color="red")
    else:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
    
        st.success(f"File uploaded: {uploaded_file.name}")
        


st.header("Leaderboard")
mock_results = pd.DataFrame(data={'Time': [1,2,3],
                                  'Name': ['Jakub', 'Lara', 'Pavel']})
st.dataframe(mock_results)