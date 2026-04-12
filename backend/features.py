import numpy as np
from scipy.stats import linregress
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.seasonal import seasonal_decompose


def extract_features(data):
    data = np.array(data)

    slope, _, r_value, _, _ = linregress(range(len(data)), data)
    trend_strength = abs(r_value)

    period = 7
    nlags = len(data) // 2
    if nlags >= 4:
        try:
            acf_vals = acf(data, nlags=nlags, fft=True)
            if len(acf_vals) > 2:
                best_lag = np.argmax(acf_vals[2:]) + 2
                if acf_vals[best_lag] > 0.1:
                    period = int(best_lag)
        except Exception:
            pass


    try:
        result = seasonal_decompose(data, period=period)
        seasonality_strength = np.std(result.seasonal) / np.std(data)
    except Exception:
        seasonality_strength = 0
        period = 7


    smooth = np.convolve(data, np.ones(3)/3, mode='same')
    residuals = data - smooth
    noise_level = np.std(residuals) / np.std(data)

    return {
        "trend_strength": float(trend_strength),
        "seasonality_strength": float(seasonality_strength),
        "noise_level": float(noise_level),
        "seasonality_period": int(period)
    }