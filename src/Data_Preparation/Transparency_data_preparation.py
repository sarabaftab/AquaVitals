import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.impute import KNNImputer
from timeseries_utils import generate_time_series_features
from sentence_transformers import SentenceTransformer



def load_transparency__data():
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

    # ✅ Drop rows where either AM or PM Transparency is missing
    df = df.dropna(subset=["AM Transparency", "PM Transparency"])

    # Feed imputation (categorical)
    df["AM Feed"] = df["AM Feed"].fillna("X")
    df["PM Feed"] = df["PM Feed"].fillna("X")

    # Feature engineering
    df["Season"] = df["Month"].apply(get_season)
    df["Spring_Temp x Rain"] = df["Spring Temp (F)"] * (df["Dec Rain"] + df["Calmar Rain"])
    df["Max Air Temp x Rain"] = df["Max air temp"] * (df["Dec Rain"] + df["Calmar Rain"])
    df["Total Rain"] = df["Dec Rain"] + df["Calmar Rain"]
    df["Day of Year"] = df["Date"].dt.dayofyear

    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
  

    ts_columns = ["Dec Rain", "Calmar Rain"]
    df = generate_time_series_features(df, cols=ts_columns, lags=[3,2,1], rolling_windows=[7])

    # ✅ Simulate natural language weather comment
    def generate_weather_comment(row):
        rain = row.get("Total Rain", 0)
        temp = row.get("Spring Temp (F)", 0)

        if rain > 0.5:
            return "Heavy rain affected the tanks today."
        elif rain > 0.2:
            return "Moderate rain was observed today."
        elif rain > 0:
            return "Light rain occurred earlier in the day."
        elif temp > 65:
            return "It was a warm and dry day."
        else:
            return "The day was calm with no rainfall."

    df["Weather_Comment"] = df.apply(generate_weather_comment, axis=1)

    # ✅ NLP Embedding for weather-style comments
    model = SentenceTransformer('all-MiniLM-L6-v2')
    df["comment_embedding"] = df["Weather_Comment"].apply(lambda x: model.encode(str(x)))

    # Split embedding into multiple columns
    embedding_df = pd.DataFrame(df["comment_embedding"].tolist(), index=df.index)
    embedding_df.columns = [f"text_emb_{i}" for i in range(embedding_df.shape[1])]

    # Add embeddings to main dataframe
    df = pd.concat([df.drop(columns=["comment_embedding"]), embedding_df], axis=1)

    return df

# === Preprocessing Pipeline ===
def create_transparency_pipeline():
    numerical_features = [
        # Core features
        "Spring Temp (F)", "Max air temp", "Min air temp",
        "Dec Rain", "Calmar Rain",
        "Spring_Temp x Rain", "Max Air Temp x Rain", "Total Rain",

        # Lag features (match actual naming style)
        "Dec Rain (Lag 1)", "Calmar Rain (Lag 1)",
        "Dec Rain (Lag 2)", "Calmar Rain (Lag 2)",
        "Dec Rain (Lag 3)", "Calmar Rain (Lag 3)",

        # Rolling features
        "Dec Rain 7-day avg", "Calmar Rain 7-day avg"
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

def split_transparency_data(df, target_col, ratios):
    """
    Splits fish data into training, dev, and test sets.
    Assumes engineered features like 'Season', 'Temp x Rain' already exist in the DataFrame.
    """
    df = df.sample(frac=1, random_state=42)

    features = [
        "Spring Temp (F)", "# fish", "Dec Rain", "Max air temp", "Min air temp", "Calmar Rain",
        "Season", "Spring_Temp x Rain", "Max Air Temp x Rain", "Total Rain",
        # Lag features
        "Dec Rain (Lag 3)", 
        "Calmar Rain (Lag 3)", 
        "Dec Rain (Lag 2)", 
        "Calmar Rain (Lag 2)", 
        "Dec Rain (Lag 1)", 
        "Calmar Rain (Lag 1)", 
        # Rolling averages
        "Dec Rain 7-day avg", "Calmar Rain 7-day avg"
    ]

      # NLP embedding features
    text_features = [col for col in df.columns if col.startswith("text_emb_")]

        # Final full feature list
    features = features + text_features

    df = df.dropna(subset=features + [target_col])

    X = df[features]
    y = df[target_col]

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

# === Convenience Loaders ===
def prepare_am_transparency_data(ratios=(0.1, 0.1)):
    df = load_transparency__data()
    return split_transparency_data(df, target_col="AM Transparency", ratios=ratios)

def prepare_pm_transparency_data(ratios=(0.1, 0.1)):
    df = load_transparency__data()
    return split_transparency_data(df, target_col="PM Transparency", ratios=ratios)