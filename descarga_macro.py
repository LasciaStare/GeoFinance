"""
Script para descargar datos macroeconómicos del Banco Mundial usando wbdata.
Los datos se guardan en formato Parquet para uso en el dashboard.
"""

import wbdata
import pandas as pd
from datetime import datetime
import os

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Códigos ISO de países que queremos analizar (solo países con índices bursátiles)
PAISES_ISO = [
    'ARG', 'AUS', 'BRA', 'CAN', 'CHN', 'FRA', 'DEU', 'IND', 'IDN', 'ITA',
    'JPN', 'MEX', 'RUS', 'SAU', 'ZAF', 'KOR', 'TUR', 'GBR', 'USA', 'COL',
    'ESP', 'NLD', 'CHE', 'SWE', 'NOR', 'DNK', 'POL', 'GRC', 'PRT', 'BEL',
    'AUT', 'CHL', 'PER', 'ISR', 'EGY', 'NGA', 'TWN', 'THA', 'MYS', 'SGP',
    'HKG', 'NZL', 'PHL', 'VNM', 'PAK'
]

# Indicadores macroeconómicos clave del Banco Mundial
# Formato: {'código_indicador': 'nombre_descriptivo'}
INDICADORES = {
    # Crecimiento Económico
    'NY.GDP.MKTP.KD.ZG': 'Crecimiento_PIB',  # GDP growth (annual %)
    'NY.GDP.PCAP.KD.ZG': 'Crecimiento_PIB_Per_Capita',  # GDP per capita growth (annual %)
    
    # Comercio e Inversión
    'NE.TRD.GNFS.ZS': 'Comercio_Porcentaje_PIB',  # Trade (% of GDP)
    'BX.KLT.DINV.WD.GD.ZS': 'Inversion_Extranjera_Directa',  # Foreign direct investment, net inflows (% of GDP)
    
    # Inflación y Precios
    'FP.CPI.TOTL.ZG': 'Inflacion',  # Inflation, consumer prices (annual %)
    
    # Sector Financiero
    'CM.MKT.LCAP.GD.ZS': 'Capitalizacion_Mercado',  # Market capitalization of listed domestic companies (% of GDP)
    'FS.AST.DOMS.GD.ZS': 'Activos_Domesticos',  # Domestic credit to private sector (% of GDP)
    
    # Empleo
    'SL.UEM.TOTL.ZS': 'Desempleo',  # Unemployment, total (% of total labor force)
    
    # Deuda
    'GC.DOD.TOTL.GD.ZS': 'Deuda_Publica',  # Central government debt, total (% of GDP)
    
    # Desarrollo Humano
    'SP.POP.TOTL': 'Poblacion_Total',  # Population, total
    'NY.GDP.PCAP.KD': 'PIB_Per_Capita',  # GDP per capita (constant 2015 US$)
    
    # Estabilidad Macroeconómica
    'NE.GDI.TOTL.ZS': 'Inversion_Bruta',  # Gross capital formation (% of GDP)
    'GC.BAL.CASH.GD.ZS': 'Balance_Fiscal',  # Cash surplus/deficit (% of GDP)
}

# Periodo de análisis
ANO_INICIO = 2015
ANO_FIN = 2025

# Directorio de salida
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)
PATH_MACRO = os.path.join(DATA_DIR, 'datos_macro.parquet')


# ============================================================================
# FUNCIÓN PRINCIPAL DE DESCARGA
# ============================================================================

def descargar_datos_macro():
    """
    Descarga datos macroeconómicos del Banco Mundial para los países seleccionados.
    """
    
    print("\n" + "="*80)
    print("DESCARGA DE DATOS MACROECONÓMICOS DEL BANCO MUNDIAL")
    print("="*80)
    print(f"\n📊 Descargando {len(INDICADORES)} indicadores para {len(PAISES_ISO)} países")
    print(f"📅 Periodo: {ANO_INICIO} - {ANO_FIN}\n")
    
    # Contenedor para todos los datos
    datos_completos = []
    
    # Iterar sobre cada indicador
    for idx, (codigo_indicador, nombre_indicador) in enumerate(INDICADORES.items(), 1):
        print(f"[{idx}/{len(INDICADORES)}] Descargando: {nombre_indicador}...")
        
        try:
            # Descargar datos del Banco Mundial
            # wbdata.get_dataframe retorna un DataFrame con MultiIndex (país, fecha)
            datos = wbdata.get_dataframe(
                {codigo_indicador: nombre_indicador},
                country=PAISES_ISO,
                date=(f"{ANO_INICIO}-01-01", f"{ANO_FIN}-12-31"),
                parse_dates=True,
                keep_levels=False
            )
            
            if datos is not None and not datos.empty:
                # Resetear índice para obtener columnas country y date
                datos = datos.reset_index()
                
                # Renombrar columnas
                if 'country' in datos.columns:
                    datos.rename(columns={'country': 'ISO3'}, inplace=True)
                if 'date' in datos.columns:
                    datos.rename(columns={'date': 'Ano'}, inplace=True)
                    # Extraer solo el año de la fecha
                    datos['Ano'] = pd.to_datetime(datos['Ano']).dt.year

                # Filtrar por rango de años deseado
                datos = datos[
                    (datos['Ano'] >= ANO_INICIO) &
                    (datos['Ano'] <= ANO_FIN)
                ]

                if datos.empty:
                    print("   ⚠️  Sin datos dentro del rango de años solicitado")
                    continue
                
                # Agregar información del indicador
                datos['Indicador'] = nombre_indicador
                datos['Codigo_Indicador'] = codigo_indicador
                
                # Renombrar la columna de valor
                datos.rename(columns={nombre_indicador: 'Valor'}, inplace=True)
                
                # Guardar datos
                datos_completos.append(datos[['ISO3', 'Ano', 'Indicador', 'Codigo_Indicador', 'Valor']])
                
                print(f"   ✅ Descargado: {len(datos)} registros")
            else:
                print(f"   ⚠️  No se encontraron datos para {nombre_indicador}")
                
        except Exception as e:
            print(f"   ❌ Error descargando {nombre_indicador}: {str(e)[:100]}")
    
    # Combinar todos los datos
    if datos_completos:
        df_macro = pd.concat(datos_completos, ignore_index=True)
        
        print(f"\n{'='*80}")
        print(f"✅ DESCARGA COMPLETADA")
        print(f"{'='*80}")
        print(f"Total de registros: {len(df_macro):,}")
        print(f"Países únicos: {df_macro['ISO3'].nunique()}")
        print(f"Indicadores únicos: {df_macro['Indicador'].nunique()}")
        print(f"Años: {df_macro['Ano'].min()} - {df_macro['Ano'].max()}")
        
        # Estadísticas de completitud
        print(f"\n📈 Estadísticas de completitud:")
        completitud = df_macro.groupby('Indicador')['Valor'].apply(
            lambda x: (x.notna().sum() / len(x)) * 100
        ).sort_values(ascending=False)
        
        for indicador, porcentaje in completitud.items():
            print(f"   {indicador}: {porcentaje:.1f}% completo")
        
        # Guardar en Parquet
        df_macro.to_parquet(PATH_MACRO, index=False)
        print(f"\n💾 Datos guardados exitosamente en: {PATH_MACRO}")
        
        return df_macro
    else:
        print("\n❌ No se pudieron descargar datos")
        return pd.DataFrame()


def crear_pivote_anual(df_macro):
    """
    Crea una tabla pivote con un indicador por columna (formato ancho).
    Útil para análisis y correlaciones.
    """
    if df_macro.empty:
        return pd.DataFrame()
    
    print("\n" + "="*80)
    print("CREANDO TABLA PIVOTE")
    print("="*80)
    
    # Crear pivote: filas = (País, Año), columnas = Indicadores
    df_pivote = df_macro.pivot_table(
        index=['ISO3', 'Ano'],
        columns='Indicador',
        values='Valor',
        aggfunc='first'  # En caso de duplicados, tomar el primero
    ).reset_index()
    
    print(f"✅ Tabla pivote creada: {df_pivote.shape[0]} filas x {df_pivote.shape[1]} columnas")
    
    # Guardar pivote
    PATH_PIVOTE = os.path.join(DATA_DIR, 'datos_macro_pivote.parquet')
    df_pivote.to_parquet(PATH_PIVOTE, index=False)
    print(f"💾 Pivote guardado en: {PATH_PIVOTE}")
    
    return df_pivote


# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("\n🌍 Iniciando descarga de datos macroeconómicos del Banco Mundial...\n")
    
    # Descargar datos
    df_macro = descargar_datos_macro()
    
    # Crear tabla pivote
    if not df_macro.empty:
        df_pivote = crear_pivote_anual(df_macro)
        
        print("\n" + "="*80)
        print("🎉 PROCESO COMPLETADO EXITOSAMENTE")
        print("="*80)
        print("\nArchivos generados:")
        print(f"  1. {PATH_MACRO} - Datos en formato largo")
        print(f"  2. {os.path.join(DATA_DIR, 'datos_macro_pivote.parquet')} - Datos en formato ancho")
        print("\n💡 Ahora puedes usar estos datos en el dashboard ejecutando: streamlit run app.py")
    else:
        print("\n⚠️  No se generaron archivos debido a errores en la descarga")
    
    print("\n" + "="*80 + "\n")
