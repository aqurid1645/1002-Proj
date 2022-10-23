import streamlit as st
import pandas as pd
import base64
import plotly.express as px
import plotly.graph_objects as go
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

st.markdown("# INCOME 💰")
st.sidebar.markdown("# INCOME 💰")

tab1, tab2, tab3 = st.tabs(["Plot 1", "Plot 2", "Plot3"])

with tab1:
    dataExploration = st.container()

    with dataExploration:
        st.header('Dataset: GINI Coefficient')
        st.text('In this project I look into ...And I try ... I worked with the dataset from ...')

        st.header('Filter')

        df = pd.read_csv('/Users/leeke/Documents/SIT/YEAR 1/Trimester 1/INF1002 - PROGRAMMING FUNDAMENTALS/Assignment/Datasets/Income Datasets/Gini Coefficient Among Resident Employed Households, 2011 - 2021.csv')
        df = df.dropna()
        df = df[df.Year > 2016]
        df.Year = df.Year.astype(int)
        df = df.rename(columns={
            'Household Income from Work Per Household Member (Including Employer CPF Contributions)': 'Before Accounting for Government Transfers and Taxes',
            'Household Income from Work Per Household Member (Including Employer CPF Contributions) After Accounting for Government Transfers and Taxes1': 'After Accounting for Government Transfers and Taxes'})

        yearmax = int(df['Year'].max())
        yearmin = int(df['Year'].min())
        select_year = st.slider("Select Year:",yearmin,yearmax,(2017,2021))
        startyear, endyear = list(select_year)[0], list(select_year)[1]
        df = df[((df.Year >= startyear) & (df.Year <= endyear))]

        st.header('Table')

        st.write(df)


        csv = convert_df(df)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='Annual Change In Income By Household.csv',
            mime='text/csv',
        )

        st.header('Analysis')

        year = list(df.iloc[:, 0])
        before = list(df.iloc[:, 1])
        after = list(df.iloc[:, 2])

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=year,
            y=before,
            name="Before Accounting for Government Transfers and Taxes"  # this sets its legend entry
        ))

        fig.add_trace(go.Scatter(
            x=year,
            y=after,
            name="After Accounting for Government Transfers and Taxes"
        ))

        fig.update_layout(
            title="Household Income from Work Per Household Member (Including Employer CPF Contributions)",
            xaxis_title="Year",
            yaxis_title="Annual Change in %",
        )

        st.plotly_chart(fig, use_container_width=True)

        st.text('Let\'s take a look into the features I generated.')


with tab2:

    dataExploration = st.container()

    with dataExploration:
        st.header('Dataset: Income By Industry')
        st.text('I found this dataset at...I decided to work with it because ...')

        st.header('Filter')

        df8 = pd.read_csv('/Users/leeke/Documents/SIT/YEAR 1/Trimester 1/INF1002 - PROGRAMMING FUNDAMENTALS/Assignment/Datasets/Income Datasets/Total Wage (Nominal) Changes by Industry.csv')
        df8 = df8.drop(columns=['ind1'])
        df8 = df8.rename(columns={'year': 'Year', 'ind2': 'Industry', 'twc': 'Percentage'})
        df8 = df8[df8.Year > 2016]

        modification_container = st.container()
        with modification_container:
            to_filter_columns = st.multiselect("Filter dataframe on", df8.columns)
            for column in to_filter_columns:
                left, right = st.columns((1, 20))
                # Treat columns with < 10 unique values as categorical
                if is_numeric_dtype(df8[column]):
                    _min = int(df8[column].min())
                    _max = int(df8[column].max())
                    user_num_input = right.slider(
                        f"Values for {column}",
                        min_value=_min,
                        max_value=_max,
                        value=(_min, _max),
                    )
                    df8 = df8[df8[column].between(*user_num_input)]

                elif is_categorical_dtype(df8[column]) or df8[column].nunique() < 15:
                    user_cat_input = right.multiselect(
                        f"Values for {column}",
                        df8[column].unique(),
                        default=list(df8[column].unique()),
                    )
                    df8 = df8[df8[column].isin(user_cat_input)]

        st.header('Table')
        st.write(df8)


        csv = convert_df(df8)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='Annual Change In Income By Industry.csv',
            mime='text/csv',
        )

        st.header('Analysis')

        year = list(df8.iloc[:, 0])
        industry = list(df8.iloc[:, 1])
        percentage = list(df8.iloc[:, 2])
        #select = st.selectbox('Select Industry?', options=industry, index=0)

        fig = px.line(df8, x=year, y=percentage, color=industry)

        fig.update_traces(mode='markers+lines')

        fig.update_layout(
            title="Change In Income By Industry",
            xaxis_title="Industry",
            yaxis_title="Percentage Change (%)",
            legend_title="Industry",
        )

        st.plotly_chart(fig, use_container_width=True)

        #select = st.sidebar.selectbox('Select a State', df8['Industry'])
        #df8 = df8[df8['Industry'] == select]


        df9 = df8[df8.Year == 2020]
        df9 = df9.drop(columns=['Year'])
        df9 = df9.sort_values(by='Percentage')

        industry1 = list(df9.iloc[:, 0])
        percentage1 = list(df9.iloc[:, 1])

        fig = go.Figure(data=[
            go.Bar(x=industry1, y=percentage1)
        ])

        fig.update_layout(
            title="Change In Income By Industry In Year 2020",
            xaxis_title="Industry",
            yaxis_title="Percentage Change (%)",
        )

        st.plotly_chart(fig, use_container_width=True)

with tab3:

    dataExploration = st.container()


    with dataExploration:
        st.header('Dataset: Mean Annual Income By Gender')
        st.text('I found this dataset at...I decided to work with it because ...')

        df10 = pd.read_csv('/Users/leeke/Documents/SIT/YEAR 1/Trimester 1/INF1002 - PROGRAMMING FUNDAMENTALS/Assignment/Datasets/Income Datasets/Average (Mean) Monthly Earnings Per Employee By Sex (Total).csv',header=1)
        df10.rename(columns={df10.columns[0]: "Year"}, inplace=True)
        df10.set_index('Year', inplace=True)
        df10 = df10.iloc[:, -5:]
        df10 = df10.reset_index()
        df10 = df10.rename(columns={'Annual.1': 'Annual', '1Q .1': 'Q1', '2Q.1': 'Q2', '3Q.1': 'Q3', '4Q.1': 'Q4'})
        df10 = df10[df10.Year > 2016]
        df11 = df10.iloc[:, :-4]

        df12 = pd.read_csv('/Users/leeke/Documents/SIT/YEAR 1/Trimester 1/INF1002 - PROGRAMMING FUNDAMENTALS/Assignment/Datasets/Income Datasets/Average (Mean) Monthly Earnings Per Employee By Sex (Male).csv',header=1)
        df12.replace("-", "0.0", inplace=True)
        df12.rename(columns={df12.columns[0]: "Year"}, inplace=True)
        df12.set_index('Year', inplace=True)
        df12 = df12.iloc[:, -5:]
        df12 = df12.reset_index()
        df12 = df12.rename(columns={'Annual.1': 'Annual', '1Q .1': 'Q1', '2Q.1': 'Q2', '3Q.1': 'Q3', '4Q.1': 'Q4'})
        df12 = df12[df12.Year > 2016]
        df13 = df12.rename(columns={'Annual': 'Male'})
        df13 = df13.iloc[:, :2]

        df14 = pd.read_csv('/Users/leeke/Documents/SIT/YEAR 1/Trimester 1/INF1002 - PROGRAMMING FUNDAMENTALS/Assignment/Datasets/Income Datasets/Average (Mean) Monthly Earnings Per Employee By Sex (Female).csv',header=1)
        df14.rename(columns={df14.columns[0]: "Year"}, inplace=True)
        df14.set_index('Year', inplace=True)
        df14 = df14.iloc[:, -5:]
        df14 = df14.reset_index()
        df14 = df14.rename(columns={'Annual.1': 'Annual', '1Q .1': 'Q1', '2Q.1': 'Q2', '3Q.1': 'Q3', '4Q.1': 'Q4'})
        df14 = df14[df14.Year > 2016]
        df15 = df14.rename(columns={'Annual': 'Female'})
        df15 = df15.iloc[:, :2]
        df16 = pd.merge(df13, df15)

        year = list(df16.iloc[:, 0])
        first = list(df16.iloc[:, 1])
        second = list(df16.iloc[:, 2])

        fig = px.line(x=df11.iloc[:, 0], y=df11.iloc[:, 1], color=px.Constant("Total"),
                      labels=dict(x="Year", y="Mean Change in Percentage", color="Legend"))

        fig.add_bar(x=year, y=first, name="Male", marker_color='rgb(0,0,255)')
        fig.add_bar(x=year, y=second, name="Female", marker_color='rgb(255,0,0)')


        df17 = pd.merge(df11, df16)

        st.header('Filter')
        yearmax2 = int(df17['Year'].max())
        yearmin2 = int(df17['Year'].min())
        select_year2 = st.slider("Select Year:",yearmin2,yearmax2,(2017,2021), key = "<uniquevalueofsomesort>")
        startyear2, endyear2 = list(select_year2)[0], list(select_year2)[1]
        df17 = df17[((df17.Year >= startyear2) & (df17.Year <= endyear2))]



        st.header('Table')

        st.write(df17)

        csv = convert_df(df17)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='Annual Change In Income By Gender.csv',
            mime='text/csv',
        )

        st.header('Analysis')
        st.plotly_chart(fig, use_container_width=True)



