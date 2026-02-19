import pandas as pd


def load_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    return pd.read_excel(file)


def validate_data(df):
    """Basic data validation rules"""
    issues = []

    if df.empty:
        issues.append("Dataset is empty")

    if df.isnull().all().any():
        issues.append("Some columns contain all null values")

    if df.duplicated().sum() > 0:
        issues.append(f"{df.duplicated().sum()} duplicate rows found")

    return issues


def clean_data(df):
    """Advanced data cleaning"""

    original_rows = len(df)
    original_columns = len(df.columns)

    # Drop columns with >40% null values
    threshold = 0.4 * len(df)
    df = df.dropna(axis=1, thresh=len(df) - threshold)

    # Remove duplicates
    df = df.drop_duplicates()

    # Fill missing values
    for column in df.columns:

        if df[column].dtype in ["int64", "float64"]:

            if abs(df[column].skew()) > 1:
                df[column] = df[column].fillna(df[column].median())
            else:
                df[column] = df[column].fillna(df[column].mean())

        else:
            if not df[column].mode().empty:
                df[column] = df[column].fillna(df[column].mode()[0])

    cleaned_rows = len(df)
    cleaned_columns = len(df.columns)

    return df, original_rows, cleaned_rows, original_columns, cleaned_columns


def generate_summary(df):
    return {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": df.isnull().sum().to_dict(),
        "Data Types": df.dtypes.astype(str).to_dict(),
    }
