import streamlit as st
from pages.dashboard import show_dashboard
from pages.juros_compostos import show_juros_compostos
from pages.liberdade import show_liberdade
from pages.reserva import show_reserva

st.set_page_config(page_title="A Cara da Riqueza | Dashboard", layout="wide")

st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background: linear-gradient(135deg, #322157, #ffdb36 85%);
            color: #fff;
        }
        .sidebar .sidebar-content img {
            border-radius: 12px;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("A Cara da Riqueza")
    st.caption("Seu hub financeiro premium")
    menu = st.radio("Navegação", [
        "Indicadores",
        "Juros Compostos",
        "Liberdade Financeira",
        "Reserva de Emergência"
    ])
    st.markdown("---")
    st.markdown('<small>Powered by A Cara da Riqueza</small>', unsafe_allow_html=True)

if menu == "Indicadores":
    show_dashboard()
elif menu == "Juros Compostos":
    show_juros_compostos()
elif menu == "Liberdade Financeira":
    show_liberdade()
elif menu == "Reserva de Emergência":
    show_reserva()
