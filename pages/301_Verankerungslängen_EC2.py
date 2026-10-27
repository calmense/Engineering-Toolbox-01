import streamlit as st
from Datenbank.Beton_Datenbank import lb_rqd

st.set_page_config(
    page_title="Verankerungslängen",
    layout="wide"
)

st.title("Verankerungslängen")

st.caption("""
DIN EN 1992-1-1 (Eurocode 2) - Abschnitt 8.4 Verankerung der Bewehrung
Verankerungslängen und Beiwertverfahren.
""")

# =====================================================
# 1. Grundwert der Verankerungslänge
# =====================================================

st.header("1. Grundwert der Verankerungslänge")

col1, col2, col3 = st.columns(3)

with col1:

    betonklasse = st.selectbox(
        "Betonfestigkeitsklasse",
        [
            "C12/15",
            "C16/20",
            "C20/25",
            "C25/30",
            "C30/37",
            "C35/45",
            "C40/50",
            "C45/55",
            "C50/60"
        ]
    )

with col2:

    verbund = st.selectbox(
        "Verbundbedingung",
        [
            "gut",
            "mäßig"
        ]
    )

with col3:

    phi = st.selectbox(
        "Stabdurchmesser ϕ [mm]",
        [6, 8, 10, 12, 14, 16, 20, 25, 28]
    )
    

lbrqd = lb_rqd[(betonklasse, verbund)][phi]


st.latex(
    rf"l_{{b,rqd}} = {lbrqd}\,\mathrm{{cm}}"
)


st.header("2. Verankerungslänge")

col1, col2 = st.columns(2)

with col1:

    stabart = st.selectbox(
        "Stabart",
        [
            "Gerader Stab",
            "Haken",
            "Winkelhaken",
            "Schlaufe"
        ]
    )

    belastung = st.selectbox(
        "Belastung",
        [
            "Zugstab",
            "Druckstab"
        ]
    )

with col2:

    querstaebe = st.selectbox(
        "Querstäbe",
        [
            "Keine",
            "Ein Querstab",
            "Zwei Querstäbe"
        ]
    )

    as_vorh_as_erf = st.number_input(
        "As,vorh / As,erf",
        value=1.00,
        min_value=1.00
    )

# =====================================================
# α1
# =====================================================

if stabart == "Gerader Stab":
    alpha1 = 1.0

elif stabart == "Haken":
    alpha1 = 0.7

elif stabart == "Winkelhaken":
    alpha1 = 0.7

elif stabart == "Schlaufe":
    alpha1 = 0.7

# =====================================================
# α4
# =====================================================

if querstaebe == "Keine":
    alpha4 = 1.0

elif querstaebe == "Ein Querstab":
    alpha4 = 0.7

else:
    alpha4 = 0.5

# =====================================================
# α5
# =====================================================

if as_vorh_as_erf <= 1.0:
    alpha5 = 1.0

else:
    alpha5 = max(
        0.70,
        1.0 - 0.04 * (as_vorh_as_erf - 1.0) * 10
    )

# =====================================================
# 3. BERECHNETE GRÖSSEN
# =====================================================

st.header("3. Berechnete Größen")

col1, col2, col3 = st.columns(3)

with col1:

    st.latex(
        rf"\alpha_1 = {alpha1:.2f}"
    )
    
with col2:
    st.latex(
        rf"\alpha_4 = {alpha4:.2f}"
    )
    
with col3:
    st.latex(
        rf"\alpha_5 = {alpha5:.2f}"
    )

with col2:

    produkt = alpha1 * alpha4 * alpha5
    lbd = produkt * lbrqd * as_vorh_as_erf

    st.latex(
        rf"\alpha_1 \cdot \alpha_4 \cdot \alpha_5 = {produkt:.3f}"
    )

    st.latex(
    rf"""
    l_{{bd}}
    =
    \alpha_1 \cdot \alpha_4 \cdot \alpha_5
    \cdot l_{{b,rqd}}
    \cdot \frac{{A_{{s,erf}}}}{{A_{{s,vorh}}}} = {lbd:.1f} cm
    """
)




