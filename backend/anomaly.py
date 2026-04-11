import numpy as np


def detect_anomalies(data):
    mean = np.mean(data)
    std = np.std(data)

    anomalies = []
    for i, val in enumerate(data):
        if abs(val - mean) > 2 * std:
            anomalies.append({
                "index": i,
                "value": float(val)
            })

    return anomalies