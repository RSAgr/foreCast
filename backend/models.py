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


def holt_winters_forecast(data, steps=7, period=7):
    model = ExponentialSmoothing(data, seasonal='add', seasonal_periods=period)
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


def train_and_forecast(data, model_name, steps=7, period=7):
    if model_name == "holt_winters":
        return holt_winters_forecast(data, steps, period)
    elif model_name == "linear_trend":
        return linear_trend_forecast(data, steps)
    else:
        return moving_average_forecast(data, steps)


def evaluate_models(data, period=7):
    # If data is ridiculously small, just default to moving average without testing
    if len(data) <= 5:
        return "moving_average", None, None
        
    # Dynamically allocate test size (up to 7 items, but max 25% of the dataset)
    test_size = min(7, max(1, len(data) // 4))
    train = data[:-test_size]
    test = data[-test_size:]

    ma_pred = moving_average_forecast(train, test_size)
    lin_pred = linear_trend_forecast(train, test_size)

    # MA is our baseline error
    ma_error = float(mean_absolute_percentage_error(test, ma_pred))
    lin_error = float(mean_absolute_percentage_error(test, lin_pred))

    hw_error = float('inf')
    # Only test Holt-Winters if we have 2 full seasons + test_size
    if len(train) >= 2 * period:
        try:
            hw_pred = holt_winters_forecast(train, test_size, period)
            hw_error = float(mean_absolute_percentage_error(test, hw_pred))
        except Exception:
            pass # Catch statsmodel math errors if data is flat

    best_error = min(ma_error, hw_error, lin_error)
    
    if best_error == hw_error:
        return "holt_winters", hw_error, ma_error
    elif best_error == lin_error:
        return "linear_trend", lin_error, ma_error
    else:
        return "moving_average", ma_error, ma_error