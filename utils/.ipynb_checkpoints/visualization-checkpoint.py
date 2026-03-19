import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def plot_revenue_trend(df):
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df_grouped = df.groupby(df["date"].dt.to_period("M"))["revenue"].sum()
    df_grouped.index = df_grouped.index.to_timestamp()

    plt.figure()
    df_grouped.plot()

    plt.title("Revenue Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.ticklabel_format(style='plain', axis='y')  # remove scientific notation

    return plt

def plot_product_performance(df):
    df_grouped = df.groupby("product")["revenue"].sum()

    plt.figure()
    df_grouped.plot(kind="bar")
    plt.title("Product Performance")

    return plt

def plot_regional_analysis(df):
    df_grouped = df.groupby("region")["revenue"].sum()

    plt.figure()
    df_grouped.plot(kind="bar")
    plt.title("Regional Sales")

    return plt

def plot_customer_age_groups(df):
    bins = [18, 25, 35, 45, 60, 100]
    labels = ["18-25", "26-35", "36-45", "46-60", "60+"]

    df["age_group"] = pd.cut(df["customer_age"], bins=bins, labels=labels)

    df_grouped = df.groupby("age_group")["revenue"].sum()

    plt.figure()
    df_grouped.plot(kind="bar")

    plt.title("Customer Age Group Analysis")
    plt.xlabel("Age Group")
    plt.ylabel("Revenue")

    return plt
