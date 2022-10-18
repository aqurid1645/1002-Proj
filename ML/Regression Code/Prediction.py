import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import shap
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import streamlit as st

dataset = pd.read_csv('combined1.csv')
X = dataset.iloc[:, 2:-1].values
y = dataset.iloc[:, -1].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.15, random_state = 0)

from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 100, random_state = 0)
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)

from sklearn.metrics import r2_score
r2_score(y_test, y_pred)

from sklearn.metrics import mean_squared_error
mean_squared_error(y_test, y_pred, squared = False)

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



