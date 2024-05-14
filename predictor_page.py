import streamlit as st
import pandas as pd
import pickle
import math

# Load model
def load_model():
    with open('saved_corner_model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

model = load_model()

def show_predict_page():
    st.title("Premier League Number of Corners Predictor")
    st.write("### Enter data here")
    
    # Get predictors
    venues = ("Home", "Away")
    oppositions = ('West Ham',
    'Liverpool',
    'Sheffield Utd',
    'Manchester City',
    'Leicester City',
    'Manchester Utd',
    'Aston Villa',
    'Leeds United',
    'Wolves',
    'Tottenham',
    'Burnley',
    'Southampton',
    'Everton',
    'Chelsea',
    'Brighton',
    'West Brom',
    'Crystal Palace',
    'Newcastle Utd',
    'Fulham',
    'Brentford',
    'Norwich City',
    'Watford',
    'Arsenal')
    venue = st.selectbox("Venue", venues)
    if venue == "Win":
        venueCode = 1
    else:
        venueCode = 0
    opposition = st.selectbox("Opposition", oppositions)
    # Load csv dataframe
    matches_rolling = pd.read_csv("matches_rolling.csv")
    filtered_rows = matches_rolling[matches_rolling["opponent"] == opposition]
    opp_code = filtered_rows.iloc[0]["opp_code"]
    prev_shots_total = st.slider("Enter shots on target in the previous game", 0, 50, 3)
    gf_rolling = st.number_input("Enter rolling gf (average gf in the last 3 games)", 0.0, 100.0, step=0.10)
    ga_rolling = st.number_input("Enter rolling ga (average ga in the last 3 games)", 0.0, 100.0, step=0.10)
    xg_rolling = st.number_input("Enter rolling xg (average xg in the last 3 games)", 0.0, 100.0, step=0.10)
    xga_rolling = st.number_input("Enter rolling xga (average xga in the last 3 games)", 0.0, 100.0, step=0.10)
    poss_x_rolling = st.slider("Enter rolling possesion (average possesion in the last 3 games to the nearest integer)", 0, 100, 50)
    ck_rolling = st.number_input("Enter rolling corner (average corners in the last 3 games)", 0.0, 100.0, step=0.10)
    touches_rolling = st.slider("Enter rolling touche (average touches in the last 3 games to the nearest integer)", 0, 2000, 500)
    result_rolling = st.number_input("Enter rolling result (average result in the last 3 games)", 0.0, 1.0, step=0.10)

    # Make prediction
    ok = st.button("Calculate Corner Prediction")
    if ok:
        # Create input dataframe for model
        future_game = {
        "venue_code": venueCode,
        "opp_code": opp_code,
        "prev_shots_total": prev_shots_total,
        "gf_rolling": gf_rolling,
        "ga_rolling": ga_rolling,
        "xg_rolling": xg_rolling,
        "xga_rolling": xga_rolling,
        "poss_x_rolling": poss_x_rolling,
        "ck_rolling": ck_rolling,
        "touches_rolling": touches_rolling,
        "binary_result_rolling": result_rolling
        }
        future_game_df = pd.DataFrame([future_game])

        # Predictors
        future_predictors = ["venue_code", "opp_code", "prev_shots_total", "gf_rolling", 
                        "ga_rolling", "xg_rolling", "xga_rolling", "poss_x_rolling", 
                        "ck_rolling", "touches_rolling", "binary_result_rolling"]
        corner_prediction = model.predict(future_game_df[future_predictors])[0].round()
        st.subheader(f"The predicted number of corners is {corner_prediction}")