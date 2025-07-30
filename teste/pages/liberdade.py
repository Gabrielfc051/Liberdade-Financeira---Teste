import streamlit as st
import pandas as pd
import plotly.graph_objs as go

def show_liberdade():
    st.markdown("<h2 style='color:#5E3C99;font-weight:900;'>Simulador de Liberdade Financeira</h2>", unsafe_allow_html=True)

    renda_desejada = st.number_input("Renda Passiva Desejada (R$/mês)", value=5000.0, step=100.0)
    patrimonio = st.number_input("Patrimônio Inicial (R$)", value=20000.0, step=1000.0)
    aporte_inicial = st.number_input("Aporte Mensal (R$)", value=1000.0, step=100.0)
    reajuste_aporte = st.number_input("Reajuste Anual do Aporte (%)", value=0.0, step=0.1, help="Percentual de aumento do aporte a cada ano")
    taxa = st.number_input("Rentabilidade ao ano (%)", value=10.0, step=0.1)
    inflacao = st.number_input("Inflação esperada (%)", value=4.0, step=0.1)

    if st.button("Simular Liberdade"):
        meses = 0
        saldo = patrimonio
        renda_desejada_atual = renda_desejada
        taxa_real = ((1+taxa/100)/(1+inflacao/100))-1
        taxa_mensal = (1 + taxa_real)**(1/12) - 1
        aporte = aporte_inicial
        historico = []
        atingiu = False

        marcos = [2, 5, 10, 100]
        marco_index = 0
        conquistados = []
        proximo_marco = patrimonio * marcos[marco_index] if marcos else None

        while meses < 1200:
            rendimento = saldo * taxa_mensal
            saldo = saldo * (1 + taxa_mensal) + aporte
            historico.append({
                "Mês": meses + 1,
                "Aporte (R$)": aporte if meses > 0 else patrimonio,
                "Rendimento (R$)": rendimento,
                "Saldo (R$)": saldo
            })
            meses += 1
            renda_desejada_atual *= (1 + inflacao/100/12)
            if meses % 12 == 0 and meses > 0:
                aporte *= (1 + reajuste_aporte/100)
            if not atingiu and rendimento >= renda_desejada_atual:
                atingiu = True
                mes_liberdade = meses
                saldo_liberdade = saldo
                break
            while marco_index < len(marcos) and saldo >= patrimonio * marcos[marco_index]:
                conquistados.append({
                    "marco": f"{marcos[marco_index]}x",
                    "mes": meses,
                    "saldo": saldo
                })
                marco_index += 1
                if marco_index < len(marcos):
                    proximo_marco = patrimonio * marcos[marco_index]

        if not atingiu:
            st.error("Você não alcançaria a liberdade financeira nas condições simuladas.")
        else:
            anos = mes_liberdade // 12
            st.success(f"Você alcançaria a liberdade financeira em {anos} anos e {mes_liberdade%12} meses.")
            st.info(f"Patrimônio necessário estimado: R$ {saldo_liberdade:,.2f}")

            df = pd.DataFrame(historico)
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["Mês"], y=df["Saldo (R$)"],
                mode='lines+markers',
                name='Saldo',
                line=dict(color='#5E3C99', width=3),
                hovertemplate=
                    'Mês: %{x}<br>' +
                    'Saldo: R$ %{y:,.2f}<br>' +
                    'Aporte: R$ %{customdata[0]:,.2f}<br>' +
                    'Rendimento: R$ %{customdata[1]:,.2f}<br>',
                customdata=df[["Aporte (R$)", "Rendimento (R$)"]].values
            ))
            for item in conquistados:
                fig.add_vline(
                    x=item["mes"],
                    line_dash="dash",
                    line_color="#FFDB36",
                    annotation_text=f'Meta {item["marco"]}',
                    annotation_position="top right"
                )
            fig.update_layout(
                title="Projeção de Patrimônio até a Liberdade",
                xaxis_title="Meses",
                yaxis_title="Saldo (R$)",
                plot_bgcolor="#FCD835",
                paper_bgcolor="#FCD835",
                font=dict(color="#5E3C99", size=14),
                hoverlabel=dict(bgcolor="#fff", font_size=13, font_family="Arial"),
                margin=dict(l=30, r=30, t=50, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

            if conquistados:
                st.markdown("<b>Conquistas de Patrimônio:</b>", unsafe_allow_html=True)
                st.markdown("<ul>", unsafe_allow_html=True)
                for item in conquistados:
                    anos_m = item["mes"] // 12
                    meses_m = item["mes"] % 12
                    st.markdown(f"<li>{item['marco']} atingido em {anos_m} anos e {meses_m} meses (Saldo: R$ {item['saldo']:,.2f})</li>", unsafe_allow_html=True)
                st.markdown("</ul>", unsafe_allow_html=True)

            df_formatado = df.copy()
            df_formatado["Aporte (R$)"] = df_formatado["Aporte (R$)"].apply(lambda x: f"R$ {x:,.2f}")
            df_formatado["Rendimento (R$)"] = df_formatado["Rendimento (R$)"].apply(lambda x: f"R$ {x:,.2f}")
            df_formatado["Saldo (R$)"] = df_formatado["Saldo (R$)"].apply(lambda x: f"R$ {x:,.2f}")

            st.markdown("<br><b>Detalhamento mês a mês:</b>", unsafe_allow_html=True)
            st.dataframe(df_formatado, use_container_width=True)
