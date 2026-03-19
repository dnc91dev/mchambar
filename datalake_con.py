import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd # Para convertir a DataFrame
import datetime # Import the datetime module

if not firebase_admin._apps:
    # Reemplaza 'ruta/a/tu/' con la ruta real dentro de tu Google Drive
    cred = credentials.Certificate("/home/adminsdk.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 2. Leer datos de la colección 'sensor_data_raw'
docs = db.collection('sensor_data_raw').stream()

data_list = []
for doc in docs:
    data_dict = doc.to_dict()
    # Asegúrate de convertir el Timestamp de Firestore a un formato que Pandas entienda
    if 'timestamp' in data_dict and isinstance(data_dict['timestamp'], datetime.datetime): # Check against datetime.datetime
        data_dict['timestamp'] = data_dict['timestamp'].isoformat() # Convertir a string ISO o a datetime de Python
    data_list.append(data_dict)

df_sensores = pd.DataFrame(data_list)

# Opcional: convertir el campo timestamp a formato datetime de Pandas
if 'timestamp' in df_sensores.columns:
    df_sensores['timestamp'] = pd.to_datetime(df_sensores['timestamp'])

# 3. Ordenar los datos (tu item #2)
df_sensores = df_sensores.sort_values("timestamp")

print(df_sensores.head())
