import numpy as np
from scipy.stats import linregress
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.seasonal import seasonal_decompose


def extract_features(data):
    data = np.array(data)

    # 🔹 Trend
    slope, _, r_value, _, _ = linregress(range(len(data)), data)
    trend_strength = abs(r_value)

    # 🔹 Seasonality
    try:
        result = seasonal_decompose(data, period=7)
        seasonality_strength = np.std(result.seasonal) / np.std(data)
    except:
        seasonality_strength = 0

    # 🔹 Noise
    smooth = np.convolve(data, np.ones(3)/3, mode='same')
    residuals = data - smooth
    noise_level = np.std(residuals) / np.std(data)

    return {
        "trend_strength": float(trend_strength),
        "seasonality_strength": float(seasonality_strength),
        "noise_level": float(noise_level)
    }