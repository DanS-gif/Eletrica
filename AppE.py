import streamlit as st
import graphviz

def calcular_resistencia_equivalente(r1, r2, r3, r4):
    r_serie_ramo = r3 + r4
    r_paralelo = (r2 * r_serie_ramo) / (r2 + r_serie_ramo) if (r2 + r_serie_ramo) != 0 else 0
    req = r1 + r_paralelo
    return req

def main():
    st.set_page_config(page_title="Visualizador de Circuitos Mistos", layout="wide")
    st.title("Simulador Paramétrico de Circuitos Elétricos")
    
    st.sidebar.header("Parâmetros")
    v_fonte = st.sidebar.number_input("Tensão (V)", min_value=1.0, value=10.0, step=1.0)
    r1 = st.sidebar.number_input("R1 (Série)", min_value=1.0, value=200.0, step=10.0)
    r2 = st.sidebar.number_input("R2 (Paralelo)", min_value=1.0, value=100.0, step=10.0)
    r3 = st.sidebar.number_input("R3 (Misto)", min_value=1.0, value=100.0, step=10.0)
    r4 = st.sidebar.number_input("R4 (Misto)", min_value=1.0, value=200.0, step=10.0)

    req = calcular_resistencia_equivalente(r1, r2, r3, r4)
    corrente_total = v_fonte / req if req > 0 else 0

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Topologia do Circuito")
        
        # Criação do diagrama de nós usando Graphviz (Nativo do Streamlit)
        graph = graphviz.Digraph(engine='dot')
        graph.attr(rankdir='LR', size='8,5')
        
        graph.node('V', f'Fonte\n{v_fonte}V', shape='circle', style='filled', fillcolor='lightyellow')
        graph.node('N1', 'Nó de\nDivisão', shape='point')
        graph.node('N2', 'Nó de\nJunção', shape='point')
        graph.node('GND', 'Terra\n(0V)', shape='invtriangle')

        # Conexões
        graph.edge('V', 'N1', label=f' R1 ({r1}Ω)')
        graph.edge('N1', 'N2', label=f' R2 ({r2}Ω)')
        
        # Nó intermediário para representar a série R3+R4
        graph.node('N_M', 'Ramo\nSérie', shape='point')
        graph.edge('N1', 'N_M', label=f' R3 ({r3}Ω)')
        graph.edge('N_M', 'N2', label=f' R4 ({r4}Ω)')
        
        graph.edge('N2', 'GND')

        # Renderiza no Streamlit
        st.graphviz_chart(graph)

    with col2:
        st.subheader("Análise Analítica")
        st.metric(label="Resistência Equivalente (Req)", value=f"{req:.2f} Ω")
        st.metric(label="Corrente Total da Fonte (It)", value=f"{corrente_total:.3f} A")
        
        st.markdown("### Memória de Cálculo")
        st.latex(r"R_{ramo} = R_3 + R_4 = " + f"{r3} + {r4} = {r3+r4} \, \Omega")
        st.latex(r"R_{paralelo} = \frac{R_2 \cdot R_{ramo}}{R_2 + R_{ramo}} = " + f"{(r2*(r3+r4))/(r2+r3+r4):.2f} \, \Omega")
        st.latex(r"R_{eq} = R_1 + R_{paralelo} = " + f"{req:.2f} \, \Omega")

if __name__ == "__main__":
    main()
