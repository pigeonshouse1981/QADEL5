
import pandas as pd
import os

def process_csv(file_path):

    dtype_map= {
        "Customer ID": "Int64",
        "Customer Name": "string"
    }


    # Read the CSV file, enforce 'books' as string
    df = pd.read_csv(file_path, dtype=dtype_map, dayfirst=True) 
    df.dropna(how='all',inplace=True)
    df.fillna({
    **{col: -1 for col in df.select_dtypes(include='number').columns},
    **{col: 'Unknown' for col in df.select_dtypes(include=['object', 'string']).columns},
    **{col: pd.NaT for col in df.select_dtypes(include='datetime').columns}
    }, inplace=True)
    # Remove quotation marks from 'book_checkout' column if it exists


    return df


if __name__ == "__main__":
    file_path = r"C:\Users\Admin\Desktop\QADEL5\data\03_Library SystemCustomers.csv"
    cleaned_df = process_csv(file_path)
    print(cleaned_df)  # Show first few rows of cleaned data




from sqlalchemy import create_engine
import urllib

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
    # Ensure 'df' is your cleaned DataFrame variable
    write_to_sql(
        df=cleaned_df,
        table_name='LibraryUsers',
        server='localhost',
        database='LibraryDB',
        username='me',
        password='Password',
        if_exists='replace'
    )
