#%%
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#%%
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2('Dash Chat Room', className='text-center'),
                html.P('Enter a message and get a response!', className='text-center'),
                html.Div(id='output', className='chat-container'),
                dcc.Input(id='input', type='text', placeholder='Type a message...',
                          className='form-control'),
                html.Button('Send', id='submit', className='btn btn-primary')
            ], className='card-body')
        ], width={'size': 6, 'offset': 3})
    ])
], className='card my-5')

#%%
app.css.append_css({
    'external_url': 'https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css'
})

@app.callback(Output('output', 'children'),
              [Input('submit', 'n_clicks')],
              [State('input', 'value')])
def update_output(n_clicks, value):
    if value is not None:
        return html.Div([
            dbc.Row([
                dbc.Col([
                    html.P(value, className='bg-primary text-white rounded p-2 mb-2 ml-2',
                           style={'max-width': '70%', 'float': 'left'})
                ], width=6, align='start'),
                dbc.Col([
                    html.P('Hi there!', className='bg-success text-white rounded p-2 mb-2 mr-2',
                           style={'max-width': '70%', 'float': 'right'})
                ], width=6, align='end')
            ])
        ])
    else:
        return ''
    
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8051)