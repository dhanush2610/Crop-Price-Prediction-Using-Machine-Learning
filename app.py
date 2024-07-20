import streamlit as st
import pandas as pd
import pickle

# Load the trained model and columns
with open("crop_price_prediction_model.pkl", 'rb') as f:
    model = pickle.load(f)

with open("Crop Price Prediction\crop_price_columns.pkl", 'rb') as f:
    columns = pickle.load(f)

st.title('Crop Price Prediction')
st.image("img1.jpg")
st.write("""
Enter the agricultural data to predict crop prices.
""")

# Sidebar - Input parameters
st.sidebar.header('Input Parameters')

def user_input_features():
    State = st.sidebar.selectbox('State', ['Select State','Uttar Pradesh', 'Karnataka', 'Gujarat', 'Andhra Pradesh',
       'Maharashtra', 'Punjab', 'Haryana', 'Rajasthan', 'Madhya Pradesh',
       'Tamil Nadu', 'Bihar', 'Orissa', 'West Bengal'])  # Update with actual state names
    
    Crop = st.sidebar.selectbox('Crop', ['Select Crop','ARHAR', 'COTTON', 'GRAM', 'GROUNDNUT', 'MAIZE', 'MOONG', 'PADDY',
       ' MUSTARD', 'SUGARCANE', 'WHEAT'])  # Update with actual crop names
    
    CostCultivation = st.sidebar.slider('Cost of Cultivation (per hectare)', 0, 20000, 0000)
    Production = st.sidebar.slider('Production (tons)', 0.0, 4000.0, 00.0)
    Yield = st.sidebar.slider('Yield (tons per hectare)', 0.0, 1500.0, 0.0)
    Temperature = st.sidebar.slider('Temperature (in Celsius)', 0.0, 50.0, 00.0)
    Rainfall_Annual = st.sidebar.slider('Annual Rainfall (in mm)', 0.0, 4000.0, 0000.0)
    data = {
        'State': State,
        'Crop': Crop,
        'CostCultivation': CostCultivation,
        'Production': Production,
        'Yield': Yield,
        'Temperature': Temperature,
        'Rainfall Annual': Rainfall_Annual
    }
    features = pd.DataFrame(data, index=[1])
    return features

input_df = user_input_features()

# One-hot encode the 'Crop' feature
input_df_encoded = pd.get_dummies(input_df, columns=['Crop'])

# Ensure all columns used during training are present
missing_cols = set(columns) - set(input_df_encoded.columns)
for col in missing_cols:
    input_df_encoded[col] = 0
input_df_encoded = input_df_encoded[columns]  # Reorder columns to match training order

# Display user input parameters
st.subheader('User Input Parameters')
st.write(input_df)

# Predicting crop yield
prediction = model.predict(input_df_encoded)

# Display the prediction
st.markdown(f"<h3 style='text-align: left; font-size: 20px;'>Predicted Crop Price</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: left; font-size: 18px;'>Price: ${prediction[0]:.2f}</p>", unsafe_allow_html=True)