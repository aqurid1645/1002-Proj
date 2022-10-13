import pandas as pd
import streamlit as st
import plotly.express as px

# Titles
st.set_page_config(layout="wide")
st.title('Recruitment and Resignation Rate Charts')


# Data tables
rate = ['Years', 'Services', 'Manufacturing',
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
    rec = pd.read_csv('recruitment rate.csv')

    # slider filter
    start = 2017
    end = 2021
    start_year, end_year = st.select_slider('Select the years to view', options=list(range(start, end+1)), value = (start, end), key='1')
    st.write('You selected the year range of', start_year, 'and', end_year)

    # Filters based on industries and presets
    filt = st.multiselect('Select the industry', rate, [
        'Years',
        'Real Estate Services',
        'Information And Communications',
        'Transportation And Storage',
        'Accommodation And Food Services',
        'Administrative And Support Services'
        ])

    # Display dataframe
    st.subheader('Recruitment Rate')
    rec = rec[(rec.Years >= start_year) & (rec.Years <= end_year)]
    st.dataframe(rec[filt], use_container_width=True)

    # Download box
    csv = convert_df(rec)
    option = st.selectbox(
        'Raw or Custom:',
        ('Raw', 'Custom'), key='3')

    if option == 'Custom':
        st.download_button(
        label="Download Recruitment Rate as custom CSV",
        data=rec[filt].to_csv(),
        file_name='recruitment rate.csv'
    )
    elif option == 'Raw':
        st.download_button(
        label="Download Recruitment Rate as raw CSV",
        data=rec.to_csv(),
        file_name='recruitment rate.csv'
    )

    # Graphs and labels
    rec_graph = px.line(rec, x='Years', y=filt)
    rec_graph.update_layout(
        title='Recruitment Rate',
        xaxis_title='Years',
        yaxis_title='Rate (%)',
        legend_title='Industry',
    )
    st.plotly_chart(rec_graph, use_container_width=True)

    # Analysis
    st.write('''In 2020, there is a decrement in Recruitment Rate from most industries
             due to the companies' financial instability to hire new employees.
             However, industries such as Information and Communications has been constant throughout the years with a sharp increment
             in 2021. Possible factors could include that ICT is more widely used to work from
             home, E learning for students, as well as to socially communicate with people.''')

# Resignation Rate
with tab2:
    # Data Tables
    res = pd.read_csv('resignation rate.csv')

    # slider filter
    min_year = 2017
    max_year = 2021
    starting, ending = st.select_slider('Select the years to view', options=list(range(min_year, max_year + 1)), value=(min_year, max_year), key='2')
    st.write('You selected the year range of', starting, 'and', ending)

    # Filters based on industries and presets
    filt = st.multiselect('Select the industry', rate, [
        'Years',
        'Accommodation And Food Services',
        'Real Estate Services',
        'Information And Communications',
        'Transportation And Storage',
        'Administrative And Support Services'])

    # Display dataframe
    res = res[(res.Years >= starting) & (res.Years <= ending)]
    st.subheader('Resignation Rate')
    st.dataframe(res[filt], use_container_width=True)

    # Download box
    csv = convert_df(rec)
    option = st.selectbox(
        'Raw or Custom:',
        ('Raw', 'Custom'),key='4')

    if option == 'Custom':
        st.download_button(
        label="Download Resignation Rate as custom CSV",
        data=res[filt].to_csv(),
        file_name='resignation rate.csv')

    elif option == 'Raw':
        st.download_button(
        label="Download Resignation Rate as raw CSV",
        data=res.to_csv(),
        file_name='resignation rate.csv'
    )


    # Graphs and labels
    res_graph = px.line(res, x='Years', y=filt)
    res_graph.update_layout(
        title='Resignation Rate',
        yaxis_title='Rate (%)',
        legend_title='Industry',
    )
    st.plotly_chart(res_graph, use_container_width=True)

    # Analysis
    st.write('''In 2020, most industries suffered a decline in their resignation rate due to the COVID-19 pandemic. 
             While the number of COVID-19 cases increased,
             the accommodations and food services industry grew as the demand for space increased during Singapore’s Circuit Breaker.
             A possible factor may include employees suffering from a burnout as they do not have much time to rest for themselves.''')

