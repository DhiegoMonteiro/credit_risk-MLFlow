import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Testa se a API está funcionando"""
    print("Testando health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"API funcionando!")
            print(f"   - Modelo: {data.get('model_loaded')}")
            print(f"   - Scaler: {data.get('scaler_ready')}")
            return True
        else:
            print(f"Erro: {response.status_code}")
            return False
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return False

def test_prediction():
    """Testa uma predição"""
    print("\n Testando predição...")
    
    test_data = {
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
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        
        if response.status_code == 200:
            result = response.json()
            status = result.get('status')
            confidence = result.get('confidence', 0)
            print(f"Predição: {status}")
            print(f"   - Confiança: {confidence:.2%}")
            return True
        else:
            print(f"Erro: {response.status_code}")
            print(f"   - Resposta: {response.text}")
            return False
    except Exception as e:
        print(f"Erro: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("Testando Credit Risk ML API")
    print("=" * 40)
    
    health_ok = test_health()
    prediction_ok = test_prediction() if health_ok else False
    
    print("\n" + "=" * 40)
    if health_ok and prediction_ok:
        print("Todos os testes passaram!!!!!")
    else:
        print(" Alguns testes falharam.")
        print(" Certifique-se que:")
        print("   1. A aplicação está rodando (python app.py)")
        print("   2. O modelo foi treinado (python src/main.py)")

if __name__ == "__main__":
    main()