import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

from preprocessing import load_data, create_yoy_growth
from kpi_engine import operating_margin, revenue_cagr
from forecasting import forecast_revenue
from anomaly_detection import detect_anomalies_multi
from insights import generate_executive_summary
from indian_comparison import (
    load_indian_data,
    build_comparison_table,
    build_indexed_growth,
    company_growth_summary,
)

BASE_DIR = Path(__file__).resolve().parent.parent

df = load_data(BASE_DIR / "data" / "Amazon_raw_data.xlsx")
df = create_yoy_growth(df)
df = operating_margin(df)

st.set_page_config(page_title="Amazon Financial Intelligence", layout="wide")
st.title("Amazon Financial Intelligence Dashboard")

st.sidebar.markdown("## About")
st.sidebar.info(
    "Financial intelligence dashboard for Amazon featuring KPI analytics, forecasting, anomaly "
    "detection, an auto-generated executive summary, and a benchmarking view against India's "
    "largest listed e-commerce/quick-commerce platforms."
)
st.sidebar.header("Dashboard Filters")
selected_years = st.sidebar.multiselect("Select Years", options=df["Year"].unique(), default=df["Year"].unique())
filtered_df = df[df["Year"].isin(selected_years)].sort_values("Year")
if filtered_df.empty:
    st.warning("Please select at least one year.")
    st.stop()


# ---------------------------------------------------------------------------
# KPI Section
# ---------------------------------------------------------------------------
total_revenue = filtered_df["Total_Revenue"].sum()
net_income = filtered_df["Net_Income"].sum()
operating_income = filtered_df["Operating_Income"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Revenue (selected years)", f"${total_revenue:.2f}B")
col2.metric("Net Income (selected years)", f"${net_income:.2f}B")
col3.metric("Operating Income (selected years)", f"${operating_income:.2f}B")

st.subheader("Financial Dataset")
st.dataframe(df)

st.subheader("Filtered Financial Dataset")
st.dataframe(filtered_df)


# ---------------------------------------------------------------------------
# Trend charts
# ---------------------------------------------------------------------------
st.subheader("Revenue Trend Analysis")
fig = px.line(filtered_df, x="Year", y="Total_Revenue", markers=True, title="Amazon Revenue Growth")
fig.update_xaxes(dtick=1, type="category")
st.plotly_chart(fig, use_container_width=True)

st.subheader("AWS Contribution Analysis")
fig = px.line(filtered_df, x="Year", y=["Total_Revenue", "AWS_Revenue"], markers=True, title="Amazon AWS Contribution")
fig.update_xaxes(dtick=1, type="category")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Operating Margin Trend")
fig = px.line(filtered_df, x="Year", y="Operating_Margin", markers=True, title="Amazon Margins")
fig.update_xaxes(dtick=1, type="category")
st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------------
# Anomaly Detection (runs on the full 5-year dataset regardless of the year
# filter above, since z-scores need a stable sample to be meaningful)
# ---------------------------------------------------------------------------
st.header("Anomaly Detection")
st.caption(
    "Z-score based outlier detection (|z| > 1.5) across key financial metrics, computed on the "
    "full 2020–2024 dataset."
)

anomaly_results = detect_anomalies_multi(df, columns=("Net_Income", "Operating_Margin"))

anomaly_cols = st.columns(len(anomaly_results))
for col, (column, result_df) in zip(anomaly_cols, anomaly_results.items()):
    with col:
        fig = px.scatter(
            result_df,
            x="Year",
            y=column,
            color="is_anomaly",
            color_discrete_map={True: "#EF553B", False: "#636EFA"},
            title=f"{column.replace('_', ' ')} — Anomaly Scan",
        )
        fig.add_trace(
            go.Scatter(
                x=result_df["Year"],
                y=result_df[column],
                mode="lines",
                line=dict(color="gray", dash="dot"),
                showlegend=False,
            )
        )
        fig.update_xaxes(type="category")
        fig.update_layout(legend_title_text="Anomaly")
        st.plotly_chart(fig, use_container_width=True)

        anomalies = result_df[result_df["is_anomaly"]]
        if not anomalies.empty:
            years = ", ".join(str(int(y)) for y in anomalies["Year"])
            st.warning(f"Flagged year(s): {years} (|z| > 1.5)")
        else:
            st.info("No anomalies above the |z| > 1.5 threshold.")


# ---------------------------------------------------------------------------
# Forecast — Linear vs Polynomial model comparison
# ---------------------------------------------------------------------------
st.header("Revenue Forecast — Model Comparison")

forecast_df, future_years, linear_predictions, linear_model, model_metrics = forecast_revenue(df)

m1, m2, m3 = st.columns(3)
m1.metric("Linear Regression R²", f"{model_metrics['linear_r2']:.3f}")
m2.metric("Polynomial (deg 2) R²", f"{model_metrics['polynomial_r2']:.3f}")
m3.metric("Historical years used", model_metrics["n_observations"])
st.caption(
    "Fit on 5 historical years (2020–2024). With this few data points, R² runs high for both "
    "models by construction — treat the forecast as directional, not a precise prediction."
)

st.dataframe(forecast_df)

fig_forecast = go.Figure()
fig_forecast.add_trace(
    go.Scatter(x=df["Year"], y=df["Total_Revenue"], mode="lines+markers", name="Actual Revenue")
)
fig_forecast.add_trace(
    go.Scatter(
        x=forecast_df["Year"],
        y=forecast_df["Linear_Forecast"],
        mode="lines+markers",
        name="Linear Forecast",
        line=dict(dash="dash"),
    )
)
fig_forecast.add_trace(
    go.Scatter(
        x=forecast_df["Year"],
        y=forecast_df["Polynomial_Forecast"],
        mode="lines+markers",
        name="Polynomial Forecast (deg 2)",
        line=dict(dash="dot"),
    )
)
fig_forecast.update_xaxes(type="category")
fig_forecast.update_layout(title="Actual vs. Forecast Revenue (2020–2027)", yaxis_title="Revenue ($B)")
st.plotly_chart(fig_forecast, use_container_width=True)


# ---------------------------------------------------------------------------
# Executive Summary (rule-based narrative generator)
# ---------------------------------------------------------------------------
st.header("Executive Summary")
summary_text = generate_executive_summary(filtered_df, anomaly_results, model_metrics, forecast_df)
st.info(summary_text)


# ---------------------------------------------------------------------------
# Indian Market Comparison
# ---------------------------------------------------------------------------
st.header("Indian Market Comparison")
st.caption(
    "Amazon vs. India's largest publicly listed e-commerce / quick-commerce platforms — "
    "Zomato (Eternal), Swiggy, and Nykaa. Real, sourced figures — see data/SOURCES.md for "
    "fiscal-year alignment and FX methodology. Flipkart, Reliance Retail, and Tata Digital are "
    "excluded because they don't publish standalone audited financials."
)

indian_df = load_indian_data(BASE_DIR / "data" / "indian_market_comparison.csv")
comparison_df = build_comparison_table(df, indian_df)
indexed_df = build_indexed_growth(df, indian_df)
growth_summary = company_growth_summary(indian_df)

amazon_latest = df.sort_values("Year").iloc[-1]
amazon_summary_row = pd.DataFrame(
    [
        {
            "Company": "Amazon",
            "Revenue_CAGR_Pct": revenue_cagr(df),
            "Latest_Revenue_USD_B": amazon_latest["Total_Revenue"],
            "Latest_Net_Income_USD_B": amazon_latest["Net_Income"],
            "Latest_Net_Margin_Pct": (amazon_latest["Net_Income"] / amazon_latest["Total_Revenue"]) * 100,
        }
    ]
)
combined_summary = pd.concat([amazon_summary_row, growth_summary], ignore_index=True)

fig_indexed = px.line(
    indexed_df,
    x="Amazon_Aligned_Year",
    y="Index",
    color="Company",
    markers=True,
    title="Revenue Growth Indexed to 100 (first aligned year = 100)",
)
fig_indexed.update_xaxes(type="category")
st.plotly_chart(fig_indexed, use_container_width=True)

col_a, col_b = st.columns(2)
with col_a:
    fig_cagr = px.bar(combined_summary, x="Company", y="Revenue_CAGR_Pct", title="Revenue CAGR % (aligned window)")
    st.plotly_chart(fig_cagr, use_container_width=True)
with col_b:
    fig_margin = px.bar(combined_summary, x="Company", y="Latest_Net_Margin_Pct", title="Latest Net Margin %")
    st.plotly_chart(fig_margin, use_container_width=True)

st.subheader("Company Comparison Summary")
st.dataframe(combined_summary)

st.subheader("Year-by-Year Comparison Detail")
st.dataframe(comparison_df)

indian_latest_total = indian_df[indian_df["Amazon_Aligned_Year"] == indian_df["Amazon_Aligned_Year"].max()][
    "Revenue_USD_B"
].sum()
scale_multiple = amazon_latest["Total_Revenue"] / indian_latest_total
fastest_grower = growth_summary.sort_values("Revenue_CAGR_Pct", ascending=False).iloc[0]

st.success(
    f"Amazon's {int(amazon_latest['Year'])} revenue (\\${amazon_latest['Total_Revenue']:.2f}B) is "
    f"roughly {scale_multiple:,.0f}x the combined revenue of Zomato, Swiggy, and Nykaa "
    f"(\\${indian_latest_total:.2f}B) in the aligned year — yet {fastest_grower['Company']} grew "
    f"revenue at a {fastest_grower['Revenue_CAGR_Pct']:.1f}% CAGR versus Amazon's "
    f"{revenue_cagr(df):.1f}%. This contrasts a mature, profitable global platform against "
    f"India's hyper-growth, still cash-burning digital commerce market."
)
