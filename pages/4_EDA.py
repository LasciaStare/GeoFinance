"""
EDA Completo: Análisis Exploratorio de Datos
Exploración profunda de los conjuntos de datos de mercados y macroeconómicos
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import os

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="EDA Completo",
    page_icon="🔍",
    layout="wide"
)

# ============================================================================
# FUNCIONES DE CARGA
# ============================================================================

@st.cache_data(ttl=3600)
def cargar_datos_mercados():
    """Carga datos de mercados desde parquet"""
    DATA_DIR = 'data'
    PATH_HISTORICO = os.path.join(DATA_DIR, 'historico_activos.parquet')
    PATH_METRICAS = os.path.join(DATA_DIR, 'metricas_activos.parquet')
    
    if not os.path.exists(PATH_HISTORICO) or not os.path.exists(PATH_METRICAS):
        return None, None
    
    df_historico = pd.read_parquet(PATH_HISTORICO)
    df_metricas = pd.read_parquet(PATH_METRICAS)
    
    # Normalizar fechas
    df_historico['Fecha'] = pd.to_datetime(df_historico['Fecha'])
    if df_historico['Fecha'].dt.tz is not None:
        df_historico['Fecha'] = df_historico['Fecha'].dt.tz_localize(None)
    
    return df_historico, df_metricas


@st.cache_data(ttl=3600)
def cargar_datos_macro():
    """Carga datos macroeconómicos desde parquet"""
    DATA_DIR = 'data'
    PATH_MACRO = os.path.join(DATA_DIR, 'datos_macro.parquet')
    
    if not os.path.exists(PATH_MACRO):
        return None
    
    return pd.read_parquet(PATH_MACRO)


# ============================================================================
# TÍTULO Y DESCRIPCIÓN
# ============================================================================

st.title("🔍 Análisis Exploratorio de Datos (EDA)")
st.markdown("""
Exploración completa de los dos conjuntos de datos principales: 
**Mercados Financieros** y **Indicadores Macroeconómicos**.
""")

# ============================================================================
# CARGAR DATOS
# ============================================================================

with st.spinner('Cargando datos...'):
    df_historico, df_metricas = cargar_datos_mercados()
    df_macro = cargar_datos_macro()

if df_historico is None or df_metricas is None or df_macro is None:
    st.error("❌ No se pudieron cargar los datos. Ejecuta los scripts de descarga.")
    st.stop()

# Normalizar datos macro
df_macro = df_macro.dropna(subset=['ISO3', 'Indicador', 'Ano', 'Valor']).copy()
df_macro['ISO3'] = df_macro['ISO3'].astype(str).str.upper()
df_macro['Ano'] = df_macro['Ano'].astype(int)

st.success("✅ Datos cargados correctamente")

# ============================================================================
# SELECTOR DE DATASET
# ============================================================================

st.sidebar.header("🎯 Configuración")
dataset_seleccionado = st.sidebar.radio(
    "Selecciona conjunto de datos:",
    ["📈 Mercados Financieros", "🌍 Indicadores Macroeconómicos", "🔗 Análisis Integrado"]
)

st.sidebar.markdown("---")

# ============================================================================
# EDA: MERCADOS FINANCIEROS
# ============================================================================

if dataset_seleccionado == "📈 Mercados Financieros":
    
    st.header("📈 EDA: Datos de Mercados Financieros")
    
    # Información general
    st.subheader("📊 Información General del Dataset")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Activos Únicos", df_metricas['Pais'].nunique())
    with col2:
        st.metric("Observaciones Históricas", f"{len(df_historico):,}")
    with col3:
        fecha_min = df_historico['Fecha'].min().strftime('%Y-%m-%d')
        fecha_max = df_historico['Fecha'].max().strftime('%Y-%m-%d')
        st.metric("Rango Temporal", f"{fecha_min}")
        st.caption(f"hasta {fecha_max}")
    with col4:
        dias_datos = (df_historico['Fecha'].max() - df_historico['Fecha'].min()).days
        st.metric("Días de Datos", f"{dias_datos:,}")
    
    # Estructura de los datos
    st.markdown("---")
    st.subheader("🔍 Estructura de los Datos")
    
    tab1, tab2, tab3 = st.tabs(["📋 Métricas por Activo", "📈 Datos Históricos", "🔢 Estadísticas"])
    
    with tab1:
        st.markdown("**Dataset: Métricas por Activo**")
        st.caption(f"Shape: {df_metricas.shape[0]} filas × {df_metricas.shape[1]} columnas")
        
        col_info, col_sample = st.columns([1, 2])
        
        with col_info:
            st.markdown("**Columnas disponibles:**")
            for col in df_metricas.columns:
                dtype = df_metricas[col].dtype
                nulls = df_metricas[col].isna().sum()
                st.text(f"• {col}: {dtype} ({nulls} nulos)")
        
        with col_sample:
            st.markdown("**Muestra de datos:**")
            st.dataframe(
                df_metricas.head(10),
                use_container_width=True,
                hide_index=True
            )
    
    with tab2:
        st.markdown("**Dataset: Histórico de Precios**")
        st.caption(f"Shape: {df_historico.shape[0]} filas × {df_historico.shape[1]} columnas")
        
        col_info, col_sample = st.columns([1, 2])
        
        with col_info:
            st.markdown("**Columnas disponibles:**")
            for col in df_historico.columns:
                dtype = df_historico[col].dtype
                nulls = df_historico[col].isna().sum()
                st.text(f"• {col}: {dtype} ({nulls} nulos)")
        
        with col_sample:
            st.markdown("**Muestra de datos:**")
            st.dataframe(
                df_historico.head(10),
                use_container_width=True,
                hide_index=True
            )
    
    with tab3:
        st.markdown("**Estadísticas Descriptivas: Métricas**")
        
        # Seleccionar columnas numéricas
        numeric_cols = df_metricas.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_cols:
            col_seleccionada = st.selectbox("Selecciona una métrica:", numeric_cols)
            
            # Estadísticas
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Media", f"{df_metricas[col_seleccionada].mean():.2f}")
            with col2:
                st.metric("Mediana", f"{df_metricas[col_seleccionada].median():.2f}")
            with col3:
                st.metric("Desv. Est.", f"{df_metricas[col_seleccionada].std():.2f}")
            with col4:
                st.metric("Mínimo", f"{df_metricas[col_seleccionada].min():.2f}")
            with col5:
                st.metric("Máximo", f"{df_metricas[col_seleccionada].max():.2f}")
            
            # Visualización
            col_hist, col_box = st.columns(2)
            
            with col_hist:
                fig_hist = px.histogram(
                    df_metricas,
                    x=col_seleccionada,
                    nbins=30,
                    title=f'Distribución: {col_seleccionada}',
                    labels={col_seleccionada: col_seleccionada}
                )
                fig_hist.update_layout(height=400)
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col_box:
                fig_box = px.box(
                    df_metricas,
                    y=col_seleccionada,
                    title=f'Box Plot: {col_seleccionada}',
                    labels={col_seleccionada: col_seleccionada}
                )
                fig_box.update_layout(height=400)
                st.plotly_chart(fig_box, use_container_width=True)
    
    # Análisis de datos faltantes
    st.markdown("---")
    st.subheader("🕳️ Análisis de Datos Faltantes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Métricas por Activo**")
        nulls_metricas = df_metricas.isnull().sum()
        nulls_pct_metricas = (nulls_metricas / len(df_metricas) * 100).round(2)
        
        df_nulls_metricas = pd.DataFrame({
            'Columna': nulls_metricas.index,
            'Nulos': nulls_metricas.values,
            'Porcentaje': nulls_pct_metricas.values
        })
        df_nulls_metricas = df_nulls_metricas[df_nulls_metricas['Nulos'] > 0]
        
        if len(df_nulls_metricas) > 0:
            st.dataframe(df_nulls_metricas, use_container_width=True, hide_index=True)
        else:
            st.success("✅ No hay datos faltantes")
    
    with col2:
        st.markdown("**Datos Históricos**")
        nulls_historico = df_historico.isnull().sum()
        nulls_pct_historico = (nulls_historico / len(df_historico) * 100).round(2)
        
        df_nulls_historico = pd.DataFrame({
            'Columna': nulls_historico.index,
            'Nulos': nulls_historico.values,
            'Porcentaje': nulls_pct_historico.values
        })
        df_nulls_historico = df_nulls_historico[df_nulls_historico['Nulos'] > 0]
        
        if len(df_nulls_historico) > 0:
            st.dataframe(df_nulls_historico, use_container_width=True, hide_index=True)
        else:
            st.success("✅ No hay datos faltantes")
    
    # Distribución temporal
    st.markdown("---")
    st.subheader("📅 Distribución Temporal")
    
    # Contar observaciones por año
    df_historico['Ano'] = df_historico['Fecha'].dt.year
    obs_por_ano = df_historico.groupby('Ano').size().reset_index(name='Observaciones')
    
    fig_temporal = px.bar(
        obs_por_ano,
        x='Ano',
        y='Observaciones',
        title='Observaciones por Año',
        labels={'Ano': 'Año', 'Observaciones': 'Número de Observaciones'}
    )
    fig_temporal.update_layout(height=400)
    st.plotly_chart(fig_temporal, use_container_width=True)
    
    # Cobertura por activo
    st.markdown("---")
    st.subheader("🗺️ Cobertura de Datos por Activo")
    
    cobertura = df_historico.groupby('Pais').agg({
        'Fecha': ['min', 'max', 'count']
    }).reset_index()
    cobertura.columns = ['Activo', 'Fecha_Inicio', 'Fecha_Fin', 'Observaciones']
    cobertura['Dias_Cobertura'] = (cobertura['Fecha_Fin'] - cobertura['Fecha_Inicio']).dt.days
    cobertura = cobertura.sort_values('Observaciones', ascending=False)
    
    st.dataframe(
        cobertura.head(20),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Fecha_Inicio": st.column_config.DateColumn("Inicio", format="YYYY-MM-DD"),
            "Fecha_Fin": st.column_config.DateColumn("Fin", format="YYYY-MM-DD"),
            "Observaciones": st.column_config.NumberColumn("Obs.", format="%d"),
            "Dias_Cobertura": st.column_config.NumberColumn("Días", format="%d")
        }
    )

# ============================================================================
# EDA: INDICADORES MACROECONÓMICOS
# ============================================================================

elif dataset_seleccionado == "🌍 Indicadores Macroeconómicos":
    
    st.header("🌍 EDA: Indicadores Macroeconómicos")
    
    # Información general
    st.subheader("📊 Información General del Dataset")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Países", df_macro['ISO3'].nunique())
    with col2:
        st.metric("Indicadores", df_macro['Indicador'].nunique())
    with col3:
        st.metric("Años", f"{df_macro['Ano'].min()}-{df_macro['Ano'].max()}")
    with col4:
        st.metric("Observaciones", f"{len(df_macro):,}")
    
    # Estructura
    st.markdown("---")
    st.subheader("🔍 Estructura del Dataset")
    
    col_info, col_sample = st.columns([1, 2])
    
    with col_info:
        st.markdown(f"**Shape:** {df_macro.shape[0]} filas × {df_macro.shape[1]} columnas")
        st.markdown("**Columnas:**")
        for col in df_macro.columns:
            dtype = df_macro[col].dtype
            nulls = df_macro[col].isna().sum()
            st.text(f"• {col}: {dtype} ({nulls} nulos)")
    
    with col_sample:
        st.markdown("**Muestra de datos:**")
        st.dataframe(
            df_macro.sample(min(10, len(df_macro))),
            use_container_width=True,
            hide_index=True
        )
    
    # Análisis por indicador
    st.markdown("---")
    st.subheader("📊 Análisis por Indicador")
    
    # Cobertura de indicadores
    cobertura_indicadores = df_macro.groupby('Indicador').agg({
        'ISO3': 'nunique',
        'Ano': ['min', 'max', 'count'],
        'Valor': ['mean', 'std']
    }).reset_index()
    cobertura_indicadores.columns = ['Indicador', 'N_Paises', 'Ano_Min', 'Ano_Max', 'Observaciones', 'Media', 'Desv_Est']
    cobertura_indicadores = cobertura_indicadores.sort_values('Observaciones', ascending=False)
    
    st.dataframe(
        cobertura_indicadores,
        use_container_width=True,
        hide_index=True,
        column_config={
            "N_Paises": st.column_config.NumberColumn("Países", format="%d"),
            "Ano_Min": st.column_config.NumberColumn("Año Min", format="%d"),
            "Ano_Max": st.column_config.NumberColumn("Año Max", format="%d"),
            "Observaciones": st.column_config.NumberColumn("Obs.", format="%d"),
            "Media": st.column_config.NumberColumn("Media", format="%.2f"),
            "Desv_Est": st.column_config.NumberColumn("Desv. Est.", format="%.2f")
        }
    )
    
    # Análisis por país
    st.markdown("---")
    st.subheader("🌍 Análisis por País")
    
    cobertura_paises = df_macro.groupby('ISO3').agg({
        'Indicador': 'nunique',
        'Ano': ['min', 'max', 'count']
    }).reset_index()
    cobertura_paises.columns = ['País', 'N_Indicadores', 'Ano_Min', 'Ano_Max', 'Observaciones']
    cobertura_paises = cobertura_paises.sort_values('Observaciones', ascending=False)
    
    col_tabla, col_viz = st.columns([1, 1])
    
    with col_tabla:
        st.markdown("**Top 20 Países por Cobertura**")
        st.dataframe(
            cobertura_paises.head(20),
            use_container_width=True,
            hide_index=True,
            column_config={
                "N_Indicadores": st.column_config.NumberColumn("Indicadores", format="%d"),
                "Ano_Min": st.column_config.NumberColumn("Desde", format="%d"),
                "Ano_Max": st.column_config.NumberColumn("Hasta", format="%d"),
                "Observaciones": st.column_config.NumberColumn("Obs.", format="%d")
            }
        )
    
    with col_viz:
        st.markdown("**Distribución de Observaciones**")
        fig_paises = px.bar(
            cobertura_paises.head(15),
            x='Observaciones',
            y='País',
            orientation='h',
            title='Top 15 Países',
            labels={'Observaciones': 'Número de Observaciones', 'País': 'País (ISO3)'}
        )
        fig_paises.update_layout(height=500)
        st.plotly_chart(fig_paises, use_container_width=True)
    
    # Evolución temporal
    st.markdown("---")
    st.subheader("📅 Evolución Temporal")
    
    obs_por_ano = df_macro.groupby('Ano').size().reset_index(name='Observaciones')
    
    fig_temporal = px.line(
        obs_por_ano,
        x='Ano',
        y='Observaciones',
        title='Observaciones por Año',
        labels={'Ano': 'Año', 'Observaciones': 'Número de Observaciones'},
        markers=True
    )
    fig_temporal.update_layout(height=400)
    st.plotly_chart(fig_temporal, use_container_width=True)
    
    # Datos faltantes
    st.markdown("---")
    st.subheader("🕳️ Análisis de Completitud")
    
    # Matriz de completitud (país x indicador)
    completitud = df_macro.groupby(['ISO3', 'Indicador']).size().reset_index(name='count')
    total_anos = df_macro['Ano'].nunique()
    
    completitud['pct_completo'] = (completitud['count'] / total_anos * 100).round(1)
    
    # Promedio de completitud por país
    completitud_paises = completitud.groupby('ISO3')['pct_completo'].mean().reset_index()
    completitud_paises.columns = ['País', 'Completitud_Promedio']
    completitud_paises = completitud_paises.sort_values('Completitud_Promedio', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Completitud Global", 
            f"{completitud['pct_completo'].mean():.1f}%",
            help="Porcentaje promedio de años con datos disponibles"
        )
    
    with col2:
        paises_completos = (completitud_paises['Completitud_Promedio'] > 80).sum()
        st.metric(
            "Países con >80% completitud",
            paises_completos,
            delta=f"{paises_completos / len(completitud_paises) * 100:.1f}% del total"
        )

# ============================================================================
# ANÁLISIS INTEGRADO
# ============================================================================

else:  # Análisis Integrado
    
    st.header("🔗 Análisis Integrado: Mercados vs Macro")
    
    st.info("Análisis de la intersección y relación entre ambos conjuntos de datos")
    
    # Normalizar ISOs
    df_metricas_norm = df_metricas.copy()
    df_metricas_norm['ISO3'] = df_metricas_norm['ISO3'].astype(str).str.upper()
    
    # Países en común
    paises_mercados = set(df_metricas_norm['ISO3'].unique())
    paises_macro = set(df_macro['ISO3'].unique())
    
    paises_comunes = paises_mercados & paises_macro
    paises_solo_mercados = paises_mercados - paises_macro
    paises_solo_macro = paises_macro - paises_mercados
    
    st.subheader("🌍 Cobertura Geográfica")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Países en Común", len(paises_comunes))
        st.caption("Disponibles en ambos datasets")
    
    with col2:
        st.metric("Solo en Mercados", len(paises_solo_mercados))
        st.caption("Sin datos macro")
    
    with col3:
        st.metric("Solo en Macro", len(paises_solo_macro))
        st.caption("Sin datos de mercados")
    
    # Diagrama de Venn (simulado con métricas)
    fig_venn = go.Figure()
    
    fig_venn.add_trace(go.Bar(
        x=['Solo Mercados', 'En Común', 'Solo Macro'],
        y=[len(paises_solo_mercados), len(paises_comunes), len(paises_solo_macro)],
        marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1'],
        text=[len(paises_solo_mercados), len(paises_comunes), len(paises_solo_macro)],
        textposition='auto'
    ))
    
    fig_venn.update_layout(
        title='Distribución de Cobertura entre Datasets',
        xaxis_title='Categoría',
        yaxis_title='Número de Países',
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_venn, use_container_width=True)
    
    # Análisis temporal comparativo
    st.markdown("---")
    st.subheader("📅 Cobertura Temporal Comparativa")
    
    # Rango temporal de mercados
    fecha_min_mercados = df_historico['Fecha'].min()
    fecha_max_mercados = df_historico['Fecha'].max()
    
    # Rango temporal de macro
    ano_min_macro = df_macro['Ano'].min()
    ano_max_macro = df_macro['Ano'].max()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📈 Mercados Financieros**")
        st.metric("Desde", fecha_min_mercados.strftime('%Y-%m-%d'))
        st.metric("Hasta", fecha_max_mercados.strftime('%Y-%m-%d'))
        st.metric("Días", (fecha_max_mercados - fecha_min_mercados).days)
    
    with col2:
        st.markdown("**🌍 Indicadores Macro**")
        st.metric("Desde", ano_min_macro)
        st.metric("Hasta", ano_max_macro)
        st.metric("Años", ano_max_macro - ano_min_macro + 1)
    
    # Países con mejor cobertura integrada
    st.markdown("---")
    st.subheader("🏆 Países con Mejor Cobertura Integrada")
    
    if len(paises_comunes) > 0:
        # Calcular métricas de cobertura
        cobertura_integrada = []
        
        for pais in paises_comunes:
            # Datos de mercados
            obs_mercados = len(df_historico[df_historico['ISO3'] == pais])
            
            # Datos macro
            obs_macro = len(df_macro[df_macro['ISO3'] == pais])
            indicadores_macro = df_macro[df_macro['ISO3'] == pais]['Indicador'].nunique()
            
            cobertura_integrada.append({
                'País': pais,
                'Obs_Mercados': obs_mercados,
                'Obs_Macro': obs_macro,
                'Indicadores_Macro': indicadores_macro,
                'Score_Cobertura': obs_mercados + obs_macro * 10
            })
        
        df_cobertura_integrada = pd.DataFrame(cobertura_integrada)
        df_cobertura_integrada = df_cobertura_integrada.sort_values('Score_Cobertura', ascending=False)
        
        st.dataframe(
            df_cobertura_integrada.head(20),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Obs_Mercados": st.column_config.NumberColumn("Obs. Mercados", format="%d"),
                "Obs_Macro": st.column_config.NumberColumn("Obs. Macro", format="%d"),
                "Indicadores_Macro": st.column_config.NumberColumn("Indicadores", format="%d"),
                "Score_Cobertura": st.column_config.NumberColumn("Score", format="%d")
            }
        )
    
    # Resumen estadístico comparativo
    st.markdown("---")
    st.subheader("📊 Resumen Estadístico Comparativo")
    
    summary_data = {
        'Métrica': [
            'Total de observaciones',
            'Entidades únicas',
            'Variables numéricas',
            'Cobertura temporal (años)',
            'Datos faltantes (%)'
        ],
        'Mercados Financieros': [
            f"{len(df_historico):,}",
            df_metricas['Pais'].nunique(),
            len(df_metricas.select_dtypes(include=[np.number]).columns),
            (fecha_max_mercados.year - fecha_min_mercados.year),
            f"{(df_historico.isnull().sum().sum() / (df_historico.shape[0] * df_historico.shape[1]) * 100):.2f}%"
        ],
        'Indicadores Macro': [
            f"{len(df_macro):,}",
            df_macro['ISO3'].nunique(),
            1,  # Solo 'Valor'
            (ano_max_macro - ano_min_macro + 1),
            f"{(df_macro.isnull().sum().sum() / (df_macro.shape[0] * df_macro.shape[1]) * 100):.2f}%"
        ]
    }
    
    df_summary = pd.DataFrame(summary_data)
    
    st.dataframe(df_summary, use_container_width=True, hide_index=True)


