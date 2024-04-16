import dash
from dash import html, dcc, callback, Input, Output

from .comps.add_course import add_course_layout
from .comps.view_course import view_course_layout
from .comps.search_bar import search_bar_layout
from .comps.search_results import search_results_layout
from .comps.add_student import add_student_layout

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

        view_course_layout,

        add_student_layout,

        search_bar_layout,

        search_results_layout,

        dcc.Store(id='store-data-course', 
                  data=[], 
                  storage_type='memory'), # 'memory', 'local' or 'session'

        dcc.Store(id='store-data-search', 
                  data=[], 
                  storage_type='memory') # 'memory', 'local' or 'session'

    ]
)



