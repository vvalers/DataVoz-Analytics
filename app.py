
import streamlit as st
import pandas as pd
import plotly.express as px

from validacion import validar_datos
from analisis import (
    calcular_total_encuestas,
    calcular_porcentaje_votos,
    encuestas_por_region,
    encuestas_por_edad
)

st.set_page_config(
    page_title="DataVoz Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 DataVoz Analytics")
st.write("Sistema de análisis y validación de encuestas ciudadanas")

st.sidebar.header("Carga de datos")

archivo = st.sidebar.file_uploader(
    "Sube tu archivo CSV o Excel",
    type=["csv", "xlsx"]
)

# Cargar archivo
if archivo is not None:
    try:
        if archivo.name.endswith(".csv"):
            df = pd.read_csv(archivo)
        else:
            df = pd.read_excel(archivo)

    except Exception as e:
        st.error(f"No se pudo leer el archivo: {e}")
        st.stop()

else:
    df = pd.read_csv("data/encuestas.csv")

# Validación
datos_validos, datos_invalidos, errores = validar_datos(df)

st.subheader("Control de calidad de datos")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total de encuestas",
    calcular_total_encuestas(df)
)

col2.metric(
    "Encuestas válidas",
    len(datos_validos)
)

col3.metric(
    "Encuestas con observaciones",
    len(datos_invalidos)
)

# Mostrar alertas
if errores:
    for error in errores:
        st.warning(error)
else:
    st.success("Los datos fueron revisados correctamente.")

# Si no existen datos válidos, no mostrar análisis
if datos_validos.empty:
    st.error("No existen datos válidos para realizar el análisis.")
    st.stop()

# Filtro por región
st.sidebar.subheader("Filtros")

regiones = ["Todas"] + sorted(
    datos_validos["region"].unique().tolist()
)

region_seleccionada = st.sidebar.selectbox(
    "Seleccionar región",
    regiones
)

if region_seleccionada == "Todas":
    df_filtrado = datos_validos.copy()
else:
    df_filtrado = datos_validos[
        datos_validos["region"] == region_seleccionada
    ].copy()

# Indicadores
st.subheader("Indicadores principales")

k1, k2 = st.columns(2)

k1.metric(
    "Encuestas analizadas",
    len(df_filtrado)
)

k2.metric(
    "Candidatos registrados",
    df_filtrado["intencion_voto"].nunique()
)

# Gráfico de intención de voto
st.subheader("Distribución de intención de voto")

votos = calcular_porcentaje_votos(df_filtrado)

if not votos.empty:
    figura_votos = px.bar(
        votos,
        x="intencion_voto",
        y="porcentaje",
        color="intencion_voto",
        text="porcentaje",
        labels={
            "intencion_voto": "Candidato",
            "porcentaje": "Porcentaje"
        }
    )

    figura_votos.update_layout(
        yaxis_title="Porcentaje (%)",
        xaxis_title="Candidato",
        showlegend=False
    )

    st.plotly_chart(
        figura_votos,
        use_container_width=True
    )

# Gráfico por región
st.subheader("Distribución por región")

region_df = df_filtrado["region"].value_counts().reset_index()

region_df.columns = ["region", "cantidad"]

fig_region = px.pie(
    region_df,
    names="region",
    values="cantidad",
    hole=0.4
)

st.plotly_chart(
    fig_region,
    use_container_width=True
)

# Gráfico por edad
st.subheader("Distribución por grupo de edad")

edad_df = encuestas_por_edad(df_filtrado)

edad_df.columns = ["grupo_edad", "cantidad"]

fig_edad = px.bar(
    edad_df,
    x="grupo_edad",
    y="cantidad",
    text="cantidad",
    labels={
        "grupo_edad": "Grupo etario",
        "cantidad": "Cantidad de encuestas"
    }
)

st.plotly_chart(
    fig_edad,
    use_container_width=True
)

# Tabla de datos válidos
st.subheader("Datos válidos")

st.dataframe(
    df_filtrado,
    use_container_width=True
)

# Tabla de datos inválidos
st.subheader("Datos que requieren revisión")

if datos_invalidos.empty:
    st.success("No se encontraron registros inválidos.")
else:
    st.dataframe(
        datos_invalidos,
        use_container_width=True
    )

# Descarga de datos
csv_descarga = df_filtrado.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Descargar datos analizados",
    data=csv_descarga,
    file_name="encuestas_analizadas.csv",
    mime="text/csv"
)

st.caption(
    "DataVoz Analytics | Prototipo académico con datos ficticios"
)
