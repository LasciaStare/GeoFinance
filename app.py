import streamlit as st
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="GeoFinance - Salud Económica Global",
    page_icon="🌍",
    layout="wide"
)

# Banner principal
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; border-radius: 15px; margin-bottom: 30px;'>
    <h1 style='color: white; text-align: center; margin: 0; font-size: 3em;'>🌍 GeoFinance</h1>
    <h3 style='color: #f0f0f0; text-align: center; margin-top: 10px; font-weight: 300;'>
        Salud Económica Global y Predicción de Tendencias
    </h3>
</div>
""", unsafe_allow_html=True)

# Descripción del proyecto
st.markdown("""
## 📊 ¿Qué es GeoFinance?

GeoFinance es una plataforma integral de análisis que integra **datos de mercados financieros** 
e **indicadores macroeconómicos** para evaluar la salud económica mundial y descubrir patrones 
que ayuden a predecir tendencias futuras.
""")

# Características principales
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🗺️ Vista Global
    
    Explora el rendimiento de **60+ mercados** 
    en un mapa interactivo mundial.
    
    - Índices bursátiles
    - Forex y divisas
    - Commodities globales
    """)

with col2:
    st.markdown("""
    ### 📊 Análisis Macro
    
    Analiza **indicadores económicos** 
    del Banco Mundial con tests estadísticos.
    
    - PIB y crecimiento
    - Inflación y empleo
    - Comercio e inversión
    """)

with col3:
    st.markdown("""
    ### 📈 Insights Profundos
    
    Descubre **patrones y correlaciones** 
    entre economías y mercados.
    
    - EDA completo
    - Visualizaciones interactivas
    - Tests de hipótesis
    """)

# Datos del proyecto
st.markdown("---")
st.subheader("📚 Fuentes de Datos")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **📈 Mercados Financieros**
    - Fuente: Yahoo Finance
    - Cobertura: 2015-2025 (diaria)
    - 60+ activos globales
    """)

with col2:
    st.markdown("""
    **🌍 Indicadores Macroeconómicos**
    - Fuente: Banco Mundial
    - Cobertura: 2015-2025 (anual)
    - 8 indicadores principales
    """)

# Navegación
st.markdown("---")
st.subheader("🧭 Navegación")

st.markdown("""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff;'>
<p style='font-size: 16px; margin: 0;'>
👈 <strong>Usa el menú lateral</strong> para navegar entre las diferentes secciones:
</p>
<ul style='font-size: 15px; margin-top: 10px;'>
    <li><strong>🌍 Vista Global:</strong> Mapa interactivo del rendimiento mundial</li>
    <li><strong>📊 Exploratorio Macro:</strong> Análisis estadístico de indicadores económicos</li>
    <li><strong>📈 Análisis Activos:</strong> Series temporales y métricas por activo</li>
    <li><strong>🔍 EDA Completo:</strong> Exploración profunda de ambos datasets</li>
    <li><strong>🎯 Conclusiones:</strong> Marco del proyecto y hallazgos principales</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Métricas rápidas
st.markdown("---")
st.subheader("📊 Cobertura de Datos")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Países", "60+", delta="Con datos completos")

with col2:
    st.metric("Indicadores Macro", "8", delta="Del Banco Mundial")

with col3:
    st.metric("Años de Historia", "10+", delta="2015-2025")

with col4:
    st.metric("Observaciones", "1M+", delta="Datos diarios + anuales")

# Pregunta de investigación
st.markdown("---")
st.markdown("""
<div style='background-color: #fff3cd; padding: 25px; border-radius: 10px; margin: 20px 0;'>
<h3 style='color: #856404; margin-top: 0;'>❓ Pregunta Central</h3>
<p style='font-size: 16px; color: #856404;'>
<strong>¿Cómo se relacionan los indicadores macroeconómicos con el desempeño de los mercados 
financieros globales, y qué patrones pueden ayudarnos a predecir tendencias económicas futuras?</strong>
</p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("""
**GeoFinance Dashboard** | Desarrollado con Python y Streamlit  
Datos: Yahoo Finance & Banco Mundial | Actualizado: Octubre 2025
""")
