
# package imports
from dash import html, callback, Output, Input, State
import dash_bootstrap_components as dbc

# component
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.H3("Link to Plotly")), # html.Img(src=logo_encoded, height='30px')
                    ],
                    align='center',
                    className='g-0',
                ),
                href='https://plotly.com',
                style={'textDecoration': 'none'},
            ),
            dbc.NavbarToggler(id='navbar-toggler', n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.NavLink(
                                'Home',
                                href='/'
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                'Guidelines',
                                href='/guidelines'
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                'Unauthorized',
                                href='/401'
                            )
                        )
                    ]
                ),
                id='navbar-collapse',
                navbar=True
            )
        ]
    ),
    color='dark',
    dark=True
)

# add callback for toggling the collapse on small screens
@callback(
    Output('navbar-collapse', 'is_open'),
    Input('navbar-toggler', 'n_clicks'),
    State('navbar-collapse', 'is_open'),
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

