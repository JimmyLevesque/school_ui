from dash import html, Input, Output, State, callback, dcc
import dash_bootstrap_components as dbc

from config import settings

# add student button ('btn-add-student') is from view_course.py




add_student_layout = html.Div([
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Add Student")),
            
    #     dbc.ModalBody(children=[
    #         dbc.Row([
    #             dbc.Col([
    #                 html.P('First name :')
    #             ], width=3),
    #             dbc.Col([
    #                 dcc.Input(id='ipt_student_firstname')
    #             ], width=3),
    #         ]),
    #         dbc.Row([
    #             dbc.Col([
    #                 html.P('Last name :')
    #             ], width=3),
    #             dbc.Col([
    #                 dcc.Input(id='ipt_student_lastname')
    #             ], width=3),
    #         ]),

    #         dbc.Button("Add Email", id="btn-add-email", n_clicks=0),

    #         html.Div(id='add-emails-container', children=[], className="mt-4"),

    #         dbc.Row([
    #             dbc.Col([
    #                 html.Button('Cancel', 
    #                             id='btn-add-student-cancel', 
    #                             n_clicks=0,
    #                             style={'width': '200px'}),
    #                 ], width=6),
    #             dbc.Col([
    #                 html.Button('Submit', 
    #                             id='btn-add-student-submit', 
    #                             n_clicks=0,
    #                             style={'width': '200px'}),
    #                 ], width=6),
                
    #         ]),
            
    #     ]),
    html.Button('Cancel', 
                                id='btn-add-student-cancel', 
                                n_clicks=0,
                                style={'width': '200px'}),
    ],
    id="modal-add-student",
    size="lg",
    is_open=False,
    )
])


@callback(
    Output('modal-add-student', 'is_open', allow_duplicate=True),
    [Input('btn-add-student', 'n_clicks'),  Input('btn-add-student-cancel', 'n_clicks')],
    State('modal-add-student', 'is_open'),
    prevent_initial_call=True
)
def create_student_toggle_modal(n_clicks_add, n_clicks_cancel, is_open):
    if n_clicks_add==0:
        return False
    
    if n_clicks_add or n_clicks_cancel:
        return not is_open
    
    return is_open