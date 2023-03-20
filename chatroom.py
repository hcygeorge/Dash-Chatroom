import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Dash Chat Room'),
    html.Div(children='''
        Enter a message and get a response!
    '''),
    dcc.Input(id='input', value='', type='text'),
    html.Button('Submit', id='submit'),
    html.Div(id='output')
])

@app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='submit', component_property='n_clicks')],
    [State(component_id='input', component_property='value')]
)
def update_output_div(n_clicks, input_value):
    return 'You entered: "{}"'.format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8051)
