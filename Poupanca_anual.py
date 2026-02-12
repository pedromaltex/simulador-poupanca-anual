import streamlit as st
import numpy as np
import plotly.graph_objects as go


st.set_page_config(page_title="💰 O Mesmo Salário, Duas Vidas Diferentes", layout="centered")

st.title("💰 O Mesmo Salário, Duas Vidas Diferentes")

tab1, tab2 = st.tabs(["📥 Dados", "📊 Resultados"])

# =====================================================
# TAB 1 — DADOS
# =====================================================

with tab1:

    st.header("💼 Rendimento")
    rendimento_mensal = st.number_input("Rendimento mensal (€)", min_value=0.0, value=1200.0)
    st.header("🏠 Despesas Mensais")

    col1, col2 = st.columns(2)

    with col1:

        renda = st.number_input("Renda / Habitação (€)", min_value=0.0, value=450.0)
        compras = st.number_input("Compras Supermercado (€)", min_value=0.0, value=250.0)
        lazer = st.number_input("Lazer / Jantares (€)", min_value=0.0, value=200.0)
    with col2:
        carro = st.number_input("Transporte (crédito + combustível + manutenção) (€)", min_value=0.0, value=300.0)
        ferias = st.number_input("Férias (mensalizado) (€)", min_value=0.0, value=80.0)
        outros = st.number_input("Outros (€)", min_value=0.0, value=100.0)

        total_despesas = renda + compras + lazer + carro + ferias + outros
        poupanca_mensal = rendimento_mensal - total_despesas

    col1, col2 = st.columns(2)
    with col2:        
        # DISTRIBUIÇÃO DESPESAS
        st.subheader("📌 Distribuição das Despesas")

        fig2 = go.Figure(data=[go.Pie(
            labels=["Renda", "Compras", "Lazer", "Carro", "Férias", "Outros"],
            values=[renda, compras, lazer, carro, ferias, outros],
            hole=0.4
        )])

        fig2.update_layout(template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)

    with col1:
        st.subheader("📌 Resumo Imediato")

        st.write(f"Total despesas: **{total_despesas:.2f} €**")
        st.write(f"Poupança mensal: **{poupanca_mensal:.2f} €**")

        if poupanca_mensal < 0:
            st.error("""
                🚨 ALERTA: Estás a gastar mais do que ganhas.

                Isto não é sustentável.
                Se nada mudar, a tendência é acumular dívida ou viver sob stress constante.

                Revê despesas fixas primeiro (renda e carro).
                Depois corta onde não traz verdadeiro valor.
                """)
        else:
            # ✅ NOVO: Percentagem de poupança do salário
            taxa_poupanca = (poupanca_mensal / rendimento_mensal) * 100
            st.subheader(f"💡 Estás a poupar {taxa_poupanca:.1f}% do teu salário")

            # Mensagem de avaliação
            if taxa_poupanca < 10:
                st.warning("Zona de risco. Pequenas mudanças agora evitam problemas futuros.")
            elif taxa_poupanca < 25:
                st.info("Caminho saudável. A consistência será o fator decisivo.")
            else:
                st.success("Excelente disciplina financeira. O tempo está a trabalhar para ti.")

# =====================================================
# TAB 2 — RESULTADOS
# =====================================================

with tab2:

    st.header("📈 Parâmetros de Investimento")

    taxa_retorno = st.slider("Taxa de retorno anual (%)", 0.0, 15.0, 7.0, 0.5)
    anos = st.slider("Anos até à reforma", 1, 50, 30)

    poupanca_anual = poupanca_mensal * 12
    taxa_decimal = taxa_retorno / 100

    valor_futuro = 0
    evolucao = []

    for ano in range(1, anos + 1):
        valor_futuro = (valor_futuro + poupanca_anual) * (1 + taxa_decimal)
        evolucao.append(valor_futuro)

    st.header("📊 Resultados")

    if poupanca_mensal <= 0:
        st.error("Só podes investir depois de poupares!")
    else:
        # Detalhes
        st.success(f"Poupança anual: {poupanca_anual:.2f} €")
        st.success(f"Valor estimado ao fim de {anos} anos: {valor_futuro:,.2f} €")

        # GRÁFICO EVOLUÇÃO
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(1, anos + 1)),
            y=evolucao,
            mode='lines',
            name='Património acumulado'
        ))

        fig.add_trace(go.Scatter(
            x=list(range(1, anos + 1)),
            y=list(range(int(poupanca_anual), int(poupanca_anual)*(anos + 1), int(poupanca_anual))),
            mode='markers',
            name='Montante Investido',

        ))

        fig.update_layout(
            title="Crescimento do Património ao Longo do Tempo",
            xaxis_title="Ano",
            yaxis_title="Valor (€)",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

