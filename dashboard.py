import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from fpdf import FPDF

# ================= CONFIG ================= #
FILE_PATH = "logs/attendance.csv"

st.set_page_config(page_title="Attendance Management System", layout="wide")

# ================= LOGIN SYSTEM ================= #
USERS = {"admin": "admin123", "student": "student123"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

if not st.session_state.logged_in:
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.role = username
            st.success(f"Welcome {username}")
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

# ================= SIDEBAR ================= #
st.sidebar.header("Controls")

search_name = st.sidebar.text_input("Search student")
show_all = st.sidebar.checkbox("Show full dataset", value=True)

st.sidebar.divider()
st.sidebar.info(f"Logged in as: {st.session_state.role}")

# ================= METRICS ================= #
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Records", len(df))

with col2:
    st.metric("Unique Students", df["Name"].nunique() if not df.empty else 0)

with col3:
    st.metric("Latest Entry", df.iloc[-1]["Name"] if not df.empty else "None")

st.divider()

# ================= DATA FILTER ================= #
filtered_df = df

if search_name:
    filtered_df = df[df["Name"].str.contains(search_name, case=False, na=False)]

# ================= TABLE ================= #
st.subheader("Attendance Records")

if show_all:
    st.dataframe(df, use_container_width=True)
else:
    st.dataframe(filtered_df, use_container_width=True)

st.divider()

# ================= CHARTS ================= #
st.subheader("Attendance Analytics")

if not df.empty:
    chart_data = df["Name"].value_counts()

    fig, ax = plt.subplots()
    chart_data.plot(kind="bar", ax=ax)

    ax.set_title("Attendance Frequency per Student")
    ax.set_xlabel("Student")
    ax.set_ylabel("Count")

    st.pyplot(fig)
else:
    st.info("No data available for charts.")

st.divider()

# ================= EXPORT (ADMIN ONLY) ================= #
if st.session_state.role == "admin":
    st.subheader("Export Data")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Export to Excel"):
            df.to_excel("attendance.xlsx", index=False)
            st.success("Exported to attendance.xlsx")

    with col2:
        if st.button("Export to CSV"):
            df.to_csv("attendance_export.csv", index=False)
            st.success("Exported to attendance_export.csv")

    if st.button("Export to PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        for i, row in df.iterrows():
            pdf.cell(200, 8, txt=str(row.values), ln=True)

        pdf.output("attendance.pdf")
        st.success("Exported to attendance.pdf")

st.divider()

# ================= SEARCH ================= #
st.subheader("Search Student")

if search_name:
    st.dataframe(filtered_df, use_container_width=True)

# ================= REFRESH ================= #
if st.button("Refresh Dashboard"):
    st.rerun()
