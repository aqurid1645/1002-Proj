# If streamlit not present
# pip install streamlit
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

import matplotlib
matplotlib.use('Agg')

import streamlit as st
st.set_page_config(layout="wide")

# Title and Sidebar informationS
st.markdown('# EMPLOYMENT 💼')
tab1, tab2, tab3 = st.tabs(['Employment Change', 'Employment By Gender and Education',
                    'Labour Force Status By Age Group'])
#explore = st.radio("Data Filters", ("Employment Data", "Quick Look", "Columns"))

# Employment Change
with tab1:
    file = "Datasets/Employment/mrsd_39_annual_ emp_chng_by_ind_and_res_stat_29072022"
    #file = "Datasets/Employment/mrsd_39_annual_ emp_chng_by_ind_and_res_stat_29072022"
    explore = st.radio("Data Filters", ("Employment Data", "Quick Look", "Columns"),key='11')

    # Reading and renaming of files for visualization
    original = pd.read_csv(file + ".csv").replace("-", 0)
    df = original
    columns = original.columns.values

    if explore == 'Employment Data':
        # Year slidebar to choose year range
        start = 2017
        end = 2021
        start_year, end_year = st.select_slider('Select the years to view',
                                                options=list(range(start, end + 1)), value=(start, end), key='1')

        # Selecting Of Columns For Display
        columns_select = st.multiselect("Select The Columns To View",
                                        columns, default=columns, key='2')
        original_new = original[(original.year >= start_year) & (original.year <= end_year)]
        st.subheader("Employment Data")
        st.dataframe(original_new[columns_select], use_container_width=True)

    elif explore == "Quick Look":
        st.subheader('Dataset Quick Look:')
        st.dataframe(original.head())

    elif explore == 'Columns':
        st.subheader('Show Columns List')
        st.write(original.columns.to_list())

    # Download box
    option = st.selectbox("Raw or Custom",
                          ("Raw", "Custom"), key='3')
    if option == "Custom":
        st.download_button(
            label="Download Customised Columns Data",
            data=original_new[columns_select].to_csv(), file_name="Employment change_custom.csv")
    else:
        st.download_button(label="Download Raw Data",
                           data=original.to_csv(), file_name="Employment change.csv")

    # Graph
    st.subheader("Employment change Sunburst From 2017 To 2021")
    df = df[df.year >= 2017]
    df["employment_change"] = df["employment_change"].astype(float)
    fig = px.sunburst(df, path=['year', "res_stat", 'industry1', "employment_change"],
                      color="employment_change", color_continuous_scale='RdBu')

    st.plotly_chart(fig)

    # Analysis
    st.write("""From the Sunburst graph that is shown, it is clear that during the year of 2020 when the pandemic was at its peak,
there was a plunge in the employment status in the services industry. This could mainly be due to the lock down that Singapore was going through. 
On top of that, many brick and mortar stores were struggling to make ends meet. It was also clear that most of the non-residents were worst off,
as many of them were forced to go back to their respective countries due to the inability of companies extending their employment passes.

However, in 2021 when the pandemic was subsiding, there was an exponential increment in the service industry. 
The main reason for this could be that Singapore was transitioning back to it status quo and these businesses required to re-employ employees. 
On top of that, the Singapore government was also granting many businesses grants and waivers to cushion the financial impact.""")

# Employment By Gender and Education
with tab2:
    file = "Datasets/Employment/employed_15_sex_edu_age_yr"
    explore = st.radio("Data Filters", ("Employment Data", "Quick Look", "Columns"), key='12')

    # Reading and renaming of files for visualization
    original = pd.read_csv(file + ".csv").replace("-", 0)
    df = original
    columns = original.columns.values

    if explore == 'Employment Data':
        # Year slidebar to choose year range
        start = 2017
        end = 2021
        start_year, end_year = st.select_slider('Select the years to view',
                                                options=list(range(start, end + 1)), value=(start, end),key='4')

        # Selecting Of Columns For Display
        columns_select = st.multiselect("Select The Columns To View",
                                        columns, default=columns, key='5')
        original_new = original[(original.year >= start_year) & (original.year <= end_year)]
        st.subheader("Employment Data")
        st.dataframe(original_new[columns_select], use_container_width=True)

    elif explore == "Quick Look":
        st.subheader('Dataset Quick Look:')
        st.dataframe(original.head())

    elif explore == 'Columns':
        st.subheader('Show Columns List')
        st.write(original.columns.to_list())

    # Download box
    option = st.selectbox("Raw or Custom",
                          ("Raw", "Custom"), key='6')
    if option == "Custom":
        st.download_button(
            label="Download Customised Columns Data",
            data=original_new[columns_select].to_csv(), file_name="Employment By Gender and Education_custom.csv")
    else:
        st.download_button(label="Download Raw Data",
                           data=original.to_csv(), file_name="Employment By Gender and Education.csv")

    # Graph
    st.subheader('Employment By Gender and Education Barplot From 2017 To 2021')
    df = original_new
    df.employed = pd.to_numeric(df.employed)
    df = df[(df.year >= 2017) & (df.age != "15-19")]
    df = df.groupby(["year", "edu_1"]).sum()
    df = df.reset_index()

    f1 = df[df['year'] == 2017]
    f2 = df[df['year'] == 2018]
    f3 = df[df['year'] == 2019]
    f4 = df[df['year'] == 2020]
    f5 = df[df['year'] == 2021]

    edu = df['edu_1'].unique().tolist()

    fig = go.Figure()
    colors = px.colors.qualitative.T10[0:5]

    fig.add_trace(go.Bar(x=edu, y=f1['employed'], name="2017", marker_color=colors[0]))
    fig.add_trace(go.Bar(x=edu, y=f2['employed'], name="2018", marker_color=colors[1]))
    fig.add_trace(go.Bar(x=edu, y=f3['employed'], name="2019", marker_color=colors[2]))
    fig.add_trace(go.Bar(x=edu, y=f4['employed'], name="2020", marker_color=colors[3]))
    fig.add_trace(go.Bar(x=edu, y=f5['employed'], name="2021", marker_color=colors[4]))
    st.plotly_chart(fig)

    # Analysis
    st.write("""From the barplot as shown, there is a clear distinction that during the pandemic, employment of Degree holders increased as opposed to the expectation.
    On the contrary, the people that had Diplomas and below saw a slight drop in employment. This is without a doubt, as the world was in a biological warfare with Covid-19.""")

# Labour Force Status by Age group
with tab3:
    file = "Datasets/Employment/pop_1_labourforce_status_age_yr"
    explore = st.radio("Data Filters", ("Employment Data", "Quick Look", "Columns"), key='13')

    # Reading and renaming of files for visualization
    original = pd.read_csv(file + ".csv").replace("-", 0)
    df = original
    columns = original.columns.values

    if explore == 'Employment Data':
        # Year slidebar to choose year range
        start = 2017
        end = 2021
        start_year, end_year = st.select_slider('Select the years to view',
                                                options=list(range(start, end + 1)), value=(start, end), key='7')

        # Selecting Of Columns For Display
        columns_select = st.multiselect("Select The Columns To View",
                                        columns, default=columns, key='8')
        original_new = original[(original.year >= start_year) & (original.year <= end_year)]
        st.subheader("Employment Data")
        st.dataframe(original_new[columns_select], use_container_width=True)

    elif explore == "Quick Look":
        st.subheader('Dataset Quick Look:')
        st.dataframe(original.head())

    elif explore == 'Columns':
        st.subheader('Show Columns List')
        st.write(original.columns.to_list())

    # Download box
    option = st.selectbox("Raw or Custom",
                          ("Raw", "Custom"), key='9')
    if option == "Custom":
        st.download_button(
            label="Download Customised Columns Data",
            data=original_new[columns_select].to_csv(), file_name="Labour Force Status by Age group_custom.csv")
    else:
        st.download_button(label="Download Raw Data",
                           data=original.to_csv(), file_name="Labour Force Status by Age group.csv")

    # Graph
    st.subheader("Labour Force Status By Age Group Piechart From 2017 To 2021")

    labels = ["20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64"]

    # Create subplots: use 'domain' type for Pie subplot
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=df["employed"][df.year == 2019], name="2019"),
                  1, 1)
    fig.add_trace(go.Pie(labels=labels, values=df["employed"][df.year == 2020], name="2020"),
                  1, 2)

    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    fig.update_layout(
        title_text="Age Group Of Employed People In The Labour Force",
        # Add annotations in the center of the donut pies.
        annotations=[dict(text='2019', x=0.175, y=0.5, font_size=20, showarrow=False),
                     dict(text='2020', x=0.825, y=0.5, font_size=20, showarrow=False)])
    st.plotly_chart(fig)

    # Analysis
    st.write("""Based on the 2 piechart shown, it is of a comparison between 2019 and 2020. The piechart shows the age groups that make up of Singapore’s labour force.
    Prior to the pandemic, it can be seen that the 45 to 49 age group were the 2nd highest in Singaopore’s labour force. However, during the pandemic, this group dropped to become the 3rd highest. 
    Instead the 40-44 age group became the 2nd highest. This could be due to employees hiring younger employees as the rate of recovery from Covid was higher as compared to older employees.""")