# 🌍 GeoFinance - Salud Económica Global y Predicción de Tendencias

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Dashboard interactivo de análisis integral que combina **mercados financieros** e **indicadores macroeconómicos** para evaluar la salud económica mundial y predecir tendencias futuras.

---

## 🎯 Pregunta Central de Investigación

> **"¿Cómo se relacionan los indicadores macroeconómicos con el desempeño de los mercados financieros globales, y qué patrones pueden ayudarnos a predecir tendencias económicas futuras?"**

---

## Características Principales

- 🗺️ **Vista Global Interactiva**: Mapa mundial con rendimiento de 60+ mercados
- 📊 **Análisis Exploratorio Macro**: 3 modos de análisis con tests estadísticos rigurosos
- 📈 **Análisis de Activos**: Series temporales, distribuciones y drawdowns
- 🔍 **EDA Completo**: Exploración profunda de calidad y estructura de datos
- ⚖️ **Comparación Estadística**: Tests de hipótesis entre mercados y macro
- 🎯 **Conclusiones y Modelo**: Marco de investigación y propuesta de ML

---

## Datos Analizados

| Dataset                  | Observaciones | Cobertura                 | Periodo   | Granularidad |
| ------------------------ | ------------- | ------------------------- | --------- | ------------ |
| **Mercados Financieros** | 59,956        | 49 países, 49 activos     | 2020-2025 | Diaria       |
| **Indicadores Macro**    | 5,280         | 44 países, 12 indicadores | 2015-2024 | Anual        |
| **Datos Coincidentes**   | 162           | 33 países                 | 2020-2024 | Anual        |

### Fuentes de Datos:
- 📈 **Mercados**: Yahoo Finance (índices, forex, commodities)
- 🌍 **Macro**: Banco Mundial API (PIB, inflación, comercio, etc.)

---

## Instalación y Uso

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/LasciaStare/GeoFinance.git
cd GeoFinance
```

### 2️⃣ Crear entorno virtual e instalar dependencias
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

### 3️⃣ Descargar datos

**A. Datos de mercados financieros:**
```bash
python descarga_datos.py
```
- Descarga datos de 60+ activos desde Yahoo Finance
- Calcula métricas (rendimiento, volatilidad, Sharpe ratio)
- Guarda en `data/historico_activos.parquet` y `data/metricas_activos.parquet`
- ⏱️ Tiempo estimado: 5-10 minutos

**B. Datos macroeconómicos:**
```bash
python descarga_macro.py
```
- Descarga 12 indicadores del Banco Mundial
- Cobertura: 44 países, 2015-2024
- Guarda en `data/datos_macro.parquet`
- ⏱️ Tiempo estimado: 2-3 minutos

### 4️⃣ Ejecutar el dashboard
```bash
streamlit run app.py
```

Abre tu navegador en: **http://localhost:8501**

---

## 📁 Estructura del Proyecto

```
GeoFinance/
├── 📄 app.py                           # Página principal del dashboard
├── 📄 descarga_datos.py                # Script para datos de mercados
├── 📄 descarga_macro.py                # Script para datos macro
├── 📄 generar_resultados.py            # Script para análisis completo
├── 📄 requirements.txt                 # Dependencias
├── 📄 GUION_PRESENTACION.md            # Guion completo con storytelling
├── 📄 PUNTOS_CLAVE_POR_PAGINA.md       # Qué decir en cada página
├── 📄 RESUMEN_EJECUTIVO.md             # Resultados visuales ejecutivos
├── 📂 pages/                           # Páginas del dashboard
│   ├── 1_Vista_Global.py           # Mapa interactivo mundial
│   ├── 2_Exploratorio_Macro.py     # Análisis macro con tests estadísticos
│   ├── 3_Analisis_Activos.py       # Series temporales de activos
│   ├── 4_EDA.py                    # EDA completo de datasets
│   ├── 5_Comparacion_Datasets.py   # Comparación estadística rigurosa
│   └── 6_Conclusiones.py           # Marco y hallazgos del proyecto
└── 📂 data/                            # Datos en formato Parquet
    ├── historico_activos.parquet
    ├── metricas_activos.parquet
    └── datos_macro.parquet
```

---

## 🔬 Hallazgos Principales

### 1. Relación entre Mercados y Economía Real

```
CORRELACIÓN DE PEARSON: -0.1023 (prácticamente NULA)
P-VALUE: < 0.001 (estadísticamente MUY SIGNIFICATIVO)
CONCLUSIÓN: Los mercados y el PIB son DIFERENTES
```

### 2. Volatilidad Comparativa

| Métrica            | Mercados | PIB    | Ratio    |
| ------------------ | -------- | ------ | -------- |
| **Media**          | +12.21%  | +1.92% | 6.4x     |
| **Desv. Estándar** | 33.88%   | 4.66%  | **7.3x** |
| **Máximo**         | +349%    | +13.4% | 26x      |

**Conclusión**: Los mercados son **7 veces más volátiles** que la economía real.

### 3. Top Performers (Periodo 2020-2025)

| Ranking | País/Activo | Rendimiento |
| ------- | ----------- | ----------- |
| 🥇       | Argentina   | +3,729%     |
| 🥈       | Turquía     | +775%       |
| 🥉       | Grecia      | +228%       |
| 4       | Israel      | +135%       |
| 5       | España      | +133%       |
| 6       | ORO         | +128%       |

### 4. Crecimiento del PIB por Región

| Región     | Media | Rango       |
| ---------- | ----- | ----------- |
| **Asia** 🚀 | 3.59% | -6% a +10%  |
| América ⚡  | 1.71% | -11% a +13% |
| Europa 🐢   | 1.57% | -11% a +9%  |

---

## Modelo Propuesto

### Arquitectura: Machine Learning Ensemble

```
Random Forest + XGBoost + LSTM
                ↓
   Predicción Multi-Horizonte
```

### Features (45+):
- 🌍 **Macroeconómicas (8)**: PIB, inflación, desempleo, comercio
- 📈 **Mercado (15)**: precio, volatilidad, volumen, correlaciones
- 📊 **Derivadas (15+)**: SMA, RSI, MACD, momentum
- 🎯 **Contexto (7)**: región, tipo de activo, trimestre

### Objetivos:
- ✅ Predicción de tendencias (1, 3, 6 meses)
- ✅ Clasificación de salud económica (Alta/Media/Baja)
- ✅ Sistema de alertas tempranas de crisis
- ✅ Recomendaciones de diversificación óptima

### Accuracy Esperado:
- 1 mes: **65-70%**
- 3 meses: **60-65%**
- 6 meses: **55-60%**

---

## Tecnologías Utilizadas

- **Python 3.10+**
- **Streamlit**: Framework para dashboard interactivo
- **Pandas**: Manipulación de datos
- **Plotly**: Visualizaciones interactivas
- **SciPy**: Tests estadísticos (Shapiro-Wilk, Mann-Whitney, ANOVA)
- **yfinance**: Datos de Yahoo Finance
- **wbdata**: API del Banco Mundial
- **PyArrow**: Almacenamiento eficiente en Parquet

---

## 📚 Documentación Adicional

### Tests Estadísticos Implementados:

| Test               | Uso                        | Interpretación                  |
| ------------------ | -------------------------- | ------------------------------- |
| **Shapiro-Wilk**   | Normalidad                 | p < 0.05 → No normal            |
| **Mann-Whitney U** | Comparación no paramétrica | p < 0.05 → Diferentes           |
| **t-test**         | Comparación paramétrica    | p < 0.05 → Diferentes           |
| **ANOVA**          | Comparación múltiple       | p < 0.05 → Al menos 1 diferente |
| **Kruskal-Wallis** | ANOVA no paramétrico       | p < 0.05 → Al menos 1 diferente |
| **Pearson**        | Correlación lineal         | r ∈ [-1, 1]                     |


---

## Limitaciones

1. **Granularidad temporal**: Macro anual vs mercados diarios
2. **Causalidad**: Correlación no implica causalidad
3. **Variables omitidas**: Faltan tasas de interés, sentimiento
4. **Periodo limitado**: Solo 5 años de solapamiento completo
5. **Sesgo de supervivencia**: Solo mercados actualmente activos

---


<div align="center">

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub ⭐**

Made with ❤️ by Jose | Octubre 2025

</div>