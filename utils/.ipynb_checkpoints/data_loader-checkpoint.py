import pandas as pd

def load_data():
    df = pd.read_csv("data/data_sales.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df
