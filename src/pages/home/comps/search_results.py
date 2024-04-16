from dash import html, Input, Output, State, dash_table, callback
import pandas as pd
import requests

from config import settings


COLS_SEARCH_DATA = ['course_name', 'teacher']

STYLE_DATA_CONDITIONAL = [
    {
        "if": {"state": "active"},
        "backgroundColor": "rgba(150, 180, 225, 0.2)",
        "border": "1px solid blue",
    },
    {
        "if": {"state": "selected"},
        "backgroundColor": "rgba(0, 116, 217, .03)",
        "border": "1px solid blue",
    },
]


search_results_layout = html.Div([
    html.Div([
        html.Div(id='search-table-placeholder', children=[])
        ], className='row')
])


@callback(
        Output('search-table-placeholder', 'children'),
        Input('store-data-search', 'data'),
        prevent_initial_call=True
)
def update_data_searach(data):
    df = pd.DataFrame([s for s in data])
    mytable = dash_table.DataTable(
        id='search_res_tbl',
        data=df[COLS_SEARCH_DATA].to_dict('records'), 
        columns=[{"name": i, "id": i} for i in COLS_SEARCH_DATA],
        style_data_conditional=STYLE_DATA_CONDITIONAL)

    return mytable


@callback(
    Output("search_res_tbl", "style_data_conditional"),
    Input("search_res_tbl", "active_cell")
)
def update_selected_row_color(active):
    style = STYLE_DATA_CONDITIONAL.copy()
    if active:
        style.append(
            {
                "if": {"row_index": active["row"]},
                "backgroundColor": "rgba(150, 180, 225, 0.2)",
                "border": "1px solid blue",
            },
        )
    
    return style

@callback(
    Output("store-data-course", "data", allow_duplicate=True),
    Input("search_res_tbl", "active_cell"),
    State('store-data-search', 'data'),
    prevent_initial_call=True
)
def update_data_course(active, data):

    if active is None:
        return []

    id_sel = data[active['row']]['id']
    api_url = settings.API_URL
    resp = requests.get(api_url + '/course/get_course/' + str(id_sel), verify=False)

    return resp.json()

