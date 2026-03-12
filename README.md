# Personalized Medicine Recommendation AI

This project is an AI-driven healthcare recommendation system that predicts health risks based on patient symptoms, medical history, and lifestyle factors.

## Project Structure
- `backend/`: FastAPI application that serves the AI model.
- `frontend/`: Interactive vanilla HTML/CSS/JS frontend (Glassmorphic design).
- `models/`: Contains the trained `health_risk_model.joblib`.
- `notebooks/`: Scripts for data simulation and model training.

## Quick Start

### 1. Prerequisites
- Python 3.8+
- Installed dependencies:
  ```bash
  pip install fastapi uvicorn pandas numpy scikit-learn joblib pydantic
  ```

### 2. Run the Backend API
Navigate to the project root and run:
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### 3. Open the Frontend
Open `frontend/index.html` in any modern web browser.

## How it Works
The system uses a **Random Forest Classifier** to evaluate patient risk profile. The frontend communicates with the FastAPI backend to provide real-time suggestions and risk probabilities.

---
**Disclaimer**: This is a demonstration project using synthetic data. Always consult a medical professional for actual healthcare advice.
