import streamlit as st

st.set_page_config(page_title="Agente do Dia", page_icon="🗓️", layout="wide")

st.title("🗓️ Agente do Dia")
st.write("Interface mínima funcionando.")

tarefas = st.text_area(
    "Tarefas (uma por linha)",
    value="estudar 30 minutos\nlavar roupa\norganizar cozinha"
)

energia = st.selectbox(
    "Energia prevista",
    ["baixa", "média", "alta"],
    index=1
)

contexto = st.text_area(
    "Contexto do dia",
    value="filhos em casa, interrupções esperadas"
)

if st.button("Gerar plano"):
    lista_tarefas = [t.strip() for t in tarefas.splitlines() if t.strip()]

    st.subheader("Resumo capturado")
    st.write("**Tarefas:**", lista_tarefas)
    st.write("**Energia:**", energia)
    st.write("**Contexto:**", contexto)

    st.subheader("Plano simples")
    st.write("1. Estudo")
    st.write("2. Casa")
    st.write("3. Filhos")