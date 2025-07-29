import pandas as pd
from sqlalchemy import create_engine
import urllib

def load_csv(file_path, dtype_map):
    return pd.read_csv(file_path, dtype=dtype_map, dayfirst=True)

def clean_quotes(df, column):
    if column in df.columns:
        df[column] = df[column].astype(str).str.replace('"', '').str.replace("'", '')
    return df

def parse_dates(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
    return df

def drop_all_na(df):
    return df.dropna(how='all')

def fill_nans(df):
    df.fillna({
        **{col: -1 for col in df.select_dtypes(include='number').columns},
        **{col: 'Unknown' for col in df.select_dtypes(include=['object', 'string']).columns},
        **{col: pd.NaT for col in df.select_dtypes(include='datetime').columns}
    }, inplace=True)
    return df

def fix_negative_days(df):
    df['Days Between'] = (df['Book Returned'] - df['Book checkout']).dt.days

    mask = (df['Days Between'] < 0) & df['Book checkout'].notna() & df['Book Returned'].notna()
    df.loc[mask, 'Book Returned'] = df.loc[mask, 'Book checkout']

    df['Days Between'] = (df['Book Returned'] - df['Book checkout']).dt.days

    df['Days Between'] = df['Days Between'].fillna(-1)

    return df

def process_csv(file_path):
    dtype_map = {
        "id": "int64",
        "Books": "string",
        "Days allowed to borrow": "string",
        "Customer ID": "Int64",
    }

    df = load_csv(file_path, dtype_map)
    df = clean_quotes(df, 'Book checkout')
    df = parse_dates(df, ['Book checkout', 'Book Returned'])
    df = drop_all_na(df)
    df = fill_nans(df)
    df = fix_negative_days(df)

    return df

def write_to_sql(df, table_name, server, database, username, password, if_exists='replace'):
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
    )
    connection_uri = "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus(connection_string)
    engine = create_engine(connection_uri)

    df.to_sql(table_name, engine, if_exists=if_exists, index=False)
    print(f"Data written to {table_name} table in {database} on {server}")

if __name__ == "__main__":
    file_path = r"C:\Users\Admin\Desktop\QADEL5\data\03_Library Systembook.csv"
    cleaned_df = process_csv(file_path)
    print(cleaned_df)

    write_to_sql(
        df=cleaned_df,
        table_name='LibraryBooks',
        server='localhost',
        database='LibraryDB',
        username='me',
        password='Password',
        if_exists='replace'
    )
