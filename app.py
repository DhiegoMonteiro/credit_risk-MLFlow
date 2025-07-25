import os
import pandas as pd
import joblib
import numpy as np
from flask_cors import CORS
from flask import Flask, request, jsonify, send_file
from io import StringIO, BytesIO
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
CORS(app)

model = None
scaler = None
required_columns = ["person_age","person_income","person_home_ownership",
                    "person_emp_length","loan_intent","loan_grade","loan_amnt",  "loan_int_rate",
                      "loan_percent_income","cb_person_default_on_file", "cb_person_cred_hist_length"]

def load_model():
    """Carrega o melhor modelo salvo"""
    global model, scaler
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "best_models", "melhor_modelo.pkl")
    DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "credit_risk_balanced_2500.csv")
    
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("Modelo carregado com sucesso!")
    else:
        print("Modelo não encontrado! Execute main.py primeiro.")
        return False
    
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        X = df.drop("loan_status", axis=1)
        scaler = StandardScaler()
        scaler.fit(X)
        print("Scaler preparado!")
    else:
        print(" Dados não encontrados, sem scaling")
        scaler = None
    
    return True

@app.route('/')
def home():
    """Página inicial simples"""
    return """
    <h1>Credit Risk ML API</h1>
    <p>API para predição de risco de crédito</p>
    <h3>Endpoints:</h3>
    <ul>
        <li><strong>POST /predict</strong> - Fazer predição</li>
        <li><strong>GET /health</strong> - Status da API</li>
        <li><strong>POST /csv</strong> - Fazer Predições ao importar csv</li>
    </ul>
    <h3>Exemplo de uso:</h3>
    <pre>
curl -X POST http://localhost:5000/predict \\
  -H "Content-Type: application/json" \\
  -d '{
    "person_age": 25,
    "person_income": 50000,
    "person_home_ownership": 1,
    "person_emp_length": 3,
    "loan_intent": 2,
    "loan_grade": 1,
    "loan_amnt": 10000,
    "loan_int_rate": 12.5,
    "loan_percent_income": 0.2,
    "cb_person_default_on_file": 0,
    "cb_person_cred_hist_length": 5
  }'
    </pre>
    """
@app.route('/csv', methods=['POST'])
def predict_csv():
    if model is None:
        return jsonify({'error': 'Modelo não carregado'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'Arquivo CSV não fornecido'}), 400

    file = request.files['file']

    try:
        df = pd.read_csv(file)

        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            return jsonify({'error': f'Colunas ausentes no CSV: {missing_cols}'}), 400
        
        if df['person_home_ownership'].dtype == object:
            df['person_home_ownership'] = df['person_home_ownership'].str.upper().map({
                'RENT': 0, 'OWN': 1, 'MORTGAGE': 2, 'OTHER': 3
            })

        if df['loan_intent'].dtype == object:
            df['loan_intent'] = df['loan_intent'].str.upper().map({
                'PERSONAL': 0, 'EDUCATION': 1, 'MEDICAL': 2,
                'VENTURE': 3, 'HOMEIMPROVEMENT': 4, 'DEBTCONSOLIDATION': 5
            })

        if df['loan_grade'].dtype == object:
            df['loan_grade'] = df['loan_grade'].str.upper().map({
                'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6
            })

        if df['cb_person_default_on_file'].dtype == object:
            df['cb_person_default_on_file'] = df['cb_person_default_on_file'].str.upper().map({
                'N': 0, 'Y': 1
            })

        X = df[required_columns]
        if scaler is not None:
            X = scaler.transform(X)
        else:
            X = X.values

        preds = model.predict(X)

        df['loan_status'] = preds
        df['status'] = df['loan_status'].apply(lambda x: 'Negado (Inadimplente)' if x == 1 else 'Aprovado (Não inadimplente)')

        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)

        return send_file(BytesIO(output.getvalue().encode()),
                         mimetype='text/csv',
                         as_attachment=True,
                         download_name='credit_risk_predicoes.csv')

    except Exception as e:
        return jsonify({'error': f'Erro ao processar o arquivo: {str(e)}'}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint principal para predições"""
    try:
        if model is None:
            return jsonify({'error': 'Modelo não carregado'}), 500
        
        data = request.json
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        df = pd.DataFrame([data])
        
        if scaler is not None:
            X = scaler.transform(df)
        else:
            X = df.values
        
        prediction = model.predict(X)[0]
        
        try:
            proba = model.predict_proba(X)[0]
            confidence = max(proba)
        except:
            confidence = 0.5
        
        return jsonify({
            'prediction': int(prediction),
            'status': 'Aprovado' if prediction == 1 else 'Negado',
            'confidence': round(float(confidence), 4)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'scaler_ready': scaler is not None
    })

if __name__ == '__main__':
    if load_model():
        print("Iniciando servidor Flask...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("Falha ao carregar modelo. Execute 'python src/main.py' primeiro.")
        exit(1)