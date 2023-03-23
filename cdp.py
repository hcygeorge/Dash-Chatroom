from dash import Dash, html, dcc, dash_table, Input, Output, State
import dash_auth
import plotly.express as px
import pandas as pd
import base64
from datetime import datetime
import io

#%% Auth
VALID_USERNAME_PASSWORD_PAIRS = {
    'data': '1234'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
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

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df_id = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df_id = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df_id['uid'].tolist()

#%% Load dataset
df = pd.read_csv('./data/cdp_sample.csv', sep=',')
df = df[['uid','gender','birth','age','zip','gender_pred','is_edm_ok','is_company','last_login', 'rfm_new', 'avgprice', 'cnt_item']]
df['rfm_new'] = df['rfm_new'].fillna('未貼標')
df['avgprice'] = df['avgprice'].fillna(0)

#%% Style settings
header_style = {'background-color':'#ffffff', 'color':'black', 'font-size':'20px', 'font-family': 'Sans-serif', 'textAlign': 'center'}
header2_style = {'display': 'inline', 'background-color':'#e8eefc', 'color':'black', 'font-size':'28px', 'font-family': 'Sans-serif'}
tab_style = {'height': '8vh', 'background-color':'#e8eefc', 'font-size':'14px', 'font-family': 'Sans-serif'}
tab_selected_style = {'height': '8vh', 'background-color':'#ffffff', 'font-size':'14px', 'font-family': 'Sans-serif'}


div2_style = {'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between'}
div4_style = {'display': 'inline-block', 'min-width': '71%', 'max-width': '71%'}
main_table_style = {'background-color':'#ffffff', 'font-family': 'Sans-serif'}
panel_style = {'display': 'flex', 'flex-direction': 'row', 'background-color':'#ffffff', 'font-family': 'Sans-serif', 'justify-content': 'space-between'}

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
        style_header={'background-color':'#f3f4f8'},
        style_cell={}
        )]


tab02 = [
    html.Br(),
    html.Label('RFM'),
    dcc.Dropdown(
        id='new_rfm_filter',
        options=df['rfm_new'].unique(),
        value=df['rfm_new'].unique(),
        multi=True,
        optionHeight=25),
]

panel = [
    html.Label('會員名單數'),
    html.H2(
        id='num-users',
        children=str(df.shape[0]),
        style={'textAlign': 'left', 'fontFamily': 'Sans-serif'}),
    html.Label('每人平均消費金額'),
    html.H2(
        id='avgprice',
        children=str(round(df['avgprice'].mean())),
        style={'textAlign': 'left', 'fontFamily': 'Sans-serif'}),
    html.Label('每人平均購買商品數'),
    html.H2(
        id='cnt_item',
        children=str(round(df['cnt_item'].mean())),
        style={'textAlign': 'left', 'fontFamily': 'Sans-serif'})
    ]

save_data = [
    html.Button("儲存名單", id="btn_csv"),
    html.A(children='', id='save_data'),
]

upload_data = dcc.Upload(
        id='upload-data',
        children=html.Div([
            html.Button('上傳名單'),
            html.A('', id='is_uploaded'),
        ]))

#%% Layout
app.layout = html.Div(children=[
    html.Div(children=[
        html.Div([
            html.Br(),
            html.Header(children='PChome24h', style=header_style),
            html.Br(),
            dcc.Tabs(id='tabs-example-1', value='tab-1', children=[
                dcc.Tab(label='基本資料', children='施工中', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='使用行為', children=tab01, style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='行銷指標', children=tab02, style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='商品偏好', children='施工中', style=tab_style, selected_style=tab_selected_style),
            ]),
            html.Div(id='filters')
        ], style={'min-width': '27%', 'max-width': '27%', 'background-color':'#ffffff'}),
        html.Div(children=[
            html.Br(),
            html.Div([
                html.Header(children='Dashboard', style=header2_style),
            ]),
            html.Br(),
            html.Div(panel, style=panel_style),
            html.Br(),
            html.Div(main_table),
            html.Br(),
            html.Div([upload_data, *save_data], style={'textAlign': 'left'}),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br()
            ], style=div4_style),
    ], style=div2_style, id='div2'),
    dcc.Store(id='intermediate-value'),
], style={'background-color':'#e8eefc', 'color':'black'})


#%% Callback
# Update dashboard
@app.callback(
    Output('cnt_item', 'children', allow_duplicate=True),
    Output('avgprice', 'children', allow_duplicate=True),
    Output('num-users', 'children', allow_duplicate=True),
    Output('main-table', 'data', allow_duplicate=True),
    Output('intermediate-value', 'data', allow_duplicate=True),
    Input('new_rfm_filter', 'value'),
    Input('last-login-slider', 'value'),
    prevent_initial_call=True
    )
    
def update_table(rfm_new, last_login):
    if 'upload_df' in globals():
        filtered_df = upload_df[upload_df.rfm_new.isin(rfm_new)][upload_df.last_login <= int(last_login)]
    else:
        filtered_df = df[df.rfm_new.isin(rfm_new)][df.last_login <= int(last_login)]

    return str(round(filtered_df['cnt_item'].mean())), str(round(filtered_df['avgprice'].mean())), str(filtered_df.shape[0]), filtered_df.to_dict('records'), filtered_df.to_json(date_format='iso', orient='split')

# Define how to save data
@app.callback(
    Output("save_data", "children"),
    Input("btn_csv", "n_clicks"),
    State('intermediate-value', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, jsonified_cleaned_data):
    try:
        jsonified_cleaned_data
    except:
        return '名單沒有經過篩選，無法儲存'
    saved_df = pd.read_json(jsonified_cleaned_data, orient='split')
    today = datetime.now().strftime("%Y%m%d_%H%M%S")
    message = f'已儲存名單: {today}.csv'
    return message

@app.callback(Output('is_uploaded', 'children'),
              Output('main-table', 'data'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              prevent_initial_call=True
              )
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        df_id = parse_contents(list_of_contents, list_of_names, list_of_dates)
        global upload_df
        upload_df = df[df['uid'].isin(df_id)].copy()
        return f'已上傳名單: {list_of_names}', upload_df.to_dict('records')

#%% Run
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8051)
