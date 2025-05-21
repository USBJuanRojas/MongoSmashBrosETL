import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
from pymongo import MongoClient

# Conexión a MongoDB
URI = "mongodb+srv://jrojasn:jrojasnusbjajaxd@cluster0.h9fcn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
try:
    client = MongoClient(URI)
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print("Error al conectarse a la base de datos:", e)
    exit()

db = client["Smash"]
collection = db["Sets"]

data = list(collection.find().limit(100000))

# Convertir la lista de documentos en un DataFrame
df = pd.DataFrame(data)

if '_id' in df.columns:
    df.drop('_id', axis=1, inplace=True)

# Asegurarse de que los scores sean numéricos
df['p1_score'] = pd.to_numeric(df['p1_score'], errors='coerce')
df['p2_score'] = pd.to_numeric(df['p2_score'], errors='coerce')

# Crear columna para la diferencia absoluta de score
df['score_diff'] = abs(df['p1_score'] - df['p2_score'])

# Gráfico Rendimiento de Jugadores

top_winners = df['winner_id'].value_counts().head(10).reset_index()
top_winners.columns = ['winner_id', 'sets_ganados']

fig_rendimiento = px.bar(top_winners,
                         x='winner_id',
                         y='sets_ganados',
                         title='Top 10 Jugadores con más sets ganados',
                         labels={'winner_id': 'Jugador', 'sets_ganados': 'Sets Ganados'})


app = Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard - Super Smash Bros Analysis", style={'textAlign': 'center'}),

    html.Div([
        dcc.Graph(figure=fig_rendimiento)
    ], style={'width': '100%', 'padding': '20px 0'}),
])

if __name__ == "__main__":
    app.run_server(debug=True)

