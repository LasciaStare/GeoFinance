"""
Análisis Detallado por País/Activo

Esta página permite realizar análisis profundos de activos individuales
con gráficos de series temporales, estadísticas y distribuciones.
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Análisis por Activo",
    page_icon="📊",
    layout="wide"
)

# ============================================================================
# FUNCIÓN DE CARGA DE DATOS (copiada desde mapa.py)
# ============================================================================
@st.cache_data(ttl=3600)  # Cache de 1 hora
def cargar_y_procesar_datos():
    """
    Descarga datos de índices bursátiles del G20 + Colombia desde Yahoo Finance
    y calcula métricas de rendimiento y volatilidad.
    """
    
    # Definición de países, tickers e información del G20 + Colombia
    paises_info = {
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
        # Nota: Rusia suspendido temporalmente por sanciones internacionales
        # 'Rusia': {'ticker': '^IMOEX', 'iso3': 'RUS', 'tipo': 'indice'},
        'Arabia Saudita': {'ticker': '^TASI.SR', 'iso3': 'SAU', 'tipo': 'indice'},
        'Sudáfrica': {'ticker': '^J203.JO', 'iso3': 'ZAF', 'tipo': 'indice'},
        'Corea del Sur': {'ticker': '^KS11', 'iso3': 'KOR', 'tipo': 'indice'},
        'Turquía': {'ticker': 'XU100.IS', 'iso3': 'TUR', 'tipo': 'indice'},
        'Reino Unido': {'ticker': '^FTSE', 'iso3': 'GBR', 'tipo': 'indice'},
        'Estados Unidos': {'ticker': '^GSPC', 'iso3': 'USA', 'tipo': 'indice'},
        # Nota: Colombia tiene disponibilidad limitada en Yahoo Finance
        # 'Colombia': {'ticker': '^COLCAP', 'iso3': 'COL', 'tipo': 'indice'},
        
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
                
                # Calcular métricas
                precio_actual = datos['Precio'].iloc[-1]
                
                # 1. Rendimiento del último mes (%)
                if len(datos) >= 21:
                    precio_hace_mes = datos['Precio'].iloc[-21]
                    rendimiento_mes = ((precio_actual - precio_hace_mes) / precio_hace_mes) * 100
                else:
                    rendimiento_mes = np.nan
                
                # 2. Rendimiento del último año (%)
                if len(datos) >= 252:
                    precio_hace_año = datos['Precio'].iloc[-252]
                    rendimiento_año = ((precio_actual - precio_hace_año) / precio_hace_año) * 100
                else:
                    rendimiento_año = np.nan
                
                # 3. Volatilidad anualizada
                rendimientos_diarios = datos['Precio'].pct_change().dropna()
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
        df_historico['Fecha'] = pd.to_datetime(df_historico['Fecha'], utc=True)
        if df_historico['Fecha'].dt.tz is not None:
            df_historico['Fecha'] = df_historico['Fecha'].dt.tz_localize(None)
    
    return df_metricas, df_historico, paises_info


# ============================================================================
# TÍTULO PRINCIPAL
# ============================================================================
st.title("📊 Análisis Detallado por Activo")
st.markdown("""
Explora en profundidad el comportamiento histórico de cada activo con gráficos
interactivos, estadísticas y análisis de volatilidad.
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

st.success(f"✅ Datos cargados exitosamente para {len(df_metricas)} activos")

# ============================================================================
# BARRA LATERAL - CONTROLES
# ============================================================================
st.sidebar.header('🎛️ Configuración de Análisis')

# Selector de país/activo
pais_seleccionado = st.sidebar.selectbox(
    'Selecciona un activo:',
    options=sorted(df_metricas['Pais'].unique()),
    key="pais_analisis"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Periodo para Análisis**")

fecha_min = df_historico['Fecha'].min().date()
fecha_max = df_historico['Fecha'].max().date()
fecha_default_inicio = fecha_max - timedelta(days=365)

col_fecha1, col_fecha2 = st.sidebar.columns(2)

with col_fecha1:
    fecha_inicio = st.sidebar.date_input(
        '📆 Inicio',
        value=fecha_default_inicio,
        min_value=fecha_min,
        max_value=fecha_max,
        key='fecha_inicio_analisis'
    )

with col_fecha2:
    fecha_fin = st.sidebar.date_input(
        '📆 Fin',
        value=fecha_max,
        min_value=fecha_min,
        max_value=fecha_max,
        key='fecha_fin_analisis'
    )

if fecha_inicio > fecha_fin:
    st.sidebar.error("⚠️ La fecha de inicio debe ser anterior a la fecha de fin")
    fecha_inicio = fecha_fin

# Opciones adicionales
st.sidebar.markdown("---")
st.sidebar.markdown("**Opciones de Visualización**")
mostrar_promedio_movil = st.sidebar.checkbox("Mostrar Promedio Móvil", value=True)
if mostrar_promedio_movil:
    periodo_ma = st.sidebar.slider("Periodo (días)", 5, 200, 50)

# Botón para refrescar
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Refrescar Datos", width='stretch'):
    st.cache_data.clear()
    st.rerun()

# ============================================================================
# ANÁLISIS PRINCIPAL
# ============================================================================

st.header(f"📈 {pais_seleccionado}")

# Filtrar datos históricos del activo seleccionado
df_pais = df_historico[df_historico['Pais'] == pais_seleccionado].copy()

# Aplicar filtro de fechas
df_pais_filtrado = df_pais[
    (df_pais['Fecha'] >= pd.to_datetime(fecha_inicio)) &
    (df_pais['Fecha'] <= pd.to_datetime(fecha_fin))
].sort_values('Fecha')

if len(df_pais_filtrado) == 0:
    st.warning(f"⚠️ No hay datos disponibles para {pais_seleccionado} en el periodo seleccionado")
    st.stop()

# Obtener información del activo
info_activo = df_metricas[df_metricas['Pais'] == pais_seleccionado].iloc[0]
ticker = info_activo['Ticker']

st.info(f"**Ticker:** {ticker} | **Periodo:** {fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')}")

# ============================================================================
# MÉTRICAS CLAVE
# ============================================================================
col1, col2, col3, col4 = st.columns(4)

precio_inicial = df_pais_filtrado['Precio'].iloc[0]
precio_actual = df_pais_filtrado['Precio'].iloc[-1]
rendimiento_total = ((precio_actual - precio_inicial) / precio_inicial) * 100

# Calcular rendimientos para estadísticas
rendimientos = df_pais_filtrado['Precio'].pct_change().dropna()
volatilidad = rendimientos.std() * np.sqrt(252) * 100 if len(rendimientos) > 0 else 0

precio_max = df_pais_filtrado['Precio'].max()
precio_min = df_pais_filtrado['Precio'].min()

with col1:
    st.metric(
        "💰 Precio Actual",
        f"${precio_actual:,.2f}",
        f"{rendimiento_total:+.2f}%"
    )

with col2:
    st.metric(
        "📈 Precio Máximo",
        f"${precio_max:,.2f}",
        f"+{((precio_max - precio_inicial) / precio_inicial * 100):.2f}%"
    )

with col3:
    st.metric(
        "📉 Precio Mínimo",
        f"${precio_min:,.2f}",
        f"{((precio_min - precio_inicial) / precio_inicial * 100):.2f}%"
    )

with col4:
    st.metric(
        "📊 Volatilidad Anualizada",
        f"{volatilidad:.2f}%"
    )

# ============================================================================
# GRÁFICO DE SERIE TEMPORAL
# ============================================================================
st.markdown("---")
st.markdown("### 📈 Evolución del Precio")

fig_serie = go.Figure()

# Línea principal de precio
fig_serie.add_trace(go.Scatter(
    x=df_pais_filtrado['Fecha'],
    y=df_pais_filtrado['Precio'],
    mode='lines',
    name='Precio',
    line=dict(color='#2E86DE', width=2.5),
    fill='tozeroy',
    fillcolor='rgba(46, 134, 222, 0.1)',
    hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Precio: $%{y:,.2f}<extra></extra>'
))

# Promedio móvil (opcional)
if mostrar_promedio_movil and len(df_pais_filtrado) >= periodo_ma:
    df_pais_filtrado['MA'] = df_pais_filtrado['Precio'].rolling(window=periodo_ma).mean()
    fig_serie.add_trace(go.Scatter(
        x=df_pais_filtrado['Fecha'],
        y=df_pais_filtrado['MA'],
        mode='lines',
        name=f'Media Móvil ({periodo_ma}d)',
        line=dict(color='#FF6348', width=2.5, dash='dash'),
        hovertemplate='<b>%{x|%d/%m/%Y}</b><br>MA: $%{y:,.2f}<extra></extra>'
    ))

fig_serie.update_layout(
    title=dict(
        text=f'<b>Evolución de {pais_seleccionado}</b>',
        font=dict(size=18, family='Arial, sans-serif')
    ),
    xaxis_title='Fecha',
    yaxis_title='Precio ($)',
    hovermode='x unified',
    template='plotly_white',
    height=500,
    showlegend=True,
    paper_bgcolor='white',
    plot_bgcolor='rgba(240, 245, 250, 0.5)',
    xaxis=dict(
        showgrid=True,
        gridcolor='rgba(200, 200, 200, 0.3)'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='rgba(200, 200, 200, 0.3)',
        tickprefix='$',
        tickformat=',.0f'
    ),
    font=dict(family='Arial, sans-serif', size=12)
)

st.plotly_chart(fig_serie, width='stretch')

# ============================================================================
# GRÁFICOS ADICIONALES
# ============================================================================
st.markdown("---")
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### 📊 Distribución de Rendimientos Diarios")
    
    if len(rendimientos) > 0:
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=rendimientos * 100,
            nbinsx=40,
            name='Rendimientos',
            marker_color='#2E86DE',
            marker_line_color='white',
            marker_line_width=1,
            opacity=0.8,
            hovertemplate='Rendimiento: %{x:.2f}%<br>Frecuencia: %{y}<extra></extra>'
        ))
        
        fig_hist.update_layout(
            title=dict(
                text='<b>Distribución de Rendimientos</b>',
                font=dict(size=14)
            ),
            xaxis_title='Rendimiento Diario (%)',
            yaxis_title='Frecuencia',
            template='plotly_white',
            height=400,
            showlegend=False,
            paper_bgcolor='white',
            plot_bgcolor='rgba(240, 245, 250, 0.5)',
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(200, 200, 200, 0.3)',
                ticksuffix='%'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(200, 200, 200, 0.3)'
            ),
            font=dict(family='Arial, sans-serif', size=11)
        )
        
        st.plotly_chart(fig_hist, width='stretch')
    else:
        st.warning("No hay suficientes datos para mostrar distribución")

with col_right:
    st.markdown("#### 📈 Estadísticas del Periodo")
    
    # Crear tabla de estadísticas
    stats_data = {
        'Métrica': [
            'Rendimiento Total',
            'Rendimiento Promedio Diario',
            'Volatilidad Diaria',
            'Volatilidad Anualizada',
            'Sharpe Ratio (aprox)',
            'Número de Observaciones'
        ],
        'Valor': [
            f"{rendimiento_total:.2f}%",
            f"{(rendimientos.mean() * 100):.4f}%" if len(rendimientos) > 0 else "N/A",
            f"{(rendimientos.std() * 100):.4f}%" if len(rendimientos) > 0 else "N/A",
            f"{volatilidad:.2f}%",
            f"{(rendimientos.mean() / rendimientos.std() * np.sqrt(252)):.2f}" if len(rendimientos) > 0 and rendimientos.std() != 0 else "N/A",
            f"{len(df_pais_filtrado)}"
        ]
    }
    
    df_stats = pd.DataFrame(stats_data)
    st.dataframe(df_stats, width='stretch', hide_index=True)
    
    # Información adicional
    st.markdown("---")
    st.markdown("""
    **📌 Notas:**
    - Sharpe Ratio calculado asumiendo tasa libre de riesgo = 0
    - Volatilidad anualizada usa 252 días de trading
    - Rendimientos calculados sobre precios de cierre
    """)

# ============================================================================
# ANÁLISIS DE DRAWDOWN
# ============================================================================
st.markdown("---")
st.markdown("### 📉 Análisis de Drawdown")
st.caption("Caída porcentual desde el máximo histórico")

# Calcular drawdown
precio_acumulado_max = df_pais_filtrado['Precio'].expanding().max()
drawdown = (df_pais_filtrado['Precio'] - precio_acumulado_max) / precio_acumulado_max * 100

fig_drawdown = go.Figure()

fig_drawdown.add_trace(go.Scatter(
    x=df_pais_filtrado['Fecha'],
    y=drawdown,
    mode='lines',
    fill='tozeroy',
    name='Drawdown',
    line=dict(color='#E74C3C', width=2),
    fillcolor='rgba(231, 76, 60, 0.3)',
    hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Drawdown: %{y:.2f}%<extra></extra>'
))

fig_drawdown.update_layout(
    title=dict(
        text='<b>Drawdown (Caída desde Máximo)</b>',
        font=dict(size=16)
    ),
    xaxis_title='Fecha',
    yaxis_title='Drawdown (%)',
    template='plotly_white',
    height=350,
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='rgba(240, 245, 250, 0.5)',
    xaxis=dict(
        showgrid=True,
        gridcolor='rgba(200, 200, 200, 0.3)'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='rgba(200, 200, 200, 0.3)',
        ticksuffix='%'
    ),
    font=dict(family='Arial, sans-serif', size=12)
)

st.plotly_chart(fig_drawdown, width='stretch')

# Estadísticas de drawdown
max_drawdown = drawdown.min()
col1, col2 = st.columns(2)
with col1:
    st.metric("📉 Máximo Drawdown", f"{max_drawdown:.2f}%")
with col2:
    # Días en drawdown
    dias_drawdown = (drawdown < -1).sum()  # Días con más del 1% de caída
    st.metric("📅 Días en Drawdown (>1%)", f"{dias_drawdown}")

# ============================================================================
# PIE DE PÁGINA
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
📊 Datos proporcionados por Yahoo Finance | Actualización: 1 hora
</div>
""", unsafe_allow_html=True)
