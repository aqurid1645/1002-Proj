import pandas as pd
import streamlit as st
import plotly.express as px
import os
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
st.set_page_config(layout="wide")
# header
st.markdown('# RETRENCHMENT 💸')

# reading file

pth = "Datasets/Retrenchment/"
r_occupation_level_1 = "retrenchment-by-industry-level-1.csv"
r_occupation_level_2 = "retrenchment-by-industry-level-2.csv"
r_overview = "retrenchment-topline.csv"
r_numbers = "statistic_id1155641_retrenchment-numbers-in-singapore-2012-2021.csv"

# main
year_max = 2021
year_min = 2017


# tabs
tab1, tab2, tab3, tab4 = st.tabs(['Industries',
                                  'Permanent vs Term-Contract',
                                  'Quantity',
                                  'Rate of Re-Entry'])


def comparison_by_industry():

    # timeline between two dates

    # reading specific file
    vfl = r_occupation_level_2
    my_file = f"{pth}{vfl}"
    df = pd.read_csv(my_file).replace("-", 0)
    df = df.rename(columns={"year": "Year",
                            "industry1": "Industry",
                            "industry2": "Sub-Industry",
                            "retrench": "Retrenched",
                            "retrench_permanent": "Retrenched Permanent",
                            "retrench_term_contract": "Retrenched Term Contract"})
    df['Year'] = df['Year'].astype(int)

    # df = df.drop(["retrench_permanent", "retrench_term_contract"], axis=1)

    # retrieve unique occupation categories
    select_industry = sorted(df["Industry"].unique())
    select_industry_dropdown = st.multiselect('Select 1 or more Industries(s):', select_industry,
                                              [
                                                  'manufacturing',
                                                  'construction',
                                                  'services',
                                                  'others'
                                              ])

    selected_industry_years = df[
        (df.Industry.isin(select_industry_dropdown)) &
        ((df.Year >= start_year) & (df.Year <= end_year))]

    # find max year and min year of data
    # select_year_range = sorted(df["Year"].unique())
    # year_max = df["Year"].max()
    # year_min = df["Year"].min()
    st.subheader('Comparison by Industry')
    st.dataframe(selected_industry_years.reset_index(drop=True), use_container_width=True)

    # download button
    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csv = convert_df(selected_industry_years)

    st.download_button("Download CSV", csv, "file.csv", "text/csv", key='download-csv-ind-comp')

    # graph
    choose_graph_viewing = st.radio("View graph:",
                                    ('Annual Retrenchment Overview',
                                     'Retrenchment by Broad Industry',
                                     'Retrenchment by Sub-Industry',
                                     ))

    if choose_graph_viewing == "Annual Retrenchment Overview":
        # reading specific file
        vfl = r_overview
        my_file = f"{pth}{vfl}"
        df = pd.read_csv(my_file).replace("-", 0)
        df = df.drop(["retrench_permanent", "retrench_term_contract"], axis=1)
        df = df.rename(columns={"year": "Year",
                                "retrench": "Retrenched"})

        selected_industry_years = df[
            ((df.Year >= start_year) & (df.Year <= end_year))]

        fig = px.line(selected_industry_years,
                      x="Year",
                      y="Retrenched"
                      )
        st.subheader('Analysis')
        st.plotly_chart(fig, use_container_width=True)

    elif choose_graph_viewing == "Retrenchment by Broad Industry":
        # reading specific file
        vfl = r_occupation_level_1
        my_file = f"{pth}{vfl}"
        df = pd.read_csv(my_file).replace("-", 0)
        df = df.drop(["retrench_permanent", "retrench_term_contract"], axis=1)
        df = df.rename(columns={"year": "Year",
                                "industry1": "Industry",
                                "retrench": "Retrenched"})
        df['Retrenched'] = df['Retrenched'].astype(int)

        selected_industry_years = df[
            ((df.Year >= start_year) & (df.Year <= end_year))]

        fig = px.line(selected_industry_years,
                      x="Year",
                      y="Retrenched",
                      color="Industry",
                      markers=True
                      )
        st.subheader('Analysis')
        st.plotly_chart(fig, use_container_width=True)

    elif choose_graph_viewing == "Retrenchment by Sub-Industry":
        # reading specific file
        vfl = r_occupation_level_2
        my_file = f"{pth}{vfl}"
        df = pd.read_csv(my_file).replace("-", 0)
        df = df.drop(["industry1", "retrench_permanent", "retrench_term_contract"], axis=1)
        df = df.rename(columns={"year": "Year",
                                "industry2": "Sub Industry",
                                "retrench": "Retrenched"})
        df['Retrenched'] = df['Retrenched'].astype(int)

        selected_industry_years = df[
            ((df.Year >= start_year) & (df.Year <= end_year))]

        fig = px.line(selected_industry_years,
                      x="Year",
                      y="Retrenched",
                      color="Sub Industry"
                      )
        st.subheader('Analysis')
        st.plotly_chart(fig, use_container_width=True)


def perm_vs_term_contract():
    st.subheader('Grouped Bar Chart of Permanent vs Term-Contract Employees')
    # perm vs term-contract
    # reading specific file
    vfl = r_overview
    my_file = f"{pth}{vfl}"
    df = pd.read_csv(my_file).replace("-", 0)
    df = df.drop(["retrench"], axis=1)
    df = df.rename(columns={"year": "Year",
                            "retrench_permanent": "Permanent",
                            "retrench_term_contract": "Term Contract"})
    df['Year'] = df['Year'].astype(int)
    df['Permanent'] = df['Permanent'].astype(int)
    df['Term Contract'] = df['Term Contract'].astype(int)

    df = df[
        ((df.Year >= start_year) & (df.Year <= end_year))]

    st.dataframe(df.reset_index(drop=True), use_container_width=True)

    # download button
    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csv = convert_df(df)

    st.download_button("Download CSV", csv, "file.csv", "text/csv", key='download-csv-perm-vs-cont')

    fig = px.bar(df,
                 x="Year",
                 y=["Permanent", "Term Contract"],
                 )
    st.subheader('Analysis')
    st.plotly_chart(fig, use_container_width=True)


def quantity():
    st.subheader('Quantity of retrenched workers')
    # nice metrics
    st.metric(
        label="Peak of chart:",
        value="Every 26.11 in 1000 people",
        delta="44.2% (from previous year)"
    )
    # reading specific file
    vfl = r_numbers
    my_file = f"{pth}{vfl}"
    df = pd.read_csv(my_file)
    df = df.rename(columns={"year": "Year", "quantity": "Quantity"})
    df['Year'] = df['Year'].astype(int)
    df['Quantity'] = df['Quantity'].astype(float)
    df['Quantity'] = df['Quantity'].apply(lambda x: "{:.2f}".format(x))

    selected_years = df[
        ((df.Year >= start_year) & (df.Year <= end_year))]

    st.dataframe(selected_years.reset_index(drop=True), use_container_width=True)

    # download button
    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csv = convert_df(selected_years)

    st.download_button("Download CSV", csv, "file.csv", "text/csv", key='download-csv-quantity')

    fig = px.line(selected_years,
                  x='Year',
                  y='Quantity',
                  title=f'Retrenchment Rates from {year_min}-{year_max}(per 1000)'
                  )
    fig.update_layout(autotypenumbers='convert types')
    st.subheader('Analysis')
    st.plotly_chart(fig, use_container_width=True)


def rate_of_reentry():
    st.subheader('Rate of Re-entry into the workplace after COVID-19')
    path = "Datasets/Retrenchment/rate-of-re-entry-into-employment-annual/"
    files = os.listdir(path)

    file_list = [os.path.splitext(file)[0] for file in files]
    # st.write(file_list)

    select_filtered_files = st.selectbox("Rate of re-entry sorted by:", file_list)

    if select_filtered_files:
        df = pd.read_csv(f"{path}/{select_filtered_files}.csv")

        if select_filtered_files == "Age":
            df = df.rename(columns={"year": "Year",
                                    "age1": "Age",
                                    "reentry_rate": "Re-entry Rate"})
            df = df.loc[df['Age'].isin(['Below 30', '30 - 39', '40 - 49', '50 - 59', '60 & Over'])]
            df['Re-entry Rate'] = df['Re-entry Rate'].astype(float)
            df['Re-entry Rate'] = df['Re-entry Rate'].apply(lambda x: "{:.1f}".format(x))

            selected_years = df[
                ((df.Year >= start_year) & (df.Year <= end_year))]

            fig = px.line(selected_years,
                          x='Year',
                          y='Re-entry Rate',
                          color="Age",
                          title=f'Retrenchment Rates from {year_min}-{year_max}(per 1000)'
                          )
            fig.update_layout(autotypenumbers='convert types')
            st.subheader('Analysis')
            st.plotly_chart(fig, use_container_width=True)

        if select_filtered_files == "Educational attainment":
            df = df.rename(columns={"year": "Year",
                                    "education1": "Education",
                                    "reentry_rate": "Re-entry Rate"})
            df['Re-entry Rate'] = df['Re-entry Rate'].astype(float)
            df['Re-entry Rate'] = df['Re-entry Rate'].apply(lambda x: "{:.1f}".format(x))

            selected_years = df[
                ((df.Year >= start_year) & (df.Year <= end_year))]

            fig = px.line(selected_years,
                          x='Year',
                          y='Re-entry Rate',
                          color="Education",
                          title=f'Retrenchment Rates from {year_min}-{year_max}(per 1000)'
                          )
            fig.update_layout(autotypenumbers='convert types')
            st.subheader('Analysis')
            st.plotly_chart(fig, use_container_width=True)

        if select_filtered_files == "Occupational group prior to retrenchment":
            df = df.rename(columns={"year": "Year",
                                    "occupation1": "Occupation",
                                    "reentry_rate": "Re-entry Rate"})
            df['Re-entry Rate'] = df['Re-entry Rate'].astype(float)
            df['Re-entry Rate'] = df['Re-entry Rate'].apply(lambda x: "{:.1f}".format(x))

            selected_years = df[
                ((df.Year >= start_year) & (df.Year <= end_year))]

            fig = px.line(selected_years,
                          x='Year',
                          y='Re-entry Rate',
                          color="Occupation",
                          title=f'Retrenchment Rates from {year_min}-{year_max}(per 1000)'
                          )
            fig.update_layout(autotypenumbers='convert types')
            st.plotly_chart(fig, use_container_width=True)

        if select_filtered_files == "Overview":
            df = df.rename(columns={"year": "Year",
                                    "reentry_rate": "Re-entry Rate"})
            df['Re-entry Rate'] = df['Re-entry Rate'].astype(float)
            df['Re-entry Rate'] = df['Re-entry Rate'].apply(lambda x: "{:.1f}".format(x))

            selected_years = df[
                ((df.Year >= start_year) & (df.Year <= end_year))]

            fig = px.line(selected_years,
                          x='Year',
                          y='Re-entry Rate',
                          title=f'Retrenchment Rates from {year_min}-{year_max}(per 1000)'
                          )
            fig.update_layout(autotypenumbers='convert types')
            st.subheader('Analysis')
            st.plotly_chart(fig, use_container_width=True)

        if select_filtered_files == "Sex":
            df = df.rename(columns={"year": "Year",
                                    "sex1": "Sex",
                                    "reentry_rate": "Re-entry Rate"})
            df['Re-entry Rate'] = df['Re-entry Rate'].astype(float)
            df['Re-entry Rate'] = df['Re-entry Rate'].apply(lambda x: "{:.1f}".format(x))

            selected_years = df[
                ((df.Year >= start_year) & (df.Year <= end_year))]

            fig = px.line(selected_years,
                          x='Year',
                          y='Re-entry Rate',
                          color="Sex",
                          title=f'Retrenchment Rates from {year_min}-{year_max}(per 1000)'
                          )
            fig.update_layout(autotypenumbers='convert types')
            st.subheader('Analysis')
            st.plotly_chart(fig, use_container_width=True)


# output
with tab1:
    # giving slider range
    select_year_slider = st.select_slider('Year range:',
                                          options=[2017, 2018, 2019, 2020, 2021],
                                          value=(2017, 2021))
    # designating start year and end year to selected slider values
    start_year, end_year = list(select_year_slider)[0], list(select_year_slider)[1]
    comparison_by_industry()

    st.write("The graphs above show that while in the year 2020, where Retrenchment rates peaked, the Services "
             "industry took the biggest hit when COVID-19 was at its climax in Singapore. "
             "On closer inspection, we can see that the industry most affected was Wholesale and Retail Trade, "
             "followed by Transportation and Storage, then Community, Social and Personal Services. With the country "
             "on lockdown in 2020, people moved their services online, which meant a significantly reduced "
             "interaction with physical services, and transport. Hence leading to a decrease in the need for "
             "employees in these sectors.")

with tab2:
    # giving slider range
    select_year_slider = st.select_slider('Year range:',
                                          options=[2017, 2018, 2019, 2020, 2021],
                                          value=(2017, 2021), key = "<uniquevaluefortab2>")
    # designating start year and end year to selected slider values
    start_year, end_year = list(select_year_slider)[0], list(select_year_slider)[1]
    perm_vs_term_contract()
    st.write("From the chart, it is evident that the year 2020 has the highest increase in retrenchment rates, "
             "in both permanent and term-contracted employees."
             " COVID-19 caused many companies to go out of business, "
             "leading to high retrenchment, and the highest retrenchment rate in the span of 5 years. ")


with tab3:

    # giving slider range
    select_year_slider = st.select_slider('Year range:',
                                          options=[2017, 2018, 2019, 2020, 2021],
                                          value=(2017, 2021), key = "<uniquevaluefortab3>")
    # designating start year and end year to selected slider values
    start_year, end_year = list(select_year_slider)[0], list(select_year_slider)[1]
    quantity()
    st.write("From the charts, it is evident that the year 2020 experienced the highest increase in retrenchment, "
             "with a 44.2% increase from the previous year, leading to every 26.11 per 1000 people being retrenched. "
             " COVID-19 caused many companies to go out of business, "
             "leading to high retrenchment, and the highest retrenchment rate in the span of 5 years. ")

with tab4:

    # giving slider range
    select_year_slider = st.select_slider('Year range:',
                                          options=[2017, 2018, 2019, 2020, 2021],
                                          value=(2017, 2021), key = "<uniquevaluefortab4>")
    # designating start year and end year to selected slider values
    start_year, end_year = list(select_year_slider)[0], list(select_year_slider)[1]
    rate_of_reentry()
    st.write("Annual re-entry rate measures the proportion of residents who are in employment in the reference year, "
             "six months after retrenchment.")
    st.write("From the graphs shown above, it is evident that re-entry rates were at "
             "their lowest in the year 2020, in a 5 year span, regardless of age, educational attainment, "
             "sex or occupational group prior to retrenchment. COVID-19 caused many companies to go out of business, "
             "leading to high retrenchment and low re-entry, since they could not afford to keep so many people in "
             "the company.")
