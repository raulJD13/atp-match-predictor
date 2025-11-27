# 🎾 ATP Match Predictor AI

> Una aplicación Full Stack de Inteligencia Artificial que predice ganadores de partidos de tenis ATP basándose en datos históricos, desplegada con arquitectura de microservicios en Docker.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![Docker](https://img.shields.io/badge/Deploy-Docker-blue)

## 🏗️ Arquitectura del Proyecto

El proyecto utiliza una arquitectura de contenedores orquestada:

1.  **Data Engineering:** Procesamiento de datasets históricos ATP (2015-Presente).
2.  **Machine Learning:** Modelo `RandomForestClassifier` entrenado con Scikit-Learn (Accuracy ~60%).
3.  **Backend:** API RESTful construida con **FastAPI** para servir las predicciones.
4.  **Frontend:** Interfaz de usuario interactiva construida con **Streamlit**.
5.  **Infraestructura:** Docker Compose para orquestación de servicios y redes.

## 🚀 Cómo ejecutarlo en local (Docker)

Si tienes Docker instalado, puedes levantar todo el sistema con un solo comando:

```bash
# 1. Clonar el repositorio
git clone [https://github.com/raulJD13/atp-match-predictor.git](https://github.com/raulJD13/atp-match-predictor.git)
cd atp-match-predictor

# 2. Construir y arrancar los contenedores
docker-compose up --build