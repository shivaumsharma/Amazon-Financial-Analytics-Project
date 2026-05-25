import streamlit as st
import pandas as pd 
from preprocessing import (load_data,create_yoy_growth)
from kpi_engine import (operating_margin)
from forecasting import (forecast_revenue)
from pathlib import Path
import plotly.express as px

BASE_DIR=Path(__file__).resolve().parent.parent
 
df=load_data(BASE_DIR/"data"/"Amazon_raw_data.xlsx")
df=create_yoy_growth(df)
df=operating_margin(df)
st.set_page_config(page_title="Amazon Financial Intelligence",layout="wide")
st.title("Amazon Financial Intelligence Dashboard")

st.sidebar.markdown("## About")
st.sidebar.info(
    "Financial intelligence dashboard for Amazon featuring KPI analytics, forecasting, anomaly detection, and executive insights."
)
st.sidebar.header("Dashboard Filters")
selected_years=st.sidebar.multiselect("Select Years",options=df["Year"].unique(),default=df["Year"].unique())
filtered_df=df[df["Year"].isin(selected_years)]



#KPI Section

total_revenue=(filtered_df["Total_Revenue"].sum())
net_income=(filtered_df["Net_Income"].sum())
operating_income=(filtered_df["Operating_Income"].sum())

col1,col2,col3=st.columns(3)

col1.metric("5-Year Revenue",f"${total_revenue:.2f}B")
col2.metric("5-Year Net Income",f"${net_income:.2f}B")
col3.metric("5-Year Operating Income",f"${operating_income:.2f}B")

st.subheader("Financial Dataset")
st.dataframe(df)

st.subheader("Financial Dataset with Filter")
st.dataframe(filtered_df)

st.subheader("Revenue Trend Analysis")
fig=px.line(filtered_df,x="Year",y="Total_Revenue",markers=True,title="Amazon Revenue Growth")
fig.update_xaxes(dtick=1)
fig.update_xaxes(type='category')
st.plotly_chart(fig,use_container_width=True)


st.subheader("AWS Contribution Analysis")
fig=px.line(filtered_df,x="Year",y=["Total_Revenue","AWS_Revenue"],markers=True,title="Amazon AWS Contribution")
fig.update_xaxes(dtick=1)
fig.update_xaxes(type='category')
st.plotly_chart(fig,use_container_width=True)

st.subheader("Operating Margin Trend")
fig=px.line(filtered_df,x="Year",y="Operating_Margin",markers=True,title="Amazon Margins")
fig.update_xaxes(dtick=1)
fig.update_xaxes(type='category')
st.plotly_chart(fig,use_container_width=True)


forecast_df,future_years,predictions,model=(forecast_revenue(df))

st.subheader("Executive Insights")
revenue_growth=((filtered_df["Total_Revenue"].iloc[-1]-filtered_df["Total_Revenue"].iloc[0])/filtered_df["Total_Revenue"].iloc[0])*100
cloud_growth=((filtered_df["AWS_Revenue"].iloc[-1]-filtered_df["AWS_Revenue"].iloc[0])/filtered_df["Total_Revenue"].iloc[0])*100
margin_change=((filtered_df["Operating_Margin"].iloc[-1]-filtered_df["Operating_Margin"].iloc[0])/filtered_df["Operating_Margin"].iloc[0])

st.success(f"Revenue grew by {revenue_growth:.2f}% over the selected period.")
st.success(f"Cloud Revenue grew by {cloud_growth:.2f}% over the selected period.")
st.success(f"Operating Margin changed by {margin_change:.2f}% over the selected period.")

st.subheader("Revenue Forecast")
st.dataframe(forecast_df)

forecast_plot_df=forecast_df.copy()

fig_forecast=px.line(forecast_plot_df,x="Year",y="Predicted_Revenue",markers=True,title="Future Revenue Forecast")
fig_forecast.update_xaxes(type='category')
st.plotly_chart(fig_forecast,use_container_width=True)

forecast_plot_df = pd.concat([
    df[["Year", "Total_Revenue"]].rename(columns={"Total_Revenue":"Revenue"}),
    forecast_df.rename(columns={"Predicted_Revenue":"Revenue"})
])