import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.impute import KNNImputer
from timeseries_utils import generate_time_series_features


def load_spring_temp_data():
    def get_season(month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Fall"

    df = pd.read_excel("../../Data/Raw/Main_Data_edited.xlsx")
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    # ✅ Drop rows where Spring Temp is missing
    df = df.dropna(subset=["Spring Temp (F)"])

    # Feed imputation (categorical)
    df["AM Feed"] = df["AM Feed"].fillna("X")
    df["PM Feed"] = df["PM Feed"].fillna("X")

    # Feature engineering
    df["Season"] = df["Month"].apply(get_season)
    df["Max Air Temp x Rain"] = df["Max air temp"] * (df["Dec Rain"] + df["Calmar Rain"])
    df["Total Rain"] = df["Dec Rain"] + df["Calmar Rain"]
    df["Day of Year"] = df["Date"].dt.dayofyear

    df["Year class"] = pd.to_numeric(df["Year class"], errors="coerce")
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Fish Age"] = df["Year"] - df["Year class"]

    ts_columns = ["Max air temp", "Dec Rain", "Calmar Rain"]
    df = generate_time_series_features(df, cols=ts_columns, lags=[3], rolling_windows=[7])

    return df

# === Preprocessing Pipeline ===
def create_spring_temp_pipeline():
    numerical_features = [
        "Max air temp", "Min air temp", "Dec Rain", "Calmar Rain",
        "Max Air Temp x Rain", "Total Rain", 
    ]

    categorical_features = ["Season"]

    num_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    cat_transformer = Pipeline([
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer([
        ("num", num_transformer, numerical_features),
        ("cat", cat_transformer, categorical_features)
    ])

    return Pipeline([("preprocessor", preprocessor)])

def split_spring_temp_data(df, ratios):
    df = df.sample(frac=1, random_state=42)

    features = [
        "Max air temp", "Min air temp", "Dec Rain", "Calmar Rain", "Season",
        "Max Air Temp x Rain", "Total Rain",
    ]

    df = df.dropna(subset=features + ["Spring Temp (F)"])

    X = df[features]
    y = df["Spring Temp (F)"]

    dev_ratio, test_ratio = ratios
    total_len = len(X)
    dev_size = int(dev_ratio * total_len)
    test_size = int(test_ratio * total_len)

    X_train = X[:-(dev_size + test_size)]
    y_train = y[:-(dev_size + test_size)]

    X_dev = X[-(dev_size + test_size):-test_size]
    y_dev = y[-(dev_size + test_size):-test_size]

    X_test = X[-test_size:]
    y_test = y[-test_size:]

    return X_train, X_dev, X_test, y_train, y_dev, y_test

# === Convenience Loader ===
def prepare_spring_temp_data(ratios=(0.1, 0.1)):
    df = load_spring_temp_data()
    return split_spring_temp_data(df, ratios)