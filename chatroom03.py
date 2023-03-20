import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2('Dash Chat Room', className='text-center'),
                html.P('Enter a message and get a response!', className='text-center'),
                html.Div(id='chat-container', className='chat-container', style={'overflow-y': 'scroll'}),
                dcc.Input(id='chat-count', value=0, type='hidden')
            ], className='card-body')
        ], width={'size': 6, 'offset': 3})
    ]),
    html.Div([
        dcc.Input(id='input', type='text', placeholder='Type a message...', className='form-control'),
        html.Button('Send', id='submit', className='btn btn-primary ml-2'),
        html.Button('Reset', id='reset', className='btn btn-danger ml-2')
    ], style={'position': 'fixed', 'bottom': 0, 'width': '50%', 'display': 'flex', 'align-items': 'center', 'padding': '10px'})
], className='card my-5')


@app.callback(
    Output('chat-container', 'children'),
    [Input('submit', 'n_clicks')],
    [State('input', 'value'), State('chat-count', 'value')]
)
def update_chat(n_clicks, input_value, count):
    if n_clicks is None:
        return []
    else:
        count = int(count)
        count += 1
        new_chat = html.Div([
            html.Div([
                html.Div([
                    html.P(input_value, className='mb-0')
                ], className='flex-grow-1'),
            ], className='d-flex flex-column'),
            html.Hr(className='my-1')
        ], id=f'chat-{count}')

        children = [new_chat]
        children.extend([html.Div(id=f'chat-{i}') for i in range(1, count)])
        return children


@app.callback(
    Output('chat-count', 'value'),
    [Input('reset', 'n_clicks')]
)
def reset_chat(n_clicks):
    if n_clicks is None:
        return dash.no_update
    else:
        return 0


if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8051)