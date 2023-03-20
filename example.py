#%%
import dash
from dash import dcc
from dash import html
import numpy as np

#%%
x = np.linspace(0, 2 * np.pi, 100)
y = 10 * 2 * np.cos(x)

app = dash.Dash()
app.layout = html.Div(children=[
 html.H1(children='Testme'),
 dcc.Graph(
 id='curve',
 figure={
 'data': [
 {'x': x, 'y': y, 'type': 'Scatter', 'name': 'Testme'},
 ],
 'layout': {
 'title': 'Test Curve'
 } } )
])

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8051)