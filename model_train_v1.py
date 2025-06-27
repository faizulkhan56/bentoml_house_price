import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import bentoml

# Generate synthetic housing data
def generate_data():
    data = {
        'square_footage': [1000,1500,1800,2000,2300,2500,2700,3000,3200,3500],
        'num_rooms':      [   3,   4,   4,   5,   5,   6,   6,   7,   7,   8],
        'price':          [200000,250000,280000,310000,340000,370000,400000,430000,460000,500000]
    }
    return pd.DataFrame(data)

# 1. Load data
df = generate_data()
X = df[['square_footage','num_rooms']]
y = df['price']

# 2. Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Train
model = LinearRegression()
model.fit(X_train, y_train)

# 4. Save with BentoML
bentoml.sklearn.save_model("house_price_model", model)
print("Model trained and saved to BentoML store.")