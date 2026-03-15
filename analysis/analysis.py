import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load data
df = pd.read_csv(r"D:/Data_Analytics_Dashboard/data/sales_data.csv")

df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
df['Total_Sales'] = df['Quantity'] * df['Price']

print("📊 KPIs")
print("Total Revenue:", df['Total_Sales'].sum())
print("Average Order Value:", df['Total_Sales'].mean())
print("Total Orders:", df['OrderID'].nunique())

# Sales by Category
category_sales = df.groupby('Category')['Total_Sales'].sum()
plt.figure()
category_sales.plot(kind='bar')
plt.title("Sales by Category")
plt.tight_layout()
plt.savefig(r"D:/Data_Analytics_Dashboard/output/bar_chart.png")
plt.close()

# Monthly Trend
monthly_sales = df.groupby(df['Date'].dt.to_period('M'))['Total_Sales'].sum()
plt.figure()
monthly_sales.plot()
plt.title("Monthly Sales Trend")
plt.tight_layout()
plt.savefig(r"D:/Data_Analytics_Dashboard/output/line_chart.png")
plt.close()

# Region Pie
region_sales = df.groupby('Region')['Total_Sales'].sum()
plt.figure()
region_sales.plot(kind='pie', autopct='%1.1f%%')
plt.title("Sales by Region")
plt.ylabel("")
plt.tight_layout()
plt.savefig(r"D:/Data_Analytics_Dashboard/output/pie_chart.png")
plt.close()

# ==============================
# HEATMAP: Category vs Region
# ==============================

pivot_table = pd.pivot_table(
    df,
    values='Total_Sales',
    index='Category',
    columns='Region',
    aggfunc='sum'
)

plt.figure(figsize=(8, 5))
sns.heatmap(
    pivot_table,
    annot=True,
    fmt=".0f",
    cmap="Blues"
)

plt.title("Sales Heatmap (Category vs Region)")
plt.xlabel("Region")
plt.ylabel("Category")
plt.tight_layout()
plt.savefig(r"D:/Data_Analytics_Dashboard/output/sales_heatmap.png")
plt.close()

print("✅ ALL charts generated successfully")
