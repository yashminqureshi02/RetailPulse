from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="RetailPulse", layout="wide")

st.title("RetailPulse")
st.subheader("Customer Analytics & Sales Dashboard")

root = Path(__file__).resolve().parent
file = root / "data" / "processed" / "online_retail_cleaned.csv"

if not file.exists():
    st.error("Cleaned dataset not found. Run the data cleaning script first.")
    st.stop()

df = pd.read_csv(file)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
df = df.dropna(subset=["InvoiceDate"])

st.sidebar.header("Filters")
countries = ["All"] + sorted(df["Country"].dropna().unique().tolist())
country = st.sidebar.selectbox("Choose country", countries)

if country != "All":
    df = df[df["Country"] == country]

sales = df["TotalAmount"].sum()
orders = df["InvoiceNo"].nunique()
customers = df["CustomerID"].nunique()
products = df["StockCode"].nunique()

a, b, c, d = st.columns(4)
a.metric("Total Sales", f"£{sales:,.2f}")
b.metric("Orders", f"{orders:,}")
c.metric("Customers", f"{customers:,}")
d.metric("Products", f"{products:,}")

daily = (
    df.set_index("InvoiceDate")
    .resample("D")["TotalAmount"]
    .sum()
    .reset_index()
)

st.subheader("Daily Sales Trend")
st.plotly_chart(
    px.line(daily, x="InvoiceDate", y="TotalAmount"),
    use_container_width=True
)

left, right = st.columns(2)

with left:
    st.subheader("Top Products")
    top_products = (
        df.groupby("Description")["TotalAmount"]
        .sum().nlargest(10).sort_values().reset_index()
    )
    st.plotly_chart(
        px.bar(top_products, x="TotalAmount", y="Description",
               orientation="h"),
        use_container_width=True
    )

with right:
    st.subheader("Sales by Country")
    top_countries = (
        df.groupby("Country")["TotalAmount"]
        .sum().nlargest(10).sort_values().reset_index()
    )
    st.plotly_chart(
        px.bar(top_countries, x="TotalAmount", y="Country",
               orientation="h"),
        use_container_width=True
    )

st.subheader("Transaction Records")
st.dataframe(df.head(100), use_container_width=True)

st.download_button(
    "Download Data",
    df.to_csv(index=False).encode("utf-8"),
    "retailpulse_data.csv",
    "text/csv"
)


st.divider()
st.header("Customer Segmentation")

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

customer_data = df.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda x: (
        df["InvoiceDate"].max() - x.max()
    ).days),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("TotalAmount", "sum")
).reset_index()

if len(customer_data) >= 3:
    features = customer_data[["Recency", "Frequency", "Monetary"]]
    scaled = StandardScaler().fit_transform(features)

    model = KMeans(n_clusters=3, random_state=42, n_init=10)
    customer_data["Segment"] = model.fit_predict(scaled)

    segment_names = {
        0: "Segment 1",
        1: "Segment 2",
        2: "Segment 3"
    }
    customer_data["Segment"] = customer_data["Segment"].map(segment_names)

    st.write("Customers are grouped into three purchasing-behaviour segments.")
    st.dataframe(customer_data.head(100), use_container_width=True)

    segment_counts = (
        customer_data["Segment"].value_counts()
        .rename_axis("Segment")
        .reset_index(name="Customers")
    )
    st.plotly_chart(
        px.bar(segment_counts, x="Segment", y="Customers",
               title="Customers by Segment"),
        use_container_width=True
    )
else:
    st.warning("Not enough customers for segmentation.")