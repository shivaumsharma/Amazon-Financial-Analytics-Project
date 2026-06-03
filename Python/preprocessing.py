import pandas as pd
from pathlib import Path

BASE_DIR=Path(__file__).resolve().parent

def load_data(path):
    df = pd.read_excel(path)
    return df


def create_yoy_growth(df):
    df["Yoy_growth"] = (df["Total_Revenue"].pct_change()) * 100
    df["Yoy_growth"]=df["Yoy_growth"].fillna(0)
    return df