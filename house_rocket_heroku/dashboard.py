import folium
import numpy as np
import pandas as pd
import streamlit as st
import geopandas
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import plotly.express as px
from datetime import datetime

st.set_page_config(layout='wide')


@st.cache(allow_output_mutation=True)
def get_data(path):
    dataframe = pd.read_csv(path)
    return dataframe


@st.cache(allow_output_mutation=True)
def get_geofile(link):
    gf = geopandas.read_file(link)
    return gf


def set_feature(data):
    if 'Unnamed: 0' in data.columns:
        data.drop(columns='Unnamed: 0', inplace=True)  # coluna criada quando fiz a limpeza de dados,
        # ela replicava o index. É necessário fazer isso só uma vez.
    data['price_m2'] = data['price'] / (data['sqft_lot'] * 0.092903)
    return data


def data_overview(data):
    st.sidebar.title('Filters for Tables')
    f_attributes = st.sidebar.multiselect('Enter columns', data.columns)
    f_zipcode = st.sidebar.multiselect('Enter zipdode', data['zipcode'].sort_values().unique())
    df = data.copy()    # salva uma cópia do df original, antes de filtrar.
    st.header('Data Overview')
    if (f_zipcode != []) & (f_attributes != []):
        data = data.loc[data['zipcode'].isin(f_zipcode), f_attributes]

    elif (f_zipcode != []) & (f_attributes == []):
        data = data.loc[data['zipcode'].isin(f_zipcode), :]

    elif (f_zipcode == []) & (f_attributes != []):
        data = data.loc[:, f_attributes]

    else:
        data = data.copy()

    st.dataframe(data)

    # definindo colunas para colocar as tabelas que estão por vir lado a lado
    c1, c2 = st.columns((1, 1))

    # average metrics
    if f_zipcode != []:
        df1 = df.loc[df['zipcode'].isin(f_zipcode)][['id', 'zipcode']].groupby('zipcode').count().reset_index()
        df2 = df.loc[df['zipcode'].isin(f_zipcode)][['price', 'zipcode']].groupby('zipcode').mean().reset_index()
        df3 = df.loc[df['zipcode'].isin(f_zipcode)][['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
        df4 = df.loc[df['zipcode'].isin(f_zipcode)][['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()
    else:
        df1 = df[['id', 'zipcode']].groupby('zipcode').count().reset_index()
        df2 = df[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
        df3 = df[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
        df4 = df[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()

    # merge
    m1 = pd.merge(df1, df2, on='zipcode', how='inner')
    m2 = pd.merge(m1, df3, on='zipcode', how='inner')
    df = pd.merge(m2, df4, on='zipcode', how='inner')

    df.columns = ['ZIP CODE', 'TOTAL HOUSES', 'MEAN PRICE', 'MEAN SQFT LIVING', 'MEAN PRICE/M2']

    c1.header('Averege Value')
    c1.dataframe(df, height=600)

    # Descriptive Statistic
    num_attributes = data.select_dtypes(include=['int64', 'float64'])
    media = pd.DataFrame(num_attributes.apply(np.mean))
    mediana = pd.DataFrame(num_attributes.apply(np.median))
    std = pd.DataFrame(num_attributes.apply(np.std))

    max_ = pd.DataFrame(num_attributes.apply(np.max))
    min_ = pd.DataFrame(num_attributes.apply(np.min))

    df1 = pd.concat([max_, min_, media, mediana, std], axis=1).reset_index()

    df1.columns = ['Attributes', 'Maximum', 'Minimum', 'Media', 'Median', 'STD']

    c2.header('Descriptive Statistic')
    c2.dataframe(df1, height=600)

    return None


def portfolio_density(data, geofile):
    st.title('Region Overview')

    c3, c4 = st.columns((1, 1))
    c3.header('Portfolio Density')

    # Base Map - Folium
    density_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()],
                             default_zoom_start=15)

    marker_cluster = MarkerCluster().add_to(density_map)
    for name, row in data.iterrows():
        folium.Marker([row['lat'], row['long']],
                      popup='Sold R${0} on: {1}. Features: {2} sqft, {3} bedrooms, {4} bathrooms, year built: {5}'.format(
                          row['price'],
                          row['date'],
                          row['sqft_living'],
                          row['bedrooms'],
                          row['bathrooms'],
                          row['yr_built'])).add_to(marker_cluster)

    with c3:
        folium_static(density_map)

    # Region Price Map
    c4.header('Price Density')

    df = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()

    df.columns = ['ZIP', 'PRICE']

    geofile = geofile[geofile['ZIP'].isin(df['ZIP'].tolist())]

    region_price_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()], default_zoom_start=15)

    region_price_map.choropleth(data=df,
                                geo_data=geofile,
                                columns=['ZIP', 'PRICE'],
                                key_on='feature.properties.ZIP',
                                fill_color='YlOrRd',
                                fill_opacity=0.7,
                                line_opacity=0.2,
                                legend_name='AVG PRICE')

    with c4:
        folium_static(region_price_map)

    return None


def commercial_distribution(data):
    # -----------------------------------------------------
    # Distribuição dos imóveis por categorias comerciais
    # -----------------------------------------------------
    st.sidebar.title('Filters for Graphics')
    st.sidebar.header('Commercial Options')
    st.title('Commercial Attributes')

    # ---------- Average Price Per Year -------------------
    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

    st.header('Average Price Per Year')
    st.sidebar.subheader('Select Year Built Range')

    # filters
    min_yr_built = int(data['yr_built'].min())
    max_yr_built = int(data['yr_built'].max())
    f_yr_built = st.sidebar.slider('Year Built', min_yr_built, max_yr_built, (min_yr_built, max_yr_built))

    # data filtering
    df = data.loc[(data['yr_built'] >= f_yr_built[0]) & (data['yr_built'] <= f_yr_built[1])]
    df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

    # plotting line graph
    fig = px.line(df, x='yr_built', y='price')
    st.plotly_chart(fig, use_container_width=True)

    # ---------- Average Price Per Day -------------------
    st.header('Average Price Per Day')
    st.sidebar.subheader('Select Day Range')

    # filters
    min_date = datetime.strptime(data['date'].min(), '%Y-%m-%d')
    max_date = datetime.strptime(data['date'].max(), '%Y-%m-%d')
    f_date = st.sidebar.slider('Date', min_date, max_date, (min_date, max_date))

    # data filtering
    data['date'] = pd.to_datetime(data['date'])
    df = data.loc[(data['date'] >= f_date[0]) & (data['date'] <= f_date[1])]
    df = df[['date', 'price']].groupby('date').mean().reset_index()

    # plotting line graph
    fig = px.line(df, x='date', y='price')
    st.plotly_chart(fig, use_container_width=True)

    # ----------------- Histogram ------------------
    st.header('Price Distribution')
    st.sidebar.subheader('Select Price Range')

    # filter
    min_price = int(data['price'].min())
    max_price = int(data['price'].max())
    f_price = st.sidebar.slider('Price Max', min_price, max_price, (min_price, max_price))

    # data filtering
    df = data.loc[(data['price'] >= f_price[0]) & (data['price'] <= f_price[1])]

    # plotting histogram
    fig = px.histogram(df, x='price', nbins=50)
    st.plotly_chart(fig, use_container_width=True)

    return None


def attributes_distribution(data):
    # ------------------------------------------------
    # Distribuição dos imóveis por categoria física
    # ------------------------------------------------
    st.sidebar.title('Attributes Options')
    st.title('House Attributes')

    # filters
    f_bedrooms = st.sidebar.selectbox('Max number of Bedrooms', data['bedrooms'].sort_values().unique(),
                                      index=(len(data['bedrooms'].unique()) - 1))

    f_bathrooms = st.sidebar.selectbox('Max number of Bathrooms', data['bathrooms'].sort_values().unique(),
                                       index=(len(data['bathrooms'].unique()) - 1))

    c1, c2 = st.columns(2)

    # House per bedrooms
    c1.header('Houses per Bedroom')
    df = data.loc[data['bedrooms'] <= f_bedrooms]
    fig = px.histogram(df, x='bedrooms', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

    # House per bathrooms
    c2.header('Houses per Bathroom')
    df = data.loc[data['bathrooms'] <= f_bathrooms]
    fig = px.histogram(df, x='bathrooms', nbins=19)
    c2.plotly_chart(fig, use_container_width=True)

    # filters

    f_floors = st.sidebar.selectbox('Max number of floors', data['floors'].sort_values().unique(),
                                    index=(len(data['floors'].unique()) - 1))

    f_waterfront = st.sidebar.checkbox('Is a waterfront house?')

    c1, c2 = st.columns(2)

    # Houses per floors
    c1.header('Houses per Floor')
    df = data[data['floors'] <= f_floors]
    fig = px.histogram(df, x='floors', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

    # Waterfront houses
    c2.header('Waterfront Houses')
    df = data[data['waterfront'] == f_waterfront]
    fig = px.histogram(df, x='waterfront', nbins=10)
    c2.plotly_chart(fig, use_container_width=True)

    return None


if __name__ == '__main__':
    st.title('Dashboard - Projeto House Rocket')
    # ETF
    # data extration
    data = get_data('kc_house_data_clean.csv')

    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
    geofile = get_geofile(url)

    # data transformation
    set_feature(data)

    data_overview(data)

    portfolio_density(data, geofile)

    commercial_distribution(data)

    attributes_distribution(data)
