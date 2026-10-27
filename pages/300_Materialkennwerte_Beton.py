import streamlit as st
from Datenbank.Holz_Datenbank import materialkennwerte_Holz


st.set_page_config(
    page_title="Materialkennwerte Holz",
    layout="wide"
)

st.title("🌲 Materialkennwerte Holz")

# =====================================================
# 1. NORMGRUNDLAGE
# =====================================================

st.header("1. Normgrundlage")

st.caption("""
DIN EN 338 - Charakteristische Festigkeits- und Steifigkeitskennwerte
für Nadel- und Laubhölzer.

DIN EN 14080 - Charakteristische Festigkeits- und Steifigkeitskennwerte
für Brettschichtholz.
""")

# =====================================================
# 2. EINGABEWERTE
# =====================================================

st.header("2. Eingabewerte")

holzart = st.selectbox(
    "Holzart",
    [
        "Nadelholz",
        "Laubholz",
        "Brettschichtholz"
    ]
)

if holzart == "Nadelholz":

    festigkeitsklasse = st.selectbox(
        "Festigkeitsklasse",
        ["C16", "C24", "C30", "C35", "C40"]
    )

elif holzart == "Laubholz":

    festigkeitsklasse = st.selectbox(
        "Festigkeitsklasse",
        ["D30", "D35", "D40", "D60"]
    )

else:

    festigkeitsklasse = st.selectbox(
        "Festigkeitsklasse",
        ["GL24h", "GL24c", "GL28h", "GL28c",
         "GL30h", "GL30c", "GL32h", "GL32c"]
    )

# =====================================================
# MATERIALDATEN
# =====================================================

w = materialkennwerte_Holz[festigkeitsklasse]

# =====================================================
# 3. MATERIALKENNWERTE
# =====================================================

st.header("3. Materialkennwerte")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.latex(rf"f_{{m,k}} = {w['fmk']:.1f}\,\mathrm{{N/mm^2}}")
    st.latex(rf"f_{{t,0,k}} = {w['ft0k']:.1f}\,\mathrm{{N/mm^2}}")
    st.latex(rf"f_{{t,90,k}} = {w['ft90k']:.1f}\,\mathrm{{N/mm^2}}")


with col2:

    st.latex(rf"f_{{c,0,k}} = {w['fc0k']:.1f}\,\mathrm{{N/mm^2}}")
    st.latex(rf"f_{{c,90,k}} = {w['fc90k']:.1f}\,\mathrm{{N/mm^2}}")
    st.latex(rf"f_{{v,k}} = {w['fvk']:.1f}\,\mathrm{{N/mm^2}}")
    


with col3:

    st.latex(rf"E_{{0,mean}} = {w['E0mean']:.0f}\,\mathrm{{N/mm^2}}")
    st.latex(rf"E_{{0,05}} = {w['E005']:.0f}\,\mathrm{{N/mm^2}}")
    st.latex(rf"G_{{mean}} = {w['Gmean']:.00f}\,\mathrm{{N/mm^2}}")
    
with col4:

    st.latex(rf"G_{{0,05}} = {w['G05']:.0f}\,\mathrm{{N/mm^2}}")
    st.latex(rf"f_{{R,k}} = {w['frk']:.1f}\,\mathrm{{N/mm^2}}")
    st.latex(rf"\rho_k = {w['rho']:.0f}\,\mathrm{{kg/m^3}}")

# =====================================================
# 4. SESSION STATE
# =====================================================

for key, value in w.items():
    st.session_state[key] = value

st.session_state["holzart"] = holzart
st.session_state["festigkeitsklasse"] = festigkeitsklasse

