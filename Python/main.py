from preprocessing import *
from visualization import *
from forecasting import *
from kpi_engine import *


df = load_data("data/Amazon_raw_data.xlsx")
print(df.head())
print(df.describe())

df = create_yoy_growth(df)
df = operating_margin(df)

revenue_trend(df)
net_income_trend(df)
aws_vs_revenue(df)
operating_margin_chart(df)
yoy_growth_chart(df)

forecast_df, future_years, predictions, model = (
    forecast_revenue(df)
)


forecast_chart(
    df,
    future_years,
    predictions
)

print(forecast_df)
print(model.coef_)
print(model.intercept_)