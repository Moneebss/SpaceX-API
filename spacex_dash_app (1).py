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
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                             ],
                                             value='ALL',
                                             placeholder="Select a Launch Site",
                                             searchable=True),
                                # Adding a line break for spacing
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                # Adding a paragraph with text to indicate the payload range
                                html.P("Payload range (Kg):"),

                                # TASK 3: Add a slider to select payload range
                                # This slider allows the user to filter the payload mass range
                                dcc.RangeSlider(id='payload-slider',
                                                min=min_payload, max=max_payload, step=1000,
                                                marks={int(min_payload): str(int(min_payload)),
                                                       int(max_payload): str(int(max_payload))},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                # This scatter chart will update based on the dropdown and slider inputs
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output('success-pie-chart', 'figure'),
              Input('site-dropdown', 'value'))
def update_pie_chart(selected_site):
    # Check if the selected site is "ALL"
    if selected_site == 'ALL':
        # For all sites, show the total success count as a pie chart
        fig = px.pie(spacex_df, values='class', 
                     names='Launch Site', 
                     title='Total Success Launches by Site')
    else:
        # Filter the dataframe based on the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        # Show success vs. failed counts for the specific site
        fig = px.pie(filtered_df, 
                     names='class', 
                     title=f'Total Success vs Failure for site {selected_site}')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), 
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Get the lower and upper bounds of the payload range from the slider
    low, high = payload_range
    # Filter data based on the payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                            (spacex_df['Payload Mass (kg)'] <= high)]
    
    # Check if the selected site is "ALL"
    if selected_site == 'ALL':
        # For all sites, show a scatter plot with the filtered data
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title='Payload vs. Outcome for All Sites')
    else:
        # Filter the data based on the selected site as well
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        # Generate a scatter plot for the specific site
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=f'Payload vs. Outcome for site {selected_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
