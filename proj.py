import pandas as pd
import streamlit as st
import plotly.express as px

# Titles
st.title('Recruitment and Resignation Rate Charts')

# Data tables
rate = ['Services', 'Manufacturing',
      'Accommodation And Food Services',
      'Wholesale And Retail Trade',
      'Transportation And Storage',
      'Information And Communications',
      'Financial And Insurance Services',
      'Real Estate Services', 'Professional Services',
      'Administrative And Support Services',
      'Community, Social And Personal Services', 'Others',
      'Professionals, Managers, Executives & Technicians',
      'Clerical, Sales & Service Workers',
      'Production & Transport Operators, Cleaners & Labourers']

# Tabs to display
tab1, tab2 = st.tabs(['Recruitment Rate', 'Resignation Rate'])

# Download box of CSV files
def convert_df(df):
    return df.to_csv().encode('utf-8')

# Recruitment Rate
with tab1:
    # Data Tables
    rec = pd.read_csv('recruitment rate.csv')
    st.subheader('Recruitment Rate Table')
    st.dataframe(rec)

    # slider filter
    years = st.select_slider(
        'Select year range',
        options = rec['Years'],
        value = (min(rec['Years']), max(rec['Years']))
    )

    # Filters based on industries and presets
    filt = st.multiselect('Select the industry', rate, [
        'Real Estate Services',
        'Information And Communications',
        'Transportation And Storage',
        'Accommodation And Food Services',
        'Administrative And Support Services'
        ])

    # Graphs and labels
    rec_graph = px.line(rec, x=years, y=filt)
    rec_graph.update_layout(
        title='Recruitment Rate',
        yaxis_title='Rate (%)',
        legend_title='Industry',
    )
    st.plotly_chart(rec_graph, use_container_width=True)

    # Download box
    csv = convert_df(rec)
    st.download_button(
        label="Download Recruitment Rate as CSV",
        data=csv,
        file_name='recruitment rate.csv',
        mime='text/csv'
    )

# Resignation Rate
with tab2:
    # Data Tables
    res = pd.read_csv('resignation rate.csv')
    st.subheader('Resignation Rate Table')
    st.dataframe(res)

    # Filters based on industries and presets
    filt = st.multiselect('Select the industry', rate, [
        'Accommodation And Food Services',
        'Real Estate Services',
        'Information And Communications',
        'Transportation And Storage',
        'Administrative And Support Services'])

    # Graphs and labels
    res_graph = px.line(res, x='Years', y=filt)
    res_graph.update_layout(
        title='Resignation Rate',
        yaxis_title='Rate (%)',
        legend_title='Industry',
    )
    st.plotly_chart(res_graph, use_container_width=True)

    #Download box
    csv=convert_df(res)
    st.download_button(
        label="Download Resignation Rate as CSV",
        data=csv,
        file_name='resignation rate.csv',
        mime='text/csv'
    )