from preprocessing import *
from visualization import *
from forecasting import *
from kpi_engine import *
from anomaly_detection import detect_anomalies_multi
from indian_comparison import load_indian_data, company_growth_summary


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

forecast_df, future_years, predictions, model, model_metrics = forecast_revenue(df)

forecast_chart(
    df,
    future_years,
    predictions
)

print(forecast_df)
print(model.coef_)
print(model.intercept_)
print(f"Linear R^2: {model_metrics['linear_r2']:.4f} | Polynomial R^2: {model_metrics['polynomial_r2']:.4f}")

print(f"Revenue CAGR (2020-2024): {revenue_cagr(df):.2f}%")

anomaly_results = detect_anomalies_multi(df)
for column, result_df in anomaly_results.items():
    flagged = result_df[result_df["is_anomaly"]]
    print(f"Anomalies in {column}: {flagged['Year'].tolist() if not flagged.empty else 'none'}")

indian_df = load_indian_data("data/indian_market_comparison.csv")
print(company_growth_summary(indian_df))