import streamlit as st
from api.aviationstack_client import get_flight_status
from api.weatherstack_client import get_weather_data
from api.gemini_client import generate_flight_insight

# Set page configuration and title
st.set_page_config(page_title="Flight Ops Intelligence", layout="wide")
st.title("✈️ Flight Operations Intelligence Assistant")

# Sidebar Input: Flight IATA code
with st.sidebar:
    st.header("Flight Input")
    flight_iata = st.text_input("Enter Flight IATA Code (e.g., AI203):")

# Main content area
if flight_iata:
    with st.spinner("Fetching flight data..."):
        data = get_flight_status(flight_iata)
        if "data" in data and len(data["data"]) > 0:
            flight = data["data"][0]

            # Display key flight details in two columns
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Airline", flight["airline"]["name"])
                st.metric("Flight", flight["flight"]["iata"])
                st.metric("Departure Airport", flight["departure"]["airport"])
                st.metric("Scheduled Departure", flight["departure"]["scheduled"])
            with col2:
                st.metric("Arrival Airport", flight["arrival"]["airport"])
                st.metric("Scheduled Arrival", flight["arrival"]["scheduled"])
                st.metric("Flight Status", flight["flight_status"])

            # Fetch weather data for both departure and arrival airports
            departure_weather = get_weather_data(flight["departure"]["airport"])
            arrival_weather = get_weather_data(flight["arrival"]["airport"])

            # Display weather information in two columns
            col1, col2 = st.columns(2)
            with col1:
                if 'current' in departure_weather:
                    st.metric(f"Departure Weather ({flight['departure']['airport']})",
                              f"{departure_weather['current']['temperature']}°C, {departure_weather['current']['weather_descriptions'][0]}")
                else:
                    st.warning(f"Weather data unavailable for {flight['departure']['airport']}")
            with col2:
                if 'current' in arrival_weather:
                    st.metric(f"Arrival Weather ({flight['arrival']['airport']})",
                              f"{arrival_weather['current']['temperature']}°C, {arrival_weather['current']['weather_descriptions'][0]}")
                else:
                    st.warning(f"Weather data unavailable for {flight['arrival']['airport']}")

            # Generate Gemini summary
            with st.spinner("Analyzing with Gemini..."):
                prompt = f"""
You're a flight ops assistant. Analyze this flight:
- Flight: {flight['flight']['iata']} ({flight['airline']['name']})
- Status: {flight['flight_status']}
- Departure: {flight['departure']['airport']} at {flight['departure']['scheduled']}
- Arrival: {flight['arrival']['airport']} at {flight['arrival']['scheduled']}
- Terminal: {flight['departure'].get('terminal')} → {flight['arrival'].get('terminal')}
- Delay (departure): {flight['departure'].get('delay')} mins
- Delay (arrival): {flight['arrival'].get('delay')} mins

Give a short operational summary and delay risk insight.
"""
                insight = generate_flight_insight(prompt)
                st.subheader("🧠 Gemini Insight")
                st.write(insight)
        else:
            st.error("No data found for this flight.")
