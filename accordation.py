import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table, Input, Output, State

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
accordion = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    html.P("This is the content of the first section"),
                    dbc.Button("Click here"),
                ],
                title="Item 1",
            ),
            dbc.AccordionItem(
                [
                    html.P("This is the content of the second section"),
                    dbc.Button("Don't click me!", color="danger"),
                ],
                title="Item 2",
            ),
            dbc.AccordionItem(
                "This is the content of the third section",
                title="Item 3",
            ),
        ],
    )
)

app.layout = accordion
#%% Run
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8051)