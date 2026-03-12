import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def train_drug_recommendation_model():
    # Load dataset
    train_path = "C:/Users/rames/Downloads/archive/drugLibTrain_raw.tsv"
    test_path = "C:/Users/rames/Downloads/archive/drugLibTest_raw.tsv"
    
    if not os.path.exists(train_path):
        print(f"Error: Dataset not found at {train_path}")
        return

    df_train = pd.read_csv(train_path, sep='\t')
    df_test = pd.read_csv(test_path, sep='\t')
    
    # Process data
    # We want to predict 'urlDrugName' based on 'condition'
    # For a more advanced version, we could use rating and effectiveness to filter
    
    # Filter for high quality data (effectiveness >= 'Considerably Effective' or 'Highly Effective')
    # and rating >= 7
    df_train = df_train[df_train['effectiveness'].isin(['Considerably Effective', 'Highly Effective'])]
    df_train = df_train[df_train['rating'] >= 7]
    
    # Label Encoding for categorical fields
    le_drug = LabelEncoder()
    le_condition = LabelEncoder()
    
    # Combine conditions from train and test to ensure all labels are covered
    all_conditions = pd.concat([df_train['condition'], df_test['condition']]).unique().astype(str)
    le_condition.fit(all_conditions)
    
    # For drugs, we only care about those in the training set for recommendation
    le_drug.fit(df_train['urlDrugName'].unique().astype(str))
    
    # Prepare features and target
    X_train = le_condition.transform(df_train['condition'].astype(str)).reshape(-1, 1)
    y_train = le_drug.transform(df_train['urlDrugName'].astype(str))
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save model and encoders
    model_dir = "models"
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    joblib.dump(model, "models/drug_recommender.joblib")
    joblib.dump(le_drug, "models/le_drug.joblib")
    joblib.dump(le_condition, "models/le_condition.joblib")
    
    # Also save a mapping of condition to top drugs for simpler lookup
    condition_drug_map = df_train.groupby('condition')['urlDrugName'].agg(lambda x: x.value_counts().index[0]).to_dict()
    joblib.dump(condition_drug_map, "models/condition_drug_map.joblib")

    print(f"Drug recommendation model trained on {len(df_train)} records.")
    print(f"Unique drugs: {len(le_drug.classes_)}")
    print(f"Unique conditions: {len(le_condition.classes_)}")

if __name__ == "__main__":
    train_drug_recommendation_model()
