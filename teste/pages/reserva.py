import streamlit as st
import plotly.graph_objs as go

def show_reserva():
    st.markdown("<h2 style='color:#5E3C99;font-weight:900;'>Calculadora de Reserva de Emergência</h2>", unsafe_allow_html=True)

    gastos = st.number_input("Gastos mensais médios (R$)", value=3000.0, step=100.0)
    renda = st.number_input("Renda mensal líquida (opcional)", value=4000.0, step=100.0)
    meses = st.slider("Por quantos meses de proteção você deseja estar coberto?", min_value=3, max_value=24, value=6)
    reserva_atual = st.number_input("Quanto você já tem reservado (R$)?", value=0.0, step=100.0)

    if st.button("Calcular Reserva"):
        valor_ideal = gastos * meses
        st.success(f"Reserva de emergência recomendada: **R$ {valor_ideal:,.2f}** ({meses} meses de proteção)")

        if reserva_atual >= valor_ideal:
            st.info("Parabéns! Sua reserva de emergência está adequada ou acima do ideal.")
        else:
            falta = valor_ideal - reserva_atual
            st.warning(f"Você precisa reservar mais **R$ {falta:,.2f}** para alcançar a proteção desejada.")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=["Reserva Ideal", "Reserva Atual"],
            y=[valor_ideal, reserva_atual],
            marker_color=["#5E3C99", "#FFDB36"],  # Roxo escuro e amarelo
            text=[f"R$ {valor_ideal:,.2f}", f"R$ {reserva_atual:,.2f}"],
            textposition='auto',
            hovertemplate='%{x}: R$ %{y:,.2f}<extra></extra>'
        ))
        fig.update_layout(
            yaxis_title="R$",
            title="Comparativo Reserva Ideal x Atual",
            font=dict(color="#5E3C99", size=14),
            plot_bgcolor="#fff",
            paper_bgcolor="#fff",
            margin=dict(l=30, r=30, t=50, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <ul>
        <li>💡 <b>Dica:</b> A reserva de emergência deve estar em investimentos de <b>alta liquidez e baixo risco</b>, como Tesouro Selic ou CDB com liquidez diária.</li>
        </ul>
        """, unsafe_allow_html=True)
