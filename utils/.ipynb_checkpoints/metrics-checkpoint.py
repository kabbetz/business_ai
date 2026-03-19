def compute_metrics(df):
    return {
        "total_sales": df["revenue"].sum(),
        "average_sales": df["revenue"].mean(),
        "sales_by_region": df.groupby("region")["revenue"].sum().to_dict(),
        "sales_by_product": df.groupby("product")["revenue"].sum().to_dict(),
    }
