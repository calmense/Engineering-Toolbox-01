import streamlit as st
from formatting import *
import math

# ---------------------------------------------------------
# Seiteneinstellungen
# ---------------------------------------------------------

st.title("Schweißnahtnachweis")
st.caption(
    "Kehlnahtnachweis nach DIN EN 1993-1-8, Abschnitt 4.5.3.3"
)

st.info(
    "Nachweis einer rechtwinkligen Kehlnaht nach dem "
    "vereinfachten Verfahren."
)

# ---------------------------------------------------------
# Eingaben
# ---------------------------------------------------------

st.header("1. Eingaben")

col1, col2, col3 = st.columns(3)

with col1:
    h1_black("Position")

    position = st.text_input(
        "Position",
        value="Treppenwange / Anschlussblech",
    )

with col2:
    h1_black("Schweißnaht")

    a_w = st.number_input(
        "Kehlnahtdicke a_w [mm]",
        min_value=3.0,
        value=3.0,
        step=1.0,
    )

    l_eff = st.number_input(
        "Wirksame Nahtlänge l_eff [mm]",
        min_value=10.0,
        value=480.0,
        step=10.0,
    )

with col3:
    h1_black("Material")

    stahlsorte = st.selectbox(
        "Stahlgüte",
        ["S235", "S275", "S355", "S420", "S460"],
        index=2,
    )

st.divider()

# ---------------------------------------------------------
# Beanspruchungen
# ---------------------------------------------------------

h1_black("Beanspruchungen")

col1, col2, col3 = st.columns(3)

with col1:

    F_perp = st.number_input(
        "F⊥,Ed [kN]",
        value=1.50,
        step=0.10,
    )


with col2:
    
    F_para = st.number_input(
            "F∥,Ed [kN]",
            value=0.50,
            step=0.10,
        )
    

with col3:
    
    M_Ed = st.number_input(
            "M_Ed [kNm]",
            value=0.00,
            step=0.10,
        )


# ---------------------------------------------------------
# Materialwerte
# ---------------------------------------------------------

fu_werte = {
    "S235": 360,
    "S275": 430,
    "S355": 510,
    "S420": 520,
    "S460": 550,
}

fu = fu_werte[stahlsorte]

beta_w = 0.80

# ---------------------------------------------------------
# Berechnung
# ---------------------------------------------------------

gamma_M2 = 1.25

l_eff_cm = l_eff / 10

N1_Ed = F_perp / l_eff_cm

if l_eff_cm > 0:
    N2_Ed = (M_Ed * 100) / (l_eff_cm**2 / 6)
else:
    N2_Ed = 0

V1_Ed = F_para / l_eff_cm

Fw_Ed = math.sqrt(
    N1_Ed**2 +
    N2_Ed**2 +
    V1_Ed**2
)

fvw_d = fu / (math.sqrt(3) * beta_w * gamma_M2)

Fw_Rd = fvw_d * a_w / 10

ausnutzung = Fw_Ed / Fw_Rd

nachweis_erfuellt = ausnutzung <= 1.0

# ---------------------------------------------------------
# Ergebnisse
# ---------------------------------------------------------

st.header("2. Nachweis")

with st.expander("Nachweis"):
    h1("Kehlnahtnachweis")
    caption("DIN EN 1993-1-8 Abschnitt 4.5.3.3")

    h2("System")

    st.image(
        "images/Schweißnaht.png",
        width=300,
    )

    caption(
        "Bild 1: Kraftkomponenten und Spannungen einer rechtwinkligen Kehlnaht "
        "nach DIN EN 1993-1-8, Abschnitt 4.5.3.3"
    )

    h2("Eingabewerte")
    h3("Schweißnaht")

    result_col1, result_col2, result_col3, result_col4 = st.columns(4)

    with result_col1:
        st.latex(rf"a_w={a_w:.1f}\,\mathrm{{mm}}")

    with result_col2:
        st.latex(rf"l_{{eff}}={l_eff:.0f}\,\mathrm{{mm}}")

    with result_col3:
        st.latex(rf"f_u={fu:.0f}\,\mathrm{{N/mm^2}} ({stahlsorte})")

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    h3("Belastung")

    result_col1, result_col2, result_col3, result_col4 = st.columns(4)

    with result_col1:
        st.latex(rf"F_{{\perp,Ed}}={F_perp:.2f}\,\mathrm{{kN}}")

    with result_col2:
        st.latex(rf"F_{{\parallel,Ed}}={F_para:.2f}\,\mathrm{{kN}}")

    with result_col3:
        st.latex(rf"M_{{Ed}}={M_Ed:.2f}\,\mathrm{{kNm}}")

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    h2("Nahtkräfte")
    h3("Nahtkräfte")

    result_col1, result_col2 = st.columns([2.5, 1])

    with result_col1:
        st.latex(
            rf"N_{{1,Ed}}=\frac{{F_{{\perp,Ed}}}}{{l_{{eff}}}}=\frac{{{F_perp:.2f}}}{{{l_eff_cm:.2f}}}={N1_Ed:.2f}\,\mathrm{{kN/cm}}\quad\mathrm{{(Nahtkraft\ aus\ senkrechter\ Kraft)}}"
        )

        st.latex(
            rf"V_{{Ed}}=\frac{{F_{{\parallel,Ed}}}}{{l_{{eff}}}}=\frac{{{F_para:.2f}}}{{{l_eff_cm:.2f}}}={V1_Ed:.2f}\,\mathrm{{kN/cm}}\quad\mathrm{{(Nahtkraft\ aus\ paralleler\ Kraft)}}"
        )
        
        st.latex(
            rf"N_{{2,Ed}}=\frac{{M_{{Ed}}}}{{l_{{eff}}^2/6}}=\frac{{{M_Ed*100:.2f}}}{{{l_eff_cm:.2f}^2/6}}={N2_Ed:.2f}\,\mathrm{{kN/cm}}\quad\mathrm{{(maximale\ Nahtkraft\ aus\ Biegemoment)}}"
        )

        
    h3("Resultierende Nahtkraft") 

    result_col1, result_col2 = st.columns([2.5, 1])
    

    with result_col1:
        st.latex(
            rf"F_{{w,Ed}}=\sqrt{{N_{{1,Ed}}^2+N_{{2,Ed}}^2+V_{{Ed}}^2}}=\sqrt{{({N1_Ed:.2f})^2+({N2_Ed:.2f})^2+({V1_Ed:.2f})^2}}={Fw_Ed:.2f}\,\mathrm{{kN/cm}}\quad\mathrm{{(resultierende\ Nahtkraft)}}\;[-1-8/(4.2)]"
        )

        
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    h2("Tragfähigkeit")

    result_col1, result_col2 = st.columns([2.5, 1])

    with result_col1:
        st.latex(
            rf"f_{{vw,d}}=\frac{{f_u}}{{\sqrt{{3}}\cdot\beta_w\cdot\gamma_{{M2}}}}=\frac{{{fu:.0f}}}{{\sqrt{{3}}\cdot{beta_w:.2f}\cdot{gamma_M2:.2f}}}={fvw_d:.1f}\,\mathrm{{N/mm^2}}\quad\mathrm{{(Bemessungswert\ der\ Schubfestigkeit)}}\;[-1-8/(4.4)]"
        )

        st.latex(
            rf"F_{{w,Rd}}=f_{{vw,d}}\cdot a_w={fvw_d:.1f}\cdot{a_w/10:.1f}={Fw_Rd:.2f}\,\mathrm{{kN/cm}}\quad\mathrm{{(Tragfähigkeit\ der\ Schweißnaht\ je\ Längeneinheit)}}\;[-1-8/(4.3)]"
        )

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    h2("Nachweis")

    result_col111, result_col222, result_col333, result_col444 = st.columns(4)

    with result_col111:
        st.latex(
        rf"\eta=\frac{{F_{{w,Ed}}}}{{F_{{w,Rd}}}}=\frac{{{Fw_Ed:.2f}}}{{{Fw_Rd:.2f}}}={ausnutzung:.3f}={ausnutzung*100:.0f}\,\%"
    )


# ---------------------------------------------------------
# Hinweise
# ---------------------------------------------------------

    h2("Hinweise")
    st.markdown(
        """
        - Vereinfachtes Verfahren nach DIN EN 1993-1-8.
        - Gültig für rechtwinklige Kehlnähte.
        - βw = 0,80 angesetzt.
        - γM2 = 1,25 als Standardwert.
        - Mindestkehlnahtdicken sind gesondert zu prüfen.
        - Mindestnahtlängen sind gesondert zu prüfen.
        """
    )