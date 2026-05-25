from sklearn.linear_model import LinearRegression
import pandas as pd

def forecast_revenue(df):
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

  return (forecast_df,future_years,predictions,model)
