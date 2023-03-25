@app.callback(Output('is_uploaded', 'children'),
              Output('main-table', 'data'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              prevent_initial_call=True
              )
def upload_data(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        df_id = parse_contents(list_of_contents, list_of_names, list_of_dates)
        global upload_df
        upload_df = df[df['uid'].isin(df_id)].copy()
        return f'已上傳名單: {list_of_names}', upload_df.to_dict('records')
    
# Define how to save data
@app.callback(
    Output("save_data", "children"),
    Input("btn_csv", "n_clicks"),
    State('intermediate-value', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, jsonified_cleaned_data):
    saved_df = pd.read_json(jsonified_cleaned_data, orient='split')
    today = datetime.now().strftime("%Y%m%d_%H%M%S")
    message = f'已儲存名單: {today}.csv'
    return message

