from langgraph.graph import StateGraph

from backend.features import extract_features
from backend.models import evaluate_models, train_and_forecast
from backend.anomaly import detect_anomalies
from backend.llm import generate_explanation
from backend.insight import generate_insights

def query_node(state):
    q = (state.get("query") or "").lower()

    if "anomaly" in q or "issue" in q:
        state["task"] = "anomaly"
    elif "trend" in q or "insight" in q:
        state["task"] = "insight"
    elif "forecast" in q or "predict" in q:
        state["task"] = "forecast"
    else:
        state["task"] = "forecast"  

    return state


def feature_node(state):
    state["features"] = extract_features(state["data"])
    return state

def forecast_node(state):
    best_model, hw_error, ma_error = evaluate_models(state["data"])
    forecast = train_and_forecast(state["data"], best_model)

    state["model"] = best_model
    state["forecast"] = forecast.tolist()
    state["model_error"] = hw_error
    state["baseline_error"] = ma_error

    return state


def anomaly_node(state):
    state["anomalies"] = detect_anomalies(state["data"])
    return state

def insight_node(state):
  
    forecast = state.get("forecast", state["data"])

    state["insights"] = generate_insights(
        state["data"],
        state["features"],
        forecast
    )
    return state

def llm_node(state):
    forecast_list = state.get("forecast", [])

    if forecast_list:
        forecast_summary = {
            "mean": float(sum(forecast_list) / len(forecast_list)),
            "min": float(min(forecast_list)),
            "max": float(max(forecast_list))
        }
    else:
        forecast_summary = {"mean": None, "min": None, "max": None}

    context = {
        "historical_data": state["data"], 
        "trend": state["features"]["trend_strength"],
        "seasonality": state["features"]["seasonality_strength"],
        "noise": state["features"]["noise_level"],
        "forecast": forecast_summary,
        "anomalies": state.get("anomalies"),
        "model": state.get("model"),
        "model_error": state.get("model_error"),
        "baseline_error": state.get("baseline_error")
    }

    state["explanation"] = generate_explanation(context, state.get("query"))
    return state


def route_task(state):
    return state["task"]


builder = StateGraph(dict)

builder.add_node("query", query_node)
builder.add_node("features", feature_node)
builder.add_node("forecast", forecast_node)
builder.add_node("anomaly", anomaly_node)
builder.add_node("insight", insight_node)
builder.add_node("llm", llm_node)

builder.set_entry_point("query")

builder.add_edge("query", "features")

builder.add_conditional_edges(
    "features",
    route_task,
    {
        "forecast": "forecast",
        "anomaly": "anomaly",
        "insight": "insight"
    }
)

builder.add_edge("forecast", "insight")

builder.add_edge("insight", "llm")

builder.add_edge("anomaly", "llm")

graph = builder.compile()