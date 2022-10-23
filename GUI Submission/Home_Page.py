import streamlit as st
import cufflinks as cf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

import plotly.express as px
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
cf.go_offline()
st.set_page_config(layout="wide")
st.write("""
# COVID-19 ANALYZER
This tool analyzes the **impacts of COVID-19**
""")

summary = st.container()
machinelearning = st.container()
with summary:
        st.header("Singapore at a glance as of 2022")
         # I created 2 rows of 3 columns but u all might want to do 3 rows of 2 columns instead
        # 3 columns means the wordings per columns will be shorter
        # So u all decided based on the situation ba
        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)
        col1.metric("Population", "5,453,566", "-4.26%")
        col2.metric("Employment", "71.3", "475.3%")
        col3.metric("Income - Gini Coefficient", "0.386%", "0.011%")
        col4.metric("Recruitement", "2.1%", "0.5%")
        col4.metric("Resignation", "1.7%", "0.2%")
        col5.metric("Retrenchment", "Every 26.11 in 1000 people", "144.2%")
        col6.metric("Inflation", "$102.119", "2.3%")

        DEFAULT_WIDTH = 30
        # #VIDEO_DATA = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        VIDEO_DATA = open('GUI DEMO.mp4', 'rb')
        VIDEO_DATA = VIDEO_DATA.read()
        #
        # #st.video(VIDEO_DATA)
        _, container, _ = st.columns([5, 10, 5])
        container.video(data=VIDEO_DATA)

with machinelearning:
        st.header("Machine Learning")

        dataset = pd.read_csv('Datasets/Machine Learning/combined1.csv')
        X = dataset.iloc[:, 2:-1].values
        y = dataset.iloc[:, -1].values
        ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0])], remainder='passthrough')
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=0)

        regressor = RandomForestRegressor(n_estimators=100, random_state=0)
        regressor.fit(X_train, y_train)

        y_pred = regressor.predict(X_test)
        np.set_printoptions(precision=2)

        value = list(range(len(y_test))) * 2
        test = y_test.tolist()
        pred = y_pred.tolist()
        test.extend(pred)
        data_type = ["test"] * len(y_test) + ["pred"] * len(y_test)

        plotting = pd.DataFrame(data={"Value": value,
                                  "Y": test,
                                  "Type": data_type})

        fig = px.scatter(plotting, x="Value", y="Y", color="Type",)

        fig.update_layout(xaxis_title_text='Value',
                          yaxis_title_text='Y')

        feature_list = dataset.columns[2:-1].tolist()

        importances = list(regressor.feature_importances_)
        feature_importances = [(feature, round(importance, 2)) for feature, importance in
                               zip(feature_list, importances)]
        feature_importances = sorted(feature_importances, key=lambda x: x[1], reverse=True)

        for feature in feature_importances:
                print("feature: {} = {}".format(feature[0], feature[1]))

        feat_plot = pd.DataFrame(data={"feature": feature_list,
                                       "importance": importances})
        fig2 = px.bar(feat_plot, x='feature', y='importance', color="importance")

        col7, col8 = st.columns(2)
        with col7:
                st.plotly_chart(fig)
                st.write('''Based on the scatterplot as shown, it sets a categorical value to the assigned X test values in accordance 
                to the y test and y predicted values. Hence, it can be seen that the y predicted value is closely in line with 
                the y test value for value 0 and 1 with a slight deviation for value 2 and 3.
                            ''')

        with col8:
                st.plotly_chart(fig2, use_container_width=True)
                st.write('''With reference to the feature importance, it shows the importance of the different features that the 
                model uses to decide the inflation rate(y predict).
                            ''')

        st.write("r2 score: " +  str(r2_score(y_test, y_pred)))

        prediction = st.container()
        with prediction:
                st.header("Inflation Calculator")
                income = st.number_input("Income Change %")
                employment = st.number_input("Employment Change %")
                resignation = st.number_input("Resignation Change %")
                recruitment = st.number_input("Recruitment Change %")
                retrenchment = st.number_input("Total Retrenchment")
                calculate = st.button("Calculate")
                if calculate:
                        inflation = regressor.predict([[income, employment, resignation, recruitment, retrenchment]])
                        st.write("Inflation rate of Singapore is : " + str(inflation))