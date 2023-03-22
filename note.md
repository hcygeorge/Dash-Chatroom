# Dash入門


## 程式碼範本

```python
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1('title'),
    html.P('text'),
    html.Button('button'),
])

if __name__ == '__main__':
    app.run_server(debug=True)
```



## Dash基本工具

### app.layout
以階層結構陳列所有元件，用於設定dashboard的版型

### dash.html
html模組提供可生成各種HTML tags的類別，並使用key:value參數設定HTML屬性如style, className和id。以下是常用html元件:

html.H1()\
設定標題

html.Div([], style={})\
html.Div元件可以用作容器，將其他Dash元件组合在一起，style可用於設定版型

html.br()\
break，代表換行

html.Table()\
```
html.Table([
    html.Tr([html.Td(['x', html.Sup(2)]), html.Td(id='square')]),
    html.Tr([html.Td(['x', html.Sup(3)]), html.Td(id='cube')]),
    html.Tr([html.Td([2, html.Sup('x')]), html.Td(id='twos')]),
    html.Tr([html.Td([3, html.Sup('x')]), html.Td(id='threes')]),
    html.Tr([html.Td(['x', html.Sup('x')]), html.Td(id='x^x')]),
])
```

### dash.dcc
dcc模組則提供可中高階控制元件(如按鈕、選單)和圖表

dcc.Graph 圖

```python
fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
dcc.Graph(id='graph_name', figure=fig)
```

dcc.Slider
滑桿
```python
dcc.Slider(
        df['year'].min(),
        df['year'].max(),
        step=None,
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        id='year-slider'
    )
```

dcc.Dropdown
下拉選單
```python
dcc.Dropdown(
    df['Indicator Name'].unique(),
    'Fertility rate, total (births per woman)',
    id='xaxis-column'
)
```

dcc.Radioitems
核取方塊
```python
dcc.RadioItems(
    ['Linear', 'Log'],
    'Linear',
    id='xaxis-type',
    inline=True
)
```



### Input, Output

### @app.callback

## 補充

設定元件以水平或垂直排列
```python
style={'display': 'flex', 'flex-direction': 'row'}
style={'display': 'flex', 'flex-direction': 'column'}
```

## 部署方案

```shell
# 安裝gunicorn
pip install gunicorn

# 啟動
nohup gunicorn -w 4 -b 0.0.0.0:$port app:server &

# 關閉
kill $(lsof -i:$port|awk '{if(NR==2)print $2}')
```