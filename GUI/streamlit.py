import streamlit as st
import cufflinks as cf
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
cf.go_offline()
st.set_page_config(layout="wide")
st.write("""
# COVID-19 analyzer
This tool analyzes the **impacts of COVID-19**
""")

summary = st.container()
with summary:
            st.header("Singapore at a glance as of 2022")
            # I created 2 rows of 3 columns but u all might want to do 3 rows of 2 columns instead
            # 3 columns means the wordings per columns will be shorter
            # So u all decided based on the situation ba
            col1, col2, col3 = st.columns(3)
            col4, col5, col6 = st.columns(3)
            col1.metric("Population", "5,637,022", "3.36%")
            col2.metric("Labour Force Participation Rate", "70.5%", "2.4%")
            col3.metric("Retrenchment?", "12345", "12%")
            col4.metric("Income?", "543231", "34%")
            col5.metric("Inflation?", "123321", "56%")
            col6.metric("Idk what else", "123698745", "-78%")
            st.video('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

