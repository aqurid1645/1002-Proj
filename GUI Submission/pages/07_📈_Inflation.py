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
    df_raw = pd.read_csv('Datasets/Inflation/cpi_full.csv')
    st.markdown('Range of year')
    xasix = st.slider('Year', min_value=2017, max_value=2021, value=[2017, 2021])
    st.write('Percentage Change in CPI')
    df = get_data()
    csv_cpi = convert_df(df)
    filtered_cpi = st.multiselect("Filter CPI columns", options=list(df.columns), default=list(df.columns))
    selectyear_cpi = df.loc[(xasix[0]):(xasix[1]), filtered_cpi]

    st.subheader('CPI')
    st.dataframe(selectyear_cpi, use_container_width=True)

    # Download box
    option = st.selectbox("Raw or Custom",
                          ("Raw", "Custom"), key='1')
    if option == "Custom":
        st.download_button(
            label="Download Customised Columns Data",
            data=selectyear_cpi.to_csv(), file_name="cpi_custom.csv")
    else:
        st.download_button(label="Download Raw Data",
                           data=df_raw.to_csv(), file_name="cpi.csv")

    st.subheader('Analysis')

    fig_cpi = px.line(selectyear_cpi)
    fig_cpi.update_layout(
        xaxis=dict(dtick=1)
    )
    st.plotly_chart(fig_cpi)

    st.write(
        'From the graph shown, we can see that majority of categories have percentage increase in CPI from 2020 '
        'especially in Transport, which could be COE being the main culprit')

with tab2:

    di_raw = pd.read_csv('Datasets/Inflation/importprice_full.csv')
    st.markdown('Range of year')
    xasix = st.slider('Year', min_value=2017, max_value=2021, value=[2017, 2021],key="tab2")
    di = get_import()
    csv_import = convert_df(di)
    filtered_import = st.multiselect("Filter Import Price columns", options=list(di.columns), default=list(di.columns))
    selectyear_import = di.loc[(xasix[0]):(xasix[1]), filtered_import]

    st.subheader('Import Price')
    st.dataframe(selectyear_import, use_container_width=True)

    # Download box
    option = st.selectbox("Raw or Custom",
                          ("Raw", "Custom"), key='2')
    if option == "Custom":
        st.download_button(
            label="Download Customised Columns Data",
            data=selectyear_import.to_csv(), file_name="import_custom.csv")
    else:
        st.download_button(label="Download Raw Data",
                           data=di_raw.to_csv(), file_name="import.csv")

    st.subheader('Analysis')

    fig_import = px.line(selectyear_import)
    fig_import.update_layout(
        xaxis=dict(dtick=1)
    )
    st.plotly_chart(fig_import)

    st.write('Again, majority have a percentage increase in import prices, ',
             'which could be due to COVID reducing the supply of workers and as a result ',
             'increasing unemployment rate which means fewer goods and services produced and thus higher prices')

