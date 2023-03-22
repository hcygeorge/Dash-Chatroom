from dash import Dash, html, dcc, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

#%% Functions

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

#%%
df = pd.read_csv('./data/cdp_sample.csv', sep=',')
df = df[['uid','gender','birth','age','zip','gender_pred','is_edm_ok','is_company','last_login', 'rfm_new']]
df['rfm_new'] = df['rfm_new'].fillna('未貼標')
#%% Figures


#%% Sub layouts
tab01 = [
    html.Label('最近登入時間'),
    dcc.Slider(
        10,
        df['last_login'].max(),
        step=None,
        value=df['last_login'].max(),
        marks={str(day): str(day) for day in range(10, df['last_login'].max()+1, 10)},
        id='last-login-slider'
        )
]

main_table = [
    html.Label('會員名單'),
    dash_table.DataTable(
        id='main-table',
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=10,
    )]


tab02 = [
    html.Br(),
    html.Label('RFM'),
    dcc.Dropdown(
        id='new_rfm_filter',
        options=df['rfm_new'].unique(),
        value=df['rfm_new'].unique(),
        multi=True),
]

panel = [
    html.Label('會員名單數'),
    html.H2(id='num-users', children=str(df.shape[0]))
            ]

save_data = [
    html.Button("Download CSV", id="btn_csv"),
    dcc.Download(id="download-dataframe-csv")
]
#%% Layout
app.layout = html.Div(children=[
    html.H1(children='PChome24h 會員名單系統'),
    html.Div(children=[
        html.Div([
            dcc.Tabs(id='tabs-example-1', value='tab-1', children=[
                dcc.Tab(label='Tab one', children=tab01),
                dcc.Tab(label='Tab two', children=tab02),
            ]),
            html.Div(id='filters')
        ]
            , style={'min-width': '30%', 'max-width': '30%'}),
        html.Div(panel + main_table + save_data, style={'display': 'inline-block', 'min-width': '70%', 'max-width': '70%'}),
    ], style={'display': 'flex', 'flex-direction': 'row'}),
    dcc.Store(id='intermediate-value')

])


#%% Callback
# Update dashboard
@app.callback(
    Output('num-users', 'children'),
    Output('main-table', 'data'),
    Output('intermediate-value', 'data'),
    Input('new_rfm_filter', 'value'),
    Input('last-login-slider', 'value'))
def update_table(rfm_new, last_login):
    filtered_df = df[df.rfm_new.isin(rfm_new)][df.last_login <= int(last_login)]

    return str(filtered_df.shape[0]), filtered_df.to_dict('records'), filtered_df.to_json(date_format='iso', orient='split')

# Define how to export date
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    State('intermediate-value', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, jsonified_cleaned_data):
    dff = pd.read_json(jsonified_cleaned_data, orient='split')
    return dcc.send_data_frame(dff.to_csv, "my_list.csv")

#%% Run
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8051)
