from dash import Dash, html, dcc, dash_table, Input, Output, State
import plotly.express as px
import pandas as pd
import base64
from datetime import datetime
import io
import dash_bootstrap_components as dbc
from utils.data import add_commas
from dash.exceptions import PreventUpdate

#%%
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


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

def create_table(df):
    return [
        html.Header('僅列印出部分數據'),
        dash_table.DataTable(
            id='main-table',
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=10,
            style_header={'background-color':'#e7f1ff'},
            style_cell={}
            )]

def update_indicator(df):
    return add_commas(round(df['cnt_item'].mean(), 2)), \
        add_commas(round(df['avgprice'].mean(), 2)), \
        add_commas(df.shape[0])

def create_rfm_bar(df):
    new_df = df.groupby(['rfm_new'])[['rfm_new']].count()
    new_df.columns = ['num']
    new_df.reset_index(inplace=True)
    return dcc.Graph(
        id='rfm_bar',
        figure=px.bar(new_df, x="num", y="rfm_new", color=None, barmode=None, orientation='h')
    )


#%% Load dataset
df = pd.read_csv('./data/cdp_sample.csv', sep=',')
df = df[['uid','gender','birth','age','zip','gender_pred','is_edm_ok','is_company','last_login', 'rfm_new', 'avgprice', 'cnt_item']]
df['rfm_new'] = df['rfm_new'].fillna('未貼標')
df['avgprice'] = df['avgprice'].fillna(0)

#%% Style settings
header_style = {'background-color':'#313a46', 'color':'white', 'font-size':'12px', 'font-family': 'Sans-serif', 'textAlign': 'left'}
header2_style = {'display': 'inline', 'background-color':'#e7f1ff', 'color':'black', 'font-size':'20px', 'font-family': 'Sans-serif'}
filter_list_style = {'background-color':'#ffffff', 'color':'black', 'font-family': 'Sans-serif', 'textAlign': 'center'}

tab_style = {'background-color':'#ffffff', 'font-size':'14px', 'font-family': 'Sans-serif'}
div2_style = {}
# div4_style = {}
panel_style = {'textAlign': 'left', 'fontFamily': 'Sans-serif'}

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

figures = [
    ''
]


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
    dbc.CardBody([
        html.Label('會員名單數'),
        html.Hr(),
        html.H2(
            id='num-users',
            children=add_commas(df.shape[0]),
            style=panel_style),    
    ]),
    dbc.CardBody([
    html.Label('每人平均消費金額'),
    html.Hr(),
    html.H2(
        id='avgprice',
        children=add_commas(round(df['avgprice'].mean(), 2)),
        style=panel_style),
    ]),
    dbc.CardBody([
    html.Label('每人平均購買商品數'),
    html.Hr(),
    html.H2(
        id='cnt_item',
        children=add_commas(round(df['cnt_item'].mean(), 2)),
        style={'textAlign': 'left', 'fontFamily': 'Sans-serif'})
    ]),
]

button_group = dbc.ButtonGroup(
    [
        dbc.Button("上傳名單", outline=True, color="primary", id='upload_list_button', n_clicks=0),
        dbc.Button("提交名單", outline=True, color="primary", id='submit_list_button', n_clicks=0),
        dbc.Button("重置名單", outline=True, color="primary", id='reset_list_button', n_clicks=0),
    ], size="sm"
)

accordions = [
    dbc.AccordionItem(title='基本資料', children='施工中', style=tab_style),
    dbc.AccordionItem(title='使用行為', children=tab01, style=tab_style),
    dbc.AccordionItem(title='行銷指標', children=tab02, style=tab_style),
    dbc.AccordionItem(title='商品偏好', children='施工中', style=tab_style),
    ]

#%% Layout
app.layout = html.Div(children=[
    dcc.ConfirmDialog(
        id='confirm_submit_button',
        message='確定要提交名單嗎?',
        ),
    html.Div([
        html.Br(),
        dbc.Row([
            dbc.Col(html.H5(children='PChome 24h')),
            dbc.Col(html.Div(id="system_message", style={'textAlign': 'right'})),
        ], style={'background-color':'#313a46'}),
    ], style=header_style),
    dbc.Row(children=[
        dbc.Col([
            html.Br(),
            dbc.Row([
                dbc.Col(html.Header(children='標籤清單', style={'textAlign': 'left'})),
                dbc.Col(dbc.Button('篩選', id='go-filter', size="sm", outline=True, color="primary"), style={'textAlign': 'right'}),
            ]),
            html.Br(),
            dbc.Accordion(id='tabs-example-1', children=accordions, start_collapsed=True),
            html.Div(id='filters')
        ], style={'max-width': '25%', 'background-color':'#ffffff'}),
        dbc.Col(children=[
            html.Br(),
            dbc.Row([
                dbc.Col(html.Header('指標', style=header2_style)),
                dbc.Col(button_group, style={'textAlign': 'right'}),
            ]),
            html.Br(),
            html.Div(dbc.Row([dbc.Col(dbc.Card(card)) for card in panel], style={'background-color':'#e7f1ff'})),
            html.Br(),
            dbc.Card([
                dbc.CardHeader(dbc.Tabs([
                    dbc.Tab(label="會員名單", tab_id="tab-1", label_style={'color':'#000000'}),
                    dbc.Tab(label="RFM客群", tab_id="tab-2", label_style={'color':'#000000'}),
                    ],
                    id="card-tabs",
                    active_tab="tab-1"
                ), style={'background-color':'#e7f1ff'}),
                dbc.CardBody(html.P(children=html.Div(create_table(df)), id="card-body", className="card-text")),
            ]),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            ], style={'background-color':'#e7f1ff'}),
    ], style=div2_style, id='div2'),
], style={'background-color':'#e7f1ff', 'color':'black'})


#%% Callback
# RFM篩選器
@app.callback(
    Output("system_message", "children", allow_duplicate=True),
    Input('new_rfm_filter', 'value'),
    prevent_initial_call=True
    )  
def rfm(rfm_new):
    global id_series
    if 'upload_df' in globals():
        id_series = upload_df['uid'][upload_df.rfm_new.isin(rfm_new)]
    else:
        id_series = df['uid'][df.rfm_new.isin(rfm_new)]
    return '篩選RFM'

# 篩選按鈕，更新card-body
@app.callback(
    Output('num-users', 'children', allow_duplicate=True),
    Input('go-filter', 'n_clicks'),
    State("card-tabs", "active_tab"),
    prevent_initial_call=True
    )  
def filter_dashboard(n_clicks, active_tab):
    global new_df
    if 'id_series' in globals():
        global id_series
        new_df = df[df['uid'].isin(id_series)]
    else:
        new_df = df

    if active_tab == 'tab-1':
        return create_table(new_df)
    elif active_tab == 'tab-2':
        return create_rfm_bar(new_df)

# 篩選按鈕，更新indicator
@app.callback(
    Output("card-body", "children", allow_duplicate=True),
    Output('cnt_item', 'children', allow_duplicate=True),
    Output('avgprice', 'children', allow_duplicate=True),
    Output('num-users', 'children', allow_duplicate=True),
    Input('go-filter', 'n_clicks'),
    State("card-tabs", "active_tab"),
    prevent_initial_call=True
    )  
def filter_dashboard(n_clicks, active_tab):
    if 'id_series' in globals():
        global id_series
        new_df = df[df['uid'].isin(id_series)]
    else:
        new_df = df

    if active_tab == 'tab-1':
        return create_table(new_df), *update_indicator(new_df)
    elif active_tab == 'tab-2':
        return create_rfm_bar(new_df), *update_indicator(new_df)


# 上傳名單按鈕
@app.callback(
        Output("system_message", "children", allow_duplicate=True),
        Input("upload_list_button", "n_clicks"),
        prevent_initial_call=True)
def upload_data(n_clicks):
    message = f'已上傳名單'
    return message

# 提交名單按鈕
@app.callback(
        Output('confirm_submit_button', 'displayed'),
        Input("submit_list_button", "n_clicks"),
        prevent_initial_call=True
        )
def confirm_submit(n_clicks):
    return True

# 確認提交按鈕
@app.callback(
        Output("system_message", "children", allow_duplicate=True),
        Input("confirm_submit_button", "submit_n_clicks"),
        prevent_initial_call=True
        )
def submit_data(n_clicks):
    # saved_df = pd.read_json(df, orient='split')
    today = datetime.now().strftime("%Y%m%d_%H%M")
    message = f'已提交名單，單號: {today}'
    return message

# 重置名單按鈕
@app.callback(
        Output("system_message", "children", allow_duplicate=True),
        Input("reset_list_button", "n_clicks"),
        prevent_initial_call=True
        )
def reset_data(n_clicks):
    message = f'已重置名單'
    return message

# 切換頁簽
@app.callback(
    Output("card-body", "children", allow_duplicate=True),
    [Input("card-tabs", "active_tab")],
    prevent_initial_call=True
)
def tab_content(active_tab):
    if 'id_series' in globals():
        global id_series
        new_df = df[df['uid'].isin(id_series)]
    else:
        new_df = df

    if active_tab == 'tab-1':
        return html.Div(create_table(new_df))
    elif active_tab == 'tab-2':
        return create_rfm_bar(new_df)

#%% Run
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8051)
