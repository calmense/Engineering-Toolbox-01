import streamlit as st
import math

st.set_page_config(
    page_title="P-Delta Nachweis",
    layout="wide"
)

st.title("P-Delta Nachweis Holzstütze")

# =====================================================
# EINGANGSWERTE
# =====================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("Geometrie")

    L = st.number_input("Stützenlänge L [m]", value=3.20)
    b = st.number_input("Breite b [m]", value=0.20)
    h = st.number_input("Höhe h [m]", value=1.40)

with col2:

    st.subheader("Einwirkungen")

    N_ed = st.number_input("Normalkraft NEd [kN]", value=265.0)
    M_y_ed = st.number_input("Moment My,Ed [kNm]", value=90.0)
    M_z_ed = st.number_input("Moment Mz,Ed [kNm]", value=0.0)

st.divider()

col3, col4 = st.columns(2)

with col3:

    st.subheader("Material")

    fc0k = st.number_input("f_c,0,k [kN/m²]", value=21000.0)
    fmyk = st.number_input("f_m,y,k [kN/m²]", value=24000.0)
    E0mean = st.number_input("E_0,mean [kN/m²]", value=11000000.0)
    E005 = st.number_input("E_0,05 [kN/m²]", value=7370000.0)

with col4:

    st.subheader("Beiwerte / Imperfektion")

    k_mod = st.number_input("k_mod", value=0.90)
    gamma_M = st.number_input("γ_M", value=1.30)
    theta = st.number_input(
        "Anfangsschiefstellung θ",
        value=0.0025,
        format="%.4f"
    )
    L_eff = st.number_input(
        "wirksame Länge L_eff [m]",
        value=L
    )

# =====================================================
# QUERSCHNITT
# =====================================================

A = b * h
Wy = b * h**2 / 6
Iy = b * h**3 / 12

e0 = theta * L * 1000

M0 = N_ed * e0 / 1000

M1 = M_y_ed + M0

fc0d = k_mod * fc0k / gamma_M
fmyd = k_mod * fmyk / gamma_M

Ncr = (
    math.pi**2
    * E005
    * Iy
    / L_eff**2
)

st.divider()
st.header("Berechnete Querschnitts- und Festigkeitswerte")

left, right = st.columns(2)

with left:

    st.metric("Fläche A", f"{A:.3f} m²")
    st.metric("Widerstandsmoment Wy", f"{Wy:.3f} m³")
    st.metric("Imperfektion e₀", f"{e0:.3f} mm")
    st.metric("Moment M₀", f"{M0:.3f} kNm")
    st.metric("Moment 1. Ordnung", f"{M1:.3f} kNm")

with right:

    st.metric("Flächenträgheitsmoment Iy", f"{Iy:.4f} m⁴")
    st.metric("f_c,0,d", f"{fc0d:.0f} kN/m²")
    st.metric("f_m,y,d", f"{fmyd:.0f} kN/m²")
    st.metric("Eulerlast Ncr", f"{Ncr:,.0f} kN")

# =====================================================
# ITERATIONSDATEN
# =====================================================

st.divider()
st.header("Schnittgrößen nach Theorie II. Ordnung")

iterations = 5

table = []

M = M1
e_total = e0

for i in range(iterations):

    e_i = (
        M
        * L_eff**2
        / (E005 * Iy)
    )

    e_i_mm = e_i * 1000

    dM = N_ed * e_i

    M_new = M + dM

    change = (
        abs(M_new - M) / M_new * 100
        if M_new != 0
        else 0
    )

    table.append(
        {
            "i": i,
            "Ausgangsmoment Mi-1 [kNm]": round(M, 3),
            "zusätzliche Auslenkung ei [mm]": round(e_i_mm, 3),
            "kumulierte Auslenkung e [mm]": round(
                e_total + e_i_mm,
                3
            ),
            "zusätzliches Moment ΔMi [kNm]": round(
                dM,
                3
            ),
            "Gesamtmoment Mi [kNm]": round(
                M_new,
                3
            ),
            "Änderung [%]": round(
                change,
                3
            )
        }
    )

    M = M_new
    e_total += e_i_mm

# =====================================================
# TABELLE
# =====================================================

st.data_editor(
    table,
    hide_index=True,
    disabled=True,
    use_container_width=True,
    column_config={
        "i": st.column_config.NumberColumn(
            width="small"
        ),
        "Ausgangsmoment Mi-1 [kNm]":
            st.column_config.NumberColumn(format="%.3f"),
        "zusätzliche Auslenkung ei [mm]":
            st.column_config.NumberColumn(format="%.3f"),
        "kumulierte Auslenkung e [mm]":
            st.column_config.NumberColumn(format="%.3f"),
        "zusätzliches Moment ΔMi [kNm]":
            st.column_config.NumberColumn(format="%.3f"),
        "Gesamtmoment Mi [kNm]":
            st.column_config.NumberColumn(format="%.3f"),
        "Änderung [%]":
            st.column_config.NumberColumn(format="%.3f"),
    }
)

st.success(
    f"Moment nach {iterations} Iterationen: "
    f"{M:.3f} kNm"
)