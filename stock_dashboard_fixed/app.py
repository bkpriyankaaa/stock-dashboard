import streamlit as st
import time
import random
import pandas as pd

st.set_page_config(page_title="Stock Broker Dashboard", layout="wide")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
.header {
    background: linear-gradient(to right, #4facfe, #00f2fe);
    padding: 20px;
    border-radius: 10px;
    color: white;
    text-align: center;
    font-size: 26px;
    margin-bottom: 20px;
    font-weight: bold;
}
.stock-card {
    background: white;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

SUPPORTED = ['GOOG', 'TSLA', 'AMZN', 'META', 'NVDA']

# ------------------ SESSION VARIABLES ------------------
if "email" not in st.session_state:
    st.session_state.email = None
if "subscribed" not in st.session_state:
    st.session_state.subscribed = []
if "chart_data" not in st.session_state:
    st.session_state.chart_data = pd.DataFrame(columns=SUPPORTED)

# ------------------ LOGIN ------------------
if st.session_state.email is None:
    st.markdown("<div class='header'>🔐 Stock Broker Login</div>", unsafe_allow_html=True)
    email = st.text_input("Enter Email")
    if st.button("Login"):
        if email.strip() != "":
            st.session_state.email = email
            st.rerun()
        else:
            st.error("Enter a valid email")
    st.stop()

# ------------------ SIDEBAR LOGOUT ------------------
st.sidebar.write(f"Logged in as: {st.session_state.email}")
if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

# ------------------ HEADER ------------------
st.markdown("<div class='header'>📊 Stock Dashboard</div>", unsafe_allow_html=True)

# ------------------ SUBSCRIBE UI ------------------
st.subheader("Manage Stock Subscriptions")

selections = st.multiselect(
    "Choose stocks:",
    SUPPORTED,
    default=st.session_state.subscribed
)

if st.button("Update"):
    st.session_state.subscribed = selections
    st.success("Subscriptions updated!")
    time.sleep(0.5)
    st.rerun()

st.write("---")

# ------------------ DASHBOARD ------------------
if not st.session_state.subscribed:
    st.info("Please subscribe to at least one stock.")
    st.stop()

# Create columns for live price metrics
cols = st.columns(len(st.session_state.subscribed))
placeholders = {stock: cols[i].empty() for i, stock in enumerate(st.session_state.subscribed)}

# Combined chart placeholder
chart_placeholder = st.empty()

# ------------------ LIVE UPDATE LOOP ------------------
while True:
    row = {}
    for i, stock in enumerate(st.session_state.subscribed):
        price = random.randint(100, 500)
        row[stock] = price
        placeholders[stock].metric(f"{stock}", f"${price}")

    # Add row to chart dataset
    new_row = pd.DataFrame([row])
    st.session_state.chart_data = pd.concat([st.session_state.chart_data, new_row], ignore_index=True)

    # Keep chart optimized
    if len(st.session_state.chart_data) > 25:
        st.session_state.chart_data = st.session_state.chart_data.tail(25).reset_index(drop=True)

    # Show single combined live chart
    chart_placeholder.line_chart(st.session_state.chart_data[st.session_state.subscribed])

    time.sleep(1)
