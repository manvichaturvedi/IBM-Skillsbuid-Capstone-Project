from altair import themes
import streamlit as st
import pickle
import sklearn
import numpy as np
st.header('User Ad Click Predictor Web App: By Manvi', divider='rainbow')

st.markdown("""
<style>
   h1 {
      font-size: 25px;
      text-align: center;
      text-transform: uppercase;
   }
  [data-testid="stAppViewContainer"] {
    background-image: linear-gradient(rgb(15, 18, 23), rgb(44, 62, 80));
}

</style>
""", unsafe_allow_html=True)


model_use = pickle.load(open('model_pred1.pkl','rb'))
Daily_Time_Spent_on_Site = st.number_input("Enter The Daily_Time_Spent_on_Site",key="a")
Age = st.number_input("Enter The Age",key="b")
Area_Income = st.number_input("Enter The Area Income",key="c")
Daily_Internet_Usage = st.number_input("Enter The Daily_Internet_Usage ",key="d")
Male = st.number_input("Enter The Gender",key="e")
parameter = np.array([[Daily_Time_Spent_on_Site, Age, Area_Income, Daily_Internet_Usage, Male]])

if st.button('Predict') :
  result = model_use.predict(parameter)[0]

  if(result == 1) :
    st.header("Yes, The User Will Click On The Add")
  else:
    st.header("No, The User Will not Click On The add")