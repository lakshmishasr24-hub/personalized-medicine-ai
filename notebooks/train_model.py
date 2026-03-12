import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train_expanded_model():
    np.random.seed(42)
    data_size = 1000
    
    data = {
        'age': np.random.randint(18, 90, data_size),
        'gender': np.random.randint(0, 2, data_size), # 0: Male, 1: Female
        'bmi': np.random.uniform(15, 45, data_size),
        'has_diabetes_history': np.random.randint(0, 2, data_size),
        'has_heart_history': np.random.randint(0, 2, data_size),
        'is_smoker': np.random.randint(0, 2, data_size),
        'heavy_drinker': np.random.randint(0, 2, data_size),
        'exercise_level': np.random.randint(0, 3, data_size), # 0: None, 1: Moderate, 2: Active
        'sleep_hours': np.random.randint(4, 10, data_size),
        'blood_sugar': np.random.randint(70, 250, data_size),
        'cholesterol': np.random.randint(150, 300, data_size),
        'bp_sys': np.random.randint(90, 180, data_size),
        'oxygen_sat': np.random.randint(85, 100, data_size),
        'chest_pain_symptom': np.random.randint(0, 2, data_size),
        'thirst_symptom': np.random.randint(0, 2, data_size),
    }
    
    df = pd.DataFrame(data)
    
    # Complex Risk Calculation logic
    risk = np.zeros(data_size)
    risk += (df['age'] / 90) * 0.2
    risk += (df['bmi'] > 30).astype(int) * 0.15
    risk += df['is_smoker'] * 0.1
    risk += (df['blood_sugar'] > 140).astype(int) * 0.2
    risk += (df['bp_sys'] > 140).astype(int) * 0.15
    risk += df['has_heart_history'] * 0.1
    risk += (df['oxygen_sat'] < 92).astype(int) * 0.2
    risk += df['chest_pain_symptom'] * 0.3
    
    df['high_risk'] = (risk > 0.5).astype(int)
    
    X = df.drop('high_risk', axis=1)
    y = df['high_risk']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    
    # Save model and feature names
    model_dir = "models"
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    joblib.dump(model, "models/health_risk_model.joblib")
    # Also save feature order to ensure consistency
    joblib.dump(list(X.columns), "models/feature_names.joblib")
    
    print(f"Expanded model saved. Test Accuracy: {model.score(X_test, y_test):.2f}")
    print(f"Features: {list(X.columns)}")

if __name__ == "__main__":
    train_expanded_model()
