def operating_margin(df):

    df["Operating_Margin"] = (
        df["Operating_Income"] /
        df["Total_Revenue"]
    ) * 100

    return df


def revenue_cagr(df, year_col="Year", value_col="Total_Revenue"):
    ordered = df.sort_values(year_col)

    start_value = ordered[value_col].iloc[0]
    end_value = ordered[value_col].iloc[-1]
    n_periods = ordered[year_col].iloc[-1] - ordered[year_col].iloc[0]

    if n_periods == 0 or start_value <= 0:
        return None

    return ((end_value / start_value) ** (1 / n_periods) - 1) * 100