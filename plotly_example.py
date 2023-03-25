#%%
import plotly.express as px
import pandas as pd

#%% Load dataset
df = pd.read_csv('./data/cdp_sample.csv', sep=',')
df = df[['uid','gender','birth','age','zip','gender_pred','is_edm_ok','is_company','last_login', 'rfm_new', 'avgprice', 'cnt_item']]
df['rfm_new'] = df['rfm_new'].fillna('未貼標')
df['avgprice'] = df['avgprice'].fillna(0)

#%%

temp = df.groupby(['rfm_new'])[['rfm_new']].count()
temp.columns = ['num']
temp.reset_index(inplace=True)

#%%
temp
#%% figures

fig = px.bar(temp, x="num", y="rfm_new", color=None, barmode=None, orientation='h')
fig
# %%
