import pandas as pd
import numpy as np

import streamlit as st
# import matplotlib.pyplot as plt
import plotly.express as px 
from plotly.subplots import make_subplots
import plotly.graph_objects as go


##################################
#           LOAD DATA            #
##################################
df = pd.read_csv('/Volumes/External/DSCI/624_Visualization/Final/raw/kaggle_survey_2021_responses.csv')
df = df.iloc[1:,1:]


##################################
#       SET UP PAGE CONFIG       #
##################################
st.set_page_config(
    page_title='Kagglers Survey 2021',
    page_icon=':bar_chart:',
    layout='wide')


##################################
#            SIDE BAR            #
##################################
st.sidebar.header('Filter Based on Following Criteria')

country = st.sidebar.selectbox(
    'Select the Country',
    options=np.sort(df.Q3.unique()),
    index = 64
)

education = st.sidebar.multiselect(
    'Select the level of education',
    options=df.Q4.unique(),
    default=df.Q4.unique()
)

gender = st.sidebar.multiselect(
    'Select a gender',
    options=df.Q2.unique(),
    default=df.Q2.unique()
)

    ## -- SET UP FILTER LOGIC -- ##

df_selection = df.query(
    'Q3==@country & Q4==@education & Q2==@gender'
)

##################################
#            MAIN PAGE           #
##################################
    ## -- SET UP PAGE TITLE -- ##
st.title('**Kagglers in Data Science Dashbaord**')
st.markdown('---')

    ## -- TOP KPI SECTION -- ##
kpi_left, kpi_right = st.columns([1,3])

with kpi_right:
    df['Q3'] = df['Q3'].str.replace(', Islamic Republic of...', '')
    map_df = pd.DataFrame()
    map_df['country'] = df['Q3'][1:].value_counts().index
    map_df['count'] = df['Q3'][1:].value_counts().values
    fig_map = px.choropleth(map_df, 
                            locations="country", 
                            locationmode='country names',
                            color="count",
                            color_continuous_scale='OrRd')
    fig_map.update_layout(
                        title = dict(text = "<b>Country Distribution of Kagglers</b>", x=0.5, xanchor='center'),
                        yaxis = {'linecolor': '#949494'})
    st.plotly_chart(fig_map, use_container_width=False)
    
with kpi_left:
    head_count = df.shape[0]
    man_count = df.Q2.value_counts().Man
    woman_count = df.Q2.value_counts().Woman
    other_count = (df.Q2.value_counts()['Prefer not to say'] +
                df.Q2.value_counts()['Nonbinary'] +
                df.Q2.value_counts()['Prefer to self-describe']
    )

    
    st.text(' ')
    st.markdown(f"**{head_count} in the Selected Country:**")
    st.text(' ')
    st.markdown('', unsafe_allow_html=True)
    st.markdown(f'**{man_count} Man**')
    st.markdown(f'**{int((man_count/head_count)*100)} %**')
    st.text(' ')
    st.markdown(f'**{woman_count} Woman**')
    st.markdown(f'**{int((woman_count/head_count)*100)} %**')
    st.text(' ')
    st.markdown(f'**{other_count} Other**')
    st.markdown(f'**{int((other_count/head_count)*100)} %**')

st.markdown('---')
    
    ## -- PLOT SECTION -- ##
# st.markdown('---')
st.markdown('## **Plots**')
st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
    unsafe_allow_html=True,
)
query_params = st.experimental_get_query_params()
tabs = ["Basic Information", "Professional Career", "Tech-Related"]

if "tab" in query_params:
    active_tab = query_params["tab"][0]
else:
    active_tab = "Basic Information"
if active_tab not in tabs:
    st.experimental_set_query_params(tab="Basic Information")
    active_tab = "Basic Information"

li_items = "".join(
    f"""
    <li class="nav-item">
        <a class="nav-link{' active' if t==active_tab else ''}" href="/?tab={t}">{t}</a>
    </li>
    """
    for t in tabs
)
tabs_html = f"""
    <ul class="nav nav-tabs">
    {li_items}
    </ul>
"""

st.markdown(tabs_html, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tab 1 -- Basic Info, place plots here

if active_tab == "Basic Information":
    
    st.markdown('''Kaggler's basic distribution including: the **age**, **level of education**, 
                **coding experience** and **salary** of the people to participated in the survey
                ''')
    
    tab1_col1, tab1_col2 = st.columns(2)
    with tab1_col1:
        # PLOT 1: AGE DISTRIBUTION ---
        CATEGORY_ORDER = ["18-21", "22-24", "25-29", 
                          "30-34", "35-39", "40-44", 
                          "45-49", "50-54", "55-59",
                          "60-69", "70+"]
        fig_age = go.Figure()
        fig_age.add_trace(go.Bar(x = df_selection.Q1.value_counts().index, 
                             y = df_selection.Q1.value_counts().values,
                             marker_color = 'firebrick'))
            # styling changes
        fig_age.update_layout(
                 title = {'text' : "Kaggler's Age Distribution", 'x':0.5, 'xanchor':'center'}, 
                 xaxis = dict(title = "Age", linecolor = "#949494",
                              categoryorder = "array", categoryarray = CATEGORY_ORDER), 
                 yaxis = dict(title = "Headcount", linecolor = "#949494"))
        # create 
        st.plotly_chart(
            fig_age, use_container_width=True
        )
        
        # PLOT 2: CODING EXPERIENCE ---
        # plot
        CODEXPR_ORDER = ['< 1 years', '1-3 years', '3-5 years', '5-10 years', '10-20 years', '20+ years', 'No Experience']
        fig_expr = go.Figure()
        fig_expr.add_trace(go.Bar(
            x = df_selection.Q6.replace({'I have never written code':'No Experience'}).value_counts().index,
            y = df_selection.Q6.replace({'I have never written code':'No Experience'}).value_counts().values,
            marker_color = 'firebrick'))
        # styling changes
        fig_expr.update_layout(
                 title = {'text' : "Coding Experience", 'x':0.5, 'xanchor':'center'},
                 xaxis = dict(title = "Coding Experience", linecolor = "#949494",
                              categoryorder = "array", categoryarray = CODEXPR_ORDER), 
                 yaxis = dict(title = "Headcount", linecolor = "#949494"))
        st.plotly_chart(fig_expr, use_container_width=True)
          
    with tab1_col2:
        # create the education distribution barchart
        fig_edu = go.Figure()
        fig_edu.add_trace(go.Bar(
        y = df_selection.Q4.replace({
                            'Some college/university study without earning a bachelor’s degree':'Some college',
                            'No formal education past high school':'High school'
                        }).value_counts().index,
        x = df_selection.Q4.replace({
                            'Some college/university study without earning a bachelor’s degree':'Some college',
                            'No formal education past high school':'High school'
                        }).value_counts().values, orientation='h',
        marker_color = 'firebrick'))
        EDU_ORDER = ["Professional doctorate", "Doctoral degree", "Master's degree", "Bachelar's degree", "Some college", "High school"]
            # styling changes
        fig_edu.update_layout(
                 title = {'text' : "Kaggler's Education Distribution", 'x':0.6, 'xanchor':'center'}, 
                 xaxis = dict(title = "Level of Education", linecolor = "#949494"), 
                 yaxis = dict(title = "Headcount", linecolor = "#949494",
                              categoryorder = "array", categoryarray = EDU_ORDER))
        st.plotly_chart(fig_edu, use_container_width=True)

        
       # SALARY BAR CHART
        df_selection.Q25 = df_selection.Q25.str.replace('$', '')
        SALARY_ORDER = ['>1,000,000', '500,000-999,999', '300,000-499,999', '250,000-299,999', '200,000-249,999',
                        '150,000-199,999', '125,000-149,999', '100,000-124,999','90,000-99,999','80,000-89,999',
                        '70,000-79,999','60,000-69,999','50,000-59,999','40,000-49,999','30,000-39,999','25,000-29,999',
                        '20,000-24,999', '15,000-19,999','10,000-14,999','7,500-9,999','7,500-9,999','5,000-7,499',
                        '4,000-4,999','3,000-3,999','2,000-2,999','1,000-1,999','0-999']
        fig_salary = go.Figure()
        fig_salary.add_trace(go.Bar(x = df_selection.Q25.value_counts().index,
                                    y = df_selection.Q25.value_counts().values,
                                    marker_color = 'firebrick'))
        # styling changes
        fig_salary.update_layout(
                        title = dict(text = "Salary Distribution", x = 0.5, xanchor = 'center'), 
                        xaxis = dict(title = "Salary Bins", linecolor = "#949494", 
                                    categoryorder = "array", categoryarray = SALARY_ORDER.reverse()), 
                        yaxis = dict(title = "Headcount", linecolor = "#949494")) 
        st.plotly_chart(fig_salary, use_container_width=True)
        

# Tab 2 -- Professional Career, place plots here  
elif active_tab == "Professional Career": 
    st.write("This page was created as a hacky demo of tabs")
    tab2_left, tab2_right = st.columns(2)
    
    with tab2_left:
        # ROLE distribution bar
        role = (
            df_selection.Q5
            .value_counts()
            .to_frame()
            .reset_index()
            .rename(columns={'index':'Role', 'Q5': 'Count'})
            .sort_values(by='Count', ascending=True)
        )
        role['percent'] = ((role['Count'] / role['Count'].sum())*100).round(2).astype(str) + '%'

        fig_role = go.Figure(go.Bar(
                    x=role['Count'],
                    y=role['Role'],
                    text=role['percent'],
                    orientation='h',
                    marker_color = 'lightseagreen'
                                ))

        fig_role.update_layout(
                        title = dict(text = "Role Distribution", x=0.5, xanchor='center'),
                        yaxis = {'linecolor': '#949494'})
                        

        st.plotly_chart(fig_role, use_container_width=True)
        
        # INDISTRY distribution bar
        industry = (
            df_selection['Q20']
            .value_counts()
            .to_frame()
            .reset_index()
            .rename(columns={'index':'Industry', 'Q20':'Count'})
            .sort_values(by=['Count'], ascending=True)   
                ) 
        industry['percent'] = ((industry['Count'] / industry['Count'].sum())*100).round(2).astype(str) + '%'

        fig_ind = go.Figure(go.Bar(
                    x=industry['Count'],
                    y=industry['Industry'],
                    text=industry['percent'],
                    orientation='h',
                    cliponaxis = False,
                    marker_color = 'lightseagreen'
                                ))
        fig_ind.update_layout(
                        title = dict(text = "Industry Distribution", x=0.5, xanchor='center'),
                        yaxis = {'linecolor': '#949494'})
        
        st.plotly_chart(fig_ind, use_container_width=True)
              
    with tab2_right:
        # BAR COMPANY SIZE
        comp_size = (
            df['Q21']
            .value_counts()
            .to_frame()
            .reset_index()
            .rename(columns={'index':'Company Size', 'Q21':'Count'})
            .sort_values(by=['Count'], ascending=True)   
                )
        comp_size['percent'] = ((comp_size['Count'] / comp_size['Count'].sum())*100).round(2).astype(str) + '%'
        fig_comps = go.Figure(go.Bar(
                    x=comp_size['Count'],
                    y=comp_size['Company Size'],
                    text=comp_size['percent'],
                    orientation='h',
                    cliponaxis = False,
                    marker_color = 'lightseagreen'
                                ))
        fig_comps.update_layout(
                        title = dict(text = "Company Size", x=0.5, xanchor='center'),
                        yaxis = {'linecolor': '#949494'})
        st.plotly_chart(fig_comps,use_container_width=True)
        
        # BAR TEAM SIZE
        team_size = (
            df_selection['Q22']
            .value_counts()
            .to_frame()
            .reset_index()
            .rename(columns={'index':'Team Size', 'Q22':'Count'})
            .sort_values(by=['Count'], ascending=True)   
                )
        team_size['percent'] = ((team_size['Count'] / team_size['Count'].sum())*100).round(2).astype(str) + '%'
        TEAM_ORDER = ['0', '1-2', '3-4', '5-9', '10-14', '15-19', '20+']

        fig_team = go.Figure(go.Bar(
                    y=team_size['Count'],
                    x=team_size['Team Size'],
                    text=team_size['percent'],
                    cliponaxis = False,
                    marker_color = 'lightseagreen'
                                ))

        fig_team.update_layout( 
                        title = dict(text = "Team Size", x=0.5, xanchor='center'),
                        xaxis = dict(categoryorder = "array", categoryarray = TEAM_ORDER, linecolor = '#949494'))
        
        st.plotly_chart(fig_team, use_container_width=True)


# Tab 3 -- Tech-related, place plots here   
elif active_tab == "Tech-Related":
    st.write("If you'd like to Tech-Related me, then please don't.")
    tab3_left, tab3_right = st.columns(2)
    
    with tab3_left:
        # PLOT LANGUAGE
        languages_cols = [col for col in df_selection if col.startswith('Q7')]
        lang_df = df_selection[languages_cols]
        lang_df.columns = ['Python', 'R', 'SQL', 'C', 'C++', 'Java', 
                            'Javascript', 'Julia', 'Swift', 'Bash',
                            'MATLAB', 'None', 'Other']
        lang_df = (
            lang_df
            .count()
            .to_frame()
            .reset_index()
            .rename(columns={'index':'Language', 0:'Count'})
            .sort_values(by='Count', ascending=True)
        )

        lang_df['percent'] = ((lang_df['Count'] / len(df_selection))*100).round(2).astype(str) + '%'

        fig_lang = go.Figure(go.Bar(
                    x=lang_df['Count'],
                    y=lang_df['Language'],
                    text=lang_df['percent'],
                    orientation='h'
                                ))
        fig_lang.update_layout(
                        title = dict(text = "Most Commonly Used Programming Language ", x=0.5, xanchor='center'),
                        yaxis = {'linecolor':'#949494'})
        st.plotly_chart(fig_lang, use_container_width=True)
        
        # PLOT OTHER PLACE HOLDER FOR STUDY RESOURCE
        courses_cols = [col for col in df_selection if col.startswith('Q40')]
        courses = df_selection[courses_cols]
        courses.columns = ['Coursera', 'edX', 
                        'Kaggle Learn Courses', 'DataCamp', 'Fast.ai', 
                        'Udacity', 'Udemy', 'LinkedIn Learning',
                        'Cloud-certification programs', 'University Courses', 'None', 'Other']
                            
        courses = (
            courses
            .count()
            .to_frame()
            .reset_index()
            .rename(columns={'index':'Courses', 0:'Count'})
            .sort_values(by=['Count'], ascending=False)
            )

        fig_cours = go.Figure(go.Treemap(
            labels = courses['Courses'],
            values = courses['Count'],
            parents = ['']*courses.shape[0],
            textinfo = "percent root+label+value+text",
        ))
        fig_cours.update_layout(plot_bgcolor = "white",
                        title = dict(text = "Most Commonly Used Course Platforms", x=0.5, xanchor='center'))
 
        st.plotly_chart(fig_cours, use_container_width=True)
        
        
    with tab3_right:
        # IDE
        ide_cols = [col for col in df_selection if col.startswith('Q9')]
        ide_df = df_selection[ide_cols]
        ide_df.columns = ['JupyterLab', 'RStudio', 'Visual Studio', 'VSCode', 
                        'PyCharm', 'Spyder', 'Notepad++', 'Sublime Text', 'Vim, Emacs, or similar', 
                        'MATLAB', 'Jupyter Notebook', 'None', 'Other']
        ide_df = (
            ide_df
            .count()
            .to_frame()
            .reset_index()
            .rename(columns={'index':'IDE', 0:'Count'})
            .sort_values(by='Count', ascending=True)
        )

        ide_df['percent'] = ((ide_df['Count'] / len(df_selection))*100).round(2).astype(str) + '%'

        fig_ide = go.Figure(go.Bar(
                    x=ide_df['Count'],
                    y=ide_df['IDE'],
                    text=ide_df['percent'],
                    orientation='h'
                                ))
        fig_ide.update_layout(
                        title = dict(text = "Most Commonly Used IDE", x=0.5, xanchor='center'),
                        yaxis = {'linecolor': '#949494'})
        st.plotly_chart(fig_ide, use_container_width=True)
        
        # PLOT COMPUTING PLATFORM
        platform = (
            df_selection['Q11']
                .value_counts()
                .to_frame()
                .reset_index()
                .rename(columns={'index':'Platform', 'Q11':'Count'})
                .sort_values(by=['Count'], ascending=False)   
                .replace(['A deep learning workstation (NVIDIA GTX, LambdaLabs, etc)',
                        'A cloud computing platform (AWS, Azure, GCP, hosted notebooks, etc)'], 
                        ['A deep learning workstation', 'A cloud computing platform'])
                    )
        platform['percent'] = ((platform['Count'] / platform['Count'].sum())*100).round(2).astype(str) + '%'
        platform = (platform
           .sort_values(by = ['Count'])
           .iloc[0:15]
           .reset_index())
        
        colors = ['#033351',] * 6
        colors[5] = '#5abbf9'
        colors[4] = '#0779c3'
        colors[3] = '#0779c3'

        fig_plat = go.Figure(go.Scatter(x = platform['Count'], 
                                y = platform["Platform"],
                                text = platform['percent'],
                                mode = 'markers',
                                marker_color =colors,
                                marker_size  = 12))

        for i in range(0, len(platform)):
                    fig_plat.add_shape(type='line',
                                    x0 = 0, y0 = i,
                                    x1 = platform["Count"][i],
                                    y1 = i,
                                    line=dict(color=colors[i], width = 4))
        fig_plat.update_layout(
            # plot_bgcolor = "white",
            title = dict(text = "Most Commonly Used Comupting Platform", x=0.5, xanchor='center')
        )
        st.plotly_chart(fig_plat, use_container_width=True)
    

else:
    st.error("Something has gone terribly wrong.")














