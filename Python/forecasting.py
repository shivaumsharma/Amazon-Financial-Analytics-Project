from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
import pandas as pd


def forecast_revenue(df, future_years=None):
    if future_years is None:
        future_years = pd.DataFrame({"Year": [2025, 2026, 2027]})

    X = df[["Year"]]
    y = df["Total_Revenue"]

    linear_model = LinearRegression()
    linear_model.fit(X, y)
    linear_r2 = r2_score(y, linear_model.predict(X))
    linear_predictions = linear_model.predict(future_years)

    poly_features = PolynomialFeatures(degree=2)
    X_poly = poly_features.fit_transform(X)
    poly_model = LinearRegression()
    poly_model.fit(X_poly, y)
    poly_r2 = r2_score(y, poly_model.predict(X_poly))
    poly_predictions = poly_model.predict(poly_features.transform(future_years))

    forecast_df = future_years.copy()
    forecast_df["Linear_Forecast"] = linear_predictions
    forecast_df["Polynomial_Forecast"] = poly_predictions
    # Kept for backward compatibility with callers expecting a single "Predicted_Revenue" column
    forecast_df["Predicted_Revenue"] = linear_predictions

    model_metrics = {
        "linear_r2": linear_r2,
        "polynomial_r2": poly_r2,
        "n_observations": len(df),
    }

    return forecast_df, future_years, linear_predictions, linear_model, model_metrics
