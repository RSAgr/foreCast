from backend.features import extract_features
from backend.models import train_and_forecast, evaluate_models
from backend.anomaly import detect_anomalies
from backend.llm import generate_explanation


def run_pipeline(data , query):
    # Step 1: Feature extraction
    features = extract_features(data)
    period = features.get("seasonality_period", 7)

    # Step 2: Validation vs baseline
    best_model, hw_error, ma_error = evaluate_models(data, period)

    # Step 3: Forecast
    forecast = train_and_forecast(data, best_model, steps=7, period=period)

    # Step 4: Anomaly detection
    anomalies = detect_anomalies(data)

    # Step 5: Prepare context for LLM
    context = {
        "historical_data": list(data),
        "trend": features["trend_strength"],
        "seasonality": features["seasonality_strength"],
        "noise": features["noise_level"],
        "forecast": {
            "mean": float(forecast.mean()),
            "min": float(forecast.min()),
            "max": float(forecast.max())
        },
        "anomalies": anomalies,
        "model": best_model,
    }

    explanation = generate_explanation(context , query)

    return {
        "features": features,
        "model_selected": best_model,
        "forecast": forecast.tolist(),
        "anomalies": anomalies,
        "explanation": explanation,
        "baseline_error": ma_error,
        "model_error": hw_error
    }