import streamlit as st
from Datenbank.Stahl_Datenbank import materialkennwerte_Stahl


st.set_page_config(
    page_title="Materialkennwerte Stahl",
    layout="wide"
)

st.title("Materialkennwerte Stahl")

st.caption("""
DIN EN 10025-2 - Charakteristische Streckgrenzen und Zugfestigkeiten
für Baustähle.
""")

# =====================================================
# 1. EINGABEWERTE
# =====================================================

st.header("1. Eingabewerte")

col1, col2 = st.columns(2)

with col1:

    stahlgüte = st.selectbox(
        "Stahlgüte",
        [
            "S235",
            "S275",
            "S355",
            "S450"
        ]
    )

with col2:

    dicke = st.selectbox(
        "Erzeugnisdicke t",
        [
            "t ≤ 40 mm",
            "40 mm < t ≤ 80 mm"
        ]
    )

# =====================================================
# DATENBANK
# =====================================================


w = materialkennwerte_Stahl[stahlgüte][dicke]

# =====================================================
# 2. MATERIALKENNWERTE
# =====================================================

st.header("2. Materialkennwerte")

col1, col2 = st.columns(2)

with col1:

    st.latex(
        rf"f_y = {w['fy']:.0f}\,\mathrm{{N/mm^2}}"
    )

with col2:

    st.latex(
        rf"f_u = {w['fu']:.0f}\,\mathrm{{N/mm^2}}"
    )

# =====================================================
# 3. ÜBERSICHT
# =====================================================

st.header("3. Übersicht")

table = [

    {
        "Stahlgüte": "S235",
        "Dicke": "t ≤ 40 mm",
        "fy [N/mm²]": 235,
        "fu [N/mm²]": 360
    },
    {
        "Stahlgüte": "S235",
        "Dicke": "40 mm < t ≤ 80 mm",
        "fy [N/mm²]": 215,
        "fu [N/mm²]": 360
    },

    {
        "Stahlgüte": "S275",
        "Dicke": "t ≤ 40 mm",
        "fy [N/mm²]": 275,
        "fu [N/mm²]": 430
    },
    {
        "Stahlgüte": "S275",
        "Dicke": "40 mm < t ≤ 80 mm",
        "fy [N/mm²]": 255,
        "fu [N/mm²]": 410
    },

    {
        "Stahlgüte": "S355",
        "Dicke": "t ≤ 40 mm",
        "fy [N/mm²]": 355,
        "fu [N/mm²]": 490
    },
    {
        "Stahlgüte": "S355",
        "Dicke": "40 mm < t ≤ 80 mm",
        "fy [N/mm²]": 335,
        "fu [N/mm²]": 470
    },

    {
        "Stahlgüte": "S450",
        "Dicke": "t ≤ 40 mm",
        "fy [N/mm²]": 440,
        "fu [N/mm²]": 550
    },
    {
        "Stahlgüte": "S450",
        "Dicke": "40 mm < t ≤ 80 mm",
        "fy [N/mm²]": 410,
        "fu [N/mm²]": 550
    }

]

st.data_editor(
    table,
    hide_index=True,
    disabled=True,
    use_container_width=True
)

# =====================================================
# 5. SESSION STATE
# =====================================================

st.session_state["stahlgüte"] = stahlgüte
st.session_state["fy"] = w["fy"]
st.session_state["fu"] = w["fu"]

