from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import pandas as pd

# Allow requests from frontend
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

# Define input schema matching dataset columns (except target)
class ScoreItem(BaseModel):
    Age: int
    Gender: str
    Academic_Level: str
    Country: str
    Avg_Daily_Usage_Hours: float
    Most_Used_Platform: str
    Affects_Academic_Performance: str  # 'Yes'/'No'
    Sleep_Hours_Per_Night: float
    Mental_Health_Score: int
    Relationship_Status: str
    Conflicts_Over_Social_Media: int

# Load trained model and column list
with open("rfr_model.pkl",'rb') as f:
    model = pickle.load(f)

with open("model_columns.pkl", "rb") as f:
    model_columns = pickle.load(f)

# Initialize FastAPI app
app = FastAPI()

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prediction endpoint
@app.post('/')
async def scoring_endpoint(item: ScoreItem):
    print("Received item:", item)
    
    # Convert Pydantic model to dict
    data = item.model_dump()

    # Ensure numeric fields are correctly typed
    data["Avg_Daily_Usage_Hours"] = float(data["Avg_Daily_Usage_Hours"])
    data["Sleep_Hours_Per_Night"] = float(data["Sleep_Hours_Per_Night"])
    data["Mental_Health_Score"] = int(data["Mental_Health_Score"])
    data["Conflicts_Over_Social_Media"] = int(data["Conflicts_Over_Social_Media"])

    # Create DataFrame
    df = pd.DataFrame([data])
    # print("DataFrame before encoding:\n", df)

    # One-hot encode categorical columns
    categorical_cols = ["Gender", "Academic_Level", "Country", "Most_Used_Platform", "Relationship_Status", "Affects_Academic_Performance"]
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=False)

    # Reindex to match model columns
    df_encoded = df_encoded.reindex(columns=model_columns, fill_value=0)
    print("Encoded DataFrame ready for prediction:\n", df_encoded)

    # Predict
    prediction = model.predict(df_encoded)[0]
    print("Prediction:", prediction)

    return {"prediction": float(prediction)}
