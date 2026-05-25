import matplotlib.pyplot as plt


def revenue_trend(df):
  plt.figure(figsize=(10,6))
  plt.plot(df["Year"],df["Total_Revenue"],marker="o")
  plt.title("Amazon revenue Trend")
  plt.xlabel("Year")
  plt.ylabel("Revenue($bn)")
  plt.grid(True)
  plt.savefig("Screenshots/charts/revenue_trend.png")
  plt.close()


def net_income_trend(df):
  plt.figure(figsize=(10,6))
  plt.plot(df["Year"],df["Net_Income"],marker='o',linewidth=2,label="Net income %")
  plt.grid(True)
  plt.title("Amazon Net Income Trend")
  plt.xlabel("Year")
  plt.ylabel("Net_Income($bn)")
  plt.savefig("Screenshots/charts/Net_income.png")
  plt.close()

def aws_vs_revenue(df):
  plt.figure(figsize=(10,6))
  plt.plot(df["Year"],df["Total_Revenue"],marker="o",label="Total Revenue")
  plt.plot(df["Year"],df["AWS_Revenue"],marker="o",label="AWS Revenue")
  plt.title("AWS VS TOTAL REVENUE")
  plt.xlabel("Year")
  plt.ylabel("Revenue")
  plt.legend()
  plt.grid(True)
  plt.savefig("Screenshots/charts/AWSvsRevenue.png")
  plt.close()

def operating_margin_chart(df):

  plt.figure(figsize=(10,6))
  plt.plot(df["Year"],df["Operating_Margin"],marker="o",label="Operating Margin %")
  plt.xlabel("Year")
  plt.legend()
  plt.grid(True)
  plt.title("Operating Margin Percentages")
  plt.ylabel("Operating Margin")
  plt.savefig("Screenshots/charts/Operating_margin.png")
  plt.close()

def yoy_growth_chart(df):
  plt.figure(figsize=(10,6))
  plt.plot(df["Year"],df["Yoy_growth"],marker='o',linewidth=2,label="YoY Growth %")
  plt.title("Year On Year Growth")
  plt.xlabel("Year")
  plt.ylabel("YoY Growth")
  plt.grid(True)
  plt.legend()
  plt.savefig("Screenshots/charts/YOY_growth.png")
  plt.close()

def forecast_chart(df,future_years,predictions):
  plt.figure(figsize=(10,6))
  plt.plot(df["Year"],df["Total_Revenue"],marker='o',linewidth='2',label="Actual_Revenue")
  plt.plot(future_years["Year"],predictions,marker='o',linewidth='2',label="Forecast Revenue",linestyle="--")
  plt.title("Current Trends Vs Future Trends")
  plt.xlabel("Years")
  plt.ylabel("Revenue Generated")
  plt.legend()
  plt.grid(True)
  plt.savefig("Screenshots/charts/Curr_vs_Fut_rev.png")
  plt.close()