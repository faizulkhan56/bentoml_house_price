# BentoML House Price Predictor Demo

This project demonstrates how to:  
1. Train a simple scikit-learn regression model  
2. Save the model into the BentoML model store  
3. Serve the model via a REST API using BentoML v1.3.x  

## Prerequisites
- Python 3.8+  
- `virtualenv` support  

## Project Structure
```
bentoml_house_price/
├── README.md             # this file
├── requirements.txt      # Python dependencies
├── model_train_v1.py     # script to train & save the model
├── model_service_v1.py   # BentoML service to serve predictions
└── .gitignore            # ignore Python caches and model artifacts
```

## Setup & Run

```bash
# 1. Clone the repo
git clone https://your.repo.url/bentoml_house_price.git
cd bentoml_house_price

# 2. Create & activate a virtualenv
python3 -m venv bentoml-env
source bentoml-env/bin/activate

# 3. Install dependencies (pins BentoML to <1.4)
pip install -r requirements.txt

# 4. Train the model
python3 model_train_v1.py

# 5. Verify the model in the BentoML store
bentoml models list

# 6. Serve the model as a REST API
bentoml serve model_service_v1:svc --reload

# 7. In another shell, test the endpoint
curl -X POST http://localhost:3000/predict_house_price \
  -H "Content-Type: application/json" \
  -d '{"square_footage":2500,"num_rooms":4}'

# 8. (Optional) Stop the server with Ctrl+C
```

---

## Theory & Architecture

1. **Data & Experimentation**  
   - Generate or load your dataset (house features & prices).  
   - Run MLflow experiments: train models (Linear, Tree, Forest) and log artifacts with `mlflow.sklearn.log_model()`.

2. **Model Registry**  
   - Register your chosen run’s artifact as a Registered Model in MLflow (e.g. `HousingRF:Production`).

3. **Packaging with BentoML**  
   - Import the MLflow-registered model into BentoML:  
     ```bash
     bentoml mlflow import --name housing_service HousingRF:Production
     ```  
   - BentoML wraps your model artifact and metadata into its own model store.

4. **Serving**  
   - Write `model_service_v1.py` that loads `housing_service` and defines a `/predict_house_price` endpoint.  
   - Launch:  
     ```bash
     bentoml serve model_service_v1:svc --reload
     ```

5. **Online Inference**  
   - Frontend POSTs JSON features to `/predict_house_price`.  
   - BentoML deserializes, runs `model.predict()`, and returns the predicted price.

---

### Quick End-to-End Diagram

```text
[ Data Generation ]
        │
        ▼
[ MLflow Experiment ] ──► mlflow.sklearn.log_model()
        │
        ▼
[ MLflow Model Registry ]
        │
        ▼
bentoml mlflow import HousingRF:Production
        │
        ▼
[ BentoML Model Store ]
        │
        ▼
bentoml serve model_service_v1:svc
        │
        ▼
[ /predict_house_price API ]
        │
        ▼
[ Frontend Client ]
```

This README covers the full lifecycle from data → experiment → registry → packaging → serving → frontend inference. Enjoy building your MLOps pipeline!
