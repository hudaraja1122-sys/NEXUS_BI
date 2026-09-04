import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_sales_data(output_path: str, n_rows: int = 1200):
    np.random.seed(42)
    
    start_date = datetime(2026, 1, 1)
    dates = [start_date + timedelta(days=int(np.random.uniform(0, 180))) for _ in range(n_rows)]
    
    categories = {
        "Electronics": ["Smartphone", "Laptop", "Wireless Headphones", "Smartwatch"],
        "Furniture": ["Ergonomic Chair", "Standing Desk", "Bookshelf", "Desk Lamp"],
        "Office Supplies": ["Notebook", "Pen Set", "Binder Clip Pack", "Desk Organizer"]
    }
    
    regions = ["North", "South", "East", "West"]
    
    data = []
    for i in range(n_rows):
        cat = np.random.choice(list(categories.keys()), p=[0.4, 0.35, 0.25])
        prod = np.random.choice(categories[cat])
        region = np.random.choice(regions, p=[0.3, 0.25, 0.25, 0.2])
        
        date = dates[i]
        is_q2 = date.month in [4, 5, 6]
        
        # Base pricing & quantity
        if cat == "Electronics":
            unit_price = float(np.random.uniform(150, 950))
            quantity = int(np.random.randint(1, 6))
            # Inject drop in Q2 Electronics demand + steeper discounts
            if is_q2:
                unit_price *= 0.82
                discount = float(np.random.choice([0.15, 0.25, 0.35], p=[0.3, 0.4, 0.3]))
            else:
                discount = float(np.random.choice([0.0, 0.05, 0.1], p=[0.6, 0.3, 0.1]))
        elif cat == "Furniture":
            unit_price = float(np.random.uniform(80, 450))
            quantity = int(np.random.randint(1, 4))
            discount = float(np.random.choice([0.0, 0.1, 0.15], p=[0.5, 0.3, 0.2]))
        else:
            unit_price = float(np.random.uniform(10, 60))
            quantity = int(np.random.randint(2, 15))
            discount = float(np.random.choice([0.0, 0.05], p=[0.8, 0.2]))
            
        gross_rev = round(unit_price * quantity, 2)
        rev = round(gross_rev * (1.0 - discount), 2)
        cost_multiplier = 0.65 if cat != "Electronics" else 0.72
        cost = round(gross_rev * cost_multiplier, 2)
        profit = round(rev - cost, 2)
        
        data.append({
            "Order_ID": f"ORD-2026-{1000 + i}",
            "Order_Date": date.strftime("%Y-%m-%d"),
            "Customer_ID": f"CUST-{np.random.randint(100, 300)}",
            "Product": prod,
            "Category": cat,
            "Region": region,
            "Quantity": quantity,
            "Unit_Price": round(unit_price, 2),
            "Discount": round(discount, 2),
            "Revenue": rev,
            "Cost": cost,
            "Profit": profit
        })
        
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Sample dataset generated: {output_path} ({len(df)} rows)")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    generate_sample_sales_data(os.path.join(current_dir, "sample_sales.csv"))