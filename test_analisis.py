
import pandas as pd

from analisis import (
    calcular_total_encuestas,
    calcular_porcentaje_votos
)

from validacion import validar_datos


def test_total_encuestas():
    df = pd.DataFrame({
        "id": [1, 2, 3]
    })

    assert calcular_total_encuestas(df) == 3


def test_porcentaje_votos():
    df = pd.DataFrame({
        "intencion_voto": [
            "Candidato A",
            "Candidato A",
            "Candidato B"
        ]
    })

    resultados = calcular_porcentaje_votos(df)

    porcentaje_a = resultados.loc[
        resultados["intencion_voto"] == "Candidato A",
        "porcentaje"
    ].iloc[0]

    assert porcentaje_a == 66.67


def test_detectar_edad_invalida():
    df = pd.DataFrame({
        "id": [1, 2],
        "region": ["Metropolitana", "Metropolitana"],
        "edad": [25, 15],
        "genero": ["Femenino", "Masculino"],
        "preferencia": ["A", "B"],
        "intencion_voto": ["Candidato A", "Candidato B"]
    })

    validos, invalidos, errores = validar_datos(df)

    assert len(validos) == 1
    assert len(invalidos) == 1
    assert len(errores) > 0


def test_detectar_id_duplicado():
    df = pd.DataFrame({
        "id": [1, 1],
        "region": ["Metropolitana", "Metropolitana"],
        "edad": [25, 30],
        "genero": ["Femenino", "Masculino"],
        "preferencia": ["A", "B"],
        "intencion_voto": ["Candidato A", "Candidato B"]
    })

    validos, invalidos, errores = validar_datos(df)

    assert len(validos) == 1
    assert len(invalidos) == 1
    assert len(errores) > 0
