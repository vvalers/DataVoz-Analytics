

import pandas as pd

COLUMNAS_REQUERIDAS = [
    "id",
    "region",
    "edad",
    "genero",
    "preferencia",
    "intencion_voto"
]

REGIONES_VALIDAS = [
    "Metropolitana",
    "Valparaiso",
    "Biobio",
    "Araucania"
]

def validar_datos(df):

    errores = []
    df = df.copy()

    # Revisar columnas obligatorias
    faltantes = [
        columna for columna in COLUMNAS_REQUERIDAS
        if columna not in df.columns
    ]

    if faltantes:
        errores.append(
            "Faltan columnas obligatorias: "
            + ", ".join(faltantes)
        )

        return pd.DataFrame(), df, errores

    # Limpiar espacios de texto
    columnas_texto = [
        "region",
        "genero",
        "preferencia",
        "intencion_voto"
    ]

    for columna in columnas_texto:
        df[columna] = (
            df[columna]
            .astype("string")
            .str.strip()
        )

    # Convertir edad a número
    df["edad"] = pd.to_numeric(
        df["edad"],
        errors="coerce"
    )

    # Convertir ID a texto y limpiar espacios
    df["id"] = df["id"].astype("string").str.strip()

    # Detectar valores vacíos
    campos_vacios = (
        df[COLUMNAS_REQUERIDAS]
        .isna()
        .any(axis=1)
    )

    for columna in COLUMNAS_REQUERIDAS:
        campos_vacios |= (
            df[columna]
            .astype("string")
            .str.strip()
            .eq("")
            .fillna(False)
        )

    # Detectar duplicados de ID
    duplicados = df.duplicated(
        subset=["id"],
        keep="first"
    )

    # Detectar edades incorrectas
    edades_invalidas = (
        df["edad"].isna() |
        (df["edad"] < 18) |
        (df["edad"] > 100)
    )

    # Detectar regiones no válidas
    regiones_invalidas = ~df["region"].isin(
        REGIONES_VALIDAS
    )

    # Combinar todas las reglas
    filas_invalidas = (
        campos_vacios |
        duplicados |
        edades_invalidas |
        regiones_invalidas
    )

    # Registrar errores
    if campos_vacios.any():
        errores.append(
            f"{campos_vacios.sum()} registros incompletos."
        )

    if duplicados.any():
        errores.append(
            f"{duplicados.sum()} registros duplicados."
        )

    if edades_invalidas.any():
        errores.append(
            f"{edades_invalidas.sum()} edades inválidas."
        )

    if regiones_invalidas.any():
        errores.append(
            f"{regiones_invalidas.sum()} regiones inválidas."
        )

    # Separar datos
    datos_validos = df.loc[
        ~filas_invalidas
    ].copy()

    datos_invalidos = df.loc[
        filas_invalidas
    ].copy()

    return datos_validos, datos_invalidos, errores

