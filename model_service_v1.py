import bentoml
from bentoml.io import JSON
from pydantic import BaseModel

# 1. Load model & create runner
model_ref    = bentoml.sklearn.get("house_price_model:latest")
model_runner = model_ref.to_runner()

# 2. Define the service with runner
svc = bentoml.Service("house_price_predictor", runners=[model_runner])

# 3. Input schema
class HouseInput(BaseModel):
    square_footage: float
    num_rooms:      int

# 4. Prediction endpoint
@svc.api(input=JSON(pydantic_model=HouseInput), output=JSON())
async def predict_house_price(data: HouseInput):
    features = [[data.square_footage, data.num_rooms]]
    prediction = await model_runner.predict.async_run(features)
    return {"predicted_price": prediction[0]}
