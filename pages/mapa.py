"""
Dashboard de Salud Económica Global (G20 + Colombia)

Archivo requirements.txt necesario:
streamlit
pandas
yfinance
plotly
numpy
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Dashboard Económico Global",
    page_icon="🌍",
    layout="wide"
)

# ============================================================================
# FUNCIÓN DE CARGA Y TRANSFORMACIÓN DE DATOS (ETL)
# ============================================================================
@st.cache_data(ttl=3600)  # Cache de 1 hora para optimizar rendimiento
def cargar_y_procesar_datos():
    """
    Descarga datos de índices bursátiles del G20 + Colombia desde Yahoo Finance
    y calcula métricas de rendimiento y volatilidad.
    
    Returns:
        tuple: (df_metricas, df_historico, paises_dict)
            - df_metricas: DataFrame con las métricas calculadas por país
            - df_historico: DataFrame con los datos históricos completos
            - paises_dict: Diccionario con información de países y tickers
    """
    
    # Definición de países, tickers e información - Índices Bursátiles Globales
    paises_info = {
        # G20 + Colombia
        'Argentina': {'ticker': '^MERV', 'iso3': 'ARG', 'tipo': 'indice'},
        'Australia': {'ticker': '^AXJO', 'iso3': 'AUS', 'tipo': 'indice'},
        'Brasil': {'ticker': '^BVSP', 'iso3': 'BRA', 'tipo': 'indice'},
        'Canadá': {'ticker': '^GSPTSE', 'iso3': 'CAN', 'tipo': 'indice'},
        'China': {'ticker': '000001.SS', 'iso3': 'CHN', 'tipo': 'indice'},
        'Francia': {'ticker': '^FCHI', 'iso3': 'FRA', 'tipo': 'indice'},
        'Alemania': {'ticker': '^GDAXI', 'iso3': 'DEU', 'tipo': 'indice'},
        'India': {'ticker': '^BSESN', 'iso3': 'IND', 'tipo': 'indice'},
        'Indonesia': {'ticker': '^JKSE', 'iso3': 'IDN', 'tipo': 'indice'},
        'Italia': {'ticker': 'FTSEMIB.MI', 'iso3': 'ITA', 'tipo': 'indice'},
        'Japón': {'ticker': '^N225', 'iso3': 'JPN', 'tipo': 'indice'},
        'México': {'ticker': '^MXX', 'iso3': 'MEX', 'tipo': 'indice'},
        'Rusia': {'ticker': 'IMOEX.ME', 'iso3': 'RUS', 'tipo': 'indice'},
        'Arabia Saudita': {'ticker': '^TASI.SR', 'iso3': 'SAU', 'tipo': 'indice'},
        'Sudáfrica': {'ticker': '^J203.JO', 'iso3': 'ZAF', 'tipo': 'indice'},
        'Corea del Sur': {'ticker': '^KS11', 'iso3': 'KOR', 'tipo': 'indice'},
        'Turquía': {'ticker': 'XU100.IS', 'iso3': 'TUR', 'tipo': 'indice'},
        'Reino Unido': {'ticker': '^FTSE', 'iso3': 'GBR', 'tipo': 'indice'},
        'Estados Unidos': {'ticker': '^GSPC', 'iso3': 'USA', 'tipo': 'indice'},
        'Colombia': {'ticker': '^COLCAP', 'iso3': 'COL', 'tipo': 'indice'},
        
        # Europa Adicional
        'España': {'ticker': '^IBEX', 'iso3': 'ESP', 'tipo': 'indice'},
        'Países Bajos': {'ticker': '^AEX', 'iso3': 'NLD', 'tipo': 'indice'},
        'Suiza': {'ticker': '^SSMI', 'iso3': 'CHE', 'tipo': 'indice'},
        'Suecia': {'ticker': '^OMX', 'iso3': 'SWE', 'tipo': 'indice'},
        'Noruega': {'ticker': 'OSEBX.OL', 'iso3': 'NOR', 'tipo': 'indice'},
        'Dinamarca': {'ticker': '^OMXC25', 'iso3': 'DNK', 'tipo': 'indice'},
        'Polonia': {'ticker': 'WIG.WA', 'iso3': 'POL', 'tipo': 'indice'},
        'Grecia': {'ticker': 'GD.AT', 'iso3': 'GRC', 'tipo': 'indice'},
        'Portugal': {'ticker': 'PSI20.LS', 'iso3': 'PRT', 'tipo': 'indice'},
        'Bélgica': {'ticker': '^BFX', 'iso3': 'BEL', 'tipo': 'indice'},
        'Austria': {'ticker': '^ATX', 'iso3': 'AUT', 'tipo': 'indice'},
        
        # América Latina Adicional
        'Chile': {'ticker': '^IPSA', 'iso3': 'CHL', 'tipo': 'indice'},
        'Perú': {'ticker': '^SPBLPGPT', 'iso3': 'PER', 'tipo': 'indice'},
        
        # Medio Oriente
        'Israel': {'ticker': '^TA125.TA', 'iso3': 'ISR', 'tipo': 'indice'},
        'Egipto': {'ticker': '^CASE30', 'iso3': 'EGY', 'tipo': 'indice'},
        
        # África
        'Nigeria': {'ticker': 'NGSEINDEX.LG', 'iso3': 'NGA', 'tipo': 'indice'},
        
        # Asia-Pacífico Adicional
        'Taiwán': {'ticker': '^TWII', 'iso3': 'TWN', 'tipo': 'indice'},
        'Tailandia': {'ticker': '^SET.BK', 'iso3': 'THA', 'tipo': 'indice'},
        'Malasia': {'ticker': '^KLSE', 'iso3': 'MYS', 'tipo': 'indice'},
        'Singapur': {'ticker': '^STI', 'iso3': 'SGP', 'tipo': 'indice'},
        'Hong Kong': {'ticker': '^HSI', 'iso3': 'HKG', 'tipo': 'indice'},
        'Nueva Zelanda': {'ticker': '^NZ50', 'iso3': 'NZL', 'tipo': 'indice'},
        'Filipinas': {'ticker': '^PSEi', 'iso3': 'PHL', 'tipo': 'indice'},
        'Vietnam': {'ticker': '^VNINDEX', 'iso3': 'VNM', 'tipo': 'indice'},
        'Pakistán': {'ticker': 'KSE100.KA', 'iso3': 'PAK', 'tipo': 'indice'},
        
        # Materias Primas
        'Oro': {'ticker': 'GC=F', 'iso3': 'GOLD', 'tipo': 'commodity'},
        'Plata': {'ticker': 'SI=F', 'iso3': 'SILVER', 'tipo': 'commodity'},
        'Petróleo WTI': {'ticker': 'CL=F', 'iso3': 'OIL', 'tipo': 'commodity'},
        'Gas Natural': {'ticker': 'NG=F', 'iso3': 'GAS', 'tipo': 'commodity'},
        'Cobre': {'ticker': 'HG=F', 'iso3': 'COPPER', 'tipo': 'commodity'},
        
        # Tasas de Cambio vs USD
        'EUR/USD': {'ticker': 'EURUSD=X', 'iso3': 'EUR', 'tipo': 'forex'},
        'GBP/USD': {'ticker': 'GBPUSD=X', 'iso3': 'GBP', 'tipo': 'forex'},
        'JPY/USD': {'ticker': 'JPYUSD=X', 'iso3': 'JPY', 'tipo': 'forex'},
        'CNY/USD': {'ticker': 'CNYUSD=X', 'iso3': 'CNY', 'tipo': 'forex'},
        'MXN/USD': {'ticker': 'MXN=X', 'iso3': 'MXN', 'tipo': 'forex'},
        'BRL/USD': {'ticker': 'BRL=X', 'iso3': 'BRL', 'tipo': 'forex'},
    }
    
    # Calcular fechas: últimos 5 años
    fecha_fin = datetime.now()
    fecha_inicio = fecha_fin - timedelta(days=5*365)
    
    # Contenedores para datos procesados
    datos_historicos = []
    metricas_paises = []
    
    # Barra de progreso para feedback visual
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_paises = len(paises_info)
    
    # Iterar sobre cada país para descargar y procesar datos
    for idx, (pais, info) in enumerate(paises_info.items()):
        status_text.text(f"Descargando datos de {pais}... ({idx+1}/{total_paises})")
        
        try:
            # Descargar datos históricos desde Yahoo Finance
            ticker = yf.Ticker(info['ticker'])
            datos = ticker.history(start=fecha_inicio, end=fecha_fin)
            
            if len(datos) > 0 and 'Close' in datos.columns:
                # Agregar información del país al DataFrame
                datos['Pais'] = pais
                datos['Ticker'] = info['ticker']
                datos['ISO3'] = info['iso3']
                # Convertir a datetime y eliminar zona horaria si existe
                fecha_index = pd.to_datetime(datos.index)
                if fecha_index.tz is not None:
                    fecha_index = fecha_index.tz_localize(None)
                datos['Fecha'] = fecha_index
                
                # Usar precio de cierre ajustado (o Close si no está disponible)
                precio_col = 'Adj Close' if 'Adj Close' in datos.columns else 'Close'
                datos['Precio'] = datos[precio_col]
                
                # Guardar datos históricos
                datos_historicos.append(datos[['Fecha', 'Precio', 'Pais', 'Ticker', 'ISO3']].reset_index(drop=True))
                
                # ============================================================
                # FEATURE ENGINEERING: Calcular métricas
                # ============================================================
                
                # 1. Rendimiento del último mes (%)
                if len(datos) >= 21:  # ~21 días hábiles en un mes
                    precio_actual = datos['Precio'].iloc[-1]
                    precio_hace_mes = datos['Precio'].iloc[-21]
                    rendimiento_mes = ((precio_actual - precio_hace_mes) / precio_hace_mes) * 100
                else:
                    rendimiento_mes = np.nan
                
                # 2. Rendimiento del último año (%)
                if len(datos) >= 252:  # ~252 días hábiles en un año
                    precio_hace_año = datos['Precio'].iloc[-252]
                    rendimiento_año = ((precio_actual - precio_hace_año) / precio_hace_año) * 100
                else:
                    rendimiento_año = np.nan
                
                # 3. Volatilidad anualizada
                # Calcular rendimientos diarios
                rendimientos_diarios = datos['Precio'].pct_change().dropna()
                
                # Volatilidad = desviación estándar * sqrt(252)
                if len(rendimientos_diarios) > 0:
                    volatilidad_anualizada = rendimientos_diarios.std() * np.sqrt(252) * 100
                else:
                    volatilidad_anualizada = np.nan
                
                # Guardar métricas calculadas
                metricas_paises.append({
                    'Pais': pais,
                    'ISO3': info['iso3'],
                    'Ticker': info['ticker'],
                    'Rendimiento_Ultimo_Mes': rendimiento_mes,
                    'Rendimiento_Ultimo_Año': rendimiento_año,
                    'Volatilidad_Anualizada': volatilidad_anualizada,
                    'Precio_Actual': precio_actual
                })
                
        except Exception as e:
            # Registrar error pero continuar con otros países
            st.warning(f"No se pudieron cargar datos de {pais}: {str(e)[:100]}")
        
        # Actualizar barra de progreso
        progress_bar.progress((idx + 1) / total_paises)
    
    # Limpiar elementos de UI temporal
    progress_bar.empty()
    status_text.empty()
    
    # Crear DataFrames finales
    df_metricas = pd.DataFrame(metricas_paises)
    df_historico = pd.concat(datos_historicos, ignore_index=True) if datos_historicos else pd.DataFrame()
    
    # Asegurar que la columna Fecha sea datetime sin zona horaria
    if not df_historico.empty and 'Fecha' in df_historico.columns:
        # Convertir a datetime, manejando tanto fechas con como sin timezone
        df_historico['Fecha'] = pd.to_datetime(df_historico['Fecha'], utc=True)
        if df_historico['Fecha'].dt.tz is not None:
            df_historico['Fecha'] = df_historico['Fecha'].dt.tz_localize(None)
    
    return df_metricas, df_historico, paises_info


def calcular_metricas_periodo(df_historico, fecha_inicio, fecha_fin):
    """
    Calcula métricas de rendimiento y volatilidad para un periodo específico.
    """
    # Filtrar datos por periodo
    fecha_inicio_dt = pd.to_datetime(fecha_inicio)
    fecha_fin_dt = pd.to_datetime(fecha_fin)
    
    df_periodo = df_historico[
        (df_historico['Fecha'] >= fecha_inicio_dt) & 
        (df_historico['Fecha'] <= fecha_fin_dt)
    ].copy()
    
    if df_periodo.empty:
        return pd.DataFrame()
    
    metricas_periodo = []
    
    # Agrupar por país/activo
    for nombre in df_periodo['Pais'].unique():
        datos_activo = df_periodo[df_periodo['Pais'] == nombre].sort_values('Fecha')
        
        if len(datos_activo) < 2:
            continue
            
        precio_inicial = datos_activo['Precio'].iloc[0]
        precio_final = datos_activo['Precio'].iloc[-1]
        
        # Rendimiento total del periodo
        rendimiento_periodo = ((precio_final - precio_inicial) / precio_inicial) * 100
        
        # Volatilidad del periodo
        rendimientos_diarios = datos_activo['Precio'].pct_change().dropna()
        if len(rendimientos_diarios) > 0:
            volatilidad = rendimientos_diarios.std() * np.sqrt(252) * 100
        else:
            volatilidad = np.nan
        
        metricas_periodo.append({
            'Pais': nombre,
            'ISO3': datos_activo['ISO3'].iloc[0],
            'Ticker': datos_activo['Ticker'].iloc[0],
            'Rendimiento_Periodo': rendimiento_periodo,
            'Volatilidad_Periodo': volatilidad,
            'Precio_Inicial': precio_inicial,
            'Precio_Final': precio_final
        })
    
    return pd.DataFrame(metricas_periodo)


# ============================================================================
# TÍTULO PRINCIPAL
# ============================================================================
st.title("🌍 Mapa de Índices Bursátiles Globales")
st.markdown("""
Visualización interactiva del rendimiento de índices bursátiles de más de 45 países.
Utiliza los controles de la barra lateral para personalizar el periodo de análisis.

*Incluye: G20, Europa, América Latina, Asia-Pacífico, Medio Oriente y África.*
""")

# ============================================================================
# CARGAR DATOS
# ============================================================================
with st.spinner('Cargando datos de mercados globales...'):
    df_metricas, df_historico, paises_info = cargar_y_procesar_datos()

# Verificar que se cargaron datos
if df_metricas.empty or df_historico.empty:
    st.error("❌ No se pudieron cargar suficientes datos. Verifica tu conexión a internet.")
    st.stop()

# Guardar datos en session_state para compartir con otras páginas
st.session_state['df_metricas'] = df_metricas
st.session_state['df_historico'] = df_historico
st.session_state['paises_info'] = paises_info

st.success(f"✅ Datos cargados exitosamente para {len(df_metricas)} activos")

# ============================================================================
# BARRA LATERAL - FILTROS DEL MAPA
# ============================================================================
st.sidebar.header('🎛️ Configuración del Mapa')

st.sidebar.markdown("**Periodo para Métricas**")

# Obtener rango de fechas disponible
fecha_min_mapa = df_historico['Fecha'].min().date()
fecha_max_mapa = df_historico['Fecha'].max().date()

# Selector de periodo predefinido o personalizado
tipo_periodo = st.sidebar.radio(
    "Tipo de periodo:",
    ["Predefinido", "Personalizado"],
    key="tipo_periodo_mapa"
)

if tipo_periodo == "Predefinido":
    periodo_mapa = st.sidebar.selectbox(
        "Selecciona periodo:",
        ["Último Mes", "Últimos 3 Meses", "Últimos 6 Meses", "Último Año", "Últimos 2 Años", "Todo el Periodo"],
        index=3
    )
    
    # Calcular fechas según el periodo
    fecha_fin_mapa = fecha_max_mapa
    if periodo_mapa == "Último Mes":
        fecha_inicio_mapa = fecha_max_mapa - timedelta(days=30)
    elif periodo_mapa == "Últimos 3 Meses":
        fecha_inicio_mapa = fecha_max_mapa - timedelta(days=90)
    elif periodo_mapa == "Últimos 6 Meses":
        fecha_inicio_mapa = fecha_max_mapa - timedelta(days=180)
    elif periodo_mapa == "Último Año":
        fecha_inicio_mapa = fecha_max_mapa - timedelta(days=365)
    elif periodo_mapa == "Últimos 2 Años":
        fecha_inicio_mapa = fecha_max_mapa - timedelta(days=730)
    else:  # Todo el Periodo
        fecha_inicio_mapa = fecha_min_mapa
else:
    st.sidebar.markdown("**Fechas Personalizadas**")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        fecha_inicio_mapa = st.sidebar.date_input(
            "Inicio",
            value=fecha_max_mapa - timedelta(days=365),
            min_value=fecha_min_mapa,
            max_value=fecha_max_mapa,
            key="fecha_inicio_mapa"
        )
    with col2:
        fecha_fin_mapa = st.sidebar.date_input(
            "Fin",
            value=fecha_max_mapa,
            min_value=fecha_min_mapa,
            max_value=fecha_max_mapa,
            key="fecha_fin_mapa"
        )
    
    if fecha_inicio_mapa > fecha_fin_mapa:
        st.sidebar.error("⚠️ Fecha inicio debe ser anterior a fecha fin")
        fecha_inicio_mapa = fecha_fin_mapa

# Métrica a visualizar
st.sidebar.markdown("---")
st.sidebar.markdown("**Métrica a Visualizar**")
metrica_mapa = st.sidebar.radio(
    "Selecciona métrica:",
    ["Rendimiento del Periodo", "Volatilidad del Periodo"],
    key="metrica_mapa"
)

# Botón para refrescar datos
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Refrescar Datos", width='stretch'):
    st.cache_data.clear()
    st.rerun()

# ============================================================================
# VISUALIZACIÓN DEL MAPA
# ============================================================================
st.header("🗺️ Mapa de Índices Bursátiles")

# Mostrar periodo seleccionado
st.info(f"📅 Analizando periodo: **{fecha_inicio_mapa.strftime('%d/%m/%Y')}** hasta **{fecha_fin_mapa.strftime('%d/%m/%Y')}**")

# Calcular métricas para el periodo seleccionado
with st.spinner('Calculando métricas para el periodo seleccionado...'):
    df_metricas_mapa = calcular_metricas_periodo(df_historico, fecha_inicio_mapa, fecha_fin_mapa)
    
    # Filtrar solo índices bursátiles
    if not df_metricas_mapa.empty:
        # Obtener el tipo de cada activo
        tipo_map = {pais: info.get('tipo', 'indice') for pais, info in paises_info.items()}
        df_metricas_mapa['Tipo'] = df_metricas_mapa['Pais'].map(tipo_map)
        # Solo mantener índices
        df_metricas_mapa = df_metricas_mapa[df_metricas_mapa['Tipo'] == 'indice']
    
    # Determinar la métrica a usar
    metrica_columna = 'Rendimiento_Periodo' if metrica_mapa == "Rendimiento del Periodo" else 'Volatilidad_Periodo'
    metrica_nombre = metrica_mapa
    
    # Filtrar datos válidos (sin NaN) para la métrica seleccionada
    df_mapa = df_metricas_mapa[df_metricas_mapa[metrica_columna].notna()].copy()
    
    if len(df_mapa) > 0:
        # Crear mapa coroplético con Plotly Express
        fig_mapa = px.choropleth(
            df_mapa,
            locations='ISO3',  # Códigos ISO 3 de países
            color=metrica_columna,  # Métrica a visualizar
            hover_name='Pais',  # Nombre del país en hover
            hover_data={
                'ISO3': False,  # No mostrar código ISO en hover
                metrica_columna: ':.2f',  # Formato de 2 decimales
                'Ticker': True,  # Mostrar ticker
                'Precio_Final': ':,.2f'  # Precio final con formato
            },
            color_continuous_scale='RdYlGn',  # Escala de rojo (mal) a verde (bien)
            labels={metrica_columna: metrica_nombre},
            title=f"<b>{metrica_nombre} - Índices Bursátiles Globales</b>"
        )
        
        # Personalizar diseño del mapa para aspecto profesional
        fig_mapa.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                coastlinecolor='#2C3E50',
                projection_type='natural earth',
                bgcolor='rgba(243, 246, 249, 0.5)',
                landcolor='rgba(220, 230, 242, 0.3)',
                oceancolor='rgba(173, 216, 230, 0.2)',
                showlakes=True,
                lakecolor='rgba(173, 216, 230, 0.3)'
            ),
            height=650,
            margin=dict(l=10, r=10, t=60, b=10),
            title_font=dict(size=20, family='Arial, sans-serif'),
            font=dict(family='Arial, sans-serif', size=12),
            paper_bgcolor='white',
            coloraxis_colorbar=dict(
                title=metrica_nombre,
                thickness=20,
                len=0.7,
                tickformat='.2f',
                ticksuffix='%'
            )
        )
        
        # Mostrar mapa
        st.plotly_chart(fig_mapa, width='stretch')
        
        # Mostrar estadísticas resumidas con iconos y colores
        st.markdown("### 📈 Estadísticas del Periodo")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            valor_max = df_mapa[metrica_columna].max()
            pais_max = df_mapa.loc[df_mapa[metrica_columna].idxmax(), 'Pais']
            st.metric(
                "🏆 Mejor Desempeño", 
                pais_max, 
                f"{valor_max:+.2f}%",
                delta_color="normal"
            )
        
        with col2:
            valor_min = df_mapa[metrica_columna].min()
            pais_min = df_mapa.loc[df_mapa[metrica_columna].idxmin(), 'Pais']
            st.metric(
                "📉 Menor Desempeño", 
                pais_min, 
                f"{valor_min:+.2f}%",
                delta_color="inverse"
            )
        
        with col3:
            promedio = df_mapa[metrica_columna].mean()
            st.metric("📊 Promedio Global", f"{promedio:+.2f}%")
        
        with col4:
            mediana = df_mapa[metrica_columna].median()
            st.metric("📈 Mediana", f"{mediana:+.2f}%")
        
        # Tabla con todos los activos
        st.markdown("---")
        st.markdown("### 📋 Ranking de Índices Bursátiles")
        
        # Preparar tabla ordenada
        df_tabla = df_mapa[['Pais', 'Ticker', metrica_columna, 'Precio_Final']].copy()
        df_tabla = df_tabla.sort_values(metrica_columna, ascending=False)
        df_tabla = df_tabla.reset_index(drop=True)
        df_tabla.index = df_tabla.index + 1  # Empezar índice en 1
        
        # Renombrar columnas para mejor presentación
        df_tabla.columns = ['País', 'Ticker', metrica_nombre, 'Precio Actual']
        
        # Aplicar formato condicional a la tabla
        def color_rendimiento(val):
            """Colorea el rendimiento: verde si positivo, rojo si negativo"""
            if isinstance(val, (int, float)):
                color = '#d4edda' if val > 0 else '#f8d7da' if val < 0 else '#fff3cd'
                return f'background-color: {color}'
            return ''
        
        # Mostrar tabla con estilo profesional
        st.dataframe(
            df_tabla.style.format({
                metrica_nombre: '{:+.2f}%',
                'Precio Actual': '${:,.2f}'
            }).applymap(
                color_rendimiento,
                subset=[metrica_nombre]
            ).set_properties(**{
                'text-align': 'center'
            }, subset=['Ticker', metrica_nombre, 'Precio Actual']),
            width='stretch',
            height=400
        )
    else:
        st.warning("⚠️ No hay datos suficientes para el periodo seleccionado. Intenta seleccionar un periodo más amplio.")

# ============================================================================
# INFORMACIÓN ADICIONAL
# ============================================================================
st.markdown("---")
st.info("""
**ℹ️ Información del Dashboard:**
- **Fuente de Datos:** Yahoo Finance
- **Periodo Analizado:** Últimos 5 años
- **Frecuencia de Actualización:** Los datos se cachean por 1 hora
- **Cobertura:** 45+ países de todos los continentes
- **Regiones:** G20, Europa, América Latina, Asia-Pacífico, Medio Oriente y África
- 👉 **Análisis Detallado:** Ve a la página **📊 analisis** para analizar índices, commodities y forex en profundidad
""")

# Footer
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p>Dashboard de Salud Económica Global | Desarrollado con Streamlit y Plotly</p>
</div>
""", unsafe_allow_html=True)

