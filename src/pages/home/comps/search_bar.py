from dash import html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import requests

from config import settings


search_bar_layout = html.Div([
    html.H3('Search'),

    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Textarea('Search text (not considered)', 
                                id='search-text',
                            style={'margin-top': '10px',
                                    'margin-bottom': '10px',
                                    'margin-left': '10px'})
                ], width=4),
            dbc.Col([
                html.Button('Search All', 
                            id='search-btn-click', 
                            n_clicks=0,
                            style={'width': '200px',
                                    'margin-top': '10px',
                                    'margin-bottom': '10px',
                                    'margin-left': '10px'})
                ], width=3),
                ])
        ], fluid=True, style={"border":"1px black solid"}),
        
])

@callback(
    Output('store-data-search', 'data'),
    Input('search-btn-click', 'n_clicks'),
    prevent_initial_call=True
)
def store_data(n_clicks):
    print('clicked search')
    
    api_url = settings.API_URL

    resp = requests.get(api_url + '/course/get_all_courses/', verify=False)

    return resp.json()


