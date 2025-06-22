
import streamlit as st
import pandas as pd

inventory = pd.read_csv("data/inventory.csv")
orders = pd.read_csv("data/orders.csv")
deliveries = pd.read_csv("data/delivery_logs.csv")
vendors = pd.read_csv("data/vendors.csv")

total_orders = len(orders)
delivered_orders = len(orders[orders['status'] == 'Delivered'])
fulfillment_rate = round((delivered_orders / total_orders) * 100, 2)

stockout_items = inventory[inventory['stock_level'] < inventory['reorder_threshold']]
stockout_risk = round((len(stockout_items) / len(inventory)) * 100, 2)

deliveries['delay_hours'] = pd.to_numeric(deliveries['delay_hours'], errors='coerce')
avg_delay = round(deliveries['delay_hours'].mean(skipna=True), 2)

sla_compliant = vendors[vendors['sla_days'] <= 4]
vendor_sla_compliance = round((len(sla_compliant) / len(vendors)) * 100, 2)

st.set_page_config(page_title="Supply Chain Control Tower", layout="centered")
st.title("📦 Supply Chain Control Tower Dashboard")

col1, col2 = st.columns(2)
col1.metric("✅ Order Fulfillment Rate", f"{fulfillment_rate} %")
col2.metric("📦 Stockout Risk", f"{stockout_risk} %")

col3, col4 = st.columns(2)
col3.metric("⏱️ Avg Delivery Delay", f"{avg_delay} hrs")
col4.metric("🤝 Vendor SLA Compliance", f"{vendor_sla_compliance} %")

st.subheader("🚨 Alerts & Issues")
if not stockout_items.empty:
    st.error("🔻 Inventory Below Threshold")
    st.dataframe(stockout_items)

pending_orders = orders[orders['status'] != 'Delivered']
if not pending_orders.empty:
    st.warning("📦 Pending Orders")
    st.dataframe(pending_orders)

delayed_deliveries = deliveries[deliveries['delay_hours'] > 0]
if not delayed_deliveries.empty:
    st.warning("🚚 Delayed Deliveries")
    st.dataframe(delayed_deliveries)
