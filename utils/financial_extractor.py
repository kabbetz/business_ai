import re

def extract_financials(text):
    data = {}

    patterns = {
        "revenue": r"(revenue|total revenue).*?(\d[\d,]*)",
        "net_income": r"(net income).*?(\d[\d,]*)",
        "total_assets": r"(total assets).*?(\d[\d,]*)",
        "current_assets": r"(current assets).*?(\d[\d,]*)",
        "current_liabilities": r"(current liabilities).*?(\d[\d,]*)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text.lower())
        if match:
            value = match.group(2).replace(",", "")
            data[key] = float(value)

    return data 
