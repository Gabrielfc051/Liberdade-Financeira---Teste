import streamlit as st
import plotly.graph_objs as go
import pandas as pd

def show_juros_compostos():
    st.markdown("<h2 style='color:#5E3C99;font-weight:900;'>Calculadora de Juros Compostos</h2>", unsafe_allow_html=True)
    valor_inicial = st.number_input("Valor Inicial (R$)", value=1000.0, step=100.0)
    aporte = st.number_input("Aporte Mensal (R$)", value=100.0, step=50.0)
    taxa = st.number_input("Taxa de Juros ao ano (%)", value=10.0, step=0.1)
    anos = st.number_input("Período (anos)", value=5, step=1)

    if st.button("Calcular"):
        taxa_mensal = (1 + taxa/100)**(1/12) - 1
        meses = int(anos * 12)
        montante = valor_inicial
        historico = []
        for i in range(meses + 1):
            historico.append({
                "Mês": i,
                "Saldo (R$)": montante,
                "Aporte (R$)": aporte if i > 0 else valor_inicial
            })
            montante = montante * (1 + taxa_mensal) + aporte

        st.success(f"Montante final: R$ {montante:,.2f}")

        df = pd.DataFrame(historico)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["Mês"], y=df["Saldo (R$)"],
            mode="lines+markers",
            name="Saldo",
            line=dict(color='#5E3C99', width=3),
            hovertemplate=
                'Mês: %{x}<br>' +
                'Saldo: R$ %{y:,.2f}<br>' +
                'Aporte: R$ %{customdata[0]:,.2f}<br>',
            customdata=df[["Aporte (R$)"]].values
        ))
        fig.update_layout(
            title="Evolução do Patrimônio",
            xaxis_title="Meses",
            yaxis_title="Saldo (R$)",
            plot_bgcolor="#FCD835",
            paper_bgcolor="#FCD835",
            font=dict(color="#5E3C99", size=14),
            hoverlabel=dict(bgcolor="#fff", font_size=13, font_family="Arial"),
            margin=dict(l=30, r=30, t=50, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<br><b>Detalhamento mês a mês:</b>", unsafe_allow_html=True)
        df_formatado = df.copy()
        df_formatado["Saldo (R$)"] = df_formatado["Saldo (R$)"].apply(lambda x: f"R$ {x:,.2f}")
        df_formatado["Aporte (R$)"] = df_formatado["Aporte (R$)"].apply(lambda x: f"R$ {x:,.2f}")
        st.dataframe(df_formatado, use_container_width=True)
