from dash import html, Input, Output, State, callback, dcc, ALL, ctx
import dash_bootstrap_components as dbc
from pydantic import BaseModel, EmailStr, ValidationError
import requests

from typing import Optional, List

from config import settings


# add student button ('btn-add-student') is from view_course.py

add_student_layout = html.Div([
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Add Student")),
            
        dbc.ModalBody(children=[
            dbc.Row([
                dbc.Col([
                    html.P('First name :')
                ], width=3),
                dbc.Col([
                    dcc.Input(id='inpt-student-firstname')
                ], width=3),
            ]),
            dbc.Row([
                dbc.Col([
                    html.P('Last name :')
                ], width=3),
                dbc.Col([
                    dcc.Input(id='inpt-student-lastname')
                ], width=3),
            ]),

            dbc.Button("Add Email", id="btn-add-email", n_clicks=0),

            html.Div(id='add-emails-container', children=[], className="mt-4"),

            dbc.Row([
                dbc.Col([
                    html.Button('Cancel', 
                                id='btn-add-student-cancel', 
                                n_clicks=0,
                                style={'width': '200px'}),
                    ], width=6),
                dbc.Col([
                    html.Button('Submit', 
                                id='btn-add-student-submit', 
                                n_clicks=0,
                                style={'width': '200px'}),
                    ], width=6),
            ])  
        ])
    ],
    id="modal-add-student",
    size="lg",
    is_open=False,
    ),

    dbc.Alert(children="", 
                color="danger",
                id="alert-entry-error",
                dismissable=True,
                fade=False,
                is_open=False)

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



def make_new_email_row(n_clicks):
    new_email_row = dbc.Row([
            dbc.Col([
                html.P('Email :')
            ], width=3),
            dbc.Col([
                dcc.Input(id={"type": "inpt-student-email", "index": n_clicks})
            ], width=3),
            dbc.Col([
                dbc.Button(
                        "X",
                        id={"type": "email-dynamic-delete", "index": n_clicks},
                        n_clicks=0,
                        color="secondary",
                    ),
            ], width=1)
        ])
    return new_email_row


@callback(
    Output("add-emails-container", "children"),
    Input("btn-add-email", "n_clicks"),
    Input({"type": "email-dynamic-delete", "index": ALL}, "n_clicks"),
    State("add-emails-container", "children"),
    prevent_initial_call=True
)
def add_delete_email(n_clicks, _, rows):
    if ctx.triggered_id == "btn-add-email" or not ctx.triggered_id:
        new_email_row = make_new_email_row(n_clicks)
        rows.append(new_email_row)
    else:
        # exclude the deleted chart
        delete_chart_number = ctx.triggered_id["index"]
        rows = [
            row
            for row in rows
            if "'index': " + str(delete_chart_number) not in str(row)
        ]
    return rows



class EmailCreate(BaseModel):
    email: EmailStr

class StudentCreate(BaseModel):
    course_id: int
    firstname: str
    lastname: str
    emails: Optional[List[EmailCreate]] 



@callback(
    [Output("alert-entry-error", 'is_open', allow_duplicate=True),
    Output("alert-entry-error", 'children', allow_duplicate=True),
    Output('store-data-course', 'data', allow_duplicate=True),
    Output('modal-add-student', 'is_open', allow_duplicate=True)],
    Input('btn-add-student-submit', 'n_clicks'),
    [State('store-data-course', 'data'),
     State('inpt-student-firstname', 'value'),
     State('inpt-student-lastname', 'value'),
     State({"type": "inpt-student-email", "index": ALL}, "value")],
    prevent_initial_call=True
)
def create_student(n_clicks_submit, course_data, student_fn, student_ln, emails):

    api_url = settings.API_URL

    val_errors = None
    try:
        payload = StudentCreate(course_id=course_data['id'],
                                firstname=student_fn,
                                lastname=student_ln,
                                emails=[EmailCreate(email=email) for email in emails])

    except ValidationError as e:
        val_errors=e

    if val_errors:
        toast_children = [dbc.Row([x for x in val_errors.__str__().split('\n')])]
        return True, toast_children, course_data, True


    _ = requests.post(api_url + '/student/create_student/', data=payload.model_dump_json(),  verify=False)

    resp = requests.get(api_url + '/course/get_course/' + str(course_data['id']), verify=False)

    return False, None, resp.json(), False
