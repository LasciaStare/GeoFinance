"""
Análisis Detallado por País/Activo

Esta página permite realizar análisis profundos de activos individuales
con gráficos de series temporales, estadísticas y distribuciones.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import os

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Análisis por Activo",
    page_icon="📊",
    layout="wide"
)

# ============================================================================
# FUNCIÓN DE CARGA DE DATOS DESDE PARQUET
# ============================================================================
@st.cache_data(ttl=3600)
def cargar_datos_locales():
    """Carga datos de índices desde los archivos Parquet generados previamente."""

    data_dir = 'data'
    path_metricas = os.path.join(data_dir, 'metricas_activos.parquet')
    path_historico = os.path.join(data_dir, 'historico_activos.parquet')

    if not os.path.exists(path_metricas) or not os.path.exists(path_historico):
        st.error("❌ No se encontraron los archivos Parquet. Ejecuta `python descarga_datos.py` para generarlos.")
        st.stop()

    df_metricas = pd.read_parquet(path_metricas)
    df_historico = pd.read_parquet(path_historico)

    # Normalizar la columna Fecha
    if 'Fecha' in df_historico.columns:
        df_historico['Fecha'] = pd.to_datetime(df_historico['Fecha'])
        if df_historico['Fecha'].dt.tz is not None:
            df_historico['Fecha'] = df_historico['Fecha'].dt.tz_localize(None)

    # Reconstruir información básica de los activos
    paises_info = {}
    for _, row in df_metricas.iterrows():
        pais = row.get('Pais')
        iso = str(row.get('ISO3', '')).upper()
        ticker = row.get('Ticker')

        if pd.isna(pais) or pd.isna(ticker) or not iso:
            continue

        if iso in {'GOLD', 'SILVER', 'OIL', 'GAS', 'COPPER'}:
            tipo = 'commodity'
        elif iso in {'EUR', 'GBP', 'JPY', 'CNY', 'MXN', 'BRL'}:
            tipo = 'forex'
        else:
            tipo = 'indice'

        paises_info[pais] = {
            'ticker': ticker,
            'iso3': iso,
            'tipo': tipo
        }

    return df_metricas, df_historico, paises_info

# ============================================================================
# TÍTULO PRINCIPAL
# ============================================================================
st.title("📊 Análisis Detallado por Activo")
st.markdown(
    """
Explora en profundidad el comportamiento histórico de cada activo con gráficos
interactivos, estadísticas y análisis de volatilidad.
"""
)

# ============================================================================
# CARGAR DATOS
# ============================================================================
with st.spinner('Cargando datos locales de mercados globales...'):
    df_metricas, df_historico, paises_info = cargar_datos_locales()

# Verificar que se cargaron datos
if df_metricas.empty or df_historico.empty:
    st.error("❌ No se pudieron cargar datos desde los archivos locales. Ejecuta `python descarga_datos.py`.")
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
