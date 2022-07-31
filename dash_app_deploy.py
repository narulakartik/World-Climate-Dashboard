#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 08:19:52 2022

@author: kartiknarula
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 06:25:39 2022

@author: kartiknarula
"""

#import psycopg2
import pandas as pd
#from sqlalchemy import create_engine
import plotly.graph_objects as go

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
#from time import time

#connection=psycopg2.connect(database='ClimateWatch')

#cursor=connection.cursor()
#connection.autocommit=True

#Engine   = create_engine('postgresql://kartiknarula@localhost:5432/ClimateWatch')
#Connection    = Engine.connect()


#cursor.execute("""SELECT table_name FROM information_schema.tables
 #      WHERE table_schema = 'public'""")
#for table in cursor.fetchall():
  #  print(table)

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#data
######################




    
#dataFrame = pd.read_sql("select * from adaptation", Connection);
#dataFrame=pd.read_csv('/Users/kartiknarula/Downloads/ClimateWatch_AllData/ClimateWatch_Adaptation/CW_adaptation.csv')

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

#app



app = Dash(__name__, external_stylesheets= ['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server


#fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")



#app.layout = html.div([html.Div(style={'backgroundColor': colors['background']}, children=[
 #   html.H1(
  #      children='World Climate Dashboard',
   #     style={
    #        'textAlign': 'center',
     #       'color': colors['text']
   #     }
   # )]),
   
m={1995:'95', 1996:'96', 1997:'97', 1998:'98', 1999:'99', 2000:'00', 2001:'01',
       2002:'02', 2003:'03', 2004:'04', 2005:'05', 2006:'06', 2007:'07', 2008:'08', 2009:'09', 2010:'10', 2011:'11', 2012:'12', 2013:'13',
       2014:'14', 2015:'15', 2016:'16', 2017:'17', 2018:'18', 2019:'19'}
app.layout=html.Div([
    html.H1('World Climate Dashboard'),
    html.Div([html.H2('Select Year'),dcc.Slider(1995, 2019, step=1, value=1995, marks=m, id='year_slider')], style={'width': '49%', 'display': 'inline-block'}),
    html.Div([html.H3('Select Sector'), dcc.Dropdown(['Transportation ' , 'Energy ', 'Agriculture ', 'Industrial Processes ', 'Waste ', 'Electricity/Heat ', 'Bunker Fuels ', 'Building', 'Manufacturing/Construction ', 'Land-Use Change and Forestry ', 'Other Fuel Combustion ', 'Fugitive Emissions ' ], 'Transportation ', id='demo-dropdown')], style={'width': '49%', 'display': 'inline-block'}),
    html.Div(dcc.Graph( id='chloropleth'),style={'display': 'inline-block', 'width': '49%'}),
    html.Div(dcc.Graph( id='vulnerability'),style={'display': 'inline-block', 'width': '49%'} ),
    html.Div(dcc.Graph( id='sector_wise'), style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    html.Div(dcc.Graph( id='line'), style={'width': '49%', 'float': 'left', 'display': 'inline-block'})
    ]
)



@app.callback(
    Output('chloropleth', 'figure'),
    Output('vulnerability', 'figure'),
    Output('sector_wise', 'figure'),
    Output('line', 'figure'),
    Input('year_slider', 'value'), 
    Input('demo-dropdown', 'value'),
    Input('vulnerability', 'hoverData'),
    Input('chloropleth', 'hoverData'),
    )
def update(slide, drop, hover, cover):
    a=str(slide)

    #cait_1 = pd.read_sql('''select * from "Historical_Emissions_CAIT" where ("Gas"= 'All GHG' ) ''' , Connection)
    cait_1=pd.read_csv('CW_HistoricalEmissions_CAIT.csv')
    cait_1=cait_1[cait_1['Gas']=='All GHG']
    cait_1=cait_1[cait_1['Country']!='WORLD']
    f=cait_1[cait_1['Sector']==drop]
    fig=go.Figure(data=go.Choropleth(
    locations = f['Country'],
    z = f[a],
    text = f['Country'],
    colorscale = 'Reds',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    
  #  colorbar_tickprefix = 'MtCO2 Eq.',
    colorbar_title = 'Emissions (MtCO2 Eq)'
))
    print(cover)  
   # v=pd.read_sql('''select * from "vulnerability"''', Connection)
    v=pd.read_csv('vulnerability.csv')
    r=pd.read_csv('readiness.csv')
  #  r=pd.read_sql('''select * from "readiness"''', Connection)
  #  fig = px.choropleth(f, locations="Country",
    k=r.merge(v, on='Name')
    gig=px.scatter(k,y=a+'_y', x=a+'_x',  labels={a+'_x':'Readiness', a+'_y':'Vulnerability'}, hover_name='Name', custom_data=['ISO3_x'])
    gig.add_hline(y = r[a].mean())
    gig.add_vline(x = v[a].mean())
   # cf=cf=f[f['Country']=='AFG']
   # t1,t2=0,0
   # print(cover)
  #  p='NOR'
  #  if (hover is None) & (cover is None):
  #     p='NOR'
  #  elif (hover is None) & (cover is not None):
  #     p=cover['points'][0]['text']
  #  elif (hover is not None) & (cover is  None):
  #     p=hover['points'][0]['customdata'][0]
    
       
    if hover is None:
         p='NOR'
    else:
         p=hover['points'][0]['customdata'][0]
    cf=f[f['Country']==p]
   # print(hover)
    n=str(r[r['ISO3']==p]['Name']).split(' ')[4].split('\n')[0]
   # n=r[r['ISO3']==p]['Name'][0]
    ct=cf.transpose()
    ct=ct.drop(['Country', 'Source', 'Sector', 'Gas'])
    ct.columns=['E']
   # hig=px.line(ct, labels={'index':'Year', 'value': drop+'Emissions (MtCO2 Eq)'}, hover_name='value',markers=True, title=drop+ ' emissions for '+n+' by year')
   # hig.update_layout(showlegend=False)
    
    layout = go.Layout(
    title=drop+' emissions for '+n+' by year',
    xaxis=dict(
        title="Year"
    ),
    yaxis=dict(
        title=drop+'Emissions (MtCO2 Eq)'
    ) )
    
    hig = go.Figure(go.Scatter(  
    x = ct.index,
    y = ct.E,
    hovertemplate =
    '%{y:.2f}',
    text = ct.E,
    showlegend = False, 
      hoverlabel = dict(namelength=0)),layout=layout )
   # hig.update_layout(title=drop+' emissions for '+n+' by year')
    
    
   # country_1    = pd.read_sql('''select "Country", "Sector", "2010" from "Historical_Emissions_CAIT" where ("Gas"= 
    tree=(cait_1[cait_1['Country']==p]).reset_index()
    tree=tree.drop([0,1])
    jig=px.treemap(tree,path=['Sector'], title='Emission breakdown by sector for '+n+' ('+a+')'+' (MtCO2 Eq)', hover_name=a, values=a)
    jig.update_traces(textinfo="label+text+value")  
    jig.layout.hovermode = False
   
  
   #                 color=a, # lifeExp is a column of gapminder
   #                 hover_name='Country', # column to add to hover information
       #             color_continuous_scale='Reds')
    return fig, gig, hig, jig
    

if __name__ == '__main__':
    app.run_server(debug=True)