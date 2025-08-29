Here’s a polished, copy-paste-ready **README.md** for your Addiction Checker project:

---

# Addiction Checker – College Students’ Social Media Analysis

Predicts a student’s **social media addiction score** from survey inputs using a **Random Forest Regressor** served via **FastAPI**, with a **React + Vite** frontend for interactive predictions.

![Status](https://img.shields.io/badge/status-active-brightgreen) ![Python](https://img.shields.io/badge/Python-3.10+-blue) ![FastAPI](https://img.shields.io/badge/API-FastAPI-teal) ![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Table of Contents

* [Features](#features)
* [Tech Stack](#tech-stack)
* [Architecture](#architecture)
* [Dataset](#dataset)
* [Modeling](#modeling)
* [Project Structure](#project-structure)
* [Backend Setup (FastAPI)](#backend-setup-fastapi)
* [API Endpoints](#api-endpoints)
* [Frontend Setup (React + Vite)](#frontend-setup-react--vite)
* [Environment Variables](#environment-variables)
* [Development Workflow](#development-workflow)
* [Testing](#testing)
* [Deployment](#deployment)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Acknowledgements](#acknowledgements)

---



## Features

* ⚙️ **ML Model**: Random Forest Regressor trained on Kaggle data to predict an addiction score.
* 🚀 **FastAPI Backend**: Serves `/predict` endpoint; loads a serialized `.pkl` model.
* ⚡ **React + Vite Frontend**: Clean form, instant predictions, validation, and result UI.
* 🔐 **Input Validation**: Pydantic schemas on the API; client-side checks in the UI.
* 📈 **Reproducible Pipeline**: Scripts for training, evaluation, and model export.

---

## Tech Stack

* **ML / Data**: Python, scikit-learn, pandas, numpy
* **API**: FastAPI, Uvicorn, Pydantic
* **Frontend**: React, Vite, (optional) TailwindCSS
* **Tooling**: Git, Postman/Bruno (API testing), joblib/pickle

---

## Architecture

```
Client (React + Vite)  ↔  FastAPI (Python)
           ⤷ sends JSON              ⤶ returns predicted addiction score (float)
                           ↳ Loads model.pkl (RandomForestRegressor)
```

---

## Dataset

* Source: **Kaggle – College students’ social media addiction/usage** (attributes like age, gender, academic level, daily usage hours, platform, sleep hours, conflicts, etc.).
* **Note**: Ensure you have permission to use and redistribute the dataset. Store raw data under `data/raw/` and never commit sensitive data.

---

## Modeling

* **Target**: `Addicted_Score` (continuous)
* **Inputs** (example): `Age`, `Gender`, `Academic_Level`, `Country`, `Avg_Daily_Usage_Hours`, `Most_Used_Platform`, `Affects_Academic_Performance`, `Sleep_Hours_Per_Night`, `Mental_Health_Score`, `Relationship_Status`, `Conflicts_Over_Social_Media`, etc.
* **Pipeline**:

  * Impute missing values (numeric: median; categorical: most frequent)
  * Encode categorical features (OneHotEncoder)
  * Scale if needed (optional for trees)
  * Model: `RandomForestRegressor` (with tuned `n_estimators`, `max_depth`)
* **Evaluation**: `MAE`, `RMSE`, `R²`
* **Serialization**: `joblib` or `pickle` → `model/model.pkl`

---

## Project Structure

```
addiction-checker/
├─ backend/
│  ├─ app.py                  # FastAPI app (main entry)
│  ├─ schema.py               # Pydantic request/response models
│  ├─ model_loader.py         # Loads model.pkl, transformer, feature order
│  ├─ requirements.txt
│  └─ model/
│     ├─ model.pkl
│     └─ preprocessor.pkl     # optional if you persist preprocessing
├─ ml/
│  ├─ train.py                # trains model & saves pkl(s)
│  ├─ evaluate.py             # prints MAE/RMSE/R²
│  └─ utils.py
├─ data/
│  ├─ raw/                    # put Kaggle CSV here (not committed)
│  └─ processed/              # cleaned/training splits
├─ client/
│  ├─ index.html
│  ├─ vite.config.js
│  ├─ package.json
│  └─ src/
│     ├─ main.jsx
│     ├─ App.jsx              # form & result UI
│     └─ api.js               # axios client
├─ .env.example
├─ README.md
└─ LICENSE
```

---

## Backend Setup (FastAPI)

1. **Create & activate venv**

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

2. **Install deps**

```bash
pip install -r requirements.txt
# if requirements.txt not created yet:
pip install fastapi uvicorn scikit-learn pandas numpy pydantic joblib
```

3. **Train the model (first time)**

```bash
cd ..
python ml/train.py --data data/raw/dataset.csv --out backend/model
python ml/evaluate.py --data data/raw/dataset.csv --model backend/model/model.pkl
```

4. **Run API**

```bash
cd backend
uvicorn app:app --reload --port 8000
```

---

## API Endpoints

### `GET /health`

* Returns API health status.

```json
{ "status": "ok" }
```

### `POST /predict`

* **Request Body** (example – adjust to your schema):

```json
{
  "age": 22,
  "gender": "Male",
  "academic_level": "Undergraduate",
  "country": "India",
  "avg_daily_usage_hours": 5.2,
  "most_used_platform": "Instagram",
  "affects_academic_performance": true,
  "sleep_hours_per_night": 6.5,
  "mental_health_score": 6,
  "relationship_status": "In Relationship",
  "conflicts_over_social_media": 3
}
```

* **Response**:

```json
{
  "predicted_addiction_score": 7.9
}
```

> Tip: Include your full `schema.py` (Pydantic models) and keep frontend field names identical.

**CORS**
If the client runs on a different port:

```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Frontend Setup (React + Vite)

1. **Install & run**

```bash
cd client
npm install
npm run dev
```

2. **Call the API** (axios example in `src/api.js`)

```js
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
});

export const predictAddiction = (payload) =>
  api.post("/predict", payload).then(res => res.data);
```

3. **Use in `App.jsx`**

```jsx
const onSubmit = async (form) => {
  setLoading(true);
  try {
    const { predicted_addiction_score } = await predictAddiction(form);
    setScore(predicted_addiction_score.toFixed(2));
  } finally {
    setLoading(false);
  }
};
```

---

## Environment Variables

Create `.env` files from the examples below.

**Backend (`backend/.env`)**

```
MODEL_PATH=backend/model/model.pkl
PREPROCESSOR_PATH=backend/model/preprocessor.pkl
PORT=8000
```

**Frontend (`client/.env`)**

```
VITE_API_BASE_URL=http://localhost:8000
```

---

## Development Workflow

* Make changes in `ml/train.py` → regenerate `model.pkl`
* Keep `schema.py` in sync with the frontend form fields
* Version your model artifacts (`model_v1.pkl`, `model_v2.pkl`) if you iterate frequently
* Use **Postman/Bruno** collections to document sample requests

---

## Testing

**Backend**

```bash
pytest -q    # if you add tests/
```

**Frontend**

```bash
npm run test # if configured (Vitest/Jest)
```

---

## Deployment

**Backend**

* Render / Railway / Fly.io / GCP Cloud Run / AWS Elastic Beanstalk
* Dockerfile (optional)
* Remember to set `MODEL_PATH` and upload `model.pkl`

**Frontend**

* Vercel / Netlify / GitHub Pages (Vite build)

```bash
npm run build
npm run preview
```

---

## Roadmap

* [ ] Improve feature engineering (interaction terms, domain features)
* [ ] Hyperparameter tuning with Optuna
* [ ] Confidence intervals / prediction uncertainty
* [ ] Better UI/UX with Tailwind & form validation
* [ ] Auth + saved assessments (Supabase/Appwrite)
* [ ] Basic analytics dashboard

---

## Contributing

1. Fork the repo & create a feature branch
2. Commit with conventional messages
3. Open a PR with a clear description & screenshots

---

## License

This project is licensed under the **MIT License**. See `LICENSE` for details.

---

## Acknowledgements

* Kaggle dataset contributors for the underlying survey data
* scikit-learn & FastAPI communities
* React & Vite ecosystem

---

> **Tip:** After you paste this into `README.md`, replace placeholders (dataset path, screenshots, metrics like MAE/RMSE), and commit your actual `schema.py`, `train.py`, and endpoint code snippets so recruiters can see the implementation.
