from sklearn.linear_model import LinearRegression
import numpy as np

def forecast_churn(history: list[int]) -> int:
    if len(history) < 3:
        return -1  # not enough data

    X = np.arange(len(history)).reshape(-1, 1)
    y = np.array(history)
    model = LinearRegression()
    model.fit(X, y)
    next_x = np.array([[len(history)]])
    return int(model.predict(next_x)[0])
