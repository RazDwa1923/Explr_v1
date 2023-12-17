#%%

#%% md
# # Creating DeFi Explorer
# 
# ##### The DeFi explorer is an online tool that helps DeFi investors to view possible stablecoin pools leveraging the Streamlit package to create a data app. The tool will specifically showcase the SoDeFi pool scoring mechanism
# 
# **_Objective_**: Create a data app that allows users to view possible stablecoin pools
# 
# **_Methodology_**: The app will be based on data created by the SoDeFi pool scoring mechanism. The data will be stored in a csv file and will be read into the app using the pandas package. The app will be created using the streamlit package.
# 
# **_Hosting_**: The app will be hosted on Heroku and integrated into the SoDeFi website
#%%
import streamlit as st
import pandas as pd

#creating a dataframe bringing the Pool data from a csv file
data = pd.read_csv("/Users/karolk/Python_Work/Data_Sets/Pool_Standings/pool_league_stable.csv", index_col=0)
pd.options.display.float_format = '{:,.2f}'.format

#Modifyinng the dataframe to include a smaller set of columns. The columns are: chain, project, symbol, tvlUsd, tvlChange1d, apy, payment, SD_score, SD_Score_7D
data = data[['chain', 'project', 'symbol', 'tvlUsd', 'tvlChange1d', 'tvlChange7d', 'apy', 'apyMean7d', 'apyStd7d' , 'apy7DStdRatio','SD_Score', 'SD_Score_7D_avg']]
#%%
#modifying the columns names to be more user-friendly
data.columns = ['Chain', 'Project', 'Token', 'TVL (USD in Millions)', 'TVL Change 1D (%)', 'TVL Change 7D (%)', 'APY (%)', 'APY 7D Average (%)', 'APY Std Deviation 7D (%)', 'SoDeFi Risk/Reward Ratio', 'SoDeFi Score', 'SoDeFi Score 7D Avg']

#changing the TVL into millions by dividing the TVL by 1000000
data['TVL (USD in Millions)'] = data['TVL (USD in Millions)']/1000000

#change the SoDeFi Risk Reward ration to 0 where the APY Std Deviation 7D is 0
data.loc[data['APY Std Deviation 7D (%)'] == 0, 'SoDeFi Risk/Reward Ratio'] = 0

#exclude all pools with TVL less than 500 thousand
data = data[data['TVL (USD in Millions)'] > 0.500]

#sort data by soDeFi Score
data = data.sort_values(by=['SoDeFi Score'], ascending=False)
#%%
#create a varable for today's date
today = pd.to_datetime('today').strftime('%Y-%m-%d')

#create a text which says 'SoDeFi Pool Explorer updated as of [today's date]'
date_text = 'SoDeFi Pool Explorer updated as of ' + today

#%%
#Write the dataframe to the app. The app should be a dataframe table with the columns above and the data below. The table should be sortable using Streamlit.

#configure the page

st.set_page_config(
    page_title="SoDeFi Pool Explorer",
    page_icon=":shark:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
    }
)

#write stream lit header
st.title("SoDeFi Pool Explorer")
st.header("Data Inspired DeFi Investment")
st.subheader("SoDeFi Pool Explorer is designed to sort through the ")
st.text('Methodology: SoDeFi Pool Scoring Mechanism')
st.text(date_text)

#write the dataframe to the app
st.dataframe(data, hide_index=True, use_container_width=True,
             column_config={'Chain': st.column_config.TextColumn(help="medium", width='medium'),
                            'Project': st.column_config.TextColumn(help="medium", width='medium'),
                            'Token': st.column_config.TextColumn(help="jjs", width='medium'),
                            'TVL (USD in Millions)': st.column_config.NumberColumn(format="$ %.1f", help="small", width='medium'),
                            'TVL Change 1D (%)': st.column_config.NumberColumn(format="%.2f", help="small", width='medium'),
                            'TVL Change 7D (%)': st.column_config.NumberColumn(format="%.2f", help="small", width='medium'),
                            'APY (%)': st.column_config.NumberColumn(format="%.1f", help="small", width='medium'),
                            'APY 7D Average (%)': st.column_config.NumberColumn(format="%.1f", help="small", width='medium'),
                            'APY Std Deviation 7D (%)': st.column_config.NumberColumn(format="%.1f", help='medium', width='medium'),
                            'SoDeFi Risk/Reward Ratio': st.column_config.NumberColumn(format="%.1f", help="small", width='medium'),
                            'SoDeFi Score': st.column_config.NumberColumn(format="%.1f", help="small", width='medium'),
                            'SoDeFi Score 7D Avg': st.column_config.NumberColumn(format="%.1f", help="small", width='medium')},
             column_order=( 'SoDeFi Score','Chain','Project',
                            'Token', 'TVL (USD in Millions)', 'APY (%)',
                            'TVL Change 1D (%)', 'TVL Change 7D (%)',
                            'APY 7D Average (%)', 'APY Std Deviation 7D (%)',
                            'SoDeFi Risk/Reward Ratio',))

st.text("Data Source: DeFiLlama API")

