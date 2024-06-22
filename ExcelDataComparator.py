import pandas as pd
from pandasql import sqldf
from ExcelFile import ExcelFile
import json

class ExcelDataComparator:
    def __init__(self, source_file_path, target_file_path, sheet_name):
        self.source_excel = ExcelFile(source_file_path, sheet_name)
        self.target_excel = ExcelFile(target_file_path, sheet_name)
    
    def execute_sql_query(self, df, query):
        """Executes SQL query on a DataFrame using pandasql."""
        return sqldf(query, locals())
    
    def get_query_columns(self, query):
        """Extracts column names from the SQL query."""
        select_part = query.split('FROM')[0]
        columns = select_part.replace('SELECT', '').split(',')
        columns = [col.split('as')[1].strip() if 'as' in col else col.strip() for col in columns]
        return columns
    
    def compare_excel_with_excel(self, src_query, dest_query):
        """Compares two Excel files using SQL query and returns rows that are different."""
        try:
            # Execute SQL queries on source and target Excel data
            source_data = self.execute_sql_query(self.source_excel.data, src_query)
            target_data = self.execute_sql_query(self.target_excel.data, dest_query)
            
            # Get the columns used in the SQL queries for comparison
            src_columns = self.get_query_columns(src_query)
            dest_columns = self.get_query_columns(dest_query)
            
            if set(src_columns) != set(dest_columns):
                raise ValueError("Source and Target queries do not select the same columns")
            
            # Compare DataFrames using the common columns
            merged_df = pd.merge(source_data, target_data, on=src_columns, how='outer', indicator=True)
            
            stats = {
                "src_row_count": len(source_data),
                "target_row_count": len(target_data),
                "matching_records": len(merged_df[merged_df['_merge'] == 'both']),
                "src_only_records": len(merged_df[merged_df['_merge'] == 'left_only']),
                "target_only_records": len(merged_df[merged_df['_merge'] == 'right_only'])
            }
            
            return merged_df, stats
        
        except Exception as e:
            print(f"Error during comparison: {e}")
            return pd.DataFrame(), {}  # Return an empty DataFrame and empty stats or handle error as appropriate
    
    def generate_html_report(self, merged_df, stats, dataset_id):
        """Generates an HTML report based on the comparison results and statistics."""
        html = f"""
        <html>
        <head>
            <title>Comparison Report - {dataset_id}</title>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .header {{ font-size: 24px; margin-bottom: 20px; }}
                .section {{ margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="header">Comparison Report - {dataset_id}</div>
            <div class="section">
                <h2>Summary</h2>
                <table>
                    <tr><th>Source File Rows</th><td>{stats['src_row_count']}</td></tr>
                    <tr><th>Target File Rows</th><td>{stats['target_row_count']}</td></tr>
                    <tr><th>Matching Records</th><td>{stats['matching_records']}</td></tr>
                    <tr><th>Source Only Records</th><td>{stats['src_only_records']}</td></tr>
                    <tr><th>Target Only Records</th><td>{stats['target_only_records']}</td></tr>
                </table>
            </div>
            <div class="section">
                <h2>Detailed Differences</h2>
                {merged_df.to_html(index=False)}
            </div>
        </body>
        </html>
        """
        return html
