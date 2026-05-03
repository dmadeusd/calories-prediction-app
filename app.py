import streamlit as st
import joblib
import pandas as pd

st.set_page_config(page_title="Calories Burnt Predictor", page_icon="🔥", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #0b0b0b;
    }

    h1, h2, h3, p, label, .stMarkdown {
        color: white !important;
    }

    div.stButton > button:first-child {
        background-color: #ff0000 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px;
        font-weight: bold;
        font-size: 18px;
        height: 50px;
        transition: 0.3s;
    }

    div.stButton > button:first-child:hover {
        background-color: #b30000 !important; 
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
    }

    .box-bmr {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .box-calories {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%); 
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
    }

    .big-font {
        font-size: 36px !important;
        font-weight: bold;
        margin: 0;
    }
    .small-font {
        font-size: 16px !important;
        opacity: 0.9;
    }

    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #1e1e1e !important;
        color: white !important;
        border: 1px solid #444 !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    model = joblib.load('./Model/rf_model.sav')
    return model

model = load_model()

def calculate_bmr(gender, weight, height, age):
    if gender == 'Male':
        return (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        return (10 * weight) + (6.25 * height) - (5 * age) - 161

st.title("Calories Burnt Prediction App")
st.write("Please enter your personal data and physical activity to predict calories burned!")
st.divider()

col1, col2 = st.columns(2)

with col1:
    gender_input = st.selectbox("Gender", options=['Male', 'Female'])
    age_input = st.number_input("Age (Years)", min_value=10, max_value=100, value=25, step=1)
    height_input = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1, format="%.1f")

with col2:
    weight_input = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=65.0, step=0.1, format="%.1f")
    heart_rate_input = st.number_input("Average Heart Rate (bpm)", min_value=60.0, max_value=200.0, value=100.0, step=0.1, format="%.1f")
    duration_input = st.number_input("Duration of Exercise (Minutes)", min_value=1.0, max_value=300.0, value=30.0, step=0.1, format="%.1f")

if st.button("Start Prediction", use_container_width=True):
    bmr_value = calculate_bmr(gender_input, weight_input, height_input, age_input)

    input_data = pd.DataFrame({
        'Age': [age_input],
        'Heart_Rate': [heart_rate_input],
        'Duration': [duration_input],
        'BMR': [bmr_value]
    })

    predicted_calories = model.predict(input_data)[0]
    
    st.divider()
    st.subheader("Prediction Results")

    st.markdown(f"""
        <div class="box-bmr">
            <p class="small-font">Your Basal Metabolic Rate (BMR)</p>
            <p class="big-font">{bmr_value:.1f} <span style="font-size:20px;">kcal/hari</span></p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="box-calories">
            <p class="small-font">Estimated Calories Burned During Exercise</p>
            <p class="big-font">{predicted_calories:.1f} <span style="font-size:20px;">kcal</span></p>
        </div>
    """, unsafe_allow_html=True)