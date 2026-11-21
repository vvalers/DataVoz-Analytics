
import pandas as pd

def calcular_total_encuestas(df):
    return len(df)

def calcular_porcentaje_votos(df):
    if df.empty:
        return pd.DataFrame(
            columns=["intencion_voto", "cantidad", "porcentaje"]
        )

    resultados = (
        df["intencion_voto"]
        .value_counts()
        .reset_index()
    )

    resultados.columns = ["intencion_voto", "cantidad"]

    resultados["porcentaje"] = (
        resultados["cantidad"] / len(df) * 100
    ).round(2)

    return resultados

def encuestas_por_region(df):
    return df["region"].value_counts().reset_index()

def encuestas_por_edad(df):
    df = df.copy()

    df["grupo_edad"] = pd.cut(
        df["edad"],
        bins=[17, 29, 39, 49, 59, 100],
        labels=[
            "18-29",
            "30-39",
            "40-49",
            "50-59",
            "60+"
        ]
    )

    return df["grupo_edad"].value_counts().sort_index().reset_index()
