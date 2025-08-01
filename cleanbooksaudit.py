import pandas as pd
from sqlalchemy import create_engine
import urllib
from datetime import datetime, timedelta
import os

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
    df['Book checkout'] = pd.to_datetime(df['Book checkout'], errors='coerce', dayfirst=True)
    df['Book Returned'] = pd.to_datetime(df['Book Returned'], errors='coerce', dayfirst=True)

    # Case 1: Book checkout is after Book Returned ➜ adjust Book checkout
    mask_checkout_after_return = (
        df['Book checkout'].notna() & 
        df['Book Returned'].notna() & 
        (df['Book checkout'] > df['Book Returned'])
    )
    df.loc[mask_checkout_after_return, 'Book checkout'] = (
        df.loc[mask_checkout_after_return, 'Book Returned'] - pd.Timedelta(days=14)
    )

    # Case 2: Book checkout is NaT but Book Returned is valid ➜ infer checkout as 14 days before return
    mask_checkout_missing = df['Book checkout'].isna() & df['Book Returned'].notna()
    df.loc[mask_checkout_missing, 'Book checkout'] = (
        df.loc[mask_checkout_missing, 'Book Returned'] - pd.Timedelta(days=14)
    )

    # Case 3: Book Returned is NaT but Book checkout is valid ➜ infer return as 14 days after checkout
    mask_return_missing = df['Book Returned'].isna() & df['Book checkout'].notna()
    df.loc[mask_return_missing, 'Book Returned'] = (
        df.loc[mask_return_missing, 'Book checkout'] + pd.Timedelta(days=14)
    )

    # Final: Calculate or fix Days Between
    df['Days Between'] = (df['Book Returned'] - df['Book checkout']).dt.days

    # If still null or negative (e.g., both dates were bad), set to 0
    df['Days Between'] = df['Days Between'].fillna(0)
    df.loc[df['Days Between'] < 0, 'Days Between'] = 0
    return df


def calculate_pipeline_stats(df_original, df_cleaned, file_path):
    now = datetime.now()
    one_year_window = (now - timedelta(days=365), now + timedelta(days=365))

    parsed_dates = pd.to_datetime(df_original['Book checkout'], errors='coerce')
    date_timestamps = (parsed_dates.dropna() - pd.Timestamp("1970-01-01")) // pd.Timedelta(days=1)
    Q1 = date_timestamps.quantile(0.25)
    Q3 = date_timestamps.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outlier_count = ((date_timestamps < lower_bound) | (date_timestamps > upper_bound)).sum()
    nulls_before = df_original.isnull().sum().sum()
    nulls_after = df_cleaned.isnull().sum().sum()
    nulls_removed = nulls_before - nulls_after



    stats_path = os.path.join(os.path.dirname(file_path), "pipeline_stats.csv")

    if os.path.exists(stats_path):
        stats_df = pd.read_csv(stats_path)
        run_count = stats_df['Run Count'].max() + 1
    else:
        run_count = 1

    stats_row = {
        'Run Count': run_count,
        'Time Run': now.strftime("%Y-%m-%d %H:%M:%S"),
        'Original Row Count': len(df_original),
        'Cleaned Row Count': len(df_cleaned),
        'Date IQR 1 Count': lower_bound,
        'Date IQR 4 Count': upper_bound,
        'Date Outliers (IQR)': outlier_count, 
        'Nulls in Original': nulls_before,
        'Nulls in Cleaned': nulls_after,
        'Nulls Removed': nulls_removed
    }

    new_stats_df = pd.DataFrame([stats_row])
    new_stats_df.to_csv(stats_path, mode='a', header=not os.path.exists(stats_path), index=False)
    print(f"Pipeline stats written to {stats_path}")

def process_csv(file_path):
    dtype_map = {
        "id": "int64",
        "Books": "string",
        "Days allowed to borrow": "string",
        "Customer ID": "Int64",
    }

    df_original = load_csv(file_path, dtype_map)
    df = df_original.copy()
    df = clean_quotes(df, 'Book checkout')
    df = parse_dates(df, ['Book checkout', 'Book Returned'])
    df = drop_all_na(df)
    df = fill_nans(df)
    df = fix_negative_days(df)

    calculate_pipeline_stats(df_original, df, file_path)

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
    file_path = os.path.join("data", "03_Library Systembook.csv")
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
