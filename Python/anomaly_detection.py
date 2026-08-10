def detect_anomalies(df, column="Net_Income", threshold=1.5):
    df = df.copy()

    mean = df[column].mean()
    std = df[column].std()

    df["z_score"] = (df[column] - mean) / std
    df["is_anomaly"] = df["z_score"].abs() > threshold

    return df


def detect_anomalies_multi(df, columns=("Net_Income", "Operating_Margin"), threshold=1.5):
    return {
        column: detect_anomalies(df, column=column, threshold=threshold)
        for column in columns
    }
