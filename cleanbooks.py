import pandas as pd
import os
from sqlalchemy import create_engine
import urllib



def process_csv(file_path):
    dtype_map = {
        "id": "int64",
        "Books": "string",
        "Days allowed to borrow": "string",
        "Customer ID": "Int64",
    }

    # Read raw, no parsing yet
    df = pd.read_csv(file_path, dtype=dtype_map, dayfirst=True)

    # Clean quotes from 'Book checkout' before parsing it as a date
    if 'Book checkout' in df.columns:
        df['Book checkout'] = df['Book checkout'].astype(str).str.replace('"', '').str.replace("'", '')

    # Now parse date columns safely
    df['Book checkout'] = pd.to_datetime(df['Book checkout'], errors='coerce', dayfirst=True)
    df['Book Returned'] = pd.to_datetime(df['Book Returned'], errors='coerce', dayfirst=True)

    df.dropna(how='all', inplace=True)

    # Fill NaNs sensibly
    df.fillna({
        **{col: -1 for col in df.select_dtypes(include='number').columns},
        **{col: 'Unknown' for col in df.select_dtypes(include=['object', 'string']).columns},
        **{col: pd.NaT for col in df.select_dtypes(include='datetime').columns}
    }, inplace=True)

    # Compute days between
    df['Days Between'] = (df['Book Returned'] - df['Book checkout']).dt.days
    df.loc[df['Days Between'] < 0, 'Book Returned'] = df.loc[df['Days Between'] < 0, 'Book checkout']
    df['Days Between'] = (df['Book Returned'] - df['Book checkout']).dt.days

    return df

def write_to_sql(df, table_name, server, database, username, password, if_exists='replace'):
    import urllib
    from sqlalchemy import create_engine

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

if __name__ == "__main__":
    write_to_sql(
            df=cleaned_df,
            table_name='LibraryBooks',
            server='localhost',
            database='LibraryDB',
            username='me',
            password='Password',
            if_exists='replace'
        )