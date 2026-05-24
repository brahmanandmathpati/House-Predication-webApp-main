import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import joblib
import pandas as pd

# Load the model
model = joblib.load('forest_model.plk')

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Define dropdown options
max_bedrooms = 6
max_bathrooms = 6
max_floors = 3
index = [0]
view_options = list(range(5))
condition_options = list(range(1, 6))
grade_options = list(range(1, 14))

# Define the layout of your app
app.layout = html.Div(style={'textAlign': 'center'}, children=[
    html.Div(style={'boxShadow': '0px 0px 5px 5px rgba(0, 0, 0, 0.1)', 'padding': '20px', 'margin': 'auto', 'width': '50%'}, children=[
        html.H1('King County House price prediction'),
        html.Label('Number of Bedrooms:'),
        dcc.Dropdown(
            id='bedrooms-dropdown',
            options=[{'label': str(i), 'value': i} for i in range(1, max_bedrooms + 1)],
            value=3  # default value
        ),
        html.Br(),
        html.Label('Number of Bathrooms:'),
        dcc.Dropdown(
            id='bathrooms-dropdown',
            options=[{'label': str(i), 'value': i} for i in range(1, max_bathrooms + 1)],
            value=2  # default value
        ),
        html.Br(),
        html.Label('Square Foot of Interior:'),
        dcc.Input(
            id='sqft-interior-input',
            type='number',
            value=1500  # default value
        ),
        html.Br(),
        html.Label('Square Foot of Land:'),
        dcc.Input(
            id='sqft-land-input',
            type='number',
            value=5000  # default value
        ),
        html.Br(),
        html.Label('Number of Floors:'),
        dcc.Dropdown(
            id='floors-dropdown',
            options=[{'label': str(i), 'value': i} for i in range(1, max_floors + 1)],
            value=1  # default value
        ),
        html.Br(),
        html.Label('Overlooking Waterfront:'),
        dcc.Dropdown(
            id='waterfront-dropdown',
            options=[{'label': "Yes", 'value': 1},
                     {'label': "No", 'value': 0}]  # default value
        ),
        html.Br(),
        html.Label('View:'),
        dcc.Dropdown(
            id='view-dropdown',
            options=[{'label': str(option), 'value': option} for option in view_options],
            value=0  # default value
        ),
        html.Br(),
        html.Label('Condition (1-5):'),
        dcc.Dropdown(
            id='condition-dropdown',
            options=[{'label': str(option), 'value': option} for option in condition_options],
            value=3  # default value
        ),
        html.Br(),
        html.Label('Grade (1-13):'),
        dcc.Dropdown(
            id='grade-dropdown',
            options=[{'label': str(option), 'value': option} for option in grade_options],
            value=7  # default value
        ),
        html.Br(),
        html.Label('Latitude'),
        dcc.Input(type='number', id = 'latitude'),
        html.Br(),
        html.Label('Longitude'),
        dcc.Input(type='number', id = 'Longitude'),
        html.Br(),
        html.Button('Submit', id='submit-val', n_clicks=0),
        html.Br(),
        html.Div(id='output-prediction')
    ])
])

# Define callback to make predictions when the button is clicked
@app.callback(
    Output('output-prediction', 'children'),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('bedrooms-dropdown', 'value'),
     dash.dependencies.State('bathrooms-dropdown', 'value'),
     dash.dependencies.State('sqft-interior-input', 'value'),
     dash.dependencies.State('sqft-land-input', 'value'),
     dash.dependencies.State('floors-dropdown', 'value'),
     dash.dependencies.State('waterfront-dropdown', 'value'),
     dash.dependencies.State('view-dropdown', 'value'),
     dash.dependencies.State('condition-dropdown', 'value'),
     dash.dependencies.State('grade-dropdown', 'value'),
     dash.dependencies.State('latitude', 'value'),
     dash.dependencies.State('Longitude', 'value')]
)
def update_prediction(n_clicks, bedrooms, bathrooms, sqft_living, sqft_lot, floors, waterfront, view, condition, grade, lat, long):
    if n_clicks > 0:
        # Combine bathrooms and bedrooms
        NumberofRooms = bathrooms + bedrooms

        # Prepare the input data for prediction
        data = pd.DataFrame({
            'bedrooms': [bedrooms],
            'bathrooms': [bathrooms],
            'sqft_living': [sqft_living],
            'sqft_lot': [sqft_lot],
            'floors': [floors],
            'waterfront': [waterfront],
            'view': [view],
            'condition': [condition],
            'grade': [grade],
            'lat': [lat],
            'long': [long],
            'NumberofRooms': [NumberofRooms],
        }, index)

        # Make prediction using the model
        prediction = model.predict(data)[0]
        return f'Prediction: ${prediction:,.2f}'
    else:
        return ''


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
