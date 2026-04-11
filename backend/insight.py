import numpy as np


def trend_direction(features):
    trend = features["trend_strength"]

    if trend > 0.6:
        return "strong trend"
    elif trend > 0.3:
        return "moderate trend"
    else:
        return "stable"


def growth_rate(data):
    if len(data) < 2 or data[0] == 0:
        return 0.0

    return float((data[-1] - data[0]) / data[0])

def risk_level(features):
    noise = features["noise_level"]

    if noise > 0.7:
        return "high"
    elif noise > 0.4:
        return "medium"
    else:
        return "low"


def data_type(features):
    if features["seasonality_strength"] > 0.5:
        return "seasonal"
    elif features["trend_strength"] > 0.5:
        return "trending"
    else:
        return "random"


def volatility(data):
    return float(np.std(data))

def confidence_interval(data, forecast):
    std = np.std(data)

    if isinstance(forecast, list) and len(forecast) > 0:
        forecast_arr = np.array(forecast)

    else:
        mean_val = np.mean(data)
        forecast_arr = np.array([mean_val] * len(data))

    lower = forecast_arr - 1.96 * std
    upper = forecast_arr + 1.96 * std

    return {
        "lower": lower.tolist(),
        "upper": upper.tolist()
    }


def generate_insights(data, features, forecast):
    return {
        "trend_direction": trend_direction(features),
        "growth_rate": growth_rate(data),
        "risk_level": risk_level(features),
        "data_type": data_type(features),
        "volatility": volatility(data),
        "confidence_interval": confidence_interval(data, forecast)
    }