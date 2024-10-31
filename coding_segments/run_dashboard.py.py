import os
import subprocess
import sys

def ensure_streamlit():
    """Ensure streamlit is installed and run the dashboard"""
    try:
        import streamlit
        print("Streamlit is already installed")
    except ImportError:
        print("Installing streamlit...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "pandas"])
        print("Streamlit installed successfully")

def get_streamlit_path():
    """Get the path to the streamlit executable"""
    if sys.platform.startswith('win'):
        # Windows
        scripts_dir = os.path.join(sys.prefix, 'Scripts')
        streamlit_path = os.path.join(scripts_dir, 'streamlit.exe')
    else:
        # Unix-like
        scripts_dir = os.path.join(sys.prefix, 'bin')
        streamlit_path = os.path.join(scripts_dir, 'streamlit')
    return streamlit_path

def main():
    """Main function to set up and run the dashboard"""
    # Ensure streamlit is installed
    ensure_streamlit()
    
    # Create the dashboard code
    dashboard_code = """
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# [Rest of your dashboard code from previous artifact]
# Generate dummy events data
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
    sender_email = "your-email@gmail.com"  # Replace with your email
    password = "your-app-password"  # Replace with your app password
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Upcoming Events List"
    
    # Convert dataframe to HTML table
    html_table = events_df.to_html(index=False)
    body = f\"\"\"
    <html>
        <body>
            <h2>Your Upcoming Events</h2>
            {html_table}
        </body>
    </html>
    \"\"\"
    
    msg.attach(MIMEText(body, 'html'))
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
        return False

def main():
    st.title("?? Event Dashboard")
    
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
                    st.success("?? Events have been sent to your email!")
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
"""
    
    # Write the dashboard code to a file
    with open('dashboard.py', 'w') as f:
        f.write(dashboard_code)
    
    # Run the dashboard
    streamlit_path = get_streamlit_path()
    print(f"Running dashboard using Streamlit at: {streamlit_path}")
    try:
        subprocess.run([streamlit_path, "run", "dashboard.py"])
    except Exception as e:
        print(f"Error running dashboard: {e}")
        print("Trying alternative method...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])

if __name__ == "__main__":
    main()
