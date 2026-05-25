def detect_anomalies(df):

    mean = df["Net_Income"].mean()

    std = df["Net_Income"].std()

    df["z_score"] = (
        df["Net_Income"] - mean
    ) / std

    anomalies = df[
        abs(df["z_score"]) > 1.5
    ]

    return anomalies