"""
Conclusiones y Marco del Proyecto
Salud Económica Global y Predicción de Tendencias
"""

import streamlit as st
import plotly.graph_objects as go

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Conclusiones",
    page_icon="🎯",
    layout="wide"
)

# ============================================================================
# TÍTULO Y CONTEXTO
# ============================================================================

st.title("🎯 Marco del Proyecto y Conclusiones")

st.markdown("""
<div style='background-color: #f0f8ff; padding: 20px; border-radius: 10px; border-left: 5px solid #4CAF50;'>
<h2 style='color: #2c3e50; margin-top: 0;'>🌍 Salud Económica Global y Predicción de Tendencias</h2>
<p style='font-size: 18px; color: #34495e;'>
Análisis integral de mercados financieros e indicadores macroeconómicos para evaluar 
la salud económica mundial y predecir tendencias futuras.
</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# PREGUNTA DE INVESTIGACIÓN
# ============================================================================

st.markdown("---")
st.header("❓ Pregunta Central de Investigación")

st.markdown("""
<div style='background-color: #fff3cd; padding: 20px; border-radius: 10px; margin: 20px 0;'>
<h3 style='color: #856404; margin-top: 0;'>¿Cómo se relacionan los indicadores macroeconómicos con el desempeño 
de los mercados financieros globales, y qué patrones pueden ayudarnos a predecir tendencias económicas futuras?</h3>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### 🎯 Objetivos Específicos:

1. **Evaluar la salud económica global** mediante el análisis integrado de:
   - Índices bursátiles de 60+ países
   - Indicadores macroeconómicos del Banco Mundial
   - Commodities y divisas internacionales

2. **Identificar patrones y correlaciones** entre:
   - Variables macroeconómicas (PIB, inflación, desempleo, etc.)
   - Rendimiento de mercados financieros
   - Tendencias temporales y ciclos económicos

3. **Desarrollar capacidades predictivas** para:
   - Anticipar tendencias económicas
   - Detectar señales de alerta temprana
   - Identificar oportunidades de inversión
""")

# ============================================================================
# MODELO Y METODOLOGÍA
# ============================================================================

st.markdown("---")
st.header("📊 Modelo y Metodología")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🔬 Enfoque Analítico
    
    **1. Análisis Exploratorio de Datos (EDA)**
    - Caracterización de datasets
    - Identificación de patrones
    - Análisis de calidad de datos
    
    **2. Análisis Estadístico**
    - Tests de normalidad
    - Correlaciones de Pearson y Spearman
    - Regresión lineal para tendencias
    - Tests de hipótesis (t-test, ANOVA)
    
    **3. Visualización Interactiva**
    - Mapas geográficos dinámicos
    - Series temporales
    - Distribuciones estadísticas
    - Matrices de correlación
    """)

with col2:
    st.markdown("""
    ### 🎯 Componentes del Sistema
    
    **📈 Vista Global**
    - Mapa interactivo mundial
    - Métricas comparativas por país
    - Filtros dinámicos por categoría
    
    **🔍 Exploratorio Macroeconómico**
    - Análisis por indicador
    - Comparación multi-país
    - Análisis temporal y tendencias
    
    **📊 Análisis de Activos**
    - Series temporales individuales
    - Métricas de riesgo y rendimiento
    - Análisis de volatilidad
    
    **🔗 EDA Completo**
    - Exploración profunda de datos
    - Análisis integrado
    - Validación de calidad
    """)

# ============================================================================
# DIAGRAMA DE FLUJO
# ============================================================================

st.markdown("---")
st.header("🔄 Flujo del Análisis")

# Crear diagrama de flujo con Plotly
fig = go.Figure()

# Nodos del flujo
steps = [
    "1. Recopilación<br>de Datos",
    "2. Limpieza y<br>Normalización",
    "3. EDA y<br>Visualización",
    "4. Análisis<br>Estadístico",
    "5. Identificación<br>de Patrones",
    "6. Interpretación<br>y Conclusiones"
]

colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DFE6E9']

for i, (step, color) in enumerate(zip(steps, colors)):
    fig.add_trace(go.Scatter(
        x=[i],
        y=[0],
        mode='markers+text',
        marker=dict(size=80, color=color, line=dict(width=2, color='white')),
        text=step,
        textposition='middle center',
        textfont=dict(size=10, color='white', family='Arial Black'),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    if i < len(steps) - 1:
        fig.add_annotation(
            x=i+0.5, y=0,
            ax=i, ay=0,
            xref='x', yref='y',
            axref='x', ayref='y',
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=2,
            arrowcolor='#7f8c8d'
        )

fig.update_layout(
    height=200,
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, len(steps)-0.5]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1, 1]),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# FUENTES DE DATOS
# ============================================================================

st.markdown("---")
st.header("📚 Fuentes de Datos")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📈 Datos de Mercados
    
    **Fuente:** Yahoo Finance API
    
    **Contenido:**
    - 60+ índices bursátiles globales
    - Datos históricos diarios (2015-2025)
    - Precios de cierre ajustados
    - Métricas de rendimiento pre-calculadas
    
    **Cobertura:**
    - Índices de países desarrollados y emergentes
    - Forex (principales pares de divisas)
    - Commodities (oro, plata, petróleo, gas, cobre)
    
    **Actualización:** Diaria
    """)

with col2:
    st.markdown("""
    ### 🌍 Datos Macroeconómicos
    
    **Fuente:** Banco Mundial (World Development Indicators)
    
    **Contenido:**
    - Indicadores económicos anuales
    - Período: 2015-2025
    - 8 indicadores principales por país
    
    **Indicadores:**
    - PIB per cápita (USD corrientes)
    - Crecimiento del PIB (% anual)
    - Inflación (% anual)
    - Desempleo (% de la fuerza laboral)
    - Gasto público (% del PIB)
    - Exportaciones de bienes y servicios (% del PIB)
    - Inversión extranjera directa neta (% del PIB)
    - Deuda pública (% del PIB)
    
    **Actualización:** Anual
    """)

# ============================================================================
# HALLAZGOS PRINCIPALES
# ============================================================================

st.markdown("---")
st.header("🔍 Hallazgos Principales")

tab1, tab2, tab3 = st.tabs(["📊 Hallazgos Estadísticos", "🌍 Patrones Geográficos", "📈 Tendencias Temporales"])

with tab1:
    st.markdown("""
    ### 📊 Hallazgos Estadísticos
    
    **Calidad de los Datos:**
    - ✅ Ambos datasets presentan alta calidad con mínimos valores faltantes
    - ✅ Cobertura temporal consistente para la mayoría de países
    - ✅ Datos normalizados y listos para análisis
    
    **Distribuciones:**
    - Las métricas de rendimiento de mercados muestran distribuciones aproximadamente normales
    - Los indicadores macroeconómicos presentan alta variabilidad entre países
    - Se identificaron outliers en commodities debido a eventos de alta volatilidad
    
    **Correlaciones:**
    - Correlaciones significativas entre PIB y rendimiento bursátil en economías desarrolladas
    - Relación inversa entre inflación y rendimiento de mercados en algunos países emergentes
    - Alta correlación entre indicadores macroeconómicos relacionados (PIB, exportaciones, IED)
    """)

with tab2:
    st.markdown("""
    ### 🌍 Patrones Geográficos
    
    **Economías Desarrolladas:**
    - Mayor estabilidad en indicadores macroeconómicos
    - Correlaciones más predecibles entre macro y mercados
    - Menor volatilidad en mercados financieros
    
    **Economías Emergentes:**
    - Mayor volatilidad en indicadores y mercados
    - Relaciones más complejas y no lineales
    - Mayor sensibilidad a factores externos (commodities, divisa)
    
    **Commodities:**
    - Alta volatilidad con patrones cíclicos
    - Correlación con mercados de países productores
    - Sensibilidad a eventos geopolíticos
    
    **Regiones:**
    - Asia: Alto crecimiento, alta volatilidad
    - América: Diversidad de comportamientos
    - Europa: Mayor integración, correlaciones más fuertes
    - África: Datos limitados, alta variabilidad
    """)

with tab3:
    st.markdown("""
    ### 📈 Tendencias Temporales
    
    **2015-2019: Expansión Global**
    - Crecimiento sostenido de mercados
    - Mejora en indicadores macroeconómicos
    - Baja volatilidad relativa
    
    **2020: Crisis COVID-19**
    - Caída abrupta de mercados (marzo 2020)
    - Deterioro de indicadores macro
    - Recuperación rápida con estímulos fiscales
    
    **2021-2022: Recuperación y Normalización**
    - Rebote fuerte de mercados
    - Presiones inflacionarias
    - Normalización de políticas monetarias
    
    **2023-2025: Ajuste y Consolidación**
    - Volatilidad moderada
    - Ajuste de expectativas
    - Divergencia entre economías
    
    **Ciclos Identificados:**
    - Ciclos de mercado correlacionados con ciclos económicos
    - Anticipación de mercados a cambios macroeconómicos (3-6 meses)
    - Patrones estacionales en algunos indicadores
    """)

# ============================================================================
# APLICACIONES
# ============================================================================

st.markdown("---")
st.header("🎯 Aplicaciones Prácticas")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 💼 Para Inversores
    
    - **Diversificación geográfica** informada por correlaciones
    - **Identificación de oportunidades** en mercados subvalorados
    - **Gestión de riesgo** basada en indicadores macro
    - **Timing de mercado** usando señales adelantadas
    """)

with col2:
    st.markdown("""
    ### 🏛️ Para Policy Makers
    
    - **Monitoreo de salud económica** en tiempo real
    - **Benchmarking internacional** de indicadores
    - **Evaluación de políticas** mediante comparaciones
    - **Identificación de vulnerabilidades** sistémicas
    """)

with col3:
    st.markdown("""
    ### 📊 Para Analistas
    
    - **Framework analítico** reproducible
    - **Visualizaciones interactivas** para reportes
    - **Tests estadísticos** rigurosos
    - **Datos actualizables** para seguimiento continuo
    """)




# ============================================================================
# REFERENCIAS Y RECURSOS
# ============================================================================

st.markdown("---")
st.header("📚 Referencias y Recursos")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📖 Referencias Metodológicas
    
    - **Tests Estadísticos:**
      - Shapiro-Wilk Test for Normality
      - D'Agostino-Pearson Test
      - Pearson & Spearman Correlations
      - Student's t-test & Mann-Whitney U
      - ANOVA & Kruskal-Wallis
    
    - **Interpretación:**
      - Cohen (1988): Effect Sizes
      - Nivel de significancia: α = 0.05
    """)

with col2:
    st.markdown("""
    ### 🔗 Fuentes de Datos
    
    - **Yahoo Finance:** https://finance.yahoo.com
    - **Banco Mundial:** https://data.worldbank.org
    - **World Development Indicators**
    
    ### 🛠️ Tecnologías
    
    - Python 3.x
    - Streamlit
    - Pandas & NumPy
    - Plotly
    - SciPy
    - yfinance & wbdata
    """)

st.markdown("---")
st.caption("""
**GeoFinance Dashboard** | Análisis de Salud Económica Global  
Desarrollado con ❤️ usando Python y Streamlit | Datos actualizados: Octubre 2025
""")
