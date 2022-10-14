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

st.set_page_config(layout="wide")
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

st.markdown("# INCOME 💰")


tab1, tab2, tab3, tab4 = st.tabs(["GINI Coefficient", "Range", "Gender","Industry"])

with tab1:
    dataExploration = st.container()

    with dataExploration:

        df_raw = pd.read_csv('Datasets/Income/Gini Coefficient Among Resident Employed Households, 2011 - 2021.csv')
        df = df_raw.dropna()
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

        st.subheader('Annual Change In GINI Coefficient')

        st.write(df)

        # Download box
        option = st.selectbox("Raw or Custom",
                              ("Raw", "Custom"), key='1')
        if option == "Custom":
            st.download_button(
                label="Download Customised Columns Data",
                data=df.to_csv(), file_name="Annual Change In GINI Coefficient_Custom.csv")
        else:
            st.download_button(label="Download Raw Data",
                               data=df_raw.to_csv(), file_name="Annual Change In GINI Coefficient.csv")

        st.subheader('Analysis')

        year = list(df.iloc[:, 0])
        before = list(df.iloc[:, 1])
        after = list(df.iloc[:, 2])

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=year,
            y=before,
            name="Before Accounting for Government Transfers and Taxes" # this sets its legend entry
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

        df2_raw = pd.read_csv(
            'Datasets/Income/Resident Households by Monthly Household Income from Work Per Household Member (Including Employer CPF Contributions), 2011 - 2021.csv',
            index_col=0)
        df2 = df2_raw.drop(df2_raw.iloc[:, 0:6], axis=1)
        df2 = df2.dropna()
        df2 = df2.drop(
            ["Total", "Solely Non-Employed Persons Aged 65 Years & Over", "Households with No Employed Person"])
        df2 = df2.stack()
        df2 = pd.DataFrame.from_dict(df2)
        df2 = df2.reset_index()
        df2 = df2.rename(columns={'level_0': 'Range', 'level_1': 'Year'})
        df2.columns = [*df2.columns[:-1], 'Percentage']
        df2['Range'] = df2['Range'].str.replace('$', ' ')

        modification_container = st.container()
        with modification_container:
            to_filter_columns = st.multiselect("Filter dataframe on", df2.columns)
            for column in to_filter_columns:
                left, right = st.columns((1, 20))
                # Treat columns with < 10 unique values as categorical
                if is_numeric_dtype(df2[column]):
                    _min = int(df2[column].min())
                    _max = int(df2[column].max())
                    user_num_input = right.slider(
                        f"Values for {column}",
                        min_value=_min,
                        max_value=_max,
                        value=(_min, _max),
                    )
                    df2 = df2[df2[column].between(*user_num_input)]

                else:
                    user_cat_input = right.multiselect(
                        f"Values for {column}",
                        df2[column].unique(),
                        default=list(df2[column].unique()),
                    )
                    df2 = df2[df2[column].isin(user_cat_input)]


        st.subheader('Annual Change In Income By Range')

        st.write(df2)

        # Download box
        option = st.selectbox("Raw or Custom",
                              ("Raw", "Custom"), key='2')
        if option == "Custom":
            st.download_button(
                label="Download Customised Columns Data",
                data=df2.to_csv(), file_name="Annual Change In Income By Range_Custom.csv")
        else:
            st.download_button(label="Download Raw Data",
                               data=df2_raw.to_csv(), file_name="Annual Change In Income By Range.csv")

        st.subheader('Analysis')

        rang = list(df2.iloc[:, 0])
        year = list(df2.iloc[:, 1])
        percentage = list(df2.iloc[:, 2])

        fig = px.bar(df2, x="Range", y="Percentage", color="Year")

        fig.update_layout(
            barmode='group',
            xaxis_tickangle=-45,
            title="Annual Change In Income By Range",
            xaxis_title="Range in Dollars ($)",
            yaxis_title="Change In Percentage (%)"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.text('Let\'s take a look into the features I generated.')

with tab3:

    dataExploration = st.container()


    with dataExploration:

        df3_raw = pd.read_csv('Datasets/Income/Average (Mean) Monthly Earnings Per Employee By Sex (Total).csv',header=1)
        df3 = df3_raw
        df3.rename(columns={df3.columns[0]: "Year"}, inplace=True)
        df3.set_index('Year', inplace=True)
        df3 = df3.iloc[:, -5:]
        df3 = df3.reset_index()
        df3 = df3.rename(columns={'Annual.1': 'Annual', '1Q .1': 'Q1', '2Q.1': 'Q2', '3Q.1': 'Q3', '4Q.1': 'Q4'})
        df3 = df3[df3.Year > 2016]
        df4 = df3.iloc[:, :-4]
        df4 = df4.rename(columns={'Annual': 'Total'})

        df5_raw = pd.read_csv('Datasets/Income/Average (Mean) Monthly Earnings Per Employee By Sex (Male).csv',header=1)
        df5 = df5_raw
        df5.replace("-", "0.0", inplace=True)
        df5.rename(columns={df5.columns[0]: "Year"}, inplace=True)
        df5.set_index('Year', inplace=True)
        df5 = df5.iloc[:, -5:]
        df5 = df5.reset_index()
        df5 = df5.rename(columns={'Annual.1': 'Annual', '1Q .1': 'Q1', '2Q.1': 'Q2', '3Q.1': 'Q3', '4Q.1': 'Q4'})
        df5 = df5[df5.Year > 2016]
        df6 = df5.rename(columns={'Annual': 'Male'})
        df6 = df6.iloc[:, :2]

        df7_raw = pd.read_csv('Datasets/Income/Average (Mean) Monthly Earnings Per Employee By Sex (Female).csv',header=1)
        df7 = df7_raw
        df7.rename(columns={df7.columns[0]: "Year"}, inplace=True)
        df7.set_index('Year', inplace=True)
        df7 = df7.iloc[:, -5:]
        df7 = df7.reset_index()
        df7 = df7.rename(columns={'Annual.1': 'Annual', '1Q .1': 'Q1', '2Q.1': 'Q2', '3Q.1': 'Q3', '4Q.1': 'Q4'})
        df7 = df7[df7.Year > 2016]
        df8 = df7.rename(columns={'Annual': 'Female'})
        df8 = df8.iloc[:, :2]
        df9 = pd.merge(df6, df8)
        df10 = pd.merge(df4, df9)

        yearmax2 = int(df4['Year'].max())
        yearmin2 = int(df4['Year'].min())
        select_year2 = st.slider("Select Year:",yearmin2,yearmax2,(2017,2021), key = "<uniquevalueofsomesort>")
        startyear2, endyear2 = list(select_year2)[0], list(select_year2)[1]
        df4= df4[((df4.Year >= startyear2) & (df4.Year <= endyear2))]

        choice = st.radio(
            "Choice of Visualisation:",
            ('Annual Change In Income By Gender (Overall)', 'Annual Change In Income By Gender (Total)', 'Annual Change In Income By Gender (Male)','Annual Change In Income By Gender (Female)'))

        if choice == 'Annual Change In Income By Gender (Overall)':

            st.subheader('Table')

            st.write(df10)

            csv = convert_df(df10)
            st.download_button(
                label="Download Customised Columns Data",
                data=csv,
                file_name='Annual Change In Income By Gender (Overall)_Custom.csv',
                mime='text/csv',
            )

            st.subheader('Analysis')

            year1 = list(df4.iloc[:, 0])
            first = list(df9.iloc[:, 1])
            second = list(df9.iloc[:, 2])

            fig = px.line(x=df4.iloc[:, 0], y=df4.iloc[:, 1], color=px.Constant("Total"),
                          labels=dict(x="Year", y="Mean Change in Percentage", color="Legend"))

            fig.add_bar(x=year1, y=first, name="Male", marker_color='rgb(0,0,255)')
            fig.add_bar(x=year1, y=second, name="Female", marker_color='rgb(255,0,0)')

            st.plotly_chart(fig, use_container_width=True)

        elif choice == 'Annual Change In Income By Gender (Total)':

            st.subheader('Table')

            df3_custom = df3[['Year', 'Q1', 'Q2', 'Q3', 'Q4']]

            st.write(df3_custom)

            # Download box
            option = st.selectbox("Raw or Custom",
                                  ("Raw", "Custom"), key='3')
            if option == "Custom":
                st.download_button(
                    label="Download Customised Columns Data",
                    data=df3_custom.to_csv(), file_name="Annual Change In Income By Gender (Total)_Custom.csv")
            else:
                st.download_button(label="Download Raw Data",
                                   data=df3_raw.to_csv(), file_name="Annual Change In Income By Gender (Total).csv")

            st.subheader('Analysis')

            year2 = list(df4.iloc[:, 0])
            Q1 = list(df3.iloc[:, 2])
            Q2 = list(df3.iloc[:, 3])
            Q3 = list(df3.iloc[:, 4])
            Q4 = list(df3.iloc[:, 5])

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=year2,
                y=Q1,
                name="Q1"  # this sets its legend entry
            ))

            fig.add_trace(go.Scatter(
                x=year2,
                y=Q2,
                name="Q2"
            ))

            fig.add_trace(go.Scatter(
                x=year2,
                y=Q3,
                name="Q3"
            ))

            fig.add_trace(go.Scatter(
                x=year2,
                y=Q4,
                name="Q4"
            ))

            fig.update_layout(
                title="Annual Change In Income By Gender (Total)",
                xaxis_title="Year",
                yaxis_title="Change In Percentage (%)",
            )

            st.plotly_chart(fig, use_container_width=True)

        elif choice == 'Annual Change In Income By Gender (Male)':

            st.subheader('Table')
            df5_custom = df5[['Year','Q1','Q2','Q3','Q4']]
            st.write(df5_custom)

            # Download box
            option = st.selectbox("Raw or Custom",
                                  ("Raw", "Custom"), key='4')
            if option == "Custom":
                st.download_button(
                    label="Download Customised Columns Data",
                    data=df5_custom.to_csv(), file_name="Annual Change In Income By Gender (Male)_Custom.csv")
            else:
                st.download_button(label="Download Raw Data",
                                   data=df5_raw.to_csv(), file_name="Annual Change In Income By Gender (Male).csv")

            st.subheader('Analysis')

            year3 = list(df4.iloc[:, 0])
            Q1 = list(df5.iloc[:, 2])
            Q2 = list(df5.iloc[:, 3])
            Q3 = list(df5.iloc[:, 4])
            Q4 = list(df5.iloc[:, 5])

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=year3,
                y=Q1,
                name="Q1"  # this sets its legend entry
            ))

            fig.add_trace(go.Scatter(
                x=year3,
                y=Q2,
                name="Q2"
            ))

            fig.add_trace(go.Scatter(
                x=year3,
                y=Q3,
                name="Q3"
            ))

            fig.add_trace(go.Scatter(
                x=year3,
                y=Q4,
                name="Q4"
            ))

            fig.update_layout(
                title="Annual Change In Income By Gender (Male)",
                xaxis_title="Year",
                yaxis_title="Change In Percentage (%)",
            )

            st.plotly_chart(fig, use_container_width=True)

        else:

            st.subheader('Table')
            df7_custom = df7[['Year', 'Q1', 'Q2', 'Q3', 'Q4']]
            st.write(df7_custom)

            # Download box
            option = st.selectbox("Raw or Custom",
                                  ("Raw", "Custom"), key='5')
            if option == "Custom":
                st.download_button(
                    label="Download Customised Columns Data",
                    data=df7_custom.to_csv(), file_name="Annual Change In Income By Gender (Female)_Custom.csv")
            else:
                st.download_button(label="Download Raw Data",
                                   data=df7_raw.to_csv(), file_name="Annual Change In Income By Gender (Female).csv")

            st.subheader('Analysis')

            year4 = list(df4.iloc[:, 0])
            Q1 = list(df7.iloc[:, 2])
            Q2 = list(df7.iloc[:, 3])
            Q3 = list(df7.iloc[:, 4])
            Q4 = list(df7.iloc[:, 5])

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=year4,
                y=Q1,
                name="Q1"  # this sets its legend entry
            ))

            fig.add_trace(go.Scatter(
                x=year4,
                y=Q2,
                name="Q2"
            ))

            fig.add_trace(go.Scatter(
                x=year4,
                y=Q3,
                name="Q3"
            ))

            fig.add_trace(go.Scatter(
                x=year4,
                y=Q4,
                name="Q4"
            ))

            fig.update_layout(
                title="Annual Change In Income By Gender (Female)",
                xaxis_title="Year",
                yaxis_title="Change In Percentage (%)",
            )

            st.plotly_chart(fig, use_container_width=True)


with tab4:

    dataExploration = st.container()

    with dataExploration:

        df11_raw = pd.read_csv('Datasets/Income/Total Wage (Nominal) Changes by Industry.csv')
        df11 = df11_raw
        df11 = df11.drop(columns=['ind1'])
        df11 = df11.rename(columns={'year': 'Year', 'ind2': 'Industry', 'twc': 'Percentage'})
        df11 = df11[df11.Year > 2016]

        modification_container = st.container()
        with modification_container:
            to_filter_columns = st.multiselect("Filter dataframe on", df11.columns)
            for column in to_filter_columns:
                left, right = st.columns((1, 20))
                # Treat columns with < 10 unique values as categorical
                if is_numeric_dtype(df11[column]):
                    _min = int(df11[column].min())
                    _max = int(df11[column].max())
                    user_num_input = right.slider(
                        f"Values for {column}",
                        min_value=_min,
                        max_value=_max,
                        value=(_min, _max),
                    )
                    df11 = df11[df11[column].between(*user_num_input)]

                elif is_categorical_dtype(df11[column]) or df11[column].nunique() < 15:
                    user_cat_input = right.multiselect(
                        f"Values for {column}",
                        df11[column].unique(),
                        default=list(df11[column].unique()),
                    )
                    df11 = df11[df11[column].isin(user_cat_input)]

        st.subheader('Annual Change In Income By Industry')
        st.write(df11)

        # Download box
        option = st.selectbox("Raw or Custom",
                              ("Raw", "Custom"), key='6')
        if option == "Custom":
            st.download_button(
                label="Download Customised Columns Data",
                data=df11.to_csv(), file_name="Annual Change In Income By Industry_Custom.csv")
        else:
            st.download_button(label="Download Raw Data",
                               data=df11_raw.to_csv(), file_name="Annual Change In Income By Industry.csv")

        st.subheader('Analysis')

        year5 = list(df11.iloc[:, 0])
        industry = list(df11.iloc[:, 1])
        percentage = list(df11.iloc[:, 2])
        #select = st.selectbox('Select Industry?', options=industry, index=0)

        fig = px.line(df11, x=year5, y=percentage, color=industry)

        fig.update_traces(mode='markers+lines')

        fig.update_layout(
            title="Annual Change In Income By Industry",
            xaxis_title="Industry",
            yaxis_title="Change In Percentage (%)",
            legend_title="Industry",
        )

        st.plotly_chart(fig, use_container_width=True)

        #select = st.sidebar.selectbox('Select a State', df8['Industry'])
        #df8 = df8[df8['Industry'] == select]

        agree = st.checkbox('Show Year 2019 Data Distribution')
        agree2 = st.checkbox('Show Year 2020 Data Distribution')
        agree3 = st.checkbox('Show Year 2021 Data Distribution')

        if agree:

            df12 = df11[df11.Year == 2019]
            df12 = df12.drop(columns=['Year'])
            df12 = df12.sort_values(by='Percentage')

            industry = list(df12.iloc[:, 0])
            percentage = list(df12.iloc[:, 1])

            fig = go.Figure(data=[
                go.Bar(x=industry, y=percentage)
            ])

            fig.update_layout(
                title="Change In Income By Industry In Year 2019",
                xaxis_title="Industry",
                yaxis_title="Change In Percentage (%)",
            )

            st.plotly_chart(fig, use_container_width=True)

        if agree2:

            df13 = df11[df11.Year == 2020]
            df13 = df13.drop(columns=['Year'])
            df13 = df13.sort_values(by='Percentage')

            industry = list(df13.iloc[:, 0])
            percentage = list(df13.iloc[:, 1])

            fig = go.Figure(data=[
                go.Bar(x=industry, y=percentage)
            ])

            fig.update_layout(
                title="Change In Income By Industry In Year 2020",
                xaxis_title="Industry",
                yaxis_title="Change In Percentage (%)",
            )

            st.plotly_chart(fig, use_container_width=True)

        if agree3:

            df14 = df11[df11.Year == 2021]
            df14 = df14.drop(columns=['Year'])
            df14 = df14.sort_values(by='Percentage')

            industry = list(df14.iloc[:, 0])
            percentage = list(df14.iloc[:, 1])

            fig = go.Figure(data=[
                go.Bar(x=industry, y=percentage)
            ])

            fig.update_layout(
                title="Change In Income By Industry In Year 2021",
                xaxis_title="Industry",
                yaxis_title="Change In Percentage (%)",
            )

            st.plotly_chart(fig, use_container_width=True)





