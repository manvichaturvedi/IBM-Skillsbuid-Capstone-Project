import streamlit as st
import pickle

model_use = pickle.load(open('model_pred.pkl','rb'))

st.title('User Ad Click Predictor')
Age = int(st.text_input("Enter The Age"))

result = model_use.predict(Age)[0]

if(result == 1) :
    st.header("Yes")
else:
    st.header("No")