import streamlit as st

grundlagen = [
    st.Page("pages/000_best-practice.py", title="Best Practices"),
]

statik = [
    st.Page("pages/100_p-Delta.py", title="P-Delta"),
]

holzbau = [
    st.Page("pages/200_Materialkennwerte_Holz.py", title="Materialkennwerte"),
    st.Page("pages/201_kmod_EC5.py", title="kmod"),
]

stahlbeton = [
    st.Page("pages/300_Materialkennwerte_Beton.py", title="Materialkennwerte"),
    st.Page("pages/301_Verankerungslängen_EC2.py", title="Verankerungslängen"),
]

stahlbau = [
    st.Page("pages/400_Materialkennwerte_Stahl.py", title="Materialkennwerte"),
    st.Page("pages/401_Balkennachweise.py", title="Balkennachweis"),
    st.Page("pages/401_Querschnittsklasse.py", title="Querschnittsklasse"),
    st.Page("pages/402_Schweißnaht.py", title="Schweißnaht"),
    st.Page("pages/403_Stabilität.py", title="Stabilität"),
    ]


brückenbau = [
]

pg = st.navigation(
{
    "📚 GRUNDLAGEN": grundlagen,
    "📐 STATIK": statik,
    "🌲 HOLZBAU": holzbau,
    "🧱 STAHLBETON": stahlbeton,
    "🔩 STAHLBAU": stahlbau,
    "🌉 BRÜCKENBAU": brückenbau,
}
)

pg.run()
