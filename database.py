from sqlalchemy import create_engine

engine = create_engine("sqlite:///business_data.db")

def save_to_database(df, table_name="cleaned_data"):
    df.to_sql(table_name, engine, if_exists="replace", index=False)
