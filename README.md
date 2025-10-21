# GeoFinance - Dashboard de Análisis Económico Global 🌍

Dashboard interactivo para análisis de mercados financieros e indicadores macroeconómicos de 45+ países.

## 🚀 Características

- **Mapa Interactivo**: Visualización global del rendimiento de índices bursátiles
- **Análisis de Mercados**: Gráficos detallados de índices, commodities y forex
- **Análisis Macroeconómico**: Correlación entre indicadores del Banco Mundial y mercados
- **Tests Estadísticos**: Pruebas de significancia (Pearson, Spearman)
- **Datos en Tiempo Real**: Integración con Yahoo Finance
- **Datos Históricos**: Hasta 20 años de datos macroeconómicos

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd GeoFinance
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

## 📊 Uso

### Paso 1: Descargar datos de mercados
Primero, descarga los datos de los índices bursátiles:

```bash
python descarga_datos.py
```

Este script:
- Descarga datos de 45+ países desde Yahoo Finance
- Incluye índices, commodities y forex
- Calcula métricas (rendimiento, volatilidad)
- Guarda en `data/metricas_activos.parquet` y `data/historico_activos.parquet`

**Tiempo estimado**: 5-10 minutos

### Paso 2: Descargar datos macroeconómicos
Luego, descarga los indicadores del Banco Mundial:

```bash
python descarga_macro.py
```

Este script:
- Descarga 13 indicadores macroeconómicos clave
- Datos anuales de 2004-2024
- 45 países con cobertura completa
- Guarda en `data/datos_macro.parquet` y `data/datos_macro_pivote.parquet`

**Tiempo estimado**: 3-5 minutos

### Paso 3: Ejecutar el dashboard
Finalmente, lanza el dashboard de Streamlit:

```bash
streamlit run app.py
```

Abre tu navegador en `http://localhost:8501`

## 🗂️ Estructura del Proyecto

```
GeoFinance/
├── app.py                      # Página principal
├── descarga_datos.py          # Script de descarga de mercados
├── descarga_macro.py          # Script de descarga macroeconómica
├── requirements.txt           # Dependencias
├── Dockerfile                # Configuración Docker
├── data/                     # Datos descargados (generados)
│   ├── metricas_activos.parquet
│   ├── historico_activos.parquet
│   ├── datos_macro.parquet
│   └── datos_macro_pivote.parquet
└── pages/                    # Páginas del dashboard
    ├── mapa.py              # Mapa interactivo global
    ├── analisis.py          # Análisis detallado de mercados
    └── macro.py             # Análisis macroeconómico
```

## 📈 Páginas del Dashboard

### 1. 🏠 Inicio (app.py)
Página de bienvenida con información general del proyecto.

### 2. 🗺️ Mapa
- Mapa coroplético interactivo
- 45+ países con índices bursátiles
- Métricas configurables (rendimiento, volatilidad)
- Periodos personalizables
- Rankings y tablas comparativas

### 3. 📊 Análisis
- Gráficos de series temporales
- Análisis técnico
- Comparación de activos
- Métricas de riesgo-retorno

### 4. 📈 Macro
- Correlaciones entre indicadores macro y mercados
- Tests estadísticos (Pearson, Spearman)
- Análisis de significancia
- Comparación multi-país
- Interpretación automática de resultados

## 🔬 Indicadores Macroeconómicos Incluidos

1. **Crecimiento Económico**
   - Crecimiento PIB (%)
   - Crecimiento PIB per cápita (%)

2. **Comercio e Inversión**
   - Comercio (% del PIB)
   - Inversión Extranjera Directa (% del PIB)

3. **Inflación**
   - Inflación al consumidor (%)

4. **Sector Financiero**
   - Capitalización de mercado (% del PIB)
   - Crédito doméstico al sector privado (% del PIB)

5. **Empleo**
   - Tasa de desempleo (%)

6. **Deuda**
   - Deuda pública (% del PIB)

7. **Otros**
   - Población total
   - PIB per cápita
   - Inversión bruta (% del PIB)
   - Balance fiscal (% del PIB)

## 🌍 Cobertura Geográfica

### G20
Argentina, Australia, Brasil, Canadá, China, Francia, Alemania, India, Indonesia, Italia, Japón, México, Rusia, Arabia Saudita, Sudáfrica, Corea del Sur, Turquía, Reino Unido, Estados Unidos

### Europa Adicional
España, Países Bajos, Suiza, Suecia, Noruega, Dinamarca, Polonia, Grecia, Portugal, Bélgica, Austria

### América Latina
Colombia, Chile, Perú

### Medio Oriente y África
Israel, Egipto, Nigeria

### Asia-Pacífico
Taiwán, Tailandia, Malasia, Singapur, Hong Kong, Nueva Zelanda, Filipinas, Vietnam, Pakistán

## 🛠️ Tecnologías Utilizadas

- **Frontend**: Streamlit
- **Visualización**: Plotly, Matplotlib, Seaborn
- **Datos**: yfinance (mercados), wbdata (macro)
- **Análisis**: pandas, numpy, scipy, scikit-learn
- **Almacenamiento**: Parquet (PyArrow)

## 📊 Tests Estadísticos

El análisis macroeconómico incluye:

1. **Correlación de Pearson**: Mide relaciones lineales
2. **Correlación de Spearman**: Mide relaciones monotónicas
3. **Tests de Hipótesis**: H₀: ρ = 0, α = 0.05
4. **Interpretación**: Cohen (1988)
   - Débil: |r| < 0.3
   - Moderada: 0.3 ≤ |r| < 0.5
   - Fuerte: |r| ≥ 0.5

## 🔄 Actualización de Datos

Para actualizar los datos, simplemente vuelve a ejecutar los scripts de descarga:

```bash
# Actualizar datos de mercados
python descarga_datos.py

# Actualizar datos macroeconómicos
python descarga_macro.py
```

**Recomendación**: Actualiza los datos:
- **Mercados**: Diariamente o semanalmente
- **Macro**: Mensualmente (los datos del Banco Mundial se actualizan menos frecuentemente)

## 🐛 Solución de Problemas

### Error: "No se encontraron los archivos de datos"
**Solución**: Ejecuta `python descarga_datos.py` y/o `python descarga_macro.py`

### Error: "No se pudieron cargar datos de [País]"
**Causa**: Yahoo Finance puede tener problemas temporales o el ticker cambió
**Solución**: Los datos de otros países se cargarán correctamente

### Error en la descarga del Banco Mundial
**Causa**: Problemas de conexión o API temporalmente no disponible
**Solución**: Espera unos minutos y vuelve a intentar

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👥 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:
1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📧 Contacto

Para preguntas o sugerencias, abre un issue en GitHub.

---

**Desarrollado con ❤️ usando Streamlit y Plotly**
