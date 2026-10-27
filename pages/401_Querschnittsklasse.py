import streamlit as st
import math
from formatting import *

# ---------------------------------------------------------
# Seiteneinstellungen
# ---------------------------------------------------------

st.title("Querschnittsklassifizierung")
st.caption("Klassifizierung von I-Querschnitten nach DIN EN 1993-1-1")

st.info("Steg und Flansch werden separat klassifiziert. Die ungünstigere Querschnittsklasse ist für den Gesamtquerschnitt maßgebend.")

# ---------------------------------------------------------
# 1. Eingaben
# ---------------------------------------------------------

st.header("1. Eingaben")

col1, col2, col3 = st.columns(3)

with col1:
    h1_black("Position")

    position = st.text_input(
        "Position",
        value="Träger"
    )
    
with col2:  
    h1_black("Profil")  
    querschnitt = st.text_input(
         "Querschnittsbezeichnung",
         value="IPE 300",
     )  
    
with col3:
    h1_black("Güte") 
    stahlsorte = st.selectbox(
            "Stahlsorte",
            options=["S235", "S275", "S355", "S420", "S460", "Benutzerdefiniert"],
            index=0,
        )

    fy_standard = {
        "S235": 235.0,
        "S275": 275.0,
        "S355": 355.0,
        "S420": 420.0,
        "S460": 460.0,
    }

    if stahlsorte == "Benutzerdefiniert":
        fy = st.number_input(
            "Streckgrenze f_y [N/mm²]",
            min_value=1.0,
            value=355.0,
            step=5.0,
        )
    else:
        fy = fy_standard[stahlsorte]        


col1, col2, col3 = st.columns(3)

with col1:
    h1_black("Spannung +")
    sigma_1 = st.number_input("σ1 [N/mm²]", value=355.0, step=5.0)

with col2:
    h1_black("Spannung -")
    sigma_2 = st.number_input("σ2 [N/mm²]", value=-100.0, step=5.0)

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    h1_black("Höhe")
    h = st.number_input("Höhe h [mm]", min_value=1.0, value=3500.0, step=10.0)

with col2:
    h1_black("Breite")
    b = st.number_input("Breite b [mm]", min_value=1.0, value=1500.0, step=10.0)

with col3:
    h1_black("Steg")
    tw = st.number_input("Stegdicke tw [mm]", min_value=0.1, value=25.0, step=1.0)
    
with col4:
    h1_black("Flansch")
    tf = st.number_input("Flanschdicke tf [mm]", min_value=0.1, value=50.0, step=1.0)
    
# ---------------------------------------------------------
# Berechnung
# ---------------------------------------------------------

c_w = h - 2 * tf
c_f = b - tw

epsilon = math.sqrt(235 / fy)
ct_w = c_w / tw
ct_f = c_f / tf

# Spannungsverhältnis Steg
psi = sigma_2 / sigma_1 if sigma_1 != 0 else 0.0

# Druckzonenanteil für lineare Spannungsverteilung
alpha = 1 / (1 - psi) if psi < 0 else 1.0
alpha = max(0.0, min(alpha, 1.0))

# ---------------------------------------------------------
# Steg – Klasse 1 und 2
# ---------------------------------------------------------

if alpha > 0.5:
    grenze_w_1 = 396 * epsilon / (13 * alpha - 1)
    grenze_w_2 = 456 * epsilon / (13 * alpha - 1)
else:
    grenze_w_1 = 36 * epsilon / alpha if alpha > 0 else float("inf")
    grenze_w_2 = 41.5 * epsilon / alpha if alpha > 0 else float("inf")

# Klasse 3
if psi > -1:
    grenze_w_3 = 42 * epsilon / (0.67 + 0.33 * psi)
else:
    grenze_w_3 = 62 * epsilon * (1 - psi) * math.sqrt(-psi)

if ct_w <= grenze_w_1:
    qk_steg = 1
elif ct_w <= grenze_w_2:
    qk_steg = 2
elif ct_w <= grenze_w_3:
    qk_steg = 3
else:
    qk_steg = 4

# ---------------------------------------------------------
# Flansch
# ---------------------------------------------------------

grenze_f_1 = 9 * epsilon
grenze_f_2 = 10 * epsilon
grenze_f_3 = 14 * epsilon

if ct_f <= grenze_f_1:
    qk_flansch = 1
elif ct_f <= grenze_f_2:
    qk_flansch = 2
elif ct_f <= grenze_f_3:
    qk_flansch = 3
else:
    qk_flansch = 4

# ---------------------------------------------------------
# Gesamtquerschnitt
# ---------------------------------------------------------

querschnittsklasse = max(qk_steg, qk_flansch)

# ---------------------------------------------------------
# 2. Nachweis
# ---------------------------------------------------------

st.header("2. Nachweis")
h1("Querschnittsklassifizierung")
caption("Klassifizierung der druckbeanspruchten Querschnittsteile")

h2("Material")
h3("Epsilon")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(r"\varepsilon=\sqrt{\frac{235}{f_y}}")
    
with result_col2:
    st.latex(rf"\varepsilon=\sqrt{{\frac{{235}}{{{fy:.0f}}}}}={epsilon:.3f}")

h2("Steg")
h3("Schlankheit und Spannungsverteilung")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(r"\frac{c}{t_w}")
    st.latex(rf"\frac{{c}}{{t_w}}=\frac{{{c_w:.1f}}}{{{tw:.1f}}}={ct_w:.2f}")

with result_col2:
    st.latex(r"\psi=\frac{\sigma_2}{\sigma_1}")
    st.latex(rf"\psi=\frac{{{sigma_2:.1f}}}{{{sigma_1:.1f}}}={psi:.3f}")

with result_col3:
    st.latex(r"\alpha=\frac{1}{1-\psi}")
    st.latex(rf"\alpha=\frac{{1}}{{1-({psi:.3f})}}={alpha:.3f}")

h3("Grenzwerte Steg")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"\left(\frac{{c}}{{t}}\right)_1={grenze_w_1:.2f}")

with result_col2:
    st.latex(rf"\left(\frac{{c}}{{t}}\right)_2={grenze_w_2:.2f}")

with result_col3:
    st.latex(rf"\left(\frac{{c}}{{t}}\right)_3={grenze_w_3:.2f}")

with result_col4:
    st.latex(rf"\mathrm{{QK}}_{{Steg}}={qk_steg}")

h2("Flansch")
h3("Schlankheit und Grenzwerte")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"\frac{{c}}{{t_f}}=\frac{{{c_f:.1f}}}{{{tf:.1f}}}={ct_f:.2f}")

with result_col2:
    st.latex(rf"\left(\frac{{c}}{{t}}\right)_1=9\varepsilon={grenze_f_1:.2f}")

with result_col3:
    st.latex(rf"\left(\frac{{c}}{{t}}\right)_2=10\varepsilon={grenze_f_2:.2f}")

with result_col4:
    st.latex(rf"\left(\frac{{c}}{{t}}\right)_3=14\varepsilon={grenze_f_3:.2f}")

h3("Flanschklassifizierung")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"\mathrm{{QK}}_{{Flansch}}={qk_flansch}")

h2("Gesamtquerschnitt")
h3("Maßgebende Querschnittsklasse")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(r"\mathrm{QK}=\max(\mathrm{QK}_{Steg},\mathrm{QK}_{Flansch})")

with result_col2:
    st.latex(rf"\mathrm{{QK}}=\max({qk_steg},{qk_flansch})={querschnittsklasse}")


# ---------------------------------------------------------
# Hinweise
# ---------------------------------------------------------

st.write("")
st.markdown(
    """
    - Steg und Flansch werden separat klassifiziert.
    - Die ungünstigere Klasse ist für den Gesamtquerschnitt maßgebend.
    - Bei Druck und Biegung hängt die Stegklassifizierung von der Spannungsverteilung ab.
    - Für Querschnittsklasse 4 sind gegebenenfalls effektive Querschnittswerte zu bestimmen.
    """
)