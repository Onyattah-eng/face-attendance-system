import streamlit as st
import pandas as pd
import os
import plotly.express as px
from fpdf import FPDF

# ================= CONFIG ================= #
FILE_PATH = "logs/attendance.csv"

st.set_page_config(
    page_title="Attendance Management System", layout="wide", page_icon="📊"
)

# ================= LOGIN SYSTEM ================= #
USERS = {"admin": "admin123", "student": "student123"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

if not st.session_state.logged_in:
    st.markdown(
        """
        <style>
        .login-title {
            text-align: center;
            font-size: 38px;
            font-weight: bold;
            margin-top: 80px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='login-title'>📊 Attendance System Login</div>",
        unsafe_allow_html=True,
    )

    username = st.text_input("Username").strip()
    password = st.text_input("Password", type="password").strip()

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.role = username
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ================= LOAD DATA ================= #
if os.path.exists(FILE_PATH):
    df = pd.read_csv(FILE_PATH)
else:
    df = pd.DataFrame(columns=["Name", "Date", "Time"])

# ================= HEADER ================= #
st.title("📊 Attendance Management System")
st.caption("Real-time biometric attendance tracking system")

st.divider()

# ================= METRICS ================= #
col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(df))
col2.metric("Students", df["Name"].nunique() if not df.empty else 0)
col3.metric("Latest Entry", df.iloc[-1]["Name"] if not df.empty else "None")

st.divider()

# ================= DATA TABLE ================= #
st.subheader("Attendance Records")
st.dataframe(df, use_container_width=True)

st.divider()

# ================= ANALYTICS (NO MATPLOTLIB) ================= #
st.subheader("Attendance Analytics")

if not df.empty:
    chart_data = df["Name"].value_counts().reset_index()
    chart_data.columns = ["Name", "Count"]

    fig = px.bar(
        chart_data, x="Name", y="Count", title="Attendance Frequency per Student"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No attendance data available yet.")

st.divider()

# ================= EXPORT SYSTEM ================= #
if st.session_state.role == "admin":
    st.subheader("Export Data")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Export CSV"):
            df.to_csv("attendance_export.csv", index=False)
            st.success("CSV exported successfully")

    with col2:
        if st.button("Export Excel"):
            df.to_excel("attendance_export.xlsx", index=False)
            st.success("Excel exported successfully")

    if st.button("Export PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        for i, row in df.iterrows():
            pdf.cell(200, 8, txt=str(row.values), ln=True)

        pdf.output("attendance_report.pdf")
        st.success("PDF exported successfully")

# ================= REFRESH ================= #
st.divider()

if st.button("Refresh Dashboard"):
    st.rerun()
