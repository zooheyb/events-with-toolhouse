import streamlit as st
import pandas as pd

# Create a DataFrame with the events data
data = {
    "Event Name": [
        "SF and Bay Area AI Events - Events Calendar",
        "AI Expo & Solution Showcase at ODSC West 2024",
        "GenAI Summit Silicon Valley 2024",
        "The AI Conference 2024",
        "TechCrunch Disrupt 2024 Side Events Schedule",
        "40 AI Conferences in 2024 - 2025: Speakers from OpenAI, ...",
        "SF Tech Events",
        "Discover AI Events & Activities in San Francisco, CA",
        "Tech Conferences: The Best Tech Events Guide for 2024",
        "ODSC | Gen AI X Summit 2024"
    ],
    "Date": [
        "October 29, 2024",
        "October 29, 2024",
        "November 1 to November 3, 2024",
        "September 10th and 11th, 2024",
        "October 30, 2024",
        "Various dates in 2024 and 2025",
        "Various dates in 2024",
        "Various dates in 2024",
        "Various dates in 2024",
        "October 29, 2024"
    ],
    "Link": [
        "https://lu.ma/genai-sf",
        "https://www.eventbrite.com/d/ca--san-francisco/artificial-intelligence/",
        "https://genaisummit.ai/",
        "https://aiconference.com/",
        "https://techcrunch.com/2024/10/23/techcrunch-disrupt-2024-side-events-schedule-mercury-jetro-enterprise-ireland-and-more-to-host/",
        "https://kristihines.com/ai-conferences/",
        "https://www.garysguide.com/events?region=sfbay",
        "https://www.eventbrite.ca/d/ca--san-francisco/ai/",
        "https://www.bizzabo.com/blog/technology-events",
        "https://agendahero.com/schedule/0f8899a0-3dbc-4d6a-ad05-58225b751316"
    ]
}

df = pd.DataFrame(data)

# Create a Streamlit app
st.title("AI Events Dashboard")

# Display the DataFrame in the Streamlit app
st.dataframe(df)