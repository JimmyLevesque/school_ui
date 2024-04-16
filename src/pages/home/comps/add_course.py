from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc
from pydantic import BaseModel
import requests

from config import settings


add_course_layout = html.Div([
    html.Button('Add Course', 
                    id='btn-add-course', 
                    n_clicks=0,
                    style={'width': '200px',
                           'margin-bottom': '10px',
                           'margin-left': '10px',}), 
    
    dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Add Course")),
                dbc.ModalBody(children=[
                    dbc.Row([
                        dbc.Col([
                            html.P('Course name :')
                        ], width=3),
                        dbc.Col([
                            dcc.Input(id='inpt-course-name')
                        ], width=3),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.P('Teacher name :')
                        ], width=3),
                        dbc.Col([
                            dcc.Input(id='inpt-teacher-name')
                        ], width=3),
                    ]),


                    dbc.Row([
                        dbc.Col([
                            html.Button('Cancel', 
                                        id='btn-add-course-cancel', 
                                        n_clicks=0,
                                        style={'width': '200px'}),
                            ], width=6),
                        dbc.Col([
                            html.Button('Submit', 
                                        id='btn-add-course-submit', 
                                        n_clicks=0,
                                        style={'width': '200px'}),
                            ], width=6),
                        
                    ]),
                    
                ]),
            ],
            id="modal-add-course",
            size="lg",
            is_open=False,
        )

])


@callback(
    Output('modal-add-course', 'is_open', allow_duplicate=True),
    [Input('btn-add-course', 'n_clicks'), Input('btn-add-course-cancel', 'n_clicks')],
    State('modal-add-course', 'is_open'),
    prevent_initial_call=True
)
def create_course_toggle_modal(n_clicks_add, n_clicks_cancel, is_open):
    if n_clicks_add==0:
        return False
    
    if n_clicks_add or n_clicks_cancel:
        return not is_open
    
    return is_open



class CourseCreate(BaseModel):
    course_name: str
    teacher: str


@callback(
    [Output('store-data-course', 'data', allow_duplicate=True),
     Output('modal-add-course', 'is_open', allow_duplicate=True)],
    Input('btn-add-course-submit', 'n_clicks'),
    [State('inpt-course-name', 'value'),
     State('inpt-teacher-name', 'value')],
    prevent_initial_call=True
)
def create_course(n_clicks, course_name, teacher_name):

    api_url = settings.API_URL

    payload = CourseCreate(course_name=course_name, teacher=teacher_name)
    
    resp = requests.post(api_url + '/course/create_course/', data=payload.model_dump_json(),  verify=False)

    return resp.json(), False


