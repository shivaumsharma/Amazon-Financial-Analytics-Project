import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import seaborn as sns
from sklearn.linear_model import LinearRegression

df=pd.read_excel("amazon_raw_data.xlsx")

print(df.head())
print(df.describe())

#Revenue Trend
plt.figure(figsize=(10,6))
plt.plot(df["Year"],df["Total_Revenue"],marker="o")
plt.title("Amazon revenue Trend")
plt.xlabel("Year")
plt.ylabel("Revenue($bn)")
plt.grid(True)
plt.savefig("charts/revenue_trend.png")
plt.close()

#Net income trend

plt.figure(figsize=(10,6))
plt.plot(df["Year"],df["Net_Income"],marker='o',linewidth=2,label="Net income %")
plt.grid(True)
plt.title("Amazon Net Income Trend")
plt.xlabel("Year")
plt.ylabel("Net_Income($bn)")
plt.savefig("charts/Net_income.png")
plt.close()


#Aws vs Total revenue

plt.figure(figsize=(10,6))
plt.plot(df["Year"],df["Total_Revenue"],marker="o",label="Total Revenue")
plt.plot(df["Year"],df["AWS_Revenue"],marker="o",label="AWS Revenue")
plt.title("AWS VS TOTAL REVENUE")
plt.xlabel("Year")
plt.ylabel("Revenue")
plt.legend()
plt.grid(True)
plt.savefig("charts/AWSvsRevenue.png")
plt.close()


#Operating Margin %

operating_margin=df["Operating_Income"]/df["Total_Revenue"]*100

plt.figure(figsize=(10,6))
plt.plot(df["Year"],operating_margin,marker="o",label="Operating Margin %")
plt.xlabel("Year")
plt.legend()
plt.grid(True)
plt.title("Operating Margin Percentages")
plt.ylabel("Operating Margin")
plt.savefig("charts/Operating_margin.png")
plt.close()


#Yoy Revenue Growth

df["Yoy_growth"]=df["Total_Revenue"].pct_change()*100

plt.figure(figsize=(10,6))
plt.plot(df["Year"],df["Yoy_growth"],marker='o',linewidth=2,label="YoY Growth %")
plt.title("Year On Year Growth")
plt.xlabel("Year")
plt.ylabel("YoY Growth")
plt.grid(True)
plt.legend()
plt.savefig("charts/YOY_growth.png")
plt.close()


X=df[["Year"]]
Y=df["Total_Revenue"]

model=LinearRegression()
model.fit(X,Y)

future_years=pd.DataFrame({
  "Year":[2025,2026,2027]
})

predictions=model.predict(future_years)

forecast_df=future_years.copy()
forecast_df["Predicted_Revenue"]=predictions 

print(forecast_df)
print(model.coef_)
print(model.intercept_)


plt.figure(figsize=(10,6))
plt.plot(df["Year"],df["Total_Revenue"],marker='o',linewidth='2',label="Actual_Revenue")
plt.plot(future_years["Year"],predictions,marker='o',linewidth='2',label="Forecast Revenue",linestyle="--")
plt.title("Current Trends Vs Future Trends")
plt.xlabel("Years")
plt.ylabel("Revenue Generated")
plt.legend()
plt.grid(True)
plt.savefig("charts/Curr_vs_Fut_rev.png")
plt.close()