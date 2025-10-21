import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os # Necesario para manejar rutas de archivos

# ============================================================================
# FUNCIÓN DE CARGA DE DATOS (ligeramente adaptada para ser independiente)
# ============================================================================
# Eliminamos @st.cache_data y la lógica de Streamlit (progress_bar, status_text, st.warning)
def cargar_y_procesar_datos_para_descarga():
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
        # Activos comentados en el original se mantienen comentados
        # 'Rusia': {'ticker': '^IMOEX', 'iso3': 'RUS', 'tipo': 'indice'},
        'Arabia Saudita': {'ticker': '^TASI.SR', 'iso3': 'SAU', 'tipo': 'indice'},
        'Sudáfrica': {'ticker': '^J203.JO', 'iso3': 'ZAF', 'tipo': 'indice'},
        'Corea del Sur': {'ticker': '^KS11', 'iso3': 'KOR', 'tipo': 'indice'},
        'Turquía': {'ticker': 'XU100.IS', 'iso3': 'TUR', 'tipo': 'indice'},
        'Reino Unido': {'ticker': '^FTSE', 'iso3': 'GBR', 'tipo': 'indice'},
        'Estados Unidos': {'ticker': '^GSPC', 'iso3': 'USA', 'tipo': 'indice'},
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

    total_paises = len(paises_info)

    # Iterar sobre cada país para descargar y procesar datos
    for idx, (pais, info) in enumerate(paises_info.items()):
        
        try:
            # Descargar datos históricos desde Yahoo Finance
            ticker = yf.Ticker(info['ticker'])
            datos = ticker.history(start=fecha_inicio, end=fecha_fin)

            if len(datos) > 0 and 'Close' in datos.columns:
                # ... (resto del procesamiento idéntico) ...
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

                # Calcular métricas (omitiendo detalle por brevedad, es el mismo código)
                precio_actual = datos['Precio'].iloc[-1]
                
                # 1. Rendimiento del último mes (%)
                rendimiento_mes = ((precio_actual - datos['Precio'].iloc[-21]) / datos['Precio'].iloc[-21]) * 100 if len(datos) >= 21 else np.nan
                
                # 2. Rendimiento del último año (%)
                rendimiento_año = ((precio_actual - datos['Precio'].iloc[-252]) / datos['Precio'].iloc[-252]) * 100 if len(datos) >= 252 else np.nan
                
                # 3. Volatilidad anualizada
                rendimientos_diarios = datos['Precio'].pct_change().dropna()
                volatilidad_anualizada = rendimientos_diarios.std() * np.sqrt(252) * 100 if len(rendimientos_diarios) > 0 else np.nan
                
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
            # Usamos print en lugar de st.warning
            print(f"ATENCIÓN: No se pudieron cargar datos de {pais}: {str(e)[:100]}")

    # Crear DataFrames finales
    df_metricas = pd.DataFrame(metricas_paises)
    df_historico = pd.concat(datos_historicos, ignore_index=True) if datos_historicos else pd.DataFrame()

    # Asegurar que la columna Fecha sea datetime sin zona horaria
    if not df_historico.empty and 'Fecha' in df_historico.columns:
        df_historico['Fecha'] = pd.to_datetime(df_historico['Fecha'], utc=True)
        if df_historico['Fecha'].dt.tz is not None:
            df_historico['Fecha'] = df_historico['Fecha'].dt.tz_localize(None)

    # El tercer valor retornado (paises_info) ya no es necesario para el guardado.
    return df_metricas, df_historico


# ============================================================================
# BLOQUE PRINCIPAL PARA DESCARGAR Y GUARDAR
# ============================================================================

if __name__ == "__main__":
    # 1. Crear el directorio de datos si no existe
    DATA_DIR = 'data'
    os.makedirs(DATA_DIR, exist_ok=True)

    # Rutas de los archivos Parquet
    PATH_METRICAS = os.path.join(DATA_DIR, 'metricas_activos.parquet')
    PATH_HISTORICO = os.path.join(DATA_DIR, 'historico_activos.parquet')

    print("\n--- INICIANDO DESCARGA DE DATOS ---")
    df_metricas, df_historico = cargar_y_procesar_datos_para_descarga()

    print("\n--- FINALIZADA LA DESCARGA ---")

    # 2. Guardar DataFrames en formato Parquet
    if not df_metricas.empty:
        df_metricas.to_parquet(PATH_METRICAS, index=False)
        print(f"✅ Métricas guardadas exitosamente en: {PATH_METRICAS}")
    else:
        print("⚠️ Advertencia: El DataFrame de Métricas está vacío. No se guardó el archivo.")

    if not df_historico.empty:
        # Nota importante: Las fechas sin zona horaria son ideales para Parquet
        df_historico.to_parquet(PATH_HISTORICO, index=False)
        print(f"✅ Histórico de precios guardado exitosamente en: {PATH_HISTORICO}")
    else:
        print("⚠️ Advertencia: El DataFrame de Históricos está vacío. No se guardó el archivo.")

    print("\nProceso de descarga y guardado completado.")