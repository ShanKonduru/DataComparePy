import pandas as pd
from CsvFile import CsvFile

class CsvDataComparator:
    def __init__(self, source_file_path, target_file_path, column_mapping):
        self.source_csv = CsvFile(source_file_path)
        self.target_csv = CsvFile(target_file_path)
        self.column_mapping = column_mapping
    
    def map_columns(self, df, column_mapping):
        """Maps columns of a DataFrame based on the given column mapping dictionary."""
        mapped_columns = {}
        for source_col, target_col in column_mapping.items():
            if source_col in df.columns:
                mapped_columns[target_col] = df[source_col]
            else:
                mapped_columns[target_col] = pd.Series(dtype=str)  # Create empty Series if column not found
        return pd.DataFrame(mapped_columns)
    
    def compare_dataframes(self, df1, df2, on_columns):
        """Compares two pandas DataFrames and returns the rows that are different."""
        try:
            # Ensure all columns in on_columns exist in both DataFrames
            for col in on_columns:
                if col not in df1.columns:
                    df1[col] = pd.Series(dtype=str)  # Add empty series if column not found
                if col not in df2.columns:
                    df2[col] = pd.Series(dtype=str)  # Add empty series if column not found
            
            # Merge DataFrames
            merged_df = pd.merge(df1, df2, on=on_columns, how='outer', suffixes=('_src', '_tgt'), indicator=True)
            
            # Filter rows where the indicator column (_merge) is not 'both'
            diff_rows = merged_df[merged_df['_merge'] != 'both'].drop(columns=['_merge'])
            
            # Filter rows where all mapped columns have identical values
            diff_rows_filtered = diff_rows[
                ~diff_rows.apply(lambda row: all(row[f'{col}_src'] == row[f'{col}_tgt'] for col in on_columns), axis=1)
            ]
            
            return diff_rows_filtered
        
        except KeyError as e:
            print(f"Error during merge operation: {e}")
            return pd.DataFrame()  # Return an empty DataFrame or handle error as appropriate
    
    def compare_csv_with_csv(self):
        """Compares two CSV files, considering column mapping, and returns rows that are different."""
        try:
            # Ensure column mapping reflects the actual column names in both DataFrames
            source_data = self.source_csv.data
            target_data = self.target_csv.data
            
            source_data_mapped = self.map_columns(source_data, self.column_mapping)
            target_data_mapped = self.map_columns(target_data, {v: k for k, v in self.column_mapping.items()})
        except KeyError as e:
            print(f"Error: {e}")
            return pd.DataFrame()  # Return an empty DataFrame or handle error appropriately
        
        # Compare DataFrames based on mapped columns
        on_columns = list(self.column_mapping.values())
        
        try:
            result = self.compare_dataframes(source_data_mapped, target_data_mapped, on_columns)
        except KeyError as e:
            print(f"Error during comparison: {e}")
            return pd.DataFrame()  # Return an empty DataFrame or handle error appropriately
        
        return result
