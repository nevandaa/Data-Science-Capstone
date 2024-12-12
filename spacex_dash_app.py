# Import required libraries 
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 *[{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]
                                             ],
                                             value='ALL',
                                             placeholder='Select a Launch Site here',
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, 
                                                max=10000, 
                                                step=1000,
                                                marks={0: '0', 
                                                       2000: '2000', 
                                                       4000: '4000', 
                                                       6000: '6000', 
                                                       8000: '8000', 
                                                       10000: '10000'},
                                                value=[min_payload, max_payload]
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2: Callback function for site-dropdown as input, success-pie-chart as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # If ALL sites are selected, create a pie chart of total launches by class
        fig = px.pie(spacex_df, names='Launch Site', values='class', 
                     title='Total Successful Launches by Site')
    else:
        # If a specific site is selected, filter the dataframe and create a pie chart of success vs failed launches
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', 
                     title=f'Launch Success for {entered_site}',
                     labels={0: 'Failed', 1: 'Success'})
    return fig

# TASK 4: Callback function for site-dropdown and payload-slider as inputs, success-payload-scatter-chart as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload_range):
    # Filter by payload range first
    df_filtered_payload = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]
    
    if entered_site == 'ALL':
        # If ALL sites are selected, create scatter plot for all sites
        fig = px.scatter(df_filtered_payload, 
                         x='Payload Mass (kg)', 
                         y='class', 
                         color='Booster Version Category',
                         title='Payload vs Launch Success for All Sites')
    else:
        # If a specific site is selected, filter by site and create scatter plot
        df_filtered = df_filtered_payload[df_filtered_payload['Launch Site'] == entered_site]
        fig = px.scatter(df_filtered, 
                         x='Payload Mass (kg)', 
                         y='class', 
                         color='Booster Version Category',
                         title=f'Payload vs Launch Success for {entered_site}')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()