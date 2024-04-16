import dash
from dash import html, dcc, callback, Input, Output, State

from .comps.add_course import add_course_layout


dash.register_page(
    __name__,
    path='/',
    redirect_from=['/home'],
    title='Home'
)

layout = html.Div(
    [
        html.H1('This is home'),

        add_course_layout,

        dcc.Store(id='store-data-course', 
                  data=[], 
                  storage_type='memory'), # 'memory', 'local' or 'session'

        html.P(children="random Initial text", id='temp-text')
    ]
)


@callback(
    Output('temp-text', 'children'),
    Input('store-data-course', 'data'),
    prevent_initial_call=True
)
def temp_txt_fct(data):
    print(data)
    return 'data has been updated'