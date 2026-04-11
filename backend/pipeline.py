from backend.features import extract_features
from backend.models import select_model, train_and_forecast, evaluate_models
from backend.anomaly import detect_anomalies
from backend.llm import generate_explanation


def run_pipeline(data):
    # Step 1: Feature extraction
    features = extract_features(data)

    # Step 2: Model selection
    model_choice = select_model(features)

    # Step 3: Validation vs baseline
    best_model, hw_error, ma_error = evaluate_models(data)

    # Step 4: Forecast
    forecast = train_and_forecast(data, best_model)

    # Step 5: Anomaly detection
    anomalies = detect_anomalies(data)

    # Step 6: Prepare context for LLM
    context = {
        "trend": features["trend_strength"],
        "seasonality": features["seasonality_strength"],
        "noise": features["noise_level"],
        "forecast": {
            "mean": float(forecast.mean()),
            "min": float(forecast.min()),
            "max": float(forecast.max())
        },
        "anomalies": anomalies,
        "model": best_model
    }

    explanation = generate_explanation(context)

    return {
        "features": features,
        "model_selected": best_model,
        "forecast": forecast.tolist(),
        "anomalies": anomalies,
        "explanation": explanation,
        "baseline_error": ma_error,
        "model_error": hw_error
    }