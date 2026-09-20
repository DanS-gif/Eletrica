import streamlit as st
import matplotlib.pyplot as plt

def calcular_resistencia_equivalente(r1, r2, r3, r4):
    r_serie_ramo = r3 + r4
    r_paralelo = (r2 * r_serie_ramo) / (r2 + r_serie_ramo) if (r2 + r_serie_ramo) != 0 else 0
    return r1 + r_paralelo

def renderizar_esquematico_nativo(v_fonte, r1, r2, r3, r4):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axis('off') # Oculta os eixos cartesianos
    
    # Desenhar as linhas principais (fios do circuito)
    ax.plot([0, 0, 2], [0, 2, 2], color='black', lw=2) # Fio da fonte até R1
    ax.plot([2, 4, 4], [2, 2, 0], color='black', lw=2) # Fio de R1 para R3 e descida para R4
    ax.plot([0, 4], [0, 0], color='black', lw=2)       # Fio inferior de retorno (Terra)
    ax.plot([2, 2], [0, 2], color='black', lw=2)       # Fio do ramo central (R2)
    
    # Desenhar a Fonte de Tensão (Círculo)
    fonte = plt.Circle((0, 1), 0.3, color='white', ec='black', lw=2, zorder=3)
    ax.add_patch(fonte)
    ax.text(0, 1, f'{v_fonte}V\n(+ -)', ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Função auxiliar para desenhar as resistências como retângulos
    def desenhar_resistor(x, y, label, horizontal=True):
        if horizontal:
            rect = plt.Rectangle((x-0.4, y-0.15), 0.8, 0.3, color='white', ec='black', lw=2, zorder=3)
            ax.text(x, y+0.25, label, ha='center', va='bottom', fontsize=10)
        else:
            rect = plt.Rectangle((x-0.15, y-0.4), 0.3, 0.8, color='white', ec='black', lw=2, zorder=3)
            ax.text(x+0.25, y, label, ha='left', va='center', fontsize=10)
        ax.add_patch(rect)

    # Posicionar os componentes
    desenhar_resistor(1, 2, f'R1\n{r1}Ω', horizontal=True)
    desenhar_resistor(2, 1, f'R2\n{r2}Ω', horizontal=False)
    desenhar_resistor(3, 2, f'R3\n{r3}Ω', horizontal=True)
    desenhar_resistor(4, 1, f'R4\n{r4}Ω', horizontal=False)
    
    # Pontos de conexão (Nós de divisão de corrente)
    ax.plot([2], [2], marker='o', color='black', markersize=6)
    ax.plot([2], [0], marker='o', color='black', markersize=6)
    
    ax.set_xlim(-1, 5)
    ax.set_ylim(-0.5, 3)
    return fig

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
        fig = renderizar_esquematico_nativo(v_fonte, r1, r2, r3, r4)
        st.pyplot(fig)

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
