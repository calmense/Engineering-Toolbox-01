import streamlit as st
import pandas as pd
from formatting import *
from Datenbank.Stahl_Datenbank import materialkennwerte_Stahl


# ---------------------------------------------------------
# Seiteneinstellungen
# ---------------------------------------------------------

st.title("Balkennachweis")
st.caption(
    "Nachweis der Durchbiegung "
    "nach DIN EN 1993-1-1"
)


# ---------------------------------------------------------
# Eingaben
# ---------------------------------------------------------

st.header("1. Eingaben")

eingabeart = st.radio("Eingabeart", ["Eingabeelemente", "Tabelle"], horizontal=True)

if eingabeart == "Eingabeelemente":
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
     

    col1, col2, col3 = st.columns(3)

    with col1:
        h1_black("Geometrie")

        l = st.number_input(
            "Spannweite l [m]",
            min_value=0.10,
            value=5.00,
            step=0.10,
        )
        
        A_v = st.number_input(
                "Querschnittsfläche Av [cm²]",
                min_value=0.10,
                value=5.00,
                step=0.10,
            )
        
        grenzwert = st.selectbox(
            "Zulässige Durchbiegung",
            ["L/200", "L/250", "L/300", "L/350", "L/400", "L/500"],
            index=2,
        )

    with col2:
        h1_black("Belastung")

        q_k = st.number_input(
            "char. Linienlast qk [kN/m]",
            min_value=0.0,
            value=5.0,
            step=0.1,
        )
        
        M_Ed = st.number_input(
                "Bemessungsmoment Md [kNm]",
                min_value=0.0,
                value=100.0,
                step=10.0,
                format="%.2f",
            )
        
        V_Ed = st.number_input(
                    "Bemessungsschub Vd [kN]",
                    min_value=0.0,
                    value=100.0,
                    step=10.0,
                    format="%.2f",
                )

    with col3:
        h1_black("Steifigkeit")

        E = st.number_input(
            "E-Modul E [N/mm²]",
            min_value=1.0,
            value=210000.0,
            step=1000.0,
        )

        I = st.number_input(
            "Flächenträgheitsmoment I [cm⁴]",
            min_value=1.0,
            value=8500.0,
            step=100.0,
        )
        
        W = st.number_input(
                "Widerstandsmoment [cm³]",
                min_value=0.01,
                value=500.0,
                step=10.0,
                format="%.2f",
            )

# Tabelle für die Eingabewerte

else: 
    input_df = pd.DataFrame({
        "Position": ["Träger"],
        "Profil": ["IPE 300"],
        "Güte": ["S235"],
        "l [m]": [5.00],
        "Av [cm²]": [5.00],
        "Zul. w": ["L/300"],
        "qk [kN/m]": [5.00],
        "Md [kNm]": [100.00],
        "Vd [kN]": [100.00],
        "E [N/mm²]": [210000.00],
        "I [cm⁴]": [8500.00],
        "W [cm³]": [500.00],
    })

    edited_df = st.data_editor(
        input_df,
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Position": st.column_config.TextColumn("Position", required=True),
            "Profil": st.column_config.TextColumn("Profil", required=True),
            "Güte": st.column_config.SelectboxColumn("Güte", options=["S235", "S275", "S355", "S420", "S460"], required=True),
            "l [m]": st.column_config.NumberColumn("Spannweite l [m]", min_value=0.01, step=0.10, format="%.2f"),
            "Av [cm²]": st.column_config.NumberColumn("Querschnitt Av [cm²]", min_value=0.00, step=0.10, format="%.2f"),
            "Zul. w": st.column_config.SelectboxColumn("Zul. w", options=["L/200", "L/250", "L/300", "L/350", "L/400", "L/500"], required=True),
            "qk [kN/m]": st.column_config.NumberColumn("qk (char.)[kN/m]", min_value=0.00, step=0.10, format="%.2f"),
            "Md [kNm]": st.column_config.NumberColumn("Md [kNm]", step=0.10, format="%.2f"),
            "Vd [kN]": st.column_config.NumberColumn("Vd [kN]", step=0.10, format="%.2f"),
            "E [N/mm²]": st.column_config.NumberColumn("E [N/mm²]", min_value=0.00, step=1000.00, format="%.2f"),
            "I [cm⁴]": st.column_config.NumberColumn("FTM I [cm⁴]", min_value=0.00, step=100.00, format="%.2f"),
            "W [cm³]": st.column_config.NumberColumn("W [cm³]", min_value=0.00, step=0.10, format="%.2f"),
        },
    )

    # Werte der ersten Tabellenzeile für die weitere Berechnung
    if not edited_df.empty:
        position = edited_df.iloc[0]["Position"]
        querschnitt = edited_df.iloc[0]["Profil"]
        stahlsorte = edited_df.iloc[0]["Güte"]
        l = float(edited_df.iloc[0]["l [m]"])
        A_v = float(edited_df.iloc[0]["Av [cm²]"])
        grenzwert = edited_df.iloc[0]["Zul. w"]
        q_k = float(edited_df.iloc[0]["qk [kN/m]"])
        M_Ed = float(edited_df.iloc[0]["Md [kNm]"])
        V_Ed = float(edited_df.iloc[0]["Vd [kN]"])
        E = float(edited_df.iloc[0]["E [N/mm²]"])
        I = float(edited_df.iloc[0]["I [cm⁴]"])
        W = float(edited_df.iloc[0]["W [cm³]"])
        
fy = materialkennwerte_Stahl[stahlsorte]["t ≤ 40 mm"]["fy"]
# ---------------------------------------------------------
# Berechnung
# ---------------------------------------------------------

# Biegung

# Umrechnung:
# W: cm³ -> mm³ = W * 1.000
# M: Nmm -> kNm = / 1.000.000
#
# M_c,Rd = W * f_y / gamma_M0
#
# Bei Eingabe von W in cm³ ergibt sich:
# M_c,Rd [kNm] = W [cm³] * f_y [N/mm²] / (1000 * gamma_M0)

M_c_Rd = W * fy / (1000.0 * 1)

if M_c_Rd > 0:
    ausnutzung_Biegung = M_Ed / M_c_Rd
else:
    ausnutzung_Biegung = float("inf")

nachweis_erfuellt = ausnutzung_Biegung <= 1.0

# Durchbiegung

L_mm = l * 1000

# kN/m -> N/mm
q_N_mm = q_k

# cm⁴ -> mm⁴
I_mm4 = I * 1e4

w_max = (5 * q_N_mm * L_mm**4) / (384 * E * I_mm4)

w_zul = {
    "L/200": L_mm / 200,
    "L/250": L_mm / 250,
    "L/300": L_mm / 300,
    "L/350": L_mm / 350,
    "L/400": L_mm / 400,
    "L/500": L_mm / 500,
}[grenzwert]

ausnutzung_Durchbiegung = w_max / w_zul

nachweis_erfuellt = ausnutzung_Durchbiegung <= 1.0

# ---------------------------------------------------------
# Biegung
# ---------------------------------------------------------

st.header("2. Biegung")

with st.expander("Biegung"):

    h1("Einaxiale Biegebeanspruchung")
    caption("Querschnittsnachweis nach DIN EN 1993-1-1, Abschnitt 6.2.5")

    h2("Eingabewerte")
    h3("Position")

    result_col1, result_col2, result_col3, result_col4 = st.columns(4)

    with result_col1:
        st.latex(rf"{position}")

    h3("Profil")

    result_col1, result_col2, result_col3, result_col4 = st.columns(4)

    with result_col1:
        st.latex(rf"{querschnitt}")

    with result_col2:
        st.latex(rf"{stahlsorte}")

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    h3("Eingabewerte")

    result_col11, result_col22, result_col33 = st.columns(3)

    with result_col11:
        st.latex(
            rf"M_{{Ed}}={M_Ed:.2f}\,\mathrm{{kNm}}\quad\mathrm{{(Bemessungsmoment)}}"
        )
     
    with result_col22:
        st.latex(
            rf"W={W:.2f}\,\mathrm{{cm^3}}\quad\mathrm{{(Widerstandsmoment)}}"
        )


    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    h2("Widerstand")

    result_col11, result_col22, result_col33 = st.columns(3)

    with result_col11:
        st.latex(
            rf"M_{{c,Rd}}=\frac{{W\cdot f_y}}{{\gamma_{{M0}}}}"
            rf"=\frac{{{W:.2f}\,\mathrm{{cm^3}}\cdot{(fy/10):.1f}\,\mathrm{{kN/cm^2}}}}{{{1:.2f}}}"
            rf"={M_c_Rd:.2f}\,\mathrm{{kNm}}"
            rf"\quad\mathrm{{(Biegemomententragfähigkeit)}}\;[-1-1/6.2.5]"
        )



    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    h2("Nachweis")

    result_col111, result_col222, result_col333, result_col444 = st.columns(4)

    with result_col111:
        st.latex(
            rf"\eta=\frac{{M_{{Ed}}}}{{M_{{c,Rd}}}}"
            rf"=\frac{{{M_Ed:.2f}\,\mathrm{{kNm}}}}{{{M_c_Rd:.2f}\,\mathrm{{kNm}}}}"
            rf"={ausnutzung_Biegung:.3f}"
            rf"={(ausnutzung_Biegung+0.01)*100:.0f}\,\%"
            rf"\quad\mathrm{{(Ausnutzungsgrad)}}"
        )

# ---------------------------------------------------------
# Querkraft
# ---------------------------------------------------------

st.header("3. Querkraft")

with st.expander("Querkraft"):

    h1("Querkraftbeanspruchung")
    caption("Querschnittsnachweis nach DIN EN 1993-1-1, Abschnitt 6.2.6")

    h2("Eingabewerte")
    h3("Position")

    result_col1, result_col2, result_col3, result_col4 = st.columns(4)

    with result_col1:
        st.latex(rf"{position}")

    h3("Profil")

    result_col1, result_col2, result_col3, result_col4 = st.columns(4)

    with result_col1:
        st.latex(rf"{querschnitt}")

    with result_col2:
        st.latex(rf"{stahlsorte}")

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    h3("Eingabewerte")


    result_col1, result_col2, result_col3, result_col4 = st.columns(4)

    with result_col1:
        st.latex(rf"V_{{Ed}}={V_Ed:.2f}\,\mathrm{{kN}}")

    with result_col2:
        st.latex(rf"A_v={A_v:.2f}\,\mathrm{{cm^2}}")

    with result_col3:
        st.latex(rf"f_y={fy:.0f}\,\mathrm{{N/mm^2}}")

    with result_col4:
        st.latex(rf"\gamma_{{M0}}={1:.2f}")

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    h2("Widerstand")

    V_Rd = (A_v * 100 * fy) / (3**0.5 * 1) / 1000

    result_col11, result_col22, result_col33, result_col44 = st.columns(4)

    with result_col11:
        st.latex(
            rf"V_{{Rd}}=\frac{{A_v\cdot f_y}}{{\sqrt{{3}}\cdot\gamma_{{M0}}}}={V_Rd:.2f}\,\mathrm{{kN}}"
        )

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    h2("Nachweis")

    ausnutzung_V = V_Ed / V_Rd
    nachweis_V_erfuellt = ausnutzung_V <= 1.0

    result_col111, result_col222, result_col333, result_col444 = st.columns(4)

    with result_col111:
        st.latex(
            rf"\eta_V=\frac{{V_{{Ed}}}}{{V_{{Rd}}}}="
            rf"\frac{{{V_Ed:.2f}}}{{{V_Rd:.2f}}}="
            rf"{ausnutzung_V:.3f}={ausnutzung_V*100:.1f}\,\%"
        )


# ---------------------------------------------------------
# Durchbiegung
# ---------------------------------------------------------

st.header("4. Durchbiegung")


with st.expander("Durchbiegung"):

    col_left, col_center, col_right = st.columns([3, 1, 1])


    h1("Durchbiegungsnachweis")
    caption("Grenzzustand der Gebrauchstauglichkeit")

    # ---------------------------------------------------------
    # Eingabewerte
    # ---------------------------------------------------------

    h2("Eingabewerte")
    h3("Position")

    result_col1, result_col2, result_col3, result_col4 = st.columns(4)

    with result_col1:
        st.latex(rf"{position}")
        
    h3("Profil")

    result_col1, result_col2, result_col3, result_col4 = st.columns(4)

    with result_col1:
        st.latex(rf"\mathrm{{{querschnitt}}}")

    with result_col2:
        st.latex(rf"{stahlsorte}")



    h3("Eingabewerte")
    result_col1, result_col2, result_col3, result_col4 = st.columns(4)

    with result_col1:
        st.latex(
            rf"L={l:.2f}\,\mathrm{{m}}"
            rf"\quad\mathrm{{(Stützweite)}}"
        )

    with result_col2:
        st.latex(
            rf"q_k={q_k:.2f}\,\mathrm{{kN/m}}"
            rf"\quad\mathrm{{(char.\ Linienlast)}}"
        )

    with result_col3:
        st.latex(
            rf"I={I:.2f}\,\mathrm{{cm^4}}"
            rf"\quad\mathrm{{(FTM)}}"
        )

    # ---------------------------------------------------------
    # Durchbiegung
    # ---------------------------------------------------------

    h2("Durchbiegung")

    result_col11, result_col22 = st.columns(2)

    with result_col11:
        st.latex(
            rf"w=\frac{{5q_kL^4}}{{384EI}}"
            rf"=\frac{{5\cdot{q_k:.2f}\,\mathrm{{kN/m}}\cdot({l*1000:.0f}\,\mathrm{{mm}})^4}}{{384\cdot{E:.0f}\,\mathrm{{N/mm^2}}\cdot{I:.0f}\,\mathrm{{mm^4}}}}"
            rf"={w_max:.2f}\,\mathrm{{mm}}"
            rf"\quad\mathrm{{(maximale\ Durchbiegung)}}"
        )
        
    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Grenzwert
    # ---------------------------------------------------------

    h2("Grenzwert")

    result_col11, result_col22 = st.columns(2)

    with result_col11:
        st.latex(
            rf"w_{{zul}}=\frac{{L}}{{300}}="
            rf"\frac{{{L_mm:.0f}\,\mathrm{{mm}}}}{{300}}="
            rf"{w_zul:.2f}\,\mathrm{{mm}}"
            rf"\quad\mathrm{{(zulässige\ Durchbiegung)}}"
        )
                
    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Nachweis
    # ---------------------------------------------------------

    h2("Nachweis")

    result_col11, result_col22 = st.columns(2)

    with result_col11:
        st.latex(
            rf"\eta=\frac{{w}}{{w_{{zul}}}}="
            rf"\frac{{{w_max:.2f}\,\mathrm{{mm}}}}{{{w_zul:.2f}\,\mathrm{{mm}}}}="
            rf"{ausnutzung_Durchbiegung:.3f}="
            rf"{(ausnutzung_Durchbiegung)*100:.0f}\,\%"
            rf"\quad\mathrm{{(Ausnutzungsgrad)}}"
        )
                
    st.markdown("</div>", unsafe_allow_html=True)

