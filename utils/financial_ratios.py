def compute_ratios(data):
    ratios = {}

    if "revenue" in data and "net_income" in data:
        ratios["profit_margin"] = data["net_income"] / data["revenue"]

    if "current_assets" in data and "current_liabilities" in data:
        ratios["current_ratio"] = data["current_assets"] / data["current_liabilities"]

    if "revenue" in data and "total_assets" in data:
        ratios["asset_turnover"] = data["revenue"] / data["total_assets"]

    return ratios 
