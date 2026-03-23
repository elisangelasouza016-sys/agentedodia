import streamlit as st

st.set_page_config(page_title="Agente do Dia", page_icon="🗓️", layout="wide")


def parse_lines(text: str) -> list[str]:
    return [t.strip("-• \t") for t in text.splitlines() if t.strip()]


def gerar_plano(tarefas: list[str], energia: str, contexto: str) -> dict:
    contexto_lower = contexto.lower()
    tarefas_lower = [t.lower() for t in tarefas]

    estudo = [t for t in tarefas if "estud" in t.lower()]
    casa = [
        t for t in tarefas
        if any(p in t.lower() for p in ["lavar", "cozinha", "casa", "organizar", "limpar", "roupa"])
    ]
    trabalho = [
        t for t in tarefas
        if any(p in t.lower() for p in ["cliente", "trabalho", "responder", "projeto", "entregar"])
    ]
    exercicio = [t for t in tarefas if any(p in t.lower() for p in ["exerc", "caminha", "treino"])]
    outras = [t for t in tarefas if t not in estudo + casa + trabalho + exercicio]

    prioridades = []
    secundarias = []
    ignorar_hoje = []

    prioridades.append("Cuidar das demandas dos filhos")

    if estudo:
        prioridades.append(estudo[0])
    else:
        prioridades.append("Estudar ao menos 30 minutos")

    casa_caotica = "casa bagunçada" in contexto_lower or "casa caótica" in contexto_lower or "muita demanda da casa" in contexto_lower

    if casa_caotica:
        if casa:
            prioridades.append(casa[0])
        else:
            prioridades.append("Organizar uma área essencial da casa")
        ignorar_hoje.extend(trabalho)
    else:
        if trabalho:
            prioridades.append(trabalho[0])
            secundarias.extend(casa[:1])
        elif casa:
            prioridades.append(casa[0])

    if energia in ["média", "alta"] and exercicio:
        secundarias.append(exercicio[0])

    secundarias.extend(outras[: max(0, 2 - len(secundarias))])

    usados = set(prioridades + secundarias + ignorar_hoje)
    restante = [t for t in tarefas if t not in usados]
    ignorar_hoje.extend(restante)

    ordem_pratica = [
        "Começar pelo estudo em bloco curto de 30 a 40 minutos",
        "Executar a prioridade principal de casa ou trabalho",
        "Resolver demandas dos filhos ao longo do dia sem abrir novas frentes",
    ]

    if energia in ["média", "alta"] and exercicio:
        ordem_pratica.append("Fazer exercício apenas se as 3 prioridades estiverem encaminhadas")

    encerrar_dia = "20:30" if energia != "alta" else "21:00"

    justificativa = (
        "O plano limita o dia a 3 prioridades, mantém estudo como fixo e evita sobrecarga."
    )

    return {
        "prioridades": prioridades[:3],
        "secundarias": secundarias[:2],
        "ignorar_hoje": ignorar_hoje,
        "ordem_pratica": ordem_pratica,
        "encerrar_dia": encerrar_dia,
        "justificativa": justificativa,
    }


st.title("🗓️ Agente do Dia")
st.caption("Planejamento simples e realista para o dia seguinte.")

col1, col2 = st.columns(2)

with col1:
    tarefas_text = st.text_area(
        "Tarefas (uma por linha)",
        value="estudar 30 minutos\nlavar roupa\norganizar cozinha\nresponder cliente\nfazer exercício",
        height=180,
    )

with col2:
    energia = st.selectbox("Energia prevista", ["baixa", "média", "alta"], index=1)
    contexto = st.text_area(
        "Contexto do dia",
        value="filhos em casa, casa bagunçada, interrupções esperadas",
        height=180,
    )

if st.button("Gerar plano", type="primary"):
    tarefas = parse_lines(tarefas_text)

    if not tarefas:
        st.warning("Informe pelo menos uma tarefa.")
    else:
        plano = gerar_plano(tarefas, energia, contexto)

        st.subheader("Plano do dia")

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("**Prioridades**")
            for item in plano["prioridades"]:
                st.write(f"- {item}")

            st.markdown("**Secundárias**")
            for item in plano["secundarias"]:
                st.write(f"- {item}")

        with c2:
            st.markdown("**Ignorar hoje**")
            for item in plano["ignorar_hoje"]:
                st.write(f"- {item}")

            st.markdown("**Encerrar o dia**")
            st.write(plano["encerrar_dia"])

        st.markdown("**Ordem prática**")
        for i, item in enumerate(plano["ordem_pratica"], start=1):
            st.write(f"{i}. {item}")

        st.markdown("**Justificativa**")
        st.write(plano["justificativa"])