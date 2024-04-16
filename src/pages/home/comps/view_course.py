from dash import callback, html, Input, Output
import dash_bootstrap_components as dbc
from pydantic import BaseModel, EmailStr

from typing import Optional, List


view_course_layout = html.Div([
    html.Div(id='course-view-placeholder', children=[])
])


class Email(BaseModel):
    id: int
    email: EmailStr

class Student(BaseModel):
    id: int
    firstname: str
    lastname: str
    emails: Optional[List[Email]]

class Course(BaseModel):
    id: int
    course_name: str
    teacher: str
    students: Optional[List[Student]]


def get_student_card(student: Student):
    emails_group_items = []

    for idx, email_schema in enumerate(student.emails):
        emails_group_items.append(dbc.ListGroupItem(f"Email {str(idx + 1)}: {email_schema.email}"))

    card = dbc.Card([
        dbc.CardHeader(f"{student.firstname} {student.lastname}"),
        dbc.ListGroup(emails_group_items, flush=True)
        ])

    return card

def get_course_card(course: Course):
    students_cards = []

    for student in course.students:
        students_cards.append(get_student_card(student))
        students_cards.append(html.Br())

    card = dbc.Card([
        dbc.CardBody([
            html.H4(f"Course Name: {course.course_name}", className="card-title"),
            html.P(f"This course is teached by {course.teacher}", className="card-text"),
            ]),
        html.Br(),
        html.P("Registered Students:",
                 style={'padding-left':'0.5em',
                        'padding-right':'0.5em'}),
        html.Div(children=students_cards,
                 style={'padding-left':'0.5em',
                        'padding-right':'0.5em'}),
        html.Br(),
        html.Button('Add Student', 
                    id='btn-add-student', 
                    n_clicks=0,
                    style={'width': '200px',
                           'margin-bottom': '10px',
                           'margin-left': '10px',})
        ])
    
    return [card]


@callback(
    Output('course-view-placeholder', 'children'),
    Input("store-data-course", 'data'),  # store-data-course not defined in this page
    prevent_initial_call=True
)
def update_view_course(data):

    if data == []:
        return []
    
    course = Course(**data)
    
    return get_course_card(course)

