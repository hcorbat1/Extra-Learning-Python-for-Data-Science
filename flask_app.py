
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
import numpy as np
import pandas as pd

# Plotly modules/methods/settings
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from plotly.offline import init_notebook_mode
init_notebook_mode(connected=True) # enables display of plotly figures in HTML/PDF notebooks

# Dash modules/methods/settings
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # Controls default visual appearance of the dashboard


gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk']
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight',
                              'educ':'education',
                              'coninc':'income',
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige',
                              'papres10':'father_job_prestige',
                              'sei10':'socioeconomic_index',
                              'fechld':'relationship',
                              'fefam':'male_breadwinner',
                              'fehire':'hire_women',
                              'fejobaff':'preference_hire_women',
                              'fepol':'men_bettersuited',
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')


overview_text = '''

Gender wage gap is a term for describing the average earning differences, usually in percentages between women and men.

The two common types of gender wage gap are non-adjusted and adjusted, but the latter one is more widely used for comparisons. The main characteristic of adjusted that differs from non-adjusted is that it is taking into account of education levels, job differences, and hours worked, etc. Therefore, adjusted wage gap would be a better choice than raw (non-adjusted) as a comparison option.

GSS stands for General Social Survey. It is a domestic and representative survey of the adults in the United States, and it has been established since 1972.

GSS is composed of the core components, such as demographic, behavioral, and attitudinal data to provide an overview of the society in terms of opinions, attitudes and behaviors.

'''

table_data = gss_clean[['sex','income','job_prestige','socioeconomic_index','education']]
summary_table = table_data.groupby('sex').agg('mean').reset_index().round(2)
summary_table.columns = ['Sex','Average Income','Occupational Prestige','Socioeconomic Index','Years of Education']
table_2 = ff.create_table(summary_table)

table_3 = gss_clean.value_counts(['sex','male_breadwinner']).reset_index()
fig_3 = px.bar(table_3,x = 'male_breadwinner',color = 'sex',y = 'count',barmode='group',
             height = 600, width= 600,
             hover_data= ['sex','male_breadwinner','count'],
             labels={'male_breadwinner': 'It is Better If the Men is the Achiever Outside the Home','sex':'Sex','count':' Count'},
             text = 'count')

fig_4 = px.scatter(gss_clean.head(500),x='job_prestige', y = 'income',color = 'sex',
                 height = 600, width= 600,
                 labels={'job_prestige':'Occupational Prestige','sex':'Sex','income':'Annual Income'},
                 trendline='ols',
                 hover_data=['education','socioeconomic_index'])

fig_5_1 = px.box(gss_clean, x= 'sex',y= 'income',color='sex',
             height = 600, width= 600,
             labels={'income':'Annual Income','sex':''})
fig_5_1.update_layout(showlegend= False)

fig_5_2 = px.box(gss_clean, x= 'sex',y= 'job_prestige',color='sex',
             height = 600, width= 600,
             labels={'job_prestige':'Occupational Prestige','sex':''})
fig_5_2.update_layout(showlegend= False)

new_df = gss_clean[['income','sex','job_prestige']]
new_df['job_cat'] = pd.cut(new_df['job_prestige'], bins = 6)
new_df= new_df.dropna()
fig_6 = px.box(new_df,x = 'sex',y= 'income',facet_col='job_cat',facet_col_wrap=2,
             height = 600, width=600,
             color = 'sex',
             labels={'income':'Annual Income','sex':''})
fig_6.for_each_annotation(lambda a: a.update(text = a.text.replace('job_cat=','')))

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
[
 html.H1("Exploring the General Social Survey"),
 dcc.Markdown(children=overview_text),
 html.H2('Descriptive Statistics'),
 dcc.Graph(figure= table_2),
 html.H3('Do you agree or disagree that only men should be the breadwinner'),
 dcc.Graph(figure = fig_3),
 html.H3('Occupational Prestige and Annual Income by Sex'),
 dcc.Graph(figure = fig_4),
 html.H2('Annual Income by Sex'),
 dcc.Graph(figure = fig_5_1),
 html.H2('Occupational Prestige by Sex'),
 dcc.Graph(figure = fig_5_2),
 html.H3('Annual Income by Sex Based on Level of Occupational Prestige'),
 dcc.Graph(figure = fig_6)

]
 )
if __name__ == '__main__':
    app.run_server(debug=True)

