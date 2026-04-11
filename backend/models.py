import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_percentage_error


def moving_average_forecast(data, steps=7):
    avg = np.mean(data[-5:])
    return np.array([avg] * steps)


def linear_trend_forecast(data, steps=7):
    from scipy.stats import linregress
    x = np.arange(len(data))
    slope, intercept, _, _, _ = linregress(x, data)
    future_x = np.arange(len(data), len(data) + steps)
    return slope * future_x + intercept


def holt_winters_forecast(data, steps=7):
    model = ExponentialSmoothing(data, seasonal='add', seasonal_periods=7)
    fit = model.fit()
    return fit.forecast(steps)


def select_model(features):
    if features["seasonality_strength"] > 0.5:
        return "holt_winters"
    elif features["noise_level"] > 0.6:
        return "moving_average"
    elif features["trend_strength"] > 0.5:
        return "holt_winters"
    else:
        return "moving_average"


def train_and_forecast(data, model_name, steps=7):
    if model_name == "holt_winters":
        return holt_winters_forecast(data, steps)
    elif model_name == "linear_trend":
        return linear_trend_forecast(data, steps)
    else:
        return moving_average_forecast(data, steps)


def evaluate_models(data):
    train = data[:-7]
    test = data[-7:]
    
    # If not enough data for complex seasonal models, use linear trend instead of flat average
    if len(train) < 14:
        return "linear_trend", None, None

    ma_pred = moving_average_forecast(train, 7)
    hw_pred = holt_winters_forecast(train, 7)
    lin_pred = linear_trend_forecast(train, 7)

    ma_error = mean_absolute_percentage_error(test, ma_pred)
    hw_error = mean_absolute_percentage_error(test, hw_pred)
    lin_error = mean_absolute_percentage_error(test, lin_pred)

    best_error = min(ma_error, hw_error, lin_error)
    
    if best_error == hw_error:
        return "holt_winters", hw_error, ma_error
    elif best_error == lin_error:
        return "linear_trend", lin_error, ma_error
    else:
        return "moving_average", ma_error, ma_error