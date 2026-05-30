# Architecture Overview

## System parts

- `scripts/`: data processing, training, evaluation, and model comparison scripts.
- `ml-service/`: FastAPI backend that loads the trained model and exposes prediction endpoints.
- `webapp/PredictTheScore.Web/`: ASP.NET Core MVC frontend for entering student data, calling the ML API, and showing history.
- `database/`: MySQL schema for prediction history.
- `reports/`: generated audit files, charts, metrics, and comparison tables.

## Prediction flow

1. The user enters student information in the web form.
2. The browser sends JSON to `POST /Predict/Submit` in the ASP.NET Core app.
3. `MlApiClient` forwards the six model fields to FastAPI `POST /predict`.
4. FastAPI validates the request with Pydantic and runs the `LinearRegression` model.
5. FastAPI returns `predicted_score`, `predicted_score_10`, `model_name`, and `message`.
6. The MVC app saves the result to MySQL through `PredictionHistoryService`.
7. The browser displays the prediction and reloads `/Predict/History`.

## Run commands

```bash
python scripts/build_dataset.py
python scripts/train_model.py --scenario web_minimal
python scripts/evaluate_model.py
python scripts/compare_models.py
uvicorn app.main:app --reload --app-dir ml-service
dotnet run --project webapp/PredictTheScore.Web/PredictTheScore.Web.csproj
```
