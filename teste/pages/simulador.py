import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_simulador():
    st.title("Simulador de Liberdade Financeira")

    with st.form("simulador_form"):
        col1, col2 = st.columns(2)
        with col1:
            renda_mensal = st.number_input("Renda Mensal (R$)", value=3000.0, step=100.0)
            aporte_mensal = st.number_input("Aporte Mensal (R$)", value=600.0, step=50.0)
            rentabilidade_anual = st.slider("Rentabilidade Anual Esperada (%)", 5, 20, 10)
        with col2:
            objetivo_renda_passiva = st.number_input("Objetivo de Renda Passiva Mensal (R$)", value=4000.0, step=100.0)
            patrimonio_atual = st.number_input("Patrimônio Atual (R$)", value=15000.0, step=1000.0)
            idade_atual = st.number_input("Idade Atual", value=30, step=1)

        submitted = st.form_submit_button("Executar Simulação")

    if submitted:
        juros_mensal = (1 + rentabilidade_anual / 100) ** (1 / 12) - 1
        objetivo_patrimonio = objetivo_renda_passiva / juros_mensal

        patrimonios = [patrimonio_atual]
        meses = 0

        while patrimonios[-1] < objetivo_patrimonio and meses < 1500:
            novo_patrimonio = patrimonios[-1] * (1 + juros_mensal) + aporte_mensal
            patrimonios.append(novo_patrimonio)
            meses += 1

        anos = meses // 12
        meses_restantes = meses % 12

        st.subheader("Resultado da Simulação")
        st.write(f"Tempo estimado: {anos} anos e {meses_restantes} meses")
        st.write(f"Patrimônio necessário: R$ {objetivo_patrimonio:,.2f}")

        df = pd.DataFrame({
            "Mês": list(range(len(patrimonios))),
            "Patrimônio (R$)": patrimonios
        })

        fig, ax = plt.subplots()
        ax.plot(df["Mês"], df["Patrimônio (R$)"], label="Evolução Patrimonial", linewidth=2)
        ax.axhline(objetivo_patrimonio, color='red', linestyle='--', label="Meta")
        ax.set_xlabel("Meses")
        ax.set_ylabel("Patrimônio (R$)")
        ax.set_title("Projeção de Patrimônio")
        ax.grid(True, linestyle="--", linewidth=0.5)
        ax.legend()
        st.pyplot(fig)
