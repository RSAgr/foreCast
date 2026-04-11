import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_percentage_error


def moving_average_forecast(data, steps=7):
    avg = np.mean(data[-5:])
    return np.array([avg] * steps)


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
    else:
        return moving_average_forecast(data, steps)


def evaluate_models(data):
    train = data[:-7]
    test = data[-7:]
    if len(train) < 14:
        return "moving_average", None, None

    ma_pred = moving_average_forecast(train, 7)
    hw_pred = holt_winters_forecast(train, 7)

    ma_error = mean_absolute_percentage_error(test, ma_pred)
    hw_error = mean_absolute_percentage_error(test, hw_pred)

    if hw_error < ma_error:
        return "holt_winters", hw_error, ma_error
    else:
        return "moving_average", hw_error, ma_error