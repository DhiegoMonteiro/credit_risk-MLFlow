# Projeto com MLFlow para predição de risco de crédito (Credit-Risk)

Desenvolvido por: **André Luiz**, **Dhiego Fernando**, **Luiz Henrique** e **Maria Morais**

## Pré-Requisitos: 
| Instalação do Python 3.13 disponível em: (https://www.python.org/downloads/)

| Instalação do Docker Desktop disponível em : (https://docs.docker.com/desktop/)

| Instalação do Git/Git bash disponível em: (https://git-scm.com/downloads/win)

### Etapas:

## 1. Primeiramente abra o GitBash e  faça o clone do projeto utilizando o seguinte comando:

```
git clone https://github.com/DhiegoMonteiro/credit_risk-MLFlow.git
```
## 2. Com o projeto clonado navegue ate a pasta src 

```
cd credit_risk-MLFlow/src/
```

## 3. Utilize o seguinte comando para executar a main.py

```
py main.py
```
*  **Este comando é de extrema importância, ele irá fazer o treinamento dos modelos e exportação do melhor modelo a ser utilizado dentre os 6 escolhidos, o treinamento e exportação deverá levar cerca de 10-20min até sua conclusão.**

## 4. Após gerar o modelo correto navegue até o diretório do projeto novamente

```
cd ..
```

## 5. Verifique a existência do diretório best_models onde encontrará o melhor modelo gerado

## 6. Abra o Docker Desktop e no diretório principal do projeto rode o comando a seguir

```
docker compose up --build -d
```

## 7. Após isso, acesse no navegador

```
http://localhost:4200/
```

## 8. Caso queira fazer um teste para verificar se a aplicação esta funcionando vá no diretório principal do projeto e execute:

```
py test_app.py
```
* **Você deverá ver algo como:**
```
Testando Credit Risk ML API
========================================
Testando health check...
API funcionando!
   - Modelo: True
   - Scaler: True

 Testando predição...
Predição: Negado
   - Confiança: 98.96%

========================================
Todos os testes passaram!!!!!
```

* **Outra alternativa é acessar:**

```
http://localhost:5000/health
```
**Você deverá ver algo como:**

```
{
  "model_loaded": true,
  "scaler_ready": true,
  "status": "healthy"
}
```




