import streamlit as st

st.title("Main Page")
st.write('''
This is Main Page.
''')

ASOAP = st.Page(
    "Pages/ASOAP.py", title="ASOAP", icon=":material/dashboard:", default=True
)

Beneficiary = st.Page(
    "Pages/Beneficiary.py", title="Beneficiary", icon=":material/dashboard:", default=True
)

Tools = st.Page(
    "Pages/Tools.py", title="Tools", icon=":material/dashboard:", default=True
)

pg = st.navigation(
    {
        "Files": [Tools],
        "Data": [ASOAP, Beneficiary],
    }
)