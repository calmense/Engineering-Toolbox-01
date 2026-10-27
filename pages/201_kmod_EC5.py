import streamlit as st

st.set_page_config(
    page_title="kmod",
    layout="wide"
)

st.title("kmod-Werte nach Eurocode 5")

st.caption("""
EN 1995-1-1 (Eurocode 5) - Tabelle 3.1: Modifikationsbeiwert kmod für Vollholz,
Brettschichtholz, Balkenschichtholz und Brettsperrholz.
""")

# =====================================================
# 2 EINGABEWERTE
# =====================================================

st.header("1. Eingabewerte")

col1, col2 = st.columns(2)

with col1:

    service_class = st.selectbox(
        "Nutzungsklasse",
        [
            "NK1",
            "NK2",
            "NK3"
        ]
    )

with col2:

    duration = st.selectbox(
        "Lasteinwirkungsdauer",
        [
            "Ständig",
            "Lang",
            "Mittel",
            "Kurz",
            "Sehr kurz"
        ]
    )

# =====================================================
# 2 BERECHNUNGEN
# =====================================================

st.header("2. Berechnete Größen")

kmod_table = {
    "NK1": {
        "Ständig": 0.60,
        "Lang": 0.70,
        "Mittel": 0.80,
        "Kurz": 0.90,
        "Sehr kurz": 1.10,
    },
    "NK2": {
        "Ständig": 0.60,
        "Lang": 0.70,
        "Mittel": 0.80,
        "Kurz": 0.90,
        "Sehr kurz": 1.10,
    },
    "NK3": {
        "Ständig": 0.50,
        "Lang": 0.55,
        "Mittel": 0.65,
        "Kurz": 0.70,
        "Sehr kurz": 0.90,
    }
}

kmod = kmod_table[service_class][duration]
gamma_M = 1.3

st.latex(
    rf"k_{{mod}} = {kmod:.2f}"
)


st.latex(
    rf"\gamma_M = {gamma_M:.2f}"
)

st.latex(
    rf"X = \frac{{k_{{mod}} }}{{\gamma_M}} = {kmod / gamma_M:.3f}"
)

# =====================================================
# 3 ERGEBNISSE
# =====================================================

st.header("3. Übersicht")

table_data = [
    {
        "Nutzungsklasse": "NK1",
        "Ständig": 0.60,
        "Lang": 0.70,
        "Mittel": 0.80,
        "Kurz": 0.90,
        "Sehr kurz": 1.10
    },
    {
        "Nutzungsklasse": "NK2",
        "Ständig": 0.60,
        "Lang": 0.70,
        "Mittel": 0.80,
        "Kurz": 0.90,
        "Sehr kurz": 1.10
    },
    {
        "Nutzungsklasse": "NK3",
        "Ständig": 0.50,
        "Lang": 0.55,
        "Mittel": 0.65,
        "Kurz": 0.70,
        "Sehr kurz": 0.90
    }
]

st.data_editor(
    table_data,
    disabled=True,
    hide_index=True,
    use_container_width=True
)

