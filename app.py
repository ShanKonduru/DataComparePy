import pandas as pd
from sqlalchemy import create_engine
import cx_Oracle  # Oracle driver
import pyodbc  # SQL Server driver

class CsvFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        
class ExcelFile:
    def __init__(self, file_path, sheet_name=0):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.data = pd.read_excel(file_path, sheet_name=sheet_name)
        
class Database:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.engine = create_engine(connection_string)
        
    def fetch_data(self, query):
        with self.engine.connect() as connection:
            return pd.read_sql(query, connection)

def map_columns(df, column_mapping):
    """Maps columns of a DataFrame based on the given column mapping dictionary."""
    return df.rename(columns=column_mapping)

def compare_dataframes(df1, df2):
    """Compares two pandas DataFrames and returns the differences."""
    return df1.compare(df2)

def compare_csv_with_database(csv_file_obj, db_obj, query, column_mapping):
    """Compares a CSV file with a database, considering column mapping."""
    csv_data = map_columns(csv_file_obj.data, column_mapping)
    db_data = map_columns(db_obj.fetch_data(query), {v: k for k, v in column_mapping.items()})
    return compare_dataframes(csv_data, db_data)

def compare_database_with_csv(db_obj, csv_file_obj, query, column_mapping):
    """Compares a database with a CSV file, considering column mapping."""
    db_data = map_columns(db_obj.fetch_data(query), column_mapping)
    csv_data = map_columns(csv_file_obj.data, {v: k for k, v in column_mapping.items()})
    return compare_dataframes(db_data, csv_data)

def compare_database_with_database(source_db_obj, target_db_obj, source_query, target_query, column_mapping):
    """Compares two databases, considering column mapping."""
    source_data = map_columns(source_db_obj.fetch_data(source_query), column_mapping)
    target_data = map_columns(target_db_obj.fetch_data(target_query), {v: k for k, v in column_mapping.items()})
    return compare_dataframes(source_data, target_data)

# Example usage:
source_csv = CsvFile('source.csv')
oracle_connection_string = 'oracle+cx_oracle://username:password@hostname:port/?service_name=service_name'
sql_server_connection_string = 'mssql+pyodbc://username:password@hostname:port/database?driver=ODBC+Driver+17+for+SQL+Server'

target_oracle_db = Database(oracle_connection_string)
target_sql_server_db = Database(sql_server_connection_string)

source_query = 'SELECT * FROM source_table'
target_query = 'SELECT * FROM target_table'

# Column mapping between CSV/Excel and Database
column_mapping = {

    "EmpID": "Emp_ID",
    "EmpName": "Emp_Name",
    "EmpAge": "Emp_Age",
    "EmpSex": "Emp_Sex",
    "EmpSalary": "Emp_Salary"
}

# Compare CSV with Oracle Database
result_csv_oracle_db = compare_csv_with_database(source_csv, target_oracle_db, target_query, column_mapping)
print(result_csv_oracle_db)

# Compare CSV with SQL Server Database
result_csv_sql_server_db = compare_csv_with_database(source_csv, target_sql_server_db, target_query, column_mapping)
print(result_csv_sql_server_db)

# Compare Oracle Database with SQL Server Database
source_oracle_db = Database(oracle_connection_string)
result_oracle_db_sql_server_db = compare_database_with_database(source_oracle_db, target_sql_server_db, source_query, target_query, column_mapping)
print(result_oracle_db_sql_server_db)
