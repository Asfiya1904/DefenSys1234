import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime
import plotly.express as px
import time

# ------------------ Auth & Session Setup ------------------
def authenticate():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.title("🔐 Welcome to DefenSys Pro")
        with st.form("login_form"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                if st.session_state.username == "admin" and st.session_state.password == "admin123":
                    st.success("Logged in successfully!")
                    st.session_state["authenticated"] = True
                else:
                    st.error("Incorrect credentials.")
        st.stop()

# ------------------ Fake Data Generation ------------------
def generate_data():
    np.random.seed(42)
    data = np.random.normal(0, 1, size=(100, 4))
    df = pd.DataFrame(data, columns=["Feature1", "Feature2", "Feature3", "Feature4"])
    model = IsolationForest(contamination=0.1)
    df["Prediction"] = model.fit_predict(df)
    df["Status"] = df["Prediction"].map({1: "🟢 Normal", -1: "🔴 Suspicious"})
    return df

# ------------------ UI Components ------------------
def dashboard():
    st.title("📊 Dashboard")
    df = generate_data()

    col1, col2 = st.columns(2)
    col1.metric("🟢 Safe", (df["Status"] == "🟢 Normal").sum())
    col2.metric("🔴 Threats", (df["Status"] == "🔴 Suspicious").sum())

    chart = df["Status"].value_counts().reset_index()
    chart.columns = ["Status", "Count"]
    fig = px.pie(chart, names="Status", values="Count", title="Threat Status Overview")
    st.plotly_chart(fig)

    st.subheader("📄 Detected Data")
    st.dataframe(df.head(10), use_container_width=True)

    st.download_button("📥 Download Report", df.to_csv(index=False), file_name="defensys_report.csv")

def profile_page():
    st.title("👤 Profile")
    st.write("**Username:** admin")
    st.write("**Email:** admin@example.com")
    st.write("**Role:** Administrator")
    st.write("**Last login:**", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    st.button("🔒 Change Password (coming soon)")

def settings_page():
    st.title("⚙️ Settings")
    st.checkbox("🔁 Auto-refresh dashboard")
    st.slider("🔔 Alert Sensitivity", min_value=0, max_value=100, value=70)
    st.radio("🌓 Theme", ["Light", "Dark"], index=0)

# ------------------ Main App ------------------
def main():
    authenticate()

    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/565/565547.png", width=60)
    st.sidebar.title("DefenSys Pro")
    selection = st.sidebar.radio("Navigation", ["Dashboard", "Profile", "Settings"])
    st.sidebar.markdown("---")
    st.sidebar.info("Built with ❤️ for financial security")

    if selection == "Dashboard":
        dashboard()
    elif selection == "Profile":
        profile_page()
    elif selection == "Settings":
        settings_page()

if __name__ == "__main__":
    main()
