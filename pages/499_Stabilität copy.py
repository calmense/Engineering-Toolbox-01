import streamlit as st
from formatting import *
import math

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

col1, col2, col3 = st.columns(3)

with col1:
    h1_black("Position")
    position = st.text_input("Position", value="Träger")

with col2:
    h1_black("Profil")
    querschnitt = st.text_input("Querschnittsbezeichnung", value="IPE 300")

with col3:
    h1_black("Güte")
    stahlsorte = st.selectbox("Stahlsorte", options=["S235", "S275", "S355", "S420", "S460", "Benutzerdefiniert"], index=0)
    fy_standard = {"S235": 235.0, "S275": 275.0, "S355": 355.0, "S420": 420.0, "S460": 460.0}
    if stahlsorte == "Benutzerdefiniert":
        fy = st.number_input("Streckgrenze f_y [N/mm²]", min_value=1.0, value=355.0, step=5.0)
    else:
        fy = fy_standard[stahlsorte]


with col1:
    h1_black("Querschnitt")
    h = st.number_input("Höhe h [mm]", value=300)
    b = st.number_input("Breite b [mm]", value=500)
    tf = st.number_input("Flansch tf [mm]", value=12)
    querschnittsklasse = st.selectbox("Querschnittsklasse", [1, 2, 3, 4], index=0)

with col2:
    h1_black("Beanspruchungen")
    N_Ed = st.number_input("Normalkraft NEd [kN]", min_value=0.0, value=300.0, step=10.0, format="%.2f")
    w_z = st.number_input("Linienlast wz,d [kN/m]", min_value=0.0, value=4.0, step=0.1, format="%.2f")
    My_Ed = st.number_input("Moment My,Ed [kNm]", value=32.0, step=1.0, format="%.2f")
    Mz_Ed = st.number_input("Moment Mz,Ed [kNm]", value=0.0, step=1.0, format="%.2f")

with col3:
    h1_black("Knicklängen")
    Lcry = st.number_input("Knicklänge Lcr,y [m]", min_value=0.1, value=8.0, step=0.1, format="%.2f")
    Lcrz = st.number_input("Knicklänge Lcr,z [m]", min_value=0.1, value=4.0, step=0.1, format="%.2f")


st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    h1_black("Widerstände")
    NRk = st.number_input("NRk [kN]", min_value=0.01, value=1264.3, step=10.0, format="%.2f")
    My_Rk = st.number_input("My,Rk [kNm]", min_value=0.01, value=100.9, step=1.0, format="%.2f")

with col2:
    h1_black("Querschnittswerte")
    Iz = st.number_input("Iz [cm⁴]", min_value=0.01, value=1340.0, step=10.0, format="%.2f")
    IT = st.number_input("IT [cm⁴]", min_value=0.01, value=21.0, step=1.0, format="%.2f")
    Iw = st.number_input("Iw [cm⁶]", min_value=0.01, value=108000.0, step=1000.0, format="%.0f")

with col3:
    h1_black("Querschnittswerte")
    iy = st.number_input("iy [cm]", min_value=0.01, value=8.28, step=0.01, format="%.2f")
    iz = st.number_input("iz [cm]", min_value=0.01, value=4.98, step=0.01, format="%.2f")
    zp = st.number_input("zp [cm]", value=-9.50, step=0.10, format="%.2f")
    xi = st.number_input("ξ [-]", min_value=0.01, value=1.35, step=0.01, format="%.2f")

st.divider()

# ---------------------------------------------------------
# Berechnung
# ---------------------------------------------------------

gamma_M1 = 1.1

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
# Knickschlankheiten
# ---------------------------------------------------------

lambda_y = (Lcry * 100) / (iy * 93.9)
lambda_z = (Lcrz * 100) / (iz * 93.9)

# ---------------------------------------------------------
# EC3-Knicklinie
# ---------------------------------------------------------

kl_y = get_knicklinie_I(h, b, tf, stahlsorte, "y-y")
kl_z = get_knicklinie_I(h, b, tf, stahlsorte, "z-z")

alpha_y = alpha_values[str(kl_y)]
alpha_z = alpha_values[str(kl_z)]

# ---------------------------------------------------------
# Abminderungsfaktoren χ
# ---------------------------------------------------------

phi_y = 0.5 * (1 + alpha_y * (lambda_y - 0.2) + lambda_y**2)
phi_z = 0.5 * (1 + alpha_z * (lambda_z - 0.2) + lambda_z**2)

chi_y = 1 / (phi_y + math.sqrt(phi_y**2 - lambda_y**2))
chi_z = 1 / (phi_z + math.sqrt(phi_z**2 - lambda_z**2))

# ---------------------------------------------------------
# Biegedrillknicken
# ---------------------------------------------------------

Ncr_z = math.pi**2 * 21000 * Iz / (Lcrz * 100)**2
c_squared = (Iw + 0.039 * (Lcrz * 100)**2 * IT) / Iz
Mcr = xi * Ncr_z * (math.sqrt(c_squared + 0.25 * zp**2) + 0.5 * zp) * 1e-2
lambda_LT = math.sqrt(My_Rk / Mcr)
phi_LT = 0.5 * (1 + alpha_y * (lambda_LT - 0.2) + lambda_LT**2)
chi_LT = 1 / (phi_LT + math.sqrt(phi_LT**2 - lambda_LT**2))
chi_LT = min(1.0, chi_LT)

# ---------------------------------------------------------
# Momentenbeiwerte
# ---------------------------------------------------------

alpha_h = 0.0
alpha_s = 0.75

cmy = 0.95 + 0.05 * alpha_h
cmz = 0.95 + 0.05 * alpha_h
cmLT = 0.20 + 0.80 * alpha_s

# ---------------------------------------------------------
# Interaktionsbeiwerte
# ---------------------------------------------------------

# ---------------------------------------------------------
# Interaktionsbeiwerte
# ---------------------------------------------------------

if querschnittsklasse in [1, 2]:
    kyy_1 = cmy * (1 + (lambda_y - 0.2) * N_Ed * gamma_M1 / (chi_y * NRk))
    kyy_2 = cmy * (1 + 0.8 * N_Ed * gamma_M1 / (chi_y * NRk))
    kyy = min(kyy_1, kyy_2)

    kzz_1 = cmz * (1 + (2 * lambda_z - 0.6) * N_Ed * gamma_M1 / (chi_z * NRk))
    kzz_2 = cmz * (1 + 1.4 * N_Ed * gamma_M1 / (chi_z * NRk))
    kzz = min(kzz_1, kzz_2)

    kyz = 0.6 * kzz

    kzy_1 = 1 - (0.1 * lambda_z / (cmLT - 0.25)) * N_Ed * gamma_M1 / (chi_z * NRk)
    kzy_2 = 1 - (0.1 / (cmLT - 0.25)) * N_Ed * gamma_M1 / (chi_z * NRk)

    if lambda_z < 0.4:
        kzy_3 = 0.6 + lambda_z
        kzy = min(max(kzy_1, kzy_2), kzy_3)
    else:
        kzy_3 = None
        kzy = max(kzy_1, kzy_2)

elif querschnittsklasse in [3, 4]:
    kyy_1 = cmy * (1 + 0.6 * lambda_y * N_Ed * gamma_M1 / (chi_y * NRk))
    kyy_2 = cmy * (1 + 0.6 * N_Ed * gamma_M1 / (chi_y * NRk))
    kyy = min(kyy_1, kyy_2)

    kzz_1 = cmz * (1 + 0.6 * lambda_z * N_Ed * gamma_M1 / (chi_z * NRk))
    kzz_2 = cmz * (1 + 0.6 * N_Ed * gamma_M1 / (chi_z * NRk))
    kzz = min(kzz_1, kzz_2)

    kyz = kzz

    kzy_1 = 1 - (0.05 * lambda_z / (cmLT - 0.25)) * N_Ed * gamma_M1 / (chi_z * NRk)
    kzy_2 = 1 - (0.05 / (cmLT - 0.25)) * N_Ed * gamma_M1 / (chi_z * NRk)
    kzy_3 = None
    kzy = max(kzy_1, kzy_2)

# ---------------------------------------------------------
# Interaktionsnachweise
# ---------------------------------------------------------

eta_y = N_Ed / (chi_y * NRk / gamma_M1) + kyy * (My_Ed ) / (chi_LT * My_Rk / gamma_M1) + kyz * (Mz_Ed ) / (Mz_Rk / gamma_M1)
eta_z = N_Ed / (chi_z * NRk / gamma_M1) + kzy * (My_Ed ) / (chi_LT * My_Rk / gamma_M1) + kzz * (Mz_Ed ) / (Mz_Rk / gamma_M1)

ausnutzung = max(eta_y,eta_z)
nachweis_erfuellt = ausnutzung <= 1.0

# ---------------------------------------------------------
# 2. Nachweis
# ---------------------------------------------------------

st.header("2. Nachweis")
h1("Stabilitätsnachweis")
caption("Nachweis bei Druck und Biegung nach DIN EN 1993-1-1")

h2("Knicken")
h3("Knickschlankheit")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"\bar{{\lambda}}_y=\frac{{L_{{cr,y}}}}{{i_y\cdot93.9}}=\frac{{{Lcry*100:.0f}}}{{{iy:.2f}\cdot93.9}}={lambda_y:.3f}")

with result_col2:
    st.latex(rf"\bar{{\lambda}}_z=\frac{{L_{{cr,z}}}}{{i_z\cdot93.9}}=\frac{{{Lcrz*100:.0f}}}{{{iz:.2f}\cdot93.9}}={lambda_z:.3f}")


h3("Knicklinien")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"\mathrm{{Knicklinie}}\ y-y:\ {kl_y}\Rightarrow\alpha_y={alpha_y:.2f}")

with result_col2:
    st.latex(rf"\mathrm{{Knicklinie}}\ z-z:\ {kl_z}\Rightarrow\alpha_z={alpha_z:.2f}")


h3("Abminderungsbeiwerte")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(r"\Phi_y=\frac{1}{2}\left[1+\alpha_y\left(\bar{\lambda}_y-0.2\right)+\bar{\lambda}_y^2\right]")
    st.latex(rf"\Phi_y=\frac{{1}}{{2}}\left[1+{alpha_y:.2f}({lambda_y:.3f}-0.2)+{lambda_y:.3f}^2\right]={phi_y:.3f}")

with result_col3:
    st.latex(r"\chi_y=\frac{1}{\Phi_y+\sqrt{\Phi_y^2-\bar{\lambda}_y^2}}")
    st.latex(rf"\chi_y=\frac{{1}}{{{phi_y:.3f}+\sqrt{{{phi_y:.3f}^2-{lambda_y:.3f}^2}}}}={chi_y:.3f}")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(r"\Phi_z=\frac{1}{2}\left[1+\alpha_z\left(\bar{\lambda}_z-0.2\right)+\bar{\lambda}_z^2\right]")
    st.latex(rf"\Phi_z=\frac{{1}}{{2}}\left[1+{alpha_z:.2f}({lambda_z:.3f}-0.2)+{lambda_z:.3f}^2\right]={phi_z:.3f}")

with result_col3:
    st.latex(r"\chi_z=\frac{1}{\Phi_z+\sqrt{\Phi_z^2-\bar{\lambda}_z^2}}")
    st.latex(rf"\chi_z=\frac{{1}}{{{phi_z:.3f}+\sqrt{{{phi_z:.3f}^2-{lambda_z:.3f}^2}}}}={chi_z:.3f}")


h2("Biegedrillknicken")
h3("Kritische Werte")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"N_{{cr,z}}=\frac{{\pi^2\cdot21000\cdot{Iz:.2f}}}{{{Lcrz*100:.0f}^2}}={Ncr_z:.2f}\,\mathrm{{kN}}")

with result_col3:
    st.latex(rf"c^2=\frac{{{Iw:.0f}+0.039\cdot{Lcrz*100:.0f}^2\cdot{IT:.2f}}}{{{Iz:.2f}}}={c_squared:.2f}\,\mathrm{{cm^2}}")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"M_{{cr}}={xi:.2f}\cdot{Ncr_z:.2f}\left(\sqrt{{{c_squared:.2f}+0.25({zp:.2f})^2}}+0.5({zp:.2f})\right)\cdot10^{{-2}}={Mcr:.2f}\,\mathrm{{kNm}}")


h3("Biegedrillknickschlankheit")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"\bar{{\lambda}}_{{LT}}=\sqrt{{\frac{{M_{{y,Rk}}}}{{M_{{cr}}}}}}=\sqrt{{\frac{{{My_Rk:.2f}}}{{{Mcr:.2f}}}}}={lambda_LT:.3f}")

with result_col3:
    st.latex(rf"\Phi_{{LT}}=\frac{{1}}{{2}}\left[1+{alpha_y:.2f}({lambda_LT:.3f}-0.2)+{lambda_LT:.3f}^2\right]={phi_LT:.3f}")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"\chi_{{LT}}=\frac{{1}}{{{phi_LT:.3f}+\sqrt{{{phi_LT:.3f}^2-{lambda_LT:.3f}^2}}}}={chi_LT:.3f}")


h2("Momentenbeiwerte")
h3("Äquivalente Momentenbeiwerte")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"c_{{my}}=0.95+0.05\cdot{alpha_h:.2f}={cmy:.3f}")

with result_col2:
    st.latex(rf"c_{{mLT}}=0.20+0.80\cdot{alpha_s:.2f}={cmLT:.3f}")


h2("Interaktionsbeiwerte")
h3("Interaktionsbeiwert kyy")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"k_{{yy,1}}={cmy:.2f}\left[1+({lambda_y:.3f}-0.2)\frac{{{N_Ed:.2f}\cdot{gamma_M1:.2f}}}{{{chi_y:.3f}\cdot{NRk:.2f}}}\right]={kyy_1:.3f}")

with result_col3:
    st.latex(rf"k_{{yy,2}}={cmy:.2f}\left[1+0.8\frac{{{N_Ed:.2f}\cdot{gamma_M1:.2f}}}{{{chi_y:.3f}\cdot{NRk:.2f}}}\right]={kyy_2:.3f}")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"k_{{yy}}=\min({kyy_1:.3f},{kyy_2:.3f},1.800)={kyy:.3f}")


h3("Interaktionsbeiwert kzy")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"k_{{zy,1}}=1-\frac{{0.1\cdot{lambda_z:.3f}}}{{{cmLT:.2f}-0.25}}\frac{{{N_Ed:.2f}\cdot{gamma_M1:.2f}}}{{{chi_z:.3f}\cdot{NRk:.2f}}}={kzy_1:.3f}")

with result_col3:
    st.latex(rf"k_{{zy,2}}=1-\frac{{0.1}}{{{cmLT:.2f}-0.25}}\frac{{{N_Ed:.2f}\cdot{gamma_M1:.2f}}}{{{chi_z:.3f}\cdot{NRk:.2f}}}={kzy_2:.3f}")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"k_{{zy,3}}=0.3\frac{{{N_Ed:.2f}\cdot{gamma_M1:.2f}}}{{{chi_z:.3f}\cdot{NRk:.2f}}}={kzy_3:.3f}")

with result_col3:
    st.latex(rf"k_{{zy}}=\max({kzy_1:.3f},{kzy_2:.3f},{kzy_3:.3f})={kzy:.3f}")


h2("Nachweis")
h3("Interaktionsnachweise")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(r"\eta_y=\frac{N_{Ed}}{\chi_y\cdot N_{Rk}/\gamma_{M1}}+k_{yy}\cdot\frac{M_{y,Ed}}{\chi_{LT}\cdot M_{y,Rk}/\gamma_{M1}}+k_{yz}\cdot\frac{M_{z,Ed}}{M_{z,Rk}/\gamma_{M1}}\leq1.0")
    st.latex(rf"\eta_y=\frac{{{N_Ed:.2f}}}{{{chi_y:.3f}\cdot{NRk:.2f}/{gamma_M1:.2f}}}+{kyy:.3f}\cdot\frac{{{My_Ed:.2f}}}{{{chi_LT:.3f}\cdot{My_Rk:.2f}/{gamma_M1:.2f}}}+{kyz:.3f}\cdot\frac{{{Mz_Ed:.2f}}}{{{Mz_Rk:.2f}/{gamma_M1:.2f}}}={eta_y:.3f}")

with result_col3:
    st.latex(r"\eta_z=\frac{N_{Ed}}{\chi_z\cdot N_{Rk}/\gamma_{M1}}+k_{zy}\cdot\frac{M_{y,Ed}}{\chi_{LT}\cdot M_{y,Rk}/\gamma_{M1}}+k_{zz}\cdot\frac{M_{z,Ed}}{M_{z,Rk}/\gamma_{M1}}\leq1.0")
    st.latex(rf"\eta_z=\frac{{{N_Ed:.2f}}}{{{chi_z:.3f}\cdot{NRk:.2f}/{gamma_M1:.2f}}}+{kzy:.3f}\cdot\frac{{{My_Ed:.2f}}}{{{chi_LT:.3f}\cdot{My_Rk:.2f}/{gamma_M1:.2f}}}+{kzz:.3f}\cdot\frac{{{Mz_Ed:.2f}}}{{{Mz_Rk:.2f}/{gamma_M1:.2f}}}={eta_z:.3f}")