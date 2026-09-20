import streamlit as st
import schemdraw.elements as elm
import matplotlib.pyplot as plt

def calcular_resistencia_equivalente(r1, r2, r3, r4):
    """
    Calcula a resistência equivalente de um circuito misto de exemplo.
    Neste exemplo: R1 em série com o bloco paralelo (R2 || (R3 + R4))
    """
    r_serie_ramo = r3 + r4
    r_paralelo = (r2 * r_serie_ramo) / (r2 + r_serie_ramo) if (r2 + r_serie_ramo) != 0 else 0
    req = r1 + r_paralelo
    return req

def renderizar_esquematico(v_fonte, r1, r2, r3, r4):
    """
    Gera a figura Matplotlib contendo o desenho técnico do circuito.
    """
    with schemdraw.Drawing(show=False) as d:
        # Configuração da espessura da linha e tamanho da fonte para boa legibilidade
        d.config(lw=2, fontsize=12)
        
        # Fonte de Tensão e laço principal
        d += (V1 := elm.SourceV().up().label(f'{v_fonte} V'))
        d += elm.Line().right().length(2)
        
        # Resistor R1 em série
        d += (R1 := elm.Resistor().right().label(f'R1\n{r1} $\Omega$'))
        d += elm.Dot()
        d.push() # Salva o estado do nó superior
        
        # Resistor R2 em paralelo (ramo vertical)
        d += (R2 := elm.Resistor().down().label(f'R2\n{r2} $\Omega$'))
        d += elm.Dot()
        d += elm.Line().left().tox(V1.start)
        d.pop() # Retorna ao nó superior
        
        # Ramo com R3 e R4 em série
        d += elm.Line().right().length(2)
        d += (R3 := elm.Resistor().down().label(f'R3\n{r3} $\Omega$'))
        d += (R4 := elm.Resistor().down().label(f'R4\n{r4} $\Omega$'))
        
        # Fechando o circuito
        d += elm.Line().left().tox(R2.end)

        # Retorna a figura do Matplotlib gerada pelo Schemdraw
        return d.draw().fig

def main():
    st.set_page_config(page_title="Visualizador de Circuitos Mistos", layout="wide")
    st.title("Simulador Paramétrico de Circuitos Elétricos")
    st.markdown("Gerenciamento de parâmetros de resistores e renderização esquemática instantânea.")

    # Gerenciamento paramétrico na barra lateral
    st.sidebar.header("Parâmetros dos Elementos")
    
    v_fonte = st.sidebar.number_input("Tensão da Fonte (V)", min_value=1.0, value=10.0, step=1.0)
    
    st.sidebar.subheader("Resistências ($\Omega$)")
    r1 = st.sidebar.number_input("R1 (Série)", min_value=1.0, value=200.0, step=10.0)
    r2 = st.sidebar.number_input("R2 (Paralelo)", min_value=1.0, value=100.0, step=10.0)
    r3 = st.sidebar.number_input("R3 (Misto)", min_value=1.0, value=100.0, step=10.0)
    r4 = st.sidebar.number_input("R4 (Misto)", min_value=1.0, value=200.0, step=10.0)

    # Cálculos das grandezas
    req = calcular_resistencia_equivalente(r1, r2, r3, r4)
    corrente_total = v_fonte / req if req > 0 else 0

    # Layout Principal
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Planta Esquemática do Circuito")
        # Aciona o motor do Matplotlib para desenhar a topologia com base no estado atual
        fig = renderizar_esquematico(v_fonte, r1, r2, r3, r4)
        st.pyplot(fig)

    with col2:
        st.subheader("Análise Analítica")
        st.info("O circuito renderizado ao lado demonstra um nó dividindo a corrente principal em um ramo direto (R2) e um ramo misto (R3 + R4).")
        
        st.metric(label="Resistência Equivalente ($R_{eq}$)", value=f"{req:.2f} Ω")
        st.metric(label="Corrente Total da Fonte ($I_t$)", value=f"{corrente_total:.3f} A")
        
        st.markdown("### Memória de Cálculo")
        st.latex(r"R_{ramo} = R_3 + R_4 = " + f"{r3} + {r4} = {r3+r4} \, \Omega")
        st.latex(r"R_{paralelo} = \frac{R_2 \cdot R_{ramo}}{R_2 + R_{ramo}} = " + f"{(r2*(r3+r4))/(r2+r3+r4):.2f} \, \Omega")
        st.latex(r"R_{eq} = R_1 + R_{paralelo} = " + f"{req:.2f} \, \Omega")

if __name__ == "__main__":
    main()
