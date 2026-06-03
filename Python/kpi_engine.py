def operating_margin(df):

    df["Operating_Margin"] = (
        df["Operating_Income"] /
        df["Total_Revenue"]
    ) * 100

    return df