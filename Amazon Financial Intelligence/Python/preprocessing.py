import pandas as pd

def load_data(path):
    df = pd.read_excel(path)
    return df


def create_yoy_growth(df):
    df["Yoy_growth"] = (df["Total_Revenue"].pct_change()) * 100
    return df