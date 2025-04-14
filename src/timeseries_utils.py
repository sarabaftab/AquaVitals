import pandas as pd

def generate_time_series_features(df, cols, lags=[3], rolling_windows=[7]):
    """
    Adds lag and rolling average features for time-series analysis.

    Args:
        df (pd.DataFrame): Input DataFrame with date-sorted values.
        cols (list): List of column names to apply transformations on.
        lags (list): List of lag days to apply (e.g., [3, 7]).
        rolling_windows (list): List of window sizes for rolling averages.

    Returns:
        pd.DataFrame: Modified DataFrame with new time-series features.
    """
    df = df.copy()
    for col in cols:
        for lag in lags:
            df[f"{col} (Lag {lag})"] = df[col].shift(lag)
        for window in rolling_windows:
            df[f"{col} {window}-day avg"] = df[col].rolling(window=window, min_periods=window).mean()
    return df