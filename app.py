import streamlit as st

st.set_page_config(page_title="Problem Standby List", page_icon="📚", layout="centered")

st.title("📚 Problem Standby List")
st.markdown("Welcome! Use the sidebar or the buttons below to navigate.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/1_Admin.py", label="🔧 Admin", icon="🔧")
    st.caption("Add, edit, or delete problems. Password protected.")

with col2:
    st.page_link("pages/2_View.py", label="📋 View", icon="📋")
    st.caption("Browse your full standby list.")
