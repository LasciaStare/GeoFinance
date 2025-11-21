"""
Dashboard Exploratorio de Indicadores Macroeconómicos
Análisis estadístico de datos del Banco Mundial
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from scipy.stats import normaltest, shapiro, kstest
import os

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Exploratorio Macro",
    page_icon="🌍",
    layout="wide"
)

# ============================================================================
# FUNCIONES DE CARGA DE DATOS
# ============================================================================

@st.cache_data(ttl=3600)
def cargar_datos_macro():
    """Carga datos macroeconómicos del Banco Mundial desde parquet"""
    DATA_DIR = 'data'
    PATH_MACRO = os.path.join(DATA_DIR, 'datos_macro.parquet')
    PATH_PIVOTE = os.path.join(DATA_DIR, 'datos_macro_pivote.parquet')
    
    if not os.path.exists(PATH_MACRO):
        st.error("❌ No se encontraron datos macroeconómicos. Ejecuta: `python descarga_macro.py`")
        return None, None
    
    df_macro = pd.read_parquet(PATH_MACRO)
    
    if os.path.exists(PATH_PIVOTE):
        df_pivote = pd.read_parquet(PATH_PIVOTE)
    else:
        df_pivote = None
    
    return df_macro, df_pivote


# ============================================================================
# FUNCIONES DE ANÁLISIS ESTADÍSTICO
# ============================================================================

def test_normalidad(data, nombre_variable="Variable"):
    """
    Realiza tests de normalidad sobre una serie de datos.
    Retorna un diccionario con los resultados.
    """
    data_clean = data.dropna()
    
    if len(data_clean) < 3:
        return None
    
    resultados = {
        'n': len(data_clean),
        'media': data_clean.mean(),
        'mediana': data_clean.median(),
        'desviacion': data_clean.std(),
        'min': data_clean.min(),
        'max': data_clean.max(),
        'rango': data_clean.max() - data_clean.min(),
        'cv': (data_clean.std() / data_clean.mean() * 100) if data_clean.mean() != 0 else None,
        'asimetria': stats.skew(data_clean),
        'curtosis': stats.kurtosis(data_clean)
    }
    
    # Test de normalidad
    if len(data_clean) >= 8:
        try:
            # Shapiro-Wilk (mejor para n < 50)
            if len(data_clean) < 50:
                shapiro_stat, shapiro_p = shapiro(data_clean)
                resultados['shapiro_stat'] = shapiro_stat
                resultados['shapiro_p'] = shapiro_p
                resultados['shapiro_normal'] = shapiro_p > 0.05
            
            # D'Agostino-Pearson (mejor para n >= 20)
            if len(data_clean) >= 20:
                dagostino_stat, dagostino_p = normaltest(data_clean)
                resultados['dagostino_stat'] = dagostino_stat
                resultados['dagostino_p'] = dagostino_p
                resultados['dagostino_normal'] = dagostino_p > 0.05
        except:
            pass
    
    return resultados


def calcular_tendencia(anos, valores):
    """Calcula la tendencia lineal de una serie temporal."""
    if len(anos) < 2:
        return None
    
    # Regresión lineal
    slope, intercept, r_value, p_value, std_err = stats.linregress(anos, valores)
    
    return {
        'pendiente': slope,
        'intercepto': intercept,
        'r_squared': r_value**2,
        'p_value': p_value,
        'significativa': p_value < 0.05,
        'tendencia': 'creciente' if slope > 0 else 'decreciente' if slope < 0 else 'estable'
    }


def comparar_grupos(grupo1, grupo2, nombre1="Grupo 1", nombre2="Grupo 2"):
    """
    Compara dos grupos de datos usando t-test o Mann-Whitney según normalidad.
    """
    g1_clean = grupo1.dropna()
    g2_clean = grupo2.dropna()
    
    if len(g1_clean) < 3 or len(g2_clean) < 3:
        return None
    
    # Test de normalidad para ambos grupos
    _, p_norm1 = normaltest(g1_clean) if len(g1_clean) >= 20 else (None, None)
    _, p_norm2 = normaltest(g2_clean) if len(g2_clean) >= 20 else (None, None)
    
    # Decidir qué test usar
    if p_norm1 and p_norm2 and p_norm1 > 0.05 and p_norm2 > 0.05:
        # Ambos normales: usar t-test
        stat, p_value = stats.ttest_ind(g1_clean, g2_clean)
        test_usado = "t-test (paramétrico)"
    else:
        # Al menos uno no normal: usar Mann-Whitney
        stat, p_value = stats.mannwhitneyu(g1_clean, g2_clean, alternative='two-sided')
        test_usado = "Mann-Whitney U (no paramétrico)"
    
    return {
        'n1': len(g1_clean),
        'n2': len(g2_clean),
        'media1': g1_clean.mean(),
        'media2': g2_clean.mean(),
        'mediana1': g1_clean.median(),
        'mediana2': g2_clean.median(),
        'estadistico': stat,
        'p_value': p_value,
        'significativo': p_value < 0.05,
        'test_usado': test_usado
    }


# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================

st.title("🌍 Exploración de Indicadores Macroeconómicos")
st.markdown("""
Análisis estadístico profundo de los indicadores del Banco Mundial. 
Explora distribuciones, tendencias temporales y compara países mediante tests estadísticos rigurosos.
""")

# Cargar datos
with st.spinner('Cargando datos macroeconómicos...'):
    df_macro, df_pivote = cargar_datos_macro()

# Verificar que los datos se cargaron
if df_macro is None:
    st.stop()

# Normalizar datos
df_macro = df_macro.dropna(subset=['ISO3', 'Indicador', 'Ano', 'Valor']).copy()
df_macro['ISO3'] = df_macro['ISO3'].astype(str).str.upper()
df_macro['Ano'] = df_macro['Ano'].astype(int)

# Obtener información general
num_paises = df_macro['ISO3'].nunique()
num_indicadores = df_macro['Indicador'].nunique()
ano_min = df_macro['Ano'].min()
ano_max = df_macro['Ano'].max()
num_observaciones = len(df_macro)

st.success(f"✅ Datos cargados: {num_paises} países, {num_indicadores} indicadores, {ano_min}-{ano_max}")

# Métricas generales
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🌍 Países", num_paises)
with col2:
    st.metric("📊 Indicadores", num_indicadores)
with col3:
    st.metric("📅 Años", f"{ano_min}-{ano_max}")
with col4:
    st.metric("🔢 Observaciones", f"{num_observaciones:,}")

# ============================================================================
# BARRA LATERAL - CONFIGURACIÓN
# ============================================================================

st.sidebar.header("🎛️ Configuración del Análisis")

# Modo de análisis
modo_analisis = st.sidebar.radio(
    "Tipo de análisis:",
    ["📊 Análisis por Indicador", "🌍 Comparación de Países", "📈 Análisis Temporal"]
)

st.sidebar.markdown("---")

if modo_analisis == "📊 Análisis por Indicador":
    # Selector de indicador
    indicadores_disponibles = sorted(df_macro['Indicador'].unique())
    indicador_seleccionado = st.sidebar.selectbox(
        "Selecciona un indicador:",
        options=indicadores_disponibles,
        index=0
    )
    
    # Filtrar datos del indicador
    df_indicador = df_macro[df_macro['Indicador'] == indicador_seleccionado].copy()
    
    # Selector de país (opcional)
    paises_con_indicador = sorted(df_indicador['ISO3'].unique())
    analizar_pais_especifico = st.sidebar.checkbox("Filtrar por país específico", value=False)
    
    if analizar_pais_especifico:
        pais_seleccionado = st.sidebar.selectbox(
            "Selecciona país:",
            options=paises_con_indicador
        )
        df_indicador = df_indicador[df_indicador['ISO3'] == pais_seleccionado]
    
    # Rango de años
    anos_disponibles = sorted(df_indicador['Ano'].unique())
    if len(anos_disponibles) > 1:
        rango_anos = st.sidebar.slider(
            "Rango de años:",
            min_value=int(min(anos_disponibles)),
            max_value=int(max(anos_disponibles)),
            value=(int(min(anos_disponibles)), int(max(anos_disponibles)))
        )
        df_indicador = df_indicador[
            (df_indicador['Ano'] >= rango_anos[0]) & 
            (df_indicador['Ano'] <= rango_anos[1])
        ]
    
    # ============================================================================
    # ANÁLISIS POR INDICADOR
    # ============================================================================
    
    st.markdown("---")
    st.header(f"📊 Análisis: {indicador_seleccionado}")
    
    if len(df_indicador) == 0:
        st.warning("⚠️ No hay datos disponibles con los filtros seleccionados")
        st.stop()
    
    # Test de normalidad y estadísticas descriptivas
    resultados_stats = test_normalidad(df_indicador['Valor'], indicador_seleccionado)
    
    # Panel de métricas estadísticas
    st.subheader("📈 Estadísticas Descriptivas")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Media", f"{resultados_stats['media']:.2f}")
    with col2:
        st.metric("Mediana", f"{resultados_stats['mediana']:.2f}")
    with col3:
        st.metric("Desv. Est.", f"{resultados_stats['desviacion']:.2f}")
    with col4:
        st.metric("Mín - Máx", f"{resultados_stats['min']:.1f} / {resultados_stats['max']:.1f}")
    with col5:
        if resultados_stats['cv'] is not None:
            st.metric("CV (%)", f"{resultados_stats['cv']:.1f}")
        else:
            st.metric("CV (%)", "N/A")
    
    # Segunda fila de métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Observaciones", resultados_stats['n'])
    with col2:
        asimetria_texto = "Simétrica" if abs(resultados_stats['asimetria']) < 0.5 else \
                         ("Sesgada →" if resultados_stats['asimetria'] > 0 else "Sesgada ←")
        st.metric("Asimetría", f"{resultados_stats['asimetria']:.2f}", 
                 delta=asimetria_texto, delta_color="off")
    with col3:
        curtosis_texto = "Normal" if abs(resultados_stats['curtosis']) < 0.5 else \
                        ("Leptocúrtica" if resultados_stats['curtosis'] > 0 else "Platicúrtica")
        st.metric("Curtosis", f"{resultados_stats['curtosis']:.2f}",
                 delta=curtosis_texto, delta_color="off")
    with col4:
        if 'shapiro_p' in resultados_stats:
            es_normal = "✅ Normal" if resultados_stats['shapiro_normal'] else "❌ No normal"
            st.metric("Test Shapiro-Wilk", es_normal,
                     delta=f"p={resultados_stats['shapiro_p']:.4f}", delta_color="off")
        elif 'dagostino_p' in resultados_stats:
            es_normal = "✅ Normal" if resultados_stats['dagostino_normal'] else "❌ No normal"
            st.metric("Test D'Agostino", es_normal,
                     delta=f"p={resultados_stats['dagostino_p']:.4f}", delta_color="off")
        else:
            st.metric("Normalidad", "N/A", delta="Pocos datos", delta_color="off")
    
    # Visualizaciones
    st.markdown("---")
    st.subheader("📊 Visualizaciones")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribución", "📈 Serie Temporal", "🗺️ Por País", "📋 Tabla"])
    
    with tab1:
        col_hist, col_box = st.columns(2)
        
        with col_hist:
            # Histograma con curva normal
            fig_hist = go.Figure()
            
            fig_hist.add_trace(go.Histogram(
                x=df_indicador['Valor'],
                name='Distribución',
                nbinsx=30,
                marker_color='lightblue',
                marker_line_color='darkblue',
                marker_line_width=1.5,
                opacity=0.7
            ))
            
            # Curva normal teórica
            x_range = np.linspace(resultados_stats['min'], resultados_stats['max'], 100)
            normal_curve = stats.norm.pdf(x_range, resultados_stats['media'], resultados_stats['desviacion'])
            normal_curve = normal_curve * len(df_indicador) * (resultados_stats['max'] - resultados_stats['min']) / 30
            
            fig_hist.add_trace(go.Scatter(
                x=x_range,
                y=normal_curve,
                name='Distribución Normal',
                line=dict(color='red', width=2, dash='dash')
            ))
            
            fig_hist.update_layout(
                title='Histograma con Distribución Normal Teórica',
                xaxis_title='Valor',
                yaxis_title='Frecuencia',
                height=400,
                showlegend=True
            )
            
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col_box:
            # Box plot
            fig_box = go.Figure()
            
            fig_box.add_trace(go.Box(
                y=df_indicador['Valor'],
                name=indicador_seleccionado,
                marker_color='lightgreen',
                boxmean='sd'
            ))
            
            fig_box.update_layout(
                title='Box Plot (con media y desviación)',
                yaxis_title='Valor',
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig_box, use_container_width=True)
        
        # Q-Q Plot
        st.markdown("**Q-Q Plot (Normalidad)**")
        from scipy import stats as sp_stats
        
        fig_qq = go.Figure()
        
        sorted_data = np.sort(df_indicador['Valor'].dropna())
        theoretical_quantiles = sp_stats.norm.ppf(np.linspace(0.01, 0.99, len(sorted_data)))
        
        fig_qq.add_trace(go.Scatter(
            x=theoretical_quantiles,
            y=sorted_data,
            mode='markers',
            name='Datos observados',
            marker=dict(color='blue', size=6)
        ))
        
        # Línea de referencia
        fig_qq.add_trace(go.Scatter(
            x=[theoretical_quantiles.min(), theoretical_quantiles.max()],
            y=[theoretical_quantiles.min() * resultados_stats['desviacion'] + resultados_stats['media'],
               theoretical_quantiles.max() * resultados_stats['desviacion'] + resultados_stats['media']],
            mode='lines',
            name='Distribución normal',
            line=dict(color='red', dash='dash')
        ))
        
        fig_qq.update_layout(
            title='Q-Q Plot (Cuantiles Teóricos vs Observados)',
            xaxis_title='Cuantiles Teóricos',
            yaxis_title='Cuantiles Observados',
            height=400
        )
        
        st.plotly_chart(fig_qq, use_container_width=True)
    
    with tab2:
        if not analizar_pais_especifico:
            # Múltiples países
            st.info("💡 Mostrando evolución promedio de todos los países. Activa 'Filtrar por país' para análisis individual.")
            
            # Agrupar por año
            df_temporal = df_indicador.groupby('Ano').agg({
                'Valor': ['mean', 'std', 'count']
            }).reset_index()
            df_temporal.columns = ['Ano', 'Media', 'Desviacion', 'N_Paises']
            
            # Gráfico con banda de confianza
            fig_temporal = go.Figure()
            
            fig_temporal.add_trace(go.Scatter(
                x=df_temporal['Ano'],
                y=df_temporal['Media'],
                name='Media',
                line=dict(color='blue', width=3),
                mode='lines+markers'
            ))
            
            # Banda de confianza (± 1 desviación estándar)
            fig_temporal.add_trace(go.Scatter(
                x=df_temporal['Ano'].tolist() + df_temporal['Ano'].tolist()[::-1],
                y=(df_temporal['Media'] + df_temporal['Desviacion']).tolist() + \
                  (df_temporal['Media'] - df_temporal['Desviacion']).tolist()[::-1],
                fill='toself',
                fillcolor='rgba(0,100,200,0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='± 1 Desv. Est.',
                showlegend=True
            ))
            
            fig_temporal.update_layout(
                title=f'Evolución Temporal: {indicador_seleccionado} (Promedio Global)',
                xaxis_title='Año',
                yaxis_title='Valor',
                height=500,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_temporal, use_container_width=True)
            
            # Test de tendencia
            tendencia = calcular_tendencia(df_temporal['Ano'].values, df_temporal['Media'].values)
            
            if tendencia:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Tendencia", tendencia['tendencia'].capitalize())
                with col2:
                    st.metric("Pendiente anual", f"{tendencia['pendiente']:.4f}")
                with col3:
                    significancia = "✅ Significativa" if tendencia['significativa'] else "❌ No significativa"
                    st.metric("Regresión", significancia, 
                             delta=f"R²={tendencia['r_squared']:.3f}, p={tendencia['p_value']:.4f}",
                             delta_color="off")
        else:
            # Un solo país
            df_temporal = df_indicador.sort_values('Ano')
            
            fig_temporal = go.Figure()
            
            fig_temporal.add_trace(go.Scatter(
                x=df_temporal['Ano'],
                y=df_temporal['Valor'],
                name=pais_seleccionado,
                line=dict(color='green', width=3),
                mode='lines+markers',
                marker=dict(size=8)
            ))
            
            # Línea de tendencia
            if len(df_temporal) >= 2:
                tendencia = calcular_tendencia(df_temporal['Ano'].values, df_temporal['Valor'].values)
                
                if tendencia:
                    x_tend = np.array([df_temporal['Ano'].min(), df_temporal['Ano'].max()])
                    y_tend = tendencia['pendiente'] * x_tend + tendencia['intercepto']
                    
                    fig_temporal.add_trace(go.Scatter(
                        x=x_tend,
                        y=y_tend,
                        name='Tendencia',
                        line=dict(color='red', width=2, dash='dash')
                    ))
            
            fig_temporal.update_layout(
                title=f'Evolución Temporal: {indicador_seleccionado} - {pais_seleccionado}',
                xaxis_title='Año',
                yaxis_title='Valor',
                height=500,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_temporal, use_container_width=True)
            
            if tendencia:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Tendencia", tendencia['tendencia'].capitalize())
                with col2:
                    st.metric("Cambio anual", f"{tendencia['pendiente']:.4f}")
                with col3:
                    significancia = "✅ Significativa" if tendencia['significativa'] else "❌ No significativa"
                    st.metric("Regresión", significancia,
                             delta=f"R²={tendencia['r_squared']:.3f}, p={tendencia['p_value']:.4f}",
                             delta_color="off")
    
    with tab3:
        # Análisis por país
        st.subheader("Comparación entre países")
        
        # Calcular promedio por país
        df_por_pais = df_indicador.groupby('ISO3').agg({
            'Valor': ['mean', 'std', 'count']
        }).reset_index()
        df_por_pais.columns = ['ISO3', 'Media', 'Desviacion', 'Observaciones']
        df_por_pais = df_por_pais.sort_values('Media', ascending=False)
        
        # Top y Bottom países
        col_top, col_bottom = st.columns(2)
        
        with col_top:
            st.markdown("**🏆 Top 10 Países (Mayor valor promedio)**")
            fig_top = px.bar(
                df_por_pais.head(10),
                x='Media',
                y='ISO3',
                orientation='h',
                color='Media',
                color_continuous_scale='Greens',
                labels={'Media': 'Valor Promedio', 'ISO3': 'País'}
            )
            fig_top.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_top, use_container_width=True)
        
        with col_bottom:
            st.markdown("**📉 Bottom 10 Países (Menor valor promedio)**")
            fig_bottom = px.bar(
                df_por_pais.tail(10),
                x='Media',
                y='ISO3',
                orientation='h',
                color='Media',
                color_continuous_scale='Reds',
                labels={'Media': 'Valor Promedio', 'ISO3': 'País'}
            )
            fig_bottom.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_bottom, use_container_width=True)
        
        # Tabla completa
        with st.expander("📋 Ver tabla completa de países"):
            st.dataframe(
                df_por_pais,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Media": st.column_config.NumberColumn("Media", format="%.2f"),
                    "Desviacion": st.column_config.NumberColumn("Desv. Est.", format="%.2f"),
                    "Observaciones": st.column_config.NumberColumn("N", format="%d")
                }
            )
    
    with tab4:
        # Tabla de datos raw
        st.dataframe(
            df_indicador.sort_values(['Ano', 'ISO3'], ascending=[False, True]),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Valor": st.column_config.NumberColumn("Valor", format="%.4f")
            }
        )

elif modo_analisis == "🌍 Comparación de Países":
    # ============================================================================
    # COMPARACIÓN DE PAÍSES
    # ============================================================================
    
    # Selección de indicador
    indicadores_disponibles = sorted(df_macro['Indicador'].unique())
    indicador_seleccionado = st.sidebar.selectbox(
        "Selecciona indicador:",
        options=indicadores_disponibles,
        index=0
    )
    
    # Filtrar datos
    df_indicador = df_macro[df_macro['Indicador'] == indicador_seleccionado].copy()
    
    # Rango de años
    anos_disponibles = sorted(df_indicador['Ano'].unique())
    if len(anos_disponibles) > 1:
        rango_anos = st.sidebar.slider(
            "Rango de años:",
            min_value=int(min(anos_disponibles)),
            max_value=int(max(anos_disponibles)),
            value=(int(min(anos_disponibles)), int(max(anos_disponibles)))
        )
        df_indicador = df_indicador[
            (df_indicador['Ano'] >= rango_anos[0]) & 
            (df_indicador['Ano'] <= rango_anos[1])
        ]
    
    # Selección de países a comparar
    paises_disponibles = sorted(df_indicador['ISO3'].unique())
    
    paises_seleccionados = st.sidebar.multiselect(
        "Selecciona países a comparar:",
        options=paises_disponibles,
        default=paises_disponibles[:5] if len(paises_disponibles) >= 5 else paises_disponibles,
        max_selections=10
    )
    
    if not paises_seleccionados:
        st.warning("⚠️ Selecciona al menos un país para analizar")
        st.stop()
    
    # Filtrar por países seleccionados
    df_comparacion = df_indicador[df_indicador['ISO3'].isin(paises_seleccionados)].copy()
    
    st.markdown("---")
    st.header(f"🌍 Comparación: {indicador_seleccionado}")
    st.info(f"Comparando {len(paises_seleccionados)} países en el periodo {rango_anos[0]}-{rango_anos[1]}")
    
    # Estadísticas por país
    st.subheader("📊 Estadísticas por País")
    
    stats_paises = df_comparacion.groupby('ISO3').agg({
        'Valor': ['mean', 'median', 'std', 'min', 'max', 'count']
    }).reset_index()
    stats_paises.columns = ['País', 'Media', 'Mediana', 'Desv. Est.', 'Mínimo', 'Máximo', 'N']
    stats_paises = stats_paises.sort_values('Media', ascending=False)
    
    st.dataframe(
        stats_paises,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Media": st.column_config.NumberColumn("Media", format="%.2f"),
            "Mediana": st.column_config.NumberColumn("Mediana", format="%.2f"),
            "Desv. Est.": st.column_config.NumberColumn("Desv. Est.", format="%.2f"),
            "Mínimo": st.column_config.NumberColumn("Mínimo", format="%.2f"),
            "Máximo": st.column_config.NumberColumn("Máximo", format="%.2f"),
            "N": st.column_config.NumberColumn("Observaciones", format="%d")
        }
    )
    
    # Tests estadísticos de comparación
    if len(paises_seleccionados) == 2:
        st.markdown("---")
        st.subheader("🔬 Test Estadístico: Comparación de Dos Grupos")
        
        pais1, pais2 = paises_seleccionados
        datos1 = df_comparacion[df_comparacion['ISO3'] == pais1]['Valor']
        datos2 = df_comparacion[df_comparacion['ISO3'] == pais2]['Valor']
        
        resultado_test = comparar_grupos(datos1, datos2, pais1, pais2)
        
        if resultado_test:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(f"Media {pais1}", f"{resultado_test['media1']:.2f}")
                st.caption(f"n = {resultado_test['n1']}")
            
            with col2:
                st.metric(f"Media {pais2}", f"{resultado_test['media2']:.2f}")
                st.caption(f"n = {resultado_test['n2']}")
            
            with col3:
                diferencia = resultado_test['media1'] - resultado_test['media2']
                st.metric("Diferencia", f"{diferencia:+.2f}")
            
            with col4:
                significativo = "✅ Significativa" if resultado_test['significativo'] else "❌ No significativa"
                st.metric("Diferencia", significativo)
                st.caption(f"p = {resultado_test['p_value']:.4f}")
            
            st.info(f"**Test utilizado:** {resultado_test['test_usado']}")
            
            if resultado_test['significativo']:
                st.success(f"""
                ✅ **Existe una diferencia estadísticamente significativa** entre {pais1} y {pais2} 
                en el indicador {indicador_seleccionado} (p = {resultado_test['p_value']:.4f} < 0.05).
                """)
            else:
                st.warning(f"""
                ⚠️ **No se encontró evidencia estadística suficiente** de diferencia entre {pais1} y {pais2} 
                en el indicador {indicador_seleccionado} (p = {resultado_test['p_value']:.4f} ≥ 0.05).
                """)
    
    elif len(paises_seleccionados) > 2:
        st.markdown("---")
        st.subheader("🔬 Test Estadístico: Comparación Múltiple (ANOVA / Kruskal-Wallis)")
        
        # Preparar datos para test
        grupos = [df_comparacion[df_comparacion['ISO3'] == pais]['Valor'].dropna() 
                  for pais in paises_seleccionados]
        
        # Filtrar grupos vacíos
        grupos = [g for g in grupos if len(g) >= 2]
        
        if len(grupos) >= 2:
            # Test de normalidad por grupo
            normalidad_grupos = [normaltest(g)[1] > 0.05 if len(g) >= 20 else None for g in grupos]
            
            # Decidir qué test usar
            if all(n is not None for n in normalidad_grupos) and all(normalidad_grupos):
                # ANOVA (paramétrico)
                f_stat, p_value = stats.f_oneway(*grupos)
                test_usado = "ANOVA (paramétrico)"
            else:
                # Kruskal-Wallis (no paramétrico)
                h_stat, p_value = stats.kruskal(*grupos)
                test_usado = "Kruskal-Wallis (no paramétrico)"
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Test utilizado", test_usado)
            
            with col2:
                significativo = "✅ Significativo" if p_value < 0.05 else "❌ No significativo"
                st.metric("Resultado", significativo)
                st.caption(f"p-value = {p_value:.4f}")
            
            if p_value < 0.05:
                st.success(f"""
                ✅ **Existen diferencias estadísticamente significativas** entre al menos dos de los países 
                seleccionados en el indicador {indicador_seleccionado} (p = {p_value:.4f} < 0.05).
                """)
            else:
                st.warning(f"""
                ⚠️ **No se encontró evidencia estadística suficiente** de diferencias entre los países 
                seleccionados en el indicador {indicador_seleccionado} (p = {p_value:.4f} ≥ 0.05).
                """)
    
    # Visualizaciones
    st.markdown("---")
    st.subheader("📊 Visualizaciones Comparativas")
    
    tab1, tab2, tab3 = st.tabs(["📈 Series Temporales", "📊 Box Plots", "🎯 Distribuciones"])
    
    with tab1:
        # Series temporales superpuestas
        fig_series = go.Figure()
        
        for pais in paises_seleccionados:
            df_pais = df_comparacion[df_comparacion['ISO3'] == pais].sort_values('Ano')
            fig_series.add_trace(go.Scatter(
                x=df_pais['Ano'],
                y=df_pais['Valor'],
                name=pais,
                mode='lines+markers',
                line=dict(width=2.5),
                marker=dict(size=6)
            ))
        
        fig_series.update_layout(
            title=f'Evolución Comparativa: {indicador_seleccionado}',
            xaxis_title='Año',
            yaxis_title='Valor',
            height=500,
            hovermode='x unified',
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            )
        )
        
        st.plotly_chart(fig_series, use_container_width=True)
    
    with tab2:
        # Box plots comparativos
        fig_box = go.Figure()
        
        for pais in paises_seleccionados:
            df_pais = df_comparacion[df_comparacion['ISO3'] == pais]
            fig_box.add_trace(go.Box(
                y=df_pais['Valor'],
                name=pais,
                boxmean='sd'
            ))
        
        fig_box.update_layout(
            title=f'Distribución Comparativa: {indicador_seleccionado}',
            yaxis_title='Valor',
            height=500,
            showlegend=False
        )
        
        st.plotly_chart(fig_box, use_container_width=True)
    
    with tab3:
        # Histogramas superpuestos
        fig_hist = go.Figure()
        
        for pais in paises_seleccionados:
            df_pais = df_comparacion[df_comparacion['ISO3'] == pais]
            fig_hist.add_trace(go.Histogram(
                x=df_pais['Valor'],
                name=pais,
                opacity=0.6,
                nbinsx=20
            ))
        
        fig_hist.update_layout(
            title=f'Histogramas Superpuestos: {indicador_seleccionado}',
            xaxis_title='Valor',
            yaxis_title='Frecuencia',
            height=500,
            barmode='overlay'
        )
        
        st.plotly_chart(fig_hist, use_container_width=True)

elif modo_analisis == "📈 Análisis Temporal":
    # ============================================================================
    # ANÁLISIS TEMPORAL
    # ============================================================================
    
    # Selector de país
    paises_disponibles = sorted(df_macro['ISO3'].unique())
    pais_seleccionado = st.sidebar.selectbox(
        "Selecciona un país:",
        options=paises_disponibles,
        index=paises_disponibles.index('USA') if 'USA' in paises_disponibles else 0
    )
    
    # Filtrar por país
    df_pais = df_macro[df_macro['ISO3'] == pais_seleccionado].copy()
    
    # Año específico para análisis transversal
    anos_disponibles = sorted(df_pais['Ano'].unique())
    ano_seleccionado = st.sidebar.select_slider(
        "Año para análisis transversal:",
        options=anos_disponibles,
        value=anos_disponibles[-1] if anos_disponibles else None
    )
    
    st.markdown("---")
    st.header(f"📈 Análisis Temporal: {pais_seleccionado}")
    
    # Vista transversal de un año
    st.subheader(f"📊 Vista Transversal: Año {ano_seleccionado}")
    
    df_ano = df_pais[df_pais['Ano'] == ano_seleccionado].sort_values('Valor', ascending=False)
    
    if len(df_ano) == 0:
        st.warning(f"⚠️ No hay datos disponibles para {pais_seleccionado} en {ano_seleccionado}")
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Gráfico de barras
            fig_bar = px.bar(
                df_ano,
                x='Valor',
                y='Indicador',
                orientation='h',
                title=f'Indicadores Macroeconómicos - {pais_seleccionado} ({ano_seleccionado})',
                labels={'Valor': 'Valor', 'Indicador': 'Indicador'},
                color='Valor',
                color_continuous_scale='RdYlGn'
            )
            fig_bar.update_layout(height=600, showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            st.markdown("**Top 5 Indicadores**")
            st.dataframe(
                df_ano[['Indicador', 'Valor']].head(5),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Valor": st.column_config.NumberColumn("Valor", format="%.2f")
                }
            )
            
            st.markdown("**Bottom 5 Indicadores**")
            st.dataframe(
                df_ano[['Indicador', 'Valor']].tail(5),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Valor": st.column_config.NumberColumn("Valor", format="%.2f")
                }
            )
    
    # Análisis de correlaciones entre indicadores
    st.markdown("---")
    st.subheader("🔗 Correlaciones entre Indicadores")
    
    # Crear matriz de datos (indicadores x años)
    df_pivote_pais = df_pais.pivot(index='Ano', columns='Indicador', values='Valor')
    
    # Calcular matriz de correlación
    corr_matrix = df_pivote_pais.corr()
    
    # Visualizar con heatmap
    fig_corr = px.imshow(
        corr_matrix,
        labels=dict(x="Indicador", y="Indicador", color="Correlación"),
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        color_continuous_scale='RdBu_r',
        aspect="auto",
        zmin=-1,
        zmax=1
    )
    
    fig_corr.update_layout(
        title=f'Matriz de Correlación entre Indicadores - {pais_seleccionado}',
        height=600
    )
    
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Encontrar correlaciones fuertes
    st.markdown("**🔍 Correlaciones más Fuertes**")
    
    # Obtener pares de correlaciones (sin duplicados ni diagonal)
    correlaciones_list = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            correlaciones_list.append({
                'Indicador 1': corr_matrix.columns[i],
                'Indicador 2': corr_matrix.columns[j],
                'Correlación': corr_matrix.iloc[i, j]
            })
    
    df_correlaciones = pd.DataFrame(correlaciones_list)
    df_correlaciones = df_correlaciones.dropna()
    df_correlaciones['Correlación_Abs'] = df_correlaciones['Correlación'].abs()
    df_correlaciones = df_correlaciones.sort_values('Correlación_Abs', ascending=False)
    
    # Mostrar top 10
    st.dataframe(
        df_correlaciones[['Indicador 1', 'Indicador 2', 'Correlación']].head(10),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Correlación": st.column_config.NumberColumn("Correlación", format="%.3f")
        }
    )
    
    # Análisis de tendencias
    st.markdown("---")
    st.subheader("📈 Análisis de Tendencias")
    
    # Calcular tendencia para cada indicador
    tendencias_list = []
    
    for indicador in df_pais['Indicador'].unique():
        df_ind = df_pais[df_pais['Indicador'] == indicador].sort_values('Ano')
        
        if len(df_ind) >= 3:
            tendencia = calcular_tendencia(df_ind['Ano'].values, df_ind['Valor'].values)
            
            if tendencia:
                tendencias_list.append({
                    'Indicador': indicador,
                    'Tendencia': tendencia['tendencia'].capitalize(),
                    'Pendiente': tendencia['pendiente'],
                    'R²': tendencia['r_squared'],
                    'p-value': tendencia['p_value'],
                    'Significativa': '✅' if tendencia['significativa'] else '❌'
                })
    
    df_tendencias = pd.DataFrame(tendencias_list)
    df_tendencias = df_tendencias.sort_values('Pendiente', key=abs, ascending=False)
    
    st.dataframe(
        df_tendencias,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Pendiente": st.column_config.NumberColumn("Cambio Anual", format="%.4f"),
            "R²": st.column_config.NumberColumn("R²", format="%.3f"),
            "p-value": st.column_config.NumberColumn("p-value", format="%.4f")
        }
    )

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.caption("""
**📚 Referencias Metodológicas:**
- **Shapiro-Wilk / D'Agostino-Pearson**: Tests de normalidad
- **t-test / Mann-Whitney**: Comparación de dos grupos
- **ANOVA / Kruskal-Wallis**: Comparación de múltiples grupos
- **Nivel de significancia**: α = 0.05
- **Fuente de datos**: Banco Mundial (World Development Indicators)

Actualiza los datos con: `python descarga_macro.py`
""")
