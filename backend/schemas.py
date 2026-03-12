from pydantic import BaseModel
from typing import List, Optional

class UserHealthInfo(BaseModel):
    # 1. Basic Information
    age: int
    gender: str
    weight: float
    height: float
    blood_group: Optional[str] = None
    
    # 2. Medical History
    existing_conditions: List[str]
    family_history: List[str]
    previous_surgeries: List[str]
    allergies: List[str]
    
    # 3. Current Symptoms (Inherited from original but expanded)
    symptoms: List[str]
    
    # 4. Lifestyle Factors
    smoking_status: str
    alcohol_consumption: str
    exercise_frequency: str
    sleep_hours: int
    diet_type: str
    
    # 5. Medical Test Results
    blood_pressure_sys: int
    blood_pressure_dia: int
    blood_sugar: int
    cholesterol: int
    heart_rate: int
    oxygen_saturation: int

class RecommendationResponse(BaseModel):
    disease_prediction: str
    risk_score: float
    recommended_treatment: str
    suggested_medicines: List[str]
    explanation: str
    explanation_details: List[str]  # For "Explainable AI" features
