import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Create dummy events data
def generate_dummy_events():
    events = [
        {"Event": "Team Meeting", "Date": datetime.now() + timedelta(days=1)},
        {"Event": "Product Launch", "Date": datetime.now() + timedelta(days=3)},
        {"Event": "Client Presentation", "Date": datetime.now() + timedelta(days=5)},
        {"Event": "Workshop", "Date": datetime.now() + timedelta(days=7)},
        {"Event": "Training Session", "Date": datetime.now() + timedelta(days=10)},
        {"Event": "Project Deadline", "Date": datetime.now() + timedelta(days=12)},
        {"Event": "Conference Call", "Date": datetime.now() + timedelta(days=15)},
        {"Event": "Team Building", "Date": datetime.now() + timedelta(days=18)},
        {"Event": "Board Meeting", "Date": datetime.now() + timedelta(days=20)},
        {"Event": "Quarterly Review", "Date": datetime.now() + timedelta(days=25)}
    ]
    return pd.DataFrame(events)

def send_email(events_df, recipient_email):
    # Email settings
    sender_email = "mowrandom@gmail.com"  # Replace with your email
    password = "ZuhSqu73gm"  # Replace with your app password
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Upcoming Events List"
    
    # Convert dataframe to HTML table
    html_table = events_df.to_html(index=False)
    body = f"""
    <html>
        <body>
            <h2>Your Upcoming Events</h2>
            {html_table}
        </body>
    </html>
    """
    
    msg.attach(MIMEText(body, 'html'))
    
    try:
        # Create server object with SSL option
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        # Perform login
        server.login(sender_email, password)
        # Send email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        # Close connection
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
        return False

def main():
    st.title("Event Dashboard")
    
    # Generate and display events
    events_df = generate_dummy_events()
    
    # Display events in a table
    st.subheader("Upcoming Events")
    st.dataframe(events_df.style.format({"Date": lambda x: x.strftime("%Y-%m-%d")}))
    
    # Email functionality
    st.subheader("Email Events")
    recipient_email = st.text_input("Enter your email:", value="zuhaib.mohiuddin@gmail.com")
    
    if st.button("Send Events to Email"):
        if recipient_email:
            with st.spinner('Sending email...'):
                if send_email(events_df, recipient_email):
                    st.success("Events have been sent to your email!")
        else:
            st.warning("Please enter an email address.")
    
    # Additional dashboard features
    st.subheader("Event Statistics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Events", len(events_df))
        
    with col2:
        events_this_week = len(events_df[events_df['Date'] <= datetime.now() + timedelta(days=7)])
        st.metric("Events This Week", events_this_week)
    
    # Show events in a line chart
    st.subheader("Events Timeline")
    chart_data = pd.DataFrame({
        'Date': events_df['Date'],
        'Count': 1
    })
    chart_data = chart_data.set_index('Date')
    st.line_chart(chart_data)

if __name__ == "__main__":
    main()