import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table, Input, Output, State


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
collapse = html.Div(
    [
        dbc.Button(
            "Open collapse",
            id="collapse-button",
            className="mb-3",
            color="primary",
            n_clicks=0,
        ),
        dbc.Collapse(
            dbc.Card(dbc.CardBody("This content is hidden in the collapse")),
            id="collapse",
            is_open=True,
        ),
    ]
)

app.layout = html.Div(collapse)


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
#%% Run
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8051)