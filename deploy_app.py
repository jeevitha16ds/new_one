import streamlit as st
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the model
model = pickle.load(open('svm_model.pkl', 'rb'))

# Initialize the scaler
scaler = MinMaxScaler()

# Streamlit app
st.title('Insurance Charges Prediction')

# Collect input data
age = st.number_input('Age', min_value=0, max_value=100, value=25)
gender = st.selectbox('Gender', ('male', 'female'))
bmi = st.number_input('BMI', min_value=0.0, max_value=100.0, value=25.0)
smoker = st.selectbox('Smoker', ('yes', 'no'))
children = st.number_input('Number of Children', min_value=0, max_value=10, value=0)
region = st.selectbox('Region', ('southwest', 'northwest', 'northeast', 'southeast'))

# Convert inputs to the format expected by the model
gender = 1 if gender == 'male' else 0
smoker = 1 if smoker == 'yes' else 0
region_dict = {'southwest': 0, 'northwest': 1, 'northeast': 2, 'southeast': 3}
region = region_dict[region]

# Prepare the input features as a DataFrame with correct column names
input_features = pd.DataFrame({
    'age': [age],
    'sex_male': [gender],
    'bmi': [bmi],
    'smoker': [smoker],
    'children': [children],
    'region': [region]
})

# Scale the numerical features
input_features[['age', 'bmi']] = scaler.fit_transform(input_features[['age', 'bmi']])

# Prediction
if st.button('Predict'):
    prediction = model.predict(input_features)
    output = round(np.exp(prediction[0]), 2)
    st.success('Predicted Charges: ${}'.format(output))
