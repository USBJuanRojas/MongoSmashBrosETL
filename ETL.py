import pandas as pd
from pymongo import MongoClient

# columnas a usar
cols_to_use = ['p1_id', 'p2_id', 'winner_id', 'p1_score', 'p2_score',
            'best_of', 'tournament_key', 'location_names', 'game']

# Leer el archivo con columnas específicas
df = pd.read_csv("sets.csv",
                    usecols=cols_to_use,
                    dtype={'p1_id': str, 'p2_id': str, 'winner_id': str},
                    low_memory=False)

# Eliminar filas con datos faltantes
df.dropna(subset=['p1_id', 'p2_id', 'winner_id', 'tournament_key'], inplace=True)

# Convertir scores a enteros si hay problemas de tipo
df['p1_score'] = pd.to_numeric(df['p1_score'], errors='coerce')
df['p2_score'] = pd.to_numeric(df['p2_score'], errors='coerce')

# Limpiar cualquier fila donde falten los scores
df.dropna(subset=['p1_score', 'p2_score'], inplace=True)

# Asegurar que los scores sean enteros
df['p1_score'] = df['p1_score'].astype(int)
df['p2_score'] = df['p2_score'].astype(int)

# Reiniciar índice después de limpiar
df.reset_index(drop=True, inplace=True)

print("Datos cargados y limpiados:")
print(df.info())
print(df.head())

# Guardar el dataset limpio en un nuevo archivo
df.to_csv("sets_limpio.csv", index=False)

print("\n\nDataset limpio guardado como 'sets_limpio.csv'")



#Apartado de MongoDB
URI = "mongodb+srv://jrojasn:jrojasnusbjajaxd@cluster0.h9fcn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

dfc = pd.read_csv("sets_limpio.csv")

try:
    connection = MongoClient(URI)
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print("Error al conectarse a la base de datos:", e)

db = connection["Smash"]
collection = db["Sets"]

dfAjuste = dfc.head(100000)  # Ajuste de tamaño
data_dict = dfAjuste.to_dict("records")

collection.insert_many(data_dict)
print("Datos insertados en MongoDB")




