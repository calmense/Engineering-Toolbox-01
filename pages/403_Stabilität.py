import streamlit as st
from formatting import *
import math
import pandas as pd

# ---------------------------------------------------------
# Seiteneinstellungen
# ---------------------------------------------------------

st.title("Stabilitätsnachweis")

st.caption(
    "Auf Biegung und Druck beanspruchte gleichförmige Bauteile "
    "nach DIN EN 1993-1-1, Abschnitt 6.3.3"
)

# ---------------------------------------------------------
# Eingaben
# ---------------------------------------------------------

st.header("1. Eingaben")

col1, col2, col3 = st.columns(3)

# ---------------------------------------------------------
# Allgemeine Angaben
# ---------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    h1_black("Position")
    position = st.text_input("Position", value="Versteifungsträger")

with col2:
    h1_black("Profil")
    querschnitt = st.text_input("Querschnittsbezeichnung", value="STDx3500x1500x25x50")

with col3:
    h1_black("Güte")
    stahlsorte = st.selectbox("Stahlsorte", options=["S235", "S275", "S355", "S420", "S460", "Benutzerdefiniert"], index=0)
    fy_standard = {"S235": 235.0, "S275": 275.0, "S355": 355.0, "S420": 420.0, "S460": 460.0}
    if stahlsorte == "Benutzerdefiniert":
        fy = st.number_input("Streckgrenze f_y [N/mm²]", min_value=1.0, value=355.0, step=5.0)
    else:
        fy = fy_standard[stahlsorte]

with col4:
    h1_black("Querschnittsklasse")
    querschnittsklasse = st.selectbox("Querschnittsklasse", options=[1, 2, 3, 4], index=3)


h1_black("Geometrie")
col1, col2, col3, col4 = st.columns(4)

with col1:
    h = st.number_input("Höhe h [cm]", value=350.00)
    b = st.number_input("Breite b [cm]", value=150.00)

with col2:
    tf = st.number_input("Flanschdicke tf [cm]", value=5.00)
    tw = st.number_input("Stegdicke tw [cm]", value=2.500)

with col3:
    Lcry = st.number_input("Knicklänge Lcr,y [m]", value=27.60)
    Lcrz = st.number_input("Knicklänge Lcr,z [m]", value=3.45)


h1_black("Belastung")
col1, col2, col3, col4 = st.columns(4)

with col1:
    N_Ed = st.number_input("Normalkraft N_Ed [kN]", value=9200.00)

with col2:
    My_Ed = st.number_input("Biegemoment My_Ed [kNm]", value=4000.00)


st.divider()

# ---------------------------------------------------------
# Berechnung
# ---------------------------------------------------------

gamma_M1 = 1.1
cmy = 1.0  # konservativ: günstiger Momentenverlauf wird nicht berücksichtigt

def get_knicklinie_I(h, b, tf, stahl, achse):
    if h / b > 1.2:
        if tf <= 40:
            return "a0" if stahl == "S460" else ("a" if achse == "y-y" else "b")
        elif tf <= 100:
            return "a" if stahl == "S460" else ("b" if achse == "y-y" else "c")
    else:
        if tf <= 100:
            return "a" if stahl == "S460" else ("b" if achse == "y-y" else "c")
        else:
            return "c" if stahl == "S460" else "d"

alpha_values = {"a0": 0.13, "a": 0.21, "b": 0.34, "c": 0.49, "d": 0.76}

# ---------------------------------------------------------
# Querschnittswerte
# ---------------------------------------------------------

hw = h - 2 * tf
A = 2 * b * tf + hw * tw
Iy = 2 * (b * tf**3 / 12 + b * tf * ((h - tf) / 2)**2) + tw * hw**3 / 12
Iz = 2 * (tf * b**3 / 12) + hw * tw**3 / 12
iy = (Iy / A) ** 0.5
iz = (Iz / A) ** 0.5
IT = (2 * b * tf**3 + hw * tw**3) / 3
Iw = tf * b**3 * (h - tf)**2 / 24
zp = -h / 2
xi = 1.12

NRk = A * fy / 1000
Wpl_y = Iy / (h / 2)
Wel_y = Wpl_y

if querschnittsklasse in [1, 2]:
    Wy_Rk = Wpl_y
    My_Rk = Wpl_y * fy / 1e6
elif querschnittsklasse == 3:
    Wy_Rk = Wel_y
    My_Rk = Wel_y * fy / 1e6
else:
    Wy_Rk = Wel_y
    My_Rk = Wel_y * fy / 1e6
    st.warning("Für Querschnittsklasse 4 sind für den endgültigen Nachweis die wirksamen Querschnittswerte Aeff bzw. Weff erforderlich. Aktuell werden näherungsweise die Bruttoquerschnittswerte verwendet.")

# ---------------------------------------------------------
# Knickschlankheit y-y
# Lcr,y = volle Trägerlänge
# ---------------------------------------------------------

lambda_y = (Lcry * 100) / ((iy / 10) * 93.9)
lambda_z = (Lcrz * 100) / ((iz / 10) * 93.9)

# ---------------------------------------------------------
# EC3-Knicklinie y-y
# ---------------------------------------------------------

kl_y = get_knicklinie_I(h, b, tf, stahlsorte, "y-y")
alpha_y = alpha_values[str(kl_y)]

# ---------------------------------------------------------
# Abminderungsfaktor χy
# ---------------------------------------------------------

phi_y = 0.5 * (1 + alpha_y * (lambda_y - 0.2) + lambda_y**2)
chi_y_unbounded = 1 / (phi_y + math.sqrt(max(0.0, phi_y**2 - lambda_y**2)))
chi_y = min(1.0, chi_y_unbounded)

# ---------------------------------------------------------
# Biegedrillknicken
# Lcr,z = Abstand der seitlichen Halterungen = 3,45 m
# ---------------------------------------------------------

Iz_cm4 = Iz / 1e4
IT_cm4 = IT / 1e4
Iw_cm6 = Iw / 1e6
zp_cm = zp / 10
Lcrz_cm = Lcrz * 100

Ncr_z = math.pi**2 * 21000 * Iz_cm4 / Lcrz_cm**2

c_squared = (Iw_cm6 + 0.039 * Lcrz_cm**2 * IT_cm4) / Iz_cm4

Mcr = xi * Ncr_z * (math.sqrt(c_squared + 0.25 * zp_cm**2) + 0.5 * zp_cm) * 1e-2

lambda_LT = math.sqrt(My_Rk / Mcr)

# ---------------------------------------------------------
# Abminderungsfaktor χLT
# ---------------------------------------------------------

alpha_LT = alpha_y

phi_LT = 0.5 * (1 + alpha_LT * (lambda_LT - 0.2) + lambda_LT**2)

chi_LT_unbounded = 1 / (
    phi_LT + math.sqrt(max(0.0, phi_LT**2 - lambda_LT**2))
)

chi_LT = min(1.0, chi_LT_unbounded)

# ---------------------------------------------------------
# Interaktionsbeiwert kyy
# Cmy = 1,0 konservativ angesetzt
# ---------------------------------------------------------

kyy_1 = cmy * (
    1
    + (lambda_y - 0.2)
    * N_Ed
    * gamma_M1
    / (chi_y * NRk)
)

kyy_2 = cmy * (
    1
    + 0.8
    * N_Ed
    * gamma_M1
    / (chi_y * NRk)
)

kyy = min(kyy_1, kyy_2, 1.8)

# ---------------------------------------------------------
# Interaktionsnachweis
# Druck + einachsige Biegung My
# ---------------------------------------------------------

eta_y = (
    N_Ed / (chi_y * NRk / gamma_M1)
    + kyy * My_Ed / (chi_LT * My_Rk / gamma_M1)
)

# ---------------------------------------------------------
# 2. Nachweis
# ---------------------------------------------------------

st.header("2. Nachweis")

h1("Stabilitätsnachweis")
caption("Nachweis bei Druck und einaxiale Biegung nach DIN EN 1993-1-1")

h2("Eingabewerte")

input_col1, input_col2, input_col3, input_col4 = st.columns(4)

with input_col1:
    st.latex(rf"h={h:.0f}\,\mathrm{{mm}}")
    st.latex(rf"N_{{Ed}}={N_Ed:.2f}\,\mathrm{{kN}}")

with input_col2:
    st.latex(rf"b={b:.0f}\,\mathrm{{mm}}")
    st.latex(rf"M_{{y,Ed}}={My_Ed:.2f}\,\mathrm{{kNm}}")

with input_col3:
    st.latex(rf"t_f={tf:.0f}\,\mathrm{{mm}}")
    st.latex(rf"L_{{cr,y}}={Lcry:.2f}\,\mathrm{{m}}")

with input_col4:
    st.latex(rf"t_w={tw:.0f}\,\mathrm{{mm}}")
    st.latex(rf"L_{{cr,z}}={Lcrz:.2f}\,\mathrm{{m}}")

# ---------------------------------------------------------
# Steifigkeitswerte
# ---------------------------------------------------------

h2("Steifigkeitswerte")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"h_w=h-2t_f={h/10:.1f}-2\cdot{tf/10:.1f}={hw/10:.1f}\,\mathrm{{cm}}\quad\text{{(Steghöhe)}}")
    st.latex(rf"A=2bt_f+h_wt_w=2\cdot{b/10:.1f}\cdot{tf/10:.1f}+{hw/10:.1f}\cdot{tw/10:.1f}={A/100:.1f}\,\mathrm{{cm^2}}\quad\text{{(Querschnittsfläche)}}")
    st.latex(rf"I_y=2\left(\frac{{bt_f^3}}{{12}}+bt_f\left(\frac{{h-t_f}}{{2}}\right)^2\right)+\frac{{t_wh_w^3}}{{12}}={Iy/1e4:.0f}\,\mathrm{{cm^4}}\quad\text{{(Flächenträgheitsmoment y)}}")
    st.latex(rf"I_z=2\frac{{t_fb^3}}{{12}}+\frac{{h_wt_w^3}}{{12}}={Iz/1e4:.0f}\,\mathrm{{cm^4}}\quad\text{{(Flächenträgheitsmoment z)}}")
    st.latex(rf"i_y=\sqrt{{\frac{{I_y}}{{A}}}}=\sqrt{{\frac{{{Iy/1e4:.0f}\,\mathrm{{cm^4}}}}{{{A/100:.1f}\,\mathrm{{cm^2}}}}}}={iy/10:.2f}\,\mathrm{{cm}}\quad\text{{(Trägheitsradius y)}}")
    st.latex(rf"i_z=\sqrt{{\frac{{I_z}}{{A}}}}=\sqrt{{\frac{{{Iz/1e4:.0f}\,\mathrm{{cm^4}}}}{{{A/100:.1f}\,\mathrm{{cm^2}}}}}}={iz/10:.2f}\,\mathrm{{cm}}\quad\text{{(Trägheitsradius z)}}")
    st.latex(rf"I_T=\frac{{2bt_f^3+h_wt_w^3}}{{3}}=\frac{{2\cdot{b/10:.1f}\cdot({tf/10:.1f})^3+{hw/10:.1f}\cdot({tw/10:.1f})^3}}{{3}}={IT/1e4:.0f}\,\mathrm{{cm^4}}\quad\text{{(Torsionsträgheitsmoment)}}")
    st.latex(rf"I_w=\frac{{t_fb^3(h-t_f)^2}}{{24}}=\frac{{{tf/10:.1f}\cdot({b/10:.1f})^3\cdot({h/10:.1f}-{tf/10:.1f})^2}}{{24}}={Iw/1e6:.0f}\,\mathrm{{cm^6}}\quad\text{{(Wölbträgheitsmoment)}}")
    st.latex(rf"z_p=-\frac{{h}}{{2}}=-\frac{{{h/10:.1f}}}{{2}}={zp/10:.1f}\,\mathrm{{cm}}\quad\text{{(Polkoordinate)}}")
    st.latex(rf"\xi={xi:.2f}\quad\text{{(Momentenbeiwert - Einfeldträger (ungünstig))}}")
    
# ---------------------------------------------------------
# Knicken
# ---------------------------------------------------------

h2("Knicken")
h3("Knickschlankheit")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"\bar{{\lambda}}_y=\frac{{L_{{cr,y}}}}{{i_y\cdot93.9}}=\frac{{{Lcry*100:.0f}\,\mathrm{{cm}}}}{{{iy/10:.2f}\,\mathrm{{cm}}\cdot93.9}}={lambda_y:.3f}")


h3("Knicklinien")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"\mathrm{{Knicklinie}}\ y-y:\ {kl_y}\Rightarrow\alpha_y={alpha_y:.2f}")

h3("Abminderungsbeiwerte")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"\Phi_y=\frac{{1}}{{2}}\left[1+\alpha_y\left(\bar{{\lambda}}_y-0.2\right)+\bar{{\lambda}}_y^2\right]=\frac{{1}}{{2}}\left[1+{alpha_y:.2f}\left({lambda_y:.3f}-0.2\right)+{lambda_y:.3f}^2\right]={phi_y:.3f}")
    st.latex(rf"\chi_y=\frac{{1}}{{\Phi_y+\sqrt{{\Phi_y^2-\bar{{\lambda}}_y^2}}}}=\frac{{1}}{{{phi_y:.3f}+\sqrt{{{phi_y:.3f}^2-{lambda_y:.3f}^2}}}}={chi_y_unbounded:.3f}\;\rightarrow\;\chi_y=\min\left(1.0,{chi_y_unbounded:.3f}\right)={chi_y:.3f}")

# ---------------------------------------------------------
# Biegedrillknicken
# ---------------------------------------------------------

h2("Biegedrillknicken")
h3("Kritische Werte")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"N_{{cr,z}}=\frac{{\pi^2 E I_z}}{{L_{{cr,z}}^2}}=\frac{{\pi^2\cdot21000\,\mathrm{{kN/cm^2}}\cdot{Iz_cm4:.0f}\,\mathrm{{cm^4}}}}{{({Lcrz*100:.0f}\,\mathrm{{cm}})^2}}={Ncr_z:.0f}\,\mathrm{{kN}}")
    st.latex(rf"c^2=\frac{{I_w+0.039\,L_{{cr,z}}^2 I_T}}{{I_z}}=\frac{{{Iw_cm6:.0f}\,\mathrm{{cm^6}}+0.039\cdot({Lcrz*100:.0f}\,\mathrm{{cm}})^2\cdot{IT_cm4:.0f}\,\mathrm{{cm^4}}}}{{{Iz_cm4:.0f}\,\mathrm{{cm^4}}}}={c_squared:.0f}\,\mathrm{{cm^2}}")
    st.latex(r"M_{cr}=\xi N_{cr,z}\left(\sqrt{c^2+0.25z_p^2}+0.5z_p\right)")
    st.latex(rf"M_{{cr}}={xi:.2f}\cdot{Ncr_z:.0f}\,\mathrm{{kN}}\left(\sqrt{{{c_squared:.0f}\,\mathrm{{cm^2}}+0.25\cdot({zp_cm:.0f}\,\mathrm{{cm}})^2}}+0.5\cdot({zp_cm:.0f}\,\mathrm{{cm}})\right)\cdot10^{{-2}}={Mcr:.0f}\,\mathrm{{kNm}}")

# ---------------------------------------------------------
# Biegedrillknickschlankheit
# ---------------------------------------------------------

h3("Biegedrillknickschlankheit")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"\bar{{\lambda}}_{{LT}}=\sqrt{{\frac{{M_{{y,Rk}}}}{{M_{{cr}}}}}}=\sqrt{{\frac{{{My_Rk:.0f}\,\mathrm{{kNm}}}}{{{Mcr:.0f}\,\mathrm{{kNm}}}}}}={lambda_LT:.3f}")
    st.latex(rf"\Phi_{{LT}}=\frac{{1}}{{2}}\left[1+\alpha_{{LT}}\left(\bar{{\lambda}}_{{LT}}-0.2\right)+\bar{{\lambda}}_{{LT}}^2\right]=\frac{{1}}{{2}}\left[1+{alpha_LT:.2f}\left({lambda_LT:.3f}-0.2\right)+{lambda_LT:.3f}^2\right]={phi_LT:.3f}")
    st.latex(rf"\chi_{{LT}}=\frac{{1}}{{\Phi_{{LT}}+\sqrt{{\Phi_{{LT}}^2-\bar{{\lambda}}_{{LT}}^2}}}}=\frac{{1}}{{{phi_LT:.3f}+\sqrt{{{phi_LT:.3f}^2-{lambda_LT:.3f}^2}}}}={chi_LT_unbounded:.3f}\;\rightarrow\;\chi_{{LT}}=\min\left(1.0,{chi_LT_unbounded:.3f}\right)={chi_LT:.3f}")

# ---------------------------------------------------------
# Interaktionsbeiwerte
# ---------------------------------------------------------

h2("Interaktionsbeiwerte")
h3("Äquivalenter Momentenbeiwert Cmy")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"C_{{my}}={cmy:.2f}\quad\text{{(konservativ, günstiger Momentenverlauf unberücksichtigt)}}")

h3("Interaktionsbeiwert kyy")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(r"k_{yy,1}=C_{my}\left[1+\left(\bar{\lambda}_y-0.2\right)\frac{N_{Ed}\gamma_{M1}}{\chi_y N_{Rk}}\right]")
    st.latex(rf"k_{{yy,1}}={cmy:.2f}\left[1+\left({lambda_y:.3f}-0.2\right)\frac{{{N_Ed:.0f}\cdot{gamma_M1:.2f}}}{{{chi_y:.3f}\cdot{NRk:.0f}}}\right]={kyy_1:.3f}")

    st.latex(r"k_{yy,2}=C_{my}\left[1+0.8\frac{N_{Ed}\gamma_{M1}}{\chi_y N_{Rk}}\right]")
    st.latex(rf"k_{{yy,2}}={cmy:.2f}\left[1+0.8\cdot\frac{{{N_Ed:.0f}\cdot{gamma_M1:.2f}}}{{{chi_y:.3f}\cdot{NRk:.0f}}}\right]={kyy_2:.3f}")

    st.latex(rf"k_{{yy}}=\min\left({kyy_1:.3f},{kyy_2:.3f},1.8\right)={kyy:.3f}")

# ---------------------------------------------------------
# Nachweis
# ---------------------------------------------------------

h2("Nachweis")
h3("Interaktionsnachweise")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(r"\eta_y=\frac{N_{Ed}}{\chi_y\cdot N_{Rk}/\gamma_{M1}}+k_{yy}\cdot\frac{M_{y,Ed}}{\chi_{LT}\cdot M_{y,Rk}/\gamma_{M1}}\leq1.0")
    st.latex(rf"\eta_y=\frac{{{N_Ed:.0f}\,\mathrm{{kN}}}}{{{chi_y:.3f}\cdot{NRk:.0f}\,\mathrm{{kN}}/{gamma_M1:.2f}}}+{kyy:.3f}\cdot\frac{{{My_Ed:.0f}\,\mathrm{{kNm}}}}{{{chi_LT:.3f}\cdot{My_Rk:.0f}\,\mathrm{{kNm}}/{gamma_M1:.2f}}}={eta_y:.3f}\leq1.0")

# ---------------------------------------------------------
# Hinweise zum vereinfachten Nachweis
# ---------------------------------------------------------

h3("Hinweise")

st.caption(
    "Der Stabilitätsnachweis wird für Drucknormalkraft und einachsige Biegung My geführt. "
    "Ein Biegemoment Mz wird nicht berücksichtigt. Für das Knicken um y-y wird die angesetzte "
    "Knicklänge Lcr,y verwendet. Die seitliche Stabilisierung des Versteifungsträgers erfolgt "
    "durch die Querträger im Abstand Lcr,z = 3,45 m. Auf die Ausnutzung eines günstigen "
    "Momentenverlaufs wird verzichtet; der äquivalente Momentenbeiwert wird konservativ mit Cmy = 1,0 angesetzt."
)

if querschnittsklasse == 4:
    st.warning(
        "Hinweis: Bei Querschnittsklasse 4 sind für den endgültigen Nachweis die wirksamen "
        "Querschnittswerte Aeff und Weff zu berücksichtigen. Der derzeitige Nachweis verwendet "
        "hierfür näherungsweise die Bruttoquerschnittswerte."
    )