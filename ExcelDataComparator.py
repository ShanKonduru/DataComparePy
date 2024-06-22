import pandas as pd
from pandasql import sqldf
from ExcelFile import ExcelFile

class ExcelDataComparator:
    def __init__(self, source_file_path, target_file_path, sheet_name):
        self.source_excel = ExcelFile(source_file_path, sheet_name)
        self.target_excel = ExcelFile(target_file_path, sheet_name)
    
    def execute_sql_query(self, df, query):
        """Executes SQL query on a DataFrame using pandasql."""
        return sqldf(query, locals())
    
    def compare_excel_with_excel(self, src_query, dest_query):
        """Compares two Excel files using SQL query and returns rows that are different."""
        try:
            # Execute SQL queries on source and target Excel data
            source_data = self.execute_sql_query(self.source_excel.data, src_query)
            target_data = self.execute_sql_query(self.target_excel.data, dest_query)
            
            # Compare DataFrames
            diff_rows = pd.concat([source_data, target_data]).drop_duplicates(keep=False)
            return diff_rows
        
        except Exception as e:
            print(f"Error during comparison: {e}")
            return pd.DataFrame()  # Return an empty DataFrame or handle error as appropriate
