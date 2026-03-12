import joblib
import os
import numpy as np
import difflib

# Load paths
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/health_risk_model.joblib")
FEATURES_PATH = os.path.join(os.path.dirname(__file__), "../models/feature_names.joblib")

# Real Drug Data Paths
DRUG_MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/drug_recommender.joblib")
LE_DRUG_PATH = os.path.join(os.path.dirname(__file__), "../models/le_drug.joblib")
LE_CONDITION_PATH = os.path.join(os.path.dirname(__file__), "../models/le_condition.joblib")
DRUG_MAP_PATH = os.path.join(os.path.dirname(__file__), "../models/condition_drug_map.joblib")

def get_recommendation(health_info):
    # 1. Automatic BMI Calculation
    height_m = health_info.height / 100
    bmi = health_info.weight / (height_m ** 2)
    
    # 2. Map Inputs to Model Features
    gender_val = 1 if health_info.gender.lower() == "female" else 0
    symptoms = [s.lower() for s in health_info.symptoms]
    conditions_input = [c.lower() for c in health_info.existing_conditions]
    history = conditions_input + [f.lower() for f in health_info.family_history]
    
    # Feature extraction logic matching train_model.py
    features_dict = {
        'age': health_info.age,
        'gender': gender_val,
        'bmi': bmi,
        'has_diabetes_history': 1 if "diabetes" in history else 0,
        'has_heart_history': 1 if "heart" in history or "hypertension" in history else 0,
        'is_smoker': 1 if health_info.smoking_status.lower() == "yes" else 0,
        'heavy_drinker': 1 if health_info.alcohol_consumption.lower() in ["frequent", "heavy"] else 0,
        'exercise_level': 1 if health_info.exercise_frequency.lower() == "moderate" else (2 if health_info.exercise_frequency.lower() == "active" else 0),
        'sleep_hours': health_info.sleep_hours,
        'blood_sugar': health_info.blood_sugar,
        'cholesterol': health_info.cholesterol,
        'bp_sys': health_info.blood_pressure_sys,
        'oxygen_sat': health_info.oxygen_saturation,
        'chest_pain_symptom': 1 if "chest pain" in symptoms else 0,
        'thirst_symptom': 1 if "excessive thirst" in symptoms or "frequent urination" in symptoms else 0
    }
    
    explanation_details = []
    if features_dict['blood_sugar'] > 140: explanation_details.append("High blood sugar levels detected.")
    if features_dict['bmi'] > 30: explanation_details.append("BMI indicates obesity segment.")
    if features_dict['bp_sys'] > 140: explanation_details.append("Systolic blood pressure is elevated.")
    if features_dict['is_smoker']: explanation_details.append("Smoking significantly increases cardiovascular risk.")
    if features_dict['chest_pain_symptom']: explanation_details.append("Reported chest pain is a critical indicator.")
    if features_dict['oxygen_sat'] < 94: explanation_details.append("Oxygen saturation is below optimal levels.")

    # 3. Health Risk Model Inference
    if os.path.exists(MODEL_PATH) and os.path.exists(FEATURES_PATH):
        model = joblib.load(MODEL_PATH)
        feature_names = joblib.load(FEATURES_PATH)
        feature_vector = np.array([[features_dict[name] for name in feature_names]])
        risk_score = float(model.predict_proba(feature_vector)[0][1])
    else:
        risk_score = 0.5 # Default if model missing
    
    # 4. Real Drug Recommendation Logic
    prediction = "General Wellness"
    treatment = "Maintain balanced lifestyle and regular checkups."
    medicines = ["Multivitamins"]
    
    # Attempt to find real drugs for active symptoms or conditions
    real_drug_found = False
    if os.path.exists(DRUG_MODEL_PATH) and os.path.exists(LE_CONDITION_PATH):
        le_condition = joblib.load(LE_CONDITION_PATH)
        le_drug = joblib.load(LE_DRUG_PATH)
        drug_model = joblib.load(DRUG_MODEL_PATH)
        
        # Combine input conditions and symptoms to search for matches in Drug dataset
        search_terms = conditions_input + symptoms
        available_conditions = le_condition.classes_
        
        for term in search_terms:
            # Find closest match in dataset
            matches = difflib.get_close_matches(term, available_conditions, n=1, cutoff=0.6)
            if matches:
                match = matches[0]
                cond_idx = np.array(le_condition.transform([match])).reshape(-1, 1)
                drug_idx = drug_model.predict(cond_idx)[0]
                rec_drug = le_drug.inverse_transform([drug_idx])[0]
                
                prediction = match.capitalize()
                treatment = f"Commonly treated condition with high-rated real-world evidence. Consult provider for {rec_drug}."
                medicines = [rec_drug.capitalize()]
                explanation_details.append(f"Recommendation based on real-world evidence for '{match}'.")
                real_drug_found = True
                break

    # Fallback to hardcoded logic if no real-world clinical match found
    if not real_drug_found:
        if features_dict['chest_pain_symptom'] or features_dict['bp_sys'] > 150:
            prediction = "High Cardiovascular Risk"
            treatment = "Immediate cardiologist consultation required. Low sodium diet."
            medicines = ["Aspirin (consult doctor)", "Antihypertensives (if prescribed)"]
        elif features_dict['blood_sugar'] > 180 or features_dict['thirst_symptom']:
            prediction = "Potential Type 2 Diabetes"
            treatment = "Endocrinology screening needed. Restricted sugar intake."
            medicines = ["Metformin (if prescribed)", "Blood sugar monitor"]
        elif features_dict['oxygen_sat'] < 92:
            prediction = "Pulmonary/Oxygenation Concern"
            treatment = "Seek respiratory evaluation. Avoid strenuous activity."
            medicines = ["Oxygen therapy (if acute)", "Bronchodilators (if prescribed)"]

    return {
        "disease_prediction": prediction,
        "risk_score": risk_score,
        "recommended_treatment": treatment,
        "suggested_medicines": medicines,
        "explanation": f"The AI analysis identifies {prediction} with a {risk_score:.0%} risk probability.",
        "explanation_details": explanation_details if explanation_details else ["No critical risk factors identified."]
    }
