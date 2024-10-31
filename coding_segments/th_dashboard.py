import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Generate dummy data
data = {
    'Event': ['Event 1', 'Event 2', 'Event 3', 'Event 4', 'Event 5', 'Event 6', 'Event 7', 'Event 8', 'Event 9', 'Event 10'],
    'Date': [datetime.date(2023, 1, 1) + datetime.timedelta(days=x) for x in range(10)]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Initialize Streamlit app
st.title("Events Dashboard")

# Display the DataFrame
st.dataframe(df)

# Add a button to email the DataFrame
email_button = st.button("Email DataFrame")

if email_button:
    # Function to send email
    def send_email(subject, content, recipient):
        import smtplib
        from email.message import EmailMessage

        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = subject
        msg['From'] = 'mowrandom@gmail.com'
        msg['To'] = recipient

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('mowrandom@gmail.com', 'ZuhSqu73gm')
        server.send_message(msg)
        server.quit()

    # Convert DataFrame to CSV and send as email
    csv_content = df.to_csv(index=False)
    subject = "Events Dashboard"
    content = "Here is the CSV content of the Events Dashboard:\n\n{csv_content}"
    recipient = "zuhaib.mohiuddin@gmail.com"

    send_email(subject, content, recipient)
    st.write("Email sent successfully!")