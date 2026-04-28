python
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load data
data = pd.read_excel("Distribution_of_Beneficiaries_2022.xlsx")

data['Quarter'] = data['Quarter'].astype(str)  # Ensure Quarter is string

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Beneficiaries Distribution Dashboard"),

    dcc.Dropdown(
        id='type-dropdown',
        options=[
            {'label': t, 'value': t} for t in data['Type'].unique()
        ],
        placeholder="Select beneficiary type",
        multi=True
    ),

    dcc.Graph(id='beneficiaries-graph'),

    dcc.Graph(id='gender-pie-chart')
])

# Callbacks for updating graphs
@app.callback(
    [Output('beneficiaries-graph', 'figure'),
     Output('gender-pie-chart', 'figure')],
    [Input('type-dropdown', 'value')]
)
def update_graphs(selected_types):
    # Filter data based on selection
    if selected_types:
        filtered_data = data[data['Type'].isin(selected_types)]
    else:
        filtered_data = data

    # Line chart for quarterly distribution
    line_fig = px.line(
        filtered_data, 
        x='Quarter', 
        y='Count', 
        color='Type', 
        title='Beneficiaries Distribution Over Quarters'
    )

    # Pie chart for gender distribution
    gender_data = filtered_data.groupby('Gender', as_index=False).sum()
    pie_fig = px.pie(
        gender_data, 
        names='Gender', 
        values='Count', 
        title='Gender Distribution of Beneficiaries'
    )

    return line_fig, pie_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
