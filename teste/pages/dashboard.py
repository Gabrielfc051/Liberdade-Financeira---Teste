import streamlit as st
import requests
import numpy as np

def pegar_selic():
    url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json'
    r = requests.get(url)
    if r.ok:
        return float(r.json()[0]['valor'].replace(",", "."))
    return None

def pegar_ipca_12m():
    url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/12?formato=json'
    r = requests.get(url)
    if r.ok:
        meses = [float(x['valor'].replace(",", ".")) for x in r.json()]
        return (np.prod([1 + (m/100) for m in meses]) - 1) * 100
    return None

def pegar_cdi_12m():
    url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados/ultimos/252?formato=json'
    r = requests.get(url)
    if r.ok:
        dias = [float(x['valor'].replace(",", ".")) for x in r.json()]
        return (np.prod([1 + (d/100) for d in dias]) - 1) * 100
    return None

def pegar_dolar():
    url = "https://brapi.dev/api/quote/USD-BRL"
    try:
        r = requests.get(url, timeout=3)
        if r.ok:
            return float(r.json()['results'][0]['regularMarketPrice'])
    except:
        pass
    return None

def pegar_ibov():
    url = "https://brapi.dev/api/quote/%5EBVSP"
    try:
        r = requests.get(url, timeout=3)
        if r.ok:
            return float(r.json()['results'][0]['regularMarketPrice'])
    except:
        pass
    return None

def show_dashboard():
    st.markdown(
        "<h2 style='color:#5E3C99; font-weight:900;'>Indicadores Econômicos</h2>",
        unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)

    card_style = "background:linear-gradient(120deg,#5E3C99,#FFDB36 80%);padding:30px 10px 20px 10px;border-radius:16px;margin:8px;color:#191326;font-weight:600;box-shadow:0 2px 12px #0001;"
    font_big = "font-size:2.2rem;font-weight:800;"

    selic = pegar_selic()
    ipca = pegar_ipca_12m()
    cdi = pegar_cdi_12m()
    dolar = pegar_dolar()
    ibov = pegar_ibov()

    if selic is not None:
        selic_txt = f"{selic:.2f}%"
    else:
        selic_txt = "N/A"
    if ipca is not None:
        ipca_txt = f"{ipca:.2f}%"
    else:
        ipca_txt = "N/A"
    if cdi is not None:
        cdi_txt = f"{cdi:.2f}%"
    else:
        cdi_txt = "N/A"
    if dolar is not None:
        dolar_txt = f"R$ {dolar:.2f}"
    else:
        dolar_txt = "N/A"
    if ibov is not None:
        ibov_txt = f"{ibov:,.0f}"
    else:
        ibov_txt = "N/A"

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"<div style='{card_style}'><span>SELIC</span><br><span style='{font_big}'>{selic_txt}</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='{card_style}'><span>IPCA 12m</span><br><span style='{font_big}'>{ipca_txt}</span></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div style='{card_style}'><span>CDI 12m</span><br><span style='{font_big}'>{cdi_txt}</span></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div style='{card_style}'><span>Dólar</span><br><span style='{font_big}'>{dolar_txt}</span></div>", unsafe_allow_html=True)
    with col5:
        st.markdown(f"<div style='{card_style}'><span>Ibovespa</span><br><span style='{font_big}'>{ibov_txt}</span></div>", unsafe_allow_html=True)

    st.markdown("<small style='color:#5E3C99;'>Fontes: Banco Central, brapi.dev</small>", unsafe_allow_html=True)
