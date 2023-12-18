# -*- coding: utf-8 -*-

"""
Created on Fri Mar  8 21:31:53 2019
@author: Frederic
"""

# pip install geopy 
# pip install Nominatim
# import requests
# import lxml.html as lh
import pandas as pd
import numpy as np
import datetime as dt
# import urllib.request
# from bs4 import BeautifulSoup
import os
# from  geopy.geocoders import Nominatim
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import plotly.graph_objects as go
import altair as alt
import streamlit as st

# os.chdir('E:\Workarea\Python\Webcrawling')

date = "21/02/2021"

# df_data = pd.read_excel('Terrain Cessy.xlsx', sheet_name='PdG').iloc[:46,:]
df_data = pd.read_excel('Terrain Cessy.xlsx', sheet_name='PdG', engine='openpyxl').iloc[:46,:]
# wb = load_workbook('Terrain Cessy.xlsx')
# ws = wb['PdG']
# df_data = pd.DataFrame(ws.values).iloc[:46,:]
# # Find Lon / Lat of cities
# lon = []
# lat = []
# location = []
# geolocator = Nominatim(user_agent="Fred")
# for i in range(len(df_data)):
#     address = df_data.loc[i,'City']
#     location = geolocator.geocode(address)
#     # print(location.address)
#     # print(location.latitude, location.longitude)
#     lon.append(location.longitude)
#     lat.append(location.latitude)

# df_data['longitude'] = lon
# df_data['latitude'] = lat
# df_data.to_pickle('df_data')

def color_survived(val):
    color = 'red' if val == 'ID' else 'lightgreen'
    return f'background-color: {color}'

def build_aggrid(df, grid_height, title, boo_editable, boo_style, row_Height): # Build Ag-Grid tables !!

    # st.header(title)

    grid_width = '100%'
    
    return_mode_value = DataReturnMode.__members__['FILTERED'] # or 'AS_INPUT' or 'FILTERED_AND_SORTED'
    update_mode_value = GridUpdateMode.__members__['VALUE_CHANGED'] # or 'MODEL_CHANGED' or 'MANUAL' or 'SELECTION_CHANGED' or 'FILTERING_CHANGED' or 'SORTING_CHANGED'
    
    #Infer basic colDefs from dataframe types
    gb = GridOptionsBuilder.from_dataframe(df)
    
    #customize gridOptions
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=boo_editable)
    gb.configure_selection('single') # or 'multiple'
    gb.configure_grid_options(domLayout='normal', rowHeight=row_Height)

    cellstyle_jscode = JsCode("""
    function(params) {
    if (params.value == '11') {
        return {
        'color': 'white',
        'backgroundColor': 'darkred'
               }
    } 
    else {
        return {
        'color': 'black',
        'backgroundColor': 'white'
        }
    }
    };
    """)

    if boo_style:
        gb.configure_column("ID", cellStyle=cellstyle_jscode)

    gridOptions = gb.build()
    
    #Display the grid
    grid_response = AgGrid(
        df, 
        gridOptions=gridOptions,
        height=grid_height, 
        width=grid_width, # '100%',
        data_return_mode=return_mode_value, 
        update_mode=update_mode_value,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
        enable_enterprise_modules=False,
        )
    
    df_output = grid_response['data']
    
    return df_output

st.set_page_config(page_title="Real Estate in Pays de Gex",layout="wide")
st.header('Real Estate Analytics')
# st.header(dt.datetime.now())
st.markdown(date)
st.markdown(
    """<a style='display: block; text-align: center;' href="https://www.leboncoin.fr/recherche?category=9&locations=Cessy_01170__46.31905_6.07205_2916_10000&real_estate_type=3">leboncoin.fr</a>
    """,
    unsafe_allow_html=True,
)
st.info("### Terrains dans le Pays de Gex")

# df_data = pd.read_pickle('df_data')
df_data.index = [""] * len(df_data) # hide index
df_data['PriceM2'] = np.round(df_data['PriceM2'],1)
# st.dataframe(df_data.iloc[:,:6],height=1000)
# st.dataframe(data=df_data.iloc[:,:6].style.applymap(color_survived, subset=['ID']), height=2000)
# st.table(df_data.iloc[:,:6])
build_aggrid(df_data.iloc[:,:7], 1700, "", False, True, 35)
st.write('')
st.write('')

st.success("### Prix au m²")
# st.bar_chart(pd.DataFrame(index=range(1,len(df_data)+1),data=df_data['PriceM2'].values, columns=["Price / m²"]),)
colors = ['lightslategray',] * len(df_data)
colors[10] = 'crimson'
fig = go.Figure(data=[go.Bar(
    x=list(range(1,len(df_data)+1)),
    y=df_data['PriceM2'].values,
    text=df_data['PriceM2'].values,
    marker_color=colors # marker color can be a single color value or an iterable
)])
st.plotly_chart(fig, use_container_width=True)
st.write('')
st.write('')
# Stacked bar chart grouped by cities
st.write('Cumulatif par commune')
st.bar_chart(pd.DataFrame(index=df_data['City'],data=df_data['PriceM2'].values, columns=["Price / m²"]),)
st.write('')
st.write('')

# Groupby chart
st.write('Moyenne par commune')
st.bar_chart(pd.DataFrame(index=range(1,len(df_data)+1),data=df_data[['PriceM2','City']].values, columns=["Price / m²","City"]).groupby(['City']).sum() / pd.DataFrame(index=range(1,len(df_data)+1),data=df_data[['PriceM2','City']].values, columns=["Price / m²","City"]).groupby(['City']).count().sort_values(by='Price / m²',ascending=False))
# temp = pd.DataFrame(index=range(1,len(df_data)+1),data=df_data[['PriceM2','City']].values, columns=["Price / m²","City"]).groupby(['City']).sum() / pd.DataFrame(index=range(1,len(df_data)+1),data=df_data[['PriceM2','City']].values, columns=["Price / m²","City"]).groupby(['City']).count().sort_values(by='Price / m²',ascending=False)
# temp['City'] = temp.index
# st.write(alt.Chart(temp).mark_bar().encode(
#     x=alt.X('City', sort=alt.EncodingSortField(field='City',
#                                           order='ascending')),
#     # x = 'City',
#     y=alt.Y('Price / m²', sort=alt.EncodingSortField(field='Price / m²',
#                                          order='descending')),    
#     # y='Price / m²',
# ))

# Display represented countries on local map
st.info("### Localisation")
st.write('')
st.write('')
st.write('')
# Get longitude and latitude of countries
lon = df_data['longitude']
lat = df_data['latitude']
df_map_data = pd.DataFrame({'lat': lat, 'lon': lon})
st.map(df_map_data, zoom=11, use_container_width=True, )
st.write('')


