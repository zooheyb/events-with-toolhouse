import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

app = dash.Dash(__name__)

# Create dummy data
events = ['Event1', 'Event2', 'Event3', 'Event4', 'Event5', 'Event6', 'Event7', 'Event8', 'Event9', 'Event10']
dates = ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01', '2023-06-01', '2023-07-01', '2023-08-01', '2023-09-01', '2023-10-01']

# Create a DataFrame
df = pd.DataFrame({'Event': events, 'Date': dates})

# Add a dropdown menu to select the event
app.layout = html.Div([html.H1('Events Dashboard'),
                             dcc.Dropdown(id='event-dropdown',
                                          options=[{'label': i, 'value': i} for i in events],
                                          placeholder='Select an event'),
                             html.Div(id='output')])

# Define the callback function
@app.callback(
    Output('output', 'children'),
    [Input('event-dropdown', 'value')]
)
def update_output(value):
    if value is not None:
        selected_event = df.loc[df['Event'] == value]
        return f'Event: {selected_event.iloc[0, 0]} - Date: {selected_event.iloc[0, 1]}'
    else:
        return 'No event selected'

# Run the app
#if __name__ == '__main__':
 #   app.run_server(debug=True)
if __name__ == '__main__':
    app.run_server(debug=True, host='192.168.1.21', port=8080)
