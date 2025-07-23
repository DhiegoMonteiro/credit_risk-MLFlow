import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_balanced_sample():
    input_path = os.path.join(BASE_DIR, "data", "processed", "credit_risk.csv")
    if not os.path.exists(input_path):
        return False
    
    df = pd.read_csv(input_path)
    
    class_0 = df[df['loan_status'] == 0]
    class_1 = df[df['loan_status'] == 1]
    
    if len(class_0) < 1250 or len(class_1) < 1250:
        return False
    
    sample_0 = class_0.sample(n=1250, random_state=42)
    sample_1 = class_1.sample(n=1250, random_state=42)
    
    balanced_sample = pd.concat([sample_0, sample_1], ignore_index=True)
    balanced_sample = balanced_sample.sample(frac=1, random_state=42).reset_index(drop=True)
    
    output_path = os.path.join(BASE_DIR, "data", "processed", "credit_risk_balanced_2500.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    balanced_sample.to_csv(output_path, index=False)
    
    return output_path

def verify_balanced_sample():
    sample_path = os.path.join(BASE_DIR, "data", "processed", "credit_risk_balanced_2500.csv")
    
    if not os.path.exists(sample_path):
        return False
    
    df = pd.read_csv(sample_path)
    dist = df['loan_status'].value_counts().sort_index()
    
    if len(dist) == 2 and dist.iloc[0] == 1250 and dist.iloc[1] == 1250:
        return True
    else:
        return False

if __name__ == "__main__":
    sample_path = create_balanced_sample()
    
    if sample_path:
        verify_balanced_sample()
