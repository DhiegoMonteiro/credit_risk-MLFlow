import os
import sys
import subprocess
import pandas as pd
import joblib
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, f1_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(file)))
SRC_DIR = os.path.dirname(os.path.abspath(file))
DATA_FILE = os.path.join(BASE_DIR, "data", "processed", "credit_risk_balanced_2500.csv")
CREATE_SAMPLE_SCRIPT = os.path.join(SRC_DIR, "create_balanced_sample.py")
MODEL_SAVE_PATH = os.path.join(BASE_DIR, "best_models")
MLFLOW_TRACKING_DIR = os.path.join(BASE_DIR, "mlruns")

sys.path.append(SRC_DIR)
sys.path.append(os.path.join(SRC_DIR, "config"))

try:
   from config.models_config import MODELS_CONFIG, TRAINING_CONFIG
except ImportError as e:
    raise ImportError(f"Erro ao importar MODEL_CONFIG: {e}")

if not os.path.exists(DATA_FILE):
    print("Arquivo balanceado não encontrado. Executando create_balance_sample.py...")
    subprocess.run(["py", CREATE_SAMPLE_SCRIPT], check=True)

print("Carregando dados...")
df = pd.read_csv(DATA_FILE)
X = df.drop("loan_status", axis=1)
y = df["loan_status"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=TRAINING_CONFIG['test_size'],
    random_state=TRAINING_CONFIG['random_state'], stratify=y
)

mlflow_tracking_uri = f"file:///{MLFLOW_TRACKING_DIR.replace(os.sep, '/')}"
mlflow.set_tracking_uri(mlflow_tracking_uri)
mlflow.set_experiment("credit_risk_experiments")

best_score = 0
best_model = None
best_model_name = ""

print(f" Treinando {len(MODELS_CONFIG)} modelos...\n")

for name, config in MODELS_CONFIG.items():
    print(f"Treinando: {name}")
    model = config['model']
    param_grid = config['params']

    with mlflow.start_run(run_name=name):
        grid = GridSearchCV(
            estimator=model, param_grid=param_grid,
            cv=TRAINING_CONFIG['cv_folds'], scoring=TRAINING_CONFIG['scoring'],
            n_jobs=TRAINING_CONFIG['n_jobs'], verbose=0  # Menos verbose
        )
        grid.fit(X_train, y_train)

        final_model = grid.bestestimator
        preds = final_model.predict(X_test)

        accuracy = accuracy_score(y_test, preds)
        precision = precision_score(y_test, preds, average="macro", zero_division=0)
        f1_macro = f1_score(y_test, preds, average="macro")

        print(f"  ✅ Acurácia: {accuracy:.4f}")

        # Log MLFlow
        mlflow.log_param("model", name)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision_macro", precision)
        mlflow.log_metric("f1_macro", f1_macro)

        if accuracy > best_score:
            best_score = accuracy
            best_model = final_model
            best_model_name = name

print(f"\n MELHOR MODELO: {best_model_name}")
print(f"MELHOR ACURÁCIA: {best_score:.4f}")

if best_model:
    os.makedirs(MODEL_SAVE_PATH, exist_ok=True)
    model_path = os.path.join(MODEL_SAVE_PATH, "melhor_modelo.pkl")
    joblib.dump(best_model, model_path)
    print(f"Modelo salvo em: {model_path}")

    with mlflow.start_run(run_name="Best_Model"):
        mlflow.sklearn.log_model(best_model, "best_model")

print("✅ TREINAMENTO CONCLUÍDO!")