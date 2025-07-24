import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on July 14th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

#new code
#adding an average profit feature to df
# Calculate average profit margin for the entire dataframe
total_sales_all = df['Sales'].sum()
total_profit_all = df['Profit'].sum()

# Avoid division by zero
avg_profit_margin = (total_profit_all / total_sales_all * 100) if total_sales_all > 0 else 0

# Add the same value to every row in a new column
df['Average_Profit_Margin'] = avg_profit_margin

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")


# Get unique values for Category
category_options = df['Category'].unique()

# Select Category first
selected_categories = st.multiselect("Select Category:", category_options)

# Filter subcategories based on selected categories
if selected_categories:
    filtered_subcats = df[df['Category'].isin(selected_categories)]['Sub_Category'].unique()
    selected_subcategories = st.multiselect("Select Sub-Category:", filtered_subcats)
else:
    st.info("Please select at least one Category to choose Sub-Categories.")
    selected_subcategories = []

# Apply filters
filtered_df = df[df['Category'].isin(selected_categories)] if selected_categories else df.copy()

if selected_subcategories:
    filtered_df = filtered_df[filtered_df['Sub_Category'].isin(selected_subcategories)]

# Display results
st.write(filtered_df)

sales_by_month_filtered = filtered_df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

#line chart
st.line_chart(sales_by_month_filtered, y="Sales")


#metrics
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0

# ---- Average Profit Margin (already computed before) ----
avg_profit_margin = df['Average_Profit_Margin'].iloc[0]  # Since all rows have same value
# ---- Difference from average ----
margin_diff = profit_margin - avg_profit_margin
diff_label = f"{margin_diff:+.2f}%"  # e.g., "+3.42%"

# ---- Display metrics with light borders ----
# Format values
formatted_sales = f"${total_sales:,.2f}"
formatted_profit = f"${total_profit:,.2f}"
formatted_margin = f"{profit_margin:.2f}%"
formatted_diff = f"{margin_diff:+.2f}%"

# --- Metric display function ---
def bordered_metric(title, value):
    st.markdown(f"""
        <div style='
            border: 1px solid #ccc;
            padding: 16px;
            border-radius: 10px;
            text-align: center;
            font-family: sans-serif;
            background-color: #f9f9f9;
        '>
            <div style='font-size: 14px; color: #333;'>{title}</div>
            <div style='font-size: 22px; font-weight: bold; margin-top: 4px;'>{value}</div>
        </div>
    """, unsafe_allow_html=True)

# --- Layout as 2x2 ---
col1, col2 = st.columns(2)
with col1:
    bordered_metric("Total Sales", formatted_sales)
with col2:
    bordered_metric("Total Profit", formatted_profit)

col3, col4 = st.columns(2)
with col3:
    bordered_metric("Profit Margin", formatted_margin)
with col4:
    bordered_metric("Δ vs Avg Margin", formatted_diff)

st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
