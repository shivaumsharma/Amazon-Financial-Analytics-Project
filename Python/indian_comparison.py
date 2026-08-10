import pandas as pd


def load_indian_data(path):
    return pd.read_csv(path)


def build_comparison_table(amazon_df, indian_df):
    amazon_slice = amazon_df[["Year", "Total_Revenue", "Net_Income"]].rename(
        columns={
            "Year": "Amazon_Aligned_Year",
            "Total_Revenue": "Amazon_Revenue_USD_B",
            "Net_Income": "Amazon_Net_Income_USD_B",
        }
    )

    merged = indian_df.merge(amazon_slice, on="Amazon_Aligned_Year", how="left")
    merged["Net_Margin_Pct"] = (merged["Net_Income_USD_B"] / merged["Revenue_USD_B"]) * 100
    merged["Amazon_Scale_Multiple"] = merged["Amazon_Revenue_USD_B"] / merged["Revenue_USD_B"]

    return merged


def build_indexed_growth(amazon_df, indian_df):
    aligned_years = sorted(indian_df["Amazon_Aligned_Year"].unique())
    amazon_sorted = amazon_df[amazon_df["Year"].isin(aligned_years)].sort_values("Year")
    base_amazon = amazon_sorted["Total_Revenue"].iloc[0]

    rows = [
        {
            "Company": "Amazon",
            "Amazon_Aligned_Year": row["Year"],
            "Index": row["Total_Revenue"] / base_amazon * 100,
        }
        for _, row in amazon_sorted.iterrows()
    ]

    for company, group in indian_df.groupby("Company"):
        group = group.sort_values("Amazon_Aligned_Year")
        base = group["Revenue_USD_B"].iloc[0]
        rows.extend(
            {
                "Company": company,
                "Amazon_Aligned_Year": row["Amazon_Aligned_Year"],
                "Index": row["Revenue_USD_B"] / base * 100,
            }
            for _, row in group.iterrows()
        )

    return pd.DataFrame(rows)


def company_growth_summary(indian_df):
    summaries = []

    for company, group in indian_df.groupby("Company"):
        group = group.sort_values("Amazon_Aligned_Year")

        start_rev = group["Revenue_USD_B"].iloc[0]
        end_rev = group["Revenue_USD_B"].iloc[-1]
        n_periods = len(group) - 1

        cagr = ((end_rev / start_rev) ** (1 / n_periods) - 1) * 100 if n_periods > 0 else None
        latest_net_margin = (
            group["Net_Income_USD_B"].iloc[-1] / group["Revenue_USD_B"].iloc[-1]
        ) * 100

        summaries.append(
            {
                "Company": company,
                "Revenue_CAGR_Pct": cagr,
                "Latest_Revenue_USD_B": end_rev,
                "Latest_Net_Income_USD_B": group["Net_Income_USD_B"].iloc[-1],
                "Latest_Net_Margin_Pct": latest_net_margin,
            }
        )

    return pd.DataFrame(summaries)
