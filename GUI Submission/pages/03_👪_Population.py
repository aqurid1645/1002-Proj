import streamlit as st
import pandas as pd
import numpy as np
import cufflinks as cf
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
cf.go_offline()
st.set_page_config(layout="wide")

st.write("""
# POPULATION 👪
""")


tab1, tab2 = st.tabs(["Population", "COVID-19"])

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

with tab1:
    population = st.container()
    with population:
        file = "Datasets/Population/M8100011.csv"
        df = pd.read_csv(file)
        df1 = df
        df1.rename(columns = {'Data Series':'Year'}, inplace = True)

        df1.columns = df1.columns.str.replace(' ', '_')
        df1.columns = df1.columns.str.replace('(', '')
        df1.columns = df1.columns.str.replace(')', '')

        df1 = df1[(df1.Year > 2016) & (df1.Year < 2022)]
        yearmax = int(df1['Year'].max())
        yearmin = int(df1['Year'].min())
        select_year = st.slider("Select Year:",yearmin,yearmax,(2017,2021))
        startyear, endyear = list(select_year)[0], list(select_year)[1]
        df1 = df1[((df1.Year >= startyear) & (df1.Year <= endyear))]

        filtered = st.multiselect("Filter columns", options=list(df1.columns), default=list(df1.columns))

        st.subheader('Annual Population')
        st.write(df1[filtered])

        # Download box
        option = st.selectbox("Raw or Custom",
                              ("Raw", "Custom"), key='1')
        if option == "Custom":
            st.download_button(
                label="Download Customised Columns Data",
                data=df1.to_csv(), file_name="Population_Custom.csv")
        else:
            st.download_button(label="Download Raw Data",
                               data=df.to_csv(), file_name="Population.csv")


        st.subheader('Analysis')
        fig = go.Figure()
        df_plot = df1.iloc[1:6,:]
        fig.add_trace(go.Scatter(x=df_plot.Year, y=df_plot.Total_Population_Number))
        fig.update_layout(title='Total Population in Singapore 2019-2022', xaxis_title='Year',
                          yaxis_title='Population',
                          xaxis=dict(dtick=1))

        st.plotly_chart(fig)
        st.write('''There is a sharp decrease in population from 2020 to 2021.
            Possible reasons include COVID-related deaths or foreigners being sent back to their home countries.
            ''')

with tab2:
        file = "Datasets/Population/owid-covid-data.csv"
        df_covid_ori = pd.read_csv(file)
        df_covid = df_covid_ori[df_covid_ori["location"] == "Singapore"]
        df_covid = df_covid.iloc[342:, :]

        st.subheader('Analysis of COVID vaccinations and COVID deaths')
        st.write(df_covid)

        # Download box
        option = st.selectbox("Raw or Custom",
                              ("Raw", "Custom"), key='2')
        if option == "Custom":
            st.download_button(
                label="Download Customised Columns Data",
                data=df_covid.to_csv(), file_name="COVID_Custom.csv")
        else:
            st.download_button(label="Download Raw Data",
                               data=df_covid_ori.to_csv(), file_name="COVID.csv")


        df_covid.date = pd.to_datetime(df_covid.date)
        df_covid.set_index('date', inplace=True)
        df_covid = df_covid.resample('MS').sum()

        x = df_covid['people_vaccinated'].values
        x = x.reshape(-1, 1)
        y = df_covid['new_deaths'].values
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=0)

        model = LinearRegression()
        model.fit(X_train, y_train)

        x_range = np.linspace(x.min(), x.max(), 100)
        y_range = model.predict(x_range.reshape(-1, 1))

        fig = go.Figure([
            go.Scatter(x=X_train.squeeze(), y=y_train, name='train', mode='markers'),
            go.Scatter(x=X_test.squeeze(), y=y_test, name='test', mode='markers'),
            go.Scatter(x=x_range, y=y_range, name='prediction')
        ])
        fig.update_layout(xaxis_title_text='Number of people vaccinated',
                          yaxis_title_text='Number of COVID deaths')


        st.subheader('Analysis')
        st.plotly_chart(fig)
        st.write("r2 score: " + str(r2_score(y_test, model.predict(X_test))))
        st.write('''There is a low death rate when the number of vaccination increases.
            Towards the end, there is a sharp increase in the number of deaths due to COVID.
            This shows that there are other factors other than just vaccinations which correlates 
            to the number of deaths. Possible reasons include the mutation of the virus, the decrease of
            strictness of government policies.
            ''')