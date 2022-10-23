import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(layout="wide")

st.markdown('# INFLATION 📈')

# tabs
tab1, tab2 = st.tabs(['CPI', 'Import Price'])


@st.cache
def get_data():
    index = pd.read_csv("Datasets/Inflation/cpi.csv")
    index.set_index('Year', inplace=True)
    return index


@st.cache
def get_import():
    index = pd.read_csv("Datasets/Inflation/importprice.csv")
    index.set_index('Year', inplace=True)
    return index


@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')


with tab1:

    st.markdown('Range of year')
    xasix = st.slider('Year', min_value=2017, max_value=2021, value=[2017, 2021])
    st.write('Percentage Change in CPI')
    df = get_data()
    csv_cpi = convert_df(df)
    filtered_cpi = st.multiselect("Filter CPI columns", options=list(df.columns), default=list(df.columns))
    selectyear_cpi = df.loc[(xasix[0]):(xasix[1]), filtered_cpi]
    fig_cpi = px.line(selectyear_cpi)

    st.subheader('CPI')

    st.write(selectyear_cpi)
    st.download_button(
        "Download CPI CSV",
        csv_cpi,
        "cpi.csv",
        "text/csv",
        key='download-csv_cpi')

    st.subheader('Analysis')
    st.plotly_chart(fig_cpi, use_container_width=True)

    st.write(
        'From the graph shown, we can see that majority of categories have percentage increase in CPI from 2020 '
        'especially in Transport, which could be COE being the main culprit')

with tab2:

    st.markdown('Range of year')
    xasix = st.slider('Year', min_value=2017, max_value=2021, value=[2017, 2021],key="tab2")
    st.write('Percentage Change in Import Prices')
    di = get_import()
    csv_import = convert_df(di)
    filtered_import = st.multiselect("Filter Import Price columns", options=list(di.columns), default=list(di.columns))
    selectyear_import = di.loc[(xasix[0]):(xasix[1]), filtered_import]
    fig_import = px.line(selectyear_import)

    st.subheader('Import Price')
    st.write(selectyear_import)
    st.download_button(
        "Download Import Price CSV",
        csv_import,
        "import.csv",
        "text/csv",
        key='download-csv_import')

    st.subheader('Analysis')
    st.plotly_chart(fig_import, use_container_width=True)

    st.write('Again, majority have a percentage increase in import prices, ',
             'which could be due to COVID reducing the supply of workers and as a result ',
             'increasing unemployment rate which means fewer goods and services produced and thus higher prices')

