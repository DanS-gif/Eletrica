import streamlit as st

def calcular_resistencia_equivalente(r1, r2, r3, r4):
    r_serie_ramo = r3 + r4
    r_paralelo = (r2 * r_serie_ramo) / (r2 + r_serie_ramo) if (r2 + r_serie_ramo) != 0 else 0
    return r1 + r_paralelo

def renderizar_svg(v_fonte, r1, r2, r3, r4):
    # Desenho técnico em vetor nativo escalável (HTML/SVG)
    return f"""
    <svg viewBox="0 0 500 300" xmlns="http://www.w3.org/2000/svg">
        <polyline points="50,150 50,50 150,50" fill="none" stroke="black" stroke-width="3"/>
        <polyline points="250,50 350,50 350,150" fill="none" stroke="black" stroke-width="3"/>
        <polyline points="350,250 350,250 50,250" fill="none" stroke="black" stroke-width="3"/>
        <polyline points="50,250 50,150" fill="none" stroke="black" stroke-width="3"/>
        <line x1="250" y1="50" x2="250" y2="250" stroke="black" stroke-width="3"/>

        <circle cx="50" cy="150" r="30" fill="white" stroke="black" stroke-width="3"/>
        <text x="50" y="145" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle">{v_fonte}V</text>
        <text x="50" y="165" font-family="Arial" font-size="16" font-weight="bold" text-anchor="middle">+-</text>

        <rect x="150" y="35" width="100" height="30" fill="white" stroke="black" stroke-width="3"/>
        <text x="200" y="25" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle">R1: {r1}Ω</text>

        <rect x="235" y="100" width="30" height="100" fill="white" stroke="black" stroke-width="3"/>
        <text x="275" y="155" font-family="Arial" font-size="14" font-weight="bold" text-anchor="start">R2: {r2}Ω</text>

        <rect x="335" y="70" width="30" height="60" fill="white" stroke="black" stroke-width="3"/>
        <text x="375" y="105" font-family="Arial" font-size="14" font-weight="bold" text-anchor="start">R3: {r3}Ω</text>

        <rect x="335" y="170" width="30" height="60" fill="white" stroke="black" stroke-width="3"/>
        <text x="375" y="205" font-family="Arial" font-size="14" font-weight="bold" text-anchor="start">R4: {r4}Ω</text>

        <circle cx="250" cy="50" r="5" fill="black"/>
        <circle cx="250" cy="250" r="5" fill="black"/>
    </svg>
    """

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
        st.components.v1.html(renderizar_svg(v_fonte, r1, r2, r3, r4), height=350)

    with col2:
        st.subheader("Análise Analítica")
        st.metric(label="Resistência Equivalente (Req)", value=f"{req:.2f} Ω")
        st.metric(label="Corrente Total da Fonte (It)", value=f"{corrente_total:.3f} A")
        
        st.markdown("### Memória de Cálculo")
        st.latex(r"R_{ramo} = R_3 + R_4 = " + f"{r3} + {r4} = {r3+r4} \\, \\Omega")
        st.latex(r"R_{paralelo} = \frac{R_2 \cdot R_{ramo}}{R_2 + R_{ramo}} = " + f"{(r2*(r3+r4))/(r2+r3+r4):.2f} \\, \\Omega")
        st.latex(r"R_{eq} = R_1 + R_{paralelo} = " + f"{req:.2f} \\, \\Omega")

if __name__ == "__main__":
    main()
