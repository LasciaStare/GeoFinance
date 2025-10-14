import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="GeoFinance - Análisis Global de Mercados",
    page_icon="🌍",
    layout="wide"
)

# Título principal
st.title("🌍 GeoFinance - Análisis Global de Mercados")
st.markdown("""
### Visualización del rendimiento de índices bursátiles globales

Bienvenido a GeoFinance, tu plataforma para analizar el rendimiento de los principales 
índices bursátiles del mundo.

Navega a la sección **Mapa** en el menú lateral para ver el rendimiento YTD de los índices globales.
""")

# Información adicional
st.info("👈 Usa el menú lateral para navegar entre las diferentes secciones de la aplicación.")
