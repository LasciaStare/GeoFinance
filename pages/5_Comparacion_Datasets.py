import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Comparación de Datasets", page_icon="⚖️", layout="wide")

st.title("⚖️ Comparación Estadística de Datasets")
st.markdown("""
Esta página realiza un análisis comparativo riguroso entre los **datos de mercados financieros** 
y los **indicadores macroeconómicos** para identificar diferencias estadísticamente significativas.
""")

# ==================== MAPEO DE PAÍSES ====================
MAPEO_PAISES = {
    'ARG': 'Argentina', 'AUS': 'Australia', 'AUT': 'Austria', 'BEL': 'Belgium',
    'BRA': 'Brazil', 'CAN': 'Canada', 'CHE': 'Switzerland', 'CHL': 'Chile',
    'CHN': 'China', 'COL': 'Colombia', 'DEU': 'Germany', 'DNK': 'Denmark',
    'EGY': 'Egypt', 'ESP': 'Spain', 'FRA': 'France', 'GBR': 'United Kingdom',
    'GRC': 'Greece', 'HKG': 'Hong Kong', 'IDN': 'Indonesia', 'IND': 'India',
    'IRL': 'Ireland', 'ISR': 'Israel', 'ITA': 'Italy', 'JPN': 'Japan',
    'KOR': 'South Korea', 'MEX': 'Mexico', 'MYS': 'Malaysia', 'NLD': 'Netherlands',
    'NOR': 'Norway', 'NZL': 'New Zealand', 'PER': 'Peru', 'PHL': 'Philippines',
    'POL': 'Poland', 'PRT': 'Portugal', 'RUS': 'Russia', 'SAU': 'Saudi Arabia',
    'SGP': 'Singapore', 'SWE': 'Sweden', 'THA': 'Thailand', 'TUR': 'Turkey',
    'TWN': 'Taiwan', 'USA': 'United States', 'VNM': 'Vietnam', 'ZAF': 'South Africa',
    'NGA': 'Nigeria', 'PAK': 'Pakistan'
}

# ==================== CARGA DE DATOS ====================
@st.cache_data
def cargar_datos():
    """Carga ambos datasets"""
    try:
        df_hist = pd.read_parquet('data/historico_activos.parquet')
        df_macro = pd.read_parquet('data/datos_macro.parquet')
        
        # Procesar fechas
        df_hist['Fecha'] = pd.to_datetime(df_hist['Fecha'])
        df_hist['Ano'] = df_hist['Fecha'].dt.year
        
        # Mapear países en macro de nombre completo a ISO3
        reverso_mapeo = {v: k for k, v in MAPEO_PAISES.items()}
        df_macro['ISO3_Original'] = df_macro['ISO3']
        df_macro['ISO3'] = df_macro['ISO3_Original'].map(reverso_mapeo)
        
        # Eliminar filas sin mapeo
        df_macro = df_macro.dropna(subset=['ISO3'])
        
        return df_hist, df_macro
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return None, None

df_hist, df_macro = cargar_datos()

if df_hist is None or df_macro is None:
    st.stop()

# ==================== SECCIÓN 1: COMPARACIÓN DE COBERTURA ====================
st.header("📊 1. Comparación de Cobertura")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Dataset de Mercados")
    st.metric("Observaciones", f"{len(df_hist):,}")
    st.metric("Países cubiertos", df_hist['ISO3'].nunique())
    st.metric("Activos", df_hist['Ticker'].nunique())
    st.metric("Periodo", f"{df_hist['Fecha'].min().year} - {df_hist['Fecha'].max().year}")
    st.metric("Granularidad", "Diaria")

with col2:
    st.subheader("🌍 Dataset Macroeconómico")
    st.metric("Observaciones", f"{len(df_macro):,}")
    st.metric("Países cubiertos", df_macro['ISO3'].nunique())
    st.metric("Indicadores", df_macro['Indicador'].nunique())
    st.metric("Periodo", f"{df_macro['Ano'].min()} - {df_macro['Ano'].max()}")
    st.metric("Granularidad", "Anual")

# Países en común
paises_comunes = set(df_hist['ISO3'].unique()) & set(df_macro['ISO3'].unique())
paises_solo_hist = set(df_hist['ISO3'].unique()) - set(df_macro['ISO3'].unique())
paises_solo_macro = set(df_macro['ISO3'].unique()) - set(df_hist['ISO3'].unique())

st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("🤝 Países en Común", len(paises_comunes))
col2.metric("📈 Solo en Mercados", len(paises_solo_hist))
col3.metric("🌍 Solo en Macro", len(paises_solo_macro))



# ==================== SECCIÓN 2: ANÁLISIS TEMPORAL ====================
st.header("⏱️ 2. Análisis de Cobertura Temporal")

# Calcular años comunes
anos_hist = set(df_hist['Ano'].unique())
anos_macro = set(df_macro['Ano'].unique())
anos_comunes = anos_hist & anos_macro

st.info(f"📅 **Años en común:** {[int(a) for a in sorted(anos_comunes)]}")

# Gráfico de líneas temporales
fig_temporal = go.Figure()

# Línea de mercados
anos_hist_sorted = [int(a) for a in sorted(anos_hist)]
fig_temporal.add_trace(go.Scatter(
    x=anos_hist_sorted,
    y=[1]*len(anos_hist_sorted),
    mode='markers+lines',
    name='Mercados Financieros',
    marker=dict(size=12, color='#3498db'),
    line=dict(width=3)
))

# Línea de macro
anos_macro_sorted = [int(a) for a in sorted(anos_macro)]
fig_temporal.add_trace(go.Scatter(
    x=anos_macro_sorted,
    y=[0.5]*len(anos_macro_sorted),
    mode='markers+lines',
    name='Indicadores Macro',
    marker=dict(size=12, color='#e74c3c'),
    line=dict(width=3)
))

# Marcar años comunes
anos_comunes_sorted = [int(a) for a in sorted(anos_comunes)]
fig_temporal.add_trace(go.Scatter(
    x=anos_comunes_sorted,
    y=[0.75]*len(anos_comunes_sorted),
    mode='markers',
    name='Años Comunes',
    marker=dict(size=15, color='#2ecc71', symbol='diamond')
))

fig_temporal.update_layout(
    title="Cobertura Temporal de Ambos Datasets",
    xaxis_title="Año",
    yaxis=dict(visible=False),
    height=300,
    showlegend=True
)

st.plotly_chart(fig_temporal, use_container_width=True)

# ==================== SECCIÓN 3: COMPARACIÓN ESTADÍSTICA POR PAÍS ====================
st.header("📊 3. Comparación Estadística por País")

st.markdown("""
Para cada país presente en ambos datasets, calculamos:
- **Rendimiento promedio anual** de los mercados financieros
- **Crecimiento del PIB** como indicador macroeconómico representativo
- **Test t de Student** para determinar si hay diferencias significativas
""")

# Preparar datos para comparación
@st.cache_data
def preparar_comparacion():
    """Prepara datos agregados por país y año para comparación"""
    
    # Calcular rendimiento anual por país (mercados)
    df_hist_ano = df_hist.groupby(['ISO3', 'Ano', 'Ticker'])['Precio'].agg(['first', 'last']).reset_index()
    df_hist_ano['Rendimiento'] = ((df_hist_ano['last'] - df_hist_ano['first']) / df_hist_ano['first']) * 100
    
    # Promedio por país-año (si hay múltiples activos)
    df_mercados_ano = df_hist_ano.groupby(['ISO3', 'Ano'])['Rendimiento'].mean().reset_index()
    df_mercados_ano.columns = ['ISO3', 'Ano', 'Rendimiento_Mercado']
    
    # Obtener PIB (indicador macroeconómico más representativo)
    df_pib = df_macro[df_macro['Codigo_Indicador'] == 'NY.GDP.MKTP.KD.ZG'].copy()
    df_pib = df_pib[['ISO3', 'Ano', 'Valor']].rename(columns={'Valor': 'Crecimiento_PIB'})
    
    # Merge de datos
    df_comparacion = pd.merge(
        df_mercados_ano,
        df_pib,
        on=['ISO3', 'Ano'],
        how='inner'
    )
    
    # Eliminar NaN
    df_comparacion = df_comparacion.dropna()
    
    return df_comparacion, df_mercados_ano, df_pib

df_comparacion, df_mercados_ano, df_pib = preparar_comparacion()

if len(df_comparacion) == 0:
    st.warning("⚠️ No hay datos suficientes para realizar la comparación estadística.")
    st.stop()

st.success(f"✅ Se encontraron **{len(df_comparacion)}** observaciones coincidentes (país-año) para comparación.")

# ==================== TEST DE HIPÓTESIS GLOBAL ====================
st.subheader("🎯 Test de Hipótesis: ¿Son diferentes los valores?")

# Normalidad
stat_shapiro_mercado, p_shapiro_mercado = stats.shapiro(df_comparacion['Rendimiento_Mercado'].sample(min(5000, len(df_comparacion))))
stat_shapiro_pib, p_shapiro_pib = stats.shapiro(df_comparacion['Crecimiento_PIB'].sample(min(5000, len(df_comparacion))))

col1, col2 = st.columns(2)

with col1:
    st.metric("Test Shapiro-Wilk (Mercados)", f"p-value: {p_shapiro_mercado:.4f}")
    if p_shapiro_mercado < 0.05:
        st.caption("❌ No sigue distribución normal")
    else:
        st.caption("✅ Sigue distribución normal")

with col2:
    st.metric("Test Shapiro-Wilk (PIB)", f"p-value: {p_shapiro_pib:.4f}")
    if p_shapiro_pib < 0.05:
        st.caption("❌ No sigue distribución normal")
    else:
        st.caption("✅ Sigue distribución normal")

# Elegir test apropiado
st.markdown("---")
st.subheader("📉 Test de Comparación de Medias")

if p_shapiro_mercado < 0.05 or p_shapiro_pib < 0.05:
    # Usar Mann-Whitney (no paramétrico)
    stat_test, p_test = stats.mannwhitneyu(
        df_comparacion['Rendimiento_Mercado'],
        df_comparacion['Crecimiento_PIB'],
        alternative='two-sided'
    )
    test_name = "Mann-Whitney U (no paramétrico)"
else:
    # Usar t-test (paramétrico)
    stat_test, p_test = stats.ttest_ind(
        df_comparacion['Rendimiento_Mercado'],
        df_comparacion['Crecimiento_PIB']
    )
    test_name = "t-test de Student (paramétrico)"

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Test utilizado", test_name)

with col2:
    st.metric("Estadístico", f"{stat_test:.4f}")

with col3:
    st.metric("p-value", f"{p_test:.6f}")

# Interpretación
st.markdown("---")
if p_test < 0.001:
    st.error("🔴 **DIFERENCIA MUY SIGNIFICATIVA** (p < 0.001)")
    st.markdown("Los valores de rendimiento de mercados y crecimiento del PIB son **estadísticamente muy diferentes**.")
elif p_test < 0.05:
    st.warning("🟡 **DIFERENCIA SIGNIFICATIVA** (p < 0.05)")
    st.markdown("Los valores de rendimiento de mercados y crecimiento del PIB son **estadísticamente diferentes**.")
else:
    st.success("🟢 **NO HAY DIFERENCIA SIGNIFICATIVA** (p >= 0.05)")
    st.markdown("No se puede rechazar la hipótesis de que ambos valores provienen de la misma distribución.")

# Estadísticas descriptivas
st.subheader("📊 Estadísticas Descriptivas")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**📈 Rendimiento de Mercados**")
    st.dataframe(df_comparacion['Rendimiento_Mercado'].describe(), use_container_width=True)

with col2:
    st.markdown("**🌍 Crecimiento del PIB**")
    st.dataframe(df_comparacion['Crecimiento_PIB'].describe(), use_container_width=True)

# ==================== VISUALIZACIONES COMPARATIVAS ====================
st.header("📊 4. Visualizaciones Comparativas")

# Histogramas superpuestos
fig_hist = go.Figure()

fig_hist.add_trace(go.Histogram(
    x=df_comparacion['Rendimiento_Mercado'],
    name='Rendimiento Mercados',
    opacity=0.7,
    marker_color='#3498db',
    nbinsx=50
))

fig_hist.add_trace(go.Histogram(
    x=df_comparacion['Crecimiento_PIB'],
    name='Crecimiento PIB',
    opacity=0.7,
    marker_color='#e74c3c',
    nbinsx=50
))

fig_hist.update_layout(
    title="Distribución de Valores: Mercados vs PIB",
    xaxis_title="Porcentaje (%)",
    yaxis_title="Frecuencia",
    barmode='overlay',
    height=500
)

st.plotly_chart(fig_hist, use_container_width=True)

# Box plots comparativos
fig_box = go.Figure()

fig_box.add_trace(go.Box(
    y=df_comparacion['Rendimiento_Mercado'],
    name='Rendimiento Mercados',
    marker_color='#3498db',
    boxmean='sd'
))

fig_box.add_trace(go.Box(
    y=df_comparacion['Crecimiento_PIB'],
    name='Crecimiento PIB',
    marker_color='#e74c3c',
    boxmean='sd'
))

fig_box.update_layout(
    title="Comparación de Distribuciones: Box Plots",
    yaxis_title="Porcentaje (%)",
    height=500
)

st.plotly_chart(fig_box, use_container_width=True)

# Scatter plot de correlación
fig_scatter = px.scatter(
    df_comparacion,
    x='Crecimiento_PIB',
    y='Rendimiento_Mercado',
    color='ISO3',
    title='Relación entre Crecimiento del PIB y Rendimiento de Mercados',
    labels={
        'Crecimiento_PIB': 'Crecimiento del PIB (%)',
        'Rendimiento_Mercado': 'Rendimiento de Mercados (%)'
    },
    height=600
)

# Añadir línea de tendencia manual
x_vals = df_comparacion['Crecimiento_PIB']
y_vals = df_comparacion['Rendimiento_Mercado']

# Calcular regresión lineal manual
z = np.polyfit(x_vals, y_vals, 1)
p = np.poly1d(z)
x_line = np.linspace(x_vals.min(), x_vals.max(), 100)
y_line = p(x_line)

fig_scatter.add_trace(go.Scatter(
    x=x_line,
    y=y_line,
    mode='lines',
    name='Línea de tendencia',
    line=dict(color='red', width=2, dash='dash')
))

st.plotly_chart(fig_scatter, use_container_width=True)

# Calcular correlación
correlacion = df_comparacion[['Rendimiento_Mercado', 'Crecimiento_PIB']].corr().iloc[0, 1]
st.metric("Correlación de Pearson", f"{correlacion:.4f}")

if abs(correlacion) > 0.7:
    st.success("🟢 Correlación fuerte")
elif abs(correlacion) > 0.4:
    st.warning("🟡 Correlación moderada")
else:
    st.info("🔵 Correlación débil")

# ==================== ANÁLISIS POR PAÍS ====================
st.header("🌍 5. Análisis Estadístico por País")

st.markdown("""
Comparación país por país para identificar donde las diferencias son más significativas.
""")

# Calcular tests por país
@st.cache_data
def calcular_tests_por_pais(df_comp):
    """Calcula tests estadísticos por país"""
    resultados = []
    
    for iso in df_comp['ISO3'].unique():
        df_pais = df_comp[df_comp['ISO3'] == iso]
        
        if len(df_pais) < 3:  # Necesitamos al menos 3 observaciones
            continue
        
        # Test de normalidad
        if len(df_pais) >= 3:
            _, p_norm_mercado = stats.shapiro(df_pais['Rendimiento_Mercado'])
            _, p_norm_pib = stats.shapiro(df_pais['Crecimiento_PIB'])
        else:
            p_norm_mercado = p_norm_pib = 1.0
        
        # Test de comparación
        if p_norm_mercado < 0.05 or p_norm_pib < 0.05:
            stat, p_value = stats.mannwhitneyu(
                df_pais['Rendimiento_Mercado'],
                df_pais['Crecimiento_PIB'],
                alternative='two-sided'
            )
            test_tipo = "Mann-Whitney"
        else:
            stat, p_value = stats.ttest_ind(
                df_pais['Rendimiento_Mercado'],
                df_pais['Crecimiento_PIB']
            )
            test_tipo = "t-test"
        
        # Correlación
        if len(df_pais) >= 3:
            corr = df_pais[['Rendimiento_Mercado', 'Crecimiento_PIB']].corr().iloc[0, 1]
        else:
            corr = np.nan
        
        resultados.append({
            'ISO3': iso,
            'N_Observaciones': len(df_pais),
            'Media_Mercado': df_pais['Rendimiento_Mercado'].mean(),
            'Media_PIB': df_pais['Crecimiento_PIB'].mean(),
            'Diferencia_Medias': df_pais['Rendimiento_Mercado'].mean() - df_pais['Crecimiento_PIB'].mean(),
            'Test': test_tipo,
            'P_Value': p_value,
            'Significativo': 'Sí' if p_value < 0.05 else 'No',
            'Correlacion': corr
        })
    
    return pd.DataFrame(resultados)

df_tests_pais = calcular_tests_por_pais(df_comparacion)

# Ordenar por p-value (más significativo primero)
df_tests_pais = df_tests_pais.sort_values('P_Value')

# Mostrar tabla
st.dataframe(
    df_tests_pais.style.format({
        'Media_Mercado': '{:.2f}%',
        'Media_PIB': '{:.2f}%',
        'Diferencia_Medias': '{:.2f}%',
        'P_Value': '{:.6f}',
        'Correlacion': '{:.4f}'
    }).background_gradient(subset=['P_Value'], cmap='RdYlGn_r'),
    use_container_width=True,
    height=400
)

# Resumen de significancia
n_significativos = (df_tests_pais['P_Value'] < 0.05).sum()
n_total = len(df_tests_pais)

col1, col2, col3 = st.columns(3)
col1.metric("Total de Países", n_total)
col2.metric("Con Diferencias Significativas", n_significativos)
col3.metric("% Significativos", f"{(n_significativos/n_total*100):.1f}%")

# Gráfico de p-values por país
fig_pvalues = go.Figure()

fig_pvalues.add_trace(go.Bar(
    x=df_tests_pais['ISO3'],
    y=df_tests_pais['P_Value'],
    marker_color=['#e74c3c' if p < 0.05 else '#95a5a6' for p in df_tests_pais['P_Value']],
    text=[f"{p:.4f}" for p in df_tests_pais['P_Value']],
    textposition='outside'
))

# Línea de significancia
fig_pvalues.add_hline(
    y=0.05, 
    line_dash="dash", 
    line_color="red",
    annotation_text="α = 0.05 (umbral de significancia)",
    annotation_position="right"
)

fig_pvalues.update_layout(
    title="P-Values por País (Test de Diferencias)",
    xaxis_title="País (ISO3)",
    yaxis_title="P-Value",
    height=500,
    showlegend=False
)

st.plotly_chart(fig_pvalues, use_container_width=True)

# ==================== CONCLUSIONES ====================
st.header("📝 6. Conclusiones de la Comparación")

st.markdown(f"""
### Hallazgos Principales:

1. **Cobertura de Datos:**
   - {len(paises_comunes)} países presentes en ambos datasets
   - {len(anos_comunes)} años con datos coincidentes ({int(min(anos_comunes))}-{int(max(anos_comunes))})
   - {len(df_comparacion)} observaciones válidas para comparación

2. **Diferencias Estadísticas Globales:**
   - Test utilizado: **{test_name}**
   - P-value: **{p_test:.6f}**
   - {'✅ Hay diferencias estadísticamente significativas' if p_test < 0.05 else '❌ No hay diferencias estadísticamente significativas'}

3. **Análisis por País:**
   - {n_significativos} de {n_total} países ({(n_significativos/n_total*100):.1f}%) muestran diferencias significativas
   - Correlación promedio: **{df_tests_pais['Correlacion'].mean():.4f}**

4. **Interpretación:**
""")

if p_test < 0.05:
    st.success("""
    ✅ **Los datasets son estadísticamente diferentes:**
    - Los rendimientos de mercados financieros y el crecimiento del PIB provienen de distribuciones diferentes
    - Esta diferencia es esperada ya que:
        - Los mercados reflejan expectativas futuras y sentimiento inversor
        - El PIB mide el crecimiento económico real pasado
        - Los mercados reaccionan más rápidamente a eventos
        - Diferentes escalas temporales (diaria vs anual)
    """)
else:
    st.info("""
    ℹ️ **No se detectan diferencias estadísticamente significativas:**
    - Ambas variables podrían provenir de distribuciones similares
    - Esto sugiere una fuerte relación entre mercados y economía real
    - Puede indicar mercados eficientes que reflejan fundamentos económicos
    """)

st.markdown("""
### 🎯 Implicaciones:

- **Para inversores:** {'Los mercados se desacopilan significativamente del crecimiento económico, requiriendo análisis independientes' if p_test < 0.05 else 'Los mercados reflejan bien los fundamentos económicos'}
- **Para analistas:** {'Considerar ambas fuentes de datos como complementarias pero distintas' if p_test < 0.05 else 'Alta confianza en la coherencia entre indicadores'}
- **Para investigadores:** {'Explorar factores adicionales que expliquen las diferencias' if p_test < 0.05 else 'Validación de la eficiencia del mercado'}
""")
