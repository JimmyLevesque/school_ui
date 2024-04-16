import dash
from dash import html

dash.register_page(__name__, path='/401')

layout = html.Div(
    [
        html.H1('401 - Unauthorized Access'),
        html.Div(
            html.A('Return home', href='/')
        )
    ]
)