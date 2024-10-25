import dash
from dash import dcc, html, dash_table
import pandas as pd
from dash.dependencies import Input, Output

# Create a dummy dataset with 10 events and their dates
data = {
    'Event': ['Event1', 'Event2', 'Event3', 'Event4', 'Event5', 'Event6', 'Event7', 'Event8', 'Event9', 'Event10'],
    'Date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08', '2023-01-09', '2023-01-10']
}

# Create a DataFrame from the dummy dataset
df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1('Events Dashboard'),
    dash_table.DataTable(
        id='events_table',
        columns=[{'name': i, 'id': i} for i in df.columns],
        data=df.to_dict('records'),
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold',
            'fontSize': 18
        },
        style_data={
            'backgroundColor': 'white',
            'fontSize': 16
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
