from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

# 1. Inicializar la App
app = FastAPI(title="ATP Match Predictor API", version="1.0")

# 2. Cargar el Modelo al iniciar
# Usamos rutas relativas para que funcione en Docker y en Local
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "modelo_atp_rf_v1.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print(f"✅ Modelo cargado desde: {MODEL_PATH}")
except Exception as e:
    print(f"❌ Error cargando el modelo: {e}")
    model = None

# 3. Definir la estructura de los datos de entrada (Data Validation)
class MatchData(BaseModel):
    diff_rank: int
    diff_pts: int
    surface: str  # "Hard", "Clay", "Grass"

# 4. Crear el Endpoint de Predicción
@app.post("/predict")
def predict_match(data: MatchData):
    if not model:
        raise HTTPException(status_code=500, detail="Modelo no cargado")

    # A. Preprocesamiento (Convertir el string de superficie a columnas One-Hot)
    # Recordamos que el modelo espera: [diff_rank, diff_pts, Surface_Clay, Surface_Grass, Surface_Hard]
    
    surface_clay = 1 if data.surface == "Clay" else 0
    surface_grass = 1 if data.surface == "Grass" else 0
    surface_hard = 1 if data.surface == "Hard" else 0
    
    # Crear el array de entrada (DataFrame para mantener nombres de columnas si es necesario, o array numpy)
    input_data = pd.DataFrame([{
        'diff_rank': data.diff_rank,
        'diff_pts': data.diff_pts,
        'Surface_Clay': surface_clay,
        'Surface_Grass': surface_grass,
        'Surface_Hard': surface_hard
    }])

    # B. Predicción
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1] # Probabilidad de que gane P1 (clase 1)

    # C. Respuesta JSON
    return {
        "winner": "Player 1" if prediction == 1 else "Player 2",
        "probability_player_1": round(float(probability), 2),
        "input_received": data.dict()
    }

@app.get("/")
def read_root():
    return {"message": "ATP Match Predictor API is running! 🎾"}