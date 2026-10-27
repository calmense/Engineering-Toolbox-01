# formatting.py

import streamlit as st

ARUP_RED = "#E30613"
ARUP_GREY = "#070707"


def h1_black(text):
    st.markdown(
        f"""
        <div style="
            font-family:'Times New Roman', Times, serif;
            color:{ARUP_GREY};
            font-size:30px;
            font-weight:400;
            margin-top:20px;
            margin-bottom:1px;">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )
    
def h1(text):
    st.markdown(
        f"""
        <div style="
            font-family:'Times New Roman', Times, serif;
            color:{ARUP_RED};
            font-size:30px;
            font-weight:400;
            margin-top:20px;
            margin-bottom:1px;">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )


def h2(text):
    st.markdown(
        f"""
        <div style="
            color:{ARUP_RED};
            font-size:20px;
            font-weight:700;
            margin-top:16px;
            margin-bottom:12px;">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )


def h3(text):
    st.markdown(
        f"""
        <div style="
            color:{ARUP_GREY};
            font-size:16px;
            font-weight:600;
            margin-top:12px;
            margin-bottom:8px;">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )   


def h4(text):
    st.markdown(
        f"""
        <div style="
            color:{ARUP_GREY};
            font-size:14px;
            font-weight:700;
            margin-top:10px;
            margin-bottom:6px;">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )
    
def caption(text):
    st.markdown(
        f"""
        <div style="
            font-family:'Times New Roman', Times, serif;
            color:{ARUP_GREY};
            font-size:14pt;
            font-style:italic;
            text-align:left;
            margin-top:0px;
            margin-bottom:10px;">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )    