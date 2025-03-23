import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.impute import KNNImputer

def load_fish_data():
    """
    Loads fish data from a specified local Excel file

    Returns:
    pd.DataFrame: DataFrame containing the fish data.
    """
    # Determine file type and read accordingly
    
    df = pd.read_excel("../Data/Raw/Main_Data_edited.xlsx")  # Specify the sheet


    return df


def create_fish_pipeline():
    """
    Creates a preprocessing pipeline for fish hatchery data.
    """
    numerical_features = [
        "Spring Temp (F)", "Max air temp",
        "Min air temp", "Dec Rain", "Calmar Rain", "# fish", "Fish Alive"
    ]

    morts_feature = ["Morts"]  # Handle separately


    transparency_features = ["AM Transparency", "PM Transparency"]
    categorical_features = ["Strain", "Lot", "Raceway", "AM Feed", "PM Feed"]

    # Numeric transformer
    num_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    # Morts transformer (fill with 0)
    morts_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="constant", fill_value=0)),
        ("scaler", StandardScaler())
    ])

    # KNN imputation for transparency columns
    transparency_transformer = Pipeline(steps=[
        ("imputer", KNNImputer(n_neighbors=5))
    ])

    # Categorical transformer
    cat_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ("morts", morts_transformer, morts_feature),
        ("num", num_transformer, numerical_features),
        ("transparency", transparency_transformer, transparency_features),
        ("cat", cat_transformer, categorical_features),
    ])

    # Final pipeline
    pipeline = Pipeline(steps=[("preprocessor", preprocessor)])

    return pipeline


def split_fish_data(df, ratios):
    """
    Splits fish data into training, dev, and test sets.
    """
    df = df.sample(frac=1, random_state=42)

    selected_features = ["Date", "Month","Day", "Year", "AM Feed", "AM Transparency", "PM Feed", "PM Transparency", "Spring Temp (F)", "Morts", "# fish", "Dec Rain", "Max air temp", "Min air temp", "Calmar Rain", "Strain", "Lot", "Sub Lot", "Raceway", "Fish Alive", "Fish survival rate"]

    X = df[selected_features]
    y = df["Fish survival rate"]

    dev_ratio, test_ratio = ratios
    dev_size = int(dev_ratio * len(X))
    test_size = int(test_ratio * len(X))

    X_train = X[:-(dev_size + test_size)]
    y_train = y[:-(dev_size + test_size)]

    X_dev = X[-(dev_size + test_size):-test_size]
    y_dev = y[-(dev_size + test_size):-test_size]

    X_test = X[-test_size:]
    y_test = y[-test_size:]

    return X_train, X_dev, X_test, y_train, y_dev, y_test

def prepare_fish_data(ratios):
    fish_data = load_fish_data()
    return split_fish_data(fish_data, ratios)