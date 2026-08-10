from kpi_engine import revenue_cagr


def generate_executive_summary(filtered_df, anomaly_results, model_metrics, forecast_df):
    sentences = []

    first_row = filtered_df.iloc[0]
    last_row = filtered_df.iloc[-1]
    span_years = int(last_row["Year"] - first_row["Year"])

    revenue_growth = (
        (last_row["Total_Revenue"] - first_row["Total_Revenue"]) / first_row["Total_Revenue"]
    ) * 100
    cagr = revenue_cagr(filtered_df)

    if span_years > 0 and cagr is not None:
        sentences.append(
            f"Between {int(first_row['Year'])} and {int(last_row['Year'])}, revenue grew from "
            f"\\${first_row['Total_Revenue']:.2f}B to \\${last_row['Total_Revenue']:.2f}B "
            f"(+{revenue_growth:.1f}% cumulative, a {cagr:.1f}% CAGR)."
        )
    else:
        sentences.append(
            f"{int(first_row['Year'])} revenue stood at \\${first_row['Total_Revenue']:.2f}B."
        )

    aws_growth = (
        (last_row["AWS_Revenue"] - first_row["AWS_Revenue"]) / first_row["AWS_Revenue"]
    ) * 100
    if span_years > 0:
        pace = "outpaced" if aws_growth > revenue_growth else "trailed"
        sentences.append(
            f"AWS revenue grew {aws_growth:.1f}% over the same period, {pace} total revenue "
            f"growth and moving cloud from {(first_row['AWS_Revenue'] / first_row['Total_Revenue']) * 100:.1f}% "
            f"to {(last_row['AWS_Revenue'] / last_row['Total_Revenue']) * 100:.1f}% of total revenue."
        )

    margin_delta = last_row["Operating_Margin"] - first_row["Operating_Margin"]
    if margin_delta > 0:
        direction = "expanded"
    elif margin_delta < 0:
        direction = "contracted"
    else:
        direction = "held steady"
    if span_years == 0:
        sentences.append(f"Operating margin stood at {last_row['Operating_Margin']:.1f}%.")
    else:
        sentences.append(
            f"Operating margin {direction} from {first_row['Operating_Margin']:.1f}% to "
            f"{last_row['Operating_Margin']:.1f}% ({margin_delta:+.1f} pts)."
        )

    flagged_notes = []
    for column, result_df in anomaly_results.items():
        anomalies = result_df[result_df["is_anomaly"]]
        if not anomalies.empty:
            years = ", ".join(str(int(y)) for y in anomalies["Year"])
            label = column.replace("_", " ")
            flagged_notes.append(f"{label} ({years})")
    if flagged_notes:
        sentences.append(
            "Statistical anomaly detection (z-score, |z| > 1.5) flagged: " + "; ".join(flagged_notes) + "."
        )
    else:
        sentences.append(
            "Statistical anomaly detection (z-score, |z| > 1.5) found no metric deviating sharply "
            "enough from trend to qualify as a formal outlier in the current selection."
        )

    if forecast_df is not None and model_metrics is not None:
        next_year = int(forecast_df["Year"].iloc[0])
        next_forecast = forecast_df["Linear_Forecast"].iloc[0]
        sentences.append(
            f"A linear trend model (R² = {model_metrics['linear_r2']:.3f} on "
            f"{model_metrics['n_observations']} years of data) projects {next_year} revenue near "
            f"\\${next_forecast:.2f}B; with only {model_metrics['n_observations']} historical points, "
            "this should be read as directional rather than precise."
        )

    return " ".join(sentences)
