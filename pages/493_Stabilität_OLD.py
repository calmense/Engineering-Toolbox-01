import streamlit as st
from formatting import *
import math
import pandas as pd
import streamlit as st

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


input_data = pd.DataFrame({
    "h [mm]": [3500.00],
    "b [mm]": [1500.00],
    "tf [mm]": [50.00],
    "tw [mm]": [25.00],
    "Querschnittsklasse": [4],
    "NEd [kN]": [9200.00],
    "My,Ed [kNm]": [4000.00],
    "Lcr,y [m]": [27.60],
    "Lcr,z [m]": [3.45],
})

st.divider()

h1_black("Querschnittswerte")

edited_data = st.data_editor(
    input_data,
    hide_index=True,
    use_container_width=True,
    column_config={
        "h [mm]": st.column_config.NumberColumn("h [mm]", format="%.2f"),
        "b [mm]": st.column_config.NumberColumn("b [mm]", format="%.2f"),
        "tf [mm]": st.column_config.NumberColumn("tf [mm]", format="%.2f"),
        "tw [mm]": st.column_config.NumberColumn("tw [mm]", format="%.2f"),
        "Querschnittsklasse": st.column_config.SelectboxColumn(
            "QK",
            options=[1, 2, 3, 4],
        ),
        "NEd [kN]": st.column_config.NumberColumn("NEd [kN]", format="%.2f"),
        "My,Ed [kNm]": st.column_config.NumberColumn("My,Ed [kNm]", format="%.2f"),
        "Lcr,y [m]": st.column_config.NumberColumn("Lcr,y [m]", format="%.2f"),
        "Lcr,z [m]": st.column_config.NumberColumn("Lcr,z [m]", format="%.2f"),
    },
)

h = edited_data.loc[0, "h [mm]"]
b = edited_data.loc[0, "b [mm]"]
tf = edited_data.loc[0, "tf [mm]"]
tw = edited_data.loc[0, "tw [mm]"]
querschnittsklasse = edited_data.loc[0, "Querschnittsklasse"]
N_Ed = edited_data.loc[0, "NEd [kN]"]
My_Ed = edited_data.loc[0, "My,Ed [kNm]"]
Lcry = edited_data.loc[0, "Lcr,y [m]"]
Lcrz = edited_data.loc[0, "Lcr,z [m]"]

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

NRk=A*fy/1000
Wpl_y = Iy/(h/2)
Wel_y = Wpl_y

if querschnittsklasse in [1,2]:
    Wy_Rk=Wpl_y
    My_Rk=Wpl_y*fy/1e6
elif querschnittsklasse==3:
    Wy_Rk=Wel_y
    My_Rk=Wel_y*fy/1e6
else:
    Wy_Rk=Wel_y
    My_Rk=Wel_y*fy/1e6
    st.warning("Für Querschnittsklasse 4 ist für My,Rk der wirksame Querschnitt Aeff bzw. Weff erforderlich. Aktuell wird näherungsweise Wel,y verwendet.")


# ---------------------------------------------------------
# Knickschlankheiten
# ---------------------------------------------------------

lambda_y = (Lcry * 100) / (iy * 93.9)

# ---------------------------------------------------------
# EC3-Knicklinie
# ---------------------------------------------------------

kl_y = get_knicklinie_I(h, b, tf, stahlsorte, "y-y")
alpha_y = alpha_values[str(kl_y)]

# ---------------------------------------------------------
# Abminderungsfaktoren χ
# ---------------------------------------------------------

phi_y = 0.5 * (1 + alpha_y * (lambda_y - 0.2) + lambda_y**2)
chi_y = 1 / (phi_y + math.sqrt(phi_y**2 - lambda_y**2))

# ---------------------------------------------------------
# Biegedrillknicken
# ---------------------------------------------------------

Ncr_z = math.pi**2 * 21000 * Iz / (Lcrz * 100)**2
c_squared = (Iw + 0.039 * (Lcrz * 100)**2 * IT) / Iz
Mcr = xi * Ncr_z * (math.sqrt(c_squared + 0.25 * zp**2) + 0.5 * zp) * 1e-2
lambda_LT = math.sqrt(My_Rk / Mcr)
phi_LT = 0.5 * (1 + alpha_y * (lambda_LT - 0.2) + lambda_LT**2)
chi_LT = 1 / (phi_LT + math.sqrt(phi_LT**2 - lambda_LT**2))
chi_LT_unbounded = chi_LT
chi_LT = min(1.0, chi_LT)

# ---------------------------------------------------------
# Interaktionsbeiwerte
# ---------------------------------------------------------

kyy = 1

# ---------------------------------------------------------
# Interaktionsnachweise
# ---------------------------------------------------------

eta_y = N_Ed / (chi_y * NRk / gamma_M1) + kyy * (My_Ed ) / (chi_LT * My_Rk / gamma_M1) 

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

h2("Steifigkeitswerte")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"h_w=h-2t_f={h:.0f}-2\cdot{tf:.0f}={hw:.0f}\,\mathrm{{mm}}\quad\text{{(Steghöhe)}}")
    st.latex(rf"A=2bt_f+h_wt_w=2\cdot{b:.0f}\cdot{tf:.0f}+{hw:.0f}\cdot{tw:.0f}={A:.0f}\,\mathrm{{mm^2}}\quad\text{{(Querschnittsfläche)}}")
    st.latex(rf"I_y=2\left(\frac{{bt_f^3}}{{12}}+bt_f\left(\frac{{h-t_f}}{{2}}\right)^2\right)+\frac{{t_wh_w^3}}{{12}}={Iy:.0f}\,\mathrm{{mm^4}}\quad\text{{(Flächenträgheitsmoment y)}}")
    st.latex(rf"I_z=2\frac{{t_fb^3}}{{12}}+\frac{{h_wt_w^3}}{{12}}={Iz:.0f}\,\mathrm{{mm^4}}\quad\text{{(Flächenträgheitsmoment z)}}")
    st.latex(rf"i_y=\sqrt{{\frac{{I_y}}{{A}}}}=\sqrt{{\frac{{{Iy:.0f}\,\mathrm{{mm^4}}}}{{{A:.0f}\,\mathrm{{mm^2}}}}}}={iy:.1f}\,\mathrm{{mm}}\quad\text{{(Trägheitsradius y)}}")
    st.latex(rf"i_z=\sqrt{{\frac{{I_z}}{{A}}}}=\sqrt{{\frac{{{Iz:.0f}\,\mathrm{{mm^4}}}}{{{A:.0f}\,\mathrm{{mm^2}}}}}}={iz:.1f}\,\mathrm{{mm}}\quad\text{{(Trägheitsradius z)}}")
    st.latex(rf"I_T=\frac{{2bt_f^3+h_wt_w^3}}{{3}}=\frac{{2\cdot{b:.0f}\cdot{tf:.0f}^3+{hw:.0f}\cdot{tw:.0f}^3}}{{3}}={IT:.0f}\,\mathrm{{mm^4}}\quad\text{{(Torsionsträgheitsmoment)}}")
    st.latex(rf"I_w=\frac{{t_fb^3(h-t_f)^2}}{{24}}=\frac{{{tf:.0f}\cdot{b:.0f}^3\cdot({h:.0f}-{tf:.0f})^2}}{{24}}={Iw:.0f}\,\mathrm{{mm^6}}\quad\text{{(Wölbwiderstand)}}")
    st.latex(rf"z_p=-\frac{{h}}{{2}}=-\frac{{{h:.0f}}}{{2}}={zp:.0f}\,\mathrm{{mm}}\quad\text{{(Polkoordinate)}}")
    st.latex(rf"\xi={xi:.2f}\quad\text{{(Momentenbeiwert - Einfeldträger (ungünstig))}}")

h2("Knicken")
h3("Knickschlankheit")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"\bar{{\lambda}}_y=\frac{{L_{{cr,y}}}}{{i_y\cdot93.9}}=\frac{{{Lcry*100:.0f}\,\mathrm{{cm}}}}{{{iy:.2f}\,\mathrm{{cm}}\cdot93.9}}={lambda_y:.3f}")

h3("Knicklinien")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"\mathrm{{Knicklinie}}\ y-y:\ {kl_y}\Rightarrow\alpha_y={alpha_y:.2f}")


h3("Abminderungsbeiwerte")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"\Phi_y=\frac{{1}}{{2}}\left[1+\alpha_y\left(\bar{{\lambda}}_y-0.2\right)+\bar{{\lambda}}_y^2\right]=\frac{{1}}{{2}}\left[1+{alpha_y:.2f}\left({lambda_y:.3f}-0.2\right)+{lambda_y:.3f}^2\right]={phi_y:.3f}")
    st.latex(rf"\chi_y=\frac{{1}}{{\Phi_y+\sqrt{{\Phi_y^2-\bar{{\lambda}}_y^2}}}}=\frac{{1}}{{{phi_y:.3f}+\sqrt{{{phi_y:.3f}^2-{lambda_y:.3f}^2}}}}={chi_y:.3f}")

h2("Biegedrillknicken")
h3("Kritische Werte")


result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"N_{{cr,z}}=\frac{{\pi^2 E I_z}}{{L_{{cr,z}}^2}}=\frac{{\pi^2\cdot21000\,\mathrm{{kN/cm^2}}\cdot{Iz:.0f}\,\mathrm{{cm^4}}}}{{({Lcrz*100:.0f}\,\mathrm{{cm}})^2}}={Ncr_z:.0f}\,\mathrm{{kN}}")
    st.latex(rf"c^2=\frac{{I_w+0.039\,L_{{cr,z}}^2 I_T}}{{I_z}}=\frac{{{Iw:.0f}\,\mathrm{{cm^6}}+0.039\cdot({Lcrz*100:.0f}\,\mathrm{{cm}})^2\cdot{IT:.0f}\,\mathrm{{cm^4}}}}{{{Iz:.0f}\,\mathrm{{cm^4}}}}={c_squared:.0f}\,\mathrm{{cm^2}}")
    st.latex(r"M_{cr}=\xi N_{cr,z}\left(\sqrt{c^2+0.25z_p^2}+0.5z_p\right)")
    st.latex(rf"={xi:.2f}\cdot{Ncr_z:.0f}\,\mathrm{{kN}}\left(\sqrt{{{c_squared:.0f}\,\mathrm{{cm^2}}+0.25\cdot({zp:.0f}\,\mathrm{{cm}})^2}}+0.5\cdot({zp:.0f}\,\mathrm{{cm}})\right)\cdot10^{{-2}}={Mcr:.0f}\,\mathrm{{kNm}}")
    
h3("Biegedrillknickschlankheit")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"\bar{{\lambda}}_{{LT}}=\sqrt{{\frac{{M_{{y,Rk}}}}{{M_{{cr}}}}}}=\sqrt{{\frac{{{My_Rk:.0f}\,\mathrm{{kNm}}}}{{{Mcr:.0f}\,\mathrm{{kNm}}}}}}={lambda_LT:.3f}")
    st.latex(rf"\Phi_{{LT}}=\frac{{1}}{{2}}\left[1+\alpha_{{LT}}\left(\bar{{\lambda}}_{{LT}}-0.2\right)+\bar{{\lambda}}_{{LT}}^2\right]=\frac{{1}}{{2}}\left[1+{alpha_y:.2f}\left({lambda_LT:.3f}-0.2\right)+{lambda_LT:.3f}^2\right]={phi_LT:.3f}")
    st.latex(rf"\chi_{{LT}}=\frac{{1}}{{\Phi_{{LT}}+\sqrt{{\Phi_{{LT}}^2-\bar{{\lambda}}_{{LT}}^2}}}}=\frac{{1}}{{{phi_LT:.3f}+\sqrt{{{phi_LT:.3f}^2-{lambda_LT:.3f}^2}}}}={chi_LT_unbounded:.3f}\;\rightarrow\;\chi_{{LT}}=\min\left(1.0,{chi_LT_unbounded:.3f}\right)={chi_LT:.3f}")
h2("Interaktionsbeiwerte")
h3("Interaktionsbeiwert kyy")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(rf"k_{{yy}}={1}\quad\text{{(ungünstig)}}")


h2("Nachweis")
h3("Interaktionsnachweise")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.latex(r"\eta_y=\frac{N_{Ed}}{\chi_y\cdot N_{Rk}/\gamma_{M1}}+k_{yy}\cdot\frac{M_{y,Ed}}{\chi_{LT}\cdot M_{y,Rk}/\gamma_{M1}}\leq1.0")
    st.latex(rf"\eta_y=\frac{{{N_Ed:.0f}\,\mathrm{{kN}}}}{{{chi_y:.3f}\cdot{NRk:.0f}\,\mathrm{{kN}}/{gamma_M1:.2f}}}+{kyy:.3f}\cdot\frac{{{My_Ed:.0f}\,\mathrm{{kNm}}}}{{{chi_LT:.3f}\cdot{My_Rk:.0f}\,\mathrm{{kNm}}/{gamma_M1:.2f}}}={eta_y:.3f}\leq1.0")
