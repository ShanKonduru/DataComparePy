import pandas as pd
from CsvFile import CsvFile  
from CsvDataComparator import CsvDataComparator

# Example usage:
if __name__ == "__main__":
    source_file_path = r'C:/MyProjects/DataComparePy/InputFiles/CSV/Src/SrcEmpData.csv'
    target_file_path = r'C:/MyProjects/DataComparePy/InputFiles/CSV/Dest/DestEmpData.csv'
    
    # Column mapping between CSV - Source and Target 
    column_mapping = {
        "EmpID": "Emp_ID",  # Adjusted mapping to match actual column names
        "EmpName": "Emp_Name",
        "EmpAge": "Emp_Age",
        "EmpSex": "Emp_Sex",
        "EmpSalary": "Emp_Salary"
    }
    
    # Create an instance of DataComparator
    data_comparator = CsvDataComparator(source_file_path, target_file_path, column_mapping)
    
    # Compare CSV with CSV
    result_csv_csv = data_comparator.compare_csv_with_csv()
    print(result_csv_csv)
