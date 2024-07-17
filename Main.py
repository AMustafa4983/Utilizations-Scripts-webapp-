import streamlit as st

asoap = st.Page(
    "Pages/ASOAP.py", title="ASOAP", icon=":material/dashboard:", default=False
)

Beneficiary = st.Page(
    "Pages/Beneficiary.py", title="Beneficiary", icon=":material/dashboard:", default=False
)

Tools = st.Page(
    "Pages/Tools.py", title="Tools", icon=":material/dashboard:", default=True
)

pg = st.navigation(
    {
        "Files": [Tools],
        "Data": [asoap, Beneficiary],
    }
)

pg.run()