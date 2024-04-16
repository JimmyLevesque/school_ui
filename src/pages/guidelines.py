import dash
from dash import html

dash.register_page(
    __name__,
    path='/guidelines',
    title='Guidelines'
)

layout = html.Div(
    [
        html.H1('Guidelines!'),
        
        html.Textarea('Use this app correctly')
    ]
)

