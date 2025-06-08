# Dashboard interactivo accesible para predicción de confianza ciudadana

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import os

# Cargar el dataset completo con escenarios futuros
file_name = "fcc_sensing_simulacion-segundo intento.csv"
file_path = os.path.join(os.getcwd(), file_name)

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    df = pd.DataFrame({
        'mes': [],
        'sentimiento_positivo': [],
        'sentimiento_negativo': [],
        'volumen_menciones': [],
        'topico_predominante': [],
        'crisis_detectada': [],
        'tiempo_respuesta_horas': [],
        'medio_principal': [],
        'indice_confianza_ciudadana': [],
        'intervenciones_comunicacion': [],
        'menciones_positivas': [],
        'menciones_negativas': []
    })

# Agregar los 3 escenarios futuros nuevamente
scenarios = pd.DataFrame({
    'mes': ['2024-01', '2024-02', '2024-03'],
    'sentimiento_positivo': [60.0, 35.0, 50.0],
    'sentimiento_negativo': [40.0, 65.0, 50.0],
    'volumen_menciones': [15000, 17000, 12000],
    'topico_predominante': ['confianza en la FCC', 'contrataciones públicas', 'caso mediático'],
    'crisis_detectada': ['No', 'Sí', 'No'],
    'tiempo_respuesta_horas': [8.0, 30.0, 12.0],
    'medio_principal': ['Twitter', 'Facebook', 'Foros'],
    'indice_confianza_ciudadana': [64.85, 55.18, 61.28],
    'intervenciones_comunicacion': [2, 0, 1],
    'menciones_positivas': [9000, 5950, 6000],
    'menciones_negativas': [6000, 11050, 6000]
})

df_full = pd.concat([df, scenarios], ignore_index=True)

# Crear la aplicación Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout accesible
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Dashboard de Confianza Ciudadana - FCC", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                figure=px.line(
                    df_full, x="mes", y="indice_confianza_ciudadana",
                    markers=True,
                    color_discrete_sequence=px.colors.sequential.Plasma,
                    title="¿Cómo ha evolucionado la confianza ciudadana en el tiempo?"
                ).update_layout(template="ggplot2", title_x=0.5)
            )
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                figure=px.bar(
                    df_full, x="mes", y=["menciones_positivas", "menciones_negativas"],
                    barmode='group',
                    color_discrete_sequence=px.colors.qualitative.Safe,
                    title="¿Cuáles fueron las menciones positivas y negativas por mes?"
                ).update_layout(template="ggplot2", title_x=0.5)
            )
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                figure=px.scatter(
                    df_full,
                    x="tiempo_respuesta_horas",
                    y="indice_confianza_ciudadana",
                    color="crisis_detectada",
                    size="volumen_menciones",
                    color_discrete_sequence=px.colors.qualitative.Safe,
                    title="¿Cómo influye el tiempo de respuesta y las crisis en la confianza?"
                ).update_layout(template="ggplot2", title_x=0.5)
            )
        ], width=12)
    ])
], fluid=True)

# Para correr localmente:
# if __name__ == '__main__':
#     app.run_server(debug=True)

server = app.server
